# AGENTS.md - Routing Module

## Purpose
This module implements a **food delivery routing system** using a **mixed-integer linear programming (MILP)** solver (`highs`) to assign orders to couriers, optimize pickup/delivery sequences, and minimize delays.

The core algorithm (`tryMatch` in `solver.ts`) batches orders, enforces time windows, and balances trade-offs between travel time and delivery delays.

---

## Key Commands
| Command          | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `npm run dev`    | Start Vite dev server (entry: `src/main.ts`).                              |
| `npm run build`  | Compile TypeScript and build for production.                                |
| `npm test`       | Run all tests with Vitest (see `src/solver.test.ts`).                       |
| `npm run bench`  | Run benchmark tests with Vitest.                                            |

---

## Toolchain
- **TypeScript**: ES2025, `moduleResolution: "bundler"`, no emit (`tsconfig.json`).
- **Vite**: Dev server and bundler.
- **Vitest**: Testing framework (supports mocks, benchmarks).
- **Highs**: MILP solver for routing optimization.

---

## Testing
### Prerequisites
- Mock `highs` and `parameters` in tests (see `solver.test.ts`).
- Reset game state before each test:
  ```ts
  [Order, Courier, Restaurant].forEach((cls) => cls.clear());
  Node.game = null as any;
  ```

### Key Test Cases
- **Single order**: Assigns a straight-line pickup+deliver route.
- **Batching**: Groups orders from the same restaurant (e.g., `maxBatch=2`).
- **Time windows**: Waits at restaurant for late orders.

---

## Entry Points
- **Application**: `src/main.ts` (initializes game and UI).
- **Core Logic**: `src/solver.ts` (`tryMatch` function).
- **Game Engine**: `src/game_engine.ts` (simulation state).

---

## Pain Points
1. **Solver Performance**: MILP is NP-hard; large batches or tight time windows may slow down solves.
2. **Mocking**: Tests require mocking `highs` and `parameters`.
3. **State Management**: Global game state (`Node.game`) can cause race conditions.
4. **Parameter Tuning**: Weights like `delayWeight` lack documentation for real-world tuning.
5. **Batch Constraints**: Hardcoded in tests (e.g., `maxBatch=2`) but may need dynamic adjustment.