# -*- coding: utf-8 -*-
# -------------------------------------------
# CineMonster - A Quiz Bot for Telegram About Series and Movies
# @author: Edward "Toy" Facundo
# @site: http://github.com/toymak3r
# -------------------------------------------


class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite://:memory:'
    TELEGRAM_BOT_KEY = '203004059:AAGgiBh3jUzsNMNkTEcmeFGH5HpxGL2B9x8'
    LOG_FILE = 'cinemonster.log'
    QUIZ_LANG = 'en'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'
    SESSION_EXPIRATION_TIME = 30  # seconds


class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_EXPIRATION_TIME = 10  # seconds


class TestingConfig(Config):
    TESTING = True