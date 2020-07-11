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
