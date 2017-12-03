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

url = 'https://www.googleapis.com/books/v1/volumes?q='

access_token = "IQXRZALWN7LAYGHQZWSNKWU2GMGYPHMA"
name = ""
controller1 = ""
updater = Updater(token='306155790:AAHshYWFsAmOKly8107HkSISlUziQz77DLs')
dispatcher = updater.dispatcher
client = Wit(access_token=access_token)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
updater.start_polling()
current_state_id = 1

# Starts next handler if it has no NONE entity. Otherwise it starts
# a job in a second
def handler_generator(bot, update, job_queue, next_state, value, response, current_state):
    global current_state_id
    exec ('dispatcher.remove_handler(' + current_state.description + '_handler)')
    if has_none_entity(next_state.id):
        current_state_id = next_state.id
        job_queue.run_once(callback_with_none, 1, context=update.message.chat_id)
    else:
        exec ('dispatcher.add_handler(' + next_state.description + '_handler)')

# This is a job for states which has NONE as entity
def callback_with_none(bot, job):
    try:
        current_state, next_state, response = get_state_variables(current_state_id, 'NONE')
        bot.send_message(chat_id=job.context, text=response.chatbot_response)
        exec ('dispatcher.add_handler(' + next_state.description + '_handler)')
    except:
        bot.send_message(chat_id=job.context, text=not_understand())


def has_none_entity(state_id):
    edges = models.Edge.objects.filter(current_state_id=state_id)
    for edge in edges:
        if edge.user_response == 'NONE':
            return True
    return False

def get_state_variables(state_id, entity):
    edge = models.Edge.objects.get(current_state_id=state_id, user_response=entity)
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
    response = random.choice(models.Response.objects.filter(state_id=1))
    responses = response_formatter(response.chatbot_response)
    for r in responses:
        bot.send_message(chat_id=update.message.chat_id, text=r)
    dispatcher.add_handler(start_message_handler)


def not_understand():
    response = random.choice(models.Response.objects.filter(state_id=11))
    return response

# each message handler selects next handler according to
# entity and sends next handler's message
# since handlers always wait for an input
# if handler does not wait for an input (if the edge between it and its prev state is NONE)
# it won't work. job_queue is used for that situations
def start_message(bot, update, job_queue):
    resp = client.message(update.message.text)
    try:
        # TODO check if list is empty (not sure if it is important)
        entity = list(resp['entities'])[0]
        current_state, next_state, response = get_state_variables(1, entity)
        bot.send_message(chat_id=update.message.chat_id, text=response.chatbot_response)
        value = ''
        handler_generator(bot, update, job_queue, next_state, value, response, current_state)
    except:
        # TODO change all except ones to a didn't understand state
        bot.send_message(chat_id=update.message.chat_id, text=not_understand())


def ask_name(bot, update, job_queue):
    resp = client.message(update.message.text)
    try:
        entity = list(resp['entities'])[0]
        current_state, next_state, response = get_state_variables(2, entity)
        value = resp['entities'][entity][0]['value']
        user = models.User.objects.filter(telegram_id=update.message.chat_id)
        if len(user) == 0:
            new_user = models.User.objects.create(telegram_id=update.message.chat_id)
            new_user.name = value
            new_user.save()
        else:
            user.update(name=value)
        bot.send_message(chat_id=update.message.chat_id, text=response.chatbot_response.format(str(value)))
        handler_generator(bot, update, job_queue, next_state, value, response, current_state)
    except:
        bot.send_message(chat_id=update.message.chat_id, text=not_understand())


def meeting_user(bot, update):
    resp = client.message(update.message.text)
    try:
        entity = list(resp['entities'])[0]
        current_state, next_state, response = get_state_variables(3, entity)
        value = resp['entities'][entity][0]['value']
        bot.send_message(chat_id=update.message.chat_id, text=response.chatbot_response.format(str(value)))
        handler_generator(bot, update, job_queue, next_state, value, response, current_state)
    except:
        bot.send_message(chat_id=update.message.chat_id, text=not_understand())


def ask_book_interests(bot, update, job_queue):
    global current_state_id
    resp = client.message(update.message.text)
    try:
        entity = list(resp['entities'])[0]
        current_state, next_state, response = get_state_variables(4, entity)
        value = ''
        if len(resp['entities'][entity]) > 0:
            for i in range(0, len(resp['entities'][entity])):
                if i != len(resp['entities'][entity]) - 1:
                    value += str(resp['entities']
                                 [entity][i]['value']) + ", "
                else:
                    value += str(resp['entities']
                                 [entity][i]['value'])
        # TODO add book interests to db
        bot.send_message(chat_id=update.message.chat_id, text=response.chatbot_response.format(str(value)))
        handler_generator(bot, update, job_queue, next_state, value, response, current_state)
    except:
        bot.send_message(chat_id=update.message.chat_id, text=not_understand())


