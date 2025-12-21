#!/usr/bin/env bash
#
# Run all lulzprime benchmarks and generate comparison report.
#
# Usage:
#   ./run_all.sh [output_dir]
#
# If output_dir is not provided, creates benchmarks/results/<timestamp>_<hostname>

set -euo pipefail

# Determine output directory
if [ $# -eq 1 ]; then
    OUTPUT_DIR="$1"
else
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    HOSTNAME=$(hostname -s)
    OUTPUT_DIR="benchmarks/results/${TIMESTAMP}_${HOSTNAME}"
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"
echo "Output directory: $OUTPUT_DIR"

# Capture environment info
echo "==> Capturing environment information..."
python3 benchmarks/harness/env_info.py > "$OUTPUT_DIR/env_info.txt"
python3 benchmarks/harness/env_info.py > /dev/null  # Also creates env_info.json
mv env_info.json "$OUTPUT_DIR/env_info.json"

# Benchmark parameters
RESOLVE_INDICES=(10000 100000 250000 500000)
PI_BOUNDS=(1000000 10000000 100000000)
FORECAST_BOUNDS=(1000000 100000000 1000000000)
FORECAST_REFINEMENTS=(1 2)
SIMULATE_STEPS=(10000 100000 1000000)
SEED=42

# Run resolve() benchmarks
echo ""
echo "==> Running resolve() benchmarks..."
for n in "${RESOLVE_INDICES[@]}"; do
    echo "  resolve($n)..."
    python3 benchmarks/pyperf/bench_resolve.py \
        --index "$n" \
        -o "$OUTPUT_DIR/resolve_${n}.json" \
        --quiet
done

# Run pi() benchmarks
echo ""
echo "==> Running pi() benchmarks..."
for x in "${PI_BOUNDS[@]}"; do
    echo "  pi($x)..."
    python3 benchmarks/pyperf/bench_pi.py \
        --upper-bound "$x" \
        -o "$OUTPUT_DIR/pi_${x}.json" \
        --quiet
done

# Run forecast() benchmarks
echo ""
echo "==> Running forecast() benchmarks..."
for n in "${FORECAST_BOUNDS[@]}"; do
    for r in "${FORECAST_REFINEMENTS[@]}"; do
        echo "  forecast($n, refinement_level=$r)..."
        python3 benchmarks/pyperf/bench_forecast.py \
            --upper-bound "$n" \
            --refinement-level "$r" \
            -o "$OUTPUT_DIR/forecast_${n}_r${r}.json" \
            --quiet
    done
done

# Run simulate() benchmarks - list mode
echo ""
echo "==> Running simulate() benchmarks (list mode)..."
for N in "${SIMULATE_STEPS[@]}"; do
    echo "  simulate($N, seed=$SEED)..."
    python3 benchmarks/pyperf/bench_simulate.py \
        --n-steps "$N" \
        --seed "$SEED" \
        -o "$OUTPUT_DIR/simulate_${N}.json" \
        --quiet
done

# Run simulate() benchmarks - generator mode
echo ""
echo "==> Running simulate() benchmarks (generator mode)..."
for N in "${SIMULATE_STEPS[@]}"; do
    echo "  simulate($N, seed=$SEED, as_generator=True)..."
    python3 benchmarks/pyperf/bench_simulate.py \
        --n-steps "$N" \
        --seed "$SEED" \
        --generator-mode \
        -o "$OUTPUT_DIR/simulate_${N}_gen.json" \
        --quiet
done

echo ""
echo "==> All benchmarks complete!"
echo "Results written to: $OUTPUT_DIR"
echo ""
echo "To compare versions, run:"
echo "  python3 benchmarks/harness/compare.py \\"
echo "    <v0.1.2_results_dir> <v0.2.0_results_dir> summary.md"
