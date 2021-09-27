import time
import os

from telegram import Update
from telegram.ext import Dispatcher, MessageHandler, Filters, CommandHandler, CallbackContext, ConversationHandler, \
    Updater

# import the search course function
from module_search_course import output_result, find_available, get_ntust_general_courses, check_available, find_mba_course


(SEARCHING, ADDING) = map(chr, range(2))  # setup the status code


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
    update.message.reply_text('目前尚有名額的課程:\n'+output_result(find_available(get_ntust_general_courses()))+output_result(find_available(find_mba_course())))


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


def alarm(context: CallbackContext) -> None:
    """
    Send the notification message.
    :param context: [telegram.ext.CallbackContext] The message callback
    :return: [int] The status code of END
    """
    job = context.job
    while not check_available(job.name.split(" ")[0]):
        time.sleep(10)
    context.bot.send_message(job.context, text=f'Your course {job.name.split(" ")[0]} is available now')


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def task(update: Update, context: CallbackContext) -> int:
    """
    The function to init the adding task
    :param update: [telegram.update] The data update
    :param context: [telegram.ext.CallbackContext] The message callback
    :return: [int] The status code to the add_task
    """
    update.message.reply_text("Please input the code of the class you want!")

    return ADDING


def add_task(update: Update, context: CallbackContext) -> int:
    """
    The function to add the task
    :param update: [telegram.update] The data update
    :param context: [telegram.ext.CallbackContext] The message callback
    :return: [int] The status code of END
    """
    chat_id = update.message.chat_id
    try:
        course_id = update.message.text
        job_removed = remove_job_if_exists(f'{str(course_id)} {chat_id}', context)
        context.job_queue.run_once(alarm, 15, context=chat_id, name=f'{str(course_id)} {chat_id}')

        text = 'Timer successfully set!'
        if job_removed:
            text += ' Old one was removed.'
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <seconds>')
    finally:
        return ConversationHandler.END


if __name__ == '__main__':

    '''
    # read the telegram bot token
    file = open("token.txt", 'r')
    token = file.read().splitlines()[0]
    file.close()
    '''

    token = os.getenv('TG_TOKEN')

    # set the bot and dispatcher
    updater = Updater(token)
    dispatcher = updater.dispatcher

    # set the ConversationHandler for the adding task
    task_conv = ConversationHandler(
        entry_points=[CommandHandler("task", task)],
        states={
            ADDING: [
                MessageHandler(Filters.regex('[A-Z]{2}[A-Z0-9]{1}[0-9]{6}'), add_task),
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

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
    dispatcher.add_handler(task_conv)
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_handler))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown_command))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()
