# Sphirus World — 5. geçiş: beden, saç, darbe ve düşme (2026-11-25 → 26)

**Durum: KISMİ.** Bu geçişte beden formu (B5 → B13), kapalı MetaHuman gövde, topuz saç, bölgesel darbe tepkisi ve aktif ragdoll ile düşüp kalkma oyuna girdi ve kaydedildi. Durma klibi sonrası ayak hizalama adımı, 180° dönüş varyantı, sırt üstü kalkma klibi, kenara asılma / uzun atlama ve yüz kimliği **yapılmadı** (gerekçeler 8. bölümde). Kullanıcı kabulü yazılmadı: kullanıcı oynayıp onaylamadı. AAA iddiası yok. Gövde kas yüzeyi prosedürel; sanatçı elinden çıkmış (artist-grade) değil.

Her şey kaydedildi ve editör **yeniden başlatıldıktan sonra diskten okundu** (`data/state_after_restart.txt`). Kullanıcı kaydı değişmedi (`SFSaveSlot.sav` sha1 `10201b8b41b7`). Satıcı orijinallerine yazılmadı. Paylaşılan MetaHuman common klasörü sha1 ile değişmemiş doğrulandı. Gövde kil (çıplak) karşılaştırmaları bu depoya **konmadı**; yalnız oyun içi giyinik görüntüler var.

Kaydedilen başlıca varlıklar: `BP_HybridA_Player`, `AC_Sph_Motion`, `/Game/Sphirus/CharacterLab/B5…B13_20261126` (gövde + 6 kıyafet; oyuncuda **B13**), `B13_20261126/Hair/GB_Sph8_HairMainH1`, `GB_Sph8_HairLooseH1`, `SM_Sph8_ScalpCover`, `M_Sph8_ScalpCover`, `SphF_am_InjuredBelly_DropToFloor_GetUp` (proje kopyası, kök hareketi açıldı). Manifestler `Saved/UE59Work/r9/manifests.txt` içinde.

## 1. Hareket altyapısı (geçişin başı)

- **Poz geçmişi:** `PoseSearchHistoryCollector`, sürücü animasyon grafiğinde RemapCurves'ün hemen arkasına alındı (`m_pshist_mcp.py early`). İzole A/B ile kanıtlandı: geç kollektörde 180° havada dönüş 75–77°, erken kollektörde 38–44°. Projenin düzeltmeleri hareket eşleştirmenin geçmişine geri besleniyordu.
- **Traversal yaklaşma hızı:** seçim artık anlık hızla değil, sönümlenen zemin hızı tepesiyle yapılıyor (`TR_SpPk`, 450 cm/s²). Koşarak gelinen 60 cm kutuda doğru varyant seçiliyor: duran adım yerine koşarak aşma.
- **Telemetri:** `sph-tele/5.1` sürümlü ve alan adıyla kayıt (`hk_tele5.py`). Eksik alan olursa yükleyici hata veriyor; eski indeks uyuşmazlığı hatası kapandı.
- **Omuz kuşağı duruşu:** `PS_ShL` 5.7 → 6.9, `PS_ShF` −0.7 → −1.6, sırt üstü yuvarlaklığı `PS_B3` −5.

## 2. Beden formu B5 → B13

Kullanıcı yönlendirmesi: ince ve doğal referans, sonra T/A-poz referans sayfası (atletik-ince gövde). İstenenler: kas ve doku gerçekçiliği, bacak arası modelleme.

| Sürüm | Değişiklik |
|---|---|
| B5 | Orijinal Sph8 + hafif delta: bel 63.0 → 65.7, kalça 97.0 → 95.9 |
| B7–B8 | Bel bandı; bel genişliği ×0.84, ön ×0.90. Kol alanları artık kolları da etkiliyor (`armless:0`) |
| B9 | Atletik: kalça / dış uyluk inceltildi, V-şekil (lats), baldır, küçültülmüş göğüs |
| B10 | Prosedürel kas katmanı (vastus medialis/lateralis, IT band, hamstring ayrımı, gluteal kıvrım, gastroknemius başları, deltoid yapışma, kürek kemiği, linea alba) |
| B11 | **Kapalı gövde** (aşağıda) |
| B12 → B13 | Kullanıcı isteği: bel yanlardan "çok azcık", sonra "birazcık daha" genişletildi. En dar bel genişliği 19.5 → 20.4 → **21.0 cm**, çevre 57.7 → 59.2 → **60.3 cm**; derinlik, kalça ve göğüs aynı. Kullanıcı: "Şimdi iyi" (görsellerden; oynanarak verilmiş bir kabul değil) |

