# SPHIRUS V2.40: Sürekli İnsan Hareketi ve Fiziksel Toparlanma — rapor

Temel: V2.39 (Bridge `395eace`). Tarih: 2026-10-30/31.

**Kısa sonuç:**
- **Üretim değişmedi.** `SHM239_Own`, `SHM240_ExtOn` ve `SHM240_HeadOn` 0'da kaldı; temiz açılışta `VERIFY240 ALL_OK`.
- **Neler çözüldü (aday `tkh`):**
  - 120 FPS devralma kaymasının ilk nedeni bulundu ve düzeltildi.
  - Devralma her FPS kipinde deterministik giriyor.
  - Devralma sonrası yanal duruş gitti.
  - Üçüncü istek, plan teslimiyle (yield) yön sapması yapmadan çalışıyor.
  - Gerçek duvar teması algılanıyor ve plan duruyor.
  - Baş, elle bakış yokken hareket yönüne dönüyor.
- **Neden aday üretime alınmadı:**
  - `j39_rl`'de yeniden başlamadaki yanal başlangıç/duruş kararsız.
  - İtme sonrası duruş kayması 26–42 cm.
  - Uzun zincirlerde (`ad_jog`, `mt_jog`) ayrışma var.
  - Duvar yanıtı, durma DB'siyle bile 120 FPS'de bin atlıyor.
  - Görsel ve oyun hissi kabulü yapılmadı.

## Sorular

### 1. 120 FPS kaymanın ilk gerçek nedeni

**Neden: kategori E → A** (FPS/zamanlama, ardından yanlış seçim). İçerik eksikliği değildi, blend de değildi.
- V2.39'un takeover kilidi, devralma klibinin **harmanlanmış** hedef eğrisi (`SHM239_Tgt`) 20'yi geçince kapanıyordu.
- Zorlanmış aramayı kare sayısıyla tekrarlıyordu.
- 120 FPS'de bir kare 0.05 s'lik blend'in yalnız ~%17'sini ilerletiyor. Eğri 4 → 14 okundu, kilit kapanmadı, her 2. karede yeni bir zorlanmış arama yapıldı.
- Seçim 0.35 s boyunca kaynaktan kaynağa atladı: `P21_K1 → P10_K1 → P22_K4 → P00_K4 …`. Ayaklar bu atlamalarla sürüklendi.
- **Karşı örnek:** 30 FPS'de tek kare 20'yi geçmeye yetti; kilit tek zorlamadan sonra kapandı (`v239reg_j39_rw_tk` 0 cm).
- **Kötü örnek:** `v239x120_j39_rw_tk`, 116 cm.

**Düzeltme** (yeni bias / bekleme / süre yaması yok):
- Anahtar, motion matching'in **gerçek seçimine** (`CurrentSelectedDatabase`) bakar.
- Tek zorlanmış arama yapılır; yeniden deneme yalnız zamanla (0.05 s).

Sonra ikinci neden çıktı: **yanlış giriş zamanı (B).** MM, takeover'ı bir tarafın bütün klipleri arasından seçiyordu. Koşu pozları birbirine benzediği için başka kaynak ya da başka faz girildi (P10 kesmesi → `P00_K4`, 10 cm).

### 2. Takeover hangi animasyonu ve hangi gerçek fiziksel durumu kullanıyor?

**Animasyon:** V2.39'un `SHM239_Tk_{R|L}_Pnn_K{k}_{Back|Opp}` klipleri. Bunlar oynayan kesmenin ön kısmının birebir kopyası; yeni plan K. temasta başlıyor.

**Seçim:** artık aramayla değil, durumdan yapılan bir eşlemeyle:
- oynayan kesmenin kaynak bin'i (yeni sabit eğri `SHM240_Src`);
- kilitli hedef (Back / Opp);
- sıradaki planlı temas (`SHM239_Step`).

Bu üçü tek bir giriş veritabanını gösterir (`PSD_SHM240_E00..E95`). İçindeki her K klibi yalnız [t_(K-1), t_K + 0.05] penceresinde girilebilir. İstek anında tek bir klip kapsar ve o kare oynayan kesmenin karesiyle aynıdır.

**Fiziksel durum:**
- Gerçek kapsül hızı (V2.28 klip-hız sözleşmesi, kesmenin kendi hızı).
- Gerçek destek ayağı ve faz (planlı temas saati).
- Gerçek yön.

