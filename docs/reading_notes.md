Paper: An Analysis of Performance Evolution of Linux's Core Operations (SOSP '19)
1) Core Findings of the Paper
1.Core Degradation: Over the past seven years, the latency of most core Linux kernel operations (system calls, context switching) has increased substantially or fluctuated wildly, with the vast majority of operations being noticeably slower than in version 4.0.
2.Primary Attribution: Performance degradations are primarily attributed to 11 performanceaffecting changes (root causes), categorized into security enhancements, new features, and configuration changes/misconfigurations.
3.Heavy Security Tax: Hardware vulnerability mitigations (Spectre / Meltdown) introduce the steepest performance penalties, with four specific changes accounting for 88% of the slowdown observed across macrobenchmarks.
2) Candidate Claims & Scope Anchoring
Claim : KPTI Penalties on ShortLatency System Calls and TLB Locality
Claim Statement: 
Kernel Page Table Isolation (KPTI) implemented for Meltdown mitigation forces pagetable pointer (CR3) switches and TLB flushes on kernel entry/exit, imposing a fixedcycle penalty (400–500 cycles). Following Amdahl’s law, this fixed overhead heavily degrades shortlatency smallread workloads, while the cost is diluted close to 0% for largescale bigread operations. Moreover, the PCID hardware mechanism can significantly suppress KPTIinduced performance loss by avoiding full TLB flushes. Without PCID hardware support, KPTI incurs much higher latency overhead.
Paper References:
1.Figure 1 & Section 4.1.1: Demonstrates the Amdahllaw dilution effect across different read data sizes.
2.Figure 3: Presents latency contrast between configurations with and without PCID; reports 113% slowdown without PCID and 47% slowdown when PCID is available.
3.Table 3 & Figure 2 (Meltdown patch): Reports a 60% slowdown on smallread and 63% on recv.
Workload & Metric:
1.Microbenchmark for direction1: read system call with three workload sizes: smallread (1 page), medread (10 pages), bigread (10 000 pages). Controlled variable: pti=off versus pti=on.
2.Microbenchmark for direction2: tests under three kernel boot arguments: 1) baseline pti=off; 2) KPTI enabled without PCID pti=on nopcid; 3) default optimized pti=on (PCID enabled).
3.Metrics: systemcall latency (ns). Hardware events dTLBloadmisses and total cycles are collected via perf stat as lowlevel hardware evidence.
3) Target Comparison Table (Paper vs. Ours)
We conduct five groups of microbenchmark experiments.

1.smallread (1 page, 4 KB): Controlled factor is KPTI activation. The original paper reports a slowdown of +59% ~ +60%. Our measured result will be filled as (Mean ± Std). Corresponding paper sources are Figure 3 and Table 3.
2.medread (10 pages, 40 KB): Controlled factor is KPTI activation. The paper observes an intermediate performance penalty between smallread and bigread. Our measured result will be filled as (Mean ± Std). Relevant materials come from Section 4.1.1 and Figure 1.
3.bigread (10 000 pages, 40 MB): Controlled factor is KPTI activation. The paper shows nearly zero slowdown (~0%). Our measured result will be filled as (Mean ± Std). Corresponding paper sources are Figure 1 and Figure 3.
4.smallread (nopcid configuration, 1 page, 4 KB): Controlled factor is KPTI enabled while PCID hardware is disabled (pti=on nopcid). The paper reports +113% slowdown. Our measured result will be filled as (Mean ± Std). The supporting figure is Figure 3.
5.smallread (pcidon configuration, 1 page, 4 KB): Controlled factor is KPTI enabled with PCID hardware optimization (pti=on). The paper reports +47% slowdown. Our measured result will be filled as (Mean ± Std). The supporting figure is Figure 3.
