import logging
import os
import asyncio
import telegram.ext

from process import GPT3Conversation

PORT = int(os.environ.get('PORT', '8443'))

with open('token.txt', 'r') as f:
    TOKEN = str(f.read()).strip().replace('\n', '')

session = {}

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    reply_keyboard = [["/start"]]  # "/help", "/about"]] "/contact"]]
    #    df = pd.read_csv('db.csv')
    # if update.message.from_user.id not in df.Conversation_ID.unique():

    update.message.reply_text("Hello! Welcome to Your Best Companion Bot. "
                              "Please provide initial context, i.e. Name, Age, Interests, Profession, Gender.")
    if update.message.from_user.id in session:
        del session[update.message.from_user.id]


def handle_context(update, context):
    # global bot_context
    # df = pd.read_csv('db.csv')
    # if update.message.from_user.id not in df.Conversation_ID.unique():
    try:
        if update.message.from_user.id not in session:
            print(update.message.text.split(','))
            name, age, interests, profession, gender = update.message.text.split(",")

            session[update.message.from_user.id] = GPT3Conversation(name, age, interests, profession, gender)

            bot_context = f"You are talking to :\nName: {name}\nAge: {age}\nInterests: {interests}\nProfession: {profession}\nGender: {gender}\n\nPlease initiate the discussion with your companion {name}"
            update.message.reply_text(bot_context)

        else:
            handle_message(update, context)
    except Exception as e:
        print(e)
        update.message.reply_text("Invalid context format. Please provide context in the format: Name, Age, "
                                  "Interests, Profession, Gender")


def error(update, context):
    logger.warning('Update "%s" caused error "%s"', context)


def handle_message(update, context):
    # df = pd.read_csv('db.csv')
    # chat_log = session.get('chat_log')
    # print('0', chat_log)
    # if update.message.from_user.id in df.Conversation_ID.unique():
    #    bot_context = df[df.Conversation_ID == update.message.from_user.id].Message[0]
    #    chat_log = bot_context
    #    #print('1',chat_log)
    # print('2', chat_log)
    answer = session[update.message.from_user.id].ask(update.message.text)
    # print('Man:', update.message.text, 'Woman:', answer)

    # session['chat_log'] = append_interaction_to_chat_log(update.message.text, answer, chat_log)
    update.message.reply_text(f"{answer}")


async def main():
    updater = telegram.ext.Updater(TOKEN, use_context=True)
    bot = updater.dispatcher

    bot.add_handler(telegram.ext.CommandHandler("start", start, run_async=True))
    bot.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_context, run_async=True))
    # bot.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, handle_message))
    # bot.add_handler(telegram.ext.CommandHandler("help", help))
    # bot.add_handler(telegram.ext.CommandHandler("about", about))
    # bot.add_handler(telegram.ext.CommandHandler("contact", contact))

    bot.add_error_handler(error)
    updater.start_polling()

    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN,
        webhook_url='https://web3taskbot.herokuapp.com/' + TOKEN
    )

    updater.idle()


if __name__ == '__main__':
    asyncio.run(main())
