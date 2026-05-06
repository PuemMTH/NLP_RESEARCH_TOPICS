# Claude Memory Import

Imported from `~/.claude/MEMORY.md` and `~/.claude/memory/*.md` on 2026-05-06.

## Memory Index

- SSH servers: known SSH hosts; when user says `remote`, `ssh`, or a server name, use `ssh <name>`.
- tl server z navigation: main folder `/lustrefs/disk/project/lt200203-aimedi/puem/tmp`; use `z <keyword>` to jump directories on `tl`.
- LANTA cluster job submission and GPU: A100-SXM4-40GB, CUDA 12.7, account `lt200203`, SBATCH templates, partition list.
- SSH tl tmux send-keys: use `tmux send-keys -t 0` instead of ssh one-liners for interactive commands on `tl`.

## SSH tl: tmux Send-Keys

When executing commands on `tl` (`transfer.lanta.nstda.or.th`), do not use bare `ssh tl 'command'` one-liners for interactive work. Use tmux send-keys so the user can see commands run inside their tmux session.

Required pattern:

```bash
ssh tl 'tmux ls 2>/dev/null'
ssh tl 'tmux send-keys -t <session> "command" Enter'
ssh tl 'tmux new-session -d -s main'
ssh tl 'tmux send-keys -t main "command" Enter'
```

Never call send-keys without checking first. If no tmux server is running, it fails with `no server running`.

Apply this as follows:

- Default target session: `0` if attached, fallback `main`.
- Use plain `ssh tl '...'` for read-only queries where output should return to Codex.
- Use send-keys for commands the user wants to see or interact with in their terminal.

## LANTA HPC Cluster

Account and identity:

- SSH via `tl` (`transfer.lanta.nstda.or.th`, user `teiamarj`).
- SLURM account: `lt200203`.
- Main working folder: `/lustrefs/disk/project/lt200203-aimedi/puem/tmp`.

GPU hardware confirmed by test job `5674528`:

- GPU: NVIDIA A100-SXM4-40GB.
- VRAM: 40 GB.
- CUDA Version: 12.7.
- Driver: 565.57.01.
- Tested node: `lanta-g-175` (`x1001c7s7b0n0`).

Partitions:

| Partition | Time limit | Notes |
| --- | --- | --- |
| `gpu` | 5 days | main GPU partition |
| `gpu-devel` | 2 hours | for testing, usually has idle nodes |
| `gpu-limited` | 1 day | limited access |
| `compute` | 5 days | CPU only |
| `compute-devel` | 2 hours | CPU testing |
| `compute-long` | 10 days | long CPU jobs |

Aliases in `~/.bashrc`:

```bash
q
qo
```

Useful commands:

```bash
sinfo
sbatch <script.sh>
scancel <jobid>
tmux ls
```

Tools and paths:

- `uv`: `/home/teiamarj/.local/bin/uv`.
- `mise`: `/home/teiamarj/.local/bin/mise`.
- `z`: sourced from `~/z.sh`.

Conda environments:

| Path | Notes |
| --- | --- |
| `/lustrefs/disk/project/lt200203-aimedi/puem/envs/env_test` | general test env |
| `/lustrefs/disk/project/lt200203-aimedi/puem/envs/env_yolo` | YOLO env |
| `/lustrefs/disk/modules/easybuild/software/Mamba/23.11.0-0/envs/pytorch-2.2.2` | system PyTorch |
| `/lustrefs/disk/modules/easybuild/software/Mamba/23.11.0-0/envs/lightning-2.2.5` | system Lightning |

SBATCH template for `gpu-devel`:

```bash
#!/bin/bash
#SBATCH -p gpu-devel
#SBATCH -N 1 -c 4
#SBATCH --gpus=1
#SBATCH --ntasks-per-node=1
#SBATCH -t 0:10:00
#SBATCH -A lt200203
#SBATCH -J <job-name>
#SBATCH --output=/lustrefs/disk/project/lt200203-aimedi/puem/tmp/<name>-%j.out
```

SBATCH template for production `gpu`:

```bash
#!/bin/bash
#SBATCH -p gpu
#SBATCH -N 1 -c 16
#SBATCH --gpus=1
#SBATCH --ntasks-per-node=1
#SBATCH -t 8:00:00
#SBATCH -A lt200203
#SBATCH -J <job-name>
#SBATCH --output=./logs-gpu-%j.out
```

