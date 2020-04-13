from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants

class GroupingWaitPage(WaitPage):
    group_by_arrival_time = True

    def is_displayed(self):
        return self.round_number == 1

    body_text = "Please wait"




class IntroWaitPagePhase1(WaitPage):
    """WaitPage to continue when everyone is ready for the next phase"""
    def is_displayed(self):
        return self.round_number in Constants.phase1

    def after_all_players_arrive(self):
        self.group.set_distribution_rule()
        self.group.set_threshold()

    body_text = "Please wait"



class DistributionRuleAnnounce(Page):
    timeout_seconds = 60


class Contribute(Page):
    """Players have to decide how much points to contribute."""
    form_model = models.Player
    form_fields = ['contribution']

 #   def set_threshold(self):
  #      return


class ResultsWaitPage(WaitPage):
    """"WaitPage to calculate the the payoffs."""
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Please wait"


class Results(Page):
    """Players payoff: How much each has earned"""
    timeout_seconds = 300


    def vars_for_template(self):
        return {
            'total_earnings': self.group.total_contribution * Constants.efficiency_factor,
        }


class EarningsWaitPage(WaitPage):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

    def after_all_players_arrive(self):
        for p in self.group.get_players():
            p.set_payoff()

    body_text = "Please wait"


class Earnings(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds

class Post_Questionnaire(Page):
    """First part of post coital questionnaire"""
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    form_model = models.Player
    form_fields = ['business', 'economics', 'heard_PGG', 'reasons_explore']

class Post_Questionnaire_2(Page):
    """Second part of post coital questionnaire"""
    def is_displayed(self):
        return self.round_number == Constants.num_rounds
    form_model = models.Player
    form_fields = ['fairness', 'fairness_explore']

class Thank_you(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds



page_sequence = [
    GroupingWaitPage,
    IntroWaitPagePhase1,
    DistributionRuleAnnounce,
    Contribute,
    ResultsWaitPage,
    Results,
    EarningsWaitPage,
    Earnings,
    Post_Questionnaire,
    Post_Questionnaire_2,
    Thank_you
]
