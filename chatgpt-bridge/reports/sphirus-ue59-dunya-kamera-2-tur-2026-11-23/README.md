# Sphirus World — 2. tur: referansların gerçek dünyaya uygulanması (2026-11-23)

Proje: `sphirus_UE59`, UE 5.9.0. Harita: `L_GR_SphirusHouse` (+ `L_GR_CurrentHouseContent`).
Durum: **kısmi**. Işık / su / iç ton, cephe dili, arka çalışma bahçesi ve eşik kamerası uygulandı, kaydedildi, yeniden açılmış projede doğrulandı.
Ev kabuğu büyütülmedi, iç bölmeler ve oda düzenleri değişmedi, orman kompozisyonuna dokunulmadı. Kullanıcı kabulü yazılmadı.
Hareket sistemi: dokunulmadı (bölüm 8'de dosya özetleriyle gösterildi).

Kanıt klasörü: `review/pass2/`. Yayın notu: bu paket herkese açık depoya konduğu için ham referans görselleri ve yerel kullanıcı yolları içermez; görsellerin tümü oyun karesidir. Yürüyüş kaydı editör penceresinden alınmıştır. Betikler `scripts/`, ölçüm çıktıları `data/` altındadır. Tüm kareler gerçek oyun kamerasından, PIE içinde, 1600×900, sabit noktalardan alındı.

## 1. Gerçekten değişen Unreal varlıkları

| Varlık | Değişiklik | Geri dönüş yedeği (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/`) |
|---|---|---|
| `L_GR_SphirusHouse.umap` | Güneş, gök ışığı, su aydınlatma kanalı, yeni iç mekân pozlama hacmi `EX_Look_PPV_Interior`, 40 yeni aktör (`R2G_Rear_*`, `R2G_Rug_Entry`) | `r2g2_light_100955` (tur öncesi hâl), `r2g2_house_110900`, `r2g2_house2_112009`, `r2g2_house3_113954` (ara hâller) |
| `L_GR_CurrentHouseContent.umap` | 13 iç lamba (sıcaklık, şiddet, dolaylı çarpan), 5 zemin kat duvarı ve 2 alınlıkta malzeme atamaları | `r2g2_light_100955` (tur öncesi hâl), `r2g2_facade_110937` |
| `AC_Sph_Camera.uasset` | Yeni değişken `HeadXTight` (0,20) ve yan kaydırma satırında tek düğüm değişikliği | `r2g2_camtight_105102` |
| `MI_GL_GrassMedium01, GrassShort01, GrassSmallSparse01, GrassLarge01–03, GroundCover01–04_FO` (10 malzeme örneği) | Üç renk parametresinde doygunluk −%45, parlaklık ×0,85 | `r2g2_grass_111755`; başlangıç değerleri `Tools/R2G2_20261123/grass_base.json` |

Yeni ağ, doku ya da malzeme içe aktarılmadı; yeni aktörlerin tümü haritada zaten bulunan aktörlerin kopyasıdır.
Geri alma: editör kapalıyken ilgili yedek klasöründeki dosyayı `Content/` altındaki yerine kopyalamak.

## 2. Evin önceki ve yeni mimarisi

Ölçüm (çarpışma izlemesiyle çıkarılan plan, `08_plan_ground_z150cm.png`):

- Dış kabuk 15,2 × 11,4 m, iki kat; ön cephede boydan boya 2,5 m derinlikte veranda. Zemin kat tavanı 3,1 m.
- Batı şeridi (6,2 m): kuzeybatıda atölye (6,2 × 3,7 m), ortada merdiven, güneyde WC / depo.
- Doğu bölümü (8,4 m): kuzeyde mutfak, ortada kiler kutusu, güneyde şömineli oturma (8,4 × 6,7 m).
- Ön kapı ile arka kapı aynı eksende; aradaki 2,2–2,8 m genişlikte hol her odaya açılıyor.

Karar: **kabuk büyütülmedi.** Ölçülen kabuk yeni ön cephe referansındaki evden küçük değil ve istenen oda düzeni (KB atölye, KD mutfak, GD şömine, B merdiven, ortada hol) zaten yerinde. Darlık izlenimi ışık, kamera ve cephe dilinden geliyordu. Duvar / çatı değişikliği yapılmadı.

Yapılan mimari değişiklik cephe dilidir (`02_exterior_*.jpg`):

- Önce: göl cephesi kireç sıva, arka ve iki yan zemin kat duvarı gri tahta kaplama, üst kat sıva. Referansın tersi ve ön cepheyle tutarsız.
- Sonra: dört cephede zemin kat aynı kireç sıva + meşe; tahta kaplama iki alınlığa taşındı (altta sıva, üstte ahşap).

Yapılmayan: iç bölmelerde yeni açıklık, hol ile oturma alanı arasında ahşap çerçeve, üst kat hacmi, çatı, veranda döşemesi ve dikmeleri.

## 3. İç mekân — işlev alanlarına göre

`01_fixed_points_0.jpg`, `01_fixed_points_1.jpg`:

| Alan | Değişen | Değişmeyen |
|---|---|---|
| Giriş holü | Pozlama ve ton; kapı ekseninde 3,1 × 1,2 m yolluk; eşikte karakter sola kaydı, arka kapı ve aplik artık saçın arkasında değil | Eşya düzeni |
| Şömineli oturma | Turuncu baskı azaldı, sıva krem okunuyor, pencere ışığı ana ışık oldu | Mobilya yerleşimi |
| Mutfak / çay | Aynı ton düzeltmesi | Tezgâh, masa, eşyalar |
| Maske atölyesi | Aynı ton düzeltmesi | Tezgâh, maskeler, aletler |
| Merdiven | Aynı ton düzeltmesi | — |

Turuncu baskının nedeni ölçüldü: 3200–3500 K lambalar dolaylı ışık çarpanı 2 ile baskındı; güneş adaylarının hiçbiri iç tonu değiştirmedi.
Uygulanan: 13 lamba 3600 K, şiddet ×0,8, dolaylı 1,3; yalnız ev içini kapsayan hacimde pozlama +0,35 ve beyaz dengesi 5300 K. Şömine ışığı (2300 K) aynı.

Yaşanmışlık düzeni (atölyede üretim aşamaları, mutfak ilişkileri, oturma düzeni) bu turda **yeniden yazılmadı**.

## 4. Ön cephe ve arka bahçe

Ön cephe (`02_exterior_1.jpg`, E5 / E7): yalnız ışık değişti; veranda, döşeme, dikmeler, saksılar aynı.

Arka bahçe (`09_rear_garden_0.jpg`, `02_exterior_0.jpg`):

- Arka kapının mutfak tarafına duvara yaslı odunluk (`R2G_Rear_LogStore`), içinde 29 parça yarılmış odun; önceki gevşek kütük yığını artık sundurmanın altında.
- Kapı yanına alet askısı (`R2G_Rear_DoorTools`).
- Kapıdan odun kesme alanına duvar boyunca 8 basamak taşı (`R2G_Rear_Stone_0…7`); son ikisi mevcut kütük yığınının kuzeyinden dolanıyor.
- Görev istasyonları, kesme kütüğü, çit ve patika girişi yerinde bırakıldı.

Bilinen kusurlar: sundurma çatısı paketin oluklu sacı (referansta ahşap padavra); kapı üstündeki yuvarlak lamba modern duruyor; yeni sıva yakından fazla temiz, arka cepheye özgü nem / sıçrama izi ayarlanmadı.

## 5. Ev – göl – orman güzergâhı

`01_fixed_points_0.jpg` (P01, P02), `01_fixed_points_1.jpg` / `_2.jpg` (P09, P10), `07_ground_green.jpg`:

- Gölgeler yumuşadı, güneşli yamalar daha az patlıyor (bölüm 7).
- Zemin örtüsünün limon yeşili, proje sahipliğindeki 10 malzeme örneğinde soluklaştırıldı. Fark küçük ama doğru yönde.

Yapılmayan: arazi biçimi, patika yüzeyi, ağaç / çalı / eğrelti dağılımı, kaya kümeleri, eski uygarlık izleri. Yonca ve yosun örtüsü (satıcı malzemeleri) hâlâ parlak.

## 6. Kamera — dar alan

Ölçüm (`AC_Sph_Camera` iç durumu, 10 nokta): eşiklerde ve duvar arasında kol 98 cm'ye iniyor ama baş her yerde kadrajın 0,30'unda tutuluyordu; kafa ve saç orta-solu kapatıyordu.
Değişiklik: baş konumu açıklığa göre harmanlanıyor (`HeadXTight` 0,20 dar → `HeadX` 0,30 açık); yan kaydırma yan duvara 28 cm sınırını koruyor.

| Nokta | Baş konumu önce | sonra |
|---|---|---|
| Ön kapı eşiği | 0,30 | 0,21 |
| Arka kapı eşiği | 0,30 | 0,22 |
| Hol açıklığı | 0,31 | 0,24 |
| Açık oda | 0,30 | 0,30 |
| Dış R04 kadrajı (kıyı) | 0,30 | 0,30 |

Kanıt: `03_camera_tight_0.jpg`. Yürüyüş kaydında (bölüm 8) kapı geçişlerinde ani sıçrama görmedim; kaydı gerçek hızda izlemedim, 1 fps kareleri inceledim.

Çözülmeyen: 1,1 × 1,2 m kiler gibi ceplerde kamera başa 25–55 cm yaklaşıyor ve saç kadrajı kaplıyor. Bunun sağlam çözümü kamera yaklaşınca karakteri soldurmak; karakter görünürlüğüne dokunduğu ve kör eklenemeyeceği için yapılmadı.
Not: iki test noktasında (atölye köşesi, WC eşiği) ışınlanınca görünen beden kapsülden yüksekte çizildi. Hareket kapsamında olduğu için incelemedim.

## 7. Işık ve su

Gölün beyaza patlamasının nedeni ölçüldü (`05_glare_cause.jpg`): güneşin su üzerindeki doğrudan specular yansıması. Güneş specular'ı kapatılınca tamamen kayboluyor; sis saçılımı kapatılınca büyüyor. Önceki 0,55 → 0,18 denemesi fark göstermemişti çünkü sinyal patlama sınırının çok üstündeydi.

Çözüm: su yüzeyi yalnız aydınlatma kanalı 1'de; güneş (kanal 0) suyu doğrudan aydınlatmıyor. Yansımalar ve gök ışığı aynı. `04_water_0.jpg`: iki göl bakışında beyaz alan yok, su koyu ve sakin, karşı kıyı gövdeleri yansıyor. Güneş pırıltısı da tamamen gitti; isterseniz ikinci bir düşük ışıkla sınırlı bir parıltı eklenebilir.

Güneş adayları 10 noktada karşılaştırıldı (`06_sun_candidates_*.jpg`):

| Aday | Sonuç |
|---|---|
| Aynı yön, 36° | Parlama yok; veranda altı duvar gölgede düz |
| Güneydoğudan, 38° | Kıyı ve patikada daha iyi derinlik; gölden bakışta cephe karanlık |
| **Seçilen:** aynı yön, 30°, şiddet 900 (1250'den), kaynak açısı 2,5° (1,4'ten), gök ışığı 2,8 (1,3'ten) | Onaylı arkadan aydınlatma yönü korundu, gölgeler yumuşadı |

## 8. Kaydedilmiş proje doğrulaması

- Tüm yazmalar projenin kapılı yolundan geçti: doğrulanmış yedek, tek kilit sahibi, yazma günlüğü.
- Editör dört kez temiz yeniden başlatıldı; son kayıttan sonraki açılışta değerler diskten geri okundu (`data/verify_saved.txt`): güneş −30 / −60, gök 2,8, su kanalı, lambalar, iç hacim, `HeadXTight` 0,20, 40 yeni aktör, iç haritadaki 559 ağ referansı tam, kirli paket yok.
- Geri okuma üç hatamı yakaladı ve düzeltildi: cephe malzemesi ilk yazmada alt haritaya işlenmemişti; alet askısı havadaydı; bir basamak taşı kütük yığınının üstündeydi.
- Sonra kareleri: 37 sabit nokta, kaydedilmiş ve yeniden açılmış projeden. Son taş düzeltmesi bu turdan sonra kaydedildiği için arka bahçenin 6 karesi son hâlden yeniden alındı (`09_rear_garden_0.jpg`).
- Oynanabilirlik: enjekte girdili tek yürüyüş kaydı (ön bahçe → veranda → ön kapı → hol → atölye → arka kapı → taşlar → odun alanı), 27 s, takılma yok (`video/walk_front_hall_workshop_rear_yard.mp4`, `10_walk_frames.jpg`). İlk denemede karakter kütük yığınına takıldı; taşlar taşındı ve kayıt tekrarlandı. Kayıt editör penceresinden alınıyor, arayüz görünüyor.
- Kullanıcı kaydı `SFSaveSlot.sav`: her çalıştırmada aynı özet (`3d81ab9d…`).
- Hareket varlıkları (`BP_HybridA_Player`, `BP_Sph_GASPCharacter`, `ABP_Sph_GASP`, `ABP_Sph_Body_GASP`, `RTG_Sph_UEFN_to_MH`, `AC_Sph_Motion`): ilk turda kaydedilen sha256 ile bayt bayt aynı.
- Performans (editör içi PIE, RTX 4060 Laptop): 19 ortak noktada önce 28,9–39,7 fps (ortalama 33,5), sonra 30,3–42,5 (ortalama 35,9); farklı editör oturumları. Arka bahçe bakışlarında 44,0 → 38,4 ve 42,0 → 39,6; yeni 38 aktörün payı ayrıştırılmadı.

Yapılmayan doğrulama: insan eliyle oynanış, üst kat ve merdiven yürüyüşü, görev istasyonlarının çalıştırılması, bağımsız (standalone) derleme, GPU dökümü, ChatGPTBridge dışa aktarımı ve yayını.

## 9. Açık kalan görsel kusurlar ve nedenleri

1. **Ev hâlâ aynı ev.** Kabuk yeterli ölçüldüğü için büyütülmedi; referanstaki uzun-alçak siluet için çatı ve veranda yeniden modellenmeli. Mimari ağlar haritaya özel, modüler değil; bu bir Blender işi.
2. **İç mekân sanat yönetimi yapılmadı.** Yalnız ışık ve yolluk. Atölye, mutfak ve oturma alanı düzenleri bir sonraki en etkili iş.
3. **Hol ile oturma alanı tek hacim okunuyor.** Referanstaki ahşap çerçeveli geçiş için yeni dikme / kiriş ağları gerekiyor.
4. **Orman kompozisyonu değişmedi.** Arazi, bitki katmanları ve görüş kümeleri bu turda ele alınmadı.
5. **Arka sıva fazla temiz**, sundurma çatısı sac, kapı lambası modern.
6. **Kiler gibi ceplerde kamera saça yapışıyor** (bölüm 6).
7. **Saçta iç ışık altında benekli parlama** görülüyor; karakter görünümü kapsamı, dokunulmadı.
8. **Oturum içi yeniden yükleme tuzağı:** alt harita doğrudan kaydedildikten sonra aynı oturumda harita yeniden yüklenince 559 aktörün ağı boş göründü; dosya sağlamdı, temiz açılışta düzeldi. Beceri notuna yazıldı.

## Referans yetkileri (güncel)

`case.json` güncellendi: `ref-007` → R02-HOUSE, `ref-006` → R02-GARDEN, `ref-008` → R03 (yeni iç mekân), `ref-003` geçersiz kılındı, `ref-002` yalnız dünya kompozisyonu, R01 / R05 yalnız karakter kimliği.

## Araçlar

`Tools/R2G2_20261123/`: `apply_light.py`, `apply_facade.py`, `apply_dress.py`, `apply_grass.py` (tekrarlanabilir değişiklik kümeleri), `m_camtight_mcp.py`, `mapwrite.sh`, `cand.sh`, `cmp.py`, `trace_plan.py`, `verify_*.py`, `views_after.txt`, `rec_walk.sh`.
