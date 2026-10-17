# SHME V2.12 — yürüme başlangıcı kolları, geri yürüme, depara itiş, toparlanma adayı

Tarih: 2026-10-17. Motor: UE 5.8.1 (CL 56057345). Üretim: `ABP_GR_MotionMatchingBase` (Sandbox) + alt ABP, `BP_GR_Player` zinciri, `DA_GR_LocomotionBehavior`.
Kanıt klasörü: `Saved/Codex/SHME_V212_20261017/`. Araçlar: `Tools/SHME_V212_20261017/`.

**Kabul ayrımı:**
- **Teknik:** benim ölçümlerim.
- **Görsel:** yakalama karelerine benim bakışım.
- **Kullanıcı kabulü:** senin oyun testin. Hiçbir maddede kullanıcı kabulünü verilmiş saymadım.

## 0. Özet durum

| Madde | Teknik | Görsel (benim) | Kullanıcı | Üretimde |
|---|---|---|---|---|
| 1 Yürüme başlangıcında kollar | PASS (4 başlangıç türü, iki destek ayağı, döngünün 5 turu) | PARTIAL (bkz. §1.5) | bekliyor | evet |
| 2 TIP rahat stil | PASS kollar korundu; PARTIAL gövde/ters dönüş | PARTIAL | bekliyor | V2.11 kolları korundu |
| 3 Geri yürüme (gerçek tuşlar) | PARTIAL: 13 dizinin 11'inde hata yok; 2 kusur bulundu, düzeltilemedi | NOT_TESTED (görüntü var, değerlendirme senin) | bekliyor | değişiklik yok |
| 4 İtiş giriş/çıkış | PARTIAL: hızlı yürüme, sahte itiş, çift itiş, kopuk çıkış giderildi; giriş kayması, tempolu→depar itişi, ters dönüş sonrası orta giriş kaldı | PARTIAL (duruş V2.11 aralığına indirildi: 35.7° / 12–13 cm) | bekliyor | evet |
| 5 Toparlanma adayı | FAIL (aday üretildi ve ölçüldü, kabul ölçütlerini karşılamıyor) | — | — | hayır (uyuyor) |
| 6 Kamera–girdi | PASS (bkz. §6) | — | bekliyor | V2.11 korundu |
| 7 Diz/zemin koruması | PASS (V2.11 ile aynı; itiş bake'i `leg_guard`'dan geçti). Kalıntı: W+A↔W+D kesiş girişinde V2.11'den kalan tek kare 31–36° diz ekseni sıçraması | PARTIAL | bekliyor | V2.10 korundu |

(Bölüm 1–7 ayrıntıları aşağıda; sayılar 30 fps ölçüm koşularından, görüntüler `pub/` altında.)

## 1. Yürüme başlangıcında kollar (ilk kabul engeli)

### 1.1 Son üretimde yeniden üretim
- V2.11 üretiminde, 30 fps ölçüm koşularında (`v212a_*`) iki bulgu:
  - Sağ kol yürüyüşte 9.0–10.1° açıklıkta; idle'da 14–17°.
  - Başlangıçtan ~1.2 s sonra sağ dirsek gövde ortasına 18.9–19.9 cm'ye yaklaşıyor.
- V2.11 raporundaki "sağ kol içeride 0.28–0.59 s" karşılaştırması aynı koşulda değildi:
  - "sonra" değeri ~22 fps'lik yakalama koşularından;
  - "önce" değeri 30 fps koşularından geliyordu.
  - Aynı koşulda (30 fps) değer 0.00–0.51 s.

### 1.2 Doğrulanmış sebepler (iki ayrı sahip)
1. **Yürüyüş döngüsü içeriği** (`A_LB_Walk_Fwd`, 5 tur × 1.367 s, bacaklar her turda aynı):
   - Sağ kol her adımda iki kez 4–9°'ye iniyor (faz 2–3 ve 8), sol kol ≥9°. Bu, tek bir turda değil, beş turun hepsinde.
   - İki başlangıç klibi de tam bu fazlarda döngüye el veriyor (sağ ayak 0.317, sol ayak 0.805).
   - MM şemasında (PSS_Default) kol kanalı yok ve bacaklar aynı. Bu yüzden MM hangi turu seçeceğine keyfî karar veriyor.
   - Araçlar: `loop_arms212.py` (çevrimdışı), `arms212.py --cycles` (çalışma zamanı).
2. **V2.11'den kalan veritabanı tekrarı:**
   - V2.11'de bake kaynağı olarak `/Rollbacks/SHME_V211_Arms_Before_20261016/` altına dosya olarak kopyalanan özgün klipler `PoseSearchBranchIn` bildirimini taşıyordu.
   - PoseSearch'ün dış bağımlılık senkronizasyonu bu kopyaları üretim veritabanlarına kendiliğinden ekledi:
     - `PSD_LB_WalkLoops` 8. giriş = özgün döngü;
     - `PSD_SHM_TurnInPlace` 8–15. girişler = özgün dönüşler.
   - MM iki kopya arasında da keyfî seçiyordu. Bu yüzden V2.12'nin ilk bake'i oyunda "hiç değişmemiş" göründü: diskteki ve sıkıştırılmış veri doğruydu ama MM özgün kopyayı oynatıyordu.
   - Kanıt: `req/probe_dbassets2.py` (giriş yolları), `req/probe_compressed.py` (sıkıştırılmış = ham).
   - V2.11 raporundaki "geri alma kopyaları referanssız" ifadesi yanlıştı.

### 1.3 Değişiklik
- **Döngü kolları:** `A_LB_Walk_Fwd` kolları özgün kaynaktan yeniden bake edildi (`v212_arm_bake.py`, "karşı kol tabanı").
  - Her kolun gövdeye göre açısı, aynı destek fazındaki karşı kolun yarım tur ötedeki ortalamasının 1.5° altına inemez (tavan 12.5°).
  - Yalnız yükseltme yapılıyor; döngüsel yumuşatma var, doğal salınım korunuyor.
