import random


class Player:
    def __init__(self, p_id, is_human):
        self.p_id = p_id
        self.num_die = 5
        self.current_roll = None
        self.is_human = is_human

    def get_move(self, current_call: tuple):
        # implement strategy here and return call
        # @param current_call: (pips, quantity)
        # @return tuple: (pips, quantity) or str: "dudo"
        if self.is_human:
            return self.get_human_move(current_call)

        if current_call[1] > 6:
            return "dudo"

        return current_call[0], current_call[1] + 1

    def get_human_move(self, current_call):
        human_input = input("pID: " + str(self.p_id) + " | Current call: " + str(current_call)
                            + " | Roll: " + str(self.current_roll) +
                            "\n Enter a move: \"dudo\", or two numbers: ").lower()

        if human_input == "dudo" or human_input == "d":
            return "dudo"

        else:
            return tuple(map(int, human_input.split()))

    def get_current_roll(self):
        return self.current_roll

    def roll(self):
        # Returns the roll for all players dice as a sorted list
        self.current_roll = sorted([random.randint(1, 6) for i in range(self.num_die)])

    def get_id(self):
        return self.p_id

    def get_num_dice(self):
        return self.num_die

    def set_num_dice(self, n):
        self.num_die = n

    def remove_die(self):
        self.num_die -= 1
