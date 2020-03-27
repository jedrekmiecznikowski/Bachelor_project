from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """The English version of Public Goods Game with exogeneous threshold
"""


class Constants(BaseConstants):
    name_in_url = 'PGGexoEN'
    players_per_group = 5
    num_rounds = 25

    endowment = c(55)
    efficiency_factor = 2 #step return
    cost_parameter_low = 1 #useless because no high/low players
    cost_parameter_high = 1 #ibid

    participation_fee = 0
    euro_per_point = 0.0647058823529412

    phase1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

    """"List of round numbers which are part of a distribution rule. """

    paying_phase1 = phase1

    """"The random round generator for the three payment periods to calculate money payoff."""

    thresholdexo = [125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125, 125]
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
        for x in range(1, 26):
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
                    p.payoff_r = p.value + p.contribution
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


    payoff_r = models.CurrencyField(
        doc=""""payoff in a certain round"""
    )

    check_r = models.FloatField(
        doc=""""The check for Equal payoff viability, if negative value,
         it's not viable"""
    )

    heard_PGG = models.BooleanField(
        label="Have you previously heard of a “public goods game”? ",
        choices=[
            [True, 'Yes'],
            [False, 'No'],

        ],
        widget=widgets.RadioSelectHorizontal
    )

    fairness = models.PositiveIntegerField(
        label="What is a 'fair' contribution in the public good? (number)",
        min=0, max=Constants.endowment
    )

    fairness_explore = models.TextField(
        label="Are you concerned about 'fairness' in making your contribution decision? Please elaborate briefly on your idea of 'fairness' and how important it is to you"
    )

    reasons_explore = models.TextField(
        label="Please state the reasons for your contributions. Elaborate on your motives, why did you make the decisions you did? Which of the reasons was the most important? "
    )

    earnings_phase1 = models.PositiveIntegerField()
    paid = models.PositiveIntegerField()


    def set_payoff(self):
        # must add all rounds one by one to self.earnings_phase1
        self.earnings_phase1 = self.in_round(1).payoff_r+self.in_round(2).payoff_r+self.in_round(3).payoff_r+self.in_round(4).payoff_r+self.in_round(5).payoff_r+self.in_round(6).payoff_r+self.in_round(7).payoff_r+self.in_round(8).payoff_r+self.in_round(9).payoff_r+self.in_round(10).payoff_r+self.in_round(11).payoff_r+self.in_round(12).payoff_r+self.in_round(13).payoff_r+self.in_round(14).payoff_r+self.in_round(15).payoff_r+self.in_round(16).payoff_r+self.in_round(17).payoff_r+self.in_round(18).payoff_r+self.in_round(19).payoff_r+self.in_round(20).payoff_r+self.in_round(21).payoff_r+self.in_round(22).payoff_r+self.in_round(23).payoff_r+self.in_round(24).payoff_r+self.in_round(25).payoff_r
        self.payoff = self.earnings_phase1
        self.paid = (self.payoff * Constants.euro_per_point) + Constants.participation_fee

        """"The calculation of the payoffs during the random periods
            and total earnings as well as the to be paid amount."""

