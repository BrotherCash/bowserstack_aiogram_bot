from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from config import TOKEN, ADMINS, ON_BUTTON, OFF_BUTTON  # import config

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

busy = False
user = {
    'id': '',
    'first_name': '',
    'last_name': '',
    'username': ''
}

bs_on = KeyboardButton(ON_BUTTON)
bs_off = KeyboardButton(OFF_BUTTON)

bs_markup = ReplyKeyboardMarkup(resize_keyboard=True).row(
    bs_on, bs_off
)


# function to set up current user name and ID
def set_user_name(message):
    global user

    user['id'] = message.from_user.id
    if message.from_user.first_name is not None:
        user['first_name'] = message.from_user.first_name
    else:
        user['first_name'] = ''

    if message.from_user.last_name is not None:
        user['last_name'] = message.from_user.last_name
    else:
        user['last_name'] = ''

    if message.from_user.username is not None:
        user['username'] = '(@' + message.from_user.username + ')'
    else:
        user['username'] = ''


# START command handler
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    set_user_name(message)

    await message.answer(f'''Бот запущен для пользователя 
{user['first_name']} {user['last_name']} {user['username']}''', reply_markup=bs_markup)


# HELP command handler
@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Бот фиксирует состояние онлайн сервиса BrowserStack.")


# message handler
@dp.message_handler()
async def echo(message: types.Message):
    global busy
    global user

    # TURN ON and NOT BUSY
    if (message.text == ON_BUTTON and busy is not True):
        set_user_name(message)
        await message.answer(f"""👍  Работа с BrowserStack НАЧАТА.

Пользователь - {user['first_name']} {user['last_name']} {user['username']}
〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️""")

        busy = True

    # TURN ON and BUSY
    elif (message.text == ON_BUTTON and busy is True):
        await message.answer(f"""🚫  Вы не можете воспользоваться сервисом BrowserStack. 

В даный момент он используется пользователем 
{user['first_name']} {user['last_name']} {user['username']} 
〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️""")

    # TURN OFF and NOT BUSY
    elif (message.text == OFF_BUTTON and busy is not True):
        await message.answer("""🟢   Сервис BrowserStack в данный момент свободен.
〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️""")

    # TURN OFF
    elif (message.text == OFF_BUTTON):

        # right user, ok to turn off
        if (message.from_user.id == user['id']):
            await message.answer(f"""🆗  Работа с BrowserStack ЗАКОНЧЕНА.

Пользователь - {user['first_name']} {user['last_name']} {user['username']}
〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️""")

            busy = False

        # wrong user, unable to turn off
        else:
            await message.answer(f"""🚫  🚫Вы не можете завершить работу
с сервисом BrowserStack.

В даный момент он используется пользователем 
{user['first_name']} {user['last_name']} {user['username']} 
〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️〰️""")

    # any other message
    else:
        # only those who are in ADMINS group are allowed to post messages
        if (message.from_user.id not in ADMINS):
            await bot.delete_message(message.chat.id, message.message_id)
            await message.answer('Для использования бота воспользуйтсь кнопками внизу', reply_markup=bs_markup)


if __name__ == '__main__':
    executor.start_polling(dp)
