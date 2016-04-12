import unittest, os
from simple_markov.io import JSON_Reader, YAML_Reader

class TestReaders(unittest.TestCase):
    def test_yaml(self):
        """
        Tests that YAML_Reader can read a simple chain
        in YAML format.
        """

        # get filename
        filename = os.path.join(os.path.dirname(__file__), 'files/test.yaml')

        # read initial probabilities and table
        init_probs, table = YAML_Reader(filename).parse_data()

        # make sure all the keys are there
        self.assertTrue(all(i in init_probs for i in ['A', 'B', 'C']))
        self.assertTrue(all(i in table for i in ['A', 'B', 'C']))

        # make sure transitions sum to 1
        self.assertTrue(
            all(abs(sum([i[1] for i in table[key]]) - 1) < 0.0001 \
                for key in table)
        )
        
    def test_json(self):
        """
        Tests that JSON_Reader can read a simple chain
        in JSON format.
        """
        # get filename
        filename = os.path.join(os.path.dirname(__file__), 'files/test.json')

        # read initial probabilities and table
        init_probs, table = JSON_Reader(filename).parse_data()

        # make sure all the keys are there
        self.assertTrue(all(i in init_probs for i in ['A', 'B', 'C']))
        self.assertTrue(all(i in table for i in ['A', 'B', 'C']))

        # make sure transitions sum to 1
        self.assertTrue(
            all(abs(sum([i[1] for i in table[key]]) - 1) < 0.0001 \
                for key in table)
        )
