# SPHIRUS: maske tutuşu, taşıma, işaret, kamera ve ortam düzeltmeleri

Tarih: 2026-11-06. Motor: UE 5.8.4-58902052. Harita: `/Game/GraceRanger/Maps/L_GR_SphirusHouse`. Oyuncu: `BP_HybridA_Player`.

## Sonuç

**Dört maske hatası yeniden üretildi, kök nedenleri bulundu ve düzeltildi.** Yeni oyundan kesintisiz rota, gerçek fareyle çevirme dahil, ışınlama olmadan geçti. Önceki turda takılan `r_pond` ve `r_up` de geçti. Çalışma hatası yok. Kayıt ve menüden yükleme sağlam.

**Bir madde çözülmedi:** `fz_walk_a` tek karelik baş sıçraması. Nedeni kanıtlandı, üç düzeltme denendi, hepsi başka yerde baş hareketini kötüleştirdi, geri alındı.

**Görsel kabul sende.** Sayılar ve kareler iyi, ama oyun hissini ben oynayarak ölçemiyorum. Ortam değişikliği küçük; önceki hedefin tamamı değil.

| Alan | Sonuç | Kısa açıklama |
|---|---|---|
| El tutuşu | PASS teknik, görsel kabul sende | Görünen el hedefe 0.2–1.4 cm yakın. Maske kenarı kavranıyor |
| Maske ölçeği | PASS | 24 × 32 cm → 16.4 × 21.8 cm, tek kanonik boyut |
| Kadraj | PASS teknik, görsel kabul sende | Maske, iki el ve omuz birlikte okunuyor |
| Elde kalan işaret ve etiket | PASS | Tüm durumlarda temizleniyor |
| Taşırken yürüyüş | PASS teknik, görsel kabul sende | Gövde artık dönüyor, alt gövde akıyor |
| Gerçek fare ile çevirme | PASS | Normal OS girdisi, iki yöne |
| Askı sonrası kamera | PASS | Kol 30 cm → 126 cm |
| Engel yakınında kamera | PASS, kısmi kapsam | Yanlış çökme kalktı. Dar açık alan tepesi yeniden koşulmadı |
| Kayıt, yükleme, SF sahipliği | PASS | Dört eski kayıt iki kez, gerçek menü iki kez |
| `fz_walk_a` baş sıçraması | FAIL | 175 m/s², 3.6 cm. Neden bulundu, düzeltme geri alındı |
| Sprint 180 duruşu | NOT_TESTED yeni iş | Bu turda değişmedi, regresyon temiz |
| Ortam | PARTIAL | Zemin tonu, patika kenarı, veranda dibi. Büyük yerleşim yok |
| Pine Forest PCG | PARTIAL | "Sopa" görüntüsünün olası nedeni bulundu. Ana sahneye eklenmedi |
| PBL | PARTIAL | Değer değiştirilmedi, gerekçesi aşağıda |
| True Lens | Kapalı bırakıldı | Hafif profil denendi, fark çok küçük |
| Bellek | PARTIAL | −117 MB. Video bellek uyarısı editörde görülebilir, kalan büyük yük aşağıda |
| Gamepad | NOT_TESTED | Bağlı gamepad yok |
| Gerçek merdiven çıkışı | NOT_TESTED | Senaryo yok |
| Paketlenmiş oyun | NOT_TESTED | Yalnız editör ve `-game` |
| Ses | NOT_TESTED | Dinlemedim |

## Satın alma düzeltmesi

Rehber güncellendi (`claude-unreal-tooling.md`). Eski raporlara dokunulmadı.

| Paket | Kütüphane | Kurulu | Projede etkin | Gerçek kullanım |
|---|---|---|---|---|
| Pine Forest - PCG Biome | Var | Var | `Content/EasyBiomes` | Zemin parçaları, rüzgâr sesi |
| True Lens | Var | Var | `Content/TrueLens` | Yok |
| PBL Database | Var | Var | Evet, eklenti | Referans |
| FF Hazel (Mature) Character Mesh + Texture | Var | Var | `Content/EditableCharacters/HazelM` | Gövde tabanı |
| Underground Tunnel | Var | Yok, önbellekte 388 KB kayıt | Hayır | Yok |
| NWIRO AI Integration Kit / MCP | Var | Motor eklentisi 1.0.15 | Hayır | Yok, aşağıda |

