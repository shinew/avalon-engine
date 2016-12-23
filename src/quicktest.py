import model as m
import rules as r
import avalon
import random

def print_game(game):
    print game
    print '-------------'

def positive_test(players, guess_merlin_right):
    g = avalon.Game(lambda a,b: a)
    pids = range(players)
    g.add_players(pids)
    print g.players
    print g.get_visibility()

    # 3 missions, each going until the 5th nomination, and the mission passes
    for mission in range(3):
        size = g.get_expected_team_size()
        for nomination in range(4):
            print 'nomination: {}'.format(nomination)
            g.nominate_team(random.sample(pids, r.size_of_nominated_team(mission, players)))
            print_game(g)
            yeses = random.sample(pids, random.randint(0, r.num_votes_for_team(players) - 1))
            g.vote_for_team(map(lambda p: r.PlayerVote(p, m.Vote.yes if p in yeses else m.Vote.no), pids))
            print_game(g)

        print 'nomination: 4'
        g.nominate_team(range(size))
        g.vote_for_team(map(lambda p: r.PlayerVote(p, m.Vote.yes), pids))
        print_game(g)

        g.vote_for_mission(map(lambda p: r.PlayerVote(p, m.Vote.yes), range(size)))
        print 'missioning'
        print_game(g)

    # guessed merlin incorrectly
    print g.players
    if guess_merlin_right:
        g.guess_merlin(0)
    else:
        g.guess_merlin(1)
    print_game(g)


def negative_test(players):
    g = avalon.Game(lambda a,b: a)
    pids = range(players)
    g.add_players(pids)
    print g.players
    print g.get_visibility()

    # 2 missions, each going until the 5th nomination, and the mission passes
    for mission in range(2):
        size = g.get_expected_team_size()
        for nomination in range(4):
            print 'nomination: {}'.format(nomination)
            g.nominate_team(random.sample(pids, r.size_of_nominated_team(mission, players)))
            print_game(g)
            yeses = random.sample(pids, random.randint(0, r.num_votes_for_team(players) - 1))
            g.vote_for_team(map(lambda p: r.PlayerVote(p, m.Vote.yes if p in yeses else m.Vote.no), pids))
            print_game(g)

        print 'nomination: 4'
        g.nominate_team(range(size))
        g.vote_for_team(map(lambda p: r.PlayerVote(p, m.Vote.yes), pids))
        print_game(g)

        g.vote_for_mission(map(lambda p: r.PlayerVote(p, m.Vote.yes), range(size)))
        print 'missioning'
        print_game(g)
    # 3 missions that fail
    for mission in range(2, 5):
        size = g.get_expected_team_size()
        for nomination in range(4):
            print 'nomination: {}'.format(nomination)
            g.nominate_team(random.sample(pids, r.size_of_nominated_team(mission, players)))
            print_game(g)
            yeses = random.sample(pids, random.randint(0, r.num_votes_for_team(players) - 1))
            g.vote_for_team(map(lambda p: r.PlayerVote(p, m.Vote.yes if p in yeses else m.Vote.no), pids))
            print_game(g)

        print 'nomination: 4'
        evils = range(players - 2, players)
        g.nominate_team(range(size - 2) + evils)
        g.vote_for_team(map(lambda p: r.PlayerVote(p, m.Vote.yes), pids))
        print_game(g)

        g.vote_for_mission(map(lambda p: r.PlayerVote(p, m.Vote.yes), range(size - 2)) + map(lambda p: r.PlayerVote(p, m.Vote.no), evils))
        print 'missioning'
        print_game(g)

#positive_test(5, False)
#positive_test(10, True)
#negative_test(5)
negative_test(10)
