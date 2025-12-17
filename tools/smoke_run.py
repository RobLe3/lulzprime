#!/usr/bin/env python3
"""
Smoke test for LULZprime.

Quick sanity check that basic functionality works.
Run this before committing changes.

Usage:
    python tools/smoke_run.py
"""

import sys


def smoke_test():
    """Run basic smoke tests."""
    print("=" * 60)
    print("LULZprime Smoke Test")
    print("=" * 60)

    try:
        import lulzprime
    except ImportError as e:
        print(f"❌ FAIL: Cannot import lulzprime: {e}")
        return False

    print(f"✓ Imported lulzprime version {lulzprime.__version__}")

    # Test resolve()
    try:
        p_10 = lulzprime.resolve(10)
        assert p_10 == 29, f"resolve(10) should be 29, got {p_10}"
        print(f"✓ resolve(10) = {p_10}")
    except Exception as e:
        print(f"❌ FAIL: resolve() test: {e}")
        return False

    # Test between()
    try:
        primes = lulzprime.between(2, 10)
        expected = [2, 3, 5, 7]
        assert primes == expected, f"between(2, 10) should be {expected}, got {primes}"
        print(f"✓ between(2, 10) = {primes}")
    except Exception as e:
        print(f"❌ FAIL: between() test: {e}")
        return False

    # Test is_prime()
    try:
        assert lulzprime.is_prime(17) is True
        assert lulzprime.is_prime(18) is False
        print("✓ is_prime() working")
    except Exception as e:
        print(f"❌ FAIL: is_prime() test: {e}")
        return False

    # Test next_prime()
    try:
        next_p = lulzprime.next_prime(10)
        assert next_p == 11, f"next_prime(10) should be 11, got {next_p}"
        print(f"✓ next_prime(10) = {next_p}")
    except Exception as e:
        print(f"❌ FAIL: next_prime() test: {e}")
        return False

    # Test forecast()
    try:
        estimate = lulzprime.forecast(100)
        assert estimate > 0, "forecast should return positive value"
        print(f"✓ forecast(100) = {estimate}")
    except Exception as e:
        print(f"❌ FAIL: forecast() test: {e}")
        return False

    # Test simulate()
    try:
        seq = lulzprime.simulate(10, seed=42)
        assert len(seq) == 10, f"simulate(10) should return 10 values, got {len(seq)}"
        print(f"✓ simulate(10) returned {len(seq)} values")
    except Exception as e:
        print(f"❌ FAIL: simulate() test: {e}")
        return False

    print("=" * 60)
    print("✓ All smoke tests passed!")
    print("=" * 60)
    return True


if __name__ == "__main__":
    success = smoke_test()
    sys.exit(0 if success else 1)
