# CS340 LEBench Replication
Paper: An Analysis of Performance for LEBench (SOSP 2019)

## Group Members
- 郝晨熙1240014126
- 邓雯煊1240000381
- 苏弘雨1240001242
- 张涵韵1240000650

# KPTI & PCID Overhead Replication (LEBench)
This repository replicates the LEBench syscall microbenchmark from SOSP 2019.
We perform two controlled experiments to characterize KPTI overhead and the mitigation effect brought by the PCID hardware feature.
All experiments run on fixed hardware with a single kernel version to preserve single-variable control.

## Experiment Goals
direction1. **KPTI latency penalty across different read working set sizes** (corresponds to Fig.1 & Sec.4.1.1 of the original paper)
   - Compare `pti=off` vs `pti=on`
   - Test three read scales: small-read (1 page), med-read (10 pages), big-read (10000 pages)
   - Validate the Amdahl dilution effect: fixed 400~500 cycle CR3-switch overhead of KPTI drastically hurts small reads (~60% slowdown), while large reads suffer nearly zero penalty (~0%).

direction2. **PCID hardware mitigation for KPTI overhead** (corresponds to Fig.3 of the original paper)
   - Three kernel boot configurations:
     - State A: baseline `pti=off`
     - State B: KPTI enabled without PCID (`pti=on nopcid`)
     - State C: KPTI enabled with default PCID optimization (`pti=on`)
   - Capture `dTLB-load-misses` and cycle counts via `perf stat` to provide hardware-level evidence for the overhead reduction.

## Repository Structure
├── docs/
│ ├── results/
│ ├── ├──direction1_kpti_effect_table
│ ├── report/ # Final project report
│ ├── deviations.md # Differences between our replication and original paper
│ ├── env_checklist.md # Hardware & kernel environment checklist
│ ├── exp_template.md # Experiment log template
│ └── reading_notes.md # Paper reading notes
├── logs/
│ └── [student_name]/ # Separated raw experiment logs for each group member
│ ├── state{A/B/C}*.log # Raw benchmark stdout log
│ ├── state{A/B/C}*_data.csv # Parsed numerical data
│ ├── state{A/B/C}_precheck.txt # Pre-run environment check record
│ ├── state{A/B/C}_result.md # Summary for this state
│ └── perf_state{A/B/C}.txt # perf stat raw counter output
├── scripts/
│ ├── precheck.sh # Pre-experiment environment validation script
│ ├── run_local.sh # LEBench runner, kernel parameter setup
│ └── plot_result.py # Data aggregation, parsing and visualization
├── .gitignore
├── original_commit.txt # Exact commit hash of upstream LEBench
└── README.md
