from bot import bot, dp
from database.spam import Spam
from database.client import User
from database.admin import Text
import config
from states import states
from keyboard import keyboard

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import Message, CallbackQuery, ContentType, MediaGroup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.middlewares import BaseMiddleware

import ast
from typing import List, Union
import asyncio

Spam_db = Spam()
User_db = User()
Text_db = Text()

class AlbumMiddleware(BaseMiddleware):
    """This middleware is for capturing media groups."""

    album_data: dict = {}

    def __init__(self, latency: Union[int, float] = 0.01):
        """
        You can provide custom latency to make sure
        albums are handled properly in highload.
        """
        self.latency = latency
        super().__init__()

    async def on_process_message(self, message: Message, data: dict):
        if not message.media_group_id:
            return

        try:
            self.album_data[message.media_group_id].append(message)
            raise CancelHandler()  # Tell aiogram to cancel handler for this group element
        except KeyError:
            self.album_data[message.media_group_id] = [message]
            await asyncio.sleep(self.latency)

            message.conf["is_last"] = True
            data["album"] = self.album_data[message.media_group_id]

    async def on_post_process_message(self, message: Message, result: dict, data: dict):
        """Clean up after handling our album."""
        if message.media_group_id and message.conf.get("is_last"):
            del self.album_data[message.media_group_id]


@dp.message_handler(lambda message: message.from_user.id in config.ADMINS, commands='panel')
async def show_panel(message: Message, state: FSMContext):
    stat_text = await User_db.stat_text()
    await message.answer(stat_text, reply_markup=keyboard.admin_panel())



