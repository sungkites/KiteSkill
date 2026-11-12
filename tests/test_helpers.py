"""Observable helper behavior; network and scientific acceptance are not inferred."""
import importlib.util
import json
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


doi = module("doi", ROOT / "skills/kite-literature/scripts/verify_doi.py")
plot = module("plot", ROOT / "skills/kite-figures/scripts/plot_csv.py")
installer = module("installer", ROOT / "scripts/install.py")


class DoiTests(unittest.TestCase):
    record = {"DOI": "10.1000/example", "title": ["A study"],
              "author": [{"family": "Wang"}], "published-print": {"date-parts": [[2025]]},
              "published-online": {"date-parts": [[2024]]}}

    def test_normalization(self):
        self.assertEqual(doi.normalize_doi("https://doi.org/10.1000/EXAMPLE"), "10.1000/example")

    def test_match_checks_only_supplied_fields(self):
        row = {"doi": "10.1000/example", "title": "A study", "year": "2024", "first_author": "Wang"}
        result = doi.verify_row(row, lambda _: self.record)
        self.assertEqual(result["status"], "metadata_match")
        self.assertEqual(result["claim_support"], "not_checked")

    def test_resolving_is_not_metadata_validation(self):
        self.assertEqual(doi.verify_row({"doi": "10.1000/example"}, lambda _: self.record)["status"], "resolved_only")

    def test_missing_optional_csv_values(self):
        row = {"doi": "10.1000/example", "title": None, "year": None, "first_author": None}
        self.assertEqual(doi.verify_row(row, lambda _: self.record)["status"], "resolved_only")

    def test_wrong_title_requires_review(self):
        result = doi.verify_row({"doi": "10.1000/example", "title": "Another study"}, lambda _: self.record)
        self.assertEqual(result["status"], "needs_review")

    def test_missing_doi_does_not_call_network(self):
        def fail(_):
            raise AssertionError("Should not fetch")
        self.assertEqual(doi.verify_row({"doi": ""}, fail)["status"], "unverified")

    def test_crossref_404_is_not_fabrication_verdict(self):
        def missing(_):
            raise HTTPError("test", 404, "not found", {}, None)
        self.assertEqual(doi.verify_row({"doi": "10.1000/example"}, missing)["status"], "unverified")

    def test_wrong_provider_identity(self):
        result = doi.verify_row({"doi": "10.1000/other"}, lambda _: self.record)
        self.assertEqual(result["status"], "unverified")


class PlotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.csv = self.root / "values.csv"

    def tearDown(self):
        self.temp.cleanup()

    def test_no_silent_duplicate_aggregation(self):
        self.csv.write_text("x,y\n1,2\n1,3\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            plot.load_data(self.csv, "x", "y")
        self.assertEqual(len(plot.load_data(self.csv, "x", "y", kind="scatter")["data"]), 2)

    def test_missing_and_infinite_values_rejected(self):
        for value in ("", "nan", "inf"):
            self.csv.write_text(f"x,y\n1,{value}\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                plot.load_data(self.csv, "x", "y")

    def test_uncertainty_requires_definition(self):
        with self.assertRaisesRegex(ValueError, "error-label"):
            plot.make_plot(self.csv, self.root / "out", "line", "x", "y", "X", "Y", yerr="sd")

    def test_no_label_without_errors(self):
        with self.assertRaisesRegex(ValueError, "requires --yerr"):
            plot.make_plot(self.csv, self.root / "out", "line", "x", "y", "X", "Y", error_label="SD")

    def test_export_and_provenance(self):
        self.csv.write_text("x,y,sd\n1,0.4,0.1\n2,0.7,0.2\n", encoding="utf-8")
        targets = plot.make_plot(self.csv, self.root / "out", "line", "x", "y", "X", "Y",
                                 yerr="sd", error_label="supplied SD")
        self.assertTrue(all(t.stat().st_size > 100 for t in targets))
        data = json.loads(targets[-1].read_text(encoding="utf-8"))
        self.assertEqual(data["aggregation"], "none; values plotted as supplied")
        self.assertEqual(data["visual_review"], "pending; inspect all final exports before publication")
        with self.assertRaisesRegex(ValueError, "exists"):
            plot.make_plot(self.csv, self.root / "out", "line", "x", "y", "X", "Y")


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source, self.dest = self.root / "source", self.root / "dest"
        self.skill = self.source / "kite-example"
        self.skill.mkdir(parents=True)
        (self.skill / "SKILL.md").write_text("version one", encoding="utf-8")

    def tearDown(self):
        self.temp.cleanup()

    def test_install_check_and_update_backup(self):
        installer.install(self.source, self.dest)
        installer.install(self.source, self.dest, check=True)
        (self.skill / "SKILL.md").write_text("version two", encoding="utf-8")
        result = installer.install(self.source, self.dest, update=True)
        backup = Path(result["backup"]) / "kite-example" / "SKILL.md"
        self.assertEqual(backup.read_text(encoding="utf-8"), "version one")
        installer.install(self.source, self.dest, check=True)

    def test_unmanaged_collision_does_not_overwrite(self):
        target = self.dest / "kite-example"
        target.mkdir(parents=True)
        (target / "SKILL.md").write_text("user work", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Unmanaged"):
            installer.install(self.source, self.dest, update=True)
        self.assertEqual((target / "SKILL.md").read_text(encoding="utf-8"), "user work")

    def test_local_edit_blocks_update(self):
        installer.install(self.source, self.dest)
        (self.dest / "kite-example" / "SKILL.md").write_text("local edit", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Local changes"):
            installer.install(self.source, self.dest, update=True)

    def test_invalid_selection_has_no_side_effect(self):
        with self.assertRaisesRegex(ValueError, "Unknown"):
            installer.install(self.source, self.dest, names=["kite-example", "../outside"])
        self.assertFalse(self.dest.exists())

    def test_second_run_is_idempotent(self):
        installer.install(self.source, self.dest)
        result = installer.install(self.source, self.dest)
        self.assertEqual(result["installed_or_updated"], [])

    def test_recursive_destination_rejected(self):
        with self.assertRaisesRegex(ValueError, "inside a source"):
            installer.install(self.source, self.skill / "nested")

    def test_manifest_failure_restores_previous_version(self):
        installer.install(self.source, self.dest)
        old_manifest = (self.dest / installer.MANIFEST).read_bytes()
        (self.skill / "SKILL.md").write_text("version two", encoding="utf-8")
        with patch.object(installer.os, "replace", side_effect=OSError("simulated manifest write failure")):
            with self.assertRaises(OSError):
                installer.install(self.source, self.dest, update=True)
        self.assertEqual((self.dest / "kite-example/SKILL.md").read_text(encoding="utf-8"), "version one")
        self.assertEqual((self.dest / installer.MANIFEST).read_bytes(), old_manifest)


if __name__ == "__main__":
    unittest.main()
