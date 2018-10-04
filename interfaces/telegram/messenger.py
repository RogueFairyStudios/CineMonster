import telegram.ext


class Messenger:
    bot = ''
    formats = {
        'regular': ">* %s *",
        'caption': ">* %s *<",
        'title': "=+= * %s  * =+=",
        'highlights': "--+ %s +--",
        'bold': "* %s * %s"
    }

    def __init__(self, bot, logger):
        self.logger = logger
        self.logger.debug(" Started... ")
        self.bot = bot

    def send_msg(self, chat_id, msg, type_msg='regular'):
        # TODO: trycat this
        msg = self.format(type_msg, msg)
        self.bot.send_message(chat_id=chat_id,
                              text=msg,
                              parse_mode=telegram.ParseMode.MARKDOWN)

    def format(self, type_msg, msg):
        return self.formats[type_msg] % msg

    def send_photo(self, chat_id, photo, caption):
        # TODO: trycat this
        self.bot.send_photo(chat_id=chat_id,
                            photo=photo,
                            caption=caption)
