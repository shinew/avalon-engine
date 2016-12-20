from collections import namedtuple

MAX_PLAYERS = 10
MIN_PLAYERS = 5
MIN_QUEST = 1
MAX_QUEST = 5

class Role(object):
    servant = 0
    minion = 1
    merlin = 2
    assassin = 3
    percival = 4
    mordred = 5
    morgana = 6
    oberon = 7

class Team(object):
    good = 0
    bad = 1

Player = namedtuple('Player', 'pid role')

class GameState(object):
    adding_players = 0
    team_selection = 3
    voting_for_team = 4
    voting_for_mission = 5
    finished_game = 6

class Vote(object):
    yes = 0
    no = 1

class VoteState(object):
    yes = 0
    no = 1
    not_yet = 2

class Board(object):
    def __init__(self):
        self.quests = [VoteState.not_yet] * 5
        self.proposals = [VoteState.not_yet] * 5
    def __repr__(self):
        return 'Quests: {}\nProposals: {}'.format(self.quests, self.proposals)

class Game(object):
    def __init__(self):
        self.state = GameState.adding_players
        self.players = []
        self.board = Board()
        self.is_merlin_alive = True
        self.current_leader = None
        self.current_team = None

    def __repr__(self):
        return 'State: {}\nBoard: {}\nPlayers: {}\nIsMerlinAlive: {}Players\nTurn: {}'.format(
                self.state, self.board, self.players, self.is_merlin_alive, self.player_turn)
