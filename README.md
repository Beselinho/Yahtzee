# Yahtzee

## What is Yahtzee
For those who don't know Yahtzee is a dice game that involves both luck and strategy. The game is played with 5 dices and a scoreboard and the goal is to score the most points given the outcomes from the scoreboard. A round of Yahtzee works like this:
- Roll the dices so you get a starting combination
- Make actions (you can choose which dice to keep and which to roll)
- Roll the dices that are not kept
- Make actions
- Roll dices
- Check if your combination scored points
- End of Round

## The Goal
My goal ? Simple. Create an intelligent agent that can play the game of Yahtzee optimally

<details>
  <summary><h2>The Early Stage</h2></summary>
<h3>The approach</h3>
For starters I reduced the game to just two rounds and two outcomes : Full House (FH) and Small Straight (SS). In the Yahtzee game you have 
- Full House: 25 points provided that one has three-of-a-kind and the other two dice are a pair;
- Small Straight: 30 points provided four of the dice have consecutive values; <br>

My idea for a strategy, quite a simple one actutally, is to always check the highest chance to score points, or in other words to always check before taking actions which scenario is more probable, hitting a FH or hitting a SS. For that I needed to know for each combination of dices what are the chances to hit either FH or SS. So I made an algorithm using expectiMax to determine for each of the two outcomes and for the number of actions left and for each of the 252 unique combinations of dices the chances to hit and stored them in a table.

<h3> The results </h3>
I needed to set a baseline so I tried the worst strategy I thought of and that is to always roll, make no actions. This strategy got surprisingly, for me at least, an average of approximately 20 points out of a total of 55 when I ran the game for 1 million times<br>
<img src="media/always_roll.jpg" width="450" title="Final build" > <br> 

I tried another bad strategy, to check the highest chance to hit one of the outcomes just before making the last actions. This strategy was somewhat better than the other one and got approximately 23 points when the game was simulated 1 million times. <br>
<img src="media/random_first_roll.jpg" width="450" title="Final build" > <br> 

The time for trying my strategy has come. Knowing the chances to hit one of the outcomes at all times seems to be quite useful. My strategy got an average score of approximately 33 points out of the total 55 when I played the game 1 million times. <br>
<img src="media/highest_chance_strategy.jpg" width="450" title="Final build" > <br> 

Another good strategy was to check the expected value (chance * score) instead of only the chances. This one was a bit worse than my strategy, scoring an average of 32.7 when simulated 1 million times.<br>
<img src="media/expected_value.jpg" width="450" title="Final build" > <be>
</details>

<h2>The algorithm on the full game </h2>
I kept using the same strategy as in the two outcomes Yahtzee and in other words insted of foucusing on 39 rounds i focues on the round at hand, pretty much a greedy type algorithm. I implemented all the Yathzee features, the 35 points bonus for the upper section, although I feel like I can upgrade this part and the bonus 100 points and free placing of hitting multiple yathzees. 
The results on the full game with this strategy were pretty decent. A good score in yahtzee is considered to be between 240 and 270, and my strategy gets an average of aproximately 230 points when I simulated 100000
<img src="media/expected_value_full_game.jpg" width="450, title="Full game"> <br>
