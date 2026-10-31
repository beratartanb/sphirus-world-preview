# Sphirus World v4: ABP geri dönüş planı, orman patikası yürüyüş testi, kalite pilotu önerisi (2026-10-31)

Bu turda görüntü karşılaştırma sistemi genişletilmedi. Odak, oyuncu kamerasından görünen gerçek kalite.

**Kanıtlar `v4/` altında:**
- `abp/`
- `walk1/`, `walk2/`: yürüyüş videoları, kareler, istasyon kareleri, loglar
- `perf/`: CSV profiller

**Yapılmayanlar:**
- Kayıt, sıfırlama veya geri yükleme.
- Asset, sahne veya kalıcı ayar değişikliği.
- Editörü yeniden başlatma.

**Yapılanlar:**
- Editöre yalnız `measure` ve `pie` işleri gönderildi.
- PIE içinde piyonun yeri ve kontrol yönü geçici olarak değişti.
- Konsol komutları kullanıldı: `csvprofile` ve `Input.+key`.
- Dirty paket listesi her işten sonra aynı kaldı: yalnız iki ABP.

---

## 1. İki dirty ABP: kontrol ve güvenli geri dönüş planı

### Kanıtlar (DOĞRULANDI)

| Kontrol | Sonuç |
|---|---|
| Diskteki dosyalar | İkisi de V2.40'ın son yazımıyla (blk2 manifesti) birebir aynı SHA1 → **üretim** |
| Bellekteki varsayılan değerler (CDO) | Farklı olan yalnız 3 değer, iki ABP'de de aynı: `SHM239_Own` 1 (üretim 0), `SHM240_HeadOn` 1 (0), `SHM240_BlkSpd` −1 (60). `SHM240_BlkDB` üretimle aynı |
| Grafik bütünlüğü (bellekte) | verify240 şimdi yeniden çalıştırıldı: 96 giriş DB'si, kaynak eğrileri, snapshot exec bütünlüğü ve `WasTk` = 3 bağlantı **geçiyor**. Kalan "bad" maddeleri yalnız şunlar: `pie_or_dirty`, `SHM239_Own = 1`, `SHM240_BlkSpd −1` (`abp/verify240_inmemory_now.txt`) |
| Oturum iş denetimi | 00:22'deki verify240'ta dirty listesi **boştu** (`abp/verify240_at_0022_clean.txt`). Sonrasında ABP'ye dokunabilen işler yalnız beş `qa_pie` koşusu: warm, o, tkh, wst, wof (00:32–00:33; `abp/session_job_audit.txt`) |
| Harness sözleşmesi | `qa_pie` yalnız koşunun `abp_flags` anahtarlarını CDO'ya yazıyor. Bu oturumda dokunulan anahtarlar `Own`, `HeadOn`, `BlkDB`, `BlkSpd`. Üretim değerlerini **bir sonraki koşunun başında** geri yüklüyor; son koşu `wof` olduğu için onun değerleri kaldı |
| Bellek görüntüsü | Bellekteki ABP'ler T3D metni ve CDO metni olarak dışa aktarıldı; SHA1'ler `abp/inmemory_t3d.sha1` içinde. Base'in 107 MB'lık T3D'si yerelde tutuluyor |

**Sınır:** Disk ile bellek arasında tam metin karşılaştırması yapılmadı. Bunun için ikinci bir Unreal süreci gerekiyor, ama boş RAM 5.2 GB'tı; çalışan editörü riske atmamak için yapılmadı. Bellek görüntüsü kaydedildiği için bu karşılaştırma geri dönüşten sonra birebir yapılabilecek.

### Geri dönüş planı (onay bekliyor)

1. **Önerilen:** Editörü kapat ve iki ABP için "Kaydetme" seç.
   - Başka dirty paket yok; listede kaydedilecek bir şey kalmamalı.
   - Yeniden açılışta üretim sürümü yüklenir.
   - Sonra verify240 çalıştırılır: beklenen `ALL_OK`.
   - Sonra ABP'ler yeniden T3D'ye aktarılır ve kaydedilmiş bellek görüntüsüyle karşılaştırılır. Beklenen fark: **yalnız bu 3 değer**, grafikte fark yok.
2. **Editör kapanmadan:** iki paket diskten yeniden yüklenir (`reload_packages`, kapılı `control` işi); aynı doğrulama yapılır.
3. **Yapılmayacaklar:**
   - "Save All": kabul edilmemiş adayı üretime sokar.
   - Değerleri elle düzeltmek: paket dirty kalır, kaynağı belirsizleşir.
