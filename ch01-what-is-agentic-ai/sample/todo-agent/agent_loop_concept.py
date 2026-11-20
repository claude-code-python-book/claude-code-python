# Listing 1-1: pseudo-code, not meant to run
while not goal_achieved(state):
    observation = observe(environment)
    action = decide_next_action(observation, goal, state)  # the LLM
    result = execute(action)                                 # a tool
    state = update_memory(state, result)
