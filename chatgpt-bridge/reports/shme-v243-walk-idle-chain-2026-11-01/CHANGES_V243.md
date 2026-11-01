# CHANGES V2.43 (2026-11-01)

## Üretime alınanlar (promote243.py, manifest `v243_prom_lat`, aday `latgl`)
| Asset | Alan | V2.42 üretim | V2.43 üretim | Etki |
|---|---|---|---|---|
| `ABP_GR_MotionMatchingBase` (+ child) | `SHM242_DB_LatStop` | `PSD_LS_CoreLateralStop` (satıcı) | `PSD_SHM242_LatStop` (32 proje klibi, kapanış adımı 8 cm) | yanal fren/duruş = temas-planlı proje ailesi |
| `BP_GR_Player` (+ `BP_PBI_Player`) | `GR242_TurnSettleGate` | false | **true** | duruş yerleşirken (`SHM_StopSettle` 0,5–2) ayakta dönüş montajı başlamaz |
| `BP_GR_Player` (+ `BP_PBI_Player`) | `GR243_TurnNeedsLook` | false | **true** | keşfedilmiş loco çerçevesi tek başına ayakta dönüş emretmez; bakış ≥ 42° ayrışmalı |

Üretimde **değişmeyen** (aday olarak kapalı): `StanceIdleGateEnabled` true, `SHM242_IdleOn` 0, `SHM242_IdleDB` None (idle zinciri — nedeni REPORT §1/§4).

## Pawn (`BP_GR_Player` + `BP_PBI_Player`), manifest `v243_pawn1`
| Değişken | Varsayılan | Etki | Kurulum |
|---|---|---|---|
| `GR243_TurnNeedsLook` (bool) | False | `GR_UpdateIdleTurn`: dönüşü başlatan AND'in A pini = (V2.42 yerleşme kapısı) ∧ NOT(kural ∧ \|Δ(kontrol yaw, aktör yaw)\| < 42°) — keşfedilmiş loco çerçevesi tek başına ayakta dönüş başlatamaz; dönüş için oyuncunun bakışı da bedenden ≥ 42° ayrışmalı | `install243_turnlook.py` |

## ABP — değişiklik yok (V2.42 kancaları kullanıldı: `SHM242_IdleOn/IdleDB`, `SHM242_DB_LatStop`)

## SHME yanıt profili (DA, aday bayrağı olarak)
| Alan | Üretim | Aday | Etki |
|---|---|---|---|
| `StanceIdleGateEnabled` | true | false (`idlg`, `og`) | `SHM_IdleHold` (= kapı ∧ SpeedPeak > 30 literal) hiç latch'lenmez → idle alt bedeni MM'den gelir (V1.2 anlık görüntü tutuşu kapalı). `IdleStanceTolerance` ABP tarafından OKUNMUYOR (architecture.md güncel değil). |

## İçerik
| Asset | Ne | Yöntem |
|---|---|---|
| `SHM242_Idle_Weighted` (yeniden yazıldı) | nefes spine_03/04/05 ×1,2°, 11,2 s açık uçlu | `gen242_idle.py` (breath_deg 1.2) |
| `SHM243_Idle_Weighted2` (yeni, aday) | aynı klip, ağırlık kayması 2,5 s'de başlıyor (388 kare) | `gen242_idle.py` (onset 2.5) |
| `PSD_SHM242_IdleB` (yeni, aday DB) | tek giriş: `SHM243_Idle_Weighted2` (tam pencere BranchIn) | `build242_idledb.py` (name) — ilk kurulum `PSD_SHM243_Idle` adı kanca testine uymadı (ad `SHM242_Idle` içermeli), silinemedi (BranchIn referansı), üretimde referanssız |
| `SHM242_LatStop_*` (yeniden yazıldı, post zinciri) | kapanış adımı tepe 8 cm, apex_min 6 (FootPlacement 4 cm'lik kapanış adımını basılı sayıp bırakınca 32 cm sıçrıyordu) | `gen242_latstop.py` (close_apex 8, apex_min 6) |

## Harness
- Senaryo `w43_idle` (yürü 3 s → 8 s bekle → yürü 3 s → bekle); adaylar `idp`/`idph` (bellek içi sekans değişimi, PRE/POST `pre243_idle.py`/`post243_idle.py`), `idlg`/`og` (kapı kapalı), `latgl`/`tl` (dönüş kuralı); `lib243.sh`, `vars243.sh`, `vars243_cap.sh`, `v243_ab.sh`.
- Yürüyüş izolasyonu: `oSCR` (omurga karşı dönüşü 0), `oPBI` (profil kapalı), `oRAW` (FootPlacement/LegIK/StrideWarping/OrientationWarping kapalı) — yürüyüş metrikleri değişmedi → karşı dönüş 23°, kol salınımı, pelvis hareketi **klip içeriği** (`A_LB_Walk_Fwd`), runtime katmanı değil.
