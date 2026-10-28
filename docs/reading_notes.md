Claim Selection
I. Core Information Comparison Table
Dimension	Retpoline (Top Choice)	KPTI (Backup Choice)
Claim Statement	Retpoline causes significant slowdown in select/poll/epoll	KPTI causes significant slowdown in recv/read; PCID only partially mitigates it
Original Data	Average 66%; poll 89%; epoll 72%	Average 22%; recv 63%; read 59%
Corresponding Figures	§4.1.2; Table 3; Figure 1(a)/(b); Figure 2; Figure 4/5/6 (mechanism)	§4.1.1; Table 3; Figure 1(a)/(b); Figure 2; Figure 3 (PCID line chart)
Introduced Version	4.14	After 4.14 (effectively around 4.15)
Reproduction Test Cases	select, poll, epoll	recv, read
Nature of Test Cases	Pure CPU/socket syscalls, no disk I/O or network transmission	recv involves socket transmission; read involves page cache/file I/O
Environmental Interference	Low; variance relatively controllable	High; I/O-related tests fluctuate more in VMs
CPU Feature Dependencies	None	If reproducing PCID comparison, requires CPU support for PCID and VM passthrough
Kernel Version Selection	4.13 (without Retpoline) vs. 4.14/4.15 (with Retpoline)	4.14 (without KPTI) vs. 4.15 (with KPTI). Note: 4.15 includes Retpoline; confounding variables need attention
Chart Intuitiveness	Spectre patch subplot in Figure 2 is intuitive; poll close to 90%	Figure 3 specifically shows PCID effect; intuitive line chart, but requires extra config to reproduce with/without PCID
Extension Space	Test a newer kernel version (e.g., 5.15/6.x) to see if Retpoline overhead is optimized; only change "kernel version" as a single variable	Try PCID on/off; requires kernel parameters/compile config, changes multiple variables, high complexity
Coding Skill Requirement	Low: just install/boot different kernels and run existing LEBench tests	Low (only reproduce KPTI slowdown); Medium-High (if reproducing PCID comparison)
Device Requirement	Standard laptops with VMs are sufficient	Standard laptops with VMs are sufficient, but PCID comparison requires CPU support confirmation
Main Risks	Old kernels may lack drivers in VMs; availability of kernel 4.13 needs confirmation	4.15 introduces both Retpoline and KPTI; separating KPTI's impact requires care; high variance for I/O tests
II. Specific Advantages of Retpoline
Pure Test Cases, Low Variance
select/poll/epoll are pure syscall loops, independent of disk or network throughput. They run relatively stably in VMs, making it easy to obtain reproducible mean ± std.

Large Numbers, Obvious Trends
The paper reports poll 89%, epoll 72%, and an average of 66%. Even with laptop noise, the difference before and after introducing Retpoline is easy to observe, avoiding the awkward situation of "tested but saw no difference."

Sufficient Chart Support

Table 3 directly provides poll 89%;

The Spectre patch subplot in Figure 2 is intuitive;

The heatmap in Figure 1(a) shows select/poll/epoll turning from green to red around 4.14.
The "Paper vs. Ours" comparison table in the report is easy to write.

Natural Extension
Change only one variable ("kernel version"): after reproducing 4.13 vs. 4.14/4.15, test another 5.15 or 6.x kernel to see if the Retpoline overhead still exists. This perfectly complies with "one factor changed at a time."

No Dependency on Special CPU Features
No need for hardware features like PCID; VM configuration is simple.

Lowest Coding Skill Requirement
No need to modify kernel source code or adjust compile parameters; just install kernels and run LEBench.

III. Specific Advantages of KPTI
Dedicated Line Chart in the Paper
Figure 3 directly shows the read test slowdown with respect to baseline latency, with two curves for with/without PCID. If you want to imitate a similar chart, KPTI provides richer chart material.

Extra Analysis Space for PCID
If someone in the group is willing to tinker with CPU features and kernel parameters, you can try to reproduce the "before/after PCID optimization" comparison, and the Extension can be built around PCID.

Involves Core Memory Management Mechanisms
KPTI is directly related to page tables and TLB, aligning closely with OS course concepts (memory management, TLB). The discussion section of the report can cover more OS principles.

Numbers are Also Relatively Obvious
recv 63%, read 59%. Although not as dramatic as Retpoline's 89%, they are still large enough for observable trends.

IV. Main Disadvantages of KPTI
High Variance in I/O Tests
recv and read involve socket transmission and file system caches. In VMs, they are easily affected by background I/O and page cache states, so the std across three runs may be large.

4.15 Introduces Both Retpoline and KPTI
If choosing 4.14 vs. 4.15, 4.15 contains both Retpoline and KPTI, so the recv/read slowdown may be mixed with Retpoline's impact. To cleanly isolate KPTI, more careful version selection or configuration control is needed, increasing experimental design complexity.

Complex PCID Comparison Configuration
To reproduce Figure 3's with/without PCID, you need to confirm CPU support, VM passthrough, and kernel boot parameters or compile options, posing higher risk for groups with weaker coding skills.

Less Natural Extension Space
Testing kernel versions for KPTI optimization is not as direct as Retpoline; PCID comparison involves multiple variables, easily violating "change one factor at a time."

V. Selection Recommendation
If the group's priority is "stable, fast, fewer pitfalls" → Choose Retpoline.
Reason: Pure test cases, low variance, large numbers, sufficient charts, natural extension, no dependency on special hardware features.

If the group's priority is "want to draw line charts, integrate memory management knowledge, and have someone willing to tinker with PCID" → Choose KPTI.
However, clearly state in the notes and report: only reproduce KPTI slowdown; treat the PCID part as an optional Extension; if PCID configuration fails, report only the KPTI main effect and acknowledge the limitation.

One-sentence conclusion:

Retpoline's advantages lie in "stable reproduction, smooth extension, fewer dependencies"; KPTI's advantages lie in "good chart material and close integration with OS concepts," but with higher variance and configuration complexity. For a group with limited coding skills and laptop devices, Retpoline is the lower-risk choice with more guaranteed output.
