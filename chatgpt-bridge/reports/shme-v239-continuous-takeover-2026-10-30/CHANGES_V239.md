# SHME V2.39: değişiklikler (V2.38 c0737f9 üzerine)

## Üretim durumu
- **Üretim davranışı V2.38.** V2.39'un bütün grafik yamaları ABP düğmesi `SHM239_Own` arkasında; varsayılanı 0, etkisiz.
- Temiz açılışta `VERIFY239 ALL_OK` (`Tools/SHME_V239_20261030/verify239.py`).
- Bu kontrol `verify238`'i yeniden okur. Eğri adları artık büyük/küçük harf duyarsız karşılaştırılır (editör `shm226_v` gösteriyor). Arama freni sarmalayıcısının eski zinciri koruduğu da doğrulanır.
- Aday: `SHM239_Own` = 1 (A/B'de `tk`). Üretime alınmadı: 120 FPS ve gerçek zamanda devralma girişi kararsız.

## Yeni içerik (`/Game/GraceRanger/SHME/Animations/V239/`)

| Varlık | Kaynak | Not |
|---|---|---|
| `SHM239_Tk_{R\|L}_Pnn_K{k}_{Back\|Opp}` (362) | `gen239_tk.py` | Kesmenin ön kısmı birebir; yeni plan K. temasta başlar. 364 adaydan 2'si bacak korumasınca reddedildi (`R_P04_K2_Opp`, `R_P11_K2_Opp`). |
| `PSD_SHM239_Tk{R\|L}_{Back\|Opp}` (4) | `build239_tkdb.py` | Giriş veritabanları; BranchIn penceresi = ön kısım (0 .. t_K + 0.05). |
| `PSD_SHM239_TkP{R\|L}_{Back\|Opp}` (4) | `build239_tkdb.py` | Oynatma veritabanları; tam pencere. |
| `PSD_SHM239_Tk_Back/Opp`, `TkP_Back/Opp` | — | Eski birleşik sürüm (iki taraf karışık); kullanılmıyor. |
| `PSD_SHM239_JogCutTk` | — | Reddedildi (kesme girişinde istenmemiş geri dönüş); kullanılmıyor. |
| `PSS_SHM239_Takeover` | `schema239.py` | Düşük trajectory ağırlığı; işe yaramadı. Yalnız eski birleşik veritabanlarında, etkisiz. |

**48 V2.38 kesme klibi:** yalnız `SHM239_Step` (planlı temas saati) ve `SHM239_StepN` eğrileri eklendi (`step239_cut.py`). Poz anahtarları değişmedi.

## ABP yamaları (`Tools/SHME_V239_20261030`, kurulum sırasıyla; hepsi `SHM239_Own` arkasında)

| Kurulum | İş |
|---|---|
| `install239_own` | Plan sahibi (`Update_MotionMatching` girişi); niyet / takeover isteği; taraf ve hedef DB'leri |
| `install239_latch` | V2.28'in tek kare düşüşü yön kilidini yeniden kilitleyemez; `ClipSpeedOn` ve `On` tutulur |
| `install239_tkon`, `install239_req`, `install239_par` | Geçiş kilidi (≤ 16 kare); istek anında; StepN sınırı |
| `install239_thr`, `install239_play`, `install239_play2` | Takeover oynarken arama freni; oynatma veritabanına geçiş (kilitli hedefle) |
| `install239_srch`, `install239_blend` | Arama kapısı ve kısa blend: etkisiz bulundu, ama zarar vermiyor |
| `install239_unthr` | **Asıl çözüm:** geçiş kilidi boyunca `SearchThrottleTime` = 0 |
| `install239_cmd` | Takeover klipleri için kesin yön eşlemesi |
| `install239_side` | Plan yönüne göre taraf veritabanı seçimi |
| `install239_ext`, `install239_ext2` | Dış etki artığı (snapshot başında); itmede plan geri çekilir |
| `install239_bal` | Canlı denge okuması (telemetri) |
| `diag239_umm` | Tanı sayacı (`Update_MotionMatching` çağrı sayısı); zararsız |

## Harness
- `Tools/SHME_V1_20260925/qa_pie.py`: `pushes` [[dt, vx, vy]] olayı eklendi (`AddImpulse` hız değişimi). Yedeği `qa_pie_pre239.py`.
- `Tools/SHME_V212_20261017/v212_run.sh`: yeni senaryolar `j39_rl / rw / rl_e / rl_l / lr / lw / push_plan / push_jog` ve V2.39 telemetrisi. Yedeği `v212_run_pre239.sh`.

## Geri dönüş
- **Davranış:** `SHM239_Own` = 0 (zaten varsayılan).
- **İkili yedekler:** `Saved/Codex/SHME_V239_20261030/checkpoint/manifests/<ad>/`, yayımlanmadı.
  - ABP: `own1 … bal1`.
  - Kesme klipleri: `step1`, `step2`.
  - Takeover klipleri ve DB'ler: `tk1 … tkside`.
