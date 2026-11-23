# Sphirus World — ilk temsilî kesit, referans turu (2026-11-23)

> Bu yayında ham referans görselleri (`references/`) ve yerel yollar yoktur; karşılaştırma görsellerinde küçültülmüş hâlleri yer alır. Skill yaklaşımı: `SKILL_YAKLASIMI.md`.

Durum: **kısmi**. Kamera R04 kadrajına taşındı, kaydedildi ve yeniden açılmış editörde doğrulandı. Dünya/ışık, karakter kıyafeti ve hareket
için bu turda kalıcı değişiklik **yok**; nedenleri aşağıda. Kullanıcı kabulü yazılmadı.

Çalışılan proje: `<proje>/sphirus_UE59` (UE 5.9.0-60738873, canlı editörden okundu).
Not: OneDrive altındaki `ActionAdventureMovementS` kopyası 5.8 temelidir ve 15 Kasım'dan beri değişmemiştir; ona dokunulmadı.

## 1. Skill ve Unreal'a uyarlama

- Kurulan: `reference-to-game@reference-to-game` 0.1.0, commit `6a00e491f578bbfcbdba45f0c7bddf4693016e61`, proje kapsamı
  (`.claude/settings.json` içinde etkin; dosyalar `~/.claude/plugins/cache/reference-to-game/reference-to-game/0.1.0/`).
  Belgelenen iki komutla kuruldu; `claude plugin list` "enabled" gösteriyor.
- Paketin Unreal üreticisi yok. Yalnız alım, yetki atama, karşılaştırma ve kanıt bölümleri kullanıldı. Tarayıcı oyunu veya Three.js
  prototipi üretilmedi.
- Proje köprüsü: `.claude/skills/sphirus-reference-review/SKILL.md` (mevcut kamera / hareket / çevre becerilerine yönlendirir; hiçbirini
  değiştirmez). `CLAUDE.md` Skills bölümüne tek cümle eklendi.
- `r2g freeze` yalnız sözleşme dosyalarını ve `app/` klasörünü özetler; `.uasset` / `.umap` okumaz. Bu yüzden
  `Tools/R2G_20261123/unreal_source_manifest.py` gerçek Unreal dosyalarının sha256 kaydını `app/UNREAL_SOURCE_MANIFEST.json` içine yazar.
  Bu bir özet kaydıdır; sanat kalitesi doğrulaması değildir. Projede git yok.
- Araç notları: motor Python'unda Pillow yoktu; `Tools/R2G_20261123/deps` altına kuruldu (sertifika doğrulaması sistem deposuyla).
  ffmpeg yok; `inspect` yalnız görselleri okudu.

## 2. Referans manifesti

Sekiz görsel geldi. İçeriklerinden tanındı; dosya adına veya sıraya güvenilmedi.

| Kimlik | Dosya (yüklenen ad) | Kasa içi | Ne | Yönlendirdiği karar |
|---|---|---|---|---|
| R01 | `69241a5f-image.png` | `ref-001` | Karakter paftası | Saç kütlesi ve duruş hedefi; kıyafet "dışarı çıkış" görünümü olarak kaydedildi. Yüz kullanılmadı |
| R02 | `59230a22-image.png` | `ref-002` | Dış dünya | Işık ve su hedefi; su parlaması teşhisi |
| R03 | `de8800f6-image.png` | `ref-003` | Ev / atölye içi | İç mekân dili; yeniden kurma yok |
| R04 | `2fe623e6-image.png` | `ref-004` | Oynanış kamerası | Kamera değişikliği (bu turun tek kalıcı değişikliği) |
| R05 | `612cb22d-image.png` | `ref-005` | Poz paftası | Yalnız silüet niyeti; değişiklik yok |
| **R06** | **gelmedi** | — | Rezonans hâli | Karar yok. Mevcut sistem yalnız belgelendi |
| X01 | `72150e00-image.png` | `ref-006` | Ek: evin servis cephesi | Yalnız malzeme / yaşanmışlık kanıtı |
| X02 | `b5c3375a-image.png` | `ref-007` | Ek: verandalı ön cephe | Aynı; R02'den farklı bir ev biçimi gösteriyor |
| X03 | `e9b55243-image.png` | `ref-008` | Ek: açık plan iç mekân | Aynı |

