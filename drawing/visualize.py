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
            node_size = 2000,
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
            font_size = 12
        )

        if show:
            plt.show()
        return fig

    def redraw_networkx(self, chain, info_dict, show = True):
        """
        Redraws a previously drawn markov chain using info about the previously
        created figure, including labels, nodes, edges, etc.

        :param chain: the markov chain to visualize
        :param info_dict: the dictionary containing the info about the
         previously created plot
        :param show: a flag indicating if the created plot should be drawn
        :returns: the dictionary containing the figure handle as well as
        info about edges, nodes, labels, etc. to be used in redrawing
        """
        # Retrieve all drawing info
        pos_state_map = info_dict['pos_state_map']
        edges = info_dict['edges']
        pos = info_dict['pos']
        fig = info_dict['fig']
        labels = info_dict['labels']
        graph = info_dict['graph']

        try:
            curr = chain.current_state
        except AttributeError:
            curr = None

        states = chain.states
        nx.draw_networkx_nodes(
                graph,
                pos,
                node_color = 'r',
                node_size = 2000,
                nodelist = [i for i in states if i != curr]
                )

        if curr:
        # draw current_state with green color
            nx.draw_networkx_nodes(
                graph,
                pos,
                node_color = 'g',
                node_size = 2000,
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

        return {
            'fig': fig,
            'pos': pos,
            'edges': edges,
            'pos_state_map': pos_state_map,
            'graph': graph
        }

    def draw_networkx(self, chain, show = True):
        """
        Draws the markov chain's corresponding graph using networkx's drawing
        facilities. By default, shows the drawn graph.

        :param chain: the markov chain to be drawn
        :param show: a flag indicating if the drawn graph should be shown
        :returns: the dictionary containing the figure handle as well as
         info about edges, nodes, labels, etc. to be used in redrawing
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
                node_size = 2000,
                nodelist = [i for i in states if i != curr]
                )
        
        if curr:
            # draw current_state with green color
            nx.draw_networkx_nodes(
                graph,
                pos,
                node_color = 'g',
                node_size = 2000,
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

        return {
            'fig': fig,
            'pos': pos,
            'edges': edges,
            'labels': labels,
            'pos_state_map': pos_state_map,
            'graph': graph
        }



