# GD11 saç turu Q: önden tepe dolgunluğu + enseden topuza uzun saç + yeni altı açılı referansın dağınık topuzu (h51a → h64a)

Tarih: 2026-10-06. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi. Yeni face auto-rig, kurulum ya da skill yok.

Hedef: kullanıcının iki geri bildirimi (önden tepe basık, topuz altında uzun ense saçı yok). Turun ortasında gönderilen altı açılı referans da (`reference/REF_6VIEW_user_20261006.png`) hedefe eklendi: ortadan ayrılmış, yanlarda dolu, arkada büyük dağınık topuz, yüz yanlarında, kulak arkasında ve ensede omuza inen dalgalı teller.

## Sabit paket ve yeni aday

| Parça | Varlık | Durum |
|---|---|---|
| Yüz / DNA | `SKM_G11RM_Face_m2` / `MHC_G11RM_M2_Head` | değişmedi (SHA1 = geri dönüş kaydı, `data/locked_package_hashes_after.json`) |
| Kaş / kirpik | `GR_GD_Eyebrows_M_SlightArch`, `GR_GD_Eyelashes_S_Thin`, M bağlamaları | değişmedi |
| Başlangıç h51a ve önceki saçlar (h48a–h56a) | O / P klasörleri | değişmedi, silinmedi |
| **Yeni saç h64a** | `GD11_HairQ_20261006/Hair/GR_LK_Hair_{Main,Loose}_h64a` + `GB_G11RQ_Hair{Main,Loose}_m2h64a` (hedef m2) | yeni, ayrı aday |

Ara adaylar h57a–h63a aynı klasörde saklandı (`SourceAssets/Characters/GD11_HairQ_20261006`). S (h51a) ve X (h64a) çekimleri aynı editör oturumunda, aynı ışık rig'leriyle ve kurulumda sıfırlanan simülasyonla (time=0) yapıldı. Kompozisyon editörden okundu (`prov/g11rqS.json`, `prov/g11rqX.json`).

## Sorulara doğrudan cevaplar

| Soru | Cevap |
|---|---|
| Önden basık görünümün ana sebebi neydi? | **Hacim vardı ama yanlış yerdeydi.** h56a'da ön kilitler köklerinden hemen yanlara inip kafatasına yapışıyordu. Önden bakınca ayrımın iki yanında saç kafatasının yalnız 0,8–1,4 cm üstündeydi (h51a'da 2,2–2,7 cm). Taç kilitleri de yanlara yönlendirildiği için tepe arkası inceldi. |
| Tepe hacmi gerçekten nerede değişti? | Ayrımın hemen yanında, ön-tepede. Ayrıma yakın ön kilitlere kökten 1–2 cm uzakta yükselen bir ara nokta eklendi (B ön-tepe, A ön kenar), ayrıma yakın taç kilitleri eski düz-geri rotasına bırakıldı, ayrım örtüsü kavislendirildi. Önden kafatası üstü: ayrım 1,0–1,4 cm, ayrımın 2–5 cm yanı 2,4–3,4 cm, kenarlar 3,0–3,9 cm (h56a: 0,8–1,7 / 2,4). Profil orta çizgi tepe 1,5 cm. Kask değil: üst dış stand-off 1,0–1,2 cm (h51a 2,3). |
| Üst saç önden daha dolu görünüyor mu? | **Evet** (board 02, 07): ayrımın iki yanında yumuşak bombe, yanlara doğru dolgun geçiş. Referansla karşılaştırıldığında hâlâ daha düzenli ve daha az dağınık. |
| Şakak ve yan kaplama iyileşti mi? | **Evet.** Şakak kaplaması %32–57 → %91, alın köşesi %24–27 → %88–93, yan dış stand-off 1,6–1,9 cm (`data/cover_table_h51a_h64a.md`). Yüz yanından inen dalgalı teller (yeni katman) referanstaki gibi yanak boyunca iniyor. |
| Enseden gelen uzun saç artık topuz altında okunuyor mu? | **Evet, ana groom'da.** Ense alanı kulak arkasına kadar genişletildi (yeni kök bandı yalnız ense alanına; ana kilit kökleri değişmedi), alan tellerine deriden ayrılan katmanlı bir kabarıklık verildi (dış stand-off 0,3 → 1,1–1,4 cm), kısa düşen ense telleri azaltıldı, saç çizgisi yumuşak ve düzensiz U biçimine getirildi. Board 04 satır 1: yalnız ana groom, arkadan yuvarlak ve dolu, ense kökünden topuza kalkan saç. Board 04 satır 3: yalnız topuza katılan uzun ense saçı (turuncu). |
| Hâlâ 3–5 numara ense etkisi kaldı mı? | **Büyük ölçüde hayır.** Dar dikey "kuyruk" ve düz alt kenar kalktı. Ana groom'da en alt sırada (z 152–154) kısa bir yumuşak kenar var; tam saçta üzerinden omuza inen dalgalı teller geçiyor. |
| Topuz altı ayrı koyu levha mı, doğal mı? | **Kısmen doğal.** Topuz büyütüldü (yarıçap 2,35 → 2,75), kaçan halka uçları artırıldı, yüzeyinden taşan 110 halka/uç kümesi eklendi; ense saçı topuzun altına kabarık katman olarak giriyor. Referanstaki kadar dağınık ve gevşek değil; arka görünümde topuz ayrı bir sarmal olarak az okunuyor. |
| Yüz/burun/kaş değişmeden kaldı mı? | **Evet.** 7 kilitli dosyanın SHA1 değeri geri dönüş kaydıyla aynı; korunan eski adaylar 89/89. |

