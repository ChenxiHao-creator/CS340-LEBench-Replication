import matplotlib.pyplot as plt
import numpy as np


labels_light = ['getpid', 'ref', 'mmap']
stateA_light = [80.3, 12.0, 682.3]    # State A: PTI=OFF, nopcid
stateB_light = [186.7, 12.0, 782.0]   # State B: PTI=ON, nopcid
stateC_light = [120.0, 12.0, 710.0]   # State C: PTI=ON, PCID=ON 

labels_heavy = ['cpu', 'fork', 'read']
stateA_heavy = [2.02, 3.53, 12.11]    # State A: PTI=OFF, nopcid
stateB_heavy = [2.02, 3.52, 11.87]    # State B: PTI=ON, nopcid
stateC_heavy = [2.02, 3.50, 11.95]    # State C: PTI=ON, PCID=ON 

x1 = np.arange(len(labels_light))
x2 = np.arange(len(labels_heavy))
width = 0.25  

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

r1_A = ax1.bar(x1 - width, stateA_light, width, label='State A (PTI=OFF, nopcid)', color='#2ca02c', alpha=0.85)
r1_B = ax1.bar(x1,         stateB_light, width, label='State B (PTI=ON, nopcid)',  color='#d62728', alpha=0.85)
r1_C = ax1.bar(x1 + width, stateC_light, width, label='State C (PTI=ON, PCID=ON)', color='#1f77b4', alpha=0.85)

ax1.set_ylabel('Time (Nanoseconds - ns)', fontweight='bold')
ax1.set_title('Lightweight Syscalls Overhead\n(KPTI Penalty & PCID Mitigation)', fontweight='bold')
ax1.set_xticks(x1)
ax1.set_xticklabels(labels_light, fontsize=11)
ax1.legend()

r2_A = ax2.bar(x2 - width, stateA_heavy, width, label='State A (PTI=OFF, nopcid)', color='#2ca02c', alpha=0.85)
r2_B = ax2.bar(x2,         stateB_heavy, width, label='State B (PTI=ON, nopcid)',  color='#d62728', alpha=0.85)
r2_C = ax2.bar(x2 + width, stateC_heavy, width, label='State C (PTI=ON, PCID=ON)', color='#1f77b4', alpha=0.85)

ax2.set_ylabel('Time (Milliseconds - ms)', fontweight='bold')
ax2.set_title('Heavyweight / Compute Tasks Overhead\n(Minimal Impact)', fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(labels_heavy, fontsize=11)
ax2.legend()

for ax, rect_groups in [(ax1, [r1_A, r1_B, r1_C]), (ax2, [r2_A, r2_B, r2_C])]:
    for rects in rect_groups:
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}' if height < 100 else f'{height:.1f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('pti_pcid_overhead_chart.png', dpi=300)
print("✅ Chart saved as 'pti_pcid_overhead_chart.png'")
