# READ PERFORMANCE RESULTS (STATUS A)

Here is the comparison of the `read` operations extracted from three independent runs under Status A. 

| Test Case | Run 1 (A1) Time (s) | Run 2 (A2) Time (s) | Run 3 (A3) Time (s) |
| :--- | :--- | :--- | :--- |
| **small read** | 0.197453722 | 0.355476539 | 0.404381948 |
| **mid read** | 0.334391163 | 0.690894401 | 0.704024703 |
| **big read** | 2.804245023 | 7.381041708 | 7.533062629 |
| **huge read** | 165.237767647 | 328.806539749 | 144.939134208 |

*Note: There is significant performance variance across the three runs, especially in the `huge read` test (Run 2 is more than twice as slow as Run 3). This is highly likely due to VM resource contention or host-level background noise (e.g., Windows host throttling or disk I/O caching), as mentioned in the environment precheck.*

---

# FULL BENCHMARK RAW RESULTS (STATUS A)

### Run 1 Raw Results
```text
Performing test ref.
Test took: 0.291500070 seconds
Performing test cpu.
Test took: 0.305247225 seconds
Performing test getpid.
Test took: 0.337269818 seconds
Performing test context siwtch.
Test took: 343.115664150 seconds
Performing test send.
Test took: 0.692053171 seconds
Performing test recv.
Test took: 0.637672569 seconds
Performing test big send.
Test took: 5.280509587 seconds
Performing test big recv.
Test took: 6.085301776 seconds
Performing test fork.
Test took: 3.560031719 seconds
Performing test thr create.
Test took: 4.244449493 seconds
Performing test big fork.
Test took: 11.160676865 seconds
Performing test huge fork.
Test took: 24.888084637 seconds
Performing test small write.
Test took: 0.650918413 seconds
Performing test small mmap.
Test took: 0.296441919 seconds
Performing test small munmap.
Test took: 1.025437966 seconds
Performing test small page fault.
Test took: 0.267679141 seconds
Performing test mid write.
Test took: 4.276848971 seconds
Performing test mid mmap.
Test took: 0.236370416 seconds
Performing test mid munmap.
Test took: 5.956160432 seconds
Performing test mid page fault.
Test took: 0.434923668 seconds
Performing test big write.
Test took: 21.998816205 seconds
Performing test big mmap.
Test took: 0.197323110 seconds
Performing test big munmap.
Test took: 13.224072902 seconds
Performing test big page fault.
Test took: 0.293190132 seconds
Performing test huge write.
Test took: 143.266856069 seconds
Performing test huge mmap.
Test took: 0.242007028 seconds
Performing test huge munmap.
Test took: 132.145616115 seconds
Performing test huge page fault.
Test took: 0.259863381 seconds
Performing test select.
Test took: 1.723875859 seconds
Performing test poll.
Test took: 1.650772055 seconds
Performing test epoll.
Test took: 2.354638608 seconds
Performing test select big.
Test took: 21.694933126 seconds
Performing test poll big.
Test took: 21.483819193 seconds
Performing test epoll big.
Test took: 28.132996012 seconds
Total Test took: 1031.274880725 seconds
```
### Run 2 Raw Results
```text
Performing test ref.
Test took: 0.393335797 seconds
Performing test cpu.
Test took: 0.309023538 seconds
Performing test getpid.
Test took: 0.401321968 seconds
Performing test context siwtch.
Test took: 596.499216726 seconds
Performing test send.
Test took: 1.432221697 seconds
Performing test recv.
Test took: 1.503301843 seconds
Performing test big send.
Test took: 12.583828157 seconds
Performing test big recv.
Test took: 14.065300142 seconds
Performing test fork.
Test took: 8.580195097 seconds
Performing test thr create.
Test took: 10.473800426 seconds
Performing test big fork.
Test took: 23.281535544 seconds
Performing test huge fork.
Test took: 45.609047381 seconds
Performing test small write.
Test took: 1.281539222 seconds
Performing test small mmap.
Test took: 0.479267558 seconds
Performing test small munmap.
Test took: 2.038473458 seconds
Performing test small page fault.
Test took: 0.596246273 seconds
Performing test mid write.
Test took: 8.744029756 seconds
Performing test mid mmap.
Test took: 0.460715886 seconds
Performing test mid munmap.
Test took: 12.189864132 seconds
Performing test mid page fault.
Test took: 0.812418486 seconds
Performing test big write.
Test took: 46.765527040 seconds
Performing test big mmap.
Test took: 0.524349327 seconds
Performing test big munmap.
Test took: 29.431703382 seconds
Performing test big page fault.
Test took: 0.599668822 seconds
Performing test huge write.
Test took: 302.519699889 seconds
Performing test huge mmap.
Test took: 0.514858081 seconds
Performing test huge munmap.
Test took: 198.311726607 seconds
Performing test huge page fault.
Test took: 0.176032882 seconds
Performing test select.
Test took: 1.106070336 seconds
Performing test poll.
Test took: 1.104660293 seconds
Performing test epoll.
Test took: 1.564161487 seconds
Performing test select big.
Test took: 16.132153429 seconds
Performing test poll big.
Test took: 15.866663963 seconds
Performing test epoll big.
Test took: 20.795171853 seconds
Total Test took: 1774.533460105 seconds
```
### Run 3 Raw Results
```text
Performing test ref.
Test took: 0.659188156 seconds
Performing test cpu.
Test took: 0.681617704 seconds
Performing test getpid.
Test took: 0.854768414 seconds
Performing test context siwtch.
Test took: 753.114506911 seconds
Performing test send.
Test took: 1.515120683 seconds
Performing test recv.
Test took: 1.546685903 seconds
Performing test big send.
Test took: 12.803727756 seconds
Performing test big recv.
Test took: 14.240271162 seconds
Performing test fork.
Test took: 8.473853340 seconds
Performing test thr create.
Test took: 10.773871238 seconds
Performing test big fork.
Test took: 25.549467277 seconds
Performing test huge fork.
Test took: 48.133762267 seconds
Performing test small write.
Test took: 1.369813512 seconds
Performing test small mmap.
Test took: 0.479196479 seconds
Performing test small munmap.
Test took: 2.242710845 seconds
Performing test small page fault.
Test took: 0.661376391 seconds
Performing test mid write.
Test took: 9.562801643 seconds
Performing test mid mmap.
Test took: 0.467701659 seconds
Performing test mid munmap.
Test took: 12.823994604 seconds
Performing test mid page fault.
Test took: 0.942027129 seconds
Performing test big write.
Test took: 47.296816334 seconds
Performing test big mmap.
Test took: 0.506695641 seconds
Performing test big munmap.
Test took: 30.337670348 seconds
Performing test big page fault.
Test took: 0.645847520 seconds
Performing test huge write.
Test took: 305.920527942 seconds
Performing test huge mmap.
Test took: 0.137282189 seconds
Performing test huge munmap.
Test took: 92.235174101 seconds
Performing test huge page fault.
Test took: 0.177065436 seconds
Performing test select.
Test took: 1.087127359 seconds
Performing test poll.
Test took: 1.075551937 seconds
Performing test epoll.
Test took: 1.556377670 seconds
Performing test select big.
Test took: 16.410595332 seconds
Performing test poll big.
Test took: 15.844515717 seconds
Performing test epoll big.
Test took: 23.343244412 seconds
Total Test took: 1657.192689467 seconds
```
