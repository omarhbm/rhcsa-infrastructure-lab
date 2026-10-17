# Network Configuration & IP Addressing

## Overview

This infrastructure lab uses three RHEL servers deployed on VMware Workstation, with separate External, DMZ, and Internal LAN networks.

The `gateway01` server provides routing between the networks, while Firewalld controls permitted traffic.

## Server IP Addressing

| Hostname | Interface | IP Address | Network | Default Gateway |
|---|---|---|---|---|
| gateway01.lab.local | ens160 | 192.168.67.161/24 | External | 192.168.67.2 |
| gateway01.lab.local | ens192 | 192.168.10.1/24 | DMZ | — |
| gateway01.lab.local | ens224 | 192.168.20.1/24 | Internal LAN | — |
| web01.local.lab | ens160 | 192.168.10.10/24 | DMZ | 192.168.10.1 |
| app01.lab.local | ens160 | 192.168.20.10/24 | Internal LAN | 192.168.20.1 |

## Network Segments

### External Network

- Subnet: `192.168.67.0/24`
- Gateway interface: `ens160`
- Gateway IP: `192.168.67.161`
- Upstream router: `192.168.67.2`

This network provides upstream connectivity through VMware NAT.

### DMZ Network

- Subnet: `192.168.10.0/24`
- Gateway interface: `ens192`
- Gateway IP: `192.168.10.1`
- Web server: `192.168.10.10`

The DMZ hosts the Apache web server and reverse proxy.

### Internal LAN

- Subnet: `192.168.20.0/24`
- Gateway interface: `ens224`
- Gateway IP: `192.168.20.1`
- Application server: `192.168.20.10`

The Internal LAN hosts the containerized FastAPI application and NFS server.

## Docker Networking

Docker creates additional virtual networks on `app01`.

| Interface | Network | Status |
|---|---|---|
| docker0 | 172.17.0.0/16 | Down |
| br-b7de20df0a1f | 172.18.0.0/16 | Up |

The active Docker bridge provides networking for the Docker Compose application.

## Routing

### gateway01

The gateway has directly connected routes to all three infrastructure networks.

Default route:

```text
default via 192.168.67.2 dev ens160
```

### web01

```text
default via 192.168.10.1 dev ens160
```

### app01

```text
default via 192.168.20.1 dev ens160
```

## Network Traffic Flow

```text
Windows Workstation
        |
        | TCP 8080
        v
gateway01 (192.168.67.161)
        |
        | Port Forwarding
        v
web01 (192.168.10.10:80)
        |
        | Apache Reverse Proxy
        | TCP 8000
        v
app01 (192.168.20.10:8000)
        |
        v
FastAPI Docker Container
```

## Verification Commands

The network configuration was inspected using:

```bash
hostname
ip -br -4 addr
ip -4 route
```

## Skills Demonstrated

- RHEL network administration
- Static IPv4 configuration
- Linux routing
- Multi-homed gateway configuration
- Network segmentation
- VMware virtual networking
- Docker bridge networking
- Infrastructure documentation