@dp.callback_query_handler(lambda call: call.from_user.id in config.ADMINS and (call.data=='edit_text'), state='*')
async def edit_text(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer('Пришли мне ID текста')
    await states.EDIT_TEXT.text_id.set()

@dp.message_handler(state=states.EDIT_TEXT.text_id)
async def edit_text(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer('Введи ID текста')
        return
    async with state.proxy() as data:
        data['text_id'] = int(message.text)
    await message.answer('Пришли мне новый текст')
    await state.set_state(states.EDIT_TEXT.text)

@dp.message_handler(state=states.EDIT_TEXT.text)
async def edit_text(message: Message, state: FSMContext):
    async with state.proxy() as data:
        await Text_db.edit_text(data['text_id'], message.html_text)
    await message.answer('Текст изменен')
    await state.finish()


@dp.callback_query_handler(lambda call: (call.data=='spam') and (call.from_user.id  in config.ADMINS), state='*')
async def spam1(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    user_id = call.from_user.id
    if user_id in config.ADMINS:
        await call.message.answer('Пришли пост')
        await states.FSM_ADMIN_SPAM.text.set()

@dp.message_handler(state=states.FSM_ADMIN_SPAM.text, is_media_group=True, content_types=ContentType.ANY,)
async def spam2_media_group(message: Message, album: List[Message], state: FSMContext):
    """This handler will receive a complete album of any type."""
    media_group = MediaGroup()
    for obj in album:
        if obj.photo:
            file_id = obj.photo[-1].file_id
        else:
            file_id = obj[obj.content_type].file_id

        try:
            # We can also add a caption to each file by specifying `"caption": "text"`
            media_group.attach({"media": file_id, "type": obj.content_type, "caption": obj.caption,
                                "caption_entities": obj.caption_entities})
        except ValueError:
            return await message.answer("This type of album is not supported by aiogram.")
    media_group = ast.literal_eval(str(media_group))
    async with state.proxy() as data:
        try:
            data['text'] = media_group[0]['caption']
        except:
            data['text'] = 'None'
        data['media'] = media_group
        await Spam_db.add_spam(data['text'], 'None', str(media_group))
    last_id = await Spam_db.select_last_id()
    await message.answer_media_group(media_group)
    await message.answer(f'Пришли команду /sendspam_{last_id} чтоб начать рассылку')
    await state.finish()

@dp.message_handler(state=states.FSM_ADMIN_SPAM.text, content_types=['photo', 'video', 'animation', 'text'])
async def spam2(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        if message.content_type in ('photo', 'video', 'animation'):
            async with state.proxy() as data:
                try:
                    data['text'] = message.html_text
                except:
                    data['text'] = None
                if message.content_type == 'photo':
                    data['media'] = ('photo', message.photo[-1].file_id)
                else:
                    data['media'] = (message.content_type, message[message.content_type].file_id)
        else:
            async with state.proxy() as data:
                data['text'] = message.html_text
                data['media'] = 'None'
        await message.answer('Теперь пришли кнопки например\n'
                             'text - url1\n'
                             'text2 - url2 && text3 - url3\n\n'
                             'text - надпись кнопки url - ссылка'
                             '"-" - разделитель\n'
                             '"&&" - склеить в строку\n'
                             'ЕСЛИ НЕ НУЖНЫ КНОПКИ ОТПРАВЬ 0')
        await states.FSM_ADMIN_SPAM.next()

@dp.message_handler(state=states.FSM_ADMIN_SPAM.btns)
async def spam3(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        if message.text != '0':
            # конструктор кнопок
            try:
                buttons = []
                for char in message.text.split('\n'):
                    if '&&' in char:
                        tmpl = []
                        for i in char.split('&&'):
                            tmpl.append(dict([i.split('-', maxsplit=1)]))
                        buttons.append(tmpl)
                    else:
                        buttons.append(dict([char.split('-', maxsplit=1)]))
                menu = InlineKeyboardMarkup()
                btns_list = []
                items = []
                for row in buttons:
                    if type(row) == dict:
                        url1 = str(list(row.items())[0][1]).strip()
                        text1 = list(row.items())[0][0]
                        menu.add(InlineKeyboardButton(text=text1, url=url1))
                    else:
                        items.clear()
                        btns_list.clear()
                        for d in row:
                            items.append(list(d.items())[0])
                        for text, url in items:
                            url = url.strip()
                            btns_list.append(InlineKeyboardButton(text=text, url=url))
                        menu.add(*btns_list)
                ###########$##############
                async with state.proxy() as data:
                    data['btns'] = str(menu)
                    media = data['media']
                    text = data['text']
                    await Spam_db.add_spam(text, str(menu), str(media))

                    if media != 'None':
                        content_type = media[0]
                        if content_type == 'photo':
                            await message.bot.send_photo(user_id, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=menu)
                        elif content_type == 'video':
                            await message.bot.send_video(user_id, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=menu)
                        elif content_type == 'animation':
                            await message.bot.send_animation(user_id, media[1], caption=text, parse_mode='HTML',
                                                             reply_markup=menu)
                    else:
                        await message.answer(text, reply_markup=menu, parse_mode='HTML', disable_web_page_preview=True)

            except Exception as e:
                await message.reply(f'Похоже что непрвильно введена клавиатура')
        else:
            async with state.proxy() as data:
                data['btns'] = 'None'
                media = data['media']
                text = data['text']
                await Spam_db.add_spam(text, 'None', str(media))


                if media != 'None':
                    content_type = media[0]
                    if content_type == 'photo':
                        await message.bot.send_photo(user_id, media[1], caption=text, parse_mode='HTML')
                    elif content_type == 'video':
                        await message.bot.send_video(user_id, media[1], caption=text, parse_mode='HTML')
                    elif content_type == 'animation':
                        await message.bot.send_animation(user_id, media[1], caption=text, parse_mode='HTML')
                else:
                    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
        last_id = await Spam_db.select_last_id()
        await message.answer(f'Пришли команду /sendspam_{last_id} чтоб начать рассылку')
        await state.finish()

@dp.message_handler(lambda message: (message.from_user.id in config.ADMINS) and (message.text.startswith('/sendspam')))
async def start_spam(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    if user_id in config.ADMINS:
        spam_id = int(message.text.replace('/sendspam_', ''))
        text = await Spam_db.select_text(spam_id)
        keyboard = await Spam_db.select_keyboard(spam_id)
        media = await Spam_db.select_media(spam_id)
        if text == 'None':
            text = None
        if keyboard == 'None':
            keyboard = None
        all_user = await User_db.get_all_user()
        await message.answer(f'Считанно {len(all_user)} пользователей запускаю рассылку')
        no_send = 0
        send = 0
        for user in all_user:
            user = int(user)
            try:
                if media != 'None' and media != None:  # Есть медиа
                    if type(media) is list:
                        await message.bot.send_media_group(user, media)
                    else:
                        content_type = media[0]

                        if content_type == 'photo':
                            await message.bot.send_photo(user, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=keyboard)
                        elif content_type == 'video':
                            await message.bot.send_video(user, media[1], caption=text, parse_mode='HTML',
                                                         reply_markup=keyboard)
                        elif content_type == 'animation':
                            await message.bot.send_animation(user, media[1], caption=text, parse_mode='HTML',
                                                             reply_markup=keyboard)

                else:  # Нету медиа
                    if keyboard != 'None' and keyboard != None:  # Есть кнопки
                        await message.bot.send_message(chat_id=user, text=text, reply_markup=keyboard,
                                                       parse_mode='HTML', disable_web_page_preview=True)
                    else:
                        await message.bot.send_message(chat_id=user, text=text, parse_mode='HTML',
                                                       disable_web_page_preview=True)
                send += 1
                await User_db.active_user(user)

            except:
                no_send += 1
                await User_db.disactive_user(user)
        await message.answer(f'Рассылка окончена.\n'
                             f'Отправленно: {send} пользователям\n'
                             f'Не отправленно: {no_send} пользователям')


dp.middleware.setup(AlbumMiddleware())