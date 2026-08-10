"""External postcondition: sinai_trail.apply_outcome clamps bounded stats to [0, 100].

The SIG specimen cites `0 <= s <= 100` as an *interface contract* the validator hands off
to, not an invariant of get_choice itself. This proves the clamp lives in apply_outcome.
"""
import unittest

import _bootstrap  # noqa: F401
import sinai_trail

BOUNDED = ("nerve", "manna", "water", "camp", "signal", "repair", "gold")


def make_state(**over):
    state = {k: 50 for k in BOUNDED}
    state.update({
        "presence_withdrawn": False,
        "lowest_nerve": 50,
        "gold_to_calf": 0,
        "standing": [],
        "strayed": [],
        "max_strayed": 0,
    })
    state.update(over)
    return state


class ClampPostcondition(unittest.TestCase):
    def test_overflow_clamped_to_100(self):
        state = make_state(nerve=90)
        sinai_trail.apply_outcome(state, {"nerve": +50})
        self.assertEqual(state["nerve"], 100)

    def test_underflow_clamped_to_0(self):
        state = make_state(water=10)
        sinai_trail.apply_outcome(state, {"water": -50})
        self.assertEqual(state["water"], 0)

    def test_within_range_exact(self):
        state = make_state(camp=50)
        sinai_trail.apply_outcome(state, {"camp": +20})
        self.assertEqual(state["camp"], 70)

    def test_all_bounded_keys_respect_bounds(self):
        for k in BOUNDED:
            hi = make_state(**{k: 80})
            sinai_trail.apply_outcome(hi, {k: +999})
            self.assertLessEqual(hi[k], 100, f"{k} exceeded 100")
            lo = make_state(**{k: 20})
            sinai_trail.apply_outcome(lo, {k: -999})
            self.assertGreaterEqual(lo[k], 0, f"{k} dropped below 0")

    def test_none_outcome_is_noop(self):
        state = make_state()
        before = dict(state)
        msg = sinai_trail.apply_outcome(state, None)
        self.assertEqual(msg, "")
        self.assertEqual(state, before)


if __name__ == "__main__":
    unittest.main()
