# -------------------------------------------
# CineMonster - A Quiz Bot for Telegram About Series and Movies
# @author: Edward "Toy" Facundo
# @site: http://github.com/toymak3r
# -------------------------------------------
import numpy
import textwrap
import os
import io
from abc import ABCMeta, abstractmethod


class Movie(object):

    __metaclass__ = ABCMeta

    id = 0
    name = ''  # Movie Name
    type = ''  # Movie Genre

    @abstractmethod
    def __init__(self, type):
        self.type

    def name(self):
        return self.name
