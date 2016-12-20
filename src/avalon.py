from random import randint
from collections import namedtuple

import model as m
import rules as r
import helper

def get_default_good_roles(num_players):
    num_good_players = r.num_good_players(num_players)
    return [m.Role.merlin] + [m.Role.servant] * (num_good_players - 1)

def get_default_bad_roles(num_players):
    num_bad_players = r.num_bad_players(num_players)
    return [m.Role.assassin] + [m.Role.minion] * (num_bad_players - 1)

def assign_team_ids(pids, intgen=randint):
    """
    pids: [t]
    intgen: int -> int -> int
    return: [Player]

    """
    roles = get_roles(len(pids))
    roles = helper.shuffle(roles, intgen) return map(lambda p,r: m.Player(p, r), pids, roles)

class Game(object):
    def __init__(pids):
        self.pids = set(pids)
        self.players = map()
