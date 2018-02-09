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
from commands import *

SESSIONS = dict()

global logger
logger = logging.getLogger(__name__)

""" configuration instance shared """
config_instance = ''


def main():
    global SESSIONS
    global config_instance

    config_instance = config_init()

    updater = Updater(config_instance.TELEGRAM_BOT_KEY)
    dp = updater.dispatcher

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        filename=config_instance.LOG_FILE
    )

    dp.add_handler(MessageHandler([Filters.text], command_check_resps))
    dp.add_handler(CommandHandler("start", command_start))
    dp.add_handler(CommandHandler("roll", command_roll, pass_args=True))
    dp.add_handler(CommandHandler("leaderboard", command_leaderboard))
    dp.add_error_handler(error)

    jq = updater.job_queue
    jq.put(update_all_timers, 1)

    logger.info("Started... ")

    updater.start_polling()
    updater.idle()


def config_init():

    arg_parser = ArgumentParser(description="CineMonster Telegram Bot")

    arg_parser.add_argument("-e", "--env", metavar='env', type=str, default="prod",
                            help="environment to run: dev, test or prod")

    arg_parser.add_argument("-v", "--verbose", metavar='verbose', type=bool, default=False,
                            help="print information about running bot")

    args = arg_parser.parse_args()

    if args.env == "prod":
        return config.ProductionConfig
    elif args.env == "dev":
        return config.DevelopmentConfig
    else:
        return config.TestingConfig


def error(update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def update_all_timers(bot):
    global SESSIONS
    for session in SESSIONS:
        SESSIONS[session].update_timer()
        SESSIONS[session].quiz.check_expiration()


if __name__ == '__main__':
    main()