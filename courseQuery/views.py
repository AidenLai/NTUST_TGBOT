from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

# Create your views here.

import json
import telegram
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler, CallbackContext

from courseQuery.module_search_course import output_result, find_available, get_ntust_general_courses

# read the telegram bot token
file = open("courseQuery/token.txt", 'r')
token = file.read().splitlines()[0]
file.close()

# set the bot and dispatcher
bot = telegram.Bot(token=token)
dispatcher = Dispatcher(bot, None)


def reply_handler(update: Update, context: CallbackContext) -> None:
    """
    To reply the message which user send
    :param update: [Telegram.update]
    :param context: []
    :return: None
    """
    text = update.message.text
    update.message.reply_text(text)


def start(update: Update, context: CallbackContext) -> None:
    """
    To handle the situation which user send the 'start' command
    :param update:
    :param context:
    :return: None
    """
    update.message.reply_text('Hello!')


def search_course(update: Update, context: CallbackContext) -> None:
    """
    To handle the situation which user send the 'course' command
    :param update:
    :param context:
    :return: None
    """
    update.message.reply_text('目前尚有名額的課程:\n'+output_result(find_available(get_ntust_general_courses())))


def unknown_command(update: Update, context: CallbackContext) -> None:
    """
    To handle the situation which user send the unrecognized command
    :param update:
    :param context:
    :return: None
    """
    update.message.reply_text("Unrecognized command. Say what?")


# set the handler
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_handler))
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("course", search_course))
dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))


@csrf_exempt
def webhook_handler(request: WSGIRequest) -> HttpResponse:
    """
    To handle the request which telegram.org send
    :param request: [WSGIRequest] The request which the client send
    :return: [HttpResponse] Return the http status code(ex. 404, 200)
    """
    if request.method == "POST":
        update = telegram.Update.de_json(dict(json.loads(request.body)), bot)

        # Update dispatcher process that handler to process this message
        dispatcher.process_update(update)
    return HttpResponse()