Jupyter on `gpu-devel`:

- Script path: `/lustrefs/disk/project/lt200203-aimedi/puem/tmp/run-jupyter.sh`.
- After submit, check log for SSH tunnel command: `ssh -L <port>:<node>:<port> teiamarj@transfer.lanta.nstda.or.th -i id_rsa`.

Apply this as follows:

- Always use account `-A lt200203` when submitting jobs.
- Use `gpu-devel` for quick tests.
- Output quick-test logs to `/lustrefs/disk/project/lt200203-aimedi/puem/tmp/`.
- Reference script: `/lustrefs/disk/project/lt200203-aimedi/pung/run-gpu.sh`.
- Load modules before conda: `module purge && module load Mamba FFmpeg cuda`.

## SSH Servers

When the user says `remote`, `ssh`, or refers to a server by name, connect via `ssh <name>`.

| Name | Host | User | Notes |
| --- | --- | --- | --- |
| `sorn` | `203.185.144.35` | `sorn` | |
| `sl` | `lanta.nstda.or.th` | `teiamarj` | uses `~/.ssh/backup_key/id_rsa` |
| `tl` | `transfer.lanta.nstda.or.th` | `teiamarj` | transfer node, uses `~/.ssh/backup_key/id_rsa` |
| `ipu` | `10.222.44.224` | `ipu` | |
| `deploy` | `10.222.44.224` | `deploy` | |
| `admin` | `10.222.44.224` | `admin` | |
| `home` | `h.puem.me` | `puem` | |
| `pv` | `157.85.98.168` | `root` | |
| `box1` | `192.111.0.102` | `www` | |
| `box2` | `192.111.0.103` | `www` | |
| `meow` | `10.222.44.73` | `meow-ipu` | |

To run a remote command: `ssh <name> <command>`.
To test connectivity: `ssh -o ConnectTimeout=10 <name> echo "connection ok"`.

## tl z Navigation

On `tl`, directory navigation uses the `z` jump tool from `~/z.sh`.

Main working folder: `/lustrefs/disk/project/lt200203-aimedi/puem/tmp`.

Use:

```bash
source ~/z.sh
z <keyword>
z -l <keyword>
```

Apply this as follows:

- Use `z <keyword>` shorthand in interactive sessions.
- Use full paths for non-interactive commands because `z` requires an interactive shell with `z.sh` sourced.

Top frecently used paths:

| Score | Path |
| --- | --- |
| 1319 | `/lustrefs/disk/home/teiamarj` |
| 405 | `/lustrefs/disk/project/lt200203-aimedi/puem/dms` |
| 404 | `/lustrefs/disk/project/lt200203-aimedi/puem` |
| 288 | `/lustrefs/disk/project/lt200203-aimedi/puem/hashing_cross-verification` |
| 283 | `/lustrefs/disk/project/lt200203-aimedi` |
| 249 | `/lustrefs/disk/project/lt200384-ff_bio/puem` |
| 220 | `/lustrefs/disk/project/lt200384-ff_bio/puem/ocr/ocr_dicom/cli-ocr-models` |
| 220 | `/lustrefs/disk/project/lt200384-ff_bio/puem/ocr/ocr_list/dicom_ocr` |
| 172 | `/lustrefs/disk/project/lt200203-aimedi/pung/LVEF_Tony/LVEF_View_CLS` |
| 162 | `/lustrefs/disk/project/lt200203-aimedi/puem/text_curr` |
| 134 | `/lustrefs/disk/project/lt200384-ff_bio/puem/ocr` |
| 134 | `/lustrefs/disk/project/lt200384-ff_bio/puem/ocr/ocr_dicom` |
| 108 | `/lustrefs/disk/project/lt200203-aimedi/puem/dms/hashing_cross-verification` |
| 104 | `/lustrefs/disk/project/lt200203-aimedi/nokdg` |
| 99 | `/lustrefs/disk/project/lt200203-aimedi/pung` |
| 99 | `/lustrefs/flash/scratch/lt200384-ff_bio/puem` |

Storage layout:

- `/lustrefs/disk/project/lt200203-aimedi/`: AI medical imaging project.
- `/lustrefs/disk/project/lt200384-ff_bio/`: bioinformatics / face recognition project.
- `/lustrefs/flash/scratch/`: fast temporary scratch space.
- `/lustrefs/disk/home/teiamarj/`: home directory.
