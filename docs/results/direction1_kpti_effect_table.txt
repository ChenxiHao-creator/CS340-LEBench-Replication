### Direction 1: KPTI Performance Dilution Effect on Read Syscalls

The following table demonstrates the performance impact of enabling KPTI (State B: `pti=on nopcid`) compared to the baseline (State A: `pti=off nopcid`) across different read syscall sizes. 

| Test Scale | State A Mean (s) | State A Stdev (s) | State B Mean (s) | State B Stdev (s) | Slowdown (%) |
| :--- | ---: | ---: | ---: | ---: | ---: |
| **Small Read** (1 page) | 0.000000437 | 0.000000268 | 0.000001167 | 0.000000933 | **+167.41%** |
| Mid Read (10 pages) | 0.000002229 | 0.000001405 | 0.000003072 | 0.000002199 | +37.81% |
| Big Read (10,000 pages) | 0.000411476 | 0.000277902 | 0.000358180 | 0.000251254 | -12.95% * |
| **Huge Read** | 0.017567249 | 0.008675619 | 0.018983302 | 0.009206658 | +8.06% |
