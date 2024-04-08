#!/bin/bash

python3 AdmiralBet/oddAdmiral.py &
python3 sansabet/sansabetscraper.py &
python3 soccerbet/soccerbetparser.py &

wait

python3 MATCHFINDER.py
python3 betfinder.py
python3 multiplierfinder.py
python3 BESTBETS.py

