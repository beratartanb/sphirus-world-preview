# Sphirus World: AI araç değerlendirmesi v3. ABP koruma, T1b, gerçek sahne değişikliği, oyuncu kamerası (2026-10-31)

v1 ve v2 raporları değiştirilmedi.

**Kaynaklar:** sayılar `t1b/data/*.json` dosyalarından, tablolar `t1b/TABLES_T1B.md`'den (kodla üretildi), betikler `tools/`'dan.

**Etiketler:**
- **DOĞRULANDI:** bu turda ölçüldü.
- **TAHMİN:** sezgisel bir yönteme dayanıyor; varsayımı belirtilmiştir.
- **NOT_TESTED:** onay gerektiriyor ya da yapılmadı.

**Bu turda değişmeyenler:**
- Editör yeniden başlatılmadı.
- Hiçbir asset, harita, ayar veya cvar değişmedi; kurulum yapılmadı; hiçbir şey kaydedilmedi.
- Editöre yalnız `measure` işleri ve bir `pie` işi gönderildi. Kilit sahibi `aitool` idi; kilit bırakıldı.

**Geçici olup sonunda geri alınanlar:**
- editör kamerasının görüş açısı;
- üç aktörün editörde geçici gizlenmesi (`temporarily hidden in editor`);
- PIE içinde piyonun yeri ve kontrol yönü.

Aktör transform hash'i ve dirty paket listesi önce ve sonra aynı.

---

## 1. İki dirty Animation Blueprint: korundu ve incelendi (DOĞRULANDI)

| | `ABP_GR_MotionMatching` | `ABP_GR_MotionMatchingBase` |
|---|---|---|
| Diskteki dosya | V2.40'ın son yazımıyla (blk2 manifesti) birebir aynı SHA1 → **üretim** | aynı |
| Blueprint durumu | BS_UP_TO_DATE (derleme hatası yok) | aynı |
| Bellekte farklı olan değerler (CDO) | `SHM239_Own` 1 (üretim 0), `SHM240_HeadOn` 1 (üretim 0), `SHM240_BlkSpd` −1 (üretim 60) | aynı |
| Aynı olan | `SHM240_BlkDB` = `PSD_Dense_Stand_Idles` | aynı |

**Nasıl dirty oldular:**
- 00:22'deki doğrulamada dirty listesi boştu.
- V2.40 QA harness'ı (`qa_pie.py`) her A/B koşusunda aday değerleri ABP'nin varsayılan değerlerine (CDO) yazıyor. Üretim değerlerini **bir sonraki koşunun başında** geri yüklüyor.
- Son koşu `v240capn_j40_wall_wofN` (`wof` varyantı) 00:33'te bitti; ardından koşu olmadığı için değerler geri yüklenmedi.
- 00:40'ta editörün otomatik kaydı bu durumu `Saved/Autosaves/...Auto1.uasset`'e yazdı.

**Sonuç:** Bellekteki içerik yalnız bu üç aday düğme değeri; grafikte değişiklik bulunmadı. Bunu kaydetmek, **kabul edilmemiş bir adayı üretime sokar**.

**Yapılanlar:**
- Kaydetme, silme, geri yükleme veya yeniden yükleme yapılmadı.
- 00:40 otomatik kayıtları proje içinde koruma klasörüne kopyalandı (`Saved/Codex/AIToolingEval_20261031/abp_dirty_protect/`). İkili dosyalar yayımlanmadı; yalnız SHA1'leri `t1b/data/abp_autosave_copies.sha1` içinde.

**Not:** Bu turdaki PIE çekimleri bellekteki bu aday değerlerle çalıştı. Karakter dururken bu düğmeler devreye girmiyor:
- `Own` yalnız kesme sırasında devralmayı açıyor;
- `HeadOn` yalnız karakter hareket ederken etkili.

Bu yüzden durağan kamera karelerini etkilemedikleri değerlendiriliyor; kanıtı yok.

