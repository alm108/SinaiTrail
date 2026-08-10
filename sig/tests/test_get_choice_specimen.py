"""Conformance: the SIG v0.2 specimen's claims vs sinai_trail.get_choice.

Each test decides one claim from fixtures/validator_v0_2.sig against the real
reference implementation. Stdlib unittest; input() is patched so the interactive
loop is driven deterministically.
"""
import copy
import inspect
import unittest
from unittest import mock

import _bootstrap  # noqa: F401  (side effect: puts repo root on sys.path)
import sinai_trail


def run_get_choice(num_options, raws, state=None, allow_special=False, allow_checkin=True):
    """Drive get_choice with a scripted sequence of raw keystrokes."""
    with mock.patch("builtins.input", side_effect=list(raws)):
        return sinai_trail.get_choice(
            num_options, state=state,
            allow_special=allow_special, allow_checkin=allow_checkin,
        )


def special_state(special_used=False):
    return {"special_used": special_used, "special": "STRIKE THE ROCK", "standing": ["x"]}


class AcceptedNumeric(unittest.TestCase):
    def test_each_option_returns_itself(self):
        for n in range(1, 4):  # num_options = 3
            self.assertEqual(run_get_choice(3, [str(n)]), str(n))

    def test_out_of_range_is_rejected_then_loops(self):
        # "4" is illegal for a 3-option menu -> loops -> "2" returned
        self.assertEqual(run_get_choice(3, ["4", "2"]), "2")

    def test_zero_is_illegal(self):
        self.assertEqual(run_get_choice(3, ["0", "1"]), "1")


class AcceptedBack(unittest.TestCase):
    def test_b_always_accepted(self):
        self.assertEqual(run_get_choice(3, ["b"]), "b")

    def test_b_accepted_even_without_state(self):
        self.assertEqual(run_get_choice(3, ["b"], state=None), "b")


class AcceptedSpecial(unittest.TestCase):
    def test_s_accepted_when_available(self):
        self.assertEqual(
            run_get_choice(3, ["s"], state=special_state(False), allow_special=True), "s")

    def test_s_rejected_when_flag_off(self):
        self.assertEqual(
            run_get_choice(3, ["s", "1"], state=special_state(False), allow_special=False), "1")

    def test_s_rejected_when_already_used(self):
        self.assertEqual(
            run_get_choice(3, ["s", "1"], state=special_state(True), allow_special=True), "1")

    def test_s_rejected_when_no_state(self):
        self.assertEqual(
            run_get_choice(3, ["s", "1"], state=None, allow_special=True), "1")


class AcceptedCheckin(unittest.TestCase):
    def test_c_accepted_with_state(self):
        self.assertEqual(run_get_choice(3, ["c"], state={"standing": []}, allow_checkin=True), "c")

    def test_c_rejected_when_flag_off(self):
        self.assertEqual(
            run_get_choice(3, ["c", "1"], state={"standing": []}, allow_checkin=False), "1")

    def test_c_rejected_when_no_state(self):
        self.assertEqual(run_get_choice(3, ["c", "1"], state=None, allow_checkin=True), "1")


class Normalize(unittest.TestCase):
    def test_strip(self):
        self.assertEqual(run_get_choice(3, ["  2  "]), "2")

    def test_lower_on_back(self):
        self.assertEqual(run_get_choice(3, ["B"]), "b")

    def test_strip_and_lower_on_special(self):
        self.assertEqual(
            run_get_choice(3, ["  S  "], state=special_state(False), allow_special=True), "s")


class Purity(unittest.TestCase):
    def test_state_not_mutated(self):
        state = special_state(False)
        before = copy.deepcopy(state)
        run_get_choice(3, ["s"], state=state, allow_special=True)
        self.assertEqual(state, before, "get_choice must not mutate state")

    def test_state_not_mutated_on_reprompt(self):
        state = special_state(False)
        before = copy.deepcopy(state)
        run_get_choice(3, ["zzz", "9", "1"], state=state, allow_special=True)
        self.assertEqual(state, before)


class Determinism(unittest.TestCase):
    def test_source_has_no_random(self):
        src = inspect.getsource(sinai_trail.get_choice)
        self.assertNotIn("random", src)

    def test_same_input_same_output(self):
        outs = {run_get_choice(3, ["2"]) for _ in range(25)}
        self.assertEqual(outs, {"2"})


class FailClosed(unittest.TestCase):
    def test_illegal_then_legal_returns_only_legal(self):
        self.assertEqual(run_get_choice(3, ["x", "99", "", "zzz", "3"]), "3")

    def test_never_emits_illegal_token(self):
        # Property-style: many illegal tokens, then a legal one; result must be legal.
        legal = {"1", "2", "3", "b"}
        for junk in (["4"], ["nope"], ["!!"], [" "], ["12"]):
            out = run_get_choice(3, junk + ["1"])
            self.assertIn(out, legal)


if __name__ == "__main__":
    unittest.main()
