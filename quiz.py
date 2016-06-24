# -*- coding: utf-8 -*-
# -------------------------------------------
# CineMonster - A Quiz Bot for Telegram About Series and Movies
# @author: Edward "Toy" Facundo
# @site: http://edwardfacundo.wordpress.com
# -------------------------------------------

from translations.required import *
from imdbpie import Imdb
import telegram.ext
from random import *
from player import Player


class Quiz:
    movies_type = ''
    imdb = ''
    movie = None

    def __init__(self, session):
        self.session = session
        self.imdb = Imdb()
        self.imdb = Imdb(cache=True)

    def set_level(self, level):
        pass

    def rand_movie(self, rand_type=None):
            movie_id = ''
            while self.movie is None:
                if rand_type == "pop":
                    pop_movies = self.imdb.top_250()
                    number = randrange(0, len(pop_movies) - 1)
                    movie_id = pop_movies[number]['tconst']

                if rand_type is None:
                    number = str(randrange(1, 99999))
                    if len(number) < 7:
                        number = '0' * (7 - len(number)) + number
                    movie_id = "tt"+number  # formatting to IMDB_ID

                self.movie = self.imdb.get_title_by_id(movie_id)

                if self.movie is not None:
                    if len(self.movie.trailer_image_urls) < 1:
                        self.movie = None

    def get_movie_photo(self):
        try:
            return choice(self.movie.trailer_image_urls)
        except ValueError as e:
            raise e

    def get_question(self, rand_type=None):
        try:
            self.rand_movie(rand_type)
            return self.get_movie_photo()
        except ValueError as e:
            raise(_("not_possible_find_movie"))

    def show(self, update, rand_type):
        chat_id = update.message.chat_id
        movie_img = self.get_question(rand_type)
        self.session.messenger.send_msg(chat_id, "CINEMONSTER", "title")
        self.session.messenger.send_photo(chat_id, movie_img, caption=_("question_which_movie"))
        self.session.update_counter()
        self.session.status = "running"

    def check_resps(self, update):
        chat_id = update.message.chat_id
        if str.lower(self.movie.title) == str.lower(update.message.text):
            player = Player(update.message.from_user.id)
            player.name = update.message.from_user.first_name+" "+update.message.from_user.last_name
            try:
                self.session.player_add(player)
            except ValueError as e:
                pass
            self.session.players[update.message.from_user.id].add_points(1)
            self.session.messenger.send_msg(chat_id,
                                            msg=(player.name, _("correct_answer")),
                                            type_msg='bold')
            self.movie = None

    def check_expiration(self):
        try:
            self.session.update_timer()
        except ValueError as e:
            pass
        if self.session.status == "timed_out":
            self.session.messenger.send_msg(chat_id=self.session.chat_id,
                                            msg=(_("times_up"), self.movie.title),
                                            type_msg='bold')
            self.session.status = "stop"
            self.movie = None
