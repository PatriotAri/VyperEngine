# Vyper Engine

Vyper Engine is a lightweight, ECS-based game engine written in Python.
It is designed with clear layering, deterministic simulation, and backend
agnosticism in mind.

The engine is intentionally minimal and educational, while still following
industry-standard ECS and engine architecture practices.

---

## Core Architecture

Vyper Engine is structured around the following layers:

- **Input** – Raw input is collected into an `InputState`
- **Intent** – Input is translated into intent components (e.g. movement)
- **Simulation (Fixed Step)** – Deterministic game logic runs at a fixed timestep
- **Camera** – Camera follows simulation state
- **Render** – Render systems receive a read-only view of the world

Render systems are explicitly prevented from mutating world state.

---

## ECS Model

- Entities are opaque IDs
- Components are pure data
- Systems are stateless logic
- World owns all entity/component storage

There are three system types:
- `UpdateSystem` – runs once per frame (input, AI)
- `FixedSystem` – runs at a fixed timestep (simulation)
- `RenderSystem` – runs after simulation with read-only access

---

## Running the Engine

### Windowed Mode (Normal Usage)

By default, the engine runs in windowed mode using the Pygame backend.

```python
engine.run()

## Headless / CI Usage

`main.py` is intended for interactive, windowed runs only.

For automated testing, CI, or tools such as Codex, use the
dedicated headless entrypoint:

```bash
python tools/run_headless.py
