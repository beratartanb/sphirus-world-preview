# SHME V2.22: doğal başlangıç, ölçülü yeniden hızlanma ve bedene yakın kamera (2026-10-22)

**Taban:** V2.21 üretimi (commit `d6fe690`). UE 5.8, yalnız Blueprint. Harita `L_GR_SphirusHouse`.

## Ölçüm ve kanıt düzeni

- **Ana kanıt sabit adımlı editördür** (`-UseFixedTimeStep -FPS=N`). Koşular deterministik, aynı girdiyle tekrarlanır.
  - Bu sürümde bir tuzak bulundu: bellek nedeniyle yeniden başlayan editör gerçek zamana dönüyordu.
  - Önlem: bütün A/B partileri `runfps.sh` ile koşuldu ve her karşılaştırmada `dt max` kontrol edildi.
- **Beden karakterin kendi çerçevesinde ölçüldü** (`body222.py`):
  - baş, göğüs ve eller görünen pelvise göre (ileri / sol / yukarı);
  - eksenler aktörün yönü; böylece dünyadaki yön değişimi çıkarılmış, yalnız bedenin kendi salınımı kalmıştır.
- **Klipler kendi kök uzayında okundu** (`clipscan222.py`). Hangi klibin ne zaman baskın olduğu, harness telemetrisindeki CP başlangıç saatinden alındı (`CP_StartEvalTime`).
  - Arka planda aranan Motion Matching klibi ile ekranda görünen poz karıştırılmadı. Bu ayrımla, eski başlangıçta görünen pozun MM'den değil CP başlangıç klibinden geldiği gösterildi.
- **Ayak teması:** `contact221` ile ayak başına net kayma / sürükleme yolu. Ayaklar toplanmadı.
- **Kamera:** `cam221` (FOV, sıçrama, sarsıntı, çerçeve, adım), `camcol221` (koridorda duvara girme).
- **Görüntüler:** normal hız GIF / AVI. ⅓ hız AVI yalnız inceleme içindir. Kareler kesilmedi; PIE'ye özel kil test görünümü kullanıldı.
- **Görsel değerlendirme teknik değerlendirmedir. Kullanıcının hareket üslubu ve kontrol hissi kabulü verilmiş sayılmaz.**

## Repertuvar sınıflandırması (bu sürümde incelenenler)

