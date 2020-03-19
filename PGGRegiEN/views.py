from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants
class Instructions(Page):
    """Description of the game: How to play and returns expected"""
    def is_displayed(self):
        return self.round_number == 1
class Introduction(Page):
    """Description of the game: How to play and returns expected"""
    def is_displayed(self):
        return self.round_number == 1
    form_model = models.Player
    form_fields = ['understand']

    def error_message (self, values):
        print('values is',values)
        if values['understand'] == False:
            return "Read the instructions again"


page_sequence = [
    Instructions,
    Introduction
]
