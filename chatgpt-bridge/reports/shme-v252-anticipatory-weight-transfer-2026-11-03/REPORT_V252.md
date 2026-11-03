# SHME V2.52 — yürüyüş kalkışında öngörülü ağırlık aktarımı (2026-11-03)

Taban: V2.51 üretimi. Sayılar `TABLES_V252.md`, değişiklikler `CHANGES_V252.md`.

Videolar 60 fps, gerçek hızda. Her çiftte aynı oturum ve aynı hareket var; solda V2.51 içeriği, sağda V2.52:
- `vid/walkstart_side`, `vid/walkstart_diag`, `vid/walkstart_gamecam`: duruştan ileri-sağ yürüyüş kalkışı (aynı klip)
- `vid/wstart_side`: geri kalkışlar
- `vid/turn180_diag`: 180° kalkış (yumuşak yaw)

**Videoları oynatıp izleyemiyorum.** Tek kareler arasında fark ince. Görsel kabul ve oyun hissi NOT_TESTED; görsel PASS verilmedi.

## 1. Yeni davranış: öngörülü ağırlık aktarımı (yürüyüş kalkışları) — üretimde

**Ölçülen eksik (klip verisi, 14 yürüyüş kalkış klibi).** Salınım ayağı yerden kalkarken pelvis, ayaklar arasındaki eksende t = 0,42–0,70 konumundaydı (0 = destek ayağı, 1 = salınım ayağı, duruş genişliği 28–33 cm). Yani beden, ağırlık hâlâ üzerindeyken bacağını kaldırıyordu. Oyunda bu daha da belirgindi (t = 0,46–0,77). İnsan yürümeye başlarken ağırlık merkezi, ayak kalkmadan önce destek ayağına doğru 3–4 cm kayar.

**Yeni içerik.** `SHM252_StartTransfer_*_APA` adıyla 14 klip ve `PSD_SHM252_StartTransferAPA_L/R` adıyla iki veritabanı üretildi. Kaynak klipler ve veritabanları değiştirilmedi.
- Pelvis, ilk karede başlayıp ayak kalkışında tepe yapan pürüzsüz bir eğriyle destek ayağına kayıyor; ardından 0,3 s içinde adımın kendi hareketine bırakılıyor.
- Destek tarafındaki kalça yükü alırken salınım tarafı 2° alçalıyor.
- Ayaklar kaynaktaki yerinde kalıyor (hata ≤0,5 cm). Diz ve ayak bileği menteşeli bacak IK'sı ile çözülüyor. Gövde pelvisi izliyor.
- Kontrol gecikmiyor: aktarım ayrı bir bekleme değil, ilk adımın içinde.
- **Harman telafisi.** MM, idle'dan kalkışa 0,5 s'lik bir harmanla geçiyor ve ayak kalkışı bu harmanın ortasına denk geliyor. Bu yüzden klipteki kayma, kalkış anındaki harman ağırlığına bölündü (en fazla 8 cm). Böylece oyunda görünen kayma ayak kalkışı civarında ~2,5–3 cm'lik pürüzsüz bir tepe yapıyor.

**Oyunda sonuç.** Aynı oturumda önce/sonra, salınım ayağı kalkarken pelvis:

| kalkış | önce | sonra |
|---|---|---|
| w42 ileri-sağ, 60 FPS | 0,59 | 0,32 |
| aynısı, 20/30/120 FPS ve 2 gerçek zaman koşusu | — | 0,31–0,37 |
| wstart ileri-sağ / sol-sol / sağ-sol | 0,64 / 0,51 / 0,46 | 0,38 / 0,32 / 0,35 |
| taps geri | 0,53 | 0,21 |
| wstart geri (B_Rfoot) | 0,77 | 0,73 (8 cm sınırında) |

**Uyum.** Temas ölçümleri V2.51 ile aynı aralıkta; taps'ta top kayması 19,0'dan 16,5 cm'e azaldı. İki yan etki görüldü:
- wstart'ta kalkış sonrası yürüyüş döngüsündeki 84°'lik pivot olayı 23,5'ten 30,7 cm'e çıktı (contact231; pivotta topun çizdiği yay).
- gait'te batma 2,2/1,8'den 2,8/3,3 cm'e çıktı.

## 2. 180° sonundaki 60 FPS sıçraması — PARTIAL (açık)

Kare kare kemik ikinci farkları (kök çerçevesi) ölçüldü. Sıçrama, geçiş karesinde değil, servonun bıraktığı ilk karede: omuz −1,9 cm, pelvis −0,65/−0,50 cm.

| Elenen sahip | sonuç |
|---|---|
| V2.51 yaw devrinin sert duruşu | Yaw artık üstel yaklaşıyor (τ 0,08 s, üretimde), dönüş hızı yumuşakça sıfıra iniyor. Pop 81 → 79. |
| Kök hareket modu geçişi | Sabit tutuldu (SHM252_KeepRM), etkisiz; kapalı. |
| Orientation warping | Kapalıyken pop aynı. |
| FootPlacement | Kapalıyken 72 (o koşuda farklı klip seçildi). |
| V2.51'deki MM zıplamaları | Zaten kaldırılmıştı. |
| Basit harmanlama | Matematiksel olarak katkısı çok küçük. |

Kalan sıçrama, bırakmadan sonraki ilk karede blend stack pozunun içinde; sahibi bu turda bulunamadı.

## 3. Değerlendirilen regresyonlar
- **j40 (60 FPS 18,7):** Aynı üretim ayarında gerçek zaman tekrarları 12,1 ile 73,9 cm arasında. Kaotik trajektori değişkenliği; değiştirilen kliplerde değil.
- **jstart (120 FPS 59,3):** V2.50'de 50,3, V2.51'de 59,3, V2.52'de 59,3; hep aynı olay. A_CT_Jog_FwdLeft döngüsünde salınım ayağının topu 6,4 m/s hızla 0,09 s zemine sürtünüyor. Eski bir döngü kusuru (ayak ucu sürtünmesi), regresyon değil; bu turda düzeltilmedi.

## 4. Ağırlıklı idle — kapalı kaldı
wstart (yanal geçişte yüklü ayağın 57° dönüp kayması) ve gait çözülmedi. Kural gereği açılmadı. Yeni ağırlık aktarımı kalkış klipleri ağırlıklı idle ile de çalışıyor (aynı veritabanları).

## 5. Görev dağılımı (yeni paralel sistem yok)
- **Motion Matching:** klip seçimi; yeni veritabanları mevcut ABP değişkeniyle bağlandı.
- **SHME (V2.51 StartLoad):** hangi ayağın serbest olduğunu seçiyor. Seçilen ayak artık gerçekten yükten kurtuluyor (bu turun içeriği).
- **Animasyon içeriği:** gerçek beden tepkisi (pelvis, kalça, diz, ayak bileği).
- **Bacak IK'sı:** üretim sırasında ayak temasını korudu.
- **ABP:** yalnızca yaw devri (τ).

## 6. Açık kalanlar
- 180° geçişindeki tek karelik pop (§2).
- Frenleme sonrası yerleşme ve dönüş momentumu bu turda yapılmadı. Bir davranış uçtan uca tamamlandı.
- Döngüdeki ayak ucu sürtünmesi (§3).
- Ağırlıklı idle (§4).
