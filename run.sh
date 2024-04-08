#!/bin/bash
echo "Running script"

python3 AdmiralBet/oddAdmiral.py &
python3 sansabet/sansabetscraper.py &
python3 soccerbet/soccerbetparser.py &
python3 PremierKladionica/KlausScraperParser.py &
python3 lobbet/lobbet.py &
python3 SBbet/SBbetParser.py &
python3 hatbet/hatbetParserScraper.py &
python3 maxbet/maxbet.py &
wait

python3 MATCHFINDER.py
python3 betfinder.py
python3 multiplierfinder.py
python3 BESTBETS.py

cd Intermediatevalues
rm -rf *
cd ../Betdata
rm -rf *
cd ..
rm soccerbet.json
rm hatbet.html
rm response_data.json
echo "Script finished running"
sleep 30
./run.sh


