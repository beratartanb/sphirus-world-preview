# SPHIRUS — SHME V2.34: beden sürekliliği, doğal performans ve bütünleşik kamera takibi (2026-10-28)

Taban: V2.33 üretimi (Bridge a4417bc). Blueprint-only UE 5.8, git yok; geri dönüş manifest yedekleriyle (sha1 doğrulamalı).
Bütün sayılar sabit adımlı editörde, aynı girdiyle ölçüldü. Aksi yazılmadıkça 30 FPS kullanıldı ve ölçüt `contact231` en kötü basılı-top kayması / sürüklenmesi (cm).
"Teknik PASS" görsel ve oyun hissi kabulü değildir; bu raporda ikisini ayrı yazıyorum. PS donanımında test yapılmadı.

**Üretime alınanlar (temiz açılışta VERIFY234 ALL_OK):**
- `loco`: gövde/hareket çerçevesi ve keşif kararı.
- `camfollow`:
  - yürüyüş takibi açık;
  - takip, gövde yönü kapısıyla yalnız ilerleme yönüne bakan gövdenin arkasına yerleşiyor;
  - 180° dönüşte taraf seçimi var;
  - sinematik tepki zarfı fren/dönüş/ters dönüş bölümüne bağlı.
- `revkeep`: bırak–yeniden basta ters dönüş devam ediyor.
- `sprintcalm`: daha sakin depar üst bedeni.
- İçerik: 21 duruş klibinin kapanış adımına parmak ucu açıklığı (kayan ayağı kaldırır).

## 0. Kısa yanıtlar

1. **Otomatik kamera kaynaklı hız değişimi giderildi mi?**
   Evet. Kaynağı bulundu ve kaldırıldı.
   - `BP_GR_Player` içindeki 7 hareket fonksiyonu (hız sınıfı, ivme, sürtünme, gait, geri niyeti, gövde dönüş hedefi, idle dönüş) kontrol yaw'unu okuyordu.
   - Artık hepsi kameradan bağımsız gövde çerçevesini (`LocoYaw`) okuyor.
   - Aynı beden, aynı girdi, kamera açık / kapalı karşılaştırması:

     | Ölçüt | V2.33 | V2.34 |
     |---|---|---|
     | Hız farkı | 73 cm/s | 0.0 |
     | Yol farkı | 297 cm | 0.0 |
     | Gövde yaw farkı | 92° | 0.0 |

   - Doğrulanan durumlar: depar, yürüyüş, tempolu ve küçük analog düzeltmeler.
   - Son oturumda da aynı sonuç: V2.33 kamerası gövdeyi 31.6 cm/s ve 68 cm değiştiriyor; V2.34'te fark 0.0.
   - Kalan dar yol: kapsül yolu aynı kaldığı hâlde animasyon seçimi kameradan etkilenebiliyor (madde 13, bölüm 7).
2. **Yürüyüşte sağ analog olmadan doğal takip çalışıyor mu?**
   Evet, gamepad profilinde. Gövde girdinin yönüne kendisi dönüyor (keşif kararı), kamera gövdeyi izliyor.
   - Yürüyüşte sağa dönüşte 1.6 s'de yerleşiyor, en çok 46°/s.
   - Kayma, kamera kapalıyla aynı (6.5 cm).
   - Fare profili yürüyüşte yavaş: 16.5°/s, 5.5 s sonunda hâlâ 28.6°. Bunu iyi saymıyorum; açık ayar kalemi.
3. **Manuel müdahale son üretimde, takip sürerken doğrulandı mı?**
   Evet. Bakış, otomatik dönüş sürerken yapıldı (`CamRecDelta` ≠ 0 anında).
   - Otomatik katkı bakışın başladığı karede sıfırlanıyor.
   - Görülen açı korunuyor, eski merkeze sıçrama yok.
   - Takip, bakıştan 1.6 s sonra yumuşakça devam ediyor.
   - İlk deneme takip başlamadan bakıyordu: NOT_TRIGGERED sayıldı ve zamanlama düzeltildi.
