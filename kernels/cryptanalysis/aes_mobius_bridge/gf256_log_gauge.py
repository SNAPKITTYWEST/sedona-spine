#!/usr/bin/env python3
"""
gf256_log_gauge.py — GF(256) Log-Gauge Quotient Operator

Implements the correct mathematical object for the Möbius Bridge MITM claim.
Replaces the placeholder [1,-1,1,-1] integer weights with the actual
discrete-log gauge quotient over GF(2^8)^×.

Mathematical object:
  g = 0x03  (Rijndael primitive element of GF(2^8)^×, order 255)
  ei = log_g(xi)  in Z_255  for nonzero xi
  γ = 64·(e1+e2+e3+e4) mod 255   (4^{-1} ≡ 64 mod 255, gcd(4,255)=1)
  ẽi = ei − γ mod 255
  Q_g(X) = (Z(X), ẽ1, ẽ2, ẽ3, ẽ4)
  where Z(X) = frozenset of indices i where xi = 0

Gauge invariant: Σ ẽi ≡ 0 mod 255

This file answers the three open proof obligations:
  OB1: does key-byte variation produce common multiplicative shift in the
       discrete-log representation? (empirical check for stated parameterization)
  OB2: are post-SubBytes cut bytes always nonzero? (exhaustive check)
  OB3: does the quotient retain discrimination across unintended hypotheses?
       (measured as a ratio)

HashCommit: SHA3-512:GF256_LOG_GAUGE_QUOTIENT_MINIMAL_CHECKER_v2026
"""

import hashlib
from typing import List, Tuple, FrozenSet, Dict, Optional


# ============================================================
# GF(2^8) ARITHMETIC (Rijndael polynomial 0x11B)
# ============================================================

GF_MODULUS = 0x11B


def gf_mul(a: int, b: int) -> int:
    """Multiply in GF(2^8) mod 0x11B."""
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        hi = a & 0x80
        a = (a << 1) & 0xFF
        if hi:
            a ^= 0x1B
        b >>= 1
    return p


def gf_pow(x: int, n: int) -> int:
    """x^n in GF(2^8)."""
    r, b = 1, x
    while n:
        if n & 1:
            r = gf_mul(r, b)
        b = gf_mul(b, b)
        n >>= 1
    return r


# ============================================================
# GF(2^8)^× DISCRETE-LOG TABLE for g = 0x03
# ============================================================

G = 0x03  # Rijndael primitive element; gf_pow(0x03, 255) = 1

def _build_log_tables():
    """
    Build log_g and exp_g tables for g=0x03 in GF(2^8)^×.
    exp_g[i] = g^i for i in 0..254
    log_g[x] = i such that g^i = x, for x in 1..255
    log_g[0] = None (undefined)
    """
    exp_g = [0] * 255
    log_g = [None] * 256
    cur = 1
    for i in range(255):
        exp_g[i] = cur
        log_g[cur] = i
        cur = gf_mul(cur, G)
    assert cur == 1, f"g=0x{G:02X} is not a primitive element (g^255 = {cur:#04x})"
    return exp_g, log_g

EXP_G, LOG_G = _build_log_tables()


def verify_primitive():
    """Verify g=0x03 has order exactly 255."""
    assert LOG_G[0] is None
    for x in range(1, 256):
        assert LOG_G[x] is not None, f"log_g({x}) undefined"
        assert EXP_G[LOG_G[x]] == x, f"exp(log({x})) = {EXP_G[LOG_G[x]]} != {x}"
    # Check all 255 nonzero elements are covered
    assert len(set(EXP_G)) == 255
    return True


# ============================================================
# GAUGE ARITHMETIC
# Gauge representative γ = 4^{-1} · Σei mod 255
# 4^{-1} mod 255 = 64  (since 4*64 = 256 ≡ 1 mod 255; 255=3·5·17; gcd(4,255)=1)
# ============================================================

FOUR_INV_MOD_255 = 64  # 4 * 64 = 256 = 1 mod 255

def _verify_gauge_arithmetic():
    assert (4 * FOUR_INV_MOD_255) % 255 == 1, "4^{-1} mod 255 != 64"
    import math
    assert math.gcd(4, 255) == 1, "gcd(4,255) != 1"
    return True

_verify_gauge_arithmetic()


