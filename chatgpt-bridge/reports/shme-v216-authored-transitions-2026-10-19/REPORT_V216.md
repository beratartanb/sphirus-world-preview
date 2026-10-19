# SHME V2.16 — üretilmiş geçiş hareketleri (kesiş→ters dönüş, yürüyüş→depar bağlantısı, yerinde ters dönüş girişi)

Tarih 2026-10-18/19. Temel: V2.15 kaydedilmiş üretim. Bütün sayılar gerçek zemin temas ölçüsüyle (`contact216.py`, §5), **ayak başına,
temas başına**; iki ayak hiç toplanmadı. "net" = temasın ilk ve son karesi arasındaki yatay yer değiştirme, "sürükleme yolu" = yerde
basılıyken (≥30 cm/s) ya da pivot noktası kayarken biriken yol. Teknik / görsel / kullanıcı kabulü ayrı; **kullanıcı kabulü verilmiş
sayılmadı.**

## Özet

| Hedef | Sonuç | Üretim |
|---|---|---|
| 1 Kesişten ters dönüşe giriş (B: yeni yöne koşmaya devam) + atletik çömelme | **PARTIAL** — yeni içerik üretildi; ana senaryolarda süpürme ve gövde eğimi belirgin azaldı; üç alt durumda gerileme var (aşağıda) | **Üretimde** |
| 2 Yürüyüş→depar, destek evresinden kısa bağlantılar | **PARTIAL** — 4 bağlantı üretildi, kadans ve adım boyu kapsül hızına bağlandı; 4 evre ortalamasında sürükleme 18.9 → 15.2 cm, en kötü 42.8 → ~22 cm; erken/geç evre iyi, standart ve yarım-adım evresi kötü | **Üretimde** (tek ayarla geri alınır) |
| 3 Yerinde ters dönüşün ilk anı | **FAIL (aday ayrıldı)** — ilk kare kaydı yapıldı, neden ölçüldü; içerik adayı tekrarlarda V2.15'ten iyi değil | Üretimde **değil** (V2.15 klipleri geri yüklendi) |

Korunanlar (değişmedi, doğrulandı): V2.14 kaynak END/START düzeltmesi, fren→itiş bağlantısında başıboş jog/depar karelerinin
kaldırılması (Rev veri tabanlarında A_LB_Sprint_Fwd yok), rahat kol ayarları, kamera–girdi eşleşmesi (dirchange `cy`), diz üreteci +
leg_guard (her yazımda), idle/diz düzeltmeleri, çift zemin uyarlaması düzeltmesi, yedek/test kliplerinin üretim veri tabanlarından ayrılığı
(`verify_prod216.txt` PASS, §8). M1 hareket profili, anatomi, iskelet, kıyafet, harita, kamera kadrajı değişmedi. Yeni framework yok.

## 1. Kesiş → ters dönüş (Hedef 1) ve çömelme

### 1.1 Doğrulanan neden
- V2.15'te sağ kesiş (D) sonrası A ile ters istekte MM, ileri-geri fren pivotu `SHM215_Pivot_F_B_*` (A niyeti: geri yürüme) seçiyordu;
  GR kapsülü ise aktörü yeni yöne döndürüp **ileri** hızlandırıyordu (B niyeti). Pivotun kökü dönmediği için basılı top 79–96 cm
  süpürülüyor, zemine 8 cm batıyordu (v216t0/v215e2).
- MM kökü kapalı oynar: klibin kök yolu kapsül yolundan farklıysa basılı ayak kayar. Pencere/veri tabanı değişikliği bu farkı kapatamaz;
  hareketin kendisi kapsül yoluna yeniden yerleştirilmeliydi.
- Çömelme: kesiş kaynakları (SHM210_Sprint_Turn_*, satıcı 721 cm/s depar) pelvisi 87 → 66–71 cm'ye indiriyor, gövdeyi 35–49° öne
  eğiyor; 300–400 cm/s kapsülde bu "atletik hamle" okunuyor. Çalışma zamanı katmanları ek ~10° eğim ekliyor.

