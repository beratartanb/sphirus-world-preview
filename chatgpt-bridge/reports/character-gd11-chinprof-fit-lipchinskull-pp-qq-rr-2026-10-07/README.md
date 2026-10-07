# GD11 turlar PP + QQ + RR: çene profili (P3), çok açılı referans fiti (Q8), dudak / çene ucu / baş arkası (RR5, R6)

Tarih: 2026-10-07. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

## Kullanıcı istekleri

1. **PP:** "Çene şekli referanstan oldukça farklı, benzetmeye çalış."
2. **QQ:** "Neden referansla birebir aynı çizgiye gelecek şekilde modelleme yapamıyorsun?" Seçim: **C**, yani bütün referanslar birlikte, çelişen yerlerde ortalama.
3. **RR:** "Hâlâ uymayan yerler var gibi. Çene ucunun, dudak üstünün ve altının hacmi yok gibi. Kafa arkası biraz ezik gibi. Bunları ve diğer şeyleri varsa düzelt; hem ön hem yan profilden."

**Taban:** O4 + k15 + M_SlightArch + e3g + S_Thin + h68e. Zincir: O4 → P3 → Q8 → RR5 / R6.

---

## ÖNEMLİ: tur RR sırasında eski bir adayın üzerine yazıldı (düzeltildi)

RR'nin ilk R5 rig'ine yanlışlıkla `r5` etiketi verildi. Bu etiket tur R'nin final adayına aitti (`SKM_G11RR_Face_r5` / `MHC_G11RR_R5`, 2026-10-06).

**Ne oldu:**
- Yeni rig, eski adayın MetaHuman karakter varlığının (`MHC_G11RR_R5`) ve DNA varlığının (`MHC/DNA/MHC_G11RR_R5_Head`) üzerine yazdı.
- Yüz mesh'inin geometrisi korundu, çünkü yeniden adlandırma adımı hata verdi. Ama mesh'e yeni DNA bağlandı.
- Korunan aday denetimleri (89/89 ve 7 kilitli dosya) bunu yakalamadı, çünkü tur R r5 korunan listede değil.

**Geri yükleme:**
1. Hatalı durum önce yedeklendi: `r5_collision_backup/`.
2. Tur R'nin kendi girdisi (`SourceAssets/Characters/GD11_FaceR_20261006/face/head_R5.npy`, md5 aynı) taze editörde yeniden rig edildi. Fit ortalaması 0,017 mm.
3. Orijinal DNA dosyası (SourceAssets yedeği, md5 `2d5f57fa…`) mesh'e yeniden bağlandı.
4. Doğrulama: 27 rig pozu temiz (`boards/16_PASSR_r5_RESTORED_RIG.jpg`).

**Geri yüklemeden sonra kalan farklar:**
- Karakter ve DNA varlıkları aynı girdiden yeniden üretildi; özdeş değiller ama işlevsel olarak eşdeğerler.
- Kendi oluşturduğum `Face/MHC_G11RR_R5_Head_DNA` yönlendiricisi yerinde kaldı. Silme izni verilmedi; silinip silinmeyeceği senin kararın.
- Gereksiz bir dışa aktarım (`MHC/Export/MHC_G11RR_R5_Head`, RR geometrisi) duruyor. Hiçbir şey onu kullanmıyor.
- r5 için iki ek bağlama oluştu: `r5h48a` (eski mesh üzerinde yeniden kuruldu) ve `h68e`.

**Önlem:** `gd11rr_cycle.sh` artık var olan bir etiketi reddediyor (TAG GUARD). RR adayı `rr5` etiketiyle yeniden rig edildi.

**Geçersiz çekimler:** `g11rsR5*`, `g11rr5Rig*` ve `g11rr5Mot*` yanlış mesh ile alındı. Bu raporda kullanılmadı.

---

## PP: çene profili (O4 → P3)

Önce çene bölgesindeki birikmiş düzenleme farkı yüzey üzerinde yumuşatıldı (low-pass). Ardından:

