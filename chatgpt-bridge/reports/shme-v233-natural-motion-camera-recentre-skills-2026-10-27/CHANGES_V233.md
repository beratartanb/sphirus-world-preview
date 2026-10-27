# CHANGES V2.33 (2026-10-27, taban V2.32 / Bridge d3f3105)

## Üretimde (VERIFY233 ALL_OK, temiz açılış)

### standback
**Yeni içerik**
- `/Game/GraceRanger/SHME/Animations/V233/SHM233_StandBack2_Jog_Bwd`
- `PSD_SHM233_StandBackStart2` (+ `A_RB_Jog_Rear`, BranchIn izi `SHME_V233_StandBack2`)

**ABP `ABP_GR_MotionMatchingBase`**
- `SHM_Snapshot` → `SHM233_StandBack` + `SHM233_SBT` zamanlayıcısı.
- Family-4 dalı + `Update_MotionMatching` giriş zorlaması.
- Knob'lar: `SHM233_StandBackOn` = 2, `SHM233_DB_StandBack`.

### camrec
**Bileşen `BP_SHM_HumanMotionComponent`**
- `SHM_UpdateCameraV21` içinde:
  - kritik sönümlü arkaya dönüş (`CamRec*`);
  - girdi kilidi durum makinesi (`MoveLatch*`);
  - bakış algılama kendi dönüşünü (`CamRecDelta`) çıkarıyor.
- Yeni değişkenler: `CamRecScale`, `TelemetryLine`.

**DA `DA_SHM_Response_Default`:** `CamRecEnabled` true, `CamRecMaxErr` 110, `CamRecMinSpeed` 170 (yürüyüş hariç).

**Profil alanları:** `CamRecFreq` 2.2, `CamRecMaxRate` 110, `CamRecDead` 6, `CamRecStable` 0.25, `CamRecTravelRate` 30, `CamRecLookHold` 1.6.

**`/Game/GraceRanger/BP_GR_Player`**
- `GR_UpdateSHMSignals`: kilit setter'ları + kontrol yaw'u += `CamRecDelta`.
- `CamRecScale` = gamepad ? `GR233_RecPadScale` (1.0) : `GR233_RecMouseScale` (0.35).

**Integrated `BP_ExampleCharacter_MotionMatching`**
- IA_Move `GetRight/ForwardVector` yaw girdisi = `Select(GR233_MoveLatchOn, GR233_MoveLatchYaw, kontrol yaw)`.

### Diğer
- **Telemetri:** `SHM_Telemetry` artık PrintString yerine `TelemetryLine` yazıyor. `qa_pie` bunu yan dosyaya alıyor (`Saved/Codex/SHME_V1_20260925/SHM/`).
- **SHM232_IS_* (9 klip):** `AnimNotifyState_PoseSearchExcludeFromDatabase` (iz `SHME_V233_Excluded`) ile aramadan çıkarıldı.

## Aday (üretimde değil)
- **sprintcalm:** `V233/SprintCalm/SHM233_Calm_*` + `PSD_SHM233_SprintCalm`.
  - Açma: ABP `SHM211_DB_Sprint` → bu DB (`promote233` grubu `sprintcalm`).

## Araçlar
**Gated runner (`runner.py`)**
- G1 eski kuyruk.
- G2 PIE.
- G3 sahip.
- G4 manifest + `unreal` vekili.
- G5 disk / kirli denetimi.
- Kayıt: `gate233.log`.

**Yeni betikler**
- `manifest233.py`, `lock233.sh`, `jobhdr.sh`, `gatetest/`.
- `qa_pie`: yan dosya, `ERROR_FLOOD`, iki geçişli `pawn_flags`.
- `build_funcs`: DSL hatasında `BUILD_FUNCS_FAILED`, LastHitBy yaması.
- `revert_v21_quit`: `ALLOWED` += oyuncu BP'leri.
- `v212_run.sh`: `cam33_*` ve `jturnj` senaryoları.

**Ölçüm ve kayıt:** `rec233.py`, `tables233.py`, `camcmp233.py`, `verify233.py`, `promote233.py` (rollback değerleriyle), `media233.sh`, `sheet233.ps1`.

## Skill'ler
- Yeni: `sphirus-natural-motion`, `sphirus-camera-direction`, `sphirus-safe-unreal-iteration`.
- `CLAUDE.md`: kural + yönlendirme satırları.
- `sync_claude_skills.py` çalıştırıldı (77 / 0 hata).

## Geri dönüş
- `promote233.py` ile `{'rollback': True}`: knob'lar ve DA değerleri V2.32 değerlerine döner.
- Grafik değişiklikleri için `checkpoint/manifests/<ad>/` yedekleri editör kapalıyken geri kopyalanır. Örnekler: `standback_abp`, `camA2`, `camB`, `telemetry_comp*`.