---

## 2. Gürültü kaynakları ayrı ayrı

### 2.1 Otomatik pozlama / global parlaklık: basamaklı, tempoya bağlı (DOĞRULANDI)

- Kare başına ortalama parlaklık yavaş kaymıyor; **iki seviye arasında atlıyor**: ev ~85.5 ↔ ~88.0, orman ~84.9 ↔ ~88.5, göl ~86.3 ↔ ~87.7. Fark %2–4.
- ≥5 s bekleme veya kamera taşımasından sonraki ilk 1–2 kare yüksek seviyede; art arda çekimler düşük seviyede.
- Nedeni (eye adaptation, Lumen veya viewport çizim durumu) **belirlenmedi**.
- **Etkisi:** global karşılaştırma bunu "değişiklik" sanar.
- **Çözüm (bu turda uygulandı):** her kare aynı ortalama parlaklığa normalize ediliyor. Ayrıca çekim temposu sabit tutulmalı: her setin ilk iki karesi atılmalı.

### 2.2 Kare-kare farkların kaynaklara ayrılması (TAHMİN)

Yaklaşık 1 s arayla çekilen ardışık karelerde fark enerjisinin dağılımı:

| Görünüm | Global (pozlama) | Yeşil olmayan pikseller, düşük frekans (gölge/güneş beneği) | Yeşil olmayan pikseller, yüksek frekans (TSR titremesi + yeşil olmayan bitki parçaları + gölge kenarları) | Yeşil bitki örtüsü | RMS (0–255) |
|---|---|---|---|---|---|
| Ev önü | %1.6 | %4.4 | %60.3 | %30.3 | 9.06 |
| Göl | %1.7 | %7.8 | %65.4 | %21.0 | 4.57 |
| Orman | %2.7 | %3.2 | %44.2 | %48.1 | 11.23 |

**Sınırlamalar:**
- Bitki maskesi yalnız yeşil baskın pikselleri yakalıyor: koyu iğne yapraklar ve gövdeler "yeşil olmayan" tarafta kalıyor.
- Bu yüzden "yüksek frekans" sütunu TSR için bir **üst sınır**.
- TSR'nin tek başına payı ancak kontrollü bir denemeyle ayrılabilir: TSR geçici kapatılır ve rüzgâr dondurulur. Bunlar oturumluk render ayarı değişikliği olduğu için uygulanmadı; **onay bekliyor**.

**5 kare medyanın gösterdiği:**
- Medyan, ~1 s'lik rastgele kısmı bastırıyor.
- Setler arası (10–30 s) fark çoğu görünümde neredeyse aynı kalıyor: ev statik çiftinde 16×9 karo maksimumu tek karede ortalama 5.38, medyanda 3.84; orman 10.24 → 10.23.
- Yani baskın gürültü saniyeler ölçeğinde değişen rüzgâr ve gölge hareketi; kare başına rastgele TSR gürültüsü değil.

---

## 3. T1b: beş karelik medyan + geri alınabilir gerçek sahne değişikliği (DOĞRULANDI)

**Düzen** (`t1b_cap.py`): her görünüm için
- S1 (5 kare);
- kamera götürülüp getirildikten sonra S2;
- küçük aktör gizlenince S3;
- orta boy aktör gizlenince S4;
- geri açıldıktan sonra S5.

Toplam 63 kare, 2 dk 48 s.

**Gerçek değişiklik:** `set_is_temporarily_hidden_in_editor`.
- Bu, editörün geçici görünürlük bayrağı; aktör özelliği değişmiyor.
- **Hiçbir paketi dirty yapmadı**; aktörlerin hepsi geri açıldı.

