# SHME V2.9 — Oyun testi rehberi

Teknik ölçümler QA zemininde, gerçek IA_Move / IA_Look yoluyla enjekte girişle yapıldı. His / kontrol kabulü senin oyun testine bağlı.
- V2.9 kayıtlı varsayılan: `SHM29_CutMode 2`, `SHM29_TipOld false`, `SHM_HC_Off false` (hepsi yeni mantık açık).
- Her madde için "doğal / hâlâ X / fazla Y" notu yeterli.
- Engebeli zemin için haritada bir basamak, eğim veya kaya kenarı seç. QA kutuları yalnız test sırasında vardı.

## 1. Engebeli zeminde duruş (asıl düzeltme 1)
- **Nasıl:** bir ayak basamakta / kaya üstünde, diğeri aşağıda kalacak şekilde yürüyüp dur. Eğimde yukarı, aşağı ve yan dönük dur. Yürüyüş, tempolu ve depar duruşlarını dene. 3–5 sn bekle.
- **Beklenen:**
  - Duruştan sonra ikinci bir çökme yok; aşağıdaki ayak yere gömülmüyor, bilek / parmaklar yüzeyde.
  - Eğimde ayak eğimi duruşun sonundaki gibi kalıyor (iki kat eğilmiyor).
  - Yüksek basamakta pelvis biraz iniyor ve diz bükülüyor: bu tek uyarlamanın gereği, normal.
- **Not et:**
  - "Pelvis hâlâ fazla iniyor" (basamak yüksekliğini tahmin et).
  - "Bekledikçe ayak kayıyor / gömülüyor."

## 2. Dizler (asıl düzeltme 2)
- **Nasıl:** yürüyüş / tempolu / depar başlangıçları ve duruşları, çapraz yönler (W+A, W+D, S+A, S+D). Yandan ve önden dizlere bak.
- **Beklenen:** diz hiçbir karede geriye bükülmüyor ya da içe / dışa burulmuyor.
- **Bilinen:** oyunun ilk açılışındaki idle'da sol dizde küçük bir yana bükülme var (bu görevden önce de vardı).

## 3. Yerinde dönüş (asıl düzeltme 3)
- **Nasıl:** dur, fareyle yavaş 45–90° dön; sonra hızlı 90° ve 180°. Dönüş bitmeden W'ye bas. Bir de basamak / eğim üstünde dön (yüksek ve alçak taraftan).
- **Beklenen:**
  - Gövde tek parça dönüyor: kalça önce ters savrulup sonra yetişmiyor.
  - Basılı ayak topun üzerinde dönüyor, bacak burulmuyor.
  - Yürüyüşe kalkarken tek karelik dönüş atlaması yok.
- **Not et:** "Dönüş fazla yavaş / fazla hızlı", "ayak yine kayıyor", "omuzda sıçrama".

## 4. Hareket hâlinde dönüşler (yeni davranış)
- **Depar → keskin 90° kesiş** (çubuk ya da hızlı fare):
  - Beklenen: kısa fren, dizler bükülüyor, gövde içe ve öne eğiliyor, sonra itiş.
  - Bilinen: klip dönüşün yalnız ilk yarısında kalıyor; ilk basan ayak her zaman dış ayak değil.
  - Not et: "Çökme fazla / az", "dönüş geç tepki veriyor".
- **Depar → hızlı 180° → yeniden hızlan:**
  - Beklenen: belirgin fren, pivot ve yeniden hızlanma; araya yürüyüş girmiyor.
  - Bilinen: ters dönüşte üst gövdede sıçrama var (önceden de vardı).
- **Tempolu ileri ↔ geri (W ↔ S):**
  - Beklenen: araya yürüyüş döngüsü girmiyor, ikinci dönüşte ayak kayması yok.
- **Tempolu fareyle 180°:** ters köprü seçiliyor. Koşu dönüş klipleri bağlı değil (açık madde).
- **Değişmemesi gerekenler:** yürüyüşte ±30°, tempolu A/D kesişi, W+A ↔ W+D, depar geniş viraj, dokun → bırak → tekrar bas → çapraz.

## 5. Kontrol tepkisi
- **Nasıl:** her dönüşte girişten sonra kapsülün ne zaman yön değiştirdiğine bak.
- **Beklenen:** V2.8'den daha geç tepki yok (kapsül hızları değişmedi; yalnız animasyon seçimi değişti).
- **Not et:** "Kesişte karakter gecikiyor" ya da "kontrol kayıyor".

## Geri alma
`ABP_GR_MotionMatchingBase` sınıf varsayılanında:
- `SHM_HC_Off = true`: engebeli zemin duruş düzeltmesi kapanır (V2.8 duruş tutma).
- `SHM29_TipOld = true`: yerinde dönüş düzeltmesi ve pivot ön ayarı kapanır.
- `SHM29_CutMode = 0`: V2.8 hareketli dönüş mantığı. `1` = niyet açısı + ters dönüş kuyruğu, depar kesiş köprüsü kapalı.
- Diz onarımı bir bayrakla kapanmaz.
  - Tam geri dönüş için editör kapalıyken geri kopyala: `Saved/Codex/SHME_V29_20261016/checkpoint/before_v29_abp_save/` (ABP'ler) ve `checkpoint/knee_repair_before/` (76 klip).
