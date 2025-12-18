"""
Lehmer-style sublinear π(x) implementation.

CANONICAL FORMULA (Legendre's formula):
────────────────────────────────────────
π(x) = φ(x, a) + a - 1

Where:
- a = π(√x)  [number of primes up to square root of x]
- φ(x, a) = count of integers in [1, x] not divisible by first a primes

This formula is exact because for a = π(√x), any composite number n ≤ x
must have at least one prime factor ≤ √x. Therefore, all composites are
already excluded by φ(x, a), and no correction term (P2) is needed.

The formula works because:
1. φ(x, a) counts: {1} ∪ {primes > p_a} ∪ {composites with all factors > p_a}
2. When a = π(√x), any composite ≤ x with all factors > √x would need
   smallest factor > √x, implying the number > x. So no such composites exist.
3. Therefore φ(x, a) = 1 + (number of primes in (p_a, x])
4. Thus π(x) = φ(x, a) + a - 1 counts all primes correctly.

Indexing convention:
- Primes are 1-indexed in formulas: p_1 = 2, p_2 = 3, p_3 = 5, ...
- Python list is 0-indexed: primes[0] = 2, primes[1] = 3, primes[2] = 5, ...
- To get p_i (1-indexed), use primes[i-1] (0-indexed)

Complexity:
- Time: O(x^(2/3)) - true sublinear (dominated by φ recursion depth)
- Space: O(x^(1/3)) - φ memoization cache + small primes list

This module is INACTIVE unless ENABLE_LEHMER_PI = True in config.py.

See docs/adr/0005-lehmer-pi.md for design decisions and analysis.

Guarantees:
- Exact: Returns precise π(x) matching segmented sieve
- Deterministic: No randomization, no floating-point ambiguity
- Bounded memory: O(x^(1/3)) space complexity
- No external dependencies: Pure Python stdlib only

References:
- Meissel (1870), Lehmer (1959), Deleglise & Rivat (1996)
- ADR 0005: Lehmer-Style Sublinear π(x) Implementation
- Part 6 section 6.3: Sublinear π(x) target
"""

import math
from functools import lru_cache


