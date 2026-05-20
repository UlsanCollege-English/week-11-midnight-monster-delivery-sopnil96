"""Week 11: Midnight Monster Delivery.
Implement Dijkstra's algorithm using a heap-based priority queue.
Rules:
- Use Python 3.11+.
- Use the standard library only.
- Use heapq for the priority queue.
- Edge weights must be positive.
"""
import heapq
from math import inf

HAUNTED_CITY = {
    "Crypt Kitchen": {
        "Fog Alley": 2,
        "Bone Bridge": 5,
    },
    "Fog Alley": {
        "Moon Bridge": 1,
        "Goblin Market": 6,
    },
    "Bone Bridge": {
        "Goblin Market": 2,
    },
    "Moon Bridge": {
        "Werewolf Den": 5,
        "Goblin Market": 3,
    },
    "Goblin Market": {
        "Vampire Tower": 5,
    },
    "Werewolf Den": {
        "Vampire Tower": 2,
    },
    "Vampire Tower": {},
}


def validate_haunted_map(graph: dict[str, dict[str, int]]) -> None:
    """Raise ValueError if the haunted map is invalid.

    A valid haunted map:
    - is a dictionary
    - each node maps to a dictionary of neighbors
    - every neighbor is also a node in the graph
    - every edge weight is positive

    Args:
        graph: Weighted graph represented as an adjacency dictionary.

    Raises:
        ValueError: If the graph is invalid.
    """
    if not isinstance(graph, dict):
        raise ValueError("Graph must be a dictionary.")

    for node, neighbors in graph.items():
        if not isinstance(neighbors, dict):
            raise ValueError(
                f"Node '{node}' must map to a dictionary of neighbors."
            )
        for neighbor, weight in neighbors.items():
            if neighbor not in graph:
                raise ValueError(
                    f"Neighbor '{neighbor}' of '{node}' is not a node in the graph."
                )
            if not isinstance(weight, (int, float)) or weight <= 0:
                raise ValueError(
                    f"Edge weight from '{node}' to '{neighbor}' must be a positive number, got {weight!r}."
                )


def monster_delivery_costs(
    graph: dict[str, dict[str, int]],
    start: str,
) -> dict[str, float]:
    """Return the cheapest delivery cost from start to every location.

    Use Dijkstra's algorithm with heapq.

    Args:
        graph: Weighted graph represented as an adjacency dictionary.
        start: Starting location.

    Returns:
        Dictionary mapping each location to its cheapest known cost.
        Unreachable locations should stay as math.inf.

    Raises:
        ValueError: If the graph is invalid or start is missing.
    """
    validate_haunted_map(graph)

    if start not in graph:
        raise ValueError(f"Start node '{start}' is not in the graph.")

    # Initialize all distances to infinity; start costs 0.
    distances: dict[str, float] = {node: inf for node in graph}
    distances[start] = 0

    # Min-heap: (cost, node)
    frontier: list[tuple[float, str]] = [(0, start)]

    while frontier:
        current_cost, current_node = heapq.heappop(frontier)

        # Skip stale entries (we already found a cheaper path).
        if current_cost > distances[current_node]:
            continue

        # Relaxation: update neighbors if a cheaper path is found.
        for neighbor, weight in graph[current_node].items():
            new_cost = current_cost + weight
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                heapq.heappush(frontier, (new_cost, neighbor))

    return distances


