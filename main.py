import json
import asyncio
from vkbottle.bot import Bot, Message

bot = Bot(token="token")

def read_file(name : str):
   with open ( name, 'r' ) as f:
      data: dict = json.load ( f )
   return data

@bot.on.message(text='!вопрос добавить <item>')
async def add_quiz(message: Message, item: dict):
   data = read_file( 'data.json' )
   # Проверка на совпадение
   for index,each in enumerate( list( data.values() ) ):
      if item in each['text']:
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
   with open ( 'data.json' , 'w'  ) as f:
      json.dump ( data , f, ensure_ascii=False, indent=4 )
   await message.answer(f"Вопрос добавлен в базу данных под id {ID}")

@bot.on.message(text="!вопрос удалить <id>")
async def remove_quiz(message: Message, id: dict):
   data = read_file( 'data.json' )
   # Проверка на id
   if id not in data:
      await message.answer(f"Вопроса с данным id в базе данных не найдено")
      return
   del data[id]
   with open ( 'data.json' , 'w'  ) as f:
      json.dump ( data , f, ensure_ascii=False, indent=4 )
   await message.answer(f"Вопрос с данным id был успешно удален")

@bot.on.message(text="!вопрос показать <id>")
async def show_quiz(message: Message, id: dict):
   data = read_file( 'data.json' )
   # Проверка на id
   if id not in data:
      await message.answer(f"Вопроса с данным id в базе данных не найдено")
      return
   info = data[id]
   await message.answer(f"Вопрос: {info['question']}\n"
                        f"Ответ: {info['answer']}")

@bot.on.message(text="!ответ <id> <answer>")
async def show_quiz(message: Message, id: dict, answer: dict):
   data = read_file ( 'data.json' )
   # Проверка на id
   if id not in data:
      await message.answer(f"Вопроса с данным id в базе данных не найдено")
      return
   # Добавляем в БД новый вопрос
   data.update( { id : { "question": data[id]['question'], "answer": answer } } )
   with open ( 'data.json' , 'w'  ) as f:
      json.dump ( data , f , ensure_ascii=False , indent=4 )
   await message.answer ( f"Ответ добавлен в базу данных под id {id}" )

asyncio.run(bot.run_polling())