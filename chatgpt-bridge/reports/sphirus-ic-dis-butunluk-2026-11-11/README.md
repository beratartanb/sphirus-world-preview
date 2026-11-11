# Sphirus — ev içi, ışık ve iç–dış bütünlük turu (2026-11-11, 22:30–23:55)

Harita: `/Game/GraceRanger/Maps/L_GR_SphirusHouse` + alt harita `L_GR_CurrentHouseContent` · UE 5.8.4 · editör PIE, 1600×900.
Durum etiketleri: **PASS**, **PARTIAL**, **NOT_TESTED**, **YAPILMADI**, **ENGEL**.

**Özet dürüstçe:** bu turda ortak ışık düzeni, gölet yüzeyi, zemin–maske–bitki rota uyumu ve iç–dış zincir testi tamamlandı. **Ev içi yerleşimi yeniden tasarlanmadı**: iç mekân önceki turlarda zaten yoğun döşenmişti, inceleme asıl sorunun ışık/renk olduğunu gösterdi; yerleşim tarafında tek kalıcı ekleme veranda kapısının yanındaki maskedir. Brifin 4. maddesi (her işlev alanında somut yerleşim değişikliği) **karşılanmadı**.

## 1. Eve giriş ve gerçek oda düzeni

Gerçek karakter verandadan ön kapıya ve arka bahçeden arka kapıya yürütüldü: ikisi de geçiliyor, takılma yok (`IN_front_door`, `IN_rear_door` kayıtları). Erişim engeli yok. PASS.

| Alan | Gerçekten var mı | Bulunanlar (editörden okundu) |
|---|---|---|
| Oturma / şömine (zemin, GD) | Var | Taş şömine, kanepe, iki koltuk, sehpa, kitaplık, şömine yanında odunluk standı |
| Mutfak / çay (zemin, KD) | Var | Döküm ocak, çaydanlık istasyonu, tezgâhlar, yemek masası, kiler rafı (110 parça) |
| Maske atölyesi (zemin, KB) | Var | Pencere boyu tezgâh, maske çalışma tezgâhı (görev), pigment çekmecesi, alet rafı, batı duvarında 4 maske, askı |
| Hol / giriş | Var | Arka kapı yanında portmanto, konsol, hol halısı |
| Kiler + alt tuvalet (zemin, B) | Var | Raflar, kasalar, kova |
| Merdiven | Var | Batı duvarı |
| Yatak / giyinme (üst) | Var | Yatak (uyanma başlangıcı), gardırop (giyinme istasyonu), komodin |
| Okuma / dikiş köşesi (üst) | Var | Koltuk, kitaplık, dikiş makinesi |
| Banyo + çamaşır (üst) | Var | Emaye küvet, lavabo, çamaşır makinesi |
| Balkon (üst, batı) | Var | Bank, masa, saksılar |
| Çatı arası | Var (merdivenle) | Aile sandıkları, raf — **bu turda içine girilip görüntülenmedi** |

Başlangıç görüntüleri: `evidence/ic_baslangic_a.jpg`, `ic_baslangic_b.jpg` (18 nokta). Zemin kat planı: `evidence/zemin_kat_plani.png`.

Başlangıç bulguları:
- Bütün iç mekânda yoğun turuncu-sarı renk; gündüz olmasına rağmen görüntüyü lambalar taşıyor.
- Üst kat sahanlığı ve banyo önü okunmayacak kadar karanlık.
- Dar yerlerde oyun kamerası karakterin kafasına sıkışıyor (yürüyüş kaydında kamera kolu en az 45 cm). Kamera tasarımı bu turun kapsamında değil; **düzeltilmedi**.
- Yerleşim ve eşya yoğunluğu çoğu odada yeterli; atölye tezgâhında iş aşamaları okunmuyor (küçük kavanozlar, dağınık).

## 2. Sanat yönetimi kararı (uygulanan hâli)

Hedef: nemli konifer ormanında, maske üreten birinin bakımlı ama yaşanmış sığınağı; dışarıda giderek belirsizleşen çevre.
- **Işık mantığı:** gündüz, yağmur sonrası yumuşak güneş. Pencereli odalarda gün ışığı önde, lambalar yalnız vurgu; penceresiz geçişlerde (hol, merdiven, kiler, banyo) sıcak lamba. Sıcaklık artık "her yer turuncu" değil, "serin gün ışığı içinde sıcak cepler".
- **Dışarısı:** aynı güneş, daha az turuncu pus; orman derinliği serin, ev cephesi patlamıyor.
- **Su:** siyah düz yüzey yerine ormanı ve gökyüzünü yansıtan sakin gölet.
- **Zanaatın dışarıdaki ilk izi:** ön kapının yanında bir maske (atölye duvarındakilerle aynı biçim ailesi).

