"""
Various rules and parameters of the game, with stateless transformations.

"""
from copy import deepcopy
from collections import namedtuple

import model as m


MIN_PLAYERS = 5
MAX_PLAYERS = 10
NUM_NOMINATIONS = 5
NUM_QUESTS = 5


Player = namedtuple('Player', 'pid role')

class GameState(object):
    def __init__(self):
        self.quests = [m.VoteStatus.unknown] * NUM_QUESTS
        self.nominations = [m.VoteStatus.unknown] * NUM_NOMINATIONS
        self.merlin = m.MerlinStatus.alive

    def copy(self):
        return deepcopy(self)


def num_good_players(num_players):
    mapping = {
        5: 3,
        6: 4,
        7: 4,
        8: 5,
        9: 6,
        10: 6,
    }
    return mapping[num_players]

def num_evil_players(num_players):
    return num_players - num_good_players(num_players)

def role_to_team(role):
    good_roles = [m.Role.servant, m.Role.merlin, m.Role.percival]
    return m.Team.good if role in good_roles else m.Team.evil

def is_good(role):
    return role_to_team(role) is m.Team.good

def is_evil(role):
    return role_to_team(role) is m.Team.evil

def size_of_proposed_team(quest_num, num_players):
    mapping = [
        [2, 2, 2, 3, 3, 3],
        [3, 3, 3, 4, 4, 4],
        [2, 4, 3, 4, 4, 4],
        [3, 3, 4, 5, 5, 5],
        [3, 4, 4, 5, 5, 5],
    ]
    return mapping[quest_num][num_players - MIN_PLAYERS]

def can_go_on_quest(votes):
    return votes.count(m.Vote.yes) * 2 > len(votes)

def does_quest_succeed(quest_num, votes):
    num_fails = votes.count(m.Vote.no)
    if quest_num == 3 and len(votes) >= 7:
        return num_fails <= 1
    else:
        return num_fails == 0

def does_good_win(game_status):
    return (game_status.quests.count(m.VoteStatus.succeeded) == 3 and
            game_status.merlin is m.MerlinStatus.alive)

def does_evil_win(game_status):
    return (game_status.quests.count(m.VoteStatus.failed) >= 3 or
            game_status.merlin is m.MerlinStatus.dead or
            game_status.nominations.count(m.VoteStatus.failed) == 5)

def is_quest_vote_valid(vote, role):
    return is_evil(role) or (vote is m.Vote.yes)

def can_see_which_other_players(player, players):
    """
    Returns the pids for which this player can know of the others.
    player -> [player] -> (Role, [player])

    """
    if player.role is m.Role.merlin:
        return (m.Role.minion,
                filter(lambda p: is_evil(p.role) and p.role is not m.Role.mordred, players))
    elif player.role is m.Role.percival:
        return (m.Role.merlin,
                filter(lambda p: p.role in [m.Role.morgana, m.Role.merlin], players))
    elif player.role is m.Role.oberon:
        return (m.Role.minion,
                filter(lambda p: is_evil(p.role) and p.role is not m.Role.oberon, players))
    elif is_evil(player.role):
        return (m.Role.minion,
                filter(lambda p: (p != player and
                                  is_evil(p.role) and
                                  p.role is not m.Role.oberon), players))
    else:
        return []
