"""
Diagnostics, verification, and self-checks.

Provides observational tools for correctness validation and performance monitoring.
See docs/manual/part_7.md for verification requirements.

Canonical reference: paper/OMPC_v1.33.7lulz.pdf

IMPORTANT: Diagnostics must observe only. They must never alter computational results.
"""

from typing import Any, Callable


def verify_resolution(result: int, index: int, pi_func: Callable, is_prime_func: Callable) -> bool:
    """
    Verify that result is the exact p_index (Tier A verification).

    From Part 7, section 7.3:
    - Verify pi(result) == index
    - Verify is_prime(result) == True

    Args:
        result: Claimed value of p_index
        index: Prime index
        pi_func: Prime counting function π(x)
        is_prime_func: Primality testing function

    Returns:
        True if verification passes

    Raises:
        AssertionError: If verification fails (hard error)
    """
    # Check primality
    if not is_prime_func(result):
        raise AssertionError(
            f"Resolution verification failed: result {result} is not prime"
        )

    # Check index
    pi_result = pi_func(result)
    if pi_result != index:
        raise AssertionError(
            f"Resolution verification failed: pi({result}) = {pi_result} != {index}"
        )

    return True


def verify_range(primes: list[int], is_prime_func: Callable) -> bool:
    """
    Verify that a range result contains only primes in correct order (Tier B).

    From Part 7, section 7.3:
    - Each value must be prime
    - Ordering must be strictly increasing
    - No duplicates

    Args:
        primes: List of claimed primes
        is_prime_func: Primality testing function

    Returns:
        True if verification passes

    Raises:
        AssertionError: If verification fails
    """
    if not primes:
        return True

    # Check all are prime
    for p in primes:
        if not is_prime_func(p):
            raise AssertionError(f"Range verification failed: {p} is not prime")

    # Check strictly increasing
    for i in range(1, len(primes)):
        if primes[i] <= primes[i-1]:
            raise AssertionError(
                f"Range verification failed: not strictly increasing at index {i}"
            )

    return True


def check_forecast_quality(index: int, forecast_value: int, pi_func: Callable, epsilon: float = 0.1) -> dict[str, Any]:
    """
    Check forecast quality (Tier C sanity check).

    From Part 7, section 7.3:
    abs(pi(forecast(n)) - n) / n < ε (configurable, non-fatal)

    Args:
        index: Prime index
        forecast_value: Forecasted value
        pi_func: Prime counting function
        epsilon: Relative error threshold

    Returns:
        Dictionary with diagnostic info:
        - 'passed': bool
        - 'relative_error': float
        - 'pi_forecast': int
    """
    pi_forecast = pi_func(forecast_value)
    relative_error = abs(pi_forecast - index) / index

    return {
        'passed': relative_error < epsilon,
        'relative_error': relative_error,
        'pi_forecast': pi_forecast,
        'threshold': epsilon,
    }


def simulator_diagnostics(sequence: list[int], pi_func: Callable) -> dict[str, Any]:
    """
    Compute diagnostics for OMPC simulator output.

    From Part 7, section 7.4:
    - Density alignment: track pi(q_n) / n
    - Convergence: verify pi(q_n) / n → 1 as n grows
    - Drift detection

    Args:
        sequence: List of pseudo-primes from simulator
        pi_func: Prime counting function

    Returns:
        Dictionary with diagnostic metrics
    """
    import math

    if not sequence:
        return {'error': 'empty sequence'}

    n = len(sequence)
    q_final = sequence[-1]

    # Compute density ratio at final point
    pi_final = pi_func(q_final)
    density_ratio = pi_final / n if n > 0 else 0.0

    # Check several points for convergence trend
    checkpoints = []
    for i in [n // 4, n // 2, 3 * n // 4, n - 1]:
        if i > 0 and i < len(sequence):
            q_i = sequence[i]
            pi_i = pi_func(q_i)
            ratio_i = pi_i / (i + 1)
            checkpoints.append({
                'step': i + 1,
                'q': q_i,
                'pi': pi_i,
                'density_ratio': ratio_i,
            })

    # Compute drift (deviation from expected ratio of 1.0)
    drift = abs(density_ratio - 1.0)

    return {
        'n_steps': n,
        'q_final': q_final,
        'pi_final': pi_final,
        'density_ratio': density_ratio,
        'drift': drift,
        'convergence_acceptable': drift < 0.15,  # Threshold from paper
        'checkpoints': checkpoints,
    }
