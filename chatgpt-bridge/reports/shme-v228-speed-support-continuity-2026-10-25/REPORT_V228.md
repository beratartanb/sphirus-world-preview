# SPHIRUS — SHME V2.28: hız, destek ve animasyon sürekliliği; inceleme kimliği ve bakış; arazi ilk basış (2026-10-25)

Taban: V2.26 üretimi + V2.27 kurulu-kapalı adayları (bridge `a6682a0`). Başlangıç durumu taze editörde doğrulandı (V2.27 `verify_fin227` ALL_OK: üretim geri dönüşleri V2.24 pivot DB'lerinde, SHM226 klipleri aday, `SHM227_RevHold`/`FPOff` 0, inceleme/arazi onarımları üretimde, `InspectZoomOn`/`StepEdgeOn`/`StepPrep` kapalı). Kontrol noktası `Saved/Codex/SHME_V228_20261025/checkpoint/pre_v228/` (ABP'ler, bileşen, iki DA, 66 V226 varlık, maske alt seviyesi) + `checkpoint/tools/` (DSL kaynakları, harness). Her koşu etkin durum kaydıyla (`_state.json`), "üretim" = kaydedilmiş durum bayraksız.

## 0. Üç teslime kısa cevap
1. **Tempolu fren–yeniden itiş:** giriş hızı, destek evresi, animasyon saati ve kapsül hareketi artık aynı eylemi anlatıyor: klip pozdayken kapsül hızı klibin tasarım hızına bağlı (|fark| ≤ 5 cm/s, integral ~1 cm, 30/60/120 FPS), basılı fren ayağı kayması ph0 49,7 → 13,0 (60 FPS 32 → 5,8), sw_ph2 31 → 9 (120 FPS 52 → 15), ovl120 23–65 → 8–15. Dönüş/çıkış 1–3 cm, iptaller: ikinci istek karşı aile klibine aynı karede (dbl 35 → 14–20, duran kalkış yok), bırakma fren sonuna tutulup duruş. **Üretimde** (bkz. §4).
2. **İnceleme:** gerçek maske kadrajı korundu (zoom yok); "aynı hedef" artık aktör kimliği (iki yakın maske ayrışıyor, 29 cm komşu aynı sayılmıyor), hedefler arası geçiş mandalı düşürmeden 0,25 s dwell sonra yumuşak, odak maske merkezi (sonda kayması giderildi). Baş/boyun ölçüldü: oturmuş bakış hatası 4–8°, baş–gövde yaw ≤ 10°, 0,6–0,9 s'de 10° içine; LookAt ekseni zaten doğru (+Y). **Üretimde**.
3. **Arazi:** koşu 28 cm basamakta ilk ayağın yüzeye girmesi (−6,3 cm) kaldırma tavanı 36 ile giderildi (−1,1…−1,7), ilk ayak kenardan 3,5 → 16 cm içeri ve topuk boşluktan çıktı (gerçek-kenar kapılı iniş uzatması 18; eğimde yanlış tetikleme 278 → 6 kare); yürüyüş kazanımları korundu (R 9 → 15,6 cm içeri). Askı (0,4 s) ve ikinci adımın 116/85 cm ileride basması açık. **Üretimde**.

## 1. HAREKET — tek problemli girişte eşleme (ph3, 60/120 FPS)
### 1.1 Anlar ve giriş durumu (`moments228.py`, `speedclock228.py`)
Aynı olay için ayrı zamanlar (ph3, S isteği t≈5,24 + girdi gecikmesi):

| FPS | istek | fren başı | bileşen bölümü | seçim (klip, ct) | poza katılım %50 | fren ayağı basış | sıfır geçişi | itiş>50 | döngüye devir |
|---|---|---|---|---|---|---|---|---|---|
| 20 | 5,350 | 5,350 | 5,350 | 5,350 P4 ct 0,067 | 5,45 | 5,35 R | 5,75 | 6,05 | 7,00 |
| 30 | 5,333 | 5,333 | 5,333 | 5,333 P21 ct 0,067 | 5,43 | 5,43 R | 5,77 | 6,10 | 6,97 |
| 60 | 5,283 | 5,283 | 5,283 | 5,283 P4 ct 0,067 | 5,40 | 5,28 R | 5,78 | 6,08 | 6,90 |
| 120 | 5,258 | 5,258 | 5,258 | 5,258 P4 ct 0,067 | 5,375 | 5,28 R | 5,78 | 6,08 | 7,23 |

