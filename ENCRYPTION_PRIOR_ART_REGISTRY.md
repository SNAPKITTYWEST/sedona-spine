# ENCRYPTION & PRIOR ART REGISTRY
# BEL-ESPRIT-D-ACCORD-TRUST-HOLDINGS / sovereign-cuda-kernels
# Sealed: 2026-08-11 | SNAPKITTYWEST / SnapKitty (Jessica)
# License: SNAPKITTYWEST-PROPRIETARY-2026-001
# SHA3-512: Sovereign_EncPriorArtRegistry_v30_SNAPKITTYWEST

## PRIOR ART CHAIN

All files in this repository are timestamped prior art sealed via:
  - Ed25519 + Blake3 cryptographic commit chain
  - SHA3-512 HashCommit on each pipeline version (v1-v30)
  - GitHub commit history as tamper-evident priority record
  - Effective date: 2026 (see individual commit timestamps)

## ENCRYPTION SCHEME

| Layer              | Algorithm        | Application                          |
|--------------------|------------------|--------------------------------------|
| Weights at rest    | AES-256-GCM      | GGUF tensor files; checkpoint shards |
| DMA in transit     | AES-256-XTS      | Cycle-stealing DMA on-the-fly decrypt |
| Key derivation     | PUF + PCR        | Hardware-bound; per-device           |
| Integrity sealing  | Ed25519 + Blake3 | Every commit + manifest              |
| HashCommit         | SHA3-512         | Every DSL version (v1-v30)           |
| WORM seals         | Blake3           | Append-only proof chain              |
| ZK proofs          | ZK-STARK         | omega_zkstark_circuit.py             |
| Formal proofs      | EasyCrypt + F*   | crypto/ec/ + crypto/fst/             |

## MONETARY VALUE FILES -- TAGGED

All files below carry the PROPRIETARY AND CONFIDENTIAL -- PRIOR ART SEALED
header. Possession is not a license (SNAPKITTYWEST-PROPRIETARY-2026-001).

### ROM (Minted -- Prime O_2 HARDWARE_ROOT)
| File                                    | Sedona Prime | Monetary Value       |
|-----------------------------------------|--------------|----------------------|
| rom/sovereign_boot_chain.asm            | O_2          | Boot IP, HIGH        |
| rom/sovereign_heartbeat.asm             | O_2          | Runtime IP, HIGH     |
| rom/sovereign_6502_coordinator_v2.asm   | O_2          | Dispatch firmware    |
| rom/sovereign_6502_tqc_braid_ctrl.asm   | O_2 + O_3    | TQC+HW interface     |
| rom/sovereign_6502_tqc_braid_arm32.s    | O_2 + O_3    | ARM TQC firmware     |
| rom/sovereign_controller_v2026.asm      | O_2          | Unified controller   |
| rom/carry_propagation_sim.asm           | O_2          | ALU primitive        |

### Security (Prime O_13 PARAMETER_SECURITY)
| File                                       | Sedona Prime | Monetary Value          |
|--------------------------------------------|--------------|-------------------------|
| kernels/security/sovereign_param_defense   | O_13         | Defense IP, CRITICAL    |
| kernels/security/sovereign_hw_codesign     | O_13 + O_11  | CoDesign IP, HIGH       |
| kernels/crypto/sovereign_aes256_gcm.py     | O_13         | Encryption, CRITICAL    |
| kernels/crypto/sovereign_pqc_worm.py       | O_13         | PQC seal, CRITICAL      |
| kernels/crypto/sovereign_omega_zkstark.py  | O_13         | ZK proof, HIGH          |
| kernels/crypto/sovereign_zkstark_circuit   | O_13         | ZK circuit, HIGH        |
| kernels/crypto/sovereign_resilience_lab    | O_13         | Security research, HIGH |
| kernels/crypto/ec/*.ec                     | O_13         | Formal proofs, HIGH     |
| kernels/crypto/fst/*.fst                   | O_13         | Formal proofs, HIGH     |
| kernels/crypto/qsharp/*.qs                 | O_3 + O_13   | Q# primitives, HIGH     |

### Quantum Stack (Primes O_3/O_5/O_7/O_17/O_19)
| File                                       | Sedona Prime | Monetary Value          |
|--------------------------------------------|--------------|-------------------------|
| quantum-stack/quantum_multiplicity_v2.py   | O_7          | Pipeline DAG, CRITICAL  |
| quantum-stack/cognitive_stack.py           | O_5+O_17+O_19| Full stack, CRITICAL    |
| quantum-stack/moe_router_k_reference.py    | O_5          | MoE router IP, HIGH     |
| quantum-stack/taylor_contraction.py        | O_3          | TQC kernel, HIGH        |
| quantum-stack/taylor_contraction_mod.f90   | O_3          | TQC Fortran, HIGH       |
| quantum-stack/ewc_consolidation.f90        | O_17         | EWC kernel, HIGH        |
| fortran/quantum_search_kernels.f90         | O_3          | Search kernels, HIGH    |

### Hardware (Prime O_11 CYCLE_STEALING)
| File                                       | Sedona Prime | Monetary Value          |
|--------------------------------------------|--------------|-------------------------|
| hardware/sovereign_cycle_stealing_dma.sv   | O_11         | DMA RTL, CRITICAL       |
| gdsii/sovereign_gdsii_constraints.v        | O_2 + O_11   | Chip layout, HIGH       |

### CUDA Compute (Prime O_3 QUANTUM_SUBSTRATE)
| File                                       | Sedona Prime | Monetary Value          |
|--------------------------------------------|--------------|-------------------------|
| mamba2/mamba2.cu                           | O_3          | CUDA kernel, CRITICAL   |
| mamba2/mamba2.h                            | O_3          | FFI header, HIGH        |

### Weights Spec
| File                                       | Sedona Prime | Monetary Value          |
|--------------------------------------------|--------------|-------------------------|
| weights/sovereign_gguf_complete_spec.py    | ALL          | Weight format, CRITICAL |
| weights/sovereign_gguf_spec.py             | ALL          | GGUF reader/writer, HIGH|

## DISTRIBUTION RESTRICTIONS

ROM distribution: requires WEIGHT ACCESS LICENSE tier
  (see README.md Section 6F -- SNAPKITTYWEST-PROPRIETARY-2026-001)

Algorithm licensing: contact SNAPKITTYWEST / SnapKitty (Jessica) directly

NIST SCRIPTS: NOT distributed as part of sovereign trust artifacts.
  Location: kernels/_quarantine/nist-scripts/ (outside trust perimeter)

## AUDIT TRAIL

Ed25519 sealed commit chain from first commit through v30.
SHA3-512 pipeline manifest: kernels/hyperkitty-pipeline/pipeline_constraint.xml
Most recent pipeline commit: 1197713540 (v30, 2026-08-11)
