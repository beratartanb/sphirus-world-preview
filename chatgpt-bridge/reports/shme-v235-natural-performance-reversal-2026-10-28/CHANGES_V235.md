# SHME V2.35 — değişiklikler (V2.34 d71d03d üzerine)

## Üretim (PROMO235, VERIFY235 ALL_OK temiz açılış)
- **İçerik (yeni):** `/Game/GraceRanger/SHME/Animations/V235/SHM235_JogRev_{F_B,B_F}_P0..31`.
  - 64 klip, `gen235_rev.py`.
  - Eğriler `curves235.py`: SHM227 rev + SHM226 hız eğrileri.
  - DB'ler `PSD_SHM235_JogRevFwd` (F_B + REAR döngüleri) ve `PSD_SHM235_JogRevBwdX` (B_F + REAR + `A_CT_Jog_Fwd`).
  - `continuing_pose_cost_bias -0.5`.
  - Döngülere `SHME_V235_*` BranchIn izi eklendi (manifest `revdbs`).
- **ABP (`rev`):** 4 ters dönüş DB değişkeni → V235 DB'leri.
- **DSL `shm_src.py`, `SHM_UpdateRouting`:**
  - `revOver`: `RevOverHard` ve aile 2'de ters aday → izinli.
  - `gapKeep`: `RevGapKeep`, aile 3 ve `SHM234_GapT < RevGraceTime` → `rdLost` ve `rdNewIntent` boşlukta tetiklenmiyor.
- **DA (`shm_profiles.py`):** `RevOverHard` true, `RevGapKeep` true (varsayılan false; üretim DA'sında true).
- **BP_GR_Player (`mouse`):** `GR233_RecMouseScale` 0.35 → 0.7. Geri dönüş değeri 0.35.

## Reddedilen / üretime alınmayan
- `gen235_stop` r1–r6 (CP2 jog duruşunun yerinde yeniden planı). V2.34 klibi geri yüklendi; sha1 `1323d4cf…` verify235 ile denetlendi.
- `rvSW` / `rvOW` / `rvFP` (giriş warping / OrientationWarping / FootPlacement varyantları): etkisiz.

## Araçlar (`Tools/SHME_V235_20261028`)
| Araç | İş |
|---|---|
| `diag235.py` | İlk bozuk kare tablosu |
| `sheet235.ps1` | Zaman damgalı kare şeridi |
| `gen235_rev.py`, `curves235.py`, `build235_dbs.py`, `db235_bias.py` | Ters dönüş içeriği ve DB'ler |
| `gen235_stop.py` | Reddedilen duruş yeniden planı |
| `probe235_route.py`, `only235_route.py` | Yönlendirme sayımı / tek fonksiyon kurulumu |
| `promote235.py`, `verify235.py` | Üretime alma ve doğrulama |
| `tables235.py` | Kayma + bekleme tabloları |
| `worst235.py` | En kötü kayma |
| `media235.sh` | Kayıtlar |
| `manifest235.py`, `v235_ab.sh`, `ab_safe235.sh` | Güvenlik ve A/B |

Harness: `j35_rev`, `j35_rev2`, `j35_relstop` senaryoları (`v212_run_v235.diff`).

## Geri dönüş
- **Bayraklar:** DA `RevOverHard` / `RevGapKeep` false; ABP DB değişkenleri V2.26/V2.32 DB'lerine.
- **Fare:** 0.35.
- **İkili dosyalar:** manifest yedekleri `Saved/Codex/SHME_V235_20261028/checkpoint/manifests/PROMO235/`. Bu yedekler yayımlanmadı.
