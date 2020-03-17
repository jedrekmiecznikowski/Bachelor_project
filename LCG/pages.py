"""This defines the pages, i.e. the different stages of the game, what players will see.
The way the game progresses is set by the page_sequence defined at the end.

Rough Draft:
1. Introduction (Consent, ...)
2. Examples
3. Demographics and Moral Character tests..?
4. Player 1 page
5. Player 2 pages
6. Player 3 (leader) page
7. Results page # pages 4-7 get looped.
8. End Results
9. Second Stage: one shot public goods Game
"""

from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import random, string

class Welcome(Page):
    "Page introducing the general rules and structure of the experiment"
    def is_displayed(self):
        return self.round_number == 1  # only show page at the first round
    pass

    def vars_for_template(self):
        return {
        'show_up_fee_kr': Constants.show_up_fee.to_real_world_currency(self.session)
        }


class Introduction(Page):
    "Page introducing the general rules and structure of the first game"
    def is_displayed(self):
        return self.round_number == 1  # only show page at the first round
    pass


class Pre_Questionnaire(Page):
    "Pre study questionnaire (demographics, moral identity questionnaire, ...)"
    def is_displayed(self):
        return self.round_number == 1  # only show page at the first round
    form_model = "player"
    form_fields = ["age", "gender"]
    pass


class Moral_Identity(Page):
    "Pre study questionnaire (moral identity questionnaire, ...)"
    def is_displayed(self):
        return self.round_number == Constants.num_rounds  # only show page at the last round
    form_model = "player"
    form_fields = ["MIq1","MIq2","MIq3","MIq4","MIq5","MIq6","MIq7","MIq8","MIq9","MIq10"]
    # form_fields = ["q1","q2","q3","q4","q5","q6","q7","q8","q9","q10","q11","q12","q13","q14","q15","q16","q17","q18","q19","q20"]
    pass

class DOSPERT(Page):
    "Pre study questionnaire (moral identity questionnaire, ...)"
    def is_displayed(self):
        return self.round_number == Constants.num_rounds  # only show page at the last round
    form_model = "player"
    form_fields = ["Dq1","Dq2","Dq3","Dq4","Dq5","Dq6"]
    pass


class Examples(Page):
    "Giving examples of the game"
    def is_displayed(self):
        return self.round_number == 1  # only show page at the first round
    pass

class WaitForPlayers(WaitPage):
    def is_displayed(self):
        return self.round_number == 1

    title_text = "The game will start after all players have read the instructions. Waiting for other players to finish..."

    def after_all_players_arrive(self):
        self.group.group_id = ''.join(random.sample(string.ascii_lowercase, 9))
        pass

class Rolls(WaitPage):
    def is_displayed(self):
        if all([p.ingame for p in self.player.in_all_rounds()]) == True:
            return self
        else:
            return False
    "Set die rolls for both players"
    def after_all_players_arrive(self):
        # for debugging purposes, set dice rolls manually
        # self.group.actual_roll_p1 = 3
        # self.group.actual_roll_p2 = 3

        # random roll of die for both players
        self.group.actual_roll_p1 = random.randint(1, 6)
        self.group.actual_roll_p2 = random.randint(1, 6)

        # print rolls to console
        print(self.group.actual_roll_p1, self.group.actual_roll_p2)

        for player in self.group.get_players():
            print("Ingame status: ", [p.ingame for p in player.in_all_rounds()])
            print("Overall ingame ", all([p.ingame for p in player.in_all_rounds()]))
    pass

class P1_Roll(Page):
    "This page is only for P1: P1 rolls first die, reports that to P2"
    def is_displayed(self):
        if self.round_number == 1 and self.player.id_in_group == 1:
            return self
        elif self.player.id_in_group == 1 and all([p.ingame for p in self.player.in_all_rounds()]) == True:
            return self
        else:
            return False

    form_model = 'group'
    form_fields = ['reported_roll_p1']

    def vars_for_template(self):
        actual_roll_p1 = self.group.actual_roll_p1
        return {"actual_roll_p1": actual_roll_p1,
                # "image_path": "LCG/dice/Dice_{}.JPG".format(self.group.actual_roll_p1)
                "video_path_mp4": "LCG/dice_vids/{}.mp4".format(self.group.actual_roll_p1),
                "video_path_wmv": "LCG/dice_vids/{}.wmv".format(self.group.actual_roll_p1)
                }
    pass


class RollWaitPage(WaitPage):
    pass


