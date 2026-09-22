# Intellectual Property Trust Protocol

**Sovereign Monorepo Structure — BEL-ESPRIT-D-ACCORD-TRUST-HOLDINGS**

Trust: Bel Esprit D'Accord Irrevocable Trust | EIN: 42-697643
License: Sovereign Source License v3.0
WORM: Ed25519 + Blake3 sealed
Prime Seal: 3,602,879,701,896,390 (product of primes 2,3,5,7,11,13,17,19,23,29,31,37)

---

## Monorepo Language Map

Every file in this repository is tagged to a language family.
The language structure maps to the Sedona Spine prime layer system.

```
sovereign-cuda-kernels/
├── src/                        # Source by language (canonical)
│   ├── python/                 # Prime 5 (MoE) + Prime 19 (Adaptive)
│   │   ├── crypto/             # AES, ZK-STARK, PQC, Quantum Euclid
│   │   ├── quantum-stack/      # Mamba, MoE router, Taylor, multiplicity
│   │   ├── security/           # HW security, extraction defense
│   │   ├── weights/            # GGUF spec, tensor layouts
│   │   ├── tests/              # Integration + unit tests
│   │   ├── build/              # CMake/Meson build scripts
│   │   └── docs/               # Model card
│   ├── fortran/                # Prime 3 (Quantum compute)
│   │   ├── quantum/            # oracle_eval, Grover, QAOA, MPS compress
│   │   └── mamba/              # SSM state transitions
│   ├── asm/                    # Prime 2 (Hardware)
│   │   ├── x86-65c02/          # 6502 firmware (coordinator, TQC braid)
│   │   ├── arm32/              # ARM32 variants
│   │   ├── ptx/                # PTX NVIDIA compute kernels
│   │   ├── boot/               # Boot chain, heartbeat
│   │   └── unified/            # Sovereign unified controller
│   ├── cuda/                   # Prime 2 (Hardware) + Prime 11 (DMA)
│   │   └── mamba2/             # CUDA Mamba2 SSM implementation
│   ├── gpu/                    # Prime 2 (Hardware) — GPU ISA
│   │   ├── sass/               # NVIDIA SASS assembly
│   │   └── futhark/            # Futhark GPU functional kernels
│   ├── formal/                 # Prime 13 (Security) + Prime 29 (LiquidLean)
│   │   ├── easycrypt/          # EasyCrypt cryptographic proofs
│   │   ├── fstar/              # F* proofs
│   │   ├── qsharp/             # Q# quantum circuits
│   │   └── lean4/              # Lean4 formal proofs
│   ├── verilog/                # Prime 2 (Hardware) — RTL
│   └── logic/                  # Prime 17 (Dream) — Logtalk + M logic
├── kernels/                    # Current organization (migrating to src/)
├── skunk/                      # Research sector (NIST + novel contributions)
├── rom/                        # Minted ROM firmware (O_2 HARDWARE_ROOT)
├── .github/workflows/          # CI/CD
├── README.md                   # Trust manifest + Sedona Spine
├── SOVEREIGN_TRUST_MANIFEST.md # Layer map + pipeline history
├── ENCRYPTION_PRIOR_ART_REGISTRY.md  # Encryption schemes + monetary-value inventory
└── IP_TRUST_PROTOCOL.md        # This document
```

---

## Current File → Language Family Map

### Python (src/python/)

