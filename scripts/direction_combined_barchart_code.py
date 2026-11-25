import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
XLSX_PATH = os.path.join(BASE_DIR, 'KPTI_Overhead_Analysis.xlsx')
OUT_DIR = BASE_DIR

STATE_COLORS = {
    'A': '#2ca02c',
    'B': '#d62728',
    'C': '#1f77b4',
}

def load_sheet(sheet):
    df = pd.read_excel(XLSX_PATH, sheet_name=sheet, header=1)
    df = df.dropna(how='all')
    for col in df.columns:
        if col != df.columns[0]:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(',', '', regex=False).str.replace('%', '', regex=False).str.replace('+', '', regex=False),
                errors='coerce')
    return df

def grouped_bar(ax, categories, vals_left, std_left, label_left, color_left,
                vals_right, std_right, label_right, color_right, ylabel):
    x = np.arange(len(categories))
    w = 0.35
    ax.bar(x - w/2, vals_left,  w, yerr=std_left,  capsize=4, label=label_left,
           color=color_left, alpha=0.85, error_kw=dict(lw=1.2, ecolor='gray'))
    ax.bar(x + w/2, vals_right, w, yerr=std_right, capsize=4, label=label_right,
           color=color_right, alpha=0.85, error_kw=dict(lw=1.2, ecolor='gray'))
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, fontsize=11)
    ax.legend()
    ax.grid(axis='y', linestyle='--', alpha=0.4, which='both')

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    df_lat = load_sheet('Dir2 Latency')
    df_hw  = load_sheet('Dir2 HW Counters')

    tests = df_lat['Test'].tolist()
    means_A = df_lat['A Mean (s)'].values
    stds_A  = df_lat['A Stdev (s)'].values
    means_B = df_lat['B Mean (s)'].values
    stds_B  = df_lat['B Stdev (s)'].values
    slowdown = df_lat['B vs A (%)'].values

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5))

    x1 = np.arange(len(tests))
    w1 = 0.35

    ax1.bar(x1 - w1/2, means_A, w1, yerr=stds_A, capsize=4,
            label='State A (PTI=OFF)', color=STATE_COLORS['A'], alpha=0.85, error_kw=dict(lw=1.2, ecolor='gray'))
    ax1.bar(x1 + w1/2, means_B, w1, yerr=stds_B, capsize=4,
            label='State B (PTI=ON)', color=STATE_COLORS['B'], alpha=0.85, error_kw=dict(lw=1.2, ecolor='gray'))

    ax1.set_yscale('log')
    ax1.set_ylabel('Latency (Seconds - log scale)', fontweight='bold')
    ax1.set_title('Read Syscall Latency: State A vs State B\n(log scale, error bars = stdev)', fontweight='bold')
    ax1.set_xticks(x1)
    ax1.set_xticklabels(tests, fontsize=11)
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.4, which='both')

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
    p1 = os.path.join(OUT_DIR, 'ab_kpti_dilution_chart.png')
    plt.savefig(p1, dpi=300); plt.close()
    print(f"Chart saved to '{p1}'")

    fig, ax = plt.subplots(figsize=(9, 5.5))
    grouped_bar(ax, tests,
                df_lat['B Mean (s)'], df_lat['B Stdev (s)'], 'State B (PTI=ON, PCID off)', STATE_COLORS['B'],
                df_lat['C Mean (s)'], df_lat['C Stdev (s)'], 'State C (PTI=ON, PCID on)',  STATE_COLORS['C'],
                'Latency (Seconds - log scale)')
    ax.set_yscale('log')
    ax.set_title('Direction 2: Read Latency - State B vs State C\n(PCID mitigation, log scale, error bars = stdev)', fontweight='bold')
    for i, v in enumerate(df_lat['C vs B (PCID %)']):
        ax.annotate(f'{v:+.1f}%', xy=(i + 0.175, df_lat['C Mean (s)'].iloc[i]),
                    xytext=(0, 6), textcoords='offset points', ha='center', fontsize=9, fontweight='bold', color='#1f4e79')
    plt.tight_layout()
    p2 = os.path.join(OUT_DIR, 'dir2_bc_read_latency.png')
    plt.savefig(p2, dpi=300); plt.close()
    print(f"Chart saved to '{p2}'")

    hw = df_hw[df_hw['Metric'].isin([
        'CPU Cycles (total per run)', 'dTLB-load-misses (total per run)'
    ])]
    metrics = hw['Metric'].tolist()

    fig, ax = plt.subplots(figsize=(9, 5.5))
    grouped_bar(ax, metrics,
                hw['B Mean'], hw['B Stdev'], 'State B (PTI=ON, PCID off)', STATE_COLORS['B'],
                hw['C Mean'], hw['C Stdev'], 'State C (PTI=ON, PCID on)',  STATE_COLORS['C'],
                'Count per run (log scale)')
    ax.set_yscale('log')
    ax.set_title('Direction 2: Hardware Counters - State B vs State C\n(PCID mitigation on cycles & dTLB-load-misses, log scale)', fontweight='bold')
    ax.tick_params(axis='x', labelsize=10)
    for i, v in enumerate(hw['C vs B (PCID %)']):
        ax.annotate(f'{v:+.1f}%', xy=(i + 0.175, hw['C Mean'].iloc[i]),
                    xytext=(0, 6), textcoords='offset points', ha='center', fontsize=9, fontweight='bold', color='#1f4e79')
    plt.tight_layout()
    p3 = os.path.join(OUT_DIR, 'dir2_bc_hw_counters.png')
    plt.savefig(p3, dpi=300); plt.close()
    print(f"Chart saved to '{p3}'")

if __name__ == '__main__':
    main()