**Kapalı gövde (B11).** MetaHuman gövdesi bir kıyafet seçimiyle kurulduğu için bel bandında, kalça yanlarında ve bacak arasında yüzleri silinmişti. Delik doldurma denemeleri reddedildi (kapak gibi düz yüzeyler, içe çöken yamalar). Karakteri kıyafetsiz yeniden kurmak üç kez başarısız oldu: bellek yetmedi, kontrol rig bağlantı hatası verdi, takıldı. Uygulanan çözüm şu:

- Eklentinin tam şablon gövdesi (`SKM_Body`, 30 455 nokta) kullanıldı.
- B10'un 29 711 noktası UV ile, UV dikişlerinde konumla şablona eşlendi. Hepsi eşleşti; eksik 744 nokta tek bir bölge.
- Bu bölgeye B10 şekil farkı biharmonik olarak taşındı.
- Eşleşen noktalarda B10'un deri ağırlıkları ve normalleri korundu. Bölgedeki ağırlıklar kenarla sürekli olacak şekilde harmonik düzeltildi.
- Sonuç MetaHuman'ın standart, müstehcen olmayan anatomisi. Açık genital modelleme yapılmadı; kullanıcıya bildirildi.
- **Açık:** LOD1–3 hâlâ eski, delikli gövde.

## 3. Saç: topuz

- Onaylı C49 h1 topuzu (ana saç + gevşek tutamlar) UE59'da zaten vardı.
- GD38 → Sph8 transfer bağıyla oyuncuya takıldı, rengi mevcut bakır `MI_Sph_Hair`. Gevşek tutamlar yüze bağlı ayrı bir bileşende.
- **Tepe lekeleri:** Saçsız çekim kanıtladı ki lekeler tellerin arasından görünen açık bej kafa derisi.
  - Düzeltme: saç köklerinin altına koyu bakır, 1.2 mm kalkık bir kafa derisi örtüsü.
  - Örtünün kenarı saç çizgisinden 1.6 cm içeride; ayrık çizgisi boşlukları dolduruldu.
  - Oyun başında `head` soketine bağlanıyor. Python bu soketi ayarlayamadığı için BeginPlay'e tek bir satır eklendi.
- Kanıt: `evidence/hair_bun_board.jpg`, `evidence/hair_crown_board.jpg`, `p5VID_hcV_*`.

## 4. Bölgesel darbe tepkisi

- Vurulan bölgenin kemikleri sürücü gövdede kısa süre fiziğe geçiyor, PhysicalAnimation motorlarıyla poza tutuluyor ve 0.6 sn'de animasyona geri karışıyor.
- Görünen gövde sürücünün pozunu kopyalıyor.
- **Ölçüm** (`data/impacts.txt`, duruşta):
  - Göğüs itmesi: baş ~15 cm geri, kollar ataletle öne.
  - Baş darbesi: baş ~13 cm, omuzlar ~5 cm.
  - Omuz darbesi: gövde 4–14 cm o yana, kol geride kalıyor.
- Yorgunluk kasları zayıflatıyor (`IMP_FatK`). Tüm üst gövdeye gelen güçlü darbe (≥ 6 m/s) sendeletme değil düşme başlatıyor.
- **Bulunan tuzaklar:**
  - Darbe yalnız tek gövdeye verilince eklem sınırları onu yutuyor.
  - Motor gücü 900 olunca tepki görünmüyor.
  - Sıfır vektörlü `LaunchCharacter` bile karakteri "havada" moduna sokuyor; koşarken 20–30 cm iniş çömelmesi yapıyordu. Artık yalnız itme > 0 iken çağrılıyor.
- Videolar: `p5VID_imp4_idle`, `p5VID_imp6_walk`.

## 5. Düşme: aktif ragdoll ve yüzüstü kalkış

Kullanıcı ilk sürümü haklı olarak "cansız manken gibi" buldu: kaslar gevşiyor, gövde son pozunda donup devriliyordu. Şimdiki sürüm:

- **Düşüş sırasında kaslar çalışıyor.** Eklem uzayındaki motorlar, sürücünün DefaultSlot'unda oynayan bir hedef poza doğru çekiyor.
  - Devrilirken: düşüş yönüne göre GASP korunma uzanması (öne, arkaya, sola, sağa). Kollar yöne uzanıyor, baş kalkıyor, dizler yumuşuyor.
  - Yere inince (0.8 sn): gövdenin o anki yönüne göre yerde pozu; yüzüstüyse kollar omuz altında, sırt üstüyse kıvrık.
- **Fiziki durum düşüşü şekillendiriyor:**
  - Kas gücü = 1 − 0.55 × yorgunluk.
  - Düşüş vücudun hızını taşıyor; koşarken düşen öne atılıp ellerinin üstüne kayıyor.
  - Darbe şiddeti yerde kalma süresini belirliyor.
  - Yorgunken kalkış daha yavaş.
