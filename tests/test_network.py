import unittest
import networkx as nx
import pandas as pd
from grina import *

class TestNode(unittest.TestCase):
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
    

if __name__ == '__main__':
    unittest.main()