| Görünüm | Gizlenen aktör | Ekranda | Görünür mü? |
|---|---|---|---|
| Ev önü küçük | `Architecture_Guard_0_3_0` (yarı boyut 49 cm, 20 m) | 7×68 px | Ağaç gövdesinin arkasında, pratikte görünmüyor (`sheets/crop_house_hidden_guard.png`) |
| Ev önü orta | `Architecture_Guard_0_4_0` (119 cm, 20 m) | 140×79 px kutu | Çoğu gövdenin arkasında |
| Orman küçük | `CATALOG_48_01a0984f` (28 cm, 14.5 m) | 52×55 px | **Açıkça görünüyor**: açık renkli küçük obje kayboluyor (`sheets/crop_forest_hidden_small_object.png`) |
| Göl | Filtreden geçen görünür aday yok | — | Test edilmedi |

### Dedektör

Bilerek basit tutuldu (`t1b_detect.py`):
- pozlama normalizasyonu;
- 5 kare medyan ya da tek kare;
- 48×27 karo (40 px);
- karo başına gürültü haritası **bağımsız** değişmemiş verilerden (S1–S2 geri dönüşü + S1 ve S2 içi kare-kare farkı);
- z-skor.

| Görünüm | Değişmemiş çift S2–S5, maks z | Orman gerçek küçük obje, kendi karosundaki z | Eklenen kalıcı yama, sessiz bölge 24 / 48 / 96 px (z) | Hareketli bölge 24 / 48 / 96 px (z) |
|---|---|---|---|---|
| Ev önü, medyan | 5.64 | — | 2.1 / 5.0 / 13.2 | 0.8 / 2.3 / 12.1 |
| Göl, medyan | 6.12 | — | 11.8 / 32.8 / 32.8 | 3.0 / 4.2 / 15.1 |
| Orman, medyan | 6.51 | 5.34 (S5) / 8.45 (S2); maks z başka karoda → **yerini bulamadı** | 0.9 / 7.1 / 17.9 | 0.5 / 1.7 / 9.1 |
| Orman, tek kare | 5.58 | 5.42 / 8.56 | 1.8 / 9.2 / 17.8 | 0.4 / 1.3 / 9.4 |

Ham gürültü modeli ("pair", tek çift): değişmemiş çiftte maks z 11–28 ve onlarca yanlış karo → **kullanılamaz**. Tüm sayılar `TABLES_T1B.md`'de.

**Sonuçlar:**
- **Medyan, kalıcı küçük değişiklikleri gizlemiyor.** Eklenen yamalarda ve gerçek orman objesinde medyan ile tek kare benzer z veriyor; gerçek objede medyan biraz daha yüksek. Ama belirgin bir kazanç da sağlamıyor: rüzgâr ve gölge saniyeler ölçeğinde değiştiği için 5 kare medyan onları ortalayamıyor.
- **Otomatik yakalanabilenler:**
  - global pozlama değişimi;
  - kamera kayması;
  - hareketli bölgede yaklaşık 96 px ve üzeri değişiklik;
  - sessiz bölgede çoğunlukla 48 px ve üzeri değişiklik.
- **Yakalanamayanlar:**
  - bitki örtüsü içindeki ~50 px'lik gerçek objeler: orman objesi gürültü düzeyinde kaldı;
  - ağaç arkasındaki değişiklikler (oyuncu da görmez).
- **Önerilen eşik:** z ≥ 7. Bu turda yanlış alarmların maksimumu 6.5'ti. Eşik 3 görünüm ve tek bir oturumdan çıktı; geçici.

---

## 4. Çalışan küçük ölçekli doğrulama döngüsü

Yeni altyapı yok; hepsi mevcut runner + Blender Python + PowerShell betikleri.

**1. Temel çekim.**
- Her görünümde: kamera taşı, 12 s bekle, 1 kare at, 5 kare çek (S1).
- Kamerayı götür-getir, 12 s bekle, 5 kare daha çek (S2).
- Süre: görünüm başına ~55 s.

**2. Değişiklikten sonra aynı çekim.**

