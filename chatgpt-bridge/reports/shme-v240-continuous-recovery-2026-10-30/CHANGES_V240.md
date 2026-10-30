# SHME V2.40: değişiklikler (V2.39 395eace üzerine)

## Üretim durumu
- **Üretim davranışı değişmedi: V2.38 / V2.39 üretimi.** V2.40'ın bütün grafik yamaları ABP düğmelerinin arkasında:
  - `SHM239_Own`: devralma, plan sahibi, üçüncü istek ve engel. Varsayılan 0.
  - `SHM240_ExtOn`: devralmadan bağımsız dış etki çekilmesi. Varsayılan 0.
  - `SHM240_HeadOn`: baş önceliği. Varsayılan 0.
- Bunun kanıtı:
  - Her kurulumdan sonra üretim davranış kapısı geçti: `GATE_CUT_FRAMES 38`, V2.38 kesmesi yönlendiriliyor.
  - Temiz açılışta `VERIFY240 ALL_OK` (`verify240.py`, `data/verify240.out`).
- **Aday:** `tkh` = `SHM239_Own` 1 + `SHM240_HeadOn` 1. Üretime alınıp alınmadığı ve gerekçesi REPORT_V240'ta.

## Yeni içerik (`/Game/GraceRanger/SHME/Animations/V240/`)

| Varlık | Kaynak | Not |
|---|---|---|
| `PSD_SHM240_E00 … E95` (96) | `build240_edb.py` | Kaynak bin (48) × hedef (Back / Opp) başına bir giriş veritabanı. İçinde yalnız o kaynağın V2.39 K klipleri var. Her K'nin BranchIn penceresi [t_(K-1), t_K + 0.05], yani istek anında tek bir klip girilebilir. Şema `PSS_SHM239_Takeover` (`schema240_edb.py`). |

**48 V2.38 kesme klibi:** yalnız sabit `SHM240_Src` eğrisi eklendi (R P00..P23 = 0..23, L = 24..47; `src240_cut.py`). Poz anahtarları değişmedi.

Yeni animasyon klibi yok.

## ABP yamaları (`Tools/SHME_V240_20261030`, kurulum sırasıyla)

| Kurulum | İş | Düğme |
|---|---|---|
| `install240_once` | Takeover anahtarı motion matching'in GERÇEK seçimine bakar (`CurrentSelectedDatabase`). Tek zorlanmış arama yapılır; yeniden deneme yalnız zamanla (0.05 s). Kare sayısı ve harmanlanmış eğri kullanılmaz. | Own |
| `install240_edb` | Deterministik giriş: kaynak eğrisi + kilitli hedef → `SHM240_EDB` (96 yapraklı SelectObject ağacı). `Update_MotionMatching` bunu kullanır. | Own, `SHM240_Det` 1 |
| `install240_done` | Giriş onayı yeni veritabanı adlarını da tanır. | Own |
| `install240_exit`, `install240_exit2` | Plan bittiği karede son yön gövde çerçevesine devredilir: bileşen `LocoYaw` / `LocoState` 1 / `LocoExplore` / `LocoInYaw`. | Own |
| `install240_fixexec` | `exit2`'nin kopardığı snapshot exec zincirini onarır (3 giriş bağlantısı). | — |
| `install240_yield` | Üçüncü istek: devralma klibi, momentum düşükken (< 80 cm/s) ve niyet hedeften > 35° saparken normal başlangıç / itme yönlendirmesine teslim eder. | Own |
| `install240_extknob` | Dış etki artığının kapısı `FMax(SHM239_Own, SHM240_ExtOn)` olur; dış etki çekilmesi ayrı test edilebilir. | ExtOn |
| `install240_wall` | Engel: `SHM239_Ext` aktif, hız < 60 cm/s ve bir plan veritabanı seçiliyken TEK zorlanmış ayakta-durma araması yapılır. Hesap snapshot'ta, okuma `Update_MotionMatching`'de. | Ext (Own veya ExtOn) |
| `install240_head` | Baş önceliği: elle bakış yokken (`TW_LastLookTime` > 0.8–1.4 s) ve hareket varken satıcı aim offset'i (`Get_AOValue` lerp alfası) FInterpTo ile kapanır. | `SHM240_HeadOn` |
| `install240_blk2` | (a) Engel aramasında throttle serbest kalır (`SearchThrottleTime` Select pick OR `SHM240_Blk`). (b) Baş solması plan eğrisi bitince başlar: × (1 − `SHM239_W`). | Ext / HeadOn |

## Harness
- `Tools/SHME_V212_20261017/v212_run.sh`:
  - yeni senaryolar `j40_rlw`, `j40_lrw` (üçüncü istek) ve `j40_wall` (planlı sağ 90 sırasında gerçek duvar teması; `Wall40` kutusu);
  - telemetride `SHM240_TkDone` / `SHM240_TkT`.
  - Yedek: `Saved/Codex/SHME_V240_20261030/v212_run_pre240.sh`.
- `tables240.py`: V2.39 tablolarının V2.40 etiketleri.
- `verify240.py`: verify239 + V2.40 düğmeleri, 96 giriş DB'si, `SHM240_Src` eğrileri, snapshot exec bütünlüğü.

## Geri dönüş
- **Davranış:** `SHM239_Own` = 0, `SHM240_ExtOn` = 0, `SHM240_HeadOn` = 0 (varsayılanlar).
- **İkili yedekler:** `Saved/Codex/SHME_V240_20261030/checkpoint/manifests/<ad>/`, yayımlanmadı. Sırasıyla:
  - `once1`, `src1`, `edb1`, `edbi1`, `done1`, `exit1`, `exit2`, `sch1`, `fix1`;
  - `yield1`, `extk1`, `wall1`, `head1`, `blk2`.
