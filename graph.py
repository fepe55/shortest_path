import matplotlib.pyplot as plt
import networkx as nx


class Hall:
    name = None
    number = None

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __repr__(self):
        return 'hall {}'.format(self.number)


def _get_edges_first_floor():
    edges = {
        0: [1, 9, 10, 12, 23],
        1: [0, 2, 3],
        2: [1],
        3: [1, 4],
        4: [3, 5],
        5: [4, 6, 9],
        6: [5],
        7: [9],
        8: [9],
        9: [0, 5, 7, 8, 10],
        10: [0, 9, 12],
        11: [12],
        12: [0, 10, 11, 13, 14],
        13: [12],
        14: [12, 15],
        15: [14, 16, 18, 20, 25],
        16: [15, 17],
        17: [16],
        18: [15, 20],
        19: [20],
        20: [15, 18, 19, 21, 22],
        21: [20],
        22: [20, 23],
        23: [22, 24, 0],
        24: [23],
        25: [15],
    }
    return edges


def _get_positions_first_floor(halls):
    positions = {
        halls[0]: (0, 0),
        halls[1]: (-2, -2),
        halls[2]: (-2, -1),
        halls[3]: (-3, -1),
        halls[4]: (-3, 0),
        halls[5]: (-3, 1),
        halls[6]: (-3, 2),
        halls[7]: (-2, 2),
        halls[8]: (-1, 2),
        halls[9]: (-2, 1),
        halls[10]: (0, 2),
        halls[11]: (1, 2),
        halls[12]: (1, 1),
        halls[13]: (2, 2),
        halls[14]: (3, 2),
        halls[15]: (4, 2),
        halls[16]: (5, 2),
        halls[17]: (6, 2),
        halls[18]: (3, 0),
        halls[19]: (3, -1),
        halls[20]: (4, -1),
        halls[21]: (5, -1),
        halls[22]: (4, -2),
        halls[23]: (3, -2),
        halls[24]: (2, -1),
        halls[25]: (4, 3),
    }
    return positions


def _get_edges_second_floor():
    edges = {
        25-25: [26-25, 39-25, 41-25, ],
        26-25: [25-25, 27-25, 28-25, ],
        27-25: [26-25, ],
        28-25: [29-25, 26-25, ],
        29-25: [30-25, 28-25, ],
        30-25: [29-25, 31-25],
        31-25: [30-25, 32-25, ],
        32-25: [33-25, 31-25, ],
        33-25: [32-25, 34-25, 41-25, ],
        34-25: [33-25, 35-25],
        35-25: [34-25, 36-25],
        36-25: [35-25, 37-25, ],
        37-25: [38-25, 36-25, ],
        38-25: [39-25, 37-25, ],
        39-25: [40-25, 25-25, 38-25, ],
        40-25: [39-25, ],
        41-25: [33-25, 25-25],
    }
    return edges


def _get_positions_second_floor(halls):
    positions = {
        halls[25-25]: (0, -1),
        halls[26-25]: (-1, -1),
        halls[27-25]: (-1, 0),
        halls[28-25]: (-3, -1),
        halls[29-25]: (-3, 0),
        halls[30-25]: (-3, 1),
        halls[31-25]: (-2, 1),
        halls[32-25]: (-1, 1),
        halls[33-25]: (0, 1),
        halls[34-25]: (1, 1),
        halls[35-25]: (2, 1),
        halls[36-25]: (3, 1),
        halls[37-25]: (3, 0),
        halls[38-25]: (3, -1),
        halls[39-25]: (1, -1),
        halls[40-25]: (1, 0),
        halls[41-25]: (0, 0),
    }
    return positions


def _check_edges_consistency(edges):
    """
    Checks that there are no two nodes N and M such as N shows in M's
    neighbours list but M doesn't in N's neighbours list
    ie: This shouldn't happen:
        {
            M: [a, b, c, N, ],
            N: [j, k, l, ],
        }
    """
    errors = []
    for vertix, neighbours in edges.items():
        for neighbour in neighbours:
            if vertix not in edges[neighbour]:
                errors.append(
                    '{} is in  {}\'s neighbours, but {} is not '
                    'in {}\'s neighbours'.format(
                        neighbour, vertix, vertix, neighbour
                    )
                )

    if errors:
        raise Exception('\n'.join(errors))


