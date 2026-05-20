# Weekly Coding #9: Midnight Monster Delivery

## Summary

This program finds the cheapest delivery routes through a haunted city modeled as a weighted directed graph. Each location is a node; each road has a positive integer cost. `monster_delivery_costs` runs Dijkstra's algorithm from a start node and returns the minimum cost to every other location. `shortest_monster_delivery` does the same but also reconstructs the exact path using a previous-node map. The stretch function `best_next_monster_stop` runs costs once, then picks the cheapest reachable target from a candidate list.

## Approach

- **Graph representation** — adjacency dictionary: `{node: {neighbor: weight}}`. Any edge lookup is O(1) and the whole structure lives in memory with no extra conversion step.
- **Priority queue / frontier** — `heapq` min-heap of `(cost, node)` tuples. The node with the lowest currently-known cost is always popped first, guaranteeing we settle each node optimally in one visit.
- **Relaxation** — on each pop, every outgoing edge is checked. If `current_cost + weight < distances[neighbor]`, the record is updated and the neighbor is pushed onto the heap. Stale heap entries (where popped cost exceeds the settled distance) are skipped immediately.
- **Path reconstruction** — `shortest_monster_delivery` maintains a `previous` dict updated during relaxation. After the target is settled, the path is recovered by walking `previous` backwards from target to start and reversing the resulting list.

## Complexity

```text
Time complexity: O((V + E) log V), where V is the number of locations and E is the number of roads.

Space complexity: O(V + E) — O(V) for distances/previous/heap, plus O(V + E) for graph storage.
```

- `monster_delivery_costs`:
  - Time: O((V + E) log V)
  - Space: O(V + E)
  - Why: Each node is settled once. Each of the E edges may trigger a heap push at O(log E) ≈ O(log V). The heap holds at most O(E) entries total. Graph storage dominates space.

- `shortest_monster_delivery`:
  - Time: O((V + E) log V)
  - Space: O(V + E)
  - Why: Identical to `monster_delivery_costs`. Early-exit on target settlement helps in practice but doesn't change the worst-case bound. The added `previous` dict and path reconstruction are both O(V), which is dominated.

## Edge-Case Checklist

- [x] start equals target
- [x] target is unreachable
- [x] start node is missing
- [x] target node is missing
- [x] node has no outgoing edges
- [x] graph contains cycles
- [x] tied shortest paths
- [x] negative edge weight
- [x] zero edge weight
- [x] neighbor not listed as a graph node

## Tests I Added

- All seven individual node costs from `"Crypt Kitchen"` verified manually against the graph to confirm every distance is correct, not just the target.
- Cycle graph (`X→Y→Z→X`) — confirms the stale-entry skip prevents an infinite loop and still finds the correct path and cost.
- Isolated graph with an unreachable node — confirms the node stays at `inf` in the output dict.
- Tied-cost graph (two paths to `T`, both cost 3) — confirms the returned minimum is correct regardless of which route is taken.
- Zero-weight and missing-node edges — confirms `validate_haunted_map` raises `ValueError` before any traversal occurs.
- `best_next_monster_stop` tie-breaking — two targets at equal cost; confirms the one appearing first in the list is returned.
- `best_next_monster_stop` all-unreachable — every candidate is in an isolated component; confirms `("", inf)` is returned.

## Assistance & Sources

AI used? Y

If yes, what did it help with?

- Implementing all four functions (`validate_haunted_map`, `monster_delivery_costs`, `shortest_monster_delivery`, `best_next_monster_stop`)
- Writing and running the test suite (30 tests, all passing)
- Drafting this README writeup

Other sources used:

- Python docs — `heapq` module
- CLRS — Dijkstra's algorithm chaptera

## Notes for Instructor

The stretch function `best_next_monster_stop` is fully implemented. It runs `monster_delivery_costs` once (a single Dijkstraa pass) and then does a linear scan over the target list — no extra Dijkstra calls per target. Tie-breaking preserves first-occurrence order from the input list.

All 30 tests pass. The test runner is embedded at the bottom of the submitted `.py` file and can be run with `python week11_monster_delivery.py`.