- **Başlangıç klipleri** (sağ/sol ayak) idle'dan döngünün *el verme fazındaki* taşıma açısına iniyor; döngü ortalamasına değil.
- **8 TIP dönüş klibi:** V2.11 ayarlarıyla, özgün kaynaktan aynen yeniden yazıldı.
- Yalnız kol zinciri değişti: gövde/bacak/kök okuması 0.0° / 0.0 cm.
- **Veritabanı temizliği:**
  - Rollbacks kopyalarından `BranchIn` kaldırıldı.
  - Fazla girişler senkronizasyonla düştü (yürüme 9→8, dönüş 16→8).
  - Diskteki iki veritabanında da Rollbacks başvurusu 0.

### 1.4 Önce / sonra (30 fps; önce = `v212a` V2.11 üretimi, sonra = `v212c`)

| Ölçü | Önce | Sonra |
|---|---|---|
| Döngü sağ kol faz 3, 5 turun her biri (°) | 8.1 / 6.5 / 7.8 / 9.1 / 6.2 | 10.6 / 11.4 / 12.3 / 12.9 / 11.1 |
| Döngüde en düşük sağ / sol (tüm turlar, °) | 6.2 / 8.5 | 9.2 / 9.5 |
| Uzun idle (5.6 s, sağ ayak): yürüyüş sağ açı / en yakın sağ dirsek | 10.1° / 19.9 cm | 11.0° / 20.9 cm |
| Kısa idle (2.7 s, sağ ayak) | 10.1° / 19.9 cm | 12.4° / 21.0 cm |
| Dur → W (sol ayak; bekleme 1.6 / 0.9 s): sağ en yakın dirsek | 18.9 / 18.9 cm | 21.2 / 20.1 cm |
| Dur → W (bekleme 1.8 / 0.4 / 1.6 s): sağ en yakın dirsek | 18.9 / 19.2 / 19.1 cm | 21.2 / 20.4 / 20.3 cm |
| Dur → W: başlangıçtan +1.16 s sonra sağ kol | 7.8°'ye dalış | dalış yok; 12–14.7° → döngü |
| Yerinde 90 sağ / sol / 180 / yavaş → W: yürüyüş sağ açı | 9.1–9.8° | 11.0–11.5° |
| Aynı dört dizi: sağ en yakın dirsek | 19.0–20.5 cm | 21.0–21.1 cm |
| Kısa bas → bırak → tekrar bas: sağ en yakın dirsek | 22.5 / 22.0 cm | 22.7 / 22.0 cm (kapanma yok) |

