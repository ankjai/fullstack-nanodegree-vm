#!/usr/bin/env python
#
# Test cases for tournament.py
# These tests are not exhaustive, but they should cover the majority of cases.
#
# If you do add any of the extra credit options, be sure to add/modify these test cases
# as appropriate to account for your module's added functionality.

from tournament import *


def testCount():
    """
    Test for initial player count,
             player count after 1 and 2 players registered,
             player count after players deleted.
    """
    deleteStanding()
    deleteOutcome()
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    c = countPlayers()
    if c == '0':
        raise TypeError(
            "countPlayers should return numeric zero, not string '0'.")
    if c != 0:
        raise ValueError("After deletion, countPlayers should return zero.")
    print "1. countPlayers() returns 0 after initial deletePlayers() execution."
    tournament_name = "Chess Knockout Tournament"
    createTournament(tournament_name)
    registerPlayer(tournament_name, "Chandra Nalaar")
    c = countPlayers()
    if c != 1:
        raise ValueError(
            "After one player registers, countPlayers() should be 1. Got {c}".format(c=c))
    print "2. countPlayers() returns 1 after one player is registered."
    registerPlayer(tournament_name, "Jace Beleren")
    c = countPlayers()
    if c != 2:
        raise ValueError(
            "After two players register, countPlayers() should be 2. Got {c}".format(c=c))
    print "3. countPlayers() returns 2 after two players are registered."
    deletePlayers()
    c = countPlayers()
    if c != 0:
        raise ValueError(
            "After deletion, countPlayers should return zero.")
    print "4. countPlayers() returns zero after registered players are deleted.\n5. Player records successfully deleted."


def testStandingsBeforeMatches():
    """
    Test to ensure players are properly represented in standings prior
    to any matches being reported.
    """
    deleteStanding()
    deleteOutcome()
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament_name = "Cricket Tournament"
    createTournament(tournament_name)
    registerPlayer(tournament_name, "Melpomene Murray")
    registerPlayer(tournament_name, "Randy Schwartz")
    standings = playerStandings(tournament_name)
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
    """
    Test that matches are reported properly.
    Test to confirm matches are deleted properly.
    """
    deleteStanding()
    deleteOutcome()
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament_name = "Baseball Tournament"
    createTournament(tournament_name)
    registerPlayer(tournament_name, "Bruno Walton")
    registerPlayer(tournament_name, "Boots O'Neal")
    registerPlayer(tournament_name, "Cathy Burton")
    registerPlayer(tournament_name, "Diane Grant")
    standings = playerStandings(tournament_name)
    [id1, id2, id3, id4] = [row[0] for row in standings]
    createMatches(id1, id2)
    createMatches(id3, id4)
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    standings = playerStandings(tournament_name)
    for (i, n, w, m) in standings:
        if m != 1:
            raise ValueError("Each player should have one match recorded.")
        if i in (id1, id3) and w != 1:
            raise ValueError("Each match winner should have one win recorded.")
        elif i in (id2, id4) and w != 0:
            raise ValueError("Each match loser should have zero wins recorded.")
    print "7. After a match, players have updated standings."
    deleteOutcome()
    deleteMatches()
    standings = playerStandings(tournament_name)
    if len(standings) != 4:
        raise ValueError("Match deletion should not change number of players in standings.")
    for (i, n, w, m) in standings:
        if m != 0:
            raise ValueError("After deleting matches, players should have zero matches recorded.")
        if w != 0:
            raise ValueError("After deleting matches, players should have zero wins recorded.")
    print "8. After match deletion, player standings are properly reset.\n9. Matches are properly deleted."


def testPairings():
    """
    Test that pairings are generated properly both before and after match reporting.
    """
    deleteStanding()
    deleteOutcome()
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    tournament_name = "Baseball Tournament"
    createTournament(tournament_name)
    registerPlayer(tournament_name, "Twilight Sparkle")
    registerPlayer(tournament_name, "Fluttershy")
    registerPlayer(tournament_name, "Applejack")
    registerPlayer(tournament_name, "Pinkie Pie")
    registerPlayer(tournament_name, "Rarity")
    registerPlayer(tournament_name, "Rainbow Dash")
    registerPlayer(tournament_name, "Princess Celestia")
    registerPlayer(tournament_name, "Princess Luna")
    standings = playerStandings(tournament_name)
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    pairings = swissPairings(tournament_name)

    # check length of pairings list
    _chkPairLength(pairings)

    createMatches(id1, id2)
    createMatches(id3, id4)
    createMatches(id5, id6)
    createMatches(id7, id8)
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)
    pairings = swissPairings(tournament_name)

    # check length of pairings list
    _chkPairLength(pairings)

    # check for valid pairs
    _chkValidPairs(standings, pairings)

    print "10. After one match, players with one win are properly paired."


