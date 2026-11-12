# Sphirus: kamera görevinden kalanlar (2026-11-12/13)

Senin listen: atmosfer ve masalsı kimlik + kamera önünden geçen yapraklar; çay ve şömine kadrajı; kapı ve dolapta ele uzanma; konfor ayarları menüsü; sınanmamışlar (merdiven, gamepad, 60/120 kare/sn, kayıt/yükleme, duraklatma, 21:9); boyun/omuz duruşu. Boyun/omuz duruşu hareket görevinde ele alındı (`chatgpt-bridge/reports/sphirus-hareket-durus-gait-2026-11-12`, §4). Bu rapor geri kalanları kapsar. **Kullanıcı kabulü yok**; teknik sonuç, görsel incelemem ve kabul ayrı yazıldı.

Kayıt güvenliği: her test senin kaydını (`SFSaveSlot.sav`, SHA1 `66556281…`) kenara alıp bayt bayt geri koydu; konfor testi kendi oluşturduğu `SphComfort.sav` dosyasını test klasörüne taşıdı (senin oyununa test ayarı taşınmadı). Varlık değişiklikleri kapılı çalıştırıcıdan (manifest yedeği + tek kilit) geçti; satıcı dosyalarına dokunulmadı.

## 1. Özet

| Madde | Önce | Sonra | Teknik | Görsel incelemem | Kullanıcı kabulü |
|---|---|---|---|---|---|
| Çay ve şömine kadrajı | NOT_TESTED: istasyonlar testte hiç başlamıyordu | ikisi de çalışıyor ve kadrajlandı; çayda içme anı artık yandan (yüz profilde, fincan ağızda) | TECH_TESTED: PASS | şömine: kütük, el ve yanan ateş görünür; çay dökme: eller gövdenin arkasında (PARTIAL) | yok |
| Kapı ve dolapta ele uzanma | "uzanma animasyonu yok" | dolapta zaten bir uzanma klibi var (`AM_GR_Day_Reach`); ev kapılarına prosedürel uzanma eklendi | TECH_TESTED: el kulpa ~130 → 17–27 cm | sol kol kanada açılıp dönüyor; el kavramıyor, kulpa ~20 cm kalıyor (PARTIAL) | yok |
| Konfor ayarları menüsü | yalnız kamera bileşeni değişkenleri | F10 (gamepad View) paneli: hareketi azalt, sol omuz, görüş alanı −8..+12°, kamera sarsıntısı, hızda görüş açılması, alan derinliği, rezonans etkisi; panel açıkken oyun durur; ayarlar ayrı kayda (SphComfort) yazılır, açılışta geri yüklenir | TECH_TESTED: aç/kapa, duraklatma, imleç, kayıt, yeniden açılışta yükleme PASS | panel okunuyor (evidence/konfor_paneli.png); fareyle sürükleme NOT_TESTED | yok |
| Kameranın önünden geçen yapraklar | yol kenarı yaprakları lensi dolduruyordu | yol kenarındaki 12 yaprak malzemesi kameraya 60 cm'de tamamen, 120 cm'ye kadar kısmen titreşimli soluyor | IMPLEMENTED; maliyet GPU +0,7 ms (28,1 → 28,8) | yolda görsel regresyon yok; yaprağın lensten geçtiği an saniyede bir karelerde yakalanmadı (PARTIAL) | yok |
| Dar alanda kamera saça giriyordu (yeni bulunan) | kol 51–60 cm'ye kısalınca baş ekranın altından çıkıyordu (y 1,07) | baş 0,72'de | TECH_TESTED: PASS | — | yok |
| Merdiven | NOT_TESTED | tırmanırken baş kadraj içinde (y 0,07 → 0,22 tempoluda), kamera sarsıntısı 13,5 → 2,9 | TECH_TESTED: PASS | — | yok |
| Gamepad | NOT_TESTED | düğmeler: L3 tempolu, sol omuz koşu modu, A zıplama — çalışıyor; analog çubuk enjekte edilemediği için hareket klavyeyle | PARTIAL | — | yok |
| 60/120 kare/sn | NOT_TESTED | 30/60/120 Hz sabit adımda kadraj ve hızlar aynı (baş ±0,02, omuz–kamera ±5 cm); zıplama tepesi 53–60 cm (adım boyu farkı). Bu donanımda gerçek 60 kare/sn yok (GPU sınırlı, ~33 kare/sn) | TECH_TESTED (adımdan bağımsızlık); PERFORMANCE: 60 kare/sn ulaşılamıyor | — | yok |
| Kayıt / yükleme | NOT_TESTED | hareket görevinde: kayıt, oturum içi yükleme ve açılışta yükleme sonrası gait merdiveni aynı | TECH_TESTED: PASS | — | yok |
| Duraklatma | NOT_TESTED | P oyunu durduruyor (konum ve kamera donuyor); ikinci P menüyü kapatmıyor (menü odaklı), Escape iki yönde çalışıyor; devamda kamera ve hareket kopmadan sürüyor | PARTIAL (P ile devam: Story Framework duraklatma menüsü davranışı) | — | yok |
| 21:9 ekran | NOT_TESTED | yapılmadı: düzenleyici içi oyun penceresinin oranı değiştirilemiyor; bağımsız oyun süreci kullanıcı kaydını açacağı için denenmedi | NOT_TESTED | — | — |
| Atmosfer ve masalsı kimlik | yapılmadı | bu turda da dünyaya kalıcı değişiklik yapılmadı (bkz. §8) | NOT_TESTED | — | — |

