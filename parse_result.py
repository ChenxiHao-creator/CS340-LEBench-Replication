import os
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
                        value = float(parts[1].strip())
                        results[test_name] = value
                    except ValueError:
                        pass
    except Exception:
        pass
    return results

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

def build_dataframe(tests, data_a, data_b, data_c):
    table_data = []
    for test in tests:
        vals_a = data_a.get(test, [])
        vals_b = data_b.get(test, [])
        vals_c = data_c.get(test, [])

        if vals_a and vals_b:
            mean_a = statistics.mean(vals_a)
            stdev_a = statistics.stdev(vals_a) if len(vals_a) > 1 else 0.0
            mean_b = statistics.mean(vals_b)
            stdev_b = statistics.stdev(vals_b) if len(vals_b) > 1 else 0.0
            slowdown_ba = ((mean_b - mean_a) / mean_a) * 100 if mean_a > 0 else 0.0

            row = {
                'Test': test.title(),
                'State A Mean (s)': f"{mean_a:.9f}",
                'State A Stdev (s)': f"{stdev_a:.9f}",
                'State B Mean (s)': f"{mean_b:.9f}",
                'State B Stdev (s)': f"{stdev_b:.9f}",
                'B vs A (%)': f"{slowdown_ba:+.2f}%"
            }

            if vals_c:
                mean_c = statistics.mean(vals_c)
                stdev_c = statistics.stdev(vals_c) if len(vals_c) > 1 else 0.0
                slowdown_ca = ((mean_c - mean_a) / mean_a) * 100 if mean_a > 0 else 0.0
                diff_cb = ((mean_c - mean_b) / mean_b) * 100 if mean_b > 0 else 0.0
                row['State C Mean (s)'] = f"{mean_c:.9f}"
                row['State C Stdev (s)'] = f"{stdev_c:.9f}"
                row['C vs A (%)'] = f"{slowdown_ca:+.2f}%"
                row['C vs B (PCID %)'] = f"{diff_cb:+.2f}%"
            else:
                row['State C Mean (s)'] = "N/A"
                row['State C Stdev (s)'] = "N/A"
                row['C vs A (%)'] = "N/A"
                row['C vs B (PCID %)'] = "N/A"

            table_data.append(row)
    return pd.DataFrame(table_data)

def main():
    global_state_a = {test: [] for test in TARGET_TESTS}
    global_state_b = {test: [] for test in TARGET_TESTS}
    global_state_c = {test: [] for test in TARGET_TESTS}

    zhang_state_a = {test: [] for test in TARGET_TESTS}
    zhang_state_b = {test: [] for test in TARGET_TESTS}
    zhang_state_c = {test: [] for test in TARGET_TESTS}

    for directory in LOG_DIRS:
        print(f"\n{'='*55}")
        print(f"Analyzing directory: {directory}")
        print(f"{'='*55}")

        if not os.path.exists(directory):
            print("Directory not found.")
            continue

        state_a = {test: [] for test in TARGET_TESTS}
        state_b = {test: [] for test in TARGET_TESTS}
        state_c = {test: [] for test in TARGET_TESTS}

        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                filepath = os.path.join(directory, filename)
                parsed_data = parse_file(filepath)

                if 'stateA' in filename:
                    for key in TARGET_TESTS:
                        if key in parsed_data:
                            state_a[key].append(parsed_data[key])
                            global_state_a[key].append(parsed_data[key])
                            if 'zhanghanyun' in directory:
                                zhang_state_a[key].append(parsed_data[key])
                elif 'stateB' in filename:
                    for key in TARGET_TESTS:
                        if key in parsed_data:
                            state_b[key].append(parsed_data[key])
                            global_state_b[key].append(parsed_data[key])
                            if 'zhanghanyun' in directory:
                                zhang_state_b[key].append(parsed_data[key])
                elif 'stateC' in filename:
                    for key in TARGET_TESTS:
                        if key in parsed_data:
                            state_c[key].append(parsed_data[key])
                            global_state_c[key].append(parsed_data[key])
                            if 'zhanghanyun' in directory:
                                zhang_state_c[key].append(parsed_data[key])

        results_a, results_b, results_c = {}, {}, {}

        for label, state_dict, res_dict in [
            ("State A (PTI=OFF, nopcid)", state_a, results_a),
            ("State B (PTI=ON,  nopcid)", state_b, results_b),
            ("State C (PTI=ON,  PCID=ON)", state_c, results_c),
        ]:
            if any(state_dict.values()):
                print(f"\n{label}:")
                for key, values in state_dict.items():
                    if values:
                        mean_val = statistics.mean(values)
                        stdev_val = statistics.stdev(values) if len(values) > 1 else 0.0
                        res_dict[key] = mean_val
                        print(f"  {key:<12} Mean: {mean_val:.9f}s, Stdev: {stdev_val:.9f}s (n={len(values)})")

        print("\nOverhead & Mitigation Comparison:")
        for key in TARGET_TESTS:
            if key in results_a and key in results_b and results_a[key] > 0:
                ba = ((results_b[key] - results_a[key]) / results_a[key]) * 100
                line = f"  {key:<12} B vs A: {ba:+7.2f}%"
                if key in results_c:
                    ca = ((results_c[key] - results_a[key]) / results_a[key]) * 100
                    cb = ((results_c[key] - results_b[key]) / results_b[key]) * 100 if results_b[key] > 0 else 0.0
                    line += f" | C vs A: {ca:+7.2f}% | C vs B (PCID): {cb:+7.2f}%"
                print(line)

    print(f"\n{'='*55}")
    print("Generating Excel Report...")

    wb = Workbook()

    # Sheet 1: Global Read Syscalls
    excel_tests = ['small read', 'mid read', 'big read', 'huge read']
    df_global = build_dataframe(excel_tests, global_state_a, global_state_b, global_state_c)
    if not df_global.empty:
        ws1 = wb.active
        ws1.title = "Global Read Analysis"
        write_styled_sheet(
            ws1,
            "Direction 1: KPTI & PCID Effect on Read Syscalls (Global)",
            df_global,
            highlight_cols=[6, 9]
        )

    # Sheet 2: ZhangHanyun All Tests (A vs B vs C)
    df_zhang = build_dataframe(TARGET_TESTS, zhang_state_a, zhang_state_b, zhang_state_c)
    if not df_zhang.empty:
        ws2 = wb.create_sheet(title="ZhangHanyun A-B-C")
        write_styled_sheet(
            ws2,
            "Physical Machine (zhanghanyun): State A vs B vs C Full Comparison",
            df_zhang,
            highlight_cols=[6, 9]
        )

    file_path = "docs/KPTI_Overhead_Analysis.xlsx"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    wb.save(file_path)
    print(f"Success! Excel file generated at: {file_path}")

if __name__ == "__main__":
    main()
