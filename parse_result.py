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

def main():
    global_state_a = {test: [] for test in TARGET_TESTS}
    global_state_b = {test: [] for test in TARGET_TESTS}

    for directory in LOG_DIRS:
        print(f"\n{'='*50}")
        print(f"Analyzing directory: {directory}")
        print(f"{'='*50}")
        
        if not os.path.exists(directory):
            print("Directory not found.")
            continue

        state_a = {test: [] for test in TARGET_TESTS}
        state_b = {test: [] for test in TARGET_TESTS}

        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                filepath = os.path.join(directory, filename)
                parsed_data = parse_file(filepath)
                
                if 'stateA' in filename:
                    for key in TARGET_TESTS:
                        if key in parsed_data:
                            state_a[key].append(parsed_data[key])
                            global_state_a[key].append(parsed_data[key])
                elif 'stateB' in filename:
                    for key in TARGET_TESTS:
                        if key in parsed_data:
                            state_b[key].append(parsed_data[key])
                            global_state_b[key].append(parsed_data[key])
                            
        results_a = {}
        results_b = {}

        print("\nState A (PTI = OFF):")
        for key, values in state_a.items():
            if values:
                mean_val = statistics.mean(values)
                stdev_val = statistics.stdev(values) if len(values) > 1 else 0.0
                results_a[key] = mean_val
                print(f"  {key:<12} Mean: {mean_val:.9f}s, Stdev: {stdev_val:.9f}s")
            
        print("\nState B (PTI = ON):")
        for key, values in state_b.items():
            if values:
                mean_val = statistics.mean(values)
                stdev_val = statistics.stdev(values) if len(values) > 1 else 0.0
                results_b[key] = mean_val
                print(f"  {key:<12} Mean: {mean_val:.9f}s, Stdev: {stdev_val:.9f}s")

        print("\nSlowdown Percentage:")
        for key in TARGET_TESTS:
            if key in results_a and key in results_b:
                mean_a = results_a[key]
                mean_b = results_b[key]
                if mean_a > 0:
                    slowdown = ((mean_b - mean_a) / mean_a) * 100
                    print(f"  {key:<12} {slowdown:+.2f}%")

    print(f"\n{'='*50}")
    print("Generating Global Excel Report...")
    
    table_data = []
    excel_tests = ['small read', 'mid read', 'big read', 'huge read']
    
    for test in excel_tests:
        vals_a = global_state_a.get(test, [])
        vals_b = global_state_b.get(test, [])
        
        if vals_a and vals_b:
            mean_a = statistics.mean(vals_a)
            stdev_a = statistics.stdev(vals_a) if len(vals_a) > 1 else 0.0
            mean_b = statistics.mean(vals_b)
            stdev_b = statistics.stdev(vals_b) if len(vals_b) > 1 else 0.0
            slowdown = ((mean_b - mean_a) / mean_a) * 100
            
            table_data.append({
                'Test Scale': test.title(),
                'State A Mean (s)': mean_a,
                'State A Stdev (s)': stdev_a,
                'State B Mean (s)': mean_b,
                'State B Stdev (s)': stdev_b,
                'Slowdown (%)': slowdown
            })
            
    if not table_data:
        print("Not enough read data across members to generate Excel.")
        return

    df = pd.DataFrame(table_data)
    
    for col in df.columns[1:5]:
        df[col] = df[col].apply(lambda x: f"{x:.9f}")
    df['Slowdown (%)'] = df['Slowdown (%)'].apply(lambda x: f"{x:+.2f}%")

    wb = Workbook()
    ws = wb.active
    ws.title = "KPTI Overhead Analysis"

    ws.merge_cells('A1:F1')
    title_cell = ws['A1']
    title_cell.value = "Direction 1: KPTI Performance Dilution Effect on Read Syscalls"
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
                
                if c_idx == 6:
                    cell.font = Font(bold=True)
                    val_str = str(value).replace('%', '')
                    try:
                        val_float = float(val_str)
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
            except:
                pass
        adjusted_width = (max_length + 2) * 1.2
        ws.column_dimensions[column].width = min(adjusted_width, 30)

    ws.freeze_panes = 'A3'

    file_path = "docs/KPTI_Overhead_Analysis.xlsx"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    wb.save(file_path)
    print(f"Success! Excel file generated at: {file_path}")

if __name__ == "__main__":
    main()
