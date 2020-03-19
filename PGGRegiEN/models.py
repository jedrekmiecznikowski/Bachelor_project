from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc =  """
The English registration form for Public Goods Game
"""


class Constants(BaseConstants):
    name_in_url = 'PGGRegiEN'
    players_per_group = 2
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass

class Player(BasePlayer):

    def role(self):
        if self.id_in_group in [1, 2]:
            return 'low'
        else:
            return 'high'

    understand = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No'],

        ],
        #widget=widgets.RadioSelect()
    )





