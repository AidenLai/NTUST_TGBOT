from django.core.handlers.wsgi import WSGIRequest
from django.shortcuts import render

# Create your views here.

import json
import telegram
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler, CallbackContext, ConversationHandler

# import the search course function
from courseQuery.module_search_course import output_result, find_available, get_ntust_general_courses

# read the telegram bot token
file = open("courseQuery/token.txt", 'r')
token = file.read().splitlines()[0]
file.close()

# set the bot and dispatcher
bot = telegram.Bot(token=token)
dispatcher = Dispatcher(bot, None)


SEARCHING = chr(1)  # setup the status code


def reply_handler(update: Update, context: CallbackContext) -> None:
    """
    To reply the message which user send
    :param update: [telegram.update] The data update
    :param context: [telegram.ext.CallbackContext] The message callback
    :return: None
    """
    text = update.message.text
    update.message.reply_text(text)


def start(update: Update, context: CallbackContext) -> None:
    """
    To handle the situation which user send the 'start' command
    :param update: [telegram.update] The data update
    :param context: [telegram.ext.CallbackContext] The message callback
    :return: None
    """
    text = (
        "Welcome! This is NTUST course assist bot. You can use the command '/course' to query the "
        "available course. And you can the command '/search' to search the specific course you want."
    )
    update.message.reply_text(text)


def search_course(update: Update, context: CallbackContext) -> None:
    """
    To handle the situation which user send the 'course' command
    :param update: [telegram.update] The data update
    :param context: [telegram.ext.CallbackContext] The message callback
    :return: None
    """
    update.message.reply_text('目前尚有名額的課程:\n'+output_result(find_available(get_ntust_general_courses())))


def unknown_command(update: Update, context: CallbackContext) -> None:
    """
    To handle the situation which user send the unrecognized command
    :param update: [telegram.update] The data update
    :param context: [telegram.ext.CallbackContext] The message callback
    :return: None
    """
    update.message.reply_text("Unrecognized command. Say what?")


def search(update: Update, context: CallbackContext) -> int:
    """
    init the search function
    :param update: [telegram.update] The data update
    :param context: [telegram.ext.CallbackContext] The message callback
    :return: [int] Status code
    """
    update.message.reply_text("Please input the course code.")

    return SEARCHING


def search_handler(update: Update, context: CallbackContext) -> int:
    """
    check the course if available
    :param update: [telegram.update] The data update
    :param context: [telegram.ext.CallbackContext] The message callback
    :return: [int] The end status code
    """
    data = []
    for course in find_available(get_ntust_general_courses()):
        data.append(course['CourseNo'])
    if update.message.text in data:
        update.message.reply_text("Available")
    else:
        update.message.reply_text("Not Available")

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """
    The quit function of a conversation
    :param update: [telegram.update] The data update
    :param context: [telegram.ext.CallbackContext] The message callback
    :return: [int] The status code of END
    """
    update.message.reply_text("bye!")
    return ConversationHandler.END


# set the ConversationHandler for the searching function conversation
search_conv = ConversationHandler(
    entry_points=[CommandHandler("search", search)],
    states={
        SEARCHING: [
            MessageHandler(Filters.regex('[A-Z]{2}[A-Z0-9]{1}[0-9]{6}'), search_handler),
            MessageHandler(Filters.text & ~Filters.command, search)
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)


# set the handler
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("course", search_course))
dispatcher.add_handler(search_conv)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_handler))
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