| Hareket | Sınıf | Kanıt |
|---|---|---|
| Rahat idle | korundu | Değişmedi. Başlangıç onun gerçek oyun içi karesinden (68 s) üretiliyor |
| Rahat idle → yürüyüş başlangıcı | **yeni hareket üretildi** (ayak planı V2.8'den; üst gövde, başlatma eğilimi ve ilk adım açıklığı yeniden tasarlandı) | Bölüm 1 |
| Durduktan hemen sonra yeniden yürüme | yeni başlangıçla düzeldi | Sağ ayak 37 → 5.9 cm |
| Yerinde dönüş → W | yeni başlangıçla iyileşti | Sağ 6.9 → 5.4 cm. Erken W değişmedi (7.8 / 12.0) |
| Kısa dokunuşlar | **açık** | Bölüm 1, kalan kusurlar |
| Yürüyüş / tempolu / depar döngüleri | korundu (incelendi) | Depar döngüsünün kolları yüksek (eller 41 cm'e kadar); bu sürümde değiştirilmedi |
| Duruşlar (V2.8 faz duruşları) | korundu | — |
| Depar → kesiş → ters → yeniden hızlanma | **kaynak yeniden düzenlendi** (bacak ve kök korundu, üst gövde yeni) | Bölüm 2 |
| Erken ters / toparlama (V2.21 tutma) | korundu | Bütün çıkışlar V2.21 ile aynı |
| Kesiş → S, kesişte bırakma, W → S tam ters | açık | V2.21'deki gibi |
| Yan / geri / çapraz başlangıçlar | korundu | `wstart` V2.21 ile eşit (L 12.3, R 2.3 → 4.6) |
| Zıplama / iniş | **incelenmedi** (NOT_TESTED) | — |
| Arazi gövde tepkisi | korundu (V2.21) | Tümsek üzerinde adımlama açık (pilot rotada 34–48 cm) |
| Kamera | runtime düzeltildi (yakınlık) | Bölüm 3 |

---

## 1. YÜRÜYÜŞ BAŞLANGICI

**Doğrulanan neden: kaynak performans.**
- Üretimde başlangıç, CP başlangıç dalının oynattığı `A_LS_M_Relaxed_Walk_Start_F_L/R` klibidir.
- Kök uzayında bu klip öndeki eli 34–38 cm ileri ve 14–15 cm yukarı kaldırıyor. Yürüyüş döngüsünde aynı el 25–29 cm ileride ve en fazla 1–2 cm yukarıda.
- Oyunda sağ el +38 cm ileri, +12 cm yukarıda tutuluyor; ilk salınım 0.6 s sürüyor. Ardından döngüye girerken el 0.2 s içinde 36 cm "atlıyor".
- Kollar, yürüyüşten önce farklı bir poza taşınmış oluyor.
- Daha önce üretilen V2.8 başlangıcı (üretimde değildi) kolları döngü sınırında tutuyor ama topuk vuruşu pozuna donuyor. Bu nedenle kol 0.6 s ileride park hâlinde kalıyor.

**Gerçek değişiklik: yeni başlangıç klipleri** `A_SHM222_WalkStart_L / _R` (`gen222_start.py`).
- **Adımlama, kök yolu ve zamanlama** V2.8'in temas planlı başlangıcından alındı:
  - kurulu mesafe saati bu kök eğrisine bağlı;
  - ağırlık aktarımı, ayak 0.26 s'de kalkıyor, ilk topuk vuruşu 0.72–0.75 s'de;
  - bunlar insanın yürüyüş başlatma zamanlamasıyla uyumlu.
- **Kollar:** faz uyumlu sanal döngü saatiyle hareket ediyor. Adım atan ayağın parmak kalkışından topuk vuruşuna kadar karşı kol bacakla birlikte öne geliyor. Genlik idle'dan döngüye tek yönlü artıyor: kol park etmiyor, ikinci kez açılmıyor.
- **Başlatma eğilimi:** spine_01'de yanal eksen etrafında 6°, ~0.35 s'de tepe; topuk vuruşu + 0.3 s'de söner. Ölçülen sorun: oyun içi idle'dan başlarken gövde 0.2 s'de 4–5° geriye kayıyordu.
- **İlk adım açıklığı 10 cm** (V2.8'de 7 cm). Oyunda ayak 4–7 cm'den süpürüyordu.
- **Duruş genişliği farkı** (~18 cm) ayak yerden kalktıktan sonra kapatılıyor.
- **Kaynak idle karesi:** oyunun başlangıç öncesi idle zamanı 68 s (7 s değil; iki kare arasında 5° gövde farkı var).

**Önce → sonra** (`d_walk`, sabit 30, karakter çerçevesi):

| Ölçü | Üretim (V2.21) | V2.22 |
|---|---|---|
| Başlangıçta sağ el | +38 ileri / +12 yukarı, 0.6 s tutuluyor | 0 → +6 → +13 → +8 → döngü; yukarı ≤ 1 cm |
| Döngüye geçişte el sıçraması | 36 cm / 0.2 s | yok (sürekli) |
| Gövde eğimi | 9 → 17° | 10.8 → 8.7 → 14 → 18° (öne düşüş) |
| El aralığı (ileri) | L 30.7 / R 45.9 cm | L 25.5 / R 21.2 cm |

- Ayak teması:
  - Yeniden yürüme R 37.0 → 5.9 cm.
  - Yerinde dönüş → W R 6.9 → 5.4 cm.
  - Gerçek harita 1 R 18.8 → 10.2 cm.
  - Düz başlangıç L 5.4 → 6.4 cm (≈1 cm kötü).
  - Çok yönlü başlangıç eşit.
  - Dokun-tut L 36.7 → 25.4 cm.
- FPS:
  - 20 / 60 / 120'de beden aralıkları aynı (eğim 7.9–18.3).
  - Yeniden yürüme 20 FPS'de R 12.2, 60 FPS'de R 5.8 cm.

**Diğer hareketlere etkisi.**
- Kısa dokunuşlar başlangıç olmadan önce bırakılıyor ve sonuç V2.21 ile aynı. Yalnız ilk W dokunuşunda L yolu 13 → 23 cm.
- Pilot rotada ayak fazı değiştiği için 20 cm'lik tümsek tırmanışındaki topuk kayması diğer ayağa geçti (o: R 23.4 / yol 34.3; p: L 20.9 / 34.2). Kaynağı tümsek üzerinde adımlamadır (açık), başlangıç değildir.

**Üretimde:** **EVET.**
- ABP `SHM28_StartMode 1`.
- `SHM28_StartL / _R` = V2.22 klipleri.

**Kalan kusurlar**
- **Kısa dokunuşlar (açık).**
  - Bırakınca SHME başlangıç-aktarım ailesi (4) 0.65 s açık kalıyor. Motion Matching sıfır hızda bir aktarım adımı seçiyor (ör. W dokunuşuna geri-sol adım) ve ayak 8–26 cm geziniyor.
  - Bu ailenin seçimini kapatan kapı (`SHM222_TapGate`) denendi. Aktarım adımı kalktı ama MM ayakları 19 cm uzakta olan bir idle karesine atladı; dokunuşlar kötüleşti.
  - Kapı reddedildi (0). Gerekenler: idle seçimine basılı ayak sınırı, ya da kök hareketli `am_*_Idle_Step_*` yerleştirme adımları.
- **Yan / geri / çapraz başlangıçlar** aynı yeni tasarımla yeniden üretilmedi. Mevcut CP / SHME yollarıyla çalışmaya devam ediyor.

**Geri alma**
- `SHM28_StartMode 0`.
- ABP kopyaları: `checkpoint/pre_promo/`. V2.8 klipleri dokunulmadı.

---

## 2. DÖNÜŞ SONRASI İTİŞ VE GENEL BEDEN SÜREKLİLİĞİ

**Doğrulanan neden: kaynak performans.**
- Dönüşten sonra yeniden hızlanma, V2.16–2.19'da kapsül yoluna yeniden oturtulmuş `SHM216_RevTurn_*` klipleridir.
- **Bacaklar, kök ve temaslar** üretimde doğrulanmış durumdaydı.
- **Üst gövde ise satıcı depar dönüşünün performansıydı:**

  | Ölçü | RevTurn | Depar döngüsü |
  |---|---|---|
  | Gövde eğimi | 32°'ye kadar | 20–25° |
  | Yuvarlanma | −15…+20° | −4…+7° |
  | Baş yanal | ±20 cm | ±9 cm |
  | Eller | 69 ileri / 45 yukarı | — |

- Oyunda bu, yeniden hızlanmada 42–50° eğim, 41°'ye açılan kollar ve 43 cm baş savrulması olarak görünüyordu: "yarışa yeniden başlar gibi" hareket.
- Aynı tepkinin iki katmanda eklendiği bulunmadı. SHME / PBI katkıları önceki sürümlerde ölçülmüştü; ana kaynak klip içeriği.

**Gerçek değişiklik: yeni üst gövde performansı** (`rb222_revturn.py`, yerinde bake).
- Bacak, kök ve pelvis korundu; okuma kontrolü 0.0 cm. Değişen kemikler: spine_01..05, boyun, baş, köprücük, kollar, eller.
- **Faz her karede bacaklardan alınıyor:** hangi ayak önde, ne kadar, açılıyor mu kapanıyor mu. Faz tek yönlü, hız sınırlı.
  - İlk sürüm topuk vuruşu çapalarını kullanıyordu; aynı ayağın yeniden basışında tam döngü atlıyor ve gövde savruluyordu.
  - İkinci sürüm bu basışları atlıyordu; kollar 0.8 s park hâlinde kalıyordu. Her ikisi düzeltildi.
- **Kaynaklar ve genlik:** tempolu → depar döngüleri, klibin kendi kök hızına göre karıştırılıyor. Salınım genliği klibin adım uzunluğuyla ölçekleniyor.
- **Gövde yönü:** döngülerinki. Kaynağın göğüs–pelvis bükülmesinin yarısı gövde ekseni etrafında korunuyor; omuzlar dönüşü hâlâ öncülüyor.
- **Giriş:** 0.50–0.95 s arasında kaynaktan yeni performansa geçiş. Kesiş klibinin çıkış pozu korunuyor.
- **Dört klip** bake edildi ve ilgili dört veritabanı yeniden anahtarlandı.
- **Orijinal anahtarlar** `revturn_src/*.json` ve `checkpoint/revturn/` altında.

**Önce → sonra** (`r_cutrev_r`, 5.45–7.25 s, sabit 30):

| Ölçü | Önce | Sonra |
|---|---|---|
| Gövde eğimi tepe | 51° | 46° |
| Yuvarlanma salınımı | ±19° | ±4° (girişte ±10) |
| Baş yanal aralığı | 43 cm | 18 cm |
| El aralığı L / R (ileri) | 69 / 81 cm | 56 / 33 cm |
| Kol açılması tepe | 38° | 14° |

- Sol kesiş (`r_cutrev_l`): el aralığı 102 / 94 → 87 / 85 cm, eğim tepesi 56 → 47°.
- Ayak teması, klip seçimi ve bütün yeniden hızlanma senaryoları (`r_cutrev_*`, `p_revpush`, `k_ws_clean`, `chain_sscut`, `k_cut_back`) **bit bit aynı.**
- 20 / 60 / 120 FPS: baş yanal 18–21 cm, eğim tepesi ~46°.

**Kalan kusurlar**
- 5.6–6.6 s'de sol ayak 0.7 s'lik bir pivot salınımında; kollar bacaklara uyumlu olarak karşı uçta duruyor. Bacakla tutarlı ama görüntüde "tutulmuş" okunabilir; görsel karar kullanıcıya ait.
- Depar döngüsünün kendisi yüksek kollu (eller 41 cm yukarı). Bu sürümde değiştirilmedi.
- Klip kuyruğunda (3.2 s; MM 2.2–2.3 s'de depar döngüsüne geçiyor) tek karelik bir el yükselmesi kaldı. Oynanan bölüm ≤ 36 cm.

**Geri alma:** `checkpoint/revturn/` dosyaları editör kapalıyken geri kopyalanır, ardından veritabanları yeniden anahtarlanır.

---

## 3. ORGANİK KAMERA, KADRAJ VE FOV / LENS DAVRANIŞI

**Taban** (V2.21 üretimi, gerçek kamera düzeneği):

| Yürüyüş | Kol | FOV | Kamera yüksekliği (başa göre) |
|---|---|---|---|
| Yürüyüş | 216 cm | 60.9° | −4 cm |
| Tempolu | 235 cm | 62.5° | −3.5 cm |
| Depar | 260 cm | 64.9° | −0.6 cm |

- Kamerayı süren: SHME sinyalleri + `GR_UpdateRig` (Black Eye Camera etkin değil).
- V2.21'den gelen doğrulanmış adım ritmi ve ileri bakış zaten etkin.
- Hız FOV'u mevcut sistemde var. İkinci bir hız FOV'u eklemek çift sayım olurdu; eklenmedi.

**Gerçek değişiklik: hıza bağlı yakınlık** (`SHM_UpdateCameraV21`, `CamCloseEnabled`).
- SHME kol ölçeği gerçek hıza göre çarpılıyor:

  | Durum | Duruş | Yürüyüş | Tempolu | Depar |
  |---|---|---|---|---|
  | Çarpan | 0.90 | 0.88 | 0.92 | 0.97 |

- Değer süzülüyor (τ 0.6). Yalnız açık alanda uygulanıyor (× açıklık); iç mekânın kolu değişmiyor.
- Işınlanmada sıfırlanıyor. FOV değişmedi. Bakış ve kontrol dönüşüne geri besleme yok.

**Önce → sonra:**

| | Önce | Sonra |
|---|---|---|
| Yürüyüş kolu | 216 cm | 190 cm |
| Tempolu kolu | 235 cm | 216 cm |
| Depar kolu | 260 cm | 251 cm |

- FOV, yuvarlanma ve bakış kaynaklı yaw aynı.
- Gerçek harita tırmanışında mesafe sarsıntısı 308 → 24 (eski kameradaki tek karelik çekilme kayboldu).
- Koridor (190 cm, tavan, uç duvar, 360° yörünge): **0 kare** duvar içi; kare başına en büyük mesafe değişimi 18.5 → 18.0 cm.
- Yükseklik takibi aynı.

**Organik his.** Doğrulanmış temaslardan gelen V2.21 adım ritmi ve ileri bakış korunuyor. Bu sürümün katkısı kadrajı bedene yaklaştırmak. Daha fazla sallantı eklenmedi.

**DOF / lens.** Değiştirilmedi.
- Sabit odak f/8, 260 cm; otomatik odak avlanması yok.
- Etkileşim odağı sistemi yok; otomatik hedef kilidi eklenmedi.
- Hareket bulanıklığı, CA, vinyet ve distorsiyon artırılmadı. "mm lens" değişikliği yok.

**Dört karşılaştırma** (görüntüler `vid/`):
- **A:** eski beden + eski kamera. Yeniden hızlanma için orijinal klip dosyaları geçici olarak yerine konup kaydedildi, sonra bake'li dosyalar geri yüklendi; geri yükleme sonrası koşu bit bit aynı.
- **B:** yeni beden + eski kamera. Beden kanıtı kameradan bağımsız: sabit yan / çapraz gözlemci kameralar.
- **C:** eski beden + yeni kamera.
- **D:** ikisi birlikte.
- Beden düzeltmesi sabit gözlemcide görünüyor; kamera kusuru gizlemiyor.

**Üretimde:** **EVET** (`CamCloseEnabled true`).

**Kalan**
- Yakınlığın kendisi kullanıcı kabulü bekliyor.
- Menüye bağlı değil; konfor ölçeği `CamComfortScale` ile kontrol ediliyor.

**Geri alma:** `CamCloseEnabled false`.

---

## Doğrulama ve son durum

**Taze editör doğrulaması.** Üç kez yapıldı; her biri editör yeniden açıldıktan hemen sonra **ALL_OK**:
- `verify_prod222_fresh1.txt`
- `verify_prod222_final.txt` (son içerikle)
- `verify_prod222_final2.txt` (yakalamalardan sonra)

Denetlenenler:
- V2.21 denetimleri;
- başlangıç klipleri ve modu, `TapGate 0`, yakınlık değerleri;
- RevTurn dosyalarının bake'li olması ve veritabanı etiketleri;
- MontTick düzeltmesi, profil referansları.

Bir ara doğrulama (`fresh3`), aynı oturumdaki harness koşularının SHME varlığını bellekte kirletmesi yüzünden "dirty" verdi. Üretim hatası değildi; sıra düzeltildi.

**Bu sürümde yakalanan iki tuzak**
- Bellek nedeniyle yeniden başlayan editör gerçek zamana dönüyordu.
- Bake'ten sonraki ilk koşuda veritabanı dizini yeniden kurulurken `None` seçiliyordu.

**Önceki kazanımlar** korundu: kesiş-ters, erken ters çıkışları, toparlama tutma, arazi gövdesi, kamera çarpışması.

**Maliyet:** yeni çalışma zamanı mantığı yalnız kamera yakınlığı (birkaç düğüm). Başlangıç ve yeniden hızlanma içerik değişikliği.

## Eksik ve sonraki iş (somut)

1. **Kısa dokunuş yerleşmesi.** Mevcut kök hareketli `CoreMotion_Retargeted/AAMS/Idle/am_Stand|Ready_Idle_Step_*` kliplerine bağlanmalı, ya da idle seçimi basılı ayağa göre sınırlanmalı.
2. **Yan / geri / çapraz başlangıçlar** aynı yöntemle yeniden üretilmeli (`gen222_start` deseni).
3. **Arazide adımlama.**
   - Eksik: tümsek, basamak ve inişte ayak yüksekliği ve yerleşimi.
   - Pilot rotada 20 cm tümsek tırmanışı topuk kayması 34–48 cm; tempolu 15 cm kenar inişinde R 51 cm.
   - Gövde tepkisi var; adım içeriği yok.
4. **Kesiş → S, kesişte bırakma, W → S tam ters:** V2.21'deki gibi açık.
5. **Zıplama / iniş** bu sürümde incelenmedi.

## Kanıt dosyaları

- `final222.txt` (p / o son parti), `fps222.txt`.
- `verify_prod222_*.txt`.
- `CHANGES_V222.md`.
- `vid/` (önce / sonra, normal hız ve ⅓ hız), `img/`.