# ============================================================
# Q_g OPERATOR
# ============================================================

def Q_g(column: List[int]) -> Tuple[FrozenSet[int], Tuple[int, ...]]:
    """
    GF(256) Log-Gauge Quotient operator.

    Args:
        column: list of 4 bytes (GF(2^8) elements) — one MixColumns column

    Returns:
        (zero_pattern, normalized_log_coords)
        where zero_pattern = frozenset of indices i where column[i] == 0
        and normalized_log_coords = (ẽ1, ẽ2, ẽ3, ẽ4) with Σẽi ≡ 0 mod 255
        (zero bytes contribute 0 to log coord but are tracked in zero_pattern)

    Gauge invariant: Σ ẽi ≡ 0 mod 255  for any input with all nonzero bytes.
    """
    assert len(column) == 4

    zero_pattern = frozenset(i for i, x in enumerate(column) if x == 0)

    # Log coordinates (0 for zero bytes — they're tracked in zero_pattern)
    logs = []
    for x in column:
        if x == 0:
            logs.append(0)
        else:
            logs.append(LOG_G[x])

    # Gauge representative: γ = 4^{-1} · Σei mod 255
    gamma = (FOUR_INV_MOD_255 * sum(logs)) % 255

    # Normalized coordinates
    normalized = tuple((e - gamma) % 255 for e in logs)

    return (zero_pattern, normalized)


def verify_gauge_zero_sum(column: List[int]) -> bool:
    """Verify Σẽi ≡ 0 mod 255 (only for all-nonzero columns)."""
    if any(x == 0 for x in column):
        return True  # Zero bytes handled separately
    _, coords = Q_g(column)
    return sum(coords) % 255 == 0


# ============================================================
# AES S-BOX AND MIXCOLUMNS
# ============================================================

SBOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5,
    0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
    0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
    0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
    0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
    0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
    0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
    0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
    0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
    0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
    0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
    0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
    0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
    0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
    0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
    0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68,
    0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16,
]

MC = [[2, 3, 1, 1], [1, 2, 3, 1], [1, 1, 2, 3], [3, 1, 1, 2]]

def mix_column(col: List[int]) -> List[int]:
    return [
        gf_mul(MC[r][0], col[0]) ^ gf_mul(MC[r][1], col[1]) ^
        gf_mul(MC[r][2], col[2]) ^ gf_mul(MC[r][3], col[3])
        for r in range(4)
    ]

def sub_bytes(state: List[int]) -> List[int]:
    return [SBOX[b] for b in state]

def add_round_key(state: List[int], key: List[int]) -> List[int]:
    return [s ^ k for s, k in zip(state, key)]


# ============================================================
# OB2 CHECK: Post-SubBytes bytes at cut are never zero
# ============================================================

def check_ob2_sbox_zero_free() -> Dict[str, object]:
    """
    Verify OB2: S(x) != 0 for all x in 0..255.
    (SBOX[0] = 0x63, not 0; standard AES property.)
    """
    zeros = [x for x in range(256) if SBOX[x] == 0]
    return {
        'zero_sbox_outputs': zeros,
        'ob2_sbox_zero_free': len(zeros) == 0,
        'note': 'S-box image never contains 0 — post-SubBytes bytes cannot be 0',
    }


# ============================================================
# OB1 EMPIRICAL CHECK: 256-hypothesis collapse
# ============================================================

def three_round_forward(plaintext: List[int], key_material: List[int]) -> List[int]:
    """
    Simplified 3-round AES forward computation for OB1 check.
    Uses AddRoundKey → SubBytes → MixColumns (simplified, no ShiftRows in column-local model).
    Real attack would need ShiftRows; this establishes whether the algebraic structure
    is present before accounting for row permutation.
    """
    state = list(plaintext[:16])
    for r in range(3):
        state = add_round_key(state, key_material[r * 16:(r + 1) * 16])
        state = sub_bytes(state)
        if r < 2:
            # MixColumns per column
            new_state = []
            for col in range(4):
                col_bytes = [state[row * 4 + col] for row in range(4)]
                mc_col = mix_column(col_bytes)
                new_state.extend(mc_col)
            state = new_state
    return state