**Sınır:** Bu durum kesme bozulmadan oynadığı sürece doğru. Dış bir etki varsa (itme, duvar) devralma değil dış etki çekilmesi (yield) devreye girer.

**Sonuç (120 FPS):**

| Senaryo | V2.39 | V2.40 |
|---|---|---|
| `rw` | 116 cm | 7.6 cm |
| `cc90` | 112 cm | 9.6 cm |

Diğer bütün devralma senaryoları 8–12 cm.

### 3. İkinci ve üçüncü istek

**İkinci istek** (sağ 90 → fren ortasında sol/ileri), aday:

| Senaryo | 30 FPS | 120 | 60 | 20 | Gerçek zaman |
|---|---|---|---|---|---|
| `rw` | 10 | 7.6 | 6.7 | 8.3 | 8.2 |
| `lr` | 6.3 | 12.2 | 10.1 | 7.0 | 9.7 |
| `cc90` | 7.0 | 9.6 | 8.8 | 13.4 | 7.2 |

Üretimde aynı senaryolar: `lr` 60 FPS'de 45.3 (RevTurn), `cc90` 120 FPS'de 21.5 (RevTurn).

**Devralma sonrası yanal duruş:** düzeldi. Plan bittiği karede son yön gövde çerçevesine devrediliyor (`install240_exit2`, V2.34 keşif durumu). `lr` 36 → 7 cm.

**Üçüncü istek** (ileri > sağ 90 > fren ortasında sol > destek kurulurken ileri):
- Bir devralma klibi tekrar devralınamaz; kaynak içerik yok, istenirse bu içerik sınırıdır.
- Bunun yerine `install240_yield`: devralma klibi momentum düşükken (< 80 cm/s) ve niyet hedeften 35°'den fazla saparken normal başlangıç / itme yönlendirmesine teslim eder.
- `j40_rlw`'de istek anında hız 35 cm/s idi. Yield sonrası 0.37 s'de yön ileri döndü; −90'lık sapma yok.
- Kayma (cm):

| | 30 FPS | 120 | 60 | Gerçek zaman | 20 |
|---|---|---|---|---|---|
| Aday | 7.9 | 8.1 | 9.5 | 6.7 | 23.8 |
| Üretim | 7.1 | 44.9 | 14.4 | 26.3 | 14.8 |

**Mimari sınır:** üçüncü istek yüksek hızda gelirse (≥ 80 cm/s) plan biter, sonra normal sistem yönlendirir.

**Görsel kusur:** yan çekimde 6.3–6.8 s'de beden neredeyse duruyor ve kısa adımlar atıyor (140°'lik toplam yön değişiminin gerçek frenidir). Bu kısım bekleme gibi okunabilir.

### 4. RevTurn yanlış yönlendirmesi kapandı mı?

- **Adayda kapandı:** `cc90`, `lr`, `lrw` hiçbir FPS'de RevTurn'e gitmedi. Üretimde 120 / 60 FPS'de RevTurn hâlâ var (`lr` 38.8 / 45.3, `cc90` 21.5).
- **`mtf_jog` kapanmadı:** iki varyantta da `SHM216_RevTurn_R_Lfoot`, 50.7 / 48.9 cm.

### 5. Canlı denge kararı gerçekten farklı destek seçiyor mu?

**Kısmen.** Ayrı bir CoM/XCoM denetleyicisi kurulmadı; `SHM239_Bal` hâlâ telemetri. Karar, oyun durumundan okunan dört kuralla farklı **hareket** seçiyor:

| Karar | Koşul | Hareket |
|---|---|---|
| Plan devam | Niyet hedefe yakın | Planın kendi temas dizisi |
| Normal yön değişimi (devralma) | Niyet > 35° sapma, sıradaki planlı temas | Yeni plan o temasta, mevcut hız ve destekten |
| Plan teslimi (üçüncü istek) | Takeover klibi, \|v\| < 80, niyet > 35° sapma | Normal başlangıç / itme yeni yönde |
| Dış etki / toparlanma adımı | Artık \|ölçülen − komut\| > 80 cm/s | Plan geri çekilir, pushRaw toparlanma aileleri (6 / 3) `SHM_Rec_FL_Rfoot` gibi adımlar seçer |
| Engel (duvar) | Ext ve \|v\| < 60 | Tek zorlanmış arama ile plan biter (durma / ayakta) |

