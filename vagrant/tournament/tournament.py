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
    """Remove tournaments from the database."""
    # sql statement
    sql = "DELETE FROM tournament;"

    # execute sql
    _exeSql(sql, None)


def deleteMatches():
    """Remove all the matches records from the database."""
    # sql statement
    sql = "DELETE FROM game;"

    # execute sql
    _exeSql(sql, None)


def deletePlayers():
    """Remove all the player records from the database."""
    # sql statement
    sql = "DELETE FROM player;"

    # execute sql
    _exeSql(sql, None)


def deleteOutcome():
    """Remove all matches played between players"""
    sql = "DELETE FROM outcome;"

    # execute sql
    _exeSql(sql, None)


def deleteStanding():
    """Remove all players standing"""
    sql = "DELETE FROM standing;"

    # execute sql
    _exeSql(sql, None)


def countPlayers():
    """Returns the number of players currently registered."""
    # sql statement
    sql = "SELECT COUNT(*) FROM player;"

    return int(_exeSql(sql, None)[0][0])


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
    _exeSql(sql, {'tournament_name': tournament_name})


def registerPlayer(tournament_name, player_name):
    """
    Adds a player to the tournament database.
    Args:
        tournament_name: name of the tournament player belongs
        player_name: the player's full name (need not be unique).
    """
    # sql statement
    sql = "SELECT tournament_id FROM tournament WHERE tournament_name=%(tournament_name)s;"

    # use bleach to
    # escapes or strips markup and attributes
    tournament_name = bleach.clean(tournament_name)

    # execute sql to get tournament_id
    tournament_id = int(_exeSql(sql, {'tournament_name': tournament_name})[0][0])

    # use bleach to
    # escapes or strips markup and attributes
    player_name = bleach.clean(player_name)

    # sql statement
    sql = "INSERT INTO player(tournament_id, player_name) VALUES(%(tournament_id)s, %(player_name)s);"

    # execute sql
    _exeSql(sql, {'tournament_id': tournament_id, 'player_name': player_name})


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

    return _exeSql(sql, {'tournament_name': tournament_name})


def createMatches(first_player_id, second_player_id):
    """
    Create/Fix match between players using their IDs. We can call this function
    in swissPairings() to automatically fix matches based on pairing algorithm.
    Args:
        first_player_id: first player's id.
        second_player_id: second player's id.
    """
    # create query
    sql = "SELECT tournament_id " \
          "FROM player " \
          "WHERE player_id=%(player_id)s;"

    # exe for first player
    [(first_player_tournament_id)] = _exeSql(sql, {'player_id': first_player_id})

    # exe for second player
    [(second_player_tournament_id)] = _exeSql(sql, {'player_id': second_player_id})

    # create query
    sql = "INSERT INTO game(tournament_id, first_player_id, second_player_id) " \
          "VALUES(%(tournament_id)s, %(first_player_id)s, %(second_player_id)s);"

    # verify players belong to same tournament
    if first_player_tournament_id == second_player_tournament_id:
        # exe query
        _exeSql(sql, {'tournament_id': first_player_tournament_id, 'first_player_id': first_player_id,
                     'second_player_id': second_player_id})
    else:
        raise AssertionError("Players are not of same tournament.")


def reportMatch(winner_id, loser_id):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    # create query
    sql = "SELECT tournament_id FROM player WHERE player_id = %(player_id)s;"

    # exe for winner
    [(winner_tournament_id)] = _exeSql(sql, {'player_id': winner_id})

    # exe for loser
    [(loser_tournament_id)] = _exeSql(sql, {'player_id': loser_id})

    # create query
    sql = "SELECT game_id " \
          "FROM game " \
          "WHERE (first_player_id=%(winner_id)s AND second_player_id=%(loser_id)s) " \
          "OR (first_player_id=%(loser_id)s AND second_player_id=%(winner_id)s);"

    # exe for game_id
    [(game_id,)] = _exeSql(sql, {'winner_id': winner_id, 'loser_id': loser_id})

    # create query
    sql = "INSERT INTO outcome(game_id, winner_player_id, loser_player_id) " \
          "VALUES(%(game_id)s, %(winner_player_id)s, %(loser_player_id)s);"

    # verify players are of same tournament
    if winner_tournament_id == loser_tournament_id:
        # exe query
        _exeSql(sql, {'game_id': game_id, 'winner_player_id': winner_id, 'loser_player_id': loser_id})
    else:
        raise AssertionError("Players are not of same tournament.")


