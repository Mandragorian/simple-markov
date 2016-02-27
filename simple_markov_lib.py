# -*- coding: utf-8 -*-
import random as rnd

# import accumulate from utils if python v3.x
# is not available
try:
    from itertools import accumulate
except ImportError:
    from utils import accumulate

# scipy - numpy imports for probability matrix algebra
from scipy import sparse
import numpy as np

import bisect

class State(object):
    """
    Represents a state in a markov chain.
    """

    def __init__(self, distribution, label):
        """
        Creates a new state that contains a distribution of transitions
        to other states with a specified label.

        :param distribution: an iterable of state - transition probability pairs
        :param label: the label of the state
        """
        self.prob = { d[0]: d[1] for d in distribution if 0 < d[1] <= 1 }
        self.cum_prob = list(accumulate(v for v in self.prob.values()))
        self.label = label

    def next_state(self):
        """
        Chooses the next state at random by simulating a coin toss with result
        in the range [0, 1], finding in which cumulative probability interval
        the result falls into, and returning the state associated with the
        interval.

        :return the next state, chosen at random
        """
        coin_toss = rnd.uniform(0, 1)
        return list(self.prob)[bisect.bisect_left(self.cum_prob, coin_toss)]

class MarkovChain(object):
    """
    An iterable that represents a discrete time Markov Chain.
    """

    def __init__(self, initial_distrib, transition_table):
        """
        Creates a new Markov Chain with a specified initial distribution vector
        and a given transition table.

        :param initial_distrib: a map of states to initial probabilities
        :param transition_table: a 2D table containing transition probabilites
        """
        self.initial_probs = initial_distrib

        # map of label-to-state pairs
        self.states = {
            k: State(transition_table[k], k) for k in transition_table
        }

        # create a frame that holds (row, column, value) entries
        # which will be used later to create the sparse array
        sparse_frame = []
        labels = sorted(key for key in self.states)
        for i, key in enumerate(labels):
            for j in range(len(labels)):
                try:
                    sparse_frame.append((transition_table[key][j][1], i, j))
                except KeyError:
                    # continue with next element
                    continue
                except IndexError:
                    # continue with next element
                    continue

        # get data and row - column vectors for sparse representation
        data, row, col = zip(*sparse_frame)
        sz = len(labels)
        self.prob_matrix = sparse.coo_matrix((data, (row, col)), shape=(sz, sz))

    def __iter__(self):
        """
        Makes this object iterable - chooses an initial state.
        """
        self.steps = 0
        # coin toss to choose first state
        toss, run_sum = rnd.uniform(0, 1), 0

        # calculate running sum and return the state
        # when coin toss is reached
        for (key, val) in self.initial_probs.items():
            run_sum += val
            if (toss <= run_sum):
                self.current_state = key
                break

        # return the modified object
        return self

    def __next__(self):
        """
        Chooses the next state for the markov chain.
        """
        # shouldn't happen, but let's be safe.
        if not self.current_state:
            raise StopIteration

        self.steps += 1
        self.current_state = self.states[self.current_state].next_state()
        return self.current_state

    def next(self):
        return self.__next__()

    def state_probabilities(self, steps=1):
        """
        Calculates the probability of the markov chain's states in the future
        after a specified number of steps (default 1).

        :param steps: the number of steps
        :return a map of state - transition probability pairs

        Example:

        >>> m_chain = MarkovChain(
                {'A': 0.5, 'B': 0.5},
                {'A': [('A', 1.0)],
                'B': [('A', 0.2), ('B', 0.8)]
                })

        >>> m_chain.state_probabilities()
        {'A': 0.6, 'B', 0.4}

        """
        
        labels = sorted(self.initial_probs)
        tran_matrix = self.prob_matrix.toarray()
        # adjust transition matrix according to number of steps
        if steps > 1:
            tran_matrix = np.linalg.matrix_power(tran_matrix, steps)

        # vector of by-label sorted initial probabilities
        init_probs_vec = np.array([
            self.initial_probs[key] for key in labels
        ])

        # pi_i * P(i, j)
        future_probs_vec = np.dot(init_probs_vec, tran_matrix)
        return {
            v[0]: v[1] for v in zip(labels, future_probs_vec)
        }
