#!/usr/bin/env python3
"""Plot CSV values as supplied; do not aggregate or infer uncertainty."""
import argparse
import csv
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path


def finite_number(value, column, line):
    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"Row {line}: {column} must be numeric; missing values need an explicit analysis") from error
    if not math.isfinite(number):
        raise ValueError(f"Row {line}: {column} must be finite")
    return number


def load_data(path, x, y, series=None, yerr=None, kind="line"):
    groups = {}
    with Path(path).open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        required = [x, y] + ([series] if series else []) + ([yerr] if yerr else [])
        if not reader.fieldnames or any(c not in reader.fieldnames for c in required):
            raise ValueError("Missing required CSV columns: " + ", ".join(required))
        for line, row in enumerate(reader, 2):
            key = row[series] if series else "data"
            if series and not key.strip():
                raise ValueError(f"Row {line}: series label must not be empty")
            xv = row[x] if kind == "bar" else finite_number(row[x], x, line)
            if kind == "bar" and not xv.strip():
                raise ValueError(f"Row {line}: category must not be empty")
            yv = finite_number(row[y], y, line)
            error = finite_number(row[yerr], yerr, line) if yerr else None
            if error is not None and error < 0:
                raise ValueError(f"Row {line}: error half-width must be nonnegative")
            groups.setdefault(key, []).append((xv, yv, error))
    if not groups:
        raise ValueError("CSV contains no observations")
    for key, values in groups.items():
        if kind in ("line", "bar") and len({v[0] for v in values}) != len(values):
            raise ValueError(f"Duplicate x values in series {key!r}; aggregate explicitly or use scatter")
        if kind == "line":
            values.sort(key=lambda value: value[0])
    return groups


def make_plot(csv_path, output, kind, x, y, xlabel, ylabel, series=None,
              yerr=None, error_label=None, width=6.4, height=4.0, overwrite=False):
    if yerr and not error_label:
        raise ValueError("--yerr requires --error-label; uncertainty is not inferred")
    if error_label and not yerr:
        raise ValueError("--error-label requires --yerr")
    if not math.isfinite(width) or not math.isfinite(height) or width <= 0 or height <= 0:
        raise ValueError("Figure dimensions must be finite and positive")
    groups = load_data(csv_path, x, y, series, yerr, kind)
    output = Path(output)
    targets = [Path(str(output) + suffix) for suffix in (".pdf", ".svg", ".png", ".provenance.json")]
    if Path(csv_path).resolve() in [p.resolve() for p in targets]:
        raise ValueError("An output would overwrite the source CSV")
    if not overwrite and any(p.exists() for p in targets):
        raise ValueError("Output exists; choose another prefix or pass --overwrite")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    colors = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#000000"]
    markers = ["o", "s", "^", "D", "v", "P", "X"]
    with plt.rc_context({"font.family": "DejaVu Sans", "font.size": 10,
                         "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
                         "axes.spines.top": False, "axes.spines.right": False}):
        fig, ax = plt.subplots(figsize=(width, height), layout="constrained")
        categories = list(dict.fromkeys(v[0] for values in groups.values() for v in values)) if kind == "bar" else []
        for index, (label, values) in enumerate(groups.items()):
            xs, ys, errors = zip(*values)
            errs = errors if yerr else None
            color, marker = colors[index % len(colors)], markers[index % len(markers)]
            if kind == "bar":
                positions = [categories.index(v) + (index - (len(groups) - 1) / 2) * 0.8 / len(groups) for v in xs]
                ax.bar(positions, ys, width=0.8 / len(groups), yerr=errs, label=label,
                       color=color, capsize=3, edgecolor="black", linewidth=0.5,
                       hatch=["", "//", "..", "xx"][index % 4])
            else:
                ax.errorbar(xs, ys, yerr=errs, label=label, color=color, marker=marker,
                            linestyle="-" if kind == "line" else "none", capsize=3, linewidth=1.3)
        if categories:
            ax.set_xticks(range(len(categories)), categories)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.grid(axis="y", alpha=0.2)
        ax.set_axisbelow(True)
        if series:
            ax.legend(frameon=False, title=series)
        if error_label:
            fig.suptitle("Error bars: " + error_label, fontsize=9)
        output.parent.mkdir(parents=True, exist_ok=True)
        try:
            for target in targets[:3]:
                fig.savefig(target, dpi=300)
        finally:
            plt.close(fig)
    provenance = {"created_at": datetime.now(timezone.utc).isoformat(),
                  "source_name": Path(csv_path).name,
                  "source_sha256": hashlib.sha256(Path(csv_path).read_bytes()).hexdigest(),
                  "kind": kind, "x": x, "y": y, "series": series, "yerr": yerr,
                  "error_label": error_label, "aggregation": "none; values plotted as supplied",
                  "group_sizes": {k: len(v) for k, v in groups.items()},
                  "group_size_meaning": "CSV rows; not independent sample sizes",
                  "visual_review": "pending; inspect all final exports before publication"}
    targets[3].write_text(json.dumps(provenance, ensure_ascii=False, indent=2), encoding="utf-8")
    return targets


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", required=True, type=Path, help="Output prefix without extension")
    parser.add_argument("--kind", choices=["line", "scatter", "bar"], default="line")
    for column in ("x", "y", "xlabel", "ylabel"):
        parser.add_argument("--" + column, required=True)
    parser.add_argument("--series")
    parser.add_argument("--yerr")
    parser.add_argument("--error-label")
    parser.add_argument("--width", type=float, default=6.4)
    parser.add_argument("--height", type=float, default=4.0)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    try:
        targets = make_plot(args.csv, args.output, args.kind, args.x, args.y,
                            args.xlabel, args.ylabel, args.series, args.yerr,
                            args.error_label, args.width, args.height, args.overwrite)
    except (ValueError, OSError) as error:
        parser.error(str(error))
    print(json.dumps({"outputs": [str(p) for p in targets], "visual_review": "pending"}))


if __name__ == "__main__":
    main()
