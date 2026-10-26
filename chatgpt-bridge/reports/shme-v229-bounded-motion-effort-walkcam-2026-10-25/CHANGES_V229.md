# SPHIRUS V2.29 — değişiklik listesi (durum: üretim / aday / araç)

Taban: V2.28 üretimi (bridge `510d32a`). Kontrol noktaları `Saved/Codex/SHME_V229_20261025/checkpoint/pre_v229/` (ABP'ler, BP_GR_Player, BP_PBI_Player, BP_GR_MotionProfile, bileşen, BP_SHM_ResponseProfile, üç DA, DSL kaynakları), `checkpoint/revturn/` (4 RevTurn klibi, düzeltme öncesi), `checkpoint/post_promo229/` (ilk terfiden sonra ABP'ler + DA'lar). Terfiler: 17:52 {camera, effort, resume}, 20:44 {pushcancel}, 22:56 {EffortScaleMin 0,7}; her birinden sonra temiz yeniden açılış `VERIFY229` ALL_OK. Geri alma `promote229.py {'rollback': True}` (+ RevTurn için dosya kontrol noktası, editör kapalı).

## DEPAR TERS DÖNÜŞÜ
| Değişiklik | Dosya | Kapsam | Durum |
|---|---|---|---|
| RevTurn yeniden pişirme: korunan burulma terimi yaw farkını ölçeklemeden ÖNCE ±180'e sarıyor (V2.22 hatası: 180° spine_01 dönüşü) | `rb229_revturn.py` (`req/rb229_write_fixed.py`) | `SHM216_RevTurn_L_Lfoot/L_Rfoot/R_Lfoot/R_Rfoot` (içerik; bacak/kök/pelvis okuması 0,0 cm) | **üretim** (hata düzeltmesi) |
| İtiş fazı iptali: `SHM228_Cancel := OR(eski, PushCancel & klip pozda & DesV·EntrySign < −1 & niyet fren yönünde & AgainstT > 0)` → karşı aile DB'si + kesen arama (V2.28 yolu) | `install_v229_pushcancel.py` | ABP `SHM_Snapshot` | **üretim** `SHM229_PushCancel` 1 |

## EFOR
| Değişiklik | Dosya | Kapsam | Durum |
|---|---|---|---|
| Efor durumu: `EffortE`, `EffortLoad`, `EffortLoadDir`, `EffortEUse` (1,2 s alçak geçiren), `EffortReqLoad` (istek karesinde mandal, 0,6 s), `EffortPrevDir`, ölçekler `EffortAccScale` / `EffortTurnScale` (taban `EffortScaleMin`) | `shm_src.py` SHM_UpdateState, `shm_component_vars.py`, `shm_profiles.py` | bileşen + profil (DSL, funcs yeniden derleme) | **üretim** `EffortEnabled` true, Gain 1,6, TurnK 0,5, AccK 0,5, LoadK 0,6, TauRec 5, ScaleMin 0,7 |
| Tüketici: `CalculateMaxAcceleration × EffortAccScale`, PhysicalRedirect sürtünmesi (`SelectFloat` B) × `EffortTurnScale` (0 → 1 koruması) | `install_v229_effort.py` | BP_GR_Player | **üretim** |
| Aday (terfi edilmedi): `RedirectEpisodeMinSpeed` 70 / 40 (`ems`, `ems40`), efor tabanı 0,8 (`sm80`), güçlü efor (ef3) | `vars229f.sh`, `vars229.sh` | bayrak | kapalı |

## GEÇİŞ
| Değişiklik | Dosya | Durum |
|---|---|---|
| Bırak–yeniden bas: `SHM229_PostT` (fren bittikten sonra geçen süre); RelHold kapısı `OR(Brake, PostT < ResumeWin)` | `install_v229_resume.py` (ABP) | **üretim** `SHM229_ResumeWin` 0,2 |

## YÜRÜYÜŞ KAMERASI
| Değişiklik | Dosya | Durum |
|---|---|---|
| Omuz değişimi yalnız `CamSwapMinSpeed` üstünde; yumuşak bölge hızla yürüyüş (`CamFolDZLatWalk/FwdWalk`) → koşu değerleri arasında (`CamWalkSpeedLo/Hi` 150/260) | `shm_src.py` SHM_UpdateCameraV21, `shm_profiles.py` | **üretim** 230 / 3 / 4 (jog/sprint değişmedi) |

## Test aracı
| Değişiklik | Dosya |
|---|---|
| Depar ters dönüş denetimi (mesh–kapsül, kamera–baş, görünürlük, burulma/SPIN) `rev229.py`, `twist229.py`, ekran izdüşümü `screen229.py`, kadraj `cam229.py`, çeviklik olayları `agil229.py`, kontrol kilidi `lock229.py`, yön `dir229.py`, karşılaştırma `cmp229.py` | `Tools/SHME_V229_20261025/` |
| qa_pie: segment analog büyüklüğü (seg[2]), görünür beden çizim bayrakları (vvis/vhid/vons/vrr) | `Tools/SHME_V1_20260925/qa_pie.py` |
| Senaryolar: s29_* (ws, ws_ph, cam, cam2, sa, dg, dbl, rel, swl08–20, wall, wstop), j29_swl10/14/20, j29_hitch, e29_* (chain, rest, load, recov, house, hitch), c29_* (look, ad, wlook, diag, jlook, combo), a29_* (ang, angb, edge, mag, kdg, csweep); cvars `Effort*` | `Tools/SHME_V212_20261017/v212_run.sh` |
| Zincirler `run229_t1..t7`, `run229_build*`, `run229_fin.sh`, `run229_pc.sh`, `run229_ems.sh`, `run229_sm.sh`, `run229_fin2.sh`, `run229_fin3(b).sh`; `lib229.sh` (RUNNER_NOT_READY'de editör + zenserver öldürüp yeniden deneme) | `Saved/Codex/SHME_V229_20261025/` |
| Skill güncellemeleri: SHME architecture (V2.29), motion-diagnosis (rota-özel poz çevrilmesi, tutulan ters tuş kilit denetimi), character-camera camera-feel (yürüyüş kadrajı), editor-automation runner-and-pitfalls (ZenServer, bash ayraç tuzağı) | `.agents/skills/…` (senkron) |
