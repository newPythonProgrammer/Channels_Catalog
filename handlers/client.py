from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

import config
from database.client import User
from database.admin import Text
from bot import bot, dp
from keyboard import keyboard

User_db = User()
Text_db = Text()

@dp.message_handler(commands='start', state='*')
async def start(message: Message, state: FSMContext):
    await state.finish()
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    await User_db.add_user(user_id, str(username))
    await User_db.active_user(user_id)
    await message.answer(f'<b>Приветствую тебя {first_name}</b>\n\n'
                         f'Я бот - справочник полезной информации о рынке телеграм.\n\n'
                         f'Используй кнопки ниже чтобы узнать подробнее', parse_mode='HTML',
                         reply_markup=keyboard.main_menu())

@dp.message_handler(lambda message: message.text=='Цены за подписчика ₽')
async def price_sub(message: Message):
    text = await Text_db.get_text(1)
    user_id = message.from_user.id
    await User_db.active_user(user_id)
    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
    if message.from_user.id in config.ADMINS:
        await message.answer(f'ID: <code>{1}</code>', parse_mode='HTML')

@dp.message_handler(lambda message: message.text=='CPM тематик👁')
async def cpm(message: Message):
    text = await Text_db.get_text(2)
    user_id = message.from_user.id
    await User_db.active_user(user_id)
    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
    if message.from_user.id in config.ADMINS:
        await message.answer(f'ID: <code>{2}</code>', parse_mode='HTML')

@dp.message_handler(lambda message: message.text=='Термины телеграмщика👅')
async def cpm(message: Message):
    text = await Text_db.get_text(3)
    user_id = message.from_user.id
    await User_db.active_user(user_id)
    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
    if message.from_user.id in config.ADMINS:
        await message.answer(f'ID: <code>{3}</code>', parse_mode='HTML')

@dp.message_handler(lambda message: message.text=='Полезные сервисы⚙️')
async def service(message: Message):
    text = await Text_db.get_text(4)
    user_id = message.from_user.id
    await User_db.active_user(user_id)
    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
    if message.from_user.id in config.ADMINS:
        await message.answer(f'ID: <code>{4}</code>', parse_mode='HTML')

@dp.message_handler(lambda message: message.text=='Работы в телеграм🔨')
async def works(message: Message):
    text = await Text_db.get_text(5)
    user_id = message.from_user.id
    await User_db.active_user(user_id)
    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True, reply_markup=keyboard.works_menu())
    if message.from_user.id in config.ADMINS:
        await message.answer(f'ID: <code>{5}</code>', parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data=='coder')
async def coder(call: CallbackQuery):
    text = await Text_db.get_text(6)
    await call.answer()
    await call.message.edit_text(text=text, reply_markup=keyboard.back(), disable_web_page_preview=True, parse_mode='HTML')
    if call.from_user.id in config.ADMINS:
        await call.message.answer(f'ID: <code>{6}</code>', parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data=='buy')
async def buyer(call: CallbackQuery):
    text = await Text_db.get_text(7)
    await call.answer()
    await call.message.edit_text(text=text, reply_markup=keyboard.back(), disable_web_page_preview=True,
                                 parse_mode='HTML')
    if call.from_user.id in config.ADMINS:
        await call.message.answer(f'ID: <code>{7}</code>', parse_mode='HTML')

@dp.callback_query_handler(lambda call: call.data=='manager')
async def manager(call: CallbackQuery):
    text = await Text_db.get_text(8)
    await call.answer()
    await call.message.edit_text(text=text, reply_markup=keyboard.back(), disable_web_page_preview=True,
                                 parse_mode='HTML')
    if call.from_user.id in config.ADMINS:
        await call.message.answer(f'ID: <code>{8}</code>', parse_mode='HTML')

