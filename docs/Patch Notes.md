Vyper Engine Patch Notes
========================


Alpha v0.1.0
============

-Renamed time.py to engtime.py to prevent import errors.

-Implemented interpolated delta time logic for smoothed graphics.

-Added __slots__ for ECS performance optimization.


Alpha v0.1.1
============

-Added reset for accumulator to prevent spiral of death (recursive lag leading to crash).

-Added fix_update function to check if resetting the accumulator is necessary.

-Added get_alpha function to apply interpolation for smoothed graphics in renderer.


Alpha v0.2.0
============

-Complete restructure of directories.

-Renamed engtime.py to engine_time.py.


Alpha v0.2.1
============

-Added serialization.py to utils/ for save/load engine.

-Added game/save/ directory.

-Populated save/ directory with save_manager.py, save_schema.py, and migrations.py.


Alpha v0.3.1
============

-Updated events.py, API for mouse and keyboard events now implemented.

-Prevented stuck keys while alt-tabbing, added safe input pause to events.py.

-Added engine/ui/ directory and subsequent necessary files.

-Added game/ui/ and subsequent files.

-Added game/ui/widgets/ directory.

-Added pygame_ui_renderer.py and opengl_ui_renderer.py to engine/rendering/.


Alpha v0.3.2
============

-Renamed engine/core/engine_time.py to clock.py. Final change.

-Renamed engine/core/engine_loop.py to loop.py. Final change.


Alpha v1.0.0
============

-First major Alpha update.

-Engine core in working state.

-Minimal pygame back end written to wire all systems.

-Pruned MANY unnecessary directories.

-Updated requirements.txt.


Alpha v1.0.1
============

-Added ecs/ directory and subsequent files to engine/.

-Built and verified ECS core.

-Added ECS systems skeleton.

-Wired ECS to engine.

-Updated empty functions in core/engine.py.

-Confirmed ticks update properly, alpha remains between 0-1.

-Final minor patches before ECS design.


Alpha v1.1.0
============

-Updated ecs/world.py to act as API between world and engine.

-Solved namespace collision and refactored imports.

-Added input abstractions.


Alpha v1.1.1
============

-Implemented basic movement system and wired to main.

-Implemented basic movement bootstrap.

-Implemented basic Transform system and wired to main.

(Final basic framework update)


Alpha v2.0.0
============

-Fixed WASD input.

-Implemented rendering.


Alpha v2.1.0
============

-Implemented first gen debugging tools.

-Press 'F3' while in game to display debug screen.

-Implemented basic camera system.

-Adjusted native window size to 960x540.

-Implemented renderable.py in components/ allowing selective rendering.

-Wired renderable.py to camera_render_system.py


Alpha v2.1.1
============

-Implemented camera movement.

-Fixed redundant rendering causing duplicate player character.


Alpha v2.1.2
============

-Added camera position to debug screen.

-Changed the way information is displayed in the debug screen.


Alpha v2.2.0
============

-Removed camera_render_system.

-Reimplementing camera_render_system into basic_render_system.

-Added camera smoothing.

-Made final improvements on basic camera system.


Alpha v2.2.1
============

-Centered camera in basic_render_system.py


Alpha v2.3.0
============

-Resolved major conflic between Renderable class in renderable.py and sprite.py.

-Fixed corrupted ports/window.py file.

-Resolved conflicting render systems in basic_render_system.py and render_system.py.

-Renamed render_system.py to world_render_system.py.

-Fixed input applying to all entities. Input now applies only things marked with PlayerController.

-Fixed camera smoothing to work with delta time.

-Enforced RenderSystem contract. RenderSystem now only reads information, no longer writes it.

-Enforced WorldView contract. WorldView now only reads information, no longer writes it.

-Fixed entities_with in the World class, no longer calls multiple termporary entities improving optimization drastically.

-Removed dead class System from system_base.py.

-Turned CameraTarget into a dataclass (cls) so it can me called manually instead of trying to follow all entities.

-Fixed debug_render_system, now prints all entity transforms.

-Added a note to ports/renderer/draw_sprite.py to reserve for later use over temporary rect.


Alpha v2.3.1
============

-Implemented headless backend architecture.

-Added tools/ directory in root. This is where engine arhcitecture that doesnt live in the engine itself stays.

-Updated README.md

-Added null_renderer.py to ports/ for headless backend.


Alpha v2.3.2
============

-Added components/velocity.py. Proper movement pipeline. This marks the start of the physics engine.

-Added components/collider.py. Implements collision physics.

-Added systems/collision_system.py.

-Added components/rigidbody.py to differentiate between static and dynamic entities like walls, objects, map boundaries, etc.

-Fixed wall and added block test entity bootstraps to main.py. Will be removed in the future.

-Final patch before refactor to fully integrate physics.


Alpha v2.4.0
============

-Final major phase (phase 4) of basic physics engine implemented.


Alpha v2.4.1
============

-Normalized diagonal speed in ecs/systems/collision_system.py.

-Fixed jittering, entity edges overlapping, or seeing occasional gaps between entities when continuously colliding.

Alpha v2.5.0
=============

-Turned project into a package.

-Added split startup for local and headless executions.

-Added setup.cfg to root.

-Added setup.py to root.

-Added runtime/mode.py to vyper_engine/.


Alpha v2.5.1 (Current)
============

-Deleted vyper_engine/run.py.

-Added vyper_engine/game.py.

-Simplified windowed branch in main.py.

-Proved ECS -> render pipeline works, renders entity.