Sağdan itmede gerçekten farklı bir destek seçiliyor: geniş yakalama adımı, `SHM_Rec_FL_Rfoot`. Bu adım karakterin tavrına göre fazla geniş görünüyor.

### 6. Toparlanma adımının tetik koşulu

Plan sırasında artık `SHM239_Resid` > 80 cm/s olunca `SHM239_Ext` 0.6 s kilitlenir. Artık şöyle hesaplanır:
- Komut hızı = son karenin klip hızı × aktör yönü.
- Ölçülen hız = CMC'nin hareket sonrası hızı.

Ölçülen değerler:
- Planlı hareket ≤ 20 cm/s.
- 300 cm/s itme: 282 cm/s.
- Duvar: 98 cm/s.

Ext varken plan sahibi, klip-hız sözleşmesi ve kesme yolu çekilir. Mevcut pushRaw toparlanması (aile 6 → 3) adımı seçer.

Ayrı düğme: `SHM240_ExtOn` bu çekilmeyi devralmadan bağımsız açar.

### 7. İtme sonrası kayma ve duruş

**FAIL / çözülmedi.**
- İtme gerçekten taşınıyor: vy −191 cm/s, toparlanma klipleri seçiliyor.
- Ama sonraki duruş / koşu kayıyor (`j39_push_plan`):

| | 30 FPS | 120 | 60 | 20 | Gerçek zaman |
|---|---|---|---|---|---|
| `tk` | 21.6 | 30.5 | — | — | — |
| `ext` | 8.8 | 30.2 | — | — | — |
| `tkh` | 26.5 | — | 33.0 | 30.7 | 41.7 |

- 120 FPS'de sahip `A_LS_Jog_Right_Stop` yanal duruşu: toparlanmadan sonra yön ile hareket ayrışıyor.
- Üretimin "0 / 10 cm"si yanıltıcı: üretimde itme tamamen siliniyor, hiçbir tepki yok.

### 8. Planlı ve dış hız değişimi üretimde ayrılıyor mu?

- **Üretimde hayır:** V2.38 davranışı; plan sırasında gerçek itme siliniyor.
- **Adayda (`tk`, `ext`) evet:** artık ölçüsü (≤ 20 vs 282 / 98 cm/s).
- **Gerçek çarpışma yapıldı:** `j40_wall`, `Wall40` kutusu yeni hareket yönünü kesiyor. Temas 6.3 s'de, y = 105.
- Duvar sonuçları (kayma cm):

