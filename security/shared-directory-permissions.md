# Shared Directory Permissions and SETGID

## Overview

A secure shared directory was configured on the RHEL 9 application server (`app01`) to allow members of the `developers` group to collaborate while restricting access from other users.

This lab demonstrates Linux file ownership, group permissions, and SETGID directory inheritance.

## 1. Directory Configuration

The shared directory was created at:

`/srv/developers`

Configuration commands:

```bash
mkdir -p /srv/developers
chown root:developers /srv/developers
chmod 2770 /srv/developers
```

## 2. Permission Explanation

The directory uses permission mode `2770`.

| Value | Meaning |
|---|---|
| 2 | Enable SETGID on the directory |
| 7 | Owner has read, write, and execute permissions |
| 7 | Group has read, write, and execute permissions |
| 0 | Other users have no permissions |

Expected directory permissions:

```text
drwxrws--- root developers /srv/developers
```

## 3. SETGID Behavior

When SETGID is enabled on a directory, newly created files and subdirectories inherit the directory's group ownership.

For example, a file created by `omar` inside `/srv/developers` inherits the `developers` group.

This helps maintain consistent group ownership in shared workspaces.

Note that SETGID does not automatically grant group write permissions to every new file. Effective permissions also depend on the user's umask or default ACLs.

## 4. Access Verification

Verify directory ownership and permissions:

```bash
ls -ld /srv/developers
```

Verify developer group membership:

```bash
id omar
```

Test file creation as the developer:

```bash
su - omar
touch /srv/developers/test.txt
ls -l /srv/developers/test.txt
exit
```

The file creation test was completed successfully.

A separate negative-access test should be performed using an account that does not belong to the `developers` group.

## 5. Security Benefits

- Group-based access control
- Restricted access for unauthorized users
- Consistent group ownership through SETGID
- Centralized shared directory management
- Reduced reliance on individual user permissions

## Skills Demonstrated

- Linux ownership management
- `chown` and `chmod`
- Special permission bits
- SETGID directory inheritance
- Group-based access control
- Filesystem permission verification
