import unittest
from simple_markov import MarkovChain

class TestSimulation(unittest.TestCase):
    def test_simulation_run(self):
        """
        Tests if the chain's run_for(N) method works properly.
        """
        # sample initial states
        init_probs = {
            'A': 0.25,
            'B': 0.25,
            'C': 0.25,
            'D': 0.25
        }

        # transition probability table
        p_table = {
            'A': [('A', 0.5), ('B', 0.5)],
            'B': [('A', 0.2), ('B', 0.6), ('C', 0.2)],
            'C': [('D', 0.5), ('C', 0.5)],
            'D': [('C', 0.9), ('D', 0.1)]
        }

        # create the chain
        chain = MarkovChain(init_probs, p_table)

        gen_exp = chain.run_for(100)
        self.assertTrue(len(list(gen_exp)) == 100)
        gen_exp = chain.run_for(0)
        self.assertTrue(len(list(gen_exp)) == 0)
        gen_exp = chain.run_for(-10)
        self.assertTrue(len(list(gen_exp)) == 0)

class TestComponents(unittest.TestCase):
    def test_simple_chain(self):
        """
        Tests if the chain's communication classes are identified
        properly for a chain with 3 states, one of which is a sink.
        """
        init_probs = {
            'A': 0.3,
            'B': 0.4,
            'C': 0.3
        }

        p_table = {
            'A': [('A', 0.5), ('B', 0.5)],
            'B': [('A', 0.8), ('B', 0.1), ('C', 0.1)],
            'C': [('C', 1.0)]
        }

        comm_classes = MarkovChain(init_probs, p_table).communication_classes()
        states = tuple(i['states'] for i in comm_classes)

        self.assertTrue({'C'} in states)
        self.assertTrue({'A', 'B'} in states)

    def test_segmented_chain(self):
        """
        Tests if a chain's communication classes are identified properly
        for a chain which consists of 4 states.
        """

        init_probs = {
            'A': 0.25,
            'B': 0.25,
            'C': 0.25,
            'D': 0.25
        }

        p_table = {
            'A': [('A', 0.5), ('B', 0.5)],
            'B': [('A', 0.2), ('B', 0.6), ('C', 0.2)],
            'C': [('D', 0.5), ('C', 0.5)],
            'D': [('C', 0.9), ('D', 0.1)]
        }

        comm_classes = MarkovChain(init_probs, p_table).communication_classes()
        states = tuple(i['states'] for i in comm_classes)
        self.assertTrue({'C', 'D'} in states)
        self.assertTrue({'A', 'B'} in states)
