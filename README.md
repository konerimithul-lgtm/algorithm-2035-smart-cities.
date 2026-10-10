# Algorithm 2035: Adaptive Algorithm Selection Framework for Smart Cities

A standard-library Python prototype for the DAA Assignment 1 handout. It models smart-city scenarios and selects/executes syllabus algorithms with explanations.

## Requirements
- Python 3.10 or newer
- No third-party packages required

## Run
```bash
python main.py
```

## Run tests
```bash
python -m unittest discover -s tests -v
```

## Modules implemented in this prototype
1. Infrastructure network: Prim and Kruskal, with an explainable graph-density heuristic and side-by-side measured comparison.
2. All-pairs connectivity: Floyd-Warshall.
3. Budgeted project selection: Fractional Knapsack and 0/1 Knapsack.
4. Constraint search: N-Queens using backtracking.
5. Small inspection tour: exact TSP using backtracking.
6. Experiment: reproducible graph generation and runtime comparison for Prim/Kruskal.
7. Data structures: B-Tree and Red-Black Tree insertion/search runtime comparison.

## Complexity summary
| Technique | Time | Space |
|---|---|---|
| Kruskal MST | O(E log E) | O(V + E) |
| Prim in this code | O(V^2 + E) | O(V + E) |
| Floyd-Warshall | O(V^3) | O(V^2) |
| Fractional Knapsack | O(n log n) | O(n) |
| 0/1 Knapsack DP | O(nW) time | O(nW) for reconstruction |
| N-Queens backtracking | Exponential worst case | O(N) auxiliary state, excluding output |
| TSP backtracking | O(n!) worst case | O(n) search state |

B-Tree and Red-Black Tree: O(log n) worst-case insertion/search; space O(n).

`W` is the integer budget/capacity. 0/1 Knapsack DP is pseudo-polynomial in W. Optimization TSP is NP-Hard; its decision version is NP-Complete.

## Important scope note
This prototype includes a B-Tree vs Red-Black Tree insertion/search comparison. It does not implement Binomial/Fibonacci heaps, so add those only if your instructor expects both priority-structure implementations.

## Suggested demonstration
- Run option 1 with a sparse graph, then add edges to make it denser and show the decision changing.
- Run option 2 on 3–5 zones and explain INF for unreachable zones.
- Run option 3 with a budget where the fractional solution can split a project but the 0/1 solution cannot.
- Run options 4 and 5 with small inputs.
- Run option 6 and discuss actual measured results, noting that results depend on hardware and implementation.

## GitHub
Create a repository named `algorithm-2035-smart-cities`, upload the project files, and paste this README into the repository's README.md. Do not upload virtual environments or secret credentials.