Animated Female Locomotion Set, Grounded Third Person Character ve Realistic Nude Girl satın alınmamış olarak işlendi. Hiçbiri beklenmedi.

## Ana hatalar

| Belirti | Kanıtlanan neden | Yapılan düzeltme | Test yöntemi | Sonuç ve kanıt |
|---|---|---|---|---|
| Elde ve kolda nokta | Widget mesh'in çocuğu, menzili aktörden okuyor. Asınca gizli mesh `hand_r` üzerinde kaldı, canlı halkayı taşıdı. Askıdaki halka da askı aktörünündü | SF'nin kendi `SoftLocked` etiketi, `GR_Sync` her karede yazar. Mesh asınca tezgâha döner | Senin açık PIE oturumunda canlı okundu, sonra tüm durumlar | `01`, `09`, `11`. Halka yok, opaklık 0 |
| Elde "Maskeyi al" | Elde maskenin çarpışması açıktı, oyuncu izi kendi maskesine çarpıyordu | Elde veya bitince aktör çarpışması kapalı | `stat()` her adımda | `02`, `04`. Hedef `None` |
| Yürüyemiyor | Taşıma animasyonu oynarken `IsAnyMontagePlaying` korumaları gövde dönüşünü kilitliyordu. Gövde açısı 22 s boyunca 87.6°. Karakter yan yan gidiyordu | `GR_CarryActive`, taşımada korumaları bırakıyor | Aynı rota, boş el ve taşıma | `03` önce, `12`, `14` sonra |
| Eller garip tutuyor | Üç ayrı neden: görünen el kaynak elden 8 cm ve 25° uzak, parmak katmanı klip kavramasını eziyordu, tutuş 1.0 boyutlu maskeye göreydi | Yeni klipler, geometriye göre parmak kapanışı, ölçüm döngüsü | Dört açı, görünen kemik okuma | `06`, `07` |
| Maske büyük | Gerçekten büyüktü: 24.2 × 32.1 cm, göz delikleri arası 11 cm. Hazel'de göz arası 5.98 cm | Tek ölçek 0.68 | Yüzle aynı düzlem | `08` |
| Kadraj sıkışık | Kamera omuz arkasında, maske çok büyük | Kamera yeri, FOV 42, odak 84, f/4 | Gerçek HUD ile 4 aday | `02` ile `04` |
| Kamera başa yapışıyor | Geniş tahmin küresi yanındaki raf direğine başlangıçta değiyor, mesafe 0 sayılıyor. Yol boşken kol 30 cm'ye iniyordu | Başlangıç teması sayılmıyor | Askı sonrası okuma, duvar noktaları | `16` önce, `15` sonra |

Elle ters tutuş için aradığın olasılıkları tek tek ölçtüm. Sağ-sol karışması, negatif ölçek ve çift IK çıkmadı. Bir yan bulgu: `IKHand` eğrileri AAMS kol IK'sını tetikleyip kolu fırlatıyor, `AT_Contact` eğrileri ise sonradan eziliyor. Bu yüzden kliplere `GR_HoldLeft/Right` eklendi.

## Tutuş

- Sağ el maskenin kenarını kavrıyor, parmaklar arkada. Sol el alttan destekliyor.
- Maske görünen sağ ele bağlı. Sol el klipten geliyor, çalışma anında hedef kovalamıyor. Döngüsel bağ yok.
- Parmaklar maskenin nokta bulutuna değene kadar kapanıyor.
- Görünen el hatası, son ölçüm: inceleme 0.2 cm, askı 0.3–0.4 cm, taşıma 0.7–1.4 cm. Masada sağ el 3.5 cm kısa kalıyor, kol uzanmıyor (`gorunen_el_hatasi.txt`).
- İnceleme dönüşü ±40° ve ±22°. Uçlarda ters bilek görmedim (`05`).
- Başparmak kapanışı hedefe 5–6 cm uzak kaldı. Bu yüzden başparmak yüzeye tam oturmuyor. Sol yüzük ve serçe parmaklar da az kapanıyor. Görsel kabulde bak.
- Kol manşetleri eli yer yer örtüyor. Kıyafet bekletildiği için dokunmadım.

