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
    players_per_group = 5
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
        #widget=widgets.RadioSelectHorizontal
    )
    consent = models.BooleanField(

        choices=[
            [True, 'Yes'],
            [False, 'No'],

        ],
        #widget=widgets.RadioSelectHorizontal
    )
    sona_id = models.StringField(
        label = "Input your SONA Identity Code (it's written in all emails you got from us about the study)"
    )
    student = models.BooleanField(
        label="Are you currently a student at a higher education facility (e.g. Aarhus University) or did you finish your studies at one?",
        choices=[
            [True, 'Yes'],
            [False, 'No'],

        ],
        widget=widgets.RadioSelectHorizontal
    )
    business = models.BooleanField(
        label = "Do you or did you study one of the following programmes: "
                 "Economics and Business Administration, BSc; Erhvervsøkonomi, HA; Erhvervsøkonomi med tilvalg; Erhvervsøkonomi og erhvervsret(HA(jur.)); Economics and Business Administration, MSc (cand.merc)?",
        choices=[
            [True, 'Yes'],
            [False, 'No'],

        ],
        widget=widgets.RadioSelectHorizontal
    )
    economics = models.BooleanField(
        label = "Do you or did you study one of the following programmes: Økonomi; Politik og økonomi; Matematik-økonomi?",
        choices=[
            [True, 'Yes'],
            [False, 'No'],

        ],
        widget=widgets.RadioSelectHorizontal
    )
    semester = models.IntegerField(
        label="Which semester are you on or how many semesters did you complete at a higher education facility?",
        min=0, max=20,
    )
    gender = models.PositiveIntegerField(
        label="What’s your gender?",
        choices=[
            [0, 'Female'],
            [1, 'Male'],
            [2,'Other'],
        ],
        widget=widgets.RadioSelect(),
    )
    comprehension1 = models.PositiveIntegerField(label='If you invested 30 tokens in the public good, how much of your income do you still have left (before the payment of the bonus or refund of the contributions)?')

    def comprehension1_error_message (self, value):
        print('values is',value)
        if value != 25:
            return "Wrong answer to question 1. Please read the instructions again. You can download them at the bottom of the page."

    comprehension2 = models.PositiveIntegerField(label='There are 5 people in your group, including you. Your income is 55 tokens. The public good threshold is 125 tokens. The group bonus for achieving the threshold is 250 tokens, equally divided between the group, e.g. 25 tokens for each player. You have contributed 25 tokens towards the public good. The contributions of the other 4 people in your group are as follows {10;25;30;20}. What is your payoff for this round?')

    def comprehension2_error_message (self, value):
        print('value is',value)
        if value != 55:
            return "Wrong answer to question 2. Please read the instructions again. You can download them at the bottom of the page. Remember that if the threshold is not reached - no bonus is paid and the contributions are refunded."

    comprehension3 = models.PositiveIntegerField(label='The number of people, threshold, your income and contributions of the other people are the same as in question 2. Your contribution is different - it is 40 tokens. What is your payoff for this round?')

    def comprehension3_error_message (self, value):
        print('value is',value)
        if value != 60:
            return "Wrong answer to question 3. Please read the instructions again. You can download them at the bottom of the page. Remember that if the threshold is reached - equal share of the bonus is paid to every member of the group."

