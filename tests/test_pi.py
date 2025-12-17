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
        """Test π(x) on very large values using sublinear algorithm."""
        # Known values from prime tables (tests Legendre implementation)
        # These values exceed the sieve threshold (10000) and use sublinear counting
        known = {
            100000: 9592,
            1000000: 78498,
        }
        for x, expected in known.items():
            result = pi(x)
            assert result == expected, f"π({x}) should be {expected}, got {result}"

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
