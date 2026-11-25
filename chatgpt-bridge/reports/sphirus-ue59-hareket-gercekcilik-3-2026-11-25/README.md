# Sphirus World — 3. hareket geçişi + yeni beden formu (B4), 2026-11-25

**Durum: KISMİ.** Referans paftasına göre beden formu gerçek ağ üzerinde değiştirildi, kıyafetlere aktarıldı, oyuncuya bağlandı, kaydedildi ve editör yeniden açılınca diskten doğrulandı. Fren adımları ortam algılı hâle getirildi (v2). Kol–şort kesişmesi ve sprint dönüşü **açık**; traversal, bölgesel çarpma, yeni düşme türleri ve yorgunluğun kol/adım etkisi **yapılmadı**. Kullanıcı kabulü yazılmadı; AAA iddiası yok.

Proje `sphirus_UE59` (UE 5.9). Oyuncu `BP_HybridA_Player`, `AC_Sph_Motion`, `AC_Sph_Camera`. Kullanıcı kaydı `SFSaveSlot.sav` baştan sona değişmedi (sha `10201b8b41b7`). Bu rapor 446b7a6'daki ara raporun yerini alır; 3. geçişin kök neden ayrıntıları `gecis3_kok_nedenler.md` içinde.

İşaretler: **U** = uygulandı (oyunda, kayıtlı), **D** = doğrulandı (ölçüm/video ile), **A** = açık veya engelli.

---

## 1. Önceki doğrulamanın tamamlanması ve denetim

| Madde | Durum |
|---|---|
| 3. geçişin son seti (46 plan 60/30/değişken Hz, düşme, 17 video) varlık değiştirilmeden bitirildi | **D** — 46 planın hepsinde zemin kayması en kötü ≤ 5.2 cm, ≥ 10 cm hiç yok; p50 kare süresi 17.5 ms (60 Hz) / 17.8 ms (30 Hz) |
| Eşzamanlı yazıcı kontrolü | **D** — VF2C oturumu 04:38'de bitmişti; kilit sahibi yalnız bu oturum (`emb`), kirli paket yoktu. VF2C kıyafet/yüz/saç değişiklikleri korunarak onların üstüne çalışıldı |
| Beden işi için ayrı yedek | **D** — `Saved/UE59Work/b4/ckpt0/` + yazma manifestleri `ue59_m29_b4apply1_092912`, `b4save1_094233`, `b4save2_100824`, `b4save3_103635` |

3. geçişin son verisi: `data_final/` (planlar, geçişler, dönüş, kol, düşme, performans, açık/kapalı karşılaştırmaları).

## 2. Görünür beden: kaynak ve ölçüm (**D**)

- Görünür ağ: `SKM_MHC_Sph8_BodyMesh` (MetaHuman, DNA kullanıcı verisi, morph yok; 4 LOD: 29 711 / 7 482 / 3 303 / 981 nokta). Yüz ağı boynu z≈138'e kadar taşıyor. Sürücü iskelet ile görünür ağ aynı iskeleti (`metahuman_base_skel`, 342 kemik) kullanıyor; retarget zinciri değişmedi.
- MetaHuman gövdesi gizli-yüz kaldırmayla üretilmiş: kıyafet altındaki gövde bandında (z 96–106 sırt/yan) ve iç çamaşırı bölgesinde **geometri yok**. Çevre ölçümleri bu yüzden yalnız tam kesitlerden alındı.
- Ölçüm aynı nötr bağlama pozunda, saç hariç, tabandan kafatası tepesine. Eklem arası mesafe ile yüzey genişliği ayrı tutuldu (deltoid genişliği = eklem arası + humerus eksenine 9 cm içindeki noktaların yanal kalınlığı). Boy gözden türetilmedi.

