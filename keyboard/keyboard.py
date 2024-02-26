from aiogram.types import KeyboardButton, InlineKeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup


def admin_panel():
    menu = InlineKeyboardMarkup(row_width=1)
    btn1 = InlineKeyboardButton(text='Рассылка по всем юзерам',callback_data='spam')
    btn2 = InlineKeyboardButton(text='Изменить текст', callback_data='edit_text')
    menu.add(btn1, btn2)
    return menu

def main_menu():
    menu = ReplyKeyboardMarkup()
    btn1 = KeyboardButton(text='Цены за подписчика ₽')
    btn2 = KeyboardButton(text='CPM тематик👁')
    btn3 = KeyboardButton(text='Термины телеграмщика👅')
    btn4 = KeyboardButton(text='Полезные сервисы⚙️')
    btn5 = KeyboardButton(text='Чаты рекламы💬')
    btn6 = KeyboardButton(text='Биржы каналов💰')
    btn7 = KeyboardButton(text='Работы в телеграм🔨')
    btn8 = KeyboardButton(text='Крутые блоги😎')
    menu.add(btn1, btn2)
    menu.add(btn3, btn4)
    menu.add(btn7)
    menu.add(btn5, btn6)
    menu.add(btn8)
    return menu

def works_menu():
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text='Кодер👨‍💻', callback_data='coder')
    btn2 = InlineKeyboardButton(text='Закупщик💰', callback_data='buy')
    btn3 = InlineKeyboardButton(text='Менеджер🤵‍♂️', callback_data='manager')
    btn4 = InlineKeyboardButton(text='Дизайнер👨‍🎨', callback_data='design')
    btn5 = InlineKeyboardButton(text='Креативщик💬', callback_data='creo')
    btn6 = InlineKeyboardButton(text='Контенщик🧠', callback_data='content')
    btn7 = InlineKeyboardButton(text='Трафферы👥', callback_data='traffer')
    menu.add(btn1, btn2)
    menu.add(btn3, btn4)
    menu.add(btn5, btn6)
    menu.add(btn7)
    return menu

def chats_btn():
    menu = InlineKeyboardMarkup(row_width=2)
    btn1 = InlineKeyboardButton(text='ЖЦА', callback_data='chat_16')
    btn2 = InlineKeyboardButton(text='МЦА', callback_data='chat_17')
    btn3 = InlineKeyboardButton(text='Новости', callback_data='chat_18')
    btn4 = InlineKeyboardButton(text='Кулинария', callback_data='chat_19')
    btn5 = InlineKeyboardButton(text='Здоровье', callback_data='chat_20')
    btn6 = InlineKeyboardButton(text='Лингвистика', callback_data='chat_21')
    btn7 = InlineKeyboardButton(text='Психология', callback_data='chat_22')
    btn8 = InlineKeyboardButton(text='Познавалки', callback_data='chat_23')
    btn9 = InlineKeyboardButton(text='История', callback_data='chat_24')
    btn10 = InlineKeyboardButton(text='Бизнес|Финансы', callback_data='chat_25')
    btn12 = InlineKeyboardButton(text='Медицина', callback_data='chat_26')
    btn13 = InlineKeyboardButton(text='Криптовалюты', callback_data='chat_27')
    btn14 = InlineKeyboardButton(text='Сохры', callback_data='chat_28')
    btn15 = InlineKeyboardButton(text='Дарк', callback_data='chat_29')
    btn16 = InlineKeyboardButton(text='IT', callback_data='chat_30')
    btn17 = InlineKeyboardButton(text='Юмор', callback_data='chat_31')
    btn19 = InlineKeyboardButton(text='Треш', callback_data='chat_32')
    btn20 = InlineKeyboardButton(text='Аниме', callback_data='chat_33')
    btn21 = InlineKeyboardButton(text='Халява', callback_data='chat_34')
    btn22 = InlineKeyboardButton(text='Товарка', callback_data='chat_35')
    btn23 = InlineKeyboardButton(text='Кино', callback_data='chat_36')
    btn24 = InlineKeyboardButton(text='Музыка', callback_data='chat_37')
    btn25 = InlineKeyboardButton(text='Авторские', callback_data='chat_38')
    btn26 = InlineKeyboardButton(text='Игры/APK', callback_data='chat_39')
    btn29 = InlineKeyboardButton(text='Смешаные', callback_data='chat_40')
    btn30 = InlineKeyboardButton(text='Прочее', callback_data='chat_41')
    menu.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10,
             btn12, btn13, btn14, btn15, btn16, btn17,btn19, btn20, btn21, btn22, btn23, btn24,
             btn25, btn26, btn29, btn30)
    return menu


def back():
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text='🔙Назад', callback_data='works_menu')
    menu.add(btn1)
    return menu

def back_chat():
    menu = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton(text='🔙Назад', callback_data='menu_chat')
    menu.add(btn1)
    return menu