Altı görsel istenmişti; R06'ya uyan bir görsel yoktu ve listede olmayan üç görsel vardı. X01–X03 en düşük öncelikle, yalnız ek kanıt
olarak kaydedildi. Yetkiler ve sınırlar: `case.json`; gözlem / çıkarım / tasarım ayrımı: `analysis/observations.md`, `style.json`.

## 3. Canlı projede doğrulananlar (eski adlar yerine)

| Konu | Canlı durum |
|---|---|
| Harita | `/Game/GraceRanger/Maps/L_GR_SphirusHouse` (+ `L_GR_CurrentHouseContent`, `L_SphirusHouse_ASSET_YARD`) |
| Oyuncu | `BP_HybridA_Player` (üst sınıf `BP_Sph_GASPCharacter`), GameMode `BP_GM_GR_GraceRanger` |
| Beden / yüz | `SKM_MHC_Sph8_BodyMesh`, `SKM_MHC_Sph8_FaceMesh`. **`MHC_HazelM` aktif piyonda değil** |
| Animasyon | Sürücü `ABP_Sph_GASP` (UEFN iskeleti) → `RTG_Sph_UEFN_to_MH` → görünür beden `ABP_Sph_Body_GASP` |
| Saç | `/Game/Grooms/001_Messy_Bob` (R01 saç kütlesiyle aynı aile) |
| Kıyafet (yeni oyun) | `SKM_Sph_RetroTop` + `SKM_Sph_Pants70` + kemer. R01'deki henley / kot / bot değil |
| Kamera | Tek sahip `AC_Sph_Camera` (`GR_SpringArm` + `Cine`). GASP'ın kendi yay kolu ve `GameplayCamera` bileşeni duruyor ama görüntüyü bu bileşen yazıyor |
| Rezonans | `AC_Sph_Camera.ResPulse` → `MPC_Sph_Perception` → `EX_Look_Resonance` PPV, `M_Sph_Resonance` |

## 4. Gerçekten değişenler

**Unreal varlığı (1):** `/Game/Sphirus/Player/Camera/AC_Sph_Camera` — sınıf varsayılanları.

| Değişken | Önce | Sonra |
|---|---|---|
| `OutD` / `OutDTight` (dış mesafe) | 124 / 108 | 165 / 135 |
| `HomeD` / `HomeDTight` (ev içi mesafe) | 98 / 86 | 118 / 98 |
| `HeadX` (başın yatay ekran konumu) | 0,34 | 0,30 |
| `HeadY` (başın dikey ekran konumu) | 0,33 | 0,24 |

FOV (66 dış / 62 iç, koşuda +3), hız kolu (4 cm), gecikme, çarpışma ve etkileşim istasyonu kadrajları değişmedi. Değerler R04'ten FOV / kol
türetilerek değil, oyuncu kamerası karelerinde gövde ölçeği eşlenerek seçildi (iki aday; ikincisi yalnız baş yüksekliğini düzeltti).