def _check_nodes_superposition(positions):
    """
    Checks that there is no node superposition
    """
    positions = [position for node, position in positions.items()]
    if len(positions) != len(set(positions)):
        print(positions)
        print(set(positions))
        raise Exception('There are at least two nodes sharing position')


def build_graph(nodes, edges):
    G = nx.MultiDiGraph()
    G.add_nodes_from(nodes)
    for vertix, neighbours in edges.items():
        for neighbour in neighbours:
            G.add_edge(nodes[vertix], nodes[neighbour])
    return G


def shortest_path(G, start, must_visit):
    _must_visit = must_visit[::-1]
    last_visited = start
    visited = [start, ]
    path = [start, ]
    while _must_visit:
        next_node = None
        minimum = None
        for node in _must_visit:
            path_length = nx.dijkstra_path_length(G, last_visited, node)
            if not minimum or path_length < minimum:
                minimum = path_length
                next_node = node
        current_path = nx.dijkstra_path(G, last_visited, next_node)
        # Remove the first one or else it'd be duplicated
        path.extend(current_path[1:])
        last_visited = next_node
        visited.append(next_node)
        _must_visit.remove(next_node)
    return path


def first_floor():
    halls = [Hall('Hall number {}'.format(i), i) for i in range(26)]
    start = halls[0]
    must_visit = [halls[1], halls[4], halls[24], halls[19], halls[7], ]

    edges = _get_edges_first_floor()
    _check_edges_consistency(edges)

    positions = _get_positions_first_floor(halls)
    _check_nodes_superposition(positions)

    G = build_graph(halls, edges)

    graph(G, start, must_visit, positions)


def second_floor():
    halls = [Hall('Hall number {}'.format(i+25), i+25) for i in range(17)]
    start = halls[41-25]
    must_visit = [halls[30-25], halls[36-25], ]

    edges = _get_edges_second_floor()
    _check_edges_consistency(edges)

    positions = _get_positions_second_floor(halls)
    _check_nodes_superposition(positions)

    G = build_graph(halls, edges)

    graph(G, start, must_visit, positions)


def graph(G, start, must_visit, positions):
    NODE_SIZE = 2000
    path = shortest_path(G, start, must_visit)
    """
    Convert path made of nodes into edges by taking them two at a time
    """
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]

    """
    Add the order of the edge in the path as its label
    """
    edge_labels = {}
    for edge in G.edges():
        if edge in path_edges:
            label = path_edges.index(edge)
        else:
            label = ''
        edge_labels[edge] = label

    nodes_not_in_path = [node for node in G.nodes() if node not in path]
    edges_not_in_path = [edge for edge in G.edges() if edge not in path_edges]

    # NODES
    # First we draw the nodes that are not in the path, transparent
    nx.draw_networkx_nodes(
        G, positions, nodelist=nodes_not_in_path, node_size=NODE_SIZE,
        alpha=0.2,
    )
    # Then, we draw the nodes that ARE in the path
    nx.draw_networkx_nodes(
        G, positions, nodelist=path, node_size=NODE_SIZE,
    )
    # And lastly, the nodes that must be visited, have an edge
    nx.draw_networkx_nodes(
        G, positions, nodelist=must_visit,
        node_size=NODE_SIZE, edgecolors='k', linewidths=2,
    )

    # NODE LABELS
    nx.draw_networkx_labels(
        G, positions, node_size=NODE_SIZE,
    )

    # EDGES
    # First we draw the edges that are not in the path, transparent
    nx.draw_networkx_edges(
        G, positions, edgelist=edges_not_in_path, edge_color='k', alpha=0.1,
        node_size=NODE_SIZE,
    )
    # And then we draw that edges that ARE in the path, in red
    nx.draw_networkx_edges(
        G, positions, edgelist=path_edges, edge_color='r', node_size=NODE_SIZE,
    )

    # EDGES LABELS
    nx.draw_networkx_edge_labels(
        G, positions, edge_labels=edge_labels, label_pos=0.7,
        node_size=NODE_SIZE
    )

    # plt.savefig("graph.png")
    plt.axis('off')
    # plt.show()


if __name__ == '__main__':
    plt.figure(1)
    first_floor()
    plt.figure(2)
    second_floor()
    plt.show()