def shortest_monster_delivery(
    graph: dict[str, dict[str, int]],
    start: str,
    target: str,
) -> tuple[float, list[str]]:
    """Return the cheapest cost and path from start to target.

    Use Dijkstra's algorithm with heapq and reconstruct the path using
    a previous-node map.

    Args:
        graph: Weighted graph represented as an adjacency dictionary.
        start: Starting location.
        target: Destination location.

    Returns:
        (cost, path), where path is in start-to-target order.
        If start or target is missing, return (math.inf, []).
        If target is unreachable, return (math.inf, []).
        If start equals target, return (0, [start]).
    """
    validate_haunted_map(graph)

    # Missing node guard.
    if start not in graph or target not in graph:
        return (inf, [])

    # Trivial case.
    if start == target:
        return (0, [start])

    # Initialize distances and previous-node map for path reconstruction.
    distances: dict[str, float] = {node: inf for node in graph}
    distances[start] = 0
    previous: dict[str, str | None] = {node: None for node in graph}

    # Min-heap: (cost, node)
    frontier: list[tuple[float, str]] = [(0, start)]

    while frontier:
        current_cost, current_node = heapq.heappop(frontier)

        # Early exit once we've settled the target.
        if current_node == target:
            break

        # Skip stale entries.
        if current_cost > distances[current_node]:
            continue

        # Relaxation.
        for neighbor, weight in graph[current_node].items():
            new_cost = current_cost + weight
            if new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                previous[neighbor] = current_node
                heapq.heappush(frontier, (new_cost, neighbor))

    # Target unreachable.
    if distances[target] == inf:
        return (inf, [])

    # Reconstruct path by walking backwards through previous-node map.
    path: list[str] = []
    node: str | None = target
    while node is not None:
        path.append(node)
        node = previous[node]
    path.reverse()

    return (distances[target], path)