## 2. Çay ve şömine

Kök neden benim test aracımdaydı: kamera görevindeki senaryo, hub durumunu yazmadan önce tanımsız bir `hub()` yardımcısını çağırıyordu; Python hata verip istasyon koşulunu hiç kurmuyordu. Ayrıca hub değişkenleri Python'dan doğrudan yazılamıyor (örnek üzerinde düzenlenemez). Düzeltme: hub'ın kendi kayıt-yükleme olayı `LoadFromDataString` doğru kodla çağrılıyor (şömine: 2 yarılmış odun; çay: ateş yanık + 1 bitki). İstasyon koşulları (Story Framework değil, hub sayaçları): şömine `Fire 0 ve Split ≥ 2`, çay `Tea 0, Herb ≥ 1, Fire 2`. Not: odun kesme artık `Split`'i doğrudan artırmıyor, düşen parçaları toplamak gerekiyor.

| | Şömine | Çay (önce, arkadan) | Çay (sonra, yandan) |
|---|---|---|---|
| İstasyon çalıştı | evet (diz çökme, kütük yerleştirme, yakma) | evet (dökme, içme) | evet |
| Sağ el görünür | %92 | dökme %17, içme %25 | dökme %15, içme %22 |
| Hedef görünür | %67 | %100 | dökme %81, içme %7 (kamera yanda, ocak arkada) |
| İçme anı | — | arkadan kalkan kol | yüz profilden, fincan ağızda |

Çay iş kadrajı (bağlam türü 5) arka 55 / yan 66 → arka 1 / yan 100 olarak kalıcı yapıldı. Dökme anı hâlâ ellerin arkasından görünüyor (PARTIAL); iki an için ayrı kadraj istersen istasyonun aşama bilgisi kameraya iletilmeli.

## 3. Kapı ve dolap