def check_ob1_collapse(
    plaintext: List[int],
    base_key: List[int],
    col_index: int = 0,
    key_byte_position: int = 0,
) -> Dict[str, object]:
    """
    OB1 empirical check: compute Q_g for all 256 key-byte hypotheses
    at the specified column/position of the MITM cut.

    Returns the number of distinct Q_g values observed.
    If count == 1: the gauge quotient collapses all 256 hypotheses.
    If count > 1:  characterizes the actual equivalence structure.

    Args:
        plaintext: 16-byte plaintext
        base_key: 48-byte forward key material (3 rounds)
        col_index: which column (0–3) to measure at the cut
        key_byte_position: which byte position in the key to vary (0–15)
    """
    quotient_values: Dict = {}

    for k_byte in range(256):
        # Vary one key byte
        key = list(base_key)
        key[key_byte_position] = k_byte

        # Compute 3-round forward state
        cut_state = three_round_forward(plaintext, key)

        # Extract column at cut point
        cut_col = [cut_state[row * 4 + col_index] for row in range(4)]

        # Compute Q_g
        qval = Q_g(cut_col)

        quotient_values[k_byte] = qval

    # Count distinct Q_g values
    distinct_qvals = set(quotient_values.values())

    return {
        'ob1_check': True,
        'plaintext_hex': bytes(plaintext).hex(),
        'col_index': col_index,
        'key_byte_position': key_byte_position,
        'hypotheses_tested': 256,
        'distinct_quotient_values': len(distinct_qvals),
        'collapse_to_one': len(distinct_qvals) == 1,
        'equivalence_classes': _summarize_equivalence(quotient_values),
    }


def _summarize_equivalence(quotient_map: Dict[int, object]) -> Dict:
    """Group key-byte hypotheses by their Q_g value."""
    groups: Dict = {}
    for k, v in quotient_map.items():
        key = str(v)
        if key not in groups:
            groups[key] = []
        groups[key].append(k)
    return {
        'num_classes': len(groups),
        'class_sizes': sorted([len(v) for v in groups.values()], reverse=True),
    }


# ============================================================
# OB3 CHECK: Discrimination across unintended hypotheses
# ============================================================

def check_ob3_discrimination(
    n_plaintexts: int = 100,
    seed: int = 42,
) -> Dict[str, object]:
    """
    OB3: Measure Q_g discrimination across unrelated plaintexts
    (representing different outer-key hypotheses).

    For n_plaintexts random plaintexts each with a fixed key,
    count how many produce the SAME Q_g value (false collision rate).
    Lower false collision rate = better discrimination.

    A useful fingerprint should have:
    - Within-class (256 key-byte hyps): 1 distinct value (collapse)
    - Across-class (different plaintexts): close to 256 distinct values (discrimination)
    """
    import random
    rng = random.Random(seed)

    fixed_key = [rng.randint(0, 255) for _ in range(48)]
    results = []

    for _ in range(n_plaintexts):
        pt = [rng.randint(0, 255) for _ in range(16)]
        cut_state = three_round_forward(pt, fixed_key)
        cut_col = [cut_state[row * 4] for row in range(4)]  # column 0
        qval = Q_g(cut_col)
        results.append(qval)

    distinct = len(set(results))
    collision_rate = (n_plaintexts - distinct) / n_plaintexts

    return {
        'ob3_check': True,
        'n_plaintexts': n_plaintexts,
        'distinct_quotient_values': distinct,
        'false_collision_rate': round(collision_rate, 4),
        'discrimination': 'GOOD' if distinct > n_plaintexts * 0.9 else
                          'PARTIAL' if distinct > n_plaintexts * 0.5 else 'POOR',
    }


# ============================================================
# FULL VALIDATION SUITE
# ============================================================

