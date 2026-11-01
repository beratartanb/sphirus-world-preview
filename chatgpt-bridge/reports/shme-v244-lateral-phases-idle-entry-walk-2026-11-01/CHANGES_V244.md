# CHANGES V2.44 (2026-11-01)

## Üretime alınan (bkz. REPORT §5; `promote244.py`, manifest `v244_prom`)
| Asset | Alan | V2.43 | V2.44 | Etki |
|---|---|---|---|---|
| `ABP_GR_MotionMatchingBase` (+child) | `SHM242_DB_LatStop` | `PSD_SHM242_LatStop` | `PSD_SHM244_LatStop` | yanal fren/duruş ailesi: ulaşılabilir ilk iniş + plant yön sürekliliği (42 klip) |

Değişmeyen: `StanceIdleGateEnabled` true, `SHM242_IdleOn` 0 / `SHM242_IdleDB` None (idle zinciri aday), yürüyüş döngüsü (satıcı `A_LB_Walk_Fwd` dokunulmadı; aday yalnız bellek içi değerlendirildi).

## İçerik (yeni, proje klasörü `/Game/GraceRanger/SHME/Animations/V244`)
| Asset | Ne | Araç |
|---|---|---|
| `SHM244_LatStop_{L,R}_B{l,r}_P00..23` (48 üretildi, 42 DB'de) | V2.42 ailesi + (a) havadaki fren ayağı ≤ doğal iniş + 60 cm/s·t_land, (b) final olmayan plant yön sürekliliği (slerp %45) | `gen244_latstop.py` (G244L: L2 ayarları + extra_v 60, qpart 0.45) |
| `PSD_SHM244_LatStop` | BranchIn DB (iz `SHME_V244_LatStop`), şema/bias `PSD_LS_CoreLateralStop` | `build244_latdb.py` |
| `SHM244_Idle_Weighted` (367 kare, 12,2 s, döngü kapalı) | ağırlıklı/nefesli idle; TABAN POZ = `SHM_A_CP2_Jog_Fwd_Stop` son karesi (duruş ailelerinin bitiş duruşu) → duruştan poz-tam devralma; onset 1,0 s | `gen244_idle.py` (base_src/base_last) |
| `PSD_SHM242_IdleC` | tek giriş; ad kanca testine uygun (`SHM242_Idle`) | `build244_idledb.py` |
| (bellek içi) `A_LB_Walk_Fwd` adayı | pelvis yaw genliği ×0,65, göğüs yaw genliği ×0,55, baş dünya yaw'ı korunur, bacaklar orijinal temaslara yeniden çözülür; KAYDEDİLMEDİ | `gen244_walk.py` + `pre244_walk.py`/`post244_walk.py` |

## Harness
`lib244.sh`, `vars244.sh`/`vars244_cap.sh` (lat4, idl4, all4, walk4 + S/D/G), zincirler `run244_gen/c1/c2/fps/walk2/promote.sh`, `strips244.sh` (0,1 s yoğun şeritler), `idlemet243.py`.
Satıcı asset değiştirilmedi; tüm yazımlar manifest/yedek ile (`v244_lat`, `v244_idle`, `v244_walkbk` (yalnız yedek), `v244_prom`).
