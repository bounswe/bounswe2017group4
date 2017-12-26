from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from wit import Wit
import random
import json
import urllib.request
import urllib.parse
import urllib.error
from . import models
from emoji import emojize
import os

selected_book = 1
url = 'https://www.googleapis.com/books/v1/volumes?q='
# wit.ai's token
access_token = "IQXRZALWN7LAYGHQZWSNKWU2GMGYPHMA"

name = "Anonymous"
if (os.environ.get('RUNMODE') == "test"):
    print("Running in test mode")
    updater = Updater(token='468419437:AAGyilEfIMQehUMjsfGWE_7pmSpzGQN45qE')
else:
    print("Running in prod mode")
    updater = Updater(token='306155790:AAHshYWFsAmOKly8107HkSISlUziQz77DLs')

dispatcher = updater.dispatcher
client = Wit(access_token=access_token)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater.start_polling()
current_state_id = 1
bookList = []
filtered_bookList = []
bookitem = ''
blush = emojize(":blush:", use_aliases=True)
blue_book = emojize(":blue_book:", use_aliases=True)
green_book = emojize(":green_book:", use_aliases=True)
orange_book = emojize(":orange_book:", use_aliases=True)
closed_book = emojize(":closed_book:", use_aliases=True)


class bookObj:
    def __init__(self, id, title, authors, publisher, description, pageCount, categories, isbn_13):
        self.id = id
        self.title = title
        self.authors = authors
        self.publisher = publisher
        self.description = description
        self.pageCount = pageCount
        self.categories = categories
        self.isbn_13 = isbn_13


def get_book_emoji():
    return random.choice([blue_book, green_book, orange_book, closed_book])

# Starts next handler if it has no NONE entity. Otherwise it starts
# a job in a second
def handler_generator(update, job_queue, next_state):
    global current_state_id
    # exec ('dispatcher.remove_handler(' + current_state.description + '_handler)')
    current_state_id = next_state.id

    if has_none_entity(next_state.id):
        # current_state_id = next_state.id
        dispatcher.remove_handler(general_handler)
        job_queue.run_once(callback_with_none, 1, context=update.message.chat_id)


# This is a job for states which has NONE as entity
def callback_with_none(bot, job):
    global current_state_id
    try:
        current_state, next_state, response = get_state_variables(current_state_id, 'None')
        bot.send_message(chat_id=job.context, text=response.chatbot_response)
        # exec ('dispatcher.add_handler(' + next_state.description + '_handler)')
        current_state_id = next_state.id
        dispatcher.add_handler(general_handler)
    except:
        bot.send_message(chat_id=job.context, text=not_understand(current_state))


def has_none_entity(state_id):
    edges = models.Edge.objects.filter(current_state_id=state_id)
    for edge in edges:
        if edge.user_response == 'None':
            return True
    return False


def get_state_variables(state_id, entity):
    try:
        edge = models.Edge.objects.get(current_state_id=state_id, user_response=entity)
    except Exception as e:
        print(e)
        edge = models.Edge.objects.get(current_state_id=state_id, user_response='*')
        print (edge)

    current_state = edge.current_state_id
    next_state = edge.next_state_id
    response = random.choice(models.Response.objects.filter(state_id=next_state.id))
    return current_state, next_state, response


# splits responses with multiple sentences
def response_formatter(chatbot_response, value=''):
    responses = chatbot_response.split('.')
    responses = [x.format(str(value)) for x in responses]
    return responses


# Start command handler
def start(bot, update):
    global current_state_id
    response = random.choice(models.Response.objects.filter(state_id=1))
    responses = response_formatter(response.chatbot_response)
    for r in responses:
        bot.send_message(chat_id=update.message.chat_id, text=r + blush, use_aliases=True)
    current_state_id = 1
    user = models.User.objects.filter(telegram_id=update.message.chat_id)
    if len(user) == 0:
        new_user = models.User.objects.create(telegram_id=update.message.chat_id)
        new_user.save()


