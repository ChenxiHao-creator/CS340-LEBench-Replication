# READ PERFORMANCE RESULTS (STATUS A)

Here is the comparison of the `read` operations extracted from two independent runs under Status A. 

| Test Case | Run 1 Time (s) | Run 2 Time (s) | Time Difference (Run 2 - Run 1) |
| :--- | :--- | :--- | :--- |
| **small read** | 0.355476539 | 0.404381948 | +0.048905409 |
| **mid read** | 0.690894401 | 0.704024703 | +0.013130302 |
| **big read** | 7.381041708 | 7.533062629 | +0.152020921 |
| **huge read** | 328.806539749 | 144.939134208 | -183.867405541 |


---

# FULL BENCHMARK RAW RESULTS (STATUS A)

### Run 1 Raw Results
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
Performing test small read.
Test took: 0.355476539 seconds
Performing test small mmap.
Test took: 0.479267558 seconds
Performing test small munmap.
Test took: 2.038473458 seconds
Performing test small page fault.
Test took: 0.596246273 seconds
Performing test mid write.
Test took: 8.744029756 seconds
Performing test mid read.
Test took: 0.690894401 seconds
Performing test mid mmap.
Test took: 0.460715886 seconds
Performing test mid munmap.
Test took: 12.189864132 seconds
Performing test mid page fault.
Test took: 0.812418486 seconds
Performing test big write.
Test took: 46.765527040 seconds
Performing test big read.
Test took: 7.381041708 seconds
Performing test big mmap.
Test took: 0.524349327 seconds
Performing test big munmap.
Test took: 29.431703382 seconds
Performing test big page fault.
Test took: 0.599668822 seconds
Performing test huge write.
Test took: 302.519699889 seconds
Performing test huge read.
Test took: 328.806539749 seconds
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
### Run 2 Raw Results
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
Performing test small read.
Test took: 0.404381948 seconds
Performing test small mmap.
Test took: 0.479196479 seconds
Performing test small munmap.
Test took: 2.242710845 seconds
Performing test small page fault.
Test took: 0.661376391 seconds
Performing test mid write.
Test took: 9.562801643 seconds
Performing test mid read.
Test took: 0.704024703 seconds
Performing test mid mmap.
Test took: 0.467701659 seconds
Performing test mid munmap.
Test took: 12.823994604 seconds
Performing test mid page fault.
Test took: 0.942027129 seconds
Performing test big write.
Test took: 47.296816334 seconds
Performing test big read.
Test took: 7.533062629 seconds
Performing test big mmap.
Test took: 0.506695641 seconds
Performing test big munmap.
Test took: 30.337670348 seconds
Performing test big page fault.
Test took: 0.645847520 seconds
Performing test huge write.
Test took: 305.920527942 seconds
Performing test huge read.
Test took: 144.939134208 seconds
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
