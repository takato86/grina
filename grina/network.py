import networkx as nx
import numpy as np


def teacher_disciple_degree(dg):
    if type(dg) != nx.DiGraph:
        raise Exception("dg is not DiGraph type.")
    g = dg.to_undirected()
    all_edges = len(g.edges)
    adj = nx.to_numpy_array(dg)
    i_adj = np.where(adj > 0, 1, 0)
    diff = i_adj - i_adj.T
    unidirect = np.count_nonzero(diff) / 2
    return unidirect / all_edges


def colleague_degree(dg):
    if type(dg) != nx.DiGraph:
        raise Exception("dg is not DiGraph type.")
    g = dg.to_undirected()
    all_edges = len(g.edges)
    adj = nx.to_numpy_array(dg)
    i_adj = np.where(adj > 0, 1, 0)
    diff = i_adj * i_adj.T
    bidirect = np.count_nonzero(diff) / 2
    return bidirect / all_edges


def unidirect_density(dg):
    if type(dg) != nx.DiGraph:
        raise Exception("dg is not DiGraph type.")
    N = len(dg.nodes)
    all_relations = N * (N-1) / 2
    adj = nx.to_numpy_array(dg)
    i_adj = np.where(adj > 0, 1, 0)
    diff = i_adj - i_adj.T
    unidirect = np.count_nonzero(diff) / 2
    return unidirect / all_relations


def bidirect_density(dg):
    if type(dg) != nx.DiGraph:
        raise Exception("dg is not DiGraph type.")
    N = len(dg.nodes)
    all_relations = N * (N-1) / 2
    adj = nx.to_numpy_array(dg)
    i_adj = np.where(adj > 0, 1, 0)
    diff = i_adj * i_adj.T
    bidirect = np.count_nonzero(diff) / 2
    return bidirect / all_relations


def components_density(g):
    if type(g) != nx.Graph:
        raise Exception("g is not Graph type.")
    component_list = [
        g.subgraph(c)
        for c in sorted(nx.connected_components(g),
                        key=len,
                        reverse=True)
    ]
    densities = []
    for component in component_list:
        densities.append(nx.density(component))
    return densities


def components_size(g):
    if type(g) != nx.Graph:
        raise Exception("g is not Graph type.")
    component_list = [
        g.subgraph(c)
        for c in sorted(nx.connected_components(g),
                        key=len,
                        reverse=True)
    ]
    sizes = []
    for component in component_list:
        sizes.append(component.number_of_nodes())
    return sizes



