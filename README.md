# Pong

A classic two-player Pong game built with Python and pygame.

![Python](https://img.shields.io/badge/python-3.13-blue) ![pygame](https://img.shields.io/badge/pygame-latest-green)

## Gameplay

Two players compete on the same keyboard. First to miss the ball concedes a point.

| Player | Move Up | Move Down |
|--------|---------|-----------|
| Left   | `W`     | `S`       |
| Right  | `↑`     | `↓`       |

Press `Esc` or close the window to quit.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install pygame
```

## Run

```bash
python pong.py
```

## How it works

The game is a single file (`pong.py`) with three components:

- **`Paddle`** — reads live key state each frame and moves with hard boundary clamping so paddles never escape the screen.
- **`Ball`** — moves at a fixed velocity per frame. Bounces off top/bottom walls using sign-forced reflection (`abs(vy)`) and position clamping to prevent wall oscillation. Paddle collisions use a direction guard to prevent tunnel-through and clamp the ball's position to end the overlap immediately.
- **`main()`** — 60 FPS game loop: process events → move paddles → update ball → check score → draw.

The serve direction alternates after each point so the ball is always sent toward the player who just scored.
