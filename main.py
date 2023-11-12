import logging
#import os
import g4f

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message


#from background import keep_alive


#from data_storage_file import users

from config import TG_BOT_KEY, ADMIN_ID


#TG_BOT_KEY = os.environ['TG_BOT_KEY']
#ADMIN_ID = os.environ['ADMIN_ID']

bot = Bot(token=TG_BOT_KEY)
dp = Dispatcher()


@dp.message((F.from_user.id == ADMIN_ID) & (F.text == '/statistics'))
async def print_stats(message: Message):
  await message.answer(f'Список пользователей: {users}')


@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
  await message.answer(f'Привет, {message.from_user.first_name}!\n'
                       f'Я - твой нейросетевой помощник.\n'
                       f'Напиши мне что-нибудь и я постараюсь тебе ответить.')


current_provider = g4f.Provider.FakeGpt


@dp.message(F.text == 'one')
async def simple_answer(message: Message):
  await message.answer('one')


@dp.message(F.text == '/statistics')
async def statistics_answer(message: Message):
  await message.answer(str(users))


@dp.message()
async def gpt_answer(message: Message):
  user_id = message.from_user.id
  name = message.from_user.first_name
  surname = message.from_user.last_name
  fullname = message.from_user.full_name

  if user_id not in users:
    '''
    users[user_id] = {
      'name': name,
      'surname': surname,
      'login': login,
      'provider': current_provider,
      'history': [],
      'history_index': 0
    }
    '''

    users[user_id] = {'name': fullname}
    #users[user_id] = {'TG_ID': user_id, 'name': fullname}
    print(users)
    #{'name': name, 'surname': surname, 'TG_id': login}

    await bot.send_message(
        chat_id=ADMIN_ID,
        #text=f'Новый пользователь: {name} {surname} ({login})'
        text=f'Новый пользователь: {fullname} (id: {user_id})')

  msg = await message.answer("Генерирую ответ ...")
  await bot.send_chat_action(user_id, 'Печатает...')
  #await bot.send_chat_action(user_id, ChatActions.TYPING)
  try:
    #response = g4f.ChatCompletion.create_async(
    response = g4f.ChatCompletion.create(
        #model="gpt-3.5-turbo",
        model=g4f.models.default,
        provider=current_provider,

        #provider= g4f.Provider.Yqcloud,
        messages=[{
            "role": "user",
            "content": message.text
        }])
    await msg.delete()
    await message.answer(f'[{current_provider.__name__}]:\n{response}')
  except Exception as e:
    await message.answer(e)


keep_alive()
if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
dp.run_polling(bot)