def save_book_interests(bot, update, job_queue):
    resp = client.message(update.message.text)
    try:
        entity = list(resp['entities'])[0]
        current_state, next_state, response = get_state_variables(5, entity)
        value = resp['entities'][entity][0]['value']
        bot.send_message(chat_id=update.message.chat_id, text=response.chatbot_response.format(str(value)))
        handler_generator(bot, update, job_queue, next_state, value, response, current_state)
    except:
        bot.send_message(chat_id=update.message.chat_id, text=not_understand())


def book_search(bot, update, job_queue):
    resp = client.message(update.message.text)
    # TODO this part should be handled by book api class
    # try:
    #     entity = list(resp['entities'])[0]
    #     value = ''
    #     search_book_result = ''
    #     current_state, next_state, response = get_state_variables(6, entity)
    #     if (len(resp['entities'][entity]) > 1):
    #         print('if')
    #         for i in range(0, len(resp['entities'][entity])):
    #             if (i != len(resp['entities'][entity]) - 1):
    #                 value += str(resp['entities']
    #                              [entity][i]['value']) + ","
    #             else:
    #                 value += str(resp['entities']
    #                              [entity][i]['value'])
    #
    #         bot.send_message(chat_id=update.message.chat_id,
    #                          text="Ok.I will send you {} books".format(str(value)))
    #
    #     else:
    #         print('else')
    #         value = resp['entities'][entity][0]['value']
    #         bot.send_message(
    #             chat_id=update.message.chat_id, text="Ok.I will send you {} books".format(str(value)))
    #         search_text = str(value)
    #         search_text = search_text.replace(' ', '+')
    #         language = 'en'
    #         maxResults = '5'
    #         full_url = url + search_text + '&langRestrict=' + \
    #                    language + '&maxResults=' + maxResults
    #         search_response = urllib.request.urlopen(
    #             full_url).read()
    #         json_obj = str(search_response, 'utf-8')
    #         data = json.loads(json_obj)
    #         search_book_result = ''
    #         for item in data['items']:
    #             search_book_result += 'Name: ' + \
    #                                   item['volumeInfo']['title'] + '\n'
    #             search_book_result += 'Author(s): '
    #             for i in range(len(item['volumeInfo']['authors']) - 1):
    #                 search_book_result += item['volumeInfo']['authors'][i] + ',  '
    #             search_book_result += item['volumeInfo']['authors'][-1]
    #             search_book_result += '\n'
    #             search_book_result += 'Category(s): '
    #             for category in range(len(item['volumeInfo']['categories']) - 1):
    #                 search_book_result += category + ', '
    #             search_book_result += item['volumeInfo']['categories'][-1]
    #             search_book_result += '\n'
    #             search_book_result += 'Page Count: ' + \
    #                                   str(item['volumeInfo']
    #                                       ['pageCount']) + '\n'
    #             search_book_result += '---------------------------\n'
    #     bot.send_message(chat_id=update.message.chat_id, text=response.chatbot_response.format(str(value)))
    #     handler_generator(bot, update, job_queue, next_state, value, response, current_state)
    # except:
    #     bot.send_message(chat_id=update.message.chat_id, text=not_understand())


def list_search(bot, update, job_queue):
    resp = client.message(update.message.text)
    # TODO this part should be handled by book api class


def filter_by_page_number(bot, update, job_queue):
    resp = client.message(update.message.text)
    # TODO this part should be handled by book api class


def filter_by_category(bot, update, job_queue):
    resp = client.message(update.message.text)
    # TODO this part should be handled by book api class

def filter_by_author(bot, update, job_queue):
    resp = client.message(update.message.text)
    # TODO this part should be handled by book api class


