# SPHIRUS UE 5.9 — Tur 8: "The Guardian" hareket tamamlama (2026-11-23)

Durum: **teknik doğrulama yapıldı, kullanıcı kabulü YOK** (USER_ACCEPTED yazılmadı). Görsel ve oyun hissi kararı kullanıcınındır. Bu tur **tamamlanmış değildir**: aşağıda §5'te açık kalanlar var; en önemlisi hızlı A/D ayak kayması.

Kapsam: `BP_HybridA_Player` (GASP / Motion Matching), test haritası `L_Sph_MoveTest`, ev haritası `L_GR_SphirusHouse`. İkinci bir hareket sistemi eklenmedi; değişiklikler mevcut sahiplerde (oyuncu Blueprint olayları, `AC_Sph_Motion`, `BP_Sph_GASPCharacter`).

Kanıt kuralı: "sonra" sayıları, videolar ve ham veri **aynı sürümden**: varlıklar kaydedildi (`scripts/w_save8.py`, son manifest `ue59_m28_r8save3_000207`), editör kapatılıp yeniden açıldı, kaydedilen değerler geri okundu (`data/log.txt` başı, `RCHK`), sonra `scripts/final_r8.sh` bu açılmış durumda çalıştı (2026-11-23 00:04–03:59). Önceki kayıttaki ilk tam koşu `data/ilk_final_kosusu/` altında; iki koşu, düzeltilen 30 Hz sprint→geri durumu dışında birbirini tutuyor.

Kayıt sayıları (son koşu): **24 kayma kaydı** (8 plan × 60 / 30 / değişken Hz) + 7 arazi kaydı, toplam 1853 ölçülen ayak teması; **33 temas kaydı** (24 gerçek çarpma / takılma olayı; 5 kayıt 30 Hz); 26 hareket videosu + 4 ev videosu; 2 ev akışı kaydı.

Test edilmeyenler (yapılmış sayılmadı): **fiziksel gamepad / analog girdi**, **standalone oyunda hareket**, paketleme, ev rotasında performans (ölçüm betiği kullanıcı kaydını taşıdığı için çalıştırılmadı). Tüm girdiler editör içinde enjekte edilen klavye tuşlarıdır.

Kullanıcı kaydı: `SFSaveSlot.sav` sha `3d81ab9dc708…` koşu başında, her ev akışından sonra ve sonda aynı (`data/log.txt`, `data/house.txt`).

---

## 0. Tur 7 raporundaki yanlışların düzeltilmesi

- **"Yorgun" kayıtları (video 21 duruşu, kamera 8,5–12,8 cm) ölçüm aracının hatasıydı.** Kayıt kancası PIE piyonuna her karede değişiklik bildirimiyle değer yazıyordu; bu, her karede construction script'i yeniden çalıştırıp yürüyüş kademesini sıfırlıyordu. Düzeltme: `PropertyAccessChangeNotifyMode.NEVER` (`scripts/hk_ct6.py`). Tur 7'deki "kamera zıplamayı büyütüyor" bulgusu da bu hatadandı.
- **30 Hz sprint→geri kayması için bu turda önce verdiğim iki açıklama da yanlıştı** (fren tabanı `RcMinSpr`, sonra ayak kaldırma). İlk "düzeldi" ölçümü, bir A/B'den bellekte kapalı kalmış `FT_On` ile alınmıştı. Gerçek neden §1.2'de. `RcMinSpr` duruyor ama ölçülen hiçbir şeyin nedeni değil.
- **Zıplama tur 7'ye göre değişmedi** (aynı segmentte 6,5 → 6,6 cm). Tur 7'nin "yürüyüş 4,6 cm" sayısı ile bu turun "4,8 cm" sayısı farklı segmentlerdir; turlar arası kazanç olarak okunmamalı.

## 1. Bulgu → katman → kök neden → değişiklik

