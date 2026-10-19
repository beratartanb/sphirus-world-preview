# SHME V2.18: gerilemeler, tempolu itişin ayrılması, yere basan toparlama adımı (2026-10-19)

**Taban.** V2.17 üretimi (commit `39172ce`, yaw-snap düzeltmesi dahil).
- "Önce" sütunu: V2.17 final üretim partisi `v217z2`. Aynı harness ve aynı pencerelerle ölçüldü; ayrı etiketlidir, V2.16 değildir.
- "Sonra" sütunu: tek, kaydedilmiş V2.18 üretim partisi `v218f`.
  - 93 koşu; en düşük telemetri hızı 22.7 satır/s; kare boşluğu yok.
  - Editör kapatılıp yeniden açıldı ve doğrulama yapıldı (`verify_prod218_f0/f1.txt`).

**Ölçüm.**
- `contact216`: ayak başına en kötü net kayma / sürükleme yolu, cm. İki ayak asla toplanmaz.
- `rec218`: toparlama penceresinde iki ayağın gerçek zemin evreleri.
- `knee217` ve ayak-ucu düzlemi (yalnızca basan ayak).

Görsel kabul kullanıcıya aittir; buradaki görsel kontroller yalnızca tekniktir.

## Kısa cevaplar

1. **Tempolu itiş ayrıldı mı?** EVET.
   - J2S bağlantıları kendi veritabanında (`PSD_SHM218_JogPush`). Yalnızca tempolu itiş bölümü (`SHM217_JogOn`) bu veritabanını arıyor.
   - Diğer itişler yeniden `PSD_RR_Start` kullanıyor.
   - Final partide J2S klibi yalnızca tempolu itiş bölümü (`JogOn`) açıkken seçildi: 17 koşu, her J2S karesi bu bölümün içinde.
     - Bu 17 koşu: p_j2s*, p_j2s_tap, p_w2s_tap ve S-kesiş sonrası Shift ile yeniden hızlanma.
     - `tapretrig`, ters dönüş, duruştan kalkış ve yürüyüş→depar koşularında J2S seçilmedi.
   - Sol giriş kayması ve nadir uzun ilk adım: p_j2s L 4/2/12 → 6/2/3 cm.
2. **Erken, ardışık ve bırakma gerilemelerinin nedeni:**
   - **Erken:** Ters yön isteği rotayı yalnızca 1 kare yükseltiyordu. O karede karşı kesiş seçiliyordu, bölüm bitiyor, MM kavis→tempolu→itiş oynuyordu.
   - **Ardışık:**
     - Pivottan sonraki itiş 61–69 cm/s'de başlıyor ve ayakta-başlangıç klibine düşüyor.
     - V2.17'deki ortak `PushStandJ` veritabanı bu itişin tam ortasında ilk-kullanım takılması ekliyordu.
   - **Bırakma:** Temiz koşularda yeniden üretilemedi. V2.17'deki 93.8 cm'lik aykırı değer, 0.12 s'lik uzun bir kareyle çakışıyordu. Final: p_w2s_rel L 17.5/93.8 → 6.7/8.7 cm.
3. **Niyet/temas gecikmesi gerçek mi?**
   - Niyet gecikmesi: HAYIR, analiz hatasıydı. Ham girdi ile CMC ivmesi aynı karede dönüyor (tuştan +0.065–0.093 s sonra).
   - Satır boşlukları: gerçek uzun kareler, çoğu bir veritabanının oturumdaki ilk kullanımı.
   - Bileşen temas bayrakları: zeminden 0.07–0.25 s geç geliyor; karar için artık kullanılmıyor.
4. **Toparlama hem basıyor hem güvenilir tetikleniyor mu?** EVET (üretimde açık).
   - Final partide hedefli 14 koşunun 14'ünde girdi; iki ayak da klip içinde yere bastı.
   - Pencere içinde en kötü kayma 6.6 cm.
   - Hedef dışındaki 79 koşuda hiç tetiklenmedi.
   - Sınır: 20 fps kayıt koşularında bir kez tetiklenmedi, bir kez de 33 cm kaydı. Düşük kare hızında zamanlama riski var (aşağıda).
