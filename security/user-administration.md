# User and Group Administration

## Overview

Local user and group administration was configured on the RHEL 9 application server (`app01`) to demonstrate identity management, role-based access control, password aging, and shared directory permissions.

## Existing Local Accounts

| Username | UID | Home Directory | Shell |
|---|---|---|---|
| q | 1000 | /home/q | /bin/bash |
| adminuser | 1001 | /home/adminuser | /bin/bash |
| developer1 | 1002 | /home/developer1 | /bin/bash |

These accounts were created during the initial infrastructure configuration.

## Role-Based User Groups

Three additional groups were configured to separate administrative responsibilities:

| Group | User | Responsibility |
|---|---|---|
| sysadmins | ahmed | System administration |
| developers | omar | Application operations |
| webadmins | khalid | Web service operations |

The existing `adminuser` account also belongs to `sysadmins`.

### User and Group Commands

```bash
groupadd sysadmins
groupadd developers
groupadd webadmins

useradd -m -G sysadmins ahmed
useradd -m -G developers omar
useradd -m -G webadmins khalid
```

**Note:** The commands above represent the initial provisioning workflow. Existing groups should not be recreated.

Passwords were configured interactively using `passwd` and are not included in this repository.

## Password Aging Policy

Password aging was configured for the three additional accounts.

```bash
chage -M 90 -m 7 -W 14 ahmed
chage -M 90 -m 7 -W 14 omar
chage -M 90 -m 7 -W 14 khalid
```

| Setting | Value |
|---|---|
| Maximum password age | 90 days |
| Minimum password age | 7 days |
| Expiration warning | 14 days |

Verification:

```bash
chage -l ahmed
chage -l omar
chage -l khalid
```

## Shared Directory Permissions

A shared directory was configured for the developers group.

```bash
mkdir -p /srv/developers
chown root:developers /srv/developers
chmod 2770 /srv/developers
```

The `2770` permission mode provides:

- Full access for the owner and group.
- No access for other users.
- SETGID inheritance so new files and subdirectories inherit the `developers` group.

The `omar` account successfully created a test file inside the shared directory.

## Verification

```bash
id ahmed
id omar
id khalid

getent group sysadmins
getent group developers
getent group webadmins

ls -ld /srv/developers

passwd -S ahmed
passwd -S omar
passwd -S khalid
```

## Skills Demonstrated

- Linux user and group administration
- Role-based access control (RBAC)
- Password aging and account policy
- Shared directory permissions
- SETGID group inheritance
- User and group verification

For privileged command restrictions, see `sudo-access-control.md`.
