# SPHIRUS V2.26 — Tasarlanan hareketin oyunda korunması, gerçek sahnede inceleme, arazi uyumu

Taban: V2.25 üretimi (bridge commit 99198f3). Tarih: 2026-10-24. Tüm ölçümler sabit adım 30 FPS (aksi yazılmadıkça), harness **üretim modu** = kaydedilmiş durum, hiçbir aday bayrağı yok; aday koşuları etiketlerinde `_<aday>_` taşır.

**Genel durum: PARTIAL.** Teknik doğrulama (`verify_prod226`: ayar/graf) ile hareket kalitesi ve görsel kabul ayrı yazıldı. Kullanıcı kabulü verilmiş sayılmadı.

## İlk sayfa — üç soru

### TEMPOLU (koşu fren–destek–yeniden itiş)
| Soru | Cevap |
|---|---|
| Klipte tasarlanan ayağı hangi işlem bozuyordu? | **Dünya çerçevesinde ölçüldü** (`req/capterm.py`: tasarlanan ayak = girişteki kapsül + kapsül tablosu yer değiştirmesi + klip ayağı; klip bileşen uzayında ileri eksen **+y**, mesh −90° — klip x'i dünya ileri ile karşılaştırmak anlamsız, ilk zincir ölçümleri bu yüzden yanlış sahip gösterdi). Hata iki terime ayrıldı: **kapsül saati terimi** (oyun kapsülü − tasarım kapsülü) 0,9 s boyunca ≤5 cm → üretecin ölçülen kapsül tablosu doğru; **poz terimi** (görünen ayak − klip ayağı, kapsül çerçevesi) FootPlacement **kapalıyken** giriş karışımından (0,25 s) sonra ≤4 cm → tasarlanan ayak oyunda gerçekleşiyor. FootPlacement **açıkken** sabitlenmiş fren ayağı 23 cm geriye itilip 0,4 s içinde geri dönüyor (bu sırada bileşen teması `ContactR` false). **Aşama D (FootPlacement) ilk kırılma noktası**; giriş (C, 32 faz kutusu) basılı ayakta 2 cm süreklilik; üreteç (A/B) r4/r5 ile düzeltildi. İkinci büyük bölüm **çıkış**: bileşen yön değiştirme bölümünü ~0,75 s'de bitiriyor (`SHM_RedirectActive` false) → ABP geri dönüş veritabanını bırakıyor → MM 1,97 s'lik klibin 1,0 s'inde `A_RB_Jog_Rear`'ı başka bir ayak evresinde seçiyor (0,1 s'de 28 cm ayak sıçraması). |
| Gerçek neden giderildi mi? | **Kısmen.** Giriş uyumsuzluğu (8 → 32 kutu, 20–25 → ≤2 cm) ve üreteç hataları (salınım sabit noktadan; toe-off öncesi döngü şekli) giderildi, ölçüldü. FootPlacement etkileşimi **giderilmedi**: veri sözleşmesi (`datacontract226`) kliplere `footspeed_l/r` (kinematik v1, salınım tabanı v2) ve `Disable_FootLock=1` (v3, t11) yazıldı — kayma tablosu 1 cm içinde aynı (t11 = t9) → FP'nin etkisi kilit üzerinden değil. Çıkış için DB `continuing_pose_cost_bias` −0,05 → −0,4 (t12) klibi tutmadı (DB anahtarı bileşende, yukarı akışta) ve bir evrede geri dönüşü tamamen atlattı → geri alındı (−0,05). Aday **üretime alınmadı**; üretim V2.24 pivot DB'lerinde kaldı. Kalan kol: SHM226 klibi seçiliyken `SHM_FootPlaceOff` kapısı (düz zeminde) + bölüm süresinin klip uzunluğuna bağlanması — izleyen tur. |
| Yeni hareket doğal ve farklı evre/FPS'de güvenilir mi? | Duruş (`posture226`): aday leğeni üretimden yüksek (−2..+7 cm vs −11..+6), gövde eğimi ≤31° (üretim 46°), diz ≤104°, kol uzanımı aynı — çömelme/kambur yok. Basılı ayak kayması karışık (tablo §3.4: 6 senaryoda daha iyi, 6'da daha kötü; medyan 19 → 23 cm). FPS taraması üretim için yapıldı (§3.6); aday için 30 FPS evre taraması (14 senaryo) var, 20/60/120 yalnız üretim (aday alınmadığı için). Üretim yavaş-çekim aileleri: değişmedi (açık liste). |

