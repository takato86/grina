import networkx as nx
from networkx.algorithms import chains, components


def to_unweighted(dg):
    """ネットワークの重みを全て1に変換する。

    Args:
        dg (nx.DiGraph or nx.Graph): 有向グラフ or 無向グラフ

    Returns:
        nx.DiGraph or nx.Graph: 有向グラフ or 無向グラフ
    """
    unweight_dg = dg.copy()
    edges = []
    for edge in unweight_dg.edges():
        edges.append(
            (edge[0], edge[1], {'weight': 1})
        )
    unweight_dg.update(edges=edges)
    return unweight_dg


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


def get_gatekeeper_degree(dg):
    """ゲートキーパー度
    入次数×出次数で計算
    Args:
        dg ([type]): [description]

    Returns:
        [type]: [description]
    """
    gatekeeper_dgree_dict = {}
    out_degrees = dict(dg.out_degree())
    # print("node\t\t:degree gatekeeper")
    for node, in_degree in dg.in_degree():
        gatekeeper = in_degree * out_degrees[node]
        gatekeeper_dgree_dict[node] = gatekeeper
    return gatekeeper_dgree_dict


def calc_degree_centralities(dg):
    degree_centers = nx.degree_centrality(dg)
    return {k:v for k,v in sorted(degree_centers.items(), key=lambda x:x[1], reverse=True)}


def calc_close_centralities(dg):
    close_centers = nx.closeness_centrality(dg)
    return {k:v for k,v in sorted(close_centers.items(), key=lambda x:x[1], reverse=True)}


def calc_between_centralities(dg):
    between_centers = nx.betweenness_centrality(dg)
    return {k:v for k,v in sorted(between_centers.items(), key=lambda x:x[1], reverse=True)}


def calc_eigen_centralities(dg):
    eigen_centers = nx.eigenvector_centrality_numpy(dg)
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
    for source, target_dict in nx.shortest_path_length(dg):
        # max_length = 0
        # for length in target_dict.values():
        #     if max_length < length:
        #         max_length = length
        # elogation_dict[source] = max_length
        elogation_dict[source] = max(list(target_dict.values))
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
    for node in dg.nodes():
        expansion_dict[node] = len(nx.shortest_path(dg, node))-1
    return expansion_dict


def node_teacher_disciple_degree(dg):
    """師弟度
    あるノードの全関係に対する単方向の関係の割合
    単方向の関係数 = 2 * 全関係数 - (入次数 + 出次数)
    全関係数は無向グラフに変換したときの全エッジ数。
    この式は双方向の関係数を算出して、全関係数から双方向の関係数を減ずることで求めることができる。

    Args:
        dg (nx.DiGraph): 有向グラフ

    Raises:
        Exception: クラスチェック

    Returns:
        dict: ノードごとの師弟度辞書
    """
    if type(dg) != nx.DiGraph:
        raise Exception("dg is not DiGraph")
    unweight_dg = dg.copy()
    for edge in unweight_dg.edges.data():
        edge["weight"] = 1
    g = unweight_dg.to_undirected()
    in_degrees = dict(unweight_dg.in_degree)
    out_degrees = dict(unweight_dg.out_degree)
    nodes = list(unweight_dg.nodes)
    degrees = dict(g.degree)
    content = {}
    for node in nodes:
        bidirect = in_degrees[node] + out_degrees[node] - degrees[node]
        content[node] = (degrees[node] - bidirect) / degrees[node]
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
        content[node] = bidirect / degrees[node]
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