- Dolap (`GR_Day_WardDoor`, tür 7) zaten bir uzanma klibi oynatıyor (`AM_GR_Day_Reach`, temas 0,9 sn) — kamera raporundaki "uzanma yok" ifadesi dolap için yanlıştı.
- Ev kapıları Story Framework `GenericDoor_BP` (satıcı); E ile kapı kendi kendine dönüyor, oyuncuya hiçbir şey oynatılmıyor. Satıcı sınıfına dokunmadan: hareket bileşeni, etkileşim yöneticisinin hedefi bir kapıysa ve kapı dönmeye başladıysa kanadın sınırlarından kulp noktasını hesaplıyor ve 1 sn'lik bir uzanma zarfı başlatıyor; görünen bedende iki-kemik IK eli o noktaya götürüyor (kulp sağdaysa sağ el). Ölçüm (`data/kapi_uzanma.txt`): el–kulp ~130 → 17–27 cm; zarf 0,28 sn'de dolar, 0,6 sn'ye kadar tutar, 1 sn'de biter.
- Sınır: oyuncu E'ye kapıdan genellikle ~2 m uzakta basıyor (Story Framework etkileşim menzili); uzanma yalnız ~1,2 m içinde etkili ve el kulpu kavramıyor. Tam bir "kapıyı tutup açma" için karakterin kapıya bir adım yaklaşması (istasyonlardaki gibi) ya da kapı klibi gerekir — PARTIAL.

## 4. Konfor ayarları

F10 (gamepad View) → `WBP_Sph_Comfort`. Ayarlar doğrudan tek kamera sahibine (`AC_Sph_Camera`) yazılır ve canlı görünür; kapatınca `SphComfort` kaydına (oyun ilerleme kaydından ayrı) yazılır, oyun açılışında geri yüklenir. Satıcı duraklatma/ayar menüsüne dokunulmadı. Sınanmadı: gamepad ile panel içinde gezinme, fareyle kaydırıcı sürükleme (otomatik testte fare imleci yok).

## 5. Kameranın önünden geçen yapraklar

Yol kenarındaki eğrelti, genç çam, çam dalı ve çalı malzemeleri satıcı `PineForestPack` ana malzemesine bağlıydı ve projeye ait bir bitki ana malzemesi yoktu. Ana malzemenin proje kopyası (`M_EX_WindFoliage_NearFade`) opaklık maskesini kameraya uzaklıkla çarpıyor: 60 cm içinde tamamen gizli, 120 cm'ye kadar titreşimli (`DitherTemporalAA`) solma. Gölge geçişinde derinlik ışıktan ölçüldüğü için gölgeler bozulmuyor. Yeniden bağlanan: 8 proje-sahipli yaprak örneği + 4 çalı/fidan ton örneği (satıcı yaprak örneklerinin proje kopyaları üzerinden). Satıcı dosyaları değişmedi (satıcı ana malzeme 124 ifade, aynı).

Maliyet (patika, aynı rota, `data/yaprak_solma_maliyet.txt`): GPU ortanca 28,1 → 28,8 ms, ortalama 33,4 → 33,7 kare/sn. Görsel: patika ve bahçe karelerinde bitkiler ve gölgeleri aynı; yaprağın lensten geçtiği an saniyede bir karelerde yakalanmadı → PARTIAL (videoda kontrol edilmeli). Diğer satıcı örnekleri (uzak taç, yosun, çim, satıcı `MI_PineTree04_FO`) bu turda dışarıda.

## 6. Dar alan ve merdiven (kamera)

- Dar köşe: karakter kameraya doğru geri yürüyüp köşeye girince kamera kolu 51–60 cm'ye kısalıyor, "arkada engel → kamerayı yükselt" terimi (22 cm) kamerayı başın 34 cm üstüne taşıyor ve baş ekranın altından çıkıyordu (y 1,07). Terim artık kol kısaldıkça sönüyor (×SafeFrac³) ve varsayılanı 10 cm: baş 0,72'de. Koridor kadrajı aynı (0,35;0,33).
- Merdiven: pivot yükseklik süzgeci sürekli eğimde ~18 cm geride kalıyordu. Süzgeç (basamak sıçramalarını gizlemek için) kaldı, hedefine düzgünleştirilmiş dikey hızla 0,2 sn ileri besleme eklendi. Tırmanırken baş 0,24 → 0,32, tempolu tırmanışta 0,07 → 0,22; kameranın kapsüle göre sarsıntısı 13,5 → 2,9. Yokuş patikada da baş daha kararlı (sarsıntı 1,08 → 0,55).

