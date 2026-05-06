---
name: tl server — z navigation tool
description: On the tl SSH server, use the `z` command (sourced from ~/z.sh) to jump to frecently used directories. Lists the top paths tracked.
type: project
---

On the `tl` server (transfer.lanta.nstda.or.th), directory navigation uses the **z** jump tool (`~/z.sh` by rupa deadwyler).

**Main working folder:** `/lustrefs/disk/project/lt200203-aimedi/puem/tmp`

To use z in a shell session on tl, it must be sourced:
```bash
source ~/z.sh
z <keyword>   # cd to most frecent directory matching keyword
z -l <keyword>  # list matches without cd-ing
```

**Why:** The tl server has deep nested paths under `/lustrefs/disk/project/` — z tracks frecency to avoid typing full paths.

**How to apply:** When navigating or suggesting paths on tl, use `z <keyword>` shorthand instead of full absolute paths. For non-interactive commands (SSH one-liners), still use full paths since z requires an interactive shell with z.sh sourced.

## Top frecently used paths (from ~/.z, higher score = more used)

| Score | Path |
|-------|------|
| 1319 | `/lustrefs/disk/home/teiamarj` (home) |
| 405 | `/lustrefs/disk/project/lt200203-aimedi/puem/dms` |
| 404 | `/lustrefs/disk/project/lt200203-aimedi/puem` |
| 405 | `/lustrefs/disk/project/lt200203-aimedi/puem/dms` |
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

## Storage layout on tl
- `/lustrefs/disk/project/lt200203-aimedi/` — AI medical imaging project (aimedi)
- `/lustrefs/disk/project/lt200384-ff_bio/` — bioinformatics / face recognition project
- `/lustrefs/flash/scratch/` — fast scratch space (temporary)
- `/lustrefs/disk/home/teiamarj/` — home directory