4. **Kalıcı önlem:** her A/B zincirinin sonuna bir "üretime dön + kaydetmeden geri al" adımı eklenir. Bu adımlar zaten var: `qa_pie` production modu ve `revert_quit`.

Otomatik kayıt kopyaları korunuyor: `Saved/Codex/AIToolingEval_20261031/abp_dirty_protect/`.

---

## 2. Orman istasyonu taşındı: gerçek GraceRanger kamerasıyla yürüyüş testi

- **Eski istasyon:** (2200, 1580). Evin yanında kalıyordu.
- **Yeni istasyon:** arka yokuş patikası, (2960, −1730). Bridge `14_uphill_path` pozu; level-art P03/P04 bölgesi.
- **Düzen:**
  - piyon `BP_PBI_Player`, kamera `BP_PCM_GR_Camera` (FOV 60, piyona 1.8–2.1 m);
  - Enhanced Input ile W tuşu, yürüme hızı;
  - 30 FPS sabit adımlı oyun zamanı, kesintisiz; videolar gerçek hızda;
  - mevcut MediaCapture yolu kullanıldı.

| Yürüyüş | Yön | Süre (oyun) | Yol | Sonuç |
|---|---|---|---|---|
| walk1 | yaw −115 (Bridge pozu, düz) | 9.0 s, 271 kare | 11.3 m | Patikadan çıktı, genç çamların içine girdi; son ~1 s kamera dalların içinde (`walk1/sheet_1fps.png`) |
| **walk2** | **yaw −92** (patika ilk karede ~23° sağa kıvrılıyor) | **13.0 s, 392 kare** | **16.6 m, +2.6 m tırmanış** | Değerlendirme bu yürüyüşe göre |

**Videolar:**
- `walk2/forest_trail_walk2_yaw-92_13s_realtime_s60.avi` (MJPEG; boyut %60, hız gerçek)
- `walk1/forest_trail_walk1_yaw-115_offtrail_realtime_s60.avi`

**Not:** Videoları gerçek zamanlı oynatıp izlemedim. Değerlendirme saniyede bir kare kâğıtlarına, 7–10 s arasının 0.2 s'lik kâğıdına ve dört istasyon karesine dayanıyor.

### 2.1 Gözlemler (walk2)

**Kameranın ağaç dallarına girmesi: VAR**
- ~7.0–9.0 s arasında kamera bir genç çamın içinden geçiyor.
- ~8.0–8.8 s arasında karakter büyük ölçüde görünmüyor.
- 9.0 s'de eğrelti objektifin önünde (`walk2/clip_sheet_7_10s.png`).
- Görüş izi (trace) hiç engel bulmadı, çünkü bitki örtüsünün çarpışması yok. Bu sorun yalnız görüntüden tespit edilebiliyor.

**Patika derinliği**
- İlk 5–6 m iyi: aşınmış iz, sağda şev, solda devrik gövde, yerde güneş benekleri. `walk2/start_forward.png` segmentin en iyi karesi.
- Sonrasında iz kayboluyor:
  - yürüyüş çizgisinin 0.8 m yakınında **21**, 1.5 m yakınında **38** bitki örneği var (zemin örtüsü, eğrelti, çalı, genç çam);
  - 3 m içinde hiç kenar nesnesi (kaya, kök, gövde aktörü) yok;
  - eğim ~4 m boyunca **21–23°**; zikzak veya basamak yok (`trail_audit.json`).

**Orta plan yoğunluğu**
- 3–12 m bandında **708** örnek var. Çoğu benzer boyda: eğrelti türleri, zemin örtüsü, çalılar, 41 genç çam, 37 genç ladin.
- Sayı yüksek ama yapı yok: orta plan bir "yeşil doku" olarak okunuyor, kütle gruplarına ayrılmıyor.

**Doğal ışık**
- En güçlü öğe yerdeki güneş benekleri.
- Ama ışığın bir hiyerarşisi yok: patikada ışık havuzu ya da varılacak bir hedef yok, sis düzgün dağılmış.
- Bitişteki geriye bakışta ev görünmüyor; AGENTS'teki "geriye bakınca sığınak" şartı bu segmentte sağlanmıyor.

**Hareket sırasında kompozisyon sürekliliği**
- Kamera hep arkada sabit; karakter alt-orta üçte biri kaplıyor.
- 6 s'den sonra kareler birbirinin yerine geçebilecek kadar benzer. Yaklaşma → sıkışma → açılma ritmi yok.
- 10–13 s'de kadraj çalılara bakıyor.

**Karakter (kapsam dışı, not):** saç bazı karelerde gürültülü veya kırpışmalı görünüyor.

