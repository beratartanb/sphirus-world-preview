# SPHIRUS — SHME V2.33: doğal hareket yönetimi, sinematik tepki + otomatik arkadan takibe dönüş, doğrulanabilir çalışma becerileri (2026-10-27)

Taban: V2.32 üretimi (Bridge d3f3105). Blueprint-only UE 5.8, git yok: geri dönüş = manifest yedekleri (sha1 doğrulamalı) + editör.
Sayılar sabit adımlı editörde aynı girdiyle ölçüldü; aksi yazılmadıkça 30 FPS. Ölçüt: `contact231` basılı-top kayması / sürüklenmesi (cm).
Teknik PASS, görsel / oyun hissi kabulü değildir. Kayıtlar sizin değerlendirmeniz içindir. Konsol (PS) donanımında test yapılmadı.

**Üretime alınanlar (2 grup, temiz açılışta VERIFY233 ALL_OK):**
1. `standback` — gerçek duruştan geri kalkış için karaktere özel başlangıç klibi + kapı.
2. `camrec` — hareket yönüne arkadan otomatik dönüş, girdi çerçevesi kilidi ve gamepad / fare profilleri. Yalnız tempolu ve depar hızında (≥ 170 cm/s); yürüyüş hariç, nedeni 7–10'da.

**Aday kalan (üretimde değil):** `sprintcalm` — daha dik, daha sakin depar üst bedeni.

## 0. Kısa yanıtlar

1. **Hangi bozuk geçişler gerçekten kapandı?**
   - Gerçek duruştan tempolu geri kalkış kapandı. j30_slow / jback / d_back'te başlangıç klibindeki kayma 35–44 → 0 cm.
   - Bu sonuç 30 (2 tekrar), 60, 120, 20 FPS ve gerçek zamanda aynı.
   - Kapanmayanlar: bırak–yeniden bas, yan / arka çapraz geçiş, 60 FPS düşük hızlı ters dönüş, geri sonrası ileri duruşun kapanış adımı (bölüm 4–5, 14).
2. **Hangi yeni doğal hareketler üretimde?**
   - Stand-back başlangıcı. 0. kare üretim idle pozunun aynısı. Kök ölçülen kapsül hız profiline bağlı. Basılı ayaklar dünyada sabit yerleştirildi. Salınım ayağı önce kalkıyor, sonra ilerliyor.
   - Kendi veritabanı ve kapısı var; ortak başlangıç DB'sine eklenmedi.
   - Brifteki üç "ek doğallık" örneği üretilmedi (sert fren sonrası yerleşme adımı, karşı yöne destek düzenleme, efor sonrası yerleşme). Açık.
3. **Deparın atletik tavrı gerçekten değişti mi?**
   - Üretimde hayır. Aday üretildi ve oyunda ölçüldü: gövde eğimi 28.4 → 17.8°, kayma regresyonu yok (medyan 14.3 → 11.6 cm).
   - Oyunda kol salınımı (58 → 56 cm) ve baş yanal salınımı pratikte değişmedi. Görsel farkı yalnızca daha dik gövde.
   - Bu yüzden üretime almadım. Yan yana kayıt: `vid/sprint_attitude_*`.
4. **Kamera kritik hareketi doğru anda çaprazdan gösteriyor mu?**
   - Kısmen. V2.32 fren / dönüş yörüngesi (13–14°) korunuyor.
   - Yeni arkaya dönüş gövde yeni yöne oturduktan sonra başlıyor. Bu sırada gövde çaprazdan görünüyor; depar sert sağda 3/4 görüş süresi 0.40 s → 1.00 s (gamepad), 2.40 s (fare).
   - Olaylara (fren başı, destek devri) bağlı tepki zarfı ve gerçek 180° dönüşte taraf seçimi bu turda yapılmadı.
5. **Sonra sağ analog olmadan arkadan takibe dönüyor mu?**
   - Evet, tempolu ve depar hızında.
   - Gamepad: tempolu sol 1.37 s, depar sert sağ 1.40 s yerleşme (hata < 20°); en çok 73–79°/s; kritik sönümlü, aşma yok.
   - Fare / klavye (ölçek 0.35, daha müdahalesiz): tempolu sol 4.5 s, en çok 30–35°/s. Depar sert sağda 6 s pencere içinde hata 61° → 25°'ye indi, 20° altına inmedi.
   - Geri harekette, duruşta bakarken, incelemede ve dar koridorda dönmüyor (ölçülen kontrol değişimi 0°).
   - Yürüyüşte üretimde kapalı (bölüm 7–10).
