import os
import csv

LOG_DIRS = [
    'logs/dengwenxuan',
    'logs/haochenxi',
    'logs/suhongyu',
    'logs/zhanghanyun'
]

def parse_csv_file(filepath):
    results = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3 and 'average:' in row[1]:
                    test_name = row[0].strip()
                    try:
                        value = float(row[2].strip())
                        results[test_name] = value
                    except ValueError:
                        pass
    except Exception:
        pass 
    return results

def main():
    target_tests = ['getpid', 'ref', 'cpu', 'read', 'mmap', 'fork']
    
    for directory in LOG_DIRS:
        print(f"\n========================================")
        print(f"👤 Analyzing member data: {directory}")
        print(f"========================================")
        
        if not os.path.exists(directory):
            print(f"❌ Directory not found. Data might not be uploaded yet.")
            continue

        stateA_data = {test: [] for test in target_tests}
        stateB_data = {test: [] for test in target_tests}

        for filename in os.listdir(directory):
            if filename.endswith(".csv"):
                filepath = os.path.join(directory, filename)
                parsed_data = parse_csv_file(filepath)
                
                if 'stateA' in filename:
                    for key in target_tests:
                        if key in parsed_data:
                            stateA_data[key].append(parsed_data[key])
                elif 'stateB' in filename:
                    for key in target_tests:
                        if key in parsed_data:
                            stateB_data[key].append(parsed_data[key])
                            
        print("🟢 State A (PTI = OFF) - Unsafe but high performance")
        has_a_data = False
        for key, values in stateA_data.items():
            if values:
                avg = sum(values) / len(values)
                print(f"  ▶ {key:<6} Avg Time: {avg:.9f} sec")
                has_a_data = True
        if not has_a_data:
            print("  (No valid data found)")
            
        print("🔴 State B (PTI = ON) - Safe but incurs performance overhead")
        has_b_data = False
        for key, values in stateB_data.items():
            if values:
                avg = sum(values) / len(values)
                print(f"  ▶ {key:<6} Avg Time: {avg:.9f} sec")
                has_b_data = True
        if not has_b_data:
            print("  (No valid data found)")

if __name__ == "__main__":
    main()
