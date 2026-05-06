# Global Codex Instructions Imported From Claude

This file mirrors the useful human-authored guidance from `~/.claude/CLAUDE.md`,
`~/.claude/RTK.md`, `~/.claude/tauri.md`, and `~/.claude/MEMORY.md`.

## Claude Memory Routing

- When the user says `remote`, `ssh`, or names a known server, prefer the SSH aliases from the imported Claude memory.
- Known SSH hosts include `tl`, `sl`, `sorn`, `ipu`, `deploy`, `admin`, `home`, `pv`, `box1`, `box2`, and `meow`.
- For `tl`, use `ssh tl`; it is `transfer.lanta.nstda.or.th` as user `teiamarj`.
- For `tl` interactive commands, check tmux first with `ssh tl 'tmux ls 2>/dev/null'`. If no session exists, create `main`, then use `tmux send-keys`.
- Use plain `ssh tl '...'` only for read-only queries such as `cat`, `ls`, `squeue`, and `tmux ls`.
- Main `tl` working folder: `/lustrefs/disk/project/lt200203-aimedi/puem/tmp`.
- On `tl`, use `source ~/z.sh` and `z <keyword>` for interactive navigation; use full paths in non-interactive one-liners.

## LANTA Cluster

- SLURM account: `lt200203`.
- GPU hardware confirmed on LANTA: NVIDIA A100-SXM4-40GB, CUDA 12.7, driver 565.57.01.
- Use `gpu-devel` for quick tests and `gpu` for longer GPU jobs.
- Always include `#SBATCH -A lt200203` in submitted jobs.
- Prefer output logs under `/lustrefs/disk/project/lt200203-aimedi/puem/tmp/` for quick tests.
- Load modules before conda on LANTA: `module purge && module load Mamba FFmpeg cuda`.
- Useful aliases on LANTA: `q` for `squeue -u $USER`, `qo` for quota.

## RTK

- `rtk` is installed as Rust Token Killer for token-optimized command output.
- Use `rtk` meta commands directly when asked: `rtk gain`, `rtk gain --history`, `rtk discover`, and `rtk proxy <cmd>`.
- If `rtk gain` fails, suspect a binary name collision with a different `rtk`.

## Tauri v2 Notes

- For Tauri v2 projects, config lives in `src-tauri/tauri.conf.json`, Rust dependencies in `src-tauri/Cargo.toml`, and permissions in `src-tauri/capabilities/*.json`.
- Rust commands use `#[tauri::command]` and are registered via `tauri::generate_handler![...]`.
- JavaScript invokes Rust commands through `import { invoke } from '@tauri-apps/api/core'`.
- Tauri v2 uses capabilities and permissions instead of the v1 allowlist; dangerous commands are blocked by default.
- Common plugins: `@tauri-apps/plugin-fs`, `@tauri-apps/plugin-dialog`, `@tauri-apps/plugin-notification`, `@tauri-apps/plugin-updater`, `@tauri-apps/plugin-shell`, and `@tauri-apps/plugin-process`.

## Imported Memory Details

The full Claude memory import is stored at `codex-local/memories/claude-memory-import.md`.
Use it as stable user context for remote server, LANTA, tmux, and Tauri workflows.
