#!/bin/bash
echo "======================================"
echo "      环境预检查 (Precheck)          "
echo "======================================"

echo -e "\n[1] 内核版本 (Kernel Version):"
uname -r

echo -e "\n[2] 当前启动参数 (Cmdline):"
cat /proc/cmdline

echo -e "\n[3] KPTI 状态 (Isolation):"
if dmesg | grep -q "Kernel/User page tables isolation: enabled"; then
    echo "=> KPTI 是【开启】状态 (enabled)"
else
    echo "=> KPTI 是【关闭】状态 (disabled / pti=off)"
fi

echo -e "\n[4] CPU 是否支持 PCID:"
if grep -q "pcid" /proc/cpuinfo; then
    echo "=> 支持 PCID (存在 pcid flag)"
else
    echo "=> 不支持 PCID"
fi

echo -e "\n[5] 当前 CPU 调频模式 (Governor):"
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo "未开启调频 (可能不支持)"

echo -e "\n[6] 当前频率 (MHz):"
lscpu | grep "MHz"

echo "======================================"
