class Role(object):
    servant = 'servant'
    minion = 'minion'
    merlin = 'merlin'
    assassin = 'assassin'
    percival = 'percival'
    mordred = 'mordred'
    morgana = 'morgana'
    oberon = 'oberon'

class Team(object):
    good = 'good'
    evil = 'evil'

class Vote(object):
    yes = 'yes'
    no = 'no'

class VoteStatus(object):
    unknown = 'unknown'
    succeeded = 'succeeded'
    failed = 'failed'

class GameStatus(object):
    error = 'error'
    not_started = 'not_started'
    nominating_team = 'nominating_team'
    voting_for_team = 'voting_for_team'
    voting_for_mission = 'voting_for_mission'
    done = 'done'

class MerlinStatus(object):
    alive = 'alive'
    dead = 'dead'
