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
        raise Exception('There are at least two nodes sharing position')


def shortest_path():
    halls = [Hall('Hall number {}'.format(i), i) for i in range(26)]

    G = nx.DiGraph()
    G.add_nodes_from(halls)

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
    pos = {
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

    _check_edges_consistency(edges)
    _check_nodes_superposition(pos)
    for vertix, neighbours in edges.items():
        for neighbour in neighbours:
            G.add_edge(halls[vertix], halls[neighbour])

    start = halls[0]
    last_visited = start
    must_visit = [halls[18], halls[17], halls[24], ]
    visited = [halls[0], ]
    path = [halls[0], ]
    while must_visit:
        next_node = None
        minimum = None
        for node in must_visit:
            path_length = nx.dijkstra_path_length(G, last_visited, node)
            if not minimum or path_length < minimum:
                minimum = path_length
                next_node = node
        j = nx.dijkstra_path(G, last_visited, next_node)
        path.extend(j[1:])
        last_visited = next_node
        visited.append(next_node)
        must_visit.remove(next_node)

    """
    Convert path made of nodes into edges by taking them two at a time
    """
    path_edges = [(path[i], path[i+1]) for i in range(len(path)-1)]

    """
    For every edge in the graph, if the edge is in the path, it gets painted
    red. If it isn't, defaults to key (black)
    """
    colors = []
    for edge in G.edges():
        if edge in path_edges:
            colors.append('r')
        else:
            colors.append('k')

    print(path)

    nx.draw(G, pos, with_labels=True, edge_color=colors, node_size=2500)
    # nx.draw_networkx_nodes(G, pos, nodelist=G.nodes(), node_size=2500)
    # nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r')
    # plt.savefig("graph.png")
    plt.show()

if __name__ == '__main__':
    shortest_path()
