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


if __name__ == '__main__':
    test()
