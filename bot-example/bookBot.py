from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from wit import Wit
access_token = "IQXRZALWN7LAYGHQZWSNKWU2GMGYPHMA"
name= "Anonymous"
updater = Updater(token='471766784:AAHJPT82C21DvW_EhZXZ9fEQdS9a94mIYs0')
dispatcher = updater.dispatcher
client = Wit(access_token = access_token)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)
updater.start_polling()
def start(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text="hello! I am book search chatbot")
	bot.send_message(chat_id=update.message.chat_id, text="May I ask a few questions to offer you a better service?")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
def controller(bot,update):
	resp = client.message(update.message.text)
	try:
		if(list(resp['entities'])[0]=="accept"):
			bot.send_message(chat_id=update.message.chat_id, text="How would you like to be called?")    
			dispatcher.remove_handler(controller_handler)
			dispatcher.remove_handler(start_handler)
		elif(list(resp['entities'])[0]=="reject"):
			bot.send_message(chat_id=update.message.chat_id, text="Ok you want to use the default version.")
			dispatcher.remove_handler(controller_handler)
			dispatcher.remove_handler(nameController_handler)
			dispatcher.remove_handler(bookController_handler)
			
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Sorry,didn't understand.")
	except:
		pass
controller_handler = MessageHandler(Filters.text, controller)
dispatcher.add_handler(controller_handler)
def nameController(bot,update):
	resp = client.message(update.message.text)
	try:
		if(list(resp['entities'])[0]=='name'):
			entity= "name"
			value=resp['entities'][entity][0]['value']
			response="Hello {},nice to meet you".format(str(value))
			global name
			name = str(value)
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Sorry,didn't understand.")
	except:
		pass
	bot.send_message(chat_id=update.message.chat_id, text=response)
	bot.send_message(chat_id=update.message.chat_id, text="What kind of books do you read most? ")
	dispatcher.remove_handler(nameController_handler)	
nameController_handler = MessageHandler(Filters.text, nameController)
dispatcher.add_handler(nameController_handler)
def bookController(bot,update):
	resp = client.message(update.message.text)
	response= None
	value=""
	try:
		if(list(resp['entities'])[0] =='booktype'):
			entity='booktype'
			if(len(resp['entities'][entity])>1):
				for i in range(0,len(resp['entities'][entity])):
					if(i!=len(resp['entities'][entity])-1):
						value+=str(resp['entities'][entity][i]['value'])+","
					else:
						value+=str(resp['entities'][entity][i]['value'])
				response="Ok.I will send you "+ str(value)+" books"
			else:
				value=resp['entities'][entity][0]['value']
				response="Ok.I will send you {} books".format(str(value))
		else:
			bot.send_message(chat_id=update.message.chat_id, text="Sorry,didn't understand.")
	except:
		pass
	bot.send_message(chat_id=update.message.chat_id, text=response)	
bookController_handler = MessageHandler(Filters.text, bookController)
dispatcher.add_handler(bookController_handler)
def stop(bot,update):
	bot.send_message(chat_id=update.message.chat_id, text="Ok.CYA LATER {}".format(str(name)))
	updater.stop()
stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)
