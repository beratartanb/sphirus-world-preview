# SHME V2.15 — Oyun testi rehberi

Teknik ölçümler QA zemininde, gerçek tuş girdisiyle. His, görünüm ve kontrol kabulü sende; ben kabul vermedim.

**V2.15 kayıtlı varsayılan (V2.14'ün üstüne):**
- Yürürken Shift: itiş klibi artık o anda basılı olan ayağın evresine göre seçiliyor (sol ayak basılıysa sol duruşun sonu, sağ ayak
  basılıysa sağ duruşun başı). Yalnız bu geçiş için yörüngeye daha az, poza daha çok bakan bir seçim düzeni.
- Depar kesişinde ters istek: fren pivotu → doğrudan itiş duruşu → depar. Aradaki 2–3 kare tempolu poz ve 0.3 s'lik ileri depar karesi
  kaldırıldı; itiş bölüm bittiği tikte başlıyor (yalnız 230 cm/s altında); gerçekten durmuşsa (<60 cm/s) küçük koşu başlangıcı.
- Yerinde dönüş: basan ayak zeminden 3–8 cm kalkıyor (önceden zemine sürünüyordu); ters isteğin ilk dönüş karesinde ayak kilidi tam.
- Hareket modeli M1, kamera, kollar, geri pedal, diz koruması V2.14'teki gibi.

**Kapalı (denendi, üretimde değil):** hız çizgisinde fren (GR215_RevBrakeDecel), fren sırasında yön tutma (GR215_RevYawHold), destek
ayağına göre pivot seçimi (SHM215_PivFoot), kesiş klibi çömelme bake'i.
Geri dönüş: SHM215_LinkOn 0, LowSpeed 0, TipLock 0, SHM211_DB_Push = PSD_SHM212_GaitPush, ters DB = PSD_SHM214_Rev_L/R + klip checkpoint'leri.

## 1. Yürüyüşten depara
Farklı ritimlerde birkaç kez yürürken Shift (sol ve sağ ayak basılıyken).
- Beklenen: basılı ayak yerinde kalır, kısa itiş, ardından depar.
- Bilinen: sol ayak tam ortadayken bazen 5–8 cm kayma kalıyor; itişin ilk yarım saniyesinde adımlar kapsül hızından kısa görünebilir.

## 2. Kesişte ters istek (erken / normal / geç; sol ve sağ)
Deparda D'ye kes, 0.15 / 0.35 / 0.6 s sonra A.
- Beklenen: pivot → itiş → depar; arada tempolu adım ya da duran kalkış yok.
- Bilinen: pivot girişinde ayak zeminde süpürülüyor gibi görünebilir (çözülmedi); kesişte pelvis 66–71 cm'e iniyor (kesiş klibinin kendisi).
- Not et: süpürme ve çömelme gözle ne kadar rahatsız edici?

## 3. Yerinde dönüş → ters
Dur, fareyi 90° çevir, 0.5 s içinde geri (90 → ters 180 de). Sağ ve sol, hafif eğimde de dene.
- Beklenen: ters dönüşte basan ayak kalkarak adım atar, basılı ayak yerinde döner.
- Bilinen: ters dönüşün ilk karesinde küçük bir ayak kayması; 90° geri dönüşte adım hâlâ alçak.

## 4. Koruma
Deparda W bırak → S, W/S örtüşmesi, Shift+S, kamera 180 + W, tempoludan depar (itiş yok — bilinen eksik), dururken Shift+W, idle →
yürü → dur → yürü, kısa bas-bırak, eğim / tek ayak yükseltide dur → dön → başla. Beklenen: V2.14 ile aynı.
