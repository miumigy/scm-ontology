# P6-A — SCM OS Cockpit v0

## Purpose

P6-A is the first **Phase 6 (SCM OS Control Plane)** slice. It turns the
existing governed SCM OS runtime into something that behaves like **one SCM OS**
from an operator-facing surface: a minimal, read-only web control plane that
exposes governed **state / exceptions, decisions, simulation, execution, and
governance**.

P6-A composes the existing contracts — R5 decisions (S358–S362), demand/supply
gap (S327), governed simulation (S363), and operational workflow (S366, which
drives S354 audit and S355 command lifecycle) — and projects them into an
immutable, content-addressed `CockpitState` snapshot. It **never re-derives a
decision, never mutates Canonical Truth, and performs no external side effect**.

## Contract

`build_cockpit_state(fixture)` accepts an immutable `CockpitFixture` and returns
an immutable `CockpitState` with `contract_version: P6A.1` and
`is_operational_tool: true`.

A `CockpitFixture` binds the governed artifacts to compose:

- `context_id`, `recorded_at`, `actor_id`;
- `decisions`: a tuple of R5 decisions (Replenishment/Procurement/Production/Distribution);
- `gaps`: a tuple of `DemandSupplyGap` results (state / exceptions);
- `simulation`: an optional `GovernedSimulationResult`;
- `workflow`: an optional `OperationalWorkflowResult`.

`CockpitState` exposes five domain projections and an `overview` aggregate:

| domain | source |
|---|---|
| `decisions` | R5 decision summaries + whether a governed result exists |
| `exceptions` | demand/supply gap results |
| `simulation` | governed simulation step records |
| `execution` | governed dry-run results and workflow command states |
| `governance` | workflow audit ids and command lifecycle states |

## Deterministic reference path

`run_cockpit_reference_path()` composes the existing governed applications end
to end (replenishment + production decisions, a demand/supply gap, a governed
simulation, and an operational workflow) and returns a `CockpitState` for every
domain. This is the **deterministic reference path first**: a testable SCM OS
surface before any external infrastructure is introduced.

## HTTP adapter

`make_cockpit_handler(state)` returns a stdlib `BaseHTTPRequestHandler` serving
read-only routes:

- `/` — minimal HTML overview;
- `/api/state` — full snapshot JSON;
- `/api/decisions`, `/api/exceptions`, `/api/simulation`, `/api/execution`,
  `/api/governance` — per-domain JSON;
- any other route — `404`; any non-GET (POST/PUT/DELETE) — `405`.

`create_cockpit_server(state, *, host, port)` builds a `ThreadingHTTPServer`
wrapper; `CockpitServerThread` runs it on a background thread. No stdlib
dependency is required beyond the Python standard library.

## Fail-closed behavior

The cockpit MUST reject:

- a `CockpitFixture` with blank `context_id` / `recorded_at` / `actor_id`;
- a `decisions` entry that is not one of the signed R5 decisions;
- a `gaps`/`simulation`/`workflow` entry of the wrong type;
- `build_cockpit_state` on a non-`CockpitFixture`;
- an unknown `domain_json` domain;
- `make_cockpit_handler`/`create_cockpit_server` on a non-`CockpitState`.

## Determinism & provenance

- The same fixture and times produce an identical snapshot (`to_json`) and a
  content-addressed `snapshot_id`.
- The cockpit is a read-only projection: it writes nothing, mutates nothing, and
  HTTP is GET-only.

## Non-goals

P6-A does not:

- re-derive or re-compute any decision/simulation it projects (composition only);
- mutate Canonical Truth or external systems;
- write to any store (in-memory snapshot only);
- introduce new canonical Entity, Relationship, or derived-state types;
- add a web framework dependency (stdlib only).