## 3. Işık ve atmosfer — karşılaştırmayla seçildi

Oyunda görüntüyü neyin belirlediği önce ölçüldü: sahne güneşi, gökyüzü, üç bölgesel pozlama hacmi ve lambalar. İnceleme ışıkları kapalı (görünmez), ağır renk filtresi yok; oyuncu kamerasında yalnız gren, hafif vinyet ve kenar yumuşatma var.

Beş düzen aynı 13 kamerada (7 iç, 6 dış) çekildi:

| Düzen | Güneş | Gökyüzü | Lambalar | Sonuç |
|---|---|---|---|---|
| L0 (önceki) | 1450, 4700 K, huzme 1,5 | 0,8 | 3800 K, tam | İçeride ve verandada turuncu pus |
| L1 | 1250, 5600 K, huzme 1,0 | 1,15 | ×0,55, 3000 K | Dışarısı belirgin iyi; içerisi hâlâ turuncu (lamba daha da sıcak) |
| L2 | 750, 6200 K, huzme 0,6 | 1,6 | L1 gibi | Fazla düz ve mavi; güneş hissi kayboluyor |
| **L3 (seçilen)** | L1 gibi | 1,3 | Pencereli odalar ×0,25 / 3500 K; geçişler ×0,6 / 3200 K | İçeride gün ışığı önde, renk doğal; sahanlık açıldı |
| L4 | L1 gibi | 1,3 | Pencereli odalar ×0,5 | L3'e yakın, biraz daha sarı |

Ev bölgesi pozlama hacmi: orta ton sıcak kayması kaldırıldı (1,03/1/0,96 → nötr), pozlama −0,55 → −0,30.
Kanıt: `isik_karsilastirma_dis_L0_L1_L2.jpg`, `isik_karsilastirma_ic_L0_L1_L2.jpg`, `isik_karsilastirma_L0_L3_L4.jpg`; son durum çiftleri `atmosfer_once_sonra_a/b.jpg`, `ic_once_sonra_a/b.jpg`.

Durum: PASS (karşılaştırma + kayıt + yeniden açılışta değerler okundu). Görsel değerlendirmem: dışarıda fark belirgin, içeride **orta düzeyde** — iç mekân hâlâ sıcak tonlu; duvar ve ahşap malzemelerin kendi rengi sarıya yakın. Malzeme tarafına dokunulmadı.

Bilinmesi gereken: ilk kayıtta lamba değerleri alt haritaya yazılmamıştı (bileşen ayarı paketi kirli işaretlemedi); yeniden açılışta fark edildi, düzeltilip tekrar kaydedildi ve okundu (mutfak sarkıtı 1100 → 275 lm, 3500 K).

## 4. Gölet yüzeyi

Proje-sahipli `MI_EX_Pond` üzerinde üç ayar dört kamerada karşılaştırıldı (`su_karsilastirma_W0_W1_W2.jpg`):

| | Specular | Roughness | Murkiness | Kenar mesafesi | Sonuç |
|---|---|---|---|---|---|
| W0 (önceki) | 0,06 | 0,70 | 7,0 | 145 | Siyah, düz; yansıma yok |
| **W1 (seçilen)** | 0,22 | 0,32 | 4,5 | 230 | Orman ve gökyüzü yansıyor, hâlâ koyu ve sakin |
| W2 | 0,35 | 0,18 | 3,5 | 300 | Ayna gibi; fazla parlak |

Durum: PASS (görüntü). Kıyı profili (sığlık, kumsal) bu turda **değişmedi**.

## 5. Zemin: maske, bitki ve kullanım hattı tek güzergâh

Önceki turun bilinen uyuşmazlığı çözüldü: bitki tasarımı artık zemin maskesinin patika kanalını doğrudan okuyor; maskede iz olan yerde (doğu duvarı hattı dahil) bitki yok, izin yumuşak kenarında yalnız alçak türler var (729 aday nokta bu kuralla boş bırakıldı). Tasarım `g7`, 16.850 zemin örneği.
Durum: PASS (kural ve sayım); doğu duvarı hattına ayrıca yakın çekimle **bakılmadı**.

