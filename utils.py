import operator

def accumulate(iterable, func=operator.add):
    """
    Return the running total in a list using the addition operator by
    default.

    :param iterable: the iterable to be traversed
    :param func: the operation to be performed
    :returns: the running total in the iterable

    >>> accumulate([1,2,3,4,5]) # 1 3 6 10 15
    >>> accumulate([1,2,3,4,5], operator.mul) # 1 2 6 24 120
    """
    it = iter(iterable)
    try:
        total = next(it)
    except StopIteration:
        return
    yield total
    for element in it:
        total = func(total, element)
        yield total


def strongly_connected_components(graph):
    """
    Find the stronly connected components of a graph by applying Tarjan's
    algorithm on a graph.

    :param graph: a graph in dict notation.
    :returns: a list containing all strongly connected components of the graph

    >>> strongly_connected_components({
        'A': {'B': 0.6, 'C': 0.4},
        'B': {'C': 0.2, 'B': 0.8},
        'C': {'B': 0.5, 'C': 0.5}
        })
    [{'B', 'C'}, {'A'}]

    """
    index, lowlinks = {}, {}
    stack, result = [], []
    index_counter = [0]

    def connect(node):
        # set this node's index to the smallest unused index
        index[node] = index_counter[0]
        lowlinks[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)

        try:
            successors = graph[node]
        except KeyError:
            successors = []

        for succ in successors:
            if succ not in lowlinks:
                # successor is unvisited
                connect(succ)
                lowlinks[node] = min(lowlinks[node], lowlinks[succ])
            elif succ in stack:
                # the successor is in the stack and therefore in the
                # currently examined component
                lowlinks[node] = min(lowlinks[node], index[succ])

        # if node is a root node, generate a stronly connected component
        if lowlinks[node] == index[node]:
            connected_component = []
            while True:
                succ = stack.pop()
                connected_component.append(succ)
                if succ == node:
                    break
            component = set(connected_component)
            result.append(component)

    # apply the connect() method on all nodes
    for node in graph:
        if node not in lowlinks:
            connect(node)

    return result