## Maske ölçeği

| Ölçü | Önce | Sonra |
|---|---|---|
| Genişlik × yükseklik | 24.2 × 32.1 cm | 16.4 × 21.8 cm |
| Göz delikleri arası | 11.0 cm | 7.5 cm |
| Karakter göz arası | 5.98 cm | 5.98 cm |

Ölçek haritada tek yerde, masada, elde, taşırken ve askıda aynı. Deformasyon yok, üç eksen eşit. Evdeki diğer maskeler 20–24 cm genişliğinde kaldı. Ev sahnesine dokunmadım, askıda yanındaki maske daha büyük görünüyor.

## İşaret durumları

| Durum | Görünen |
|---|---|
| Masada, yakın | "Yarım Maske / E — Maskeyi al" |
| Elde inceleme | Yalnız "Fare: çevir  E: bırak" (`W_GR_MaskHint`) |
| Taşırken | İşaret yok |
| Askıya yaklaşınca | "Askı / E — Maskeyi as" |
| Asıldıktan sonra | Elde, kolda, askıda işaret yok |

Ekranın ortasındaki küçük nokta oyunun normal nişangâhı, kaldırılmadı. HUD ve SF taraması kapatılmadı.

## Taşırken yürüyüş

Taşıma hızı 80'den 115 cm/s'ye çıktı, normal yürüyüş 132. Üst gövde `UpperBody` katmanında, bacaklar normal hareket hattından geliyor. Sprint engelli: Shift ile 115 kaldı. Zıplama zinciri bozmuyor. Asma, geri koyma ve iptal sonrası hız 132'ye dönüyor, girdi kilidi kalmıyor.

Bir davranış notu: taşırken A ve D yan adım, S geri adım. Gövde kameraya bakıyor. Dururken fareyle dönünce gövde yürümeye başlayınca dönüyor; duruş dönüş animasyonu taşımayı kestiği için kapalı.

Elde maske gövdede sabit, üst gövdenin yürüyüş salınımı bu katmanda yok. Görsel kabulde sertlik hissi verirse sonraki iş budur.

## Kamera

- Asıl hata yanlış çökmeydi. Askı sonrası kol 30 → 126 cm, 30 FPS'te de 126.
- Gerçek duvar önünde kol 64–92 cm, sırt ekranı kaplamıyor (`15`).
- Tezgâh ve askı kameraları sonrası görüş hedefi oyuncu, kontrol ve hareket doğru yöne dönüyor.
- Dar alan için eklediğim yukarı kaydırma etkisiz çıktı, zincirden çıkarıldı.
- Eski raporda geçen tepe rotası koşusu bu turda tekrarlanmadı.

## `fz_walk_a` baş sıçraması

t=27.38'de yeniden üretildi: 175 m/s², 3.64 cm. Göğüs ve omuz sabitken yalnız baş sıçrıyor. Hız sıfırdan geçince bakış noktası tek karede yaklaşık 180° ters tarafa atlıyor.

| Deneme | `fz_walk_a` en kötü | `fz_walk_m` en kötü | Karar |
|---|---|---|---|
| Üretim | 175 | 51 | Korundu |
| Hız sınırlı bakış | 109 | 200 | Geri alındı |
| Ağırlığı arkada söndürme | 130 | 200 | Geri alındı |
| Yalnız ters dönüşte söndürme, 0.2 s | 109 | 200 | Geri alındı |
| Aynısı, 0.45 s | 144 | 200 | Geri alındı |

Son tablo doğrulanmış yedekten geri dönüş sonrası: `w54_rev` 60 FPS yeniden hız 1.10 s, ayak 2.6 cm, geri yürüyüş 0.02 s. `fz_walk_m` 51, sprint 180 57. `w54_rev` satırındaki 172 değeri t=0.02'de 0 cm hareketli başlangıç kaydı.

## Ortam

Evden kıyıya ve arka patikaya çalıştım. Karşılaştırma: `17` önce, `18` sonra, aynı poz. Fark küçük.

