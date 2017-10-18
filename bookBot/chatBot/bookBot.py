from telegram.ext import Updater
import logging
from chatBot.deneme import wit_response
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
name= "Anonymous"
updater = Updater(token='463468162:AAGwj6oo_CrGeHip_Hzhh8IXHzSwQNDSwnE')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
print("started")
def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="Welcome to the Book Master")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
def echo(bot, update):
	entity,value =wit_response(update.message.text)
	response= None
	print(entity)
	if(entity =='booktype'):
		response="Ok.I will send you {} books".format(str(value))
	elif(entity=='start'):
		response="Hello {},nice to meet you".format(str(value))
		global name
		name = str(value)
	elif(entity=='thanks'):
		response="No need for a thanks"
	else:
		response="Sorry didn't understand"
	bot.send_message(chat_id=update.message.chat_id, text=response)
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)
def stop(bot,update):
	bot.send_message(chat_id=update.message.chat_id, text="Ok.CYA LATER {}".format(str(name)))
	updater.stop()
stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)