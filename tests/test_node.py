import unittest
import pandas as pd
from grina.node import *

class TestNode(unittest.TestCase):
    def test_node_colleague_degree(self):
        columns = ["source", "target", "weight"]
        edges = [
            [1, 2, 2],
            [1, 3, 5],
            [2, 1, 6],
            [2, 4, 1],
        ]
        edges_df = pd.DataFrame(edges, columns=columns)
        DG = nx.from_pandas_edgelist(edges_df, "source", "target", ["weight"], create_using=nx.DiGraph)
        node_dict = node_colleague_degree(DG)
        correct_dict = {1:0.5 , 2:0.5 , 3:0, 4:0} 
        self.assertTrue([node_dict[l] == correct_dict[l] for l in node_dict.keys()].all())

    def test_node_teacher_disciple_degree(self):
        columns = ["source", "target", "weight"]
        edges = [
            [1, 2, 2],
            [1, 3, 5],
            [2, 1, 6],
            [2, 4, 1],
        ]
        edges_df = pd.DataFrame(edges, columns=columns)
        DG = nx.from_pandas_edgelist(edges_df, "source", "target", ["weight"], create_using=nx.DiGraph)
        node_dict = node_teacher_disciple_degree(DG)
        correct_dict = {1:0.5 , 2:0.5 , 3:1, 4:1} 
        self.assertTrue([node_dict[l] == correct_dict[l] for l in node_dict.keys()].all())

    def test_node_unidirect_density(self):
        columns = ["source", "target", "weight"]
        edges = [
            [1, 2, 2],
            [1, 3, 5],
            [2, 1, 6],
            [2, 4, 1],
        ]
        edges_df = pd.DataFrame(edges, columns=columns)
        DG = nx.from_pandas_edgelist(edges_df, "source", "target", ["weight"], create_using=nx.DiGraph)
        node_dict = node_unidirect_density(DG)
        correct_dict = {1:1/3 , 2:1/3 , 3:1/3, 4:1/3} 
        self.assertTrue([node_dict[l] == correct_dict[l] for l in node_dict.keys()].all())

    def test_node_bidirect_density(self):
        columns = ["source", "target", "weight"]
        edges = [
            [1, 2, 2],
            [1, 3, 5],
            [2, 1, 6],
            [2, 4, 1],
        ]
        edges_df = pd.DataFrame(edges, columns=columns)
        DG = nx.from_pandas_edgelist(edges_df, "source", "target", ["weight"], create_using=nx.DiGraph)
        node_dict = node_bidirect_density(DG)
        correct_dict = {1:1/3 , 2:1/3 , 3:0, 4:0} 
        self.assertTrue([node_dict[l] == correct_dict[l] for l in node_dict.keys()].all())



if __name__ == '__main__':
    unittest.main()