| Varyant | 30 FPS | 120 FPS | Gözlem |
|---|---|---|---|
| Üretim | 35.2 | — | GR plan hızını duvara yazmaya devam ediyor (artık 298 cm/s). Beden 0.4 s yerinde koşuyor ve 6.70–6.77 s'de duvarın içine kısmen giriyor (kare kaydında görüldü). |
| `wst` (Ext + durma DB'sine tek zorlanmış arama) | 25.7 | 22.6 | Temas karesinde durma pozuna geçiyor; yerinde koşu ve duvara girme yok. 120 FPS'de durma bin'leri karede bir atlıyor (P01 → P14 → P02; V2.37 bin atlama tuzağı). |
| `tkh` (ayakta DB) | 43.1 | 35.8 | Reddedildi. |
| `wof` (yalnız Ext çekilmesi) | 24.2 | 35.8 | Klip 0.7 s yerinde oynuyor. |

- Duvara tepki içeriği yok (el desteği, geri sekme); bu bir içerik sınırı.

### 9. Baş, göğüs ve pelvis

**İlk ayrışan katman:** satıcının aim offset'i (`Get_AOValue` = Delta(ControlRotation, RootTransform), lerp `Disable_AO`).
- Oyuncu bakmadığı hâlde kamera yönüne doğru dönüyor: başı, göğsü **ve pelvisi**.
- Örnek: sert sağ 90'dan sonra baş − hareket yönü = −80°, kamera dönene kadar.
- Kaynak / MM pozu ve V2.25 / V2.38 LookAt hareket yönüne bakıyor.

**Öncelik kuralı** (`install240_head`, `SHM240_HeadOn`):
- **Elle bakış:** `TW_LastLookTime` son 0.8–1.4 s içindeyse AO sahiptir.
- **Fiziksel hareket:** hareket var ve elle bakış yoksa AO, FInterpTo ile (kare hızından bağımsız) kapanır.
- **Ayakta:** değişmez.

**İlk sürüm (plan sırasında da sönme):**
- Baş sapması `c90r` 47 → 2°, `c90l` 59 → 2°, `lr` 54 → 10°.
- Ama AO'nun pelvis payı kalkınca yere basmış top tek karede 3 cm kaydı (`c90r` 0 → 10 cm).

**İkinci sürüm** (sönme plan eğrisinden sonra, × (1 − W)):
- Ayak kayması yok (`c90r_tkh` 0.0).
- Ama plan sırasında baş üretimdeki gibi kalıyor; kazanç plan sonrasıyla sınırlı.
- +1.8 s'de pelvis / göğüs / baş − hız (derece):

| Senaryo | Üretim | Aday |
|---|---|---|
| `lr` | −14 / −26 / −13 | −5 / −1 / −3 |
| `cc90` | 37 / 30 / 79 | 7 / −7 / 13 |

- Oyun kamerası kare kaydı (`head_after_cut_*`, 7.0–7.7 s):
  - üretimde göğüs ve baş kamera yönüne döndü;
  - adayda hareket yönünde kaldı.

**Durum: PARTIAL, üretime alınmadı.** Kalıcı çözüm, AO'nun yalnız boyun/baş payını ayırmak (bone başına blend). Bu yapılmadı.

### 10. mtf_jog, jlean ve diğer regresyonlar (30 FPS, o → tkh, cm)

- **Değişmeyen:**
  - `mtf_jog` 50.7 → 48.9 (RevTurn);
  - `jlean` 11.9 → 12.0;
  - `j36_sside` 22.2 → 22.2;
  - `e29_chain` 6.4 → 6.4;
  - `j38_c135r` (gerçek 135) 9.7 → 9.8;
  - `j35_rev` (180) 9.3 → 9.3.
- **İyileşen:**
  - `jstart` 83.0 → 57.4 (hâlâ kötü);
  - `c29_combo` 15.4 → 8.8;
  - `j39_rl_l` 31.7 → 7.1;
  - `cam32_j90` 11.2 → 5.6;
  - `j36_stopr` 5.5 → 0.
- **Kötüleşen:**
  - `j39_rl` 27.3 → 78.9: yeniden başlamada `A_LS_Jog_Left_Start`. Aynı build'de odak koşusunda 26.6; kararsız.
  - `ad_jog` 10.3 → 26.3 (`LoadRev`, 16.6 s'de).
  - `mt_jog` 14.4 → 23.6 (12.6 s'de bir kesme).
  - `w38_c90r` 0 → 5.6.
  - Uzun zincirlerde adayın seçimleri üretimden ayrışıyor; neden bu oturumda izole edilemedi.
- **Sprint 90:** yalnız plan, yapılmadı. Aynı mimari (kaynak eğrisi + kaynak/hedef başına giriş DB'si + yield) bir sprint kesme ailesine uygulanabilir. Önce 550 cm/s'den iki fren temasının bütçesi ölçülmeli; aile ancak devralma üretime alınınca üretilmeli.
- **Arazi:** NOT_TESTED.

### 11. Hangi hareket hangi FPS'de doğrulandı?

Teknik ölçüm (kayma/pop); görsel değil:

| | 30 sabit | 60 | 120 | 20 | Gerçek zaman |
|---|---|---|---|---|---|
| İkinci istek (`rw`, `lr`, `cc90`) | ✓ | ✓ | ✓ | ✓ | ✓ |
| Üçüncü istek (`rlw`, `lrw`) | ✓ | ✓ | ✓ | `rlw` 23.8 zayıf | ✓ |
| `rl` (yeniden başlama) | ✗ | ✗ | ✗ | = | ✗ |
| İtme | ✗ (duruş kayması) | ✗ | ✗ | ✗ | ✗ |
| Duvar | kısmi (`wst`) | — | kısmi (`wst`) | — | — |
| Baş | ✓ (kısmi) | — | ✓ | — | — |

- "Aynı zamanlı komut": bütün A/B'ler aynı girdi zamanlarıyla yapıldı.
- "Aynı fiziksel durum": `rl_e` / `rl` / `rl_l` (kesmenin farklı fazlarında istek) var. Duruma göre tetiklenen ayrı bir test kurulmadı: **NOT_TESTED**.
- 120 FPS'deki üst beden "pop" değerleri (307 m/s²): tek karelik ~2 mm konum sıçraması. İvme ölçütü 120 FPS'de gürültüyü büyütüyor; poz kesintisi değil.

### 12. Üretim, deneysel, reddedilen

- **Üretime alınan:** yok. Yalnız etkisiz kurulumlar:
  - 96 giriş DB'si;
  - 48 klipte `SHM240_Src` eğrisi;
  - düğmeler 0.
- **Deneysel (aday):**
  - `tkh`: devralma + yield + çıkış devri + baş;
  - `ext`: bağımsız dış etki çekilmesi;
  - `hd`: yalnız baş;
  - `wst`: duvarda durma DB'si (bayrakla `SHM240_BlkDB`).
- **Reddedilen:**
  - Duvarda ayakta-DB'sine zorlanmış arama (43 cm).
  - Plan sırasında da sönen baş (yere basmış ayak 3 cm tek kare).
  - V2.39'un kare sayısı ve harmanlanmış eğri kilidi.

### 13. `SHM239_Own` açık mı? Neden?

**Kapalı (0).** Koşulların hepsi sağlanmadı:
- `j39_rl` yeniden başlamada kararsız (26.6 / 78.9 aynı build).
- İtme sonrası duruş 26–42 cm.
- `ad_jog` / `mt_jog` uzun zincir ayrışması.
- Duvar yanıtı içerik sınırlı.
- Görsel / oyun hissi kabulü yapılmadı.

Bağımsız alt düzeltmelerin (`ext`, `hd`) her biri tam regresyonla ayrıca doğrulanmadı; bu yüzden ayrı ayrı da üretime alınmadı.

### 14. Yeni klip, PIE koşusu, editör açılışı

- Yeni animasyon klibi: **0**.
- Yeni veritabanı: 96 (`PSD_SHM240_E*`).
- 48 kesme klibine bir eğri eklendi.
- PIE koşusu: **322** V2.40 etiketli koşu (A/B, regresyon, FPS kipleri, 23 çekim), artı ~27 ısınma koşusu.
- Editör yeniden açılışı: **27**.
- Editör yazma işleri: 14 manifestli kurulum. 2'si derleme hatasıyla kaydetmeden geri döndü (thread-safe ve pin adı).

## Medya (`vid/`)

- Normal hız, kesilmemiş. 30 FPS sabit adım oyun zamanı = gerçek hız. Gif + `_realtime.avi`.
- Aynı girdi, önce/sonra:

| Dosya | Kamera |
|---|---|
| `third_request_v238/v240_side` | Sabit yan |
| `third_request_v240_diag` | Sabit çapraz (dörtte üç) |
| `third_request_v238/v240_game` | Oyun kamerası |
| `right_then_left`, `left_then_right`, `consecutive_cuts`, `shove_during_cut` | Sabit yan |
| `wall_during_cut_v238` / `_v240_stand` / `_v240_stop` | Sabit yan, duvarın karşı tarafından |
| `head_after_cut_v238` / `v240_game` | Oyun kamerası |

- **İzleme durumu:** videoları gerçek zamanlı OYNATIP İZLEMEDİM. Kontrol ettiğim, çekim karelerinden zaman damgalı kare kâğıtlarıydı (`sheets/`). Yukarıdaki görsel kusurlar bu karelerde görülenlerdir:
  - Üretimde duvara girme ve yerinde koşu.
  - `wst`'de temas karesinde durma.
  - Üçüncü istekte 6.3–6.8 s'de neredeyse duruş.
  - İtmede geniş yakalama adımı.
  - Oyun kamerasında üretimde göğüs ve başın kameraya dönmesi.
- Hareketin akıcılığı ve "doğallık" kararı kullanıcının izlemesine kalıyor.

## Kod ve doğrulama
- `code/`: bütün kurulum betikleri, istek sarmalayıcıları, zincirler (`run240_a..j.sh`), harness (`v212_run_v240.sh`), `tables240.py`, `verify240.py`, `sheet240.ps1`, `media240.sh`.
- `data/`: `chain.out`, tablolar, `verify240.out`.
- `manifests/`: yalnız JSON, ikili yedek yok.
- `skills/`: güncellenen beceriler (`sphirus-safe-unreal-iteration`, `sphirus-balance-recovery` V2.40 bölümleri).