### 1.1 Başlangıçta baş düşmesi
- Katman: kaynak klip (yürüyüş başlangıcı → koşuya geçiş klibi pelvis çöküşü).
- Değişiklik: `GR_Bob` içine başlangıç çöküş sınırlayıcı (`BOB_DipK 0,6`, `BOB_DipFree 4`, `BOB_DipMax 9`, `BOB_DipAcc 150`): klibin pelvis düşüşünün 4 cm'den fazlası ×0,6 ile azaltılır. Baş / pelvis sabitlenmedi.
- Sonuç: koşu başlangıcı baş düşmesi **19,4 → 13,6 cm** (30 Hz 18,7 → 12,6); 90° başlangıç **22,5 → 18,5–18,7 cm**. 90° başlangıç hâlâ yüksek (§5).

### 1.2 Sprint → geri, 30 Hz sağ ayak kayması (16,5 cm)
- Katman: oyuncu Blueprint, `GR_StopHold` (duruş klibi sırasında girdiyi tutan mantık).
- Kök neden: tutma 80 cm/s altında bırakıyordu. 30 Hz'de bir kare içinde kapsül sıfırı geçip −1 cm/s'e düşüyor, Motion Matching o karede **geri başlangıç** klibini (`Run_Start_B_Lfoot`) seçiyordu; 60 Hz'de seçim +40 cm/s'te yapılıp **pivot** klibi (`Run_Pivot_F_B_Rfoot`) geliyordu. Yani bir klip çatalı.
- Değişiklik: bırakma eşiği kare süresine bağlı: `GR_StopRel + GR_StopLead × dt` = 80 + 2000 × dt (`scripts/m_stophold8_mcp.py`). Girdi gecikmesi eklemez; düşük kare hızında girdiyi biraz **daha erken** geri verir.
- Sonuç (kaydedilmiş + yeniden açılmış): `g8_B_30` zemin kayması **16,4 → 2,2 cm**, `g8_K_30` **16,9 → 1,7 cm**; 60 Hz ve değişken Hz aynı kaldı (≤ 2,8). Düzeltme öncesi kayıtlar: `raw/g8a_B_30`, `raw/g8a_K_30`; ikiye bölme ve denetim: `data/bis8.txt`, `data/sh8.txt`.

### 1.3 Sendeleme hızı (415 → 344 → 635)
- Katman: temas katmanı (GR_Contact v7), klip oynatma hızı.
- Değişiklik: sendeleme klibinin oynatma hızı kapsül hızına göre yönetilir (`CT_StumK 0,85`); havadayken takılmada sendeleyen ayak, alçaktaki ayağa göre seçilir.
- Sonuç: sendeleme sırasında tepe hız **635 → 414–415 cm/s** (giriş 415; başlangıçta 331).

### 1.4 Geriye çarpma klipleri
- `CT_BwdK 1,7`; geri, geri-sol, geri-sağ çarpmada üç ayrı klip tetikleniyor (`back`, `back-left`, `back-right`; `data/contact.txt`).
- Açık: düz geri çarpmada sistem destek ayağını "yok" görüyor, gerçek faz sol destek (§5).

### 1.5 Kademeli yorgunluk
- Değişiklik: `GR_KFat 0,12` (yorgunken tempo düşer), nefes `PS_BrAmp 0,5`, `PS_BrEff 1,6`, `PS_BrRate0/1 0,25/0,75`. Toplu animasyon yavaşlatma yok; yalnız hedef hız ve nefes genliği değişir.
- Sonuç: yorgun koşu 415 → 370 cm/s, yorgun sprint 585 → 522 cm/s; yorgun kayıtta kamera dikey ≤ 5,2 cm.

### 1.6 Ayak kaldırma ve engel
- `FT_In 60`, `FT_Ext 3`. Basamak koşu kaval kemiği girişi 5,0 cm / 2 kare (30 Hz 4,2 cm / 6 kare); kütük yürüyerek aşma ayak ucu 4,3 cm / 1 kare. Azaldı, sıfır değil.

