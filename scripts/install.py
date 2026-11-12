#!/usr/bin/env python3
"""Install Kite skills, protecting unmanaged folders and local edits."""
import argparse
import hashlib
import json
import os
import re
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ".kite-install.json"


def hashes(folder):
    result = {}
    for path in sorted(folder.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"Symlinks are not supported in a skill: {path.name}")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
            result[path.relative_to(folder).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def install(source, dest, names=None, update=False, check=False):
    source, dest = Path(source).resolve(), Path(dest).resolve()
    available = {p.name: p for p in sorted(source.iterdir())
                 if p.is_dir() and not p.is_symlink() and (p / "SKILL.md").is_file()}
    selected = names or list(available)
    if not selected:
        raise ValueError("No skills selected")
    if len(selected) != len(set(selected)):
        raise ValueError("Duplicate skill selection")
    for name in selected:
        if not re.fullmatch(r"kite-[a-z0-9]+(?:-[a-z0-9]+)*", name) or name not in available:
            raise ValueError(f"Unknown Kite skill: {name}")
        if (dest / name).is_symlink():
            raise ValueError(f"Refusing a symlink destination: {name}")
        if available[name] == dest / name:
            raise ValueError("Source and destination must differ")
        if available[name] == dest or available[name] in dest.parents:
            raise ValueError("Destination must not be inside a source skill")
        if (dest / name).exists() and not (dest / name).is_dir():
            raise ValueError(f"Destination is not a directory: {name}")
    manifest_path = dest / MANIFEST
    if manifest_path.is_symlink():
        raise ValueError("Refusing a symlink installation manifest")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {"schema": 1, "skills": {}}
    if manifest.get("schema") != 1 or not isinstance(manifest.get("skills"), dict):
        raise ValueError("Unsupported installation manifest")
    source_hashes = {name: hashes(available[name]) for name in selected}
    changed = []
    for name in selected:
        target = dest / name
        current = hashes(target) if target.exists() else None
        expected = source_hashes[name]
        if check:
            if current != expected:
                raise ValueError(f"Installed skill missing or differs: {name}")
            continue
        if current == expected:
            continue  # Also adopts an identical skill installed by the official installer.
        if current is not None:
            if not update:
                raise ValueError(f"Destination exists: {name}; use --update for managed, unchanged skills")
            prior = manifest["skills"].get(name, {}).get("files")
            if prior is None:
                raise ValueError(f"Unmanaged skill differs: {name}; preserve it and choose another destination")
            if current != prior:
                raise ValueError(f"Local changes detected: {name}; preserve/reconcile them before updating")
        changed.append(name)
    if check:
        return {"checked": selected, "destination": str(dest)}
    dest.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix=".kite-stage-", dir=dest))
    backup_root = dest.parent / "kite-skill-backups" / (
        datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8])
    moved, installed = [], []
    try:
        # Stage the complete batch before changing any installed directory.
        for name in changed:
            shutil.copytree(available[name], stage / name,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            if hashes(stage / name) != source_hashes[name]:
                raise ValueError(f"Staged content verification failed: {name}")
        for name in changed:
            target = dest / name
            # Recheck for edits made since preflight.
            if target.is_symlink():
                raise ValueError(f"Destination became a symlink: {name}")
            if target.exists():
                if hashes(target) != manifest["skills"].get(name, {}).get("files"):
                    raise ValueError(f"Destination changed during installation: {name}")
                backup_root.mkdir(parents=True, exist_ok=True)
                shutil.move(str(target), str(backup_root / name))
                moved.append(name)
            shutil.move(str(stage / name), str(target))
            installed.append(name)
        for name in selected:
            manifest["skills"][name] = {"files": source_hashes[name], "version": "0.1.0"}
        manifest["updated_at"] = datetime.now(timezone.utc).isoformat()
        temp_manifest = stage / "manifest.json"
        temp_manifest.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        os.replace(temp_manifest, manifest_path)
    except Exception:
        # Paths are validated direct children of dest; remove only our newly installed copies.
        for name in reversed(installed):
            target = dest / name
            if target.parent != dest or target.is_symlink():
                raise RuntimeError("Unsafe rollback target; manual recovery required")
            shutil.rmtree(target)
        for name in reversed(moved):
            shutil.move(str(backup_root / name), str(dest / name))
        raise
    finally:
        if stage.parent == dest and stage.name.startswith(".kite-stage-"):
            shutil.rmtree(stage)
    return {"installed_or_updated": changed, "verified_identical": [n for n in selected if n not in changed],
            "destination": str(dest), "backup": str(backup_root) if moved else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    codex_root = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    parser.add_argument("--dest", type=Path, default=codex_root / "skills")
    parser.add_argument("--skills", nargs="+")
    parser.add_argument("--update", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        result = install(ROOT / "skills", args.dest, args.skills, args.update, args.check)
    except (ValueError, OSError) as error:
        parser.exit(1, f"Installation stopped: {error}\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
