[![Build Status](https://travis-ci.org/VHarisop/simple-markov.svg?branch=master)](https://travis-ci.org/VHarisop/simple-markov)

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

from simple_markov import MarkovChain

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

from simple_markov import MarkovChain

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

* Create a Markov chain and get its communication classes

```python
#!/usr/bin/env python3

from simple_markov import MarkovChain

# Create a markov chain with 4 states and 2 communication classes

initial_probs = {
	'A': 0.25,
	'B': 0.25,
	'C': 0.25,
	'D': 0.25
}

transition_table = {
	'A': [('A', 0.5), ('B', 0.4), ('C', 0.1)],
	'B': [('A', 1.0)],
	'C': [('C', 0.2), ('D', 0.8)],
	'D': [('C', 0.5), ('D', 0.5)]
}

chain = MarkovChain(initial_probs, transition_table)

# get the communication classes
comm_classes = chain.communication_classes()
print(comm_classes)
```

## Installing as a pip package
For now, `simple-markov` has not been added to the PyPI package index.
Therefore you will need to work locally. 
First, clone the package branch of the repo:

```shell
git clone -b package git@github.com:VHarisop/simple-markov.git
```

Then, simply run `pip install -r requirements.txt .`

[orig-code]: http://www.math.ntua.gr/~loulakis/info/python_codes_files/
[tetraktida]: https://github.com/tetraktida
