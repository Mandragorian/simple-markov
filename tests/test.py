#!/usr/bin/env python3
import simple_markov_lib as lib

# initial facing of the coin
initial_probs = {
    'Heads': 0.5,
    'Tails': 0.5
}

# transition table for coin tosses
transition_table = {
    'Heads': [('Heads', 0.5), ('Tails', 0.5)],
    'Tails': [('Heads', 0.5), ('Tails', 0.5)]
}

chain = lib.MarkovChain(initial_probs, transition_table)

# get the first 10 coin tosses:
for i, step in zip(chain, range(10)):
    print('Step %d: %s' % (step + 1, i))

