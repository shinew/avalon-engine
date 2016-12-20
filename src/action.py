"""
User-facing API.

Every call may throw.

"""
import random
import model as m
import helper as h

def create_game():
    return m.Game()

def start_game(game, pids, intgen=random.randint):
    """
    Assigns roles to the given pids according to intgen.
    intgen: int -> int -> int

    """
    assert game.state == m.GameState.adding_players
    assert len(set(pids)) == len(pids)
    game.players = h.assign_team_ids(pids, intgen)
    game.start = 0
    game.state = m.GameState.team_selection
    game.current_leader = game.players[intgen(0, len(game.players) - 1)]

def get_visibility(game):
    """
    Computes a mapping of pids to which players should know of which others.
    return: {pid: [players]}

    """
    assert game.state != m.GameState.adding_players
    return dict([(p.pid, h.see_other_players(p, game.players)) for p in game.players])


def select_team(game, pid, pids):
    """
    Nominates a team.

    """
    assert game.state == m.GameState.team_selection
    assert game.current_leader.pid == pid
    game.
