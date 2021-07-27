# Introduction to the ML-Contract-Bridge Project

```
Version 0.1
Work-in-Progress
23-Jul-2021
By Robert Salita
```

## Mission
The ML-Contract-Bridge Project is an experiment in collecting data, statistical analysis and applying AI techniques to the game of duplicate contract bridge.
This document explains the mission and status of the project. The project is in the proof-of-concept stage and research is on-going.
The significance of this project is that it uses AI to make predictions about contracts, results and scores.
The project is currently written in Python and uses sklearn for AI modeling. ACBL and/or The Common Game data is used.

## Introdction
Initial experiments constrain the AI to neither having any understanding of the play of the hand nor any clues provided by bidding. This is
opposed to par score calculation engines which have perfect double dummy knowledge of the play of the hand, or human players who obtain
valuable information conveyed by bidding sequences. Keep in mind, the AI has been given some single dummy information and a final contract.
The initial experiments ask the AI to:

1. Predict the maximum number of tricks which can be taken in the NS and EW directions for each suit. Accuracy is calculated by comparing
    the AI’s predictions to double dummy results.
2. Predict par score and calculate accuracy by comparing predicted to actual par score.
3. Using the above predictions, calculate the AI’s game percentage and ranking. Matchpoint information is obtained from club data from ACBL and/or The Common
    Game’s (TCG).

An important aspect of ML-Bridge is the creation of charts. The charts prove helpful in understanding the accuracy of predictions. Mistakes in
predictions often become visible through examination of charts. The charts contain a wealth of valuable information for bridge enthusiasts,
teachers and pros. The following charts are both simple and technical. Although they show simple relationships, such as HCP vs tricks taken, they
are not so easy to comprehend unless you are experienced at reading charts. Patience is recommended.

Experimental results have been obtained by using ACBL and/or TCG data. This project does not make any data available. However, you can obtain the same
data by executing the provided scripts. Predictions are made using unseen data.
It is safe to assume that using more years of data will result in more accurate predictions. However, improvements in the model will far outweigh results
obtained from providing additional data. About 5 times more TCG data is available than used.

## Explanation of "Sample Charts Produced from ML Bridge Project.pdf"

### Bridge specific terminology
1. “Par” means Par score as seen on hand records. Par score is derived from play engines which are guarenteed to be 100% accurate. This
    is a super-important measure frequently used by ML-Bridge.
2. “Pred” is an AI predicted value. It’s the contract (trick count) having the highest probability of making.
3. “Exp” is a value derived from “Pred” multiplied by the contract score. “Exp” is the maxiumum predicted score whereas “Pred” is the
    most likely making contract. Neither “Pred” nor “Exp” contracts may be the final contract due to higher competitive bids.
4. “Exp_Par” is the AI predicted “Par” score. It’s a super-important measure. It’s derived from “Pred”. Like “Par”, it’s the contract where
    neither side can improve upon by making a further bid. AKA, a Nash-equilibrium. “Par” is calculated by a hand playing engine with
    double dummy knowledge thus guarenteeing an accuracy of 100%. On the other hand, “Exp_Par” has absolutely no knowledge about
    play of the hand nor is it 100% accurate. “Exp_Par” is an AI prediction learned by seeing 100,000s of example hands.
5. “MP” is the matchpoint award.
6. “ACBL” or American Contract Bridge League, http://acbl.org is the governing body for contract bridge in the United States, Mexico, Bermuda and Canada and is a member of the World Bridge Federation, the international bridge governing body.
7. “TCG” The Common Game – https://thecommongame.com provides data on contract scores, MPs and frequency of contracts, scores and results.
8. “Contract Type” can be either Pass, Partial, Game, SSlam, or GSlam.
9. “Strain” can be either Clubs, Diamonds, Hearts, Spades or No-trump abbreviated as C, D, H, S, N.

## AI Terminology
1. “Prediction” a forecast enabled by learning from many examples.
2. “Ground Truth” is the actual, real-life, result. For example, Par score and double dummy trick calculations are considered “Ground
    Truth” as they are 100% accurate.
3. “Mean” is a synonym for “average”.
4. “Frequency” is how often something occurs usually presented as a count or percentage.
5. “Variance” is the difference between two numbers such as bidding level vs tricks taken.

## Chart Notes
1. Percentages are shown using the preferred mathematical scale of 0 to 1 which can be considered a rescaling of 0 to 100%.
2. Sometimes one should ignore outlier statistics. Yes, 8 HCP can take 13 tricks but that’s an exception which should be disregarded.

