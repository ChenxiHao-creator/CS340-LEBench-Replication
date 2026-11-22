#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import glob
import hashlib
import statistics
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.utils.dataframe import dataframe_to_rows

LOG_DIRS = [
    'logs/dengwenxuan',
    'logs/haochenxi',
    'logs/suhongyu',
    'logs/zhanghanyun'
]
PERF_POOL_DIR = 'logs/perf_All'

READ_TESTS = ['small read', 'mid read', 'big read', 'huge read']
STATES = ['stateA', 'stateB', 'stateC']
STATE_LABELS = {
    'stateA': 'A (pti=off)',
    'stateB': 'B (pti=on nopcid, PCID off)',
    'stateC': 'C (pti=on, PCID on)',
}

RUNNER_MAP = {
    'suhongyu': 'suhongyu', 'su': 'suhongyu',
    'dengwenxuan': 'dengwenxuan', 'deng': 'dengwenxuan',
    'haochenxi': 'haochenxi', 'hao': 'haochenxi',
    'zhanghanyun': 'zhanghanyun', 'zhang': 'zhanghanyun',
}
RUNNER_KEYS = sorted(RUNNER_MAP.keys(), key=len, reverse=True)

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

def parse_perf_blocks(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
    except Exception:
        return [], None, None, None

    runner = None
    m = re.search(r'LEBENCH_DIR=(\S+)', content)
    if m:
        path = m.group(1).lower()
        for k in RUNNER_KEYS:
            if k in path:
                runner = RUNNER_MAP[k]
                break

    kernel = None
    m = re.search(r"OS_Eval 0 (\S+?)'?:", content)
    if m:
        kernel = m.group(1)

    header_state = None
    m = re.search(r'4\.15\.0-213-([ABC])', content)
    if m:
        header_state = 'state' + m.group(1)

    blocks = []
    for chunk in content.split('Performance counter stats for')[1:]:
        cycles = 0
        n_cyc = 0
        dtlb = 0
        n_dtlb = 0
        elapsed = None
        for line in chunk.splitlines():
            em = re.search(r'([\d.]+)\s+seconds time elapsed', line)
            if em:
                if elapsed is None:
                    elapsed = float(em.group(1))
                continue
            core = line.split('#')[0]
            tokens = core.split()
            if len(tokens) < 2 or not re.fullmatch(r'[\d,]+', tokens[0]):
                continue
            val = int(tokens[0].replace(',', ''))
            event = tokens[1]
            if 'cycles' in event:
                cycles += val
                n_cyc += 1
            elif 'dTLB-load-misses' in event or 'umask=0x01' in event:
                dtlb += val
                n_dtlb += 1
        if n_cyc:
            blocks.append({
                'cycles': cycles,
                'dtlb': dtlb if n_dtlb else None,
                'elapsed': elapsed,
            })
    return blocks, runner, kernel, header_state

def detect_state_from_log(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            head = f.read(8192)
        for line in head.splitlines():
            if 'BOOT_IMAGE=' in line:
                if 'pti=off' in line:
                    return 'stateA'
                if 'pti=on' in line and 'nopcid' in line:
                    return 'stateB'
                if 'pti=on' in line:
                    return 'stateC'
        for line in head.splitlines():
            if 'pti=' in line and 'cmdline should be' not in line and 'confirmed' not in line:
                if 'pti=off' in line:
                    return 'stateA'
                if 'pti=on' in line and 'nopcid' in line:
                    return 'stateB'
                if 'pti=on' in line:
                    return 'stateC'
    except Exception:
        pass
    return None

def state_of(filename):
    for s in STATES:
        if s in filename:
            return s
    return None

def collect_latency():
    latency = {s: {t: [] for t in READ_TESTS} for s in STATES}
    print(f"\n{'='*60}\n[1/2] 延迟数据（*_data.csv，状态由同名 .log 的真实 cmdline 判定）\n{'='*60}")
    for directory in LOG_DIRS:
        if not os.path.exists(directory):
            print(f"  目录不存在，跳过: {directory}")
            continue
        for filename in sorted(os.listdir(directory)):
            if not filename.endswith('.csv'):
                continue
            state = state_of(filename)
            if state is None:
                continue
            filepath = os.path.join(directory, filename)
            eff = state
            tag = filename[:-len('_data.csv')] if filename.endswith('_data.csv') else filename[:-4]
            logpath = os.path.join(directory, tag + '.log')
            if os.path.exists(logpath):
                det = detect_state_from_log(logpath)
                if det:
                    eff = det
                else:
                    print(f"  ⚠️  {directory}/{filename}: 同名 log 里没有 cmdline，按文件名 {state} 归类（建议人工确认）")
            parsed = parse_file(filepath)
            for t in READ_TESTS:
                if t in parsed:
                    latency[eff][t].append(parsed[t])
            member = os.path.basename(directory)
            print(f"  [CSV] {member:<12} {filename:<26} -> {STATE_LABELS[eff]}")
    return latency

def member_from_pool_filename(fname):
    stem = fname.rsplit('.', 1)[0]
    m = re.match(r'([A-Za-z]+)_perf_(state[ABC])$', stem)
    if m:
        return RUNNER_MAP.get(m.group(1).lower()), m.group(2)
    m = re.match(r'perf_(state[ABC])$', stem)
    if m:
        return 'suhongyu', m.group(1)
    return None, None

def collect_counters():
    best = {}

    def consider(member, state, blocks, src, kernel, prio):
        if member is None or state is None or not blocks:
            return
        key = (member, state)
        h = hashlib.md5(str(blocks).encode()).hexdigest()
        if key not in best:
            best[key] = (prio, src, kernel, blocks, {h})
            return
        cur = best[key]
        if prio < cur[0]:
            print(f"  ℹ️  {member}/{state}: 采用 {src}（替换较低优先级来源 {cur[1]}）")
            best[key] = (prio, src, kernel, blocks, {h})
        elif prio == cur[0]:
            if h in cur[4]:
                print(f"  ℹ️  {member}/{state}: 跳过 {src}（与已采用的 {cur[1]} 内容完全相同，不重复计数）")
            else:
                print(f"  ℹ️  {member}/{state}: 合并 {src}（同一状态的另一轮运行）")
                best[key] = (prio, cur[1] + ' + ' + src, kernel, cur[3] + blocks, cur[4] | {h})
        else:
            print(f"  ℹ️  {member}/{state}: 跳过 {src}（已有更高优先级来源 {cur[1]}）")

    def runner_check(fname, member, runner):
        if runner and runner != member:
            print(f"  ⚠️  {fname}: 内容路径显示真正跑的人是 {runner}，与文件位置/名字({member})不一致 → 改记为 {runner}")
            return runner
        return member

    print(f"\n{'='*60}\n[2/2] 硬件计数器（perf stat，状态只认文件名，去重后每人每状态只计一次）\n{'='*60}")

    if os.path.isdir(PERF_POOL_DIR):
        for fname in sorted(os.listdir(PERF_POOL_DIR)):
            if not fname.endswith('.txt'):
                continue
            member, state = member_from_pool_filename(fname)
            if state is None:
                print(f"  ⚠️  {PERF_POOL_DIR}/{fname}: 文件名认不出状态，已跳过")
                continue
            path = os.path.join(PERF_POOL_DIR, fname)
            blocks, runner, kernel, header_state = parse_perf_blocks(path)
            member = runner_check(f'{PERF_POOL_DIR}/{fname}', member, runner)
            if header_state and header_state != state:
                print(f"  ⚠️  {PERF_POOL_DIR}/{fname}: 文件内 perf 标题写的是 4.15.0-213-{header_state[-1]}，文件名却是 {state} → 以文件名为准（当时 GRUB 条目名可能没改）")
            consider(member, state, blocks, f'{PERF_POOL_DIR}/{fname}', kernel, 1)
    else:
        print(f"  目录不存在: {PERF_POOL_DIR}")

    for directory in LOG_DIRS:
        if not os.path.isdir(directory):
            continue
        member = os.path.basename(directory)
        for path in sorted(glob.glob(os.path.join(directory, 'perf_state[ABC]*'))):
            fname = os.path.basename(path)
            state = state_of(fname)
            blocks, runner, kernel, header_state = parse_perf_blocks(path)
            member2 = runner_check(f'{directory}/{fname}', member, runner)
            if header_state and header_state != state:
                print(f"  ⚠️  {directory}/{fname}: 文件内 perf 标题写的是 4.15.0-213-{header_state[-1]}，文件名却是 {state} → 以文件名为准")
            consider(member2, state, blocks, f'{directory}/{fname}', kernel, 2)

    for directory in LOG_DIRS:
        if not os.path.isdir(directory):
            continue
        member = os.path.basename(directory)
        for path in sorted(glob.glob(os.path.join(directory, '*.log'))):
            state = detect_state_from_log(path)
            if state is None:
                continue
            blocks, runner, kernel, _ = parse_perf_blocks(path)
            member2 = runner_check(f'{directory}/{os.path.basename(path)}', member, runner)
            consider(member2, state, blocks, f'{directory}/{os.path.basename(path)}(log内嵌)', kernel, 3)

    counters = {s: {'cycles': [], 'dtlb': [], 'elapsed': []} for s in STATES}
    print(f"\n  {'成员':<12} {'状态':<8} {'样本数':<6} 内核版本              来源")
    print('  ' + '-' * 80)
    for (member, state) in sorted(best, key=lambda k: (STATES.index(k[1]), k[0])):
        _, src, kernel, blocks, _ = best[(member, state)]
        for b in blocks:
            counters[state]['cycles'].append(b['cycles'])
            if b['dtlb'] is not None:
                counters[state]['dtlb'].append(b['dtlb'])
            if b['elapsed'] is not None:
                counters[state]['elapsed'].append(b['elapsed'])
        print(f"  {member:<12} {state:<8} {len(blocks):<6} {str(kernel):<21} {src}")

    for member_dir in LOG_DIRS:
        member = os.path.basename(member_dir)
        if not os.path.isdir(member_dir):
            continue
        for s in STATES:
            if (member, s) not in best:
                print(f"  ⚠️  缺 {member} 的 {s} 硬件计数器（可把 perf 输出按 {member}_perf_{s}.txt 放进 {PERF_POOL_DIR}/）")
    return counters

def mean_std(vals):
    if not vals:
        return None, None
    m = statistics.mean(vals)
    sd = statistics.stdev(vals) if len(vals) > 1 else 0.0
    return m, sd

def build_latency_df(latency):
    rows = []
    for t in READ_TESTS:
        ma, sa = mean_std(latency['stateA'][t])
        mb, sb = mean_std(latency['stateB'][t])
        mc, sc = mean_std(latency['stateC'][t])
        if ma is None or mb is None:
            continue
        row = {
            'Test': t.title(),
            'A Mean (s)': f"{ma:.9f}", 'A Stdev (s)': f"{sa:.9f}",
            'B Mean (s)': f"{mb:.9f}", 'B Stdev (s)': f"{sb:.9f}",
            'B vs A (%)': f"{(mb - ma) / ma * 100:+.2f}%",
        }
        if mc is not None:
            row['C Mean (s)'] = f"{mc:.9f}"
            row['C Stdev (s)'] = f"{sc:.9f}"
            row['C vs A (%)'] = f"{(mc - ma) / ma * 100:+.2f}%"
            row['C vs B (PCID %)'] = f"{(mc - mb) / mb * 100:+.2f}%"
        else:
            row['C Mean (s)'] = 'N/A'; row['C Stdev (s)'] = 'N/A'
            row['C vs A (%)'] = 'N/A'; row['C vs B (PCID %)'] = 'N/A'
        rows.append(row)
    rows.append({
        'Test': 'Paper Ref (Fig.3, small read)',
        'A Mean (s)': '-', 'A Stdev (s)': '-',
        'B Mean (s)': '-', 'B Stdev (s)': '-', 'B vs A (%)': '+113.00%',
        'C Mean (s)': '-', 'C Stdev (s)': '-', 'C vs A (%)': '+47.00%', 'C vs B (PCID %)': '-'
    })
    return pd.DataFrame(rows)

def build_counter_df(counters):
    rows = []
    for label, key in [('CPU Cycles (total per run)', 'cycles'),
                       ('dTLB-load-misses (total per run)', 'dtlb'),
                       ('Wall Time (s per run)', 'elapsed')]:
        ma, sa = mean_std(counters['stateA'][key])
        mb, sb = mean_std(counters['stateB'][key])
        mc, sc = mean_std(counters['stateC'][key])
        if ma is None or mb is None:
            continue
        fmt = "{:,.0f}" if key != 'elapsed' else "{:.2f}"
        row = {
            'Metric': label,
            'A Mean': fmt.format(ma), 'A Stdev': fmt.format(sa),
            'B Mean': fmt.format(mb), 'B Stdev': fmt.format(sb),
            'B vs A (%)': f"{(mb - ma) / ma * 100:+.2f}%",
        }
        if mc is not None:
            row['C Mean'] = fmt.format(mc); row['C Stdev'] = fmt.format(sc)
            row['C vs A (%)'] = f"{(mc - ma) / ma * 100:+.2f}%"
            row['C vs B (PCID %)'] = f"{(mc - mb) / mb * 100:+.2f}%"
        else:
            row['C Mean'] = 'N/A'; row['C Stdev'] = 'N/A'
            row['C vs A (%)'] = 'N/A'; row['C vs B (PCID %)'] = 'N/A'
        rows.append(row)
    return pd.DataFrame(rows)

def write_styled_sheet(ws, title, df, highlight_cols):
    num_cols = len(df.columns)
    end_col_letter = get_column_letter(num_cols)
    ws.merge_cells(f'A1:{end_col_letter}1')
    title_cell = ws['A1']
    title_cell.value = title
    title_cell.font = Font(size=14, bold=True, color="FFFFFF")
    title_cell.fill = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30
    header_font = Font(bold=True, color="FFFFFF")
    header_fill = PatternFill(start_color="4472C4", end_color="4472C4", fill_type="solid")
    header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    thin_border = Border(left=Side(style='thin', color='D9D9D9'),
                         right=Side(style='thin', color='D9D9D9'),
                         top=Side(style='thin', color='D9D9D9'),
                         bottom=Side(style='thin', color='D9D9D9'))
    for r_idx, row in enumerate(dataframe_to_rows(df, index=False, header=True), 2):
        for c_idx, value in enumerate(row, 1):
            cell = ws.cell(row=r_idx, column=c_idx, value=value)
            if r_idx == 2:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = header_alignment
            else:
                cell.alignment = Alignment(horizontal="center", vertical="center")
                if c_idx in highlight_cols and isinstance(value, str) and '%' in value:
                    cell.font = Font(bold=True)
                    try:
                        val_float = float(value.replace('%', ''))
                        if val_float > 50:
                            cell.fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
                            cell.font = Font(bold=True, color="9C0006")
                        elif val_float > 10:
                            cell.fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
                            cell.font = Font(bold=True, color="9C5700")
                        else:
                            cell.fill = PatternFill(start_color="C6EFCE", end_color="C6EFCE", fill_type="solid")
                            cell.font = Font(bold=True, color="006100")
                    except ValueError:
                        pass
            cell.border = thin_border
    for idx, col in enumerate(ws.columns, 1):
        max_length = 0
        column = get_column_letter(idx)
        for cell in col:
            if cell.coordinate in ws.merged_cells:
                continue
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except Exception:
                pass
        ws.column_dimensions[column].width = min((max_length + 2) * 1.2, 30)
    ws.freeze_panes = 'A3'

def main():
    latency = collect_latency()
    counters = collect_counters()

    print(f"\n{'='*60}")
    print("Direction 2 Summary (all members aggregated)")
    print(f"{'='*60}")
    df_lat = build_latency_df(latency)
    df_cnt = build_counter_df(counters)
    with pd.option_context('display.max_columns', None, 'display.width', 250):
        print("\n[延迟] read 测试 average 口径")
        print(df_lat.to_string(index=False))
        print("\n[硬件计数器] perf stat 整轮总量")
        print(df_cnt.to_string(index=False))

    wb = Workbook()
    first = True
    if not df_lat.empty:
        ws = wb.active
        ws.title = "Dir2 Latency"
        write_styled_sheet(ws,
            "Direction 2: PCID Mitigation on KPTI Overhead - Read Latency (Paper Fig.3: B +113%, C +47%)",
            df_lat, highlight_cols=[6, 9, 10])
        first = False
    if not df_cnt.empty:
        ws = wb.active if first else wb.create_sheet()
        ws.title = "Dir2 HW Counters"
        write_styled_sheet(ws,
            "Direction 2: Hardware Evidence from perf stat (whole-run totals)",
            df_cnt, highlight_cols=[6, 9, 10])

    if wb.sheetnames:
        file_path = "docs/Direction2_PCID_Analysis.xlsx"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        wb.save(file_path)
        print(f"\nSuccess! Excel file generated at: {file_path}")
    else:
        print("\nNo data collected, Excel not generated.")

if __name__ == "__main__":
    main()
