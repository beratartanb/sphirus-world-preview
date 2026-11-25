> Bu dosya 446b7a6'daki ara raporun kök neden ayrıntılarıdır. Son sayılar README.md ve data_final/ içinde.

# Sphirus World — İnsan fizikselliği ve hareket gerçekçiliği, 3. geçiş (2026-11-25)

> **ARA RAPOR.** Değişiklikler kaydedildi ve editör yeniden açılarak diskten doğrulandı. **Son doğrulama seti (46 girdi planı, 60/30/değişken Hz, düşme testi, 17 video) şu an çalışıyor**; bittiğinde bu rapor son ölçümler, videolar ve kare incelemesiyle güncellenecek. Aşağıdaki sayılar geliştirme sırasındaki tek tek kayıtlardan; nihai tablo değil.

**Durum: KISMİ.** Hareket geçişleri (P1), kol/şort, dönüş yatması, sprint duruşu (P2–P3 kısmen), çömelme-zıplama yasağı, koşu kamerası ve yorgunluk nefesi uygulandı. Bağlamsal tırmanma (P5), bölgeye göre çarpma tepkileri (P6), yeni düşme türleri, çevre algısında yeni iş, saç/kıyafet/yüz **yapılmadı**. Kullanıcı kabulü yazılmadı; AAA düzeyi iddia etmiyorum.

Proje: `sphirus_UE59` (UE 5.9), oyuncu `BP_HybridA_Player`, `AC_Sph_Motion`, `AC_Sph_Camera`, `ABP_Sph_GASP`.

## 0. Denetim (P0)