| Ölçü (cm) | Önce | Sonra | Başlangıç aralığı (×174.7/168) | Not |
|---|---|---|---|---|
| Boy (saç hariç) | 174.7 | 174.7 | — | ilk geçişte korundu |
| Baş yüksekliği | 21.5 | 21.5 | — | |
| Boy / baş | 8.13 | 8.13 | 7.4–7.6 | **A** — baş/yüz kimliği için değiştirilmedi |
| Doğal bel (z≈113) | 63.0 | **75.6** | 74.9–81.1 | aralığa girdi |
| Kalça | 97.0 | **99.3** | 97.7–104.0 | aralıkta |
| Koltuk altı hizası göğüs kafesi | 86.0 | 90.3 | — | |
| Göğüs hizası genişlik × derinlik | 23.6 × 19.6 | 27.1 × 21.3 | — | kaburga genişliği ve derinliği |
| Dış deltoid genişliği | 44.8 | 44.0 | 40.6–42.6 | zaten üstündeydi, omuz **genişletilmedi** |
| Gevşek üst kol | 21.7 | **26.8** | 28.1–30.2 | **A** — 1.3 cm altında |
| En dolgun önkol | 21.0 | **23.8** | 23.9–26.0 | sınırda |
| Üst uyluk | 53.7 | **56.6** | 56.2–60.3 | aralıkta |
| En dolgun baldır | 34.5 | **36.3** | 35.4–38.5 | aralıkta |
| Ayak bileği | 19.0 | 19.0 | — | inceliği korundu |
| Kol açıklığı / boy (kemik zinciri) | 0.889 | 0.889 | 0.98–1.02 | **A** — kemiklere dokunulmadı (bkz. §9) |
| El / boy, ayak / boy | 0.096 / 0.133 | aynı | — | değiştirilmedi |

Tam tablo ve ham değerler: `beden/data/measure_table.md`, `measure_before.json`, `measure_after.json`.

## 3. Beden formu değişikliği (**U**, **D**)