4. **Fren ve destek hareketi kritik anda çaprazdan gösteriliyor mu?**
   Kısmen evet. Sinematik açı fren/dönüş/ters dönüş bölümünde oluşuyor, bölüm bitince çözülüyor.
   - Depar sert sağda, dönüş bittikten sonra 4°'nin üstündeki savrulma 1.33 s'den 0.40 s'ye indi.
   - Sonradaki tepe 11.7°'den 6.8°'ye indi; eylem sırasındaki tepe 8.9°.
   - Kamera zincirinde: 0.83 s → 0.40 s.
   - Görsel kabul sizde.
5. **Gerçek 180° dönüş ile geri hareket ayrıldı mı?**
   - Geri hareket hiçbir koşuda kamerayı yarım tur döndürmüyor (kontrol değişimi 0°).
   - Bu bakış güdümlü kontrolde S her zaman bilinçli geri hareket. Depar sonrası S de geri koşuya dönüyor.
   - Gövdenin yeni yöne döndüğü gerçek bir 180° bu şemada oluşmuyor.
   - Gövde yönüyle taraf seçimi uygulandı (gövde ilerlemeye bakıyorsa, döndüğü taraf), ama hiçbir senaryoda tetiklenmedi: **NOT_TRIGGERED**.
6. **Başlangıç–fren–yeniden itiş–duruş zincirinin hangi açıkları kapandı?**
   - Bırak–yeniden bas: j30_rel_3200 35.0 → 13.5 cm; ters dönüş kısmı 35 → 5–8 cm. j30_rel_3450 19.4 → 8.6 cm.
   - İleri duruş kapanışı: j30_slow 22.1 → 12.3 cm; zincir 1 22.1 → 16.2 cm.
   - Stand-back kilidi komutu kilitlemiyor (j34_sbcancel).
   - Bırak–yeniden bas FPS'e göre (bölüm 12):
     - 30 ve 20 FPS'de kapalı.
     - 60 FPS'de (51.0 cm) ve gerçek zamanda (21.7 cm) geri başlangıç hâlâ seçiliyor.
   - 60 FPS'deki açığın nedeni yönlendirme kilidi:
     - aile önce "sert dönüş"e (2) giriyor;
     - en kısa tutma süresi 2 → 3 geçişini engelliyor;
     - ABP tutması aile 3 istediği için devreye girmiyor.
   - Önerilen düzeltme: "ters dönüş, sert dönüşe öncelikli". Bu turda yapılmadı.
7. **Üç ek doğal hareketten hangileri gerçekten üretildi ve kullanılıyor?**
   Hiçbiri yeni hareket olarak tamamlanmadı. Bunu açıkça belirtiyorum.
   - **A (sert fren sonu yerleşme adımı):** fiziksel tetikleyici bulundu ama içerik ve yönlendirme yapılmadı.
     - Tetikleyici: e29 sonrası 39–50 cm'lik kademeli duruş, beden o pozda donuyor.
     - Hazır küçük adımlar (shuffle) yalnız vendor döngü veritabanlarında var.
   - **B:** üretilmedi. V2.31'in yüklü yakalama adımı sürüyor (e29_load).
     - Bırak–yeniden bas düzeltmesi bir "desteği sürdürme" düzeltmesi; B değil.
   - **C:** üretilmedi.
8. **Deparın baş ve kol değişikliği son görünen bedene ulaşıyor mu?**
   Evet. V2.33'teki "kollar değişmedi" yorumu ölçüm hatasıydı (dönüşlü senaryo, farklı ölçüt). Düz ve kararlı deparda, aynı ölçütle:

   | Ölçüt | Önce | Sonra |
   |---|---|---|
   | Üst kol salınımı | 89.5° | 70.5° |
   | El salınımı (görünür beden) | 56 cm | 43 cm |
   | Gövde eğimi (görünür) | 29.4° | 17.7° (tempolu 12.4°) |
   | Omuz karşı-dönüşü | 52° | 31° |
   | Boyun yanal salınımı | 12.7 cm | 10.4 cm |

   - Çalışma zamanı yanal salınıma ~3 cm ekliyor. Bu katkı PBI, ayak yerleşimi ve destek kayması kapalıyken de değişmiyor; MM karışımından geliyor.
   - Görünür beden gövde eğimine retarget'tan sabit +5–6° ekliyor.
