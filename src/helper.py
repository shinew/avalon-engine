"""
Internal API.

"""
import copy
import model as m

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

def num_bad_players(num_players):
    return num_players - num_good_players(num_players)

def role_to_team(role):
    good = [m.Role.servant, m.Role.merlin, m.Role.percival]
    return m.Team.good if role in good else m.Team.bad

def is_role_good(role):
    return role_to_team(role) is m.Team.good

def get_default_good_roles(num_good_players):
    return [m.Role.merlin] + [m.Role.servant] * (num_good_players - 1)

def get_default_bad_roles(num_bad_players):
    return [m.Role.assassin] + [m.Role.minion] * (num_bad_players - 1)

def get_roles(num_players):
    assert m.MIN_PLAYERS <= num_players <= m.MAX_PLAYERS
    return (get_default_good_roles(num_good_players(num_players)) +
            get_default_bad_roles(num_bad_players(num_players)))

def shuffle(lst, intgen):
    """
    Fisher-Yates shuffle implementation.
    lst: [t]
    intgen: int -> int -> int
    return: [t]

    """
    ret = copy.copy(lst)
    for i in reversed(range(1, len(ret) - 1)):
        j = intgen(0, i)
        ret[j], ret[i] = ret[i], ret[j]
    return ret

def num_of_team_votes(num_quest, num_players):
    assert m.MIN_QUEST <= num_quest <= m.MAX_QUEST
    assert m.MIN_PLAYERS <= num_players <= m.MAX_PLAYERS
    mapping = [
        [2, 2, 2, 3, 3, 3],
        [3, 3, 3, 4, 4, 4],
        [2, 4, 3, 4, 4, 4],
        [3, 3, 4, 5, 5, 5],
        [3, 4, 4, 5, 5, 5],
    ]
    return mapping[num_quest - m.MIN_QUEST][num_players - m.MIN_PLAYERS]

def can_go_on_quest(num_yes, num_votes):
    assert 0 <= num_yes <= num_votes <= m.MAX_PLAYERS
    return num_yes * 2 > num_votes

def does_quest_succeed(num_yes, num_quest, num_votes):
    assert 0 <= num_yes <= num_votes <= m.MAX_PLAYERS
    num_fails = num_votes - num_yes
    if num_quest == 4 and num_votes >= 7:
        return False if num_fails >= 2 else True
    return False if num_fails >= 1 else True

def does_good_win(game):
    return (game.board.quests.count(m.VoteState.yes) >= 3 and
            game.is_merlin_alive)

def does_bad_win(game):
    return (game.board.quests.count(m.VoteState.no) >= 3 or
            not game.is_merlin_alive or
            game.board.proposals.count(m.VoteState.no) == 5)

def is_vote_valid(vote, role):
    return False if is_role_good(role) and vote is m.Vote.no else True

def assign_team_ids(pids, intgen):
    """
    pids: [t]
    intgen: int -> int -> int
    return: [Player]

    """
    roles = get_roles(len(pids))
    roles = shuffle(roles, intgen) return map(lambda p,r: m.Player(p, r), pids, roles) 

def pid_to_player(pid, players):
    return filter(lambda p: p.pid == pid, players)[0]

def see_other_players(player, players):
    """
    Returns the pids for which this player can know of the others.
    player -> [player] -> [player]
    """
    if player.role is m.Role.merlin or not is_role_good(player.role):
        return filter(lambda p: p != player and not is_role_good(p.role), players)
    else:
        return []