6. **Manuel bakış ve hareket yönü korunuyor mu?**
   - Evet. Oyuncu bakışı geldiği kare otomatik dönüşü durduruyor; görülen açı korunuyor, eski merkeze sıçrama yok. Bakış bitip 1.6 s geçince yumuşakça devam ediyor.
   - Basılı tutulan girdinin dünya yönü görüş dönerken kilitli. Kilitsiz deneme 110° spiral çiziyordu.
   - Yeni bilinçli girdide çerçeve ~0.1 s'de görülen görüşe devrediliyor.
   - Görüş dönerken hareket yönü değişmiyor; değişen hız. Kamera arkaya geçince yan-göreli koşu (417 cm/s) ileri-göreli depara (490 cm/s) dönüyor. Bu mevcut bakış güdümlü hareket kuralından geliyor; görsel kabul sizde.
7. **Arazi bağlantısı hangi koşullarda tamamlandı?** Bu turda üzerinde çalışılmadı. Mevcut arazi senaryoları yalnızca regresyon için koşuldu (bölüm 11).
8. **Hangi eski sorunlar açık kaldı?** Bölüm 14.
9. **Güvenlik kapıları hangi hatayı engelledi?** Bölüm 2. Gerçek yakalamalar:
   - ikinci editör açılması (2 kez),
   - manifest dışı bağımlı BP kirlenmesi,
   - PIE içinde yazma (V2.32'deki hata, test T5),
   - manifest dışı varlık kaydı,
   - eski kuyruk işi.
   - Bir hata kapıdan kaçtı: başarısız DSL kurulumu boş kamera fonksiyonunu kaydetti. Onarıldı ve artık kurulum betiği hata verip kaydı durduruyor.
10. **Test / yeniden başlatma süreleri?** Bölüm 12.

## 1. Başlangıç, durum, koruma

- **Temizlik (brif öncesi, kullanıcı isteği).** 40 947 dosya / 33.96 GB silindi; C: 79 → 110 GB boş.
  - Korunanlar: atıf yapılan her dosya, son iki kayıt, panolar / referans / kaynak.
  - Ayrıntı: `Saved/Codex/_Cleanup_20261027/README.md` + `manifest_apply.json`.
- **Taban kontrolü.** V2.32 durum dosyaları ve yayın d3f3105 ile eşleşti. Eski V2.32 brifi değil, V2.33 brifi kullanıldı.
- **A_CT_Ref_Walk_Stop_F_L/R.** Kaydedilmiş hiçbir checkpoint'te eski kopyası yok; yalnız türetilmiş SRC_Sample varyantları var.
  - Mevcut dosyalar yedeklendi (manifest `actref_current`).
  - V2.32 öncesi sürüme tek yol OneDrive sürüm geçmişi; bu sizin tarafınızda.
- **SHM232_IS_* kopyaları.** 9 klip desteklenen yöntemle (`AnimNotifyState_PoseSearchExcludeFromDatabase`, iz `SHME_V233_Excluded`) aktif aramadan çıkarıldı. Manifest `is_exclude`.
  - Python'da DB girdisi silme API'si yok: `RemoveAnimationAssetAt` yalnız C++'ta.
- **Değiştirilmeyenler:** anatomi, yüz, kıyafet, harita. Yeni lokomotion / kamera framework'ü kurulmadı.
  - Kamera dönüşü mevcut V2.21 kamera fonksiyonuna eklendi; girdi kilidi mevcut hareket düğümüne bağlandı.

## 2. Yazma ve test güvenliği (kodda, runner'da uygulanıyor)

Runner: `code/runner_v233_gated.py` (fark: `code/runner_v233.diff`). Kayıt: `data/gate233.log`.

| Kapı | Ne yapıyor | Kanıt |
|---|---|---|
| G1 eski kuyruk | Runner başlamadan önce kuyruktaki eski işleri `stale/` içine taşır | test `zz_stale_test` hiç çalışmadı |
| G2 PIE | PIE varken yazma / DB / PIE işi reddedilir | `REFUSED_PIE` (T5 = V2.32 `bfx_write2` hatası) |
| G3 tek sahip | İş başlığındaki `SHME_OWNER` kilitle (`lock233.sh`) eşleşmeli | `REFUSED_OWNER owner=other lock=v233` |
| G4 manifest | Yazma işi doğrulanmış yedekli manifest ister (`manifest233.py`). İş sırasında `unreal` modülü bir vekil; listede olmayan paketin save / delete / rename / duplicate çağrısı reddedilir | `REFUSED_NO_MANIFEST`, `REFUSED_SAVE outside manifest` |
| G5 denetim | Yazma sonrası Content disk taraması + yeni kirli paketler | `GUARD_WRITTEN` (vekil atlatılarak yapılan kayıt yakalandı), `GUARD_DIRTY` |

**Ek kapılar**
- `lib233 relaunch`: eski editör kirli olduğu için kapanmayı reddederse ikinci editör açılmaz (`RELAUNCH_FAILED`).
- `qa_pie ERROR_FLOOD`: 200'den fazla BP çalışma hatasında koşu durur, ilk hata saklanır.
- `build_funcs`: herhangi bir DSL hatası `BUILD_FUNCS_FAILED` ile işi düşürür. Zincirler `FAIL DSL` arar; kayıttan önce düğüm sayımı yapılır.
- Derleme sonrası LastHitBy köprüsü otomatik yamalanıyor ve doğrulanıyor (`lhb_linked 0`).

**Oturumdaki gerçek yakalamalar (`data/chain.out`)**
1. `REFUSED_MANIFEST`: zincirin ikinci işi, ilk işin meşru yazmasını değişiklik saydı. Manifest durum dosyası eklendi.
2. Kirli bileşen yüzünden kapanmayı reddeden editörün üstüne ikinci editör açılacaktı. `RELAUNCH_FAILED` ile durdu (2 kez: camG, f30).
3. `GUARD_DIRTY BP_PBI_Player`: `build_comp_vars` bağımlı oyuncu BP'lerini kirletti; manifest dışıydı. Manifest `camA2` oluşturuldu.
4. **Kaçan hata.** Var olmayan bir DSL düğümü (`GetLastMovementInputVector`) kurulumu bozdu ama iş "OK" döndü ve boş `SHM_UpdateCameraV21` kaydedildi.
   - Yeniden kurulumla onarıldı (1430 düğüm).
   - Artık kurulum betiği hata verip kaydı durduruyor ve kayıttan önce düğüm sayımı yapılıyor. Skill'de "başarısız örnek" olarak yazılı.

**Değişen paketler:** yalnız manifestlerdeki paketler (`manifests/*.json`, sha1'li yedek listesi). Yedekler projede, `checkpoint/manifests/` altında; yayımlanmadı.

## 3. Üç proje becerisi

| Skill | Ana dosya | İçerik |
|---|---|---|
| `sphirus-natural-motion` | 49 satır | niyet → hız / destek → plan → kaynak → entegrasyon → görünen beden; gerçek başarısız örnekler; kabul testi; araç yolları; geri dönüş |
| `sphirus-camera-direction` | 47 satır | bakış önceliği → temel takip → geçici tepki → arkaya dönüş → çarpışma / girdi denetimi; girdi çerçevesi kuralı; başarısız örnekler; kabul testi |
| `sphirus-safe-unreal-iteration` | 61 satır | manifest + yedek, tek sahip, PIE / eski iş reddi, yazma sonrası denetim, hata seli durdurma, aşamalı test, kanıt sürümü |

- Kanonik dosyalar `.agents/skills/` altında.
- `sync_claude_skills.py` çalıştırıldı: 77 skill, 0 hata.
- `CLAUDE.md`'ye yalnız kritik kural + yönlendirme satırı eklendi.
- Kapılar skill metninde değil, runner yolunda çalışıyor. Engellenen gerçek hata bölüm 2'de.
- Kopyalar: `skills/`.

## 4–5. Hareket

### Zincir 1: gerçek duruş → geri kalkış → düşük hızda ileri → duruş (senaryo j30_slow)

**Neden.** AAMS kökenli tempolu geri başlangıç klibi:
- idle duruşundan ayak başına 16 cm uzakta ve 5 cm alçakta başlıyor;
- ayaklar 58–68° dönük;
- kapsül hemen hızlanırken kök 0.25 s duruyor;
- bunlara bir karelik geç seçilen yoğun başlangıç ekleniyor.

**Çözüm (üretimde).**
- İçerik: `gen233_standback2.py`. Dayandığı veri: kapsül profili + yeniden yerleştirilen stance'ler.
- Yönlendirme: ABP `SHM_Snapshot` içinde `SHM233_StandBack` koşulu:
  - tempolu yürüyüş;
  - düz geri niyet (dot < −0.95);
  - gerçekten duruyor (hız < 15, iki ayak temasta, poz idle DB'de);
  - 1.2 s kilit.
- Giriş, `Update_MotionMatching` başında zorlanıyor.

**Başlangıç klibi içindeki kayma (r1)**

| FPS | j30_slow önce → sonra | jback | d_back |
|---|---|---|---|
| 30 | 38.1 → 0 | 38.3 → 0 | 38.3 → 0 |
| 60 | 38.8 → 0 | 34.9 → 0 | 34.7 → 0 |
| 120 | 38.8 → 0 | 36.7 → 0 | 36.7 → 0 |
| 20 | 38.0 → 0 | 38.0 → 0 | 38.0 → 0 |
| gerçek zaman | 37.7 → 0 | 43.9 → 0 | 41.1 → 0 |

**Karşı durumlar (final, 30 FPS).** k_jogback, jstart, j30_rel_3200/3450 ve wstart stand-back'i almıyor; değerleri değişmedi.
- İlk kapı çok genişti: 135° çapraz ve bırak–yeniden bas da bu yolu seçiyordu. Daraltıldı (C1C).

**Zincirin geri kalanı (açık).**
- Geri sonrası ileri duruşta kapanış adımı: `SHM_A_CP2_Jog_Fwd_Stop` 22–28 cm.
- Düşük hızlı ters dönüş: `SHM226_JogRev_B_F_P23` 60 FPS'de 17 cm.
- Bu yüzden j30_slow koşu genelinde en kötü değer 38 → 22 cm. Sıfır değil.

**60 / 120 FPS jback geç sürüklenmesi (teşhis, `data/ep_d60.txt`).**
- Aday Q ile jback'te t ≈ 10.5–12.5 s'de yeni bir sürüklenme çıktı: 60 FPS'de 62.9 cm, 120 FPS'de 54.7 cm (`A_CT_Jog_BwdRight` → `A_LS_Jog_Left_Stop`).
- Nedeni: Q'nun eski kamera ayarı (MaxErr 150, MinSpeed 60). Bu ayar geri-çapraz harekette görüşü döndürüyordu; yol ayrışıyor ve farklı bir duruş seçiliyordu.
- Üretim ayarıyla (110 / 170) 60 FPS'de yeniden koşuldu:
  - jback en kötü 8.6 / 10.1 cm (2 tekrar), geç sürüklenme yok;
  - yalnız beden (body233) 7.1 / 8.6 cm;
  - V2.32 38.8 cm (başlangıç klibi).
- j30_slow 60 FPS: üretim ve yalnız beden aynı (27.7 cm, ileri duruş `SHM_A_CP2_Jog_Fwd_Stop`). Bu açık kalem kamerayla ilgili değil.

### Zincir 2: tempolu / depar → sert dönüş → ikinci istek → yakalama / yerleşme → devam

- Regresyon olarak koşuldu: e29_chain 11.2, cam32_chain, cam33_sturn 10.0, cam33_jturnj 38.8 cm.
- Yeni yakalama / yerleşme adımı üretilmedi. Açık.
- jturnj'deki 34 → 39 cm ve beden adayındaki 83.6 cm değeri sınıflandırıcının parçalamasından geliyor:
  - top yolları kare kare karşılaştırıldı, fark ≤ 7 cm;
  - seçilen klipler aynı.
- Sınıflandırıcı sonucu güzel göstermek için değiştirilmedi.

### Depar tavrı adayı (`sprintcalm`, `gen233_sprintcalm.py`)

- Üretim sprint döngülerinin kopyaları üzerinde: gövde eğimi −12° (spine_01'de; boyun karşı yönde telafi ediyor).
- Gövde / baş / köprücük / kol sapmaları 0.6 / 0.5 / 0.7 / 0.8 ile ölçeklendi. Bacak, pelvis ve kök dokunulmadı.

**Klip ölçümü:** eğim 24.1 → 12.9°, baş yanal 13.6 → 7.1 cm, el salınımı 60 → 37 cm.

**Oyun içi ölçüm**
- Gövde 28.4 → 17.8°.
- Kol 58 → 56 cm, baş yanal değişmedi: runtime üst beden katmanları baskın.
- Kayma medyanı 14.3 → 11.6 cm.

**Görsel karar.** Yan karelerde (`sheets/sprint_side_zoom.png`) aday belirgin biçimde daha dik. Kol ve baş hareketi neredeyse aynı. Atletik / sakin farkı yarım kaldığı için üretime alınmadı.

### Açık hareket kalemleri

- Yan / arka çapraz geçiş (5C).
- Bırak–yeniden bas (j30_rel_3200 30 FPS 51.5 cm; başlangıç klibi içinde).
- 60 FPS düşük hızlı ters dönüş.
- Yüklü ters dönüşte çift iniş bu turda yeniden ele alınmadı; V2.32 durumu korunuyor.

Ayak kaldırarak kayma gizleme yapılmadı.

## 7–10. Kamera: temel takip / geçici tepki / otomatik arkaya dönüş / girdi çerçevesi

### Mimari (tek koordinatör = mevcut `SHM_UpdateCameraV21`)

- **Temel takip ve geçici tepki:** V2.32 yörünge (orbit) katmanı, değişmedi.
- **Yeni arkaya dönüş (`CamRec*`):** kritik sönümlü yay (frekans 2.2, en çok 110°/s).
- **Arkaya dönüşün koşulları:**
  - kararlı seyahat;
  - fren / ters dönüş / yön değişimi yok;
  - son oyuncu bakışından 1.6 s geçmiş;
  - inceleme yok;
  - hata 6° ile 110° arasında (arka çapraz = 135°, bu yüzden dönmez);
  - hız ≥ 170.
- **Uygulama:** sonuç `CamRecDelta` olarak `BP_GR_Player.GR_UpdateSHMSignals` içinde kontrol yaw'una ekleniyor.
- **Öz-engelleme düzeltmesi:** bakış algılama kendi dönüşünü çıkarıyor. Önceden kendi dönüşünü oyuncu bakışı sanıp duruyordu.
- **Girdi kilidi:** hareket girdisi `Select(GR233_MoveLatchOn, GR233_MoveLatchYaw, kontrol yaw)` ile seçiliyor. Basılı tuşun dünya yönü sabit; yeni bilinçli girdide 0.06 s karışımla yeni görüşe devrediliyor.
- **Cihaz profili:** InputDeviceSubsystem son kullanılan donanımı veriyor. Gamepad'de ölçek 1.0, fare / klavyede 0.35.
- **Ayrı anahtarlar:** takip ve tepki DA'da ayrı (`CamRecEnabled` / `CamOrbitEnabled`).

### Kanıt (final koşuları, `data/rec_fin.txt`; hata = |kamera yaw − seyahat yaw|)

| Senaryo | V2.32 (pre233) | V2.33 fare / klavye | V2.33 gamepad |
|---|---|---|---|
| tempolu → sol | 77 → 108°, dönüş yok | 78 → 18°, 4.5 s, ≤ 30°/s | 78 → 15°, 1.37 s, ≤ 73°/s |
| depar → sert sağ | 61 → 114°, dönüş yok | 61 → 25° (6 s içinde), ≤ 35°/s | 62 → 9°, 1.40 s, ≤ 79°/s |
| geri hareket | — | dönmez (kontrol 0°) | — |
| duruşta bakış / inceleme / koridor | — | dönmez (0°) | — |

**FPS.** Gamepad süresi 30 / 60 / 120 / 20 / gerçek zamanda aynı (1.1–1.5 s); FPS'e bağlı değil (tablolar `tables_f*.txt`, kamera sütunu).

**3/4 görüş süresi (depar sert sağ).** V2.32: 0.40 s. Gamepad: 1.00 s. Fare: 2.40 s. Dönüş sonrasında kamera dışarı savrulmuyor; tek yönlü, aşmasız yerleşiyor.

**Bakış önceliği**
- Kanıt aday koşusundan (k2, eşik 60): bakış geldiği kare durdu, görülen açı korundu, sonra 1.83 s'de yerleşti.
- Üretimde yürüyüş hariç olduğu için `look` senaryosu (yürüyüş) üretimde dönüş tetiklemiyor. Yayımlanan `walk_look_no_recentre` kaydı bu yüzden yalnız "dönüş yok, bakış aynen" gösteriyor.

**Duvar.** Duvar mesafesi değişmedi (78 cm). Çarpışma güvenliği V2.32 kamera yolunda.

### Yürüyüş neden hariç (açık 5C)

- Yürüyüşte görüş dönerken pelvis salınımı ve dönüş, basılı ayakta 18–22 cm kayma üretti.
- Bu yüzden üretim eşiği 170 cm/s (yalnız tempolu ve depar).
- Not: "jturn" senaryosu aslında yürüyüş hızındaydı (112–132). Gerçek tempolu için `jturnj` eklendi.

**Kirli veri.** Harness `pawn_flags` geri yükleme hatası, ilk gamepad koşusundan sonraki 30 FPS fare kamera değerlerini kirletti (`tables_f30.txt`, Q sütunu). Hata düzeltildi (iki geçişli uygulama). 60 FPS ve sonrası temiz.

**180° gerçek dönüş.** Taraf seçimi ve olaya bağlı tepki zarfı yapılmadı. MaxErr 110 nedeniyle 180°'de otomatik dönüş tetiklenmez; bu bilinçli bir seçim.

## 11. Arazi — açık

- Arkadaki ayak ve iniş için bu turda çalışılmadı.
- ter_drop_walk (6.5 cm) ve legs_slope_sprint (17.2 cm) yalnız regresyon olarak koşuldu, değişmedi.
- Kameranın arazi / duvar çarpışma yolu değişmedi.

## 12. Test ve geliştirme döngüsü

**Aşamalar (zaman damgaları `data/chain.out`'ta)**

| Aşama | Saat | Konu |
|---|---|---|
| GATES / GATES2 | 12:38–12:49 | kapı testleri T1–T8 |
| TEL | 12:52–13:07 | telemetri yan dosyası |
| C1–C1C | 13:17–14:33 | stand-back |
| CAM–CAM5 | 14:33–17:02 | arkaya dönüş, kilit, cihaz profili; 8 temiz editör açılışı, her biri bir fonksiyon yeniden kurulumu |
| K1 / K2 | — | ölçüm |
| F | 17:03–20:11 | 30 / 60 / 120 / 20 / gerçek zaman |
| X | 20:11–20:39 | kamera varyantları Q2 / Q3 |
| S | 20:39–20:54 | depar adayı |
| FIN | 20:55–21:32 | üretime alma → temiz açılış → doğrulama → 41 koşu |
| CAP | 21:32–21:39 | 12 kayıt |
| D60 | 21:43–21:56 | 60 FPS jback teşhisi (üretim / yalnız beden / yalnız kamera / V2.32) |

**Ölçülen süreler**
- Editör yeniden açılışı: 2.5–6 dk. 23 yeniden açılış yapıldı (+2 güvenle reddedilen); her birinin nedeni günlükte.
- 30 FPS koşu: ~35 s. 60 FPS: ~50 s. 120 FPS: ~80 s.

**Telemetri.** SHM| satırları artık editör günlüğüne değil yan dosyaya yazılıyor. Günlükte 0 satır, yan dosyada 352 satır, kanıt aynı. Tüm oturumun günlüğü ~2.25 MB.

**IsUnique.** Toplu soak yapılmadı, brif gereği; bu turda çalışılmadı.


## 13. Üretime alma ve doğrulama

**Sıra:** üretime alma → temiz açılış → doğrulama.

1. `promote233.py` (manifest `promo233`):
   - ABP `SHM233_StandBackOn` = 2, `SHM233_DB_StandBack` = `PSD_SHM233_StandBackStart2`;
   - DA `CamRecEnabled` = true, `CamRecMaxErr` = 110, `CamRecMinSpeed` = 170.
   - Kayıt sonrası kirli paket yok.
   - İlk deneme bash `GROUPS` yerleşik değişkeni yüzünden yazmadan önce güvenle düştü.
2. Temiz açılış, ardından `verify233.py`. Kontrol ettikleri:
   - V2.32 sözleşmeleri;
   - knob'lar, stand-back grafiği ve DB girdileri;
   - kamera fonksiyon sayımı (≥ 1000 düğüm, LastHitBy bağlı değil);
   - telemetri;
   - hareket çerçevesi seçimi;
   - kontrol yaw yazıcısı ve cihaz ölçekleri;
   - gated runner'ın kullanımda olduğu.
   - Sonuç: **ALL_OK = true** (`data/verify_fin.out`).
3. Son kanıt: üretimde 41 koşu (`data/tables_fin.txt`) + A/B/C/D matrisi (`data/matrix_fin.txt`).

**Geri dönüş:** `promote233.py` içindeki `rollback` değerleri, ya da `checkpoint/manifests/` yedekleri.

### A/B/C/D (beden × kamera, final, 30 FPS)

| Senaryo | A V2.32 | B yeni beden | C yeni kamera | D V2.33 |
|---|---|---|---|---|
| j30_slow en kötü / başlangıç | 38.3 / 38.3 | 22.1 / 0 | 38.3 / 38.3 | 22.1 / 0 |
| jturnj en kötü | 34.4 | 83.6 (parçalama) | 29.3 | 38.8 |
| sturn en kötü | 11.0 | 6.5 | 6.6 | 10.0 |

- Kamera bedeni etkilemiyor: C, A ile aynı başlangıç değerini veriyor.
- Kamera dönerken yön sabit; yalnız hız farkı var (bölüm 0, madde 6).

## 14. Teslim tablosu

| Kalem | Durum |
|---|---|
| Güvenlik kapıları runner'da + gerçek yakalama | PASS |
| Üç skill + CLAUDE.md yönlendirmesi | PASS (teknik) |
| Gerçek duruş → geri kalkış (38–44 → 0, 5 FPS modu) | PASS teknik; görsel kabul sizde |
| Zincir 1'in ileri duruş / düşük hızlı ters dönüş kısmı | AÇIK |
| Zincir 2 yakalama / yerleşme adımı, üç doğallık örneği | YAPILMADI |
| Depar tavrı | ADAY (gövde evet, kol / baş hayır), üretimde değil |
| Otomatik arkaya dönüş (tempolu / depar, gamepad + fare) | PASS teknik; görsel / his kabulü sizde |
| Yürüyüşte otomatik dönüş | AÇIK (kayma maliyeti) |
| Olaya bağlı tepki zarfı, 180° taraf seçimi | YAPILMADI |
| Girdi çerçevesi devri, istenmeyen yön değişimi yok | PASS (yalnız hız farkı) |
| Yan / arka çapraz, bırak–yeniden bas, 60 FPS düşük hızlı ters dönüş | AÇIK |
| Arazi (arkadaki ayak, iniş) | YAPILMADI |
| IsUnique | ÇALIŞILMADI |
| PS donanımı | TEST EDİLMEDİ |
| A_CT_Ref eski sürüm | yalnız OneDrive geçmişinde |
| Yayın | bu rapor + kod + kayıtlar (Bridge) |

### Kayıtlar (`vid/`, normal hız, düzenlenmemiş tam kare; GIF + gerçek zaman AVI)

- `sprint_hard_right_before_game` / `_v233_mouse_game` / `_v233_gamepad_game`: aynı girdi, önce / sonra.
- `jog_left_v233_gamepad_game`
- `walk_look_no_recentre_v233_game`: yürüyüşte üretimde dönüş yok; bakış aynen korunuyor.
- `backward_no_halfturn_v233_game`
- `camera_chain_v233_gamepad_game`
- `stand_back_start_before_side` / `_v233_side`
- `sprint_attitude_current_side` / `_calm_candidate_side`
- `sprint_hard_right_body_v233_side`
