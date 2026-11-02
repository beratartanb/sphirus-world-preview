# SHME V2.49 — dönüşlü kalkışta kapsül = klip kök yolu (2026-11-02)

Taban: V2.48 üretimi. Sayılar `TABLES_V249.md`, değişiklikler `CHANGES_V249.md`, ham puanlar `data/score_final.md`.
Görsel: `vid/turn135_diag_realtime_part1.avi` (çapraz kamera, iki tarafta da 135° dönüşlü kalkış) ve `vid/turn_gamecam_realtime_part1.avi` (oyun kamerası; V2.48 o koşuda yanal kalkış seçti). **Videoyu oynatıp izleyemiyorum**; tek tek kareleri inceledim. Oyun hissi NOT_TESTED.

## Özet (durum)
| konu | durum |
|---|---|
| 135°/180° dönüşlü kalkışta kapsülün klip kök yolunu izlemesi | **PASS, üretimde** (servo hatası ≤ 3,5 cm, basılı ayak ötelemesi 0,6–0,9 cm; V2.48 4,0–4,8) |
| 0,12 s geç devreye girme | **PASS, üretimde** (istek karesinde doğru veritabanı, ara Shuffle karesi yok) |
| klip yaw hızı ↔ kapsül yaw ayrışması | **PASS, üretimde** (yaw = çapa + klip kök yaw'ı; oynatma hızından bağımsız) |
| koşu içindeki dönüşlere yan etki | **PASS** (dinlenme kapısı; j41 29,8 / üretim 28,3) |
| 135° kalkışta top-temelli kayma (V2.48 raporundaki ölçüm) | **FAIL**: 24–25 → 27–29 cm. Baskın terim girişteki parmak ucu batması (aşağıda), çözülmedi |
| 180° kalkış (jstart −180 segmenti) | **PARTIAL**: top-temelli 30–35 → 22–24 cm, öteleme 2 cm |
| 60 FPS sıçramalar | **PARTIAL**: 180° kırpma sonundaki tek karelik devir 69 m/s² (1,4 cm fazla yer değiştirme), V2.48'de 48 |
| ağırlıklı idle üretime | **FAIL / alınmadı** (kalkış regresyonları, §4) |
| yeni gerçekçilik davranışları | **NOT_STARTED** |
| saklama düzeni | **PASS** (kuru çalıştırma; boş alan 88 GB) |

## 1. Kare kare kök neden
Araçlar: `turn249.py` (kapsülün klip kök yolundan sapması), `pivot249.py` (temas fazında ayağın en az hareket eden noktasının yolu = gerçek öteleme; topuk etrafında dönmeyi kayma saymaz), `probe249_compressed.py`, `fy` kare dökümü.
1. **0,1 s geç devreye girme:** V2.28/V2.38 sözleşmesi eğri tanığı W'yi bir önceki değerlendirmeden okuyordu ve karışım ağırlığı 0,3'ü geçince açılıyordu. Ayrıca istek karesinde bir kare Dense_Stand_Run_Loops/Shuffle seçiliyordu.
2. **Kapsül yaw ↔ klip yaw ayrışması:** Motion Matching klibi 0,72–1,25× oynatıyor, sözleşme ise hızı 1× eğriden yazıyordu. Kapsül yolu 5,5 cm ve −5…+8° sapıyordu.
3. **Motorun kök hareketi kullanılamıyor:** MM blend-stack alt grafiğindeki `ResetRoot` düğümü kök hareketini sıfırlıyor; `RootMotionFromEverything` ile kapsül donuyor.
4. **İçerik kusuru:** `CoreMotionAAMS/Candidate/af_Loco_Jog_*_Start*_AAMS` kliplerinde ayak 83–84° bükük, top zeminin 8 cm altında.
5. **Girişte parmak ucu batması (açık):** 135°/180° kırpmanın ilk 0,15 s'sinde oyundaki iki ayağın topu −9 cm'e iniyor, ayak ~110° bükülüyor. Kırpma sırasında ayaklar sivri (bale gibi) görünüyor. V2.48'de de birebir aynı. Elenen sahipler, ölçümle: klip ham verisi ve sıkıştırılmış verisi (ikisi de −0,9 cm), FootPlacement (dönüş boyunca kapatıldı, batma aynı), inertialization (kapalıyken aynı), aynalama (şemada mirror tablosu yok), kök eğimi (kök düz). Kalan adaylar: MM blend-stack'in idle örneğinden kırpmaya geçişi ve AnimGraph sonrası katmanlar (orientation/stride warping, LegIK, SHM duruş katmanları).

## 2. Üretime alınanlar
- **Kapsül konum servosu:** kırpma kliplerine kök konum eğrileri (`SHM249_RX/RY`) yazıldı. Her karede hedef kapsül pozu = giriş çapası ∘ klip kökü(t). Hız = klibin kendi kök hızı (ileri + yanal) + 0,35 kazançla konum düzeltmesi; yaw = çapa + klip kök yaw'ı.
- **İstek karesinde doğru veritabanı:** TurnStart açılırken `Update_MotionMatching` girişinde doğrudan T2 dönüş veritabanı aranıyor.
- **Dinlenme kapısı:** sahiplik yalnız duruştan kalkışta (hız < 40 cm/s); koşan dönüşlere dokunmuyor.
- **Tutma = kırpma klibi:** dönüş tamamlanınca kilitleniyor (`SHM249_TurnDone`), 1 s zaman tutması kaldırıldı (`SHM248_HoldT` 0), sol dönüşlerin tutmayı erken bırakması (|T|) düzeltildi.
- **Ayak zemin teması onarımı (14 dönüş klibi):** klip verisinde top zeminde (84° → 35°). Oyundaki giriş batmasını değiştirmedi (§1.5); onarım verisi doğru olduğu için yerinde bırakıldı.

## 3. Denenip üretime alınmayanlar
- T2 veritabanı devam-pozu sapması −0,5: 60 FPS sıçramasını değiştirmedi; orijinal −2,0'a geri alındı.
- FootPlacement'in dönüşte yol vermesi (`SHM249_FPOff`, kurulu, anahtar 0): batmayı değiştirmedi. Gerçek zamanda R180 sonrası 54–56 cm kayma üretti.
- Top-sabit ayak onarımı (v3): duruşu 14 cm kaydırdı.

## 4. Idle
V2.44'ten beri hazırlanan ağırlıklı idle (30 FPS): w43 iyileşti (öteleme 7,3 → 3,8), ama idle'dan kalkışlar kötüleşti (wstart 21,0 → 39,5, w42 10,2 → 19,7, gait 6,8 → 14,7). Kalkış klipleri idle pozuyla uyumlu girişe sahip değil. Üretime alınmadı.

## 5. FPS ve gerçek zaman (üretim, temiz oturum)
135° kırpma seçilen koşularda basılı ayak ötelemesi: 60 FPS 0,6, gerçek zaman 0,7–0,9 cm. 20 FPS'de öteleme ölçümü kare yetersizliğinden boş; top-temelli 31,9. 120 ve 30 FPS'de bu senaryoda bakış açısına göre yanal kalkış seçiliyor (V2.48 ile aynı). Diğer senaryolarda V2.48 ile aynı aralık; regresyon yok.

## 6. Disk saklama düzeni
`Tools/Retention/retention.py` (varsayılan kuru çalıştırma, `--apply` ile siler; korunan etiketler `Tools/Retention/protect.txt`; kayıt `Saved/Codex/Retention/`). Yalnız yeniden üretilebilir test çıktılarını budar (son 3 tur dışındaki ham telemetri ve kare klasörleri, yayımlanmış kopyalar, 6 saatten eski medya geçici klasörleri, 7 günden eski log/çökme, pycache). Content/Config/Plugins, `.uasset/.umap`, checkpoint/manifest yedekleri, `data/` ve raporlara dokunmaz. Boş alan 40 GB altına inerse uyarır. Bu tur boş alan 93 → 88 GB (V2.49 telemetri, kayıtlar, yedekler).

## 7. Sonraki adım
Giriş batmasının sahibini bulmak: MM çıktısını AnimGraph sonrası katmanlardan önce ve sonra kemik düzeyinde kaydetmek (ac_ eğrileri ayak ve top kemikleri için genişletilir), sonra blend-stack geçişini idle örneği yerine kırpmanın ilk karesine eşlemek. Ardından idle uyumu ve gerçekçilik davranışları.
