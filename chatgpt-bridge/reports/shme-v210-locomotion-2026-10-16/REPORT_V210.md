# SHME V2.10 — Hareket hâlinde dönüşler, diz üreticisi güvencesi, idle diz (2026-10-16)

**İstek:** V2.9'un yararlı düzeltmelerini koruyarak:
- yarıda kesilen depar dönüşünü tamamla;
- tempolu dönüşleri, kontrollü toparlama adımını ve kalan diz–pelvis uyumunu oyun içinde çöz;
- diz onarımını üretim güvencesine dönüştür;
- temiz karşılaştırmayı kanıtlarıyla yayımla.

## Sonuç (kısa)
- **Diz bozan üretici düzeltildi ve kilitlendi.**
  - Kök neden: `v137_animedit.solve_leg`. Kemikleri en kısa yayla döndürüyor, diz düzlemini ham "diz ipucu"ndan alıyordu. 10 bake aracı (11 çağrı) bunu kullanıyor.
  - Aynı girdiyle üretim üreteci: eski çözücü 26 klibin **26'sında** geriye bükülen diz üretiyor (3–36 kare). Yeni çözücü **0**; ayak hatası, kayma ve pelvis birebir aynı.
  - Kayıt öncesi bir **bacak kontrolü** (`leg_guard`) eklendi. Eski çözücüyle 26 yazma denemesinin 26'sı reddedildi; dosya değişmedi (md5 aynı).
- **Kontrol, V2.9 taramasının kaçırdığı canlı kusurları da buldu; hepsi giderildi.**
  - Yürüyüş döngüsünde ve V2.8 yürüyüş duruşlarında, düz bacakta tek karede **bacak burulması** vardı (oyunda sol baldır ekseni 52–77°/kare sıçrıyordu). Düzeltmeden sonra 8.5°.
  - 33 canlı başlangıç klibinde menteşe dışı diz vardı; onarıldı.
  - Başlangıç idle'ında sol dizin içe kaçmasının sahibi idle klibinin kendisiydi. Onarıldı: menteşe 0.47 → 1.00, diz–parmak açısı −68° → −7°.
- **Depar 90° kesişi artık tam oynuyor.**
  - Kök neden: Motion Matching klibe dönüşün ortasından giriyordu (0.90 s). Fren / basma evresi atlanıyor, itişten önce çıkılıyordu.
  - Bunun iki sebebi vardı: satıcı klibi 716 cm/s, bizim depar 490 cm/s; kapsülün yüzü hızdan 2 kat hızlı dönüyordu.
  - Düzeltme üç parça:
    - yüz yönü hızın en fazla 15° önünde;
    - yeni sahip olunan kesiş veritabanı, dönüş ortasına girişi engelleyen pencereyle;
    - hız hizalanana kadar süren köprü.
  - Sonuç: klibe fren başında (0.77 s) giriliyor; fren → destek → dönüş → itiş kesintisiz oynuyor. Kapsülün yön tepkisi değişmedi (0.60–0.65 s).
- **Tempolu dönüşler:**
  - Geniş viraj ve fareyle keskin dönüş zaten tutarlı (kalça–kapsül 9–14°, sıçrama yok).
  - İki aday denendi, ikisi de **reddedildi** (gerekçe §5).
  - İleri↔geri ters dönüş köprüsüyle çalışıyor.
- **Ayrı toparlama adımı: uygulanmadı (NOT_IMPLEMENTED, gerekçeli).**
  - Hareket modelinde gerçek bir momentum taşması oluşmuyor. SHME toparlaması tasarım gereği yalnız itmeye tepki veriyor.
  - Projede koşarken kullanılabilecek bir yakalama adımı içeriği yok. Hedefli içerik brifi §6'da.
- **Pelvis:** tek ayak yükseltide oturmuş idle'da gereksiz çift çömelme yok. V2.9 raporundaki "62/57°" değerleri geçişin maksimumuymuş; düzeltildi (§7).
- **Teknik PASS / görsel inceleme / kullanıcı kabulü ayrı tutuldu** (§10). His ve kontrol kabulü NOT_TESTED; `USER_PLAYTEST_V210.md`.

## 1. Başlangıç durumu, korunanlar, yöntem
- **Okunanlar:** AGENTS.md, CLAUDE.md, `sphirus-game-dev-director` → SHME (motion-diagnosis, contact-authoring, mm-coverage, V2.9 bölümleri), `support-momentum-intents`, V2.9 raporu ve oyun testi rehberi.
- **Canlıdan doğrulananlar (16:1x, editör):**
  - UE 5.8. Üretim ABP'si `/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase` (+ child).
  - V2.9 değerleri yerindeydi: `SHM29_CutMode 2`, `SHM29_TipOld false`, `SHM_HC_Off false`, `SHM28_StopMode 1`, `SHM_RedirectDB_SL = PSD_SHM_SprintCut`.
  - GR sınırları: TurnLatAccelMax 1400, CutLatAccelMax 650.
  - Daha yeni bir çalışma yoktu.
