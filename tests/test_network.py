import unittest
import networkx as nx
import pandas as pd
from grina import *

class TestNetwork(unittest.TestCase):
    def test_teacher_disciple_degree(self):
        columns = ["source", "target", "weight"]
        edges = [
            [1, 2, 2],
            [1, 3, 5],
            [2, 1, 6],
            [2, 4, 1],
        ]
        edges_df = pd.DataFrame(edges, columns=columns)
        DG = nx.from_pandas_edgelist(edges_df, "source", "target", ["weight"], create_using=nx.DiGraph)
        deg = teacher_disciple_degree(DG)
        self.assertEqual(deg, 2/3)

    def test_colleague_degree(self):
        columns = ["source", "target", "weight"]
        edges = [
            [1, 2, 2],
            [1, 3, 5],
            [2, 1, 6],
            [2, 4, 1],
        ]
        edges_df = pd.DataFrame(edges, columns=columns)
        DG = nx.from_pandas_edgelist(edges_df, "source", "target", ["weight"], create_using=nx.DiGraph)
        deg = colleague_degree(DG)
        self.assertEqual(deg, 1/3)

    def test_unidirect_density(self):
        columns = ["source", "target", "weight"]
        edges = [
            [1, 2, 2],
            [1, 3, 5],
            [2, 1, 6],
            [2, 4, 1],
        ]
        edges_df = pd.DataFrame(edges, columns=columns)
        DG = nx.from_pandas_edgelist(edges_df, "source", "target", ["weight"], create_using=nx.DiGraph)
        deg = unidirect_density(DG)
        self.assertEqual(deg, 2/6)
    
    def test_bidirect_density(self):
        columns = ["source", "target", "weight"]
        edges = [
            [1, 2, 2],
            [1, 3, 5],
            [2, 1, 6],
            [2, 4, 1],
        ]
        edges_df = pd.DataFrame(edges, columns=columns)
        DG = nx.from_pandas_edgelist(edges_df, "source", "target", ["weight"], create_using=nx.DiGraph)
        deg = bidirect_density(DG)
        self.assertEqual(deg, 1/6)
    
    def test_components_density(self):
        columns = ["source", "target", "weight"]
        edges = [
            [1, 2, 2],
            [1, 3, 5],
            [2, 4, 1],
            [5, 6, 1]
        ]
        edges_df = pd.DataFrame(edges, columns=columns)
        G = nx.from_pandas_edgelist(edges_df, "source", "target", ["weight"], create_using=nx.Graph)
        densities = np.array(components_density(G))
        correct = np.array([0.5, 1])
        self.assertTrue((densities == correct).all())

    def test_components_size(self):
        columns = ["source", "target", "weight"]
        edges = [
            [1, 2, 2],
            [1, 3, 5],
            [2, 4, 1],
            [5, 6, 1]
        ]
        edges_df = pd.DataFrame(edges, columns=columns)
        G = nx.from_pandas_edgelist(edges_df, "source", "target", ["weight"], create_using=nx.Graph)
        sizes = np.array(components_size(G))
        correct = np.array([4, 2])
        self.assertTrue((sizes == correct).all())

 

if __name__ == '__main__':
    unittest.main()