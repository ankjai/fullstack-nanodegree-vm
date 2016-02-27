#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#
import random

import bleach
import networkx as nx
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


def deleteStanding():
    """Remove all players standing"""
    sql = "DELETE FROM standing;"
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
    # create query
    sql = "SELECT player_id, player_name, player_win_count, player_game_count " \
          "FROM vw_player_details " \
          "WHERE tournament_name=%(tournament_name)s " \
          "ORDER BY player_win_count DESC;"

    return exeSql(sql, {'tournament_name': tournament_name})


def createMatchesByPlayerNames(first_player_name, second_player_name):
    # create query
    sql = "SELECT player_id, tournament_id " \
          "FROM player " \
          "WHERE player_name=%(player_name)s;"

    # exe for first player
    [(first_player_id, first_player_tournament_id)] = exeSql(sql, {'player_name': first_player_name})

    # exe for second player
    [(second_player_id, second_player_tournament_id)] = exeSql(sql, {'player_name': second_player_name})

    createMatches(first_player_tournament_id, second_player_tournament_id, first_player_id, second_player_id)


def createMatchesByPlayerIDs(first_player_id, second_player_id):
    # create query
    sql = "SELECT tournament_id " \
          "FROM player " \
          "WHERE player_id=%(player_id)s;"

    # exe for first player
    [(first_player_tournament_id)] = exeSql(sql, {'player_id': first_player_id})

    # exe for second player
    [(second_player_tournament_id)] = exeSql(sql, {'player_id': second_player_id})

    createMatches(first_player_tournament_id, second_player_tournament_id, first_player_id, second_player_id)


def createMatches(first_player_tournament_id, second_player_tournament_id, first_player_id, second_player_id):
    # create query
    sql = "INSERT INTO game(tournament_id, first_player_id, second_player_id) " \
          "VALUES(%(tournament_id)s, %(first_player_id)s, %(second_player_id)s);"

    # verify
    if first_player_tournament_id == second_player_tournament_id:
        # exe query
        exeSql(sql, {'tournament_id': first_player_tournament_id, 'first_player_id': first_player_id,
                     'second_player_id': second_player_id})
    else:
        raise AssertionError("Players are not of same tournament.")


def reportMatchByPlayerNames(winner_name, loser_name):
    # create query
    sql = "SELECT player_id, tournament_id FROM player WHERE player_name = %(player_name)s;"

    # exe for winner
    [(winner_player_id, winner_tournament_id)] = exeSql(sql, {'player_name': winner_name})

    # exe for loser
    [(loser_player_id, loser_tournament_id)] = exeSql(sql, {'player_name': loser_name})

    # verify players are of same tournament
    if winner_tournament_id == loser_tournament_id:
        reportMatchByPlayerIDs(winner_player_id, loser_player_id)
    else:
        raise AssertionError("Players are not of same tournament.")


def reportMatchByPlayerIDs(winner_id, loser_id):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # create query
    sql = "SELECT tournament_id FROM player WHERE player_id = %(player_id)s;"

    # exe for winner
    [(winner_tournament_id)] = exeSql(sql, {'player_id': winner_id})

    # exe for loser
    [(loser_tournament_id)] = exeSql(sql, {'player_id': loser_id})

    # create query
    sql = "SELECT game_id " \
          "FROM game " \
          "WHERE (first_player_id=%(winner_id)s AND second_player_id=%(loser_id)s) " \
          "OR (first_player_id=%(loser_id)s AND second_player_id=%(winner_id)s);"

    # exe for game_id
    [(game_id,)] = exeSql(sql, {'winner_id': winner_id, 'loser_id': loser_id})

    # verify players are of same tournament
    if winner_tournament_id == loser_tournament_id:
        reportMatch(game_id, winner_id, loser_id)
    else:
        raise AssertionError("Players are not of same tournament.")


def reportMatch(game_id, winner_player_id, loser_player_id):
    # create query
    sql = "INSERT INTO outcome(game_id, winner_player_id, loser_player_id) " \
          "VALUES(%(game_id)s, %(winner_player_id)s, %(loser_player_id)s);"

    # exe query
    exeSql(sql, {'game_id': game_id, 'winner_player_id': winner_player_id, 'loser_player_id': loser_player_id})


def hasPlayedEarlier(first_player_id, second_player_id):
    # create query
    sql = "SELECT COUNT(*) " \
          "FROM game " \
          "WHERE (first_player_id=%(first_player_id)s AND second_player_id=%(second_player_id)s) " \
          "OR (first_player_id=%(second_player_id)s AND second_player_id=%(first_player_id)s);"

    # exe query
    matchCount = exeSql(sql, {'first_player_id': first_player_id, 'second_player_id': second_player_id})

    if int(matchCount[0][0]) == 0:
        return False
    else:
        return True


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
    # retrieve current player standing from DB
    players_standing = playerStandings(tournament_name)

    # group players by their standing (win_count)
    players_group = groupPlayers(players_standing)

    print players_group, len(players_group)

    makePairs(players_group)


def groupPlayers(players_standing):
    # as we know players_standing is list of players in desc order
    # i.e player w/ most winning is on the top
    win_count = players_standing[0][2]

    # group's list
    list_ = []
    # player's in same group list
    inner_list = []

    for player in players_standing:
        # players of same standing
        if win_count == player[2]:
            inner_list.append(player)
        # players of lower standing
        elif win_count > player[2]:
            list_.append(inner_list)
            win_count = player[2]
            inner_list = []
            inner_list.append(player)

    list_.append(inner_list)

    return list_


def makePairs(players_group):
    pairs = []
    # graph_ = nx.Graph()
    # graph_.add_nodes_from(players_group)

    for group in players_group:

        graph_ = nx.Graph()
        graph_.add_nodes_from(group)

        length = len(group)

        for idx, player in enumerate(group):
            print "INFO: ", length, idx, player
            while idx < (length - 1):
                wgt = random.randint(1, length)
                print "group", group[idx + 1], " idx", idx, "wgt", wgt
                if hasPlayedEarlier(player[0], group[idx + 1][0]):
                    print "PLAYED"
                else:
                    print "NOT PLAYED"
                    graph_.add_edge(player, group[idx + 1], weight=wgt)
                idx = idx + 1

    pairing = nx.max_weight_matching(graph_)

    print "PAIRING", pairing
    return pairs


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
