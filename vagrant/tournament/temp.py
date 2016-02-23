from tournament import *

def test():
    deleteMatches()
    deletePlayers()
    deleteTournaments()
    # create tournament
    baseball_tournament_name = "jr. baseball tournament"
    football_tournament_name = "football tournament"
    createTournament(baseball_tournament_name)
    createTournament(football_tournament_name)
    # create players
    registerPlayer(baseball_tournament_name, "Roger Rabbit")
    registerPlayer(baseball_tournament_name, "Smith Jones")
    registerPlayer(football_tournament_name, "Jon Doe")
    registerPlayer(football_tournament_name, "Dan North")
    # check standings
    playerStandings(baseball_tournament_name)
    playerStandings(football_tournament_name)
    # create matches
    swissPairings(baseball_tournament_name)
    swissPairings(football_tournament_name)