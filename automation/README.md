# System Automation & Health Monitoring

## Overview

This lab implements automated system health reporting on `app01.lab.local` using Bash, systemd services, systemd timers, and cron.

The health-check script collects:

- Hostname and current date
- System uptime
- Memory utilization
- Filesystem usage for `/` and `/data`
- Docker service status

## Bash Script

File: `health-check.sh`

The script uses standard Linux administration commands to generate a system health report.

## Systemd Service

File: `health-check.service`

A `Type=oneshot` service executes the script and appends its output to:

```text
/var/log/health-check-timer.log
```

## Systemd Timer

File: `health-check.timer`

The timer is configured with:

```ini
OnBootSec=5min
OnUnitActiveSec=30min
```

It schedules the first execution after boot and subsequent executions approximately 30 minutes after the service was last activated.

## Cron Job

The root crontab also contains a daily scheduled health check:

```cron
0 8 * * * /usr/local/bin/health-check.sh >> /var/log/health-check.log 2>&1
```

This runs daily at 08:00 according to the server's configured cron timezone.

The cron job and systemd timer use separate log files. Both schedules are documented here for demonstration purposes.

## Installation

Copy the script to the server:

```bash
sudo install -m 755 health-check.sh /usr/local/bin/health-check.sh
```

Copy the systemd unit files:

```bash
sudo cp health-check.service health-check.timer /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now health-check.timer
```

To configure the optional daily cron job, run `sudo crontab -e` and add the cron entry shown above.

## Verification

```bash
systemctl status health-check.timer
systemctl list-timers --all
sudo systemctl start health-check.service
sudo tail -n 30 /var/log/health-check-timer.log
```

## Skills Demonstrated

- Bash scripting
- Cron scheduling
- Systemd service units
- Systemd timer units
- Automated health reporting
- Log file redirection
- Service troubleshooting
