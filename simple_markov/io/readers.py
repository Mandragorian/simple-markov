# -*- coding: utf-8 -*-
import json, yaml

class JSON_Reader(object):
    """
    JSON_reader is a class that aims to facilitate I/O from files that
    contain descriptions of Markov Chains in JSON format.

    The structure of the JSON file should be as follows:

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
                "State N": ...
            }
        }

    In the above specification, the keys in the dictionary that follows any
    state in the [Table] field need not be exhaustive. For more info, see the
    documentation in the MarkovChain class.
    """

    def __init__(self, filename):
        """
        Creates a new JSON_reader object to read data from a file.

        Args:
            filename (str): The name of the input file.
        """

        with open(filename, 'r') as f:
            self.data = json.load(f)
        
    def parse_data(self):
        """
        Parses the input data to identify initial states and the
        transition table and returns them in a format readable by
        the constructor of the MarkovChain class.

        Returns:
            a tuple containing the initial probability vector as well
            as the transition table, in the format expected by the
            MarkovChain class constructor
        """

        init_table = self.data['Initial']
        trans_table = {
            key: [(k, v) for k, v in value.items()] \
                for key, value in self.data['Table'].items()
        }

        return init_table, trans_table

class YAML_Reader(object):
    """
    YAML_Reader is a class that aims to facilitate I/O from files that
    contain descriptions of Markov Chains in YAML format.

    The structure of the YAML file should be as follows:

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
                State K: TransitionProbability K
            ...
            State N:
                ...
        
    In the above specification, the keys that follow the states
    in the [Table] field need not be exhaustive. For more info,
    check out the documentation in MarkovChain.
    """

    def __init__(self, filename):
        """
        Initializes a YAML_Reader object to read data from a specified
        file.

        Args:
            filename (str): the name of the YAML file
        """
        
        with open(filename, 'r') as f:
            self.data = yaml.load(f)
       
    def parse_data(self):
        """
        Parses the data read from the YAML file and converts them
        to a format that is compatible with the expected format of
        the MarkovChain constructor.

        Returns:
            a tuple containing the initial probability vector as well
            as the transition table in the format that is expected by
            the MarkovChain class constructor
        """
        init_table = self.data['Initial']
        trans_table = {
            key: [(k, v) for k, v in value.items()] \
                for key, value in self.data['Table'].items()
        }

        return init_table, trans_table
