# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment

Python 3.13 with pygame, managed via a local venv:

```bash
source venv/bin/activate
```

## Running the game

```bash
venv/bin/python pong.py
```

The game requires a display (X11/Wayland). It cannot run headlessly without mocking pygame's display subsystem.

## Testing game logic headlessly

Pygame display and event calls must be stubbed out before importing game logic. Use `unittest.mock` to patch `pygame.display.set_mode`, `pygame.display.set_caption`, `pygame.font.SysFont`, and `pygame.time.Clock` at the module level, then instantiate `Ball` and `Paddle` directly and test their methods (`update`, `move`, `out_of_bounds`, `reset`).

Run a test script with:

```bash
venv/bin/python test_pong.py
```

## Architecture

Everything lives in `pong.py` — no modules, no config files. The structure:

- **`Paddle`** — wraps a `pygame.Rect`, reads live key state in `move()` each frame
- **`Ball`** — moves by `(vx, vy)` each frame; bounces off top/bottom walls, reverses `vx` on paddle collision, reports scorer via `out_of_bounds()`
- **`main()`** — game loop: tick → events → move paddles → update ball → check score → draw

Global constants (`WIDTH`, `HEIGHT`, `PADDLE_SPEED`, `BALL_SPEED`) control all physics. Ball always resets to center moving at `(+BALL_SPEED, +BALL_SPEED)` — direction is not randomized on reset.
