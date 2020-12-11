import networkx as nx
import numpy as np


def teacher_disciple_degree(dg):
    """師弟度
    全関係数に対する単方向の接続数
    全関係数は無向グラフの全エッジ数として算出
    重みを全て1に変換後、
    隣接行列Aに変換して、A - A.T差分を算出し、非ゼロの要素数をカウント。
    
    i->jの関係からj->iの関係を減じて、0以上であれば単方向の接続数を求めることができる。
    Args:
        dg (nx.DiGraph): [description]

    Raises:
        Exception: [description]

    Returns:
        dict: [description]
    """
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
    """同僚度
    全関係数に対する単方向の接続数
    全関係数は無向グラフの全エッジ数として算出
    重みを全て1に変換後、
    隣接行列Aに変換して、A ○ A.T（アダマール積）を算出し、非ゼロの要素数をカウント。
    
    i->jの関係とj->iの関係の両方が存在すれば、1になるので、双方向の接続数を求めることができる。

    Args:
        dg (nx.DiGraph)): [description]

    Raises:
        Exception: [description]

    Returns:
        float: [description]
    """
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
    """単方向密度
    師弟度の分母を完全グラフの場合のエッジ数にしたもの
    Args:
        dg (nx.DiGraph): [description]

    Raises:
        Exception: [description]

    Returns:
        float: [description]
    """
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
    """双方向密度
    同僚度の分母を完全グラフの場合のエッジ数にしたもの
    Args:
        dg (nx.DiGraph): [description]

    Raises:
        Exception: [description]

    Returns:
        float: [description]
    """
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
    """コンポーネントごとのネットワーク密度

    Args:
        g (nx.Graph)): [description]

    Raises:
        Exception: [description]

    Returns:
        list: [description]
    """
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
    """コンポーネントごとのネットワークサイズ

    Args:
        g ([type]): [description]

    Raises:
        Exception: [description]

    Returns:
        list: [description]
    """
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

def get_n_bidirect_connect(dg):
    checked_bidirect_edges = []
    for source, target in dg.out_edges:
        for ttarget, _ in dg.adj[target].items():
            if source == ttarget and\
               (target, source) not in checked_bidirect_edges:
                checked_bidirect_edges.append((source, target))
    return len(checked_bidirect_edges)


def get_n_unidirect_connect(dg):
    counter = 0
    for source, target in dg.out_edges:
        counter += 1
        for ttarget, _ in dg.adj[target].items():
            if source == ttarget:
                counter -= 1
                break
    return counter


def calc_network_density(dg):
    n_nodes = len(dg.nodes)
    n_edges = len(dg.edges)
    if n_nodes > 1:
        if(type(dg) == nx.DiGraph):   
            return n_edges / (n_nodes * (n_nodes - 1))
        else:
            return 2 * n_edges / (n_nodes * (n_nodes - 1))
    else:
        return 0


