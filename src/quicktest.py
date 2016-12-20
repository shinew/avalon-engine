import avalon
g = avalon.Game()
g.add_players(range(5), lambda a,b: b)
print g.players
print g.get_visibility()