def testMultiTournament():
    deleteStanding()
    deleteOutcome()
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    chess_tournament = "Chess Tournament"
    createTournament(chess_tournament)
    cricket_tournament = "Cricket Tournament"
    createTournament(cricket_tournament)
    # create chess players
    registerPlayer(chess_tournament, "Roger Rabbit")
    registerPlayer(chess_tournament, "Smith Jones")
    registerPlayer(chess_tournament, "Jon Doe")
    registerPlayer(chess_tournament, "Dan North")
    registerPlayer(chess_tournament, "John Smith")
    registerPlayer(chess_tournament, "William Hunt")
    registerPlayer(chess_tournament, "Daniel D")
    registerPlayer(chess_tournament, "Jessica Jones")
    # create cricket players
    registerPlayer(cricket_tournament, "Stacey Mckinney")
    registerPlayer(cricket_tournament, "Tommie Obrien")
    registerPlayer(cricket_tournament, "Wade Patterson")
    registerPlayer(cricket_tournament, "Dale Reed")
    registerPlayer(cricket_tournament, "Freddie Tran")
    registerPlayer(cricket_tournament, "Darrell Lucas")
    registerPlayer(cricket_tournament, "Jennifer Hoffman")
    registerPlayer(cricket_tournament, "Gwendolyn Scott")

    # chess tournament
    chess_standings = playerStandings(chess_tournament)
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in chess_standings]

    # get chess swiss pairing
    chess_pairings = swissPairings(chess_tournament)

    # check length of chess pairings list
    _chkPairLength(chess_pairings)

    # create and report match result for chess tournament
    createMatches(id1, id2)
    createMatches(id3, id4)
    createMatches(id5, id6)
    createMatches(id7, id8)
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)

    # cricket tournament
    cricket_standings = playerStandings(cricket_tournament)
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in cricket_standings]

    # get cricket swiss pairing
    cricket_pairings = swissPairings(cricket_tournament)

    # check length of cricket pairings list
    _chkPairLength(cricket_pairings)

    # create and report match result for cricket tournament
    createMatches(id1, id2)
    createMatches(id3, id4)
    createMatches(id5, id6)
    createMatches(id7, id8)
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)

    # get swissPairing of chess tournament after 1st rnd
    chess_pairings = swissPairings(chess_tournament)

    # check length of pairings list
    _chkPairLength(chess_pairings)

    # check for valid pairs
    _chkValidPairs(chess_standings, chess_pairings)

    # get swissPairing of cricket tournament after 1st rnd
    cricket_pairings = swissPairings(cricket_tournament)

    # check length of pairings list
    _chkPairLength(cricket_pairings)

    # check for valid pairs
    _chkValidPairs(cricket_standings, cricket_pairings)

    print "11. In both the tournaments after 1st round, players with one win are properly paired."


def _chkPairLength(pairings):
    if len(pairings) != 4:
        raise ValueError(
            "For eight players, swissPairings should return 4 pairs. Got {pairs}".format(pairs=len(pairings)))


def _chkValidPairs(standings, pairings):
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]

    [(pid1, pname1, pid2, pname2), (pid3, pname3, pid4, pname4), (pid5, pname5, pid6, pname6),
     (pid7, pname7, pid8, pname8)] = pairings
    possible_pairs = set([frozenset([id1, id3]), frozenset([id1, id5]),
                          frozenset([id1, id7]), frozenset([id3, id5]),
                          frozenset([id3, id7]), frozenset([id5, id7]),
                          frozenset([id2, id4]), frozenset([id2, id6]),
                          frozenset([id2, id8]), frozenset([id4, id6]),
                          frozenset([id4, id8]), frozenset([id6, id8])
                          ])
    actual_pairs = set(
        [frozenset([pid1, pid2]), frozenset([pid3, pid4]), frozenset([pid5, pid6]), frozenset([pid7, pid8])])
    for pair in actual_pairs:
        if pair not in possible_pairs:
            raise ValueError(
                "After one match, players with one win should be paired.")


if __name__ == '__main__':
    testCount()
    testStandingsBeforeMatches()
    testReportMatches()
    testPairings()
    testMultiTournament()
    print "Success!  All tests pass!"
