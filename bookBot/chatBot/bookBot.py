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
        print('STARTED SEARCH')
        global bookList
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
                                print(full_url)
                                search_response = urllib.request.urlopen(
                                    full_url).read()
                                json_obj=str(search_response,'utf-8')
                                data = json.loads(json_obj)
                                search_book_result = ''
                                #Fill the array of books by id, title, authors, publisher, description, page count and categories
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
                                        title = item['volumeInfo']['title']
                                    if 'authors' in volumeInfo :
                                        for author in item['volumeInfo']['authors']:
                                            if  author!='':
                                                authors.append(author)
                                    if 'categories' in volumeInfo:
                                        for category in item['volumeInfo']['categories']:
                                            if category !='':
                                                categories.append(category)
                                    if 'pageCount' in volumeInfo:
                                        pageCount = str(item['volumeInfo']['pageCount'])
                                    if 'description' in volumeInfo:
                                        description = item['volumeInfo']['description']
                                    if 'publisher' in volumeInfo:
                                        publisher = item['volumeInfo']['publisher']
                                    bookElem = bookObj(id, title, authors, publisher, description, pageCount,
                                                       categories)
                                    bookList.append(bookElem)
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
                                    for j in range(len(bookElem.categories) - 1):
                                        search_book_result += bookElem.categories[j] + ', '
                                    search_book_result += bookElem.categories[-1]
                                    search_book_result += '\n'
                                    search_book_result += 'Page Count: ' + \
                                                          bookElem.pageCount + '\n'
                                    search_book_result += '---------------------------\n'
                                    if (i == 5):
                                        break
                                    i += 1
                                #Filter by page number

                                #del bookList[:]

                else:
                        bot.send_message(
                            chat_id=update.message.chat_id, text="Sorry,didn't understand.")
        except:
                pass
                bot.send_message(chat_id=update.message.chat_id,
                         text="Sorry,didn't understand.")
        bot.send_message(chat_id=update.message.chat_id,
                         text=search_book_result)
        dispatcher.remove_handler(searchBookController_handler)
        dispatcher.add_handler(filterBooks_handler)


searchBookController_handler = MessageHandler(
    Filters.text, searchBookController)

def filterBooks(bot, update):
    print('STARTED FILTER')
    global bookList
    resp = client.message(update.message.text)
    search_book_result = ''
    if ('page_filter' in list(resp['entities'])):
        print('PAGE FILTER IS ENTERED')
        if 'is_more' in list(resp['entities']):
            filter_num_String = list(resp['entities']['page_filter'])[0]['value']
            filter_num = 0
            print('cast value is '+filter_num_String)
            try:
                filter_num = int(filter_num_String)
                is_more = list(resp['entities']['is_more'])[0]['value']
                #fill_the_list(bookList, filter_num, is_more)
                if is_more == 'more':
                    for bookElem in bookList:
                        i = 1
                        if int(bookElem.pageCount)>filter_num:
                            search_book_result += 'Name: ' + \
                                                  bookElem.title + '\n'
                            search_book_result += 'Author(s): '
                            for j in range(len(bookElem.authors) - 1):
                                search_book_result += bookElem.authors[j] + ',  '
                            search_book_result += bookElem.authors[-1]
                            search_book_result += '\n'
                            search_book_result += 'Category(s): '
                            for j in range(len(bookElem.categories) - 1):
                                search_book_result += bookElem.categories[j] + ', '
                            search_book_result += bookElem.categories[-1]
                            search_book_result += '\n'
                            search_book_result += 'Page Count: ' + \
                                                  bookElem.pageCount + '\n'
                            search_book_result += '---------------------------\n'
                            if (i == 5):
                                break
                            i += 1
                elif is_more == 'less':
                    for bookElem in bookList:
                        i = 1
                        if int(bookElem.pageCount) < filter_num:
                            search_book_result += 'Name: ' + \
                                                  bookElem.title + '\n'
                            search_book_result += 'Author(s): '
                            for j in range(len(bookElem.authors) - 1):
                                search_book_result += bookElem.authors[j] + ',  '
                            search_book_result += bookElem.authors[-1]

                            search_book_result += '\n'

                            search_book_result += 'Category(s): '
                            for j in range(len(bookElem.categories) - 1):
                                search_book_result += bookElem.categories[j] + ', '
                            search_book_result += bookElem.categories[-1]
                            search_book_result += '\n'
                            search_book_result += 'Page Count: ' + \
                                                  bookElem.pageCount + '\n'
                            search_book_result += '---------------------------\n'
                            if (i == 5):
                                break
                            i += 1

            except:
                print('Couldnt cast to int')
        bot.send_message(chat_id=update.message.chat_id,
                         text=search_book_result)
    elif ('booktype' in list(resp['entities']) and (("filter" in update.message.text) or ("Filter" in update.message.text))):
        filter_category = list(resp['entities']['booktype'])[0]['value']
        search_book_result = fill_the_list(bookList, filter_category,'category')
        bot.send_message(chat_id=update.message.chat_id,
                     text=search_book_result)
    elif('author' in list(resp['entities'])):
        filter_category = list(resp['entities']['author'])[0]['value']
        search_book_result = fill_the_list(bookList, filter_category, 'author')
        bot.send_message(chat_id=update.message.chat_id,
                         text=search_book_result)
    else:
        print('NO FILTER DETECTED')
        dispatcher.remove_handler(filterBooks_handler)
        dispatcher.add_handler(searchBookController_handler)



