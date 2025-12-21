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

## 2. New Features (v0.2.0)

### 2.1 JSON Export Support

Added in `simulator.py` for structured export of simulation results.

**Functions:**
- `simulation_to_json(sequence, *, n_steps, seed, anneal_tau, ...) -> dict`
- `simulation_to_json_string(sequence, ...) -> str`

**Schema: lulzprime.simulation.v0.2**

```python
{
  "schema": "lulzprime.simulation.v0.2",
  "params": {
    "n_steps": int,
    "seed": int | null,
    "anneal_tau": float | null,
    "beta_initial": float,
    "beta_decay": float,
    "initial_q": int,
    "as_generator": bool
  },
  "sequence": [int, ...],
  "diagnostics": [dict, ...] | null,
  "meta": {
    "library": "lulzprime",
    "version": "0.1.2",
    "timestamp": null  # Always null for determinism
  }
}
```

**Python Usage:**
```python
from lulzprime import simulate, simulation_to_json, simulation_to_json_string

# Basic export
seq = simulate(100, seed=42)
json_data = simulation_to_json(seq, n_steps=100, seed=42)

# With diagnostics
seq, diag = simulate(100, seed=42, diagnostics=True)
json_data = simulation_to_json(seq, n_steps=100, seed=42, diagnostics=diag)

# Deterministic JSON string
json_str = simulation_to_json_string(seq, n_steps=100, seed=42)
# Uses sort_keys=True for deterministic output
```

**Key Features:**
- Deterministic output (sorted keys, no timestamps)
- All values JSON-safe (stdlib json module)
- Captures all simulation parameters for reproducibility
- Supports diagnostics records when available

**Use Cases**: Save sequences for offline analysis, sharing results, archival, or integration with web dashboards.

### 2.2 Command-Line Interface (CLI)

Basic CLI added using `argparse` (stdlib only). Entry point: `python -m lulzprime`

**Available Commands:**

#### resolve
Get the exact nth prime (Tier A: Exact)

```bash
python -m lulzprime resolve <n>

# Examples
python -m lulzprime resolve 100000
# Output: 1299709

python -m lulzprime resolve 1
# Output: 2
```

**Arguments:**
- `n`: Prime index (1-based, must be >= 1)

**Errors:**
- Returns exit code 1 with error message for invalid input

#### pi
Count primes <= x (Tier B: π(x) function)

```bash
python -m lulzprime pi <x>

# Examples
python -m lulzprime pi 1000000
# Output: 78498

python -m lulzprime pi 100
# Output: 25
```

**Arguments:**
- `x`: Upper bound (must be >= 2)

#### simulate
Generate pseudo-primes using OMPC simulation (Tier C: statistical)

```bash
python -m lulzprime simulate <n_steps> [OPTIONS]

# Basic usage
python -m lulzprime simulate 1000 --seed 42
# Output: 1000 pseudo-prime values, one per line

# Generator mode (low memory, streaming)
python -m lulzprime simulate 1000000 --seed 42 --generator

# With annealing (reduced early variance)
python -m lulzprime simulate 50000 --seed 1337 --anneal-tau 10000

# Export to JSON
python -m lulzprime simulate 100 --seed 42 --json output.json
```

**Arguments:**
- `n_steps`: Number of steps to simulate (must be > 0)

**Options:**
- `--seed SEED`: Random seed for reproducibility (default: None, non-deterministic)
- `--anneal-tau TAU`: Annealing time constant (must be > 0, default: None)
- `--generator`: Stream results with O(1) memory (default: False)
- `--json FILENAME`: Export results to JSON file (default: None, text output)

**Output Modes:**
- **Text (default)**: One value per line to stdout
- **JSON (--json)**: Writes JSON to specified file, confirmation message to stderr

**Important:** simulate() generates pseudo-primes that are statistically prime-like but NOT exact primes. Use for testing and analysis only.

**Help:**
```bash
python -m lulzprime --help              # Show all commands
python -m lulzprime resolve --help      # Command-specific help
python -m lulzprime simulate --help     # Simulate options
```

### 2.3 Configuration and Defaults

Default values defined in `config.py`:
- `SIMULATOR_BETA_INITIAL = 2.0`
- `SIMULATOR_BETA_DECAY = 1.0`
- `SIMULATOR_INITIAL_Q = 2`
- `SIMULATOR_DEFAULT_SEED = None`
- `ENABLE_LEHMER_PI = True` (Meissel-Lehmer backend enabled by default in v0.2.0)

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

## 4. README Updates

README now includes:

**CLI Quickstart Section:**
- resolve, pi, simulate commands with examples
- All CLI flags documented (--seed, --anneal-tau, --generator, --json)
- Help text references

**Python API Quickstart:**
- forecast() with refinement_level parameter
- simulate() with as_generator and anneal_tau
- simulation_to_json() and simulation_to_json_string() examples
- Tier C simulation guarantees and limitations

**Use Cases:**
| Task                          | Command / Code Example                               |
|-------------------------------|------------------------------------------------------|
| Exact nth prime               | `python -m lulzprime resolve 100000`                 |
| Count primes                  | `python -m lulzprime pi 1000000`                     |
| Forecast large n              | `forecast(10**8, refinement_level=2)`                |
| Generate pseudo-primes        | `python -m lulzprime simulate 1000 --seed 42`        |
| Streaming simulation          | `simulate(10**6, seed=42, as_generator=True)`        |
| Export to JSON                | `python -m lulzprime simulate 100 --seed 42 --json out.json` |

## 5. Non-Goals (Reaffirmed)

- No GUI, web server, or heavy dependencies.
- No automatic internet lookups (e.g., prime tables).
- No breaking changes to core API.

These extensions make lulzprime not just powerful, but actually pleasant to use—because science should be accessible, scriptable, and a little bit fun.

**Next:** Part 9 - Historical and Maintenance.