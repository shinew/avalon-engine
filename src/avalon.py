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
    """
    pids: [t]
    intgen: int -> int -> int
    return: [Player]

    """
    roles = get_default_roles(len(pids))
    shuffled_roles = shuffle(roles, intgen)
    return map(lambda pid, role: r.Player(pid, role), pids, shuffled_roles)

def expect_status(status):
    def h(f):
        def g(self, *args, **kwargs):
            if self.status != status:
                return
            return f(self, *args, **kwargs)
        return g
    return h

class Game(object):
    def __init__(self):
        self.pids = []
        self.players = []
        self.state = r.GameState()
        self.status = m.GameStatus.not_started
        self.current_leader = None
        self.current_team = []
        self.error = None

    @expect_status(m.GameStatus.not_started)
    def add_players(self, pids, intgen=randint):
        self.status = m.GameStatus.nominating_team
        self.pids = deepcopy(pids)
        self.current_leader = intgen(0, len(pids) - 1)
        self.players = assign_team_ids(pids, intgen)

    def copy(self):
        game = Game()
        game.pids = deepcopy(self.pids)
        game.players = deepcopy(self.players)
        game.state = self.state.copy()
        game.status = self.status
        game.current_leader = self.current_leader
        game.current_team = deepcopy(self.current_team)
        game.error = deepcopy(self.error)
