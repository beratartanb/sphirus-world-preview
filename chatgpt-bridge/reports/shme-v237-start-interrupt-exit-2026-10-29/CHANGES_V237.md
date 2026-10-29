# SHME V2.37: değişiklikler (V2.36 eaaedca üzerine)

## Üretim (temiz açılışta VERIFY237 ALL_OK — yalnız yapılandırma kontrolü)

Değişiklikler ABP veritabanı değişkenleri, bir FootPlacement özelliği ve yeni varlıklardır.

V2.36 üretim klipleri ve veritabanları **değişmedi**; V2.37 içeriği yeni kopyalarda.

| Grup | ABP değişkeni / özelliği | Yeni değer | Geri dönüş |
|---|---|---|---|
| `start` | `SHM_JogStartDB_L` / `_R` | `V237/PSD_SHM237_JogStartS_L` / `_R` | `V236/PSD_SHM236_JogStartS_L` / `_R` |
| `resume` | `SHM236_DB_JogResume` (CP kalkış yolu) | `V237/PSD_SHM237_JogResume` | `PSD_CP2_JogStart` |
| `stop` | `SHM236_DB_JogStop` | `V237/PSD_SHM237_JogStop` | `V236/PSD_SHM236_JogStop2` |
| (ABP) | FootPlacement `PelvisSettings.DisablePelvisCurveName` | `SHM237_FPPelvisOff` | boş |

- **FootPlacement eğri adı:** bu eğriyi taşımayan klipler için hiçbir şeyi değiştirmez.
  - Kontrol: ABP düzenlemesinden sonraki `j36_stop:o` koşusu, düzenleme öncesiyle aynı çıktı.

## Yeni içerik (`/Game/GraceRanger/SHME/Animations/V237/`)

| Varlık | Kaynak | Açıklama |
|---|---|---|
| `SHM237_JogStart_F_Lfoot` / `_Rfoot` | `gen237_start.py` | Adım planlı düz tempolu kalkış (aşağıda). |
| `SHM237_RePush_<bin>_T010/026/042/058` (96) + `SHM237_RePush_Br_P00_T038` | `gen237_start.py` | Duruşun içinden yeniden itiş: 24 duruş bölmesi × 4 yeniden basma anı. Kare 0 = V237 duruşunun o andaki pozu. |
| `SHM237_JogStop_B{l\|r}_P00..23` | `gen237_stop.py` | V2.36 duruş ailesinin aynı adım planı. Fren pelvisi kliple taşınır (`SHM237_FPPelvisOff`). |
| `PSD_SHM237_JogStartS_L` / `_R` | `build237_dbs.py` | Vendor kalkış DB'lerinin (`Starts/PSD_SHM_JogStartS_*`) kopyası + V2.37 kalkışı. |
| `PSD_SHM237_JogResume` | `build237_dbs.py` | `PSD_CP2_JogStart` kopyası + 2 kalkış + 97 yeniden itiş. |
| `PSD_SHM237_JogStop` | `build237_stopdb.py`, `db236_bias.py` | 24 V237 duruşu. Continuing bias **−25** (ilk sürüm −3; aşağıda). |

### Kalkış üreteci (`gen237_start.py`)
- **Kök:** ölçülen oyun içi kapsül (165 → 245 cm/s², efor ölçeği dahil).
  - V2.36: 470 cm/s² → MM hızı 0.70–0.84.
- **İnişler:**
  - Her iniş planlı: 30 → 65 → 105 cm.
  - Son iniş döngünün kendi inişi (aynı ayak, aynı uzanma). Sonrası döngü, kökle tutarlı saatle.
- **Yük taşıyan ayak:**
  - Düz duruşuna göre en çok 50° topuk kalkışı.
  - Döngünün kendi topuk kalkışı (toe-off) yalnız itişin son 0.16 s'sinde.
  - V2.36: havadaki döngü pozuna 122°'ye kadar dönüyordu.
- **Kalkma zamanı:** ayak, kök erişim sınırını geçince **veya** adım saatine göre döngünün kaldırdığı anda kalkar (hangisi önce).
- **Salınım:** döngünün salınım şekli adım boyuna göre ölçeklenir; salınım bacak boyunu geçmez.
- **Ofsetler:** yalnız salınımda çözülür.
- **Yeniden itiş:**
  - Kaynak = duruş klibi, yeniden basma anındaki pozu.
  - Kök hızı = duruşun o anki hızı.
  - Havadaki ayak kendi hızıyla iner.
  - Kare 0'dan önce basılmış ayağa yeni duruş süresi uygulanmaz.

