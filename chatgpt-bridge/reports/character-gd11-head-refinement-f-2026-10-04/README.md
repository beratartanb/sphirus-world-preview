# GD11 saç revizyonu F: h39i'nin doğallığını ve referansa benzerliğini tamamlama (yüz sabit)

Tarih: 2026-10-04. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Production'a hiçbir şey geçmedi.

## Başlangıç (doğrulandı)

**Kaynak:** E raporu, commit `6770f3f1`.

| Parça | Asset / dosya |
|---|---|
| Saç (başlangıç) | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementE_20261004/Hair/GR_LK_Hair_{Main,Loose}_h39i` |
| Bağlamalar | `Face/Bindings/GB_G11RE_*_f4abh39i` |
| Kaynaklar | `Saved/Codex/GD11_HeadRefinementE_20261004/hair/h39i/` (`build_env.txt`, `strands.npz`, `.abc`) |
| Yüz (değişmedi) | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementD_20261004/Face/SKM_G11RD_Face_f4ab` + DNA `MHC_G11RD_F4AB_Head` |
| Ten / göz / kaş / kirpik | k10 / e2 / M_SlightArch / S_Thin; değişmedi |

E'den daha yeni yerel çalışma yoktu. h38d ve h37 yalnız geçmiş karşılaştırma için kullanıldı.

## Yeni aday

`/Game/Sphirus/CharacterLab/GD11_HeadRefinementF_20261004/`

| Parça | Asset / dosya |
|---|---|
| Saç | `Hair/GR_LK_Hair_{Main,Loose}_h40d` + kask; LOD tablosu ayarlı |
| Bağlamalar | `Face/Bindings/GB_G11RF_*_f4abh40d`; hepsi F4ab yüzünü hedefliyor |
| Korunan kaynak kopyası (Saved dışında) | `SourceAssets/Characters/GD11_HairF_20261004/`: `h40d/build_env.txt`, `strands.npz`, `hair_main.abc`, `hair_loose.abc`, `helmet.json`; `tools/blender_g11rf_hair.py`; yapım kafası `headC8.npy`; `sculpt_package_v6.json.gz`; yeniden üretim talimatı `README.txt` |
| Çalışma kaynakları | `Saved/Codex/GD11_HeadRefinementF_20261004/hair/h40a…h40d/` |
| Ham render'lar | `Saved/Codex/GD11_HeadRefinementF_20261004/frames/raw/` (370 dosya) |

`.blend` dosyası yok: groom bu girdilerden prosedürel üretiliyor. Düzenlenebilir kılavuz, oluşturucunun açık parametreleri ve `build_env.txt`.

**Yazma yolları:** ilk çekimden önce E'ye özel olmayan, F'ye yazan scriptler kuruldu.
- `gd11rf_face_run.sh` stüdyo klasörü ve kayıt yolu F; B, C, D ve E'ye bağlama yazmayı reddediyor.
- `gd11rf_caps.sh`, stüdyo klasörü F değilse çekim yapmıyor.
- Doğrulama: **56/56 korunan grup birebir aynı**. E (h39i) dahil, eski adaylara hiçbir yazma olmadı.

**Paylaşılan araçta tek ek değişiklik:** çekim aracı `ue_lk_capture.py`'ye arkadan aydınlatma için iki ışık modu eklendi: `rearR` ve `rearL`. Değişiklik eklemeli, mevcut modlar aynı. Önceki hali: `data/ue_lk_capture_before_F.py` (yerel).

## 1. Ana/ikincil tutam hesap denetimi (board 06)

| Kod yolu | Durum |
|---|---|
| Ana kilit yolu (`lock_path`, `SPH_FIELD_PATH=1`, `FLOW_E`) | Yükseklik her yol noktasında `lift_field_arc` ile hesaplanıyor. Ana kilitte hesaplanan `lift = lift_field(r)` argümanı bu yolda **kullanılmıyor**; etkisiz, bilerek bırakıldı. |
| **İkincil derinlik `sdep`** | E'de hâlâ eski, yüksekliğe bağlı `lift_field` farkını kullanıyordu: `(Δ) × 0,55`. Eski alanda tepe kaldırma 3,0, eğimi yaklaşık 3,5 cm. Kökü yüksekte olan ikinciller 0,8 cm'ye varan ek şişkinlik alabiliyordu. **Değişti:** `SPH_SDEP_ARC=1` ile aktif yay profilini kullanıyor. |
| Üçüncül derinlik (σ 0,08), son tel dolgusu ve kıvırcıklık | Alandan bağımsız; değişmedi. |
| Uygulama sırası | Kilitler (ana → ikincil → üçüncül → teller → topuz halkası) → ön dolgu (yalnız kilit telleri) → ayrım örtüsü → bebek tüyleri → serbest teller (yüz çerçevesi, şakak, kulak arkası, ense). |

