"""
Configuration and default parameters for lulzprime.

Defines tunables, thresholds, and operational defaults.
See docs/manual/part_2.md for constraints.
"""

# Performance constraints (Part 2, section 2.5)
MAX_MEMORY_MB = 25  # Target maximum memory footprint

# Small primes cache for optimization
# These are used for quick lookups and divisibility checks
SMALL_PRIMES = [
    2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
    53, 59, 61, 67, 71, 73, 79, 83, 89, 97
]

# Forecast thresholds
# Below this index, use hardcoded lookup instead of analytic estimate
FORECAST_SMALL_THRESHOLD = 100

# π(x) implementation defaults
PI_CACHE_SIZE = 1000  # Configurable cache size for π(x) results

# Primality testing configuration
# For deterministic Miller-Rabin in 64-bit range
MILLER_RABIN_BASES_64BIT = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

# Diagnostic sampling rate (Part 7)
# Sample diagnostics every N steps to control overhead
DIAGNOSTIC_SAMPLE_RATE = 100

# Simulator defaults (Part 5, section 5.7)
SIMULATOR_DEFAULT_SEED = None  # None = random, int = deterministic
SIMULATOR_INITIAL_Q = 2
SIMULATOR_BETA_INITIAL = 1.0
SIMULATOR_BETA_DECAY = 0.99

# Parallel π(x) configuration (opt-in, ADR 0004)
# Note: These settings are for pi_parallel() only, NOT used by default resolve()
ENABLE_PARALLEL_PI = False  # Opt-in flag (not currently wired to auto-use)
PARALLEL_PI_WORKERS = 8  # Default worker count (capped at min(cpu_count, 8))
PARALLEL_PI_THRESHOLD = 1_000_000  # Minimum x for parallel (avoid overhead below)

# Lehmer π(x) configuration (opt-in, ADR 0005)
# IMPORTANT: _pi_lehmer() is currently a PLACEHOLDER delegating to segmented sieve
# True Meissel-Lehmer algorithm is not yet implemented
# This flag MUST remain False until true sublinear algorithm is validated
ENABLE_LEHMER_PI = False  # Opt-in flag - DISABLED until true algorithm implemented
LEHMER_PI_THRESHOLD = 5_000_000  # Threshold for Lehmer dispatch (if enabled)
