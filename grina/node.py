import logging
import networkx as nx
import numpy as np
from grina.core import to_unweighted
import igraph as ig

logger = logging.getLogger("grina")

try:
    import cugraph as cnx
    logger.info("Imported cugraph!")
except Exception:
    import networkx as cnx
    logger.info("Imported networkx.")


def get_n_entry(dg):
    """入次数の算出

    Args:
        dg ([nx.DiGraph]): [description]

    Returns:
        [dict]: [description]
    """
    return dict(dg.in_degree())


def get_n_exit(dg):
    """出次数の算出

    Args:
        dg ([nx.DiGraph]): [description]

    Returns:
        [dict]: [description]
    """
    return dict(dg.out_degree())


def get_diff_entry_exit(dg):
    """入次数と出次数の差の算出
    |入次数-出次数|で計算
    Args:
        dg ([nx.DiGraph]): [description]

    Returns:
        [dict]: [description]
    """
    diff_dict = {}
    out_degrees = dict(dg.out_degree())
    # print("node\t\t:absolute diff")
    for node, in_degree in dg.in_degree():
        diff = abs(in_degree-out_degrees[node])
        # print(f"{node}\t:{diff}")
        diff_dict[node] = diff
    return diff_dict


def get_out_in_degree(dg):
    """出次数 - 入次数で算出

    Args:
        dg ([type]): [description]

    Returns:
        [type]: [description]
    """
    out_in_dict = {}
    out_degrees = dict(dg.out_degree())
    # print("node\t\t:absolute diff")
    for node, in_degree in dg.in_degree():
        diff = out_degrees[node] - in_degree
        out_in_dict[node] = diff
    return out_in_dict


def get_gatekeeper_degree(dg):
    """ゲートキーパー度
    (入次数×出次数)**0.5で計算
    Args:
        dg ([type]): [description]

    Returns:
        [type]: [description]
    """
    gatekeeper_dgree_dict = {
        k: np.sqrt(v) for k, v in get_inxout_degree(dg).items()
    }
    
    return gatekeeper_dgree_dict


def get_inxout_degree(dg):
    """入次数X出次数で計算

    Args:
        dg (nx.DiGraph): [description]

    Returns:
        dict: [description]
    """
    inxout_degree_dict = {}
    out_degrees = dict(dg.out_degree())
    # print("node\t\t:degree gatekeeper")
    for node, in_degree in dg.in_degree():
        inxout_degree = in_degree * out_degrees[node]
        inxout_degree_dict[node] = inxout_degree
    return inxout_degree_dict


def calc_degree_centralities(dg):
    degree_centers = nx.degree_centrality(dg)
    return {k:v for k,v in sorted(degree_centers.items(), key=lambda x:x[1], reverse=True)}


def calc_close_centralities(dg):
    dg_ig = ig.Graph.from_networkx(dg)
    keys = dg_ig.vs["_nx_name"]
    close_centers = [(key, value) for key, value in zip(keys, dg_ig.closeness())]
    return {k:v for k,v in sorted(close_centers, key=lambda x:x[1], reverse=True)}


def calc_between_centralities(dg):
    between_centers = cnx.betweenness_centrality(dg)
    return {k:v for k,v in sorted(between_centers.items(), key=lambda x:x[1], reverse=True)}


def calc_eigen_centralities(dg):
    eigen_centers = nx.eigenvector_centrality(dg, max_iter=1000)
    return {k:v for k,v in sorted(eigen_centers.items(), key=lambda x:x[1], reverse=True)}


def get_elongation(dg):
    """伸長度の算出
    任意ノードから遷移できる最大の長さ
    Arguments:
        dg {DirectedGraph} -- 有向グラフインスタンス
    
    Returns:
        dict -- ノードIDと伸長度の辞書
    """
    elogation_dict = {}
    dg_ig = ig.Graph.from_networkx(dg)

    for vertex in dg_ig.vs:
        shortest_path_lengths = [
            len(path)
            for path in vertex.get_shortest_paths(output="vpath")
        ]
        elogation_dict[vertex["_nx_name"]] = max(shortest_path_lengths)

    return elogation_dict