| Current Path | Target Path | Sedona Prime |
|-------------|-------------|-------------|
| kernels/crypto/sovereign_aes256_gcm.py | src/python/crypto/ | P5, P13 |
| kernels/crypto/sovereign_quantum_euclid.py | src/python/crypto/ | P5, P13 |
| kernels/crypto/sovereign_quantum_euclid_reductions.py | src/python/crypto/ | P5, P13 |
| kernels/crypto/sovereign_quantum_resilience_lab.py | src/python/crypto/ | P5, P13 |
| kernels/crypto/sovereign_pqc_worm.py | src/python/crypto/ | P5, P13 |
| kernels/crypto/sovereign_omega_zkstark.py | src/python/crypto/ | P5, P13 |
| kernels/crypto/sovereign_zkstark_circuit.py | src/python/crypto/ | P5, P13 |
| kernels/crypto/sovereign_6502_tqc_braid_controller.py | src/python/crypto/ | P5, P2 |
| kernels/crypto/sovereign_6502_tqc_synthesis.py | src/python/crypto/ | P5, P2 |
| kernels/quantum-stack/sovereign_*.py | src/python/quantum-stack/ | P5, P7 |
| kernels/mamba2/mamba2_torch.py | src/python/cuda/ | P5, P11 |
| kernels/mamba2/build_mamba2.py | src/python/cuda/ | P5, P2 |
| kernels/mamba2/test_mamba2.py | src/python/tests/ | P5 |
| kernels/security/*.py | src/python/security/ | P13 |
| kernels/weights/*.py | src/python/weights/ | P7 |
| kernels/tests/*.py | src/python/tests/ | P5 |
| kernels/build/*.py | src/python/build/ | P2 |
| kernels/docs/*.py | src/python/docs/ | P17 |

### Fortran (src/fortran/)

| Current Path | Target Path | Sedona Prime |
|-------------|-------------|-------------|
| kernels/fortran/sovereign_quantum_search_kernels.f90 | src/fortran/quantum/ | P3 |
| kernels/quantum-stack/sovereign_quantum_kernels.f90 | src/fortran/quantum/ | P3 |
| kernels/quantum-stack/sovereign_taylor_contraction_mod.f90 | src/fortran/quantum/ | P3 |
| kernels/quantum-stack/sovereign_ewc_consolidation_kernel.f90 | src/fortran/mamba/ | P3, P17 |

### Assembly (src/asm/)

| Current Path | Target Path | Sedona Prime |
|-------------|-------------|-------------|
| kernels/crypto/sovereign_6502_tqc_braid_controller.asm | src/asm/x86-65c02/ | P2 |
| kernels/crypto/sovereign_6502_tqc_braid_controller_arm32.s | src/asm/arm32/ | P2 |
| kernels/hardware/sovereign_6502_coordinator_v2.asm | src/asm/x86-65c02/ | P2 |
| kernels/boot/sovereign_boot_chain.asm | src/asm/boot/ | P2 |
| kernels/boot/sovereign_heartbeat.asm | src/asm/boot/ | P2 |
| kernels/sovereign_unified/carry_propagation_sim.asm | src/asm/unified/ | P2 |
| kernels/sovereign_unified/sovereign_controller_v2026.asm | src/asm/unified/ | P2 |
| kernels/hyperkitty-pipeline/asm/*.ptx | src/asm/ptx/ | P2, P11 |
| kernels/hyperkitty-pipeline/asm/*.asm | src/asm/ptx/ | P2 |

### CUDA (src/cuda/)

| Current Path | Target Path | Sedona Prime |
|-------------|-------------|-------------|
| kernels/mamba2/mamba2.cu | src/cuda/mamba2/ | P2, P11 |
| kernels/mamba2/mamba2.h | src/cuda/mamba2/ | P2, P11 |

### GPU (src/gpu/)

| Current Path | Target Path | Sedona Prime |
|-------------|-------------|-------------|
| kernels/sass/*.sass | src/gpu/sass/ | P2 |
| kernels/futhark/*.fut | src/gpu/futhark/ | P2 |

### Formal Verification (src/formal/)

| Current Path | Target Path | Sedona Prime |
|-------------|-------------|-------------|
| kernels/crypto/ec/*.ec | src/formal/easycrypt/ | P13, P29 |
| kernels/crypto/fst/*.fst | src/formal/fstar/ | P13, P29 |
| kernels/crypto/qsharp/*.qs | src/formal/qsharp/ | P3, P29 |

### Verilog / SystemVerilog (src/verilog/)

| Current Path | Target Path | Sedona Prime |
|-------------|-------------|-------------|
| kernels/gdsii/sovereign_gdsii_constraints.v | src/verilog/ | P2 |
| kernels/hardware/sovereign_cycle_stealing_dma.sv | src/verilog/ | P11 |

### Logic (src/logic/)

| Current Path | Target Path | Sedona Prime |
|-------------|-------------|-------------|
| kernels/logic/sovereign_logic.m | src/logic/ | P17 |
| kernels/logic/sovereign_orchestrator.lgt | src/logic/ | P17 |
| kernels/sovereign_unified/sovereign_compile_unified.lgt | src/logic/ | P17 |

---

## IP Trust Hierarchy

```
Level 0: WORM Chain (Ed25519 + Blake3)
Level 1: Prior Art Registry (PAR-001 through PAR-018)
Level 2: Trust Manifest (SOVEREIGN_TRUST_MANIFEST.md)
Level 3: Encryption Registry (ENCRYPTION_PRIOR_ART_REGISTRY.md)
Level 4: IP Trust Protocol (this document)
Level 5: Source Files (with prior art headers)
Level 6: Skunk Sector (novel contribution documentation)
```

## Sedona Spine → Language Mapping

| Prime | Layer | Language Family |
|-------|-------|----------------|
| P2 | HARDWARE_ROOT | ASM (6502, ARM32, PTX), CUDA, SystemVerilog, SASS |
| P3 | QUANTUM_SUBSTRATE | Fortran (OMP+AVX512), Q# |
| P5 | MOE_INTELLIGENCE | Python (MoE, routing, inference) |
| P7 | CLASSICAL_SCALING | Python (weights, GGUF, dispatch) |
| P11 | CYCLE_STEALING | CUDA, ASM (DMA), Futhark |
| P13 | PARAMETER_SECURITY | Python (security), EasyCrypt, F* |
| P17 | DREAM_CONSOLIDATION | Logtalk, M logic, Python (EWC) |
| P19 | ADAPTIVE_LEARNING | Python (MAML, REINFORCE) |
| P23 | JORDAN_JST | Lean4 (JST formal), Haskell |
| P29 | LIQUIDLEAN | Lean4 + Liquid Haskell + HOC + m4 |
| P31 | WORM_TRAIL | Rust (WORM append), SHA3 chains |
| P37 | SOVEREIGN_ART | WebGPU/WASM, algorithmic art |

---

HashCommit: SHA3-512:IP_TRUST_PROTOCOL_MONOREPO_LANGUAGE_MAP_v2026_SNAPKITTYWEST
