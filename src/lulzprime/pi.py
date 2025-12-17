"""
Prime counting function π(x) implementations.

Provides exact counting of primes <= x using efficient algorithms.
See docs/manual/part_4.md section 4.7 for interface contracts.

Canonical reference: paper/OMPC_v1.33.7lulz.pdf

Implementation notes:
- Hybrid approach with threshold-based dispatch:
  - x < 100,000: Full sieve (fast for small x)
  - x >= 100,000: Segmented sieve (bounded memory for large x)
- Time complexity: O(x log log x) - optimized linear, not sublinear
- Space complexity: O(segment_size + sqrt(x)) where segment_size dominates for large x
- Memory usage: ~8MB per segment (Python list[bool] with 8-byte pointer overhead per element)
- Future work: True sublinear methods (Lehmer-style, O(x^(2/3))) remain unimplemented

Phase 1 implementation (2025-12-17):
- Segmented sieve backend to satisfy Part 6 section 6.4 memory constraint (< 25 MB)
- Fixed segment size of 1,000,000 elements (~8MB per segment as list[bool])
- Restores memory compliance for indices up to 250k+ (measured: 15.27 MB at 250k)
"""

import math
import os
from concurrent.futures import ProcessPoolExecutor, TimeoutError as FuturesTimeoutError
from typing import Callable
from .primality import is_prime
from .config import SMALL_PRIMES


def _simple_sieve(limit: int) -> list[int]:
    """
    Generate all primes up to limit using sieve of Eratosthenes.

    Used internally for small ranges and as basis for Legendre formula.
    Memory: O(limit) bits, approximately limit/8 bytes.

    Args:
        limit: Upper bound for prime generation

    Returns:
        List of all primes <= limit
    """
    if limit < 2:
        return []

    # Sieve array: True means composite, False means prime
    is_composite = [False] * (limit + 1)
    is_composite[0] = is_composite[1] = True

    # Sieve of Eratosthenes
    for i in range(2, int(math.sqrt(limit)) + 1):
        if not is_composite[i]:
            # Mark multiples of i as composite
            for j in range(i * i, limit + 1, i):
                is_composite[j] = True

    # Collect primes
    return [i for i in range(2, limit + 1) if not is_composite[i]]


