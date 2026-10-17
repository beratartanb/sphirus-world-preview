# SHME V2.13 — Oyun testi rehberi

Teknik ölçümler QA zemininde, gerçek tuş girdisiyle. His, görünüm ve kontrol kabulü sende; ben kabul vermedim.

**V2.13 kayıtlı varsayılan (V2.12'nin üstüne):**
- hareket modeli: depar ivmesi 360 → 300, tempolu 300 → 270, kesiş yanal tavanı 650 → 450, dönüşte hız kaybı 0.35 → 0.5 (en az %60 hız). Yürüyüş değişmedi.
- kesiş sırasında ters istek: hız–niyet açısı 110°'yi geçince hemen fren pivotu (eski kesiş itişi artık sürmüyor).
- yerinde dönüş sırasında ters istek: ilk dönüş kesiliyor, ters dönüş ~0.5 s'de başlıyor.
- yürüyüşten ve duruştan depara: daha az öne eğilme, daha yüksek pelvis, daha küçük kol hamlesi.
- fren pivotu (sabah): çömelme 17–21 → 5–11 cm.

**Kapalı (uyuyor):** kök hareketli fren–pivot–itiş montajı (madde 5 adayı), ABP bölüm yeniden başlatma algılama.

## 1. Atiklik ve ağırlık
Deparda W+D / W+A ile viraj al, fareyle 45–90° çevir, tempoluda W+A↔W+D değiştir. Yürürken küçük düzeltmeler yap.
- Beklenen: depar/tempolu dönüşleri daha geniş ve hız kaybıyla; yürüyüş eskisi gibi.
- Not et: "hâlâ fırlıyor" mu, "fazla hantal" mı (hangi gait'te).

## 2. Kesiş sırasında ters istek
Deparda D'ye sert kes, kesiş bitmeden A (erken ve geç dene; sol aynası). Deparda D'ye kesip S.
- Beklenen: eski kesiş itişi sürmez; hemen fren pivotu, sonra yeni yöne koşu.
- Bilinen: pivottan sonra tempolu döngü → koşu başlangıcı ("ikinci kalkış"). Bunu görüyor musun?

## 3. Yerinde dönüş → ters
Dur, fareyi 90° çevir ve 0.5 s içinde geri çevir; 90 → ters 180 de dene.
- Beklenen: ilk dönüş yarıda kesilir, ters dönüş hemen başlar.
- Bilinen: kesilen dönüşte basılı ayak biraz kayabilir.

## 4. Depara atılma
Yürürken Shift; dururken Shift+W; tempoluyken Shift.
- Beklenen: yürüyüşten daha az eğilen, kolları daha sakin bir itiş; duruştan daha dik başlangıç.
- Bilinen: tempolu → depar itişsiz; yürüyüşten itişe girişte ~10 cm ayak kayması.
- Not et: eğilme/kol hamlesi "normal insan" mı, hâlâ atlet mi?

## 5. Geri
Deparda W bırak → S; S+A/S+D; W basılıyken S.
- Beklenen: fren daha yumuşak (ilk kare kesiği azaldı), sonra geri koşu ≤ tempolu.

## 6. Koruma
Kamera dönerken W (ekran yönü), eğim/tek ayak yükseltide dur → dön → başla, uzun düz yürüyüş (kollar).