def get_degree_expansion(dg):
    """拡張度の算出
    任意ノードから最短経路の終端ノード数
    Arguments:
        dg {DirectedGraph} -- 有向グラフのインスタンス
    
    Returns:
        dict -- ノードIDと拡張度の辞書
    """
    expansion_dict = {}
    dg_ig = ig.Graph.from_networkx(dg)

    for vertex in dg_ig.vs:
        expansion_dict[vertex["_nx_name"]] = len(vertex.get_shortest_paths(output="vpath")) - 1

    return expansion_dict


def node_teacher_disciple_degree(dg):
    """師弟度
    あるノードの全関係に対する単方向の関係の割合
    単方向の関係数 = 2 * 全関係数 - (入次数 + 出次数)
    全関係数は無向グラフに変換したときの全エッジ数。
    全関係数から双方向の関係数を減ずることで求めることができる。

    Args:
        dg (nx.DiGraph): 有向グラフ

    Raises:
        Exception: クラスチェック

    Returns:
        dict: ノードごとの師弟度辞書
    """
    if type(dg) != nx.DiGraph:
        raise Exception("dg is not DiGraph")
    unweight_dg = to_unweighted(dg)
    g = unweight_dg.to_undirected()
    in_degrees = dict(unweight_dg.in_degree)
    out_degrees = dict(unweight_dg.out_degree)
    nodes = list(unweight_dg.nodes)
    degrees = dict(g.degree)
    content = {}
    for node in nodes:
        bidirect = in_degrees[node] + out_degrees[node] - degrees[node]
        if degrees[node] > 0:
            content[node] = (degrees[node] - bidirect) / degrees[node]
        else:
            content[node] = 0
    return content


def node_colleague_degree(dg):
    """同僚度
    あるノードの全関係に対する双方向の関係の割合
    双方向の関係数 = (入次数 + 出次数) - 全関係数
    全関係数は全ての接続が単方向だった場合の関係数とみなせ、
    接続されているエッジ数の合計から全単方向の関係数を減ずることで求めている。    

    Args:
        dg (nx.DiGraph): 有向グラフ

    Raises:
        Exception: クラスチェック

    Returns:
        dict: ノードごとの同僚度
    """
    if type(dg) != nx.DiGraph:
        raise Exception("dg is not DiGraph")
    unweight_dg = to_unweighted(dg)
    g = unweight_dg.to_undirected()
    in_degrees = dict(unweight_dg.in_degree)
    out_degrees = dict(unweight_dg.out_degree)
    nodes = list(unweight_dg.nodes)
    degrees = dict(g.degree)
    content = {}
    for node in nodes:
        bidirect = in_degrees[node] + out_degrees[node] - degrees[node]
        if degrees[node] > 0:
            content[node] = bidirect / degrees[node]
        else:
            content[node] = 0
    return content


def node_unidirect_density(dg):
    """単方向密度
    単方向の接続数 / 完全グラフとした時の接続数
    Args:
        dg (nx.DiGraph): [description]

    Raises:
        Exception: [description]

    Returns:
        dict: [description]
    """
    if type(dg) != nx.DiGraph:
        raise Exception("dg is not DiGraph")
    unweight_dg = to_unweighted(dg)
    g = unweight_dg.to_undirected()
    in_degrees = dict(unweight_dg.in_degree)
    out_degrees = dict(unweight_dg.out_degree)
    nodes = list(unweight_dg.nodes)
    degrees = dict(g.degree)
    content = {}
    for node in nodes:
        bidirect = in_degrees[node] + out_degrees[node] - degrees[node]
        content[node] = (degrees[node] - bidirect) / (2 * len(nodes))
    return content


def node_bidirect_density(dg):
    """双方向密度
    単方向の接続数 / 完全グラフとした時の接続数
    Args:
        dg (nx.DiGraph): [description]

    Raises:
        Exception: [description]

    Returns:
        dict: [description]
    """
    if type(dg) != nx.DiGraph:
        raise Exception("dg is not DiGraph")
    unweight_dg = to_unweighted(dg)
    g = unweight_dg.to_undirected()
    in_degrees = dict(unweight_dg.in_degree)
    out_degrees = dict(unweight_dg.out_degree)
    nodes = list(unweight_dg.nodes)
    degrees = dict(g.degree)
    content = {}
    for node in nodes:
        bidirect = in_degrees[node] + out_degrees[node] - degrees[node]
        content[node] = bidirect / (2 * len(nodes))
    return content