### İNCELEME (gerçek R05 atölye maskeleri)
| Soru | Cevap |
|---|---|
| Gerçek atölye maskelerinde çalışıyor mu? | **Evet (t7, üretim modu; final tur §4.5).** Neden çalışmıyordu: bakış küre izi batı duvarına (x≈42) çarpıyordu; maskeler x=33'te, duvar çarpışmasının **içinde** asılı. Çözüm (sahne çarpışması değişmedi): her maskeye yalnız **Visibility** kanalını bloke eden, diğer her şeyi yok sayan QueryOnly küre bileşeni (r 12, maskenin 25 cm önünde, bileşen etiketi `GR_Inspect`; `inspect_probes226.py`, geri alma `V226_PROBE_REMOVE`), maskelere aktör etiketi (`tag_masks226.py`). Sözleşme ad değil **etiket** (`InspectTag` = GR_Inspect, aktör veya bileşen); odak = aktör sınır merkezi (sabit nokta, aktör kimliğine bağlı bekleme; **not:** kaydedilmiş DA `InspectJump` 45 cm — DSL varsayılanı 2 var olan DA'ya yazılmadı, bu turda değiştirilmedi → 29 cm aralıklı iki maske bekleme için "aynı hedef" sayılır, komşuya geçiş yeniden bekleme olmadan olur). Yakalama ilk bakışta 0,43–0,53 s (cand 3,87 → on 4,43), bırakma bakış kayınca; kendini tetikleyen kayıp/yeniden kazanım döngüsü yok (ins_ws 1 yakalama / 1 bırakma). |
| Yakınlaşma olmadan anlamlı fark var mı? | A/B/C aynı senaryo (ins_ws, t7): **A** normal takip: yakalama yok, kamera–kapsül 149, ekranda gövde −0,45. **B** (üretim, `InspectZoomOn` kapalı): kamera–kapsül 149 → 148 (eşit), FOV 62 sabit; gövde ekranda −0,45 → −0,37 (hedefe yer açan yan ofset), takip sakinleşiyor (jerk95 içeride 0,41 / dışarıda 1,26), baş/boyun bakış alfası 1,0. **C** (yakınlaşma): 149 → 113, ikinci bakışta 133 — tutarsız, **üretime alınmadı**. Fark yakınlaşma değil: kadraj + gövde/baş bakışı. |
| Son görünen baş/boyun ve kontrol güvenli mi? | Kontrol yaw/pitch yalnız girdiyle değişiyor (inceleme kamera ofsetine ve bakış alfasına yazıyor; `ay` sabit). Baş/boyun dönüş açısı kemik ekseninden güvenilir çıkarılamadı (eksen kuralı bilinmiyor) → **NOT_MEASURED**; bakış alfası 1,0 ve videolar kanıt. İki yakın maske (29 cm): 175°'de ışın ikisinin arasından geçip Silent'ı tuttu (r 20 küreler çakışıyor) → r 12 küre + `InspectRadius` 12 (üretime alındı), senaryo 172° (§4.5). Paketlenmiş geçerlilik: etiket + bileşen sözleşmesi paketlemede değişmez (GetDisplayName tuzağı yok); paketli test **NOT_TESTED**. |

