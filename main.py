# -*- coding: utf-8 -*-
# -------------------------------------------
# CineMonster - A Quiz Bot for Telegram About Series and Movies
# @author: Edward "Toy" Facundo
# @site: http://edwardfacundo.wordpress.com
# -------------------------------------------

import logging

from translations.required import *
from conf import config
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from argparse import ArgumentParser
from session import Session
from messenger import Messenger
from player import Player
from quiz import Quiz

SESSIONS = dict()

global logger
logger = logging.getLogger(__name__)

""" configuration instance shared """
config_instance = ''


def main():
    global config_instance

    arg_parser = ArgumentParser(description="CineMonster Telegram Bot")

    arg_parser.add_argument("-e", "--env", metavar='env',
                            type=str, default="prod",
                            help="environment to run: dev, test or prod")

    arg_parser.add_argument("-v", "--verbose", metavar='verbose',
                            type=bool, default=False,
                            help="print information about running bot")

    args = arg_parser.parse_args()

    if args.env == "prod":
        config_instance = config.ProductionConfig
    if args.env == "dev":
        config_instance = config.DevelopmentConfig
    if args.env == "test":
        config_instance = config.TestingConfig

    updater = Updater(config_instance.TELEGRAM_BOT_KEY)
    dp = updater.dispatcher

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=config_instance.LOG_FILE)

    dp.add_handler(MessageHandler([Filters.text], command_check_resps))
    dp.add_handler(CommandHandler("start", command_start))
    dp.add_handler(CommandHandler("roll", command_roll, pass_args=True))
    dp.add_handler(CommandHandler("leaderboard", command_leaderboard))
    # dp.add_handler(CommandHandler("action", command_action))
    # dp.add_handler(CommandHandler("repeat", command_repeat))
    # dp.add_handler(CommandHandler("cut", command_cut))
    # dp.add_handler(CommandHandler("stop", command_stop))
    dp.add_error_handler(error)

    jq = updater.job_queue
    jq.put(update_all_timers, 1)

    logger.info("Started... ")

    updater.start_polling()
    updater.idle()


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def command_start(bot, update):
    chat_id = update.message.chat_id
    if chat_id not in SESSIONS.keys():
        messenger = Messenger(bot, logger)
        SESSIONS[chat_id] = Session(chat_id, config_instance, logger)
        SESSIONS[chat_id].set_messenger(messenger)
        SESSIONS[chat_id].quiz = Quiz(SESSIONS[chat_id])


def command_roll(bot, update, args=''):
        chat_id = update.message.chat_id
        rand_type = args is None and args[0] or None
        SESSIONS[chat_id].messenger.send_msg(chat_id, _("searching_movies"))
        SESSIONS[chat_id].quiz.show(update, rand_type)


def command_leaderboard(bot, update):
    chat_id = update.message.chat_id
    session = SESSIONS[chat_id]
    try:
        session.messenger.send_msg(chat_id, _("leader_board_title"), 'highlights')
        ldb = session.get_leaderboard()
        session.messenger.send_msg(chat_id, ldb)
    except ValueError as e:
        session.messenger.send_msg(chat_id, update.message.from_user.first_name+e.args[0])


def command_action(bot, update):
    group = update.message.chat_id
    try:
        player = Player(update.message.from_user.id)
        player.name = update.message.from_user.first_name+" "+update.message.from_user.last_name
        SESSIONS[group].player_add(player)
        SESSIONS[update.message.chat_id].messenger.send(update, player.name+" entrou na partida!")
    except ValueError as e:
        SESSIONS[update.message.chat_id].messenger.send(update, update.message.from_user.first_name+e.args[0])


def command_repeat(bot, update):
    movie_img = SESSIONS[update.message.chat_id].quiz.get_question()
    SESSIONS[update.message.chat_id].messenger.send(update, "=========REPETINDO=========")
    bot.send_photo(chat_id=update.message.chat_id, photo=movie_img, caption="Qual o nome do filme/série?")
    SESSIONS[update.message.chat_id].messenger.send(update, "===========================")


def command_cut(bot, update):
    group = update.message.chat_id
    try:
        player = Player(update.message.from_user.id)
        SESSIONS[group].player_quit(player)
        SESSIONS[update.message.chat_id].messenger.send(update, update.message.from_user.first_name+" saiu da partida!")
    except ValueError as e:
        SESSIONS[update.message.chat_id].messenger.send(update, update.message.from_user.first_name+e.args[0])


def command_stop(bot, update):
    try:
        del(SESSIONS[update.message.chat_id])
        SESSIONS[update.message.chat_id].messenger.send(update, "Encerrando a partida...")
    except ValueError as e:
        SESSIONS[update.message.chat_id].messenger.send(update, "Não foi possível encerrar a partida: %s" % e)


def command_check_resps(bot, update):
    SESSIONS[update.message.chat_id].quiz.check_resps(update)


def update_all_timers(bot):
    for session in SESSIONS:
        SESSIONS[session].update_timer()
        SESSIONS[session].quiz.check_expiration()


if __name__ == '__main__':
    main()

