from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import string, random

# TODO: complete the documentation
doc = """
This is the corruption leadership game.....
"""

# Defining Constants
class Constants(BaseConstants):
    # For the main Game
    name_in_url = 'Rely_Or_Verify'
    players_per_group = 3
    num_rounds = 2
    show_up_fee = c(100) # show up fee: gets converted from points to kroner in 2 : 1 (see settings.py)
    instructions_template = 'LCG/Instructions.html'
    LoseGameChance = 0.003
    LoseGamePercent = LoseGameChance * 100
    LoseGameNegPercent = 100 - LoseGamePercent

    # Define Equation for payoffs: x = reported number, check: Rely, cheat: team cheated?, ingame = has team lost?
    def PayoffEQ(x, check, cheat):
        return c(x - (check * x / 2) - (check * cheat * x / 2))

    # For the Public Goods Game
    endowment = c(25)
    multiplier = 2


# Setting Subsession Level Data
class Subsession(BaseSubsession):
    # For Public Goods Game
    def vars_for_admin_report(self):
        contributions = [p.contribution for p in self.get_players() if p.contribution != None]
        if contributions:
            return {
                'avg_contribution': sum(contributions) / len(contributions),
                'min_contribution': min(contributions),
                'max_contribution': max(contributions),
            }
        else:
            return {
                'avg_contribution': '(no data)',
                'min_contribution': '(no data)',
                'max_contribution': '(no data)',
            }
    pass


# Defining Group level data
class Group(BaseGroup):
    group_id = models.StringField()

    ######## Rely - Verify Game ########
    # Actual Rolls
    actual_roll_p1 = models.IntegerField()
    actual_roll_p2 = models.IntegerField()

    # Fields for reported rolls
    reported_roll_p1 = models.IntegerField(
        label="What number did you roll?",
        min=0, max=6,
        doc="""Number reported by P1"""
    )

    reported_roll_p2 = models.IntegerField(
        label="What number did you roll?",
        min=0, max=6,
        doc="""Number reported by P2"""
    )

    # Leader Decision: Rely or Verify?
    checked = models.BooleanField(default = True)

    # Determining cheating
    p1_cheat = models.IntegerField()
    p2_cheat = models.IntegerField()
    team_cheated = models.IntegerField()

    # Payoff Function
    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        p3 = self.get_player_by_id(3)

        # All players get the same payoff, depending on whether they cheated or not
        if self.reported_roll_p1 == self.reported_roll_p2:
            p1.payoff = p2.payoff = p3.payoff = Constants.PayoffEQ(
                self.reported_roll_p1, self.checked, self.team_cheated)

        else:
            p1.payoff = p2.payoff = p3.payoff = c(0)


    ######### Public Goods game ########
    total_contribution = models.CurrencyField()

    individual_share = models.CurrencyField()

    max_amount = models.CurrencyField()

    # Payoff Function
    def set_payoffs_PGG(self):
        self.total_contribution = sum(
        [p.contribution for p in self.get_players()])

        for p in self.get_players():
            if all([p.ingame for x in p.in_all_rounds()]) == True:
                cumulative_payoff = sum([p.payoff for p in p.in_all_rounds()])
                self.max_amount = Constants.endowment + cumulative_payoff
            else:
                cumulative_payoff = 0
                self.max_amount = Constants.endowment + cumulative_payoff

        self.individual_share = self.total_contribution * \
            Constants.multiplier / Constants.players_per_group

        for p in self.get_players():
            p.payoff = (self.max_amount - p.contribution) + \
                self.individual_share

