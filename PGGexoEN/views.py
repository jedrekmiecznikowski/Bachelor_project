from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
from .models import Constants


class IntroWaitPagePhase1(WaitPage):
    """WaitPage to continue when everyone is ready for the next phase"""
    def is_displayed(self):
        return self.round_number in Constants.phase1

    def after_all_players_arrive(self):
        self.group.set_distribution_rule()
        self.group.set_threshold()

    body_text = "Please wait"





class Phase1Intro(Page):
    """Introduction page for phase 1"""
    def is_displayed(self):
        return self.round_number == min(Constants.phase1)
    form_model = models.Player
    form_fields = ['comprehension1', 'comprehension2', 'comprehension3']
    timeout_seconds = 360











class DistributionRuleAnnounce(Page):
    timeout_seconds = 60


class Contribute(Page):
    """Players have to decide how much points to contribute."""
    form_model = models.Player
    form_fields = ['contribution']

    def set_threshold(self):
        return


class ResultsWaitPage(WaitPage):
    """"WaitPage to calculate the the payoffs."""
    def after_all_players_arrive(self):
        self.group.set_payoffs()

    body_text = "Please wait"


class Results(Page):
    """Players payoff: How much each has earned"""
    timeout_seconds = 300

    def set_payoff(self):
        return

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

    def set_payoff(self):
        return

page_sequence = [
    IntroWaitPagePhase1,
    Phase1Intro,
    DistributionRuleAnnounce,
    Contribute,
    ResultsWaitPage,
    Results,
    EarningsWaitPage,
    Earnings
]
