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
            'A': [('A', "0.5"), ('B', "0.5")],
            'B': [('A', "0.2"), ('B', "0.6"), ('C', "0.2")],
            'C': [('D', "0.5"), ('C', "0.5")],
            'D': [('C', "0.9"), ('D', "0.1")]
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
    def test_arbitrary_labels(self):
        """
        Tests if the chain's labels work properly, if the labels are not
        of type string.
        """
        # Create a proof-of-concept class that provides a hash() and
        # ordering methods.
        class C(object):
            def __init__(self, val):
                self.val = val
            def __hash__(self):
                return hash(self.val)
            def __eq__(self, other):
                return self.val == other.val
            def __str__(self):
                return 'C: %s' % str(self.val)
            def __repr__(self):
                return 'C: %s' % repr(self.val)
            def __lt__(self, rhs):
                return self.val < rhs.val
            def __gt__(self, rhs):
                return self.val > rhs.val
            def __ge__(self, rhs):
                return self.val >= rhs.val
            def __le__(self, rhs):
                return self.val <= rhs.val

        # initial probability table
        init_probs = {
            C(5): "0.1",
            C(7): "0.2",
            C(1): "0.2",
            C(10): "0.1",
            C(6): "0.2",
            C(4): "0.2"
        }

        # transition table
        transition_table = {
            C(5): [(C(7), "0.7"), (C(1), "0.1"), (C(10), "0.2")],
            C(1): [(C(7), "0.5"), (C(10), "0.5")],
            C(7): [(C(7), "0.9"), (C(5), "0.1")],
            C(10): [(C(5), "0.3"), (C(10), "0.5"), (C(4), "0.2")],
            C(4): [(C(4), "0.5"), (C(6), "0.5")],
            C(6): [(C(4), "1.0")]
        }

        # these two methods should not fail
        chain = MarkovChain(init_probs, transition_table)
        classes = chain.communication_classes()

        # did it find the correct classes though?
        states = tuple(i['states'] for i in classes)
        self.assertTrue({C(4), C(6)} in states)

    def test_simple_chain(self):
        """
        Tests if the chain's communication classes are identified
        properly for a chain with 3 states, one of which is a sink.
        """
        init_probs = {
            'A': "0.3",
            'B': "0.4",
            'C': "0.3"
        }

        p_table = {
            'A': [('A', "0.5"), ('B', "0.5")],
            'B': [('A', "0.8"), ('B', "0.1"), ('C', "0.1")],
            'C': [('C', "1.0")]
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
            'A': "0.25",
            'B': "0.25",
            'C': "0.25",
            'D': "0.25"
        }

        p_table = {
            'A': [('A', "0.5"), ('B', "0.5")],
            'B': [('A', "0.2"), ('B', "0.6"), ('C', "0.2")],
            'C': [('D', "0.5"), ('C', "0.5")],
            'D': [('C', "0.9"), ('D', "0.1")]
        }

        comm_classes = MarkovChain(init_probs, p_table).communication_classes()
        states = tuple(i['states'] for i in comm_classes)
        self.assertTrue({'C', 'D'} in states)
        self.assertTrue({'A', 'B'} in states)

    def test_bad_initial_probs(self):
        """
        Tests if a bad initial distribution is caught and an exception
        is raised.
        """

        err_string = (
            "Initial probabilities don't form a proper distribution"
        )
        flag = False

        init_probs = {
                'A' : "0.25",
                'B' : "0.25",
                'C' : "0.52",
                'D' : "0.25"
	}

        p_table = {
            'A': [('A', "0.5"), ('B', "0.5")],
            'B': [('A', "0.2"), ('B', "0.6"), ('C', "0.2")],
            'C': [('D', "0.5"), ('C', "0.5")],
            'D': [('C', "0.9"), ('D', "0.1")]
        }

        try:
            m = MarkovChain(init_probs, p_table)
        except ValueError as e:
            self.assertEqual(e.args[0], err_string)
            flag = True

        self.assertTrue(flag)

    def test_bad_transitioon_table(self):
        """
        Tests if a bad initial distribution is caught and an exception
        is raised.
        """
        err_string = ("Transitions from state D do not form a "
                      "probability distribution")
        flag = False

        init_probs = {
                'A' : "0.25",
                'B' : "0.25",
                'C' : "0.25",
                'D' : "0.25"
        }

        p_table = {
            'A': [('A', "0.5"), ('B', "0.5")],
            'B': [('A', "0.2"), ('B', "0.6"), ('C', "0.2")],
            'C': [('D', "0.5"), ('C', "0.5")],
            'D': [('C', "0.9"), ('D', "1.1")]
        }

        try:
            m = MarkovChain(init_probs, p_table)
        except ValueError as e:
            self.assertEqual(e.args[0], err_string)
            flag = True
    def test_monte_carlo(self):
        """
        Tests if monte carlo method functions properly
        """
        N = 10000

        p = 0.6
        q = 1-p

        init_probs = {
                '0-0':1.0
        }

        markov_table = {
            '0-0':[('15-0',p),('0-15',q)],
            '15-0':[('30-0',p),('15-15',q)],
            '0-15':[('15-15',p),('0-30',q)],
            '30-0':[('40-0',p),('30-15',q)],
            '15-15':[('30-15',p),('15-30',q)],
            '0-30':[('15-30',p),('0-40',q)],
            '40-0':[('A',p),('40-15',q)],
            '30-15':[('40-15',p),('D',q)],
            '15-30':[('D',p),('15-40',q)],
            '0-40':[('15-40',p),('B',q)],
            '40-15':[('A',p),('AA',q)],
            'D':[('AA',p),('BB',q)],
            '15-40':[('BB',p),('B',q)],
            'AA':[('A',p),('D',q)],
            'BB':[('D',p),('B',q)],
            'A':[('A',1)],
            'B':[('B',1)]
        }

        def a_won(state):
            return state == 'A'

        def game_ended(state):
            return state in ['A', 'B']

        m = MarkovChain(init_probs, markov_table)
        hits, steps = m.monte_carlo_estimation(N, game_ended, a_won)
        self.assertTrue(hits > 7250 and hits < 7480)
        self.assertTrue(steps > 64000 and steps < 65500)
