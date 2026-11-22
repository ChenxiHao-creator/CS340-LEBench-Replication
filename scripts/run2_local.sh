#!/bin/bash
# run_local_perf.sh —— run_local.sh + perf stat 采集（报告并入 .log）
# 用法: ./run_local_perf.sh <experiment_tag_name>
# 示例: ./run_local_perf.sh stateB_pti_on_nopcid_perf_run1

if [ -z "$1" ]; then
    echo "Usage: ./run_local_perf.sh <experiment_tag_name>"
    echo "示例: ./run_local_perf.sh stateB_pti_on_nopcid_perf_run1"
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

# 自动寻找可用的 perf
PERF_BIN=$(command -v perf || true)
if [ -z "$PERF_BIN" ]; then
    PERF_BIN=$(ls /usr/lib/linux-tools/*/perf 2>/dev/null | head -n 1)
fi
if [ -z "$PERF_BIN" ]; then
    echo "❌ 找不到 perf。请先安装："
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

# 清理父目录里可能残留的旧 CSV
rm -f ${LEBENCH_DIR}output.*.csv ${LEBENCH_DIR}output_file.csv

# OS_Eval 包在 perf stat 里运行（计数会继承到 fork/线程子进程）
cd ${LEBENCH_DIR}TEST_DIR
sudo $PERF_BIN stat -o "$PERF_FILE" \
  -e task-clock,cycles,instructions,context-switches,cpu-migrations,page-faults,cpu/event=0xcb,umask=0x01/ \
  -- env LEBENCH_DIR=$LEBENCH_DIR ./OS_Eval 0 4.15.0-041500-generic >> $LOG_FILE 2>&1

# CSV 备份
if ls ${LEBENCH_DIR}output.*.csv 1> /dev/null 2>&1; then
    LATEST_CSV=$(ls -t ${LEBENCH_DIR}output.*.csv | head -n 1)
    mv "$LATEST_CSV" "$LOG_DIR/${TAG}_data.csv"
    echo "✅ Backup success: ${TAG}_data.csv saved in logs." >> $LOG_FILE
else
    echo "Note: No output CSV found in LEBENCH_DIR (Data is safely recorded in the .log file)." >> $LOG_FILE
fi

# 🌟 perf 报告追加进 .log 尾部（同时保留单独的 _perf_stat.txt）
if [ -s "$PERF_FILE" ]; then
    {
        echo ""
        echo "########## perf stat report (also saved as ${TAG}_perf_stat.txt) ##########"
        cat "$PERF_FILE"
        echo "###########################################################################"
    } >> "$LOG_FILE"
    echo "✅ perf stat saved: ${TAG}_perf_stat.txt（内容已同时并入 ${TAG}.log 尾部）" | tee -a $LOG_FILE
else
    echo "⚠️ perf stat 报告未生成（文件为空或不存在），请检查 perf 是否正常工作。" | tee -a $LOG_FILE
fi

echo "======================================"
echo "✅ Experiment $TAG finished!"
echo "Log saved to:  $LOG_FILE"
echo "Perf saved to: $PERF_FILE"
echo "======================================"
