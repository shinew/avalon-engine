import action
g = action.create_game()
action.start_game(g, range(6))
print g
print action.get_visibility(g)
