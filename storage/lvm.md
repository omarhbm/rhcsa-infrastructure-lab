
# LVM & XFS Storage Management

## Overview

This lab demonstrates Logical Volume Manager (LVM) configuration and online storage expansion on RHEL 9 using a dedicated virtual disk.

The configuration includes a physical volume, volume group, logical volume, XFS filesystem, persistent mount, and filesystem expansion without unmounting.

## Storage Architecture

| Component | Configuration |
|---|---|
| Server | app01.lab.local |
| Physical Volume | /dev/nvme0n1 |
| Volume Group | datavg |
| Logical Volume | datalv |
| Initial Logical Volume Size | 6 GiB |
| Current Logical Volume Size | 8 GiB |
| Filesystem | XFS |
| Mount Point | /data |
| Volume Group Size | Approximately 10 GiB |
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
    +-- Logical Volume: datalv (8 GiB)
    |       |
    |       v
    |    XFS Filesystem
    |       |
    |       v
    |     /data
    |
    +-- Remaining Free Space (~2 GiB)
```

## Persistent Mount Configuration

The following entry is configured in `/etc/fstab`:

```fstab
/dev/datavg/datalv  /data  xfs  defaults  0 0
```

This configures the filesystem to mount automatically during system startup.

## Initial LVM Configuration

Before expansion, the logical volume was 6 GiB.

Initial verification:

```text
LV      VG       LSize
datalv  datavg   6.00g
```

The volume group originally had approximately 4 GiB of available space.

## Logical Volume Expansion

The `datalv` logical volume was expanded from 6 GiB to 8 GiB.

### Step 1: Expand the Logical Volume

```bash
lvextend -L 8G /dev/datavg/datalv
```

### Step 2: Grow the XFS Filesystem

```bash
xfs_growfs /data
```

XFS supports online filesystem growth, allowing the mounted `/data` filesystem to be expanded without unmounting it.

### Step 3: Verify the New Size

```bash
df -h /data
```

Verified output:

```text
Filesystem                 Size  Used Avail Use% Mounted on
/dev/mapper/datavg-datalv  8.0G   90M  7.9G   2% /data
```

The output confirms that the mounted filesystem now has a total size of 8.0 GiB.

## Filesystem Verification

The filesystem was verified as XFS and mounted at `/data`.

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
df -h /data
grep '/data' /etc/fstab
```

## Skills Demonstrated

- Physical Volume management
- Volume Group management
- Logical Volume configuration
- Online Logical Volume expansion
- XFS filesystem growth
- Persistent filesystem mounting
- LVM capacity management
- Storage verification and troubleshooting

## Notes

The logical volume was successfully expanded from 6 GiB to 8 GiB, and the XFS filesystem was grown to use the additional capacity.

The expansion was performed on the dedicated data volume without modifying the root or swap logical volumes.
