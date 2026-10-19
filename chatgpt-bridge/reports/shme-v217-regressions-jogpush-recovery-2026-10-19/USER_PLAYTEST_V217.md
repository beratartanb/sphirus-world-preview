# SHME V2.17 — oyun içi deneme listesi (kullanıcı kabulü için)

Harita: `/Game/GraceRanger/Maps/L_GR_SphirusHouse`, oyun kamerası, PIE. Her maddeyi en az iki kez, sağ ve sol yönde dene.
Teknik ölçümler raporda (`REPORT_V217.md`); buradaki maddeler **görsel ve oyun hissi** kabulü içindir — bu kabul sende.

## Onarımlar (üretimde)
1. **Sol kesişten ters dönüş** — Shift+W depar → A (kesiş) → ~0.35 s sonra D. Bak: ilk ters adımda sol ayak yerde kayıyor mu,
   sonra depar döngüsüne çıkış temiz mi. Aynısını sağ yönde (D → A) dene.
2. **Kesişten geri koşu** — Shift+W → D (0.4 s) → S basılı. Bak: geri koşunun ilk 2–3 adımı yere basıyor mu, gövde geriye mi
   kayıyor, ayak sürünüyor mu.
3. **Diz** — aynı kesiş/ters dönüşleri yandan izle: diz içe kapanıyor mu, bacaklar çaprazlanıyor mu.
4. **Yürüyüş → depar** — W ile yürürken Shift bas (farklı adım anlarında); kısa bas-bırak; Shift'i itiş sırasında bırak.
   (V2.16 bağlantıları; V2.17'de bu kısımda üretim değişikliği yok.)

## Yeni davranışlar
5. **Tempolu koşudan depara itiş (üretimde, PARTIAL)** — Shift'e kısa dokun (tempolu koşu) → W → sonra Shift'i basılı tut.
   Bak: 2–3 adımlık daha hızlı adım ve kol ritmi, öne çökme / blok startı yok, depar döngüsüne kesintisiz geçiş.
   Kontrol: depar sırasında Shift'i kısa bırakıp yeniden bas → **ikinci itiş olmamalı**; W+A / W+D ile küçük yön değişiminde itiş tekrar
   etmemeli.
6. **Toparlama adımı (ADAY — üretimde KAPALI)** — denemek istersen ABP_GR_MotionMatchingBase sınıf varsayılanında
   `SHM217_Recover` = 280 ve `SHM217_RecAge` = 0.3 yap (kaydetmeden PIE). Shift+W → D → **hemen** (≈0.15 s) A.
   Beklenen: bir fren basışı + tek yeniden yerleşme adımı + yeni yöne itiş. Geniş kavislerde (W+D bas, sonra W+A) tetiklenmemeli.

## Yerinde dönüş
7. **Yerinde ters dönüş** — dururken kamerayı hızla 90° çevir, dönüş bitmeden geri çevir; 180° dene; dönüşten hemen W'ye bas.
   Üretim V2.16 ile aynı (aday `GR217_TipHand` kapalı).

Bir şey kötü görünürse: hangi madde, hangi yön, kaçıncı adım — bana yaz; ilgili kanıt kaydını (raporda) birlikte açarız.
