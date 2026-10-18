# Sudo Access Control

## Overview

Role-based sudo access control was implemented on the RHEL 9 application server (`app01`) to enforce the principle of least privilege.

Three administrative roles were configured with different levels of access.

## Role-Based Permissions

| User | Group | Authorized Operations |
|---|---|---|
| ahmed | sysadmins | Full sudo administration |
| omar | developers | Restart the `infra-api` Docker container |
| khalid | webadmins | Restart the Apache HTTP service |

## 1. System Administrator Permissions

Configuration file:

`/etc/sudoers.d/sysadmins`

```sudoers
%sysadmins ALL=(ALL) ALL
```

Members of the `sysadmins` group can execute administrative commands through sudo, subject to authentication.

## 2. Developer Permissions

The developer role was restricted to restarting the existing FastAPI application container.

A dedicated root-owned script was created:

`/usr/local/sbin/restart-infra-api`

```bash
#!/bin/bash
exec /usr/bin/docker restart infra-api
```

File ownership and permissions:

```bash
chown root:root /usr/local/sbin/restart-infra-api
chmod 750 /usr/local/sbin/restart-infra-api
```

Sudo configuration:

`/etc/sudoers.d/developers`

```sudoers
%developers ALL=(root) /usr/local/sbin/restart-infra-api
```

The script uses a fixed container name rather than accepting user-supplied arguments.

This avoids granting unrestricted access to the Docker CLI.

### Developer Verification

```bash
sudo -l -U omar
```

Verified authorization:

```text
(root) /usr/local/sbin/restart-infra-api
```

The following command was successfully executed by `omar`:

```bash
sudo /usr/local/sbin/restart-infra-api
```

The `infra-api` container restarted successfully and remained running.

## 3. Web Administrator Permissions

Configuration file:

`/etc/sudoers.d/webadmins`

```sudoers
%webadmins ALL=(root) /usr/bin/systemctl restart httpd.service
```

The `webadmins` group is authorized to restart the Apache HTTP service without receiving general administrative access.

Verification:

```bash
sudo -l -U khalid
```

## 4. Sudo Configuration Security

Sudo configuration files were protected using:

```bash
chmod 0440 /etc/sudoers.d/sysadmins
chmod 0440 /etc/sudoers.d/developers
chmod 0440 /etc/sudoers.d/webadmins
```

Configuration syntax was validated using:

```bash
visudo -c
```

All four configuration files passed validation:

```text
/etc/sudoers: parsed OK
/etc/sudoers.d/developers: parsed OK
/etc/sudoers.d/sysadmins: parsed OK
/etc/sudoers.d/webadmins: parsed OK
```

## 5. Docker and Systemd Conflict Resolution

During testing, the `infra-app.service` systemd unit failed because port `8000` was already allocated to the running Docker container.

The conflict was identified using:

```bash
journalctl -u infra-app.service -n 40 --no-pager
ss -lntp | grep ':8000'
docker ps
```

The existing Docker deployment was retained, and the redundant systemd service was disabled:

```bash
systemctl disable --now infra-app.service
```

The application continued running in Docker with the following port mapping:

```text
192.168.20.10:8000 -> 8000/tcp
```

## Security Considerations

- Avoid adding restricted users to the `docker` group because Docker daemon access can provide root-equivalent privileges.
- Keep privileged scripts owned by root and protected against unauthorized modification.
- Restrict write access to Docker Compose files, service definitions, and privileged executable paths.
- Review the container's mounts, runtime privileges, and file ownership before treating the delegation as production-ready.
- Test unauthorized operations separately to confirm access restrictions.

## Skills Demonstrated

- Sudoers configuration
- Principle of least privilege
- Role-based access control
- Restricted Docker operations
- Linux file ownership and permissions
- Systemd troubleshooting
- Docker port conflict diagnosis
- Security configuration validation
