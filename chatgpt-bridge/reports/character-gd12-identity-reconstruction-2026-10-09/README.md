# GD12: referansa dayalı yüz anatomisi ve kimlik rekonstrüksiyonu (Identity Master)

Tarih: 2026-10-09. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi. Unreal'daki hiçbir varlık değiştirilmedi.

| | |
|---|---|
| Yeni kaynak | `SourceAssets/Characters/GD12_IdentityMaster_20261009/GD12_IdentityMaster.blend` (düzenlenebilir, GD12_MASTER + salt-okunur F1H karşılaştırması + kameralar + iki ışık düzeni) |
| Dışa aktarım | `export/GD12_IdentityMaster.glb`, `export/GD12_IdentityMaster.obj` (yerel; büyük binary olduğu için GitHub'a yüklenmedi) |
| Taban | GD11 F1H (ww5bt1h başı) |
| Referanslar | `data/references.txt` (orijinal Tier A sayfası + copper 3/4; AI turnaround birincil kaynak olarak kullanılmadı) |

## 1. GD11'in tespit edilen ana anatomik eksikleri — PASS

Karşılaştırmalar orijinal referansların daha önce çözülmüş kameralarında yapıldı: ön ve yakın 3/4 kamera, aynı kadraj ve dokusuz clay. Kontur değil, yüz kimliği üzerinden bakıldığında GD11'in eksikleri şunlardı:

| Bölge | GD11 F1H | Referans |
|---|---|---|
| **Kaş ve üst orbita (en büyük kimlik farkı)** | Kaş yüksek, kaş–göz arası uzun, üst kapak açıkta; bakış "şaşkın" | Kaş alçak ve düz, dışta daha alçak; üst kapak yumuşak dokuyla örtülü (hooded); göz derinde ve sakin |
| **Göz kapağı açıklığı** | İrisin çevresinde beyaz görünüyor | Üst kapak irisin üstünü örtüyor |
| **Orta yüz** | Göz altı–elmacık yağ dokusu düz | Malar yağ ve elmacık daha dolgun, öne ve yana |
| **Dudaklar** | İnce; alt dudak düz | Dolgun; alt dudak belirgin biçimde öne ve aşağı dolgun; ağız köşeleri hafif aşağı |
| **Çene** | Dar çene yastığı, köşeli çene açısı | Daha geniş, yuvarlak çene yastığı; daha yumuşak çene açısı |

GD11 yalnız alt yanak ve çene altı dolgularıyla çalışmıştı; yukarıdaki kimlik formlarına hiç dokunmamıştı.

## 2. Gerçekten yeniden şekillendirilen hacimler — PARTIAL

**Yöntem: yüzeye yapışan sculpt fırçaları** (`tools/blender_gd12_sculpt.py`; Blender'daki Inflate, Grab, Smooth ve Relax karşılıkları):
- fırça merkezi yüzeydeki noktaya oturuyor;
- yumuşak düşüşlü;
- normal kapısıyla ağız içine ya da göz kapağının arkasına geçmiyor;
- simetrik.

**Kapak kenarı ayrı bir araçla indirildi** (`blender_gd12_lids.py`).

**Sanat değerlendirme turları:** her turdan sonra referans kameralarında karşılaştırıldı.

| Tur | Sonuç |
|---|---|
| G12a, G12b | Elipsoid hedefleme dudak yüzeyine oturmadı: dudakta ortalama 0,4 mm, görünmez |
| G12c | 1–3 mm, görsel değişim yok |
| G12d | Görünür değişim, ama elmacıkta yumrular ve kaşta sıkışma kıvrımları |
| G12e | Tek, geniş orta yüz hacmi; yumrular gitti |
| G12f–h | Kapak kenarı indirildi; kapak üstü kıvrımları düzleştirildi |
| G12i | İç kaş geri kaldırıldı (kızgın değil, referanstaki endişeli bakış) |
| G12j | Çene açısı ve dış yanak temizliği |
| Son temizlik | Dudak kenarı ve dudak–çene geçişi |

Ağız içi korumasının alt dudak birleşimini yanlışlıkla kilitlediği bulundu, düzeltildi ve tarif F1H'den baştan kuruldu (`tools/build_gd12.sh`). Son adımda katlanmış üçgenler giderildi (82 → 0) ve kapak örtüsündeki ikinci kıvrım düzleştirildi.

| Hacim | Ne yapıldı |
|---|---|
| Kaş yağ yastığı / supraorbital | aşağı ve öne indi (dışta daha çok); kaş sırtı hafif öne |
| Üst kapak örtüsü | kıvrım dokusu aşağı ve öne, oluk dolduruldu, sıkışma kıvrımları düzleştirildi |
| Kapak açıklığı | üst kapak kenarı 1,5 mm aşağı, alt kapak 0,5 mm yukarı |
| İç kaş / glabella | iç kaş geri kaldırıldı, glabella düzleştirildi |
| Orta yüz | tek geniş malar hacmi + zigoma genişliği; yumru yok |
| Burun | uç ve kanat yumuşak doku hacmi, kanat hafif genişledi |
| Dudaklar | üst dudak vermilyonu yukarı ve dolgun; alt dudak belirgin dolgun; köşeler hafif aşağı |
| Çene / çene açısı | çene yastığı ve yanları genişledi; çene açısı yumuşak ve hafif geniş |

**Değişmeyenler:**
- **Alın, şakak ve kafatası:** referansta saç çizgisi ve saç bu bölgeleri örttüğü için güvenilir bir fark ölçülemedi.
- **Burun sırtı ve uzunluğu.**
- **Çene projeksiyonu ve alt yüz yüksekliği:** bilinçli olarak korundu; çene uzatma daha önce üç kez reddedilmişti.

Bu yüzden "bütün yüz yeniden kuruldu" demek doğru olmaz.

## 3. Somut geometrik değişiklikler (F1H → GD12) — PASS

Ölçüm F1H yüzey normali yönünde; + = dışarı / dolgu. Vektör: yan / ön / yukarı, mm.

| Bölge | Normal ort. | En çok | Ortalama vektör | Anatomik amaç |
|---|---|---|---|---|
| Alın | 0 | 0 | — | değişmedi |
| Şakak | 0 | 0 | — | değişmedi |
| Kaş / supraorbital | +0,23 | 6,5 | 0,19 / 0,19 / **−1,00** | kaş aşağı ve öne |
| Üst kapak / örtü | **+0,95** | 6,5 | 0,04 / 0,20 / **−1,52** | kapak örtüsü, kenar aşağı |
| Alt kapak / göz altı | +0,20 | 1,0 | yukarı 0,26 | alt kapak hafif yukarı |
| Malar / zigoma | **+0,87** | 2,4 | **+0,55 / +0,61** / 0 | elmacık dolgunluğu, yana ve öne |
| Orta yanak | +0,39 | 2,3 | 0,25 / 0,28 / −0,08 | orta yüz geçişi |
| Alt yanak / jowl | +0,16 | 1,6 | | yumuşak alt yanak |
| Burun-dudak | +0,08 | 2,3 | | korundu |
| Burun ucu / kanat | +0,24 | 2,5 | 0,10 / 0,15 | uç ve kanat hacmi |
| Üst dudak | +0,19 | 3,8 | yukarı 0,13 | vermilyon dolgunluğu |
| **Alt dudak** | **+1,13** | **4,9** | 0,13 / **0,85 / −1,01** | dolgun alt dudak |
| Çene | +0,42 | 2,1 | **+0,40 yana** | daha geniş çene yastığı |
| Çene gövdesi / açısı | +0,15 | 1,4 | | yumuşak, hafif geniş açı |
| Çene altı | 0 | 0 | — | değişmedi |
| **Toplam** | | **6,5** | | 5666 vertex hareket etti, ortalama 0,87 mm |

- **Deformasyon haritası:** `C1_DEFORMASYON_HARITASI.jpg`. Kaşın aşağı inişi büyük ölçüde yüzeye teğet olduğu için normal yönlü haritada zayıf görünüyor; vektör sütununa bakın.
- **Katlanma:** keskin kıvrım 42 (F1H 43).
- **Ölçüm belirsizliği:**
  - Ön referansta yüz yaklaşık 100 px; ×4 büyütülmüş kırpımla çalışıldı. 3/4 referansta yüz yaklaşık 250 px.
  - Kameralar önceki geçişlerde çözüldü; perspektif ve lens varsayımına bağlı. Görüntülerden mm düzeyinde 3D ölçü çıkarılamaz.
  - İzleyiciyle göz/dudak yeniden ölçümü yapılamadı: Unreal editörü bu çalışmanın dışında kapanmıştı (log 04:57'de hatasız bitiyor). Bu ölçüm **NOT TESTED**.

## 4. Referans benzerliğinde neler iyileşti — PARTIAL

`A1`, `B1`, `B3` board'larında aynı kamera ve ışıkta görülenler:
- **Göz bölgesi:** kaş daha alçak ve göze yakın, dış kaş aşağıda, iç kaş hafif yukarıda; üst kapak örtülü, iris üstü kapalı. Referanstaki ağır kapaklı, sakin-endişeli bakışa belirgin biçimde yaklaştı. En büyük kazanım bu.
- **Dudaklar:** alt dudak referanstaki gibi dolgun, ağız köşeleri hafif aşağı.
- **Orta yüz:** elmacık–göz altı dolgun ve yumuşak; F1H'deki düz orta yüz okuması azaldı.
- **Çene:** daha geniş ve yuvarlak çene yastığı.

Değişim gözle görülür, fakat orta düzeyde. Clay'de F1H ile GD12 aynı kişinin iki versiyonu gibi duruyor, yeni bir yüz gibi değil.

## 5. Hâlâ yeterince benzemeyen bölgeler — FAIL / PARTIAL

| Bölge | Durum |
|---|---|
| Burun ucu ve burun biçimi | Referansta daha iri, yuvarlak ve hafif sarkık uç. Yalnız hacim eklendi, biçim yeniden kurulmadı. |
| Alt yüz oranı ve çene–dudak ilişkisi | Referansta dudak daha dolgun ve öne, çene yastığı daha etli. Kısmen yaklaştı. |
| Kapak örtüsü | İç tarafta zayıf bir ikinci kıvrım izi kaldı; elle sculpt gerekiyor. |
| Alın, şakak, kafatası, profil | Değerlendirildi, değiştirilmedi. |
| Ten | Benzerlik algısının büyük kısmı ten dokusu, çil, kaş ve saçtan geliyor. Bunlar bu görevin dışında kaldı. |

Genel benzerlik F1H'den daha iyi (özellikle göz ve dudak), fakat "referansın kendisi" düzeyinde değil. **Bu yüzden genel kimlik hedefi PARTIAL, PASS değil.**

## 6. Eski karakter ve dosyalar korundu mu — PASS

| Kontrol | Sonuç |
|---|---|
| Unreal varlıkları | hiçbiri değiştirilmedi; üretim ve oyun karakteri aynı |
| Korunan adaylar | 89/89 |
| Kilitli dosyalar | geri dönüş kaydıyla aynı (7/7) |
| Saç, kıyafet, vücut, animasyon | h74b / h75a / h75c saçları, Henley, Chaos şort, B2 vücut, animasyon ve kamera dokunulmadı |
| Saç yeniden hizalama | gerekmiyor: kafatası değişmedi (kalan iş listesinde not edildi) |

## 7. Yeni Blender kaynak modeli kullanılabilir mi — PASS

- `.blend` yeniden açılıp doğrulandı:
  - GD12_Head 33 845 vertex, düzenlenebilir;
  - materyaller M_Clay, M_Skin, M_Eye;
  - 7 kamera (2 çözülmüş referans + 5 inceleme);
  - LIGHTS_A ve LIGHTS_B;
  - F1H salt-okunur karşılaştırma koleksiyonu.
- GLB geri yüklenip doğrulandı; OBJ de yazıldı.
- Tarif baştan üretilebilir: `tools/build_gd12.sh` + `data/*.json`.
- MetaHuman topolojisi korundu. Büyük değişiklikleri sınırlayan şey topoloji değildi, aynı topoloji üzerinde sculpt edilebildi. Bu yüzden ayrı bir remesh yapılmadı ve sonraki rig aktarımı kolay kaldı.

## 8. Rig ve oyun entegrasyonu için gerekenler — NOT TESTED

Ayrıntı: `data/remaining_work.txt`. Bunlar yalnız onaydan sonra:
1. Aynı DNA vertex sırası korunduğu için doğrudan fark olarak yeni bir SKM kopyasına bake (858 morph ve DNA korunur).
2. Kapak açıklığı değişti: göz kırpma ve kapak morph'ları, kirpik ve göz kenarı mesh'leri UE'de kontrol edilmeli; gerekirse düzeltici morph.
3. Kaş, kirpik ve saç groom'larını yeni SKM'ye yeniden bağlama; gerçek kaş groom'unu alçalan kaşa yerleştirme.
4. Rig pozları, hareket kareleri, LOD, checkpoint, korunan varlık doğrulaması.

## Board'lar

| Dosya | İçerik |
|---|---|
| `A1_CLAY_REFERANS_KAMERALARI.jpg` | A: orijinal referans / F1H / GD12, çözülmüş ön ve 3/4 kamerada clay; A ön ışık, B üst-yan ışık |
| `A2_CLAY_5_ACI.jpg` | A: 5 açıda clay, F1H / GD12, iki ışık |
| `B1_KIMLIK_TEN.jpg` | B: basit ten, geçici kaş, saçsız: referans / F1H / GD12 (+ copper 3/4) |
| `B2_KIMLIK_5_ACI.jpg` | B: 5 açıda ten, F1H / GD12 |
| `B3_YAKIN_PLANLAR.jpg` | göz–kaş (ön, 3/4), orta yüz, ağız–çene yakın planları |
| `C1_DEFORMASYON_HARITASI.jpg` | F1H → GD12 gerçek mesh farkı |

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
