import json
import asyncio
import time
from vkbottle.dispatch.rules.base import CommandRule
from vkbottle.bot import Bot, Message
from sett import token
from typing import Tuple #Нада
from vkbottle import VKAPIError

bot = Bot(token=token) # Свой токен
symbols = ["!"] # С чего начинается команда

def read_file(path: str):
   with open ( path, 'r' ) as f:
      data: dict = json.load ( f )
   return data

def write_file(path: str, data: dict):
   with open ( path , 'w'  ) as f:
      json.dump ( data , f, ensure_ascii=False, indent=4 )

@bot.on.private_message(CommandRule("вопрос добавить", symbols, 1,sep=str(time.time())))
async def add_quiz(message: Message, args: Tuple[str]):
   try:
      item = args[0]
      data = read_file( 'data.json' )
      # Проверка на совпадение
      for index,each in enumerate( list( data.values() ) ):
         if item in each['question']:
            await message.answer(f"Данный вопрос уже есть базе данных под id {index+1}")
            return
      # Проверяем целосность ID, что бы если удалили один, то он заменился добавленным
      arr = list(data.keys())
      last_key = 0
      for i in arr:
         if int(i) > last_key: last_key = int(i)
      ID = False
      for key in range(1,last_key+1):
         if str(key) not in arr:
            ID = key
            break
      if not ID:
         ID = len(data)+1
      # Добавляем в БД новый вопрос
      data.update ( { ID: { "question": item , "answer": None } } )
      write_file( 'data.json',data )
      await message.answer(f"Вопрос добавлен в базу данных под id {ID}")
   except VKAPIError as e:
      print ( "Возникла ошибка [1]" , e.code )

@bot.on.private_message(CommandRule("вопрос удалить", symbols, 1,sep=str(time.time())))
async def remove_quiz(message: Message, args: Tuple[str]):
   try:
      id = args[0]
      data = read_file( 'data.json' )
      # Проверка на id
      if id not in data:
         await message.answer(f"Вопроса с данным id в базе данных не найдено")
         return
      del data[id]
      write_file ( 'data.json' , data )
      await message.answer(f"Вопрос с данным id был успешно удален")
   except VKAPIError as e:
      print ( "Возникла ошибка [2]" , e.code )

@bot.on.private_message(CommandRule("вопрос показать", symbols, 1,sep=str(time.time())))
async def show_quiz(message: Message, args: Tuple[str]):
   try:
      id = args [ 0 ]
      data = read_file( 'data.json' )
      # Проверка на id
      if id not in data:
         await message.answer(f"Вопроса с данным id в базе данных не найдено")
         return
      info = data[id]
      await message.answer(f"Вопрос: {info['question']}\n"
                           f"Ответ: {info['answer']}")
   except VKAPIError as e:
      print ( "Возникла ошибка [3]" , e.code )

@bot.on.private_message(CommandRule("ответ", symbols, 1,sep=str(time.time())))
async def show_quiz(message: Message, args: Tuple[str]):
   try:
      args = args[0]
      args = args.split(maxsplit=1)
      id, answer = args[0], args[1]
      data = read_file ( 'data.json' )
      # Проверка на id
      if id not in data:
         await message.answer(f"Вопроса с данным id в базе данных не найдено")
         return
      # Добавляем в БД новый вопрос
      data.update( { id : { "question": data[id]['question'], "answer": answer } } )
      write_file ( 'data.json' , data )
      await message.answer ( f"Ответ добавлен в базу данных под id {id}" )
   except VKAPIError as e:
      print ( "Возникла ошибка [4]" , e.code )

asyncio.run(bot.run_polling())