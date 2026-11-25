# Sphirus World — Hareket gerçekçiliği, 4. geçiş (2026-11-25)

**Durum: KISMİ.** Başlangıç: `f4a76ec` raporu; çalışma kopyasında o tarihten sonra değişiklik yoktu (varlık zaman damgaları kontrol edildi), başka oturum yazmıyordu, kilit bu oturumdaydı. Beden/kıyafet/ölçü çalışması yapılmadı. Kullanıcı kabulü yazılmadı; AAA iddiası yok.

Oyunda kalan (kaydedildi, editör yeniden açılınca diskten okundu): **fren yardımı v3.1**, **ivme eğilmesi**, **klip-özel kol yolu**, **yakın yüzey farkındalığı**, **gerçek geometride traversal**. Denenip **geri alınan** (ölçüm kötüleştirdi): durduktan sonra ayak tutma, 180° havada dönme tutma. **Yapılmayan**: bölgesel darbe tepkileri, arka/yan düşüş, yorgunluğun kol/adım etkisi, kamera ivme tepkisi.

Kaydedilen varlıklar: `BP_HybridA_Player`, `AC_Sph_Motion`, yeni `/Game/Sphirus/Player/Traversal/AC_Sph_Traversal` (GASP `AC_TraversalLogic` kopyası; satıcı orijinali değişmedi). Manifestler `ue59_m29_travc_192414`, `p4save1_200418`, `p4save2_210044`. Kullanıcı kaydı değişmedi (`10201b8b41b7`). Her davranış bir parametreyle kapatılabilir (`CS_On`, `AW_On`, `TR_On`, `PS_AbdBwd`, `AL_Deg`; geri alınanlar `SH_On 0`, `ATH_On 0`).

## 0. Ölçüm düzeltmeleri (13)

- `an_loco4.py`: 0 → 415 artık "duruştan koşu kalkışı"; destek = ayağın sallanma + iniş fazı (aynı ayağın birkaç kare arayla yeniden algılanması sayılmıyor, bölüm başında zaten basan ayak sayılmıyor); bölüm içinde durmayan hareket "DURMADI (son hız)" yazıyor; durduktan sonra ayak hareketi ve erken idle ayrı bayrak; yeni tuş → fren yardımının kesilmesi süresi ölçülüyor; **gerçek kare süreleri** raporlanıyor.
- `an_coast5.py`: engel mesafesi X farkı değil, kapsül çemberi ile döndürülmüş kutu arasındaki **geometrik** mesafe.
- `armsurf5.py`: nötr pozdaki kıyafet ofseti çıkarılmıyor; ince kıyafetin normalinden "içeride" işareti üretilmiyor. Her karede pozlanmış şort + uyluk derisinin 3 cm yükseklik dilimindeki dış hattı (kasık üstünde tek, altında bacak başına) kuruluyor; el noktası hattın içindeyse derinlik = hatta uzaklık. Temas süresi yalnız **ardışık karelerden**.
- Kayma: zemin temasıyla filtrelenen ("ground") ve klip eğrisi ("curve") ayrı.
- **FPS**: kayıtlar sabit 16.7 ms oyun adımıyla, gerçek kare süresi p50 ≈ 42 ms (kayıt maliyeti). "30/değişken" planlar oyun adımını değiştiriyor; bunlar FPS kanıtı değil. Oyunun kendi FPS'i bu turda ölçülmedi.

## 1. Yürüyüş–tempo–koşu–sprint geçişleri (2) — kısmen

**Bulunan kök neden (duruşlar):** satıcı Relaxed duruş kliplerinin hepsi, kök hızı sıfırlandıktan 0.3–0.7 sn sonra **sabit bir "ayak hizalama" adımı** içeriyor (yürüme duruşu: sağ ayak 18 cm, klip 2.0–2.4 sn; `probe_stopclip.py`). Oyunda bu adım kapsül durduktan 0.6–0.9 sn sonra oynuyor; ayaklar klibin beklediği yerde olmadığı için adım bazen **geriye** atılıyor (−20 cm). Her duruşta durduktan sonra 14–29 cm ayak hareketi, 1–2 ek destek.