### Duruş pelvisi (`gen237_stop.py`)
- **Sorun (V2.36):** iki sahip.
  - Klip, freni neredeyse düz bacakla 91–94 cm'ye kaldırıyordu.
  - FootPlacement (AllLegs, yaylı) bunu 6–9 cm indiriyordu (`SHM_HCo − SHM_HCi`).
  - Sonuç: diz bükük çömelme.
- **V2.37:** aynı adım planı.
  - `SHM237_FPPelvisOff` frende 1, son basıştan sonra 0.25 s'de 0.
  - Oturmuş duruşta eğimli zeminde FootPlacement yine uyarlar.
- **Fark:** reach-drop kuralının boşta-bacak tabanı son inişe kadar kaldırıldı.
  - Kaynakta en çok 6.1 cm iniş.

### Duruş girişinin yapışması (continuing bias −3 → −25)
- **Sorun (V2.36 ve V2.37 ilk sürüm):** bırakmadan sonraki ~0.08 s'de duruş DB'si her aramada **klip zamanı 0'da yeni bir faz bölmesi** seçiyordu.
  - 120 FPS dizisi: P04 → P16 → P05 → P17 → P06. 30 FPS'te bir sıçrama (P16 → P05).
  - Son seçilen bölme bırakmadan ~0.07 s sonra başlar, ama hız saati bırakma hızındadır (300 cm/s; kapsül 259'da).
  - Sonuç: basılı ayak 60/120 FPS'te 15–20 cm kayar. `j36_rse` / `j36_rsl` 30 FPS sürüklemesinin sahibi de aynı sıçrama.
- **Aday karşılaştırması (aynı editör, ABP değişkeniyle):**
  - cb10 (−10): sıçramayı yalnız kısalttı (19.8 → 16.8 cm).
  - cb25 (−25): ilk bölmede kaldı. 120 FPS `j36_stop` 19.8 → 5.0, `rsm` 19.8 → 5.0, `stopb` 11.4 → 0. 30 FPS `rse` 14.0 → 0.
- **Üretim:** üretimdeki `PSD_SHM237_JogStop` özelliği −25 yapıldı (manifest `bias1`, ikili yedek).
  - Kopyalar `PSD_SHM237_JogStop_cb10` / `_cb25` yalnız A/B adayıdır, üretimde değildir.

## Reddedilen / üretime alınmayan
- **Fren dizi payı 5 cm (`km_brake 5`):**
  - Kaynak pelvisi 80.4 cm'e indi (kaynakta çömelme).
  - Kuru koşuda görüldü, oyuna alınmadı; yazılan aday hemen yeniden yazıldı.
- **İlk aşama temsilî yeniden itiş (`Br_P00_T038`, V2.36 duruş kaynağı, eğrisiz):**
  - Doğrulamada yakalandı, güncel üreteçle yeniden üretildi.

## Araçlar (`Tools/SHME_V237_20261029`)

| Araç | İş |
|---|---|
| `gen237_start.py` | Adım planlı kalkış + yeniden itiş üreteci |
| `gen237_stop.py` | V2.36 duruş planı + klip pelvisi |
| `build237_dbs.py`, `build237_stopdb.py` | DB kopyaları ve BranchIn |
| `install237_fppelvis.py` | FootPlacement eğri adı |
| `promote237.py`, `verify237.py` | Üretime alma ve doğrulama |
| `probe237_fp.py`, `probe237_stopsearch.py` | FootPlacement ayarları; ABP veritabanı arama çağrıları ve kesme modları (salt okunur) |
| `dbcopy237_bias.py` | Başka continuing bias'lı DB adayı kopyası |
| `dump237.py`, `pelvis237.py`, `upper237.py`, `ab237.py`, `tables237.py` | Aynı karelerde temas, pelvis zinciri, üst beden, A/B ve tablolar |
| `media237.sh`, `manifest237.py`, `v237_ab.sh`, `ab_safe237.sh` | Kayıt, manifest, A/B |

## Geri dönüş
- **Değişkenler:** `promote237.py` ile `{'rollback': True}`. Değerler `PROMO237` çıktısında.
- **FootPlacement eğri adı:** `install237_fppelvis.py` ile `{'name': ''}`.
- **Duruş DB bias:** `db236_bias.py` ile `{'bias': -3.0}`.
- **İkili yedekler:** `Saved/Codex/SHME_V237_20261029/checkpoint/manifests/<ad>/` (yayımlanmadı).
