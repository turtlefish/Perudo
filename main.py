from player import Player
from game import Gamestate

gs = Gamestate([Player(0, True), Player(1, True)])
gs.roll_all()
# print(gs.get_all_rolls())
# print(gs.get_dice_dict())
# print(gs.is_call_valid())

gs.play_game()

" implement palifico "
