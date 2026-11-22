Paper: An Analysis of Performance Evolution of Linux's Core Operations (SOSP '19)

Core Findings of the Paper

Core Degradation: Over a seven-year span, the latency of most core Linux kernel operations (system calls, context switching) has increased substantially or fluctuated widely, leaving the vast majority of operations noticeably slower than in Linux 4.0.

Primary Attribution: Performance degradations are primarily attributed to 11 performance-affecting changes (root causes), categorized into security enhancements, new features, and configuration changes/misconfigurations.

Heavy Security Tax: Hardware vulnerability mitigations (Spectre / Meltdown) introduce the steepest performance penalties, with four specific changes accounting for 88% of the slowdown observed across macrobenchmarks.

Candidate Claim & Scope Anchoring

Claim: KPTI Penalties on Short-Latency System Calls and TLB Locality

Claim Statement: Kernel Page Table Isolation (KPTI), implemented for Meltdown mitigation, forces page-table pointer (CR3) switches and TLB flushes on kernel entry/exit, imposing a fixed-cycle penalty (400–500 cycles). Following Amdahl's Law, this fixed overhead produces a clear decreasing trend as workload size grows: it heavily degrades short-latency small-read workloads while being substantially diluted on large-scale big-read operations. Moreover, the PCID hardware mechanism significantly suppresses KPTI-induced performance loss by avoiding full TLB flushes; without PCID support, KPTI incurs much higher latency overhead.

Paper References:

Figure 1 & Section 4.1.1: Demonstrates the Amdahl's Law dilution effect, showing a clear decreasing overhead trend across increasing read data sizes.

Figure 3: Plots dual slowdown curves for read across increasing baseline latencies with and without PCID relative to the pti=off baseline, reporting a +113% slowdown without PCID (nopcid) and a +47% slowdown with PCID enabled on small-read—equivalent to a calculated -30.99% latency change rate (
1.47
−
2.13
2.13
2.13
1.47−2.13
​
 ) when comparing PCID-enabled directly against nopcid.

Workload & Metrics:

Microbenchmark for Direction 1 (Dilution Effect, State B vs. State A): read system calls across three workload sizes—small-read (1 page), med-read (10 pages), and big-read (10,000 pages)—comparing pti=on nopcid (State B) against baseline pti=off nopcid (State A).

Microbenchmark for Direction 2 (PCID Mitigation, State C vs. State B): Direct comparison between KPTI with PCID enabled (pti=on, State C) and KPTI with PCID disabled (pti=on nopcid, State B) across all three read scales (small-read, med-read, and big-read), aiming to observe performance recovery (a negative latency change rate) and validate that PCID mitigates the overhead introduced by the KPTI patch.

Metrics: System-call latency (ns) via LEBench; hardware events dTLB-load-misses and total cycles collected via perf stat as low-level hardware evidence.

Target Comparison Scope (Paper vs. Ours)
We conduct two directions of microbenchmark comparisons across three read scales (our measured results will be recorded as Mean ± Std):

small-read (State B vs. State A, 1 page, 4 KB): Controlled factor is KPTI enabled with PCID disabled (pti=on nopcid). The paper reports a +113% slowdown relative to baseline (Figure 3).

med-read (State B vs. State A, 10 pages, 40 KB): Controlled factor is KPTI activation. The paper observes an intermediate penalty following a decreasing trend between small-read and big-read (Section 4.1.1, Figure 1).

big-read (State B vs. State A, 10,000 pages, 40 MB): Controlled factor is KPTI activation. The paper shows that the fixed KPTI overhead is heavily diluted to a minimal level, completing the decreasing trend (Figure 1, Figure 3).

small-read (State C vs. State B, 1 page, 4 KB): Controlled factor is PCID hardware optimization under KPTI (pti=on vs. pti=on nopcid). Based on the paper's +47% (PCID) and +113% (nopcid) slowdowns in Figure 3, enabling PCID yields a calculated -30.99% latency change rate (performance recovery) compared to nopcid.

med-read & big-read (State C vs. State B, 10 pages & 10,000 pages): Controlled factor is PCID hardware optimization under KPTI across larger read scales. Supported by the dual curves in Figure 3, these tests verify whether enabling PCID consistently produces performance recovery (a negative latency change rate), thereby corroborating that PCID was introduced to mitigate the performance penalty of the KPTI patch.