## 6. Taş yayı

Yayın iç zemini bitkisiz bırakıldı, A rotasından yayın açık tarafına bir yaklaşma izi eklendi, taşların arkasında bitki toplanması artırıldı. Durum: PARTIAL — yalnız bitki dışlaması ve iz; **zemin biçimi, görüş çerçevesi ve yaklaşma kompozisyonu tasarlanmadı**, son durumdan yakın görüntü alınmadı.

## 7. Ev içi yerleşim

- Atölye tezgâhına üç aşamalı maske dizisi denendi (ham → oyulmuş → kemik). Projede kullanılmayan Chapter01 maske ağları tezgâh mesafesinde düz oval disk gibi okundu; **geri alındı**. Somut eksik: iş aşamasını gösterecek kalitede yarım maske ağı yok (`SM_C01EQ_*` 38–716 üçgen).
- Kalıcı ekleme: `INT_MaskVerandaPeg` — ön kapının yanında askıda bir maske.
- Mobilya, dolaşım, depolama, mutfak, şömine, yatak odası düzenine **dokunulmadı**.

Durum: YAPILMADI (büyük ölçüde). Bu, brifin açık bıraktığım ana maddesi.

## 8. Ses — ENGEL

Editör oturumu `-nosound` ile başlatılmış (`LogAudio: Audio Device Manager not initializing due to all audio being disabled`). Oyun içinde 17 ortam sesinin hepsi "çalmıyor" okunuyor; bu oturumda hiçbir ses duyulamaz, ben de dinleyemem. Gereken adım: editörü `-nosound` olmadan açıp kulakla dinlemek.

Yapılabilen: her kaynağın yedi dinleme noktasındaki hesaplanmış seviyesi çıkarıldı. Buradan bir kusur bulundu ve düzeltildi: şömine çıtırtısı ve bahçe rüzgârında mesafe azalması yoktu (80 m ötedeki açıklıkta bile 0,7 ve 0,5 seviyesinde). Şömine: iç 160 cm, düşüş 950 cm; bahçe rüzgârı: iç 450 cm, düşüş 1900 cm. Kıyı sesleri yalnız kıyıda (0,27–0,35), gıcırtı yalnız dar geçitte (0,27), kuşlar ev ve kıyıda düşük (0,09–0,19) hesaplanıyor. Bunlar hesap, işitsel doğrulama değil.

## 9. Final zincir testi (son mekânsal değişikliklerden sonra)

Tek kesintisiz yürüyüş, gerçek karakter: oturma odası → atölye kenarı → hol → ön kapı → veranda → bahçe basamağı → düz taşlar → iskele → kıyı → evin güneydoğusu → yokuş rotası → kapı noktası → arka çalışma alanı (odunluk, kesme kütüğü) → arka kapı → hol → oturma odası.

| Koşu | Sonuç | Süre | Takılma | Hız | Ort. kare | p95 |
|---|---|---|---|---|---|---|
| Zemin katmanı gizli | hedefe ulaştı | 85,0 sn | 0 | 159 cm/sn | 34,6 ms | 53,0 ms |
| Zemin katmanı açık | hedefe ulaştı | 84,9 sn | 0 | 158 cm/sn | 33,3 ms | 47,3 ms |

Zemin katmanının maliyeti bu zincirde ölçüm gürültüsünün içinde kaldı (açıkken daha hızlı çıktı). Kareler: `evidence/zincir_yuruyus.jpg` (4 sn aralıkla 21 kare; kesintisiz video değil). Yürüyüş, lamba değerlerinin ikinci kaydından önce yapıldı; aradaki fark yalnız lamba parlaklığı.

Etkileşimler (kapı açma/kapama, maske tezgâhı, çay, şömine, gardırop, yatak): **NOT_TESTED**. Kapılar açık durumda geçildi; E ile etkileşim akışı koşulmadı.
Doku akışı, bellek, bitki kaybolması ve rüzgâr fazı: **NOT_TESTED**.

## 10. Kayıt ve geri dönüş

