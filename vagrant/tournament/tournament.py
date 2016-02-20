#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import bleach
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournamentproj")


def deleteMatches():
    """Remove all the match records from the database."""
    # sql statement
    sql = "DELETE FROM game;"

    # execute sql
    exeSql(sql, None)


def deletePlayers():
    """Remove all the player records from the database."""
    # sql statement
    sql = "DELETE FROM player;"

    # execute sql
    exeSql(sql, None)


def countPlayers():
    """Returns the number of players currently registered."""
    # sql statement
    sql = "SELECT COUNT(*) FROM player;"

    return int(exeSql(sql, None)[0][0])


def createTournament(tournament_name):
    """
    Args:
        tournament_name: the tournament name in which player will register
         and matches will be played.

    Returns:
        NONE
    """
    # sql statement
    sql = "INSERT INTO tournament(tournament_name) VALUES(%(tournament_name)s);"

    # use bleach to
    # escapes or strips markup and attributes
    tournament_name = bleach.clean(tournament_name)

    # execute sql
    exeSql(sql, {'tournament_name': tournament_name})


def registerPlayer(tournament_name, player_name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    # sql statement
    sql = "SELECT tournament_id FROM tournament WHERE tournament_name=%(tournament_name)s;"

    # use bleach to
    # escapes or strips markup and attributes
    tournament_name = bleach.clean(tournament_name)

    # execute sql to get tournament_id
    tournament_id = int(exeSql(sql, {'tournament_name': tournament_name})[0][0])

    # use bleach to
    # escapes or strips markup and attributes
    player_name = bleach.clean(player_name)

    # sql statement
    sql = "INSERT INTO player(tournament_id, player_name) VALUES(%(tournament_id)s, %(player_name)s);"

    # execute sql
    exeSql(sql, {'tournament_id': tournament_id, 'player_name': player_name})


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """


def exeSql(sql, dict_):
    # db conn object
    conn = connect()

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # execute delete
    if dict_ is None:
        cur.execute(sql)
    else:
        cur.execute(sql, dict_)

    # declare resultSet
    resultSet = ()

    # fetch results only for select stmns.
    if "SELECT" in cur.statusmessage:
        resultSet = cur.fetchall()

    # make the changes to the db persistent
    conn.commit()

    # Close communication with the database
    cur.close()
    conn.close()

    return resultSet