class P2_Roll(Page):
    "This page is only for P2. P2 receives information from Player 1. P2 rolls die. P2 reports roll to Leader"
    def is_displayed(self):
        if self.round_number == 1 and self.player.id_in_group == 2:
            return self
        elif self.player.id_in_group == 2 and all([p.ingame for p in self.player.in_all_rounds()]) == True:
            return self
        else:
            return False

    form_model = 'group'
    form_fields = ['reported_roll_p2']

    def vars_for_template(self):
        reported_roll_p1 = self.group.reported_roll_p1
        actual_roll_p2 = self.group.actual_roll_p2
        return {"reported_roll_p1": reported_roll_p1,
                "actual_roll_p2": actual_roll_p2,
                # "image_path": "LCG/dice/Dice_{}.JPG".format(self.group.actual_roll_p2),
                "video_path_mp4": "LCG/dice_vids/{}.mp4".format(self.group.actual_roll_p2),
                "video_path_wmv": "LCG/dice_vids/{}.wmv".format(self.group.actual_roll_p2)}


class Leader_Page(Page):
    """This page is only for the leader.
    The leader receives the team report and then plays a rely or verify game"""

    def is_displayed(self):
        if self.round_number == 1 and self.player.id_in_group == 3 and self.group.reported_roll_p1 == self.group.reported_roll_p2:
            return self
        elif self.player.id_in_group == 3 and self.group.reported_roll_p1 == self.group.reported_roll_p2 and all([p.ingame for p in self.player.in_all_rounds()]) == True:
            return self
        else:
            return False

    def vars_for_template(self):
        reported_roll_p1 = self.group.reported_roll_p1
        reported_roll_p2 = self.group.reported_roll_p2
        return {"reported_roll_p1": reported_roll_p1, "reported_roll_p2": reported_roll_p2}

    form_model = 'group'
    form_fields = ['checked']


class ResultsWaitPage(WaitPage):
    "Compute payoff, and record cheating and verifying (checking) if it happened"
    def is_displayed(self):
        if all([p.ingame for p in self.player.in_all_rounds()]) == True:
            return self
        else:
            return False

    def after_all_players_arrive(self):
        # Determine whether Player 1 cheated
        if self.group.reported_roll_p1 != self.group.actual_roll_p1:
            self.group.p1_cheat = 1
        else:
            self.group.p1_cheat = 0

        # Determine whether Player 2 cheated
        if self.group.reported_roll_p2 != self.group.actual_roll_p2:
            self.group.p2_cheat = 1
        else:
            self.group.p2_cheat = 0

        # Determine whether the group cheated
        if self.group.p1_cheat == 1 or self.group.p2_cheat == 1:
            self.group.team_cheated = 1
        else:
            self.group.team_cheated = 0

        # Print ingame status for debugging purposes
        print("Results Waiting Page 1")
        for player in self.group.get_players():
            print("Ingame status for all rounds: ", [p.ingame for p in player.in_all_rounds()])


        # Set ingame status based on leader checking, team cheating, and random chance
        if self.group.checked == False and self.group.team_cheated == 1 and random.random() <= Constants.LoseGameChance:
            for player in self.group.get_players():
                player.ingame = False
        else:
            for player in self.group.get_players():
                player.ingame = True

        self.group.set_payoffs()

        # Print ingame status for debugging
        print("Results Waiting Page 2")
        for player in self.group.get_players():
            print("Ingame status for all rounds: ", [p.ingame for p in player.in_all_rounds()])

    pass


class Results(Page):
    """This page displays the earnings of each player"""
    def is_displayed(self):
        if all([p.ingame for p in self.player.in_all_rounds()]) == True:
            return self
        else:
            return False

    def vars_for_template(self):
        actual_roll_p1 = self.group.actual_roll_p1
        actual_roll_p2 = self.group.actual_roll_p2
        cumulative_payoff = sum(
            [p.payoff for p in self.player.in_all_rounds()])

        return {
            "actual_roll_p1": actual_roll_p1,
            "actual_roll_p2": actual_roll_p2,
            "cumulative_payoff": cumulative_payoff
        }


class LostGame(Page):
    """This page is only shown if a team loses"""

    def is_displayed(self):
        if self.player.ingame == False and self.group.reported_roll_p1 != None:
            return self
        else:
            return False


