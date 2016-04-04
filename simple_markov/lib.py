# -*- coding: utf-8 -*-
import random as rnd

# import accumulate from utils if python v3.x
# is not available
try:
    from itertools import accumulate
except ImportError:
    from simple_markov.utils import accumulate

# import strongly_connected_components function for
# MarkovChain.communication_classes()
from simple_markov.utils import strongly_connected_components

# scipy - numpy imports for probability matrix algebra
from scipy import sparse
import numpy as np

# import graphviz for graph drawing
import graphviz as gv

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

        :returns: the next state, chosen at random
        """
        coin_toss = rnd.uniform(0, 1)
        return list(self.prob)[bisect.bisect_left(self.cum_prob, coin_toss)]

    def accessible_states(self):
        """
        Returns a set containing all the states accessible from this
        state, or equivalently all keys of the transition table.

        :returns: a set containing all the states this state can lead to
        """
        return set(i for i in self.prob)

    def populate_graph(self, graph):
        """
        Populates a graphviz.Digraph object with the transitions that
        this state contains.

        :param graph: a graphviz.Digraph object to be populated
        """
        # add edges for all transitions with corresponding costs
        for (state_to, cost) in self.prob.items():
            graph.edge(self.label, state_to, label=str(cost))
        # [NOTE: graphviz.Digraph objects are mutable, so there is
        #  no need for this function to return the modified object]

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

        # initialize current_state to None
        self.current_state = None

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
        if self.current_state == None:
            raise StopIteration

        self.steps += 1
        self.current_state = self.states[self.current_state].next_state()
        return self.current_state

    def next(self):
        return self.__next__()

    def run_for(self, steps):
        """
        Simulate the markov chain for a specified number of steps.
        :param steps: the number of steps to simulate
        :returns: a sequence of states as a generator expression

        >>> chain = MarkovChain(
                {'A': 0.5,'B': 0.5},
                {'A': [('A', 0.4), ('B', 0.6)],
                 'B': [('A', 0.8), ('B', 0.2)]
                })

        >>> states = [i for i in chain.run_for(5)]
        >>> states[4]
        'A'

        """

        # if negative number of steps has been given, return
        if (steps <= 0):
            return

        # initialize iterable
        it = iter(self)
        simulation_step = 0

        while simulation_step < steps:
            try:
                next_state = next(it)
            except StopIteration:
                return

            # update simulation step
            simulation_step += 1
            yield next_state

    def state_probabilities(self, steps=1):
        """
        Calculates the probability of the markov chain's states in the future
        after a specified number of steps (default 1).

        :param steps: the number of steps
        :returns: a map of state - transition probability pairs

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

    def to_graph(self):
        """
        Converts the markov chain into a graph representation, where the
        chain's states become the graph's vertices and the transitions become
        directed edges, if their probability is higher than 0.
        The chain's graph representation is implemented by a dictionary mapping
        nodes (keys) to dictionaries containing transitions along with their
        probabilities (weighted edges).

        :returns: the chain's graph representation

        >>> chain.to_graph()
        {
            'A': {'A': 0.1, 'B': 0.9},
            'B': {'A': 0.3, 'C': 0.7},
            'C': {'A': 0.5, 'B': 0.5}
        }

        """
        return { s: self.states[s].prob for s in self.states }

    def communication_classes(self):
        """
        Finds the communication classes of this markov chain by applying
        Tarjan's strongly connected components algorithm to the chain's
        digraph. For each class, also returns info about whether it is
        open or closed.

        >>> m_chain = MarkovChain(
            {'A': 0.3, 'B': 0.5, 'C': 0.2},
            {
                'A': [('A', 0.2), ('B', 0.8)],
                'B': [('A', 0.5), ('B', 0.3), ('C', 0.2)],
                'C': [('C', 1.0)]
            })
        
        >>> m_chain.communication_classes()
        [{'states': {'C'}, 'type': 'closed'},
         {'states': {'A', 'B'}, 'type': 'open'}]

        :returns: a set containing the chain's communication classes
        """

        return strongly_connected_components(self.to_graph())

    def get_class_connections(self):
        """
        Finds the communication classes of this chain and subsequently finds
        all connections between them.

        :returns: a dictionary containing all inter-class connections, where
         keys / values are tuples / lists of tuples containing the class 
         states.

        >>> ch = MarkovChain(
                {'A' : 0.2, 'B': 0.2, 'C': 0.3, 'D': 0.3},
                {
                    'A': [('A', 0.5), ('B', 0.5)],
                    'B': [('A', 0.9), ('C', 0.1)],
                    'C': [('C', 0.9), ('D', 0.1)],
                    'D': [('C', 0.5), ('D', 0.5)]
                })

        >>> ch.get_class_connections()
        {('A', 'B'): [('C', 'D')], ('C', 'D'): []}

        """
        # get the classes first
        c_classes = self.communication_classes()

        # anonymous fun that checks if a state belongs to another class (x)
        # in a list of classes provided this class does not have the same states
        # as (y).
        filt = lambda s, x, y: s in x['states'] if x['states'] != y else False

        # find all open classes
        open_classes = filter(lambda x: x['type'] == 'open', c_classes)

        # dict containing class -> class accessibility mappings
        class_conns = {tuple(i['states']): [] for i in c_classes}

        # for each open communication class, find out which other
        # classes it communicates with
        for s_set in (i['states'] for i in open_classes):
            # states accessible from this class
            can_access = set.union(
                *(self.states[s].accessible_states() for s in s_set)
            )

            for acc in can_access:
                # find all classes accessible from this one by keeping only
                # classes whose states contain any state from the accessible
                # set.
                found = filter(lambda x: filt(acc, x, s_set), c_classes)
                class_conns[tuple(s_set)].extend(tuple(i['states']) for i in found)

        return class_conns

    def draw_class_connections(self, return_graph = False):
        """
        Finds all connections between communication classes in this markov
        chain and draws them in a graph in DOT format.

        :param return_graph: a boolean indicating if the underlying
         graphviz.Digraph object should be returned instead of the DOT string.

        :returns: a representation of inter-class connections in DOT format.

        >>> ch = MarkovChain(
                {'A': 0.5, 'B': 0.25, 'C': 0.25},
                {
                    'A': [('A', 0.5), ('B', 0.5)],
                    'B': [('A', 0.7), ('B', 0.2), ('C', 0.1)],
                    'C': [('C', 1.0)]
                })

        >>> print(ch.draw_class_connections())
        digraph {
            "{A, B}"
            "{C}"
                "{A, B}" -> "{C}"
        }

        """
        connections = self.get_class_connections()
        graph = gv.Digraph(format = 'svg')
        # anonymous function to extract class labels in pretty format
        label = lambda x: '{' + ', '.join(x) + '}'

        for key in connections:
            # add node with class label
            graph.node(label(key))
            for val in connections[key]:
                graph.edge(label(key), label(val))

        return graph if return_graph else graph.source

    def to_dot(self, return_graph=False):
        """
        Creates a DOT format representation of this chain, where states
        are represented as labelled nodes and transitions as directed arcs
        labelled by their probabilities. If return_graph is set to True,
        the graphviz.Digraph object that contains the representation is
        returned instead.

        :param return_graph: a boolean indicating if the underlying Digraph
         object should be returned instead of the string representation
        :returns: a representation of the chain in DOT format
        """
        graph = gv.Digraph(format='svg')
        for st in self.states.values():
            st.populate_graph(graph)

        return graph if return_graph else graph.source
