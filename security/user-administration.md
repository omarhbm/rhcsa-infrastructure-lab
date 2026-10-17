
# User and Group Administration

## Overview

User and group administration was configured and verified on the RHEL 9 application server (`app01`).

## Local Users

| Username | UID | Home Directory | Shell |
|---|---|---|---|
| q | 1000 | /home/q | /bin/bash |
| adminuser | 1001 | /home/adminuser | /bin/bash |
| developer1 | 1002 | /home/developer1 | /bin/bash |

## Administrative Group

A dedicated administrative group is configured:

```text
sysadmins:x:1001:adminuser
```

The `adminuser` account is a member of the `sysadmins` group.

## Sudo Configuration

Configuration file:

`/etc/sudoers.d/sysadmins`

```sudoers
%sysadmins ALL=(ALL) ALL
```

This grants members of the `sysadmins` group permission to execute commands as any user through sudo, subject to sudo authentication requirements.

## Verification

The following commands were used:

```bash
getent passwd
getent group
sudo -l -U adminuser
grep -RnE '^[[:space:]]*[^#[:space:]].*(adminuser|sysadmins)' /etc/sudoers /etc/sudoers.d/
```

The verification confirmed that `adminuser` has sudo permissions through the `sysadmins` group.

## Skills Demonstrated

- Local user administration
- Linux groups and group membership
- Sudo privilege management
- User and group verification
- Access control configuration