## Index of Charts
1. Chart 1: Tricks Taken per HCP (High Card Points)
2. Chart 2: Frequency of Tricks Taken
3. Chart 3: Frequency of Variance in Contract Type Between Par and Exp_Par
4. Chart 4: Frequency of Variance in Tricks Taken Between Par and Exp_Par
5. Chart 5: Frequency of MP (Match Points) awarded (299ers game) by Contract Type
6. Chart 6: Frequency of MP (Match Points) awarded (open game) by Contract Type
7. Chart 7: Frequency of MP (Match Points) awarded for Par, Pred, Exp, Exp_Par.
8. Chart 8: How often is the Par score contract a sacrifice?
9. Chart 9: What is the frequency of scores for Par sacrifices?
10. Chart 10: What is the frequency of contract types (Pass, Partial, Game, SSlam, GSlam) for Par scores?
11. Chart 11: Chart showing the frequency of scores for Par, Pred, Exp and Exp_Par.
12. Chart 12: Frequency of MP (Match Points) for Par, Pred, Exp, Exp_Par broken out by direction (EW) and suit.
13. Chart 13: Frequency of MP (Match Points) for Par, Pred, Exp, Exp_Par broken out by direction (NS) and suit.
14. Chart 14: Frequency of MP (Match Points) for Par, Pred, Exp, Exp_Par broken out by direction (NS).
15. Chart 15: How does the mean (average) MP (Match Point) compare between suits for Par, Pred, Exp, Exp_Par?
16. Chart 16: How does the mean (average) MP (open game and 299ers) for Par, Pred, Exp, Exp_Par)?
17. Chart 17: How often is a Par score so unique that TCG (The Common Game) hasn’t recorded any other instance?
18. Chart 18: Relationship between HCP, tricks taken and the frequency of tricks taken.

## Detailed Chart Information
Chart 1: How often does a specific HCP holding take a
specific number of tricks? Bottom row shows (HCP,
Tricks Taken). For example, 20 HCP most often takes 9
tricks but occassionaly just 7 or even 13.

Chart 2: How often does a Par score take a specific
number of tricks? Also shown is Pred (Predicted), Exp
(Expected) and Exp_Par (Expected Par).

Chart 3: How well does Exp_Par (Expected Par)
predict Par score? This chart shows the variance
between what Exp_Par thought it could take and the
actual number (Par) it really could take.

Chart 4: This chart compares actual number of tricks
taken (Par) with Pred (Predicted), Exp (Expected),
Exp_Par (Expected Par).

Chart 5: Frequency of MP (Match Points) awarded
(299ers Game) by Contract Type (Pass, Partial, Game,
SSlam, GSlam) for Par, Pred, Exp, Exp_Par. Scale
shown is 0 to 1 instead of 0 to 100%.

Chart 6: Frequency of MP (Match Points) awarded
(open game) by Contract Type (Pass, Partial, Game,
SSlam, GSlam) for Par, Pred, Exp, Exp_Par. Scale
shown is 0 to 1 instead of 0 to 100%.

Chart 7: Frequency of MP (Match Points) awarded for
Par, Pred, Exp, Exp_Par.

Chart 8: How often is the Par score contract a
sacrifice? A Par score is considered a sacrifice if the
contract results in a set. Contract types are (Partial,
Game, SSlam, GSlam)? Also shown is Exp_Par
(Expected Par).

Chart 9: What is the frequency of scores for Par
sacrifices? Also shown is Exp_Par (Expected Par).
Some Exp_Par sacrifices actually made (oops). FYI, all
Par sacrifices are doubled.

Chart 10: What is the frequency of contract types
(Pass, Partial, Game, SSlam, GSlam) for Par scores?
Also shown are Pred, Exp and Exp_Par.

Chart 11: This is not a visual acuity eye exam. It’s a
chart showing the frequency of scores for Par, Pred,
Exp and Exp_Par.

Chart 12: Frequency of MP (Match Points) for Par,
Pred, Exp, Exp_Par broken out by direction (EW) and
suit.

Chart 13: Frequency of MP (Match Points) for Par,
Pred, Exp, Exp_Par broken out by direction (NS) and
suit.

Chart 14: Frequency of MP (Match Points) for Par,
Pred, Exp, Exp_Par broken out by direction (NS).

Chart 15: How does the mean (average) MP (Match
Point) compare between suits for Par, Pred, Exp,
Exp_Par?

Chart 16: How does the mean (average) compare for
MP (open game and 299ers) for Par, Pred, Exp,
Exp_Par)?

Chart 17: How often is a Par score so unique that TCG
(The Common Game) hasn’t recorded any other
instance? Also compared with Pred, Exp, Exp_Par.

Chat 18: This is a bubble chart. It’s a different type of
chart than we have previously seen. It shows the
relationship between HCP (oops, legend is missing
from bottom row), tricks taken and the frequency of
occurrence. Hence it shows three dimensions of data
instead of the usual two. This chart conveys crucial
information when designing a bidding system.
