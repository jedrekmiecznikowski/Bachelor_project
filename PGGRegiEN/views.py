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

class Pre_Questionnaire(Page):
    "Pre study questionnaire (demographics, study programme, ...)"
    def is_displayed(self):
        return self.round_number == 1  # only show page at the first round
    form_model = "player"
    form_fields = ["sona_id", "student", "semester", "gender"]
    pass
class Consent_form(Page):
    """Consent form pending signature for processing data"""
    def is_displayed(self):
        return self.round_number == 1  # only show page at the first round
    form_model = "player"
    form_fields = ["consent"]
    def error_message (self, values):
        print('values is',values)
        if values['consent'] == False:
            return "If you are sure you want to withdraw from this study and give up your compensation, email 201811497@post.au.dk now"
    pass
class Comprehension(Page):
    """Comprehension questions"""
    def is_displayed(self):
        return self.round_number == 1
    form_model = models.Player
    form_fields = ['comprehension1', 'comprehension2', 'comprehension3']
    timeout_seconds = 360

page_sequence = [
    Instructions,
    Consent_form,
    Pre_Questionnaire,
    Introduction,
    Comprehension
]
