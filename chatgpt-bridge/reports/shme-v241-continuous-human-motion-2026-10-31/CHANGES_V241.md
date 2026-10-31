# SHME V2.41: değişiklikler (V2.40 9420bb5 üzerine)

## Üretim durumu
- **Üretim davranışı değişmedi.** V2.41'in bütün grafik yamaları, varsayılanı V2.40 davranışı olan anahtarların arkasında:
  - `SHM239_Own = 0`, `SHM240_ExtOn = 0`, `SHM240_HeadOn = 0`. Dokunulmadı.
  - `SHM241_KOn 0`, `SHM241_PushYawK 1`, `SHM241_StartOn 0`, `SHM241_BlkOnce 0`.
  - Pawn (`BP_GR_Player` / `BP_PBI_Player`): `GR241_YawRateK 1`, `GR241_StartOn false`.
- Her yapısal yamadan sonra üretim davranış kapısı koşuldu (`run241_g.sh`): `j38_c90r`, `j39_rl`, `j38_cc90`, `j40_wall`, hepsi `o`.
- `verify241.py`: anahtarlar, pawn varsayılanları, 362 K-DB, eğriler, AO düğümü ve snapshot öksüzleri. Çıktı `data/verify241.out`.
- Her yazma işi manifest + doğrulanmış yedekle (`manifest241.py`) ve tek kilit sahibiyle (`v241`) yapıldı. PIE sırasında yazma yapılmadı.

## Yeni içerik

| Varlık | Kaynak | Not |
|---|---|---|
| `PSD_SHM240_E<ee>_K<k>` (362, V241 klasörü) | `build241_kdb.py` | (kaynak bin, hedef, K) başına tek klipli takeover giriş DB'si. Ad, V2.40'ın giriş onayı / engel ad testleri eşleşsin diye `PSD_SHM240_E` önekini taşıyor. |
| `PSS_SHM241_TkEntry` | `install241_sch.py` | `PSS_SHM239_Takeover` kopyası, yörünge ağırlığı 0. Kanal eklenmedi; Python'dan kanal eklemek indeksleyiciyi çökertti (`rejected/`). |
| `BS_SHM241_AO_Head` + 15 sekans kopyası | `ao241_copy.py` | Bölgesel AO: kök / pelvis / bacak ofseti 0, omurga ×0.3, boyun / baş tam. Satıcı orijinalleri değişmedi. ABP'ye bağlı değil; yalnız bellek içi PRE (`pre241_ao.py`) ile denendi. |

**Değişen aday verisi** (üretim yolunda kullanılmıyor):
- 362 V2.39 takeover klibine yeni BranchIn izi `SHME_V241_K` eklendi. Penceresi [t_(K-1), t_K + 0.05]; V2.40 izi `SHME_V240_E` olduğu gibi duruyor.
- 96 V2.40 giriş DB'si (`PSD_SHM240_E00..95`) şema olarak `PSS_SHM241_TkEntry` kullanıyor.
- Kökü dönen 8 kalkış kopyasına (`SHM_JogQ_af_Loco_Jog_Start_Turn{L,R}{045,090,…}`) `SHM241_SYaw` / `SHM241_SW` eğrileri işlendi (`bake241_syaw.py`). Poz anahtarları değişmedi.
- Teşhis: `SHM239_Tk_R_P10_K3_Opp` penceresi `diag241_win.py` ile daraltılıp geri alındı (`win1` / `win1r`). `diag241_e21.py` değişiklik yapmadan hata verdi.

**Yeni hareket animasyonu yok.**

## ABP / pawn yamaları (`Tools/SHME_V241_20261031`, kurulum sırasıyla)

| Kurulum | İş | Anahtar |
|---|---|---|
| `install241_kdb` | K = `SHM239_Step` → `KIdx = 4·EIdx + K−1` → `SHM241_KDB` (384 yapraklı SelectObject ağacı; boş yuva = V2.40 E DB'si). `Update_MotionMatching`'te `SHM240_EDB`'nin bütün okuyucuları `SHM241_KDB`'yi okuyor. | `SHM241_KOn` |
| `install241_push` | Snapshot: `pawn.GR241_YawRateK := SHM239_Ext ? PushYawK : 1`. `GR_Impl_CP_PhysicalRedirect`'in `RInterpTo_Constant` hızı × `GR241_YawRateK`. | `SHM241_PushYawK` |
| `install241_start` (+ `install241_startfix`) | Kalkış yön sözleşmesi: kökü dönen bir kalkış pozdayken kapsül yönü = giriş yönü + `SYaw / max(SW, 0.01)` (bir kare ileri bakışla), kısa tutma süresiyle. | `SHM241_StartOn` |
| `install241_blk` | Engel zorlamalı arama için throttle yalnız zorlanan karede bırakılıyor (`SHM241_BlkPrev`). **Hipotez çürüdü**: 120 FPS duvar atlaması aynı. | `SHM241_BlkOnce` |

Her yamada exec bağlantıları korundu: araya ekleme sonrası bütün gelen bağlantılar yeniden bağlandı ve yeniden sayıldı (V2.40 exec-splice tuzağı).

## Harness
- `qa_pie.py`: `move.gates`. Bir girdi olayı bir ABP / bileşen değerine kapılanabiliyor (ör. `A_CT_Jog_Fwd` döngü zamanı). `j41_*` senaryoları aynı fiziksel girişi test ediyor.
- `v212_run.sh`: `j41_rl_p10/p16/p21/p04`, `j41_rw_*`, `j41_lr_*`, `j41_rlw_*`.
- Analiz araçları:
  - `entry241.py`: beklenen / girilen K, atlama, taşma, gecikme.
  - `align241.py`: pelvis / göğüs / baş − yön.
  - `fps241.py`: FPS tablosu.
  - `worst241.py`, `seq241.py`, `win241.py`, `tables241.py`.
- Medya: `media241.sh`.

## Beceri güncellemeleri (yeni beceri yok)
- `sphirus-balance-recovery`: devralmada K seçimi ile itmede gövde yönü.
- `sphirus-safe-unreal-iteration`:
  - Bayat PRE manifesti sessizce reddediliyor; PREAO sayımı yapılmalı.
  - Python'dan PoseSearch kanalı eklenmez.
  - Aynı build'de aynı fiziksel durum garantisi yok.
- `sphirus-human-motion-engine/references/validation.md`: kapılı senaryolar ve ilk adımdaki ayrışma.
