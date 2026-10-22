# V2.22 değişiklik özeti (kod / graf / içerik / araç)

Bütün ikili varlık değişiklikleri editör üzerinden yapıldı. Kopyalar:
- `checkpoint/pre_promo/`: ABP'ler, SHME DA, bileşen;
- `checkpoint/revturn/`: dört RevTurn orijinali;
- `checkpoint/tools_v1/*.v222a`: DSL kaynakları.

## Üretimde

**İçerik (yeni)**
- `/Game/GraceRanger/SHME/Animations/V222/A_SHM222_WalkStart_L`, `_R` — `gen222_start.py` ile üretildi.
- Ayak planı, kök yolu ve zamanlama V2.8 temas planlı başlangıçtan; kurulu mesafe saati bu kök eğrisine bağlı.
- Yeni olanlar:
  - kollar için faz uyumlu sanal döngü saati, genlik tek yönlü artıyor;
  - 6° başlatma eğilimi;
  - 10 cm ilk adım açıklığı;
  - duruş genişliği farkı ayak havadayken kapatılıyor;
  - kaynak idle karesi 68 s (oyunun gerçek başlangıç karesi).

**İçerik (yerinde bake)**
- `/Game/GraceRanger/SHME/Animations/V216/SHM216_RevTurn_{L,R}_{L,R}foot` üst gövdesi — `rb222_revturn.py`.
  - Bacak, kök ve pelvis değişmedi (okuma kontrolü 0.0 cm).
  - Gövde, boyun, baş ve kollar tempolu → depar döngülerinden alınıyor, bacakların fazına bağlı, genlik klibin adım uzunluğuyla ölçeklenmiş.
  - Kaynak bükülmesinin yarısı gövde ekseninde korunuyor; giriş 0.50–0.95 s arasında karışıyor.
- Yeniden anahtarlanan veritabanları (etiket `SHME_V222_RB3`): `PSD_SHM214_RevPush`, `PSD_SHM215_RevPushLow`, `PSD_SHM215_Rev_L`, `PSD_SHM215_Rev_R`.

**ABP_GR_MotionMatchingBase (CDO)**
- `SHM28_StartMode 1`.
- `SHM28_StartL / _R` = V2.22 klipleri.
- `SHM222_TapGate 0`. Kapı grafı kuruldu (`install_v222_tapgate.py`) ama reddedildi.

**BP_SHM_HumanMotionComponent** — `SHM_UpdateCameraV21`, `CamCloseEnabled`.
- Kol ölçeği hıza göre çarpılıyor:

  | Durum | Duruş | Yürüyüş (140 cm/s) | Tempolu (300 cm/s) | Depar (490 cm/s) |
  |---|---|---|---|---|
  | Çarpan | 0.90 | 0.88 | 0.92 | 0.97 |

- Yalnız açık alanda (× `CamOpenness`), τ 0.6 ile süzülüyor, ışınlanmada sıfırlanıyor.
- Fark dosyası: `diff_shm_src.py.txt`.

**DA_SHM_Response_Default:** `CamCloseEnabled true` (varsayılan anahtarlar).

## Araçlar (Tools/SHME_V222_20261022/)

- **Tanı:** `body222.py` (karakter çerçevesi), `clipscan222.py` (klip kök uzayı).
- **Üretim:** `gen222_start.py`, `rb222_revturn.py` (orijinal anahtarlar `revturn_src/*.json`).
- **Kurulum ve terfi:** `install_v222_tapgate.py`, `promote222.py`, `verify_prod222.py`, `v222_patch.py`, `v222_build.sh`.
- **Harness:**
  - `v222_ab.sh`: taban = V2.21 üretimi.
  - `ab_safe222.sh`, `runfps.sh`, `vars222.sh`.
  - Değişkenler: `p` = V2.22, `o` = V2.21 başlangıç + kamera; `s22`, `cc`, `tg`.
- **Medya:** `media222.sh`.