### 1.2 Üretilen içerik (yeni hareket)
- **Ölçülen kapsül yolları** (`paths216.py`): kesiş ve ters dönüşün gerçek kapsül hızı / yönü / aktör yaw profili.
- **`remap216.py`** (yazım aracı): kaynak klibin kökü bu kapsül yoluna oturtuluyor; her **duruş** (top zemine ≤2.5 cm) dünyaya tek
  noktada sabitleniyor (top pinlenir, topuk–parmak yuvarlanması korunur), salınım kareleri sınır hatalarını smoothstep ile eritir;
  yanal duruş genişliği ×0.75 (dar ayak yerleşimi), pelvis 80 cm tabana doğru %70 yükseltildi ama yalnız **duruştaki** bacakların
  erişimiyle sınırlı (0.985 × bacak boyu), gövde eğimi hıza bağlı tavanla (150 cm/s 15°, 300 cm/s 20°, 490 cm/s 26°) spine_01–03'ten
  geri alındı, boyun ters döndürülerek baş yönü korundu; dizler hip-göreli, ±3 kare yumuşatılmış ipucuyla çözüldü (diz ekseni sıçraması
  ≤44°/kare; satıcı kliplerinde ölçülen üst sınır 51°), leg_guard her yazımda.
- **8 yeni klip**: `SHM216_Cut_{L,R}_090_{L,R}foot` (kesiş; giriş 0.40–0.78) ve `SHM216_RevTurn_{L,R}_{L,R}foot` (B niyeti: yeni
  yöne dönüp ileri hızlanma; giriş 0.52–0.68; kuyruğu kapsülle birlikte 300 cm/s² ile 490'a hızlanır). Pelvis minimumu klipte
  66–71 → 75.8–77.2 cm, gövde eğimi tepe 43–49° → 29–35°.
- **Entegrasyon**: SHM210 orijinalleri SprintCut'tan çıkarıldı; RevTurn klipleri **her iki** Rev_L/Rev_R'de (çalışma zamanı iki kesiş
  yönünü de tek veri tabanına yönlendiriyordu → dönüş yönünü yörünge seçer), devamı RevPush / RevPushLow'da; Reface ve F_B pivot
  kopyaları ileri-ters veri tabanlarından çıkarıldı. **A niyeti** (Shift+S geri) kendi V1.3.5 SprintReversal yolunda, dokunulmadı.
- Uçuş evresi: ters istek anında iki temas sinyali de yanlışken L/R rastgele seçilmiyor — giriş karesini klibin kendi destek düzeni ve
  MM poz maliyeti belirliyor; havadaki ayak kilitlenmiyor (kilit yalnız duruşlarda).

### 1.3 Önce / sonra (olay pencereli; V2.15 = v215e2 üretim, V2.16 = v216z üretim; her hücre tekrarların en kötüsü)
| Durum | Sürüm | n | Sol net / sürükleme | Sağ net / sürükleme | batma kare | pelvis min / gövde eğimi |
|---|---|---|---|---|---|---|
| Sağ kesiş → A: ters giriş + dönüş | V2.15 | 3 | 36.8 / 60.2 | 79.4 / 96.2 | 13 | 75.3 / 58° |
| | **V2.16** | 3 | **2.8 / 14.2** | **31.8 / 35.4** | 2 | 75.2 / **40°** |
| Sol kesiş → D: ters giriş + dönüş | V2.15 | 3 | 22.3 / 28.1 | 36.3 / 42.4 | 8 | 77.6 / 51° |
| | **V2.16** | 3 | 18.3 / 20.4 | 17.7 / 33.6 | 0 | 75.5 / **43°** |
| Sağ: depar döngüsüne çıkış | V2.15 / V2.16 | 3/3 | 12.9/30.1 → **5.9/9.8** | 5.1/5.8 → 3.6/5.5 | 2 → 0 | |
| Sol: çıkış | V2.15 / V2.16 | 3/3 | 7.3/8.2 → **42.3/49.3 (gerileme)** | 5.6/8.3 → 7.5/11.5 | 1 → 5 | |
| Çok erken ters (D+0.15) | V2.15 / V2.16 | 1/3 | 47.8/79.5 → **6.9/6.8** | 9.2/12.6 → 13.8/16.1 | 4 → 5 | 74.0/39° → 79.8/32° |
| Geç ters (D+0.6) | V2.15 / V2.16 | 2/3 | 42.0/57.3 → 28.3/51.6 | 41.0/50.2 → **1.9/1.9** | 6 → 2 | 73.2/56° → 74.9/45° |
| Kesiş → S: kesiş penceresi | V2.15 / V2.16 | 1/3 | 29.3/44.4 → **0/0** | 12.6/16.8 → 19.9/25.8 | 5 → 6 | 73.6/59° → 75.3/**34°** |
| Kesiş → S: geri koşu girişi (A niyeti) | V2.15 / V2.16 | 1/3 | 0/0 → **74.2/90.4 (2/3 koşu)** | 1.4/3.1 → 48.0/60.7 | 0 → 4 | |
| S-kesiş (ikinci kesiş, çömelme) | V2.15 / V2.16 | 2/2 | 16.9/29.7 → 8.5/14.7 | 8.6/11.8 → **30.1/41.4** | 7 → 6 | 73.7/59° → **71.9**/45° |
| Kesiş sırasında tuş bırakma | V2.15 / V2.16 | 1/3 | 46.2/58.5 → 15.4/17.3 | 128.0/145.5 → **32.5/41.2** | 52 → 37 | 74.4/53° → 75.2/41° |

- Seçim zinciri (3+3 koşu tutarlı): `Cut_*@0.47` → `RevTurn_*@0.53` (doğru dönüş yönü) → RevPush devamı → depar döngüsü (+1.8 s).
- **Kalan / gerileme:** (a) ters girişte sağ ayak bir temasında 15–18 cm net (inişte blend sırasında yatay hızla iniyor; destek evresi
  uyumu tam değil), (b) sol kesişten çıkışta sol ayak 42–49 cm, (c) kesiş→S sonrası geri koşu girişinde 2/3 koşuda 61–90 cm (V2.14'te
  de 76 cm vardı; V2.15'in tek koşusu temizdi — kesin neden ayrıştırılmadı), (d) S-kesişte ikinci kesişte pelvis klipte 76 iken
  çalışma zamanında 71.9 cm (bir çalışma zamanı katmanı 4 cm daha indiriyor; katman ayrıştırması yapılmadı).
- **Görsel risk (sayfa `cut_reverse_before_after.jpg` f18–f20, `cut_crouch_before_after.jpg` S-kesiş f11–f13):** ters dönüş başlangıcında
  ve ilk S-kesişte dizler içe kapanıyor (ayaklar ayrık, dizler yakın) — yanal ayak yerleşimi ×0.75 daraltıldı, kalça genişliği aynı
  kaldı; ölçü araçları bunu yakalamıyor, görsel kabulde özellikle bak.
- Denenen ve bırakılanlar (kanıt: v216a4/a5): ters giriş ofseti 0.70 + geniş pencere (MM yine pencere başına girip yarı dönüşte
  diğer ayak varyantına geçti, sol temas 16–28 cm), dar geç pencere 0.76–0.88 (giriş temasları 17–35 cm, a3'ten kötü).

## 2. Yürüyüş → depar (Hedef 2) — PARTIAL, üretimde

### 2.1 Neden (ölçüldü)
V2.15 itiş klibi girişten sonra 0.40–0.67 s yürüme adımında kalıyor (144 cm/s), kapsül 152 → 300 cm/s hızlanıyor; ardından satıcı
depar hızlanmasının 0.20–0.27 s'lik adımlarını (721 cm/s ölçekli) oynuyor, adım boyunu stride warping uyduruyor. Basılı ayak itiş
sırasında 2–6 cm yüksekte "yüzüyor" ve 20–45 cm/s sürünüyor (yeni HOVER sınıfı, §5).

### 2.2 Üretilen aday
- `timewarp216.py`: girişten önce özdeşlik; girişten sonra hız = kaynak adım süresi / hedef adım süresi(kapsül hızı)
  ([132→0.53, 250→0.42, 350→0.35, 490→0.31 s]); `remap216.py` ile adım boyu kapsül yer değiştirmesine oturtuldu (stride warping'e
  bırakılmadı). 4 klip `SHM216_W2S_{L,R}foot_{a,b}`: a = basan ayağın orta duruşu [0.62, 0.89], b = geç duruş/karşı ayak erken
  [0.89, 1.16]; ayrı veri tabanı `PSD_SHM216_WalkLink` (V2.15 şeması). İlk sürüm (hıza göre zaman bükme) adımları 0.12–0.16 s'ye
  sıkıştırdı ve depar döngüsüne evre dışı çıktı (sol 23–57 cm) → kadans sürümüyle değiştirildi.
- Sonuç: girişten sonra kalan yürüme adımı 0.67 → 0.57 s / 0.40 → 0.37 s (az kısaldı); sonraki adımlar 0.30–0.36 s (depar döngüsü
  kadansı) — V2.15'te 0.20–0.27 s. Giriş gecikmesi aynı (Shift → itiş klibi 0.26–0.29 s), 300/420/480 cm/s zamanları aynı (M1).

### 2.3 Temas (Shift −0.1 … +1.8 s; V2.15 aynı oturumda ölçülen üretim)
| Zamanlama | V2.15 sol / sağ (net/sürükleme) | Aday sol / sağ |
|---|---|---|
| Standart (Shift 3.0) | 8.4/9.9 · 3.3/2.3 | 9.6/15.8 · 9.7/9.1 (kötü) |
| Erken (1.2) | 7.0/7.9 · 14.3/17.9 | 5.2/7.4 · 9.5/13.9 (iyi) |
| Yarım adım sonra | 2.1/3.1 · 11.7/12.4 | 10.3/17.2 · 18.9/20.7 (kötü) |
| Bir adım sonra | 4.0/4.0 · 25.5/31.8 | 5.8/6.3 · 10.7/16.2 (iyi) |
| İtişte Shift bırakma | 6.4/9.5 · 5.3/5.6 | 6.4/9.3 · 21.2/22.6 (kötü) |
| İtişte W+D | 20.3/32.9 · 4.2/11.1 | 8.1/31.5 · 8.5/7.9 |
| Kısa Shift dokunuşları | itiş yok (jog), ikinci kalkış yok | aynı |

Aynı oturumda tekrar ölçüm (nihai üretim koşuları v216f = V2.15 itiş, aday koşuları v216z/a7 = bağlantılar) ve bütün oturumların
havuzu (kötü ayağın sürükleme yolu, koşu başına; ortalama):

| Evre | Üretim (V2.15 itiş) | Bağlantılar |
|---|---|---|
| Standart | e2 9.9 / 6.5 / 8.6, a6 7.8, f 15.6 / 11.9 / 15.0 → **10.8** | a7 13.7 / 14.8 / 11.6, z 11.2 / 9.0 / 15.8 → **12.7** |
| Erken | e2 17.9 / 10.5 / 17.9, a6 42.8, f 20.1 / 17.1 / 18.5 → **20.7** | a7 9.3 / 9.7 / 9.7, z 13.9 / 11.8 / 9.5 → **10.7** |
| Yarım adım sonra | a6 12.4 (n=1) | a7 21.6, z 20.7 → **~21** |
| Bir adım sonra | a6 31.8 (n=1) | a7 16.3 / 16.1, z 16.2 → **16.2** |
| 4 evre ortalaması | **18.9** | **15.2** |

Karar: Shift anı yürüyüş döngüsünde her evreye eşit olasılıkla düşer; ortalama ve en kötü durum iyileşti, kadans gereksinimi karşılandı →
**üretime alındı (PARTIAL)**. Aynı oturumda bile koşudan koşuya ±5 cm oynuyor; standart ve yarım-adım evresi kötüleşti (MM her pencereye
**başından** giriyor → her bağlantı fiilen tek giriş karesi, ±0.13 s evre hatası). Geri alma: ABP `SHM211_DB_Push` ve
`SHM214_DB_GaitPush` = `PSD_SHM215_WalkPush`. Sonraki adım (yapılmadı): evre başına daha sık giriş noktası ya da destek evresine göre kapı.
(Ara karar: bağlantılar bir kez yalnız önceki oturumun V2.15 koşularına göre geri alınmıştı; aynı oturum ölçümü bunu düzeltti.)

## 3. Yerinde ters dönüşün ilk anı (Hedef 3) — FAIL, aday ayrıldı

### 3.1 İlk kare kaydı (yeni harness satırları `mpos` / `mslw` / `mbt`, v216a7_t_tiprev2)
| +s | montaj konumu | slot ağırlığı | aktör yaw | kilit | sağ top yolu (yükseklik) |
|---|---|---|---|---|---|
| 0.000 | 0.000 | 0.00 | 0.0 | 0.86 | 0.0 (0.3) |
| 0.039 | 0.039 | 0.25 | +25.9 | 0.81 | 1.3 (2.2) |
| 0.081 | 0.081 | 0.76 | +51.5 | 1.00 | 6.2 (1.8) |
| 0.129 | 0.130 | 1.00 | +78.6 | 1.00 | 14.0 (3.3) |
| 0.178 | 0.178 | 1.00 | +102.6 | 1.00 | 14.0 (sabit) |

- Montaj 0.12 s'de karışıyor (dinamik slot montajı); motor kaynağına göre kök hareketi ağırlıkla ölçeklenir, ama 180 klibi ilk
  kareden 650°/s döndüğü için daha poz büyük ölçüde idle iken aktör dönüyor; sağ top tam bu 0.13 s'de 14 cm yerde süpürülüyor,
  ağırlık 1 olunca sabit. İkinci etken: klibin başlangıç duruşu idle'dan geniş/önde (klip sol 12.7/20.6, sağ 10.3/16.8; idle sol
  8.3/13.4, sağ 7.4/15.1 cm). Kalan açı iki kez uygulanmıyor (aktör tam −90 → +90; montaj boyunca GR yaw yazmıyor).

### 3.2 Aday ve sonuç
- `tipstart216.py`: (a) klip zamanı karışma süresince 0.35×'ten 1×'e yumuşak başlıyor (kök dönüşü poz ağırlığıyla birlikte büyüyor;
  kayıp 0.04 s yerleşik kuyrukta geri alınıyor, uzunluk/notify/eğri zamanları aynı), (b) her ayağın ilk duruşu idle duruşuna
  yerleştirildi ve sonraki salınımda eritildi. İki ayak katı kilitlenmedi; sert kesme yok.
- 180 kliplerinde kötüleşti (90→180 tersinde sağ sürükleme 19 → 23–39 cm; idle'dan 180'de 0 → 6.8) → hemen geri alındı.
- 045/090/135'te tekrarlarda üretimden ayırt edilemiyor (90 → geri tersinde giriş, sağ ayak net: V2.15 e2 0.7 / 2.1 / 1.0, nihai üretim
  v216f 15.8 / 5.4 / 1.2, aday v216z 15.9 / 1.9 / 7.6 cm; 90 → 180 tersinde sağ: üretim f 9.8 / 9.4 / 13.6, aday z 12.6 / 12.6 / 5.6) →
  kazanç gösterilemedi, **geri alındı**; aday kopyaları `checkpoint/tipstart_candidate/` içinde. Kesinti duruşu koşudan koşuya çok değişiyor.
- Doğru çözüm yönü (yapılmadı): çalışma zamanında karışma süresince destek ayağının dünya konumunu tutan kısa köprü (FootPlacement
  bırakma eşiklerinin dönüş hızında aşılması bu kayıtta görüldü) — içerikle sabit bir idle referansına eşlemek kesinti durumlarını
  kapsamıyor.

## 4. Gerçek hareket referansı (yalnız erişilen metinler; video izlenmedi)
- Yan adım kesişi derlemesi ve 90° kesiş çalışmaları: geniş ayak yerleşimi ve kesiş bacağına doğru gövde yatması yüksek yük profili;
  önerilen: yanal ayak mesafesini azaltmak, gövdeyi dik / hedef yöne tutmak, frenlemeyi sondan bir önceki basışta yoğunlaştırmak
  ([Sports Med 2021](https://link.springer.com/article/10.1007/s40279-021-01448-3), [PMC8363537](https://pmc.ncbi.nlm.nih.gov/articles/PMC8363537),
  [Sports Med Open tablo](https://sportsmedicine-open.springeropen.com/articles/10.1186/s40798-020-00276-5/tables/7)) → dar yanal duruş (×0.75) ve eğim tavanı.
- Kendiliğinden yürü→koş geçişi: hızlanma önce adım frekansıyla, sonra adım boyuyla ([JEB 2013](https://cob.silverchair.com/jeb/article-split/216/16/3047/11528/Biomechanics-of-spontaneous-overground-walk-to-run),
  [Sci Rep 2017](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5435734/)) → kadans hedefli zaman bükme.
- Yerinde dönüş: tek ayak pivotu + diğer bacak itişi; adım dönüşü / pivot dönüşü sınıflaması ([Golyski 2017](https://sites.gatech.edu/p-golyski/wp-content/uploads/sites/755/2018/01/Golyski-2017-A-computational-algorithm-for-classifying-step-and-spin-turns-using-pelvic-center-of-mass-trajectory-and-foot-position.pdf),
  [Rhodes](https://www.xylenepower.com/Fisher%20Shotokan%20Turn%20Dynamics.htm)). 180° dönüş özgün makalesinin (Santoro 2021) yalnız künyesi görüldü.
- Ücretli kaynak / satın alma / harici yükleme yapılmadı.

## 5. Ölçüm (`Tools/SHME_V216_20261018/contact216.py`)
Zemin = harness'in her ayak altındaki çizgi izinin çarpma z'si (gzl/gzr, QA zemini ve eğim). Kalibrasyon ayak başına: b0 = top yavaşken
(<8 cm/s) yüksekliğin 10. yüzdeliği, a0 = top yerdeyken ayak bileği yüksekliğinin 10. yüzdeliği. Sınıflar: DRAG (düz basılı, top
>30 cm/s), pivot (bir uç sabit, diğeri dönüyor — hata değil), PIVSLIDE (pivot noktası kayıyor), SKIM (havada, <4 cm, >60 cm/s),
**HOVER** (havada, <6 cm, ≤60 cm/s: yere ulaşmayan "basılı" ayak), SINK (top −1 / bilek −1.5 cm altında), air. Temaslar ayrı
(2 kare kalkış = yeni temas). Doğrulama: idle net 1.3–1.6 cm, düz yürüyüş net 1.5–7, depar sürükleme 2–16 cm.
Yardımcılar: `sum216.py`, `crouch216.py`, `w2s216.py`, `tip216.py`, `prot216.py`, `final216.py`.

## 6. Koruma testleri (v216z = nihai üretim + o sırada tipstart dönüş adayı; dönüş senaryoları nihai üretimde v216f'de 3'er tekrar; `prot_v216z.json`)
Zorunlu zincirler: sağ kesiş→ters sol + ayna, erken/orta/geç ters, kesiş→S, fren bitmeden W (k_ws_w), kesiş/itişte tuş bırakma
(chain_scutrel), itiş bitmeden ikinci yön değişimi (r_kb2), farklı evrelerden yürüme→depar, TIP→ters→yürü (t_tiprev, a_tipw / a_tipwl),
idle→yürü→dur→yürü (a_restart2), eğim dur→dön→kalk (chain_slope_r / l). MM "None" seçimi 0, ikinci kalkış yok, montaj iki kez yok.
Tüm koşu penceresi (2.5 s … son) satırları raporun ekinde (`prot_v216z.txt`); olay pencereli karşılaştırma §1.3/§2.3.
Gecikmeler ayrı: girdi → kapsül tepkisi 0.26–0.29 s (itiş), animasyon geçişi = seçilen klibin ilk karesi (aynı satır), fiziksel
tamamlanma 300/420/480 cm/s 0.79/1.19/1.39 s (değişmedi).

## 7. Üretim, dosyalar, geri dönüş
- Üretimde (kaydedildi): `/Game/GraceRanger/SHME/Animations/V216/SHM216_Cut_*` ve `SHM216_RevTurn_*` (8 klip), veri tabanları
  PSD_SHM210_SprintCut, PSD_SHM215_Rev_L/R, PSD_SHM214_RevPush, PSD_SHM215_RevPushLow; SHM210 kesiş orijinalleri, Reface_180 ve
  SHM215_Pivot_F_B kopyalarının BranchIn'leri bu veri tabanlarından çıkarıldı (klipler duruyor).
- Üretimde (Hedef 2): `SHM216_W2S_{L,R}foot_{a,b}` + `PSD_SHM216_WalkLink`; ABP `SHM211_DB_Push` = `SHM214_DB_GaitPush` =
  PSD_SHM216_WalkLink (`promote216_w2s.py`; geri: `rollback216_w2s.py`). Diğer ABP değerleri V2.15 (LinkOn 1, LowSpeed 60, TipLock 1, PivFoot 0).
- Üretimde değil: tipstart kopyaları `checkpoint/tipstart_candidate/` (dönüş klipleri V2.15 ile sha eşit, verify kontrol ediyor).
- Harness: `qa_pie.py` montaj konumu/ağırlık/karışma satırları (`mpos`, `mslw`, `mbt`), `v212_run.sh` yeni senaryolar `p_w2s_mid /
  late / tap / dir / rel` (yedekler `checkpoint/*.pre216`).
- Geri dönüş: `Saved/Codex/SHME_V216_20261018/checkpoint/baseline_v215/` (ABP, pawn, profil, DA, bileşen, V210/V212/V214/V215/Turns
  klipleri, Rev/RevPushLow/SprintCut veri tabanları) + `pre_g2/`, `pre_remap/`, `pre_tipstart/`, `pre_w2s_cadence/`; editör kapalıyken
  kopyala. Yalnız Hedef 1'i geri almak: SHM210 orijinallerinin BranchIn'ini SprintCut'a, Reface/F_B kopyalarını Rev_L/R'ye geri hedefle
  (ya da baseline_v215 klip + veri tabanlarını geri koy).
- Doğrulama: `verify_prod216.txt` (PASS: sızıntı yok, uyuyan adaylar kapalı, satıcı LocoTransitions dosyası değişmedi),
  `scan_dormant_v216z.txt` (61 koşu SCAN_OK), `scan_dormant_v216f_tip.txt` (dönüş tekrarları yalnız itiş veri tabanı bayrağında farklı:
  o koşular bağlantılar geçici geri alınmışken koşuldu; ayakta dönüş itiş veri tabanını kullanmıyor).

## 8. Kabul
- Teknik: Hedef 1 PARTIAL (ölçülen iyileşme + 4 açık madde), Hedef 2 PARTIAL (ortalama/en kötü iyileşme, 2 evrede gerileme), Hedef 3 FAIL (aday ayrıldı, neden ölçüldü).
- Görsel: kayıtlar `pub/vid` (gerçek hız GIF + realtime AVI + 1/3 yavaş AVI; yan / çapraz / oyun kamerası, tam vücut, kesilmemiş kare),
  önce/sonra sayfaları `pub/img`. Görsel kabul ve oyun hissi kabulü **sende**; benim tarafımdan verilmedi.
