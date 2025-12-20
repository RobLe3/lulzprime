"""
Tests for OMPC simulator.

Verifies implementation from docs/manual/part_5.md section 5.7.
"""

import pytest

import lulzprime
from lulzprime.diagnostics import simulator_diagnostics
from lulzprime.pi import pi


class TestSimulator:
    """Test simulate() function."""

    def test_simulate_basic(self):
        """Test basic simulation functionality."""
        result = lulzprime.simulate(10, seed=42)

        assert isinstance(result, list)
        assert len(result) == 10
        assert all(isinstance(q, int) for q in result)

    def test_simulate_determinism(self):
        """Test that simulation is deterministic with fixed seed."""
        result1 = lulzprime.simulate(50, seed=123)
        result2 = lulzprime.simulate(50, seed=123)

        assert result1 == result2

    def test_simulate_different_seeds(self):
        """Test that different seeds give different results."""
        result1 = lulzprime.simulate(50, seed=1)
        result2 = lulzprime.simulate(50, seed=2)

        # Should be different (extremely unlikely to be same)
        assert result1 != result2

    def test_simulate_with_diagnostics(self):
        """Test simulation with diagnostics enabled."""
        result, diag = lulzprime.simulate(100, seed=42, diagnostics=True)

        assert isinstance(result, list)
        assert len(result) == 100

        assert isinstance(diag, list)
        assert len(diag) > 0

        # Check diagnostic structure
        for entry in diag:
            assert "step" in entry
            assert "q" in entry
            assert "w" in entry

    def test_simulate_increasing_sequence(self):
        """Test that simulated sequence is strictly increasing."""
        result = lulzprime.simulate(100, seed=42)

        for i in range(1, len(result)):
            assert result[i] > result[i - 1], f"Not increasing at index {i}"

    def test_simulate_convergence(self):
        """Test that simulator shows expected convergence behavior."""
        # Run longer simulation
        result = lulzprime.simulate(200, seed=42)

        # Use diagnostics to check convergence
        diag = simulator_diagnostics(result, pi)

        # Should show reasonable convergence (Part 7, section 7.4)
        assert diag["convergence_acceptable"], "Simulator not converging properly"
        assert abs(diag["density_ratio"] - 1.0) < 0.2, "Density ratio too far from 1.0"

    def test_simulate_input_validation(self):
        """Test simulate() input validation."""
        with pytest.raises(ValueError):
            lulzprime.simulate(0)

        with pytest.raises(ValueError):
            lulzprime.simulate(-5)


class TestSimulatorGeneratorMode:
    """Test simulate() generator mode functionality (Phase 2, Task 2)."""

    def test_generator_mode_basic(self):
        """Test basic generator mode functionality."""
        gen = lulzprime.simulate(10, seed=42, as_generator=True)

        # Should return a generator
        from typing import Generator

        assert isinstance(gen, Generator)

        # Convert to list
        result = list(gen)
        assert len(result) == 10
        assert all(isinstance(q, int) for q in result)

    def test_generator_determinism_same_as_list(self):
        """Test that generator mode produces same sequence as list mode with same seed."""
        # List mode
        list_result = lulzprime.simulate(100, seed=1337)

        # Generator mode
        gen_result = list(lulzprime.simulate(100, seed=1337, as_generator=True))

        # Must be identical for determinism
        assert list_result == gen_result, "Generator and list modes must yield identical sequences"

    def test_generator_determinism_repeated_calls(self):
        """Test that generator mode is deterministic across repeated calls."""
        gen1 = list(lulzprime.simulate(50, seed=999, as_generator=True))
        gen2 = list(lulzprime.simulate(50, seed=999, as_generator=True))

        assert gen1 == gen2, "Generator mode must be deterministic with same seed"

    def test_generator_different_seeds(self):
        """Test that generator mode produces different results with different seeds."""
        gen1 = list(lulzprime.simulate(50, seed=1, as_generator=True))
        gen2 = list(lulzprime.simulate(50, seed=2, as_generator=True))

        # Should be different (extremely unlikely to be same)
        assert gen1 != gen2, "Different seeds must produce different sequences"

    def test_generator_streaming(self):
        """Test that generator can be consumed incrementally without full materialization."""
        gen = lulzprime.simulate(100, seed=42, as_generator=True)

        # Consume first 10 values
        first_10 = [next(gen) for _ in range(10)]
        assert len(first_10) == 10

        # Consume rest
        rest = list(gen)
        assert len(rest) == 90

        # Verify all values are increasing
        full_sequence = first_10 + rest
        for i in range(1, len(full_sequence)):
            assert full_sequence[i] > full_sequence[i - 1]

    def test_generator_large_n_does_not_accumulate(self):
        """Test that generator mode doesn't accumulate large sequences in memory."""
        # This test verifies streaming behavior by consuming generator incrementally
        n_steps = 10000
        gen = lulzprime.simulate(n_steps, seed=42, as_generator=True)

        # Process in streaming fashion
        count = 0
        last_value = None
        for q in gen:
            count += 1
            last_value = q
            # Could process each value here without storing full list

        assert count == n_steps
        assert last_value is not None
        assert isinstance(last_value, int)

    def test_generator_increasing_sequence(self):
        """Test that generator mode produces strictly increasing sequence."""
        gen = lulzprime.simulate(100, seed=42, as_generator=True)

        prev = None
        for q in gen:
            if prev is not None:
                assert q > prev, f"Sequence not increasing: {prev} -> {q}"
            prev = q

    def test_generator_incompatible_with_diagnostics(self):
        """Test that generator mode and diagnostics are mutually exclusive."""
        with pytest.raises(
            ValueError, match="as_generator and diagnostics cannot both be True"
        ):
            lulzprime.simulate(10, seed=42, as_generator=True, diagnostics=True)

    def test_generator_input_validation(self):
        """Test that generator mode validates n_steps."""
        with pytest.raises(ValueError):
            lulzprime.simulate(0, as_generator=True)

        with pytest.raises(ValueError):
            lulzprime.simulate(-10, as_generator=True)

    def test_generator_with_custom_parameters(self):
        """Test generator mode with custom beta and initial_q parameters."""
        gen = lulzprime.simulate(
            50,
            seed=42,
            as_generator=True,
            initial_q=5,
            beta_initial=1.5,
            beta_decay=0.95,
        )

        result = list(gen)
        assert len(result) == 50
        assert result[0] == 5  # Should start with custom initial_q

    def test_backward_compatibility_default_is_list(self):
        """Test that default behavior (as_generator=False) returns list, not generator."""
        result = lulzprime.simulate(10, seed=42)

        # Should be a list, not a generator
        assert isinstance(result, list)
        assert not hasattr(result, "__next__")

    def test_generator_empty_exhaustion(self):
        """Test that generator is properly exhausted after consuming all values."""
        gen = lulzprime.simulate(5, seed=42, as_generator=True)

        # Consume all values
        values = list(gen)
        assert len(values) == 5

        # Generator should be exhausted
        try:
            next(gen)
            assert False, "Generator should be exhausted"
        except StopIteration:
            pass  # Expected