### ARAZİ
| Soru | Cevap |
|---|---|
| Kaldırma–temas geri beslemesi önlendi mi? | **Evet.** V2.25 T1b (0,10 s onaylı salınım) düz zeminde ve tümsekte kaldırmayı 0/kararlı tutuyor (d_walk/d_jog kaldırma 0; tümsek basılı ayak z ikinci farkı 6,2). V2.26 T3d: platform içinde kalan ayak temas sayılıp hızlı bırakılmıyor, dışarı kaldırılıyor (`StepPenLiftMax` 36). |
| Yüksek basışta doğru yere basılıyor mu? | **Kök neden bulundu ve giderildi:** kaldırma hedefi kaldırma uygulanmış ayağa göre hesaplanıyordu → ihtiyacın **yarısına** yakınsıyordu (28 cm basamakta 34 gerekirken 17; V2.24'ten beri tümseklerde de). T3g (`v226_patch_terrain10.py`): açık kaldırmasız poz ayağından (`fz = FootCenter.z − SwingLift`). Sonuç 28 cm basamak yürüyüş: basış **platform üstünde** z 31,8 (önce 18 cm içinde); 20 cm basamak z 24,4. İniş kaydırması (`StepEdgeOn`: destek ayağı + adım tahmini, kenar sondası, ik_foot dünya-uzayı kaydırma): basış kenardan 10 → 22–23 cm içeri (28 cm), 7 → 19 cm (20 cm). Koşu 28 cm: ilk ayak kenarda askıda kalıp 0,1 s basamağa 13 cm giriyor, basmıyor (sağ ayak 112 cm içeri basıyor) — **açık**. Kapsül ön-yükselmesiyle gizleme yok. Son üretim kararı §5.5. |
| Gerçek ev–orman rotasında çalışıyor mu? | map_r2 (24 m, 223 cm kabartma, aynı yöntem): temas bölümü kayma p90 5,8 / max 9,0 cm (V2.24 üretim koşuları p90 2,3–6,0 / max 4,7–10,2) → **değişim yok**, regresyon yok; kaldırma ve ayak basışı yüksek basamakta iyileşti (§5.2/5.6). Kapıların dışında basamak yok (`probe_route226`: veranda 50 cm düşüş adımlanamaz) → gerçek rota kanıtı inişli-çıkışlı map_r1/r2/r3 (§5.6). |

---

## 1. Test aracı (§2) — gerçek durum
- `qa_pie.py` **state_mode**: `production` = kaydedilmiş SHME DA / ABP varsayılanlarına dokunulmaz (eski şema-varsayılanı sıfırlaması kaldırıldı — eski harness kaydedilmiş üretim değerlerini hiç test etmiyordu); `candidate` = üretim + yalnız o koşunun `abp_flags`/`shme_flags`/cvar'ları, bir sonraki koşudan önce geri alınır.
- Koşu başı/sonu etkin durum kaydı (`<label>_state.json`): SHME DA alanları, ABP veritabanı referansları (varlık, dosya zamanı, giriş sayısı), cvar'lar; fark → `INVALID_STATE` (pop_report özetinde durum + mod).
- Kullanıcının kirli paketlerine dokunulmadı: her mutasyon öncesi ikili kontrol noktası `checkpoint/pre_v226/` (DA, bileşen, profil, ABP taban+çocuk, BP_PBI/GR_Player, L_GR_SphirusHouse) + araç kaynakları; ev alt seviyesi için etiket-sonrası / küre-öncesi / küre-sonrası kopyalar (etiket-öncesi bayt kopyası alınmadı — geri alma `untag_masks226.py`).
- Son birleşim: üretime alma → temiz yeniden açılış (`relaunch`) → `verify_prod226` (ALL_OK) → üretim modunda kanıt (aday override yok) → tam-kare yakalamalar.

## 2. Zincir tanısı yöntemi (A–E)
`clipfoot226.py` (klip tabloları 120 Hz, kök-göreli = kapsül çerçevesi; tüm klipler EnableRootMotion+ForceRootLock, kök izi 0) + `req/capterm.py` (dünya çerçevesi ayrışımı) + cvar aşama çıkarma (`rv32F` FP kapalı, `rv32RAW` FP+LegIK+Stride+Orientation kapalı) + `plant225.py` (basılı ayak bölümleri) + `posture226.py`. Hizalama olaylara göre (giriş karesi = ilk SHM226 karesi; `av_Phase27_SelectedTime` saat).

| Aşama | Ölçüm (ph3, F_B_P21, v226t9) | Sonuç |
|---|---|---|
| A kaynak klip | tablo: fren ayağı kapsül çerçevesinde +19 → −20 cm (0,07–0,48 s); tasarım dünyası 7738 ± 2 cm sabit | tasarım doğru (pinlenmiş) |
| B klip tek başına | kapsül saati terimi ≤5 cm (0,9 s) | kapsül tablosu doğru |
| C giriş + karışım | giriş 5,33 s ct 0,067; basılı R ayak 7740,5 (döngü) → 7738,3 (klip): 2 cm; salınan L 15 cm (havada), 0,25 s'de kapanıyor | iyi |
| D ayak/leğen düzeltmeleri | FP kapalı: R 7738 → 7731,8 (−6, karışım kuyruğu) → 7741–7743; FP açık: R 7738 → **7714,8** (5,63 s) → 7741 (6,07 s) | **ilk kırılma: FootPlacement** |
| E retarget/final | RAW ≈ FP kapalı (warp'lar katkısız) | — |
| Çıkış | 6,27 s klip ct 0,97'de bırakılıyor (klip 1,97 s); R ayak 7745 → 7773 (0,1 s) | **bileşen bölüm sonu → DB anahtarı** |

## 3. Geri dönüş — içerik ve çalışma zamanı
### 3.1 İçerik (aday, üretimde değil)
- `gen226_rev.py`: 32 faz kutusu (giriş 20–25 → ≤2 cm), ölçülen kapsül tablosu (`capsule_rev_table.json`), r4 yön değiştirmeye kadar pin, r5 salınım pinlenen ayaktan. 64 klip `SHM226_JogRev_{B_F,F_B}_P0..31`, DB `PSD_SHM226_JogRevBwd/Fwd` (`build_v226_revdbs.py`, tam BranchIn pencereleri, döngüler dahil).
- Veri sözleşmesi (`datacontract226.py`): ABP'de eğri okuyan tek düğüm FootPlacement (`footspeed_l/r`, `Disable_FootLock`); notify/sync marker tüketilmiyor; şema PSS_Default Trajectory+Group. `add_footspeed226.py` v1/v2/v3 kliplerin kendi izlerinden (kör kopya yok). Diğer DB'lere SHM226 sızıntısı yok (verify kontrolü `db_leak226`).
### 3.2 Çalışma zamanı
Üretim rotası değişmedi (V2.24 JRMode 3). Aday yalnız DB referanslarıyla (`SHM224_DB_JRBwd/Fwd(+M)` → PSD_SHM226) test edildi.
### 3.3 Kapsül profili
Kapsül bileşene ait, üretim = aday (aynı eğri): 300 → 0 0,43 s (~700 cm/s²), geri hız 150 cm/s² ile; tablo ile fark ≤5 cm.
### 3.4 Basılı ayak kayması (en kötü net cm; `plant225`)
| Senaryo | üretim (V2.24 pivot) | rv32 t4 (eğri yok) | t9 (footspeed v2) | t11 (+Disable_FootLock) |
|---|---|---|---|---|
| sw_ph0 | 16,7 | 20,1 | 24,6 | 25,1 |
| sw_ph1 | 21,5 | 20,2 | 24,5 | 25,1 |
| sw_ph2 | 26,1 | 17,8 | 16,7 | 16,6 |
| sw_ph3 | 10,6 | 14,8 | 16,7 | 16,8 |
| sw_ph4 | 14,5 | 11,9 | 16,7 | 16,6 |
| ph0 | 49,7 | 21,0 | 24,6 | 25,1 |
| ph1 | 32,5 | 19,9 | 24,6 | 25,2 |
| ph2 | 14,5 | 12,1 | 21,7 | 17,8 |
| ph3 | 16,6 | 32,0 | 24,6 | 23,7 |
| ph4 | 16,6 | 22,3 | 22,9 | 24,2 |
| rel (kısa bırak-bas) | 30,4 | 5,7 | 9,0 | 12,0 |
| dbl (ikinci dönüş) | 35,5 | 16,5 | 10,2 | 19,5 |
| ad_ph0 (çapraz) | 26,8 | — | — | 0,0* |
| m180w (fare 180+W) | 0,0 | — | — | 0,0 |
*ad_ph0 adayda klip seçilmedi (0 = JogRev bölümü yok). Adayda en kötü bölümler çıkış karışımı (23–25) ve tasarımın yumuşak iniş yaklaşımı (+10 cm, yükseklik ölçütüyle "basılı" sayılıyor); FP açık 23 cm fren ayağı gezintisi ayrıca. Üretimde en kötü bölümler fren ayağının 36–50 cm kayması (ph0).
### 3.5 Duruş (olay evresi, `posture226`)
Aday leğen −2..+7 cm (üretim −11..+6), gövde eğimi ≤31° (46°), diz ≤104°, kol uzanımı aynı. Çömelme/kambur yok; yavaş-çekim hissi ölçülmedi (video).
### 3.6 Üretim FPS / gerçek zaman taraması (final zincir)
Üretim (V2.24 pivot) sabit adım, en kötü basılı ayak net kayması (cm), aynı senaryo dosyası, olaylara göre hizalı:

| Senaryo | 20 FPS | 30 FPS (fin) | 60 FPS | 120 FPS |
|---|---|---|---|---|
| ph0 (W→S→W) | 49,6 | 49,7 | 32,4 | 30,5 |
| sw_ph2 (S→W) | 25,3 | 31,2 | 21,6 | **51,6** |
| ph3 (geç istek) | 16,8 | 16,6 | 15,4 | 26,7 |
| ovl120 (örtüşen istek) | **65,4** | — | 23,4 | 35,2 |

Üretim geri dönüşü **FPS'e bağımlı** (MM arama zamanlaması + FootPlacement kilit bırakma kare hızına bağlı; V2.25'te de gözlenmişti). Sıçrama sayacı (>25 m/s²) kare hızıyla ölçeklendiği için 60/120'de karşılaştırılamaz (metrik uyarısı).
Gerçek zaman (sabit adım yok, editör ~27–32 fps): **soğuk başlatma** (taze editör, ısınma koşusu yok, ilk PIE; DB ilk indeks durumu `_pie.json` first_index/db_first alanları boş = DB önceden indekslenmiş, gizli ısınma yok) ph0 48,4 (sabit 30: 49,7); kısa takılma koşuları sw_ph2 26,5, dbl 32,6, rel 21,4. Durum kayıtları (`*_state.json`): mode production, diff {} — tüm final koşular geçerli.
### 3.7 Karar
rv32 üretime **alınmadı** (karışık kayma, FP gezintisi çözülmedi). Üretim geri dönüşü V2.24 ile aynı; V2.26'da geri dönüşte **çalışma zamanı değişikliği yok**.

## 4. İnceleme kamerası
### 4.1 Tanı (t2/t3 telemetri I3)
`InspectHitActorName/Dist/Z/Match`: ins_ws'de çarpılan aktör batı duvarı (x≈42), mesafe ~130, maske x=33 → ışın maskeye ulaşamıyor; eski ad sözleşmesi (`Mask` içeren display name) duvarda eşleşmiyor.
### 4.2 Sözleşme (I4, üretimde)
`Aktör|ActorHasTag` / `Bileşenler|ComponentHasTag` `InspectTag`; odak `GetActorBounds` merkezi; `InspectJump` (kaydedilmiş 45 cm, bkz. not); `InspectZoomOn` (false) boom ve bakış-yönü pivot payını kapatır. Küre sondaları §İlk sayfa. Sahne çarpışması değişmedi; duvar yok sayılmıyor (duvarın ÖNÜNDEKİ küre bloke ediyor).
### 4.3 A/B/C (ins_ws, t7, sabit 30)
| | A takip | B inceleme (üretim) | C yakınlaşma |
|---|---|---|---|
| yakalama | yok | 4,43 s (bak 3,87) | 4,43 s |
| kamera–kapsül | 149 | 149 → 148 | 149 → 113 (2. bakış 133) |
| FOV | 62 | 62 | 62 |
| gövde ekran x | −0,45 | −0,45 → −0,37 | −0,45 → −0,30 |
| kamera jerk95 içeride/dışarıda | — | 0,41 / 1,26 | 0,48 / 1,26 |
| bakış alfa | 0 | 1,0 | 1,0 |
### 4.4 Testler
İki yakın maske (ins_ws2: 180→172→180→172 bakış): r 20'de 175° ışın arada → Silent; r 12 + InspectRadius 12 (final §4.5). Uzaklaş-bak / ileri-geri / dar alan (ins_qa lamba) / yürürken serbest bakış (>60 cm/s tetiklemez): t3/t7 geçti. Kontrol yaw'ı yalnız komut dosyası girdisiyle.
### 4.5 Final üretim modu
Üretim modu, temiz yeniden açılış sonrası (`inspect226`):
| Koşu | aday → açık | kamera–kapsül önce/içinde/sonra | FOV | çarpılan hedefler (sırayla) | not |
|---|---|---|---|---|---|
| ins_ws (atölye, tek maske) | 4,00 → 4,57 (0,57 s), bırakma 5,20 | 149 / 148 / 147 | 62 sabit | Cerulean → Silent → duvar | bakış kayınca bırakma; kontrol yaw değişimi yalnız senaryo girdisi (44°) |
| ins_ws2 (iki maske, 172°) | 3,60 → 4,17, açık 4,17–13,10 | 148 / 150 / 145 | 62 | Silent → Cerulean → Silent | r 12 küre + sorgu 12: iki maske ayrı ayrı çarpılıyor; `InspectJump` 45 nedeniyle komşuya geçiş aynı pencerede (yeniden bekleme yok) |
| ins_qa (lamba, dar alan) | 4,70 → 5,27, açık 5,27–8,20 | 198 / 193 / 202 | 60,8 / 60,0 | INS_Lantern → boş | V2.25 davranışı korunmuş |
Kemik yaw dönüşü eksen kuralı nedeniyle NOT_MEASURED (bakış alfası 1,0; video). Yakınlaşma yok (mesafe ±2 cm, FOV sabit); fark yalnız kadraj ofseti + gövde/baş bakışı.

## 5. Arazi
### 5.1 Değişiklik zinciri (T3a–T3g; `v226_patch_terrain5..10.py`, `install_v226_shift.py`)
T3a destek zemini üstündeki platform kapısı; T3b/c/f iniş tahmini + kenar sondası + `StepEdgeShift` kaydırma (ABP dünya-uzayı ModifyBone `SHM226_ShiftL/R`, LegIK öncesi), basılıyken/platform üstünde tutma; T3d penetrasyon kaldırma; T3e `StepPenLiftMax`; T3g tam-açık kaldırma (kök neden). StepPrep (V2.25 reddi) başka adla geri eklenmedi; kapsül ön-yükselmesi yok.
### 5.2 Basamak tablosu (yürüyüş; `step226`)
| basamak | V2.25 üretim | V2.26 m6 (T3g, margin 6) | te6 (+kaydırma) |
|---|---|---|---|
| 28 cm | kenardan 10 cm, z 18 (içinde, pop) | 10 cm, z 31,8 (üstte; basmadan önce ~0,3 s askı) | 23 cm, z 38 |
| 20 cm | 7,5 cm, z 18 | 7,5 cm, z 24,4 | 19 cm, z 22,5 |
| koşu 28 cm | içinde | sol ayak basmıyor (askı → 13 cm batma 0,1 s), sağ 112 cm içeri | aynı |
### 5.3 Regresyonlar (m6)
Tümsek yürüyüş kaldırma 18–21 → 14–15 cm (yeterli), kayma max 4,6 aynı; düz zemin kaldırma 0; map_r2 kayma aynı yöntemle V2.24 bandında (§5.6).
### 5.4 Rota sondası
`probe_route226`: kapı önlerinde yürünebilir basamak kenarı yok; veranda 50 cm düşüş. Gerçek rota kanıtı = map_r1/r2/r3 (iniş, çıkış, çapraz eğim, kısa duruş, yeniden başlama senaryo içinde).
### 5.5 Üretim kararı
Ön-aşama (final zincir, aday te6x = kaydırma + `StepEdgeMin` 10): gerçek rotalarda kaydırma **sessiz kalmadı** — map_r1 278 karede (max 12 cm, 14–16° eğimli bölümde), map_r3 35 karede (max 11 cm), map_r2 0. Kenar sondası eğimli zemini kenar sanıyor → iniş kaydırması **üretime alınmadı** (`StepEdgeOn` false kaldı; ABP düğümleri kurulu ama sıfır vektör = etkisiz; "kurulu ama kapalı ≠ eklendi"). Üretime alınan arazi değişikliği: **T3a + T3d/T3e + T3g** (kaldırma kök neden düzeltmesi) ve `SwingLiftMargin` 10,5 → 6 (m6). Basamak kanıtı m6 sütunu (§5.2); koşu 28 cm basamak açık.
### 5.6 Final üretim modu rotalar
Üretim modu, temiz yeniden açılış sonrası (m6 = T3a/d/e/g + SwingLiftMargin 6; `step226`, temas-bölümü kayma istatistiği):
| Koşu | sonuç |
|---|---|
| ter_drop_walk 28 cm (sağ ayak ilk) | R basış kenardan 11,2 cm içeri, ball z 30,4 (üst 28) — **üstte**; platform üstünde en alçak salınım 25,8 (içine girmiyor); leğen z 86 → 120, max 2,0 cm/kare (sıçrama yok) |
| ter_drop_walkB (sol ayak ilk / farklı yaklaşım) | R basış 11,2 cm içeri z 33,2; en alçak 27,1 | 
| ter_drop_jog 28 cm | L basış kenardan 4,7 cm içeri, z **23,1** (5 cm içinde, kaldırma 8,2), sonra R 117 cm içeri z 29,4 — **koşu yüksek basamak açık** (V2.25: basmıyordu) |
| ter_step2 8 / 20 / 13 cm | 8: z 9,3 üstte; 20: L 7 cm içeri z 21,3 üstte (en alçak 20,5); 13: z 15,9 üstte |
| ter_bump_walk (tümsek) | düz bölüm plant_slip 4,3 / 5,6, catch 0 |
| d_walk / d_jog (düz) | kaldırma 0, sıçrama 0; kayma p90 5,4 / 4,5 |
| map_r1 / r2 / r3 (gerçek ev–orman, 26,6 s, iniş-çıkış-çapraz-duruş-başlama) | temas bölümü kayma p90 4,5 / 5,8 / 3,7 cm, max 13,4 / 9,0 / 8,8, birikmiş 80 / 69 / 54 cm; max kaldırma 23–25 cm; sıçrama 10 / 6 / 8 (montaj 2–4) |
| map_r2 gerçek zaman | p90 8,3 / max 18,7 (değişken dt; sabit adımla karşılaştırılmaz) |
Aynı yöntemle önceki üretim koşuları (map_r2): V2.24 p90 2,3–6,0 / max 4,7–10,2; V2.25-durumu (v226t6) p90 3,7 / max 6,9 → yuvarlanmış zeminde **değişim yok** (koşudan koşuya varyans içinde); kazanç yalnız yüksek basamakta.

## 6. Üretim anahtarları ve temiz yeniden açılış
Üretime alınan anahtarlar (`promote226.py`, `promo_fin2.out`): `StepPrepEnabled` false, `CamInspectEnabled` true, `InspectZoomOn` false, `StepEdgeOn` false, geri dönüş DB'leri V2.24 (`PSD_SHM224_JogRevBwdO/FwdM…`, SHM226 **yok**), `SwingLiftMargin` 10,5 → 6, `InspectRadius` 22 → 12; DA kaydedildi, `dirty_after []`. Grafik/işlev değişiklikleri (T3a/d/e/g, I3/I4, SHM226_Shift düğümleri) build sırasında kaydedilmişti (`build_b*.out`). Ev alt seviyesi: etiketler + r 12 küreler kaydedildi.
Temiz yeniden açılış doğrulaması (`verify_prod226`, taze editör, PIE yok): **ALL_OK** (`verify_fin.out` → `pub/verify_prod226_final.txt`): ABP DB referansları V2.24, StepEdgeOn/InspectZoomOn false, InspectTag GR_Inspect, SwingLiftMargin 6, Snapshot SHM226_Shift kopyası + 2 dünya-uzayı ModifyBone, BodyTargets SwingShift, CameraV21 etiket+sınır sözleşmesi ve çarpma telemetrisi, SHM226 DB sızıntısı yok, 4 maske etiket + 1 küre; PIE yok, kirli paket yok.

## 7. Geçersiz / yeniden başlatılan koşular
MEM_RESTART (editör 38–40 GB, otomatik yeniden başlatma, koşular tekrarlandı): 05:01, 05:27, 05:46, 06:12, 06:31, 07:04, 07:22, 08:08, 08:28. INVALID_STATE: yok. Durdurulan zincirler: b7/b8/b9, m2/m3 (bayat DONE işareti tuzağı — tek sıralı ana zincire geçildi); BF_ABORT ×3 (funcs build pin-tipi hataları, bileşen kirli → `revert_comp_quit`), SHIFT_ABORT, PROBES_ABORT (API; düzeltildi). Çift editör tuzağı: 1 REFUSED. Kaza sonrası tüm koşular ayrı etiketle tekrarlandı. Final zincir kazası: `req/probes_r12.py` önceki işten kalan `V226_PROBE_REMOVE=True` builtins değerini devraldı → küreler yeniden silindi (had 0); `promote226.py` kararı eski ad `V225_PROMO` altında okuyordu → `decision {}` ve kayıt yok (PROMO_FAILED). Düzeltme aynı editörde: `req/probes_r12b.py` (tüm bayraklar açık yazılı: remove false, r 12, save) → 4 maskeye küre eklendi, `promo_fin2.py` (`V225_PROMO`/`V225_PROMO_SAVE`) → `saved true, dirty_after []`; zincir `run_fin2.sh` ile temiz doğrulamadan itibaren sürdürüldü.

## 8. Performans
Kaynaktan sorgu sayısı (her kare, her şey açık): 14 line trace + 1 sphere trace (inceleme) + `StepEdgeOn` ile 4 ek line trace. Oyun/anim süresi ve bellek ölçülmedi (sabit dt perf değildir) → **NOT_TESTED**. Editör bellek tavanı (39–40 GB'de otomatik yeniden başlatma) harness düzenlemesi, oyun maliyeti değil.

## 9. Medya (tam kare, gerçek hız, kesilmemiş)
Tam kare (viewport 64'ün katına daraltıldı, kırpma yok), sabit 30 FPS oyun zamanı = gerçek hız, kesilmemiş; tümü **üretim modu** (aday override yok). `vid/*.gif` gerçek hız, `*_realtime.avi` gerçek zaman, `*_slow3x.avi` 1/3 hız (yan görünüşler). Kameralar: S sabit yan, D sabit çapraz, G oyun kamerası.
| Dosya | İçerik |
|---|---|
| jogrev_SW_prod_side / _game | tempolu S→W, üretim (V2.24 pivot; V2.26'da değişmedi) — yan / oyun kamerası |
| jogrev_WS_ph3_prod_side | W→S→W geç istek evresi, yan |
| jogrev_WS_ph0_prod_diag | W→S→W, çapraz |
| inspect_masks_game / _diag | atölye: yürü → maskeye bak → incele → bakışı kaydır; gerçek R05 maskeleri, oyun kamerası / çapraz |
| inspect_two_masks_game | iki yakın maske arasında bakış geçişi (172°) |
| terrain_step28_walk_side / _game | 28 cm basamak çıkış + iniş, yan / oyun kamerası |
| route_house_forest_game | map_r2 gerçek rota, oyun kamerası |
`img/`: inspect_masks_before_f30 / on_f90 / diag_f90, inspect_two_masks_f150, step28_walk_side_f60 / f72 (her iki ayak platform üstünde), jogrev_SW_prod_side_f60, jogrev_WS_prod_diag_f70, route_map_r2_game_f200. Aday geri dönüş (rv32) videosu yayınlanmadı (üretime alınmadı; sayısal kanıt §3).

## 10. Açık liste
- Geri dönüş: FootPlacement'ın pinlenmiş fren ayağını 23 cm geri itmesi (kilit dışı mekanizma; `SHM_FootPlaceOff` klip kapısı adayı), bölüm sonu → DB anahtarı → çıkış sıçraması (bölümü klip uzunluğuna bağla ya da klibi bölüm sonunda döngü evresiyle bitir), ad_ph0'da klip seçilmemesi, yavaş-çekim koşu aileleri (dokunulmadı), tasarımın yumuşak iniş yaklaşımı.
- İnceleme: baş/boyun açısı ölçümü (eksen kuralı), paketli test, DOF (yok), dar geçit, el teması, ses.
- Arazi: koşu yüksek basamakta ilk ayak askı/batma; 28 cm basamakta basıştan önce 0,3 s askı; gerçek rotada basamak yok (kanıt yalnız yuvarlanmış zemin); iniş kaydırmasının gerçek basamaklarda farklı açılardan genellenmesi.
- Araç: v2_check pin tipi yakalamıyor; funcs build balon tuzağı (taze editör).

## 11. Geri alma
- Üretim anahtarları: `promote226.py` ile `V226_PROMO={...False}` + `V226_PROMO_EXTRA` eski değerler (SwingLiftMargin 10.5, InspectRadius 22, StepEdgeMin 6) → DA kaydı.
- İkili: `checkpoint/pre_v226/` kopyaları (DA, bileşen, profil, ABP, oyuncu BP'leri, harita) editör kapalıyken geri kopyalanır.
- Ev alt seviyesi: `req/probes_remove.py` (küreler), `untag_masks226.py` (etiketler) veya `checkpoint/L_GR_CurrentHouseContent_after_tag.umap`.
- Aday içerik (SHM226 klipler/DB'ler) üretimde referanssız; silinebilir.
