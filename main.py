"""
Algorithm 2035: Adaptive Algorithm Selection Framework for Smart Cities
Educational DAA project. Python 3.10+; standard library only.

Run: python main.py
Tests: python -m unittest discover -s tests -v
"""
from __future__ import annotations
from dataclasses import dataclass
from time import perf_counter
from typing import Any
import math
import random
from data_structures import BTree, RedBlackTree


@dataclass
class Decision:
    problem: str
    algorithm: str
    reason: str
    time_complexity: str
    space_complexity: str
    alternative: str


def graph_density(n: int, edges: list[tuple[int, int, float]]) -> float:
    possible = n * (n - 1) / 2
    return len(edges) / possible if possible else 0.0


def choose_mst(n: int, edges: list[tuple[int, int, float]]) -> Decision:
    density = graph_density(n, edges)
    # A transparent heuristic, not a universal claim that one algorithm is always faster.
    if density < 0.35:
        return Decision("Minimum-cost city network", "Kruskal",
                        f"Sparse graph (density={density:.2f}); sorting the available edges is a natural fit.",
                        "O(E log E)", "O(V + E)",
                        "Prim; benchmark both because representation and implementation affect performance.")
    return Decision("Minimum-cost city network", "Prim",
                    f"Relatively dense graph (density={density:.2f}); Prim is selected for this run.",
                    "O(V^2) with adjacency matrix; O(E log V) with a binary heap",
                    "O(V^2) with matrix; O(V + E) with adjacency list",
                    "Kruskal; benchmark both rather than assuming this choice is always faster.")


def kruskal(n: int, edges: list[tuple[int, int, float]]) -> tuple[float, list[tuple[int, int, float]]]:
    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> bool:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            parent[ra] = rb
        elif rank[ra] > rank[rb]:
            parent[rb] = ra
        else:
            parent[rb] = ra
            rank[ra] += 1
        return True

    chosen, total = [], 0.0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if union(u, v):
            chosen.append((u, v, w))
            total += w
            if len(chosen) == n - 1:
                break
    if n > 0 and len(chosen) != n - 1:
        raise ValueError("The graph is disconnected; no spanning tree exists.")
    return total, chosen


