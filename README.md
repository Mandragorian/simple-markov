[![Build Status](https://travis-ci.org/Mandragorian/simple-markov.svg?branch=master)](https://travis-ci.org/Mandragorian/simple-markov)

# simple-markov
A simple library for simulating Markov Chains. Initially used in Stochastic
Processes course in NTUA.

This library is loosely based on the code developed by
[tetraktida][tetraktida].
The original files can be found [here][orig-code].

### Examples

#### Simulate a coin toss

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

#### Get the state probabilities after N steps

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

#### Create a Markov chain and get its communication classes

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

#### Using arbitrary objects as state labels

In recent versions, you can use any kind of object as state label, as long as
it is an ordered (required for fundamental operations, e.g. choosing next
state) and hashable type. For example:

```python
from simple_markov import MarkovChain

class P(object):
	def __init__(self, val):
		self.val = val
		# other parameters here

	def __hash__(self):
		# make sure __hash__ is overloaded properly

	# other overloads here (__gt__, __ge__, __lt__, __le__ ideally)

	def __str__(self):
		return 'P: %s' % str(self.val)
	def __repr__(self):
		return 'P: %s' % repr(self.val)

init_probs = {
	P(1): 0.2,
	P(2): 0.3,
	P(4): 0.5
}

transition_table = {
	P(1): [(P(4), 0.1), (P(2), 0.9)],
	P(2): [(P(4), 1)],
	P(4): [(P(1), 1)]
}

chain = MarkovChain(init_probs, transition_table)
```

#### Reading markov chains from files
You can also read chains from .yaml or .json files, using the `io` subpackage.
In JSON, the structure of the file should be:

```
{
	"Initial": {
		"State 1": Probability 1,
		"State 2": Probability 2,
		...
		"State N": Probability N
	},
	"Table": {
		"State 1": {
			"State 1": Transition Probability 1,
			"State 2": Transition Probability 2,
			...
			"State K": Transition Probability K
		},
		...
		"State N": {
			...
		}
	}
}
```

An example JSON-formatted chain is given below:

```shell
$ cat chain.json
{
	"Initial": {
		"A": 0.25,
		"B": 0.25,
		"C": 0.5
	},
	"Table": {
		"A": {
			"A": 0.1,
			"B": 0.5,
			"C": 0.4
		},
		"B": {
			"A": 0.5,
			"C": 0.5
		},
		"C": {
			"C": 0.9
			"A": 0.1
		}
	}
}
```
You can read this file into a markov chain using the `JSON_Reader` class.

```python
from simple_markov import MarkovChain
from simple_markov.io import JSON_Reader

rdr = JSON_Reader('chain.json') # creates a JSON reader that loads the file
init_table, transition_table = rdr.parse_data() # parses the data

chain = MarkovChain(init_table, transition_table)
```

or, more simply:

```python
chain = MarkovChain(*JSON_Reader('chain.json').parse_data())
```

The same can be done with a .yaml file. The format is similar to JSON:

```yaml
Initial:
	State 1: Probability 1
	State 2: Probability 2
	...
	State N: Probability N
Table:
	State 1:
		State 1: Transition Probability 1
		State 2: Transition Probability 2
		...
		State K: Transition Probability K
	State 2:
		...
	...
	State N:
		...
```

Let's try the file 'chain.yaml':

```shell
$ cat chain.yaml
Initial:
	A: 0.5
	B: 0.2
	C: 0.3
Table:
	A:
		B: 0.2
		C: 0.8
	B:
		A: 0.5
		B: 0.5
	C:
		A: 0.9
		C: 0.1
```

You can parse the chain from this file using `YAML_Reader`. Similarly to
before:

```python
from simple_markov import MarkovChain
from simple_markov.io import YAML_Reader

yaml_rdr = YAML_Reader('chain.yaml')
init_table, transition_table = yaml_rdr.parse_data()

chain = MarkovChain(init_table, transition_table)
```

## Installing as a pip package
For now, `simple-markov` has not been added to the PyPI package index.
Therefore you will need to work locally. 
First, clone the package branch of the repo:

```shell
git clone git@github.com:Mandragorian/simple-markov.git
```

Then, run `pip install -r requirements.txt .` to get all dependencies and then:

```shell
python setup.py install
```

Make sure to use `sudo` if required, or use `virtualenv` to build a local
environment.

[orig-code]: http://www.math.ntua.gr/~loulakis/info/python_codes_files/
[tetraktida]: https://github.com/tetraktida
