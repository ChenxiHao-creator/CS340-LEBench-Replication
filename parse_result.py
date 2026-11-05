import os
import re
import numpy as np

LOG_DIRS = ['../logs/deng', '../logs/han', '../logs/zhang']

def parse_log_file(filepath):
    results = {
        'latency': [],
        'cycles': [],
        'dTLB-load-misses': [],
        'dTLB-loads': []
    }
    
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            
            lat_match = re.search(r'Latency:\s+([0-9.]+)', content)
            cyc_match = re.search(r'([0-9,]+)\s+cycles', content)
            dtlb_miss_match = re.search(r'([0-9,]+)\s+dTLB-load-misses', content)
            dtlb_load_match = re.search(r'([0-9,]+)\s+dTLB-loads', content)
            
            if lat_match:
                results['latency'].append(float(lat_match.group(1)))
            if cyc_match:
                results['cycles'].append(int(cyc_match.group(1).replace(',', '')))
            if dtlb_miss_match:
                results['dTLB-load-misses'].append(int(dtlb_miss_match.group(1).replace(',', '')))
            if dtlb_load_match:
                results['dTLB-loads'].append(int(dtlb_load_match.group(1).replace(',', '')))
                
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        
    return results

def calculate_statistics(data_list):
    if not data_list:
        return None, None
    return np.mean(data_list), np.std(data_list)

def main():
    print("Scanning log directories...")
    for directory in LOG_DIRS:
        if os.path.exists(directory):
            print(f"Found directory: {directory}")
            for filename in os.listdir(directory):
                if filename.endswith(".log"):
                    filepath = os.path.join(directory, filename)
                    data = parse_log_file(filepath)
        else:
            print(f"Warning: Directory {directory} not found. Please check uploads.")

if __name__ == "__main__":
    main()
