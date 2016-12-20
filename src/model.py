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
    evil = 1

class Vote(object):
    yes = 0
    no = 1

class VoteStatus(object):
    unknown = 0
    succeeded = 1
    failed = 2

class GameStatus(object):
    nominating_team = 1
    voting_for_team = 2
    voting_for_mission = 3
    done = 4

class MerlinStatus(object):
    alive = 0
    dead = 1