filterBooks_handler = MessageHandler(
    Filters.text, filterBooks)

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

def fill_the_list(bookList, filter_category, type):
    print('fill the list is entered')
    print('filter category is '+filter_category)
    search_book_result = ''
    for bookElem in bookList:
        print('bookElem is '+bookElem.title)
        i = 1
        if(type=='more' or type=='less'):
            if(type=='more'):
                for bookElem in bookList:
                    i = 1
                    if int(bookElem.pageCount) > filter_category:
                        search_book_result += 'Name: ' + \
                                              bookElem.title + '\n'
                        search_book_result += 'Author(s): '
                        for j in range(len(bookElem.authors) - 1):
                            search_book_result += bookElem.authors[j] + ',  '
                        search_book_result += bookElem.authors[-1]
                        search_book_result += '\n'
                        search_book_result += 'Category(s): '
                        for j in range(len(bookElem.categories) - 1):
                            search_book_result += bookElem.categories[j] + ', '
                        search_book_result += bookElem.categories[-1]
                        search_book_result += '\n'
                        search_book_result += 'Page Count: ' + \
                                              bookElem.pageCount + '\n'
                        search_book_result += '---------------------------\n'
                        if (i == 5):
                            break
                        i += 1
            elif(type=='less'):
                for bookElem in bookList:
                    i = 1
                    if int(bookElem.pageCount) < filter_category:
                        search_book_result += 'Name: ' + \
                                              bookElem.title + '\n'
                        search_book_result += 'Author(s): '
                        for j in range(len(bookElem.authors) - 1):
                            search_book_result += bookElem.authors[j] + ',  '
                        search_book_result += bookElem.authors[-1]
                        search_book_result += '\n'
                        search_book_result += 'Category(s): '
                        for j in range(len(bookElem.categories) - 1):
                            search_book_result += bookElem.categories[j] + ', '
                        search_book_result += bookElem.categories[-1]
                        search_book_result += '\n'
                        search_book_result += 'Page Count: ' + \
                                              bookElem.pageCount + '\n'
                        search_book_result += '---------------------------\n'
                        if (i == 5):
                            break
                        i += 1
        else:
            if(type=='category'):
                searchIn = bookElem.categories
            elif(type=='author'):
                searchIn = bookElem.authors
            if filter_category.lower() in (bookElemItem.lower() for bookElemItem in searchIn):
                search_book_result += 'Name: ' + \
                                      bookElem.title + '\n'
                search_book_result += 'Author(s): '
                for j in range(len(bookElem.authors) - 1):
                    search_book_result += bookElem.authors[j] + ',  '
                search_book_result += bookElem.authors[-1]
                search_book_result += '\n'
                search_book_result += 'Category(s): '
                for j in range(len(bookElem.categories) - 1):
                    search_book_result += bookElem.categories[j] + ', '
                search_book_result += bookElem.categories[-1]
                search_book_result += '\n'
                search_book_result += 'Page Count: ' + \
                                      bookElem.pageCount + '\n'
                search_book_result += '---------------------------\n'

                if (i == 5):
                    print(search_book_result)
                    break
                i += 1
    print('metodun içinde searchbookresult'+search_book_result)
    return search_book_result
