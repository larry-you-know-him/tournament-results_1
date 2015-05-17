
GENERAL INFO:
-------------
Project Name: Tournament
This is a combination of three files that comprise the persistence solution in the Python language using the PostgeSQL database
for a tournament system where determination of match pairings is done using the Swiss-style (the loser of a match is not removed from playing 
further matches but cannot become the overall winner).  The user features in the system in regards to the tournament are:
- creating an overall tournament; deleting all tournaments
- adding a player (both to a specific tournament and to no tournament); deleting all players
- recording of matches within a tournament between players; deleting all matches
- verification of player registration in a given tournament
- produce a listing of player standings in a given tournament
- produce a list of Swiss-style player pairings for the next round in a given tournament
- count the number of players (both registered in a given tournament and overall)


FILES:
------
1. tournament.sql - this file contains the PostgreSQL database commands to create the data structures needed to store and retrieve the
information used in the tournament system.  These structures need to be created in a database called "tournament".  There is a command in the 
file to create the database but it is commented out.  It is recommended to create the database first then switch to that database then run all
the commands in the file.  In this manner you will ensure all the data structures required will be created in the correct location and
there will be no problems in the other parts of the system finding and using the data structures.
2. tournament.py - this Python file uses the psycopg2 library to connect to the PostgreSQL tournament database and defines several methods that
can be called which implements the user features listed in the General Info section.  It cannot be run independently.
3. tournament_test.py - this Python file calls methods in Python file tournament.py and contains all its tests for.  After the tournament 
database is created, you can run it to ensure all the methods in tournament.py are performing correctly.  Run it using this command:
	python tournament_test.py