5. **Geç ters dönüşte diz ve TIP devri çözüldü mü?** HAYIR, ikisi de.
   - **Geç ters dizi:** Ayak-ucu düzlemine göre diz ≤8.5 cm, ama kalçaya göre burulma 1213–1895 °/s.
     - Pencereyi 0.60'a daraltmak dönüş ortasında klip değiştirmeyi tamamen engellemedi (3 koşunun 1'inde sürüyor).
     - Görselde dizler içe giriyor (`late_reverse_knee_after.jpg`).
   - **TIP devri:** İstek anındaki açı 55–85°. Başlatma dalının açı kutuları ve dönmeye devam eden ilk montaj, devri ilk montajın sonuna kadar bekletiyor. Aday kapalı.
6. **Final testler kaydedilmiş üretim mi?** EVET.
   - Kayıttan sonra editör kapatılıp yeniden açıldı; ardından doğrulama PASS, sızıntı yok, kirli paket yok.
   - Bayrak farkı yalnızca `TelemetryEnabled`; yalnızca kayıt için kullanılıyor.
   - Final partiden sonra editör yeniden açılıp aynı kontroller tekrarlandı: yine PASS.

## ONARIMLAR

| Hedef | Doğrulanan neden | Gerçek değişiklik | Önce → sonra (en kötü, cm) | Gerileme sonucu | Üretimde | Kalan kusur | Geri dönüş |
|---|---|---|---|---|---|---|---|
| Çok erken ters (kesiş +0.15 s), sağ | 1 karelik ters rotası → karşı kesiş → bölüm sonu → kavis/itiş | `SHM218_FlipLatch` 0.6 s: istek 60° içinde kaldıkça ters rotası tutuluyor; bırakma/yeni yön = güvenli çıkış. Erken olanlar toparlamaya gidiyor | L 54.5 → 6.4 (koşular: 5/54/24 → 6/6/5) | R 7.6 → 17.3: kesişin kendi R'si, ters isteğinden önce. V2.18 mekanizması o anda aktif değil | EVET | Kesiş R'si koşudan koşuya 5–17 | `FlipLatch 0`, `Recover 0` |
| Çok erken ters, sol | aynı | aynı + sol toparlama içeriği v6 | L 29.9 → 7.6; R 4.1 → 4.8 | yok | EVET | — | aynı |
| Erken ters (+0.25 s) | aynı | aynı | L 46.8 → 6.3; R 20.5 → 0 | yok | EVET | — | aynı |
| Ardışık ters (r_kb2) | Pivottan sonraki itiş ayakta-başlangıç klibine düşüyor; ayrıca `PushStandJ` ilk-kullanım takılması | J2S izolasyonu + `SHM218_LowStand`: yön değişimi bölümü içinde ya da bitişinden sonraki 0.8 s içinde başlayan itiş (30–220 cm/s, ileri ters itiş penceresi dışında) → `RevPushLow` | L 42.0 → 23.7; R 54.8 → 33.4 (koşular: L 18/20/24, R 33/17/20) | Ters itiş ve yürüme→S→itiş farkları V2.18 mekanizmasından değil (aşağıda) | EVET | Pivot ve kalkış ayağında 17–33 cm | `LowStandOn 0` |
| Tempolu→depar sol giriş / uzun ilk adım | J2S duruşu geniş (R +25 cm, döngülerde 4–9) | J2S rev4 lat_cap 7 + kendi veritabanı | p_j2s L 11.8 → 6.1; mid L 10.2 → 10.9 (6/6); rel R 13.6 → 12.0 | tap L 13.6 → 40.1: J2S yok; depar döngüsü sonundan (2.13) yeniden girişte kayma. V2.17 tapretrig'de de vardı (44.7) | EVET | Depar döngüsüne yeniden giriş kayması (önceden vardı) | `SHM212_DB_PushStand` / `PushStand0` = `PushStandJ`, `JogOn` dalı kalsa da zararsız |
| Yürüyüş→depar orta adım | W2S duruşu yürüyüş döngüsünden geniş (L −8 / R +6..10, döngüde +2/+0.5) | Yeni klipler `SHM218_W2S_*` (lat_cap 6, yarım adım pencere, kol sınırı), `PSD_SHM218_WalkLink`; V2.16 klipleri olduğu gibi duruyor | mid R 21.9 → 14.2 (14/14/4); rel L 17.5 → 6.7; early R 8.8 → 14.1 | late R 10.6 → 26.7 (3 koşunun 1'i; bağlantıdan depar döngüsüne çıkışta, ön ayak kayması) | EVET | late çıkışında tek koşuda 27 | `SHM211_DB_Push` / `SHM214_DB_GaitPush` = `PSD_SHM216_WalkLink` |
| Geç ters diz | Dönüş ortasında klip değiştiriyordu (`L_Lfoot` → `L_Rfoot`) | RevTurn pencereleri [0.52, 0.60] (V2.18 başında üretime alındı) | medial L 21/26 → 18/11/27; plane rate 646/1779 → 1213/645/1895 | Değişim 3 koşunun 1'inde sürüyor; içerik burulması değişmedi | EVET (pencere) | **ÇÖZÜLMEDİ** | `checkpoint/pre_e2` RevTurn klipleri |
| Yerinde ters devir (TIP) | Başlatma açı kutuları + dönmeye devam eden ilk montaj → devir ilk montajın sonunda | Adaylar `GR218_TipHandMinT` / `MinAngle` (aday, kapalı) | t_tiprev üretim değişmedi | — | HAYIR | **ÇÖZÜLMEDİ** | — |

**V2.18 mekanizmasından kaynaklanmayan farklar.** Aşağıdaki koşularda hiçbir V2.18 bayrağı aktif değil (`FlipOn` / `RecOn` / `PushRevOn` hepsi kapalı) ve klip dizisi V2.17 ile aynı. Farklar, kesiş anındaki depar döngüsü evresinden geliyor (0.41 ↔ 0.98) ve partiden partiye değişiyor:
- kesiş→S kesiş penceresi: R 9 → 16;
- ters itiş: 8/16 → 22/28;
- yürüme→S→itiş: R 44, koşu sonundaki RR_Stop'ta;
- kesiş sırasında tuş bırakma: L 33, RR_Stop'ta.

Bunlar kalan kusur olarak listeleniyor; sonucu ortalamayla gizlenmedi.

## YENİ DAVRANIŞLAR

| Davranış | İçerik / tetik | Kanıt (kapalı → açık) | Gerileme | Üretimde | Kalan kusur | Geri dönüş |
|---|---|---|---|---|---|---|
| Durumsal tek toparlama adımı (erken ters yön) | **İçerik:** AAMS `Run_Turn_090` kopyaları, kadans warp + ölçülen erken-ters yoluna yeniden yerleşim. Sağ: `L_Lfoot` [0.933, 1.133]. Sol: `R_Lfoot` [1.04, 1.12] + `entry_foot` (kesişin hâlâ bastığı R ayağı). Rfoot varyantları yanlış ayak seçiyordu (53–70 cm), veritabanından çıkarıldı. **Tetik:** ham niyet (CMC ivmesi aynı karede), hız > 150, kesiş yaşı < 0.25 s, latch süresi `RecLen` 1.0 s, tutulan veritabanı = toparlama | Final 14/14 girdi. Fren ayağı 0.23–0.32 s basıyor, ikinci ayak 0.06–0.20 s, pencerede en kötü 6.6 cm. Kalça en düşük 74.7–77.7 cm (depar 88–90). Ayak-ucu diz 5–10.6 cm (kesiş klibinin kendisi 12–13) | 79 hedef dışı koşuda tetik yok. Normal ters dönüş (yaş 0.31) kasten dışarıda: orada 42–50 cm kaydırıyordu | EVET | Atletik çömelme (kalça −12 cm) ve sağda kollar açık; görsel kabul kullanıcıda. 20 fps kayıtta tetik kaçabiliyor (1/4) | `SHM217_Recover 0` |
| Hareketli itiş (pivottan sonra) | yukarıdaki LowStand | r_kb2 d2 (eski): L 38.8/49.2; V2.18: 17–24 | p_revpush / k_ws_w'de devreye girmiyor (ileri ters itiş penceresi) | EVET | 17–33 cm | `LowStandOn 0` |

## Bölüm notları

**Bölüm 1.**
- `DA_SHM_Response_Default`'un kirli olmasının nedeni: harness `TelemetryEnabled=true` yazıyor (yalnızca kayıt).
- Bellek ile disk arasında başka fark yok (`flag_diff_v217.txt`, `flag_diff_v218_f0/f1.txt`).
- Her varyant kaydedilmiş ABP'yi yeniden yüklüyor. Pawn bayraklı varyantlar (TIP) için `POST = pawn_reset_save.py` eklendi; bayraklar koşular arasında taşınmıyor.

**Bölüm 2 (tanı varyantları).** v218d1b/d2:
- A: kaydedilmiş V2.17;
- B: JogLink kapalı (`jb`);
- C: + PushStand → `RR_Start` (`jc`);
- D: kendi jog veritabanı (`jd`).

Erken ters gerilemesi dört varyantın hepsinde vardı; yani J2S ile ilgili değil. Ardışık ters yalnız D'de ilk-kullanım takılmasından kurtuldu.

**Bölüm 3 (ilk bozuk kare).** Zincir: girdi (aynı kare) → rota 1 kare → karşı kesiş seçimi → bileşen bölümü biter → kavis/jog klibi → gövde döner, ayak basılı → kayma. Toparlama bir kaymayı örtmek için değil; doğru evrede giren ayrı içerik.

**Bölüm 5 (toparlama doğrulama sırası).**
1. İçerik önce kontrollü tetikle test edildi (d3–d8, `fr*` varyantları).
2. Başarısız içerik sürümleri: v3 (kalça tabanı 82), v4/v5 (fren-duruşu girişi, 30–46 cm `entry_foot` kayması). Kanıt dosyaları: `rm218_recover3..5.json`.
3. Tetik, ham niyetten bağlandı.
4. Bırakma (`r0_rel`) ve yeni yön (`r0_w`) koşuları her iki tekrarda da güvenli çıktı.

## Kayıtlar

Kayıtlar gerçek hızda, kil test görünümüyle; kareler düzenlenmedi.
- `vid/`: GIF ve gerçek zamanlı AVI.
- `img/`: kare tabloları.
- Erken ters, sol: yan / oyun / çapraz kamera.
- Erken ters, sağ: yan / oyun kamerası. Çapraz kayıtta (20 fps) toparlama tetiklenmedi; dosya adı `earlyrev_right_nottriggered_diag`.

## Dosyalar ve geri dönüş

- **Kaynak.** Araçlar `Tools/SHME_V218_20261019/`; kanıtlar `Saved/Codex/SHME_V218_20261019/` (proje içi, yayımlanmadı).
- **Üretim kararları** (`promote218.py`, `before` değerleri = geri dönüş):
  - `SHM212_DB_PushStand` / `SHM214_DB_PushStand0`: `PushStandJ` → `RR_Start`
  - `SHM218_FlipLatch`: 0 → 0.6
  - `SHM217_Recover`: 0 → 1
  - `RecAge`: 0.3 → 0.25
  - `RecLen`: 1.4 → 1.0
  - `DB_Recover`: `PSD_SHM217_Recover` → `PSD_SHM218_Recover`
  - `SHM218_LowStandOn`: 0 → 1
  - `SHM211_DB_Push` / `SHM214_DB_GaitPush`: `PSD_SHM216_WalkLink` → `PSD_SHM218_WalkLink`
- **Kontrol noktaları.** `checkpoint/pre_e1` … `pre_e9` ve `pre_promote` (ABP, pawn, V218 içeriği, lisp).
- **ABP grafik eklemeleri.** Knob kapalıyken etkisizler.
  - `install_v218_jogroute.py`
  - `install_v218_flip.py`
  - `install_v218_reclen.py`
  - `install_v218_lowstand.py` / `lowstand2` / `lowstand3`
  - `install_v218_rechold.py`
- **Pawn adayları.** `install_v218_tipgate.py` / `tiptime`; `GR217_TipHand` 0.