### 2.2 Performans (DOĞRULANDI)

Stok `csvprofile`, editör PIE'de, viewport 1741×922, ölçekleme ayarları 3, sabit adım; ölçüm yürüyüşün B geçişinde, kayıt kapalıyken alındı.

| Yürüyüş | Kare süresi ort. / p95 / maks | GPU ort. / p95 | Oyun thread'i | Render thread'i | VRAM kullanılan / bütçe |
|---|---|---|---|---|---|
| walk1 | 43.9 / 48.0 / 57.4 ms | 42.4 / 45.7 ms | 15.6 ms | 43.9 ms | 6275 / 7122 MB |
| walk2 | 41.6 / 45.1 / 156.3 ms (tek takılma) | 40.0 / 43.0 ms | 15.6 ms | 37.7 ms | 6335 / 7122 MB |

- Sistem GPU sınırlı; bu, donanım temel raporuyla uyumlu (bitki gölgesi ve VSM payı).
- Editör içi ölçüm; standalone değil. Pilot değişikliklerinin performans etkisi aynı ölçümle karşılaştırılacak.

---

## 3. Kalite pilotu önerisi: arka orman patikası, 16 m'lik segment (ONAY BEKLİYOR)

**Alan:** walk2 hattı, (2960, −1730) → yaklaşık (2900, −3390). Yolun iki yanında 3 m'lik koridor + 12 m'lik orta plan bandı.

**Neden bu alan:**
- Küçük ve tek pakette: bitki örtüsü ile arazi `L_GR_SphirusHouse` içinde.
- AGENTS şartı: dar, kapalı, yokuş yukarı bir orman patikası; yol orman zemininden doğmalı; geriye bakınca sığınak görünmeli.
- Referans ilkelerinin üçü burada sınanabiliyor:
  - The Last of Us Part II: rota okunurluğu;
  - A Plague Tale: insan ölçeğinde zenginlik ve okunur kütleler;
  - Alan Wake 2: orman kapalılığı ve derinlik katmanları.

### 3.1 En önemli 3 görsel eksik ve kök nedenleri

| # | Eksik (referans ilkesine göre) | Kanıt | Kök neden |
|---|---|---|---|
| 1 | **Rota okunurluğu 5–6 m'de kayboluyor.** TLOU2'deki "işaretsiz okunan yol" ilkesi ve AGENTS'teki "kökler, döküntü, kesintili bitki" şartı karşılanmıyor | Yürüyüş çizgisinde 21 örnek 0.8 m içinde; 3 m içinde kenar nesnesi yok; 21–23° tırmanış | Patika yalnız başlangıçtaki zemin ve şev şekliyle tanımlı; serpme bitkiler yürüyüş çizgisine de düşmüş; yolu kenarlardan sınırlayan hiçbir öğe yok |
| 2 | **Gövde ve kamera bitkilerin içinden geçiyor.** Referans oyunlarda oyuncu katı görünen genç ağaçların içinden geçmez; kamera mesh içine girmez | ~2 s kamera genç çamın içinde; eğrelti objektifin önünde | Uzun ve yumuşak bitkiler (genç çam, ladin, çalı) çizgiye 1.5–3 m mesafede; dalları çizgiye taşıyor. Bitki örtüsünün çarpışması yok (oyun için doğru), ama yakın kamerada soldurma da yok |
| 3 | **Orta planda kütle hiyerarşisi, hedef ve geriye bakış yok.** Requiem'in okunur kütleleri ve AW2'nin katmanlı derinliği eksik; AGENTS'teki sığınak görünümü sağlanmıyor | 3–12 m bandında 708, çoğu benzer boyda örnek; yapısal öğeler (25 m içinde 10 ölü gövde, 5 kaya, 3 kök, 4 kütük) görünür bantta değil; geriye bakışta ev yok | Serpme yoğunluğa göre yapılmış, kompozisyona göre değil. Büyük biçimler görüş hattında değil; açıklık ve hedef tasarlanmamış |

### 3.2 Uygulanabilir düzenlemeler

Yalnız mevcut örneklerin yerini değiştirmek:
- **Yeni asset yok, örnek sayısı aynı.** AGENTS'in "önce denetle, sonra yeniden dağıt" kuralına uygun.
- Işık ve arazi değişmiyor.
- Yalnız `InstancedFoliageActor0` içinde örneklerin konumu değişiyor.