- **Tetikleyiciler:** güçlü darbe, yaklaşık 6 m üstü sert iniş (dikey hız < −11 m/s), ya da `FL_Fire`.
- **Yön testi** omuz çizgisiyle yapılıyor (bükülü bacaklarda uyluk tabanlı test yanılıyordu). Sırt üstüyse gövde uzun ekseni etrafında, yüksekte kalan omuz üstten geçecek şekilde dönüyor.
- **Kalkış:** Kapsül ragdoll'un yerine ve yönüne taşınıyor, leğen kinematiğe alınıyor, mesh konumu sıfırlanıyor. Yüzüstü kalkma klibi kök hareketiyle oynuyor, fizik 0.75 sn'de devrediliyor. Ragdoll boyunca kapsül leğeni izliyor, böylece kamera gövdeyi kaybetmiyor.
- **Bulunan kritik hatalar:**
  - Tüm gövde fizikteyken leğen kök gövdesi mesh bileşenini sürüklüyordu; bileşen 150 cm kayık ve 77 cm havada kalıyor, kalkıştan sonra karakter çömelik duruyordu.
  - Kullanılan ilk "yerde" pozu aslında sırt üstü bir pozdu; her düşüşü sırta çeviriyordu.
  - Doğrusal yuvarlanma itişi karakteri 1 m havaya fırlatıyordu.
- **Testler** (`data/falls.txt`): arkadan, önden, yandan itme; 0.9 yorgunlukla itme; koşarken düşme; 6.5 m'den düşme. Hepsi yüzüstü bitip ayağa kalkışla sonuçlandı. Olaysız yürüyüş etkilenmedi (leğen en düşük 82 cm).
- Videolar: `p5VID_af4_back`, `p5VID_af4_side`, `p5VID_af4_tired`, `p5VID_af3_run`, `p5VID_af5_drop`, `p5VID_af5_walk`. Kareler: `evidence/af4_board.jpg`, `af3_run_board.jpg`, `af5_board.jpg`, `fall_drop_board.jpg`.
- **Kusurlar:**
  - Kalkış başında kol bir an yukarı kalkıyor (klipten mi, geçişten mi, ayrılmadı).
  - Sırt üstü kalıp dört denemede dönemezse yüzüstü klip yanlış pozdan başlıyor.
  - Koşarken düşüşte bacaklar biraz fazla havaya kalkıyor.
- Not: `af4_*` kayıtları darbe-yorgunluk ayarı ve 0.75 sn geçiş eklenmeden önce alındı; `af5_*` son kaydedilmiş hâl.

## 6. Doğrulama ve ölçüm notları

- Kayıtlar sabit 16.7 ms oyun adımıyla alındı. Bunlar FPS kanıtı değil.
- Oyun içi görüntüler yalnız giyinik karakteri gösteriyor. Gövdenin kapalı yüzeyi kil görünümünde özel olarak kontrol edildi ve kullanıcıya gösterildi.
- B13 oyun içi kontrol: duruş ön/arka/¾ ve koşu; kıyafetten taşma görülmedi (`evidence/b13_ingame_board.jpg`).

## 7. Kalan ve engellenen işler

| İş | Durum | Neden |
|---|---|---|
| Durduktan sonra ayak hizalama adımı | **yapılmadı** | Satıcı PoseSearch veritabanlarının girişleri Python'dan değiştirilemiyor, AnimBlueprint MCP DSL ile düzenlenemiyor. Satıcı orijinallerini değiştirmek proje kuralına aykırı; kopyalar betikle oyuncuya bağlanamıyor |
| 180° dönüş klip varyantı | **yapılmadı** | Aynı veritabanı engeli |
| Sırt üstü kalkma | **klip yok** | Projede yalnız yüzüstü kalkma var; Core Motion "Knockdown" klipleri yere inmiyor, "Kickdown" yerde bitiyor |
| Kenara asılma, tırmanma, uzun atlama | yapılmadı | SK_Mannequin kliplerinin retarget'ı gerekiyor |
| Kol yolu, entegre parkur | yapılmadı | — |
| Yüz kimliği (referans sayfası) | başlanmadı | Kimlik değişikliği; önce kapsam gösterilecek, referans dosyası diskte yok |
| LOD1–3 kapalı gövde | açık | Yakında LOD0 kullanılıyor; bölge kıyafet altında |

## Dosyalar

- `videos/`: 11 oyun içi kayıt (giyinik).
- `evidence/`: oyun içi kare panoları.
- `data/`: darbe ve düşme ölçümleri, bel ölçüleri, şablon eşleşme raporu, yeniden açılış okuması.
- `scripts/`: MCP grafik düzenlemeleri (`m_impact*`, `m_fall*`, `m_scalp_attach`), kapı arkasındaki yazma işleri (`w_*`), test kancası `hk_imp.py`, `an_imp.py`, `b11_match.py` (şablon eşleme), `scalp_region.py`, varsayılanlar `c_p5_defaults.py`.
