# SHME V2.51 — kalkışın ilk karesi, ağırlığa göre ilk adım, 180° devri (2026-11-03)

Taban: V2.50 üretimi. Sayılar `TABLES_V251.md`, değişiklikler `CHANGES_V251.md`.
Videolar (60 fps, gerçek hız; aynı oturumda aynı hareket, solda V2.51 düzeltmeleri kapalı = V2.50, sağda V2.51):
- `vid/start45_side` ve `vid/start45_diag`: 45° kalkış
- `vid/startLS_side`: yanal kalkış
- `vid/turn180_diag`: 180° kalkış

**Videoları oynatıp izleyemiyorum**; tek tek kareleri inceledim. Görsel kabul ve oyun hissi NOT_TESTED.

## 1. Kapatılan sorun: duruştan her jog kalkışında ayak ucu batması
- **Ölçüm.** 45° kalkış, yanal kalkış ve geri kalkışta ilk 0,15 s'de iki ayağın topu 4–5 cm zemine giriyordu.
- **Sahip, kare kare.** İstek karesinde aile rotası bir kare geç kalıyor. MM o tek karede vendor yoğun veritabanında arama yapıyor: `PSD_Dense_Stand_Run_Starts` içindeki `af_Loco_Jog_Right/Bwd_Start_AAMS` (V2.50'de bulunan bozuk Candidate retarget'ı: ayaklar aşağı-geri) ya da Shuffle. Bu tek örnek blend stack'e giriyor ve sönerken bozuk ayaklarını harmana katıyor. V2.49 bu durumu yalnız dönüşlü kalkışlar için düzeltmişti.
- **Düzeltme (`SHM251_StartEntry`).** Duruştan jog isteğinin ilk karesinde, rotanın bir sonraki karede zaten arayacağı SHM kalkış veritabanı aranıyor. Vendor varlıklarına dokunulmadı; yeni klip üretilmedi.
- **Sonuç.** Aynı oturumda önce/sonra, 60 FPS:

| kalkış | önce, batma (sol/sağ) | sonra |
|---|---|---|
| 45° | 3,8 / 3,9 cm | yok / yok |
| yanal | 4,4 / 5,0 cm | yok / 1,1 cm |
| geri | 3,9 / 4,0 cm | yok / yok |

20/30/120 FPS ve iki gerçek zaman koşusunda da batma ≤1,1 cm. Kare kontrolü: önce tarafında ayak uçları zemine dikiliyor, sonra tarafında ayaklar düz basıyor.

## 2. Yeni fiziksel davranış: ağırlık durumuna göre ilk adım (`SHM251_StartLoad`)
- **Sorun.** Kalkışta adım atan ayak bileşenin `SupportSide` değerinden seçiliyordu. Bu değer iki ayak yerdeyken son adımın tarafında takılı kalıyor, bedenin o anki ağırlık durumunu yansıtmıyor.
- **Kural.** Duruştan kalkışta adımı yükü taşımayan ayak atar:
  1. Önce ağırlık merkezinin ayaklar arasındaki izdüşümü kullanılır (bileşenin hesapladığı SupportLoad).
  2. Ağırlık merkezi ortadaysa gevşek bacak (topuğu kalkık olan) belirleyicidir. Bu bilgi bekleme klibinden ölçülüp eğri olarak yazıldı (`SHM251_IdleSupport`).
- **Ağırlıklı idle ile sonuç.** Sağ bacak gevşek, ağırlık solda; artık serbest sağ ayak adım atıyor. 30 FPS top-temelli ölçüm:

| | üretim (idle kapalı) | idle açık, önce | idle açık, sonra |
|---|---|---|---|
| w42 kalkışı | 10,2 cm | 19,7 cm | **8,8 cm** |
| taps | 17,3 cm | 19,0 cm | **6,7 cm** |

- **Üretimdeki etkisi.** Normal idle'da ağırlık ortada ve eğri yok, bu yüzden kural seçimi değiştirmiyor; testlerde üretim değerleri birebir aynı. Davranış ağırlıklı idle ve dengesiz duruşlarda devreye girer.

