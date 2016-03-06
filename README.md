# simple-markov
A simple library for simulating Markov Chains. Initially used in Stochastic
Processes course in NTUA.

This library is loosely based on the code developed by
[tetraktida][tetraktida].
The original files can be found [here][orig-code].

### Examples

* Simulate a coin toss

```python
#!/usr/bin/env python3

from simple_markov_lib import MarkovChain

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

chain = MarkovChain(initial_probs, transition_table)

# get the first 10 coin tosses:
for i, step in zip(chain, range(10)):
	print('Step %d: %s' % (step + 1, i))
	
```

* Get the state probabilities after N steps

```python
#!/usr/bin/env python3

from simple_markov_lib import MarkovChain

# initial facing of the unfair coin
initial_probs = {
	'Heads': 0.5,
	'Tails': 0.5
}

# transition table for coin tosses
transition_table = {
	'Heads': [('Heads', 1.0)],
	'Tails': [('Heads', 0.2), ('Tails', 0.8)]
}

chain = MarkovChain(initial_probs, transition_table)

# get state probability after N = 3 steps
states_after = chain.state_probabilities(3)

print(states_after)  # prints {'Heads': 0.744, 'Tails': 0.256}
```

### Running the tests
Test files for `simple_markov_lib` are included in the `tests/` subfolder.
Run them with

```bash
$ python -m unittest
```

as long as your current working directory is the project's root folder.

[orig-code]: http://www.math.ntua.gr/~loulakis/info/python_codes_files/
[tetraktida]: https://github.com/tetraktida