| İşlem | Değer |
|---|---|
| Menton yuvarlatma | −2,9 mm |
| Çene alt köşeleri | −2 mm |
| Çene altı eğimi | +2,2 mm yukarı |
| Çene açısı ve kenarı | +5,4 / +2,7 mm yukarı |
| Gevşetme | uygulandı |

Değişim (O4'e göre): çene ortalama 0,48 mm, en çok 3,1 mm; dudak en çok 2,0 mm; göz 0. Board'lar: `14_PP_O4_P3_PROFILE.jpg`, `15_PP_CLAY.jpg`.

## QQ: çok açılı silüet fiti (P3 → Q8)

Yeni araç `blender_g11rqq_fit.py` (kaynaklarda) aynı anda dört referansa fit yapıyor:
- önden ve 3/4'ten çözülmüş referans kameraları (kontur noktaları);
- kel profil;
- saçlı sağ profil.

Çözüm yöntemi: kısıtlardan gradyan adımı, ardından yüzey üzerinde Laplace yayılımı, sağ-sol simetri ve göz/kulak/ağız/boyun dondurma.

**Elenenler:**
- Q3: kafa bütününe fit. Tepe yükseldi, burun ve kapak bozuldu.
- Q4: baş arkasında maske sınırında bir sırt oluştu (`11_QQ_Q4_REJECTED.jpg`).
- Q5 ve Q6: geniş geçişle arka kafa düzleşti (`12_QQ_Q5Q6_REJECTED.jpg`). Neden: yüz noktalarıyla hizalanan bir fotoğrafta küçük bir ölçek hatası, yüzden yaklaşık 18 cm uzaktaki arka kafada 5 mm'den fazla sapma yaratıyor. Bu yüzden arka kafa mutlak konuma göre fit edilmemeli.

**Q8:** yalnız alt yüz.
- Kalan fark 3/4'te 0,54 → 0,45 cm. Önden 0,99 cm'de kaldı; nedeni saçla örtülü bir kontur noktası ve boyuna denk gelen bir çene noktası.
- Değişim: çene en çok 4,2 mm, dudak en çok 2,5 mm, göz 0.

## RR: dudak hacmi, çene ucu, baş arkası (Q8 → RR5 / R6)

### Teşhis (orta hat profili, `data/` ve araçlar)

- **Ön görünüm:** dudak yükseklikleri zaten referansla aynı.

  | Kırmızı dudak yüksekliği | Q8 | Referans |
  |---|---|---|
  | Üst dudak | 1,16 cm | 1,23 cm |
  | Alt dudak | 0,91 cm | 0,89 cm |

  Yani "hacim yok" okuması yükseklikten değil, derinlikten geliyor.
- **Alt yüz profili (Q8):** z 151,6 ile 154,8 arası tek düz bir eğim. Alt dudak çıkıntısı, dudak altı oluğu ve çene ucu çıkıntısı yoktu. Üst dudakta, sınır ile dudak ortası arasında bir çukur vardı (z 155,8).
- **Yan referanslarla karşılaştırma:**

  | Bölge | Kel profil | Saçlı profil |
  |---|---|---|
  | Alt dudak | 4 mm geride | 4,5–5 mm geride |
  | Üst dudak | 3 mm geride | eşit |
  | Çene ucu | yaklaşık 2 mm geride | — |

- **Baş arkası:** O4'teki tepe-arka kesimi profilde düz, eğimli bir düzlem bırakmıştı; "ezik" okuması buradan geliyor. Yeni araç `blender_g11rrr_skull.py` boyutu değil biçimi karşılaştırıyor (referans ölçeği fit ediliyor). Referans dışbükey, düzgün bir yay.

### İşlemler (`data/gen_ops.py`, `ops/`)

Orta hat profil hedefleri, yanlara yumuşak sönümlü uygulandı. Yalnız dış yüzey değişiyor; ağız içi değişmiyor.

| İşlem | RR5 | R6 |
|---|---|---|
| Alt dudak ileri (en çok) | 5,1 mm | 6,1 mm |
| Dudak altı oluğu | −1,7 mm | −1,8 mm |
| Çene ucu ileri | 2,4 mm | 2,6 mm |
| Menton yuvarlatma | 1,3 mm | 1,4 mm |
| Üst dudak çukuru dolgu | 2,5 mm (ikisinde aynı) | 2,5 mm |
| Baş arkası (radyal, dışbükey yay) | en çok 6,9 mm dolgu + tepe 4 mm | aynı |

Kapaklar, gözler ve yanaklar ≤ 0,25 mm.

### Gözlemlerim (karar senin)

- **Yan profil:** RR5 ve R6'da alt dudak dolu ve yuvarlak; dudak altında oluk ve yuvarlak bir çene ucu var. Profil referansa belirgin biçimde yaklaştı. R6 referansa en yakın, ama dudak dolgunluğu daha fazla. RR5 daha ölçülü.
- **Ön görünüm:** alt dudak biraz daha dolu; değişim önde küçük okunuyor.
- **Baş arkası:** düz düzlem kayboldu; profil tek, düzgün bir kubbe.

### Kalan farklar (dürüst durum)

- **Kafa oranı:** kel referansla biçim karşılaştırmasına göre referansın kafası daha yüksek, arkası kulağa daha yakın; bizim kafa daha uzun ve basık. Aynı ölçeğe getirildiğinde tepe 1,2–1,9 cm alçak, arka 1,0–1,3 cm uzun.

  Bunu tam düzeltmek için kafa formunun yeniden yapılması gerekir (tepeyi yaklaşık 1 cm yükseltip arkayı yaklaşık 1 cm kısaltmak); saç kökleri de etkilenir. Bu turda yalnız yuvarlaklık düzeltildi. İstersen ayrı bir turda yapılabilir.
- **Ön kontur:** fark, saçın örttüğü noktalar yüzünden ölçülemiyor; görsel karşılaştırma board'larda.

## Teknik

| Kontrol | Sonuç |
|---|---|
| p3, q8, r6 ve rr5 auto-rig | taze editör, rig kapısıyla; fit ort. 0,020–0,021 mm, maks 0,37 mm; göz 0,000; 858 morph; DNA bağlı |
| q8, r6 ve rr5 rig pozları ve hareket kareleri | 27 + 27 her biri |
| Kilitli dosyalar | geri dönüş kaydıyla aynı (7); korunan adaylar 89/89 |
| Disk | C: 0,5 GB'a düştü. Motor DDC önbelleğinden 14 + 9 GB temizlendi; proje ve kullanıcı klasörlerine dokunulmadı. |
| LOD | TEST EDİLMEDİ |

## Board'lar

| Dosya | İçerik |
|---|---|
| `01_LIPS_CHIN_PROFILE.jpg` | dudak ve çene ucu profili (dokulu + kil): Q8 / RR5 / R6 / referans |
| `02_FACE.jpg` | ön, 3/4 ve kil dudak görünümü |
| `03_HEAD_SHAPE.jpg` | baş arkası (saçsız), kil arka 3/4, kel referansla biçim karşılaştırması |
| `04_WITH_HAIR.jpg` | h68e saçlı görünüm |
| `05_REF_CAMERA.jpg` | çözülmüş referans kameraları, %50 bindirme |
| `06_CLAY_Q8_R3_R5_R6.jpg` | kil karşılaştırması |
| `06b_HEAT_R6.jpg` | değişim ısı haritası |
| `07`–`10` | r6 ve rr5: 27 rig pozu + 27 hareket karesi |
| `11`–`13` | QQ: Q4 ve Q5/Q6 (elendi), Q8 |
| `14`–`15` | PP: O4 / P3 profil ve kil |
| `16_PASSR_r5_RESTORED_RIG.jpg` | geri yüklenen tur R r5 adayının rig pozları |

Kaynaklar: `SourceAssets/Characters/GD11_ChinProfFitLipChinSkullPPQQRR_20261007`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
