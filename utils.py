import operator

def accumulate(iterable, func=operator.add):
    """
    Return the running total in a list using the addition operator by
    default.

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

    :return a list containing all strongly connected components of the graph
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
            connected_component = set()

            # keep a list of reachable neighbours in order to determine
            # if the component is closed or open
            neighbours = set()
            while True:
                succ = stack.pop()
                connected_component.add(succ)

                # add all neighbours to set
                for nb in graph[succ]:
                    neighbours.add(nb)
                if succ == node:
                    break

            # check if neighbours are a subset of the connected component
            cp_type = "closed" if neighbours <= connected_component else "open"

            # return a dict containing component info
            result.append({
                "states": connected_component,
                "type": cp_type
            })

    # apply the connect() method on all nodes
    for node in graph:
        if node not in lowlinks:
            connect(node)

    return result