@dp.callback_query_handler(lambda call: call.data=='design')
async def design(call: CallbackQuery):
    text = await Text_db.get_text(9)
    await call.answer()
    await call.message.edit_text(text=text, reply_markup=keyboard.back(), disable_web_page_preview=True,
                                 parse_mode='HTML')
    if call.from_user.id in config.ADMINS:
        await call.message.answer(f'ID: <code>{9}</code>', parse_mode='HTML')

@dp.callback_query_handler(lambda call: call.data=='creo')
async def creo(call: CallbackQuery):
    text = await Text_db.get_text(10)
    await call.answer()
    await call.message.edit_text(text=text, reply_markup=keyboard.back(), disable_web_page_preview=True,
                                 parse_mode='HTML')
    if call.from_user.id in config.ADMINS:
        await call.message.answer(f'ID: <code>{10}</code>', parse_mode='HTML')


@dp.callback_query_handler(lambda call: call.data=='content')
async def content(call: CallbackQuery):
    text = await Text_db.get_text(11)
    await call.answer()
    await call.message.edit_text(text=text, reply_markup=keyboard.back(), disable_web_page_preview=True,
                                 parse_mode='HTML')
    if call.from_user.id in config.ADMINS:
        await call.message.answer(f'ID: <code>{11}</code>', parse_mode='HTML')

@dp.callback_query_handler(lambda call: call.data=='traffer')
async def traff(call: CallbackQuery):
    text = await Text_db.get_text(12)
    await call.answer()
    await call.message.edit_text(text=text, reply_markup=keyboard.back(), disable_web_page_preview=True,
                                 parse_mode='HTML')
    if call.from_user.id in config.ADMINS:
        await call.message.answer(f'ID: <code>{12}</code>', parse_mode='HTML')

@dp.callback_query_handler(lambda call: call.data=='works_menu')
async def back_works(call: CallbackQuery):
    await call.answer()
    text = await Text_db.get_text(5)
    await call.message.edit_text(text, parse_mode='HTML', disable_web_page_preview=True, reply_markup=keyboard.works_menu())


@dp.message_handler(lambda message: message.text=='Биржы каналов💰')
async def stock_exchange(message: Message):
    text = await Text_db.get_text(13)
    user_id = message.from_user.id
    await User_db.active_user(user_id)
    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
    if message.from_user.id in config.ADMINS:
        await message.answer(f'ID: <code>{13}</code>', parse_mode='HTML')

@dp.message_handler(lambda message: message.text=='Крутые блоги😎')
async def blog(message: Message):
    text = await Text_db.get_text(14)
    user_id = message.from_user.id
    await User_db.active_user(user_id)
    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True)
    if message.from_user.id in config.ADMINS:
        await message.answer(f'ID: <code>{14}</code>', parse_mode='HTML')

@dp.message_handler(lambda message: message.text=='Чаты рекламы💬')
async def chats(message: Message):
    text = await Text_db.get_text(15)
    user_id = message.from_user.id
    await User_db.active_user(user_id)
    await message.answer(text, parse_mode='HTML', disable_web_page_preview=True, reply_markup=keyboard.chats_btn())
    if message.from_user.id in config.ADMINS:
        await message.answer(f'ID: <code>{15}</code>', parse_mode='HTML')

@dp.callback_query_handler(lambda call: call.data.startswith('chat_'))
async def get_chats(call: CallbackQuery):
    await call.answer()
    text_id = call.data.split('_')[-1]
    text = await Text_db.get_text(text_id)
    await call.message.edit_text(text, disable_web_page_preview=True, reply_markup=keyboard.back_chat(), parse_mode='HTML')
    if call.from_user.id in config.ADMINS:
        await call.message.answer(f'ID: <code>{text_id}</code>', parse_mode='HTML')

@dp.callback_query_handler(lambda call: call.data=='menu_chat')
async def back_from_chat(call: CallbackQuery):
    text = await Text_db.get_text(15)
    await call.message.edit_text(text, parse_mode='HTML', disable_web_page_preview=True, reply_markup=keyboard.chats_btn())

@dp.message_handler()
async def html(message: Message):
    print(message.html_text)
