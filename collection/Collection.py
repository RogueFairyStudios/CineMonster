# -------------------------------------------
# CineMonster - A Quiz Bot for Telegram About Series and Movies
# @author: Edward "Toy" Facundo
# @site: http://github.com/toymak3r
# -------------------------------------------
# Collection Class
# -------------------------------------------


from miners import Miner
from random import *


class Collection:

    movie_list = ''

    def __init__(self, miner, type):
        self.miner = miner
        self.type = type

    def top_250(self):
        self.movie_list = self.miner.top_list(250)

    def general(self):
        pass

    def get_rand_movie(self):
        movie = None
        while movie is None:
            if self.type is None:
                number = str(randrange(1, 99999))
                if len(number) < 7:
                    number = '0' * (7 - len(number)) + number
                movie_id = "tt" + number  # formatting to IMDB_ID
            else:
                self.top_250()
                number = randrange(0, len(self.movie_list) - 1)
                movie_id = self.movie_list[number]['tconst']

            images, movie = self.miner.get_movie_by_id(movie_id)
            print(movie['base']['title'])
            if images is not None:
                if images['totalImageCount'] < 1:
                    movie = None

        return movie, images