### 1.7 Ölçüm düzeltmeleri
- `an_bob8.py`: zıplama yalnız gerçek döngü klibinde ve tam adım çevrimlerinde ölçülür (geçiş klipleri dışarıda, ayrı raporlanır).
- `an_air8.py`: havada kalma kapsül–zemin boşluğundan.
- `an_ev8.py`: olay anındaki **gerçek** ayak fazı ile sistemin gördüğü destek yan yana.
- `perf8.py`: gerçek kare süresi özeti.
- 24 kombinasyon: 8 plan × 60 / 30 / değişken Hz. Eşikler gevşetilmedi, kötü fazlar dışlanmadı; "EARLY-FLAG" satırları (ayak havadayken eğri kayması 10–21 cm) zemin kayması değildir ve ayrı sütunda durur.

## 2. Önce → sonra

"Önce" = tur 7 son kayıtları, tur 8 analiz araçlarıyla yeniden ölçüldü (`data/before8.txt`). "Sonra" = bu turun son koşusu.

| Konu | Önce | Sonra | Durum |
|---|---|---|---|
| Sprint→geri, 30 Hz, zemin kayması | 16,5 cm | 2,2 cm | DÜZELDİ |
| Aynı durum, ikinci plan (K, 30 Hz) | 16,9 cm (bu turun ilk koşusu) | 1,7 cm | DÜZELDİ |
| Hızlı A/D, 180° dönüş klibi kayması | 39,6 / 22,6 / 15,8 cm | 37,0 cm (R_60), 32,7 cm (A_60) | **AÇIK** |
| Diğer 22 kayma kaydı, en kötü zemin kayması | ≤ 2,8 cm (6 kayıt) | ≤ 3,4 cm (22 kayıt) | aynı düzey |
| Koşu başlangıcı baş düşmesi | 19,4 cm | 13,6 cm | azaldı |
| 90° başlangıç baş düşmesi | 19,9–22,5 cm | 17–18,7 cm | kısmen |
| Koşu→geri, yeni yöne geçiş | 0,25 s | 0,23 s (30 Hz 0,27; değişken 0,24) | aynı |
| Sendeleme tepe hızı (giriş 415) | 635 cm/s | 414–415 cm/s | DÜZELDİ |
| Pelvis zıplaması, sabit yürüyüş / koşu / sprint | — (ilk kez bu yöntemle) | 4,8 / 5,7 / 3,3 cm; kamera dikey 1,0–1,3 | ölçüldü |
| Koşu→yürüyüş sonrası yürüyüş (2 çevrim) | 6,5 / 7,4 cm | 6,6 / 7,3 cm | **değişmedi** |
| Koşu→yürüyüş geçiş klibi | atlanıyor | hâlâ atlanıyor / 0,10 s; kapsül klipten 0,10–0,20 s hızlı | **AÇIK** |
| Düşme (60 Hz) ayak girişi | 2 kare / 2,6 cm | ≤ 2,4 cm, 1–3 kare | aynı düzey |
| Düşme (30 Hz) | — | düşerken 3,6 cm / 2 kare, kalkarken 2,5 cm / 2 kare | **AÇIK** |
| Tek el taşıma, el duvara giriş | 5,8 cm / 4 kare | 5,6 cm / 3 kare (ilk koşu 5,4 / 2) | **değişmedi sayılır** |
| Yan sıyırma dirsek | — | 1,3 cm / 4 kare | ölçüldü |
| Merdiven havada kalma / zıplama | 0 / 3 × ~0,6 s | 0 / 3 × 0,60–0,62 s | aynı |
| Arazi (merdiven, rampa) zemin kayması | — | ≤ 4,7 cm, ≥ 10 cm yok | ölçüldü |
| Kare süresi (kayıt sınırı 24 Hz) | p50 41,7 ms | p50 41,7, p95 42,2–42,4, p99 42,5–42,7 ms | aynı |
| Ev akışları (yatak, maske, dolap, çay, odun-ateş) | PASS | PASS, kayıt değişmedi | korundu |

## 3. Değişen varlıklar (manifest + doğrulanmış yedek, `data/manifests.txt`)

