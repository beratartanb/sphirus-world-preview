# SPHIRUS V2.27 — değişiklik listesi (durum: üretim / aday / araç)

Taban: V2.26 üretimi (bridge commit 9634d8d). Kontrol noktası `Saved/Codex/SHME_V227_20261024/checkpoint/pre_v227/` (ABP_GR_MotionMatching(.Base), BP_SHM_HumanMotionComponent, DA_SHM_Response_Default, 66 V226 klip+DB varlığı) + `checkpoint/tools/`. Tüm ABP değişiklikleri grafik düzeyinde yama (`qa_graph`), DSL yeniden derlemesi yok; bileşen ve DA değişmedi.

## ABP_GR_MotionMatchingBase (SHM_Snapshot + AnimGraph MM düğümü) — kurulu, KAPALI (üretime alınmadı; düğmeler 0, üretim DB’leri V2.24 pivot)
| Geçiş | Dosya | Ne yapar | Değişkenler |
|---|---|---|---|
| a | `install_v227_revhold.py` | `SHM226_Rev` eğrisi → `SHM227_Rev`; tutma koşulu (RevHold>0,5 & kalan>HoldExit & önceki kare ABP bölümü & HasIntent) `SHM_RedirectActive` ve kare sayacı koşuluna OR; `SHM_FootPlaceOff` = FPOff>0,5 & klip pozda & \|eğim\|<FlatMax & salınım kaldırmaları<2 cm | `SHM227_RevHold` 0, `SHM227_FPOff` 0, `SHM227_HoldExit` 0,25, `SHM227_FlatMax` 6, `SHM227_Rev`, `SHM227_Hold` |
| b | `install_v227b_restart.py` | bileşen `RedirectTime` azaldı = yeni bileşen bölümü → `cStart`'a OR (köprü karesi yeniden rotalar); FootPlaceOff değeri bölüme bağlı | `SHM227_Restart`, `SHM227_PrevRdT` |
| c | `install_v227c_reentry.py` | bileşen bölümü bitmişken kalan süre >0,05 s yükseldi = MM klip başına yeniden girdi → `SHM227_Dead` (yeni bileşen bölümüne kadar) → tutma iptal | `SHM227_Dead`, `SHM227_PrevRev` |
| d | `install_v227d_throttle.py` | klip pozdayken MM düğümü `SearchThrottleTime` = FMax(eski, Select(Thr, ThrottleT, 0)) | `SHM227_Thr`, `SHM227_ThrottleT` 2,5 |
| e | `install_v227e_intent.py` | Thr koşulu bileşen `RedirectActive`'i de sayar (giriş+1. kareden itibaren); bileşen `RedirectEnd` 3 (yeni niyet) / 4 (kayıp) → `SHM227_IntentEnd` → Dead | `SHM227_IntentEnd` |

Üretim davranışı düğmeler 0 iken değişmez (kurulu, kapalı). Üretime alma anahtarı `promote227.py` (= promote226 Reversal226 + RevHold/FPOff 1), geri alma `req/rollback227.py`, doğrulama kapısı `req/verify_fin227.py` (düğmeler + 64 eğri + V2.26 üretim doğrulaması → `ALL_OK`).

## İçerik (aday varlıklar, V2.26'dan)
| Değişiklik | Dosya | Durum |
|---|---|---|
| 64 `SHM226_JogRev_*` klibine `SHM226_Rev` eğrisi (kalan klip saniyesi, [0,T]→[T,0]) | `add_revcurve227.py` | kaydedildi (klipler aday varlık; PSD_SHM226 DB’leri üretimde değil) |

## Test aracı
| Değişiklik | Dosya | Not |
|---|---|---|
| Telemetri: `SHM227_Rev/Hold/Restart/Dead/Thr/IntentEnd` avars, `SHM226_Rev` acurves | `Tools/SHME_V212_20261017/v212_run.sh` (`code/v212_run_v227.diff`) | |
| A/B sürücüsü `v227_ab.sh` (etiket `v227<tag>_…`), `ab_safe227.sh`, `vars227.sh` (rv32, rh, rhH, rhF, rhX4, rhX1) | `Tools/SHME_V227_20261024/` | |
| Zincirler: `lib227.sh`, `run227_sweep.sh`, `run227_t4.sh`, `run227_t5.sh`, `run227_fin.sh <PROMO>` | `Saved/Codex/SHME_V227_20261024/` | |
| Ölçüm: `exitjump227.py` (klip ömrü, çıkış sıçraması, SWITCH listesi), `plant227.py` (temas-başlangıçlı basılı kayma), `trace227.py` (kare izi), tablolar `req/tables227*.sh` | `Tools/SHME_V227_20261024/`, `req/` | |
| Sondalar (salt okunur): `probe_snapshot227.py`, `probe_fp227.py`, `probe_fp227b.py` | | `data/probe227.json`, `data/probe_fp227.json` |
| Medya `media227.sh`, yayın `pub227.sh` / `publish227.sh` | | |
