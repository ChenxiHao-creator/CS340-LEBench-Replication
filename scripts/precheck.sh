#!/bin/bash
echo "======================================"
echo "      Environment Precheck            "
echo "======================================"

echo -e "\n[1] Kernel Version:"
uname -r

echo -e "\n[2] Current Boot Cmdline:"
cat /proc/cmdline

echo -e "\n[3] KPTI Status (Isolation):"
if dmesg | grep -q "Kernel/User page tables isolation: enabled"; then
    echo "=> KPTI is [ENABLED]"
else
    echo "=> KPTI is [DISABLED] (disabled / pti=off)"
fi

echo -e "\n[4] PCID Status:"
if grep -q "nopcid" /proc/cmdline; then
    echo "=> [DISABLED] (boot parameter active: nopcid)"
elif grep -q "pcid" /proc/cpuinfo; then
    echo "=> [NOT DISABLED / ENABLED] (CPU supported and no nopcid parameter)"
else
    echo "=> [NOT SUPPORTED] (CPU hardware does not support PCID)"
fi

echo -e "\n[5] Current CPU Frequency Governor:"
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor 2>/dev/null || echo "Frequency scaling not enabled (possibly unsupported)"

echo -e "\n[6] Current Frequency (MHz):"
lscpu | grep "MHz"

echo "======================================"
