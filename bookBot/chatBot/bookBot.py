from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from wit import Wit
import json
import urllib.request
import urllib.parse
import urllib.error
class bookObj:
    def __init__(self, id, title, authors, publisher, description, pageCount, categories):
        self.id = id
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.description = description
        self.pageCount = pageCount
        self.categories = categories
bookList = []
url = 'https://www.googleapis.com/books/v1/volumes?q='
access_token = "IQXRZALWN7LAYGHQZWSNKWU2GMGYPHMA"
name = ""
controller1 = ""
updater = Updater(token='471766784:AAHJPT82C21DvW_EhZXZ9fEQdS9a94mIYs0')
dispatcher = updater.dispatcher
client = Wit(access_token=access_token)
logging.basicConfig(
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater.start_polling()


def start(bot, update):
        global name
        if(name == ""):
                bot.send_message(chat_id=update.message.chat_id,
                                 text="hello! I am book search chatbot")
                bot.send_message(chat_id=update.message.chat_id,
                                 text="May I ask a few questions to offer you a better service?")
                dispatcher.add_handler(controller_handler)
        else:
                bot.send_message(chat_id=update.message.chat_id,
                         text="Ok.What do u want to search {}".format(str(name)))
                dispatcher.remove_handler(controller_handler)
                dispatcher.remove_handler(nameController_handler)
                dispatcher.remove_handler(bookController_handler)
                dispatcher.add_handler(searchBookController_handler)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def controller(bot, update):
        resp = client.message(update.message.text)
        global name
        try:
                if (list(resp['entities'])[0] == "accept"):
                        bot.send_message(
                            chat_id=update.message.chat_id, text="How would you like to be called?")
                        dispatcher.remove_handler(controller_handler)
                        dispatcher.add_handler(nameController_handler)
                elif (list(resp['entities'])[0] == "reject"):
                        name = "Anonymous"
                        bot.send_message(
                            chat_id=update.message.chat_id, text="Ok you want to stay mysterious.I will call you Anonymous from now on.")
                        bot.send_message(chat_id=update.message.chat_id,
                         text="What do u want to search?")
                        dispatcher.remove_handler(controller_handler)
                        dispatcher.remove_handler(nameController_handler)
                        dispatcher.remove_handler(bookController_handler)
                        dispatcher.add_handler(searchBookController_handler)

                else:
                        bot.send_message(
                            chat_id=update.message.chat_id, text="Sorry,didn't understand.")
        except:
                pass
                bot.send_message(chat_id=update.message.chat_id,
                         text="Sorry,didn't understand.")


controller_handler = MessageHandler(Filters.text, controller)



def nameController(bot, update):
        resp = client.message(update.message.text)
        try:
                if (list(resp['entities'])[0] == 'name'):
                        entity = "name"
                        value = resp['entities'][entity][0]['value']
                        bot.send_message(chat_id=update.message.chat_id,
                                 text="Hello {},nice to meet you".format(str(value)))
                        global name
                        name = str(value)
                else:
                        bot.send_message(
                            chat_id=update.message.chat_id, text="Sorry,didn't understand.")
        except:
                pass
                bot.send_message(chat_id=update.message.chat_id,
                         text="Sorry,didn't understand.")
        if(name != ""):
                bot.send_message(chat_id=update.message.chat_id,
                         text="What kind of books do you read most? ")
                dispatcher.remove_handler(nameController_handler)
                dispatcher.add_handler(bookController_handler)


nameController_handler = MessageHandler(Filters.text, nameController)



def bookController(bot, update):
        resp = client.message(update.message.text)
        value = ""
        try:
                if (list(resp['entities'])[0] == 'booktype'):
                        entity = 'booktype'
                        if (len(resp['entities'][entity]) > 1):
                                for i in range(0, len(resp['entities'][entity])):
                                        if (i != len(resp['entities'][entity]) - 1):
                                                value += str(resp['entities']
                                                             [entity][i]['value']) + ","
                                        else:
                                                value += str(resp['entities']
                                                             [entity][i]['value'])
                                response = "I have saved that you like " + \
                                    str(value) + " books."
                                bot.send_message(chat_id=update.message.chat_id, text=response)
                                bot.send_message(
                            chat_id=update.message.chat_id, text='From now on, you can search books. :)')
                                dispatcher.remove_handler(bookController_handler)
                                dispatcher.add_handler(searchBookController_handler)

                        else:
                                value = resp['entities'][entity][0]['value']
                                bot.send_message(chat_id=update.message.chat_id,
                                 text="I have saved that you like " + str(value) + " books.")
                                bot.send_message(
                            chat_id=update.message.chat_id, text='From now on, you can search books. :)')
                                dispatcher.remove_handler(bookController_handler)
                                dispatcher.add_handler(searchBookController_handler)
        except:
                pass
                bot.send_message(chat_id=update.message.chat_id,
                         text="Sorry didn't understand.")


bookController_handler = MessageHandler(Filters.text, bookController)


def searchBookController(bot, update):
        resp = client.message(update.message.text)
        response = None
        value = ""
        search_book_result = ''
        try:
                if (list(resp['entities'])[0] == 'booktype'):
                        entity = 'booktype'
                        if (len(resp['entities'][entity]) > 1):
                                for i in range(0, len(resp['entities'][entity])):
                                        if (i != len(resp['entities'][entity]) - 1):
                                                value += str(resp['entities']
                                                             [entity][i]['value']) + ","
                                        else:
                                                value += str(resp['entities']
                                                             [entity][i]['value'])

                                bot.send_message(chat_id=update.message.chat_id,
                                 text="Ok.I will send you {} books".format(str(value)))

                        else:
                                value = resp['entities'][entity][0]['value']
                                bot.send_message(
                                    chat_id=update.message.chat_id, text="Ok.I will send you {} books".format(str(value)))
                                search_text = str(value)
                                search_text = search_text.replace(' ', '+')
                                language = 'en'
                                maxResults = '40'
                                full_url = url + search_text + '&langRestrict=' + \
                                    language + '&maxResults=' + maxResults
                                search_response = urllib.request.urlopen(
                                    full_url).read()
                                json_obj=str(search_response,'utf-8')
                                data = json.loads(json_obj)
                                search_book_result = ''
                                '''for item in data['items']:
                                        search_book_result += 'Name: ' + \
                                            item['volumeInfo']['title'] + '\n'
                                        search_book_result += 'Author(s): '
                                        for i in range(len(item['volumeInfo']['authors']) - 1):
                                                search_book_result += item['volumeInfo']['authors'][i] + ',  '
                                        search_book_result += item['volumeInfo']['authors'][-1]
                                        search_book_result += '\n'
                                        search_book_result += 'Category(s): '
                                        for category in range(len(item['volumeInfo']['categories']) - 1):
                                                search_book_result += category + ', '
                                        search_book_result += item['volumeInfo']['categories'][-1]
                                        search_book_result += '\n'
                                        search_book_result += 'Page Count: ' + \
                                            str(item['volumeInfo']
                                                ['pageCount']) + '\n'
                                        search_book_result += '---------------------------\n'
                                '''
                                for item in data['items']:
                                    volumeInfo = item['volumeInfo']
                                    id = ''
                                    title = ''
                                    authors = []
                                    publisher = ''
                                    description = ''
                                    pageCount = ''
                                    categories = []
                                    if 'id' in item:
                                        id = item['id']
                                    if 'title' in volumeInfo:
                                        #print('Name: ' + item['volumeInfo']['title'])
                                        title = item['volumeInfo']['title']
                                    if 'authors' in volumeInfo:
                                        #print('Author(s): ', end='')
                                        for author in item['volumeInfo']['authors']:
                                            #print(author + '\t', end='')
                                            authors.append(author)
                                        #print()
                                    if 'categories' in volumeInfo:
                                        #print('Category(s): ', end='')
                                        for category in item['volumeInfo']['categories']:
                                            #print(category + '\t', end='')
                                            categories.append(category)
                                        #print()
                                    if 'pageCount' in volumeInfo:
                                        #print('Page Count: ' + str(item['volumeInfo']['pageCount']))
                                        pageCount = str(item['volumeInfo']['pageCount'])
                                    if 'description' in volumeInfo:
                                        description = item['volumeInfo']['description']
                                    if 'publisher' in volumeInfo:
                                        publisher = item['volumeInfo']['publisher']
                                    bookElem = bookObj(id, title, authors, publisher, description, pageCount,
                                                       categories)
                                    bookList.append(bookElem)
                                    #print('---------------------------')
                                i = 1
                                #List first results
                                search_book_result=''
                                j=1
                                for bookElem in bookList:
                                    search_book_result += str(i)+'. '+'Name: ' + \
                                                          bookElem.title + '\n'
                                    search_book_result += 'Author(s): '
                                    for j in range(len(bookElem.authors)-1):
                                        search_book_result += bookElem.authors[j]   + ',  '
                                    search_book_result += bookElem.authors[-1]

                                    search_book_result += '\n'

                                    search_book_result += 'Category(s): '
                                    for category in range(len(bookElem.categories) - 1):
                                        search_book_result += categories[i] + ', '
                                    search_book_result += categories[-1]
                                    search_book_result += '\n'
                                    search_book_result += 'Page Count: ' + \
                                                          bookElem.pageCount + '\n'
                                    search_book_result += '---------------------------\n'
                                    if (i == 5):
                                        break
                                    i += 1

                                del bookList[:]

                else:
                        bot.send_message(
                            chat_id=update.message.chat_id, text="Sorry,didn't understand.")
        except:
                pass
                bot.send_message(chat_id=update.message.chat_id,
                         text="Sorry,didn't understand.")
        bot.send_message(chat_id=update.message.chat_id,
                         text=search_book_result)


searchBookController_handler = MessageHandler(
    Filters.text, searchBookController)


def stop(bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="Ok.CYA LATER {}".format(str(name)))


stop_handler = CommandHandler('stop', stop)
dispatcher.add_handler(stop_handler)
def chitchat(bot, update):
        bot.send_message(chat_id=update.message.chat_id,
                         text="Oh ok you want to give some information about you.Please enter /start")
        global name
        name = ""
        dispatcher.remove_handler(controller_handler)
        dispatcher.remove_handler(nameController_handler)
        dispatcher.remove_handler(bookController_handler)
        dispatcher.remove_handler(searchBookController_handler)

chitchat_handler = CommandHandler('chitchat', chitchat)
dispatcher.add_handler(chitchat_handler)
