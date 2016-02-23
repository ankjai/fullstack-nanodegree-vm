#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import bleach
import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournamentproj")


def deleteTournaments():
    """Remove a tournament from the database."""
    # sql statement
    sql = "DELETE FROM tournament;"

    # execute sql
    exeSql(sql, None)


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


def deleteOutcome():
    """Remove all matches played between players"""
    sql = "DELETE FROM outcome;"
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


def playerStandings(tournament_name):
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
    sql = "SELECT * FROM standing ORDER BY player_win_count DESC"


def createMatches(first_player, second_player):
    sql = "select * from player where player_name=%(player_name)s;"
    result = exeSql(sql, {'player_name': first_player})
    for first_player_id, first_player_tournament_id, first_player_name in result:
        print "ID:", first_player_id, "TID:", first_player_tournament_id, "NAME:", first_player_name

    result = exeSql(sql, {'player_name': second_player})
    for second_player_id, second_player_tournament_id, second_player_name in result:
        print "ID:", second_player_id, "TID:", second_player_tournament_id, "NAME:", second_player_name

    print "IDs:", first_player_id, second_player_id

    sql = "INSERT INTO game(tournament_id, first_player_id, second_player_id) VALUES(%(first_player_tournament_id)s, %(first_player_id)s, %(second_player_id)s);"

    if (first_player_tournament_id == second_player_tournament_id):
        print "Players are of same tournament"
        exeSql(sql, {'first_player_tournament_id': first_player_tournament_id, 'first_player_id': first_player_id,
                     'second_player_id': second_player_id})
    else:
        raise AssertionError("Players are not of same tournament.")


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    sql = "SELECT player_id, tournament_id FROM player WHERE player_name = %(winner)s;"
    result = exeSql(sql, {'winner': winner})

    for winner_player_id, winner_tournament_id in result:
        print "Winner ID:", winner_player_id, "Winner tournament id:", winner_tournament_id

    sql = "SELECT player_id, tournament_id FROM player WHERE player_name = %(loser)s;"
    result = exeSql(sql, {'loser': loser})

    for loser_player_id, loser_tournament_id in result:
        print "Loser ID:", loser_player_id, "Loser tournament id:", loser_tournament_id

    sql = "SELECT game_id FROM game WHERE (first_player_id=%(winner)s AND second_player_id=%(loser)s) OR (first_player_id=%(loser)s AND second_player_id=%(winner)s);"
    result = exeSql(sql, {'winner': winner_player_id, 'loser': loser_player_id})

    for game_id in result:
        print "Game ID:", game_id

    sql = "INSERT INTO outcome(game_id, winner_player_id, loser_player_id) VALUES(%(game_id)s, %(winner_player_id)s, %(loser_player_id)s);"

    if (winner_tournament_id == loser_tournament_id):
        exeSql(sql, {'game_id': game_id, 'winner_player_id': winner_player_id, 'loser_player_id': loser_player_id})
    else:
        raise AssertionError("Players are not of same tournament.")


def swissPairings(tournament_name):
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
