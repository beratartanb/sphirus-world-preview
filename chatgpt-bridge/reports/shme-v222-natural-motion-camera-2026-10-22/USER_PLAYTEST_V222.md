# V2.22 oyun testi (kullanıcı kabulü)

Harita: `L_GR_SphirusHouse`. Oyun kamerası, normal WASD / Shift.

1. **Rahat duruştan yürüme.**
   - Birkaç saniye bekleyip W'ye basın.
   - Beklenen: ağırlık hafifçe aktarılır, beden öne düşer ve ilk adım atılır.
   - Kollar ilk adımla birlikte sallanmaya başlar; ileri / yukarı uzanma, bekleme ya da ikinci açılma olmaz.
2. **Durup hemen yeniden yürüme.** Durduktan hemen sonra W. Beklenen: ayak kaymadan kalkış.
3. **Depar → keskin dönüş → yeniden koşu.**
   - Shift + W, D ile kesiş, hemen A.
   - Beklenen: yeniden hızlanırken gövde dik, baş ileri bakar, kollar gövdeye yakın çalışır.
   - Yarış başlangıcı gibi derin eğilme ya da kol savurma olmaz.
4. **Kamera.**
   - Yürüyüşte kamera bedene daha yakındır; tempoluda ve deparda yakınlık azalır.
   - FOV ve sallantı değişmedi. Fazla yakın ya da uzak gelirse söyleyin.
5. **Bilinen ve çözülmeyenler:**
   - Kısa dokunuşlarda ayak kayması.
   - Yan / geri başlangıçlar eski yolla çalışıyor.
   - Tümsek ve basamak üzerinde adımlama.
   - Kesiş → S.
   - Zıplama / iniş bu sürümde incelenmedi.
