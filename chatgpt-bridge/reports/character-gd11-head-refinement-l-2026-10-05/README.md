# GD11 baş revizyonu L: doğrulanmış F4ab üzerinden kontrollü devam — yüz tanısı (kaş arası–burun kökü–üst sırt) ve saç (h45b | h46a | h47a) ayrı

Tarih: 2026-10-05. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Production'a hiçbir şey geçmedi. Yeni auto-rig çalıştırılmadı. K5 yeniden uygulanmadı.

## Sorulara doğrudan cevaplar

| Soru | Cevap |
|---|---|
| F4ab başlangıcı doğru muydu? | Evet. Başlangıç editörden okundu (`prov/*.json`, her çekim için): yüz `/Game/Sphirus/CharacterLab/GD11_HeadRefinementD_20261004/Face/SKM_G11RD_Face_f4ab`, DNA `MHC_G11RD_F4AB_Head`, 858 morph, `ABP_Face` nötr (animasyon yok), h45b + `GB_G11RJ_*_f4abh45b` (hedef F4ab), k10/e2. Korunan dosyalar 76/77 grup birebir aynı (`data/preservation_check.json`; tek fark K kaynak verisindeki `cycle_k5.log` günlük dosyası — durdurulan ilk K5 döngüsünün artık süreci sonradan yazdı; hiçbir asset/kaynak değişmedi). |
| K5'in reddedilen işlemlerinden biri yeniden uygulandı mı? | **Hayır.** Bu turda yüz geometrisi değiştirilmedi (aşağıda neden). Değerlendirilen L1–L4 denemeleri yalnız burun kökü/üst sırt bandındaydı (çene, yanak, ağız, kaş kemeri, göz: 0,00 mm) ve hiçbiri aday olarak seçilmedi. |
| Ölçüm sistemindeki yapay sınır ve ölçek sorunları nasıl ele alındı? | (1) Kontur ölçümü yalnız **tanı** için tutuldu; sculpt hedefi olarak kullanılmadı. (2) "Çene 9 mm yukarıda" sonucu: maske boyun/çene altı yüzeyleri çıkarılarak üretilmişti; bu yapay kesme kenarı artık anatomik hedef sayılmıyor ve bu turda çene ölçümü kullanılmadı. (3) 5,95 cm IPD varsayımı: referansın gerçek ölçeği bilinmiyor; sonuçlar piksel/IPD oranı olarak okunur, santimetre değerleri yalnız yaklaşık. (4) K'daki "burun kökünde dip yok" bulgusu **hatalıydı**: sellion algoritması kaş arası–alın eğimini seçiyordu; düzeltilmiş profil ölçümü (`tools/blender_g11rl_radix.py`, 0,1 cm bölmeli dış orta çizgi) F4ab'da normal bir kök dibi gösteriyor. (5) Her ölçüm ve görüntü gerçek aday adı + kaynak dosya + zaman damgasıyla eşleşiyor (`data/radix_metrics.txt`, `prov/`). |
| Yüzde hangi tek ilişki değişti ve neden? | **Hiçbiri.** Tek aktif hedef (kaş arası–burun kökü–üst sırt) tanıya göre geometri düzeltmesi gerektirmiyor: F4ab'da burun kökü kaş arası–sırt kirişinin 4,6 mm altında (z 162,9), kaş arasının 2,6 mm altında — doğal aralık. Kökü derinleştiren L1/L2 (−1,4 / −2,9 mm) istenmeyen yönde ("derin oyulmuş kök"); üst sırt yan duvarını yumuşatan L3/L4 (+0,44 mm) clay ve dokulu okumada görünmez. Kaş gizlenince (board 02) geçiş düz ve doğal; görünür farkın ana kaynağı **kaş groom'unun yerleşimi/biçimi** (M_SlightArch: referanstan yüksek, ince, kemerli) ve sıyırma ışığında dar sırt sırtı. Kaş groom değişikliği bu turun kapsamı dışında bırakıldı (kullanıcı kararı gerekir). |
| Korunan yüz bölgelerinde toplam değişim? | 0,00 mm (yüz değişmedi). L1–L4 deneme ısı haritaları `data/heat_L*.txt`: dudak/ağız, burun tabanı, çene, yanak, kulak, kafatası 0,00 mm; göz/kapak ≤0,28 mm (L2) / ≤0,25 mm (L4) — yine de aday olmadılar. |
| h46a'dan hangi saç kazanımları tutuldu, hangileri reddedildi? | h46a aynı F4ab + k10 üzerinde h45b ile karşılaştırıldı (board 05/06; `prov/g11rlHA.json`, `prov/g11rlHB.json`: her ikisi F4ab'ı hedefleyen bağlamalar). **Tutulan:** kulak arkası `ear_frame` kütlesi (315 → 546 tel; kulağı kapatmıyor, kepçe okunuyor), ense `nape_field` kaldırma varyasyonu (katmanlı okuma; levha/L yok, kökler saç çizgisinde: %17–18 çizgiye 1 cm içinde, uzunluk 11–26 cm), çapraz şakak tutamları (kök çizgisinden, alın köşesi → kulak üst arkası; perde değil). **Reddedilen:** hiçbir grup geri alınmadı; ama h46a'nın çapraz tutamları zar zor görünüyordu (eklenti düzeyinde) ve topuz altı hâlâ blok okunuyordu → **h47a** aynı yapıyla devam: çapraz tutam kalınlık/sayı ↑ ve daha alçak yol (ztop 161,8–162,6), kulak arkası 672 tel (+ ense kulak arkası yoğunluğu 2,0), ense alt tutam/yama/kaldırma varyasyonu ↑ (0,50 / 0,6 / 0,85), serbest ense teli 0,18 → 0,24. h45b → h46a → h47a farkları: `data/hair_h45b_to_h46a_env_diff.txt`, `data/hair_h46a_to_h47a_env_diff.txt`. **Sınır (dürüst):** ana ön/şakak kütlesinin yönü (topluca geriye taranmış) oluşturucuda değişmedi; çaprazlık ek tutamlarla okunuyor; `temple_veil` tellerinin kulak kutusu nokta sayısı arttı (3.005 → 9.859; kulak üst kenarının üstünden geçiş), görsel kontrolde kulak açık. |
| Referansa yaklaşma bütün başta görülüyor mu? | Kısmen. Saçta ön çerçeve biraz daha çapraz/gevşek, kulak arkası dolu ve ense katmanlı; yüz değişmediği için yüz benzerliği başlangıç seviyesinde (K5'in bozduğu tip korunuyor). Bütün başta referansa yaklaşma yalnız saç çerçevesinden geliyor; kaş groom yerleşimi ve referansın yumuşak dokusu hâlâ fark. |
| Hangi eksikler hâlâ duruyor? | Çene/alt yüz, yanak doluluğu, göz çevresi/sakin ifade, burun genişliği, kaş groom yerleşimi: **bu turda düzenlenmedi, açık işler.** Ana ön/şakak tutamlarının yönü (topluca geriye taranmış) saç oluşturucusunda değişmedi; çapraz akış yalnız ek tutamlarla. Aktif groom LOD indeksi Python'dan okunamıyor (mesafe testi görsel). |

## 1. Başlangıç (board 01)

F4ab + h45b + k10. Editörden okunan kompozisyon kayıtları `prov/g11rlHA.json` (zaman damgalı). Reddedilen K5 paketi (`GD11_HeadRefinementK_20261005`) yalnız kayıt; L zinciri K klasörünü de korunan gruba aldı (76/77 grup birebir aynı (`data/preservation_check.json`; tek fark K kaynak verisindeki `cycle_k5.log` günlük dosyası — durdurulan ilk K5 döngüsünün artık süreci sonradan yazdı; hiçbir asset/kaynak değişmedi)).

Not: K zincirinin durdurulan kabuğunun alt süreçleri sonradan K adayına iş kuyruklamış ve editörü çökertmişti (`EXCEPTION_ACCESS_VIOLATION`, K5 binding yeniden derlemesi); korunan gruplar etkilenmedi (SHA), K adayının kendi bağlamaları/DNA bağı yeniden yazılmış olabilir (K reddedilmiş kayıt). Süreç ağacı öldürüldü, editör temiz başlatıldı.

## 2. Yüz tanısı: kaş arası–burun kökü–üst sırt (board 02, 03, 04)

| Ölçü (`data/radix_metrics.txt`) | F4ab | L1 | L2 | K5 (red) |
|---|---|---|---|---|
| Sellion y / z (cm) | 13,28 / 162,9 | 13,17 / 163,6 | 13,03 / 163,6 | 13,28 / 162,9 |
| Kaş arası (glabella) y / z | 13,54 / 164,3 | 13,57 / 164,5 | 13,56 / 164,5 | 13,75 / 164,5 |
| Kök dibi: kiriş altı / kaş arası altı (mm) | 4,57 / 2,60 | 4,89 / 3,99 | 6,20 / 5,29 | 5,44 / 4,61 |
| 162→163 sırt eğimi (mm/cm) | 5,28 | 5,97 | 7,21 | 5,28 |

Ayrıştırma: kaş gölgesi (board 02: kaş gizli/açık, stüdyo + sıyırma + dengeli ön ışık), kaş üstü yumuşak doku, kök derinliği, üst sırt eğimi, kamera. Sonuç yukarıda. L1–L4 ısı haritaları ve clay kırpımları board 02'de "reddedilen yön / görünmez" olarak gösteriliyor; hiçbiri rig'lenmedi.

## 3. Saç: h45b | h46a | h47a — aynı F4ab, aynı k10, aynı kameralar (board 05, 06)

| Ölçü (`data/strand_control_summary.txt`) | h45b | h46a | h47a |
|---|---|---|---|
| `ear_frame` tel / kulak kutusu nokta | 315 / 94 | 546 / 213 | 672 / 216 |
| `temple_veil` tel / kulak kutusu nokta | 309 / 3.005 | 873 / 8.204 | 1.066 / 9.859 |
| `nape_field` uzun tel / serbest tel | 4.692 / 691 | 4.696 / 687 | 4.463 / 908 |
| ense kök çizgiye 1 cm içinde | %18 | %18 | %17 |
| ense tel ortası kafatasına (cm) q1/orta | 0,30 / 0,62 | 0,31 / 0,60 | 0,31 / 0,56 |

Görsel (board 05/06): **ense** üç sürümde de doğal çizgiden topuza uzun saç; h47a'da katmanlanma biraz daha okunuyor, bloklaşma/kabarma yok. **Kulak arkası** h47a'da belirgin daha dolu; kulak kepçesi her üçünde okunuyor; kalın ip yok. **Çapraz akış** h46a'da zayıf, h47a'da şakak üstünde görünür; ana kütle yönü aynı. **Topuz altı** h47a'da hafif daha katmanlı, hâlâ koyu ve düzenli. **Ön/3/4 çerçeve** dengeli, iki taraf farklı (asimetrik tablo). Seçim: **h47a** (F4ab'a `GB_G11RL_*_f4abh47a` ile bağlı).

