# SPHIRUS dış dünyası XR2: bütünsel dolaşım, doğal sınırlar ve yer kimliği (kil prototipi)

İzole deneme, kaydedilmedi. Tarih: 2026-10-31. UE 5.8.1, `L_GR_SphirusHouse`, oyuncu kamerası BP_PBI_Player + GraceRanger (kapsül r 30 cm, yarı yükseklik 86 cm; yürünebilir eğim 44,8°; basamak 45 cm).

Bu tur ana haritayı değiştirmedi. Bütün dış alan gerçek Unreal sahnesinde **bellek içinde** yeniden kuruldu, ölçüldü ve sonra **bayt bayt geri alındı**. Kalıcı kayıt için onayınız gerekiyor (bölüm 11).

## Kısa sonuç

| Alan | Durum | Kanıt |
|---|---|---|
| Kök neden: dünya her yöne serbestçe yürünüyordu | **Doğrulandı (BEFORE)** | 60 gerçek girdi denemesinin 58'i hedefe ulaştı. 30 sınır denemesinin 30'u evden 60 m dışarı çıktı. Oyuncu göl tabanından karşıya yürüyebiliyordu. Erişilebilir alan 6,7 ha+ ve harita kenarına kadar uzanıyordu. |
| Kapalı, doğal sınırlı dünya | **PASS (teknik)** | x8'de 30 sınır denemesinin **0'ı** dışarı çıktı (ortalama ilerleme 60,1 → 17,2 m). Erişilebilir alan 0,83 ha'ya indi ve kapalı. Hiçbir sınır görünmez duvar değil: yalnız sığ su sınırı görünmez (bölüm 9). |
| İki ana rota oyuncu hareketiyle | **PASS (A), PARTIAL (B)** | Kil görünümünde, yalnız oyuncu kamerası görüntülerine bakarak yön seçtim. A rotasında 8 kararın 8'i doğru çıktı. B rotasında bir yanlış dönüş oldu (evin köşesinde) ve sık genç ağaç kümesi oyuncuyu geri çevirdi. |
| Kestirmeler | **PASS** | 8 düz çizgi kestirmenin 6'sı doğal engelde durdu. Ulaşan 2'si zaten tasarlanan rota boyunca uzanıyor. Kuş uçuşu oranları 1,01–1,08'den 1,31–1,45'e çıktı. |
| Fazla geçirgen kalan yerler | **Belirlendi** | Vadi tabanı (bilerek açık bırakıldı), batı korusu cebi ve göl batı kıyısı. Ayrıntı bölüm 4.3'te. |
| Kil/nötr ışıkta büyük kütleler ve yer kimliği | **PARTIAL** | İskele/sandal, kaya sekisi, karşı kıyı geri bakışı ve sırt açıklığı güçlü. Batı açıklığı ve karşı kıyının arka yamacı zayıf. |
| Işık, renk, malzeme ve foliage aşaması | **REVIEW_REQUIRED** | Patika toprağı (decal) ve sinematik ışık önerisi gösterildi. Decal tonu soğuk ve yer yer şerit gibi; sınır kayalarının (CliffRock) malzemesi sıcak turuncu-kahve, serin gri taş paletine uymuyor. |
| Görsel ve oyun hissi kabulü | **NOT_TESTED** | Videoları gerçek zamanlı oynatıp izlemedim. Kararlar istasyon görüntüleri, 3'lü bakış şeritleri ve video kare örnekleriyle verildi. |
| Performans | **Anlamlı fark yok** | GPU medyanı: A 40,8 → 37,7 ms, B 40,2 → 39,2 ms (giydirme dahil). VRAM yaklaşık +180 MB. |
| Geri alma | **PASS** | Yükseklik sha1 aynı, foliage 57/8305 aynı, aktörler 768/768 aynı, 0 XR2 aktörü kaldı. Diskteki harita sha1 `70dd481a…` değişmedi. |

---

## 1. Kök neden (BEFORE ölçümü)

