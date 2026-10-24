# Deviations from SOSP'19 LEBench Setup

Maintainer: Member C.
Rule: add a row before changing any experimental condition; after running, attach evidence path and update status.

Severity: high = may change Figure 1/Table 3 direction or verdict; medium = may change magnitude/variance; low = documentation risk.
Status: expected / confirmed / controlled / accepted-risk.

| ID | Item | Paper original setting | Our setting used | Reason | Affects | Controlled check / evidence | Severity | Status |
|---:|---|---|---|---|---|---|---|---|
| D01 | Claim-figure linkage | Main latency/root-cause claim supported by Figure 1, Table 3, Figure 2; security details in §4.1 | same | group note incorrectly used Figure 4 as main evidence | report structure | this deviation note | high | confirmed |
| D02 | Architecture scope | paper focuses x86 server; sensitivity on Intel laptop only | x86-64 only | course/group scope | all | report scope statement | low | confirmed |
| D03 | Runner OS | Linux with /boot, GRUB, sudo, reboot-based kernel switching | Windows 10/11 for static scan only now | LEBench run.py requires Linux root/grub; Windows cannot run it | feasibility | get_kern.py:4; run.py:76; run.py:180-183 | high | confirmed |
| D04 | Machine type | HP DL160G9 bare-metal server for main results | <FILL: bare-metal/VM; hypervisor if VM> | lab availability | absolute latency; variance | `systemd-detect-virt`; hypervisor info | high | expected |
| D05 | CPU model | Intel Xeon E5-2630v3 Haswell-EP, 2.40GHz, L1 512KB/L2 2MB/L3 20MB | <FILL: our CPU model/stepping> | different microarchitecture/generation | all; especially idle-state/TLB/PCID claims | `lscpu`; flags pcid/ibrs/ibpb/stibp if shown | high | expected |
| D06 | Memory/storage | 128GB 1866MHz DDR4; 960GB SSD | <FILL: RAM size/speed; disk type> | different memory hierarchy | big-read/big-fork/select variance | `free -h`; `lsblk` | medium | expected |
| D07 | Kernel version set | 36 versions: majors 3.0-3.19 and 4.0-4.20, latest minor before next major | <FILL: reduced subset> | old kernels/packages hard to obtain; time limited | Figure 1 evolution claim | list versions + source + dates | high | expected |
| D08 | Kernel config source | Ubuntu distribution kernels, not vanilla default | <FILL: Ubuntu release + kernel package + config path> | distro config affects root-cause enablement | all root-cause attributions | `/boot/config-$(uname -r)`; `apt policy linux-image-*` | high | expected |
| D09 | Security mitigations | KPTI after 4.14; Retpoline in 4.14; usercopy since 4.8; SLAB randomization since 4.7; PCID used for Fig1/Table3 | <FILL: defaults on chosen kernels; boot params if any> | modern kernels enable mitigations by default; CPU features differ | security claim; KPTI/Retpoline verdict | `grep . /sys/devices/system/cpu/vulnerabilities/*`; `cat /proc/cmdline`; `lscpu | grep pcid` | high | expected |
| D10 | PCID optimization | paper Figure1/Table3 obtained with PCID optimization; Fig3 shows with/without PCID | <FILL: our CPU PCID support and kernel use> | KPTI cost depends on PCID | KPTI magnitude | `lscpu`; kernel config `CONFIG_X86_UMIP`/PCID-related if present | medium | expected |
| D11 | Repetitions/statistics | 10,000 repetitions; K-best K=5 tolerance=5% | same if repo config allows; at least 3 full benchmark runs for course | must match paper estimator | all reported numbers | runner config; raw logs; summary script | high | expected |
| D12 | Reduced workload scale | Figure1/Table3 cover full LEBench matrix | <FILL: included tests; excluded tests> | time/compute constraints | claim scope | included/excluded table tied to Fig1 rows | high | expected |
| D13 | Table1 workload selection | Spark/PostgreSQL/Chromium/kernel-build used with strace to select syscalls | likely skipped | selection workloads are heavy and not needed to run microbench | setup provenance | state as limitation | medium | expected |
| D14 | Macrobenchmark validation | Redis/Apache/Nginx 100k requests, 50/100 concurrency; disable 11 causes for impact | optional/later | time | extension/real-world impact only | benchmark configs if run | medium | expected |
| D15 | Python version | repo uses Python 2 style print in run.py | <FILL: python2 not available / converted to py3> | modern systems lack Python 2 | runner feasibility | `python --version`; `2to3` patch if used | medium | expected |
| D16 | Paths/hard-coding | repo expects Linux paths such as /boot and /iteration | keep relative paths in our scripts; document absolute OS paths | reproducibility grading | clean-machine build | README/commands; no hard-coded user paths in our docs | medium | expected |
| D17 | Log/trace retention | paper reports trends; course requires traceability | logs/<date>_kernel_<ver>_<test>.txt + summary.csv; large logs not committed | repo size and grading | traceability | .gitignore; log naming convention | low | expected |
| D18 | Safety note for disabling mitigations | paper disables/configures features for analysis | we only do controlled local tests if needed; do not recommend disabling security mitigations in production | ethics/security | security claim wording | explicit note in report | medium | confirmed |

## Decisions needed from group

- [ ] Adopt corrected evidence linkage: Figure 1/Table 3/Figure 2 for main claim; KPTI §4.1.1/Figure 3; Retpoline §4.1.2/Figures 5-6. Do not use Figure 4 as main evidence.
- [ ] Choose reduced kernel subset: must justify at least one pre-KPTI/Retpoline and one post-KPTI/Retpoline kernel if we claim security mechanisms cause slowdown.
- [ ] Decide runner: bare-metal vs VM. If VM, record hypervisor and accept D04-D06 limitations.
- [ ] Decide whether we only reproduce trends or also attempt controlled config/patch disabling. Any disablement must be one-factor-at-a-time and documented as local testing only.
