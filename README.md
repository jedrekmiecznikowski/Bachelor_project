# oTree studies on collaborative corruption

These are study designs looking at issues in collaborative corruption.
So far, this focusses on one predominant study design: The rely or verify game, also referred to as Leadership Corruption Game (LCG), which is followed up by either a public goods game (PGG), or trust game (TG).

This design is implemented in various ways:

## Rely or Verify
This is the original, three player version of the game. This has been run in the lab with 180+ participants.

## Rely or Verify - SINGLE LEADER
This is a blueprint for a single leader version. Currently not developed.

## Rely or Verify - SINGLE LEADER SIMPLE
Not currently developed - not sure what this was for.

## Rely or Verify - SINGLE P1 SIMPLE
This is a two player design (P1 and leader): This version has a computerized leader, and a single player 1. Every 5 rounds, P1 can evaluate the leader on a set of dimensions.
This has been run on mTurk with 400 participants.

## Rely or Verify - SINGLE COMPETING
This is a variation of the Boston design. This has two conditions, competing vs. aligned payoffs.

## Rely or Verify - SINGLE Changing
No idea what this is...

## Rely or Verify - Same vs. Change
This is a variation of the SINGLE P1 SIMPLE design. There are two conditions: Same vs. Change.
- Same Condition: P1 and Leader stay in the same group for all rounds
- Change Condition: P1 gets assigned a new Leader every x rounds

## Rely or Verify - SINGLE SUB LEADER
This is a variation of the SINGLE P1 SIMPLE design. Here, the subordinate becomes the leader after x rounds.
Currently in development.


# oTree version and extra packages
Currently, this is using
- otree[mturk] == 2.2.4
- otree_tools # for tracking time focus
- django-recaptcha # for using google recaptchas


# Best Practices
1. For testing the studies, it's advisable to test them using 127.0.0.1:8000, rather than localhost:8000. This is because the google recaptcha is not registered for the localhost adress, so will fail to load.
2. ...
