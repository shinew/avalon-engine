import model as m
import rules as r
import avalon

g = avalon.Game()
g.add_players(range(5), lambda a,b: b)
print g.players
print g.get_visibility()
print g.leader_idx, g.leader
print g.get_expected_team_size()

g.nominate_team(range(2))
print g.state
g.vote_for_team(map(lambda p: r.PlayerVote(p, m.Vote.yes), range(5)))
print g.state
g.vote_for_mission(map(lambda p: r.PlayerVote(p, m.Vote.yes), range(2)))
print g.status, g.error
print g.state

print '---------------'
