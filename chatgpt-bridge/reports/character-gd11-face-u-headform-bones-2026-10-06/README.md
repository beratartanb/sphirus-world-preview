# GD11 tur U: kafa formu ve kemik yapısı, ölçüme dayalı (s5 → t6)

Tarih: 2026-10-06. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi. Önceki adaylar değiştirilmedi.

## Yöntem: önce teşhis

Modeli referans fotoğrafların çözülmüş kameralarından render edip referansın üstüne yarı saydam bindirdim. Silüetini de çizdim (board 01). Ayrıca "fark kemikten mi, baş duruşundan mı geliyor?" sorusunu test ettim: kafayı göz merkezi çevresinde −6° ile +8° arasında katı olarak eğip referans konturlarını yeniden ölçtüm (`data/pitch_*.json`).

| Bulgu | Sonuç |
|---|---|
| Göz, burun, ağız, elmacık genişliği, alın | Referansla 1–3 mm içinde örtüşüyor (önden ve 3/4) |
| Çene ucu ve çene alt kenarı | Referansta 0,7–1,3 cm daha aşağıda. Baş eğimiyle açıklanmıyor (her açıda fark kalıyor), yani gerçek bir biçim farkı. Referansta ağız–çene mesafesi yaklaşık 1 cm daha uzun. |
| **Kafa formu (3/4)** | En büyük fark burada. Referansın kafatası arkaya ve tepe-arkaya doğru çok daha dolu ve yuvarlak. Bizimki arkada düz, tepe-arka köşesi keskin (midline profil: ense arkası 2,7 cm, yuvarlanmadan tepeye dik geçiş). |
| Çene açısı ve çene–boyun çizgisi | Referansta kulak altında belirgin bir çene açısı ve net bir çene–boyun çizgisi var. Bizde yumuşak ve boyna karışıyor. |

**Bilinçli sınır.** Çene ucunu uzatmak ve ağız–çene mesafesini değiştirmek iki kez reddedildiği (K5 ve O kararları) için yapılmadı. Bu fark açık kalıyor.

## Yapılan (t6 = s5 + `data/T6.json`)

| Bölge | Yöntem | Değer |
|---|---|---|
| Kafatası arka ve tepe-arka (posterior vault, oksiput) | Yeni `radial` işlemi: kafatası merkezinden dışa doğru, sagital açıya göre yumuşak genlik eğrisi (arka 1,2 mm → tepe-arka 6 mm → tepe 0,4 mm), yanlara kosinüs azalması. Yüz, alın, kulak ve ense maskeli. | en çok 6 mm |
| Çene açısı (gonion) | aşağı ve hafif dışa | 2,6 mm |
| Çene gövdesi alt kenarı | aşağı | 1,2 mm |
| Çene altı (submental) | yukarı-geri, çene–boyun çizgisini netleştirir | 2,1 mm |

Önce noktasal kaydırmalarla denedim (t1–t5): kafa arkasında basamak ve tepe-arkada tümsek oluştu, reddettim. Radyal yöntem bunu tek, sürekli bir eğriye çevirdi (board 03).

Midline arka profil s5 → t6:
- z 165: −5,81 → −6,10
- z 169: −4,39 → −5,19
- z 170: −3,62 → −4,36
- z 171: −2,72 → −3,43 cm

**Değişmeyen:** yüz ön yüzeyi (y>6, z>153,5: 0,03 mm), alın, dudaklar, çene ucu (önü ve alt noktası), kulak kepçesi (0,0 mm), boyun dikişi, kafatası genişliği (s5'teki daralma korundu), tepe yüksekliği.

## Teknik (board 05)

| Kontrol | Sonuç |
|---|---|
| t6 auto-rig | taze editör, rig sonucu kontrolüyle; fit ort. 0,017 / maks 0,35 mm; 858 morph; DNA bağlı |
| 27 rig pozu + hareket (t6 + k13 + h66b) | temiz; saç büyüyen kafa arkasıyla birlikte hareket ediyor, kök kopması ve kesişme yok |
| Kilitli dosyalar | m2, M DNA, M_SlightArch ve bağlamaları, h51a geri dönüş kaydıyla aynı; korunan eski adaylar 89/89; r5 yüzü ve h65b değişmedi |
| LOD | TEST EDİLMEDİ |

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| KAFA FORMU (arka ve tepe-arka dolgunluğu) | BAŞARILI: saçsız profil ve arka 3/4'te belirgin. Saçla etkisi daha küçük; topuz ve saç hacmi bu farkı kısmen örtüyor. |
| ÇENE AÇISI / ÇENE–BOYUN ÇİZGİSİ | KISMEN (daha net, abartısız) |
| ÇENE UCU UZUNLUĞU | TEST EDİLMEDİ: bilinçli olarak dokunulmadı, kullanıcı kararı gerekiyor |
| YÜZ ORANLARI (göz–burun–ağız–elmacık) | ölçümde referansla örtüşüyor |
| KİMLİK KORUNUMU | BAŞARILI |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (LOD TEST EDİLMEDİ) |

## Board'lar

`boards/01_DIAGNOSIS.jpg` referans kameralarında bindirme ve silüet · `02_REF_CAMERA_AND_HEADFORM.jpg` s5 ile t6 karşılaştırması: referans kamerasıyla, saçlı ve saçsız profil / arka 3/4 · `03_CLAY.jpg` kil s5 ile t6 · `04_FINAL.jpg` aynı oturumda s5 ile t6 · `05_TECH.jpg` rig pozları + hareket.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
