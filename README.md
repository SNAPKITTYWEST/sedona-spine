# Sedona Spine

Public source record of the Sedona Spine prime-layer architecture, extracted from `sovereign-cuda-kernels` for prior-art publication.

The spine assigns prime-numbered operators to architectural layers and extends the layer sequence through successive source definitions. This repository preserves the original documents, source headers, authorship, and license. Copyright and attribution remain as stated in the individual files: Jessica / SNAPKITTYWEST / SnapKitty, with Ahmad Parr and Jessica Westerhoff credited where present in the source.

## Source map

| Layer sequence | Source |
| --- | --- |
| 8 primes, 2–19: hardware, quantum substrate, MoE, scaling, cycle stealing, security, consolidation, learning | [Trust manifest](SOVEREIGN_TRUST_MANIFEST.md) |
| 12 primes, 2–37: Jordan, LiquidLean, WORM, art extensions | [Parr papers](kernels/lean4/parr-papers/Parr_Papers_Formalized_v2026.lean) |
| 18 primes, 2–61: QAL extension | [QAL](kernels/lean4/qal/QAL_Formalized_v2026.lean) |
| 25 primes, 2–97: HK-DSL extension | [HK-DSL](kernels/lean4/hkdsl/HK_DSL_Formalized_v2026.lean), [tripartite definitions](kernels/lean4/HK_DSL_Tripartite.lean) |
| 32 primes, 2–131: witness stack extension | [Witness stack](kernels/lean4/proofs/SnapKitty_Proofs_Witness_Stack_v2026.lean) |
| 44 primes, 2–193: Boole/E7/GKN extension | [Boole/E7/GKN](kernels/lean4/boole-e7/Boole_E7_GKN_Formalized_v2026.lean) |
| 55 primes, 2–257: Mythos extension | [Mythos](kernels/lean4/mythos/Mythos_Cryptanalysis_Swarm_v2026.lean) |

The 55-prime source defines `all_55_primes` and `prime_seal_55`, the product of that list. The source documents also contain their layer descriptions, trust-scalar expressions, and accompanying declarations.

## Other representations

- [Prolog](kernels/proofs/symbolic_law/snapkitty_proofs.pl): `sedona_primes/1` and symbolic-law definitions.
- [Pipeline manifest](kernels/hyperkitty-pipeline/pipeline_constraint.xml): the spine's integration into the source pipeline document.
- [Language mapping](IP_TRUST_PROTOCOL.md): prime layers and their language families.

## Provenance

[PROVENANCE.json](PROVENANCE.json) records the extraction time, source checkout revision, original relative paths, byte lengths, and SHA-256 hashes for all 12 copied files. These files were copied unchanged from the local working tree. The complete containing files are retained so each spine definition remains in its original context; references to other parts of the original repository remain intact.

Dates and sealing statements inside the source files are preserved as supplied. This repository's Git history records this extraction and publication.

## License

The original [Sovereign Proprietary License](LICENSE) is retained. This repository is publicly visible as a source record; the original rights and attribution notices remain in effect.
## Cryptanalysis source collection

The original cryptanalysis directory is included with its source paths and headers preserved:

- [AES / Mobius bridge](kernels/cryptanalysis/aes_mobius_bridge/): algebraic structure, GF(256) log gauge, bridge search, differential-trail search, Lean declarations, and result documents.
- [Rhythmic Fibonacci phase engine](kernels/cryptanalysis/phase_engine/): Python implementation and accompanying Lean source.
- [Cryptanalysis paper](AHMAD_CRYPTANALYSIS_PAPER.md).
- [AES claim registry](AES_CLAIM_REGISTRY.md).
- [Encryption prior-art registry](ENCRYPTION_PRIOR_ART_REGISTRY.md).

[CRYPTOANALYSIS_PROVENANCE.json](CRYPTOANALYSIS_PROVENANCE.json) records SHA-256 hashes for these 15 unchanged source files. Claims and result labels in the copied documents belong to the supplied research record. Python imports include PuLP for differential-trail search; the Lean sources import Mathlib.
