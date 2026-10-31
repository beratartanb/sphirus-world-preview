# T1 evidence: capture repeatability within one editor session (2026-10-31 02:54–02:56 local)

## Setup
- **Editor:** the running UE 5.8.1 editor (V2.40 session, launched 2026-10-31 00:20 with `-UseFixedTimeStep -FPS=30`). It was **not restarted**.
- **Map:** `/Game/GraceRanger/Maps/L_GR_SphirusHouse`.
- **Viewport:** 1741×922.
- **Runner:** gated runner. Jobs: `t1_cap.py` (kind `measure`), `t3_cv.py` (`measure`), `refresh_probe.py` (`control`). Lock owner `aitool`, released afterwards.
- **Capture:** `AutomationLibrary.take_high_res_screenshot(1920,1080,file,delay=0.2,force_game_view=True)`, then a viewport redraw through `EditorAppToolset.CaptureViewport`. This is the same pattern as the ChatGPT Bridge exporter.
- **Settings recorded in `data/t1_log.json`:**
  - cvars (sg.* = 3, `r.AntiAliasingMethod` 4, Lumen GI and reflections, VSM, HW RT);
  - scene sun, sky, fog and post-process volumes (histogram auto exposure, bias −0.65, EV100 −2…16);
  - viewport pose before and after;
  - dirty packages before and after (2 pre-existing ABP packages, unchanged);
  - actor transform hash (unchanged).

## Files

**`shots/`** — 24 engine renders, PNG 1920×1080 RGBA (alpha 255).
- Names follow `<view>__<tag>`.
- `A_tXX` = seconds after the camera move (planned).
- **Caveat:** for `house_front`, A_t00.5 / t02.5 / t06.0 were actually requested at 4.64 / 8.24 / 9.06 s, because the first call of the session took 3.6 s. Actual times are in `TABLES_T1.md` and `data/t1_log.json`.
- `B_round2` / `B_round3` = the camera was moved away and back, then waited 10 s.

**`captureviewport/`** — 3 PNGs (1741×922) returned by `EditorAppToolset.CaptureViewport`.
- The MCP tool function was called in-process via `ToolsetRegistry.ExecuteTool`; the MCP server was not running.
- Metadata layout is in `data/t3_log.json`.

**`heatmaps/`** — for the static (t10 vs t14) and revisit (round 2 vs round 3) pairs:
- `absdiff_x8` = |Δ luma| × 8;
- `one_minus_ssim_x2` = (1 − SSIM map) × 2.

**`sheets/`** — review sheets:
- `t1_overview.png` — 3 views × (first shot, t14, round 3, revisit heat map);
- house static pair;
- forest revisit pair;
- HighResShot vs CaptureViewport.

**`data/`**
- `metrics_t1.json` — full resolution: SSIM, Unreal 8×8 SSIM, PSNR, MAE, p99, and the Unreal Low-tolerance comparison re-implemented with and without the AA exemption.
- `metrics_lowres.json` — downsampled metrics, tile metrics, and synthetic-change sensitivity.
- `luma_per_shot.json`
- `refresh_probe.json`
- `t1_log.json`, `t3_log.json`

**`TABLES_T1.md`** — tables generated from the JSON files.

## Tools
In `../tools/`:
- `t1_cap.py`, `t3_cv.py`, `refresh_probe.py`
- `metrics_t1.py`, `metrics_lowres.py`, `gen_tables.py`
- `imgconv.ps1` — PNG↔raw via System.Drawing.
- `pngcheck.py` — independent PNG decoder; showed max difference 0 against the raw conversion.
- `mini.ps1` — sheets.

Metrics ran with Blender 5.2's bundled Python (numpy 2.3.4). Nothing was installed.

## Not done
- FLIP: needs approval to install.
- Cross-session repeat: needs approval to restart.
- Deterministic capture: median, MRQ, or a test sublevel.
- Player-camera stations.
