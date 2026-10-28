# SHME V2.36: değişiklikler (V2.35 742af76 üzerine)

## Üretim (temiz açılışta VERIFY236 ALL_OK)

Değişiklikler yalnız ABP veritabanı değişkenleri ve yeni varlıklardır. Üretimdeki klip ve veritabanlarının içeriği değişmedi; yalnız birkaç üretim döngüsüne ve CP2 başlangıç klibine aday DB'lere giriş notify izi eklendi (manifestli, altta).

| Grup | ABP değişkeni | Yeni değer | Geri dönüş |
|---|---|---|---|
| `stop` | `SHM236_DB_JogStop` (yeni değişken) | `V236/PSD_SHM236_JogStop2` | `PSD_CP2_JogStop` |
| `start` | `SHM_JogStartDB_L` / `_R` | `V236/PSD_SHM236_JogStartS_L` / `_R` | `PSD_SHM_JogStartS_L` / `_R` |
| `rev` | `SHM224_DB_JRFwd` / `JRFwdM` / `JRBwd` / `JRBwdM` | `V236/PSD_SHM236_JogRevFwd` / `JogRevBwdX` | V2.35 DB'leri |
| `load` | `SHM230_DB_JRFwdL` | `V236/PSD_SHM236L_LoadRevFwd` | `V231/PSD_SHM231L_LoadRevFwd` |

### ABP grafik kancaları (`Update_MotionMatching`)
- `K2Node_CallFunction_42` ve `K2Node_Select_3` (option 0): literal `PSD_CP2_JogStop` yerine `SHM236_DB_JogStop` değişkenini okuyor.
- `K2Node_CallFunction_40`: literal `PSD_CP2_JogStart` yerine `SHM236_DB_JogResume` değişkenini okuyor.
  - Varsayılan değer üretimdeki DB; `resume` grubu reddedildi.

### Yeni içerik (`/Game/GraceRanger/SHME/Animations/V236/`)

| Varlık | Kaynak | Açıklama |
|---|---|---|
| `SHM236_JogStop_B{l\|r}_P00..P23` | `gen236_stop.py` | 24 bırakma evresi klibi. B = fren ayağı; tam beden fren; sonu vendor duruşunun son karesi. Ayrıca `SHM_StopSettle`, `footspeed_l/_r`, `pbi_authoredforwardlean` eğrileri. |
| `PSD_SHM236_JogStop2` | | Bu 24 klibin DB'si; continuing bias −3 |
| `SHM236_JogStart_F_Lfoot` / `_Rfoot` | `gen236_start.py` | Düz tempolu kalkış, önce sol / sağ ayak salınır |
| `PSD_SHM236_JogStartS_L` / `_R` | | Üretim başlangıç DB'lerinin kopyası + yeni kalkış |
| `SHM236_JogRev_{F_B,B_F}_P0..31` | `gen236_rev.py` | V2.35 ayak planı aynı; frende kol genliği %25, kollarda atalet salınımı, dirsek açılması, boyun dengeleme. Ayrıca `SHM226_Rev/V/W` eğrileri. |
| `PSD_SHM236_JogRevFwd` / `JogRevBwdX` | | Bias −0.5 |
| `SHM236L_LoadRev_F_B_P0..15` | `gen236_load.py` | Eforlu ters dönüş, bekleme kaldırıldı |
| `PSD_SHM236L_LoadRevFwd` | | P15 yerine dinlenik P30/P31 |
| Aday, kullanılmıyor | | `PSD_SHM236_JogStop` (2 temsilî klip, aşama 1), `PSD_SHM236_JogResume` (reddedildi) |

## Reddedilen / üretime alınmayan
- **`resume`:** durma sırasında yeniden basışta tempolu döngü de aranabilsin diye yapıldı. Kayma 19 cm'de kaldı, değişmedi.
- **Daha kısa adım varyantı** (step_max 30): çökme azalmadı. Çözüm pelvis yükselme planı oldu.
- **İki klipli duruş:** arama bir karede diğer klibin 0. karesine atlıyordu, kayma 46 cm. Sonuç: 24 evre.
- **Duruşun idle karesinde bitmesi:** sol-ayak başlangıç DB'sine düşüyor, TurnL045 ile 85 cm sürtünme.

## Araçlar (`Tools/SHME_V236_20261028`)

| Araç | İş |
|---|---|
| `gen236_stop.py` | Duruş ailesi üreteci |
| `gen236_start.py` | Düz kalkış üreteci |
| `gen236_rev.py` | Tam beden ters dönüş üreteci |
| `gen236_load.py` | Eforlu ters dönüş üreteci |
| `curves236.py` | Ters dönüş eğrileri |
| `build236_stopdb.py`, `build236_startdbs.py`, `build236_revdbs.py`, `build236_resumedb.py`, `db236_bias.py` | DB'ler ve bias |
| `install236_stopvar.py`, `install236_resumevar.py` | ABP kancaları |
| `promote236.py`, `verify236.py` | Üretime alma ve doğrulama |
| `stop236.py` | Görünür bedende duruş denetimi |
| `tables236.py` | Son tablolar |
| `stick236.ps1` | Kaynak klip çubuk-figür şeridi (oyun olmadan) |
| `probe236_stop.py` | Duruş yolu probu |
| `media236.sh`, `manifest236.py`, `v236_ab.sh`, `ab_safe236.sh` | Kayıt, manifest, A/B |

## Test altyapısı
- **Harness senaryoları** (`v212_run_v236.diff`): `j36_stop`, `j36_stopb`, `j36_stopr`, `j36_rse`, `j36_rsm`, `j36_rsl`, `j36_rsx`, `j36_wjs`, `j36_wjsb`, `j36_sside`.
- **`qa_pie.py`:** `SHM236_DB_JogStop` durum kaydına eklendi.

## Geri dönüş
- `promote236.py` ile `{'rollback': True}` çalıştırılır; değerler `PROMO236` çıktısında yazılı.
- İkili dosya yedekleri: `Saved/Codex/SHME_V236_20261028/checkpoint/manifests/<ad>/`.
  - Bu yedekler yayımlanmadı.
  - Döngü kliplerine eklenen giriş notify izleri `revdb1` / `rev2` / `resume1` manifestlerinde.
