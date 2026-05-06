---
name: SSH servers
description: Known SSH hosts from ~/.ssh/config — when user says "remote", "ssh", or names a server, use `ssh <name>`
type: reference
---

When the user says "remote", "ssh", or refers to a server by name, connect via `ssh <name>`. Available hosts from `~/.ssh/config`:

| Name | Host | User | Notes |
|------|------|------|-------|
| sorn | 203.185.144.35 | sorn | |
| sl | lanta.nstda.or.th | teiamarj | uses ~/.ssh/backup_key/id_rsa |
| tl | transfer.lanta.nstda.or.th | teiamarj | transfer node, uses ~/.ssh/backup_key/id_rsa |
| ipu | 10.222.44.224 | ipu | |
| deploy | 10.222.44.224 | deploy | |
| admin | 10.222.44.224 | admin | |
| home | h.puem.me | puem | |
| pv | 157.85.98.168 | root | |
| box1 | 192.111.0.102 | www | |
| box2 | 192.111.0.103 | www | |
| meow | 10.222.44.73 | meow-ipu | |

To run a remote command: `ssh <name> <command>`
To test connectivity: `ssh -o ConnectTimeout=10 <name> echo "connection ok"`
