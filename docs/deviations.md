# Deviations from SOSP'19 LEBench Setup

Maintainer: Member Suhongyu.
Rule: add a row before changing any experimental condition; after running, attach evidence path and update status.

Severity: high = may change Figure 1/Table 3 direction or verdict; medium = may change magnitude/variance; low = documentation risk.
Status: expected / confirmed / controlled / accepted-risk.

| ID | Item | Paper original setting | Our setting used | Reason | Affects | Controlled check / evidence | Severity | Status |
|---:|---|---|---|---|---|---|---|---|
| D01 | Claim-figure linkage | Main latency/root-cause claim supported by Figure 1, Table 3, Figure 2; security details in §4.1 | same | group note incorrectly used Figure 4 as main evidence | report structure | this deviation note | high | confirmed |
| D02 | Architecture scope | paper focuses x86 server; sensitivity on Intel laptop only | x86-64 only | course/group scope | all | report scope statement | low | confirmed |
| D03 | Runner OS | Linux with /boot, GRUB, sudo, reboot-based kernel switching | Windows 11 host for docs/static scan; experiments inside VMware VM running Ubuntu 18.04.6 | LEBench requires Linux root/GRUB/reboot; host Windows cannot run it | feasibility | get_kern.py:4; run.py:76; run.py:180-183; systemd-detect-virt = vmware | high | confirmed |
| D04 | Machine type | HP DL160G9 bare-metal server for main results | VMware virtual machine (VMware Workstation, hypervisor confirmed by systemd-detect-virt) | bare-metal server unavailable; use controlled VM instead | absolute latency; variance | `systemd-detect-virt` -> vmware; `lscpu` Hypervisor vendor: VMware | high | confirmed |
| D05 | CPU model | Intel Xeon E5-2630v3 Haswell-EP, 2.40GHz, L1 512KB/L2 2MB/L3 20MB | Host CPU 13th Gen Intel Core i9-13900H exposed as VMware vCPU; flags include pti ssbd ibrs ibpb ibrs_enhanced; no pcid flag (invpcid present) | VM vCPU depends on host CPU and VMware feature masking; 10-generation gap vs paper Haswell-EP | all; especially idle-state/TLB/PCID claims | `lscpu`: Model name 13th Gen i9-13900H; Hypervisor vendor VMware | high | confirmed |
| D06 | Memory/storage | 128GB 1866MHz DDR4; 960GB SSD | TBD: fill from VM `free -h` and `lsblk` | VM allocated resources differ from paper server | big-read/big-fork/select variance | `free -h`; `lsblk` | medium | expected |
| D07 | Kernel version set | 36 versions: majors 3.0-3.19 and 4.0-4.20, latest minor before next major | reduced to kernels installed on VM: running 4.15.0-213-generic (Ubuntu bionic GA); also installed mainline 4.14.15-041415-generic; stock 5.4.0-150/5.4.0-84 present | full 3.0-4.20 set too heavy; focus on 4.14/4.15 boundary for C2 | Figure 1 evolution claim; C2 boundary | `uname -r` = 4.15.0-213-generic; `dpkg -l` lists 4.14.15-041415, 4.15.0-213, 5.4.0-150, 5.4.0-84 | high | confirmed |
| D08 | Kernel config source | Ubuntu distribution kernels, not vanilla default | Running kernel 4.15.0-213-generic IS the Ubuntu 18.04 distribution GA kernel (package linux-image-generic 4.15.0.213.196); mainline 4.14.15-041415 installed separately via .deb | 4.15.0-213 available directly from Ubuntu archive; mainline 4.14.15 added for comparison | all root-cause attributions; C2 | `dpkg -l`: linux-image-generic 4.15.0.213.196; linux-image-4.15.0-213-generic signed Ubuntu package | high | confirmed |
| D09 | Security mitigations | KPTI after 4.14; Retpoline in 4.14; usercopy since 4.8; SLAB randomization since 4.7; PCID used for Fig1/Table3 | Boot pins mitigation state: GRUB_CMDLINE_LINUX_DEFAULT="quiet splash pti=on nopcid"; CPU flags show ibrs/ibpb/ibrs_enhanced/pti | mitigation state must be fixed and recorded before verdicts; pti=on matches paper's KPTI-present condition | security claim; KPTI/Retpoline verdict | `/etc/default/grub` (pti=on nopcid); `lscpu` flags; vulnerabilities output TBD paste | high | confirmed |
| D10 | PCID optimization | paper Figure1/Table3 obtained with PCID optimization; Fig3 shows with/without PCID | VM has no pcid flag (invpcid only); boot sets nopcid -> KPTI runs WITHOUT PCID optimization | reproduces paper's "without PCID" curve (Fig3), not the with-PCID default | KPTI magnitude | `lscpu` flags: invpcid present, pcid absent; GRUB nopcid | medium | confirmed |
| D11 | Repetitions/statistics | 10,000 repetitions; K-best K=5 tolerance=5% | same if repo config allows; at least 3 full benchmark runs for course | must match paper estimator | all reported numbers | runner config; raw logs; summary script | high | expected |
| D12 | Reduced workload scale | Figure1/Table3 cover full LEBench matrix | proposal for C2: read/recv tests (KPTI) + select/poll/epoll tests (Retpoline); final list pending B/D confirmation | time/compute constraints; C2 focuses on KPTI/Retpoline affected tests | claim scope | included/excluded table tied to Fig1 rows | high | expected |
| D13 | Table1 workload selection | Spark/PostgreSQL/Chromium/kernel-build used with strace to select syscalls | skipped | selection workloads are heavy and not needed to run microbench | setup provenance | state as limitation | medium | confirmed |
| D14 | Macrobenchmark validation | Redis/Apache/Nginx 100k requests, 50/100 concurrency; disable 11 causes for impact | optional/later | time | extension/real-world impact only | benchmark configs if run | medium | expected |
| D15 | Python version | repo uses Python 2 style print in run.py | TBD: fill `python --version` in VM; if python2 missing, plan py3 conversion | modern systems lack Python 2 | runner feasibility | `python --version`; `2to3` patch if used | medium | expected |
| D16 | Paths/hard-coding | repo expects Linux paths such as /boot and /iteration | keep relative paths in our scripts; document absolute OS paths | reproducibility grading | clean-machine build | README/commands; no hard-coded user paths in our docs | medium | expected |
| D17 | Log/trace retention | paper reports trends; course requires traceability | logs/<date>_kernel_<ver>_<test>.txt + summary.csv; large logs not committed | repo size and grading | traceability | .gitignore; log naming convention | low | expected |
| D18 | Safety note for disabling mitigations | paper disables/configures features for analysis | we only do controlled local tests if needed; do not recommend disabling security mitigations in production | ethics/security | security claim wording | explicit note in report | medium | confirmed |
| D19 | Virtualization software version | Paper runs on bare-metal HP DL160G9 server | VMware virtual machine on Windows host (Workstation, Pro; version per VM settings) | bare-metal unavailable; VMware gives repeatable VM environment for course reproduction | absolute latency; device emulation overhead; timer/TLB behavior | `systemd-detect-virt` = vmware; `lscpu` Hypervisor vendor: VMware | high | confirmed |
| D20 | VM hardware compatibility | Paper uses physical Haswell-EP server hardware | VM hardware compatibility set to Workstation 25H2 or later (per setup notes) | required by upgraded VMware version; changes virtual hardware presentation to guest | CPU feature exposure; benchmark stability | VMware VM Settings → Compatibility | medium | confirmed |
| D21 | Kernel install method | Paper uses released Ubuntu distribution kernels selected per major version | Mixed: 4.15.0-213 from Ubuntu bionic archive (standard package); mainline 4.14.15-041415 installed via downloaded .deb; earlier note claiming 4.15.0-041500 was inaccurate and is corrected here | obtain near-4.14/4.15 boundary kernels; reduced-scale C2 reproduction | kernel config provenance; module compatibility; reproducibility | `dpkg -l` output distinguishes Ubuntu signed packages (4.15.0-213) from mainline naming (4.14.15-041415) | high | confirmed |
| D22 | GRUB menu exposed | Paper/repository expects booting selected kernels via GRUB | /etc/default/grub: GRUB_TIMEOUT_STYLE=menu, GRUB_TIMEOUT=10, so non-default kernels can be selected at boot | multiple kernels installed; manual selection needed | experiment procedure; boot consistency | `grep` of /etc/default/grub | medium | confirmed |
| D23 | Boot cmdline: mitigation pinning, not nomodeset | Setup note documented nomodeset for black screen; actual grub file shows GRUB_CMDLINE_LINUX_DEFAULT="quiet splash pti=on nopcid" (no nomodeset present) | correct the record: effective boot parameters pin KPTI on and PCID off | actual runtime condition differs from earlier setup note; must record true cmdline | all latency results depend on this | `grep GRUB_CMDLINE_LINUX_DEFAULT /etc/default/grub` | high | confirmed |
| D24 | VMware Tools | Paper server environment does not use VMware Tools | open-vm-tools 11.0.5 and open-vm-tools-desktop installed | operator convenience between Windows host and Ubuntu VM | operator workflow only; not expected to affect LEBench metrics | `dpkg -l`: open-vm-tools 2:11.0.5-4ubuntu0.18.04.3 | low | confirmed |
| D25 | Controlled-condition opportunity from cmdline | Paper measures KPTI with/without PCID by hardware capability (Fig3) | Our pti=on/nopcid boot state fixes the "without PCID" arm; a paired run with pti=off (same kernel, same VM, one variable) gives the KPTI delta directly | VM lacks pcid, so hardware-switched arms are impossible; boot parameter is the cleanest single-factor control | C2 KPTI verdict | GRUB cmdline vs alternate pti=off boot; keep all else identical | high | confirmed |