def general(bot, update, job_queue):
    global current_state_id
    resp = client.message(update.message.text)
    if len(list(resp['entities'])) == 1:
        # TODO check if list is empty (not sure if it is important)
        try:
            entity = list(resp['entities'])[0]
            print('my intent is: ' + entity)
            current_state, next_state, response = get_state_variables(current_state_id, entity)
            print('my state is: ' + current_state.description)
            try:
                text = eval(next_state.description + '(response.chatbot_response, update, entity)')
            except Exception as e:
                print(e)
                text = general_state(response.chatbot_response, update, entity)
            bot.send_message(chat_id=update.message.chat_id, text=text)
            handler_generator(update, job_queue, next_state)
        except Exception as e:
            print(e)
            bot.send_message(chat_id=update.message.chat_id,
                             text=not_understand(models.State.objects.get(id=current_state_id)))
    elif len(list(resp['entities'])) > 1:
        try:
            entity = list(resp['entities'])[1]
            current_state, next_state, response = get_state_variables(current_state_id, entity)
            try:
                text = eval(next_state.description + '(response.chatbot_response, update, entity)')
            except Exception as e:
                print(e)
                text = general_state(response.chatbot_response, update, entity)
            bot.send_message(chat_id=update.message.chat_id, text=text)
            value = ''
            handler_generator(update, job_queue, next_state)
        except Exception as e:
            print(e)
            bot.send_message(chat_id=update.message.chat_id, text=not_understand(models.State.objects.get(id=current_state_id)))
    else:
        try:
            entity = ''
            current_state, next_state, response = get_state_variables(current_state_id, entity)
            try:
                text = eval(next_state.description + '(response.chatbot_response, update, entity)')
            except Exception as e:
                print(e)
                text = general_state(response.chatbot_response, update, entity)
            bot.send_message(chat_id=update.message.chat_id, text=text)
            value = ''
            handler_generator(update, job_queue, next_state)
        except Exception as e:
            print(e)
            bot.send_message(chat_id=update.message.chat_id, text=not_understand(models.State.objects.get(id=current_state_id)))


def not_understand(current_state):
    response = random.choice(
        models.Response.objects.filter(state_id=models.State.objects.get(description="does_not_understand")))
    resp = response.chatbot_response
    try:
        edge = random.choice(models.Edge.objects.filter(current_state_id=current_state_id))
        if edge.recommended_response != '':
            resp += '\nYou can enter something like this:\n\"' + edge.recommended_response + '\"'
    except:
        pass
    return resp


def general_state(response, update, entity):
    resp = client.message(update.message.text)
    print('Entered start message')
    print (str(models.Edge.objects.filter(current_state_id=current_state_id)))
    try:
        value = resp['entities'][entity][0]['value']
    except:
        value = ''
    return response.format(str(value))


def meeting_user(response, update, entity):
    resp = client.message(update.message.text)
    try:
        value = resp['entities'][entity][0]['value']
    except:
        value = ''
    user = models.User.objects.filter(telegram_id=update.message.chat_id)
    if len(user) == 0:
        new_user = models.User.objects.create(telegram_id=update.message.chat_id)
        new_user.name = value
        new_user.save()
    else:
        user.update(name=value)
    return response.format(str(value))


def save_book_interests(response, update, entity):
    resp = client.message(update.message.text)
    value = ''
    if len(resp['entities'][entity]) > 0:
        for i in range(0, len(resp['entities'][entity])):
            if i != len(resp['entities'][entity]) - 1:
                value += str(resp['entities']
                             [entity][i]['value']) + ", "
            else:
                value += str(resp['entities']
                             [entity][i]['value'])
    user = models.User.objects.get(telegram_id=update.message.chat_id)
    user_interest = models.UserInterest.objects.create(user=user)
    user_interest.interest = value
    user_interest.save()
    return response.format(str(value))