9. **Yan/arka çapraz ve bırak–yeniden bas ne durumda?**
   - c29 yürüyüş yan zinciri 57.6 → 9.9 cm.
   - wdiag oturumdan oturuma 8–24 cm arasında oynuyor; V2.34 son koşusunda 20.5 cm. İyileştiği kanıtlanmadı.
   - Bırak–yeniden bas: 30 ve 20 FPS'de kapalı, 60 FPS'de ve gerçek zamanda açık (madde 6).
   - Gerilemeler (nedenleri bölüm 5'te):

     | Senaryo | 30 FPS | Diğer FPS |
     |---|---|---|
     | jstart (başlangıç) | 43 → 50 cm | gerçek zaman 43 → 54 cm |
     | Tempolu sol | — | 20 FPS 7 → 26 cm; gerçek zaman 17.6 → 26.3 cm |
     | Depar sert sağ, fare profili | 11 → 14 cm | gerçek zaman 10 → 20 cm |
10. **Arazi bağlantısına gerçekten ne uygulandı?**
    Müdahale yapılmadı; yalnız teşhis edildi. Açık kalem.
    - Basamak inme/çıkmada pelvis kapsülün 27–33 cm gerisinde kalıyor; tempoluda 2 s'de oturuyor.
    - İnişte salınım ayağı alt zeminin 36–52 cm üstünde kalıp düşüyor.
    - Sahibi: kapsülün anlık basamak geçişi ile görsel pelvis/ayak hedefinin uyumsuzluğu.
11. **Yeni skill kuralları hangi yanlış kabulü veya işlemi engelledi?**
    - "Kamera hızı da değiştirmemeli" kuralı, `camab234` ile V2.33'teki 73 cm/s bağımlılığını hata olarak yakalattı.
    - "Bir başlangıçta sıfır ≠ zincirde sıfır" kuralı, stand-back'in 0'ına rağmen zincir 1'deki 22 cm'yi açık tuttu.
    - "Aynı ölçüt / aynı pencere" kuralı, V2.33'ün depar yorumunu tersine çevirdi.
    - "Hedef durum etkin değilse NOT_TRIGGERED" kuralı, yanlış zamanlı bakış testini geçersiz saydırdı.
    - Kesik log satırından çıkan yanlış "başarısız" ve fazla katı sayım kuralı yakalandı ve düzeltildi.
    - Thread-safe olmayan `IsValid` derleme hatası kayıttan önce durduruldu.
12. **Kaç yeniden açılış gerekti ve somut nedenleri neydi?**
    Toplam 19 açılış: oturum başında 1, ardından 18 yeniden açılış. Her birinin nedeni `data/chain.out`'ta:
    - 8 açılış, 4 yapıda ikişer editör (B1, B2, B3, B10):
      - yeni DA alanları ve bileşen değişkenleri taze bir sınıf derlemesi istiyor;
      - fonksiyon yapısı, V2.30 bellek kuralı gereği ayrı ve taze bir editörde yapılıyor.
    - 3 açılış, yalnız fonksiyon yapısı (B6, B8, B12): ~70–100 PIE koşusundan sonra aynı editörde fonksiyon yapısı bellek balonu riski taşıyor.
    - 1 üretime alma (FIN) ve 1 temiz açılışta doğrulama (FINV).
    - 4 FPS modu: FPS bir editör başlatma argümanı.
    - 1 kayıtlar için 30 FPS'e dönüş.
    - Hiçbir açılış "fonksiyon değişti" gerekçesiyle yapılmadı; ikinci bir editör açılmadı.
13. **Üretimde açık, kapalı aday ve açık kalan sonuçlar hangileri?** Bölüm 14.

## 1. Başlangıç, durum, koruma
- **Taban:** V2.33 üretimi.
  - Motor UE 5.8.
  - Etkin sahipler güncel grafik dökümlerinden doğrulandı.
  - Kilit sahibi `v234`.
- **Yazma güvenliği:**
  - Her yazma işi kesin varlık listeli manifest ve sha1 doğrulamalı yedekle yapıldı.
  - Hepsi gated runner'dan (G1–G5) geçti.
  - Manifestler `manifests/` altında.
- **Korunanlar (V2.33):**
  - stand-back;
  - klip–kapsül uyumu;
  - RevTurn;
  - düşük hızlı dönüşler, çıkış döngüleri, yüklü destek adımları;
  - tempolu/depar takip;
  - inceleme;
  - telemetri yan dosyası.
- **Değişmeyenler:** anatomi, yüz, kıyafet, harita. Yeni framework yok.
- **Reddedilen adaylar** (C, C2, C3, F): yalnız DA/ABP bayraklarıydı. Aktif aramada içerikleri yok.

## 2. Kamera ↔ hareket ayrımı

**Sahip.** Kontrol yaw'unu hareket amacıyla okuyan 7 `BP_GR_Player` fonksiyonu:

| Fonksiyon | Kontrol yaw'unu ne için okuyordu |
|---|---|
| `CalculateMaxSpeed` | yan ve geri hız ölçeği |
| `CalculateMaxAcceleration` | ivme sınıfı |
| `CalculateGroundFriction` | sürtünme |
| `GetDesiredGait` | gait seçimi |
| `GR_Impl_CR_UpdateBackwardIntent` | geri niyeti |
| `GR_Impl_CP_PhysicalRedirect` | bakış güdümlü modda aktör yaw'unu yazan tek yer |
| `GR_UpdateIdleTurn` | idle dönüş |

Kamera fonksiyonlarına (`GR_UpdateRig`, orbit, `CT_*`) dokunulmadı.

**Artık ayrı tutulan katmanlar:**
- ham hareket girdisi;
- ham bakış girdisi;
- `LocoIFY`: korunan dünya niyeti;
- `LocoYaw`: gövde/hareket çerçevesi;
- `CamRecDelta`: otomatik dönüş;
- `CamOrbitYaw`: geçici ofset, yalnız boom'a uygulanıyor.

**Girdi devri:**
- Çubuğun, kamera dönmeye başladığı andaki açısından **net** sapmasıyla (10–70°). Küçük düzeltmeler göreli uygulanır, yok sayılmaz.
- Oyuncu bakışıyla.
- Bırakınca hemen.
- Sonuç:
  - **jcor:** kamera açık/kapalı gövde farkı 0.0.
  - **wflow:** yön değişim hızı kamera açık 226°/s, kapalı 228°/s. Ek sıçrama yok.

**Kanıt (`camab234`).** Aynı beden sürümünde, basılı tuşlarla ve analog küçük düzeltmelerle hız, yön, ivme, gait ve yol farkı 0.0. V2.33'te bu farklar 73 cm/s, 297 cm ve 92° idi.

**Cihaz geçişi:** yalnız profil bayrağıyla sınandı (gamepad 1.0 / fare 0.35). Gerçek cihaz geçişi NOT_TESTED.

**Kalan dar bağımlılık:**
- Son oturumda depar sert sağda D ile B koşularında kapsül yolu, hız ve yaw birebir aynı.
- Buna rağmen D farklı bir kesme klibi seçiyor: 14.0 cm, B'de 6.5 cm.
- Olası sahip: MM poz geçmişi, kameraya bakan LookAt/aim-offset katmanından *sonra* toplanıyor (`PoseSearchHistoryCollector` ← `LayersCache`).
- Durum: açık. Öneri: geçmişi LookAt'tan önceki pozdan almak.

## 3–4. Yürüyüş takibi ve manuel bakış

**Keşif kararı (bedenin kararı).** Gövde, kamerayı beklemeden yeni yöne kendisi döner; kamera gövdeyi izler.
- Ne zaman: yürüyüş/tempolu (< 380 cm/s) sürerken girdi çerçeveye 20–120° açıyla (yan veya çapraz-ileri) tutuluyorsa.
- Hangi yöne: girdinin dünya yönüne.
- Şu durumlarda başlamaz:
  - oyuncu bakıyorsa;
  - inceleme sırasında;
  - ters dönüşte;
  - depardan başlayan yön değişiminde;
  - başlangıç ailesinin içinde ve bitişinden sonraki 0.5 s içinde.
- Bırakınca gövde çerçevesi tutulur. Kamera duran gövdeyi döndürmez.
- Oyuncu bakıyorsa beden görüşe bakar ve yana/geri adım atar. Otomatik takip yalnız ilerleme yönüne bakan gövdenin arkasına yerleşir (`CamRecFaceMax 40`).

**Sonuçlar (son üretim, gamepad):**

| Hareket | Arkaya yerleşme |
|---|---|
| Yürüyüş sağ | 1.6 s (en çok 46°/s) |
| Tempolu sol | 1.2 s |
| Depar sert sağ | 1.57 s |

- 20/60/120 FPS ve gerçek zamanda 1.55–1.86 s.
- Yürüyüşte kayma, kamera kapalıyken ölçülenle aynı.
- Gamepad akışı sağ analoga dokunmadan sınandı: yürü → sağ → ileri → sol → ileri → çapraz → dur → devam (`vid/walk_flow_v234_gamepad_game`).
- **Fare profili:**
  - tempolu 3.9 s, depar 4.3 s;
  - yürüyüşte çok yavaş: 16.5°/s, 5.5 s sonunda hâlâ 28.6° yan açı. **AÇIK.**

**Manuel bakış:**
- Otomatik dönüş sürerken (2.4°/kare) bakış başladığı karede otomatik katkı 0'a iniyor.
- Görülen açı korunuyor.
- Takip, bakış bitince 1.6 s sonra yeniden başlıyor.
- Tempoluda (jlook) ve deparda (slook) sınandı.
- 2°/s çubuk kayması bakış sayılmadı.

## 5. Zincirler

**Zincir 1 (j34_chain1):**
- Stand-back başlangıç kayması 0 cm'de korunuyor.
- İleri duruş kapanışı 22.1 → 16.2 cm.
- j34_sbcancel: S'den 0.35 s sonra W'ye basınca ileri başlangıç geliyor; stand-back kilidi komutu kilitlemiyor.

**Bırak–yeniden bas.** İki sahip vardı:
1. Bileşen, girdi boşluğunda ters dönüş ailesini bırakıyordu → `RevGraceTime` + boşluk zamanlayıcısı.
2. ABP'nin varsayılan seçicisi ivme yokken duruş, yeniden basışta duruştan başlangıç veritabanını arıyordu → `Update_MotionMatching` girişinde son ters dönüş veritabanı tutuluyor.

| FPS | Önce | Sonra | Durum |
|---|---|---|---|
| 30 | 35.0 cm | 13.5 cm (ters dönüş kısmı 5–8) | kapandı |
| 20 | 38 cm | 18.7 cm | kapandı |
| 60 | — | 51.0 cm | **açık** |
| Gerçek zaman | — | 21.7 cm | **açık** |

60 FPS ve gerçek zamandaki açığın nedeni için madde 6'ya bakın.

**İleri duruş kapanışı:**
- Kaynak klipte kapanış adımında parmak ucu 40–70 cm zeminde kayıyor.
- Topuk kalkışına bakan ilk kural sonucu değiştirmedi (22.1 → 22.1).
- Parmak ucu kuralı:
  - j30_slow: 22.1 → 12.3 cm;
  - zincir 1: 22.1 → 16.2 cm;
  - cam_corr: 34.4 → 26.3 cm.
- 21 klipte yalnız kapanış adımı değişti.

**c29 yan zinciri (V2.33 değerleri → V2.34):**

| FPS | Önce | Sonra |
|---|---|---|
| 30 | 57.6 | 9.9 |
| 60 | 62.4 | 11.3 |
| 120 | 54.6 | 14.6 |
| 20 | 36.6 | 11.4 |
| Gerçek zaman | 24.6 | 16.0 |

**wdiag:** iyileştiği kanıtlanmadı.

**Gerilemeler (açık):**
- **jstart:** 30 FPS'de 43 → 50, gerçek zamanda 43 → 54 cm. Keşifle bir yöne dönmüş ve tutulmuş gövde, ters yöne yeni basışta geri başlangıca düşüyor.
- **Tempolu sol:** 20 FPS'de 7 → 26, gerçek zamanda 17.6 → 26.3 cm. Tempolu keşif dönüşü strafe klibi içinde gerçekleşiyor.
- **Depar sert sağ (fare):** 11 → 14 ve 10 → 20 cm. Neden: madde 2'deki dar bağımlılık ya da sakin depar seçimi; ayrıştırılmadı.

## 6. Üç ek doğal hareket
**Tamamlanmadı.**
- **A:** tetikleyici ölçüldü; sert fren sonrası beden 39–50 cm'lik kademeli duruşta donuyor. İçerik ve yönlendirme yok.
- **B:** yapılmadı.
- **C:** yapılmadı.

## 7. Depar baş–kol tavrı
**Yöntem:** `stage234` / `clipstage234`. Aynı ölçüt ve aynı düz/kararlı pencere; kaynak klip, MM örgüsü ve görünür beden ayrı ayrı ölçüldü. Değişikliğin ulaştığı değerler madde 8'de.

**Çalışma zamanının yanal salınım katkısı (~3 cm):**
- PBI, ayak yerleşimi, destek kayması, eğri eğimi, APA tek tek veya birlikte kapatılınca değişmiyor; kaynağı MM karışımı.
- Sakin depar kliplerindeki azalma kısmen korunuyor.

**Süreklilik:** tempolu ile depar tavrı birbirine yakın (gövde 12.4° ve 17.7°; önce 29.4°).

**Görsel değerlendirmem:** daha dik ve daha az savrulan, hâlâ deparda olan bir beden. Baş–omuz savurması azalmış, kollar hâlâ çalışıyor.

## 8. Geçiş sürekliliği
- Uzun karışım kullanılmadı; ayaklar temas sınıfından çıkarılmadı.
- Duruş kapanışı gerçek ayak kaldırma olarak üretildi; ayağın yatay yolu aynı.
- Görsel karşılık: `sheets/stop_closing_side.png`.

## 9. Sinematik tepki
- **Zarf (`CamEnv`):**
  - fren, ters dönüş, dönüş veya yön değişimi bölümünde yükselir;
  - bölüm bittikten 0.3 s sonra söner;
  - orbiti çarpar;
  - süreklidir, yeni istekte sıfırdan başlamaz.
- Otomatik takip bölüm sırasında çalışmaz.
- Tek koordinatör: `SHM_UpdateCameraV21`.

**Dönüş bittikten sonra 4°'yi aşan savrulma süresi:**

| Senaryo | Önce | Sonra |
|---|---|---|
| Depar sert sağ | 1.33 s (tepe 11.7°) | 0.40 s (tepe 6.8°) |
| Kamera zinciri | 0.83 s | 0.40 s |
| Duvar | — | 0 s |

- Eylem sırasındaki tepe: 8.9°.
- FOV, zoom, roll veya sarsıntı kullanılmadı.

## 10. Arazi
**Uygulanmadı.** Yalnız teşhis (`terrain232`, üretim):

| Durum | Pelvis gecikmesi | Diğer |
|---|---|---|
| Yürüyüş, −30 cm iniş | 28.7 cm | — |
| Yürüyüş, +18 cm çıkış | 27 cm | 0.97 s'de oturma, 0.13 s askıda kalma |
| Tempolu, −15 cm iniş | 32–33 cm | 2.0 s'de oturma; salınım ayağı alt zeminin 36–52 cm üstünde |

Kameranın çarpışma yolu değişmedi (V2.32 yolu).

## 11. Skill güncellemeleri
- **`sphirus-camera-direction`:**
  - "Kamera yönü de hızı da değiştirmez" kuralı ve gövde çerçevesi.
  - Gerçek başarısız örnekler:
    - V2.33 bağımlılığı;
    - kapatılmış yürüyüş takibi;
    - NOT_TRIGGERED bakış testi;
    - birikimli devir.
  - `camab234` kabul testi.
- **`sphirus-natural-motion`:**
  - Kabul kaydı formatı.
  - Kurallar:
    - "oynanmadıkça sayılmaz";
    - "temiz açılış kabulün parçası";
    - "oturum farkı gerekçe değil";
    - "ALL_OK ≠ doğal performans".
  - Örnekler:
    - depar ölçüm hatası;
    - duruşta parmak ucu sürüklenmesi;
    - ABP seçicisi.
- **`sphirus-safe-unreal-iteration`:**
  - İşin tam çıktısına bakma kuralı.
  - Yeni durum yazıcısı sayımı ve davranış kontrolü.
  - Sayım kurallarının kaynağa uyması.

## 12. Test ve çalışma süresi
**Akış (04:00–11:42).**
- Aşamalar sırasıyla:
  - B1–B12: aday ve yapı;
  - FIN: üretime alma;
  - FINV: temiz açılışta doğrulama;
  - F60, F120, F20, FREAL: FPS modları;
  - CAP: kayıtlar.
- Her yapıdan sonra:
  1. kayıttan önce yeni durum yazıcısı ve düğüm sayımı;
  2. davranış kontrolü;
  3. önce bir kırık örnek ve bir sağlam karşı örnek, sonra aile ve iptal koşuları.

**Yakalanan hatalar.**
- 4 iş durdu, hiçbirinde kayıt yapılmadı:
  - kesik log satırı;
  - fazla katı sayım;
  - geçici dosya kilidi;
  - yerelleştirilmiş düğüm tipi.
- 1 derleme hatası kayıttan önce durduruldu: thread-safe olmayan `IsValid`.

**FPS karşılaştırması.** En kötü kayma (cm), V2.33 değerleri → V2.34. "—" o FPS'te V2.33 koşusu yok.

| Senaryo | 20 | 30 | 60 | 120 | Gerçek zaman |
|---|---|---|---|---|---|
| Depar sert sağ (fare) | 9.0 → 6.0 | 11.1 → 14.0 | 11.8 → 10.0 | 26.4 → 8.6 | 10.0 → 20.3 |
| Yürüyüş sağ | 6.0 → 6.0 | 12.2 → 6.5 | 10.6 → 0.0 | 10.9 → 10.3 | 8.7 → 8.0 |
| Tempolu sol | 7.0 → 26.2 | — → 11.2 | 37.4 → 28.9 | 37.4 → 25.2 | 17.6 → 26.3 |
| Bakış (tempolu) | 14.1 → 8.6 | — → 13.0 | 16.7 → 12.3 | 17.3 → 14.1 | 13.8 → 17.4 |
| c29 | 36.6 → 11.4 | 57.6 → 9.9 | 62.4 → 11.3 | 54.6 → 14.6 | 24.6 → 16.0 |
| Bırak–yeniden bas | 38.0 → 18.7 | 35.0 → 13.5 | 55.8 → 51.0 | 24.5 → 25.6 | 18.3 → 21.7 |
| j30_slow | 16.3 → 16.3 | 12.3 → 12.3 | 15.4 → 9.7 | 13.6 → 15.9 | 10.9 → 10.3 |
| jstart | 51.2 → 51.1 | — → 50.4 | 42.8 → 43.4 | 44.3 → 49.5 | 43.3 → 54.4 |
| e29 | 9.0 → 9.0 | — → 6.5 | 20.6 → 20.6 | 18.9 → 17.6 | 16.4 → 7.9 |
| Düz depar | 18.3 → 18.6 | 15.9 → 15.9 | 19.8 → 16.5 | 17.4 → 18.1 | 22.7 → 18.0 |

- Duruş kliplerindeki içerik düzeltmesi iki tarafta da var.
- Kamera ölçümleri: `data/rec_fin.txt`, `data/env_fin.txt`.

## 13. Üretime alma ve doğrulama

**1. Üretime alma.** `promote234.py` (manifest `promo234`); geri dönüş değerleri betik çıktısında.

**2. Temiz açılışta doğrulama.** `verify234` ALL_OK. Doğrulananlar:
- V2.32 ve V2.33 sözleşmeleri. Tek kasıtlı fark: `CamRecMinSpeed` 170 → 60.
- DA ve ABP değerleri.
- Bileşen fonksiyonları: kamera 1767 düğüm, yönlendirme 709 düğüm.
- 7 hareket okuyucusu gövde çerçevesini okuyor.
- Ters dönüş tutma grafiği yerinde.
- Bağlı `LastHitBy` yok.

**3. A/B/C/D karşılaştırması (30 FPS).** En kötü kayma (cm):

| Senaryo | A (V2.33 değerleri) | B (yeni beden) | C (yeni kamera) | D (V2.34) |
|---|---|---|---|---|
| Depar sert sağ | 11.1 | 6.5 | 11.1 | 14.0 |
| Yürüyüş sağ | 12.2 | 6.5 | 10.3 | 6.5 |
| c29 | 57.6 | 21.9 | 57.6 | 9.9 |
| Bırak–yeniden bas | 35.0 | 12.9 | 35.0 | 13.5 |
| Kamera zinciri | 23.0 | 6.5 | 23.0 | 6.5 |
| j30_slow | 12.3 | 12.3 | 12.3 | 12.3 |
| Düz depar | 15.9 | 15.9 | 15.9 | 15.9 |

## 14. Teslim tablosu
| Kalem | Durum |
|---|---|
| Kamera → hız/yön/gövde | **PASS**. Animasyon seçimine dar etkisi **AÇIK** |
| Yürüyüş takibi (gamepad) | **PASS** (teknik); görsel kabul sizde |
| Yürüyüş takibi (fare) | **AÇIK** (çok yavaş) |
| Takip sırasında manuel bakış (üretim) | **PASS** |
| Evrelere bağlı sinematik tepki | **PASS** (teknik); görsel kabul sizde |
| 180° | Geri hareket **PASS**; gerçek dönüş **NOT_TRIGGERED** |
| Bırak–yeniden bas | 30 / 20 FPS **PASS**; 60 FPS ve gerçek zaman **AÇIK** |
| Duruş kapanışları | **PARTIAL** (22 → 12–16 cm) |
| c29 yan zinciri | **PASS** (bütün FPS modları) |
| wdiag | **AÇIK** |
| jstart, tempolu sol, depar kesme | **GERİLEME, AÇIK** |
| Üç doğal hareket | **YAPILMADI** |
| Depar baş–kol tavrı | Üretimde, son bedene ulaşıyor; görsel kabul sizde |
| Arazi | **YAPILMADI** (teşhis var) |
| Skill'ler | **PASS** |
| PS donanımı | **TEST EDİLMEDİ** |
| Gerçek cihaz geçişi | **NOT_TESTED** |

**Genel değerlendirme.**
- Ana hedef teknik olarak tamamlandı: kamera bedeni değiştirmiyor, yürüyüşte doğal takip çalışıyor, oyuncu bakışı öncelikli.
- Belirgin iyileşmeler: yan zincir ve bırak–yeniden bas (30 / 20 FPS).
- Açık kalanlar:
  - tempolu/depar yan kesmeleri ve başlangıçlarda bazı FPS modlarında gerileme;
  - üç doğal hareket;
  - arazi.

## Kayıtlar (`vid/`)
Normal hız, düzenlenmemiş tam kare; her kayıt GIF ve gerçek zamanlı AVI olarak.

| Konu | Önce / sonra kayıtları |
|---|---|
| Yürüyüşte sağa dönüş (oyun kamerası) | `walk_right_before_game` / `walk_right_v234_game` |
| Depar sert sağ (oyun kamerası) | `sprint_right_before_game` / `sprint_right_v234_game` |
| Gamepad akışı | `walk_flow_v234_gamepad_game` |
| Takip sırasında manuel bakış | `jog_look_during_follow_v234_game` |
| Kamera zinciri | `camera_chain_v234_game` |
| Depar tavrı (yan) | `sprint_attitude_before_side` / `sprint_attitude_v234_side` |
| Bırak–yeniden bas (yan) | `release_repress_before_side` / `release_repress_v234_side` |
| Zincir 1: geri kalkış → ileri → duruş (yan) | `back_start_forward_stop_v234_side` |
| Yürüyüş yan zinciri (yan) | `walk_lateral_chain_before_side` / `walk_lateral_chain_v234_side` |

Kare sayfaları: `sheets/`.