| Değişiklik | Oyunda | Kanıt | Kalan |
|---|---|---|---|
| **İvme eğilmesi** (`AC_Sph_Motion.AccLean`): ölçülen ileri ivmeye göre gövde 700 cm/s²'de 5° öne, frende 900 cm/s²'de 3° geriye; mevcut efor/eğim eğilmesine ek, hızlı | kalkışta gövde hareketi önceden "yükleniyor", frende hafif geri | `p4VID_starts_side2.mp4` | görsel etkisi küçük; açı ölçümü raporlanmadı |
| **Durduktan sonra ayak tutma** (`SH_*`, görünür beden ayak IK'sı) | **geri alındı**: hizalama adımını kaldırdı (ek destek 2 → 1) ama bırakıldığı anda ayak 15–25 cm **kaydı** (idle slot animasyonu başlarken, dönerek kalkışta) ve oyun başında bir ayağı yukarı çekti | `data/slide.txt` (tutma açıkken: 15–25 cm kaymalar), `data/slide5.txt` (kapatıldıktan sonra: en kötü 1.5–2.3 cm) | **açık**: doğru çözüm, hizalama adımı kırpılmış proje kopyası duruş klipleri; PoseSearch veritabanı girişleri 5.9'da Python'dan değiştirilemiyor, editör arayüzü işi |

Ölçülen (kaydedilip açılmış durum, 60 Hz oyun adımı, `data/loco5.txt`): yürüme durması 0.50 sn / 54 cm; tempo 0.60 sn / 109 cm; koşu 0.62–0.83 sn / 133–192 cm, 2–3 destek; sprint 0.88–0.92 sn / 297–303 cm, 2–3 destek — sabit değil, hıza ve destek ayağına bağlı. Kalkış: duruştan koşu 0.85 sn (%90), duruştan sprint 1.60 sn. Kısa dokunuşlar: 0.15 sn yürüme 12 cm, 0.25 sn koşu 21–24 cm yer değiştirme; ama ardından hizalama adımı ayakları 15–27 cm daha oynatıyor (**açık**, yukarıdaki nedenle). Yürüme→tempo klip atlaması **ele alınmadı**.

## 2. Fren yardımı ortam boyunca (3) — uygulandı, doğrulandı

**Değişiklik (`m_coast5/6`):** artık **her karede** yeniden değerlendiriliyor. Önce yol boyunca zemin profili (kapsülün ön kenarında 1 + yol boyunca 10 yoklama, aralık ≤ 32 cm): her yoklama **bir önceki desteklenen yoklamaya** göre ±(35 cm + aralık × 0.36) içinde ve yürünebilir olmalı — boşluk, uçurum kenarı, desteksiz yüzey burada biter. Sonra ölçülen eğimi izleyen, 25 cm (çıkılabilir basamak) yükseltilmiş kapsül süpürmesi; yalnız yürünemeyen yüzey engel sayılıyor. Bütçe her karede güncel konumdan. Eğim/merdivende yavaşlama 900 cm/s² (kapanmıyor).

| Sahne (sprint 584 cm/s bırakma) | v3 öncesi | Şimdi (kaydedilmiş durum) |
|---|---|---|
| Açık alan | 289 cm | 288 cm, 0.90 sn |
| Duvar 260 cm | duvara 57 cm | duvara **75 cm** (geometrik) |
| 45° köşe | — | duvara **29 cm** |
| 35 cm alçak kutu | (v3'te üstüne çıkıp takılma/düşme) | yardım yok, kutuya **21 cm** |
| 60 cm platform kenarı | (v3'te kenardan düştü) | yardım yok, platformda kaldı |
| Merdiven | yardım hiç başlamıyordu | süpürme engellemiyor; temas sisteminin merdiven hız kuralı devralıyor, 155 cm'de basamakta duruş |
| 12° rampa | — | kontrollü yavaşlama, 264 cm |
| 110 cm dar geçit | — | beden sığıyor, devam |
| Hareketli engel | — | bütçe 283 → 74 cm'ye düştü, yardım erken bitti (test kutusu sonra duran karaktere çarptı: test kusuru) |
| Yeni yön / çömel / zıpla / tekrar basma | — | yardım 1–3 karede (0.017–0.05 sn) kesiliyor |

Video: `p4VID_brake_wall.mp4`. **Açık:** su — test haritasında su yok, evdeki göl kenarında test edilmedi.

## 3. Kol–şort kesişmesi (4) — kısmen

Düzeltilmiş ölçümle (bkz. 0) satıcı kliplerinde el pelvis önünü kesiyor: geri tempo başlangıcı (`CM_af_Loco_Jog_Bwd_Start`) 6–8 cm, geri koşu durması (`M_Relaxed_Run_Stop_B_*`) 1.4–10.8 cm (koşudan koşuya çok değişken), ileri tempo (`CM_af_Loco_Jog_Fwd`) 2–4 cm / ~0.3 sn.

- Kol açıklık geri beslemesine pelvis-önü terimi (A/B `p4A0/p4A1`): **sağlam iyileşme yok** (bir yerde 6.4 → 4.2, başka yerde 1.4 → 7.3). Kapalı.
- **Uygulanan:** klip-özel kol yolu (`PS_AbdBwd 9°`, `PS_AbdFwdJog 4°`): yalnız bu klipler seçiliyken kolların açılma hedefine küçük, yumuşak (6/sn) ek; başka her klipte sıfır, kalıcı açık kol yok.
- Sonuç (`p4A2`): geri durma en kötüler arasından çıktı; geri tempo başlangıcı hâlâ **7.5 / 4.9 cm** (önce 7.7 / 6.4); ileri tempo 3.5 cm / 0.26 sn. **Açık.**
- Ölçüm ile görüntü aynı karede **doğrulanmadı** (kemik kayıtları videosuz alındı). Video: `p4VID_tempo_front.mp4` (ölçümle aynı kayıt değil).

## 4. Dönüş ve sprint (5) — açık

- Yeni 180° havada dönme tutma (kalça yaw'ı uçuşta karşı döndürülüp destekte bırakılıyor) iki işaretle de **kötüleştirdi**: uçuştaki pelvis dönüşü 38–55° → 64–77°, uçuş 0.25 → 0.35 sn (görünür pozun değişmesi hareket eşleştirmenin poz geçmişini etkiliyor). **Kapatıldı** (`ATH_On 0`).
- Kaydedilmiş durumda (`data/turn.txt`): `Sprint_Turn_180_R_Lfoot` uçuşta 55°, `L_Rfoot` 9–18°; omuz–kalça burulma aralığı ~52°. Sprint baş/boyun/kol koordinasyonunda **değişiklik yok**.

## 5. Yakın yüzey farkındalığı (6) — uygulandı

**Değişiklik (`m_aware`):** göğüs hizasında her yana bir yan, bir çapraz-ön küre yoklaması; açıklık c = min(yan, 0.7 × çapraz). Histerezis: 32 cm'de devreye, 45 cm'de çıkış; güç hıza bağlı (30 cm/s altı sıfır), giriş 5/sn, çıkış 2.5/sn. Çıktılar mevcut sahiplerde: yakın kolun açılma hedefi −6° × güç (uyluk açıklığı korunuyor), gövde yaw'ı ±7° × güç (`SphSpineRot`), devreye girişte kısa baş bakışı (8°, ~0.7 sn sönüm).

**Ölçülen (duvar boyunca yürüme+koşu, A/B):** kapsül yolu iki kayıtta da tam y = 2000 (**yön değişmiyor, mıknatıslama yok**); güç en fazla 0.73; gövde komutu −5.1°, baş −2°; sağ el–duvar en yakın 17.6 → 19.1 cm. Video: `p4VID_aware_game.mp4`. **Sınır:** gövde yaw işaretinin görüntüde doğru yöne gittiği ayrıca doğrulanmadı; gerçek çarpışma tepkisi mevcut temas sisteminde ayrı.

## 6. Traversal (7) — kısmen uygulandı

**Neden önceki bağlantı çalışmıyordu:** GASP kontrolü yalnız `LevelBlock_Traversable` aktörlerini kabul ediyor; seçici düğümü grafik araçlarıyla düzenlenemiyor.
**Değişiklik (`m_trav6`):** zıplama tuşunda oyuncu gerçek geometriyi yokluyor — yüzeye bakan dik yüz (30 cm üstü), yürünebilir üst, derinlik, arka zemin, **baş boşluğu** (kenarın önünde ve üstte/üzerinden ayakta kapsül), erişim (durarak 110, yürüyerek 170, koşarak 260 cm). Seçim: < 35 cm hiçbir şey; ince engel (≤ 70 cm derin, arka zemin var, ≤ 130 cm) → hurdle; ≤ 160 cm → mantle; ≤ 260 cm → 2.5 m tırmanma; daha yüksek → normal zıplama. Varyant = hız (dur/yürü/koş) + o an basan ayak. Proje bileşeni `SphTraversal` motion-warping'li montajı oynatıyor (uzuv esnetme/ışınlama yok, kök ölçülen kenarlara bükülüyor).

| Engel | Sonuç (kaydedilmiş durum) |
|---|---|
| 60 cm kutu (koşarak) | hurdle (yürüme varyantı), arkasına iniş |
| 90 cm kutu (yürüyerek) | hurdle (durarak varyantı) |
| 150 cm platform | mantle → üstte (z +150) |
| 240 cm platform | 2.5 m tırmanma (ayak duvarda, eller kenarda) → üstte (z +240) |
| 330 cm duvar | reddedildi → normal zıplama |

Videolar: `p4VID_trav_h60/h150/h240.mp4`; senkron kareler `evidence/traversal_frames.jpg` (150 cm: duvara ayak + kenara uzanma + üstte çömelme; 240 cm: duvarda tırmanma + üste çıkış) — bu kareler görsel olarak incelendi.
**Açık:** kenarda **asılı kalma**, asılıyken yukarı çekilme/bırakma ve uzak hedefe **atılma** yok (projede yalnız `SK_Mannequin` iskeletinde asılma klipleri var; retarget gerekli). Mevcut temas sisteminin önceden frenlemesi koşu hızını düşürüyor (tuşa basıldığında 31–36 cm/s) → çoğunlukla durarak varyantı seçiliyor.
**Alçak tavan (doğrulandı):** 120 cm tavan altında çömelme çalışıyor, ayağa kalkma reddediliyor, zıplama yok sayılıyor ve biriktirilmiyor; tavandan çıkınca ayağa kalkıyor (`p4VID_ceil.mp4`).

## 7. Darbe, düşme, yorgunluk, kamera (8–11) — yapılmadı

- **Darbe:** önceki turların temas sistemi duruyor (önden duvar/bel/diz yoklamalarıyla ağırlık, yana göre sendeleme klibi, sıyırma, takılma → tökezleme/öne düşme, arkadan çarpma, aynı nesneye ayrılmadan yeniden tetiklenmeme). Omuz/kol/bacak bölgesine ve yana/arkaya göre ayrım **eklenmedi**.
- **Düşme:** yalnız öne düşme + kalkış var. Oyuncuda GASP'ın `Ragdoll_Start/End` fonksiyonları ve ragdoll poz kaynakları bulundu (görünür beden sürücüden retarget edildiği için kullanılabilir), ama bağlanmadı. Ayak ucunun engele 3.5 cm girme kusuru **açık**.
- **Yorgunluk:** mevcut `Fat` hıza ve nefese etki ediyor; kol taşıma/adım/duruşa etkisi **eklenmedi**.
- **Kamera:** 3. geçiş ayarları duruyor; ivme/fren tepkisi **eklenmedi**.

## 8. Sistem öncelikleri (12)

Fren yardımı: montaj (traversal, tepki), havada, çömelme ve yeni tuş ile kapanıyor. Farkındalık: yerde ve 30 cm/s üstünde; traversal sırasında hareket modu uçuş olduğu için kapalı. Traversal: çömelikken ve iki elle taşırken başlamıyor. Kapalı olanlar (`SH_On`, `ATH_On`) hiçbir pozu etkilemiyor.

## 9. Regresyon ve performans

Kaydedilmiş durumda zemin kayması (`data/slide5.txt`): hızlanma en kötü 1.5 cm, sprint A/D 2.3 cm, tempo 2.0 cm; ≥ 10 cm yok. Gerçek kare süresi p50 41.6–41.7 ms (kayıt modunda; değişikliklerden önce de aynı). Yeni yoklamaların ayrı maliyeti **ölçülmedi** (fren: hareket varken yalnız yardım adayı olduğu sürece 11 iz + 1 kapsül; farkındalık: hareket ederken 4 küre izi/kare). Standalone, paket ve gamepad **çalıştırılmadı**.

## 10. Videolar

Normal hızda, kesintisiz (30 fps ekran görüntüsü): `videos/p4VID_starts_side2` (ayak tutma kapalı, kaydedilmiş durum), `p4VID_starts_side` (tutma açıkken, karşılaştırma), `p4VID_tempo_front`, `p4VID_ADsprint_side`, `p4VID_trav_h60/h150/h240`, `p4VID_aware_game`, `p4VID_brake_wall`, `p4VID_ceil`. Yalnız traversal kareleri tek tek incelendi; diğer videoları görsel olarak doğrulamadım.

Veri: `data/`; betikler: `scripts/`.
