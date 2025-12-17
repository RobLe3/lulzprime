"""
Jump-adjust pipelines for prime resolution.

Provides the internal machinery for resolving p_n using forecast + π(x) refinement.
See docs/manual/part_5.md section 5.3 for canonical workflow.

Canonical reference: paper/OMPC_v1.33.7lulz.pdf
"""

from typing import Callable
from .forecast import forecast
from .pi import pi
from .primality import is_prime, prev_prime, next_prime


def resolve_internal(index: int) -> int:
    """
    Internal resolution pipeline: forecast → bracket → π(x) refinement → correction.

    This implements the canonical chain from Part 5, section 5.3:
    1. Get analytic forecast
    2. Bracket the target
    3. Binary search using π(x) to find minimal x where π(x) >= index
    4. Deterministic correction to exact prime

    Args:
        index: Prime index (1-based)

    Returns:
        Exact p_index

    Note: This is an internal function. Public API is in resolve.py.
    """
    # Use default pi function
    return resolve_internal_with_pi(index, pi)


def resolve_internal_with_pi(index: int, pi_fn: Callable[[int], int]) -> int:
    """
    Internal resolution pipeline with injected π(x) function.

    This variant accepts a π(x) function as a parameter, enabling
    batch operations to inject a cached version without global state mutation.

    Same workflow as resolve_internal(), but uses pi_fn instead of global pi.

    Args:
        index: Prime index (1-based)
        pi_fn: Prime counting function π(x) to use

    Returns:
        Exact p_index

    Note: This is an internal function for dependency injection.
          Public API should use resolve() or resolve_many().
    """
    # Step 1: Get forecast
    guess = forecast(index)

    # Step 2-3: Bracket and refine using binary search with π(x)
    # Find minimal x where π(x) >= index
    x = _binary_search_pi(index, guess, pi_fn)

    # Step 4: Deterministic correction (Part 5, section 5.3, step 8)
    # If x is not prime, step to previous prime
    if not is_prime(x):
        x = prev_prime(x)

    # While pi(x) > index, step backward prime-by-prime
    while pi_fn(x) > index:
        x = prev_prime(x - 1)

    # While pi(x) < index, step forward prime-by-prime
    # Note: Due to binary search finding minimal x where pi(x) >= index,
    # this forward step is typically a no-op, but required for Part 5 compliance
    while pi_fn(x) < index:
        x = next_prime(x + 1)

    # Verification (should always pass if implementation is correct)
    if pi_fn(x) != index:
        raise RuntimeError(
            f"Resolution failed: pi({x}) = {pi_fn(x)} != {index}. "
            "This indicates a bug in the resolution pipeline."
        )

    return x


def _binary_search_pi(target_index: int, guess: int, pi_fn: Callable[[int], int] = pi) -> int:
    """
    Binary search to find minimal x where π(x) >= target_index.

    Args:
        target_index: Target prime index
        guess: Initial forecast estimate
        pi_fn: Prime counting function to use (default: global pi)

    Returns:
        Minimal x where π(x) >= target_index
    """
    # Establish bounds
    # Lower bound: start near guess but ensure we don't overshoot
    lo = max(2, int(guess * 0.9))
    # Upper bound: use analytic upper bound for p_n
    # For n >= 6: p_n < n * (log n + log log n)
    if target_index >= 6:
        import math
        n = target_index
        hi = int(n * (math.log(n) + math.log(math.log(n))) * 1.1)
    else:
        hi = guess * 2

    # Adjust if initial bounds are wrong
    if pi_fn(lo) > target_index:
        # Widen lo downward
        lo = 2

    if pi_fn(hi) < target_index:
        # Widen hi upward (double until we exceed)
        while pi_fn(hi) < target_index:
            hi *= 2

    # Binary search for minimal x where π(x) >= target_index
    while lo < hi:
        mid = (lo + hi) // 2
        if pi_fn(mid) < target_index:
            lo = mid + 1
        else:
            hi = mid

    return lo