- Sağ kol "içeride" süresi (dirsek hem idle'ın hem yürüyüşün 1 cm içinde): bütün başlangıçlarda 0.00–0.28 s (önce 0.00–0.51).
- Bir koşuda 0.54 s görünüyor; bu 0.5 cm'lik eşik farkı (bkz. `arms_before.txt` / `v212c` çıktıları).
- **Kol açısal hızı** en çok 85–186°/s: doğal salınım. Önceki `w` ölçüsü birim olmayan vektör yüzünden 0'a kırpılıyordu; düzeltildi.
- **El–kalça açıklığı** her başlangıçta en az +11.0 cm: gövdeye/kıyafete temas yok.
- **Omuz kalkması** −2.1..+1.9 cm; dirsek bükümü 1..39°. Kolu geride tutma, aşırı açılma ya da bilek/dirsek burulması ölçülmedi.

### 1.5 Kalanlar ve görsel kontrol
- **Kademeli yaklaşma:** sağ kolun idle açısı 14–17°, yürüyüş ortalaması ~12°. Kol ~1.3 s içinde kademeli olarak ~3° gövdeye yaklaşıyor; ani değil.
- **Doğal en düşük nokta:** döngüdeki en düşük sağ değer (9.2–10.3°, faz 8), kolun kalçanın yanından geçtiği an. Sol kolda yarım tur kaymış aynı nokta var.
- **Kısa basış:** kısa basışın durma klibinde sağ kol 18°'ye açılıyor, sonra yürüyüşte 13°'ye dönüyor. Bu durma içeriğinden geliyor; değiştirmedim.
- **Görüntü:** `pub/vid/arms_*` (önce = V2.11 son yakalamaları, aynı senaryo ve kamera). Benim bakışım §8'de.

### 1.6 Geri alma
- **Kollar ve veritabanları:** `checkpoint/baseline_v211/` (V2.11 hali) veya `checkpoint/pre_dbclean/` (temizlik öncesi). Editör kapalıyken kopyalanır.
- **Önemli:** veritabanı temizliği geri alınırsa tekrar sorunu da geri gelir.

## 2. Yerinde dönüş (TIP) rahat stil
- **V2.11 kolları korundu:** hızlı dönüş ölçüleri V2.11 son koşusuyla aynı (fark ≤0.5°). Dönüş veritabanının özgün kopyaları kaldırıldığı için artık hep V2.11 kolları oynuyor.
- **Stil, ayrı ayrı** (`tip212.py`):
  - kollar idle'ın +0..+13° üstünde, el en çok 10.8 cm dışarıda;
  - omuz kalkması ≤3.5 cm;
  - gövde yana 4–10.7°, öne −0.3..5.7°;
  - pelvis düşüşü ≤2.4 cm;
  - her ayakla bir adım (2–9 cm kalkış).
  - Gövdenin yana yatması AAMS dönüş içeriğinden geliyor; değiştirmedim. "Aksiyon tavrı" hâlâ görünüyorsa sahibi bu.
- **Zincirler:**
  - **Dönüş bitmeden W** (sağ/sol 90, 180): montaj 0.12–0.54 s'de kesiliyor; başlangıç geçiş klibi devralıyor. İlk 1.2 s kollar idle'ın en çok +2.4° üstünde, el–kalça ≥12.4 cm. Dönüş sonrası başlangıç bozulmuyor.
  - **Dönüş → ters dönüş** (0.5 / 0.7 s sonra): ikinci dönüş birincinin bitmesini bekliyor; tepki 1.8–2.0 s. Sahibi `GR_UpdateIdleTurn` montajının kesilememesi. **Kalıntı, değiştirilmedi.**

## 3. Geri yürüme — gerçek tuş dizileriyle
### 3.1 Okunan gerçek eşleme
- **`IMC_BC_Player`:** W → IA_Move +Y, S → −Y, A → −X, D → +X; LeftShift → `IA_Ranger_GaitShift`.
- **`IA_Move` birikim kuralı `TAKE_HIGHEST_ABSOLUTE_VALUE`:**
  - Eksen başına son eşleme kazanıyor; **W+S birlikte basılıyken girdi S oluyor**, sıfır değil.
  - Kayıtta CMC ivmesi ve `CR_Backpedal` aynı karede değişiyor.
- **Geri niyet** (`GR_Impl_CR_UpdateBackwardIntent`):
  - Girdi kameraya göre −0.35 iç çarpımdan geride ise devreye giriyor.
  - Geri azami hız: 300 (Shift), 245 (tempolu), 125 (yürüme).
- **Harness:** artık tuşları `Input.+key/-key` ile mapping context üzerinden basıyor (`qa_pie.key_step`). Kayıtta basılı tuşlar, Shift, `CR_Backpedal`, hedef/görünen yürüyüş türü, azami hız, veritabanı/klip ve gerçek hız aynı satırda.

### 3.2 Denenen 13 dizi (`v212d_k_*`, `back212.py`)

| Dizi | Sonuç |
|---|---|
| W bırak → 0.1 s sonra S (Shift basılı) | Fren pivotu 0.6 s; ileri yüz dönük geri koşu ≤300; kapsül dönmüyor; ileri klip yok |
| S bas → W 0.15 / 0.40 s sonra bırak | Örtüşme = S. Geri koşu ≤300. **İlk karede 490→416 cm/s (2400–2700 cm/s²), sonra 730–790** |
| Shift bırak → S → Shift tekrar | ≤300; sorun yok |
| Shift'siz S | Geri tempolu ≤245 |
| S+A / S+D | Geri-sol / geri-sağ koşu klipleri ≤300 |
| S → fren bitmeden W | İleri yeniden hızlanma; geri hareket yok (doğru) |
| **Depar D kesişi → S** | **0.44 s kesiş veritabanı kilidi; kesiş içinde başka kesiş klibine atlama; pelvis 4.4 cm / 79 m/s²** |
| Yürüme → S, örtüşmeli | Geri yürüme ≤125 |
| Tempolu → S | ≤245 |
| S basılıyken kamera 90° döner | Kapsül kamerayı izliyor (en çok 22°), geri koşu ≤300 |

- **Hiçbir dizide:**
  - geri hız onaylı sınırı aşmıyor;
  - ileri depar/koşu klibi geriye taşınmıyor;
  - S, "kamera 180 + W" gibi davranmıyor (kapsül kameraya göre 0°).

### 3.3 Bulunan iki kusur
1. **Tam deparda S'ye basılınca (W basılı olsa da olmasa da) ilk karede ~73 cm/s düşüş.**
   - Sahip denemeleri:
     - "sürtünme bir kare gecikmeli" hipotezi: düzeltme (F1, `RedirectInputNow`) ölçülebilir etki yapmadı;
     - V2.5 dönüş hız kaybı: `TurnSpeedLoss` 0 ile de değişmedi.
   - **Sahip bulunamadı.** F1 geri alındı (`BP_GR_Player` / profil / alt pawn V2.11 dosyalarıyla aynı).
   - O karelerdeki sıçrama ≤34 m/s². **Kalıntı.**
2. **Depar kesişi sırasında S:**
   - Bileşenin yanal bölümü kesiş sınıfını ilk 0.3 s'de kilitliyor. Geri isteği tanımadan 0.44 s kesiş veritabanını tutuyor ve MM bu sırada başka kesiş klibine atlıyor.
   - Asgari düzeltme denemeleri:
     - **F2** (yeni niyet 60–120° sapınca bölümü kırmak): `k_cut_back` en kötü 76 → 62. Ama hızlı ardışık depar kesişlerinde V2.10'un destek adımlı kesiş kliplerini virajlara çevirdi; bu yüzden alınmadı.
     - **C1** (geri isteğini ters dönüş köprüsüne yönlendirmek): geri bayrağı girdiden 1–3 kare sonra geldiği için bu dizide tetiklenmedi.
   - **Kalıntı, düzeltilmedi.**

Bu iki durum dışında: **"Bu koşullarda yeniden üretilemedi"**. Sınır: düz zemin, 30 fps, 13 dizi, her biri 1 koşu.

## 4. Depara itiş — giriş/çıkış ve yanlış tetikleme
### 4.1 Doğrulanmış sahipler (V2.11 üretimi, gerçek tuşlar, `push212.py` + `contactslip.py`)
- **Hızlı yürüme (0.23–0.25 s, 150–230 cm/s):**
  - V2.11 itiş rotası yalnız tempolu/depar veritabanlarını yönlendiriyordu.
  - İtiş bayrağı ~150'de açılınca, gösterilen yürüyüş türü koşuya geçene kadar (210) yürüme döngüsü hızlanmış oynuyordu.
- **İtiş girişi:**
  - MM `RR_Start`'a (duran koşu başlangıcı) ortasından (0.43 s) giriyor; gövde 0.1 s'de 16.5° öne kopuyor.
  - Kaynak klibin kendi ilk itiş adımı 12.3 cm kayıyor.
- **Yanlış tetikleme:**
  - Shift'siz yürüme başlangıcında 0.12–0.21 s itiş bayrağı açılıyordu (yürümede görünmez).
  - Shift dokunuşuyla tempolu başlangıçta itiş açılıyor; `RR_Start`'ın başına (0.07 s) girip sağ ayak 45.6 cm kayıyor. Bu "ikinci başlangıç".
  - Ters dönüş sonrası itiş bitip 0.09 s sonra yeniden açılıyor (çift itiş).
- **Tempolu → depar:** itiş yok; tempolu döngü 300→415 boyunca 0.6 s hızlanmış oynuyor, depar duruşu 415'te geliyor.

### 4.2 Değişiklik (ABP + itiş içeriği, varsayılan olarak üretimde)
- **`SHM212_Guard` (EventGraph, `SHM211_PushGate` sonrası):**
  - İtiş yalnız depar niyetiyle (azami hız >400 = Shift tutuluyor).
  - Bir itiş bitince 1 s yeni itiş yok; hız kol hızının (200) altına yeniden düşerse olabilir.
  - İtiş yürüme bandında (110–210 cm/s) başladıysa "yürüyüşten itiş" olarak kilitleniyor.
- **Rota (EventGraph):**
  - Yürüyüşten itiş → `PSD_SHM212_GaitPush`.
  - Dururken başlangıç / ters dönüş sonrası → V2.11 `PSD_RR_Start` (değişmedi).
- **`Update_MotionMatching`:** itiş sırasında yürüme `SetDatabaseToSearch`'ü de itiş veritabanına dallanıyor.
- **`PSD_SHM212_GaitPush`:**
  - AAMS `M_Neutral_Transition_Walk_to_Sprint_L/Rfoot` ve `Run_to_Sprint_L/Rfoot`'un projeye ait kopyaları.
  - Satıcının kendi giriş pencereleri: yürüme 1.01–1.45 s, koşu 0.56–0.81 s. Satıcı orijinalleri değişmedi.
  - Kopyalardaki yabancı `BranchIn` kaldırıldı.
- **Duruş bake'i (`v212_push_posture.py`, yalnız bu dört kopya):**
  - Satıcı klibi oyunda bir koşucunun blok çıkışı gibi görünüyordu: tepe öne eğilme 50.4°, pelvis 21.4–22.9 cm iniyor (`img/push_walk_side_before_after.jpg`, orta satır). Bunu üretimde bırakmadım.
  - Satıcı orijinalinden tek geçişte kopyaya yazıldı:
    - gövdenin 20°'yi aşan öne eğilmesinin %75'i geri alındı; itişten sonra taban 29°'ye dönüyor, yani depar döngüsüne giriş değişmiyor;
    - pelvis 88 cm tabanına doğru kaldırıldı;
    - bacaklar aynı ayak konumlarına yeniden çözüldü; ayak hatası 0.0 cm;
    - başın bakışı korundu.
  - Kaldırma, her karedeki bacak erişim sınırının (%99.5) yumuşatılmış alt zarfı:
    - Ayak kopuşunda arka bacak düz olduğu için kare kare sınır, pelviste 0.1 s'de 6 cm'lik zıplama yapıyordu; bu ilk denemede görüldü ve yumuşatmayla giderildi.
    - V2.10 `leg_guard` yazımda geçti.
  - Ara deneme (tek geçiş, yumuşatmasız, oyunda 40.5° / 14.8 cm) yeterli bulunmadı ve üzerine yazıldı.
- **`SHM211_PushMaxSpeed` 420 → 485:** itiş depar gösterimi başladıktan sonra bitiyor; arada tempolu kare kalmıyor.

### 4.3 Önce / sonra

Önce = V2.11 akışı aynı içerikte (`v212k_*_b`), sonra = son kayıtlı üretim (`v212n_*`). Her biri 2 koşu, 30 fps.

| Ölçü | Önce (V2.11) | Sonra (V2.12) |
|---|---|---|
| Yürü → Shift: hızlı yürüme | 0.23–0.24 s (220 cm/s'ye kadar) | 0 |
| Yürü → Shift: itişe giriş | 230 cm/s, `RR_Start` 0.43 s (itişin ortası) | 141–149 cm/s, `Walk_to_Sprint` 1.03 s (son yürüme adımı) |
| Giriş basışı kayması (±0.1 s) | 7.1–12.6 cm | 9.6–10.9 cm |
| Gövde öne eğilmesi, en hızlı değişim | 16.6–17.0°/0.1 s | 11.4–12.0°/0.1 s (kademeli) |
| Gövde öne eğilmesi, tepe | 35.1–35.2° | 35.6–35.8° |
| Pelvis inişi (itiş öncesi → en alçak) | 9.5–9.7 cm | 11.9–12.8 cm |
| Depar döngüsüne çıkış | 424–426 cm/s, 4.5–6.1 cm kayma | 488–490 cm/s, 0.4–2.0 cm kayma |
| İtiş penceresindeki basışlar (`contactslip`) | toe-off 11–15 cm | toe-off ≤ 6.8 cm, ortası ≤ 4.6 cm |
| Bütün koşu `contactslip` toplam en çok (normal / erken Shift) | 23.2–29.5 / 23.8–25.3 cm | 10.7* / 13.9–14.6 cm |
| Yürümede sahte itiş bölümü (Shift'siz başlangıç) | 1 (0.12–0.15 s) | 0 |
| Kısa Shift bırak-bas, W+A↔W+D: yeniden tetiklenme | 0 | 0 |
| Ters dönüş → W: itiş bölümü | 2 (ikinci başlangıç) | 1 |
| Diz ekseni sıçraması (>30°, itiş koşuları) | 0 | 0 (en çok 11–14°) |

\* İkinci koşuda toplam en çok 31.5 cm. Bu itişte değil: koşunun sonunda tuş bırakılınca depar durma klibindeki bir ayak kopuşu (t = 10.76 s).

**Karşılaştırma için:**
- Dururken Shift+W (V2.11 `RR_Start`, değişmedi): 36.9–37.0° ve 16.4–17.1 cm.
- Yani yürüyüşten itiş artık karakterin mevcut duruştan koşu başlangıcıyla aynı duruş ailesinde.

### 4.4 Kalanlar
- **Giriş kayması:** geçiş karesinde ±0.1 s içinde 10–11 cm (önce 7–13).
  - Destek fazına bağlı başlatma (bileşenin destek tarafı değiştikten sonraki 0.12 s) denendi. İtişi 210 cm/s'nin üstüne kaydırdı veya hiç başlatmadı; kapalı (`SHM212_PhaseGate` 0).
- **Pelvis inişi:** V2.11'den 2–3 cm daha fazla.
  - Daha fazla kaldırma, itiş adımında arka bacağın erişim sınırına takılıyor.
  - Daha azı için adım uzunluğunu (ayak konumlarını) değiştirmek gerekir; bunu yapmadım.
- **Ters dönüş → W itişi:**
  - Tek itiş var (önce iki).
  - Ama hâlâ `RR_Start`'ın ortasından (0.41–0.43 s) giriyor ve kısa (0.2–0.3 s, 219 → 300 cm/s).
  - Giriş basışı 6–10 cm kayıyor.
- **Tempolu → depar küçük itişi:** denendi (F3b), alınmadı.
  - Depar sırasında kısa Shift bırak-bas iki kez yanlış itiş tetikledi.
  - MM ayrıca tempolu koşudan yürüme→depar klibinin yürüme adımına giriyordu.
  - Tempolu → depar önceki gibi itişsiz. **Kalıntı.**
- **Stil:** "Belirgin ama karaktere uygun" kararı senin.
  - Ölçü olarak V2.11 yürüyüş itişi ve duruştan başlangıçla aynı aralıkta.
  - Görsel: `img/push_walk_side_before_after.jpg`.
- **Geri alma:**
  - Yalnız duruş: `checkpoint/pre_posture/` dört kopya (editör kapalıyken).
  - Bütün itiş: `SHM212_WalkPush` 0, `SHM211_DB_Push` = `PSD_RR_Start`, `SHM211_PushMaxSpeed` 420.

## 5. Toparlanma adayı — üretildi, kabul edilmedi
### 5.1 Olay, niyet ve destek
- **Olay:** düz zemin; depar W → D (sert sağ kesiş); kesişin itişi bitmeden, 0.15 / 0.35 / 0.6 s sonra A (ters yön). Sol ayna da var.
- **Niyet:** oyuncu karşı tarafa gitmek istiyor, yani **planlı yön değişimi**. Bu durumda denge kaybı yok; sendeleme beklenmiyor.
- **Ölçülen destek düzeni:**
  - istek anında kesiş klibinde sağ ayak basılı (1.03–1.17 s);
  - hız 310–350 cm/s, yön +40..+50°.

### 5.2 Mevcut üretim (aday kapalı)
- **Sağ kesiş → A:** kesiş bölümü 0.3 s daha sürüyor. Kapsül sola dönerken animasyon sağa dönmeye devam ediyor. Ardından MM sol kesiş klibine 113 cm/s'de giriyor.
- **Destek ayakları kayıyor:** en çok 8–27 cm; sol aynada olay anında 99 cm; erken/geç isteklerde 96–108 cm.
- **Kollar/gövde:** kollar +20..+40° açılıyor; gövde yuvarlanma/eğilme 21–26°, geç istekte eğilme 51°.
- **Sonrası:** tempolu döngü → koşu başlangıcı ile ikinci bir başlangıç.

### 5.3 Denenen aday
- **C1:** bölüm içinde girdi bir karede >120° dönerse, ters dönüş olarak bir kez yeniden yönlendirmek.
  - Sınıf 2, köprü karesi, taraf = hız × istenen yön.
  - İlk sürüm köprüyü tetiklemedi; iki ayrı sebep bulundu ve düzeltildi:
    - DSL `bind` saf ifadeleri her kullanımda yeniden hesaplanıyor;
    - bölüm içinde `SHM_RedirectHold` MM aramasını 0.25 s'de bire kısıyor ve `PostSelection` eski veritabanını geri yazıyor.
  - Sonra köprü çalıştı. Ama ters dönüş veritabanında MM geri pivotu / geri koşuyu seçti.
- **C1b:** yalnız 180° depar dönüşlerinden oluşan aday veritabanları (`PSD_SHM212_CutRev_L/R`).
  - Kopyalar, yalnız fren evresinde girişe izinli: `L_180_Lfoot` (sağ fren → sol pivot/dengeleme → sağ itiş), `R_180_Rfoot`, `R_180_Lfoot`.
  - `L_180_Rfoot` alınmadı: basışları 22–56 cm kayıyor.

### 5.4 Sonuç (indekslenmiş veritabanlarıyla geçerli koşular `v212j_*`)

| Ölçüt | Sonuç |
|---|---|
| Yük taşıyan destek ayağı | **Yok:** fren basışı 48–132 cm kayıyor |
| Görünür, zemine uygun ek adım | Pivot adımı var ama 31–45 cm kayıyor |
| Gevşek gövde/kol tepkisi | Sağ ve erken: yuvarlanma 21–23° → 13°, eğilme 26° → 12–22°. **Sol ayna kötüleşiyor (36.8°)** |
| Bağlantılı itiş | **Yok:** +0.46 s'de bölüm bitince tempolu döngü → koşu başlangıcı (ikinci başlangıç) |
| Normal geniş virajda tetiklenme | 0 (iki viraj senaryosu) |
| Yanlış tetiklenme | **Var:** düz depar → S ve ardışık ters dönüşlerde bileşenin kendi bölümünde de tetikleniyor; kesiş → S'de ise geç gelen geri bayrağı yüzünden tetiklenmiyor |

- **Bozulma noktası:** kaynak 180° fren 727 cm/s'den ~0.3 s'de duruyor (~2400 cm/s²); oyundaki kapsül ~300 cm/s'den ~800 cm/s² ile yavaşlıyor. Animasyon sert fren gösterirken kapsül kaymaya devam ediyor, yani ayak yükü taşımıyor.
- **Eksik kaynak hareket:**
  - oyun depar hızında (300–490 cm/s, ≤1000 cm/s²) bir dengeleme adımıyla frenleyen ve yeni yöne iten 180° yön değişimi;
  - veya tepki süresince kapsülü klibin kök hareketine bağlayan bir mod.
  - Projede ve satıcı paketlerinde önizlemesini gördüğüm içerikte bu yok. Görmediğim paketler için bir iddiam yok.
- **Üretim:** aday uyuyor; bayraklar 0 (`SHM212_RdRev`, `SHM212_RevTurnMode`). Kod ve veritabanları yerinde.

## 6. Kamera–girdi koruması (son kayıtlı üretim, `v212z_d_*`, `dirtl.py`)
- **Ekran (kamera) − girdi referansı (kontrol yönü), en büyük fark:**
  - idle'da kamera dönüşleri arasında W: 0.0°;
  - yürürken kamera 120°/s dönerken: 0.1°;
  - deparda: 1.2°.
  - V2.11 ile aynı.
- **Hız yönünün istenen yöne oturması:** 0.18–0.50 s.
- **Değişmeyenler:**
  - idle kamera serbestliği (`CameraIdleOrbitMaxYaw` 180);
  - FOV / mesafe / omuz;
  - kameranın gövdeyi izlemesi.

## 7. Diz / zemin ve V2.10–2.11 korunması
- **Bake okuması:** kol bake'i dışında bacak, pelvis ve kök izleri değişmedi (okuma 0.0° / 0.0 cm).
- **Diz ekseni sıçraması** (`calfjump.py`, >30° kare sayısı):
  - itiş, kol, dönüş, geri ve zemin koşularında 0; yeni itiş içeriğinde en çok 11–14°.
  - **Düzeltme (ilk taslaktaki "bütün koşularda 0" yanlıştı):** W+A↔W+D depar senaryosunda (`p_swawd`) depar kesişi girişinde tek karede 31–36° var.
    - V2.11 üretim koşusunda da var (`v212d_p_swawd_base`: 31.5 / 32.5°); V2.12 değişikliklerinden gelmiyor. **Kalıntı, düzeltilmedi.**
  - Aynı senaryoda 45–74° görünen değerler sıçrama değil: ölçüm koşusunda 0.15–0.31 s'lik kare takılması; açı, o boşluk boyunca biriken dönüş.
- **Tek ayak yükseltide idle** (`strip_idle.py`, V2.11 son koşusuna karşı):
  - pelvis alçak/yüksek zeminin üstünde 95.5 / 85.5 cm (aynı);
  - diz bükümü 18.3 / 57.1° (aynı);
  - ayak–zemin aralığı aynı.
- **Eğimde dur → dön → başla** (`contactslip.py`): V2.11 ile aynı düzeyde (duruş ortası en çok 17.5 / 17.9 cm, basış 6.4 / 6.5 cm).
- **Ölçüm bayrağı hatası (bulundu, giderildi):**
  - A/B ve yakalama betiğinin taban ayarlarında `SHM212_RdRev` / `RevTurnMode` 1.0 kalmıştı; kayıtlı üretimde 0.0.
  - Bu yüzden ilk "son üretim" yakalamalarından ters yönlü olanlar (W bırak → S, S+A, ters dönüş sonrası itiş, kesiş → ters istek) uyuyan toparlanma adayıyla çalışmıştı. Kanıtta `SHM212_RevOn` ve `CutRev` veritabanı görülüyor.
  - Taban düzeltildi (`v212_ab3.sh`). Bu sahneler gerçek üretimle yeniden çekildi (`cap_fix212.sh`); yanlış kareler `invalid_caps_rdrev1/` altında saklı.
  - Etkilenmeyenler: geri ölçümleri (`v212d/e/f`) ve toparlanma ölçümleri (`v212h/i/j`). Hepsinde aday ya kapalıydı ya da açıkça bir varyanttı.
- **Üretim değerleri** (`verify_prod212.txt`):
  - CutMode 2, TipOld false, HC_Off false, StopMode 1, StartMode 0, CutTail 0.8;
  - SL = `PSD_SHM210_SprintCut`, `SHM211_PushMode` 1;
  - `CameraIdleOrbitMaxYaw` 180, `SprintCutFaceLead` 15, TurnLatAccelMax 1400, CutLatAccelMax 650.

## 8. Benim görsel incelemem (yakalama kareleri; kabul değil)
- **Uzun idle → W** (`img/arms_long_start_*`):
  - İki sürümde de kol idle'daki gibi yanda asılı başlıyor; ilk adımda gövdeye yapışma, tutulma, yeniden açılma görmüyorum.
  - Bu koşudaki fark ince (2–3°, 1–2 cm). Asıl kazanç ölçülen dalışlarda (dur → W, dönüş → W, döngü turları).
  - Dur → W için V2.11 yakalaması başlangıç anını kapsamıyor; orada önce/sonra sayılarla, görüntü yalnız sonrası.
- **Düz yürüyüş, 6 tur yandan** (`img/walk_loop_cycles_side.jpg`): kollar her turda doğal ileri-geri; geride tutma veya tek turda daralma yok.
- **İtiş** (`img/push_walk_side_before_after.jpg`, 3 satır):
  - Ham satıcı içeriği (orta satır) bir koşucunun blok çıkışı gibiydi; üretimde bırakmadım.
  - Duruş bake'inden sonra (alt satır): orta düzey öne eğilmeyle hızlanan bir koşu; baş ileri bakıyor, dizde/bacakta tuhaflık görmüyorum.
  - Bana V2.11 itişiyle (üst satır) aynı ailede görünüyor. Fark: son yürüme adımından kesintisiz çıkıyor. Kabul senin.
- **Geri** (`img/back_and_reversal_sheet.jpg`, gerçek üretimle yeniden çekildi):
  - Deparda W bırak → S'de fren pivotu (`A_LR_Run_Pivot_F_B`) kalçayı 17.2–19.1 cm indiriyor (iki temiz koşu); neredeyse çömelme. V2.11'de aynı düzey (19.3 cm).
  - Senin saydığın geri ölçütlerini ihlal etmiyor, ama "aksiyon tavrı" görüntüsü veriyor. Geri şikâyetinin görsel kaynağı bu olabilir.
  - **Değiştirmedim; ayrı içerik işi.**
- **Depar kesişi → A (toparlanma olayı, üretim; gerçek üretimle yeniden çekildi):**
  - A'ya basıldığı anda kesiş klibinin kendi frenlemesinde pelvis 14–17.7 cm iniyor.
  - Ardından sol 90 kesiş klibi ~110 cm/s'de, sonra tempolu → koşu başlangıcı (+1.16 s; ikinci başlangıç).
  - Doğal bir yakalama adımı değil (§5).
- **Yerinde sol 90 → W yakalaması:** 73 m/s² "sıçrama", 0.125 s'lik yakalama takılmasından. 30 fps ölçüm koşusunda 0. Videoda o anda bir kare atlaması görünebilir; animasyon değil.

## 9. Değişen dosyalar, ayarlar, geri alma
**Animasyon içeriği** (yalnız kol izleri; okuma: gövde/bacak/kök 0.0° / 0.0 cm):
- `/Game/GraceRanger/Animations/LocomotionBehavior/A_LB_Walk_Fwd`;
- `.../LookStrafe/Sample/A_LS_M_Relaxed_Walk_Start_F_Lfoot`, `_Rfoot`;
- `/Game/GraceRanger/SHME/Animations/Turns/SHM_M_Neutral_Stand_Turn_{045,090,135,180}_{L,R}`. Bunlar V2.11 ayarlarıyla, özgün kaynaktan yeniden yazıldı.

**Veritabanları:**
- `PSD_LB_WalkLoops` 9 → 8 giriş; `PSD_SHM_TurnInPlace` 16 → 8 giriş. Etiket `V212A`, yeniden anahtarlandı.
- `/Game/ActionAdventureMovementS/Rollbacks/SHME_V211_Arms_Before_20261016/*`: 9 kopyadan `PoseSearchBranchIn` kaldırıldı; kemik izleri aynı.

**Yeni varlıklar** (`/Game/GraceRanger/SHME/Animations/V212/`):
- `PSD_SHM212_GaitPush` + `SHM212_Walk_to_Sprint_{L,R}foot`, `SHM212_Run_to_Sprint_{L,R}foot`: AAMS kopyaları; satıcı orijinalleri değişmedi. Kopyalarda duruş bake'i var: pelvis, bacaklar, omurga, boyun, baş; ayak konumları aynı (§4.2).
- `PSD_SHM212_CutRev_L/R` + `SHM212_Sprint_Turn_L_180_Lfoot`, `_R_180_Rfoot`, `_R_180_Lfoot`: uyuyan aday.

**ABP** `/Game/GraceRanger/Experimental/BodyInertia/Sandbox/Animations/ABP_GR_MotionMatchingBase` (+ alt ABP derlemesi):
- `SHM212_*` üyeleri ve `SHM212_Guard` fonksiyonu (DSL; kaynak `install_guard2_src.lisp`).
- EventGraph:
  - `SHM211_PushGate` → `SHM212_Guard` → C1b rota dalı → itiş dalı → yürüyüş/duruş itiş rota dalı.
- `Update_MotionMatching`:
  - `K2Node_CallFunction_88` önüne yürüme itiş dalı + `SetDatabaseToSearch` kopyası;
  - köprünün SRL/SRR okumaları `SHM212_RouteSRL/SRR` üzerinden.
- **Varsayılanlar:** `SHM212_WalkPush` 1; `SHM211_DB_Push` = `PSD_SHM212_GaitPush`; `SHM211_PushMaxSpeed` 485; `SHM212_DB_PushStand` = `PSD_RR_Start`. `SHM212_RdBreak` / `RdRev` / `RevTurnMode` / `JogPush` / `PhaseGate` 0.

**Değişmeyenler:**
- `BP_GR_Player`, `BP_GR_MotionProfile`, `BP_PBI_Player`, `DA_GR_LocomotionBehavior` V2.11 dosyalarıyla bayt düzeyinde aynı (F1 denendi, geri alındı).
- Karakter anatomisi, iskelet, kıyafet, üretim haritası, kamera (FOV / mesafe / omuz), CMC hız/ivme değerleri.

**Geri alma:**
- **Hızlı** (yalnız itiş): `SHM212_WalkPush` 0, `SHM211_DB_Push` = `PSD_RR_Start`, `SHM211_PushMaxSpeed` 420 → V2.11 itişi.
- **İtiş duruş bake'i:** `checkpoint/pre_posture/` (dört kopyanın bake öncesi hali). Editör kapalıyken kopyalanır.
- **ABP tam:** `checkpoint/baseline_v211/` (V2.11) veya `checkpoint/pre_promote/` (V2.12 terfi öncesi). Editör kapalıyken kopyalanır.
- **Kollar ve veritabanları:** `checkpoint/baseline_v211/` (kollar + iki veritabanı); `checkpoint/pre_dbclean/` (temizlik öncesi veritabanları ve Rollbacks kopyaları). Veritabanları geri alınırsa tekrar sorunu geri gelir.
- **Yeni V212 varlıkları:** referans dışı bırakıldığında silinebilir. `ABP` geri alınınca hiçbir şey onlara başvurmaz.

**Araçlar** (`Tools/SHME_V212_20261017/`):
- **Bake:** `v212_arm_bake.py` (`make_v212_bake.py` ile üretilir).
- **Kurulum:**
  - `install_v212_guard.py`, `install_v212_guard2.py`, `install_v212_pushroute.py`, `install_v212_cutrevroute.py`;
  - `build_v212_gaitpush.py`, `build_v212_cutrev.py`;
  - `promote_v212.py`, `verify_prod212.py`;
  - `v212_push_posture.py` (itiş duruş bake'i; `v137_bake_posture.py` kopyası + kaynak/yumuşatma);
  - uygulanmayan: `install_v212_rdnow.py` (F1).
- **Ölçüm:**
  - `arms212.py`, `loop_arms212.py`;
  - `back212.py`, `tip212.py`, `push212.py`, `pushpose212.py`;
  - `recov212.py`, `recov_src.py`.
- **Koşum:**
  - `v212_run.sh` (gerçek tuş senaryoları);
  - `v212_ab.sh` / `v212_ab2.sh` / `v212_ab3.sh`;
  - `ab_safe*.sh`, `cap_final212.sh`, `cap_fix212.sh` (yeniden çekim), `media212.sh`.
- **Probe'lar:** `Saved/Codex/SHME_V212_20261017/req/`.

## 10. Medya (`pub/`)
- **`img/`:**
  - `arms_long_start_before_after.jpg`: uzun idle → W, aynı oyun zamanında V2.11 / V2.12.
  - `arms_long_start_upper_zoom.jpg`: üst gövde yakın.
  - `push_walk_side_before_after.jpg`: yürü → Shift, yandan; V2.11 / ham satıcı içeriği (atıldı, yalnız karşılaştırma için) / V2.12 son.
  - `walk_loop_cycles_side.jpg`: düz yürüyüş, döngü turları.
  - `back_and_reversal_sheet.jpg`: W bırak → S, kesiş → S, kesiş → A (üretim).
- **`vid/`:**
  - **GIF:** gerçek hız, her 2. kare.
  - **AVI:** ölçülen yakalama hızında, oynatma süresi = simülasyon süresi.
  - İtiş ve toparlanma için ayrıca 1/3 hız.
  - Adlar `media212.sh` listesinde.
- **Yakalama hızı:** 20–25 fps (30 fps tavan). Bir kare takılması (0.115–0.125 s) sıçrama ölçüsüne yanlış değer verebiliyor; bu yüzden sayılar 30 fps ölçüm koşularından.
- **Yeniden çekim:** ters yönlü sahnelerin ilk çekimleri uyuyan aday açıkken yapılmıştı (§7). Gerçek üretimle yeniden çekildi; yayımlanan bütün 28 çekimin kanıtında aday izi yok.
- **Test görünümü:** yalnız test dünyasında, görünen gövdede opak gri kil. Kıyafet, yüz ve saç üretim görünümünde. Hiçbir kare kesilmedi veya düzenlenmedi.

## 11. Beceri eklemeleri (yalnız doğrulananlar)
`sphirus-human-motion-engine` (senkron: `sync_claude_skills.py`, 0 hata):
- **`architecture.md`:** V2.12 üretim düğümleri, uyuyan modlar, geri alma.
- **`motion-diagnosis.md`:**
  - "kol düzeltmesi oyunda yok" = veritabanı tekrarı;
  - döngünün her turunda kol daralması;
  - geri tuşlarında birikim kuralı ve ilk kare düşüşü (sahip açık);
  - kesiş içinde S kilidi;
  - itişin üç sahibi.
- **`authoring.md`:**
  - karşı kol tabanı bake'i;
  - `BranchIn` kopya tuzağı;
  - DSL `bind` yeniden hesaplama tuzağı;
  - UE 5.8 `Multiply_VectorFloat` tuzağı.
- **`mm-coverage.md`:**
  - satıcı giriş pencereli itiş içeriği ve duruş bake'i (oyun ölçüsüyle kalibrasyon: oyunda eğilme ≈ klip + ~11°, pelvis ~9 cm aşağıda; yumuşatılmış erişim zarfı);
  - duruş başlangıcını ayırma;
  - destek fazı denemesi;
  - toparlanma adayının bozulma sebebi;
  - köprü arama kısıtı.
- **`validation.md`:**
  - gerçek tuş harness'ı ve yeni araçlar;
  - çalışan bash betiğini düzenleme tuzağı;
  - yeni veritabanının ilk kullanımda indekslenmesi;
  - A/B ve yakalama taban bayrakları kayıtlı üretime eşit olmalı (yayından önce kanıtta uyuyan modların izini tara);
  - bellek yeniden başlatmasında süpürülen runner işi ve asılı bekleyici;
  - `pushpose212.py`.

## 12. Oyun testi
`USER_PLAYTEST_V212.md`. His, görünüm ve kontrol kabulü sende; ben kabul vermedim.
