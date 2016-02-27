from tournament import *


def test():
    deleteOutcome()
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    # create tournament
    baseball_tournament_name = "jr. baseball tournament"
    createTournament(baseball_tournament_name)
    # create players
    registerPlayer(baseball_tournament_name, "Roger Rabbit")
    registerPlayer(baseball_tournament_name, "Smith Jones")
    registerPlayer(baseball_tournament_name, "Jon Doe")
    registerPlayer(baseball_tournament_name, "Dan North")
    registerPlayer(baseball_tournament_name, "John Smith")
    registerPlayer(baseball_tournament_name, "William Hunt")
    registerPlayer(baseball_tournament_name, "Daniel D")
    registerPlayer(baseball_tournament_name, "Jessica Jones")

    swissPairings(baseball_tournament_name)

    # create matches
    # rnd 1
    createMatchesByPlayerNames("Roger Rabbit", "Smith Jones")
    reportMatchByPlayerNames("Roger Rabbit", "Smith Jones")
    createMatchesByPlayerNames("Jon Doe", "Dan North")
    reportMatchByPlayerNames("Jon Doe", "Dan North")
    createMatchesByPlayerNames("John Smith", "William Hunt")
    reportMatchByPlayerNames("John Smith", "William Hunt")
    createMatchesByPlayerNames("Daniel D", "Jessica Jones")
    reportMatchByPlayerNames("Daniel D", "Jessica Jones")

    swissPairings(baseball_tournament_name)

    # rnd 2
    # winners from rnd 1
    createMatchesByPlayerNames("Roger Rabbit", "Jon Doe")
    reportMatchByPlayerNames("Roger Rabbit", "Jon Doe")
    createMatchesByPlayerNames("John Smith", "Daniel D")
    reportMatchByPlayerNames("John Smith", "Daniel D")
    # loosers from rnd 1
    createMatchesByPlayerNames("Smith Jones", "Dan North")
    reportMatchByPlayerNames("Smith Jones", "Dan North")
    createMatchesByPlayerNames("William Hunt", "Jessica Jones")
    reportMatchByPlayerNames("William Hunt", "Jessica Jones")

    swissPairings(baseball_tournament_name)

    # rnd 3
    # winners from rnd 2
    createMatchesByPlayerNames("Roger Rabbit", "John Smith")
    reportMatchByPlayerNames("Roger Rabbit", "John Smith")
    createMatchesByPlayerNames("Smith Jones", "William Hunt")
    reportMatchByPlayerNames("Smith Jones", "William Hunt")
    # loosers from rnd 2
    createMatchesByPlayerNames("Jon Doe", "Daniel D")
    reportMatchByPlayerNames("Jon Doe", "Daniel D")
    createMatchesByPlayerNames("Dan North", "Jessica Jones")
    reportMatchByPlayerNames("Dan North", "Jessica Jones")

    swissPairings(baseball_tournament_name)


def testPair():
    deleteOutcome()
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    # create tournament
    tournament_name = "tt tournament"
    createTournament(tournament_name)
    registerPlayer(tournament_name, "Twilight Sparkle")
    registerPlayer(tournament_name, "Fluttershy")
    registerPlayer(tournament_name, "Applejack")
    registerPlayer(tournament_name, "Pinkie Pie")
    registerPlayer(tournament_name, "Rarity")
    registerPlayer(tournament_name, "Rainbow Dash")
    registerPlayer(tournament_name, "Princess Celestia")
    registerPlayer(tournament_name, "Princess Luna")

    swissPairings(tournament_name)


if __name__ == '__main__':
    test()
    # testPair()
