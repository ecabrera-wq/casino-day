# Day in the Life: Casino Day

## Game Summary

This game simulates a day trip from my dorm to a casino in Atlantic City. You start the day with $30. You decide whether to snooze your alarm, whether to buy breakfast, how to get to Atlantic City, how much to bet at the blackjack table, and where to eat dinner. The goal is to come back to your dorm at the end of the day with more money than you left with.

## How to Run the Game

1. Put `main.py`, `cards.py`, and `scenes.py` in the same folder.
2. Open a terminal in that folder.
3. Type `python main.py` (or `python3 main.py` on a Mac).

## How to Play

The day has four parts:

1. **Morning:** Your alarm goes off. You can get up right away or hit snooze. If you snooze, you'll snooze a random number of times. If you snooze 3 or more times, you miss the early bus and pay $3 more for a later one. Then you decide whether to buy a $2 breakfast at the bodega.
2. **Getting there:** You pick the bus ($5) or the train ($8). Something random might happen on the way, like getting stuck in traffic or finding $2 between the seats. When you arrive, your money turns into chips (1 chip = $1).
3. **The casino:** You play up to 5 rounds of blackjack. Each round you bet 5 chips, 10 chips, or all in. After each round a random event might happen, like finding chips on the floor or spilling your drink.
4. **Dinner:** You pick a pizza slice ($3), a steakhouse ($12), or skipping dinner. If you're out of money, you skip dinner automatically.

For every menu, type the number of the option you want. If you type something that isn't on the menu, the game asks again.

### Blackjack terms

The game asks if you know how to play blackjack and explains the rules if you don't. Here they are too:

- **Goal:** get closer to 21 than the dealer without going over.
- **Card values:** 2-9 are worth their number. 10, Jack, Queen, and King are worth 10. An Ace (shown as `A`) is worth 11, or 1 if 11 would put you over 21.
- **Hit:** take another card.
- **Stand:** keep your cards and end your turn.
- **Bust:** going over 21. If you bust, you lose the round.
- **Dealer:** the dealer has to keep hitting until they have 17 or more.
- **Push:** a tie. You get your bet back.

### Winning and losing

- You **win** if you get back to your dorm with more than $30.
- You **lose** if you come home with $30 or less, or if you run out of money.
- If you reach 60 chips at the casino, you cash out early so you don't lose it all.

## How the Player's State Is Stored

The player's state is the amount of money they have, stored in one variable called `chips`. It starts at `STARTING_CHIPS` (30).

**Why I used one plain variable:**

- **Money is the only thing that carries through the whole day.** Every choice (snoozing, breakfast, bus or train, bets, dinner) changes how much money you have, so that is the one thing I need to keep track of. Other values, like the round number and the cards, only matter inside the casino, so they are local variables inside `casino_scene()` and `play_round()`.
- **It's easy to follow where the money changes.** Every function that changes the money takes `chips` as an input and returns the new amount. In `main()` the whole day reads like a list of steps:
  ```python
  chips = scenes.morning_scene(chips)
  chips = scenes.travel_scene(chips)
  chips = casino_scene(chips)
  chips = scenes.dinner_scene(chips)
  ```
  Each line passes the money into the next part of the day and gets back the updated amount.
- **No global variables.** Because the money is passed in and returned, no function changes it "secretly." This makes each function easier to test on its own. For example, `random_event(30)` always gives back a number I can check.
- **Why not a dictionary or a list?** A dictionary would make sense if I had a lot of stats, like energy and mood. Since there is only one value that changes across the whole day, one variable is simpler and easier to read.

**The cards** are stored in lists (one for the deck, one for the player's hand, and one for the dealer's hand) because cards get added with `append()` and removed with `pop()` during each round.

**How the winner is decided:** at the end of the day, `check_win(chips)` decides if you won. It first calls `is_broke(chips)` to see if you ran out of money. If you're broke, you lose. If not, it checks whether you have more than `STARTING_CHIPS`. `is_broke()` is also used by `casino_scene()` to stop the blackjack rounds early when you run out of chips.

## Control Flow

### Written description

1. `main()` asks for your name and sets `chips` to 30.
2. `main()` calls `scenes.morning_scene(chips)`. You choose whether to snooze. If you snooze, `random.randint()` picks how many times, and a `for` loop prints each snooze. An `if` statement charges the late fee if you snoozed 3 or more times. Then you choose whether to buy breakfast.
3. `main()` calls `scenes.travel_scene(chips)`. You pick the bus or the train, and `random.choice()` picks what happens on the way.
4. `main()` calls `casino_scene(chips)`. It calls `show_rules()`, then a `while` loop runs the blackjack rounds. The loop keeps going while the round number is under 5, you're not broke, and you have fewer than 60 chips. Each round:
   - `choose_bet()` asks for your bet.
   - `play_round()` makes a new deck with `cards.create_deck()` (which uses `random.shuffle()`) and deals two cards to you and the dealer.
   - `player_turn()` uses a `while` loop that keeps asking hit or stand until you stand or reach 21.
   - If you didn't bust, `dealer_turn()` uses a `while` loop to hit until the dealer has 17 or more.
   - `determine_winner()` compares the hands and returns `"player"`, `"dealer"`, or `"push"`.
   - `update_chips()` adds or subtracts your bet.
   - `random_event()` uses `random.choice()` to maybe add or take away chips.
5. `main()` calls `scenes.dinner_scene(chips)`. You pick where to eat, or you skip dinner if you're out of money.
6. `main()` calls `check_win(chips)`, which calls `is_broke(chips)`, and prints whether you won or lost.

**Input checking:** every menu uses `scenes.get_menu_choice()`, which uses a `while` loop to keep asking until you type a number that's on the menu. `get_player_choice()` does the same for hit and stand. Because all the menus use numbers that are compared as text (like `"1"`), the game never has to turn text into a number, so typing letters can't crash it. I didn't use `try`/`except` because we haven't covered it in class yet.

### Diagram

```
start: ask name, chips = 30
  |
  v
MORNING (scenes.morning_scene)
  snooze? --yes--> random number of snoozes (for loop)
                   3 or more? --yes--> pay late fee
  breakfast? --yes--> pay $2
  |
  v
GETTING THERE (scenes.travel_scene)
  bus or train? --> pay fare --> random event on the way
  |
  v
THE CASINO (casino_scene)
  show_rules()
  +---- WHILE round < 5 and not broke and chips < 60 ----+
  |  choose_bet()                                        |
  |  play_round():                                       |
  |     create_deck() (shuffle) -> deal 2 cards each     |
  |     player_turn(): WHILE "hit" and total < 21        |
  |     busted? --no--> dealer_turn(): WHILE total < 17  |
  |     determine_winner() -> player / dealer / push     |
  |  update_chips()                                      |
  |  random_event()                                      |
  +------------------------------------------------------+
  |
  v
DINNER (scenes.dinner_scene)
  broke? --yes--> skip dinner
  else pick pizza / steakhouse / skip
  |
  v
END: check_win() -> calls is_broke() -> print win or lose
```

## Files

- `main.py`: starts the game, runs the casino and the blackjack rounds, and decides if you won.
- `cards.py`: everything about the cards: making and shuffling the deck, dealing, adding up a hand, hitting, checking for a bust, and showing a hand.
- `scenes.py`: the parts of the day outside the casino (morning, travel, dinner) and the menu function that every part of the game uses.