**Kontrollü karşılaştırma:** h39i ile h40a. Yalnız `SPH_SDEP_ARC` farklı; kökler, kümeler ve tohumlar aynı.
- Ön (+10…+30°): 0,1–0,3 cm alçaldı.
- Orta hat tepe-arka: 0,1–0,3 cm yükseldi.
- Arka ve topuz: aynı.

**Sonuç:** tutarsızlık gerçekten etkiliydi ama küçük. Görselde fark hafif (board 06). Düzeltme kötüleştirmediği için tutuldu.

## 2. Sanatsal değişiklikler (h40a → h40d)

Tam fark: `data/hair_h39i_to_h40d_env_diff.txt`. Oluşturucu: `blender_g11rf_hair.py`.

| Bölge | Ne değişti | Neden |
|---|---|---|
| Alın kenarı | `SPH_FILL_EDGE` 0,4 / `W` 1,5 cm: saç çizgisine 1,5 cm içinde köklenen teller ön dolgudan daha az itiliyor. Alçak yatıp kenarı yumuşatıyorlar; arkadaki ana kütle yükselişini koruyor. | Kenar h38d'ye göre sertti. Seyrekleştirme veya bebek tüyü artırma yapılmadı. |
| Ayrım | Ayrımı çaprazlayan örtü telleri yükselişin %50'siyle kalkıyor (`SPH_PC_LIFT`). İki yükselmiş yan arasında köprü kuruyor; E'nin ayrım çukuru korundu. | Koyu V, iki yanın yükselmesi ile düz yatan örtü telleri arasındaki boşluktu. Sağ/sol farkı (`PART_VAR` 0,04) V'yi büyüttüğü için 0'da kaldı. |
| Şakak / üst kulak | Yeni `SPH_TEMPLE_VEIL` tutamları yan saç çizgisinden çıkıyor; şakağın üzerinden (z 164,1) kulağın üstünden geçiyor (z ≥ 164,6 veya kulağın dışından |x| ≥ 9,6), sonra yan-arka kütleye katılıyor. Karakter solunda 2, sağında 3 tutam; biri kulağın üst kenarını hafifçe örtüyor. Genişlik 0,5–0,75, tel sayısı ×1,5. | Profilde şakak çok açıktı. Saç çizgisi aşağı çekilmedi. |
| Kulak arkası | E'nin katılan/serbest yapısı korundu; geometri değişmedi. | Arkadan aydınlatma eklendi; etki artık görülebiliyor. |
| Ense | Kaldırma tabanı 0,25 → 0,08, ense profili düşürüldü, yoğunluk 1,8 → 1,25. Ense saç çizgisi boyunca 1,3 cm'lik yoğunluk geçişi (`SPH_NAPE_EDGE`). | Arkadan aydınlatınca ense kütlesi düz alt kenarlı bir blok gibiydi. |
| Topuz | Grup 8 → 10, giriş dağılımı 0,5, tutam başına tur sayısı çeşitliliği (`SPH_BUN_TURN_VAR` 0,7) ve eksen eğimi (`SPH_BUN_TILT_L` 0,25). Konum, boyut ve kaçan uç sınırları aynı. | Topuz düzenli iç içe bir sarmal gibiydi. |
| İkincil derinlik çeşitliliği | `SPH_SEC_DS` 0,17 → 0,24 | Tutamlar daha az eşit katmanlanıyor. |

**Reddedilen denemeler:**
- **h40b:** `PART_VAR` 0,04 ayrım V'sini büyüttü; topuz halka yarıçapı 1,1 topuzu büyüttü.
- **h40c:** ense düzeltmesinin ilk hali; düz kenar sürdü, yoğunluk geçişi eklendi.
- **h40c'nin ilk build'i:** ayrım örtüsü satırına eklenen yorum döngü sayacını yorumun içine aldı ve sonsuz döngü oluştu. Bu bir kodlama hatasıydı, düzeltildi.

**Renk ve materyal:** h39i değerleri aynen. **Ten:** k10. Değişmedi.

## 3. Teknik