- **Hiçbir sınır yoktu.** Analitik yürünebilirlik haritası `maps/CMP_walk_before_vs_x8.png`, sol panel.
  - Bütün çanak ve ötesi yürünebilir.
  - Yürüme açısını aşan eğim yalnız 505 m², bunların hiçbiri sınır oluşturmuyor.
  - Ormanın sırtları yaklaşık 28°: yürünebilir.
- **Gerçek girdi denemeleri.** Karakter W tuşuyla, sabit bir yönde yürüdü. Ağaç gövdesine takılınca bir oyuncunun yapacağı gibi ±35/70/105° yana çekildi, sonra asıl yönüne döndü. Rota takibi yoktu. Sonuç: 60 denemenin 58'i hedefe ulaştı, sınırların 30'u da 30'u da dışarı çıktı. Harita: `maps/CMP_probes_before_vs_x8.png`, sol (kırmızı çizgiler).
- **Göl tabanı yürünebilirdi.** Gölde su hacmi yok (yalnız bir yüzey mesh'i var). Karakter 1,4 m derin suda tabandan karşıya yürüyebiliyor; BEFORE haritasında gölün içinden geçen kırmızı çizgiler bunu gösteriyor.
- **Rotalar biçimle tanımlanmamıştı.** Patikalar yalnız bir boya izi ve hafif bir oluktu. Kenar kütlesi, şev ve görüş hattı onları desteklemiyordu. Kuş uçuşu analizinde her iki hedef arası ormandan dümdüz gidiliyordu: oran 1,01–1,08 (`maps/CMP_geo_before_vs_x8.png`).
- **Orman eşit aralıklıydı.** Ağaçlar yaklaşık 7 m aralıkla serpilmişti; koru, açıklık ya da kenar hiyerarşisi yoktu (R1 teşhisi, değişmemişti).

## 2. Masterplan: dünyanın gerçek yapısı

Görsel: `maps/XR2_x8_MASTERPLAN.png` (kuzey yukarıda, 10 m ızgara).

**Coğrafi omurga:** arka ormanın yükselen vadisi → evin sekisi → göle iniş → gölet çanağı → çanağı kapatan sırtlar.

- **Ev sekisi.** Ev hâlâ hafif bir yükseltide. Arka bahçe yamaca oyulmuş gibi okunuyor: arkasında bir "bahçe şevi" var, tek çıkışı doğudaki kapı.
- **Dünya sınırı (485 m).** Çanağın dış yamaçlarına işlenmiş dik bir şev (2,5–4 m, yürüme açısının üstünde).
  - Rotaların gördüğü yerlerde şev kaya (27 CliffRock/PineCliff) ve devrik ağaçla (27) sıvalı.
  - Sınır her hedefin 8–15 m arkasından geçiyor; oyuncu bir duvara değil, yükselen ormana bakıyor.
- **İç sınırlar:**
  - **Göl doğu kıyısının kaya sekisi.** A rotasını su ile kaya arasına sıkıştırıyor ve doğudan B rotasına kestirmeyi kesiyor.
  - **Vadi duvarı (W1).** Batı korusunu kuzey vadisinden ayıran kaya bandı.
  - **Bahçe şevi (W0).** Bahçeden vadiye kestirmeyi kesiyor.
  - **Sığ su sınırı.** Oyuncu suya diz boyu girebiliyor ama göl tabanından karşıya geçemiyor.

**İki ana rota:**

| Rota | Sıra | Uzunluk / en dik |
|---|---|---|
| **A: Göl Yolu** | Veranda → küçük ön patika → **iskele (sandal)** → kaya sekisi boyunca dar kıyı rafı (sıkışma) → dere ağzı → güney kıyısı → **karşı kıyı açıklığı** (kahraman meşe, oturma kayası, suyun üstünden eve geri bakış) | 101 m / 11° |
| **B: Sırt Patikası** | Ev köşesi → bahçe kapısı → **kaya boğazı** (r6: mahmuz uçlarında kaya çıkıntıları) → çukur geçişi → **tırmanış** (r6: iki çalı kütlesinin arasındaki doğal boşluktan) → **sırt açıklığı** (kahraman meşe, kaya oturağı, eve geri bakış) | 89 m / 16° |

**Bağlayıcılar:** veranda ↔ ev köşesi, ev köşesi ↔ kıyı. Bunlar evin önünde küçük bir döngü oluşturuyor.

**Keşfedilebilir yan bölgeler** (her biri dürüst bir sonla biter):
- kuru dere cebi (kaya basamağının altı);
- doğu koyu cebi;
- eski kesim açıklığı (kütük, kesme bloğu);
- göl batı kıyısında sazlık "zor iz" (dar, kesik, isteğe bağlı döngü).

**Doğal olarak geçilemeyen alanlar:**
- dış sınır;
- kaya sekisinin doğusu (doğu terası);
- ana koru (bahçe şevinin arkası);
- rüzgâr devriği kümeleri: 9 küme, 36 gövde, kestirme hatlarına konumlandı;
- KB kaya tepesi.

**Orman kompozisyonu:**
- Ağaçlar eşit serpme yerine yoğun korulara (10 koru) toplandı.
- Patikalar, açıklıklar ve geri bakış koridorları boşaltıldı.
- Kıyılar seyreltildi, böylece okunur zemin düzlemleri açıldı.
- Yapı aşamasında yeni ağaç eklenmedi. 44 büyük ağaç, 51 genç ağaç, 42 çalı, 21 sert obje ve 163 yer örtüsü taşındı; 3061 instance yeni zemine oturtuldu. Bileşen başına instance sayısı aynı kaldı.
- Yalnız giydirme aşamasında (bölüm 5), karşı kıyı arkasına 6 ağaç ve 10 eğrelti/genç ladin aktör olarak eklendi.

## 3. Gerçek sahnede ne kuruldu (x8, bellek içi)

- **Arazi** (−3,0 ile +6,0 m arası, 2,15 ha):
  - dünya sınırı şevi;
  - R1 arka formları ve r6'nın daha cesur mahmuz uçları (+4,2/+5,2 m);
  - bahçe şevi, vadi duvarı, kaya sekisi;
  - kuru dere cebi, karşı kıyı terası;
  - rotalarda aşınmış, eğim sınırlı tabanlar (8–12 cm).
- **Yapısal aktörler** (203, `XR2_*`, klasör `XR2_Trial`):

  | Tür | Adet |
  |---|---|
  | sınır kayası | 27 |
  | sınır devriği | 27 |
  | vadi duvarı kayası | 5 |
  | bahçe şevi (ForestEmbankment + devrik) | 3 + 7 |
  | r6 çıkıntıları | 6 |
  | rüzgâr devriği | 36 |
  | tek kütük | 14 |
  | yer işaretleri (sandal, 2 oturma kayası, kesme bloğu) | 4 |
  | görünmez sığ su sınırı | 74 |

  Bütün mesh'ler projede zaten vardı (PineForestPack, Fishermans_Cabin). Satıcı orijinallerine dokunulmadı.
- **Kamera kuralı (VMP v7 dersi):** kütükler ve küçük objeler GR kamera kanalını yok sayıyor. Büyük kayalar kamerayı engellemeye devam ediyor.
- **Foliage:** 55 bileşen yeniden dağıtıldı, sayılar aynı.

## 4. Kanıt

### 4.1 Gerçek girdi ile serbest hareket denemeleri (60 deneme, aynı başlangıç noktaları ve yönleri)

| Set | BEFORE: ulaşan / ort. ilerleme | x7 | **x8 (son)** |
|---|---|---|---|
| Sınır (30 deneme, 60 m dışarı) | 30 / 60,1 m | 0 / 16,5 m | **0 / 17,2 m** |
| Rota yanından kaçış (22 deneme, 25 m) | 20 / 24,0 m | 4 / 14,3 m | **7 / 16,7 m** |
| Kestirme (8 deneme, düz çizgi) | 8 / 67,5 m | 2 / 40,4 m | **2 / 40,6 m** |

Ortalama kaçınma manevrası deneme başına 0,4–1,0'dan 4,6–6,9'a çıktı: orman artık "her yöne aynı kolaylıkta" değil.

- **x8'de ulaşan 2 kestirme:** doğu kıyısı → kaya boğazı ve dere ağzı → bahçe kapısı. İkisinin düz çizgisi de A → ev köşesi → B rotası boyunca uzanıyor; yani rota zaten en kısa yol.
- **Ulaşan 7 yan kaçış:**
  - 4'ü vadi tabanında (B tırmanışının iki yanı, bilerek açık bırakılan "vadi odası");
  - 1'i iskelenin batısında (sazlık iz);
  - 1'i güney kıyısında, A rotasının güneyi (devrik kümesinin yanından 25 m);
  - 1'i B'nin başında, kapının batısında.

Haritalar: `maps/CMP_probes_before_vs_x8.png`, `maps/AFTER_x7_probes.png`. Ham kayıtlar: `data/probe_*_log.json`.

### 4.2 Analitik yürünebilirlik ve kuş uçuşu

| | BEFORE | x8 |
|---|---|---|
| Evden erişilebilir alan | 6,7 ha+ (harita kenarına kadar, sınırsız) | **0,83 ha, kapalı** |
| Yürüme açısını aşan eğim | 505 m² | 1923 m² (sınır ve iç şevler) |
| Batı → sırt (yol / kuş uçuşu) | 1,07 | **1,31** (bahçe ve B rotası üzerinden) |
| Bahçe → tırmanış | 1,08 | **1,45** |
| Sırt → bahçe | 1,05 | **1,37** |
| İskele → karşı kıyı | 1,23 (analiz derin suyu kapalı sayıyor; PIE'de BEFORE'da göl tabanından geçilebiliyordu) | **1,43** |

Görsel: `maps/CMP_geo_before_vs_x8.png`. BEFORE'da yollar ormandan dümdüz gidiyor; x8'de yalnız tasarlanan rotalardan geçiyor.

### 4.3 Oyuncu gözüyle yön bulma (kil, nötr ışık, yönlendirme çizgisi/işaret yok)

Yöntem:
- PIE açık kaldı. Her adımda oyuncu kamerasından sol −55° / orta / sağ +55° görüntüsü alındı.
- Yönü yalnız bu görüntülere bakarak seçtim; sonra karakter gerçek W girdisiyle o yöne yürüdü.
- Şeritler `navigation_clay/strip_NN.jpg`, kayıt `data/nav_log_clay.json`.
- **Sınır:** yön seçen benim ve haritayı tasarlayan da benim. Bu yanlılık testi zayıflatır; gerçek bir oyuncu testi yerine geçmez (REVIEW_REQUIRED).

**A rotası** (verandadan karşı kıyıya 102 m, 8 yürüyüş, hepsi hedef mesafeye ulaştı, 0 kaçınma):

| Adım | Görüntüde okunan | Seçim |
|---|---|---|
| Veranda | Ortada su ve kıyıda sandal; solda kayalar arasında aydınlık bir yarık | Sandal (orta) |
| İskele | Önüm su; solda kaya çıkıntıları arasından kıvrılan aydınlık iz | Sol |
| Kaya sekisi girişi | Sol kaya duvarı, sağ su, ortada dar kıyı rafı | Orta (tek seçenek) |
| Sekinin ortası | Yol kayanın ardından sağa kıvrılıyor | Sağ |
| Dere ağzı | Solda yukarı açılan cep (kuru dere), sağda kıyı | Sağ-ileri (kıyı); cep okunuyor |
| Güney kıyısı | Solda devrikli koyu orman, sağda aydınlık kıyı | Sağ |
| Güney kıyısı 2 | **Belirsiz:** kameranın önünde çalı, üç yön benzer | Orta-sağ |
| Açıklık girişi | **Kusur:** kamera yola çok yakın, alçak dallı bir ağacın tepesine girdi | 5 m ileri |
| Karşı kıyı | Açıklığın kendisi zayıf okunuyor; **geri bakış güçlü:** ev suyun öbür yanında çerçeveli | — |

**B rotası** (verandadan sırta):

| Adım | Görüntüde okunan | Seçim |
|---|---|---|
| Veranda (doğu) | Evin yanından yükselen koridor | Orta-sol |
| Ev köşesi | Çalı kütleleri arasında yukarı açık koridor | Orta, **yanlış**: patika burada kuzeye kıvrılıyor; dümdüz devam edip güney mahmuzu üstündeki sık genç ağaçlara girdim |
| Mahmuz üstü | Her yön sık; kamera dalların içinde; ev geride görünüyor | Geri çekildim (5 m batı) |
| Bahçe kapısı | Solda çit ve bahçe; ortada kuzeye koridor | Orta, doğru |
| Kaya boğazı öncesi | Ortada yol; sağda aydınlık kayalı cep (doğu koyu) | Orta |
| Boğaz sonrası | **Orta düzeyde belirsiz çatal:** sol-ortada çukura inen iz, ortada sağ-yukarı aydınlık yamaç | Sol-orta, doğru |
| Tırmanış başı | Genç ağaç kümeleri arasında yükselen koridor | Orta-sağ |
| Tırmanış | Tepede aydınlık açıklık (hedef ışığı) | Orta |
| Sırt | Geriye bakış: vadi iki kütle arasından aşağı iniyor | — |

**Belirsiz kalan karar noktaları ve nedenleri:**
1. **Ev köşesi (B):** patikanın kuzeye dönüşünü hiçbir kütle ya da şev vurgulamıyor. Düz devam eden açık koridor mahmuza çıkıyor. Düzeltme: dönüşün dışına (doğuya) bir kaya ya da gövde kümesi koymak ve mahmuz eteğini daraltmak.
2. **Güney kıyısının gölgeli bölümü (A):** kamerayı kapatan çalılar ve birbirine benzeyen yönler. Düzeltme: yol kenarı çalılarını 2 m geri itmek, ileride bir odak göstermek (açıklıktaki meşenin gövdesi).
3. **Boğaz sonrası çatal (B):** çukur geçişi ile doğu yamacı eşit güçte. Düzeltme: doğu yamacına alçak bir devrik ya da kaya koyup ışık bandını çukura vermek.
4. **Karşı kıyı açıklığının kimliği:** kahraman meşe girişten okunmuyor. Düzeltme: meşeyi açıklığın girişine, görüş hattına almak.

### 4.4 Karar noktası görselleri (önce/sonra, kil ve ışıklı)

13 karar noktası; her biri ileri, ±90° ve geri bakışla, oyuncu kamerasından. Karşılaştırmalar: `compare/cmp_clay8_*.jpg` ve `compare/cmp_lit_*.jpg` (üst BEFORE, alt AFTER). Ham kareler: `stills/`.

Belirgin kazanımlar:
- **D01 veranda:** sandal, ilk hedef olarak görüş hattının ortasında.
- **D02 ev köşesi:** önce kamera çam dallarına gömülüydü, şimdi açık bir koridor var.
- **D03 iskele:** yol, kaya şevi ile su arasındaki bir raf olarak okunuyor.
- **D06 karşı kıyı (ileri):** ev suyun üstünden çerçeveli; sığınağa geri bakış.
- **D10 tırmanış:** iki kütle arasında yükselen koridor; geri bakışta çatı.
- **D11 sırt:** kaya arkalı, kapalı bir oda.
- **D13 bahçe:** şev ve devrikle kapanan bir oda.

Zayıflar:
- **D06 geri bakış:** açıklığın arkası çıplak yamaç. x8 düzeltmesi kili değiştirmedi; giydirme aşamasında 6 ağaç ve eğrelti eklendi.
- **D12 batı:** kesim açıklığı kimliksiz.
- **D04 geri:** CliffRock'un turuncu-kahve malzemesi paletle çatışıyor.

### 4.5 Normal hızlı rota videoları

- `video/XR2_routeA_*` ve `XR2_routeB_before_vs_after_clay_vs_lit_part1..4.avi`: BEFORE ışıklı | AFTER kil (nötr ışık) | AFTER ışıklı, yan yana. Aynı kare aynı oyun zamanı.
  - Kayıt sabit adımlı 30 FPS; kareler ikide bir seyreltildi ve 15 FPS'de oynatılıyor, yani **gerçek hız**.
- `video/XR2_routeA_after_dress_cinematic_part1..3.avi`: giydirme ve sinematik ışık önerisi.
- Bu videolarda yürüyüş rota çizgisini izleyen bir sürücüyle yapıldı (görüntüleme amaçlı). Rotanın işlevi bölüm 4.1–4.3'te bundan bağımsız test edildi.
- **Videolar gerçek zamanlı izlenmedi.** Yalnız kare örneklerine baktım.
- Karelerde kırmızı bir motor uyarısı görünüyor (Lumen yüzey önbelleği/bellek baskısı). BEFORE B karelerinde de var, bu turla ilgili değil.

## 5. Işık, renk, malzeme ve foliage: yapı sinematik dünyaya nasıl dönüşür

Karşılaştırmalar: `compare/cmp_look_*.jpg`. Her biri üç panel: üretim ışığı (giydirmesiz) | üretim ışığı + giydirme | sinematik öneri + giydirme.

- **Patika malzemesi.**
  - Landscape ağırlık haritası bu sürümde Python'dan okunamadı (`render_weightmap` false döndü), bu yüzden boya katmanına dokunmadım.
  - Bunun yerine 141 adet `Forest_Ground` toprak decal'i kullandım: eğime hizalı, 30 cm projeksiyon, kesik aralıklı.
  - Patika artık malzemede de okunuyor (en belirgin tırmanışta).
  - **Sorun:** ton soğuk-mavimsi ve yer yer sürekli bir şerit gibi duruyor. Kalıcı çözüm landscape'te bir patika katmanı; eski izin silinmesi de orada yapılmalı.
- **Foliage.** Karşı kıyı arkasına bir köknar/çam korusu ve eğrelti eteği eklendi (giydirme aşaması). Kalıcı sürümde bunlar spawn edilmiş aktör olarak değil, foliage sistemine taşınmalı.
- **Işık.** Sinematik öneri VMP'nin seçtiği TRIAL2 (güneş −36°, 2600 lux, gök 1,4, sis 0,010).
  - Tırmanışta dağınık ışık lekeleri ve sırt açıklığında hedef ışığı veriyor.
  - Göletteki ışık hüzmeleri azalıyor; bu VMP'den bilinen bir ödünleşme.
  - Üretim ışığı korunuyor. Bu yalnız bir öneri.
- **Renk ve malzeme uyumu:**
  - CliffRock malzemesi sıcak turuncu-kahve; projenin serin, ıslak gri taş paletine uymuyor. Proje sahipli bir MI kopyasıyla (satıcı orijinali değişmeden) tonu kırılmalı.
  - Devrik gövdelerin bir kısmı soyulmuş ve açık renkli; nemli, koyu ve yosunlu varyantlar tercih edilmeli.

## 6. İterasyonlar (offline analiz + motor)

| Sürüm | Bulgu | Düzeltme |
|---|---|---|
| x1 | Dünya sınırı çalışıyor; ama 70 kütük eşit serpilmiş (eleştirilen "rastgele serpme" deseni) | x2: 9 rüzgâr devriği kümesi, kestirme hatlarına |
| x2 | Batı korusu vadiye açık: batı → sırt oranı 1,18 | x3: vadi duvarı (W1, kaya bandı) |
| x4 | Bahçenin kuzeyindeki kütük zincirinde boşluklar: bahçeden vadiye kestirme | x5: bahçe şevi (W0) |
| x5 | Şevin yarım düzlemi hattın sonunda bitmiyordu, B rotasını kesti | x6: uç ve başlangıç sönümü |
| x7 (motor) | Kil ve ışıklı görüntüler + 60 deneme. Karşı kıyı arkası düz bir şev duvarı gibi | x8: daha geniş ve yumuşak açıklık, arkaya kaya |
| x8 (offline) | Rastgele bir devrik gövde B rotasının üstüne düştü (geodezik kontrol yakaladı) | Bütün kütüklere "yola uzanma" kontrolü eklendi |
| **x8 (son, motor)** | Bütün kanıt seti | — |

Motor uygulamasında bir tuzak: iş içi yükseklik geri okuması sıfır döndü (R1'de de görülen render target zamanlaması). Arazinin doğru yazıldığı ayrı bir dışa aktarmayla doğrulandı (0 fark). Geri okumaya yeniden deneme eklendi.

## 7. Güncellenmiş r6 alternatifleri (bütünsel dolaşıma göre)

Haritalar: `maps/alt_r6A.png`, `alt_r6B.png`, `alt_r6C.png`.

| Alternatif | Dolaşım | Artı | Eksi |
|---|---|---|---|
| **r6-A (uygulandı)** Göl döngüsü | Doğuda ana göl yolu, batıda zor ve isteğe bağlı sazlık izi; arka patika bahçe kapısından | Göl çevresinde geri dönüşsüz bir döngü; ev–göl bağlantısı küçük bir ev döngüsüyle çözülüyor | Batı kıyısı da bir geçit gibi okunabilir (4.1'deki yan kaçış) |
| **r6-B** Doğrusal | Batı kıyısı sazlık ve devrikle kapalı, göl yolu karşı kıyıda biter | En net hiyerarşi, en kolay okunur | Geri dönüş aynı yoldan; keşif azalır |
| **r6-C** Büyük döngü | Sınır doğu sırtının dışına taşınır; sırttan doğu sırtı boyunca kuru dereye inen ikinci bir yol | Dünya tek bir büyük döngü; sırt bir çıkmaz değil | En pahalısı (yeni arazi ve sınır); kaya sekisinin kestirme kesme işlevi yeniden kurulmalı |

**r6 kalemlerinin durumu:**

| Kalem | Durum | Açıklama |
|---|---|---|
| 1. Mahmuz uçlarına büyük kaya | **Yapıldı** | 6 çıkıntı; uçlar +4,2/+5,2 m |
| 2. Tırmanışı çalı kütlesini koruyarak geçirmek | **Yapıldı** | İki kütle arasındaki doğal boşluktan |
| 3. Sırta kahraman ağaç ve çerçeve | **Yapıldı** | Meşe + kaya oturağı; geri bakış kilde okunuyor |
| 4. Patika boya katmanı | **NOT_TESTED** | Python ağırlık haritası API'si başarısız; decal ile gösterildi |

Ev ve göl bağlantısı aynı masterplan içinde çözüldü: iskele ilk hedef, kıyı rafı sıkışma, karşı kıyıdan sığınağa geri bakış.

## 8. Performans

CSV profiler, rota yürüyüşü, ışıklı, pass B (yakalama kapalı). Değerler p50 / p95, ms.

| Koşu | Kare | Oyun iş parçacığı | GPU | VRAM MB | Sahne instance |
|---|---|---|---|---|---|
| BEFORE A | 42,1 / 48,4 | 18,9 / 23,2 | 40,8 / 46,0 | 6847 | 9361 |
| AFTER A (giydirme dahil, yeniden ölçüm) | 39,4 / 52,7 | 17,1 / 20,2 | 37,7 / 50,5 | 7046 | 9788 |
| BEFORE B | 41,8 / 48,3 | 18,2 / 22,2 | 40,2 / 46,0 | 6719 | 9361 |
| AFTER B (giydirme dahil, yeniden ölçüm) | 40,8 / 46,7 | 15,5 / 17,3 | 39,2 / 45,1 | 6900 | 9788 |

İlk AFTER B ölçümünde GPU +20 ms çıktı, ama artış rota boyunca her yerde eşitti; yani konuma bağlı değildi. Yeniden ölçümde artış kayboldu: geçici bir yüktü (büyük olasılıkla yeni mesh'lerin ilk kullanımı). İki ölçüm de `data/` altında.

## 9. Açık sorunlar ve riskler (dürüst liste)

- **Görünmez sığ su sınırı (74 küp).** Yalnız Pawn kanalını engelliyor; kamera ve görüş etkilenmiyor. Su doğal bir sınır, ama bir oyuncu kıyıda "neden suya giremiyorum" diye hissedebilir. Bir yüzme ya da derin su davranışı yoksa sektör standardı budur. Alternatifi gerçek bir su hacmi.
- **Kil görünümünde dik şev yüzleri** (kaya yokken) düzgün, sıvasız yüzeyler gibi okunuyor. Işıklıda eğime bağlı "Cliff" dokusu geliyor, yine de kaya ve foliage sıvası artırılmalı.
- **Kamera dallara giriyor.** Açıklık girişinde ve güney mahmuzunda yola yakın genç ağaçlar var. Yol kenarı temizliği kamera tarafında 3 m olmalı.
- **Sınır ve iç barikat kütükleri spawn edilmiş aktörler.** Kalıcı sürümde foliage tiplerine (HISM) taşınmalı.
- **Patika malzemesi geçici** (decal). Asıl çözüm landscape boya katmanı.
- **NOT_TESTED:**
  - gamepad;
  - 60 FPS ve gerçek FPS'de dolaşım hissi;
  - gece ve diğer ışık durumları;
  - bilgisiz gerçek bir oyuncuyla test.

## 10. Güvenlik ve geri alma

- **Kayıt:** hiçbir paket kaydedilmedi. Her yazma işi map manifesti (`vmp_map`, yedek sha1 `70dd481a…`) ve tek kilit sahibiyle (`xr2`) yapıldı. PIE sırasında yazma yok.
- **Sıra:** x7 uygula → geri al → x8 uygula → giydir → geri al.
- **Son doğrulama** (`data/restore_verify.txt`): yükseklik haritası sha1 aynı, foliage 57 bileşen / 8305 instance aynı, aktörler 768/768 aynı, XR2 aktörü 0. Işık sahipleri `look_variant restore` ile geri döndü.
- **Harita bellek içinde "dirty"** (işlem kayıtları yüzünden), içerik orijinal. **Editörü kapatırken "Don't Save" seçin.**
- **Disk:** C: sürücüsünde boş alan bu tur sırasında 7,7 GB'a kadar düştü. Ham video kareleri silindi; şu an yaklaşık 21 GB boş. Editör ve otomatik rig işleri için 30 GB+ önerilir.

## 11. Kalıcı kayıt için onay

Önerim, kalıcı kaydı iki adımda yapmak:
1. x8 yapısını (arazi, foliage yeniden dağıtımı, yapısal kütleler) **bir veri katmanı ya da alt seviye** olarak kaydetmek. Arazi ana haritada olduğu için ana harita paketine yazılır; manifest ve yedek hazır.
2. Belirsiz 4 karar noktasının düzeltmelerini (bölüm 4.3), CliffRock tonunu ve patika boya katmanını ayrı bir tur olarak yapmak; ardından AGENTS'ın istediği Bridge export ve `LATEST.json` doğrulaması.

Hangisini istediğinizi söyleyin. Seçenekler:
- **(a)** x8'i şimdi kaydet;
- **(b)** önce düzeltmeler (x9), sonra kayıt;
- **(c)** r6-B ya da r6-C yönünde yeni bir deneme.

## Dosyalar

| Klasör | İçerik |
|---|---|
| `maps/` | masterplan; önce/sonra deneme, yürünebilirlik, geodezik ve kil haritaları; x7 denemeleri; r6 alternatifleri; geniş plan |
| `compare/` | 13 karar noktası × kil/ışıklı önce/sonra, 6 ışık/giydirme karşılaştırması, iterasyonlar |
| `navigation_clay/` | yön bulma şeritleri (sol / orta / sağ) |
| `stills/` | oyuncu kamerası kareleri (ileri ve geri; BEFORE/AFTER, kil/ışıklı/giydirme/sinematik) |
| `video/` | 11 AVI parçası (gerçek hız) |
| `data/` | deneme kayıtları, deneme tablosu, geodezik, yürünebilirlik, plan/spawn/apply/restore, performans, yön bulma kaydı, varlık ölçümleri |
| `tools/` | `xr2_design.py` (masterplan → arazi, foliage, kütleler), `xr2_apply.py` (bellek içi uygula / giydir / geri al), `xr2_probe.py` (serbest hareket denemesi), `xr2_nav.py` + `nav.sh` (oyuncu gözüyle yön bulma), `xr2_views.py`, `xr2_walkmap.py` + `xr2_geodesic.py` (analitik geçirgenlik), `xr2_chain.sh`, medya ve paket betikleri |