- Başka bir oturum (VF2/vf2c, 04:38'de bitmiş) oyuncu Blueprint'ini, kıyafet ağlarını ve saç kopyasını değiştirmişti. Kilidi bıraktığını ve kirli paket olmadığını doğrulayıp onun kayıtlı durumunun üstünde çalıştım. Onun bulgusu (bilek kalçanın içinden geçiyor, hareket sisteminin alanı) bu geçişte ele alındı.
- Oyuncuda gerçekten kullanılan bileşenler: `AC_Sph_Motion`, `AC_Sph_Camera`, `AC_PreCMCTick`, `AC_FoleyEvents`, `AC_VisualOverrideManager`, `AC_SmartObjectAnimation`, ayrıca **`AC_TraversalLogic` ve `MotionWarping`** (taban sınıftan miras; projenin zıplama tuşuna bağlı değil, hiç çağrılmıyordu).
- 2. geçiş değerleri yerinde (`RcOpen 150` vb.). Yedek: `Saved/UE59Work/mr3/ckpt0/` (6 varlık + SHA). Yazma manifestleri: `ue59_m29_mr3save1_052820`, `mr3save2_061528`, `mr3save3_062913`. Kullanıcı kaydı değişmedi (`10201b8b41b7`).

## 1. Hareket geçişleri (P1) — uygulandı

| | Önce | Sonra |
|---|---|---|
| Yürüyüş → koşu (180 → 415) | 0.37 sn, 1 adım | 0.7–1.0 sn, 2–4 adım |
| Duruştan koşuya | 0.62 sn, tepe ivme 921 | 0.8 sn |
| Duruştan sprinte | 1.04 sn | 1.6–1.7 sn, 4 adım |
| Koşu → sprint | 0.35 sn | 0.72 sn |
| Yürüyüş → hızlı yürüyüş (180 → 278) | ~0.3 sn | ölçüm son sette |
| Koşudan duruş | 0.47 sn, 96 cm, **1 adım**, 981 cm/s² | 0.75 sn, ~180 cm, 2 adım |
| Sprintten duruş | 0.50 sn, 138 cm, **1 adım**, 1602 cm/s² | 0.9 sn, ~315 cm, 4 adım |
| Dönerek yürüyüş başlangıcı | 0.15–0.18 sn, ayak 47 cm yer değiştiriyor | 0.37–0.47 sn, en kötü 3.3–5.3 cm (60/30/değişken Hz) |

- **Kök neden (hızlanma):** vites yükseltme ivmesi tek adımlık bir sıçramaya izin veriyordu (`GaitUpAcc 0.8`). Şimdi oyuncu vitese göre yayımlıyor (`GU_Run 0.38`, `GU_Tempo 0.16`).
- **Kök neden (duruş):** tuş bırakılınca doğrudan duruş klibine giriliyordu; sprint hızındaki momentum tek temasta yok oluyordu. Şimdi 350 cm/s üstünde bırakılınca karakter yürüyüş vitesi isteyerek hız yönünde "süzülüyor": mevcut rampalı hız sınırı ve koşu→yürüyüş geçiş klibiyle fren adımları atıyor, 320 cm/s'de normal duruş klibine giriyor. Adım sayısı bırakma hızına bağlı; sabit değil.
- **Güvenlik:** fren mesafesinde (uyluk yüksekliğinde iz) engel varsa veya zemin bitiyorsa süzülme hiç başlamaz; havada, çömelikken, geri giderken, tepki kilidinde ve herhangi bir tuşa basılınca da devre dışı. **Test:** açık alanda 289 cm'de duruş; 259 cm ileride duvarla süzülme 0 sn, duvardan 115 cm önce duruş. Uçurum/su kenarı **test edilmedi** (test haritasında yok).
- **Kök neden (dönerek başlangıç):** kalkış ivmesi klibe 1400 cm/s² tavanla bağlıydı; hareket eşleştirme dönüş başlangıç klibine ilk adımından sonra giriyordu. Duruştan kalkış tavanı 800'e indi. Dönüş çıkışları 1400'de kaldı: orada 800 yeni bir 24.8 cm kayma üretti, geri alındı.
- Ayak kayması (yerde) geliştirme kayıtlarında en kötü 1.4–2.1 cm; dokunuş planlarında 2.4–4.6 cm.

## 2. Kol anatomisi ve şort (P2) — uygulandı, kısmen

- **Ölçüm (görünür beden):** üst kol 26.8 cm (boyun %15.4'ü; yetişkin kadın referansı %18.6), ön kol 24.8 cm (%14.2; ref. %14.6), bilek yüksekliği boyun %52.6'sı (ref. ~%48.5). **Kollar uzun değil; referansa göre kısa.** Kemiklere dokunulmadı. "Uzun görünme" izlenimi için omuz eklemleri arası 24.8 cm (dar) ve kol duruşu daha olası nedenler; bunu görsel olarak doğrulamadım.
- **Kök neden (şorta girme):** duruş katmanı her kolu tek bir ortalama açıklık açısına sürüyordu, bacağın nerede olduğunu bilmiyordu. Yürüyüşte bilek uyluk yüzeyine 0.5 cm'ye kadar yaklaşıyordu (karelerin %22'sinde 3 cm'den yakın).
- **Çözüm:** her kol için bilek–uyluk ekseni açıklığı ölçülüyor; hedefin altına inince o kolun açıklık hedefi gerektiği kadar artıyor (hızlı açılır, yavaş kapanır). Yürüyüşte %22 → %3, en yakın 0.4 → 1.6 cm; boşta 3.0 → 5.1 cm.
- **Kalan:** koşu/yürüyüş duruş kliplerinde bilek birkaç kare boyunca hâlâ −1 ile −3 cm (bacağın içinde); düzeltme o kadar hızlı değil.
- **Geri hızlı yürüyüş:** klipte (`CM_af_Loco_Jog_Bwd`) bilekler pelvisin önünde 20 cm'ye kadar yaklaşıyordu. Geri giderken ek açıklık: bilekler arası en az 20 → 27–31 cm, dirsekler arası 30 → 40 cm.

## 3. Dönüşte "yılan" hareketi (P3) — kısmen

- **Ölçüm:** 90° dönüşte kalça hattı koşuda 23°, sprintte 35° yatıyor (düz koşuda 9–11°), pelvis 15–18 cm çöküyor.
- **Kök neden (doğrulandı):** satıcı dönüş kliplerinin içeriği (`M_Relaxed_Run_Turn_*_090`, `M_Relaxed_Sprint_Turn_090_*`: atletik, yatık kesme). Sürücü iskelet ve görünür beden aynı; benim eklediğim kalça, duruş ve pelvis katmanlarını kapatmak sonucu değiştirmedi — yani prosedürel katmanlar üst üste binmiyor.
- **Çözüm:** kliplere dokunmadan, klibin kalça yatmasının 14° üstündeki kısmının %60'ı geri alınıyor (yarısı omurgaya). Koşu 22.6° → 17.5°, sprint 34.8° → 25.6°; yana bükülme 10.4° → 8.4° ve 18.3° → 15.1°.
- **Kalan:** omuz–kalça burulma aralığı sprint dönüşünde ~51° (değişmedi); sprint 180° dönüşündeki havada dönüş ele alınmadı. Yanal ivmeye bağlı yeni bir eğilme eklemedim: klipler zaten dönüşe 5–10° yatıyor.

## 4. Sprint duruşu (P4) — uygulandı

Gövde eğimi koşuda 10.5°, sprintte yalnız 12.6° idi. Sprint hızında (430 cm/s üstü) üç omurga eklemine dağıtılmış ek eğim: sprint 16.4°, koşu değişmedi. Kol sürüşü, adım ritmi ve itiş mekaniği klipten geliyor, **değişmedi**.

## 5. Çömelikken zıplama — uygulandı

Zıplama tuşu çömelme durumunu kontrol etmiyordu; motor zıplamayı reddediyor ama tuş basılı kaldıkça isteği saklıyordu (ayağa kalkınca zıplıyordu), zıplama animasyonu da çömelik bedende oynuyordu. Tuş artık çömelikken yok sayılıyor. Test: çömelikken zıplama yok, tuş basılıyken ayağa kalkınca zıplama yok, çömelerek yürürken yok, ayakta normal. Ayağa kalkarken tavan kontrolü motorun kendi kontrolü; alçak tavanla **test edilmedi**.

## 6. Koşu kamerası (P11) — uygulandı

Kamera bileşeni hız terimlerine zaten sahipti ama koşuda kolu **uzatıyordu**. Koşu: 193 → 177 cm; sprint: 194 → 172 cm; görüş açısı sprintte 68.9° → 71.8°. Yeni sarsıntı, yatma veya bulanıklık yok; mevcut "hareketi azalt" seçeneği yeni terimleri de ölçekliyor. Ev içi ve tırmanma kamerası değişmedi.

## 7. Yorgunluk (P10) — kısmen

Nefes katmanı kısa süreli efora bağlıydı (duruştan ~3 sn sonra sönüyordu) ve yalnız üst omurgayı 1–2° döndürüyordu. Artık mevcut yorgunluk değerine de bağlı ve omuzları kaldırıyor: yorgun duruşta omuz hareketi ~1.75 → 2.95 cm. İkinci bir dayanıklılık sistemi yok. Adım, kol ve duruşta yorgunluğa bağlı yeni değişiklik **yok**.

## 8. Yapılamayanlar

- **Bağlamsal tırmanma / engelden atlama / kenara tutunma / duvar destekli çıkış / boşluk atlama (P5):** satıcı bileşeni zıplama tuşuna bağlayan değişiklik yazıldı, ama testte geçici blok satıcı sistemin beklediği kenar verisini üretmedi ve karakter normal zıpladı. **Kaydedilmedi; oyunda eski davranış sürüyor.** Eksikler: `LevelBlock_Traversable` dışındaki gerçek geometri için kenar tespiti, kadın iskeletinde doğrulanmış tırmanma animasyonları, el/ayak temas IK'sı.
- **Çevre algısı (P4/5):** yeni iş yok. Önceki turların temas sistemi (yakınlık, sıyırma, kol toplama, takılma sınıfları) duruyor.
- **Bölgeye göre çarpma tepkileri, yeni düşme türleri (P6–P8):** yapılmadı; mevcut öne düşme/kalkma son sette yeniden ölçülecek.
- **Saç fiziği, kıyafet, yüz (P13):** dokunulmadı.
- Gamepad/analog girdi, standalone, paket: denenmedi.

## 9. Değişen varlıklar

`/Game/Sphirus/Player/Motion/AC_Sph_Motion`, `/Game/Sphirus/Player/Camera/AC_Sph_Camera`, `/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player`. Satıcı klipleri, haritalar ve kullanıcı kaydı değişmedi. Her değişiklik parametreyle kapatılabilir (`CS_On`, `CA_On`, `TLM_On`, `PS_S2..4`, `BR_Sh`, `GU_*`, kamera değerleri). Betikler: `scripts/`.

## 10. Bekleyenler

Son doğrulama tablosu (60/30/değişken Hz), performans karşılaştırması, video listesi, kare incelemesi ve "değişiklikler kapalı" karşılaştırma videoları bu rapora eklenecek.