| Kontrol | Sonuç |
|---|---|
| Bağlama | `GB_G11RF_*_f4abh40d` dördü de `SKM_G11RD_Face_f4ab`'i hedefliyor; temiz editörde okundu. Yüz auto-rig yok. |
| Baş eğimi (E'nin test klibi, dinamik saç) | Yaklaşık 26° öne ve 30° yukarı. Alın kökleri yerinde; şakak ve kulak tutamları yüze girmiyor; topuz girişleri açılmıyor; serbest tutamlar kütleden kopuk görünmüyor; nötre temiz dönüş. |
| Hareket (27 çekim) | Dönüşler, koşu-durma, etrafa bakma temiz. |
| LOD | Temiz editörde ayarlandı (%65 ×1,25 / %40 ×1,7 / kask), yeniden açılışta korunmuş. Mesafe testi 1,25 / 3 / 6 / 9 / 12 / 16 / **20 / 25 m**, önden ve 45°'den. Stüdyo arka plan küresi (yarıçap yaklaşık 20 m) yalnız bu çekim için yaklaşık 35 m'ye büyütüldü, böylece kamera stüdyonun içinde. Alın çizgisi, ayrım, şakak örtüsü, topuz ve silüet geçişlerde sıçramıyor. **Aktif LOD indeksi bu build'de Python'dan okunamıyor**; bu yüzden bu bir mesafe görünüm testidir, aktif LOD kanıtı değildir. |
| Yeniden açılış | Temiz editörde yüz (D), DNA, 858 morph, h40d groom'ları, materyaller, kask ve 4 bağlama yüklendi. Kaydedilmemiş paket yok. |
| Korunan dosyalar | **56/56** |

## Sorulara ayrı cevaplar

- **Hesap tutarsızlığı gerçekten etkili miydi?** Evet, ama küçük: ±0,1–0,3 cm ve görselde hafif.
- **Hangi kod yolu değişti?** İkincil `sdep` aktif profile bağlandı. Ana kilidin `lift` argümanı etkisiz olduğu için bilerek bırakıldı. `lift_field`, `FLOW_E` kapalı eski yollar için duruyor.
- **Alın kenarı daha doğal mı, örtü korundu mu?** Evet. Kenar daha yumuşak, kel bant yok.
- **Şakak ve kulak çevresi referansa yaklaştı mı?** Kısmen. Kulak üstü daha dolu; şakak önü profilde hâlâ referanstan açık.
- **Topuz bağlantısı daha doğal mı?** Kısmen. Halkalar daha az düzenli, giriş kademeli. Topuz hâlâ derli toplu, referanstaki dağınık topuz değil.
- **Saç hâlâ fazla düzenli veya kask gibi mi?** Kask gibi değil. Ama yüzeyi referansa göre hâlâ düzenli; elle yazılmış rehber groom olmadan bu sınır sürüyor.
- **Yüz, DNA ve ten gerçekten sabit mi?** Evet. Yüz ve DNA asset'leri D'de duruyor ve okunarak kullanıldı; 56/56 birebir.
- **Hangi eksikler sürüyor?**
  - Ense alt kenarı arkadan hâlâ belirgin bir çizgi.
  - Şakak önü açık.
  - Saç karakteri düzenli.
  - Aktif LOD indeksi okunamıyor.

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| MEVCUT YÜZÜN KORUNUMU | BAŞARILI |
| ANA/İKİNCİL TUTAM HESAP TUTARLILIĞI | BAŞARILI |
| ALIN KENARININ DOĞALLIĞI | BAŞARILI |
| ALIN ÖRTÜCÜLÜĞÜ | BAŞARILI |
| AYRIM | BAŞARILI (dar, köprülü; V yok) |
| ÖN–TEPE–ARKA AKIŞININ KORUNUMU | BAŞARILI |
| ŞAKAK/KULAK ÇERÇEVESİ | KISMEN |
| KULAK ARKASI AKIŞ | KISMEN (arkadan aydınlatmada okunuyor; ense kenarı hâlâ sert) |
| TOPUZ BİRLEŞİMİ | KISMEN |
| ORİJİNAL SAÇA BENZERLİK | KISMEN |
| BÜTÜN BAŞIN GERÇEKÇİLİĞİ | KISMEN |
| BINDING | BAŞARILI |
| HAREKET | BAŞARILI |
| LOD | BAŞARILI (25 m'ye kadar mesafe testi; aktif indeks doğrulanamadı) |
| YENİDEN AÇILIŞ | BAŞARILI |
| KORUNAN DOSYALAR | BAŞARILI (56/56) |

**Yöntem:** bütün değişiklikler kodla (oluşturucunun F kopyası ve parametreleri) yapıldı. Serbest elle groom yapılmadı.

## Board'lar

| Board | İçerik |
|---|---|
| 01 | Bütün baş: orijinal / h39i / h40d, ön ve 3/4 |
| 02 | İki profil ve arka; arka görünümler arkadan aydınlatmalı |
| 03 | Alın kökleri ve ayrım: nötr / yan ışık, yakın ve bütün baş |
| 04 | Şakak ve üst kulak örtüsü, iki taraf, orijinalle |
| 05 | Kulak arkası ve topuz birleşimi, arkadan aydınlatmalı tanı ışığı |
| 06 | Akış sistemi kontrolü: h39i / yalnız hesap düzeltmesi h40a / final h40d |
| 07 | Hareket, LOD ve yeniden açılış |
