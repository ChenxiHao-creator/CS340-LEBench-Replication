#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: ./run_local.sh <experiment_tag_name>"
    exit 1
fi

TAG=$1
WORKSPACE_DIR="/home/deng/LEBench_Workspace"
LOG_DIR="$WORKSPACE_DIR/logs/deng"
mkdir -p $LOG_DIR
LOG_FILE="$LOG_DIR/${TAG}.log"

export LEBENCH_DIR="/home/deng/LEBench/"

echo "======================================="
echo "Starting local experiment: $TAG"
echo "======================================="

$WORKSPACE_DIR/scripts/precheck.sh >> $LOG_FILE 2>&1
echo "[Starting LEBench...]" | tee -a $LOG_FILE

cd $LEBENCH_DIR
echo "4.15.0-041500-generic" > kern_list

# 🌟 Core Fix 1: Clean up any residual old CSVs in the parent directory (using the correct dot wildcard)
rm -f ${LEBENCH_DIR}output.*.csv ${LEBENCH_DIR}output_file.csv 

# Enter the subdirectory to run the program
cd ${LEBENCH_DIR}TEST_DIR
sudo env LEBENCH_DIR=$LEBENCH_DIR ./OS_Eval 0 4.15.0-041500-generic >> $LOG_FILE 2>&1

# 🌟 Core Fix 2: After running, retrieve the latest generated CSV from the parent directory and rename it for backup
if ls ${LEBENCH_DIR}output.*.csv 1> /dev/null 2>&1; then
    # Find the most recently generated csv file
    LATEST_CSV=$(ls -t ${LEBENCH_DIR}output.*.csv | head -n 1)
    # Move to the logs directory and rename
    mv "$LATEST_CSV" "$LOG_DIR/${TAG}_data.csv"
    echo "✅ Backup success: ${TAG}_data.csv saved in logs." >> $LOG_FILE
else
    echo "Note: No output CSV found in LEBENCH_DIR (Data is safely recorded in the .log file)." >> $LOG_FILE
fi

echo "======================================="
echo "✅ Experiment $TAG finished!"
echo "Log saved to: $LOG_FILE"
echo "======================================="
