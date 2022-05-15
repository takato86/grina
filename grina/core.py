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

