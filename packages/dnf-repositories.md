
# DNF Repository Management

## Overview

Package repositories were configured and verified on the RHEL 9 application server (`app01`).

## Enabled Repositories

| Repository ID | Description |
|---|---|
| rhel-9-for-x86_64-baseos-rpms | RHEL 9 BaseOS packages |
| rhel-9-for-x86_64-appstream-rpms | RHEL 9 AppStream packages |
| docker-ce-stable | Docker CE Stable packages |

## Repository Configuration

The RHEL repositories are managed through:

`/etc/yum.repos.d/redhat.repo`

The Docker repository is configured through:

`/etc/yum.repos.d/docker-ce.repo`

Docker repository URL:

```text
https://download.docker.com/linux/rhel/9/x86_64/stable
```

## Verification

List enabled repositories:

```bash
dnf repolist --enabled
```

Inspect repository metadata:

```bash
dnf repoinfo --enabled
```

The verification confirmed that all three repositories were enabled and that DNF could access their package metadata.

## Skills Demonstrated

- DNF repository management
- RHEL BaseOS and AppStream repositories
- Third-party RPM repository integration
- Repository metadata inspection
- Package source verification
