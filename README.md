# CS340 LEBench Replication: KPTI & PCID Overhead Analysis

> **Course Project**: CS340 Operating Systems — Paper Replication  
> **Reference Paper**: *An Analysis of Performance Evolution of Linux’s Core Operations* (SOSP 2019, LEBench)  
> **Upstream Baseline**: Exact upstream LEBench commit recorded in [`original_commit.txt`](./original_commit.txt)

---

## 1. Group Members

* 郝晨熙 (`1240014126`)
* 邓雯煊 (`1240000381`)
* 苏弘雨 (`1240001242`)
* 张涵韵 (`1240000650`)

---

## 2. Project Overview & Experiment Design

This repository replicates the **LEBench** syscall microbenchmark (SOSP 2019) to quantify the performance overhead caused by **Kernel Page-Table Isolation (KPTI)** and evaluate the hardware mitigation provided by **Process-Context Identifiers (PCID)**.

All experiments run on fixed hardware with a single kernel version under strict single-variable control, varying only kernel boot parameters:

### Direction 1: KPTI Latency Penalty Across Read Working Set Sizes (Paper Fig. 1 & Sec. 4.1.1)
* **Comparison**: `pti=off` (**State A**) vs. `pti=on` (**State B**)
* **Workloads**: `small-read` (1 page), `med-read` (10 pages), and `big-read` (10,000 pages)
* **Mechanism (Amdahl Dilution Effect)**: Fixed ~400–500 cycle `CR3`-switching overhead per syscall boundary crossing severely inflates `small-read` latency, whereas its relative impact is amortized/diluted in `big-read` workloads where bulk data copying dominates.

### Direction 2: PCID Hardware Mitigation for KPTI Overhead (Paper Fig. 3)
* **Three Kernel Boot States**:
  * **State A (`pti=off`)**: Baseline without KPTI.
  * **State B (`pti=on nopcid`)**: KPTI enabled with PCID disabled (frequent TLB flushes across address-space switches).
  * **State C (`pti=on`)**: KPTI enabled with default PCID hardware optimization active.
* **Hardware-Level Evidence**: `perf stat` collects `cycles` and `dTLB-load-misses` alongside latency measurements to connect syscall overhead with microarchitectural TLB behavior.

---

## 3. Repository Structure

```text
CS340-LEBench-Replication/
├── docs/
│   ├── report/                              # Final project report folder (.gitkeep)
│   ├── results/                             # Output tables & comparison charts
│   │   ├── dir1_ab_kpti_dilution_chart.png  # Direction 1: A vs. B latency & KPTI dilution
│   │   ├── dir2_bc_hw_counters.png          # Direction 2: B vs. C cycles & dTLB-load-misses
│   │   ├── dir2_bc_read_latency.png         # Direction 2: B vs. C read latency comparison
│   │   ├── direction1_kpti_effect_table.md  # Direction 1 quantitative summary table
│   │   └── KPTI Latency & PCID Mitigation...# Combined analysis workbook / summary
│   ├── deviations.md                        # Differences between replication and original paper
│   ├── env_checklist.md                     # Hardware & kernel environment checklist
│   └── reading_notes.md                     # Paper reading notes
├── logs/                                    # Intermediate run logs & perf outputs
│   ├── dengwenxuan/
│   ├── haochenxi/
│   ├── perf_All/
│   ├── suhongyu/
│   └── zhanghanyun/
├── scripts/                                 # Benchmark runners, aggregation & plotting
│   ├── direction_combain_barchart_code.py   # Generates comparison charts from Excel sheets
│   ├── direction_combain_table_code.py      # Aggregates & deduplicates group results to Excel
│   ├── plot_result.py                       # Log parsing & plotting utility
│   ├── precheck.sh                          # Pre-run environment validation script
│   ├── run1_local.sh                        # Direction 1 benchmark runner
│   └── run2_local.sh                        # Direction 2 benchmark runner
├── .gitignore
├── original_commit.txt                      # Exact commit hash of upstream LEBench
└── README.md

---

## 4. Core Scripts & Processing Logic

### Benchmark Execution & Precheck

* `scripts/precheck.sh`: Checks environment readiness and kernel/CPU state prior to running benchmarks.
* `scripts/run1_local.sh` & `scripts/run2_local.sh`: Execute the local LEBench runs for Direction 1 and Direction 2, producing raw logs and `perf` records.
* `scripts/plot_result.py`: Parses benchmark outputs and plots results for individual/local inspection.

### Group Data Aggregation & Deduplication (`direction_combain_table_code.py` / Direction 2 Pipeline)

* Extracts `read` test latencies from each member's `*_data.csv`, determining the actual experimental state from the real kernel `cmdline` recorded inside the `.log` file.
* Extracts hardware counters (`cycles`, `dTLB-load-misses`, and elapsed time) from `logs/perf_All/`, member `perf` files, and inline `perf` outputs inside `.log` files.
* Deduplicates by `(member, state)` and across counter sources so each `(member, state)` pair is counted once.
* Exports `docs/Direction2_PCID_Analysis.xlsx` containing `Latency` and `HW Counters` sheets, group **mean** and **standard deviation**, `B-vs-A` / `C-vs-A` / `C-vs-B` comparisons, and reference comparisons against the paper.

### Comparison Chart Generation (`direction_combain_barchart_code.py`)

* Reads the `Latency` and `HW Counters` sheets produced by the table aggregation script and outputs three comparison figures into `docs/results/`:
* `docs/results/dir1_ab_kpti_dilution_chart.png`: **State A vs. State B** read latency and KPTI dilution effect.
* `docs/results/dir2_bc_read_latency.png`: **State B vs. State C** read latency showing PCID mitigation.
* `docs/results/dir2_bc_hw_counters.png`: **State B vs. State C** comparison of `CPU cycles` and `dTLB-load-misses`.



---

## 5. Logs & Documentation Notes

* **`logs/`**: Stores intermediate execution logs per member (`dengwenxuan/`, `haochenxi/`, `suhongyu/`, `zhanghanyun/`) and centralized `perf` outputs (`perf_All/`) used as inputs for aggregation and plotting.
* **`docs/`**: Houses reference notes (`reading_notes.md`), environment records (`env_checklist.md`), replication vs. paper differences (`deviations.md`), final figures/tables under `docs/results/`, and report files under `docs/report/`.

---

## 6. How to Run

```bash
bash scripts/precheck.sh
bash scripts/run1_local.sh
bash scripts/run2_local.sh
python3 scripts/direction_combain_table_code.py
python3 scripts/direction_combain_barchart_code.py

```

```

```