**3. Ölçüm:**
- pozlama normalizasyonu;
- medyan;
- 48×27 karo z-skoru; gürültü modeli: temel çekimdeki S1–S2 farkı + set içi kare farkları;
- global parlaklık farkı ve d8 SSIM.

**4. İşaretleme:** z ≥ 7 olan karolar ya da \|Δ global\| > 1.0.
- İşaretlenen bölgeler yan yana yakın plana kırpılır; bu adım şimdilik elle, `crop.ps1` ile.
- Kırpımlar görsel olarak incelenir (ben ve kullanıcı).
- Sonuç bir **görsel kabul değildir**; yalnız "değişiklik var, buraya bak" der.

**5. Ayrı hat: oyuncu kamerası istasyonları** (bölüm 5). Sinematik değerlendirme burada yapılır; regresyon kararına karışmaz.

**Döngünün sınırları:**
- Bitki içindeki küçük değişiklikler için bir insan bakışı şart.
- Oturumlar arası tekrarlanabilirlik ölçülmedi.

---

## 5. Gerçek GraceRanger oyuncu kamerası (DOĞRULANDI: çekim; değerlendirme yalnız durağan karelerden)

**Düzen** (`pie_cam.py`):
- PIE: piyon `BP_PBI_Player`, kamera yöneticisi `BP_PCM_GR_Camera`.
- Piyon, T1 görünümlerinin x/y'sine zemine konuldu.
- 4 yön: ileri, sol 90°, sağ 90°, geriye bakış. Pitch −5°.
- HighResShot 1920×1080; toplam 12 kare.
- Ölçülen kamera: **FOV 60**, piyona ~2.1 m.
- Kareler `t1b/player_camera/`, kâğıtlar `t1b/sheets/player_*.png`.

### 5.1 Sinematik değerlendirme (regresyondan ayrı)

Kaynak: STILL_IMAGES_VIEWED. Önce/sonra karşılaştırması olmadığı için Tier verilmedi. Yürüyüş görüntüsü izlenmedi; o kategoriler NOT_TESTED.