# def start(bot, update):
#         global name
#         if(name == ""):
#                 bot.send_message(chat_id=update.message.chat_id,
#                                  text="hello! I am book search chatbot")
#                 bot.send_message(chat_id=update.message.chat_id,
#                                  text="May I ask a few questions to offer you a better service?")
#                 dispatcher.add_handler(controller_handler)
#         else:
#                 bot.send_message(chat_id=update.message.chat_id,
#                          text="Ok.What do u want to search {}".format(str(name)))
#                 dispatcher.remove_handler(controller_handler)
#                 dispatcher.remove_handler(nameController_handler)
#                 dispatcher.remove_handler(bookController_handler)
#                 dispatcher.add_handler(searchBookController_handler)
#
# start_handler = CommandHandler('start', start)
# dispatcher.add_handler(start_handler)
#
#
# def controller(bot, update):
#         resp = client.message(update.message.text)
#         global name
#         try:
#                 if (list(resp['entities'])[0] == "accept"):
#                         bot.send_message(
#                             chat_id=update.message.chat_id, text="How would you like to be called?")
#                         dispatcher.remove_handler(controller_handler)
#                         dispatcher.add_handler(nameController_handler)
#                 elif (list(resp['entities'])[0] == "reject"):
#                         name = "Anonymous"
#                         bot.send_message(
#                             chat_id=update.message.chat_id, text="Ok you want to stay mysterious.I will call you Anonymous from now on.")
#                         bot.send_message(chat_id=update.message.chat_id,
#                          text="What do u want to search?")
#                         dispatcher.remove_handler(controller_handler)
#                         dispatcher.remove_handler(nameController_handler)
#                         dispatcher.remove_handler(bookController_handler)
#                         dispatcher.add_handler(searchBookController_handler)
#
#                 else:
#                         bot.send_message(
#                             chat_id=update.message.chat_id, text="Sorry,didn't understand.")
#         except:
#                 pass
#                 bot.send_message(chat_id=update.message.chat_id,
#                          text="Sorry,didn't understand.")
#
#
# controller_handler = MessageHandler(Filters.text, controller)
#
#
#
# def nameController(bot, update):
#         resp = client.message(update.message.text)
#         try:
#                 if (list(resp['entities'])[0] == 'name'):
#                         entity = "name"
#                         value = resp['entities'][entity][0]['value']
#                         bot.send_message(chat_id=update.message.chat_id,
#                                  text="Hello {},nice to meet you".format(str(value)))
#                         global name
#                         name = str(value)
#                 else:
#                         bot.send_message(
#                             chat_id=update.message.chat_id, text="Sorry,didn't understand.")
#         except:
#                 pass
#                 bot.send_message(chat_id=update.message.chat_id,
#                          text="Sorry,didn't understand.")
#         if(name != ""):
#                 bot.send_message(chat_id=update.message.chat_id,
#                          text="What kind of books do you read most? ")
#                 dispatcher.remove_handler(nameController_handler)
#                 dispatcher.add_handler(bookController_handler)
#
#
# nameController_handler = MessageHandler(Filters.text, nameController)
#
#
#
# def bookController(bot, update):
#         resp = client.message(update.message.text)
#         value = ""
#         try:
#                 if (list(resp['entities'])[0] == 'booktype'):
#                         entity = 'booktype'
#                         if (len(resp['entities'][entity]) > 1):
#                                 for i in range(0, len(resp['entities'][entity])):
#                                         if (i != len(resp['entities'][entity]) - 1):
#                                                 value += str(resp['entities']
#                                                              [entity][i]['value']) + ","
#                                         else:
#                                                 value += str(resp['entities']
#                                                              [entity][i]['value'])
#                                 response = "I have saved that you like " + \
#                                     str(value) + " books."
#                                 bot.send_message(chat_id=update.message.chat_id, text=response)
#                                 bot.send_message(
#                             chat_id=update.message.chat_id, text='From now on, you can search books. :)')
#                                 dispatcher.remove_handler(bookController_handler)
#                                 dispatcher.add_handler(searchBookController_handler)
#
#                         else:
#                                 value = resp['entities'][entity][0]['value']
#                                 bot.send_message(chat_id=update.message.chat_id,
#                                  text="I have saved that you like " + str(value) + " books.")
#                                 bot.send_message(
#                             chat_id=update.message.chat_id, text='From now on, you can search books. :)')
#                                 dispatcher.remove_handler(bookController_handler)
#                                 dispatcher.add_handler(searchBookController_handler)
#         except:
#                 pass
#                 bot.send_message(chat_id=update.message.chat_id,
#                          text="Sorry didn't understand.")
#
#
# bookController_handler = MessageHandler(Filters.text, bookController)
#
#
# def searchBookController(bot, update):
#         resp = client.message(update.message.text)
#         response = None
#         value = ""
#         search_book_result = ''
#         try:
#                 if (list(resp['entities'])[0] == 'booktype'):
#                         entity = 'booktype'
#                         if (len(resp['entities'][entity]) > 1):
#                                 for i in range(0, len(resp['entities'][entity])):
#                                         if (i != len(resp['entities'][entity]) - 1):
#                                                 value += str(resp['entities']
#                                                              [entity][i]['value']) + ","
#                                         else:
#                                                 value += str(resp['entities']
#                                                              [entity][i]['value'])
#
#                                 bot.send_message(chat_id=update.message.chat_id,
#                                  text="Ok.I will send you {} books".format(str(value)))
#
#                         else:
#                                 value = resp['entities'][entity][0]['value']
#                                 bot.send_message(
#                                     chat_id=update.message.chat_id, text="Ok.I will send you {} books".format(str(value)))
#                                 search_text = str(value)
#                                 search_text = search_text.replace(' ', '+')
#                                 language = 'en'
#                                 maxResults = '5'
#                                 full_url = url + search_text + '&langRestrict=' + \
#                                     language + '&maxResults=' + maxResults
#                                 search_response = urllib.request.urlopen(
#                                     full_url).read()
#                                 json_obj=str(search_response,'utf-8')
#                                 data = json.loads(json_obj)
#                                 search_book_result = ''
#                                 for item in data['items']:
#                                         search_book_result += 'Name: ' + \
#                                             item['volumeInfo']['title'] + '\n'
#                                         search_book_result += 'Author(s): '
#                                         for i in range(len(item['volumeInfo']['authors']) - 1):
#                                                 search_book_result += item['volumeInfo']['authors'][i] + ',  '
#                                         search_book_result += item['volumeInfo']['authors'][-1]
#                                         search_book_result += '\n'
#                                         search_book_result += 'Category(s): '
#                                         for category in range(len(item['volumeInfo']['categories']) - 1):
#                                                 search_book_result += category + ', '
#                                         search_book_result += item['volumeInfo']['categories'][-1]
#                                         search_book_result += '\n'
#                                         search_book_result += 'Page Count: ' + \
#                                             str(item['volumeInfo']
#                                                 ['pageCount']) + '\n'
#                                         search_book_result += '---------------------------\n'
#
#                 else:
#                         bot.send_message(
#                             chat_id=update.message.chat_id, text="Sorry,didn't understand.")
#         except:
#                 pass
#                 bot.send_message(chat_id=update.message.chat_id,
#                          text="Sorry,didn't understand.")
#         bot.send_message(chat_id=update.message.chat_id,
#                          text=search_book_result)
#
#
# searchBookController_handler = MessageHandler(
#     Filters.text, searchBookController)
#
#
# def stop(bot, update):
#         bot.send_message(chat_id=update.message.chat_id,
#                          text="Ok.CYA LATER {}".format(str(name)))
#
#
# stop_handler = CommandHandler('stop', stop)
# dispatcher.add_handler(stop_handler)
# def chitchat(bot, update):
#         bot.send_message(chat_id=update.message.chat_id,
#                          text="Oh ok you want to give some information about you.Please enter /start")
#         global name
#         name = ""
#         dispatcher.remove_handler(controller_handler)
#         dispatcher.remove_handler(nameController_handler)
#         dispatcher.remove_handler(bookController_handler)
#         dispatcher.remove_handler(searchBookController_handler)
#
# chitchat_handler = CommandHandler('chitchat', chitchat)
# dispatcher.add_handler(chitchat_handler)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
start_message_handler = MessageHandler(Filters.text, start_message, pass_job_queue=True)
meeting_user_handler = MessageHandler(Filters.text, meeting_user, pass_job_queue=True)
ask_name_handler = MessageHandler(Filters.text, ask_name, pass_job_queue=True)
ask_book_interests_handler = MessageHandler(Filters.text, ask_book_interests, pass_job_queue=True)
save_book_interests_handler = MessageHandler(Filters.text, save_book_interests, pass_job_queue=True)
book_search_handler = MessageHandler(Filters.text, book_search, pass_job_queue=True)
list_search_handler = MessageHandler(Filters.text, list_search, pass_job_queue=True)
filter_by_page_number_handler = MessageHandler(Filters.text, filter_by_page_number, pass_job_queue=True)
filter_by_category_handler = MessageHandler(Filters.text, filter_by_category, pass_job_queue=True)
filter_by_author_handler = MessageHandler(Filters.text, filter_by_author, pass_job_queue=True)
