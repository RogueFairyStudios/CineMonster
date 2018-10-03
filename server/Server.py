# -*- coding: utf-8 -*-
# -------------------------------------------
# CineMonster - A Quiz Bot for Telegram About Series and Movies
# @author: Edward "Toy" Facundo
# @site: http://edwardfacundo.wordpress.com
# -------------------------------------------

import logging
from translations.required import *
from argparse import ArgumentParser
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

import conf
import interfaces
import session
import quiz
import player


class Server:
    logger = logging.getLogger(__name__)
    SESSIONS = dict()

    def __init__(self):
        self.config_instance = self.config_init()
        updater = Updater(self.config_instance.TELEGRAM_BOT_KEY)
        dp = updater.dispatcher

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename=self.config_instance.LOG_FILE
        )

        dp.add_handler(MessageHandler(
            [Filters.text], self.command_check_resps))
        dp.add_handler(CommandHandler("start", self.command_start))
        dp.add_handler(CommandHandler(
            "roll", self.command_roll, pass_args=True))
        dp.add_handler(CommandHandler("leaderboard", self.command_leaderboard))
        dp.add_error_handler(self.error)

        jq = updater.job_queue
        jq.put(self.update_all_timers, 1)

        self.logger.info("Started... ")

        updater.start_polling()
        updater.idle()

    def config_init(self):
        arg_parser = ArgumentParser(description="CineMonster Telegram Bot")

        arg_parser.add_argument("-e", "--env", metavar='env', type=str, default="prod",
                                help="environment to run: dev, test or prod")

        arg_parser.add_argument("-v", "--verbose", metavar='verbose', type=bool, default=False,
                                help="print information about running bot")

        args = arg_parser.parse_args()

        if args.env == "prod":
            return conf.ProductionConfig
        elif args.env == "dev":
            return conf.DevelopmentConfig
        else:
            return conf.TestingConfig

    def error(self, update, error):
        self.logger.warning('Update "%s" caused error "%s"' % (update, error))

    def update_all_timers(self, bot):
        for session in self.SESSIONS:
            self.SESSIONS[session].update_timer()
            self.SESSIONS[session].quiz.check_expiration()

    def command_start(self, bot, update):
        chat_id = update.message.chat_id
        if chat_id not in self.SESSIONS.keys():
            self.messenger = interfaces.TelegramMessenger(bot, self.logger)
            self.SESSIONS[chat_id] = session.Session(
                chat_id, self.config_instance, self.logger)
            self.SESSIONS[chat_id].set_messenger(self.messenger)
            self.SESSIONS[chat_id].quiz = quiz.Quiz(self.SESSIONS[chat_id])

    def command_roll(self, bot, update, args=''):
        chat_id = update.message.chat_id
        rand_type = args is None and args[0] or None
        self.SESSIONS[chat_id].messenger.send_msg(
            chat_id, _("searching_movies"))
        self.SESSIONS[chat_id].quiz.show(update, rand_type)

    def command_leaderboard(self, bot, update):
        chat_id = update.message.chat_id
        session = self.SESSIONS[chat_id]
        try:
            session.messenger.send_msg(chat_id, _(
                "leader_board_title"), 'highlights')
            ldb = session.get_leaderboard()
            session.messenger.send_msg(chat_id, ldb)
        except ValueError as e:
            session.messenger.send_msg(
                chat_id, update.message.from_user.first_name + e.args[0])

    def command_action(self, bot, update):
        group = update.message.chat_id
        try:
            player = player.Player(update.message.from_user.id)
            player.name = update.message.from_user.first_name + \
                " " + update.message.from_user.last_name
            self.SESSIONS[group].player_add(player)
            self.SESSIONS[update.message.chat_id].messenger.send(
                update, player.name + " entrou na partida!")
        except ValueError as e:
            self.SESSIONS[update.message.chat_id].messenger.send(
                update, update.message.from_user.first_name + e.args[0])

    def command_repeat(self, bot, update):
        movie_img = self.SESSIONS[update.message.chat_id].quiz.get_question()
        self.SESSIONS[update.message.chat_id].messenger.send(
            update, "=========REPETINDO=========")
        bot.send_photo(chat_id=update.message.chat_id,
                       photo=movie_img, caption="Qual o nome do filme/série?")
        self.SESSIONS[update.message.chat_id].messenger.send(
            update, "===========================")

    def command_cut(self, bot, update):
        group = update.message.chat_id
        try:
            player = player.Player(update.message.from_user.id)
            self.SESSIONS[group].player_quit(player)
            self.SESSIONS[update.message.chat_id].messenger.send(update,
                                                                 update.message.from_user.first_name + " saiu da partida!")
        except ValueError as e:
            self.SESSIONS[update.message.chat_id].messenger.send(
                update, update.message.from_user.first_name + e.args[0])

    def command_stop(self, bot, update):
        try:
            del (self.SESSIONS[update.message.chat_id])
            self.SESSIONS[update.message.chat_id].messenger.send(
                update, "Encerrando a partida...")
        except ValueError as e:
            self.SESSIONS[update.message.chat_id].messenger.send(
                update, "Não foi possível encerrar a partida: %s" % e)

    def command_check_resps(self, bot, update):
        self.SESSIONS[update.message.chat_id].quiz.check_resps(update)
