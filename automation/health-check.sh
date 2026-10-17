
#!/bin/bash

echo "===== System Health Report ====="
echo "Hostname: $(hostname)"
echo "Date: $(date)"

echo "===== Uptime ====="
uptime

echo "===== Memory ====="
free -h

echo "===== Disk Usage ====="
df -h / /data

echo "===== Docker Status ====="
systemctl is-active docker