- `/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player` — GR_Bob çöküş sınırlayıcı, GR_StopHold eşiği, yorgunluk / nefes değerleri, temas değerleri (`CT_StumK`, `CT_BwdK`), ayak kaldırma değerleri.
- `/Game/Sphirus/Player/Motion/AC_Sph_Motion` — `RcMinSpr 150`, `RcMinV 500`.
- `/Game/Sphirus/Player/GASP/BP_Sph_GASPCharacter` — yeni değişkenlerin varsayılanları.
- Satıcı asılları ve kullanıcı kaydı üzerine yazılmadı. Bellekte denenip **kaydedilmeyen**: `PSS_Relaxed_Pivots` yörünge ağırlığı 10 → 3 (etkisizdi, geri alındı).

## 4. Videolar (`videos/`, gerçek hız, aynı son sürüm)

01–26 hareket (omuz kamerası `omuz_`, sabit yan kamera `yan_`), 27–30 ev. Not: açık alandaki yan kamera videolarında güneş alan taraf **aşırı pozlanmış** (ten ve üst beyaza yanıyor; tur 7 videolarında da aynıydı). Siluet ve ayak teması okunuyor, yüzey ayrıntısı okunmuyor. Benim baktığım kareler `evidence/` içinde; videoların tamamını kare kare izlemedim.

## 5. Açık kalanlar ve yapılmayanlar

1. **Hızlı A/D ayak kayması (22–40 cm).** Yaklaşık yarı yarıya gelen bir çatal: kötü dalda `Turn_*_180_*foot` klibi, basma ayağı zaten yerdeyken ve kapsül hâlâ ~330 cm/s giderken başlıyor. MM karışım süresi ve dönüş veritabanının yörünge ağırlığı etkisiz çıktı. Gereken iş klip / seçim düzeyinde (dönüş klibine giriş fazı veya A/D için ayrı fren klibi); ayar ile kapanmıyor.
2. **Koşu→yürüyüş geçiş klibi** atlanıyor veya 0,10 s oynuyor (chooser); sonraki iki yürüyüş çevriminde zıplama 6,6–7,3 cm.
3. **Düşme:** eller düşerken havada asılı kalıyor (`evidence/01`), ağırlık aktarımı zayıf; yana / geriye düşme klibi yok; 30 Hz'de düşme ve kalkmada 2,5–3,6 cm giriş.
4. **90° başlangıç baş düşmesi** 17–18,7 cm.
5. **Tek el taşıma el sıyırması** 5,6 cm; basamak koşu kaval 5,0 cm.
6. **Kafa kafaya çarpma klibi** destek ayağına göre seçilmiyor; düz geri çarpmada sistem desteği "yok", gerçek faz sol destek.
7. **Kamera:** maske inceleme kadrajı ve koridorda saç yakınlığı için bu turda değişiklik yapılmadı (tur 7'deki geniş kadraj denemesi maskeyi başın arkasına saklıyordu).
8. 45° / 135° / 180° dönerek başlangıçlar yalnız ters yön planı içinde kısmen ölçüldü; ayrı plan yok.
9. Analog / gamepad, standalone, paket, ev rotası performansı: **test edilmedi**.

Ölçüldü / görüldü / doğrulanamadı ayrımı: §2'deki sayılar ölçümdür. Görsel olarak yalnız `evidence/` kareleri incelendi. Oyun hissi (ağırlık, kontrol, "Guardian" okunuşu) doğrulanamaz; kullanıcı kararıdır.

## 6. Yeniden üretim

- Varsayılanları uygula: `scripts/alldef.py` (her ölçümden ve kayıttan önce; bellekte kalan A/B değerlerini temizler).
- Kaydet: `scripts/job8.sh scripts/w_save8.py <etiket> 300 --assets <3 varlık>`; editörü yeniden aç; `scripts/rchk.py` ile geri oku.
- Tam doğrulama: `scripts/final_r8.sh` (~4 saat; kayma 24 → ters yön / başlangıç / zıplama → temas → arazi → duruş → video → ev).
- Çatal teşhisi: IDLE→MOVING karesinde seçilen klibi ve o karedeki hız işaretini listele; her kolu en az iki kez koş (koşular kare kare aynı değildir).
- Ham kayıtlar `raw/*.json.xz` (satır: t, vx, vy, yaw, gasp [klip, DB, kademe, durum], ayak hızları, rdt…).
