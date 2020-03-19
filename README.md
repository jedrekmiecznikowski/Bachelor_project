# Jedrek's oTree folder on Be-Lab server

This repo exists to host Jedrek's oTree experiment for his BA. 

Below follow a few technical details, and a short description of existing projects.

## Rely or Verify

This is just an illustrative project, to check whether the server works - currently has a small bug for Player 1. 



## Jedrek's Project

... to come ...




# oTree version and extra packages
Currently, this server is using the following:
- otree[mturk] == 2.2.4
- otree_tools # for tracking time focus
- django-recaptcha # for using google recaptchas
- python3.6

When testing your otree study locally (using otree devserver), it is important to have at least the same version of otree! 


# Important info
1. This repo is connected to the server hosting www.be-lab.au.dk. Changes made here can be pushed to the server.
2. Pushing changes to this repo will not immediately update the oTree version running on be-lab.au.dk. For this, oTree has to be restarted server side. Currently, the only person who has rights to do so is Simon. 
3. It's best to use this repo to develop and test your study locally (using devserver). This way, chances of it working when pushing it to the server are highest (though not guaranteed, as there's always some small things that can go wrong). 
4. Regardings settings.py: Do not change any of the authentication or mTurk parameters! Only make changes for Session Configs and Rooms, if necessary.

# TODO

1. Set up mTurk API credentials
2. Push first version of Jedrek's study to repo
3. Pretest Jedrek's study on server





