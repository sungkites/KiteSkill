#!/usr/bin/env python3
"""Validate skill metadata, local links and Python syntax without network access."""
import ast
import json
import re
import sys
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {"kite-research", "kite-ideation", "kite-literature", "kite-experiments",
            "kite-writing", "kite-figures", "kite-review"}


def validate(root=ROOT):
    errors = []
    folders = {p.name for p in (root / "skills").iterdir() if p.is_dir()}
    if folders != EXPECTED:
        errors.append(f"Unexpected skill set: {sorted(folders)}")
    for name in sorted(EXPECTED):
        folder = root / "skills" / name
        try:
            text = (folder / "SKILL.md").read_text(encoding="utf-8")
            match = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
            if not match:
                raise ValueError("Missing YAML frontmatter")
            front = yaml.safe_load(match.group(1))
            if front.get("name") != name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
                errors.append(f"{name}: name/folder mismatch")
            description = front.get("description")
            if not isinstance(description, str) or not 20 <= len(description) <= 1024:
                errors.append(f"{name}: invalid description")
            ui = yaml.safe_load((folder / "agents" / "openai.yaml").read_text(encoding="utf-8"))
            interface = ui["interface"]
            if not 25 <= len(interface["short_description"]) <= 64:
                errors.append(f"{name}: UI description must have 25–64 characters")
            if "$" + name not in interface["default_prompt"]:
                errors.append(f"{name}: prompt must invoke the skill")
        except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as error:
            errors.append(f"{name}: {error}")
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        body = path.read_text(encoding="utf-8")
        for target in re.findall(r"\]\(([^)]+)\)", body):
            if "://" in target or target.startswith("#"):
                continue
            relative = target.split("#")[0]
            if relative and not (path.parent / relative).exists():
                errors.append(f"{path.relative_to(root)}: broken link {target}")
        if re.search(r"(?m)^\s*\[TODO:", body):
            errors.append(f"{path.relative_to(root)}: unfinished scaffold")
    for path in root.rglob("*.py"):
        if ".git" in path.parts:
            continue
        try:
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except SyntaxError as error:
            errors.append(str(error))
    return errors


if __name__ == "__main__":
    errors = validate()
    print(json.dumps({"skills": len(EXPECTED), "errors": errors}, ensure_ascii=False, indent=2))
    sys.exit(bool(errors))
