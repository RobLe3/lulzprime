"""
Tests for π(x) prime counting function.

Verifies implementation from docs/manual/part_4.md section 4.7.
"""

import pytest
from lulzprime.pi import pi, pi_range


class TestPi:
    """Test π(x) prime counting function."""

    def test_pi_small_values(self):
        """Test π(x) on small values with known results."""
        known = {
            0: 0, 1: 0, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4,
            10: 4, 20: 8, 30: 10, 50: 15, 100: 25
        }
        for x, expected in known.items():
            assert pi(x) == expected, f"π({x}) should be {expected}"

    def test_pi_larger_values(self):
        """Test π(x) on larger values."""
        # Known values from prime tables
        known = {
            1000: 168,
            10000: 1229,
        }
        for x, expected in known.items():
            assert pi(x) == expected, f"π({x}) should be {expected}"

    def test_pi_very_large_values(self):
        """Test π(x) on very large values using segmented sieve."""
        # Known values from prime tables
        # These values exceed the segmented threshold (100,000) and use bounded memory
        known = {
            100000: 9592,
            1000000: 78498,
        }
        for x, expected in known.items():
            result = pi(x)
            assert result == expected, f"π({x}) should be {expected}, got {result}"

    def test_pi_segmented_threshold(self):
        """Test π(x) around the segmented sieve threshold (100,000)."""
        # Test values just below and above threshold to ensure consistency
        # Threshold is 100,000 - test at boundary
        test_values = [
            99999,   # Just below threshold (uses full sieve)
            100000,  # Exactly at threshold (uses segmented sieve)
            100001,  # Just above threshold (uses segmented sieve)
        ]

        # All should produce correct, monotone results
        results = [pi(x) for x in test_values]

        # Verify monotonicity at threshold boundary
        assert results[0] <= results[1] <= results[2], \
            f"π(x) not monotone at threshold: {results}"

        # Verify known value at threshold
        assert results[1] == 9592, f"π(100000) should be 9592, got {results[1]}"

    def test_pi_segmented_large_values(self):
        """Test π(x) at large values to verify segmented sieve correctness."""
        # Test additional large values to stress-test segmented implementation
        # Values chosen to test multiple segments (segment_size = 1,000,000)
        # Values verified against full sieve implementation
        known = {
            250000: 22044,   # ~2.5 segments
            500000: 41538,   # ~5 segments
            750000: 60238,   # ~7.5 segments
        }
        for x, expected in known.items():
            result = pi(x)
            assert result == expected, f"π({x}) should be {expected}, got {result}"

    def test_pi_segmented_vs_full_sieve(self):
        """Test that segmented and full sieve produce identical results."""
        # Import internal functions for direct testing
        from lulzprime.pi import _simple_sieve, _segmented_sieve

        # Test values where both methods can be used
        test_values = [10000, 50000, 99999]

        for x in test_values:
            full_result = len(_simple_sieve(x))
            segmented_result = _segmented_sieve(x)
            assert full_result == segmented_result, \
                f"Mismatch at x={x}: full={full_result}, segmented={segmented_result}"

    def test_pi_monotonicity(self):
        """Test that π(x) is monotone increasing."""
        values = [0, 1, 5, 10, 50, 100, 500]
        pi_values = [pi(x) for x in values]

        for i in range(1, len(pi_values)):
            assert pi_values[i] >= pi_values[i-1], "π(x) not monotone"

    def test_pi_input_validation(self):
        """Test π(x) input validation."""
        with pytest.raises(TypeError):
            pi(1.5)

        with pytest.raises(ValueError):
            pi(-1)


class TestPiRange:
    """Test π(x, y) range counting function."""

    def test_pi_range_basic(self):
        """Test pi_range() basic functionality."""
        # Primes in (10, 20]: 11, 13, 17, 19 = 4 primes
        assert pi_range(10, 20) == 4

        # Primes in (2, 10]: 3, 5, 7 = 3 primes
        assert pi_range(2, 10) == 3

    def test_pi_range_empty(self):
        """Test pi_range() on empty ranges."""
        assert pi_range(10, 10) == 0
        assert pi_range(10, 5) == 0

    def test_pi_range_consistency(self):
        """Test that pi_range(x, y) == pi(y) - pi(x)."""
        test_cases = [(0, 10), (10, 50), (50, 100), (100, 200)]
        for x, y in test_cases:
            assert pi_range(x, y) == pi(y) - pi(x)