- **Korunanlar:** V2.9 diz onarımları, idle çift uyarlama düzeltmesi, yerinde dönüş çift telafi düzeltmesi, pivot ayak kilidi ve V2.8 yürüyüş duruşu mantığı. Hepsi açık kaldı ve doğrulamada ölçüldü (§8).
- **Yedek (git yok):** her değişiklikten önce `.uasset` kopyası + SHA256, `Saved/Codex/SHME_V210_20261016/checkpoint/` altında:
  - `baseline_v29` (75 dosya);
  - `knee_repair210_before`, `v28_before_regen`, `walkloop_before_repair`, `idle_before_repair`;
  - `before_v210_sprintcut`, `before_v210_jogcut`, `before_v210_promote`;
  - `tools_before`, `skills_before`.
- **Karşılaştırma koşulları:**
  - Aynı giriş (gerçek IA_Move / IA_Look), aynı başlangıç ve ayarlar.
  - Her koşuda temel bayraklar açıkça veriliyor (harness bayrakları sıfırlamıyor).
  - Bellekteki denemeler her koşudan önce diskten geri yükleniyor (`pre_base.py`).
  - Aynı anda iki test işi çalışmıyor (`ab_safe.sh`).
- **Isınma koşusu:** her editör açılışında bir veritabanının ilk kullanımı indeks kurulumu yüzünden 0.1–0.4 s takılma yapıyor. Bu yüzden ölçümlerden önce atılan bir ısınma koşusu yapıldı; takılmanın denk geldiği bir olay (eğimde sağ dönüş) ölçümden ayrıldı.
- **Toplam:** ~150 PIE koşusu, 4 bellek kaynaklı editör yeniden başlatması.

## 2. Diz üreticisi: kalıcı üretim güvencesi (madde 1)
- **Kök neden:** `Tools/SHME_V1_20260925/v137_animedit.solve_leg`. 10 bake aracında 11 çağrı noktası (V1.3.7 → V2.8 üreticisi) bunu kullanıyordu.
  - Uyluk ve baldırı **en kısa yayla** döndürüyordu. Böylece baldırın menteşe ekseni yeni bacak düzleminden kayıyordu.
  - Diz düzlemini kaynak dizin ham konumundan alıyordu. Neredeyse düz bacakta bu yön gürültü; geriye döner.
- **Düzeltme (aynı fonksiyon):**
  - Uyluk ve baldır, kemik yönü + yerel Z (menteşe) ile tam çerçeve olarak kuruluyor; diz her karede bir menteşe.
  - Diz ipucu yalnız güvenilirken kullanılıyor. Düz bacakta ya da ayak ekseninden 25–45° saptığında düzlem yumuşakça ayağın yanal eksenine dönüyor.
  - Eski çözücü yalnız karşılaştırma için `solve_leg_v137` olarak duruyor.
