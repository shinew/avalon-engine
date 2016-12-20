import avalon
g = avalon.Game()
g.add_players(range(6, 0, -1), lambda a,b: b)
print g.players
print g.get_visibility()
print g.current_leader, g.leader
