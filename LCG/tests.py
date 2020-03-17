from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants

# TODO: program bot for testing


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.MyPage)
        yield (pages.Results)