| İstasyon | Kompozisyon ve ölçek | Yoğunluk / orta plan | Işık ve atmosfer | Bulgu |
|---|---|---|---|---|
| Ev önü, ileri | Ev sol üst üçte birde; çatı kadraj üstünden kesiliyor. Karakter merkezi kaplıyor. Ev/karakter ölçeği doğru okunuyor | Ön planda eğrelti, ortada gövdeler, arkada ev ve orman: 4 düzlem | Yerde benekli güneş; arka planda nem ve pus | Ev önünde gövdeler kütleyi bölüyor. Kahraman kare olarak kamera yüksekliği ve yönü yeniden ele alınmalı |
| Ev önü, sol 90° | Açık eğim, seyrek gövde ve taş | **Orta plan boş**, düz çimen | Düz, düşük kontrast (yeşil olmayan pikseller p95 147) | "Boş orta plan" adayı (skill'deki hata listesi) |
| Ev önü, sağ 90° | Göl ve sis | Arka planda gövde sırası | Sis kontrastı düşürüyor (yerel kontrast 11.2, en düşük) | Ruh hali uygun; ama değer ayrımı zayıf |
| Ev önü, geriye | Güçlü ışık huzmeleri | Çalılar | Huzmeler baskın | Atmosfer güçlü, odak dağınık |
| Göl, ileri | Su parlak bir yüzey; kıyı çizgisi belirsiz | Ön planda genç ağaç | **Yoğun huzme ve pus**, medyan parlaklık 92 (en yüksek), yerel kontrast 13.8 | Görüntü yıkanmış, su okunması zayıf |
| Göl, sağ 90° | Ev verandası bitkiler arasından çerçeveleniyor | Dolu, katmanlı | İyi | En güçlü "sığınak" okuması |
| Göl, sol / geriye | Kamera çalı ve gövdeye çok yakın | Çok yoğun | — | Ön plan kalabalığı |
| Orman, ileri | Patika okunuyor; derinlik iyi | Katmanlı | Benekli ışık | İyi |
| Orman, sol 90° | **Ev köşesi** kadrajı dolduruyor | — | — | İstasyon ormanın içinde değil, evin kenarında: **yeniden seçilmeli** |
| Orman, sağ 90° | **Kamera çam dallarının içine giriyor**; karakter dalların arkasında | — | — | Kamera bitki örtüsüyle çarpışmıyor; sahibi kamera/çevre skill'leri (değiştirilmedi) |
| Orman, geriye | Yakın çam dalları | Yoğun | — | Ön plan kalabalığı |

**Açıklayıcı göstergeler:** `t1b/data/player_stats.json`. Karakter kutusu hariç parlaklık yüzdelikleri, değer grupları, doygunluk ve yerel kontrast. Kalite puanı değildir.

**Karakterle ilgili gözlem** (kapsam dışı, yalnız not): bazı karelerde saç kırpışmalı/gürültülü görünüyor. HighResShot ile TSR geçmişi ya da groom kaynaklı olabilir; incelenmedi.

---

## 6. Doğrulanmış sonuçlar, eksikler, riskler

**DOĞRULANDI**
- ABP'lerin içeriği ve kayıt durumu; diskteki sürüm üretim.
- Pozlamanın basamaklı ve tempoya bağlı olduğu.
- Medyanın kalıcı değişiklikleri gizlemediği, ama belirgin kazanç da sağlamadığı.
- Geçici gizlemeyle gerçek, geri alınabilir sahne değişikliği; hiçbir şey dirty olmadı.
- Dedektörün sınırları (yakalanan ve yakalanamayan boyutlar).
- Oyuncu kamerasından 12 kare; kamera parametreleri.
- PIE, dirty listeyi değiştirmedi.

**Eksik / NOT_TESTED**
- TSR ve rüzgârın kontrollü ayrımı.
- FLIP.
- Oturumlar arası tekrar.
- Göl görünümünde gerçek değişiklik testi (uygun aday aktör yok).
- Seçilmiş P istasyonları; mevcut istasyonlar T1 x/y'sinden türetildi ve orman istasyonu yanlış yerde.
- 5–15 s yürüyüş görüntüsü.
- İşaretlenen bölgelerin otomatik kırpılması (şimdilik elle).
- Pozlama basamağının nedeni.

**Riskler**
- Bitki içindeki küçük değişiklikler kaçabilir.
- Eşikler tek bir oturumdan çıktı.
- Bellekteki aday ABP değerleri "Save All" ile üretime geçebilir.
- Uzun PIE'den sonra editör viewport'unda bilinen çizim tuzağı var: bir sonraki editör çekiminden önce editör yeniden açılmalı.
- Oyuncu kamerası kareleri aday ABP düğmeleriyle alındı; durağan kareler için etkisiz olduğu değerlendiriliyor, kanıtı yok.

## 7. Onay bekleyenler (hiçbiri yapılmadı)

1. **ABP'lerdeki aday değerleri atmak.** Paketleri diskten yeniden yüklemek ya da editörü kaydetmeden kapatmak. Önerilen bu; kayıt yok.
2. **Oturumluk kontrollü gürültü ayrımı:** TSR'yi geçici kapatma (`r.AntiAliasingMethod`), pozlamayı kilitleme ve rüzgârı dondurma. Kalıcı değil, sonunda geri alınır; yine de render ayarı değişikliği.
3. **Editörü yeniden başlatıp oturumlar arası tekrar.**
4. **FLIP kurulumu** (proje dışında ayrı bir ortam).
5. **P istasyonlarının seçimi:** ev önü, göl manzarası, orman içi. Kullanıcı seçecek; ardından yürüyüş kayıtları.
6. **Orman sağ 90°'deki kameranın dalların içine girmesi:** kamera ve çevre sahiplerine ayrı bir iş olarak.
