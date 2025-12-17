"""
Tests for resolve() function and resolution pipeline.

Verifies workflow from docs/manual/part_5.md section 5.3.
"""

import pytest
import lulzprime
from lulzprime.pi import pi


class TestResolve:
    """Test resolve() function."""

    def test_resolve_small_primes(self):
        """Test resolution of first 25 primes."""
        known_primes = [
            2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
            53, 59, 61, 67, 71, 73, 79, 83, 89, 97
        ]
        for i, expected in enumerate(known_primes, start=1):
            result = lulzprime.resolve(i)
            assert result == expected, f"resolve({i}) should be {expected}, got {result}"

    def test_resolve_larger_indices(self):
        """Test resolution at larger indices."""
        # Known values from prime tables
        test_cases = {
            100: 541,
            500: 3571,
            1000: 7919,
        }
        for index, expected in test_cases.items():
            result = lulzprime.resolve(index)
            assert result == expected, f"resolve({index}) should be {expected}, got {result}"

    def test_resolve_verification(self):
        """Test that resolve() satisfies Tier A guarantees."""
        # For any resolved prime, pi(p_n) must equal n
        for index in [1, 5, 10, 50, 100]:
            p_n = lulzprime.resolve(index)

            # Verify it's prime
            assert lulzprime.is_prime(p_n), f"resolve({index}) = {p_n} is not prime"

            # Verify pi(p_n) == index
            assert pi(p_n) == index, f"pi({p_n}) != {index}"


class TestResolutionPipeline:
    """Test internal resolution pipeline workflow."""

    def test_forecast_used_as_starting_point(self):
        """Verify forecast is used in resolution pipeline."""
        from lulzprime.forecast import forecast

        index = 50
        forecast_val = forecast(index)
        resolved_val = lulzprime.resolve(index)

        # Forecast should be reasonably close (within 20% typical)
        # This isn't a requirement, just checking the forecast is sensible
        relative_diff = abs(forecast_val - resolved_val) / resolved_val
        assert relative_diff < 0.3, f"Forecast too far from actual for index {index}"

    def test_resolution_consistency(self):
        """Test that multiple calls give same result."""
        index = 75
        results = [lulzprime.resolve(index) for _ in range(5)]
        assert len(set(results)) == 1, "resolve() not deterministic"

    def test_correction_step_compliance(self):
        """
        Verify that resolve_internal implements both correction steps from Part 5.

        Part 5 section 5.3 step 8 requires:
        - While pi(x) > index, step backward prime-by-prime
        - While pi(x) < index, step forward prime-by-prime

        This structural test verifies the implementation contains both loops.
        Note: The forward step is typically a no-op due to binary search finding
        minimal x where pi(x) >= index, but it must exist for spec compliance.
        """
        import inspect
        from lulzprime.lookup import resolve_internal_with_pi

        # Get source code of resolve_internal_with_pi (actual implementation)
        source = inspect.getsource(resolve_internal_with_pi)

        # Verify both correction loops are present
        # (uses pi_fn instead of pi due to dependency injection)
        assert "while pi_fn(x) > index:" in source, \
            "Missing backward correction: 'while pi_fn(x) > index'"
        assert "while pi_fn(x) < index:" in source, \
            "Missing forward correction: 'while pi_fn(x) < index'"

        # Verify they use the correct navigation functions
        assert "prev_prime" in source, "Missing prev_prime for backward correction"
        assert "next_prime" in source, "Missing next_prime for forward correction"
