# Lulzprime Development Manual - Part 8: Extensions and Usability

**Version:** 0.2.0 (Updated for usability enhancements in Q1 2026)  
**Author:** Roble Mumin  
**Date:** February 25, 2026 (Following primality/resolution tuning and forecasting refinements)  
**Reference:** Optimus Markov Prime Conjecture (OMPC) Paper v1.33.7lulz, December 2025 (Section 10: Applications and Practical Use Cases; References to SymPy, mpmath)  
**Status:** Added minor usability features, JSON export, enhanced CLI, and documented extension points. Core purity preserved.

This part of the manual covers **extensions, usability improvements, and integration points** introduced in v0.2.0 to make lulzprime more practical for everyday scripting, statistical analysis, and potential hybrid use with other tools. While the library remains pure Python with no external dependencies, these additions focus on developer experience, output flexibility, and future extensibility—without altering the core API or guarantees.

## 1. Usability Philosophy

- **Minimalism First**: Core functions remain simple and focused.
- **Progressive Enhancement**: Optional features for power users.
- **Fun Factor**: Keep the lulz alive—clear errors, helpful messages, and examples that spark joy.

## 2. New Minor Features (v0.2.0)

### 2.1 JSON Export Support
Added in `__init__.py` and `simulate.py` for easy serialization.

```python
from lulzprime import simulate_sequence, to_json

# List or generator → JSON-serializable dict
seq = list(simulate_sequence(max_n=10000, seed=42))
json_data = to_json(seq, metadata={"beta": 2.0, "seed": 42, "n": len(seq)})

# Outputs:
# {
#   "primes": [2, 3, 5, ..., 78498],
#   "count": 10000,
#   "metadata": {...},
#   "final_density_ratio": 0.991
# }
import json
print(json.dumps(json_data, indent=2))
```

**Use Cases**: Save sequences for offline analysis, web dashboards, or sharing results.

### 2.2 Enhanced CLI via config.py
Basic command-line interface added using `argparse` (stdlib).

```bash
# Examples
python -m lulzprime resolve 1000000          # → 15485863
python -m lulzprime forecast 100000000 --refinement 2
python -m lulzprime simulate --n 50000 --beta 2.0 --seed 1337 --json output.json
python -m lulzprime batch 1000000 1000100 1000200 --workers 8
```

**Features**:
- Progress bars via print statements (no tqdm dependency).
- JSON output flag.
- Help text with OMPC paper references.

### 2.3 Configuration and Flags
Centralized in `config.py`:
```python
class Config:
    DEFAULT_BETA = 2.0
    DEFAULT_REFINE_LEVEL = 2
    VERBOSE = False
    MAX_WORKERS = None  # os.cpu_count()
```

Accessible via module or CLI overrides.

## 3. Documented Extension Points

### 3.1 Custom Gap Distributions
Users can inject custom `base_p0` dict into simulation:
```python
custom_gaps = {2: 0.15, 4: 0.10, 6: 0.20, ...}  # Normalized
seq = simulate_sequence(..., base_distribution=custom_gaps)
```

**Use Case**: Test sensitivity to altered local statistics (paper Section 7).

### 3.2 Hybrid Usage Examples (Documented, Not Required)
While pure, users may combine with allowed external tools:
```python
# Example with SymPy (user-installed)
from sympy import prime as sympy_prime
assert resolve(1000000) == sympy_prime(1000000)

# Example with mpmath for ultra-precision logs (if available)
```

Documented in README and this manual as "optional ecosystem integration."

### 3.3 Parallel Batch Extensions
`resolve_many` now supports callback hooks (for progress GUIs in user apps).

## 4. README and Example Updates

- New "Quick Start" section with CLI and JSON examples.
- "Use Cases" table:
  | Task                      | Command / Code Example                     |
  |---------------------------|--------------------------------------------|
  | Exact nth prime           | `resolve(10**8)`                          |
  | Forecast large n          | `forecast(10**12, refinement_level=2)`    |
  | Generate pseudo-primes    | `simulate --n 100000 --json seq.json`     |
  | Batch lookup              | `batch 10**7 10**7+1000 ...`              |

- ASCII art reminder: "Keep the lulz alive."

## 5. Non-Goals (Reaffirmed)

- No GUI, web server, or heavy dependencies.
- No automatic internet lookups (e.g., prime tables).
- No breaking changes to core API.

These extensions make lulzprime not just powerful, but actually pleasant to use—because science should be accessible, scriptable, and a little bit fun.

**Next:** Part 9 - Historical and Maintenance.