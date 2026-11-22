#!/bin/bash
# run_local_perf.sh -- run_local.sh + perf stat collection (output appended to .log)
# Usage: ./run_local_perf.sh <experiment_tag_name>
# Example: ./run_local_perf.sh stateB_pti_on_nopcid_perf_run1

if [ -z "$1" ]; then
    echo "Usage: ./run_local_perf.sh <experiment_tag_name>"
    echo "Example: ./run_local_perf.sh stateB_pti_on_nopcid_perf_run1"
    exit 1
fi

TAG=$1
WORKSPACE_DIR="/home/deng/LEBench_Workspace"
LOG_DIR="$WORKSPACE_DIR/logs/deng"
mkdir -p $LOG_DIR
LOG_FILE="$LOG_DIR/${TAG}.log"
: > "$LOG_FILE"
PERF_FILE="$LOG_DIR/${TAG}_perf_stat.txt"

export LEBENCH_DIR="/home/deng/LEBench/"


PERF_BIN=$(command -v perf || true)
if [ -z "$PERF_BIN" ]; then
    PERF_BIN=$(ls /usr/lib/linux-tools/*/perf 2>/dev/null | head -n 1)
fi
if [ -z "$PERF_BIN" ]; then
    echo "❌ perf not found. Please install it first:"
    echo "   sudo apt install linux-tools-common linux-tools-4.15.0-041500-generic -y"
    exit 1
fi
echo "[perf] using: $PERF_BIN"

echo "======================================"
echo "Starting local experiment (with perf): $TAG"
echo "======================================"

$WORKSPACE_DIR/scripts/precheck.sh >> $LOG_FILE 2>&1
echo "[Starting LEBench...]" | tee -a $LOG_FILE

cd $LEBENCH_DIR
echo "4.15.0-041500-generic" > kern_list

# Clean up any residual old CSVs in the parent directory
rm -f ${LEBENCH_DIR}output.*.csv ${LEBENCH_DIR}output_file.csv

# Run OS_Eval wrapped in perf stat (counters will inherit into fork/thread child processes)
cd ${LEBENCH_DIR}TEST_DIR
sudo $PERF_BIN stat -o "$PERF_FILE" \
  -e task-clock,cycles,instructions,context-switches,cpu-migrations,page-faults,cpu/event=0xcb,umask=0x01/ \
  -- env LEBENCH_DIR=$LEBENCH_DIR ./OS_Eval 0 4.15.0-041500-generic >> $LOG_FILE 2>&1

# Backup CSV
if ls ${LEBENCH_DIR}output.*.csv 1> /dev/null 2>&1; then
    LATEST_CSV=$(ls -t ${LEBENCH_DIR}output.*.csv | head -n 1)
    mv "$LATEST_CSV" "$LOG_DIR/${TAG}_data.csv"
    echo "✅ Backup success: ${TAG}_data.csv saved in logs." >> $LOG_FILE
else
    echo "Note: No output CSV found in LEBENCH_DIR (Data is safely recorded in the .log file)." >> $LOG_FILE
fi

# 🌟 Append perf report to the end of .log (also keep the standalone _perf_stat.txt)
if [ -s "$PERF_FILE" ]; then
    {
        echo ""
        echo "########## perf stat report (also saved as ${TAG}_perf_stat.txt) ##########"
        cat "$PERF_FILE"
        echo "###########################################################################"
    } >> "$LOG_FILE"
    echo "✅ perf stat saved: ${TAG}_perf_stat.txt (content also appended to the end of ${TAG}.log)" | tee -a $LOG_FILE
else
    echo "⚠️ perf stat report was not generated (file is empty or does not exist). Please check if perf is working properly." | tee -a $LOG_FILE
fi

echo "======================================"
echo "✅ Experiment $TAG finished!"
echo "Log saved to:  $LOG_FILE"
echo "Perf saved to: $PERF_FILE"
echo "======================================"