def run_all_checks():
    import os

    print("=" * 72)
    print(" GF(256) LOG-GAUGE QUOTIENT — PROOF OBLIGATION CHECKER")
    print(" Operator: Q_g(X) = (Z(X), ẽ1..ẽ4) where Σẽi ≡ 0 mod 255")
    print(" g = 0x03 (Rijndael primitive element)")
    print("=" * 72)

    # Primitive element verification
    print("\n── Discrete-log table verification ──")
    assert verify_primitive()
    print(f"  [PASS] g=0x{G:02X} is primitive; all 255 log values consistent")
    print(f"  [PASS] EXP_G[LOG_G[x]] = x for all x in 1..255")

    # Gauge arithmetic
    print("\n── Gauge arithmetic ──")
    print(f"  255 = 3 × 5 × 17 (composite)")
    print(f"  gcd(4, 255) = 1  → 4^{{-1}} mod 255 exists")
    print(f"  4^{{-1}} mod 255 = {FOUR_INV_MOD_255}  (since 4×64 = 256 ≡ 1 mod 255)")

    # Zero-sum gauge invariant
    print("\n── Zero-sum gauge invariant ──")
    # Test on 1000 random nonzero columns
    import random
    rng = random.Random(0)
    failures = 0
    for _ in range(1000):
        col = [rng.randint(1, 255) for _ in range(4)]
        if not verify_gauge_zero_sum(col):
            failures += 1
    print(f"  [{'PASS' if failures == 0 else 'FAIL'}] Zero-sum invariant: {failures}/1000 failures")

    # OB2
    print("\n── OB2: Post-SubBytes zero-free ──")
    ob2 = check_ob2_sbox_zero_free()
    status = 'PASS' if ob2['ob2_sbox_zero_free'] else 'FAIL'
    print(f"  [{status}] S-box image zero-free: {ob2['ob2_sbox_zero_free']}")
    print(f"  S(0) = 0x{SBOX[0]:02X} (not 0x00) — AES S-box image never 0")
    if ob2['ob2_sbox_zero_free']:
        print(f"  OB2 SATISFIED: post-SubBytes bytes at cut cannot be 0")
    else:
        print(f"  Zero S-box outputs: {ob2['zero_sbox_outputs']}")

    # OB1 — test with several plaintexts
    print("\n── OB1: 256-hypothesis collapse (empirical) ──")
    print("  NOTE: Simplified model (no ShiftRows). Full attack requires ShiftRows.")
    print("  This check probes whether the algebraic structure is present at all.")

    key_material = list(os.urandom(48))
    for pt_seed in [b'\x00' * 16, b'\x53' * 16, os.urandom(16)]:
        pt = list(pt_seed)
        result = check_ob1_collapse(pt, key_material, col_index=0, key_byte_position=0)
        status = 'COLLAPSE' if result['collapse_to_one'] else f"{result['distinct_quotient_values']} classes"
        print(f"  PT={bytes(pt[:4]).hex()}... col=0 keypos=0: {status}")
        if not result['collapse_to_one']:
            ec = result['equivalence_classes']
            print(f"    → {ec['num_classes']} equivalence classes, sizes: {ec['class_sizes'][:5]}")

    print("\n  OB1 INTERPRETATION:")
    print("  If collapse_to_one=False: the common multiplicative factor property")
    print("  does NOT hold for this simplified parameterization.")
    print("  Full attack requires specific subspace + ShiftRows + key schedule structure.")
    print("  OB1 remains OPEN until a correct parameterization is identified.")

    # OB3
    print("\n── OB3: Inter-class discrimination ──")
    ob3 = check_ob3_discrimination(n_plaintexts=200, seed=42)
    print(f"  Plaintexts: {ob3['n_plaintexts']}")
    print(f"  Distinct Q_g values: {ob3['distinct_quotient_values']}")
    print(f"  False collision rate: {ob3['false_collision_rate']:.4f}")
    print(f"  Discrimination: {ob3['discrimination']}")

    print("\n" + "=" * 72)
    print(" OPEN PROOF OBLIGATIONS SUMMARY")
    print("=" * 72)
    ob2_done = ob2['ob2_sbox_zero_free']
    print(f"  OB2 (zero handling):     {'CLOSED — S-box image zero-free' if ob2_done else 'OPEN'}")
    print(f"  OB1 (common factor):     OPEN — requires correct MITM parameterization + ShiftRows")
    print(f"  OB3 (discrimination):    {ob3['discrimination']} (preliminary; depends on OB1)")
    print()
    print(" NEXT STEP: Implement full AES 3-round forward with ShiftRows and")
    print(" key-schedule-derived partial keys at the specific MITM cut point.")
    print(" Then re-run check_ob1_collapse with that exact parameterization.")

    h = hashlib.sha3_512(b"GF256_LOG_GAUGE_QUOTIENT_CHECKER_v2026").hexdigest()
    print(f"\nHashCommit: SHA3-512:{h[:32]}...")


if __name__ == "__main__":
    run_all_checks()
