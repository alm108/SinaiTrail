"""Spec<->code binding: parse the fixture's CLAIMS block, then assert the reference
implementation actually satisfies each claim, plus header well-formedness from 03.

This is the fixture that makes the SIG-as-code specimen falsifiable: if get_choice's
behavior and the packet's claims disagree, this test fails.
"""
import copy
import inspect
import unittest
from unittest import mock

import _bootstrap
import sinai_trail
from sig_fixture import parse_claims

FIXTURE = _bootstrap.FIXTURES_DIR / "validator_v0_2.sig"


def run(num, raws, **kw):
    with mock.patch("builtins.input", side_effect=list(raws)):
        return sinai_trail.get_choice(num, **kw)


class FixtureParses(unittest.TestCase):
    def setUp(self):
        self.claims = parse_claims(FIXTURE)

    def test_expected_claim_keys_present(self):
        for key in ("level", "shape", "accepted_numeric", "accepted_special",
                    "accepted_checkin", "accepted_back", "normalize", "purity",
                    "determinism", "fail_closed", "max_base_dimension"):
            self.assertIn(key, self.claims, f"claim '{key}' missing from fixture")


class HeaderWellFormedness(unittest.TestCase):
    """From 03-levels-dimensions.md: shape present  <=>  level >= L5; no base dim > d5."""

    def setUp(self):
        self.claims = parse_claims(FIXTURE)

    def test_shape_iff_level_ge_l5(self):
        level = int(self.claims["level"].lstrip("Ll"))
        has_shape = bool(self.claims.get("shape"))
        self.assertEqual(has_shape, level >= 5,
                         "shape must be declared iff level >= L5")

    def test_max_base_dimension_not_exceeding_5(self):
        self.assertLessEqual(int(self.claims["max_base_dimension"]), 5)


class ClaimsBindToImplementation(unittest.TestCase):
    def setUp(self):
        self.claims = parse_claims(FIXTURE)

    def test_accepted_back_always(self):
        self.assertIn("b", self.claims["accepted_back"])
        self.assertEqual(run(3, ["b"], state=None), "b")

    def test_accepted_numeric_returns_itself(self):
        self.assertEqual(run(3, ["2"]), "2")

    def test_accepted_special_conditional(self):
        st = {"special_used": False, "special": "X", "standing": []}
        self.assertEqual(run(3, ["s"], state=st, allow_special=True), "s")
        self.assertEqual(run(3, ["s", "1"], state=st, allow_special=False), "1")

    def test_accepted_checkin_conditional(self):
        self.assertEqual(run(3, ["c"], state={"standing": []}, allow_checkin=True), "c")
        self.assertEqual(run(3, ["c", "1"], state=None, allow_checkin=True), "1")

    def test_normalize_claim(self):
        self.assertIn("strip", self.claims["normalize"])
        self.assertIn("lower", self.claims["normalize"])
        self.assertEqual(run(3, ["  2  "]), "2")
        self.assertEqual(run(3, ["B"]), "b")

    def test_determinism_claim(self):
        self.assertEqual(self.claims["determinism"], "no_random")
        self.assertNotIn("random", inspect.getsource(sinai_trail.get_choice))

    def test_purity_claim(self):
        self.assertEqual(self.claims["purity"], "no_state_mutation")
        st = {"special_used": False, "special": "X", "standing": []}
        before = copy.deepcopy(st)
        run(3, ["s"], state=st, allow_special=True)
        self.assertEqual(st, before)

    def test_fail_closed_claim(self):
        self.assertIn("never emit illegal", self.claims["fail_closed"])
        self.assertEqual(run(3, ["nope", "4", "1"]), "1")


if __name__ == "__main__":
    unittest.main()