- Kayıt: gated runner, manifest `int_all`, `int_all3` (62 varlık + iki harita). Yeniden açılışta kirli paket yok; güneş 1250/5600 K, gökyüzü 1,3, su W1, lamba değerleri okundu.
- Başlangıç noktası (sha1 doğrulamalı): `C:\Users\berat\SphirusCheckpoints\Interior_20261111_Start`.
- Işık ve su özgün değerleri: `Saved/Codex/Interior_20261111/light_orig.json`, `water_orig.json` (`light_set.py` L0, `water_set.py` W0 ile geri yazılır).
- Araçlar: `Tools/Interior_20261111/`.

## 11. Açık kalanlar

1. Ev içi işlev alanlarının yerleşim tasarımı (atölye iş akışı, mutfak, şömine, yatak/giyinme, giriş eşikleri).
2. İç mekân malzemelerinin sarıya yakın tonu; çatı arası incelemesi.
3. Taş yayı keşif kompozisyonu; kıyı profili.
4. Ses dinleme (editör sessiz açılmış), etkileşim akışı, kesintisiz video.
5. Dar iç mekânda kamera sıkışması.
6. Bu turun Bridge dışa aktarımı ve GitHub yayını yapılmadı.

## 12. Yaşanmışlık katmanı — ev içi ve ev çevresi (12 Kasım, 00:00–01:00)

