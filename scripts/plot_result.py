import matplotlib.pyplot as plt
import numpy as np

labels_light = ['getpid', 'ref', 'mmap']
stateA_light = [80.3, 12.0, 682.3]
stateB_light = [186.7, 12.0, 782.0]

labels_heavy = ['cpu', 'fork', 'read']
stateA_heavy = [2.02, 3.53, 12.11]
stateB_heavy = [2.02, 3.52, 11.87]

x1 = np.arange(len(labels_light))
x2 = np.arange(len(labels_heavy))
width = 0.35

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

rects1_A = ax1.bar(x1 - width/2, stateA_light, width, label='State A (PTI=OFF)', color='#2ca02c', alpha=0.8)
rects1_B = ax1.bar(x1 + width/2, stateB_light, width, label='State B (PTI=ON)', color='#d62728', alpha=0.8)

ax1.set_ylabel('Time (Nanoseconds - ns)', fontweight='bold')
ax1.set_title('Lightweight Syscalls Overhead\n(Notice the surge in getpid)', fontweight='bold')
ax1.set_xticks(x1)
ax1.set_xticklabels(labels_light, fontsize=11)
ax1.legend()

for rects in [rects1_A, rects1_B]:
    for rect in rects:
        height = rect.get_height()
        ax1.annotate(f'{height}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

rects2_A = ax2.bar(x2 - width/2, stateA_heavy, width, label='State A (PTI=OFF)', color='#2ca02c', alpha=0.8)
rects2_B = ax2.bar(x2 + width/2, stateB_heavy, width, label='State B (PTI=ON)', color='#d62728', alpha=0.8)

ax2.set_ylabel('Time (Milliseconds - ms)', fontweight='bold')
ax2.set_title('Heavyweight / Compute Tasks Overhead\n(Almost unaffected)', fontweight='bold')
ax2.set_xticks(x2)
ax2.set_xticklabels(labels_heavy, fontsize=11)
ax2.legend()

for rects in [rects2_A, rects2_B]:
    for rect in rects:
        height = rect.get_height()
        ax2.annotate(f'{height}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3), 
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('pti_overhead_chart.png', dpi=300)
print("✅ Chart successfully generated and saved as 'pti_overhead_chart.png'")
