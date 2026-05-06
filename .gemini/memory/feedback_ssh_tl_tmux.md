---
name: SSH tl — run commands via tmux send-keys
description: When running commands on the tl server, always check tmux session is active before send-keys, create one if missing.
type: feedback
---

When executing commands on `tl` (transfer.lanta.nstda.or.th), do NOT use bare `ssh tl 'command'` one-liners for interactive work. Use tmux send-keys instead.

**Why:** User wants to see commands run inside their tmux session rather than Gemini executing them silently. Output is visible in real-time and session persists across disconnects.

## Required pattern — always check before send-keys

```bash
# Step 1: check if session exists
ssh tl 'tmux ls 2>/dev/null'

# Step 2a: if session exists → send-keys
ssh tl 'tmux send-keys -t <session> "command" Enter'

# Step 2b: if NO session → create one first, then send-keys
ssh tl 'tmux new-session -d -s main'
ssh tl 'tmux send-keys -t main "command" Enter'
```

**NEVER call send-keys without checking first** — if no tmux server is running, it will fail with `no server running`.

## How to apply
- Default session to target: `0` (if attached), fallback: `main`
- Still use plain `ssh tl '...'` for read-only queries (`cat`, `ls`, `squeue`, `tmux ls`) where output goes back to Gemini
- Only use send-keys for commands the user wants to see/interact with in their terminal