def prim(n: int, edges: list[tuple[int, int, float]]) -> tuple[float, list[tuple[int, int, float]]]:
    if n == 0:
        return 0.0, []
    # Simple O(V^2 + E) implementation; suitable for small classroom examples.
    adj = [[] for _ in range(n)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    used = [False] * n
    best = [math.inf] * n
    parent: list[tuple[int, float] | None] = [None] * n
    best[0] = 0
    total, chosen = 0.0, []
    for _ in range(n):
        candidates = [i for i in range(n) if not used[i]]
        if not candidates:
            break
        u = min(candidates, key=lambda x: best[x])
        if best[u] == math.inf:
            raise ValueError("The graph is disconnected; no spanning tree exists.")
        used[u] = True
        if parent[u] is not None:
            p, w = parent[u]
            chosen.append((p, u, w))
            total += w
        for v, w in adj[u]:
            if not used[v] and w < best[v]:
                best[v] = w
                parent[v] = (u, w)
    return total, chosen


def floyd_warshall(n: int, edges: list[tuple[int, int, float]]) -> list[list[float]]:
    dist = [[math.inf] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    for u, v, w in edges:
        dist[u][v] = min(dist[u][v], w)
        dist[v][u] = min(dist[v][u], w)  # city travel links are modelled as undirected
    for k in range(n):
        for i in range(n):
            if dist[i][k] == math.inf:
                continue
            for j in range(n):
                candidate = dist[i][k] + dist[k][j]
                if candidate < dist[i][j]:
                    dist[i][j] = candidate
    return dist


def fractional_knapsack(items: list[tuple[str, float, float]], capacity: float) -> tuple[float, list[tuple[str, float]]]:
    """Items are (name, benefit, cost); divisible items may be partially selected."""
    if capacity < 0 or any(cost < 0 or benefit < 0 for _, benefit, cost in items):
        raise ValueError("Capacity, benefits and costs must be non-negative.")
    if any(cost == 0 and benefit > 0 for _, benefit, cost in items):
        # Include all zero-cost positive-benefit items fully.
        zero = [(name, 1.0) for name, benefit, cost in items if cost == 0 and benefit > 0]
    else:
        zero = []
    ordered = sorted((x for x in items if x[2] > 0), key=lambda x: x[1] / x[2], reverse=True)
    selected = list(zero)
    total = sum(b for _, b, c in items if c == 0)
    remaining = capacity
    for name, benefit, cost in ordered:
        if remaining <= 0:
            break
        fraction = min(1.0, remaining / cost)
        selected.append((name, fraction))
        total += benefit * fraction
        remaining -= cost * fraction
    return total, selected


def knapsack_01(items: list[tuple[str, int, int]], capacity: int) -> tuple[int, list[str]]:
    """Items are (name, benefit, integer_cost); each item is indivisible."""
    if capacity < 0 or any(cost < 0 or benefit < 0 for _, benefit, cost in items):
        raise ValueError("Capacity, benefits and costs must be non-negative.")
    dp = [0] * (capacity + 1)
    take = [[False] * (capacity + 1) for _ in items]
    for i, (_, benefit, cost) in enumerate(items):
        for cap in range(capacity, cost - 1, -1):
            candidate = dp[cap - cost] + benefit
            if candidate > dp[cap]:
                dp[cap] = candidate
                take[i][cap] = True
    selected = []
    cap = capacity
    for i in range(len(items) - 1, -1, -1):
        if take[i][cap]:
            name, _, cost = items[i]
            selected.append(name)
            cap -= cost
    selected.reverse()
    return dp[capacity], selected


def n_queens(n: int) -> list[int] | None:
    """Return one solution where solution[row] = column, or None if no solution."""
    if n < 1:
        raise ValueError("N must be at least 1.")
    cols, diag1, diag2 = set(), set(), set()
    solution = [-1] * n

    def backtrack(row: int) -> bool:
        if row == n:
            return True
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            solution[row] = col
            cols.add(col); diag1.add(row-col); diag2.add(row+col)
            if backtrack(row + 1):
                return True
            cols.remove(col); diag1.remove(row-col); diag2.remove(row+col)
            solution[row] = -1
        return False

    return solution[:] if backtrack(0) else None


def tsp_backtracking(matrix: list[list[float]]) -> tuple[float, list[int]]:
    """Exact TSP for small complete weighted graphs; start/end at vertex 0."""
    n = len(matrix)
    if n < 2 or any(len(row) != n for row in matrix):
        raise ValueError("TSP requires a square cost matrix with at least 2 cities.")
    best_cost, best_path = math.inf, []
    path = [0]
    visited = {0}

    def search(cost: float) -> None:
        nonlocal best_cost, best_path
        if len(path) == n:
            back = matrix[path[-1]][0]
            total = cost + back
            if total < best_cost:
                best_cost, best_path = total, path[:] + [0]
            return
        # Prune only when current cost already cannot beat the best (non-negative edge costs assumed).
        if cost >= best_cost:
            return
        last = path[-1]
        for nxt in range(1, n):
            if nxt not in visited:
                visited.add(nxt); path.append(nxt)
                search(cost + matrix[last][nxt])
                path.pop(); visited.remove(nxt)

    search(0.0)
    return best_cost, best_path


def benchmark_mst() -> list[dict[str, Any]]:
    rows = []
    rng = random.Random(2035)
    for n in (20, 50, 100):
        # Connected backbone plus random edges; graph is reproducible.
        edges = [(i, i + 1, rng.randint(1, 30)) for i in range(n - 1)]
        existing = {(u, v) for u, v, _ in edges}
        target = min(n * (n - 1) // 2, (n - 1) + n * 2)
        while len(edges) < target:
            u, v = sorted(rng.sample(range(n), 2))
            if (u, v) not in existing:
                existing.add((u, v))
                edges.append((u, v, rng.randint(1, 30)))
        for name, fn in (("Prim", prim), ("Kruskal", kruskal)):
            start = perf_counter()
            total, chosen = fn(n, edges)
            elapsed = (perf_counter() - start) * 1000
            rows.append({"vertices": n, "edges": len(edges), "algorithm": name,
                         "total_cost": total, "runtime_ms": round(elapsed, 3),
                         "edges_selected": len(chosen)})
    return rows


def demo() -> None:
    print("\\n=== Algorithm 2035: Adaptive Smart City Framework ===")
    print("1. Infrastructure network (Prim vs Kruskal)")
    print("2. All-pairs city connectivity (Floyd-Warshall)")
    print("3. Budgeted project selection (Fractional vs 0/1 Knapsack)")
    print("4. Sensor placement (N-Queens backtracking)")
    print("5. Service inspection tour (TSP backtracking; small instances)")
    print("6. Run MST performance experiment")
    print("7. Compare B-Tree vs Red-Black Tree")
    print("0. Exit")
    while True:
        choice = input("\\nChoose a module: ").strip()
        try:
            if choice == "1":
                n = int(input("Number of city sites: "))
                m = int(input("Number of connections: "))
                edges = []
                print("Enter each connection as: site1 site2 cost (site IDs start at 0)")
                for _ in range(m):
                    u, v, w = input("> ").split()
                    edges.append((int(u), int(v), float(w)))
                if n < 1 or any(u < 0 or v < 0 or u >= n or v >= n or u == v for u,v,_ in edges):
                    raise ValueError("Invalid vertex or self-loop.")
                decision = choose_mst(n, edges)
                print(f"Decision: {decision.algorithm} — {decision.reason}")
                print(f"Alternative: {decision.alternative}")
                for name, fn in (("Prim", prim), ("Kruskal", kruskal)):
                    start = perf_counter()
                    total, selected = fn(n, edges)
                    elapsed = (perf_counter() - start) * 1000
                    print(f"{name}: cost={total:g}, edges={selected}, runtime={elapsed:.3f} ms")
                print(f"Selected by framework: {decision.algorithm}")
                print(f"Complexity: {decision.time_complexity}; space: {decision.space_complexity}")
            elif choice == "2":
                n = int(input("Number of city zones: "))
                m = int(input("Number of connections: "))
                edges = []
                print("Enter each connection as: zone1 zone2 cost (zone IDs start at 0)")
                for _ in range(m):
                    u, v, w = input("> ").split()
                    edges.append((int(u), int(v), float(w)))
                dist = floyd_warshall(n, edges)
                print("Shortest-path cost matrix (INF means unreachable):")
                for row in dist:
                    print(" ".join("INF" if x == math.inf else f"{x:g}" for x in row))
                print("Time: O(V^3); space: O(V^2).")
            elif choice == "3":
                capacity = int(input("Available city-project budget (integer): "))
                count = int(input("Number of projects: "))
                items = []
                for _ in range(count):
                    name, benefit, cost = input("Enter project_name benefit cost: ").split()
                    items.append((name, int(benefit), int(cost)))
                frac, frac_sel = fractional_knapsack([(a,float(b),float(c)) for a,b,c in items], capacity)
                whole, whole_sel = knapsack_01(items, capacity)
                print(f"Fractional: benefit={frac:.2f}; selections (project, fraction)={frac_sel}")
                print(f"0/1: benefit={whole}; selected whole projects={whole_sel}")
                print("Fractional time: O(n log n); 0/1 DP time: O(nW), space: O(nW) here for reconstruction.")
                print("Note: 0/1 Knapsack DP is pseudo-polynomial in the numeric capacity W.")
            elif choice == "4":
                n = int(input("Board size N: "))
                sol = n_queens(n)
                if sol is None:
                    print(f"No solution exists for N={n}.")
                else:
                    print("One placement (row -> column):", sol)
                    for r in range(n):
                        print(" ".join("Q" if sol[r] == c else "." for c in range(n)))
                print("Backtracking has exponential worst-case search; this returns one solution.")
            elif choice == "5":
                n = int(input("Number of cities (keep small, e.g. 4–10): "))
                matrix = []
                print("Enter each row of the complete cost matrix, space-separated.")
                for _ in range(n):
                    row = list(map(float, input("> ").split()))
                    if len(row) != n:
                        raise ValueError("Each row must contain exactly n costs.")
                    matrix.append(row)
                cost, path = tsp_backtracking(matrix)
                print("Best tour:", path, "cost:", cost)
                print("Optimization TSP is NP-Hard; exact backtracking has factorial worst-case time.")
            elif choice == "6":
                print("MST experiment (your runtime will vary by computer):")
                print(f"{'V':>5} {'E':>6} {'Algorithm':>10} {'Cost':>8} {'Runtime(ms)':>13}")
                for row in benchmark_mst():
                    print(f"{row['vertices']:>5} {row['edges']:>6} {row['algorithm']:>10} "
                          f"{row['total_cost']:>8g} {row['runtime_ms']:>13.3f}")
                print("Use measured values as evidence; do not claim one algorithm always wins.")
            elif choice == "7":
                count = int(input("Number of city records to insert (e.g. 1000): "))
                if count < 1:
                    raise ValueError("Record count must be positive.")
                rng = random.Random(2035)
                values = rng.sample(range(count * 10), count)
                btree, rbtree = BTree(degree=3), RedBlackTree()
                start = perf_counter()
                for value in values:
                    btree.insert(value)
                b_insert = (perf_counter() - start) * 1000
                start = perf_counter()
                for value in values:
                    rbtree.insert(value)
                rb_insert = (perf_counter() - start) * 1000
                queries = values[::max(1, count // 100)]
                start = perf_counter()
                b_found = sum(btree.search(q) for q in queries)
                b_search = (perf_counter() - start) * 1000
                start = perf_counter()
                rb_found = sum(rbtree.search(q) for q in queries)
                rb_search = (perf_counter() - start) * 1000
                print(f"Records inserted: {count}; search queries: {len(queries)}")
                print(f"B-Tree: insert={b_insert:.3f} ms, search={b_search:.3f} ms, found={b_found}")
                print(f"Red-Black Tree: insert={rb_insert:.3f} ms, search={rb_search:.3f} ms, found={rb_found}")
                print("Both balanced structures support O(log n) search and insertion in the worst case.")
                print("B-Tree has multi-key nodes and is useful for block/disk-oriented indexes;")
                print("Red-Black Tree is a binary balanced tree commonly suited to in-memory ordered maps.")
                print("Runtime is implementation- and machine-dependent; compare repeated trials for stronger evidence.")
            elif choice == "0":
                print("Good luck with your submission!")
                break
            else:
                print("Please choose one of the listed options.")
        except (ValueError, IndexError) as exc:
            print("Input error:", exc)


if __name__ == "__main__":
    demo()
