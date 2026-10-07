# GD11 tur SS: göz, çene, burun, ense/boyun, kafa formu ve cilt k16 (R6 → SS4)

Tarih: 2026-10-07. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

## Kullanıcı isteği

R6 seçildi. Kalan farklardan şunlar istendi:

| No | Grup |
|---|---|
| 1 | göz bölgesi |
| 3 | çene açısı ve alt yanak |
| 4 | çene ucu (3/4'te) |
| 5 | burun |
| 7 | boyun |
| 8 | kafa oranı |
| 2 | cilt detayı — "karakteri çok yaşlı göstermeyecekse" |

**Taban:** R6 + k15 + M_SlightArch + e3g + S_Thin + h68e. R6'ya dokunulmadı.

## İki düzeltme: önceki raporumdaki iki tespit ölçünce yanlış çıktı

- **Burun (5):** "referansta burun kanatları daha geniş" demiştim. Referans kamerasında ölçünce tersi çıktı: bizim burun tabanı göz arası mesafeye göre yaklaşık %15 daha geniş. Bu yüzden kanatlar daraltıldı; buna karşılık burun ucu dolgunlaştırıldı ve burun sırtı hafifçe genişletildi.
- **Boyun (7):** önden boyun referanstan ince değil; referansınki biraz daha geniş bile. Kalın görünüm enseden geliyor. Kel profilde bizim ense ve baş arkası, kulağa göre referanstan 1,5–2 cm geride. Referansta kafatasının hemen altında ense içe kıvrılıyor, bizde düz iniyordu. Düzeltme ensede yapıldı; önden boyun daraltılmadı.

## Yapılanlar (`data/gen_ss.py`, `ops/`)

| Grup | İşlem |
|---|---|
| 1 göz | Üst kapak 1,5° aşağı, kapak örtüsü +1,2 / +0,7 mm: tur Y1'de kaldırılan ağırlığın yaklaşık %75'i geri geldi. Kaş dokusu 2 mm aşağı; kaş tipi (M_SlightArch) aynı. |
| 3 çene açısı | Çene köşesi çıkıntısı −3 mm, alt yanakta +1 mm yumuşak dolgu |
| 4 çene ucu | Çene yanları −2,5 mm, çene ucu −0,8 mm geri |
| 5 burun | Burun kanatları her yanda 1,4 mm dar, burun ucu her yanda 0,6 mm dolgun, burun sırtı 0,5 mm geniş |
| 7 ense/boyun | Ense kafatası altında 12 mm öne (boyun dikişinin üstünde sönümlü); boyun yanında hafif boyun kası (SCM) belirginliği |
| 8 kafa formu | Tepe 6 mm yukarı, baş arkası 7 mm kısa |
| 2 cilt k16 | k15'ten türetildi (k15 değişmedi). Yalnız bölgesel detay yoğunlukları arttı: alın %25, göz çevresi %20, burun-dudak bölgesi %30, kaş arası %15, genel %10. Ten rengi, gözenek ve kızarıklık aynı. |

Kafa formunda ilk deneme radyal işlemle yapılmıştı. Şakakta bir çentik ve tepede bir sırt bıraktı (SS1/SS2), bu yüzden geniş ve yumuşak iki hacim hareketine geçildi (SS3/SS4).

## Ölçümler

### Kafa formu (biçim karşılaştırması, ölçek fit edilmiş; − bizim dışarıda, + referans dışarıda)

| Bölge | R6 | SS4 |
|---|---|---|
| Arka (psi 0–25) | −1,0 ile −1,3 cm | −0,35 ile −0,66 cm |
| Tepe (psi 90–105) | +1,2 ile +1,9 cm | +0,9 ile +1,6 cm |

### Ense (kel profil; − bizim daha geride)

| z | R6 | SS4 |
|---|---|---|
| 154,5–156 | −2,4 / −2,2 cm | −2,0 / −1,6 cm |

### Rig'in koruduğu oran

Auto-rig bazı bölgeleri kendi şablonuna geri çekiyor. Ölçüm, rig'den önceki hedef ile rig'den sonraki mesh karşılaştırılarak yapıldı.

| Bölge | Hedef (en çok) | Rig sonrası (en çok) |
|---|---|---|
| Kafa formu | 4,6–6,5 mm | tamamı |
| Göz/kaş | 1,4 mm | 0,7 mm |
| Burun | 1,1 mm | 0,7 mm |
| Çene ucu | 2,1 mm | 0,7 mm |
| Ense | 9,1 mm | 2,6 mm |
| Çene açısı | 2,0 mm | 0,1 mm |

**Önemli:**
- Çene açısı değişikliği (3) rig'den sonra pratikte kayboldu. Bu bölge boyuna geçiş bölgesi ve auto-rig onu şablona geri çekiyor. Bu yol bu bölge için çalışmıyor.
- Ensenin de ancak yaklaşık üçte biri kaldı.

Önceki turlarda rig'in koruduğu oran: R6 %91, J5 %82, P3 %50 (çene altı). SS4 genelde %75.

## Gözlemlerim (karar senin)

- **Kafa formu ve profil:** en görünür değişiklik bu. Saçsız profilde tepe daha yüksek, arka daha kısa ve yuvarlak; referansın kafa biçimine belirgin şekilde yaklaştı. Saç kökleri yeni yüzeye oturdu; saçlı görünümde kopma ya da boşluk yok.
- **Göz:** kapak biraz daha ağır, kaş göze biraz daha yakın. Etki küçük; referansın ağır kapağına ve gözün çukurda duruşuna hâlâ uzak.
- **Burun:** kanatlar biraz daha dar, uç biraz daha dolgun. Önden küçük bir fark.
- **Çene ucu:** 3/4'te biraz daha az çıkık.
- **Cilt k16:** bu ışıkta k15'ten zor ayırt ediliyor. Yaşlı göstermiyor, ama referanstaki çizgileri de getirmiyor.

## Teknik

| Kontrol | Sonuç |
|---|---|
| ss4 auto-rig | taze editör, rig kapısıyla; yüz fit ort. 0,22 mm; en büyük sapma 6,5 mm, ensede (yukarıda); göz 0,000; 858 morph; DNA bağlı |
| ss4 rig pozları ve hareket kareleri | 27 + 27, temiz |
| Kilitli dosyalar | geri dönüş kaydıyla aynı (7); korunan adaylar 89/89 |
| Etiket koruması | `ss4` yeni etiket; TAG GUARD açık |
| LOD | TEST EDİLMEDİ |

## Board'lar

| Dosya | İçerik |
|---|---|
| `01_FACE.jpg` | ön ve 3/4: R6 / SS4 (k15) / SS4 + k16 / referans |
| `02_PROFILE_NECK.jpg` | çene profili, boyun 3/4, saçsız baş profili ve baş arkası |
| `03_WITH_HAIR.jpg` | h68e saçlı görünüm |
| `04_REF_CAMERA.jpg` | çözülmüş referans kameraları, %50 bindirme |
| `05_EYES_SKIN_REFCAM.jpg` | referans kamerasında göz ve cilt yakın plan |
| `06_CLAY_R6_SS4.jpg` | kil karşılaştırması |
| `07_TECH_RIG_ss4.jpg`, `08_TECH_MOTION_ss4.jpg` | rig pozları ve hareket kareleri |

Kaynaklar: `SourceAssets/Characters/GD11_EyeJawNoseNeckSkullSS_20261007`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