Kullanıcı isteği: yüksek detay, evin sağında solunda ve içinde dağınık eşya, yaşanmış ve dolu his. Yalnız projede zaten bulunan eşyalar kullanıldı (Fishermans Cabin ve Modular Rural Cabins küçük eşyaları; 404 aday ölçüldü, 93'ünün görünüşü küçük resimle doğrulandı). Radyo, plastik kasa, sprey, lastik, soba borusu gibi modern görünenler bilinçli olarak dışarıda bırakıldı.

**185 eşya** kaydedildi (yeniden açılışta sayıldı), her küme bir gündelik işe bağlı:

| Bölge | Adet | Ne anlatıyor |
|---|---|---|
| Atölye | 39 | Pencere tezgâhının iki ucunda çalışılan yüzey: tepsi, ahşap parçaları, bez, kalem, defter, teneke kutular, mum, kupa; tezgâh altında kasalar, yerde talaş/kırpıntı, kova. Görev tezgâhının yalnız ön kenarına üç küçük şey |
| Mutfak | 33 | Masada kesme tahtası, meyve, kupa, bez, kitap; tezgâhlarda tencere, tava, baharat kavanozları, kase, çatal-kaşık; yerde meyve kasası |
| Oturma / şömine | 20 | Şömine önünde kütükler ve çıra, köşede kül kovası ve bez; sehpada kitaplar, mum, kibrit; koltuk yanında yere bırakılmış kitap yığını ve kupa |
| Hol / ön giriş | 6 | Konsolda mum ve kutu; ön kapı içinde paspas, çıra kasası, sulama kabı |
| Yatak odası | 15 | Komodinde mum, kitaplar, kutu; yatağın yanında kitap yığını; yerde bırakılmış bez; pencere sekisinde örtü |
| Okuma köşesi | 5 | Sehpada kupa, kitap, mum |
| Balkon | 8 | Masada kitap, mum, kase, mala; saksılar ve sulama kabı |
| Veranda | 27 | Kapının yanında duvara dayalı iki kürek, kova, çıra kasası, paspas; batı ucunda büyük kasa, saksılar, fıçı, süpürge, duvarda asılı ip; doğu ucunda odun istifinin yanında kütükler, balta, yonga |
| Doğu duvarı (dış) | 16 | Odun tarafı: iki odun istifi, palet üstünde kasa, kalas yığını, kova, balta, dağılmış yarma odun. Duvara yaslı; x>1620'deki patika izi açık |
| Batı duvarı (dış) | 9 | Bakımsız taraf: kırık palet, kontrplak, kalas, yağmur fıçısı, devrik kasa, ahşap çerçeve, sac |
| Arka kapı (dış) | 7 | Mutfak odunu istifi, duvar dibinde kürek ve tırmık, kasa, kütük ve yongalar |

Kanıt: `evidence/yasanmislik_ic.jpg`, `yasanmislik_dis.jpg`, `yasanmislik_yakin.jpg` (21 oyun içi yakın görüntü).

Görsel değerlendirmem: dış kümeler (doğu odun istifi, batı paleti, arka istif, veranda batı ucu) güçlü ve doğal okunuyor. İç kümeler yerinde ama küçük eşyalar oyun kamerası mesafesinde ince kalıyor; atölye tezgâhının doğu ucu ve veranda doğu ucu görüntülerde net seçilmiyor. Tek tek eşyaların yüzeye oturuşunu (havada kalma, iç içe geçme) hepsi için kontrol etmedim: PARTIAL.

**Yakalanan hata:** arka kapının iç tarafına koyduğum paspas, kasa, kütük ve balta çarpışmasız olmalarına rağmen kapının açılmasını engelledi; zincir yürüyüşü eşikte (x=802, y=18) takıldı. Dördü kaldırıldı, o bölge boş bırakıldı ve betiğe not düşüldü. Ön kapıdaki benzer eşyalarla geçiş sorunsuz.

Zincir yürüyüşü (son kayıtlı düzenle, `CHAIN_lived2`): hedefe ulaştı, 84,7 sn, takılma 0, hız 160 cm/sn. Kareler: `evidence/zincir_yuruyus_son.jpg`. Ortalama kare süresi 38,4 ms (önceki zincirde 33–35 ms); bu farkın eşyalardan mı yoksa uzayan editör oturumundan mı geldiği **ayrıştırılmadı** (eşyalar için aynı anda gizle/göster ölçümü yapılmadı).

Hâlâ eksik: "kapı ve kiriş" düzeyinde mimari detay (kirişe asılı eşya, kapı çevresi aşınması, çivi/askı) yalnız veranda duvarındaki ip ve maske ile sınırlı; mobilya yerleşimi değişmedi; etkileşim akışı ve ses yine test edilmedi.

Kayıt: manifest `int_liv`, iki harita + 62 varlık; yeniden açılışta kirli paket yok. Tümünü geri almak: `LIV_*` etiketli aktörleri silmek (klasör `LIVED/20261112`). Betik: `Tools/Interior_20261111/dress_lived.py`.

## 13. Blender ile üretilen eksik eşyalar ve uyumsuz eşyaların ayıklanması (12 Kasım, 00:05–00:45)

**Üretim:** `Tools/Interior_20261111/gen_handmade.py` (Blender 5.2, komut satırı, tamamen betikle). Kaynak FBX'ler ve önizlemeler `SourceAssets/Handmade_20261112/` altında (Content dışında). İçe aktarma eski FBX fabrikasıyla, yalnız yeni paketlere: `/Game/Sphirus/Props/Handmade20261112/` (12 mesh + bir köşe-rengi materyali). Yüzeyler evin mevcut malzeme örneklerine bağlandı (el yontması meşe, dövme demir, keten, kırmızı kil, maske ahşabı); yeni doku üretilmedi.

| Model | Üçgen | Boyut (cm) | Nerede |
|---|---|---|---|
| Maske aşama 1 — ham blok | 468 | 30×9×38 | Pencere tezgâhı, duvara yaslı |
| Maske aşama 2 — kaba yontu | 1.172 | 27×11×35 | Tezgâh, pencere önü |
| Maske aşama 3 — oyulmuş (göz ve ağız açık) | 9.624 | 25×11×33 | Atölye güney duvarı, askıda |
| Maske aşama 4 — boyalı (alın bandı, yanak, kaş çizgisi) | 9.624 | 25×11×33 | Atölye güney duvarı; ön kapının yanı |
| Talaş kıvrımları | 828 | 30×31×5 | Tezgâh üstü, tezgâh altı, çalışma tezgâhı önü |
| Tokmak | 88 | 14×32×9 | Tezgâh |
| Oyma bıçağı | 88 | 19×3×3 | Tezgâh |
| Pigment kâseleri (3 kil kâse) | 696 | 22×23×3 | Tezgâh |
| Askı çıtası (5 ahşap çivi) | 292 | 92×11×9 | Atölye güney duvarı; ön kapı içi (üstünde havlu ve bez) |
| Kuru ot demeti | 608 | 15×16×53 | Mutfak tezgâhı üstünde tavandan üç demet; atölye askısında bir |
| Mumlu fener | 312 | 15×15×31 | Veranda kirişlerinde iki, hol kirişinde bir |
| Ahşap takunya (çift) | 140 | 29×26×8 | Ön kapı içi; yatağın yanı |

Önizleme: `evidence/blender_esyalar_onizleme.jpg`; oyun içi: `evidence/blender_esyalar_oyun_ici.jpg`, `blender_tezgah_son.png`.

**Ayıklanan uyumsuz eşyalar** (önceki turda benim koyduklarım): baskılı un tenekesi (iki yerde), endüstriyel palet ve kırık palet, kontrplak levha, oluklu sac. Yerlerine kalas ve kütük kondu. Önceki turda denenen düz oval `SM_C01EQ_*` maskesi veranda kapısından kaldırıldı, yerine boyalı maske geldi.

**Durum:** 208 eşya (185 mevcut paketlerden + 23 yeni model örneği), kaydedildi, yeniden açılışta sayıldı, kirli paket yok. Zincir yürüyüşü (`CHAIN_hm`): hedefe ulaştı, 84,9 sn, takılma 0.

**Görsel değerlendirmem (oyun kamerasından):**
- İyi çalışanlar: duvardaki oyulmuş ve boyalı maskeler (atölyedeki mevcut maskelerle aynı aileden okunuyor), ön kapı yanındaki maske, mutfak tavanındaki ot demetleri, kiriş fenerleri, tokmak.
- **Kusur — talaş siyah okunuyor.** Açık ahşap rengi verildi, yeniden içe aktarıldı, yine koyu. Neden doğrulanmadı (ince tek katmanlı şeritlerde ışıklandırma ya da köşe renginin bu mesh'te okunmaması). Sahnede duruyor; düzeltilmeli ya da kaldırılmalı.
- Aşama 1 ham bloğun kenarı testere dişli (ızgara kesimi); "ham" okunuyor ama kaba.
- Fenerlerin içinde ışık yok (yalnız nesne); gündüz sahnesi olduğu için ışık eklenmedi.
- Pigment kâseleri ve oyma bıçağı tezgâhta küçük kalıyor, uzaktan seçilmiyor.
- Takunyalara ve ön kapı içindeki askı çıtasına yakın çekimle bakılmadı.

Hata notu: ilk içe aktarma 100 kat küçük geldi (Blender metre + FBX ölçek seçeneği); modeller santimetre sayılarıyla yeniden üretilip aynı paketlerin üstüne aktarıldı.

## 14. Blender üretimi, ikinci tur (12 Kasım, 00:50–01:20)

- **Talaş kusuru giderildi:** şeritlere gerçek kalınlık verildi ve köşe-rengi yerine evin açık maske ahşabı materyali bağlandı; oyunda artık açık ahşap okunuyor (`evidence/blender_tur2_oyun_ici.jpg`, J1). Önceki siyah görüntünün kesin nedeni ayrıca doğrulanmadı; çözüm işe yaradı.
- **Yedi yeni model** (toplam 19): alet askısı (meşe tahta, altı iskarpela/oyma kalemi, 384 üçgen), üç ayaklı tabure (324), örme sepet (1.128), çalı süpürgesi (416), kil testi (656), kaşıklık çıtası (dört oyma kaşık, 492), demir çemberli fıçı kova (536). Önizleme: `evidence/blender_esyalar_onizleme_19.jpg`.
- **Yerleşim (18 yeni örnek):** atölyede tezgâh köşesi duvarında alet askısı, tabure, tezgâhta testi; mutfakta ocağın yanındaki duvarda kaşıklık, masada testi, yerde kova; oturma odasında koltuk yanında sepet; verandada kapı yanında ve batı ucunda çalı süpürgesi, sepet, masada testi, tabure; arka kapı dışında kova ve süpürge; doğu duvarında kova; yatak odasında sepet; balkonda tabure. Fabrika yapımı görünen süpürge (`Garden_Set_01`) çıkarıldı, yerine çalı süpürgesi kondu.
- **Düzeltme:** alet askısı ilk yerleşimde batı penceresinin önüne denk geldi; tezgâh köşesindeki duvara alındı (`evidence/blender_alet_askisi.png`).

Durum: 226 eşya, kaydedildi, yeniden açılışta sayıldı, kirli paket yok. Zincir yürüyüşü `CHAIN_hm2`: hedefe ulaştı, 84,8 sn, takılma 0, ortalama 37,3 ms.

Görsel değerlendirmem: talaş, kaşıklık, sepetler, verandadaki süpürge ve arka kapıdaki düzen yerinde okunuyor. Alet askısında saplar da demir kadar koyu çıkıyor (meşe materyali gölgede koyu). Tabure, kova ve testilere tek tek yakın çekimle bakılmadı; mutfak masasındaki testi J5 karesinde seçilmiyor (karakterin arkasında kalmış olabilir). Kapı çevresi aşınması ve eşik izleri (decal işi) **yapılmadı**.

## 15. Kapı çevresi ve eşik izleri (12 Kasım, 01:25–01:45) — büyük ölçüde başarısız

Projedeki mevcut decal malzemeleriyle 15 iz denendi (`Tools/Interior_20261111/door_wear.py`), oyun kamerasından dokuz noktada bakıldı (`evidence/esik_izleri_deneme.jpg`):

| İz | Sonuç |
|---|---|
| Yaprak döküntüsü (veranda boşluğu, veranda batı ve doğu köşesi, arka basamak) | Görünüyor, doğal: **kaldı (4 iz)** |
| Ayak izleri (ön kapı içi, veranda tahtaları, arka kapı içi, hol) | Görünmüyor: kaldırıldı |
| Akıntı izleri (mutfak penceresi altı, batı ve doğu duvar) | Görünmüyor ya da belli belirsiz: kaldırıldı |
| Kapı pervazı dibinde nem (ön ve arka) | Arka kapıda duvarda gri dikdörtgen olarak okundu: kaldırıldı |

Son durum `evidence/esik_izleri_arka_kapi_son.png`: dikdörtgen yok, basamak önünde yapraklar var. Kaydedildi, yeniden açılışta kirli paket yok.

Sonuç: eşik aşınması ve kapı çevresi kiri **hâlâ yok**. Mevcut decal malzemeleri bu yüzeylerde çalışmıyor; doğru çözüm, evin zemin ve duvar malzemesine uygun yeni aşınma decal'leri (doku) üretmek. Bu turda doku üretilmedi.

## 16. Aşınma dokusu denemesi durduruldu (12 Kasım, 02:00)

Blender ile dört aşınma dokusu ve bir decal malzemesi üretildi (`/Game/Sphirus/Props/Handmade20261112/Wear/`), 18 iz yerleştirildi. İlk içe aktarmada dokular 32×32 geldi (asenkron yol), izler bloklu ve dikdörtgen okundu; eski doku fabrikasıyla 512×512 olarak yeniden aktarıldı. Bu noktada kullanıcı işi durdurdu: aşınma için sahip olunan hazır paketler kullanılacak (120 Grunge Damage Leak Decals, AutoEnv decay), eşyalar için Fab/Megascans kütüphanesine bakılacak.

Sahne, yalnız dört yaprak döküntüsü izinin bulunduğu kayıtlı duruma geri getirildi ve yeniden açılarak doğrulandı. Üretilen dokular projede duruyor ama sahnede kullanılmıyor.

Bulgular (diskte doğrulandı):
- "120 Grunge Damage Leak Decals" paketi projede, Fab indirme önbelleğinde ve diğer proje klasörlerinde **yok**.
- `Content/AutoEnvTools` projede var: decal değil, beton, tuğla, metal ve plastik için sekiz yüzey malzemesi (`MI_DC_*`) ve bir gösterim Blueprint'i. Evin ahşap ve sıva yüzeylerine doğrudan uygulanamaz; duvar malzemelerini değiştirmek gerekir.
- Megascans: projede yalnız iki kök/zemin parçası ve bir yüzey var; `Documents/Megascans Library/Downloaded/UAssets` boş. Çevrimiçi Fab kütüphanesi giriş istiyor.

## 17. Sahip olunan decal paketiyle aşınma ve Fab kütüphanesi taraması (12 Kasım, 01:10–01:35)

**Paket:** "120 Grunge, Damage, Leak Decal Pack" (Katayama Studio) kullanıcının indirdiği yerde bulundu (`SmartTerrain/DecalPackByKatayama`, UE 5.1 projesi) ve `Content/DecalPackByKatayama` altına aynı `/Game` yoluyla kopyalandı (548 varlık, 1,6 GB; demo haritası alınmadı). Editörde 120 örnek yüklendi (30 çatlak, 30 hasar, 30 kir, 30 akıntı), dokular 2048 px. Katalog: `evidence/gtex_dirt.jpg`, `gtex_leak.jpg` (renk + maske).

**Yerleşim: 27 iz** (`DWR_G_*`, paket örnekleri olduğu gibi), yaprak döküntüsüyle birlikte 31:
- Zemin (9): ön kapı içi ve dışı, veranda boşluğu, arka kapı içi, hol, atölye tezgâhı önü, ocak önü, şömine önü, yatak odası kapısı.
- Kapı pervazları (4): ön ve arka kapıda el hizasında kir.
- Tavan (2): ocağın ve şöminenin üstünde is.
- Dış cephe (12): mutfak penceresi altı ve saçak altlarında akıntı (6), duvar diplerinde sıçrama kiri (4), veranda beton eteğinde kir (2).

Oyun içi: `evidence/grunge_paket_oyun_ici.jpg` (12 görüntü). Görsel değerlendirmem: dikdörtgen ya da blok yok; duvar dibi kiri (doğu ve arka cephe) ve pervaz kiri okunuyor ve doğal. Zemin kiri ve dış akıntılar **çok hafif**, bazı karelerde seçilmiyor; opaklık artırılmadı. **Tavan isleri doğrulanamadı** (kamera açısı tavanı göstermedi). Kaydedildi, yeniden açılışta 31 iz sayıldı, kirli paket yok.

**AutoEnv:** indirilen sürüm projedekiyle neredeyse aynı (iki karo zemin malzemesi fazla); içerik yüzey malzemesi (beton, tuğla, metal, plastik), decal yok. Bu turda kullanılmadı.

**Fab kütüphanesi (tarayıcıda, giriş yapılmış):** yalnız en yeni 24 kayıt okunabildi (sayfa devamını yüklemedi); liste eksik.

| Kayıt | Değerlendirme |
|---|---|
| Megaplants: Lingonberry, Common Heather | Uygun: kuzey konifer ormanı alt örtüsü |
| Megaplants: Common Bulrush | Uygun ve eksikti: kıyı için kamış/saz |
| Megaplants: Black Poplar | Koşullu: yalnız gölet kenarında tek tük |
| Megaplants: Huckleberry Oak, Utah Juniper, Japanese Knotweed | Uygun değil (Kaliforniya çalı meşesi, çöl ardıcı, istilacı tür) |
| Historic Bazaar: hasır sepetler (12, 13, 14, 15, 18, 20), ahşap kasa (08, 15), sandık (04, 05), ahşap masa 02, kil çömlek 39, kil tabak 02, ekmek 02 | Uygun: el yapımı, eski; kendi ürettiğim sepet, testi ve kasaların yerine geçebilir |
| Historic Bazaar: dolma, pasta; Medieval Castle Door | Evle ilgisiz ya da ölçek/üslup dışı |

Bu kayıtların hiçbiri henüz projede değil; indirme/projeye ekleme kullanıcı adımı.

## 18. Aşınma izlerinin güçlendirilmesi (12 Kasım, 01:40–02:00)

Paket örnekleri değiştirilmedi; her kullanılan iz için proje-sahipli bir alt örnek kuruldu (`/Game/Sphirus/Props/Handmade20261112/Wear/MI_GW_*`, opaklık çarpanı ve ton).

- **İlk deneme fazla sertti** (`evidence/grunge_fazla_sert_deneme.jpg`): batı ve doğu duvarındaki akıntılar sert üst ve yan kenarlı dikdörtgen olarak okundu; kapı içlerinde ve pervazlarda siyah lekeler; zemin izleri duvar dibine şerit olarak taştı.
- **Düzeltme:** duvar ortasındaki beş akıntı kaldırıldı (bu paketteki akıntılar bir çıkıntının altına saklanmadan kullanılamıyor); çarpanlar düşürüldü (zemin 2,6 → 1,5; pervaz 1,8 → 1,1; is 3,0 → 1,8; akıntı 2,4 → 1,4); zemin izlerinin projeksiyon derinliği 10 → 3 cm.
- **Son durum** (`evidence/grunge_son.jpg`, 12 oyun içi görüntü): 22 paket izi + 4 yaprak döküntüsü = 26. Ön ve arka kapı içinde eşik kiri, veranda tahtalarında kir, pervazlarda el kiri, ocak ve şömine üstündeki tavanda is, duvar diplerinde kir bandı görünüyor. Kaydedildi, yeniden açılışta sayıldı, kirli paket yok.

Görsel değerlendirmem: tavan isleri artık doğrulandı (iki noktada da duvarla tavanın birleştiği yerde koyu leke). Arka kapı içindeki leke hâlâ biraz koyu ve tek parça; pervaz kirleri leke gibi, sürtünme izi gibi değil. Atölye tezgâhı ve şömine önündeki zemin izleri halı ve gölge yüzünden seçilmiyor. Dış cephede saçak altı akıntısı artık yok (yalnız mutfak penceresi altında bir tane, o da belirsiz).
