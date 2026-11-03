# V2.54 değişiklikleri

Tüm yazımlar kapılı runner üzerinden, manifest ve doğrulanmış yedekle yapıldı (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/v254_*.json`).

## Yeni içerik (`/Game/GraceRanger/SHME/Animations/V254`)

- `SHM254_Rev_R_T25`, `SHM254_Rev_L_T45`, `SHM254_Rev_R_T186`, `SHM254_Rev_L_T216` (sprint 180 ters dönüşleri) ve `PSD_SHM254_SprintRev` (bias −25).
- `SHM254_Cut_R_T186`, `SHM254_Cut_L_T186` (sprint 90 fren-kesişleri) ve `PSD_SHM254_SprintCut`.
- Her klipte `SHME_V254_Block` var: PoseSearch BlockTransition [0,12 s, son].
- Eğriler:
  - `SHM226_V/W` (klip hızı);
  - `SHM238_W/Turn` (yön sözleşmesi);
  - `SHM254_W/Side/Own`;
  - `SHM237_FPPelvisOff`.

## ABP (`ABP_GR_MotionMatchingBase` ve alt sınıfı)

Hepsi `SHM254_Turn` anahtarının arkasında; anahtar 0 iken etkisizler.

- **install254_turn:** dönüş işareti (Delta) ve SHM254_W düşen kenarında gövde çerçevesi devri (LocoExplore/State/On/Yaw).
- **install254_hold:** `Update_MotionMatching` girişinde rota tutma.
- **install254_v2:**
  - `SHM254_HoK`: devirde `GR241_YawRateK` 0 → 1 rampası, 0,2 s;
  - `SHM254_Cancel`: niyet iptali, eşik `SHM254_CancelDeg` 75;
  - iptal anında `SHM238_On` kapanıyor.
- **install254_v3:** iptal `SHM228_On`'u da kapatıyor.
- **install254_v4:** iptal anında, girdi varsa ve hız `SHM254_CancelMinV` (250) üstündeyse `PSD_SHM233_SprintCalm`'a zorlama (InterruptOnDatabaseChangeAndInvalidateContinuingPose).
- **install254_v5:** plan sürerken V2.38 bakışı açık, bakış noktası gövdenin ileri yönü.

## Üretim değerleri (promote254.py)

| Ayar | Önce | Sonra |
|---|---|---|
| `SHM254_Turn` | 0 | 1 |
| `SHM_RedirectDB_SR` | `PSD_SHM_Redirect_SprintReversal` | `PSD_SHM254_SprintRev` |
| `SHM_RedirectDB_SRL`, `SHM212_RouteSRL` | `..._SprintReversal_L` | `PSD_SHM254_SprintRev` |
| `SHM_RedirectDB_SRR`, `SHM212_RouteSRR` | `..._SprintReversal_R` | `PSD_SHM254_SprintRev` |
| `SHM_RedirectDB_SL` | `PSD_SHM210_SprintCut` | `PSD_SHM254_SprintCut` |
| `DA_SHM_Response_Default` kamera | — | Değişmedi (CamSwapV21Enabled true, CamClose 0,90/0,88/0,92/0,97, Tau 0,6) |

**Geri alma:** `req/rollback_req.py` (promote254 rollback modu, `data/promote254_before.json`).

## Araçlar (`Tools/SHME_V254_20261104`)

| Araç | Görevi |
|---|---|
| `gen254_rev.py` | Üreteç (fren/pivot/aktarım/itiş planı, BLOCK_T, OWN_TAIL) |
| `build254_db.py` | Veritabanı kurulumu |
| `install254_*.py` | ABP yamaları |
| `add254_block.py` | Ortadan giriş engeli |
| `promote254.py` | Yükseltme ve geri alma |
| `redir254.py` | Yön değişimi olay analizi |
| `cam254.py` | Kamera kadrajı; ayak/baş ekran yüksekliği eklendi |

Harness senaryoları `v212_run.sh` içinde: s54_*, j54_*, w54_rev.
