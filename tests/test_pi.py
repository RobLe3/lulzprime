"""
Tests for π(x) prime counting function.

Verifies implementation from docs/manual/part_4.md section 4.7.
"""

import pytest
from lulzprime.pi import pi, pi_range, pi_parallel, _create_segment_ranges, _count_segment_primes


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


class TestPiParallelHelpers:
    """Test helper functions for parallel π(x)."""

    def test_create_segment_ranges_basic(self):
        """Test segment range creation with basic inputs."""
        segments = _create_segment_ranges(100, 200, 4)

        # Should create 4 segments covering [100, 200]
        assert len(segments) == 4

        # First segment starts at 100
        assert segments[0][0] == 100

        # Last segment ends at 200
        assert segments[-1][1] == 200

        # Segments are contiguous
        for i in range(len(segments) - 1):
            assert segments[i][1] + 1 == segments[i + 1][0]

    def test_create_segment_ranges_uneven_split(self):
        """Test segment range creation with uneven splits."""
        # 101 elements split into 4 workers: sizes 26, 25, 25, 25
        segments = _create_segment_ranges(0, 100, 4)

        assert len(segments) == 4

        # First segment gets the remainder (26 elements)
        assert segments[0][1] - segments[0][0] + 1 == 26

        # Others get 25 elements each
        for i in range(1, 4):
            assert segments[i][1] - segments[i][0] + 1 == 25

    def test_create_segment_ranges_invalid_workers(self):
        """Test that invalid worker counts raise ValueError."""
        with pytest.raises(ValueError, match="num_workers must be positive"):
            _create_segment_ranges(100, 200, 0)

        with pytest.raises(ValueError, match="num_workers must be positive"):
            _create_segment_ranges(100, 200, -1)

    def test_create_segment_ranges_empty_range(self):
        """Test segment creation with empty range."""
        segments = _create_segment_ranges(200, 100, 4)
        assert segments == []

    def test_count_segment_primes_basic(self):
        """Test counting primes in a segment."""
        from lulzprime.pi import _simple_sieve

        # Count primes in [100, 200]
        small_primes = _simple_sieve(14)  # sqrt(200) ≈ 14
        count = _count_segment_primes(100, 200, small_primes)

        # Primes in [100, 200]: 101, 103, ..., 199 (21 primes)
        assert count == 21

    def test_count_segment_primes_empty(self):
        """Test counting primes in empty segment."""
        from lulzprime.pi import _simple_sieve

        small_primes = _simple_sieve(10)
        count = _count_segment_primes(200, 100, small_primes)
        assert count == 0


class TestPiParallel:
    """Test parallel π(x) implementation."""

    def test_pi_parallel_correctness_small(self):
        """Test pi_parallel matches pi() for small values."""
        # Small values (below threshold, should use sequential path)
        test_values = [100, 1000, 10000, 100000]

        for x in test_values:
            result_parallel = pi_parallel(x)
            result_sequential = pi(x)
            assert result_parallel == result_sequential, \
                f"pi_parallel({x}) = {result_parallel} != pi({x}) = {result_sequential}"

    def test_pi_parallel_correctness_large(self):
        """Test pi_parallel matches pi() for large values (above threshold)."""
        # Large value (above threshold = 1M, should use parallel path)
        # Use 1M which is known: π(1,000,000) = 78498
        x = 1_000_000
        result_parallel = pi_parallel(x, workers=2)
        result_sequential = pi(x)

        assert result_parallel == result_sequential == 78498, \
            f"pi_parallel({x}) = {result_parallel} != pi({x}) = {result_sequential}"

    def test_pi_parallel_determinism(self):
        """Test that pi_parallel is deterministic (same x yields same result)."""
        x = 1_000_000
        workers = 4

        # Run multiple times with same parameters
        results = [pi_parallel(x, workers=workers) for _ in range(3)]

        # All results should be identical
        assert len(set(results)) == 1, \
            f"pi_parallel not deterministic: got {results}"

    def test_pi_parallel_different_workers_same_result(self):
        """Test that different worker counts yield same result."""
        x = 1_000_000

        # Test with different worker counts
        result_1 = pi_parallel(x, workers=1)
        result_2 = pi_parallel(x, workers=2)
        result_4 = pi_parallel(x, workers=4)

        assert result_1 == result_2 == result_4, \
            f"Different worker counts gave different results: {result_1}, {result_2}, {result_4}"

    def test_pi_parallel_threshold_fallback(self):
        """Test that values below threshold use sequential path."""
        # Below default threshold (1M), should use sequential pi()
        x = 500_000

        # Should work correctly even though below threshold
        result_parallel = pi_parallel(x)
        result_sequential = pi(x)

        assert result_parallel == result_sequential

    def test_pi_parallel_custom_threshold(self):
        """Test pi_parallel with custom threshold."""
        x = 100_000

        # With high threshold, should use sequential path
        result_high_threshold = pi_parallel(x, threshold=200_000)

        # With low threshold, should use parallel path
        result_low_threshold = pi_parallel(x, threshold=50_000, workers=2)

        # Both should match sequential result
        result_sequential = pi(x)
        assert result_high_threshold == result_low_threshold == result_sequential

    def test_pi_parallel_invalid_workers(self):
        """Test that invalid worker counts raise ValueError."""
        with pytest.raises(ValueError, match="workers must be positive"):
            pi_parallel(1_000_000, workers=0)

        with pytest.raises(ValueError, match="workers must be positive"):
            pi_parallel(1_000_000, workers=-1)

    def test_pi_parallel_input_validation(self):
        """Test pi_parallel input validation (same as pi)."""
        # Non-integer x
        with pytest.raises(TypeError):
            pi_parallel(1.5)

        # Negative x
        with pytest.raises(ValueError):
            pi_parallel(-1)

    def test_pi_parallel_edge_cases(self):
        """Test pi_parallel edge cases."""
        # x < 2
        assert pi_parallel(0) == 0
        assert pi_parallel(1) == 0

        # x = 2 (first prime)
        assert pi_parallel(2) == 1

        # Small primes
        assert pi_parallel(10) == 4

    def test_pi_parallel_default_workers(self):
        """Test that default workers parameter works."""
        x = 1_000_000

        # Should use default worker count (min(cpu_count, 8))
        result = pi_parallel(x)

        # Should match sequential result
        assert result == pi(x)

    def test_pi_parallel_monotonicity(self):
        """Test that pi_parallel is monotone increasing like pi."""
        # Test at various scales, including above threshold
        values = [100_000, 500_000, 1_000_000]
        results = [pi_parallel(x, workers=2) for x in values]

        # Should be monotone increasing
        for i in range(1, len(results)):
            assert results[i] >= results[i-1], \
                f"pi_parallel not monotone at {values[i]}"