| Alan | Değişiklik |
|---|---|
| Yerde kuru yaprak | Turuncu renk serin palete çekildi. `MI_EX_PF_DeadLeaves01/02` |
| Patika | Mevcut çiğnenmiş kanal korundu, kenar düzensizleştirildi, merkez sıkıldı, üstündeki döküntü azaltıldı |
| Patika üstü bitki | Patika merkezinden ve tekrar eden yaprak yamalarından toplam 806 örnek kaldırıldı |
| Veranda dibi | 20 döküntü yığını, zemine geçiş için |
| Taş dizileri | Değişmedi, kural eşleşmedi. Taş sayıları aynı kaldı |

Yeni patika çizmedim. İlk denemem mevcut yolla örtüşmedi, iptal ettim.

**Arazi boyası:** Python'da yol var: `landscape_import_weightmap_from_render_target`. Ama arazi tek katmanlı ve metrede bir örnek. Asıl zemin karışımı `T_EX_RefugeHabitat`, 23 cm çözünürlükte. Onu kullandım.

**Pine Forest:** Paket kötü değil. `SM_PineDry_02` tek ağaç olarak iyi görünüyor (`20`). İlk karelerde aynı ağaç ince siyah çizgi (`21`). Ağaç modeli 444 MB, Nanite verisi sonradan yükleniyor. Önceki "sopa" görüntüsünün en olası nedeni budur, kesin kanıt değil. Sanal doku farkı yalnız iki zemin ve kumaş malzemesinde hata veriyor, ağaçları etkilemiyor. Bellek sınırda olduğu için ana sahneye ağaç eklemedim. Çift orman yok, proje preseti yok.

**PBL:** Referans bulutlu sabah 4952–8772 lux. Sahne fiziksel ölçek yerine göreli değer kullanıyor (güneş 1500, pozlama −0.45). Mutlak değeri yapıştırmak iç-dış dengeyi bozar, değiştirmedim. İç-dış pozlama için kalibrasyon yapılmadı.

**True Lens:** Hafif profil: hafif kenar kararması, ince gren, %5 pus. Kenar bulanıklığı yok (`19`). Fark çok küçük, efekt eklemek yerine kapalı bıraktım.

## Araçlar

Smart App Control hâlâ etkin, Kit `sphirus.uproject` dışında. Editör MCP portu cevap veriyor, ama bu oturumda MCP araçları yüklenmedi. İşler proje koşucusuyla yapıldı. Güvenlik ayarına dokunulmadı.

## Performans

Editör PIE, aynı poz ve sıra, 8 s, tek koşu. Değerler yön gösterir, kesin değildir.

| Nokta | Kare önce | Kare sonra | GPU belleği önce | Sonra |
|---|---|---|---|---|
| Oda | 25.4 ms | 22.8 ms | 6733 MB | 6630 MB |
| Ön patika | 37.3 ms | 35.1 ms | 6682 MB | 6567 MB |
| Kıyı | 36.1 ms | 33.8 ms | 6683 MB | 6566 MB |
| Arka patika | 36.1 ms | 33.7 ms | 6683 MB | 6566 MB |

GPU ve CPU ayrımını ölçemedim. Kare süresi tümü.

İki ayrı uyarı var:

- **Ray tracing geometrisi:** 125 MiB, 400 MiB bütçenin %20'sini aşıyor. Bu bir oran uyarısı, `-game` çalışmasında da var. Çözmedim.
- **Video bellek aşımı:** Editörde 81 MB aşım görüldü. `-game` yükleme görüntüsünde çıkmadı, bu tek görüntü.

| Yük | Boyut | Durum |
|---|---|---|
| `approaching_storm_4k` | 192 MB | Editörün HDRI aracı yüklüyor. Oyun yükü değil. PBL'yi kapatmak fark etmedi, geri açıldı |
| `AAMS2_0_Logo` | 83 MB | Sıkıştırmasız demo logosu. Satıcı dosyası olduğu için dokunmadım, senin kararın |
| Kıyafet dokuları | 9 doku, 118 MB | Akışa açıldı. −117 MB büyük ihtimalle buradan, tek ölçüm |

Aynı Henley dokusunun iki kopyası bellekte. Kıyafet bekletildiği için bıraktım.

## Hazel