- **Bacak kontrolü (`leg_guard`):**
  - Yerleri: ortak yazma noktası `write_tracks` (9 aracın yazma yolu) ve V2.8 üreticisinin kendi yazımı (varlık oluşturulmadan önce).
  - Reddedilenler: geriye ya da menteşe dışı diz (fleks ≥ 8°'de menteşe < 0.85); uyluk–baldır ekseni uyumsuzluğu (< 0.90); karelik menteşe ekseni sıçraması (> 60°, kaynak verilirse kaynağın 1.2 katı); kemik boyu değişimi; ayak hedefi hatası.
  - Eşikler 259 satıcı klibinden kalibre edildi: menteşe min 0.97, eksen min 0.95, hızlı 180'lerde sıçrama maks 51°/kare.

| Test | Eski çözücü | Yeni çözücü |
|---|---|---|
| Sentetik bacak (düz, zayıf / geri ipucu) | menteşe −1.00 (geriye) | 1.00, ayak hatası 0 |
| Üretim üreteci, üretim ayarı (24 faz duruşu + 2 başlangıç, sol ve sağ, tüm destek evreleri), aynı girdi | **26 / 26** klip kontrolden kalıyor (3–36 geriye kare, menteşe −1.00'e kadar) | **0 / 26** |
| Aynı klipler: ayak hatası / sabit ayak kayması / pelvis / giriş hatası | — | eskisiyle birebir (≤ 0.06) |
| Yazma denemesi (kontrol açık) | 26 / 26 **REDDEDİLDİ**, dosya md5 aynı | 26 / 26 kaydedildi |
| Oyunda (6 faz durma + yürüme başlangıcı) hareket menteşesi | üretim (V2.9 onarımlı) 0.88–0.91 | 0.97–0.99; geriye kare 0 |

## 3. Kontrolün bulduğu canlı kusurlar (giderildi)
- **Tarama (sahip olunan 159 + LB 22 + satıcı 259 klip):**
  - 34 canlı klip menteşe / eksen eşiğinin altında; hepsi canlı başlangıç veritabanlarında. Geriye bükülen yoktu.
  - `SHM_Run_Start_*` V1.3.9 bake'leri: sol menteşe 0.14–0.34, uyluk–baldır ekseni 0.58'e kadar. V2.9 taraması bu klasörü kapsamamıştı.
- **Düz bacakta bacak burulması (menteşe metriğinin göremediği):**
  - Görülen yerler:
    - 10 üretim yürüyüş duruşu (`A_SHM28_WalkStop_P00–05, P20–23`): 112–134°/kare;
    - `WalkStart_R`: 99°/kare;
    - **üretim yürüyüş döngüsü `A_LB_Walk_Fwd`**: sol bacak, her adımın ortasında 88°/kare.
  - Oyunda sol baldır ekseni yürürken 52–77° tek karede sıçrıyordu; sürücü ve görünür MetaHuman aynı. Koşu başına 11–13 kare > 30°.
- **Düzeltmeler (ayak dönüşümü ve fleks birebir korunarak):**
  - V2.8 klipleri üretim üreteciyle yeni çözücüden yeniden üretildi: 26/26, uzunluklar aynı, giriş öznitelikleri 0.31 cm içinde.
  - 33 başlangıç klibi `v210_knee_repair.py` ile onarıldı. `A_SHM28_WalkStop_P00` kontrol tarafından **reddedildi**: dokunulmayan bacakta 126.6°/kare sıçrama vardı. Bu klip zorlanmadı, yeniden üretildi.
  - Yürüyüş döngüsü onarıldı: sol eksen sıçraması 87.6 → 8.8°/kare.
- **Oyunda yürüyüş (sürücü = görünür):** sol baldır ekseni sıçraması **77.5° → 8.5°**, > 30° kare **11–13 → 0** (`calfjump.py`).
- **Son tarama:** 216 sahip olunan klip (SHME animasyonları, LB döngüleri, idle) içinde kontrolden kalan **0**.

## 4. Depar dönüşünün yarıda kesilmesi (madde 2)
- **Ölçüm (üretimde zaman çizelgesi, `cut_timeline.py`):**
  - Seçilen klip ve klip zamanı ilk kez kapsülle aynı zaman ekseninde kaydedildi.
  - Köprü veritabanı seçiliyordu, ama Motion Matching satıcı depar dönüşüne **0.90 s'den** giriyordu, yani dönüşün ortasından.
  - 0.3 s sonra diğer ayak varyantının 0.90 s'sine yeniden giriyordu (aynı yarım tekrar). Bölüm hız 25° içine girince (~0.5 s) bitiyor, itişten önce düz depar döngüsüne geçiliyordu.
- **Klibin kendi evreleri (`cutclip_table.py`):**
  - hız düşüşü 0.63 s; dönüş %10 / 50 / 90 → 0.67 / 0.90 / 1.4–1.6 s;
  - yüz ve gidiş yönü birlikte dönüyor (fark ≤ 6°);
  - iç ayak 0.50–0.63, dış ayak itişi 0.73–0.93, sonraki itiş 1.2–1.6 s;
  - pelvis en alçak 0.77 s.
- **Neden ortadan giriliyordu:**
  1. Satıcı klibi 716 cm/s, bizim depar 490 → kesişte 307 cm/s. Arama, yörüngeye en çok uyan en yavaş kareleri (dönüş ortası) seçiyor.
  2. Kapsülün yüzü 0.3 s'de 63° dönüyordu, hız yönü ise 0.72 s'de dönüyordu; kapsül "dönüşün ortasında" görünüyordu.
  - Not: kapsül hız dönüşü (0.72 s) ile klibin hız dönüşü (0.86 s) aslında yakın. V2.9'daki "1.2 s" tahmini hız ölçeklemesine dayanıyordu; doğru tespit giriş zamanı ve bölüm sonuydu.
- **Değerlendirilen ve reddedilen yollar:**
  - Oyuncuyu kilitlemek, tüm gait'lerin dönüşünü yavaşlatmak, animasyonu hızlandırmak, uzun blend: istekte yasak.
  - BranchIn penceresini daraltmak: örnekleme aralığını keser, devam pozu kaybolur. UE 5.8 kaynağıyla doğrulandı.
- **Uygulanan (yalnız depar, kaydedildi):**
  1. **S1 — yüz yönü sınırı (GR, `SprintCutFaceLead` 15°):**
     - Depar "girdiye bak" kuralı aktifken gövde yönü hız yönünün en fazla 15° önünde.
     - Hız kendisi değişmedi; girdiye anında tepki var.
     - Tek başına girişi düzeltmedi (ölçüldü), ama gövdeyi yoluna bağlıyor.
  2. **S2 — yeni sahip olunan kesiş veritabanı `PSD_SHM210_SprintCut`:**
     - İçerik: satıcı depar 90° destek adımlı dönüşlerinin kopyaları + `A_LB_Sprint_Fwd`. Satıcıya dokunulmadı.
     - Kopyalarda **"Pose Search: Block Transition In"** penceresi [0.78 s, son]. Dönüşe yalnız yaklaşma / fren evresinde girilebiliyor; içinden oynamaya devam serbest.
     - Döngünün BranchIn'i 0..uzunluk. V2.9 veritabanındaki `−0.001` döngüyü "döngüsüz" yapıyordu (V1.3.8 tuzağı).
  3. **S3 — köprü kuyruğu (ABP, `SHM210_CutTail` 0.8 s, `SHM210_TailAngle` 8°):**
     - Bileşen bölümü bitirdikten sonra ABP bölümü, hız girişe 8° yaklaşana kadar (en çok 0.8 s, girdi varken) sürüyor.
     - Yeni niyet sayacı sıfırlar ve köprü yeniden seçilir; bırakma bölümü bitirir.
     - Not: veritabanı tutma `SHM_RedirectActive && SHM_RedirectFrames > 1.5` ile çalışıyor; `SHM_RedirectHold` yalnız arama aralığını uzatıyor. İlk deneme bu yüzden işlemedi; bulundu ve düzeltildi.

**Son doğrulama (kaydedilmiş üretim) — ESKİ = aynı onarılmış klipler + V2.9 depar mantığı (yüz sınırı 0, kuyruk 0, eski veritabanı); YENİ = V2.10 üretimi. 5 çubuk 90° kesişi (`chain_sprint`, `ad_sprint`) + fare dönüşleri (`chain_sflick`), YENİ 2 tekrar:**

| Ölçü | ESKİ | YENİ |
|---|---|---|
| Kesiş klibine giriş zamanı (klip saniyesi) | 0.87–0.93 (dönüş ortası) | **0.77 (fren başı), 7 / 7 olay** |
| Klip içinde ikinci varyanta yeniden giriş | var (0.90 → 0.93) | yok |
| Hizalanma süresi (kontrol tepkisi) | 0.59–0.71 s | 0.59–0.66 s |
| Tepe yanal ivme | 0.87–2.42 g (bir sıçrama) | 0.86–0.93 g |
| Kalça–kapsül ayrılması | 16.9–21.9° | 13.5–20.4° |
| Basılı ayak kayması | 2.9–6.0 cm | 2.2–6.0 cm |
| Fren çökmesi (pelvis) | 7.3–11.6 cm | 7.8–18.2 cm |
| En kötü üst gövde sıçraması (`chain_sprint` / `ad_sprint`) | 121 / 59 m/s² | 39–63 / 38 m/s² |
| Depar 180 (çubuk) kalça–kapsül | 95° | 43–56° |
| Fareyle 180 (`chain_sflick`) | ikinci bölüm 90° kesiş köprüsüne gidiyor → tempolu | ters dönüş köprüsü |

- **İlk basan ayak:** fren başında giriş iki varyantla (sol / sağ ayak) faza göre seçiliyor; "ilk basan mutlaka dış ayak" kuralı zorlanmadı. Olayların bir kısmında ilk basan iç ayak (fren adımı), ardından dış ayakla itiş geliyor; bu klibin kendi düzeni (iç ayak 0.50–0.63 s, dış ayak 0.73–0.93 s).
- **Fren çökmesi** bazı olaylarda arttı (en çok 18 cm), çünkü klibin fren evresi artık oynanıyor. Görsel yargı ve his kabulü kullanıcıda.
- **Fareyle 90° depar dönüşleri** çoğunlukla döngü / virajla yapılıyor (köprüye geçmeden bölüm bitiyor). Gövde yüz sınırıyla yoluna bağlı (kalça–kapsül 15–20°).

## 5. Tempolu dönüşler (madde 3)
- **Tempolu bu projede bakışa bağlı.** Gövde kameraya bakıyor, A/D yana koşu.

| Durum | Aday | Sonuç | Karar |
|---|---|---|---|
| Fareyle yavaş geniş viraj → keskin dönüş (60°/s, sonra 90°/210°) | üretim döngüleri | kalça–kapsül 9–14°, kalça–ayak 10–17°, yaw sıçraması 0, basılı ayak dönmesi 2–6° | korundu |
| Fareyle hızlı 90° | J1: yüz yönü hıza bağlı (`JogTurnFaceLead` 20) | üretimde yüz zaten hızın ≤ ~25° önünde; ölçülebilir değişiklik yok (kalça–kapsül 11 → 11°, hizalanma 0.54 → 0.52 s) | **üretime alınmadı** (alan kurulu, 0) |
| Fareyle 90° / A-D kesiş için koşu dönüş klipleri | J2: satıcı `Run_Turn_*_090` kopyaları + aynı giriş penceresi, ayrı köprü | fare dönüşlerinde hiç seçilmedi (bölüm erken bitiyor). Çubukla yana kesişte devreye girip **129 m/s²** sıçrama (üretim 32) — yüz döndüren klip yana koşu değişimine uymuyor. İçerik 512 cm/s, gidiş 0.33 s'de dönüyor, 26–33 cm fren çökmesi (tempolu 300 cm/s) | **reddedildi** |
| Çubukla yana keskin kesiş | üretim döngüleri | dış ayak ilk 0.07–0.24 s, hız kaybı %22–35, 0.82–0.87 g, kayma 2.2–3.0 cm | korundu |
| Fareyle 180° / ileri↔geri | V2.9 ters dönüş köprüsü | hizalanma 0.46–0.65 s, kayma 0.6–2.4 cm, yürüyüş döngüsü araya girmiyor | korundu |
| W+A ↔ W+D | döngüler | 0.33–0.54 s, kayma 2.0–4.7 cm | korundu |

- **Dürüst sonuç:** tempoluda "fren adımlı keskin dönüş" klibi yok. Mevcut adayların ikisi de bizim tempoluya uymadı; döngü tabanlı dönüşler ölçülerde tutarlı. Hedefli içerik §6'da.

## 6. Ayrı toparlama adımı (madde 4) — uygulanmadı, gerekçeli
- **Ölçülen (yeni telemetri `RecoveryDemand`, `TractionExcess`, `CaptureError`, `Family`):**
  - Depar kesişi, kesiş ortasında bırakma ve ardışık S kesişlerde `TractionExcess` ve `RecoveryDemand` her karede **0**. Toparlama ailesi (1/6) hiç seçilmedi.
  - Hareket modelinde (CMC) kesişin yanal ivmesi ~0.9 g'de kalıyor ve çekiş modelini aşmıyor; gövde "taşmıyor", kapsül eğri çiziyor.
- **Tasarım kararı (V1.3.1, kodda belgeli):** SHME toparlaması yalnız **dış itmeye** tepki veriyor. Niyet uyumsuzluğu ve çekiş aşımı dâhil edildiğinde kasıtlı dönüş, duruş ve duvar çarpmalarında yanlış toparlama adımları üretmişti (depar 90 duruşunda 35 cm, tempolu duvarda 84 cm kayma). Bunu geri açmak ölçülmüş bir regresyonu geri getirir.
- **İçerik:**
  - `SHM_Rec*` / `SHM_RecS*`: duran karakterin itilme toparlamaları (kök hızı ~0, basılı biter).
  - Satıcı `Run_Shuffle`: 512 cm/s yana koşu yön değiştirmesi.
  - Koşarken dışa yakalama adımı içeren klip projede yok.
- **Kesişte bırakma (dur isteği) bugün:** SprintCut → koşu duruşu. Basmalar 0.23 / 0.51 / 0.88 / 1.29 / 1.79 s, kayma 1.7–2.6 cm. Momentum çok adımlı bir duruşla sönümleniyor; ayrı bir "sendeleme" yok.
- **Hedefli içerik brifi (satın alma yapılmadı):**
  - Hız: depar ~4.9 m/s ve tempolu ~3 m/s.
  - Aşırı keskin (75–110°) kesişte iç / dış ayak varyantlı, 1 destek adımı + **1 dışa yakalama adımı** (çapraz ya da yan adım).
  - Gövde ve kollar karşı tepkili; sonra yeni yöne itiş (yeniden hızlanma). L/R, iki faz.
  - Ayrıca "kesiş ortasında dur" yakalama-duruş adımları.
  - Kök hareketi, Manny uyumu, 30 fps+. Fren çökmesi ≤ 10–12 cm (bizim karakter atletik değil).
- **Tetikleme tasarımı (içerik gelince):**
  - Normal viraj: talep ≤ 1 adımlık kapasite.
  - Planlı keskin dönüş: mevcut kesiş köprüsü.
  - Toparlama: kesiş, dış ayağın havada olduğu fazda başlıyor ve talep > ~1.6, ya da önceki kesişin itişi bitmeden ters kesiş.
  - Klip, oyuncu yön değiştirince veya durunca kesilebilir olmalı.

## 7. Pelvis ve idle diz (madde 5)
- **Tek ayak yükseltide oturmuş idle (`strip_idle.py`, son 1 s medyan):**
  - Pelvis **alttaki** zeminin 94.4–96.5 cm üstünde; düz zeminde 94.6–95.8.
  - Alttaki bacak düz zemindeki fleksiyonunu koruyor (11–18°), yalnız yüksekteki bacak bükülü (41–58°).
  - Gereksiz çift çömelme yok. Bu V2.9 düzeltmesinin sonucu; bu görevde pelvis için ayar değiştirilmedi.
  - **Düzeltme:** V2.9 tablosundaki "62/57°" duruş → idle geçişinin **maksimumuydu**, oturmuş hâl değil.
- **Bu motor sürümündeki etkin düğüm ayarları okundu:**
  - FootPlacement pelvis: HorizontalRebalancingWeight 0.3, MaxOffsetHorizontal 10, HeelLiftRatio 0.5, AllLegs.
  - Basma ön ayarları fonksiyona bağlı (`Get_FootPlacementPlantSettings`), düğüm değil.
  - LegIK: HingeRotationAxis Z, bEnableRotationLimit açık, diz burulma düzeltmesi varsayılan açık.
- **Tek değişkenli testlerde hiçbiri değişiklik yapmadı** (idle pelvis, fleksiyon, sol diz birebir aynı):
  - yatay dengeleme 0;
  - MaxExtensionRatio 0.8;
  - HeelLiftRatio 1 / 0;
  - LegIK diz burulma düzeltmesi kapalı.

  Sahip bunlar değil; üretim ayarları korundu.
- **Başlangıç idle'ında sol diz:**
  - Sahip: idle klibinin kendisi (`af_Stand_Idle_NaturalBaseline_Phase275`, oyunun açılışında oynanan 65.8–68.2 s).
  - Bu aralıkta sol bacak 1.5–2.7° ile neredeyse düz; dizin hat dışı 0.5–1 cm'lik kayması parmakların 30–68° **içine** bakıyor.
  - IK bacağı 10°'ye bükerken bu yönü koruyor; sonuç içe kaçan diz.
  - Onarım: neredeyse düz karelerde diz kayması ayağın menteşe düzlemine alındı. Ayak ve fleks birebir; sol 686 kare, sağ 30 kare.
  - Oyunda: menteşe **0.47 → 1.00**, diz–parmak **−68° → −7°**, burulmuş kare **15–23 → 0**; sürücü ve görünür aynı.

## 8. Doğrulama zincirleri (son kaydedilmiş üretim) ve kare hızı
Tüm zincirler son kaydedilmiş üretimde, gerçek giriş yoluyla (`v210v_*`). Baldır ekseni sıçraması = koşu başına kare sayısı > 30° (sürücü = görünür).

| Zincir | Ana ölçüler | Sıçrama > 25 m/s² (en kötü) | Baldır sıçraması > 30° |
|---|---|---|---|
| Yürü → dur → sağa / sola yerinde 90° → yürü | kalça–kapsül 44 / 34°, kalça gecikmesi 0.18 / 0.21 s, yürüyüş başlangıcında sıçrama yok | 1 (28) / 1 (34) | 0 / 0 |
| Hızlı fare yerinde 90 / 180 (`tip_fast`) | kalça–kapsül 34–71°, kalça–ayak 36–68°, gecikme 0.09–0.22 s | 4 (33) | — |
| Tempolu → geniş viraj → keskin dönüş → dur | kalça–kapsül 9–14°, kalça–ayak 10–17°, yaw sıçraması 0 | 1 (37) | 0 |
| Depar → 90° kesiş → devam (+ ters) | §4 tablosu | 6–7 (39–63) | 0–1 |
| Depar → 180° → yeniden hızlan | ters köprü, hizalanma 0.57–0.84 s, fren 18–24 cm | (yukarıda) | ≤ 1 |
| W+A ↔ W+D | 0.33–0.54 s, kayma 2.0–4.7 cm | 2 (28) | 0 |
| İleri ↔ geri (tempolu) | ters köprü, 0.46–0.64 s, kayma 0.6–1.7 cm | 3 (28) | 0 |
| Kısa bas → bırak → tekrar → çapraz | hata / sıçrama yok | 3 (35) | 0 |
| Yürüyüşte ±30° | hız kaybı %0–2, 0.22 g, kayma 3.0–4.2 cm | 0 | — |
| Eğimde dur → sağa / sola 90° → yürü | sol: kalça–kapsül 34°, gecikme 0.22 s. sağ: doğrulama koşusu dönüş anında 0.37 s editör takılmasına denk geldi (geçersiz); yakalama turundaki tekrar 44° / 0.22 s (V2.9: 44° / 0.21 s) | 1 (34) / 1 (36) | 0 / 0 |
| Tek ayak yükseltide (sol / sağ 10 cm) dur → 180 → yürü | oturmuş idle: pelvis alttaki zeminden 94.4–96.1 cm (düz 94.6–95.8); alttaki bacak 11–15°, yüksekteki 55–58° | 1 (35–39) | 0 |
| 8° eğim / 10° çapraz eğim / 18 cm basamaklar | geriye diz 0, burulma 0, menteşe ≥ 0.92 | 1 (34–36) | 0 |
| Yürüyüş duruşu 6 faz / yürüyüş başlangıcı | idle menteşe 1.00, sol diz 12° | 0 | 0 |
| Depar kesişi ortasında bırakma | çok adımlı duruş, kayma 1.7–2.6 cm | 7 (41) | 0 |
| Depar ardışık S kesiş | kalça–kapsül 12–34°, 1.2–1.75 g | 4 (57) | 1 |

- **Hatasızlık:**
  - 32 / 32 doğrulama koşusunda Accessed None (SHME) 0, PoseSearch indeks atlaması 0.
  - Editör günlüklerinde Blueprint Runtime Error 0, Accessed None 0.
  - Günlükteki diğer "Error:" satırları hareketle ilgisiz: oyun modu bildirimleri, iki çevre / kumaş malzemesinin VT parametre uyarısı ve editör açılışındaki 17 "Condition failed" (V2.9 günlüğünde de birebir 17).
  - İlk kullanım takılmaları (indeks kurulumu) editöre özgü; ısınma koşusuyla ayrıldı.

**Kare hızı (60 fps hedefi, yakalamasız ayrı çalıştırma, `t.MaxFPS`; elde edilen = oyun zamanı kare aralıklarının medyanı):**

| Çalıştırma | Depar kesiş | 10 cm şerit | Yürü-dur-dön |
|---|---|---|---|
| tam telemetri, sınır 30 | 30.3 fps (p10 29.4) | 23.3 | — |
| tam telemetri, sınır 60 | 35.7 (33.3) | 23.8 | 26.3 |
| hafif telemetri, sınır 60 | 35.7 (32.3) | 34.5 | 37.0 |
| hafif telemetri, sınır 60 + `r.ScreenPercentage 50` | 47.6 (43.5) | 34.5 | 37.0 |

- **60 fps: NOT_TESTED.** Editör PIE'de en yüksek medyan 47.6 fps; ulaşılamayan hız geçti sayılmadı.
- **Yük ayrıştırması:**
  - Harness'in kare başı telemetrisi belirgin bir yük: şerit ve yürüyüş 24–26 → 34–37 fps.
  - Ekran yüzdesi editör PIE'de etkisiz (şerit ve yürüyüşte birebir aynı; daha önce de kayıtlı). Depardaki tek yüksek koşu koşu-arası farka bağlandı.
  - Fizik ve animasyon ayarlarına dokunulmadı.
- **Hızdan bağımsızlık:** 23–48 fps arasındaki tüm koşularda depar kesiş girişi 0.77 s. Şerit idle'ı (pelvis 96.0, alt bacak 11.1°, üst 56.8°) birebir aynı.

## 9. Değişen dosyalar, etkin ayarlar, geri alma
- **Varlıklar (kaydedildi):**
  - `ABP_GR_MotionMatchingBase` + child: DSL kuyruk kuralı, `SHM210_*` değişkenleri; varsayılanlar `SHM210_CutTail 0.8`, `SHM210_TailAngle 8`, `SHM210_JogCutMode 0`, `SHM_RedirectDB_SL = PSD_SHM210_SprintCut`.
  - `BP_GR_Player` (+ `BP_PBI_Player` derleme): S1 / J1 düğümleri.
  - `BP_GR_MotionProfile`: 7 yeni alan.
  - `DA_GR_LocomotionBehavior`: `SprintCutFaceLead 15`, `JogTurnFaceLead 0`.
  - Yeni: `/Game/GraceRanger/SHME/Animations/V210/` (`PSD_SHM210_SprintCut` + 4 kopya; reddedilen aday `PSD_SHM210_JogCut` + 4 kopya, kullanılmıyor).
  - Test klipleri: `/Game/GraceRanger/SHME/Animations/V210_KneeTest/` (26 klip, yalnız kanıt).
  - Onarılan / yeniden üretilen: 26 V2.8 klibi, 33 başlangıç klibi, `A_LB_Walk_Fwd`, `af_Stand_Idle_NaturalBaseline_Phase275`.
  - Notify eklenen: `A_LB_Sprint_Fwd` ve `A_CT_Jog_Fwd` (yalnız yeni veritabanları için BranchIn).
- **Araçlar:**
  - `Tools/SHME_V1_20260925/v137_animedit.py` (çözücü + kontrol);
  - `Tools/SHME_V28_20261015/v28_gen_startstop.py` (yazma öncesi kontrol);
  - `Tools/SHME_V1_20260925/install_idle_wait.py` (kuyruk, tempolu test anahtarı);
  - `Tools/SHME_V1_20260925/qa_pie.py` (`test_look`);
  - `Tools/SHME_V210_20261016/*`: kurulumlar, onarım, analiz (`cut_timeline`, `cutclip_table`, `calfjump`, `strip_idle`, `idle_knee`, `final_tables`), A/B, yakalama, medya.
- **Hızlı geri alma (V2.9 depar mantığı):** `DA_GR_LocomotionBehavior.SprintCutFaceLead = 0`, ABP `SHM210_CutTail = 0`, `SHM_RedirectDB_SL = PSD_SHM_SprintCut`.
- **Tam geri alma:** editör kapalıyken `checkpoint/before_v210_promote` (ABP'ler, DA, GR, PBI) ve klip yedekleri:
  - `knee_repair210_before`, `v28_before_regen`, `walkloop_before_repair`, `idle_before_repair`;
  - `baseline_v29` (V2.9 sonu).
- **Skill eklemeleri** (yalnız doğrulanmış):
  - `sphirus-human-motion-engine`: architecture, authoring, validation, motion-diagnosis, mm-coverage, contact-authoring.
  - `sphirus-character-camera/support-momentum-intents`.
  - `sync_claude_skills.py`: 0 hata.

## 10. Teknik PASS / görsel inceleme / kullanıcı kabulü
- **Teknik PASS (ölçüldü, son üretim):**
  - Diz kontrolü (216 klip 0 kusur; eski çözücü reddediliyor).
  - Yürüyüşte diz burulma sıçraması yok.
  - Idle sol diz düzeldi.
  - Depar kesiş girişi fren başında ve kesintisiz; hizalanma süresi değişmedi.
  - Oturmuş idle pelvisi doğru.
  - Hatasızlık: §8.
- **Görsel inceleme:** §11. Benim değerlendirmem his kabulü değildir.
- **Kullanıcı kabulü: NOT_TESTED** (`USER_PLAYTEST_V210.md`).
- **Açık / kalan:**
  - Ayrı toparlama adımı yok (§6, içerik ihtiyacı).
  - Tempoluda fren adımlı keskin dönüş klibi yok (§5).
  - Hızlı depar / tempolu dönüşlerde ve 180 ters dönüşlerde tek tek karelerde baldır ekseni sıçraması (koşu başına ≤ 1 kare > 30°, en çok 119°). Eski mantıkta da var (133°'ye kadar); satıcı hızlı dönüş içeriği ve ters dönüş geçişleri. Ayrı ele alınmalı.
  - Depar ters dönüşünde üst gövde pop'ları (V2.9'dan beri).
  - FootPlacement pelvisi yalnız dikey; basamak kenarında ayak kenara oturabiliyor (bir koşuda 11.7 cm, kenar).
  - Kıyafet göğüs delinmesi (kapsam dışı; videolarda test görünümü, §11).

## 11. Görseller ve videolar
- **Kayıt koşulları:**
  - Tümü son kaydedilmiş üretimden. ESKİ = aynı onarılmış klipler + V2.9 depar mantığı, anahtarlarla.
  - Gerçek zamanlı yakalama 30 fps sınırında (elde 20–26 fps). AVI'ler ölçülen yakalama hızında oynuyor, yani oynatma süresi = simülasyon süresi; `*_slow3x` 1/3 hız. GIF'ler gerçek hızda (her 2. kare).
  - Kameralar: kapsülü izleyen ama dünya yönü sabit **yan** ve **ön-çapraz** kameralar (dönüşte kamera dönmüyor), ayrıca **oyun kamerası**. Pawn'a bağlı 3 nötr dolgu ışığı, QA zemini.
  - Tam gövde, ayaklar ve gövde–kalça aynı karede.
- **Test görünümü (önemli fark):**
  - Kıyafetin göğüste delinmesi (kapsam dışı) ten göstermesin diye **yalnız test dünyasında** görünür gövdeye (Manny) opak gri QA kili malzemesi verildi. Kollar ve bacaklar gri.
  - Kıyafet, yüz ve saç üretim görünümünde. Üretim varlıklarına dokunulmadı.
  - Hiçbir kare çıkarılmadı ya da düzenlenmedi.
- **Arka plan:** QA zemininde üstte görünen ters ağaç görüntüsü test sahnesinin kendisi, hareketle ilgisiz.

| Dosya (`vid/`) | Ne gösteriyor |
|---|---|
| `sprint_cut_old_side.gif` / `sprint_cut_new_side.gif` (+ `*_realtime.avi`, `*_slow3x.avi`) | depar 90° kesiş + ters dönüş, yan: ESKİ / YENİ |
| `sprint_cut_new_diag.gif`, `sprint_cut_new_game.gif` | aynı zincir, YENİ: çapraz / oyun kamerası |
| `sprint_flick_old_diag.gif` / `sprint_flick_new_diag.gif`, `sprint_flick_new_game.gif` | depar + fareyle 90 / 90 / 180 |
| `sprint_cut_release_diag.gif` | depar kesişi ortasında bırakma (dur) |
| `walk_stop_turnR_side.gif` (+ `walk_stop_turnR_side_realtime.avi`), `walk_stop_turnR_diag.gif`, `walk_stop_turnL_diag.gif`, `walk_stop_turnR_game.gif` | yürü → dur → yerinde sağa / sola 90° → yürü |
| `strip_stop_turn_side.gif` (+ AVI), `strip_stop_turn_diag.gif` | 10 cm şeritte dur → idle → 180 → yürü |
| `slope_stop_turn_side.gif`, `xslope_stop_turn_diag.gif`, `slope_turnR_side.gif`, `slope_turnL_side.gif` | 8° eğim / 10° çapraz eğim; eğimde sağa / sola dönüş |
| `spawn_idle_knee_diag.gif` (+ AVI) | oyun açılışı idle: sol diz (onarılmış idle klibi) |
| `jog_curve_sharp_diag.gif` (+ AVI), `jog_curve_sharp_game.gif` | tempolu geniş viraj → keskin fare dönüşü → dur |
| `jog_strafe_cut_diag.gif`, `jog_wa_wd_diag.gif`, `jog_fwd_back_side.gif` | tempolu A/D kesiş, W+A ↔ W+D, ileri ↔ geri |
| `tap_release_diag_diag.gif` | kısa bas → bırak → tekrar → çapraz |

- **Durağan görüntüler (`img/`):**
  - `sprint_cut_old_top_new_bottom.jpg`: depar kesişinde aynı karelerin yakın planı; üst ESKİ, alt YENİ.
  - `spawn_idle_knee_new.jpg`: açılış idle'ı, sol diz.
  - `strip_stop_turn_new.jpg`: şeritte dur → dön.
- **Diz onarımları için önce/sonra:** eski klipler oyunda bir anahtarla geri getirilemediği için görüntü değil, aynı senaryoda ölçülen kare değerleriyle veriliyor (§3, §7). Eski hâl checkpoint'te duruyor.
- **Kendi görsel incelemem (gerçek hız, sonra yakın plan karelerle):**
  - **Depar kesişi:**
    - ESKİ: gövde ilk karelerde aniden yeni yöne dönmüş, dik.
    - YENİ: yana koşarken önce uzun bir fren adımı ve içe eğilme, basılı ayak, destek adımı, sonra gövdenin dönerek itişi. Dönüş parça parça değil, sıralı okunuyor.
    - Fren çökmesi bazı olaylarda belirgin; "fazla mı?" yargısı kullanıcıda.
  - **Açılış idle'ı:** iki diz parmak hizasında; içe kaçma görülmüyor.
  - **Şerit / eğim:** ayaklar yüzeyde, alttaki bacak düz, yüksekteki bükülü.
  - **Tempolu:** viraj ve keskin fare dönüşü döngülerle akıcı, belirgin bir fren adımı yok (§5).

