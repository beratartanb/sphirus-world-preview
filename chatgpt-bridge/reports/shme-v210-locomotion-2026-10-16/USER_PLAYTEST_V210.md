# SHME V2.10 — Oyun testi rehberi

Teknik ölçümler QA zemininde, gerçek IA_Move / IA_Look yoluyla enjekte girişle yapıldı. His / kontrol kabulü senin oyun testine bağlı.
- V2.10 kayıtlı varsayılan: depar kesiş paketi açık (yüz yönü sınırı 15°, yeni kesiş veritabanı, 0.8 s köprü kuyruğu).
- Diz onarımları (yürüyüş döngüsü, V2.8 duruşları, idle, 33 başlangıç klibi) kalıcı; bir bayrakla kapanmaz.
- Her madde için "doğal / hâlâ X / fazla Y" notu yeterli.

## 1. Depar → keskin 90° kesiş (asıl değişiklik)
- **Nasıl:** Shift ile depar at, D veya A ile ya da fareyle 90° kes. Hem çubukla hem fareyle; sağa ve sola. Yandan ve oyun kamerasından bak.
- **Beklenen:**
  - Önce kısa bir fren: dizler bükülür, gövde hafif içe eğilir.
  - Sonra destek adımı, ardından yeni yöne itiş. Dönüş yarıda kesilip düz koşuya atlamaz.
  - Gövde koşu yönüne dönük: dönüş sırasında gövde yönü ile koşu yolu arası en fazla ~15°.
  - Kontrol: kapsül V2.9'daki kadar hızlı tepki verir (hizalanma 0.60–0.65 s).
- **Not et:**
  - "Fren fazla / az."
  - "Dönüşten sonra bir an düz koşu animasyonu hızla geliyor."
  - "Kontrol gecikmiş hissettiriyor" (ölçüm değişmedi diyor; senin hissin belirleyici).

## 2. Depar → 180° → yeniden hızlan
- **Nasıl:** depar, sonra S veya fareyle 180°.
- **Beklenen:** belirgin fren, pivot ve yeniden hızlanma. Bu kısım V2.9 ile aynı mantıkta; bilinen üst gövde sıçraması (rapor §10) devam edebilir.

## 3. Yürüyüş ve idle'da dizler (kalıcı onarımlar)
- **Nasıl:** W ile düz yürü (5–10 sn), dur, 2–3 sn bekle. Oyun açılır açılmaz karakterin bacaklarına önden-çaprazdan bak.
- **Beklenen:**
  - Yürürken sol dizde tek karelik "kırılma" ya da burulma yok (önceden adımın ortasında görülebilirdi).
  - Oyunun ilk açılışında sol diz içe (karşı dize doğru) kaçmıyor.
  - Duruşlarda diz geriye ya da içe dönmüyor.

## 4. Tempolu dönüşler (değişmedi — kontrol)
- **Nasıl:** fareyle yavaş viraj, sonra keskin dönüş, sonra dur. W+A ↔ W+D. İleri ↔ geri. Tempoluda A/D ile yana kesiş.
- **Beklenen:**
  - V2.9 ile aynı ya da daha iyi; diz onarımları burada da etkili.
  - Tempolu keskin dönüşte ayrı bir "fren adımı" klibi yok; döngülerle dönüyor. Bu bilinçli: denenen koşu dönüş klipleri bizim tempolumuza uymadı.
- **Not et:** tempolu keskin dönüş için fren / destek adımı eksik geliyorsa yaz. Bu bir içerik (mocap) ihtiyacı (rapor §6).

## 5. Eğim ve tek ayak yükseltide dur → dön → ilerle
- **Nasıl:** bir ayağın basamakta / kayada olacağı şekilde dur, 3 sn bekle, yerinde dön, yürü.
- **Beklenen:**
  - Oturmuş idle'da alttaki bacak düz zemindeki gibi.
  - Yalnız yüksekteki bacak bükülü; pelvis gereksiz yere inmiyor.
  - Dönüş V2.9'daki gibi tek parça.

## 6. Bilinen eksik
- Keskin dönüşte momentumun taşıp ayrı bir yakalama adımıyla toparlanması davranışı yok (rapor §6).

## Geri alma
- **Hızlı:**
  - `DA_GR_LocomotionBehavior.SprintCutFaceLead = 0`
  - `ABP_GR_MotionMatchingBase` sınıf varsayılanında `SHM210_CutTail = 0`
  - `SHM_RedirectDB_SL = PSD_SHM_SprintCut`

  Bu üçüyle V2.9 depar mantığına dönülür.
- **Tam:** editör kapalıyken `Saved/Codex/SHME_V210_20261016/checkpoint/` altındaki kopyalar geri kopyalanır (rapor §9).
