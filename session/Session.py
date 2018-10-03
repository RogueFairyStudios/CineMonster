# -------------------------------------------
# CineMonster - A Quiz Bot for Telegram About Series and Movies
# @author: Edward "Toy" Facundo
# @site: http://edwardfacundo.wordpress.com
# -------------------------------------------

import datetime
import time


class Session:
    quiz = ''
    players = dict()
    started = ''
    ended = ''
    status = ''
    messenger = ''
    bot = ''
    expiration = 30  # default
    counter = 0
    chat_id = 0
    config = ''

    def __init__(self, chat_id, config, logger):
        self.logger = logger
        self.started = datetime.datetime.utcnow()
        self.chat_id = chat_id
        self.config = config
        self.expiration = self.config.SESSION_EXPIRATION_TIME

    def player_add(self, player):
        if player.id not in self.players.keys():
            self.players[player.id] = player
        else:
            self.update_log()
            raise ValueError(' já está na partida...')

    def player_quit(self, player):
        del(self.players[player.id])

    def end(self):
        self.ended = datetime.datetime.utcnow()

    def get_leaderboard(self):
        ldb = ''
        for x in self.players:
            ldb += self.players[x].name+" : " + \
                str(self.players[x].get_points())+" \n"
        return ldb

    def set_messenger(self, messenger):
        self.messenger = messenger

    def update_timer(self):
        if self.status == "running":
            t = self.update_log()
            if t.seconds > self.expiration:
                self.status = "timed_out"

    def update_counter(self):
        self.counter = datetime.datetime.utcnow()
        self.logger.debug(str(self.chat_id)+" : " +
                          "updater_counter: "+str(self.counter))

    def update_log(self):
        t = datetime.datetime.utcnow() - self.counter
        self.logger.debug(str(self.chat_id) + " : " +
                          "updater_timer: " + str(t))
        return t
