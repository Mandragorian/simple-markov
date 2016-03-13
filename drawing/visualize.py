# -*- coding: utf-8 -*-

import simple_markov_lib as lib
import networkx as nx
import matplotlib.pyplot as plt

class Visualizer(object):
    """
    Visualizer creates markov chain visualizations using the matplotlib
    and networkx libraries.
    """
    def __init__(self):
        pass

    def draw_classes_networkx(self, chain, show = True):
        """
        Draws the markov chain's communication class graph using networkx's
        drawing facilities.

        :param chain: the markov chain to be drawn
        :param show: a flag indicating if the drawn graph should be shown
        :returns: the figure created and populated by the method
        """
        connections = chain.get_class_connections()
        class_labels = {
            i: r'$\{{ {0} \}}$'.format(', '.join(i)) for i in connections
        }
        edges = [
            [(i, j) for j in connections[i]] for i in class_labels
        ]

        # flatten edge list 
        edges = [item for sublist in edges for item in sublist]

        # add nodes, get positions, add edges and finally labels
        graph = nx.DiGraph()
        graph.add_nodes_from(i for i in connections)
        pos = nx.spring_layout(graph)

        # create a new figure
        fig = plt.figure(1)
        # draw nodes
        nx.draw_networkx_nodes(
            graph,
            pos,
            node_size = 1500,
            node_color = 'b'
        )

        # draw edges
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist = edges
        )

        # finally, draw the labels
        nx.draw_networkx_labels(
            graph,
            pos,
            labels = class_labels,
            font_size = 14
        )

        if show:
            plt.show()
        return fig
         
    def draw_networkx(self, chain, show = True):
        """
        Draws the markov chain's corresponding graph using networkx's drawing
        facilities. By default, shows the drawn graph.

        :param chain: the markov chain to be drawn
        :param show: a flag indicating if the drawn graph should be shown
        :returns: the figure created and populated by the method
        """
        states = chain.states
        # an array of (state, position) tuples to make drawing easier
        pos_state_map = zip((i for i in states), range(len(states)))

        # labels in latex 
        labels = { i: r'${0}$'.format(i) for i in states }

        # create an edge map 
        edges = [ 
            [(s_from.label, i) for i in s_from.accessible_states()] \
                for s_from in states.values()
        ]

        # flatten the edge map
        edges = [item for sublist in edges for item in sublist]

        try:
            curr = chain.current_state
        except AttributeError:
            curr = None

        graph = nx.DiGraph()

        # add nodes and get positions
        graph.add_nodes_from([i for i in states])
        pos = nx.spring_layout(graph)

        fig = plt.figure(1)
        # plot nodes, mark current state green
        nx.draw_networkx_nodes(
                graph,
                pos,
                node_color = 'r',
                node_size = 1500,
                nodelist = [i for i in states if i != curr]
                )
        
        if curr:
            # draw current_state with green color
            nx.draw_networkx_nodes(
                graph,
                pos,
                node_color = 'g',
                node_size = 1500,
                nodelist = [curr]
            )

        # draw the edges of the network
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist = edges
        )

        # now draw the state labels
        nx.draw_networkx_labels(
            graph,
            pos,
            labels = labels,
            font_size = 14
        )

        # if flag is set, show the graph
        if show:
            plt.show()

        return fig



