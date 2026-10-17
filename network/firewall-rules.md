# Firewall & Network Segmentation

## Overview

The infrastructure uses RHEL 9 Firewalld to enforce network segmentation between the External, DMZ, and Internal LAN networks.

## Firewall Zones

| Zone | Interface | Network |
|---|---|---|
| External | ens160 | 192.168.67.0/24 |
| DMZ | ens192 | 192.168.10.0/24 |
| Internal | ens224 | 192.168.20.0/24 |

## Security Policies

| Policy | Source | Destination | Action |
|---|---|---|---|
| dmz-to-lan | DMZ | Internal | DROP |
| lan-to-dmz | Internal | DMZ | DROP |
| dmz-to-internet | DMZ | External | ACCEPT |
| lan-to-internet | Internal | External | ACCEPT |
| dmz-to-app | DMZ | Internal | Allow specific traffic |

### Application Access

The `dmz-to-app` policy permits:

- TCP 8000 from `web01` (192.168.10.10) to `app01` (192.168.20.10) for FastAPI access.
- TCP 2049 from `web01` to `app01` for NFS access.

### SSH Access

The `lan-to-dmz` policy includes an exception allowing TCP 22 traffic destined for `web01`.

## NAT and Port Forwarding

Masquerading is enabled on the External zone.

The following port-forwarding rule is configured:

```text
192.168.67.161:8080
        |
        v
192.168.10.10:80
```

This forwards HTTP requests to the Apache web server in the DMZ.

## Security Design

The architecture follows a segmented network model:

- The DMZ hosts the public-facing web service.
- The Internal LAN hosts the containerized application.
- Firewall policies restrict communication between security zones.
- Only explicitly permitted application and storage traffic is allowed from the DMZ into the Internal LAN.
- The gateway provides NAT and controlled port forwarding.

## Validation

The active firewall configuration was inspected using:

```bash
firewall-cmd --list-all-policies
firewall-cmd --list-all-zones
```

The configuration demonstrates practical Linux networking, Firewalld policy management, NAT, and network isolation.