def best_next_monster_stop(
    graph: dict[str, dict[str, int]],
    start: str,
    targets: list[str],
) -> tuple[str, float]:
    """Return the reachable target with the cheapest delivery cost.

    Stretch challenge.

    Rules:
    - Ignore unreachable targets.
    - If no target is reachable, return ("", math.inf).
    - If there is a tie, return the target that appears first in targets.

    Args:
        graph: Weighted graph represented as an adjacency dictionary.
        start: Starting location.
        targets: Possible destination locations.

    Returns:
        A tuple of (target, cost).
    """
    # Run Dijkstra once from start, then pick the cheapest reachable target.
    if start not in graph:
        return ("", inf)

    all_costs = monster_delivery_costs(graph, start)

    best_target = ""
    best_cost: float = inf

    for t in targets:
        cost = all_costs.get(t, inf)
        # Keep first occurrence on ties (iterate in order, strict less-than).
        if cost < best_cost:
            best_cost = cost
            best_target = t

    return (best_target, best_cost)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def run_tests() -> None:
    """Run all tests, printing PASS / FAIL for each."""
    passed = 0
    failed = 0

    def check(label: str, got, expected) -> None:
        nonlocal passed, failed
        if got == expected:
            print(f"  PASS  {label}")
            passed += 1
        else:
            print(f"  FAIL  {label}")
            print(f"        expected: {expected!r}")
            print(f"        got:      {got!r}")
            failed += 1

    # ------------------------------------------------------------------
    # validate_haunted_map
    # ------------------------------------------------------------------
    print("\n--- validate_haunted_map ---")

    try:
        validate_haunted_map(HAUNTED_CITY)
        check("valid graph passes", True, True)
    except ValueError:
        check("valid graph passes", False, True)

    try:
        validate_haunted_map({"A": {"B": 1}})          # B not in graph
        check("missing neighbor raises ValueError", False, True)
    except ValueError:
        check("missing neighbor raises ValueError", True, True)

    try:
        validate_haunted_map({"A": {"A": -1}})          # negative weight
        check("negative weight raises ValueError", False, True)
    except ValueError:
        check("negative weight raises ValueError", True, True)

    try:
        validate_haunted_map({"A": {"A": 0}})           # zero weight
        check("zero weight raises ValueError", False, True)
    except ValueError:
        check("zero weight raises ValueError", True, True)

    try:
        validate_haunted_map("not a dict")              # type error
        check("non-dict raises ValueError", False, True)
    except ValueError:
        check("non-dict raises ValueError", True, True)

    # ------------------------------------------------------------------
    # monster_delivery_costs
    # ------------------------------------------------------------------
    print("\n--- monster_delivery_costs ---")

    costs = monster_delivery_costs(HAUNTED_CITY, "Crypt Kitchen")
    check("Crypt Kitchen → Crypt Kitchen", costs["Crypt Kitchen"], 0)
    check("Crypt Kitchen → Fog Alley", costs["Fog Alley"], 2)
    check("Crypt Kitchen → Moon Bridge", costs["Moon Bridge"], 3)
    check("Crypt Kitchen → Bone Bridge", costs["Bone Bridge"], 5)
    check("Crypt Kitchen → Goblin Market", costs["Goblin Market"], 6)
    check("Crypt Kitchen → Werewolf Den", costs["Werewolf Den"], 8)
    check("Crypt Kitchen → Vampire Tower", costs["Vampire Tower"], 10)

    # Unreachable node
    isolated = {
        "A": {"B": 1},
        "B": {},
        "C": {},
    }
    c2 = monster_delivery_costs(isolated, "A")
    check("unreachable node stays inf", c2["C"], inf)

    # Missing start raises
    try:
        monster_delivery_costs(HAUNTED_CITY, "Nowhere")
        check("missing start raises ValueError", False, True)
    except ValueError:
        check("missing start raises ValueError", True, True)

    # ------------------------------------------------------------------
    # shortest_monster_delivery
    # ------------------------------------------------------------------
    print("\n--- shortest_monster_delivery ---")

    cost, path = shortest_monster_delivery(
        HAUNTED_CITY, "Crypt Kitchen", "Vampire Tower"
    )
    check("CK→VT cost", cost, 10)
    check(
        "CK→VT path",
        path,
        ["Crypt Kitchen", "Fog Alley", "Moon Bridge", "Werewolf Den", "Vampire Tower"],
    )

    cost, path = shortest_monster_delivery(
        HAUNTED_CITY, "Crypt Kitchen", "Crypt Kitchen"
    )
    check("start == target cost", cost, 0)
    check("start == target path", path, ["Crypt Kitchen"])

    cost, path = shortest_monster_delivery(
        HAUNTED_CITY, "Crypt Kitchen", "Ghost Island"
    )
    check("missing target → inf", cost, inf)
    check("missing target → []", path, [])

    cost, path = shortest_monster_delivery(isolated, "A", "C")
    check("unreachable target → inf", cost, inf)
    check("unreachable target → []", path, [])

    # Cycle graph — should still terminate
    cycle = {
        "X": {"Y": 3},
        "Y": {"Z": 2},
        "Z": {"X": 1},
    }
    cost, path = shortest_monster_delivery(cycle, "X", "Z")
    check("cycle graph cost X→Z", cost, 5)
    check("cycle graph path X→Z", path, ["X", "Y", "Z"])

    # Tied path — Goblin Market reachable via two routes with same cost
    tied = {
        "S": {"A": 2, "B": 1},
        "A": {"T": 1},
        "B": {"T": 2},
        "T": {},
    }
    cost, _ = shortest_monster_delivery(tied, "S", "T")
    check("tied shortest paths cost", cost, 3)

    # Zero-weight edges should be rejected by validate
    zero_w = {"A": {"B": 0}, "B": {}}
    try:
        shortest_monster_delivery(zero_w, "A", "B")
        check("zero weight raises ValueError", False, True)
    except ValueError:
        check("zero weight raises ValueError", True, True)

    # ------------------------------------------------------------------
    # best_next_monster_stop (stretch)
    # ------------------------------------------------------------------
    print("\n--- best_next_monster_stop ---")

    best, c = best_next_monster_stop(
        HAUNTED_CITY,
        "Crypt Kitchen",
        ["Goblin Market", "Werewolf Den", "Vampire Tower"],
    )
    check("best stop target", best, "Goblin Market")
    check("best stop cost", c, 6)

    best, c = best_next_monster_stop(isolated, "A", ["C"])
    check("all targets unreachable → ('', inf)", (best, c), ("", inf))

    # Tie: first in list wins
    tied2 = {
        "S": {"A": 5, "B": 5},
        "A": {},
        "B": {},
    }
    best, c = best_next_monster_stop(tied2, "S", ["B", "A"])
    check("tie → first in list wins", best, "B")

    # ------------------------------------------------------------------
    print(f"\nResults: {passed} passed, {failed} failed.\n")


if __name__ == "__main__":
    run_tests()