def hasPlayedEarlier(first_player_id, second_player_id):
    # create query
    sql = "SELECT COUNT(*) " \
          "FROM game " \
          "WHERE (first_player_id=%(first_player_id)s AND second_player_id=%(second_player_id)s) " \
          "OR (first_player_id=%(second_player_id)s AND second_player_id=%(first_player_id)s);"

    # exe query
    matchCount = _exeSql(sql, {'first_player_id': first_player_id, 'second_player_id': second_player_id})

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
    players_group = _groupPlayers(players_standing)

    # print players_group, len(players_group)

    return _makePairs(players_group)


def _groupPlayers(players_standing):
    """
    Private method to be used by swissPairings() to group players based on their standings.
    Args:
        players_standing: ungrouped list of players w/ their win records.

    Returns: list of players grouped according to their standings.

    """
    # as we know players_standing is list of players in desc order
    # i.e player w/ most winning is on the top
    win_count = players_standing[0][2]

    # group's list
    group_list = []

    # player's in same group list
    grp_wise_player_list = []

    # loop thru list to group players
    # according to their standing
    for player in players_standing:
        # players of same standing
        if win_count == player[2]:
            grp_wise_player_list.append(player)
        # players of lower standing
        elif win_count > player[2]:
            group_list.append(grp_wise_player_list)
            win_count = player[2]
            grp_wise_player_list = []
            grp_wise_player_list.append(player)

    group_list.append(grp_wise_player_list)

    return group_list


def _makePairs(players_group):
    """
    Private method to be used by swissPairing() to pair players according to their
    standings.
    The algorithm uses graph data structure and 'blossom algorithm' to fix game between players
    of similiar standings.
    Args:
        players_group: list of players grouped according to their standings.

    Returns:
        A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    # create graph
    graph_ = nx.Graph()

    for group in players_group:
        # add players to graph
        graph_.add_nodes_from(group)

        # no. of players in each standing
        length = len(group)

        for idx, player in enumerate(group):
            while idx < (length - 1):
                # weight players randomly to ensure pairing are not always same
                wgt = random.randint(1, length)
                # connect nodes (players) only when they have not played
                # against each other
                if not hasPlayedEarlier(player[0], group[idx + 1][0]):
                    graph_.add_edge(player, group[idx + 1], weight=wgt)
                idx = idx + 1

    # get dict of paired palyers
    pair_dict = nx.max_weight_matching(graph_)

    # temp dict to store unique pairings
    temp_pair_dict = {}

    for key, value in pair_dict.iteritems():
        if not temp_pair_dict.has_key(key):
            if not key in temp_pair_dict.values():
                temp_pair_dict[key] = value

    # convert dict to list
    pair_list_frm_dict = temp_pair_dict.items()

    # final list which will carry
    # tuples of paired players
    swiss_pairs = []

    for pair in pair_list_frm_dict:
        temp_list_of_pairs = []
        for pl_info in pair:
            temp_list_of_pairs.append(pl_info[0])
            temp_list_of_pairs.append(pl_info[1])
        # convert list of pair to tuple and add
        # it to final list
        swiss_pairs.append(tuple(temp_list_of_pairs))

    return swiss_pairs


def _exeSql(sql, dict_):
    """
    Private method to be used by methods of this class to exe sql query.
    Args:
        sql: sql query
        dict_: dictionary of params that need to be replaced in sql query.

    Returns: resultSet returned by SELECT statements.
    """
    # db conn object
    conn = connect()

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # execute sql query
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
