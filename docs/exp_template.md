# LEBench Experiment Record

## 1. Environment Check
- Tester: [e.g., Deng/Han/Zhang]
- Machine ID: [1/2/3]
- CPU Model: [e.g., Intel Core Ultra 5 125H]
- CPU Governor: performance
- Kernel Version: [Actual version]
- LEBench Commit Hash: [Hash value]

## 2. Status Log
> Rule: Each test must include LEBench latency + perf stat (cycles, dTLB-load-misses, dTLB-loads). Do not modify raw logs manually.

### Status A: Baseline (pti=off)
| Workload | Runs | Log Filename (Format: pti_off_workload_id.log) | Exceptions |
| :--- | :--- | :--- | :--- |
| small-read (1 page) | 3 | | |
| med-read (10 pages) | 3 | | |
| big-read (10000 pages) | 3 | | |

### Status B: KPTI ON, PCID ON (pti=on)
| Workload | Runs | Log Filename (Format: pti_on_workload_id.log) | Exceptions |
| :--- | :--- | :--- | :--- |
| small-read (1 page) | 3 | | |
| med-read (10 pages) | 3 | | |
| big-read (10000 pages) | 3 | | |

### Status C: KPTI ON, PCID OFF (pti=on nopcid)
| Workload | Runs | Log Filename (Format: nopcid_workload_id.log) | Exceptions |
| :--- | :--- | :--- | :--- |
| small-read (1 page) | 3 | | |
| med-read (10 pages) | 3 | | |
| big-read (10000 pages) | 3 | | |

