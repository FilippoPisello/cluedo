# AIM OF THE PROJECT
[Cluedo](https://en.wikipedia.org/wiki/Cluedo) is a popular board game. The
object of the game is to determine who murdered the game's victim, where and
which weapon was used. Each player attempts to deduce the correct answer by
strategically moving around a game board and collecting clues about the
circumstances of the murder from the other players.

The aim of the project is to create the perfect Cluedo player, who extracts all
the possible information from the ongoing game, delivering the solution as soon
as it is logically possible.

The initial idea is to realize an algorithm which can be fed up with the events
of the game in the simplest way possible, making its way towards the solution.

Python-wise, this project is a way for me to explore the object-oriented
programming which I rarely use while performing data analysis.

## V 0.8
### Algorithm's structure
1. Start the game:
    1. Define the players' order
    1. Add all the cards to the suspects
    1. Intake the cards taken from the USER
        1. Remove them from the suspects
        1. Register the fact that USER owns them
        1. Register the fact that the other players do not own them
1. As long as there is more than one element for at least one of the three
suspects' groups (characters, weapons, rooms), start the turn of one of the
players:
    1. Ask if an accusation was made:
        1. If no:
            - Go to next player
        1. If yes:
            1. Register which character, weapon and room were included in the
            accusation
            1. Register that PLAYER X showed the cards
            1. Deduce which players did not show any card
                1. Register the fact that they do not own all the cards included
                in the accusation
            1. If the player is USER:
                1. Register which card was shown
                    1. Remove it from the suspects
                    1. Register the fact that PLAYER X owns it
                    1. Register the fact that the other players do not own it
            1. If the player is not USER:
                1. Remove from the accusation the cards that PLAYER X does
                not own.
                1. Register that one of the cards of PLAYER X is one of the
                cards of the remaining cards of the accusation. This happens
                adding a list of items instead of a single element.
        1. Make logical deductions with the information in possess:
            1. For each player, check if any of the cards stored as potentially owned turned out not to be in possess of that player. In this case,
            remove it from the cards owned.
            1. If doing this any of the doubtful slots, thus containing a list,
            turn into sure slots, thus containing a single element:
                1. Remove that card from the suspects
                1. Register that all the other players do not own it
            1. Check if among the slots with multiple elements there are any
            which contain cards which turned out to be true:
                1. In that case, reset the doubtful slot since it contains
                redundant information
            1. Check if there are duplicates among the slot:
                1. If any, reset to empty the redundant ones.
            1. Run for safety the initial check
    1. Go to the next player
1. The official accusation to be made is certain, display it to the user

### To be implemented
1. Card revealed
1. Cards owned by the table

## V 0.0
### Preliminary reasoning on the game structure
From the perspective of a single player (A)

#### Information's sources
1. Cards received by (A) at the beginning of the game
    1. Exclude from the components of the murder the cards (A) owns
1. Other players' reaction to accusations by (A)
    1. Exclude from the components of the murder the cards directly shown to (A)
    1. Derive partial information from the people not having the cards called by
    (A)
1. Other players' reaction to third-party accusations
    1. Derive partial information from people showing a card to a third-party
    player
    1. Derive partial information from the people not having the cards called by
    third-party players
1. Cards publicly revealed during the gameplay either for the passing of time or
for the elimination of opponents
    1. Exclude from the components of the murder the cards showed to (A) and to
    the other players

In brief, the process consist in gradually excluding elements from the three
pools of items (characters, weapons, rooms) until each of them includes only a
single item.

#### Four game phases:
1. [ONE SHOT] Beginning of the game:
    1. Rule out from the suspects the cards owned by (A)
1. [RECURSIVE] Cards publicly revealed:
    1. Rule out from the suspects the cards revealed to everybody
1. [RECURSIVE] Accusations made by the player:
    1. Rule out from the suspects the cards showed by other players to (A)
    1. Store incomplete information on what the other do not own
1. [RECURSIVE] Other players' accusations:
    1. Store incomplete information on what the other own and shown to
    third-party players
    1. Store incomplete information on what the other do not own


### Potential algorithm for N players
The algorithm builds on three list:
1. The list of the suspects
    - Containing three lists, one for each type of item
1. The list of the cards owned by each player
    - Containing N-1 lists, one for each player.
1. The list of the cards not owned by each player.
    - Containing N-1 lists, one for each player.

Sequence of the events:
1. Check the pools of suspects for the three categories. Is there a single item
in each of them?
    - If yes:
        1. Formulate the official accusation
1. Is it the first turn?
    - If yes:
        1. Remove from the suspects the cards owned by (A)
        1. Add the cards owned to the ones that each player from 2 to N does not
        have
1. Is further direct information revealed?
    - If yes:
        1. Remove from the suspects the card(s) revealed
        1. Add the cards revealed to the ones that each player from 2 to N does
        not have
1. Does player (A) make an accusation?
    - If yes, call [S, W, P] the three items included in the accusation:
        1. While PLAYER do not have the cards:
            - Store the fact that they do not own neither [S, W, P]
            - Check if there is any element nobody owns
                - If yes and if there are no covered cards on the table:
                    - Store it as one of the three final cards
        1. When a PLAYER has a card:
            - Store that PLAYER owns that card
            - Remove from the suspects the card revealed
            - Add the cards revealed to the ones that each player from 2 to N
            does not have
1. For player from 2 to N: does player make an accusation?
    - If yes, call [S, W, P] the three items included in the accusation:
        1. While PLAYERS do not have the cards:
            - Store the fact that they do not own neither [S, W, P]
            - Check if there is any element nobody owns
                - If yes and if there are no covered cards on the table:
                    - Store it as one of the three final cards
        1. When a PLAYER has a card:
            - Take away from [S, W, P] the cards which PLAYER is registered not
            to have
            - Store the fact that PLAYER has either one of the remaining ones
                - If only one remains in the list:
                    - Store that PLAYER owns that card
                    - Remove that card from the suspects
