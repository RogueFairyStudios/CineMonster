# -------------------------------------------
# CineMonster - A Quiz Bot for Telegram About Series and Movies
# @author: Edward "Toy" Facundo
# @site: http://github.com/toymak3r
# -------------------------------------------
# IMDB Miner
# -------------------------------------------

from miners.Miner import Miner
from imdbpie import Imdb


class IMDB(Miner):

    def __init__(self):

        self.handle = Imdb()
        super(IMDB, self).__init__()

    def top_list(self, number):
        pop_movies = self.handle.top_250()
        return pop_movies

    def get_movie_id(self, index):
        return "tt" + index  # formatting to IMDB_ID

    def get_movie_by_id(self, movie_id):
        return self.handle.get_title_images(movie_id), self.handle.get_title(movie_id)