def list_search(response, update, entity):
    resp = client.message(update.message.text)
    print('STARTED SEARCH')
    global bookList
    del bookList[:]
    value = ''
    search_book_result = ''
    text = ''
    if (len(resp['entities'][entity]) > 1):
        print('IT DOES NOT ENTER HERE ANYTIME!!!!')
        for i in range(0, len(resp['entities'][entity])):
            if (i != len(resp['entities'][entity]) - 1):
                value += str(resp['entities']
                             [entity][i]['value']) + ","
            else:
                value += str(resp['entities']
                             [entity][i]['value'])

        search_book_result += response + '\n'
    else:
        value = resp['entities'][entity][0]['value']
        user = models.User.objects.get(telegram_id=update.message.chat_id)
        history = models.History.objects.create(user=user)
        history.query = value
        history.save()
        search_book_result += response + '\n'
        search_text = str(value)
        search_text = search_text.replace(' ', '+')
        language = 'en'
        maxResults = '40'
        full_url = url + search_text + '&langRestrict=' + \
                   language + '&maxResults=' + maxResults
        print(full_url)
        search_response = urllib.request.urlopen(
            full_url).read()
        json_obj = str(search_response, 'utf-8')
        data = json.loads(json_obj)

        # Fill the array of books by id, title, authors, publisher, description, page count and categories
        for item in data['items']:
            volumeInfo = item['volumeInfo']
            id = ''
            title = ''
            authors = []
            publisher = ''
            description = ''
            pageCount = ''
            categories = []
            isbn_10 = ''
            if 'id' in item:
                id = item['id']
            if 'title' in volumeInfo:
                title = item['volumeInfo']['title']
            if 'authors' in volumeInfo:
                for author in item['volumeInfo']['authors']:
                    if author != '':
                        authors.append(author)
            if 'categories' in volumeInfo:
                for category in item['volumeInfo']['categories']:
                    if category != '':
                        categories.append(category)
            if 'pageCount' in volumeInfo:
                pageCount = str(item['volumeInfo']['pageCount'])
            if 'description' in volumeInfo:
                description = item['volumeInfo']['description']
            if 'publisher' in volumeInfo:
                publisher = item['volumeInfo']['publisher']
            if 'industryIdentifiers' in volumeInfo:
                getFirst = True
                for identifier in item['volumeInfo']['industryIdentifiers']:
                    if getFirst:
                        isbn_10 = identifier['identifier']
                    getFirst = False
            bookElem = bookObj(id, title, authors, publisher, description, pageCount,
                               categories, isbn_10)
            bookList.append(bookElem)
        i = 1
        # List first results
        # search_book_result = ''
        j = 1
        for bookElem in bookList:
            search_book_result += get_book_emoji() + ' ' + str(i) + '. ' + 'Name: ' + \
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
    return search_book_result


def filter_by_page_number(response, update, entity):
    global bookList
    resp = client.message(update.message.text)
    search_book_result = ''
    print('PAGE FILTER IS ENTERED')
    print (list(resp['entities']))
    if 'is_more' in list(resp['entities']):
        filter_num_String = list(resp['entities']['page_filter'])[0]['value']
        filter_num = 0
        print('cast value is ' + filter_num_String)
        try:
            filter_num = int(filter_num_String)
            is_more = list(resp['entities']['is_more'])[0]['value']
            # fill_the_list(bookList, filter_num, is_more)
            if is_more == 'more':
                value = 'more than ' + resp['entities'][entity][0]['value']
                search_book_result += (response + '\n').format(str(value))
                for bookElem in bookList:
                    i = 1
                    if int(bookElem.pageCount) > filter_num:
                        search_book_result += get_book_emoji() + ' ' + str(i) + '. ' + 'Name: ' + \
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
                value = 'less than ' + resp['entities'][entity][0]['value']
                search_book_result += (response + '\n').format(str(value))
                for bookElem in bookList:
                    i = 1
                    if int(bookElem.pageCount) < filter_num:
                        search_book_result += get_book_emoji() + 'Name: ' + \
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
            print('some error that I don\'t know')
    return search_book_result


def filter_by_category(response, update, entity):
    global bookList
    resp = client.message(update.message.text)
    filter_category = list(resp['entities']['filter_category'])[0]['value']
    value = resp['entities'][entity][0]['value']
    search_book_result = (response + '\n').format(str(value))
    search_book_result += fill_the_list(bookList, filter_category, 'category')
    return search_book_result
    # TODO this part should be handled by book api class


def filter_by_author(response, update, entity):
    global bookList
    resp = client.message(update.message.text)
    filter_category = list(resp['entities']['author'])[0]['value']
    value = resp['entities'][entity][0]['value']
    search_book_result = (response + '\n').format(str(value))
    search_book_result += fill_the_list(bookList, filter_category, 'author')
    return search_book_result
    # TODO this part should be handled by book api class


