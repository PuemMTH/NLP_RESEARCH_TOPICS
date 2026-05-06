---
name: LANTA HPC cluster — job submission & hardware
description: SLURM job submission details for LANTA HPC; GPU specs, partitions, account, working paths, aliases, and tools for puem (teiamarj).
type: project
---

## Account & identity
- SSH via: `tl` (transfer.lanta.nstda.or.th, user: teiamarj)
- SLURM account: `lt200203`
- Main working folder: `/lustrefs/disk/project/lt200203-aimedi/puem/tmp`

## GPU Hardware (confirmed by test job 5674528)
- **GPU: NVIDIA A100-SXM4-40GB**
- VRAM: 40 GB
- CUDA Version: 12.7
- Driver: 565.57.01
- Tested node: `lanta-g-175` (x1001c7s7b0n0)

**Why important:** A100-SXM4 is a high-end HPC GPU — relevant when sizing batch sizes, mixed precision, and memory-heavy models.

## SLURM Partitions
| Partition | Time limit | Notes |
|-----------|-----------|-------|
| `gpu` | 5 days | main GPU partition |
| `gpu-devel` | 2 hours | for testing, usually has idle nodes (lanta-g-175/176) |
| `gpu-limited` | 1 day | limited access |
| `compute` | 5 days | CPU only |
| `compute-devel` | 2 hours | CPU testing |
| `compute-long` | 10 days | long CPU jobs |

## Aliases (in ~/.bashrc)
```bash
q        # squeue -u $USER — show my jobs
qo       # myquota — show storage quota
```

## Useful commands
```bash
sinfo                        # cluster node status
sbatch <script.sh>           # submit job
scancel <jobid>              # cancel job
tmux ls                      # list tmux sessions (default session: 0)
```

## Tools & paths
- `uv` (Python env manager): `/home/teiamarj/.local/bin/uv`
- `mise` (runtime manager): `/home/teiamarj/.local/bin/mise`
- `z` jump tool: sourced from `~/z.sh` (in bashrc)

## Conda environments available to puem
| Path | Notes |
|------|-------|
| `/lustrefs/disk/project/lt200203-aimedi/puem/envs/env_test` | general test env |
| `/lustrefs/disk/project/lt200203-aimedi/puem/envs/env_yolo` | YOLO env |
| `/lustrefs/disk/modules/easybuild/software/Mamba/23.11.0-0/envs/pytorch-2.2.2` | system PyTorch |
| `/lustrefs/disk/modules/easybuild/software/Mamba/23.11.0-0/envs/lightning-2.2.5` | system Lightning |

## SBATCH template (gpu-devel)
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

## SBATCH template (gpu — production)
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

## SBATCH template (jupyter on gpu-devel)
Script at: `/lustrefs/disk/project/lt200203-aimedi/puem/tmp/run-jupyter.sh`
```bash
#!/bin/bash
#SBATCH -p gpu-devel
#SBATCH -N 1 -c 4
#SBATCH --gpus=1
#SBATCH --ntasks-per-node=1
#SBATCH -t 2:00:00
#SBATCH -A lt200203
#SBATCH -J puem-jupyter
#SBATCH --output=/lustrefs/disk/project/lt200203-aimedi/puem/tmp/jupyter-%j.out
# ... loads Mamba, cuda, activates env, runs jupyter notebook with port tunnel instructions
```
After submit, check log for SSH tunnel command: `ssh -L <port>:<node>:<port> teiamarj@transfer.lanta.nstda.or.th -i id_rsa`

## How to apply
- Always use account `-A lt200203` when submitting jobs
- Use `gpu-devel` for quick tests (2h limit, usually has idle nodes)
- Output logs to `/lustrefs/disk/project/lt200203-aimedi/puem/tmp/`
- Reference scripts: `/lustrefs/disk/project/lt200203-aimedi/pung/run-gpu.sh`
- Load modules before using conda: `module purge && module load Mamba FFmpeg cuda`
