# CS340 LEBench Replication
Paper: An Analysis of Performance for LEBench (SOSP 2019)

## Group Members
- 郝晨熙1240014126
- 邓雯煊1240000381
- 苏弘雨1240001242
- 张涵韵1240000650

## Project Overview
This repo replicates the LEBench syscall microbenchmark from SOSP 2019. We conduct two controlled experiments targeting KPTI overhead and the mitigation effect of the PCID hardware feature. We fix hardware and use one single kernel version to guarantee single-variable isolation.
KPTI latency penalty across different read working set sizes (Fig.1 & Sec.4.1.1)
PCID hardware mitigation for KPTI overhead (Fig.3)

## Repository Structure
docs/         # Project report, methodology notes, experiment documentation

logs/         # Raw benchmark outputs, perf stat logs, repeated experimental data

scripts/      # Automation scripts: LEBench runner, boot parameter setup, data parsing & plotting

.gitignore

README.md

original_commit.txt  # Record the exact commit hash of the upstream LEBench we replicate

## Original Repository
https://github.com/LinuxPerf/LEBench
