import sys
import os
import unittest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from main import (prim, kruskal, floyd_warshall, fractional_knapsack,
                  knapsack_01, n_queens, tsp_backtracking, choose_mst)
from data_structures import BTree, RedBlackTree

class Algorithm2035Tests(unittest.TestCase):
    def setUp(self):
        self.edges = [(0,1,4), (0,2,3), (1,2,1), (1,3,2), (2,3,4)]

    def test_mst_costs_match(self):
        self.assertEqual(prim(4, self.edges)[0], 6)
        self.assertEqual(kruskal(4, self.edges)[0], 6)

    def test_mst_adaptation_sparse(self):
        d = choose_mst(6, [(0,1,1),(1,2,2),(2,3,3),(3,4,4),(4,5,5)])
        self.assertEqual(d.algorithm, "Kruskal")

    def test_floyd_warshall(self):
        d = floyd_warshall(3, [(0,1,5),(1,2,2),(0,2,10)])
        self.assertEqual(d[0][2], 7)

    def test_fractional_knapsack(self):
        value, chosen = fractional_knapsack([("A",60,10),("B",100,20)], 15)
        self.assertAlmostEqual(value, 85)

    def test_01_knapsack(self):
        value, selected = knapsack_01([("A",60,10),("B",100,20),("C",120,30)], 50)
        self.assertEqual(value, 220)
        self.assertEqual(set(selected), {"B","C"})

    def test_n_queens(self):
        sol = n_queens(4)
        self.assertIsNotNone(sol)
        self.assertEqual(len(set(sol)), 4)
        self.assertEqual(len(set(r-c for r,c in enumerate(sol))), 4)
        self.assertEqual(len(set(r+c for r,c in enumerate(sol))), 4)

    def test_tree_comparison_search(self):
        values = [10, 5, 20, 3, 7, 15, 30, 6, 8, 25]
        for tree in (BTree(degree=2), RedBlackTree()):
            for value in values:
                tree.insert(value)
            for value in values:
                self.assertTrue(tree.search(value))
            self.assertFalse(tree.search(999))

    def test_tsp(self):
        m = [[0,10,15,20],[10,0,35,25],[15,35,0,30],[20,25,30,0]]
        cost, path = tsp_backtracking(m)
        self.assertEqual(cost, 80)
        self.assertEqual(path[0], 0)
        self.assertEqual(path[-1], 0)

if __name__ == "__main__":
    unittest.main()
