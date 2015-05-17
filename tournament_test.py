#!/usr/bin/env python
#
# Test cases for tournament.py

from tournament import *

def testDeleteMatches():
    deleteMatches()
    print "1. Old matches can be deleted."

def testDeletePlayers():
    deletePlayers()
    print "1a. Old players can be deleted."

def testDeleteTournaments():
    deleteTournaments()
    print "1b. Old tournaments can be deleted."

def testDeleteAll():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    print "2. Match, Player and Tournament records can be deleted."


def testCount():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    c = countPlayersRegistered()
    if c == '0':
        raise TypeError(
            "countPlayersRegistered() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayersRegistered() should return zero.")
    c = countPlayersInSpecificTournament("Foobar tournament","2015-05-01","2015-05-10")
    if c == '0':
        raise TypeError(
            "countPlayersInSpecificTournament() should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deleting, countPlayersInSpecificTournament() should return zero.")
    print "3. After deleting, both countPlayersRegistered() and countPlayersInSpecificTournament() return zero."


def testRegister():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerPlayer("Peter Bogdonovich") #registration of user for no particular tournament
    registerTournament("Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Chandra Nalaar","Foobar tournament","2015-05-01","2015-05-10")  #registration of user for a specific tournament
    c = countPlayersRegistered()
    if c != 2:
        raise ValueError(
            "After two players register (one for a specific tournament), countPlayersRegistered() should be 2.")
    c = countPlayersInSpecificTournament("Foobar tournament","2015-05-01","2015-05-10")
    if c != 1:
        raise ValueError(
            "After one player registers for a specific tournament, countPlayersInSpecificTournament() should be 1.")
    print "4. After registering two players, both countPlayersRegistered() and countPlayersInSpecificTournament() returns the correct values."


def testVerify():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerTournament("Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Chandra Nalaar","Foobar tournament","2015-05-01","2015-05-10")  #registration of user for a specific tournament
    tournament_id = verifyPlayerTournamentRegistration("Chandra Nalaar","Foobar tournament","2015-05-01","2015-05-10")
    if tournament_id <= 0:
        raise ValueError(
            "The player should be registered in the specific tournament.")
    print "4a. Player registration in a specific tournament was verified."


def testRegisterCountDelete():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerTournament("Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Markov Chaney","Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Joe Malik","Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Mao Tsu-hsi","Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Atlanta Hope","Foobar tournament","2015-05-01","2015-05-10")
    c = countPlayersInSpecificTournament("Foobar tournament","2015-05-01","2015-05-10")
    if c != 4:
        raise ValueError(
            "After registering four players, countPlayers should be 4.")
    deletePlayers()
    c = countPlayersInSpecificTournament("Foobar tournament","2015-05-01","2015-05-10")
    if c != 0:
        raise ValueError("After deleting, countPlayers should return zero.")
    print "5. Players can be registered and deleted."


def testStandingsBeforeMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerTournament("Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Melpomene Murray","Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Randy Schwartz","Foobar tournament","2015-05-01","2015-05-10")
    standings = playerStandings("Foobar tournament","2015-05-01","2015-05-10")
    
    #print standings

    if len(standings) < 2:
        raise ValueError("Players should appear in playerStandings even before "
                         "they have played any matches.")
    elif len(standings) > 2:
        raise ValueError("Only registered players should appear in standings.")
    if len(standings[0]) != 4:
        raise ValueError("Each playerStandings row should have four columns.")
    [(id1, name1, wins1, matches1), (id2, name2, wins2, matches2)] = standings
    if matches1 != 0 or matches2 != 0 or wins1 != 0 or wins2 != 0:
        raise ValueError(
            "Newly registered players should have no matches or wins.")
    if set([name1, name2]) != set(["Melpomene Murray", "Randy Schwartz"]):
        raise ValueError("Registered players' names should appear in standings, "
                         "even if they have no matches played.")
    print "6. Newly registered players appear in the standings with no matches."


def testReportMatches():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerTournament("Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Bruno Walton","Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Boots O'Neal","Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Cathy Burton","Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Diane Grant","Foobar tournament","2015-05-01","2015-05-10")
    standings = playerStandings("Foobar tournament","2015-05-01","2015-05-10")
    
    #print standings

    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, "Foobar tournament","2015-05-01","2015-05-10")
    reportMatch(id3, id4, "Foobar tournament","2015-05-01","2015-05-10")
    standings = playerStandings("Foobar tournament","2015-05-01","2015-05-10")
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."


def testPairings():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    registerTournament("Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Twilight Sparkle","Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Fluttershy","Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Applejack","Foobar tournament","2015-05-01","2015-05-10")
    registerPlayerInTournament("Pinkie Pie","Foobar tournament","2015-05-01","2015-05-10")
    standings = playerStandings("Foobar tournament","2015-05-01","2015-05-10")
    [id1, id2, id3, id4] = [row[0] for row in standings]
    reportMatch(id1, id2, "Foobar tournament","2015-05-01","2015-05-10")
    reportMatch(id3, id4, "Foobar tournament","2015-05-01","2015-05-10")
    pairings = swissPairings("Foobar tournament","2015-05-01","2015-05-10")
    if len(pairings) != 2:
        raise ValueError(
            "For four players, swissPairings should return two pairs.")
    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4)] = pairings
    correct_pairs = set([frozenset([id1, id3]), frozenset([id2, id4])])
    actual_pairs = set([frozenset([pid1, pid2]), frozenset([pid3, pid4])])
    if correct_pairs != actual_pairs:
        raise ValueError(
            "After one match, players with one win should be paired.")
    print "8. After one match, players with one win are paired."


if __name__ == '__main__':
    testDeleteMatches()
    testDeletePlayers()
    testDeleteTournaments()
    testDeleteAll()
    testCount()
    testRegister()
    testVerify()
    testRegisterCountDelete()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    print "Success!  All tests pass!"


