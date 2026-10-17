# LVM & XFS Storage Management

## Overview

This lab demonstrates Logical Volume Manager (LVM) configuration on RHEL 9 using a dedicated virtual disk.

The storage configuration includes a physical volume, volume group, logical volume, XFS filesystem, and persistent filesystem mount.

## Storage Architecture

| Component | Configuration |
|---|---|
| Server | app01.lab.local |
| Physical Volume | /dev/nvme0n1 |
| Volume Group | datavg |
| Logical Volume | datalv |
| Logical Volume Size | 6 GiB |
| Filesystem | XFS |
| Mount Point | /data |
| Volume Group Size | Approximately 10 GiB |
| Free Space | Approximately 4 GiB |
| Physical Extent Size | 4 MiB |

## LVM Layout

```text
/dev/nvme0n1
    |
    v
Physical Volume (PV)
    |
    v
Volume Group: datavg (~10 GiB)
    |
    +-- Logical Volume: datalv (6 GiB)
    |       |
    |       v
    |    XFS Filesystem
    |       |
    |       v
    |     /data
    |
    +-- Free Space (~4 GiB)
```

## Persistent Mount Configuration

The following entry is configured in `/etc/fstab`:

```fstab
/dev/datavg/datalv  /data  xfs  defaults  0 0
```

This configures the filesystem to be mounted automatically during system startup.

## Verification

### Logical Volumes

The `lvs` command confirmed the following logical volume:

```text
LV      VG       LSize
datalv  datavg   6.00g
```

### Volume Group

The `vgdisplay datavg` command confirmed:

```text
VG Name: datavg
VG Status: resizable
PE Size: 4.00 MiB
Total PE: 2559
Allocated PE: 1536
Free PE: 1023
```

### Filesystem Mount

The `findmnt /data` command confirmed:

```text
TARGET  SOURCE                    FSTYPE
/data   /dev/mapper/datavg-datalv xfs
```

## Verification Commands

```bash
lsblk -f
pvs
vgs
lvs
vgdisplay datavg
findmnt /data
grep '/data' /etc/fstab
```

## Skills Demonstrated

- Physical Volume management
- Volume Group management
- Logical Volume configuration
- XFS filesystem management
- Persistent filesystem mount configuration
- LVM storage inspection and troubleshooting

## Notes

The logical volume is currently 6 GiB, with approximately 4 GiB of free space remaining in the volume group.

Logical volume expansion is not documented as completed in this verification.
