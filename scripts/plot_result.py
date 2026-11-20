import os
import statistics
import matplotlib.pyplot as plt
import numpy as np

LOG_DIR = 'logs/zhanghanyun'
TARGET_TESTS = [
    'getpid', 'ref', 'cpu',
    'small read', 'mid read', 'big read', 'huge read'
]

def parse_file(filepath):
    results = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.split(',')
                if len(parts) >= 2 and 'average:' in parts[0]:
                    raw_name = parts[0].replace('average:', '').strip()
                    test_name = " ".join(raw_name.split())
                    try:
                        results[test_name] = float(parts[1].strip())
                    except ValueError:
                        pass
    except Exception:
        pass
    return results

def load_means(directory):
    data = {
        'A': {t: [] for t in TARGET_TESTS},
        'B': {t: [] for t in TARGET_TESTS},
        'C': {t: [] for t in TARGET_TESTS},
    }
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory not found: {directory}")

    for filename in os.listdir(directory):
        if not filename.endswith('.csv'):
            continue
        parsed = parse_file(os.path.join(directory, filename))
        state = None
        if 'stateA' in filename:
            state = 'A'
        elif 'stateB' in filename:
            state = 'B'
        elif 'stateC' in filename:
            state = 'C'

        if state:
            for t in TARGET_TESTS:
                if t in parsed:
                    data[state][t].append(parsed[t])

    means = {s: {} for s in ['A', 'B', 'C']}
    for s in ['A', 'B', 'C']:
        for t in TARGET_TESTS:
            if data[s][t]:
                means[s][t] = statistics.mean(data[s][t])
    return means

def main():
    means = load_means(LOG_DIR)

    for s in ['A', 'B', 'C']:
        if not means[s]:
            print(f"⚠️ Warning: No data found for State {s} in {LOG_DIR}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))


    light_tests = [t for t in ['getpid', 'ref'] if t in means['A'] and t in means['B'] and t in means['C']]
    x1 = np.arange(len(light_tests))
    w1 = 0.25

    vals_A_ns = [means['A'][t] * 1e9 for t in light_tests]
    vals_B_ns = [means['B'][t] * 1e9 for t in light_tests]
    vals_C_ns = [means['C'][t] * 1e9 for t in light_tests]

    r1_A = ax1.bar(x1 - w1, vals_A_ns, w1, label='State A (PTI=OFF, nopcid)', color='#2ca02c', alpha=0.85)
    r1_B = ax1.bar(x1,      vals_B_ns, w1, label='State B (PTI=ON, nopcid)',  color='#d62728', alpha=0.85)
    r1_C = ax1.bar(x1 + w1, vals_C_ns, w1, label='State C (PTI=ON, PCID=ON)', color='#1f77b4', alpha=0.85)

    ax1.set_ylabel('Latency (Nanoseconds - ns)', fontweight='bold')
    ax1.set_title('Lightweight Syscalls Latency\n(KPTI Penalty & PCID Mitigation)', fontweight='bold')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(light_tests, fontsize=11)
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.4)

    for rects in [r1_A, r1_B, r1_C]:
        for rect in rects:
            h = rect.get_height()
            ax1.annotate(f'{h:.1f}',
                         xy=(rect.get_x() + rect.get_width() / 2, h),
                         xytext=(0, 3), textcoords="offset points",
                         ha='center', va='bottom', fontsize=8.5)

    overhead_tests = [
        t for t in ['getpid', 'small read', 'mid read', 'big read', 'huge read', 'cpu']
        if t in means['A'] and t in means['B'] and t in means['C'] and means['A'][t] > 0
    ]
    x2 = np.arange(len(overhead_tests))
    w2 = 0.35

    ov_B = [((means['B'][t] - means['A'][t]) / means['A'][t]) * 100 for t in overhead_tests]
    ov_C = [((means['C'][t] - means['A'][t]) / means['A'][t]) * 100 for t in overhead_tests]

    r2_B = ax2.bar(x2 - w2/2, ov_B, w2, label='State B vs A (PTI=ON, nopcid)', color='#d62728', alpha=0.85)
    r2_C = ax2.bar(x2 + w2/2, ov_C, w2, label='State C vs A (PTI=ON, PCID=ON)', color='#1f77b4', alpha=0.85)

    ax2.axhline(0, color='black', linewidth=0.8)
    ax2.set_ylabel('Overhead vs State A (%)', fontweight='bold')
    ax2.set_title('KPTI Overhead & Dilution Effect\n(Lower is Better)', fontweight='bold')
    ax2.set_xticks(x2)
    ax2.set_xticklabels([t.replace(' ', '\n') for t in overhead_tests], fontsize=10)
    ax2.legend()
    ax2.grid(axis='y', linestyle='--', alpha=0.4)

    for rects in [r2_B, r2_C]:
        for rect in rects:
            h = rect.get_height()
            va = 'bottom' if h >= 0 else 'top'
            offset = 3 if h >= 0 else -10
            ax2.annotate(f'{h:+.1f}%',
                         xy=(rect.get_x() + rect.get_width() / 2, h),
                         xytext=(0, offset), textcoords="offset points",
                         ha='center', va=va, fontsize=8)

    plt.tight_layout()
    out_path = 'docs/pti_pcid_overhead_chart.png'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=300)
    print(f"✅ Chart successfully generated and saved as '{out_path}'")

if __name__ == "__main__":
    main()
