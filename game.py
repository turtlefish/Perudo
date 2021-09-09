"""
Handles information about the game state, such as
the number of players, the number of dice left in the game,
if the game is on-going or who has won.
"""


class Gamestate:
    def __init__(self, players):
        self.turn = 0
        self.players = players
        self.num_players = len(players)
        self.current_call = (0, 0)  # (pips, quantity)
        self.palifico = False
        self.winner = None

    def play_game(self):
        while self.winner is None:
            self.play_turn()

        print(str(self.winner) + " wins! Remaining dice: " + str(self.players[self.winner].get_num_dice()))
        return self.winner

    def play_turn(self):
        move = self.players[self.turn].get_move(self.current_call)

        if move == "dudo":
            if self.is_call_valid():
                self.players[self.turn].remove_die()

                if self.players[self.turn].get_num_dice() <= 0:
                    self.winner = 1 - self.turn
                    return

            else:
                self.players[1 - self.turn].remove_die()

                if self.players[self.turn].get_num_dice() <= 0:
                    self.winner = 1 - self.turn
                    return

                self.change_turn()

            self.reset_round()

        else:
            self.current_call = move
            self.change_turn()

    def reset_round(self):
        self.roll_all()
        self.current_call = (0, 0)

    def change_turn(self):  # NOTE: CURRENTLY ONLY WORKS WITH 2 PLAYERS
        # Swaps turn between 1 and 0
        self.turn = 1 - self.turn

    def get_dice_dict(self):
        # Returns a dictionary with the total number of die for each value
        rolls_dict = dict.fromkeys([1, 2, 3, 4, 5, 6], 0)
        all_rolls = self.get_all_rolls()

        for roll in all_rolls:
            for die in roll:
                rolls_dict[die] += 1

        return rolls_dict

    def get_all_rolls(self):
        # Returns a list of lists containing the rolls of each player
        rolls = []
        for p in self.players:
            rolls.append(p.get_current_roll())

        return rolls

    def roll_all(self):
        # Rolls dice for all players
        for p in self.players:
            p.roll()

    def get_call(self):
        return self.current_call

    def raise_call(self, new_call):
        # Raises the current call to a new call (pips, quantity)
        if new_call[0] > 6 or new_call[0] < 0 or not isinstance(new_call[0], int):
            raise ValueError("Tried to call an invalid pip value: " + str(new_call[0]))

        if not isinstance(new_call[1], int):
            raise ValueError("Tried to call a non-integer quantity: " + str(new_call[1]))

        elif new_call[0] >= self.current_call[0] and new_call[1] < self.current_call[1]:
            raise ValueError("Tried to raise lower than the current call: (=> pips & < quantity): " + str(new_call))

        elif new_call[0] < self.current_call[0] and new_call[1] <= self.current_call[1]:
            raise ValueError("Tried to raise lower than the current call: (< pips & <= quantity): " + str(new_call))

        self.current_call = new_call

    def is_call_valid(self):
        return self.get_dice_dict()[self.current_call[0]] >= self.current_call[1]

    def get_num_players(self):
        return self.num_players

