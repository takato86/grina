import networkx as nx


def get_max_shortest_path_length(edge_list_df, graph_type, vertex):
    G = nx.from_pandas_edgelist(edge_list_df, create_using=graph_type)
    shortest_path_lengths = [
        path_length
        for path_length in nx.shortest_path_length(G, vertex)
    ]
    return (vertex, max(shortest_path_lengths))

def get_n_shortest_paths(edge_list_df, graph_type, vertex):
    G = nx.from_pandas_edgelist(edge_list_df, create_using=graph_type)
    n_shortest_paths = len(nx.shortest_path_length(G, vertex)) - 1
    return (vertex, n_shortest_paths)