## 4. Ayrıştırma (board 07)

Başlangıç (F4ab + h45b) | yalnız yüz: **yok (yüz değişmedi)** | yalnız saç (F4ab + h47a) | birleşik = yalnız saç.

## 5. Teknik (board 08)

| Kontrol | Sonuç | Kayıt |
|---|---|---|
| Bağlamalar | 4 bağlama `GB_G11RL_*_f4abh47a` → hedef `SKM_G11RD_Face_f4ab` (yeniden açılışta okundu) | `data/reopen_check.json`, `prov/g11rlHC.json` |
| Rig (54 çekim; saç gizli): göz kırpma tek/çift, bakış 4 yön, kaş, gülümseme, dudak kapama, çene/ağız açma, vizemler ee/mbp/oo/w, üst dudak, burun deliği, yanak | Temiz; dudak ayrılması, kapak açıklığı, nostril çökmesi yok | `g11rlrig_*` |
| Hareket (27: bakınma, dönüşler, durma) + baş eğimi (7) + arka/ön ışık setleri (10) | Temiz; kulak/boyun kesişmesi, saç kökü kopması yok | `g11rlmot_*`, `g11rlP_*`, `g11rlRL_*` |
| Groom LOD | Temiz editörde ayarlandı (Main/Loose: 1.0/0.65/0.4/0.1 azaltma; kalınlık 1/1.25/1.7/1), yeniden açılışta tablo aynı; mesafe testi 1,25–25 m ön/45°/arka (24 çekim) **görsel**; aktif LOD indeksi Python'dan okunamıyor (`prov/*`: `groom_lod` unreadable) | `G11RL_LOD`, `g11rllod_*` |
| Yeniden açılış (temiz editör) | F4ab 858 morph + DNA `MHC_G11RD_F4AB_Head`, h47a groom'ları, MI'lar, kask, 4 bağlama yüklendi; kirli paket yok (önce/sonra) | `data/reopen_check.json` |
| Kaynak/bellek | Zincir öncesi C: 23 GB boş; editör çökmesi yok; auto-rig çalıştırılmadı | — |
| Korunan dosyalar | 76/77 (yalnız `cycle_k5.log` günlüğü) | `data/preservation_check.json` |

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| F4ab BAŞLANGICININ DOĞRULANMASI | BAŞARILI |
| K5 İŞLEMLERİNİN TEKRARLANMAMASI | BAŞARILI |
| ÖLÇÜM SİSTEMİ KONTROLÜ | BAŞARILI (yapay sınır tespit edildi; çene ölçümü kullanım dışı; sellion hatası düzeltildi) |
| KAŞ ARASI–BURUN KÖKÜ–ÜST SIRT GEÇİŞİ | KISMEN (tanı tamam; geometri değişikliği gerekmedi; kaş groom'u açık iş) |
| KORUNAN YÜZ BÖLGELERİ | BAŞARILI (0,00 mm) |
| SAÇ: ENSE | BAŞARILI (doğal kökten topuza; katmanlanma KISMEN) |
| SAÇ: KULAK ARKASI | KISMEN (kütle arttı, kulak açık; referanstan ince) |
| SAÇ: ÇAPRAZ ÖN/YAN AKIŞ | KISMEN (görünür çapraz tutamlar; ana kütle yönü değişmedi) |
| SAÇ: TOPUZ ALTI | KISMEN |
| REFERANSA GENEL BENZERLİK | KISMEN |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (aktif LOD indeksi TEST EDİLMEDİ — okunamıyor) |
| ESKİ KAYNAKLARIN KORUNUMU | BAŞARILI (asset düzeyinde 100%; bir günlük dosyası farkı açıklandı) |

## Dosyalar

`boards/01..08`, `data/` (radix metrikleri, ısı haritası özetleri, op JSON'ları L1–L4, strand kontrolü, saç env farkları, koruma kontrolü, yeniden açılış), `prov/` (her çekim setinin editörden okunan kompozisyonu), `tools/`.