## 7. Sınanmamışlar

- **Gamepad:** L3 tempolu, sol omuz koşu modu, A zıplama — çalışıyor (`gamepad_dugmeleri`). Analog çubuk komutla enjekte edilemiyor: çubukla hareket ve gamepad ile menü gezinmesi NOT_TESTED.
- **60/120 kare/sn:** 30/60/120 Hz sabit adımda aynı rota (`data/kare_hizi_30_60_120.txt`): baş konumu ±0,02, omuz–kamera ±5 cm, hızlar aynı; zıplama tepesi 53–60 cm (karakter fiziğinin adım boyu farkı). Bu donanımda gerçek oyunda 60 kare/sn'ye ulaşılmıyor (GPU sınırlı, ~33 kare/sn).
- **Kayıt/yükleme:** hareket raporunda PASS (kayıt, oturum içi yükleme, açılışta yükleme sonrası gait merdiveni). Konfor ayarları ayrı kayıtta, açılışta yükleme PASS.
- **Duraklatma:** P oyunu durduruyor, konum ve kamera donuyor; ikinci P menüyü kapatmıyor (Story Framework duraklatma menüsü odakta), Escape açıp kapatıyor; devamda kamera ve hareket kopmadan sürüyor. P ile devam istenirse menüye bağlanmalı (satıcı menüsü, bu turda değiştirilmedi).
- **21:9:** NOT_TESTED. Düzenleyici içindeki oyun penceresinin oranını değiştiremiyorum; bağımsız oyun süreci senin kaydını açacağı için denemedim.

## 8. Atmosfer ve masalsı kimlik

Dünyaya kalıcı bir değişiklik yapmadım. Işık/sis/renk tabanı 1 Kasım'da senin onayınla üretime alınan XR5 "gümüş nem" bakışı. "Masalsı" bir katman (ör. ışık huzmesi ve havada toz, yerel sis, pencere sıcaklığı, nemli malzeme parlaklığı) bir beğeni kararı ve AGENTS.md'ye göre eşli öncesi/sonrası görünümler, 24 istasyonda pozlama istatistiği, Bridge dışa aktarımı ve `LATEST.json` doğrulaması gerektiriyor. Bunu ayrı bir aday çalışma olarak öneriyorum; seçeceğin yönü görmeden üretime almam.

## 9. Değişiklik listesi ve geri alma

`changes/changes.md`. Her yazma işinin manifest yedeği `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/day_mot_*` altında. Temiz açılış (`data/temiz_acilis_denetimi.txt`): 9 Blueprint güncel ve hatasız, yeni malzemeler doğru zincirde, kirli paket yok, senin kaydın aynı.

## 10. Videolar (gerçek hız, 30 kare/sn)

`sonra_somine_ates_yakma`, `once_cay_arkadan` / `sonra_cay_yandan`, `sonra_kapi_uzanma_oyun_kamerasi`, `sonra_kapi_uzanma_on_aci`, `once_dar_kose_bas_kadraj_disi` / `sonra_dar_kose`, `once_merdiven` / `sonra_merdiven`, `once_patika_yaprak` / `sonra_patika_yaprak_solma`, `sonra_bahce_yaprak_solma`, `gamepad_dugmeleri`.

## 11. Açık kalanlar

- Çay dökme anında eller arkada; kapı uzanması kulpu kavramıyor ve uzaktan basışta etkisiz; yaprak solmasının lens anı videoda doğrulanmalı.
- Konfor paneli sade (varsayılan görünüm); gamepad gezinmesi ve fareyle kullanım sınanmadı.
- 21:9 ve gerçek 60 kare/sn sınanmadı; P ile devam satıcı menüsünde.
- Atmosfer/masalsı kimlik yapılmadı (§8).
- Kullanıcı kabulü yok.
