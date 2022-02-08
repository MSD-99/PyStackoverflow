
from loguru import logger
import emoji

from src.db import mongodb
from src.utils.constants import Keyboards
from src.utils.io import proxy, read_json, write_json
from src.utils.constants import Keyboards, Keys, States
from src.filters import IsAdmin
from src.bot import bot

class Bot:
    """
    Template  for telegram bot.
    """
    def __init__(self, Telebot, Db) -> None:
        # self.proxy = '123.231.226.114:47562'
        # proxy(proxy_url=self.proxy, type='HTTPS')

        self.bot =  Telebot
        self.db = Db
        # add mustom filter
        self.bot.add_custom_filter(IsAdmin())

        # register handler
        self.handlers()

        # run bot
        logger.info('Bot is running...')
        self.bot.infinity_polling()

        self.echo_all = self.bot.message_handler(\
            func=lambda message: True)\
            (self.echo_all)

    def handlers(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            """
            Welcome Message
            """
            self.send_message(
                message.chat.id,
                f"Hey <strong> {message.chat.first_name} </strong>",
                reply_markup=Keyboards.main
                )

            self.db.users.update_one(
                {'chat.id': message.chat.id},
                {'$set': message.json},
                upsert=True
                )
            self.upadte_state(chat_id=message.chat.id, state=States.main)

        @self.bot.message_handler(is_admin=True)
        def admin_of_group(message):
             self.send_message(message.chat.id, 'You are admin of this group')

        @self.bot.message_handler(func=lambda _: True)
        def echo(message):
            self.send_message(
            message.chat.id,
            message.text,
            reply_markup=Keyboards.main
            )

    def send_message(self, chat_id, text, reply_markup=None, emojize=True):
        """
        Send message to telegram bot.
        """
        if emojize:
            text = emoji.emojize(text, use_aliases=True)

        self.bot.send_message(chat_id, text, reply_markup=reply_markup)


        def upadte_state(self, chat_id, state):
            """
            Update user state.
            """

            self.db.users.update_one(
                {"chat.id": chat_id},
                {"$set": {"state": state}},
            )

if __name__ == '__main__':
    logger.info('Bot started!')
    bot  = Bot(Telebot=bot, Db=mongodb)
    bot.run()