## Yöntem

- Kılavuzlar: P'deki aile tabanlı tam merkez çizgisi yazımı (`tools/blender_g11rq_guides.py`, q4) + ayrım yanı yükselme noktası + dalga artışı; kök kimliği korumalı uygulama (0 uyumsuzluk). Örnekleme h51a ile aynı.
- Ense alanı ve dağınık katman kendi RNG'lerini kullanıyor: ana kilit telleri ense değişikliklerinden önce/sonra bit-bit aynı (h59a ↔ h60a/h60b doğrulandı).
- Yeni dağınık katman (Loose groom'da, simülasyonlu): `mess_face` (yüz yanından köprücük kemiğine), `mess_ear` (kulak arkasından boyun yanına), `mess_nape` (enseden aşağı), `mess_bun` (topuzdan taşan halkalar), `mess_surf` (ana kütle üstünde dalgalı ayrık teller); 5.188 tel, 4–40 tellik kümeler. Bu katman ana yapıyı gizlemek için değil, referanstaki dağınıklık için; ana yapı yalnız-Main panolarında ayrıca gösterildi.
- Her turda tel geometrisi ölçüldü (siluet yüksekliği, ense stand-off, kök haritası, bölge kaplaması), sonra Unreal'da referansın altı açısıyla çekildi. Yoğun üretimler: h57a–h64a (8 tur; h58a tepe fazla yüksekti, geri alındı).

## Teknik (`data/tech_h64a.jpg`, board 07)

| Kontrol | Sonuç |
|---|---|
| Bağlama | iki yeni bağlama hedef m2; yüz rig'i çalıştırılmadı |
| Hareket 27 + eğim 7 | Temiz: kökler scalp'ta, kulak/boyun kesişmesi yok, topuz açılmıyor, sarkan teller başla gidiyor, nötre dönüş var |
| Tel kontrolü | 2 tel 3 cm üstü segment (topuz halkası), yüz önünden geçen 265 tel = yüz yanı sarkan teller (bilinçli) |
| Simülasyon koşulu | S ve X aynı oturum, kurulumda sıfırlama, time=0 |
| LOD | h64a için LOD'lar üretildi; mesafe/kalınlık tablosu ve aktif LOD indeksi TEST EDİLMEDİ |

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| ÖNDEN TEPE HACMİ | BAŞARILI |
| ÜST KÜTLENİN DOĞALLIĞI | KISMEN (dolu ama referanstan daha düzenli) |
| ŞAKAK / YAN KAPLAMA | BAŞARILI |
| KULAK ARKASI HACİM | KISMEN (kaplama %88–98; kütle var, referanstaki gevşeklik yok) |
| ENSEDEN GELEN UZUN SAÇ | BAŞARILI (ana groom'da yuvarlak dolu ense, topuza kalkıyor) |
| TOPUZ ALTI BAĞLANTISI | KISMEN |
| SAÇIN BAŞI DOLU KAPLAMASI | BAŞARILI |
| REFERANS SAÇ KARAKTERİ | KISMEN (topuz referanstan küçük ve daha düzgün; sarkan teller daha ince ve düzenli dalgalı; genel dağınıklık daha az) |
| YÜZ / BURUN / KAŞ KORUNUMU | BAŞARILI |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (LOD mesafe ayarı TEST EDİLMEDİ) |

## Board'lar

`boards/01_REF_START_NEW.jpg` · `02_FRONT_HAIR_SHAPE.jpg` · `03_TEMPLE_SIDE.jpg` · `04_NAPE_LONG_HAIR.jpg` · `05_UNDER_BUN.jpg` · `06_GUIDES.jpg` · `07_UNREAL_FINAL.jpg`; `data/h64a_vs_ref.jpg` referansın altı açısı ile yan yana. Ham kareler `captures/g11rq*` (yayımlanmadı).

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
