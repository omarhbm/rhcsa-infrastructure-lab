# NFS & AutoFS Storage Configuration

## Overview

This lab implements NFS shared storage between two RHEL servers across segmented networks.

- **NFS Server:** `app01.lab.local` — `192.168.20.10`
- **AutoFS Client:** `web01.local.lab` — `192.168.10.10`
- **NFS Export:** `/srv/nfs/shared`
- **Client Mount Path:** `/remote/shared`
- **Protocol:** NFSv4

## NFS Server Configuration

**Server:** `app01`

The following export is configured in `/etc/exports`:

```text
/srv/nfs/shared 192.168.10.10(rw,sync,root_squash,no_subtree_check)
```

### Export Options

| Option | Description |
|---|---|
| `rw` | Allows read/write requests, subject to filesystem permissions |
| `sync` | Uses synchronous write handling |
| `root_squash` | Maps remote root requests to an anonymous identity |
| `no_subtree_check` | Disables subtree checking |

The exported directory has the following permissions:

```text
drwxrwxr-x+ root root /srv/nfs/shared
```

The `+` indicates that extended ACL entries exist. Their contents were not included in this inspection.

### NFS Service Status

```text
systemctl is-enabled nfs-server
enabled

systemctl is-active nfs-server
active
```

## AutoFS Client Configuration

**Client:** `web01`

### Master Map

File: `/etc/auto.master.d/*.autofs`

```text
/remote /etc/auto.remote
```

### Indirect Map

File: `/etc/auto.remote`

```text
shared -fstype=nfs4,rw 192.168.20.10:/srv/nfs/shared
```

This maps the NFS export to `/remote/shared` and allows AutoFS to mount it on demand.

### AutoFS Service Status

```text
systemctl is-enabled autofs
enabled

systemctl is-active autofs
active
```

## Firewall Integration

The gateway's `dmz-to-app` policy explicitly permits TCP port `2049` from `web01` to `app01`.

Other DMZ-to-Internal LAN traffic is restricted by the network segmentation policies.

## Verification

The following commands can be used to verify the configuration:

```bash
# On app01
exportfs -v
systemctl status nfs-server

# On web01
ls /remote/shared
findmnt /remote/shared
systemctl status autofs
```

## Skills Demonstrated

- NFS server configuration
- NFS export security
- AutoFS indirect maps
- On-demand network filesystem mounting
- Systemd service management
- Network storage across segmented networks
- Firewall integration
