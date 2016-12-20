from copy import deepcopy
from random import randint
from collections import namedtuple

import model as m
import rules as r
from helper import shuffle

def get_default_good_roles(num_players):
    num_good_players = r.num_good_players(num_players)
    return [m.Role.merlin] + [m.Role.servant] * (num_good_players - 1)

def get_default_evil_roles(num_players):
    num_evil_players = r.num_evil_players(num_players)
    return [m.Role.assassin] + [m.Role.minion] * (num_evil_players - 1)

def get_default_roles(num_players):
    return get_default_good_roles(num_players) + get_default_evil_roles(num_players)

def assign_team_ids(pids, intgen):
    '''
    pids: [t]
    intgen: int -> int -> int
    return: [Player]

    '''
    roles = get_default_roles(len(pids))
    shuffled_roles = shuffle(roles, intgen)
    return map(lambda pid, role: r.Player(pid, role), pids, shuffled_roles)

def expect_status(status):
    def h(f):
        def g(self, *args, **kwargs):
            if self.status != status:
                self.status = m.GameStatus.error
                self.error = 'expected status {}, given {}'.format(status, self.status)
                return
            return f(self, *args, **kwargs)
        return g
    return h

def expect_initialized(f):
    def g(self, *args, **kwargs):
        if self.status in [m.GameStatus.error, m.GameStatus.not_started]:
            self.error = 'ran a method that requires initialization'
            return
        return f(self, *args, **kwargs)
    return g

class Game(object):
    def __init__(self):
        self.pids = []
        self.players = []
        self.state = r.GameState()
        self.status = m.GameStatus.not_started
        self.current_leader = 0
        self.current_team = []
        self.current_quest = 0
        self.current_proposal = 0
        self.error = None

    @expect_status(m.GameStatus.not_started)
    def add_players(self, pids, intgen=randint):
        if (not (r.MIN_PLAYERS <= len(pids) <= r.MAX_PLAYERS) or
            len(pids) != len(set(pids))):
            self.status = m.GameStatus.error
            self.error = 'too few players'
            return
        self.status = m.GameStatus.nominating_team
        self.pids = deepcopy(pids)
        self.current_leader = intgen(0, len(pids) - 1)
        self.players = assign_team_ids(pids, intgen)

    @expect_initialized
    def get_visibility(self):
        '''
        Returns a mapping of pid -> (Role, [pid])?

        '''
        def strip_roles(result):
            if result:
                role, players = result
                return (role, [p.pid for p in players])
        return dict([(p.pid, strip_roles(r.can_see_which_other_players(p, self.players))) for p in self.players])

    @expect_status(m.GameStatus.nominating_team)
    def nominate_team(self, pids):
        if (any(p not in self.pids for p in pids) or
            len(pids) != len(set(pids)) or
            len(pids) != r.size_of_proposed_team(self.current_quest, len(self.pids))):
            self.status = m.GameStatus.error
            self.error = 'bad team nomination'
            return
        self.status = m.GameStatus.voting_for_team
        self.current_team = deepcopy(pids)

    @property
    @expect_initialized
    def leader(self):
        return self.pids[self.current_leader]

    def copy(self):
        return deepcopy(self)
