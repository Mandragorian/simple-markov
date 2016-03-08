import unittest
import simple_markov_lib as lib

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
        chain = lib.MarkovChain(init_probs, p_table)

        # generate simulations for various number of steps
        gen_exp = chain.run_for(100)
        self.assertTrue(len(list(gen_exp)) == 100)
        gen_exp = chain.run_for(0)
        self.assertTrue(len(list(gen_exp)) == 0)
        gen_exp = chain.run_for(-10)
        self.assertTrue(len(list(gen_exp)) == 0)
