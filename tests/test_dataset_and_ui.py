"""
End-to-end verification and validation test suite for Indonesian Top Universities Selectivity Platform.
Verifies dataset parity, institutional coverage (35 PTN + 15 PTS = 50 total), regional distribution,
metric mathematical formulas, UI element contracts in index.html, and strict zero-emoji compliance.
"""

import os
import json
import csv
import re
import unittest

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")
INDEX_HTML = os.path.join(ROOT_DIR, "index.html")
README_MD = os.path.join(ROOT_DIR, "README.md")


class TestDatasetIntegrity(unittest.TestCase):
    """Test data files in data/ directory for consistency and validity."""

    @classmethod
    def setUpClass(cls):
        # Load metadata
        with open(os.path.join(DATA_DIR, "metadata.json"), "r", encoding="utf-8") as f:
            cls.metadata = json.load(f)

        # Load JSON dataset
        with open(os.path.join(DATA_DIR, "ptn_keketatan.json"), "r", encoding="utf-8") as f:
            cls.dataset_json = json.load(f)

        # Load JS dataset
        with open(os.path.join(DATA_DIR, "ptn_keketatan.js"), "r", encoding="utf-8") as f:
            content = f.read()
            match_data = re.search(r"window\.PTN_KEKETATAN_DATA\s*=\s*(\[[\s\S]*?\]);", content)
            assert match_data is not None, "ptn_keketatan.js must define window.PTN_KEKETATAN_DATA"
            cls.dataset_js = json.loads(match_data.group(1))

            match_cat = re.search(r"window\.PTN_CATALOG\s*=\s*(\{[\s\S]*?\});", content)
            assert match_cat is not None, "ptn_keketatan.js must define window.PTN_CATALOG"
            cls.catalog_js = json.loads(match_cat.group(1))

        # Load CSV dataset
        with open(os.path.join(DATA_DIR, "ptn_keketatan.csv"), "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            cls.dataset_csv = list(reader)

    def test_total_counts(self):
        """Verify total universities and programs match targets exactly."""
        self.assertEqual(self.metadata["total_universitas"], 50)
        self.assertEqual(self.metadata["total_ptn"], 35)
        self.assertEqual(self.metadata["total_pts"], 15)
        self.assertEqual(self.metadata["total_prodi"], 295)
        self.assertEqual(len(self.dataset_json), 295)
        self.assertEqual(len(self.dataset_js), 295)
        self.assertEqual(len(self.dataset_csv), 295)
        self.assertEqual(len(self.catalog_js), 50)

    def test_institutions_breakdown(self):
        """Verify distinct institutions, types, and regions across all programs."""
        campuses = {}
        regions = set()
        for item in self.dataset_json:
            ptn_id = item["ptn_id"]
            if ptn_id not in campuses:
                campuses[ptn_id] = {
                    "tipe": item["ptn_tipe"],
                    "wilayah": item["ptn_wilayah"],
                    "kota": item["ptn_kota"],
                    "nama": item["ptn_nama"]
                }
            regions.add(item["ptn_wilayah"])

        self.assertEqual(len(campuses), 50, "Must contain exactly 50 distinct campuses")
        ptn_count = sum(1 for c in campuses.values() if c["tipe"] == "PTN")
        pts_count = sum(1 for c in campuses.values() if c["tipe"] == "PTS")
        self.assertEqual(ptn_count, 35, "Must contain exactly 35 PTN")
        self.assertEqual(pts_count, 15, "Must contain exactly 15 PTS")

        expected_regions = {"Jawa", "Sumatera", "Kalimantan", "Sulawesi", "Bali-Nusa Tenggara"}
        self.assertEqual(regions, expected_regions, "Must cover all 5 designated Nusantara regions")

    def test_mathematical_metrics(self):
        """Verify selectivity rate and competition ratio formulas."""
        for item in self.dataset_json:
            for track in ["snbp", "snbt"]:
                data = item[track]
                kuota = data["daya_tampung"]
                peminat = data["peminat"]
                keketatan = data["keketatan_persen"]
                rasio_str = data["rasio_persaingan"]

                self.assertGreater(kuota, 0, f"{item['id']} {track} kuota must be > 0")
                self.assertGreater(peminat, 0, f"{item['id']} {track} peminat must be > 0")

                expected_rate = round((kuota / peminat) * 100, 2)
                self.assertAlmostEqual(keketatan, expected_rate, places=2)

                expected_ratio_denom = round(peminat / kuota)
                self.assertEqual(rasio_str, f"1 : {expected_ratio_denom}")

    def test_program_profiles(self):
        """Verify qualitative bilingual profile fields exist and are non-empty."""
        for item in self.dataset_json:
            profil = item.get("profil", {})
            deskripsi = profil.get("deskripsi", {})
            self.assertTrue(len(deskripsi.get("id", "")) > 10, f"{item['id']} missing Indonesian description")
            self.assertTrue(len(deskripsi.get("en", "")) > 10, f"{item['id']} missing English description")

            fokus = profil.get("fokus", {})
            self.assertTrue(len(fokus.get("id", [])) >= 2, f"{item['id']} missing Indonesian focus")
            self.assertTrue(len(fokus.get("en", [])) >= 2, f"{item['id']} missing English focus")

            karir = profil.get("karir", {})
            self.assertTrue(len(karir.get("id", [])) >= 2, f"{item['id']} missing Indonesian career prospects")
            self.assertTrue(len(karir.get("en", [])) >= 2, f"{item['id']} missing English career prospects")

            for track in ["snbp", "snbt"]:
                riwayat = item[track].get("riwayat_peminat", {})
                self.assertIn("2022", riwayat)
                self.assertIn("2023", riwayat)
                self.assertIn("2024", riwayat)
                self.assertGreater(riwayat["2024"], 0)


class TestUIElements(unittest.TestCase):
    """Test index.html contract and DOM element IDs for filters, modals, and simulators."""

    @classmethod
    def setUpClass(cls):
        with open(INDEX_HTML, "r", encoding="utf-8") as f:
            cls.html = f.read()

    def test_required_dom_ids(self):
        """Ensure all required element IDs for filtering and interactivity exist in HTML."""
        required_ids = [
            # Top Bar & Nav
            "announcement-text",
            "announcement-updated",
            "lang-toggle-btn",
            "nav-title",
            "nav-subtitle",
            # Hero Metrics
            "hero-pill",
            "hero-title",
            "hero-desc",
            "stat-ptn-val",
            "stat-prodi-val",
            "stat-extreme-val",
            # Navigation Tabs
            "tab-btn-leaderboard",
            "tab-btn-compare",
            "tab-btn-simulator",
            "tab-btn-directory",
            # Sections
            "section-leaderboard",
            "section-compare",
            "section-simulator",
            "section-directory",
            # Leaderboard Elements
            "lb-track-snbt",
            "lb-track-snbp",
            "lb-tipe-select",
            "lb-wilayah-select",
            "lb-rumpun-select",
            "leaderboard-body",
            # Comparison Elements
            "compare-prodi-select",
            "comp-track-snbt",
            "comp-track-snbp",
            "compare-results-container",
            # Simulator Elements
            "sim-p1-ptn",
            "sim-p1-prodi",
            "sim-p2-ptn",
            "sim-p2-prodi",
            "sim-track-snbt",
            "sim-track-snbp",
            "simulation-output-card",
            # Directory Elements
            "dir-search",
            "dir-wilayah-select",
            "dir-tipe-select",
            "dir-ptn-select",
            "dir-rumpun-select",
            "dir-grid-container",
            "dir-table-container",
            "dir-btn-reset",
            # Modal Dialog
            "prodi-modal",
            "modal-ptn-badge",
            "modal-tipe-badge",
            "modal-wilayah-badge",
            "modal-prodi-name",
            "modal-trend-bars",
            "modal-btn-spmb"
        ]
        for elem_id in required_ids:
            pattern = f'id="{elem_id}"'
            self.assertIn(pattern, self.html, f"Missing required DOM id: {elem_id}")

    def test_bilingual_dictionary_keys(self):
        """Ensure both ID and EN dictionaries contain essential translation keys."""
        for key in ["announcement_text", "nav_title", "hero_title", "tab_leaderboard", "tab_compare", "tab_simulator", "tab_directory"]:
            self.assertIn(f'{key}:', self.html, f"Missing translation key {key} in index.html I18N")


class TestEmojiExclusion(unittest.TestCase):
    """Strictly verify zero emojis in codebase, data, and documentation."""

    def test_no_emojis_in_critical_files(self):
        files_to_check = [
            INDEX_HTML,
            README_MD,
            os.path.join(DATA_DIR, "metadata.json"),
            os.path.join(DATA_DIR, "ptn_keketatan.json"),
            os.path.join(DATA_DIR, "ptn_keketatan.js"),
            os.path.join(DATA_DIR, "ptn_keketatan.csv")
        ]
        for file_path in files_to_check:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            # Test for emoji characters (surrogate pairs / high code points above 0x1F000 or specific emoji ranges)
            emoji_chars = [c for c in content if ord(c) in range(0x1F300, 0x1FAFF) or ord(c) in range(0x2600, 0x27BF)]
            self.assertEqual(len(emoji_chars), 0, f"Emoji detected in {file_path}: {emoji_chars}")


if __name__ == "__main__":
    unittest.main()
