# SELinux Security Configuration

## Overview

This lab demonstrates SELinux configuration on RHEL 9 while maintaining Apache HTTP Server functionality as a reverse proxy.

**Server:** `web01.local.lab`

## SELinux Status

SELinux is enabled and operating in enforcing mode.

```text
SELinux status: enabled
Loaded policy name: targeted
Current mode: enforcing
Mode from config file: enforcing
```

The configured mode is also enforcing, ensuring that SELinux remains enabled after reboot under the current configuration.

## Apache Reverse Proxy Integration

Apache forwards requests from `/api/` to the FastAPI application hosted on `app01` at `192.168.20.10:8000`.

SELinux controls whether Apache processes can initiate outbound network connections.

The following Boolean is enabled:

```text
httpd_can_network_connect --> on
```

This permits Apache to initiate network connections while SELinux remains in enforcing mode.

## Verification Commands

```bash
getenforce
getsebool httpd_can_network_connect
sestatus
```

## Security Approach

- SELinux remains enabled.
- Enforcing mode is maintained.
- The targeted SELinux policy is used.
- Apache network connectivity is permitted through the appropriate SELinux Boolean.
- SELinux was not disabled to make the reverse proxy work.

## Skills Demonstrated

- SELinux status verification
- SELinux enforcing mode
- SELinux Boolean management
- Apache and SELinux integration
- Linux security troubleshooting
