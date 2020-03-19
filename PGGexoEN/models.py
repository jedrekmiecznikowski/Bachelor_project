from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """The English version of Public Goods Game with exogeneous threshold
"""


class Constants(BaseConstants):
    name_in_url = 'PGGexoEN'
    players_per_group = 2
    num_rounds = 2

    endowment = c(10)
    efficiency_factor = 2
    cost_parameter_low = 1
    cost_parameter_high = 1

    participation_fee = 0
    euro_per_point = 0.45

    phase1 = [1, 2]

    """"List of round numbers which are part of a distribution rule. """

    paying_phase1 = phase1

    """"The random round generator for the three payment periods to calculate money payoff."""

    thresholdexo = [25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25, 25,25]
    """"The threshold levels in each round, starting in round 1 to round 25."""


class Subsession(BaseSubsession):

    def vars_for_admin_report(self):
        contributions = [p.contribution for p in self.get_players() if p.contribution is not None]
        return {
            'total_contribution': sum(contributions),
            'min_contribution': min(contributions),
            'max_contribution': max(contributions),
        }


class Group(BaseGroup):

    distribution_rule = models.CharField()
    threshold = models.CurrencyField()
    bonus = models.CurrencyField()
    total_contribution = models.CurrencyField()
    avg_contribution = models.CurrencyField()
    avg_payoff = models.CurrencyField()

    def set_distribution_rule(self):

            self.distribution_rule = 'Equal share of the bonus'


            """"This sets the distribution rule of each phase."""

    def set_threshold(self):
        for x in range(1, 3):
            if self.round_number == x:
                self.threshold = Constants.thresholdexo[x-1]

                """the variable x is every number between 1 and 13, excluding 13.
                    When the round number is equal to the variable x, it will look
                    up the element in thresholdexo list of threshold levels."""

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.avg_contribution = self.total_contribution / Constants.players_per_group
        if self.total_contribution < self.threshold:
            self.bonus = 0
        else: self.bonus = Constants.efficiency_factor * self.threshold

        for p in self.get_players():
            if 'low' in p.role():
                p.value = (Constants.endowment - Constants.cost_parameter_low * p.contribution)
            else:
                p.value = (Constants.endowment - Constants.cost_parameter_high * p.contribution)

                """"p.value is the amount of points a player has left after contributing."""

        if self.distribution_rule == 'Equal payoff':
            if self.total_contribution < self.threshold:
                for p in self.get_players():
                    p.payoff_r = p.value
            else:
                for p in self.get_players():
                    p.payoff_r = (sum([p.value for p in self.get_players()]) + self.bonus)\
                                 / Constants.players_per_group

                    """"When threshold is met, payoff is calculated by summing the p.values,
                        adding them to the bonus, and dividing it by the amount of players 
                        per group (4 in this case)"""

                    p.check_r = p.payoff_r - p.value
                    if any(p.check_r < 0 for p in self.get_players() if p.check_r is not None):
                        self.distribution_rule = 'Equal share of the bonus exception'
                        p.payoff_r = p.value + (self.bonus / Constants.players_per_group)

                    """"An exception to the Equal payoff occurs when p.payoff_r is less
                        than p.value, resulting in a value loss for a player. In that case
                        the distribution rule is adjusted to equal share of the bonus"""

        else:
            if self.total_contribution < self.threshold:
                for p in self.get_players():
                    p.payoff_r = p.value
            else:
                for p in self.get_players():
                    p.payoff_r = p.value + (self.bonus / Constants.players_per_group)

                    """"Equal share of the bonus is calculated by adding the individual's p.value
                     with an equal share of the bonus, if the threshold is met."""

        self.avg_payoff = sum([p.payoff_r for p in self.get_players()]) / Constants.players_per_group





class Player(BasePlayer):

    def role(self):
        if self.id_in_group in [1, 2]:
            return 'low'
        else:
            return 'high'

    contribution = models.CurrencyField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player.""",
    )

    value = models.CurrencyField(
        doc=""""The player's individual payoff before bonus is taken into account."""
    )

    prule = models.PositiveIntegerField(
        choices=[
            [0, 'Equal share of the bonus'],
            [1, 'Equal payoff']
        ],
        widget=widgets.RadioSelect(),
        doc=""""The player's vote for distribution rule in phase 3."""
    )

    comprehension1 = models.PositiveIntegerField(label='If you invested 4 tokens in the public good, how much of your income do you still have left?')

    def comprehension1_error_message (self, value):
        print('values is',value)
        if value != 6:
            return "Wrong answer to question 1. Please read the instructions again"

    comprehension2 = models.FloatField(label='There are 10 people in your group. Your income (endowment) is 10 tokens. The public good threshold is 25 tokens. The group bonus for achieving the threshold is 50 tokens, equally divided between the group, e.g. 5 tokens for each player. You have contributed 3,5 tokens towards the public good. The contributions of the other 9 people in your group are as follows {0; 2.5; 3; 0; 2; 2.5; 3; 3; 4}. What is your payoff for this round?')

    def comprehension2_error_message (self, value):
        print('value is',value)
        if value != 7.5:
            return "Wrong answer to question 2. Please read the instructions again. Remember that if the threshold is not reached - no bonus is paid and the investments are not refunded."

    comprehension3 = models.PositiveIntegerField(label='If you invested 4 tokens in the public good, how much of your income do you still have left?')

    def comprehension3_error_message (self, value):
        print('value is',value)
        if value != 10:
            return "Wrong answer to question 3. Please read the instructions again. Remember that if the threshold is reached - equal bonus is paid to every member of the group."


    payoff_r = models.CurrencyField(
        doc=""""payoff in a certain round"""
    )

    check_r = models.FloatField(
        doc=""""The check for Equal payoff viability, if negative value,
         it's not viable"""
    )

    earnings_phase1 = models.CurrencyField()
    paid = models.CurrencyField()

    def set_payoff(self):
        self.earnings_phase1 = self.in_round(1).payoff_r+self.in_round(2).payoff_r
        self.payoff = self.earnings_phase1
        self.paid = (self.payoff * Constants.euro_per_point) + Constants.participation_fee

        """"The calculation of the payoffs during the random periods
            and total earnings as well as the to be paid amount."""