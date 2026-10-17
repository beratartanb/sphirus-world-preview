# SHME V2.14 — Oyun testi rehberi

Teknik ölçümler QA zemininde, gerçek tuş girdisiyle. His, görünüm ve kontrol kabulü sende; ben kabul vermedim.

**V2.14 kayıtlı varsayılan (V2.13'ün üstüne):**
- Bileşen (BP_SHM_HumanMotionComponent) yönlendirme bölümü yeni istekte artık gerçekten biter ve aynı tikte yeniden başlar (kaynak
  düzeltmesi; bayrak yok). V2.13'ün ABP telafisi (hız–girdi açısı yeniden sınıflama) ve eski RdRev köprüsü **kapalı**; ABP yeniden
  başlatma tespiti açık.
- Depar kesişinde ters istek: fren pivotu (+0.09 s) → doğrudan **itiş duruşundan** yeniden hızlanma (+0.68 s) → depar döngüsü (+1.8 s).
  Tempolu döngü ve ayakta koşu başlangıcı ("ikinci kalkış") bu zincirde yok.
- İtişten sonra yönlendirme soğuma süresi 0.35 → 0 s.
- Yürüyüş→depar klipleri yeniden adımlandı: ilk itiş adımı kısaldı (yürüyüş hızında 1.45 s'ye kadar, sonra 0.8/0.9/1.0 ölçek),
  depar döngüsüne çıkış kayması 23–27 → ~3 cm; pelvis düşüşü 6–8 cm; gövde eğimi 30°.
- Hareket modeli M1, kamera, kollar, diz koruması, geri pedal limitleri V2.13'teki gibi.

**Kapalı (uyuyor):** V2.13 montajı (SHM213_RevMont), V2.14 "kuyruk" (SHM214_TailSpeed 0), ABP telafisi (SHM213_RevVel, SHM212_RdRev).
Geri dönüş: `verify_prod213.txt` değerleri (RevTurnMode 0, PushRevWin 0, RdRev 1, RevVel 1, RestartOn 0, PushRdCool 0.35).

## 1. Kesiş sırasında ters istek (ana hedef)
Deparda D'ye sert kes, kesiş bitmeden (0.3–0.4 s içinde) A; sol aynası; erken (0.15 s) ve geç (0.6 s) dene.
- Beklenen: fren pivotu, sonra **doğrudan itiş duruşundan** yeni yöne koşu; arada tempolu adım ya da duran koşu başlangıcı yok.
- Bilinen: **geç** ters istekte (gövde ~90° dönmüşken, gerçek 180°) hız ~90'a düşer ve itiş duruşu düşük hızdan girer (poz kapsülden
  hızlı görünebilir); yan kamerada pivot ile itiş arasında 2–3 kare tempolu poz kalabilir. Bunu görüyor musun?
- Not et: fren "ağır ve insan" mı, yoksa durup kalkıyor gibi mi?

## 2. Kesiş → S (geri)
Deparda D'ye kesip S. Beklenen: V2.13 gibi fren pivotu → geri koşu (≤ tempolu). Değişmemeli.

## 3. Yürüyüşten depara
Yürürken Shift (sol ve sağ ayak basılıyken dene: ritmi değiştirerek birkaç kez).
- Beklenen: daha kısa ilk itiş adımı, depar döngüsüne kaymasız geçiş, 30° eğim, kollar sakin.
- Bilinen: itişe **girişte** basılı ayak 4–10 cm kayabiliyor (yürüyüş fazına bağlı; çözülmedi — rapor §3). Gözle fark ediyor musun?
- Dururken Shift+W, tempoluyken Shift: değişmemeli.

## 4. Yerinde dönüş → ters
Dur, fareyi 90° çevir ve 0.5 s içinde geri çevir. Beklenen: V2.13 gibi (ilk dönüş kesilir). Bilinen: kesilen dönüşte basılı ayak kayması
(rapor §4).

## 5. Koruma
Deparda W bırak → S, S+A/S+D; deparda S → W; kesiş sırasında tuşu bırak; iki ardışık yön değişimi; geniş virajlar; eğim / tek ayak
yükseltide dur → dön → başla; idle → yürü → dur → yürü. Beklenen: V2.13 ile aynı.
