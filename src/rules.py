'''
Various rules and parameters of the game, with stateless transformations.

'''
from copy import deepcopy
from collections import namedtuple

import model as m
from helper import index_of


MIN_PLAYERS = 5
MAX_PLAYERS = 10
NUM_NOMINATIONS = 5
NUM_QUESTS = 5

Player = namedtuple('Player', 'pid role')
PlayerVote = namedtuple('PlayerVote', 'pid vote')

class GameState(object):
    def __init__(self):
        self.quests = [m.VoteStatus.unknown] * NUM_QUESTS
        self._clear_nominations()
        self.merlin = m.MerlinStatus.alive

    # -- computed properties --

    @property
    def current_quest(self):
        return index_of(lambda x: x == m.VoteStatus.unknown, self.quests)

    @property
    def current_nomination(self):
        return index_of(lambda x: x == m.VoteStatus.unknown, self.nominations)

    # ^^ computed properties ^^

    def increment_quest(self, vote_status):
        if self.current_quest is not None:
            self.quests[self.current_quest] = vote_status
            self._clear_nominations()

    def increment_nomination(self, vote_status):
        if self.current_nomination is not None:
            self.nominations[self.current_nomination] = vote_status

    def does_good_win(self):
        return (self.does_good_win_minus_merlin() and
                self.merlin is m.MerlinStatus.alive)

    def does_good_win_excluding_merlin(self):
        return self.quests.count(m.VoteStatus.succeeded) >= 3

    def does_evil_win(self):
        return (self.quests.count(m.VoteStatus.failed) >= 3 or
                self.merlin is m.MerlinStatus.dead or
                self.nominations.count(m.VoteStatus.failed) == 5)

    def _clear_nominations(self):
        self.nominations = [m.VoteStatus.unknown] * NUM_NOMINATIONS

    def __str__(self):
        mapping = {
            m.VoteStatus.succeeded: 'Y',
            m.VoteStatus.failed: 'X',
            m.VoteStatus.unknown: '?',
        }
        def pretty_print(lst):
            return ''.join(map(lambda x: mapping[x], lst))
        return 'Quests: {}\nNominations: {}'.format(*map(pretty_print, [self.quests, self.nominations]))

def num_good_players(num_players):
    mapping = {
        5: 3,
        6: 4,
        7: 4,
        8: 5,
        9: 6,
        10: 6,
    }
    return mapping.get(num_players)

def num_evil_players(num_players):
    return num_players - num_good_players(num_players)

def role_to_team(role):
    if role is None:
        return None
    good_roles = [m.Role.servant, m.Role.merlin, m.Role.percival]
    return m.Team.good if role in good_roles else m.Team.evil

def is_good(role):
    return role_to_team(role) is m.Team.good

def is_evil(role):
    return role_to_team(role) is m.Team.evil

def size_of_proposed_team(quest, num_players):
    # quest is 0-indexed
    mapping = [
        [2, 2, 2, 3, 3, 3],
        [3, 3, 3, 4, 4, 4],
        [2, 4, 3, 4, 4, 4],
        [3, 3, 4, 5, 5, 5],
        [3, 4, 4, 5, 5, 5],
    ]
    try:
        return mapping[quest][num_players - MIN_PLAYERS]
    except KeyError:
        return None

def num_votes_for_team(num_players):
    return num_players / 2 + 1

def num_votes_for_quest(quest, num_players):
    if quest == 3 and num_players >= 7:
        return size_of_proposed_team(quest, num_players) - 1
    else:
        return size_of_proposed_team(quest, num_players)

def is_quest_vote_valid(vote, role):
    return is_evil(role) or (vote is m.Vote.yes)

def can_see_which_other_players(player, players):
    '''
    Returns the pids for which this player can know of the others.
    player -> [player] -> (Role, [player])?

    '''
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
        return None