def book_detail(response, update, entity):
    global bookList
    global bookitem
    resp = client.message(update.message.text)
    bookOrder = list(resp['entities']['ordinal'])[0]['value']
    bookItem = bookList[bookOrder - 1]
    bookitem = bookItem
    bookDetailMessage = 'Name: ' + bookItem.title + '\n'
    bookDetailMessage += 'Author(s): '
    for j in range(len(bookItem.authors) - 1):
        bookDetailMessage += bookItem.authors[j] + ',  '
    bookDetailMessage += bookItem.authors[-1] + '\n'
    bookDetailMessage += 'Category(s): '
    for j in range(len(bookItem.categories) - 1):
        bookDetailMessage += bookItem.categories[j] + ',  '
    bookDetailMessage += bookItem.categories[-1] + '\n'
    bookDetailMessage += 'Page number: ' + bookItem.pageCount + '\n'
    bookDetailMessage += 'Description: ' + bookItem.description + '\n'
    bookDetailMessage += 'Publisher: ' + bookItem.publisher + '\n'
    bookDetailMessage += 'Buy from Amazon: ' + buy_book(bookItem.isbn_13)
    bookDetailMessage += '\n'
    return bookDetailMessage


def save_rating(response, update, entity):
    global bookitem
    resp = client.message(update.message.text)
    try:
        print (resp)
        value = resp['_text']
        user = models.User.objects.get(telegram_id=update.message.chat_id)
        try:
            user_rating = models.UserRating.objects.get(user=user, book_id=bookitem.title)
            user_rating.rating = value
            user_rating.update()
        except Exception as e:
            print(e)
            user_rating = models.UserRating.objects.create(user=user, book_id=bookitem.title, rating=value)
            user_rating.rating = value
            user_rating.save()
    except Exception as e:
        print(e)
        value = ''
    print ('rating: ' + response)
    return response.format(str(value))


def save_comment(response, update, entity):
    global bookitem
    resp = client.message(update.message.text)
    try:
        value = resp['_text']
        user = models.User.objects.get(telegram_id=update.message.chat_id)
        try:
            user_comment = models.UserComment.objects.get(user=user, book_id=bookitem.title)
            user_comment.comment = value
            user_comment.update()
        except Exception as e:
            print(e)
            user_comment = models.UserComment.objects.create(user=user, book_id=bookitem.title, comment=value)
            user_comment.save()
    except Exception as e:
        print(e)
        value = ''
    return response.format(str(value))

def view_comments_ratings(response,update,entity):
	global bookitem
	resp = client.message(update.message.text)
	value=""
	try:
		user = models.User.objects.get(telegram_id=update.message.chat_id)
		try:
			user_comment = models.UserComment.objects.filter(book_id=bookitem.title)
			user_rating= models.UserRating.objects.filter(book_id=bookitem.title)
			value+=bookitem.title+"\nComments\n"
			for j in range(len(user_comment)):
				value+= str(j+1)+") "+user_comment[j].comment+"\n"
			value+= "\nRatings\n"
			for j in range(len(user_rating)):
				value+= str(j+1)+") "+str(user_rating[j].rating)+"\n"

		except Exception as e:
			print(e)
	except Exception as e:
		print(e)
		value=""		
	return response.format(str(value))

def buy_book(isbn_13):
    # generate amazon link
    amazonUrl = "https://www.amazon.com/gp/search/ref=sr_adv_b/?search-alias=stripbooks&unfiltered=1&field-keywords=&field-author=&field-title=&field-isbn="
    amazonUrl += isbn_13
    amazonUrl += "&field-publisher=&node=&field-p_n_condition-type=&p_n_feature_browse-bin=&field-age_range=&field-language=&field-dateop=During&field-datemod=&field-dateyear=&sort=relevanceexprank&Adv-Srch-Books-Submit.x=39&Adv-Srch-Books-Submit.y=15"
    return amazonUrl


def fill_the_list(bookList, filter_category, type):
    print('fill the list is entered')
    print('filter category is ' + filter_category)
    search_book_result = ''
    for bookElem in bookList:
        i = 1
        if (type == 'more' or type == 'less'):
            if (type == 'more'):
                for bookElem in bookList:
                    i = 1
                    if int(bookElem.pageCount) > filter_category:
                        search_book_result += get_book_emoji() + 'Name: ' + \
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
            elif (type == 'less'):
                for bookElem in bookList:
                    i = 1
                    if int(bookElem.pageCount) < filter_category:
                        search_book_result += get_book_emoji() + 'Name: ' + \
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
            if (type == 'category'):
                searchIn = bookElem.categories
            elif (type == 'author'):
                searchIn = bookElem.authors
            if filter_category.lower() in (bookElemItem.lower() for bookElemItem in searchIn):
                search_book_result += get_book_emoji() + 'Name: ' + \
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
    return search_book_result


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
general_handler = MessageHandler(Filters.text, general, pass_job_queue=True)
dispatcher.add_handler(general_handler)