Görünen gövde `SKM_MHC_HazelM_BodyMesh`, kaynak gövde görünmez. Yüz `SKM_Hazel_Face_a`, yani GD38 yüzü. Hazel'in kendi yüzü kullanılmıyor. Saç ve kıyafet bekletme kararı korundu. Beyaz saç lekeleri ışıkta hâlâ görünüyor.

## Test sonuçları

| Test | Sonuç | Kanıt |
|---|---|---|
| Yeni oyundan tam rota | PASS | `rota_testi.txt`. Tüm bacaklar `ok True`, `stuck 0` |
| `r_pond`, `r_up` | PASS | Hedefler yürünebilir ızgaranın dışındaydı, test aracı hatası. İçeri alındı, yol sıklaştırıldı |
| Gerçek fare (OS girdisi) | PASS | +33.7° ve −32.1° |
| E ve F girdileri | Action injection | Fare dışındaki tuşlar test komutuyla verildi |
| Hızlı E, duraklatma, F ile çıkış | PASS | `kenar_testleri.txt` |
| Bağlamayı iptal, şerit korunuyor | PASS | Aynı dosya |
| Taşırken zıplama, duraklatma, geri koyma, Shift | PASS | `kenar_testleri.txt`, `ek_testler.txt` |
| Taşırken `load()` | PARTIAL | Maske elde kaldı. Gerçek menüde harita yeniden açılıyor, menüde bu durum denenmedi |
| Dört eski kayıt, iki yükleme | PASS | Tek maske, tek şerit, tek günlük |
| Gerçek menüden yükleme, `-game` | PASS | `22`. Senin kaydının kopyası, iki yükleme. İkinci sonrası görüntü yok, pencereyi yanlışlıkla kapattım |
| 30 FPS taşıma, asma, kamera | PASS | `fps30_testi.txt` |
| 60 FPS regresyon | PASS, `fz_walk_a` hariç | `hareket_60fps_*.txt` |
| Temiz açılış | PASS | Kirli paket yok, geçersiz kalıntı yok |

## Bridge dışa aktarımı

Run `2026-11-06_205901_116556_2b507d`, 18 görünüm, hata 0. Görünüm 03, 11 ve 13 siyah: eski kamera planı artık kaya ve bitkilerin içinde kalıyor. Bu dışa aktarım kusuru, oyun kusuru değil. Plan güncellenmedi.

## Yeni bulgu

`Furniture_R3_MaskWorkbench` çarpışmasız. Karakter masanın içinden geçebiliyor. Duruş noktası masa kenarının içine düştüğü için çarpışma eklemek tutuşu bozar. Bu turda düzeltmedim.

## Değişen dosyalar

- Oyun: `BP_GR_Player`, `ABP_GR_MetaHuman`, `BP_GR_MaskBench`, `BP_GR_MaskHook`.
- Klipler: `A_GR_Mask_*`, `AM_GR_Mask_*` (Take, Put, Inspect, Carry, Hang).
- Yeni: `/Game/GraceRanger/SF/MaskJob/UI/W_GR_MaskHint`.
- Harita: mask ölçeği, bitmiş maske konumu, iki kamera, bitki ve veranda.
- Ortam: `T_EX_RefugeHabitat`, `MI_EX_PF_DeadLeaves01/02`.
- Dokular: 9 `T_LK_*` akışa açıldı.
- Belge: `claude-unreal-tooling.md`.
- Araçlar: `Tools/Grip_20261106/`, `Tools/Embodied_20261105/grip_*.py`.

`ABP_GR_MotionMatchingBase` son durumda değişmedi.

## Geri alma

Yedekler `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/` altında.

| Ne | Yedek |
|---|---|
| Oyuncu, görünen ABP, tezgâh | `emb_gcore_170227`, `emb_gcore2_170631` |
| Kamera | `emb_gcam_175426` |
| Klipler | `emb_gen_*`, ilk tur |
| Harita, ölçek öncesi | `grip_map_m1_173616` |
| Harita, ortam öncesi | `grip_map_e1_185037` |
| Zemin ve yaprak | `grip_hab_184919` |
| Dokular | `grip_stream_190953` |

## Sonraki iş

1. Oyunda tutuşa ve taşıma hissine bak.
2. `AAMS2_0_Logo` kararı: küçültülsün mü?
3. Baş sıçraması için ayrı çalışma.
4. Ortam için büyük yerleşim turu.