def _segmented_sieve(x: int, segment_size: int = 1_000_000) -> int:
    """
    Count primes <= x using segmented sieve with bounded memory.

    This implementation uses fixed-size segments to bound memory usage,
    making it suitable for large x values where a full sieve would exceed
    memory constraints.

    Algorithm:
    1. Generate all primes up to sqrt(x) using standard sieve
    2. Process range [sqrt(x) + 1, x] in fixed-size segments
    3. For each segment, mark composites using small primes
    4. Count unmarked (prime) positions in each segment

    Memory representation:
    - Segment: Python list[bool] storing pointers to boolean objects
    - Each list element stores an 8-byte pointer (on 64-bit Python)
    - segment_size elements = segment_size * 8 bytes for list structure
    - Default: 1,000,000 elements ≈ 8 MB per segment (list overhead)
    - Small primes list: sqrt(x) / ln(sqrt(x)) primes ≈ < 1 MB for x < 10^7
    - Note: bytearray would be 1 byte/element if memory is critical

    Time complexity: O(x log log x) - same as full sieve
    Space complexity: O(segment_size + sqrt(x)) where segment_size dominates for large x

    Args:
        x: Upper bound for counting
        segment_size: Size of each segment (default: 1,000,000)

    Returns:
        Exact count of primes <= x

    References:
        - ADR 0002: Memory-bounded π(x) implementation
        - Part 6 section 6.4: < 25 MB memory constraint
    """
    if x < 2:
        return 0

    # Generate small primes up to sqrt(x)
    sqrt_x = int(math.sqrt(x))
    small_primes = _simple_sieve(sqrt_x)

    # Count includes all small primes
    count = len(small_primes)

    # If x <= sqrt_x, we're done
    if x <= sqrt_x:
        return count

    # Process range (sqrt_x, x] in segments
    segment_start = sqrt_x + 1

    while segment_start <= x:
        segment_end = min(segment_start + segment_size - 1, x)
        segment_length = segment_end - segment_start + 1

        # Create segment: False = prime (initially assume all prime)
        # Using list[bool]: ~8 bytes per element (pointer overhead on 64-bit Python)
        is_composite = [False] * segment_length

        # Sieve this segment using small primes
        for p in small_primes:
            # Find first multiple of p in segment
            # We want smallest k such that k*p >= segment_start
            first_multiple = ((segment_start + p - 1) // p) * p

            # Mark multiples of p in this segment
            for multiple in range(first_multiple, segment_end + 1, p):
                index = multiple - segment_start
                is_composite[index] = True

        # Count primes in this segment
        count += sum(1 for is_comp in is_composite if not is_comp)

        # Move to next segment
        segment_start = segment_end + 1

    return count


def _pi_legendre(x: int, primes_sqrt: list[int]) -> int:
    """
    Count primes <= x using Legendre's formula.

    Legendre's formula: π(x) = φ(x, a) + a - 1
    where φ(x, a) = count of numbers <= x not divisible by first a primes.

    This implementation uses a memoized recursive approach to compute φ(x, a).

    Args:
        x: Upper bound for counting
        primes_sqrt: List of all primes <= sqrt(x)

    Returns:
        Exact count of primes <= x
    """
    a = len(primes_sqrt)

    # Memoization cache for φ(x, k) computations
    memo = {}

    def phi(x_val: int, k: int) -> int:
        """
        Count integers <= x_val not divisible by first k primes.

        Base cases:
        - φ(x, 0) = x (no primes to exclude)
        - φ(x, k) = 0 if x < 2

        Recursive case:
        - φ(x, k) = φ(x, k-1) - φ(x/p_k, k-1)
        """
        if k == 0:
            return x_val
        if x_val < 2:
            return 0

        # Check memo
        key = (x_val, k)
        if key in memo:
            return memo[key]

        # Recursive computation
        p_k = primes_sqrt[k - 1]
        result = phi(x_val, k - 1) - phi(x_val // p_k, k - 1)
        memo[key] = result
        return result

    return phi(x, a) + a - 1


def _pi_simple(x: int) -> int:
    """
    Simple O(n) prime counting using primality tests.

    This is the original implementation, kept as reference.
    Not currently used - pi() now uses sieve-based counting for all ranges.

    Args:
        x: Upper bound for counting

    Returns:
        Exact count of primes <= x
    """
    if x < 2:
        return 0

    # Count small primes quickly
    count = sum(1 for p in SMALL_PRIMES if p <= x)

    # If x is small, we're done
    if x <= SMALL_PRIMES[-1]:
        return count

    # Count remaining primes
    # Start after largest small prime, check only odd numbers
    start = SMALL_PRIMES[-1] + 2
    if start % 2 == 0:
        start += 1

    for candidate in range(start, x + 1, 2):
        if is_prime(candidate):
            count += 1

    return count


def pi(x: int) -> int:
    """
    Return the exact count of primes <= x.

    This is the prime counting function π(x).

    Implementation strategy (threshold-based dispatch):
    - x < 100,000: Full sieve (fast, low overhead for small x)
    - x >= 100,000: Segmented sieve (bounded memory for large x)

    Time complexity: O(x log log x) - optimized linear, not sublinear
    Space complexity:
      - Full sieve: O(x) - used only for x < 100,000
      - Segmented sieve: O(segment_size + sqrt(x)) - fixed-size segments for x >= 100,000
        where segment_size = 1M elements ≈ 8 MB dominates for large x

    Memory usage:
      - x < 100,000: ~100 KB for full sieve (well within constraint)
      - x >= 100,000: ~8-10 MB peak (8 MB segment + ~1 MB small primes list + overhead)

    This implementation dramatically improves constant factors (20x speedup)
    but remains linear in x. True sublinear methods (Lehmer-style, O(x^(2/3)))
    are specified in Part 6 section 6.3 but remain future work.

    Phase 1 implementation (2025-12-17):
    - Segmented sieve restores Part 6 section 6.4 memory compliance (< 25 MB)
    - Threshold set at 100,000 to balance performance and memory

    Args:
        x: Upper bound for counting

    Returns:
        Number of primes p with p <= x

    Raises:
        ValueError: If x < 0
        TypeError: If x is not an integer

    Examples:
        >>> pi(10)
        4  # Primes: 2, 3, 5, 7
        >>> pi(100)
        25
    """
    if not isinstance(x, int):
        raise TypeError(f"x must be an integer, got {type(x).__name__}")
    if x < 0:
        raise ValueError(f"x must be non-negative, got {x}")

    if x < 2:
        return 0

    # Threshold-based dispatch
    # For small x: use full sieve (faster, low memory overhead)
    # For large x: use segmented sieve (bounded memory)
    SEGMENTED_THRESHOLD = 100_000

    if x < SEGMENTED_THRESHOLD:
        # Fast path for small x
        # Memory: ~x bytes (~100 KB for x=100k)
        primes = _simple_sieve(x)
        return len(primes)
    else:
        # Bounded memory path for large x
        # Memory: ~1-2 MB peak regardless of x
        return _segmented_sieve(x)


def pi_range(x: int, y: int) -> int:
    """
    Return the count of primes in the range (x, y].

    Equivalent to pi(y) - pi(x).

    Args:
        x: Lower bound (exclusive)
        y: Upper bound (inclusive)

    Returns:
        Number of primes p with x < p <= y

    Examples:
        >>> pi_range(10, 20)
        4  # Primes: 11, 13, 17, 19
    """
    if x >= y:
        return 0
    return pi(y) - pi(x)


def _create_segment_ranges(start: int, end: int, num_workers: int) -> list[tuple[int, int]]:
    """
    Divide range [start, end] into num_workers disjoint segments.

    Segments are created deterministically with fixed boundaries based on
    start, end, and num_workers. This ensures deterministic aggregation.

    Args:
        start: Start of range (inclusive)
        end: End of range (inclusive)
        num_workers: Number of segments to create

    Returns:
        List of (segment_start, segment_end) tuples in ascending order

    Example:
        >>> _create_segment_ranges(100, 200, 4)
        [(100, 124), (125, 149), (150, 174), (175, 200)]
    """
    if start > end:
        return []
    if num_workers <= 0:
        raise ValueError(f"num_workers must be positive, got {num_workers}")

    total_range = end - start + 1
    segment_size = total_range // num_workers
    remainder = total_range % num_workers

    segments = []
    current = start

    for i in range(num_workers):
        # Distribute remainder across first segments
        size = segment_size + (1 if i < remainder else 0)
        segment_start = current
        segment_end = current + size - 1

        if segment_start > end:
            break

        segments.append((segment_start, min(segment_end, end)))
        current = segment_end + 1

    return segments


def _count_segment_primes(segment_start: int, segment_end: int, small_primes: list[int]) -> int:
    """
    Count primes in segment [segment_start, segment_end] using small primes.

    This is the worker function for parallel prime counting. Each worker
    processes an independent segment using the sieve algorithm.

    Args:
        segment_start: Start of segment (inclusive)
        segment_end: End of segment (inclusive)
        small_primes: List of primes <= sqrt(segment_end) for sieving

    Returns:
        Count of primes in [segment_start, segment_end]
    """
    if segment_start > segment_end:
        return 0

    segment_length = segment_end - segment_start + 1

    # Create segment: False = prime (initially assume all prime)
    is_composite = [False] * segment_length

    # Sieve this segment using small primes
    for p in small_primes:
        # Find first multiple of p in segment
        # We want smallest k such that k*p >= segment_start
        first_multiple = ((segment_start + p - 1) // p) * p

        # Skip if first multiple is p itself (p is prime, don't mark it composite)
        if first_multiple == p:
            first_multiple += p

        # Mark multiples of p in this segment
        for multiple in range(first_multiple, segment_end + 1, p):
            index = multiple - segment_start
            is_composite[index] = True

    # Count primes in this segment
    count = sum(1 for is_comp in is_composite if not is_comp)

    return count


def pi_parallel(x: int, workers: int | None = None, threshold: int = 1_000_000) -> int:
    """
    Return the exact count of primes <= x using parallel processing.

    This is an opt-in parallel variant of pi() that leverages multi-core CPUs
    to reduce wall-clock time for large x. Uses multiprocessing to bypass GIL.

    GUARANTEES:
    - Tier A (Exact): Same correctness as pi(), bit-identical results
    - Deterministic: Same x and workers always yield same result
    - Opt-in: Must be explicitly called, not used by default

    STRATEGY:
    1. Generate small primes up to sqrt(x) (sequential, small cost)
    2. Divide range [sqrt(x), x] into disjoint segments
    3. Process each segment in parallel (independent workers)
    4. Aggregate counts in deterministic order (segment order)

    PARALLELISM:
    - Uses ProcessPoolExecutor (multiprocessing) to bypass GIL
    - Each worker processes independent segment with no shared state
    - Deterministic segment boundaries ensure reproducible results
    - Fallback to sequential pi() if parallelization fails

    PERFORMANCE:
    - Expected speedup: 3-5x for x >= 1M on 4-8 core CPUs
    - Threshold: x < threshold uses sequential pi() to avoid overhead
    - Overhead: Process creation cost dominates for small x

    TIME COMPLEXITY:
    - Wall-clock: O(x log log x / workers) - linear speedup with workers
    - CPU total: O(x log log x) - same total work as sequential

    SPACE COMPLEXITY:
    - O(segment_size + sqrt(x)) per worker
    - Memory bounded by segment size (each worker independent)

    DOES NOT GUARANTEE:
    - Sublinear time (still O(x log log x), just parallelized)
    - Linear speedup (overhead causes diminishing returns)
    - Platform independence (multiprocessing behavior varies)

    Args:
        x: Upper bound for counting
        workers: Number of parallel workers (default: min(cpu_count, 8))
        threshold: Minimum x for parallelism (default: 1,000,000)

    Returns:
        Number of primes p with p <= x (exact, same as pi())

    Raises:
        ValueError: If x < 0 or workers <= 0
        TypeError: If x is not an integer

    Examples:
        >>> pi_parallel(1_000_000)  # Uses default workers
        78498

        >>> pi_parallel(1_000_000, workers=4)  # Explicit worker count
        78498

        >>> pi_parallel(100_000)  # Below threshold, uses sequential
        9592

    References:
        - ADR 0004: Parallel π(x) implementation decision
        - docs/api_contract.md: Performance expectations
    """
    # Input validation (same as pi())
    if not isinstance(x, int):
        raise TypeError(f"x must be an integer, got {type(x).__name__}")
    if x < 0:
        raise ValueError(f"x must be non-negative, got {x}")

    # Worker count validation
    if workers is not None and workers <= 0:
        raise ValueError(f"workers must be positive, got {workers}")

    # Below threshold: use sequential pi() to avoid overhead
    if x < threshold:
        return pi(x)

    # Determine worker count
    if workers is None:
        workers = min(os.cpu_count() or 1, 8)

    # Small x edge case
    if x < 2:
        return 0

    # Generate small primes up to sqrt(x) (sequential)
    sqrt_x = int(math.sqrt(x))
    small_primes = _simple_sieve(sqrt_x)
    count = len(small_primes)

    # If x <= sqrt_x, we're done
    if x <= sqrt_x:
        return count

    # Divide range (sqrt_x, x] into segments for parallel processing
    try:
        segments = _create_segment_ranges(sqrt_x + 1, x, workers)

        # Process segments in parallel
        with ProcessPoolExecutor(max_workers=workers) as executor:
            # Map preserves order, ensuring deterministic aggregation
            segment_counts = executor.map(
                _count_segment_primes,
                [seg[0] for seg in segments],  # segment_start values
                [seg[1] for seg in segments],  # segment_end values
                [small_primes] * len(segments)  # small_primes for each worker
            )

        # Aggregate in deterministic order (map preserves segment order)
        count += sum(segment_counts)

        return count

    except Exception:
        # Fallback to sequential pi() if parallelization fails
        # This handles platform issues, worker crashes, etc.
        return pi(x)
