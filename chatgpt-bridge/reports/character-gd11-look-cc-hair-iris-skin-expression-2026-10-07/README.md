# GD11 tur CC: genel görünüm — saç, iris, cilt parlaklığı, dinlenik ifade, alt yüz/ense, ışık

Tarih: 2026-10-07. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi.

Kullanıcı: "Hepsini yapalım." Önceki listedeki altı madde: saç, göz, cilt yüzeyi, ifade, alt yüz genişliği, karşılaştırma ışığı.

| | Yüz | Cilt | İris | Kaş | Saç |
|---|---|---|---|---|---|
| Önce | ss4 | k15 | e3g | m2 | h68e |
| Sonra | **ss4j** | **k17** | **e3m** | m2j | **h70c** |

Önceki hiçbir varlık değiştirilmedi; hepsi yeni kopyalar.

## Maddeler ve sonuçlar

| # | Ne yapıldı | Sonuç (dürüst) |
|---|---|---|
| 1 Saç | h70a/b/c: yüz çerçevesi telleri açıldı; kulak üstüne dökülen şakak örtüsü açıldı ve çoğaltıldı; omuza inen ön yan teller eklendi; renk koyulaştırıldı. h70c'de renk ortada, yan teller daha dışarıda ve yoğun. | **KISMEN.** Yan teller biraz daha dolu, renk referansa biraz yaklaştı. Ama referanstaki şakakları ve kulakları örten yan kütle oluşmadı: gevşek tel katmanı bunu taşımıyor, ana saç kütlesi hâlâ geriye topuza gidiyor. Bunu sağlamak için ana saç rehber çizgilerinin (şakak, kulak üstü, yan aileler) yeniden çizilmesi gerekiyor; bu ayrı bir saç turu. h70a/b fazla koyuydu. |
| 2 Göz | İris e3k (koyu kahve) ve **e3m (orta kahve)**. Değişen yalnız renk değerleri; sıcak-sarı çarpan kahveye çekildi. | e3k uzaktan siyah okunuyor, fazla koyu. **e3m** kahve ve seçilebilir; referansa yakın. Göz açıklığı için dinlenik ifadede kapak hafif iniyor (madde 4). |
| 3 Cilt | **k17** = k16 + parlaklık %30 az, pürüzlülük %12 fazla. Ton, çil ve kızarıklık aynı. | Alın ve burun parlaması azaldı; fark ölçülü. |
| 4 İfade | Dinlenik ifade animasyonu `AS_G11CC_RestFace` (rig kontrol eğrileri). rest A: kapak %12 aşağı, kaş hafif çatık %10, ağız köşeleri %18 aşağı, dudaklar %12 bastırılmış. rest B daha güçlü; ayrıca yalnız kapak seçeneği var. | Yüz biraz daha yorgun ve gergin, referansın ifadesine yakın. Şimdilik yalnız çekimlerde uygulanıyor. Oyunda kalıcı olması için karakterin yüz animasyonuna bir boşta-ifade katmanı eklenmesi gerekir (entegrasyon yapılmadı). |
| 5 Alt yüz ve ense | Yeni yöntem: auto-rig'in geri aldığı düzeltme, rig'den sonra doğrudan yüz mesh'inin bir **kopyasına** (ss4j) yazıldı: çene açısı −2,8 mm, alt yanak +0,9 mm, ense +6 mm. | **Teknik olarak BAŞARILI:** 858 ifade şekli ve DNA bağlantısı korundu, 27 rig pozu temiz. Görsel etki küçük, çünkü mesh bu bölgelerde seyrek (ense 101, çene açısı her yanda 21 köşe). Miktarlar istenirse artırılabilir. |
| 6 Işık | Yumuşak "sky" ışığı bu sahnede siyah çıktı; "interior" ışığı fazla karanlık. Karşılaştırmalar simetrik ön ışıkla yapıldı. | Referans gibi düz ve aydınlık bir çekim ışığı sahnede yok; eklenmesi ayrı bir iş. |

## Teknik

| Kontrol | Sonuç |
|---|---|
| ss4j | ss4 kopyası. LOD0 kaynak mesh'i GeometryScript ile güncellendi; morph sayısı 858 → 858; DNA kullanıcı verisi mevcut. |
| ss4j rig pozları | 27, temiz (`05_TECH_RIG_ss4j.jpg`) |
| ss4j + h70c hareket kareleri | 27, temiz; saç başla gidiyor (`08_TECH_MOTION_h70c.jpg`) |
| Kaş m2j | aynı eşleme tablosu, ss4j için yeniden bağlandı |
| Kilitli dosyalar | geri dönüş kaydıyla aynı (7); korunan adaylar 89/89 |
| LOD | TEST EDİLMEDİ; ss4j'de yalnız LOD0 güncellendi |
| Disk | C: 7 GB boş |

**Yeni varlıklar:**
- `SKM_G11RR_Face_ss4j` ve bağlamaları (`*_ss4jh48a`, `*_ss4jh68e`, `*_ss4jh70c`, kaş `EyebrowsCustom_m2j`);
- `MI_LK_Face_*_VT_gqk17`;
- `MI_G11CC_Eye{L,R}_e3k|e3m`;
- `AS_G11CC_RestFace`;
- saçlar `GR_LK_Hair_{Main,Loose}_h70a|h70b|h70c`.

## Board'lar

| Dosya | İçerik |
|---|---|
| `00_BEFORE_AFTER.jpg` | önce / sonra (e3k) / sonra (e3m) / e3m + dinlenik ifade / referans |
| `01_MATERIALS_SOFT.jpg` | cilt ve iris, interior ışık |
| `02_REST_EXPRESSION.jpg` | ifade seçenekleri |
| `03_HAIR.jpg` | h68e / h70a / h70c / referans |
| `04_JAW_NAPE_BAKE.jpg` | ss4 / ss4j |
| `05_TECH_RIG_ss4j.jpg` | rig pozları |
| `06_REF_CAMERA.jpg` | referans kameraları |
| `07_IRIS.jpg` | iris karşılaştırması |
| `08_TECH_MOTION_h70c.jpg` | hareket kareleri |

Kaynaklar: `SourceAssets/Characters/GD11_LookCC_20261007`.

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