## Decisions needed from group

- [x] Adopt corrected evidence linkage: Figure 1/Table 3/Figure 2 for main claim; KPTI §4.1.1/Figure 3; Retpoline §4.1.2/Figures 5-6. Do not use Figure 4 as main evidence.
- [x] Runner: VMware VM on Windows host, Ubuntu 18.04.6. D04-D06 limitations accepted.
- [x] Running kernel: 4.15.0-213-generic with pti=on nopcid (= paper's KPTI-without-PCID condition).
- [ ] Confirm C2 test subset: proposal = read/recv (KPTI) + select/poll/epoll (Retpoline). B/D to confirm before first run.
- [ ] Decide KPTI controlled experiment: proposed design is same kernel 4.15.0-213, run A with pti=on nopcid (current), run B with pti=off, one variable only; local test only, no production recommendation.
- [ ] Retpoline controlled experiment: TBD whether 4.15.0-213 retpoline can be disabled via spectre_v2 boot parameter; check `cat /sys/devices/system/cpu/vulnerabilities/spectre_v2` output first.
- [ ] Fill TBD cells D06 (free -h, lsblk) and D15 (python --version).

## Evidence commands already run (outputs recorded in this file's cells)

```bash
uname -a                        # 4.15.0-213-generic
lsb_release -a                  # Ubuntu 18.04.6 LTS bionic
systemd-detect-virt             # vmware
dpkg -l | grep -E 'linux-image|open-vm-tools'
grep -E 'GRUB_TIMEOUT_STYLE|GRUB_TIMEOUT|GRUB_CMDLINE_LINUX_DEFAULT' /etc/default/grub
lscpu | grep -E 'Model name|Hypervisor|pcid|ibrs|ibpb|stibp'