## 3. 180° kalkış sonundaki 60 FPS sıçraması — PARTIAL
- **Kare kare bulunan sahipler.**
  1. MM, her kırpmadan klip sonuna tam 0,30 s kala çıkıyor (129 çıkışın hepsinde). Kırpmanın son 0,30 s'si aday değil, dönüş ise sondan 0,25 s önce bitiyor.
  2. T2 veritabanı tutulduğu için MM tek karelik zıplamalarla diğer kırpmaların ortasına giriyordu (R135 @0,83, R090 @0,63).
  3. Servo yaw'ı kök eğrisinden, devralan V2.38 sözleşmesi dönüş ilerlemesinden yazıyor; bu iki tanımın farkı tek karede 6,4° yaw sıçraması yaratıyordu.
- **Düzeltmeler.**
  - Yaw devri: bırakmadan sonraki 0,35 s içinde yaw en fazla 150°/s ile kapanıyor (`SHM251_YawSlew`).
  - Kırpmalara yalnız ilk 0,25 s'den girilebiliyor (PoseSearch BlockTransition). Zıplamalar kalktı; artık tek bir geçiş var (R180 → CP2).
- **Sonuç.** Omuz pop'u 77–79'dan 73–74 m/s²'ye indi (1,44 cm). Kalan tek karelik pop bu tek geçişin kendisinde; sahibi bu turda bulunamadı.
- **Etkisiz kalan denemeler.** Devam-pozu bonusu (−6) ve TurnDone'ı çıkış eğrisine bağlamak sıçramayı değiştirmedi. İkisi varlıklarda kurulu ama işlevsiz (ExitOn 0).

## 4. j42_lr_p10 regresyonu (12,5 → 17,3 cm)
- **Mekanizma.** V2.49 ile V2.50'nin B turu 410 satırın hepsinde birebir aynı. Fark, V2.50'nin top pivotu değişikliğinden sonra başlıyor.
- **Neden.** Kalkış ve T2 veritabanları aynı normalizasyon kümesini (PSN_SHM) paylaşıyor. Kırpmalardaki ayak konumlarının değişmesi tüm maliyetleri kaydırdı. Koşu 6,9 s'de, değiştirilmemiş bir 90° kesme klibinde 0,002 s farkla ayrışıyor ve sonra başka bir trajektoriye kayıyor; 17,3 cm'lik olay değişmemiş bir koşu döngüsünde (A_CT_Jog_Right).
- **Durum.** V2.51 üretiminde j42 = 10,9 cm (V2.49: 12,5). Aynı kaotik ayrışma j40'ta 60 FPS'de (9,9 → 18,7) ve jstart'ın ilk koşu döngüsünde de görülüyor. Bunlar değiştirilen kliplerde değil.

## 5. Ağırlıklı idle — yine üretime alınmadı
- **Kapanan:** w42 ve taps kalkışları (§2), artık üretimden iyi.
- **Kalan:**
  - wstart: ağırlıklı duruştan yanal kalkış geçişinde yüklü sol ayak 1,1 s boyunca 57° dönüyor ve 30 cm kayıyor (üretim 21,0).
  - gait: 14,7 cm (üretim 6,8); kalkıştan sonra yürüyüş döngüsünde oluşuyor.
- Kural gereği regresyon yaratan sistem alınmadı. Kalkış kuralları idle hazır olduğunda devrede.

## 6. Sistemlerin görev dağılımı (yeni paralel sistem kurulmadı)
- **Motion Matching:** klip seçimi. İstek karesindeki veritabanı ve kırpma giriş engeli bu katmanda.
- **SHME bileşeni:** fiziksel durum (destek, yük, ağırlık merkezi). Kalkış ayağı burada okunuyor.
- **ABP:** sahiplik ve devirler (servo, yaw devri).
- **Klip içeriği:** veri onarımları, yalnız proje kopyalarında.
- **IK / Control Rig:** yeni görev verilmedi. FootPlacement ve LegIK'in batmanın sahibi olmadığı V2.50'de gösterildi.

## 7. Açık kalanlar
- **180° geçiş pop'u:** 73 m/s², tek kare (§3).
- **RevTurn iniş adımı:** 6 cm batma. Klip ailesi farklı, bu turda incelenmedi.
- **135° ilk adım:** kaynakta yazılı 5–6 cm sürtünme; V2.50'de top pivotu ile 2–4 cm'e indi.

## 8. Disk
Saklama düzeni korunuyor (`Tools/Retention/retention.py`, kuru çalıştırma). Kapanış ölçümü CHANGES'ta.