**Yöntem:** topoloji, UV, deri ağırlıkları, yardımcı eklemler ve DNA verisi aynı kalacak şekilde, **kopya** bir iskelet ağına nokta başına konum farkı yazıldı (GeometryScript `copy_mesh_from/to_skeletal_mesh`, tüm LOD'lar). Actor Scale, tek eksenli sıkıştırma veya çalışma zamanı kemik ölçeği **yok**. Kaynak varlıklar değişmedi. Eski GD43 aday/farkları yeniden takılmadı (topoloji bu bedenle uyumsuz).

- Gövde: kesit merkezi etrafında yükseklik boyunca genişlik / ön derinlik / arka derinlik eğrileri (kaburga genişliği z 108–118'de ×1.22–1.27; sırtta kürek kemiği hacmi; bel yan dokusu; alt karın).
- Uzuvlar: kemik ekseni etrafında radyal hacim profili; üst kol orta bölgede ×1.38, önkol üst üçte birde ×1.24 ve bileğe doğru ×1.0'a iniyor; uyluk ×1.09, baldır ×1.07; iç tarafta (medial) azaltılmış.
- Yerel alanlar: trokanter (kalça yanı), kalça arkası, alt karın, kürek kemiği.
- Boyun dikişi korundu: yüz ağına yakın noktalarda fark 0.00 cm; normaller yalnız hareket eden yerde yeniden hesaplandı, boyun/el/ayakta orijinal normal kaldı.
- Kontroller: en büyük yer değiştirme 2.80 cm, ters dönen üçgen 0, üçgen alan oranı 0.94–1.40, tüm LOD'larda geri okuma hatası 0.
- Yüz ve saç kimliğine dokunulmadı.

Varlık: `/Game/Sphirus/CharacterLab/B4_20261125/Body/SKM_Sph_B4_BodyMesh` (fizik varlığı `PHYS_MHC_Sph8`, DNA verisi korundu).

Kanıt: `beden/evidence/board_{front,side,back,front34}.png` (aynı kamera/ölçek kil render, önce | sonra) ve oyun içi `beden/evidence/oyun_idle_{front,side,back,f34}.jpg` (aynı oyun kamerası, eski beden | B4).

**Görsel değerlendirme (dürüst):** kil renderlarda gövde, bel yanı, kaburga, üst kol ve uyluk farkı açık. **Oyun içinde fark orta düzeyde**: açık bel/karın bölgesi ve kollar belirgin dolgun, ama kısa üst kaburga değişikliğinin çoğunu örtüyor. Beden hâlâ "ince-orta" okunuyor; referanstaki "orta-dolgun" hedefe tam ulaşmadı. Baş/boy oranı 8.1 olduğundan karakter referanstan daha uzun bacaklı ve küçük başlı görünmeye devam ediyor (bkz. §9).

## 4. Kıyafet uyarlaması ve oyuna bağlama (**U**, kısmen **D**)

- Beden farkı her kıyafet noktasına en yakın beden yüzeyinden (barisentrik) aktarıldı, 12 cm'den sonra 30 cm'ye kadar sönümlenerek; kıyafet normalleri korundu. Yeni kopyalar: `SKM_Sph_RetroTop_B4`, `SKM_Sph_CuffedShorts_B4`, `SKM_Sph_S8Tank_B4` (3 LOD), `SKM_Sph_Pants70_B4`, `SKM_Sph_Cargo_B4`, `SKM_Sph_Belt2_B4`. Hepsinde geri okuma hatası 0.
- Bağlama: oyuncu şablonundaki beden ve kıyafet bileşenleri ile `GR_OutfitTop / GR_OutfitLow / GR_BeltList` listeleri B4 kopyalarına yönlendirildi (`beden/scripts/c_b4_wire.py`; `B4_OFF` ile geri alınabilir). Kaydedildi.
- **Yeniden açma (D):** editör kapatılıp açıldı; diskten okuma: beden `SKM_Sph_B4_BodyMesh`, kıyafet listeleri B4, 3. geçiş ayarları yerinde, kirli paket yok (`beden/data/reopen_read.txt`; son doğrulama setinden sonraki kontrol `data_b4final/reopen_read_end.txt`).
- **Hareket içinde kıyafet:** koşu ve geri tempo karelerinde şortun yan ve arka kenarında açık renkli yamalar görüldü; aynı kare/aynı zamanda **eski bedende de aynı yerde var** (sol kalçada asılı açık renkli parça ve kıvrık paça içi). Yeni bedenin derisi kıyafetten çıkmıyor görünüyor — yalnız incelenen karelerde; tüm hareket setinde kare kare görsel kontrol yapılmadı.
- Çevrimdışı poz kontrolü denendi (beden ve şort kayıtlı kemiklerle çevrimdışı deri-kaplandı, en yakın nokta işareti): ince, çift katmanlı şortta işaret güvenilmez çıktı (eski ve yeni beden aynı sonucu verdi, sabit eşikte doygun). **Kanıt olarak kullanılmadı.**
- **A:** 18 kemerden yalnız `Belt2` uyarlandı; diğer 17 kemer, iç çamaşırı (gizli) ve takılmayan kıyafetler eski bedene göre. Fizik varlığı kapsülleri (`PHYS_MHC_Sph8`) Python'dan düzenlenemediği için değişmedi; hareket kapsülü değişmedi. El/ayak IK ve tutma soketleri kemik tabanlı olduğu için beden ağından etkilenmiyor; ayrıca test edilmedi. Uzanma/eğilme/çömelme pozlarında kıyafet ayrıca incelenmedi.

## 5. Yeni bedenle hareket doğrulaması (**D**)

Yeni bedenle 23 regresyon planı (60/30/değişken Hz): zemin kayması ortalama 0.4–0.9 cm, en kötü 4.6 cm, ≥ 10 cm **hiç yok** (`data_b4final/plans.txt`).

| Geçiş (yeni beden, 60 Hz) | Süre | Mesafe | Temas |
|---|---|---|---|
| Duruştan yürüyüş | 0.37 sn | 31 cm | — |
| Yürüyüş → koşu (0 → 415) | 0.89–0.95 sn | 201–212 cm | 2–4 |
| Duruştan sprint (0 → 578) | 1.77–1.80 sn | 609–622 cm | 4–5 |
| Koşu → sprint | 0.72–0.76 sn | 349–368 cm | 3 |
| Koşudan duruş | 0.71–0.79 sn | 166–212 cm | 2 |
| Sprintten duruş | 0.79–0.99 sn | 284–348 cm | 2–5 |

Adım sayısı bırakma hızına ve hangi ayağın destekte olduğuna göre değişiyor; sabit 180/315 cm hedefi yok.

- Çömelikken zıplama: tuş yok sayılıyor, ayağa kalkınca da zıplamıyor; ayakta normal zıplama (**D**). Alçak tavan **test edilmedi (A)**.
- Öne düşme (585 cm/s'de takılma): düşüyor → yatıyor → kalkıyor → normal (5 sn), en düşük pelvis 15.7 cm; ayak ucu engelin içine 3 karede en fazla 3.5 cm giriyor (**D**, küçük kusur).

## 6. Fren: ortam algılı süzülme v2 (**U**, **D**)

**Kök neden:** 3. geçişteki fren süzülmesi uyluk yüksekliğinde tek bir çizgiyle engel arıyordu; beden hacmini, yan boşluğu ve zemin sürekliliğini bilmiyordu.

**Şimdi:** tuş bırakıldığında bir kez ölçülüyor —
- karakterin kapsülü hız yönünde `hız × 0.45 + 60 cm` boyunca süpürülüyor (duvar, köşe, dar geçit, alçak engel);
- bu mesafenin 1/4–4/4'ünde dört zemin yoklaması: zemin var mı, yürünebilir mi (eğim), ayak seviyesinin ±35 cm içinde mi (boşluk, uçurum, su yüzeyi, dik eğim burada biter);
- bütçe = min(süpürme, zemin) − (duruş klibinin mesafesi + 40 cm). Süzülme yalnız bütçe içinde sürüyor; bütçe yoksa normal duruş klibi hemen giriyor;
- yeni yön tuşu, geri, çömelme, zıplama, montaj (etkileşim/tepki) süzülmeyi hemen bitiriyor (ölçüldü: 0.22–0.27 sn'de).

Test (sprint bırakma ~584 cm/s; geçici bloklarla, test sonrası kaldırıldı):

| Sahne | Sonuç |
|---|---|
| Açık alan | 319 cm / 0.97 sn'de duruş (süzülme 0.40 sn) |
| Duvar 260 cm ileride | süzülme 0.07 sn, duvardan 57 cm önce duruş |
| Duvar 150 cm ileride | süzülme yok, 83 cm boşluk |
| 45° köşe | duvardan 82 cm önce duruş |
| 110 cm dar geçit | süzülme sürüyor (beden sığıyor), 294 cm |
| 35 cm alçak kutu | süzülme yok, 18 cm boşluk |
| 60 cm platform kenarı (uçurum) | zemin 81 cm'de bitiyor → süzülme yok, kenardan ~15 cm önce duruş |
| 12° rampa, merdiven | süpürme rampaya/basamağa çarpıyor → süzülme yok, normal duruş klibi |
| 45° rampa | süzülme yok |
| Koşu (415) açık alan | süzülme 0.18 sn, 143 cm |

**A:** su kenarı test edilmedi (test haritasında su yok; yoklama su yüzeyini zemin saymıyor ama ölçülmedi). Rampa ve merdivende süzülme hiç başlamıyor — güvenli ama eğimde fren adımı yok.

## 7. Kol–şort kesişmesi (**A**, ölçüldü)

Sabit yarıçaplı vekile ek olarak **gerçek yüzey** ölçümü: oyunda her karede 223 kemiğin dünya dönüşümü kaydedildi, beden ve şort çevrimdışı deri-kaplandı, el/önkol noktalarının uyluk derisine ve şort katmanına işaretli mesafesi hesaplandı (her segment, her ikinci kare; segment başları atlanmadı).

| Hareket (klip) | Bölge | En derin (şort / deri) | Süre |
|---|---|---|---|
| Geri duruş (`M_Relaxed_Run_Stop_B_Rfoot`) | sol el | −9.7 / −5.9 cm | 0.30 sn |
| Geri tempo (`CM_af_Loco_Jog_Bwd`) | sol el | −7.5 / −6.0 cm | 0.33 sn |
| Geri tempo başlangıcı (`CM_af_Loco_Jog_Bwd_Start`) | sağ el | −6.7 / −5.2 cm | — |
| İleri tempo (`CM_af_Loco_Jog_Fwd`) | sağ el | −3.0 / −2.2 cm | 0.50 sn |
| Koşu → sprint geçişi | sol el | −3.7 / −2.6 cm | — |
| Koşudan duruş (`M_Relaxed_Run_Stop_F_Lfoot`) | sol el | −2.5 / −1.1 cm | 0.18 sn |
| Önkol (tüm planlar) | — | girmiyor (en yakın +1.6 cm) | — |

- **Vekil ile fark:** sabit yarıçaplı bilek–uyluk vekili geri tempoda en az +0.8 cm (temiz) diyor; gerçek yüzey eli pelvisin önünde 5–6 cm deri içinde gösteriyor. Vekil bu durumu kaçırıyor.
- **Kök neden:** geri tempo kliplerinde eller pelvisin önünden geçiyor (bilekler orta hatta 1–2 cm'ye kadar yaklaşıyor); yeni beden kalça/uyluk önünü doldurduğu için boşluk azaldı. Kol açıklık düzeltmesi (`CA_*`) uyluk eksenine göre çalışıyor, pelvis önünü görmüyor. Pelvis hattına göre ek sınırlama (`m_arm5`) denendi, iyileşme olmadı, **kapatıldı**. Avuç noktası düzeltmesi (`m_arm4`) açık, etkisi küçük.
- **Görsel doğrulama yok:** bu değerler hesaplı; kare üzerinde tek tek doğrulanmadı.
- **Önerilen düzeltme (yapılmadı):** proje sahipli klip kopyalarında geri tempo/geri duruş kol yolunun düzenlenmesi (eller pelvis önünden değil yan-önden). Kalıcı kol açma katmanı eklenmedi; kollar sürekli açık değil.

## 8. Dönüş ve sprint (**A**)

- 90° sprint dönüşünde kalça yatması 24.9–25.5° (3. geçiş öncesi 35.7°) — kazanç yeni bedende de duruyor (**D**).
- Omuz–kalça burulma aralığı 48–50° — **değişmedi**.
- 180° sprint dönüşü: `Sprint_Turn_180_R_Lfoot` 0.32 sn uçuşla, pelvis uçuşta 4 dönüşün 2'sinde 59–60° dönüyor; `L_Rfoot` 0.15–0.22 sn, 10–18°. Havada dönme **duruyor**. Kaynak klip içeriği; dört varyant var (`L_Lfoot`, `L_Rfoot`, `R_Lfoot`, `R_Rfoot`). Düzeltme yolu: proje sahipli klip kopyasında dönüşü destek ayağına taşıyan faz düzenlemesi veya seçimde destek ayağına uygun varyant — **yapılmadı**.
- Ek karşı-dönme veya klip eğimini yok sayan eğilme katmanı eklenmedi. Sprint, omurga açısıyla "tamam" sayılmadı.

## 9. Bilinçli olarak yapılmayanlar ve nedenleri

- **Kol uzunluğu / boy / baş oranı:** kemik zinciri kol açıklığı 0.89 H (başlangıç aralığı 0.98–1.02), baş 8.1 (7.4–7.6). Bunlar iskelet ve kafa ölçeği değişikliği gerektiriyor (retarget, IK, tüm klipler, yüz kimliği). Talimata uygun olarak ön kabulle kemik değiştirilmedi; ilk geçişte boy korundu. Ölçümle belgelendi, karar senin.
- **Traversal (alçak engel, kenara tutunma, çekilme, duvar destekli çıkış, boşluk atlama):** satıcı `AC_TraversalLogic` / `MotionWarping` oyuncuda var ama çağrılmıyor; 3. geçişteki bağlama denemesi kaydedilmedi. **A.**
- **Çevre algısı (omuz/kol/gövde küçük uyumları):** yeni iş yok. **A.**
- **Bölgeye/yöne/hıza göre çarpma tepkileri, yan/arka düşme ve kalkış:** yok; yalnız mevcut öne düşme ölçüldü. **A.**
- **Yorgunluk:** nefes ve omuz kalkması var (yorgun duruşta omuz hareketi 4.3 cm); kol taşıma, gövde, adım ve dinlenme duruşuna etkisi yok. **A.**
- **Koşu kamerası:** 3. geçiş ayarı (koşuda kol 193→177 cm, sprintte görüş 68.9°→71.8°, "hareketi azalt" yeni terimleri ölçekliyor) yeni bedenle oyun kamerası karelerinde çerçeveyi bozmuyor. Lens değişimi ayrıca test edilmedi.
- Gamepad, standalone, paket: denenmedi.

## 10. Videolar ve kanıt

Tüm videolar normal hızda, kesintisiz. Yeni beden doğrulamasında eski beden videoları kullanılmadı; `OFF` videoları yalnız karşılaştırma içindir (aynı oturumda B4 bellekte kapatılıp kaydedildi, sonra açılış diskten doğrulandı).

- Yeni beden (B4): `videos/b4V_F_*.mp4` — duruş önden/yandan/arkadan/¾, hızlanma (oyun kamerası ve yandan), tempo önden, A/D sprint yandan, WAWD sprint arkadan, ev çevresinde koşu, duvara ve açık alana fren.
- Karşılaştırma (eski beden, aynı ayarlar): `videos/b4V_OFF_*.mp4`.
- Ölçüm verisi: `beden/data/`, `data_b4final/`; betikler: `beden/scripts/`, `scripts/`.

## 11. Değişen varlıklar

Yeni: `/Game/Sphirus/CharacterLab/B4_20261125/Body/SKM_Sph_B4_BodyMesh`, `.../Garments/SKM_Sph_{RetroTop,CuffedShorts,S8Tank,Pants70,Cargo,Belt2}_B4`.
Değişen: `BP_HybridA_Player` (şablon + kıyafet listeleri + fren v2), `AC_Sph_Motion`, `AC_Sph_Camera`.
Değişmeyen: satıcı klipleri, kaynak MetaHuman ağları, VF2 kıyafetleri, haritalar, kullanıcı kaydı.

## 12. Sıradaki adımlar (öneri)

1. Oyunda oynayıp yeni bedeni ve fren davranışını değerlendir (kabul senin).
2. Beden 2. geçiş: üst kol hacmi (+1.3 cm), gövde dolgunluğunun kıyafet altında okunması; baş/boy oranı ve kol açıklığı için iskelet kararı.
3. Geri tempo/geri duruş kol yolu için proje sahipli klip kopyaları.
4. 180° sprint dönüşü faz/klip seçimi.
5. Traversal, çarpma, düşme türleri, yorgunluk etkileri.
