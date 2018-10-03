# -*- coding: utf-8 -*-
# -------------------------------------------
# CineMonster - A Quiz Bot for Telegram About Series and Movies
# @author: Edward "Toy" Facundo
# @site: http://github.com/toymak3r
# -------------------------------------------

from movie.Movie import Movie


class Pop(Movie):

    def __init__(self):
        self.type = "pop"
