# Perudo
A project for a server and client to connect and play the board game *Perudo*.
## Rules
- A round starts with both players rolling their dice.
- The players dice are hidden from each other - (they only know their own dice)
- Players take turns make calls on the number of dice of a specific value:
- For example: Player 1 says 2 ones's: *(2 dice with 1 pip)*
- The other player then either raises this call, or calls "dudo".
 - If the player chooses to raise the call, they must either raise the pip value (two's to four's),
or the number of the dice.
-- They can also choose to raise both the pip value as well as the quantity at the same time.
- If the player thinks their opponents call was invalid, they can call "dudo" instead, if they do this, both players reveal their dice - and both are counted up together.
-- If the opponents call was less than the quantity of that pip value on the table, they lose a dice.
-- Otherwise, the player that called "dudo" loses a dice, (when there are that many or more on the table)
- A new round starts, and the loser of the start round makes the first call.
- The first round when a player has only one dice left (Palifico), the calls may only raise the quantity - NOT change the pip value
- The game ends when the a player has no dice left. (they lose)
