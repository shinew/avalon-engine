'''
An implementation of the Avalon game.

'''
from collections import namedtuple
from copy import deepcopy
from functools import wraps
from random import randint

import model as m
import rules as r
from helper import shuffle, first_of

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
        @wraps(f)
        def g(self, *args, **kwargs):
            if self.status != status:
                self._update_error('expected previous status {}, given {}'.format(status, self.status))
                return
            return f(self, *args, **kwargs)
        return g
    return h

def expect_initialized(f):
    @wraps(f)
    def g(self, *args, **kwargs):
        if self.status is m.GameStatus.not_started:
            self._update_error('ran a method that requires initialization')
            return
        return f(self, *args, **kwargs)
    return g

class Game(object):
    def __init__(self, intgen=randint):
        self.status = m.GameStatus.not_started
        self.pids = []
        self.players = []
        self.state = r.GameState()
        self.current_team = set()  # set of pids

        self._leader_idx = 0  # index of pids
        self._winner = None
        self._errors = []
        self._intgen = intgen

    @expect_status(m.GameStatus.done)
    def get_winner(self):
        return self._winner

    def set_winner(self, winner):
        self.status = m.GameStatus.done
        self._winner = winner

    winner = property(get_winner, set_winner)

    @property
    @expect_initialized
    def num_players(self):
        return len(self.pids)

    @property
    @expect_initialized
    def leader(self):
        return self.pids[self._leader_idx]

    @expect_status(m.GameStatus.not_started)
    def add_players(self, pids):
        if (not (r.MIN_PLAYERS <= len(pids) <= r.MAX_PLAYERS) or
            len(pids) != len(set(pids))):
            self._update_error('wrong number of players')
            return
        self.status = m.GameStatus.nominating_team
        self.pids = deepcopy(pids)
        self._leader_idx = self._intgen(0, len(pids) - 1)
        self.players = assign_team_ids(pids, self._intgen)

    @expect_status(m.GameStatus.nominating_team)
    def nominate_team(self, pids):
        if (not self._are_unique_valid_pids(pids) or
            len(pids) != r.size_of_proposed_team(self.state.current_quest, self.num_players)):
            self._update_error('bad nominate-team')
            return

        self.status = m.GameStatus.voting_for_team
        self.current_team = set(deepcopy(pids))

    @expect_status(m.GameStatus.voting_for_team)
    def vote_for_team(self, pid_votes):
        if (not self._are_unique_valid_pids([pv.pid for pv in pid_votes]) or
            len(pid_votes) < self.num_players):
            self._update_error('bad vote-for-team')
            return

        yes_votes = len([pv for pv in pid_votes if pv.vote == m.Vote.yes])
        if yes_votes >= r.num_votes_for_team(self.num_players):
            self.status = m.GameStatus.voting_for_mission
            self.state.increment_nomination(m.VoteStatus.succeeded)
        else:
            self.state.increment_nomination(m.VoteStatus.failed)
            if self.state.does_evil_win():
                self.winner = m.Team.evil
            else:
                self.status = m.GameStatus.nominating_team
                self._increment_leader()

    @expect_status(m.GameStatus.voting_for_mission)
    def vote_for_mission(self, pid_votes):
        if (not self._are_unique_valid_pids([pv.pid for pv in pid_votes]) or
            set([pv.pid for pv in pid_votes]) != self.current_team or
            not all(r.is_quest_vote_valid(pv.vote, self.pid_to_role(pv.pid)) for pv in pid_votes)):
            self._update_error('bad vote-for-mission')
            return

        self.current_team = set()
        yes_votes = [pv.vote for pv in pid_votes].count(m.Vote.yes)
        if yes_votes >= r.num_votes_for_quest(self.state.current_quest, self.num_players):
            self.state.increment_quest(m.VoteStatus.succeeded)
        else:
            self.state.increment_quest(m.VoteStatus.failed)

        if self.state.does_good_win_excluding_merlin():
            self.status = m.GameStatus.guessing_merlin
        elif self.state.does_evil_win():
            self.winner = m.Team.evil
        else:
            self.status = m.GameStatus.nominating_team
            self._increment_leader()

    @expect_status(m.GameStatus.guessing_merlin)
    def guess_merlin(self, pid):
        if self.pid_to_role(pid) is m.Role.merlin:
            self.winner = m.Team.evil
        else:
            self.winner = m.Team.good

    @expect_initialized
    def get_visibility(self):
        '''
        @return: { pid : (Role, [pid])? }
        Role being what pid sees the other pids as (either merlin or minion).

        '''
        def strip_roles(result):
            if result:
                role, players = result
                return (role, [p.pid for p in players])

        return dict([(p.pid, strip_roles(r.can_see_which_other_players(p, self.players))) for p in self.players])

    @expect_initialized
    def get_expected_team_size(self):
        return r.size_of_proposed_team(self.state.current_quest, self.num_players)

    @expect_initialized
    def pid_to_role(self, pid):
        return first_of(lambda p: p.pid == pid, self.players)

    @expect_initialized
    def role_to_pid(self, role):
        return first_of(lambda p: p.role == role, self.players)

    @expect_initialized
    def _increment_leader(self):
        self._leader_idx = (self._leader_idx + 1) % self.num_players

    @expect_initialized
    def _are_unique_valid_pids(self, pids):
        return (all(p in self.pids for p in pids) and
                len(pids) == len(set(pids)))

    def _update_error(self, error):
        self._errors.append(error)

    def __str__(self):
        ret = 'Status: {}\nState: {}\nCurrent Leader: {}\nCurrent Team: {}\nWinner: {}'.format(
            self.status, self.state, self.leader, self.current_team, self._winner)
        if self._errors:
            ret += '\nErrors: {}'.format(self._errors)
        return ret