class FinalEvaluation(Page):
    "This is the end of the rely and verify game"
    def is_displayed(self):
        if self.round_number == Constants.num_rounds and all([p.ingame for p in self.player.in_all_rounds()]) == True:
            return self
        else:
            return False

    def vars_for_template(self):
        cumulative_payoff = sum([p.payoff for p in self.player.in_all_rounds()])

        return {"cumulative_payoff": cumulative_payoff}



class PGGInstructions(Page):
    "Instruct players for one shot PGG"
    def is_displayed(self):
        if self.round_number == Constants.num_rounds:
            return self
        else:
            return False

    def vars_for_template(self):
        if all([p.ingame for p in self.player.in_all_rounds()]) == True:
            cumulative_payoff = sum([p.payoff for p in self.player.in_all_rounds()])
            max_amount = Constants.endowment + cumulative_payoff
        else:
            cumulative_payoff = 0
            max_amount = Constants.endowment + cumulative_payoff

        return {"cumulative_payoff": cumulative_payoff,
                "max_amount": max_amount,
                'example1_sum': max_amount * 3,
                'example1_doubled': (max_amount * 3) * Constants.multiplier,
                'example1_final': ((max_amount * 3) * Constants.multiplier) / 3,

                'example2_sum': max_amount * 2,
                'example2_final': ((max_amount * 2) * Constants.multiplier) / 3,
                'example2_p3': ((max_amount * 2) * Constants.multiplier) / 3 + max_amount,
                }


class PGGContribute(Page):
    """Player: Choose how much to contribute"""
    def is_displayed(self):
        if self.round_number == Constants.num_rounds:
            return self
        else:
            return False

    form_model = 'player'
    form_fields = ['contribution']

    # setting dynamic maximum based on endowment and cumulative payoff of previous game
    def contribution_max(self):
        if all([p.ingame for p in self.player.in_all_rounds()]) == True:
            cumulative_payoff = sum(
            [p.payoff for p in self.player.in_all_rounds()])
            return(Constants.endowment + cumulative_payoff)
        else:
            cumulative_payoff = 0
            return(Constants.endowment + cumulative_payoff)

    def vars_for_template(self):
        if all([p.ingame for p in self.player.in_all_rounds()]) == True:
            cumulative_payoff = sum(
            [p.payoff for p in self.player.in_all_rounds()])
        else:
            cumulative_payoff = 0
        return {"max_amount" : Constants.endowment + cumulative_payoff}

    # def contribution_label(self):
    #     cumulative_payoff = sum(
    #         [p.payoff for p in self.player.in_all_rounds()])
    #     max_amount = Constants.show_up_fee + cumulative_payoff
    #     return f"How much will you contribute to the project (from 0 to {max_amount})?"


class PGGResultsWaitPage(WaitPage):
    def is_displayed(self):
        if self.round_number == Constants.num_rounds:
            return self
        else:
            return False

    def after_all_players_arrive(self):
        self.group.set_payoffs_PGG()

    body_text = "Waiting for other participants to contribute."
    pass

class PGGResults(Page):
    """Players payoff: How much each has earned"""

    def is_displayed(self):
        if self.round_number == Constants.num_rounds:
            return self
        else:
            return False

    def vars_for_template(self):
        return {
            'total_earnings': self.group.total_contribution * Constants.multiplier,
            'amount_kept': self.group.max_amount - self.player.contribution
        }


class FinalPage(Page):
    def is_displayed(self):
        if self.round_number == Constants.num_rounds:
            return self
        else:
            return False

    def vars_for_template(self):
        return{
        'show_up_fee_kr': Constants.show_up_fee.to_real_world_currency(self.session),
        'game_payoff_currency': c(self.player.payoff).to_real_world_currency(self.session),
        'final_payoff': c(self.player.payoff + Constants.show_up_fee).to_real_world_currency(self.session),
        }


page_sequence = [
    # Pre Game Stuff
    Welcome, Pre_Questionnaire, Introduction, Examples, WaitForPlayers,

    # Rely Verify Game
    Rolls, P1_Roll, RollWaitPage, P2_Roll, RollWaitPage, Leader_Page, ResultsWaitPage, LostGame, Results, FinalEvaluation,

    # PGG
    PGGInstructions, PGGContribute, PGGResultsWaitPage, Moral_Identity, DOSPERT, PGGResults,

    # Finish
    FinalPage]

# Page sequence for debugging
# page_sequence = [Rolls, P1_Roll, RollWaitPage, P2_Roll,
#                  RollWaitPage, Leader_Page, ResultsWaitPage, LostGame, FinalPage]