# Setting Player level data
class Player(BasePlayer):
    def role(self):
        return {1: 'Player 1', 2: 'Player 2', 3: "Leader"}[self.id_in_group]

    # Ingame Boolean, for losing the game
    ingame = models.BooleanField(default = True)

    age = models.IntegerField(
        label='What is your age?',
        min=18, max=90)

    gender = models.StringField(
        choices=['Male', 'Female', 'Other'],
        label='What is your gender?',
        widget=widgets.RadioSelect)

    # For Public Goods Game
    contribution = models.CurrencyField(min=0,
        doc="""The amount contributed by the player""",)


    ######## Questionnaires ########

    # Moral Identity Scale as by Aquino and Reed
    def make_field_MI(label):
        return models.IntegerField(
            choices = [1,2,3,4,5],
            label = label,
            widget = widgets.RadioSelectHorizontal
            )

    MIq1 = make_field_MI("It would make me feel good to be a person who has these characteristics.")
    MIq2 = make_field_MI("Being someone who has these characteristics is an important part of who I am.")
    MIq3 = make_field_MI("I would be ashamed to be a person who has these characteristics.")
    MIq4 = make_field_MI("Having these characteristics is not really important to me.")
    MIq5 = make_field_MI("I strongly desire to have these characteristics.")
    MIq6 = make_field_MI("I often wear clothes that identify me as having these characteristics.")
    MIq7 = make_field_MI("The types of things I do in my spare time (e.g. hobbies) clearly identify me as having these characteristics. ")
    MIq8 = make_field_MI("The kinds of books and magazines that I read identify me as having these characteristics.")
    MIq9 = make_field_MI("The fact that I have these characteristics is communicated to others by my membership in certain organizations.")
    MIq10 = make_field_MI("I am actively involved in activities that communicate to others that I have these characteristics.")


    # DOSPERT - Financial Subscale
    def make_field_DQ(label):
        return models.IntegerField(
            choices=[[1, "1"], [2, "2"], [3,"3"], [4,"4"], [5,"5"], [6, "6"], [7, "7"]],
            label=label,
            widget=widgets.RadioSelectHorizontal
            )

    Dq1 = make_field_DQ("Betting a day’s income at the horse races.")
    Dq2 = make_field_DQ("Investing 10% of your annual income in a moderate growth mutual fund.")
    Dq3 = make_field_DQ("Betting a day’s income at a high-stake poker game.")
    Dq4 = make_field_DQ("Investing 5% of your annual income in a very speculative stock.")
    Dq5 = make_field_DQ("Betting a day’s income on the outcome of a sporting event.")
    Dq6 = make_field_DQ("Investing 10% of your annual income in a new business venture.")



    # # Defining a method to make many fields # DEPRECATED - OLD SCALE!
    # def make_field(label):
    #     return models.IntegerField(
    #         choices=[[1, "1"], [2, "2"], [3,"3"], [4,"4"], [5,"5"], [6, "6"]],  # 6 point likert scale
    #         label=label,
    #         widget=widgets.RadioSelectHorizontal
    #     )
    #
    # # Moral Identity Questionnaire
    # q1 = make_field("I try hard to act honestly in most things I do.")
    # q2 = make_field("Not hurting other people is one of the rules I live by.")
    # q3 = make_field("It is important for me to treat other people fairly.")
    # q4 = make_field("I want other people to know they can rely on me.")
    # q5 = make_field("I always act in ways that do the most good and least harm to other people.")
    # q6 = make_field("If doing something will hurt another person, I try to avoid it even if no one would know.")
    # q7 = make_field("One of the most important things in life is to do what you know is right.")
    # q8 = make_field("Once I′ve made up my mind about what is the right thing to do, I make sure I do it.")
    # q9 = make_field("As long as I make a decision to do something that helps me, it does not matter much if other people are harmed.")
    # q10 = make_field("It is ok to do something you know is wrong if the rewards for doing it are great.")
    # q11 = make_field("If no one is watching or will know, it does not matter if I do the right thing.")
    # q12 = make_field("It is more important that people think you are honest than being honest.")
    # q13 = make_field("If no one could find out, it is okay to steal a small amount of money or other things that no one will miss.")
    # q14 = make_field("There is no point in going out of my way to do something good if no one is around to appreciate it.")
    # q15 = make_field("If a cashier accidentally gives me kr 10 extra change, I usually act as if I did not notice it.")
    # q16 = make_field("Lying and cheating are just things you have to do in this world. ")
    # q17 = make_field("Doing things that some people might view as not honest does not bother me.")
    # q18 = make_field("If people treat me badly, I will treat them in the same manner.")
    # q19 = make_field("I will go along with a group decision, even if I know it is morally wrong.")
    # q20 = make_field("Having moral values is worthless in today's society.")