Giriş durumu (seçim karesi): kapsül hızı 245–298 cm/s (+x), istenen hız −245…−284 (tam ters), gövde yönü 0°, destek evresi FPS'e göre farklı (sağ ayak 19–35 cm önde; 30'da temas öncesi, 60/120'de salınımın daha erken evresi) → MM 30'da P21, 20/60/120'de P4 kutusunu seçiyor. **İstek anındaki hız ile klibin başladığı andaki hız zaten aynı kare** (seçim = istek karesi); fark, klibin **ct 0,067'den** girmesi: klip saati tasarım tablosunda 2 kare ilerideyken kapsül yalnız 1 kare (FPS'e göre 8–50 ms) frenlemiş.

### 1.2 Kapsül–klip saat uyumsuzluğu (giriş zamanından yeniden başlatılmış karşılaştırma)
`speedclock228`: kapsülün eski yön boyunca gerçek hızı − klibin seçili zamandaki tasarım hızı, kare kare; integrali = tasarıma sabit basılı ayağın dünya kayması.

| FPS | klip saati kapsülün ne kadar önünde | fren boyunca sabit hız farkı | integral (0,7 s) | ölçülen fren ayağı sürüklenmesi (V2.27 rh) |
|---|---|---|---|---|
| 20 | −0,008 s | ≈0 | −0,3 cm | 11 |
| 30 | +0,035 s | +25 cm/s | +9…11 cm | 21 |
| 60 | +0,056 s | +50…60 cm/s | +24 cm | 35 |
| 120 | +0,065 s | +75 cm/s | +22 cm (0,33 s'de) | 36 |

GR sürtünme freni (kesme kapağı 450 → 636 cm/s²) tasarım eğimiyle aynı; fark sabit bir saat kayması. V2.27'nin "giriş hızı FPS'e göre 136/72" bulgusu araç hatasıydı (`capterm` konum farkını her FPS'te 30 ile çarpıyordu); kapsül hız eğrisi FPS'ten bağımsız (üretim ve aday aynı), FPS'e bağlı olan girdi gecikmesi → ayak evresi → kutu.

### 1.3 Seçilen yaklaşım ve gerekçe (B-lite: tasarlanmış eylem kendi hız yolunu yürütür, CMC çarpışma + oyuncu iptali korunur)
A (kapsül ana kaynak, içerik gerçek girişe göre) için giriş-saatine duyarlı klip üretimi gerekirdi; MM'in girişi (ct 0,067–0,10) yörünge kanalı (−0,05/0/0,35/0,7/1,0 s) ile bağlıdır ve her FPS'te farklı kalır. B-lite: klipler tasarlanmış kapsül yolunu zaten kök izi olarak taşıyor (ABP root motion modu "montajlar" → hiç tüketilmemiş). Uygulama:
- 64 klibe `SHM226_V` (tasarım hızı, karakter ileri ekseni, cm/s) + `SHM226_W` (=1, karışım ağırlığı tanığı: V/W her ağırlıkta tam) eğrileri (`add_speedcurve228.py`).
- ABP `SHM_Snapshot`: `SHM228_DesV` = V/W (W>0,1); `SHM228_Cmd` = DesV + LeadFrames·(DesV−PrevDesV) (hareket güncellemesi anim güncellemesinden önce çalışır → bir kare ileri bakış); `SHM228_On` = düğme & klip pozda & bölüm canlı & ¬Dead → bileşen sözleşmesi `ClipSpeed`/`ClipSpeedOn` (yeni bileşen değişkenleri).
- `BP_GR_Player.GR_Impl_CP_PhysicalRedirect` sonunda (bu karenin bütün hız yazımlarından sonra): `Velocity = ActorForward × (ClipSpeed − MaxAccel·dt·dot(forward, DesiredDir))`, o karelerde `GroundFriction` 0 → CMC kendi ivmesini uygular ve sonuç tam ClipSpeed olur; **ivme vektörü korunur** (SHME niyet sinyali). Düğme `GR228_ClipSpeed` (profil/DA).
- Zaman ve yer değiştirmeyi kim yönetiyor: klip pozdayken **klip saati** (tasarım tablosu) kapsül hızını yönetir, CMC taşır/çarpışır, root motion tüketilmez (çift yer değiştirme yok); klip biter/bölüm biter/yeni niyet → aynı kare normal CMC.

İlk aday (CMC ivmesini sıfırlayan sürüm) niyet sinyalini öldürdü (HasIntent düştü, bölüm "kayıp", yürüyüş-durma; 58 cm) — düzeltme: ivme korunur, hız yazımında önceden telafi edilir.

### 1.4 Sonuç — klip saatini kapsül izliyor mu? (`clipspeed228`)
`clipspeed228` (kapsülün eski yön hızı − klibin tasarım hızı, kare kare): ilk telafi karesinden sonra |fark| ≤ 5 cm/s, integral ~1 cm — 30 FPS (ph3: 1,3 cm), 60 FPS (ph3: 1,1 cm), 120 FPS (sw_ph2: −0,1 cm). Klip pozdayken kapsül klibin saatini izliyor; FPS'e bağlı giriş ofseti artık kaymaya dönüşmüyor. İlk sürümde (CMC ivmesi sıfırlanmış) niyet sinyali düştü ve karakter durma klibine düştü (ph0 58 cm) — ölçülüp düzeltildi (ivme korunur, hız yazımında önceden telafi edilir).

### 1.5 Kayma tabloları (sabit 30 ve FPS)
En kötü basılı ayak kayması cm (yükseklik-ölçütü | temas-başlangıçlı; `plant225`/`plant227`). rhC = tutma + klip-bağlı kapsül (FP açık). rhCR = + bırakma tutuşu + iptal yeniden rotası (son sürüm, §1.7).

| Sabit 30 | Üretim V2.26 | V2.27 rh (e) | **V2.28 rhC** | V2.28 rhCF (FP klipte kapalı) | V2.28 rhC0 (ileri bakış yok) |
|---|---|---|---|---|---|
| ph0 | 49,7 \| 49,7 | 18,1 \| 17,8 | **13,0 \| 13,0** | 18,0 | — |
| ph3 | 16,6 \| 16,6 | 21,5 \| 14,6 | **12,1 \| 7,7** | 21,9 \| 9,5 | 16,5 \| 8,5 |
| sw_ph0 | 16,7 \| 10,9 | 9,4 \| 9,4 | **5,8 \| 5,8** | — | — |
| sw_ph2 | 26,1–31,2 | 21,5 \| 9,5 | **9,2 \| 9,2** | — | — |
| rel (bırak–bas) | 30,4 \| 30,4 | 21,3 \| 13,2 | 36,6 \| 37,7 | — | — |
| dbl (ikinci ters) | 35,5 \| 5,2 | 21,7 \| 17,7 | 26,9 \| 26,5 | — | — |

| FPS | Senaryo | Üretim | V2.27 rh (e) | **V2.28 rhC** |
|---|---|---|---|---|
| 20 | ph0 | 49,6 | 9,6 | **15,0** |
| 20 | ph3 | 16,8 \| 13,3 | 11,5 \| 13,1 | 18,5 \| 20,1 |
| 20 | sw_ph2 | 25,3 | 11,1 | **7,4** |
| 20 | ovl120 | 65,4 \| 24,4 | 11,1 \| 10,4 | **7,6** |
| 20 | dbl | 32,5 \| 7,2 | 16,3 \| 15,9 | 22,2 |
| 60 | ph0 | 32,4 | 32,2 \| 16,7 | **5,8** |
| 60 | ph3 | 15,4 \| 15,1 | 34,8 | 18,5 |
| 60 | sw_ph2 | 21,6 | 21,4 \| 14,9 | **11,7** |
| 60 | ovl120 | 23,4 \| 21,1 | 22,6 | **8,8** |
| 60 | dbl | 31,2 \| 27,8 | 30,7 \| 21,3 | 32,0 \| 32,4 |
| 120 | ph0 | 30,5 | 25,5 \| 17,0 | **13,0 \| 12,2** |
| 120 | ph3 | 26,7 \| 17,7 | 36,2 | **13,3** |
| 120 | sw_ph2 | 51,6 | 37,5 \| 12,5 | 30,7 (B_F P6 içerik) → **15,0** (P6 yeniden üretildi) |
| 120 | ovl120 | 35,2 \| 24,7 | 29,5 | **14,5 \| 14,3** |

Gerçek zaman (sabit adım yok, ısınmalı): sw_ph2 34,7 (üretim 17,6; P6 kutusu, yeniden üretim öncesi), dbl 23,8 (15,3), ph3 13,5 \| 14,1. Soğuk ilk koşu (ph0) GEÇERSİZ: Shift dokunuşu başlangıç gecikmesinde kaçtı, karakter yürüdü — harness olayı (V2.27'deki gibi).

Okuma: 30/60/120 FPS'te ph0, sw_ph0, sw_ph2, ovl120 üretimden belirgin iyi; ph3 60'ta +3, 20'de +2…7 cm (üretim zaten iyi); rel/dbl iptal yollarına bağlı (§1.7).

### 1.6 FootPlacement
"Hep açık / hep kapalı" kurulmadı. Karşılaştırma (sabit 30): yalnız tutma (rhH, V2.27) ph3 17,2, ph0 15,1; tutma + FP klipte kapalı (rhCF) ph3 21,9, ph0 18,0; **tutma + klip-bağlı kapsül + FP açık (rhC) ph3 12,1, ph0 13,0** → kapsül klibe bağlandığında FootPlacement artık kapsül–klip farkını örtmek zorunda değil ve açık kalması daha iyi; o evrede FP yalnız yerel zemin uyarlaması yapıyor. B_F P26/P29 çıkış sıçraması (V2.27'de FP kapalı varyantta 21 cm) FP açıkken 1,8 cm. Destek ayağını klip evresinde kapsül saati + FP birlikte yönetiyor; çift düzeltme yok (root motion tüketilmiyor, hız yalnız GR katmanında yazılıyor).

### 1.7 Çıkış, iptaller, kol/baş/gövde
- **Döngüye çıkış** (`exitjump227`, rhC 30): klipler 1,43–1,60 s oynar (bitime 0,29–0,30 s), çıkış penceresi sıçraması ph0 1,8/2,7, ph3 1,9/1,8, sw_ph0 2,7/1,6, sw_ph2 1,8/2,0 cm; 60/120 FPS'te 0,5–1,4 cm. V2.27'nin B_F P26/P29 21 cm çıkışı FP açık + bağlı kapsülle 1,8.
- **Kol/baş/gövde** (`arms228`): devir penceresinde el kare-sıçraması 11 cm (üretim pivot 14–17), baş 1–2 cm, göğüs–leğen karşı dönüş −9…+13° korunuyor, sol el salınım ters dönüşü 0 — ikinci hazırlık yok.
- **İptaller** (rhCR): üç sürüm ölçüldü. (1) ilk sürüm: ikinci istekte yeniden rota aramaya girmedi (arama kısıtı), klip-bağlı kapsül W basılıyken 3 s geriye koştu — **kontrol kilidi**, ölçülüp düzeltildi; (2) kısıt rota karesinde kalkar + güçlü interrupt + niyete-karşı güvenlik → güvenlik fren fazında ateşledi (frenlerken tasarım hızı niyete zıttır) ve tutmayı/slave'i 2–3 kare düşürüp bırakmada mandalladı; (3) güvenlik yalnız push fazında. Son sürüm (rhCR, sabit 30 / 60 / 120): **dbl 16,7 \| 11,0 / 19,9 \| 12,3 / 13,9** (üretim 35,5 \| 5,2 / 31,2 \| 27,8 / —): ikinci W isteğinde F_B klibi aynı karede karşı aile (B_F) klibinin itiş fazına rotalanıyor (ct 0,33), kapsül tasarım hızını izliyor (−26 → 0 → +ileri), döngüye çıkış 1,0–1,8 cm, **duran kalkış yok**. Bırakma (rel): klip fren sonuna (0,37–0,40 s, sıfır geçişi) kadar tutulup gövde tasarımla duruyor; yeniden basışta vendor `Jog_Bwd_Start_AAMS` / idle kalkışı 32–34 cm kayıyor (üretim 30,4) — kalkış klibi sınıfı, açık. Normal senaryolar rhCR ile değişmedi (ph0 13,0, ph3 12,1, sw_ph2 9,2, sw_ph0 5,8).
- **Arama kısıtı**: yalnız klip pozdayken; yeniden rota karesinde kalkıyor; engel/yeni niyet/bırakma yolları çalışıyor.

## 2. İNCELEME
**Değişiklik:** "aynı hedef" kararı mesafe (InspectJump 45) yerine **aktör kimliği sürekliliği** (son karedeki nesne adı eşitliği); yeni aday mandalı düşürmez, `InspectSwitchOn` 0,25 s dwell sonra yumuşak geçiş; mandal yokken odak noktasına anında geçiş; odak = **aktör konumu** (maske pivotu = merkez; sonda küresi actor bounds merkezini 15 cm odaya kaydırıyordu: x 47,7–48,6 → 33,0). Düğmeler `InspectIdOn`/`InspectFocusMode` (aday ins5). Zoom açılmadı (B kadrajı korundu: kamera–kapsül 148–150 cm, FOV 62).

**İki yakın maske (ins_ws2):** üretim mesafe kuralı Silent'tan 3 kare sonra 29 cm sağdaki Cerulean'ı "aynı hedef" saydı ve mandalı 3,93'te aldı; kimlik kuralı dwell'i sıfırlayıp Cerulean'ı 4,07'de ayrı hedef olarak aldı; 5,63'te bakış Silent'a dönünce mandal düşmeden 0,27 s dwell sonra nokta 0,3 s'de kaydı (üretimde anlık). Hareket eden hedef: kimlik aktör adıyla sürer, nokta her kare odağa lerp (6/s) — statik maskelerde test edildi, hareketli nesne sahnesi harness'ta yok (açık).

**Baş/boyun (gaze228, kemik eksenlerinden ileri):** ileri eksen +Y (nötr karede yüze kosinüs 0,997; baş/boyun/omurga/leğen aynı). ins_ws2: InspectOn>0,5 boyunca bakış hatası ort. 5,8–6,1°, min 0,2–0,3°, baş–gövde yaw −8…+10°, baş–göğüs −15…+20°, pitch −12…+7°, mandaldan 0,57–0,93 s sonra 10° içinde. ins_ws (yürüyüş dönüşü sonrası): ort. 10,6–11,2 (geçişler), oturunca 4–8°. LookAt düğümleri (spine_03/neck_01/head, alfa 0,18/0,35/0,55, kelepçe 25/30/35°) zaten yerel +Y'yi hedefliyor — ilk "aşağı eğiliyor" okuması yanlıştı, düğüm değiştirilmedi. Kamera bakışı sürmüyor (CamOffset payı yalnız yan bileşen); mandal hız/dönüş hızıyla düşüyor. QueryOnly sondalar yalnız Visibility sorgusuna cevap veriyor (V2.26 sözleşmesi).

## 3. ARAZİ
**Ölçüm tabanı** (`step228`: basış yüksekliği koşunun düz zemindeki basılı top yüksekliğine göre), 28 cm basamak. Yürüyüş üretim: ilk sağ ayak 9 cm içeri, topuk 7 cm boşlukta, z −1,7, basıştan önce 0,47 s yüzeyin 4 cm üstünde askı; sol 85 cm içeri. Koşu üretim: ilk sol 3,5 cm içeri, topuk 12,5 cm boşlukta, **z −6,3 (yüzeye girme)**, kaldırma 24,8 = tavan 25'te doyma; sonraki sağ 116 cm içeri. 15 cm "kenar" rampa üstüyle aynı seviyede (sorun değil).

| 28 cm basamak | Üretim | tl36 (tavan 36) | te4 (gerçek-kenar, uzat 12) | **te4b (gerçek-kenar, uzat 18)** |
|---|---|---|---|---|
| koşu, ilk ayak: kenardan içeri / topuk / z hatası | 3,5 / −12,5 / −6,3 | 3,5 / −12,5 / **−1,7** | 9,3 / −6,7 / −1,7 | **16,0 / +0,0 / −1,1** |
| yürüyüş, ilk ayak | 9,1 / −6,9 / −1,7 | 11,1 / −4,9 / +1,7 | 13,4 / −2,6 / +1,9 | **15,6 / −0,4 / +2,2** |
| yürüyüş askısı | 0,47 s | 0,47 | 0,37 | 0,40 |
| sonraki ayak | 116 / 85 cm içeri | aynı | aynı | aynı |

**Gerçek-kenar kapısı** (yanlış tetikleme): map_r1 te4 7 kare (maks 8 cm), te4b 6 kare — V2.26 kaydırma adayı 278 kare; hill8_jog 0; bump_jog 27–32 (13 cm gerçek kutu kenarı); step2 70 (gerçek basamaklar). Pop'lar üretimle aynı (map_r1 10/57). Tavan 36: map_r1 t≈20 s dik yokuş sprintinde (kapsül 1 s'de 135 cm yükseliyor, zemin önde 35–40 cm) kaldırma 33–36 (eskiden 25'te doyuyordu), pop/sıçrama yok. Yürüyüş 0,4 s askı ve koşuda ikinci adımın 116 cm ileride basması açık (adım zamanı/yaklaşma hızı bu turda değiştirilmedi).

## 4. Doğrulama, üretime alma, kanıt
**Üretime alma (`promote228.py`, taze editör 03:30):** gruplar hareket + iptal + arazi + gerçek-kenar + inceleme: 32 kutulu DB'ler (`PSD_SHM226_JogRevBwd/Fwd`, 10 kutu yeniden üretilmiş) üretim rotasında (`SHM224_DB_JR*`), ABP `SHM227_RevHold` 1, `SHM227_FPOff` 0, `SHM228_ClipSpeed` 1, `SHM228_RelHold` 1, `SHM228_CancelOn` 1; DA_GR `GR228_ClipSpeed` 1; DA_SHM `SwingLiftMax` 36, `StepEdgeOn` true, `StepEdgeShift` 18, `StepEdgeShort` 12, `InspectIdOn` 1, `InspectFocusMode` 1, `InspectSwitchOn` 0,25; `InspectZoomOn`/`StepPrep` kapalı. Geri alma: `promote228.py` `{'rollback': True}` (kontrol noktası `checkpoint/pre_v228/`).

**Temiz yeniden açılış doğrulaması (`verify_fin228`, taze editör 05:40):** ABP düğmeleri, GR düğmesi, DA değerleri, 4 DB referansı = PSD_SHM226 çifti, 64 klipte 3 eğri, V2.26 üretim doğrulaması (DB-ref dışı kalemler) → `ALL_OK: true`. (V2.26 doğrulayıcısının 32 kutulu DB'ler için beklentisi yoktu; o sekiz anahtar burada açıkça kontrol ediliyor — ilk iki deneme bu yüzden "VERIFY_FAILED" verdi, düzeltilip tekrarlandı.)

**Üretim-modu kanıt (taze editör, bayraksız, 20 senaryo, `data/tables228_fin.txt`, `state/`):**

| Senaryo (sabit 30) | Önce (V2.26 üretimi, v227fin) | **Sonra (v228fin)** |
|---|---|---|
| sw_ph0 | 16,7 \| 10,9 | **5,8 \| 5,8** |
| sw_ph2 | 26,1 \| 26,1 | **9,2 \| 9,2** |
| ph0 | 49,7 \| 49,7 | **13,0 \| 13,0** |
| ph3 | 16,6 \| 16,6 | **12,1 \| 7,7** |
| rel | 30,4 \| 30,4 | 33,9 \| 35,0 (kalkış klibi, açık) |
| dbl | 35,5 \| 5,2 | **16,7 \| 11,0** (duran kalkış yok) |
| ad_ph0 / m180w (pivot ailesi, değişmedi) | 26,8 / — | 26,8 / — |

Klip saati: ph0 integral 2,0 cm (maks fark 19 cm/s), ph3 1,3, sw_ph2 −1,4. Çıkışlar: ph0 1,8/2,7, ph3 2,0/1,8, sw_ph2 1,8/2,0, sw_ph0 2,7/1,8, dbl 1,8/1,8 (karşı aile klibinden döngüye), rel 7,3 (kalkış). Kol/baş/gövde: el devir sıçraması 10,7–12,2, baş 1,1–1,8, gövde karşı dönüşü korundu. Pop'lar: j23_m180 292/292, r_cutrev 57/57, ins_ws 43/43, ter_drop_walk 260/260, ter_step2 190/190, map_r2 56/56 aynı; m180w 291 → 305 (klip içi, pivot ailesi; aynı aşama). Hiçbir koşu `INVALID_STATE` değil.

**Arazi (üretim):** 28 cm koşu ilk ayak 16,0 cm içeri, topuk +0,0, z −1,3 (önce 3,5 / −12,5 / −6,3); yürüyüş R 15,6 / −0,4 / +2,2 (önce 9,1 / −6,9 / −1,7). Kaydırma kareleri: map_r1 6, map_r2 0, map_r2 gerçek zaman 14, bump_jog 40, step2 48 (gerçek kenarlar). Pop'lar değişmedi.

**İnceleme (üretim):** ins_ws2 bakış hatası ort. 6,0° (min 0,3), baş–gövde yaw −8…+9°, 10° içine 0,93 s; ins_ws ort. 10,7 (geçişler); kamera–kapsül 148–150 cm, FOV 62 (zoom yok).

**Gerçek zaman (sabit adım yok), soğuk başlatma ilk koşu `j24_ph0` (bu kez klip seçildi):** ph0 7,3 (klip F_B_P15, çıkış temiz), sw_ph2 30,5 \| 6,5 (ilk kare yüksek-ölçüt), rel 24,0 \| 30,1, ins_ws2 ort. 5,9°, map_r2 21,4 kare/s (7 pop, en kötü 46; önce 56). rt dbl koşusu SHM226 klibi seçmedi (pivot yoluna gitti, 18,4) — gerçek-zaman giriş gecikmesi çeşitliliği (açık listede).

**Yakalamalar (`vid/`, üretim, sabit 30 = gerçek hız, tam kare, kesintisiz):** tempolu S>W (yan + oyun kamerası), W>S>W erken/geç evre (yan), çift geri dönüş (yan), bırakma (yan), 28 cm basamak koşu/yürüyüş (yan), iki yakın maske incelemesi (oyun kamerası + yan). Yavaş çekim yok.

## 5. Açık liste
- İkinci adım: 28 cm basamakta ilk ayak düzeldi, ama sonraki ayak 116 (koşu) / 85 cm (yürüyüş) içeri basıyor; yürüyüşte basış öncesi 0,4 s askı — adım zamanı/yaklaşma hızı/pelvis devri bu turda ele alınmadı.
- Hareketli inceleme hedefi ve örtülme senaryoları harness'ta yok (kimlik kuralı tasarımca destekliyor, ölçülmedi).
- rel (bırak–bas): fren sonunda duruş + vendor `Start_AAMS` kalkışı 15–37 cm kayma (kalkış klibinin basılı ayaktan başlatılması gerekir).
- ph3 20/60 FPS +2…7 cm (üretim 15–17 zaten iyi); dbl temas-başlangıçlı 12–13 (üretim 5).
- Yeniden rotalı B_F klibi bitiminde aile kapısı (iptal 3 ile OR) — ara sürümde (m2) yeniden rotalı B_F klibi bitiminde bileşen ailesi 6 (kalkış) olduğu için tutma yolu atlanıp kurtarma DB'si seçildi (tek kare 29 cm); son sürümde (r2/r60) çıkışlar döngüye 1,0–1,8 cm, ama aile kapısı tutuşla OR'lanamadı (tüketici bulunamadı) — tekrar edebilir, izlenmeli.
- Soğuk başlatma gerçek-zaman kanıtı (Shift kaçması) ve P6 benzeri kutuların gerçek-zaman tekrarı nihai zincirde.
- Kol/baş katmanı: ölçüm var (arms228), yeniden tasarım gerekmedi; dar geçiş, el teması, ses ve diğer hareket aileleri önceki açık listede.

## 6. Test aracı olayları
- İlk GR kurulumu `CalculateMaxAcceleration`'ı sıfırladı → CMC ivme vektörü = SHME niyet sinyali söndü (HasIntent false, bölüm "kayıp", yürüyüş-durma; ph0 58 cm). Düzeltme: ivme korunur, hız yazımında bu karenin ivmesi önceden telafi edilir.
- `qa_graph` sınıf pini yol dizesi ister (yüklenmiş nesne str() çöp → alıcı çıkışı ActorComponent kaldı, bağlantı reddedildi).
- Yarım kalan GR yamasını atmak için profil SINIF paketini yeniden yükledim → `BP_PBI_Player.GR_Profile` None (V2.5 tuzağının tekrarı); kurucu kaydetmeyi reddetti, editör kaydedilmeden kapatıldı.
- `GetWorldDeltaSeconds` qa_graph NATIVE'de yok → bileşen `DeltaTime`. InRange tip adı yerelleşmiş (`InRange(Float)`). W tanığı eşiği 0,3 sözleşmeyi 3 kare geciktirdi → 0,1.
- İptal 1: `SelectObject` tipli DB pinine bağlanamadı → exec dalları. İptal 2: AnimGraph'ta NOT/AND bağlantısı reddedildi → bayrak snapshot'ta (`SHM228_ThrOK`); yeniden rota çağrısı tarayıcısı Condition pini olmayan düğümde patladı → korumalı; çağrı seçimi iki eşleşme → yalnız dalın then ucu. İptal 3: niyete-karşı güvenlik fren fazında ateşledi (tasarım hızı frenlerken niyete zıt) → yalnız push fazında; idempotent kontrol pin hatası → işaret değişkeni.
- LookAt ekseni: `unreal.Axis` FAxis yapısı (Vector eksen) — düğüm zaten +Y, kurulum iptal.
- Soğuk gerçek-zaman ph0: Shift dokunuşu başlangıçta kaçtı → yürüyüş (geçersiz koşu). MEM_RESTART 39–43 GB (×4); bir kez "editor did not quit" (43 GB) → elle kapatıldı.
- Çevrimdışı "klip çerçevesinde sürükleme" taraması yanlış yöne götürdü (basılı ayak klip çerçevesinde zorunlu olarak −D(t) hareket eder); tasarım doğrulaması dünya çerçevesinde (sgn·D + y) yapıldı: 10 kutuda fren ayağı tau0'da zemindeyken 24–46 cm yeniden konumlanıyordu.

## 7. Dosyalar
`code/` (kurucular, ölçerler, zincirler, terfi/doğrulama), `data/` (tablolar, zincir günlüğü, sondalar), `state/`, `vid/`, `CHANGES_V228.md`.
