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

# Key point: Hardcode the environment variable in the script!
export LEBENCH_DIR=/home/deng/LEBench

echo "======================================"
echo "Starting local experiment: $TAG"
echo "======================================"

# 1. Record environment
$WORKSPACE_DIR/scripts/precheck.sh >> $LOG_FILE 2>&1

echo "[Starting LEBench...]" | tee -a $LOG_FILE

# 2. Enter LEBench to run benchmarks
cd $LEBENCH_DIR

# ⚠️ Because perf reports <not supported> in the VM, we comment out the perf line to avoid exiting with an error
# sudo perf stat -e cycles,dTLB-load-misses,dTLB-loads \
#     python run.py -t read >> $LOG_FILE 2>&1

# Automatically generate kernel list
echo "4.15.0-041500-generic" > kern_list

# Directly call the underlying C program
cd $LEBENCH_DIR/TEST_DIR
sudo env LEBENCH_DIR=$LEBENCH_DIR ./OS_Eval 0 4.15.0-041500-generic >> $LOG_FILE 2>&1

echo "======================================"
echo "✅ Experiment $TAG finished!"
echo "Log saved to: $LOG_FILE"
echo "======================================"