| Adım | Düzenleme | Hedef |
|---|---|---|
| E1 iz | 0.8 m içindeki 21 örneğin eğrelti/çalı/çam olanları 0.9–2.0 m'ye, kenarlara, **asimetrik** taşınır (yokuş tarafı daha dolu). Alçak zemin örtüsü ve yaprak döküntüsünün ~%30'u izde kesintili döküntü olarak kalır: temiz kahverengi şerit olmaz | Rota 16 m boyunca okunur |
| E2 açıklık | Dalları çizginin 1.2 m'sine ya da kameranın arkadaki ~2 m'lik yayına giren uzun bitkiler 1.5–3 m dışarı taşınır | Aynı yürüyüşte **sıfır** "kamera bitki içinde" karesi |
| E3 kütle ve hedef | 3–12 m bandındaki genç çam ve ladinlerin ~%30'u 3–4 grupta toplanır; aralarında **bir yukarı görüş hattı** açılır. 10–14 m ileride, mevcut bir ölü gövde + kök + kaya grubu (25 m içindeki örneklerden taşınarak) şeve hedef olarak yerleştirilir. Bitişte 3–5 genç ağaç inceltilerek ev çatısını gösteren **bir geriye bakış penceresi** açılır | Yaklaşma → sıkışma → hedef ritmi; sığınak görünümü |

**Uygulama yolu**
- Kapılı runner `write` işleri; her iş tek bir konuya.
- Önce manifest ve doğrulanmış yedek alınır: `L_GR_SphirusHouse.umap` (`manifest233.py`).
- Her taşınan örneğin özgün transform'u JSON'a yazılır; geri alma bu JSON ya da yedekle yapılır.
- Bilinen tuzak: aynı mesh birden çok FoliageType'ta kullanılıyor (ör. `SM_Pine_Juvenile_01`). Bu yüzden örnekler bileşen ve FoliageType üzerinden seçilir, mesh adına göre değil.
- Runner'ın kayıt koruması, kaydı manifestteki harita ile sınırlar; ABP'ler kaydedilemez.

**Doğrulama** (aynı araçlarla):
- aynı yürüyüş: yaw −92, 13 s, aynı başlangıç;
- aynı dört istasyon karesi;
- CSV performans profili;
- `trail_audit` sayımları;
- üç regresyon görünümü: ev önü, göl, eski orman. Pilotun başka yerden görünüşü bozmadığı kontrol edilir.
- AGENTS gereği: Bridge dışa aktarımı ve `LATEST.json` doğrulaması.

**Kabul ölçütleri**
- *Teknik:*
  - örnek sayısı aynı;
  - yalnız harita kaydedildi;
  - GPU ortalaması en fazla +1 ms;
  - kamera bitki içinde kare sayısı 0.
- *Görsel:* önce/sonra video ve kareler yan yana; segment için kullanıcının verdiği Tier ≥ 3. Kahraman alan sayılırsa Tier 4.

**Riskler**
- Kenara taşınan bitkiler çıplak zemin bırakabilir ("boş" sorunu): döküntü ve zemin örtüsü bu yüzden kısmen yerinde kalıyor.
- Başka açılardan görünen siluet değişebilir: üç görünüm kontrol edilecek.
- Uzun PIE'den sonra editör viewport'unda çizim tuzağı var: Bridge dışa aktarımından önce editör yeniden açılmalı (onay).
- Kameranın bitki içinde soldurulması **pilotun parçası değil**; kamera sahibine ayrı iş.

---

## 4. Onay bekleyen kararlar

1. **ABP geri dönüşü:** 1. bölümdeki seçenek 1 (önerilen) ya da 2.
2. **Pilot E1–E3:** `L_GR_SphirusHouse` içinde yalnız örnek konumları; manifest ve yedek ile; yalnız harita kaydı.
3. **Editörü yeniden başlatma:** ABP seçenek 1 ile birleşebilir; Bridge dışa aktarımı öncesi temiz viewport için.
4. **Kamera ve bitki etkileşimi:** yakın bitki soldurma veya dither; kamera/çevre sahiplerine ayrı iş olarak.

## 5. Eksikler ve doğrulanmamışlar

- Değişiklik sonrası görseller: pilot onaylanmadığı için yok. Bu turda yalnız "önce" seti var: walk2, istasyon kareleri, performans.
- Disk ile bellek arasında tam ABP metin karşılaştırması (geri dönüşten sonra yapılacak).
- Videolar gerçek zamanlı izlenmedi.
- Patika yönü elle seçildi (yaw −92); patika eğrisi tam izlenmiyor (walk2'nin sonunda çalılara yöneliyor).
- Standalone performans ölçülmedi.
- Arazi boya katmanları okunamadı (`editor_layer_settings` erişilemez); arazi düzenlemesi pilotun dışında.
