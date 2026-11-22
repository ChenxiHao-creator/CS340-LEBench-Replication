import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(BASE_DIR, 'kptixlsx', 'KPTI_Overhead_Analysis.xlsx')
OUT_PATH = os.path.join(BASE_DIR, 'docs', 'ab_kpti_dilution_chart.png')

def load_table(path):
    df = pd.read_excel(path, header=1)
    df = df[df['Test Scale'].notna()]
    df['Slowdown (%)'] = (
        df['Slowdown (%)'].astype(str).str.replace('%', '', regex=False).str.replace('+', '', regex=False).astype(float)
    )
    return df

def main():
    df = load_table(XLSX_PATH)

    tests = df['Test Scale'].tolist()
    means_A = df['State A Mean (s)'].values
    stds_A  = df['State A Stdev (s)'].values
    means_B = df['State B Mean (s)'].values
    stds_B  = df['State B Stdev (s)'].values
    slowdown = df['Slowdown (%)'].values

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    # ---- Left: Latency comparison (log scale) ----
    x1 = np.arange(len(tests))
    w1 = 0.35

    r1_A = ax1.bar(x1 - w1/2, means_A, w1, yerr=stds_A, capsize=4,
                   label='State A (PTI=OFF)', color='#2ca02c', alpha=0.85, error_kw=dict(lw=1.2, ecolor='gray'))
    r1_B = ax1.bar(x1 + w1/2, means_B, w1, yerr=stds_B, capsize=4,
                   label='State B (PTI=ON)', color='#d62728', alpha=0.85, error_kw=dict(lw=1.2, ecolor='gray'))

    ax1.set_yscale('log')
    ax1.set_ylabel('Latency (Seconds - log scale)', fontweight='bold')
    ax1.set_title('Read Syscall Latency: State A vs State B\n(log scale, error bars = stdev)', fontweight='bold')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(tests, fontsize=11)
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.4, which='both')

    # ---- Right: KPTI slowdown / dilution ----
    colors = ['#d62728' if v > 0 else '#2ca02c' for v in slowdown]
    r2 = ax2.bar(np.arange(len(tests)), slowdown, 0.5, color=colors, alpha=0.85)

    ax2.axhline(0, color='black', linewidth=0.8)
    ax2.set_ylabel('Slowdown vs State A (%)', fontweight='bold')
    ax2.set_title('KPTI Performance Dilution Effect\n(Higher Read Cost -> Lower Overhead %)', fontweight='bold')
    ax2.set_xticks(np.arange(len(tests)))
    ax2.set_xticklabels(tests, fontsize=11)
    ax2.grid(axis='y', linestyle='--', alpha=0.4)

    for rect, v in zip(r2, slowdown):
        h = rect.get_height()
        va = 'bottom' if h >= 0 else 'top'
        offset = 3 if h >= 0 else -3
        ax2.annotate(f'{v:+.2f}%',
                     xy=(rect.get_x() + rect.get_width() / 2, h),
                     xytext=(0, offset), textcoords="offset points",
                     ha='center', va=va, fontsize=9)

    plt.tight_layout()
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    plt.savefig(OUT_PATH, dpi=300)
    print(f"Chart saved to '{OUT_PATH}'")

if __name__ == "__main__":
    main()
