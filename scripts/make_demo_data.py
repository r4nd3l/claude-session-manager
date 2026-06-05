#!/usr/bin/env python3
"""Generate fake Claude Code sessions for screenshots and demos.

Usage:
    python3 scripts/make_demo_data.py
    XDG_CONFIG_HOME=/tmp/csm-demo/config CSM_PROJECTS_DIR=/tmp/csm-demo/projects \\
        python3 -m claude_session_manager
"""

from __future__ import annotations

import json
import os
import time
import uuid
from pathlib import Path

ROOT = Path("/tmp/csm-demo")

# (project, preview prompt, age in seconds, custom name or None, favorite)
SESSIONS = [
    ("portfolio-website", "Redesign the hero section with a dark theme and subtle animations",
     300, "Homepage redesign", True),
    ("portfolio-website", "Fix the contact form validation, emails with a plus sign are rejected",
     7200, None, False),
    ("todo-api", "Add JWT authentication to the API with refresh tokens", 5400, "JWT auth", True),
    ("todo-api", "Write integration tests for the todo endpoints", 86400, None, False),
    ("dotfiles", "Migrate my neovim configuration from vimscript to lua", 172800, None, False),
    ("snake-game", "Build a snake game in pygame with a persistent high score list",
     259200, "Snake 🐍", False),
    ("data-pipeline", "Optimize the CSV import, it is too slow on files over 1GB", 518400, None, False),
]


def make_transcript(cwd: str, prompt: str, timestamp: float) -> tuple[str, str]:
    iso = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime(timestamp))
    session_id = str(uuid.uuid4())
    lines = [
        {"type": "mode", "sessionId": session_id},
        {
            "type": "user",
            "cwd": cwd,
            "sessionId": session_id,
            "timestamp": iso,
            "message": {"role": "user", "content": prompt},
        },
        {
            "type": "assistant",
            "cwd": cwd,
            "sessionId": session_id,
            "timestamp": iso,
            "message": {
                "role": "assistant",
                "model": "claude-opus-4-8",
                "content": [{"type": "text", "text": "On it."}],
                "usage": {"input_tokens": 1200, "output_tokens": 400, "cache_read_input_tokens": 9000},
            },
        },
    ]
    return session_id, "\n".join(json.dumps(line) for line in lines)


def main() -> None:
    projects_dir = ROOT / "projects"
    config_dir = ROOT / "config" / "claude-session-manager"
    projects_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)

    names: dict[str, str] = {}
    favorites: list[str] = []
    now = time.time()

    for project, prompt, age, custom_name, favorite in SESSIONS:
        cwd = f"/home/demo/projects/{project}"
        project_dir = projects_dir / cwd.replace("/", "-")
        project_dir.mkdir(exist_ok=True)
        mtime = now - age
        session_id, content = make_transcript(cwd, prompt, mtime)
        path = project_dir / f"{session_id}.jsonl"
        path.write_text(content, encoding="utf-8")
        os.utime(path, (mtime, mtime))
        if custom_name:
            names[session_id] = custom_name
        if favorite:
            favorites.append(session_id)

    (config_dir / "state.json").write_text(
        json.dumps({"names": names, "favorites": favorites, "hidden": [], "settings": {}}, indent=2),
        encoding="utf-8",
    )

    print(f"Demo data written to {ROOT}")
    print("Launch with:")
    print(
        f"  XDG_CONFIG_HOME={ROOT}/config CSM_PROJECTS_DIR={ROOT}/projects "
        "python3 -m claude_session_manager"
    )


if __name__ == "__main__":
    main()
