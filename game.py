import random
from dataclasses import dataclass

import numpy as np

NUM_STARTING_DICE = 5
NUM_PIPS = 6
NUM_PLAYERS = 2


@dataclass
class Bid:
    num: int = 0
    pip: int = 0


@dataclass
class GameState:
    p1_dice: tuple[int, ...]
    p2_dice: tuple[int, ...]
    current_bid: Bid
    current_player: int  # 1 or -1


class Perudo:
    def __init__(self):
        self.action_size: int = NUM_PLAYERS * NUM_STARTING_DICE * NUM_PIPS + 1  # all possible bids and dudo call

    def get_initial_state(self) -> GameState:
        return GameState(
            p1_dice=tuple(random.randint(1, NUM_PIPS) for _ in range(NUM_STARTING_DICE)),
            p2_dice=tuple(random.randint(1, NUM_PIPS) for _ in range(NUM_STARTING_DICE)),
            current_bid=Bid(),
            current_player=1,
        )

    def get_valid_moves(self, state: GameState) -> np.ndarray:
        mask = np.zeros(self.action_size, dtype=np.uint8)

        # dudo is valid if there's an existing bid to challenge
        if state.current_bid.num > 0:
            mask[0] = 1

        # mark valid bids
        for bid in self.get_valid_bids(state):
            mask[self.bid_to_action(bid)] = 1

        return mask

    def get_valid_bids(self, state: GameState) -> list[Bid]:
        bids = []

        if state.current_bid.num == 0 or state.current_bid.pip == 0:  # if this is the first bid
            for pip in range(2, NUM_PIPS + 1):
                for num in range(1, len(state.p1_dice) + len(state.p2_dice) + 1):
                    bids.append(Bid(num=num, pip=pip))

            return bids

        if state.current_bid.pip == 1:
            for pip in range(2, NUM_PIPS + 1):  # non-wildcard bids that must be double + 1
                for num in range((state.current_bid.num * 2) + 1, len(state.p1_dice) + len(state.p2_dice) + 1):
                    bids.append(Bid(num=num, pip=pip))

            for num in range(state.current_bid.num + 1, len(state.p1_dice) + len(state.p2_dice) + 1):  # wildcard bids
                bids.append(Bid(num=num, pip=1))

            return bids

        # else if the current bid is not a wildcard bid
        for pip in range(2, NUM_PIPS + 1):  # non-wildcard bids that raise the number of dice
            for num in range(state.current_bid.num + 1, len(state.p1_dice) + len(state.p2_dice) + 1):
                bids.append(Bid(num=num, pip=pip))

        for pip in range(state.current_bid.pip + 1, NUM_PIPS + 1):  # non-wildcard bids that only raise the pip
            bids.append(Bid(num=state.current_bid.num, pip=pip))

        wildcard_min = -(state.current_bid.num // -2)  # wildcard bids halves the minimum bid, rounding up
        for num in range(wildcard_min, len(state.p1_dice) + len(state.p2_dice) + 1):
            bids.append(Bid(num=num, pip=1))

        return bids

    def get_next_state(self, state: GameState, action: int) -> GameState:
        if action == 0:  # dudo action
            if self.is_successful_bid(state):
                loser = state.current_player
            else:
                loser = -state.current_player

            num_p1_dice = len(state.p1_dice) - (1 if loser == 1 else 0)
            num_p2_dice = len(state.p2_dice) - (1 if loser == -1 else 0)

            return GameState(
                p1_dice=self.roll_dice(num_p1_dice),
                p2_dice=self.roll_dice(num_p2_dice),
                current_bid=Bid(),
                current_player=loser,
            )

        # bid action
        new_bid = self.action_to_bid(action)
        if new_bid is None:
            raise TypeError(f"{new_bid=} (dudo), expected to be a valid bid")

        return GameState(
            p1_dice=state.p1_dice,
            p2_dice=state.p2_dice,
            current_bid=new_bid,
            current_player=-state.current_player,
        )

    def get_value_and_terminated(self, state: GameState) -> tuple[float, bool]:
        if len(state.p1_dice) == 0:
            return -1, True  # p1 lost

        if len(state.p2_dice) == 0:
            return 1, True  # p2 lost

        return 0, False  # ongoing

    def is_successful_bid(self, state: GameState) -> bool:
        all_dice = state.p1_dice + state.p2_dice

        if state.current_bid.pip == 1:
            count = sum(dice == 1 for dice in all_dice)

        else:
            count = sum(dice == state.current_bid.pip or dice == 1 for dice in all_dice)

        return count >= state.current_bid.num

    def action_to_bid(self, action: int) -> Bid | None:
        if action == 0:
            return None  # dudo action

        action -= 1
        pip = (action % NUM_PIPS) + 1
        num = (action // NUM_PIPS) + 1
        return Bid(num=num, pip=pip)

    def bid_to_action(self, bid: Bid | None) -> int:
        if bid is None:
            return 0  # dudo action

        return (bid.num - 1) * NUM_PIPS + (bid.pip - 1) + 1

    def roll_dice(self, num_dice: int) -> tuple[int, ...]:
        if num_dice < 0:
            raise ValueError(f"{num_dice=}, expected 0 or more")

        return tuple(random.randint(1, NUM_PIPS) for _ in range(num_dice))


p = Perudo()
state = p.get_initial_state()

while True:
    valid_moves_mask = p.get_valid_moves(state)

    if state.current_player == 1:
        print(f"your dice: {state.p1_dice}, computer has {len(state.p2_dice)} dice")
        player_input = input("your move: ")
        if player_input in ["dudo", "d"]:
            print(f"player dice: {state.p1_dice}, computer dice: {state.p2_dice}")
            action = 0
        
        else:
            num, pip = [int(_) for _ in player_input.split()]
            action = p.bid_to_action(Bid(num=num, pip=pip))

        if valid_moves_mask[action] == 0:
            print(f"{p.action_to_bid(action)} action is not valid")
            continue

    else:
        legal_moves = np.where(valid_moves_mask == 1)[0]
        action = np.random.choice(legal_moves)
        if action == 0:
            print(f"computer says dudo! your dice: {state.p1_dice}, computer dice: {state.p2_dice}")

        else:
            print(f"computer bids {p.action_to_bid(action)}")

    state = p.get_next_state(state, action)

    value, is_terminal = p.get_value_and_terminated(state)

    if is_terminal:
        if value == 1:
            print("you won")

        else:
            print("computer won")

        break