- sha1: `59384767…` → `441d7ab3…`. Yedek ve geri alma: `review/data/write_manifest.json`
  (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/r2g_cam_064140/…`, editör kapalıyken geri kopyalanır).
- Harita, su malzemesi, oyuncu Blueprint'i ve kullanıcı kaydı diskte **değişmedi** (`app/UNREAL_SOURCE_MANIFEST.json`; kayıt sha1
  `3d81ab9d…` her koşuda aynı).

**Belge / araç:** bu klasör; `.claude/skills/sphirus-reference-review/`; `CLAUDE.md` (bir cümle); `.claude/settings.json` (plugin etkin);
`Tools/R2G_20261123/`.

## 5. Referans – önce – sonra

- R04 ↔ oyun: `review/compare/R04_vs_before_shore.png`, `review/compare/R04_vs_after_shore.png`.
  Önce: yalnız baş ve sırtın üstü, kadraj bel hizasında kesiliyor. Sonra: baş–kalça görünür, karakter sol üçte birde, yol ve ev için sağ taraf açık.
- Aynı girdi planı, eşleşen kareler: `review/candidates/vid_out_pairs.jpg` (kıyı), `review/candidates/vid_in_pairs.jpg` (ev içi → arka kapı → bahçe).
- Sabit noktalar: `review/stills_before/` ve `review/stills_after/` (15 nokta, 1600×900, oyuncu kamerası).
- R02 / R03 ↔ oyun: `review/compare/R02_*.png`, `review/compare/R03_*.png` (bu turda değişiklik yok; farkın kaydı).
- Denenip geri alınan adaylar: `review/candidates/atm_ab1…4.jpg`, kamera adayları `cam_ab1…2.jpg`.
- Rezonans (mevcut hâl): `review/stills_after/res_*.jpg`.

## 6. Oynanış kayıtları

`review/videos/` — 30 Hz sabit oyun adımı, 30 fps (gerçek hız), oyuncu kamerası, ev haritası:

| Dosya | İçerik |
|---|---|
| `r2g_before_out.mp4` / `r2g_after_out.mp4` | Kıyı yolu: yürüyüş, tempolu (Shift), yürüyüş, duruş, sağa / sola kavis, S geri, D / A yan, 180° dönüş, yürüyüş, depar, duruş (~31 sn) |
| `r2g_before_in.mp4` / `r2g_after_in.mp4` | Mutfak → arka kapı → bahçe yolu, tempolu bölüm, iki 180° dönüş (~39 sn) |

Yayın notu: iki kıyı videosu GitHub dosya sınırı için aynı çözünürlük ve kare hızında daha düşük bit hızıyla yeniden kodlandı (`scripts/transcode.py`); özgün kodlamalar yerelde duruyor. `review.json` içindeki özetler özgün dosyalara aittir.

Girdinin niteliği: tuşlar editör içinden enjekte edildi, bakış yönünü koşum takımı yazdı. İnsan eliyle oynanmış veya gamepad ile alınmış
kayıt değildir. "Sonra" kayıtları kaydedilmiş ve yeniden açılmış durumdan alındı. **Videoları gerçek hızda izleyemedim**; saniyede bir
karelere baktım. Zamanlama, ağırlık aktarımı ve ayak teması için görsel doğrulama yok.

## 7. Ayrı sonuçlar

| Alan | Sonuç | Dayanak |
|---|---|---|
| Kamera kadrajı | **İyileşti, kaydedildi** | R04 karşılaştırması; kıyı kaydında yürüyüş / tempo / depar karelerinde kol ve kalça kadrajda |
| Kamera — dar alan | **Açık** | Ev içi kaydın ilk saniyesinde (arkada duvar) ve kapı eşiğinde saç kadrajın büyük bölümünü kapatıyor; önce de böyleydi |
| Kamera davranışı (takip, gecikme, dönüşte kadraj) | **Doğrulanmadı** | Yalnız kareler; hareketli izleme yok |
| Dünya / ışık (R02) | **Değişmedi** | Göl, güneşe karşı bakışta beyaza yanıyor; batı kıyısından bakışta koyu ve sakin |
| İç mekân (R03) | **Değişmedi** | Aynı malzeme ailesi; referans daha kaba ve el yapımı |
| Karakter kimliği | **Korundu** | Yüz, beden, saç dokunulmadı |
| Kıyafet (R01) | **Açık** | Yeni oyunda kolsuz üst + şort; gardırop setlerinde henley / kot / bot olup olmadığı bu turda incelenmedi |
| Hareket | **Değişmedi, bu turda ölçülmedi** | Bugünkü Tur 8 raporu geçerli (`chatgpt-bridge/reports/sphirus-ue59-guardian-tamamlama-2026-11-23`): hızlı A/D kayması 22–40 cm ve diğer açıklar duruyor |
| Rezonans | **Mevcut hâl belgelendi** | Tepe değerde hafif doygunluk düşüşü, soğuk gölge, vinyet; yerleşim ve çarpışma aynı; dönüş ~3 sn. Hikâye tetikleyicisi değil, işlev elle çağrıldı |
| Oynanabilirlik | **Kısmi** | İki rota takılmadan tamamlandı (enjekte girdi) |
| Build | **Test edilmedi** | Paket / standalone yok |
| Performans | **Kısmi** | Aşağıda |

Performans (editör içi PIE, RTX 4060 Laptop, i7-13650HX, 31,6 GB; nokta başına 4 sn ortalama; `review/data/perf_*.txt`):
önce 27,9–42,4 fps, sonra 29,3–44,9 fps (aynı 15 nokta). Kamera değişikliği kare süresini ölçülebilir biçimde değiştirmedi. Bu sayılar paketlenmiş
oyun FPS'i değildir. Yeniden başlatmadan hemen sonraki ilk tur 3 fps ölçtü (editör arka plan kısıtlaması); o tur atıldı ve tekrarlandı.

## 8. Su parlaması: elenenler

Ev → göl ana görüşünde (A00, A02) su beyaza yanıyor; R02'den en büyük sapma bu. Her biri tek başına, bellekte denendi, aynı noktalardan
çekildi ve görünür kazanç olmadığı için **geri alındı**:

| Deneme | Değer | Sonuç |
|---|---|---|
| `MI_EX_Pond` Roughness | 0,32 → 0,06 | Parlak alan biraz daraldı, beyazlık aynı |
| Güneş hacimsel saçılım | 1,0 → 0,45 | Işık huzmeleri azaldı, su aynı |
| Güneş speküler ölçeği | 0,55 → 0,18 | Hafif kararma, alan aynı |
| `MI_EX_Pond` Murkiness | 4,5 → 1,2 | Fark yok |

Kalan açıklama: ana görüş alçak güneşe (24°) karşı bakıyor. Aynı su batı kıyısından (W01) koyu ve sakin okunuyor. Çözüm güneş yönü / yüksekliği
veya göl ile güneş arasındaki ağaç örtüsü; bu, alan kartında yazılı "ana görüşte arkadan ışık" kararını ve onaylı görünümü değiştirir.

## 9. Engellenen ve yapılmayanlar

- R06 gelmediği için rezonans yönü uygulanmadı.
- Ev kabuğu, arazi, bitki dağılımı, eski uygarlık izleri: bu turda dokunulmadı.
- Hareket düzeltmeleri (kol açıklığı, baş–boyun, dönüş ağırlığı, iniş): bu turda yapılmadı.
- Projenin kendi kuralındaki ChatGPTBridge dışa aktarımı ve GitHub yayını yapılmadı (dışarıya yayın; ayrıca çevre değişikliği yok).
- `r2g validate --release` bilerek geçmiyor: build, durum / yeniden başlatma ve varlık kontrolleri için kanıt yok.
- Yan bulgu: `unreal-engine-skills-for-claude-code` eklentisi yalnız OneDrive kopyasının yoluna kayıtlı; bu projede "failed to load" görünüyor.

## 10. Sıradaki en etkili düzeltme

Ana görüş için güneş yönü kararı (bölüm 8). Tek değişkenle hem su parlamasını hem güneşte beyaza yanan ten ve kumaşı ele alır ve R02'nin
yumuşak, nemli ışığına en büyük adımı atar. İkinci sıra: dar alanda saçın kadrajı kapatması.

## Yeniden üretim

```
bash Tools/R2G_20261123/tour2_r2g.sh <etiket> Tools/R2G_20261123/views_slice.txt   # sabit nokta kareleri
bash Tools/R2G_20261123/rec_r2g.sh <etiket>                                        # iki rota kaydı
bash Tools/R2G_20261123/res_r2g.sh <etiket>                                        # rezonans kareleri
python Tools/R2G_20261123/unreal_source_manifest.py && r2g.py freeze <kasa>        # kaynak özeti
```
Kilit sahibi `emb` (`Tools/SHME_V233_20261027/lock233.sh`). Derleme içeren yazma işinden sonra `Tools/Embodied_20261105/relaunch.sh`.
