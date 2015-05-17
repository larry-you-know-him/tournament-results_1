#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("delete from match")
    conn.commit()
    cursor.close()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("delete from player")
    conn.commit()
    cursor.close()
    conn.close()


def deleteTournaments():
    """Remove all the tournament records from the database."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("delete from tournament")
    conn.commit()
    cursor.close()
    conn.close()


def countPlayersRegistered():
    """Returns the number of players currently registered (regardless of whether they're in a tournament."""
    cursor = connect().cursor()
    cursor.execute("select count(*) as player_count from player")
    count = cursor.fetchone()
    cursor.close()
    #print "Player count: " + str(count[0])
    return count[0]


def countPlayersInSpecificTournament(tournament_name, tournament_start, tournament_end):
    """Returns the number of players currently in a specified tournament."""
    cursor = connect().cursor()
    cursor.execute(
        """select count(*) as player_count
        from player
        where tournament_id = (select id from tournament where upper(name) = upper(%s) and start_date = %s and end_date = %s)
            and tournament_id is not null
        """, (tournament_name, tournament_start, tournament_end,))
    count = cursor.fetchone()
    cursor.close()
    #print "Player count: " + str(count[0])
    return count[0]


def registerTournament(tournament_name, tournament_start, tournament_end):
    """Adds a tournament to the tournament database.
  
    The database assigns a unique serial id number for the tournament.
  
    Args:
      name: the tournament's name.
      start: the date the tournament starts (format: YYYY-MM-DD).
      end: the date the tournament ends (format: YYYY-MM-DD).
      NOTE: the combination of tournament name, start date and end date must be unique
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("insert into tournament (name, start_date, end_date) values (%s,%s,%s);", (tournament_name, tournament_start, tournament_end,))
    conn.commit()
    cursor.close()
    conn.close()


def registerPlayer(name):
    """Registers a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        insert into player (name) values
        (%s);
        """
        , (name,))
    conn.commit()
    cursor.close()
    conn.close()


def registerPlayerInTournament(name, tournament_name, tournament_start, tournament_end):
    """Adds a player to the tournament database for a specific tournament.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
      tournament_name: the tournament's name.
      tournament_start: the tournament's starting date YYYY-MM-DD.
      tournament_end: the tournament's ending date YYYY-MM-DD.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        insert into player (name, tournament_id) values
        (%s,
            (
                select id from tournament where upper(name) = upper(%s) and start_date = %s and end_date = %s
            )
        );
        """
        , (name,tournament_name,tournament_start,tournament_end,))
    conn.commit()
    cursor.close()
    conn.close()


def verifyPlayerTournamentRegistration(player_name, tournament_name, tournament_start, tournament_end):
    """Verifies that the player referenced by player_name is actually registered at the specified tournament.

    The database will query its registration tables and look for a player player_name is registered in the tournament
    uniquely identified by tournament_name, tournament_start, and tournament_end.
  
    Args:
      player_name: the name of the player.
      tournament_name: the tournament's name.
      tournament_start: the tournament's starting date YYYY-MM-DD.
      tournament_end: the tournament's ending date YYYY-MM-DD.

    Returns:
      The unique tournament identifier that the player is registered in or an error is thrown if the player
      is not registered in the specified tournament or some other error occurs.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        select id from tournament where upper(name) = upper(%s) and start_date = %s and end_date = %s
        """
        , (tournament_name,tournament_start,tournament_end,))
    tournament_id = cursor.fetchone()
    if tournament_id[0] > 0:
        # The tournament is valid; check to see if the player is registered in the tournament
        cursor.execute(
            """
            select count(*) from player where upper(name) = upper(%s) and tournament_id = %s
            """
            , (player_name,tournament_id[0]))
        player_count = cursor.fetchone()
        cursor.close()
        conn.close()
        if player_count[0] == 1:
            # The player is registered in the tournament; return the tournament id
            return tournament_id[0]
        elif player_count[0] == 0:
            # The player is not registered in the tournament; throw an error
            raise ValueError("There is no player [%s] registered within the specified tournament. Please check your inputs.", (player_id,))
        else:
            # Some other error occurred.
            raise ValueError("An error occurred finding the player id [%s] within the specified tournament.", (player_id,))
    elif tournament_count[0] == 0:
        cursor.close()
        conn.close()
        # The tournament is invalid - throw an error
        raise ValueError("There is no tournament with that name, start and end combination. Please check your inputs.")
    else:
        cursor.close()
        conn.close()
        # Some other error occurred.
        raise ValueError("An error occurred finding tournament with that name, start and end combination.")
        

def playerStandings(tournament_name, tournament_start, tournament_end):
    """Returns a list of the players and their win records within a given tournament, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.
  
    Args:
      tournament_name: the tournament's name.
      tournament_start: the tournament's starting date YYYY-MM-DD.
      tournament_end: the tournament's ending date YYYY-MM-DD.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
                    select
                        p.id as id,
                        p.name as name,
                        coalesce(w.win_count,0) as wins,
                        coalesce(m.match_count,0) as matches
                    from
                        player p
                            left join player_win_count w on w.winner_id = p.id
                            left join player_match_count m on m.player_id = p.id
                    where p.tournament_id =
                    (
                        select id from tournament where upper(name) = upper(%s) and start_date = %s and end_date = %s
                    )
                    order by wins desc
                   """,(tournament_name,tournament_start,tournament_end,))
    standings = cursor.fetchall()
    cursor.close()
    conn.close()
    return standings


def reportMatch(winner, loser, tournament_name, tournament_start, tournament_end):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
      tournament_name: the tournament's name.
      tournament_start: the tournament's starting date YYYY-MM-DD.
      tournament_end: the tournament's ending date YYYY-MM-DD.
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
      insert into match (winner_id, loser_id, tournament_id)
      values (%s, %s, (
        select id from tournament where upper(name) = upper(%s) and start_date = %s and end_date = %s));""",
                   (winner, loser, tournament_name, tournament_start, tournament_end))
    conn.commit()
    cursor.close()
    conn.close()

 
def swissPairings(tournament_name, tournament_start, tournament_end):
    """Returns a list of pairs of players for the next round of a match within a given tournament.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Args:
      tournament_name: the tournament's name.
      tournament_start: the tournament's starting date YYYY-MM-DD.
      tournament_end: the tournament's ending date YYYY-MM-DD.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """

    standings = playerStandings(tournament_name, tournament_start, tournament_end)

    #print standings

    # each standing tuple: (id, name, wins, matches)

    #print "starting loop"
    pairings = []
    for num in xrange(0,len(standings) - 1, 2):
        #print num
        pairings.append( (standings[num][0], standings[num][1], standings[num + 1][0], standings[num + 1][1]) )
    
    #print pairings

    return pairings