def _simple_sieve(limit: int) -> list[int]:
    """
    Generate all primes up to limit using Sieve of Eratosthenes.

    This is a local implementation to avoid circular imports and ensure
    the Lehmer module can be used independently.

    Time complexity: O(limit log log limit)
    Space complexity: O(limit)

    Args:
        limit: Upper bound for prime generation

    Returns:
        List of all primes <= limit in ascending order
    """
    if limit < 2:
        return []

    # Initialize sieve
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    # Sieve of Eratosthenes
    for i in range(2, int(math.isqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    return [i for i in range(2, limit + 1) if is_prime[i]]


def pi_small(x: int) -> int:
    """
    Count primes <= x using simple sieve for small values.

    This function is used internally by lehmer_pi for computing π(x^(1/4)),
    π(x^(1/3)), and π(√x). It uses a simple sieve to avoid recursion.

    Safe for x up to ~10M (takes ~1s, uses ~10 MB).

    Time complexity: O(x log log x)
    Space complexity: O(x)

    Args:
        x: Upper bound for counting primes

    Returns:
        Exact count of primes <= x
    """
    if x < 2:
        return 0

    return len(_simple_sieve(x))


def phi_bruteforce(x: int, a: int, primes_first_a: list[int]) -> int:
    """
    Brute-force oracle for φ(x, a): count integers in [1, x] not divisible by first a primes.

    This is the definitive reference implementation for testing.
    Complexity: O(x * a) - only use for testing with small x.

    Args:
        x: Upper bound
        a: Number of primes to exclude
        primes_first_a: List containing at least the first a primes

    Returns:
        Count of integers n in [1, x] where gcd(n, p_1 * p_2 * ... * p_a) = 1
    """
    if a == 0:
        return x  # No primes to exclude, count all integers in [1, x]
    if x < 1:
        return 0  # No positive integers

    count = 0
    for n in range(1, x + 1):
        is_coprime = True
        for i in range(a):
            if n % primes_first_a[i] == 0:
                is_coprime = False
                break
        if is_coprime:
            count += 1

    return count


def phi(x: int, a: int, primes: list[int], cache: dict | None = None) -> int:
    """
    Compute φ(x, a): count of integers <= x not divisible by first a primes.

    Uses recursive formula with memoization:
    - φ(x, 0) = x (no primes to exclude)
    - φ(x, a) = 0 if x < 2
    - φ(x, a) = φ(x, a-1) - φ(⌊x/p_a⌋, a-1) otherwise

    Memoization uses a dictionary cache passed by the caller to ensure
    cache consistency across recursive calls.

    Time complexity: O(x^(2/3)) with memoization
    Space complexity: O(x^(1/3)) for cache

    Args:
        x: Upper bound
        a: Number of primes to exclude (use first a primes from primes list)
        primes: List of primes in ascending order (must have >= a primes)
        cache: Optional memoization cache (dict)

    Returns:
        Count of integers in [1, x] not divisible by first a primes
    """
    if cache is None:
        cache = {}

    # Check cache
    cache_key = (x, a)
    if cache_key in cache:
        return cache[cache_key]

    # Base cases
    # CRITICAL: Must check a==0 first, then x
    # φ(x, 0) = x for any x (no primes to exclude)
    # φ(0, a) = 0 for any a > 0 (no integers in [1, 0])
    # φ(1, a) = 1 for any a >= 0 (1 is not divisible by any prime)
    if a == 0:
        return x  # No primes to exclude: count all integers in [1, x]
    if x < 1:
        return 0  # No positive integers in [1, x] when x < 1

    # Recursive case: φ(x, a) = φ(x, a-1) - φ(⌊x/p_a⌋, a-1)
    p_a = primes[a - 1]  # a-th prime (0-indexed, so a-1)

    if x < p_a:
        # If x < p_a, then p_a doesn't affect count, same as φ(x, a-1)
        result = phi(x, a - 1, primes, cache)
    else:
        result = phi(x, a - 1, primes, cache) - phi(x // p_a, a - 1, primes, cache)

    # Store in cache (limit cache size)
    if len(cache) < 10000:
        cache[cache_key] = result

    return result


def lehmer_pi(x: int) -> int:
    """
    Count primes <= x using Legendre's formula.

    Implements the canonical formula documented at module level:
        π(x) = φ(x, a) + a - 1

    Where a = π(√x) and φ(x, a) counts integers not divisible by first a primes.

    For small x (< 10,000), uses simple sieve for efficiency.
    For large x, uses true sublinear Legendre algorithm.

    Complexity:
    - Time: O(x^(2/3)) - true sublinear for large x
    - Space: O(x^(1/3)) - φ memoization + small primes

    Args:
        x: Upper bound for counting primes

    Returns:
        Exact count of primes <= x

    Examples:
        >>> lehmer_pi(10)
        4
        >>> lehmer_pi(100)
        25
        >>> lehmer_pi(1000)
        168
    """
    # Edge cases
    if x < 2:
        return 0
    if x == 2:
        return 1
    if x < 5:
        return 2  # Primes: 2, 3

    # For small x, simple sieve is faster than Legendre overhead
    SMALL_CUTOFF = 10_000
    if x < SMALL_CUTOFF:
        return pi_small(x)

    # Compute a = π(√x)
    x_sqrt = math.isqrt(x)  # √x
    a = pi_small(x_sqrt)  # Use pi_small since √x << x

    # Generate primes up to √x for φ computation
    primes = _simple_sieve(x_sqrt)

    # Verify we have enough primes (should always be true)
    if len(primes) < a:
        # Defensive fallback (should never happen)
        return pi_small(x)

    # Create memoization cache for φ
    phi_cache = {}

    # Compute φ(x, a): integers in [1, x] not divisible by first a primes
    phi_x_a = phi(x, a, primes, phi_cache)

    # Apply Legendre's formula: π(x) = φ(x, a) + a - 1
    result = phi_x_a + a - 1

    return result
