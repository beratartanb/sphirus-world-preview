# V2.18 oyun testi (kullanıcı kabulü)

Harita: `L_GR_SphirusHouse`. Oyun kamerası, normal Shift ve WASD. Teknik ölçümler raporda; aşağıdakiler gözle değerlendirilecek.

1. **Çok erken ters dönüş (yeni toparlama adımı).**
   - Depar koşusunda D/A ile keskin kesiş yap; kesişten hemen sonra (~0.1–0.2 s) ters yöne bas.
   - Beklenen: fren ayağı yere basar, tek bir yeniden yerleşme adımı gelir, sonra koşu devam eder.
   - Bak: çömelme fazla mı, kollar fazla açık mı, sol ve sağ aynı his mi?
2. **Normal ters dönüş.** Kesişten ~0.3 s ya da daha geç ters yöne bas. Toparlama gelmemeli; eski dönüş oynamalı.
3. **Tempolu → depar.** Shift'siz koş, sonra Shift'i basılı tut. Kısa bir itiş; sol ayak girişi kaymamalı, ilk adım uzun olmamalı. Shift'e kısa dokunmak ve tekrar basmak itişi yeniden tetiklememeli.
4. **Yürüyüş → depar.** Yürürken adımın ortasında Shift'e bas.
5. **Ardışık ters.** Depar → S (pivot) → hemen W. Pivottan sonraki kalkış hareket hâlinde başlamalı.
6. **Bilinen ve çözülmeyenler:**
   - geç ters dönüşte (kesişten ~0.6 s sonra) dizler içe giriyor;
   - yerinde dönerken ters istek, ilk dönüş bittikten sonra devrediliyor;
   - S-kesiş pivotunda sol ayak kayıyor (önceden vardı);
   - depar döngüsüne yeniden girişte kayma var (önceden vardı).
7. **Düşük kare hızı.** Oyun 20 fps civarına düşerse erken ters dönüşte toparlama kaçabilir. Görürsen not et.
