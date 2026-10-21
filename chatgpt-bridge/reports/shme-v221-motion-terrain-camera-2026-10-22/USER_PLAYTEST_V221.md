# V2.21 oyun testi (kullanıcı kabulü)

Harita: `L_GR_SphirusHouse`. Oyun kamerası, normal WASD / Shift. Teknik ölçümler raporda; aşağıdakileri gözle değerlendirin.

1. **Eğimli zemin.**
   - Evin yanından ormana doğru yokuş yukarı yürüyün, sonra tempolu koşun.
   - Beklenen: gövde yokuşta hafifçe öne verir; inişte dik ya da hafif geride kalır. Düzlükte fark olmaz.
   - Abartılı öne eğilme varsa söyleyin.
2. **Yan eğim.**
   - Eğimi yandan geçin.
   - Beklenen: gövde hafifçe yokuş tarafına denge verir; aşağı tarafa yatmaz.
3. **Duruşta yerleşme.**
   - Tempolu koşu ya da depar sırasında tuşları bırakın.
   - Beklenen: tek, küçük bir öne-sonra-geri ağırlık oturması; sallantı yok.
   - Durur durmaz yeniden basın: hiç beklemeden yeniden hareket etmeli.
4. **Kamera adım ritmi.**
   - Yürüyün, tempolu koşun, depar atın.
   - Beklenen: yürüyüşte çok hafif, tempoluda biraz daha belirgin bir adım hissi. Depar atarken yalnızca Shift'e basmak tek başına bir efekt yaratmaz.
   - Fazla gelirse söyleyin; düşük hareket profili hazır (`CamComfortScale` 0.3 + yuvarlanma kapalı).
5. **Erken ters dönüş + takılma.**
   - Depar → D kesiş → hemen A.
   - Oyun takılsa bile toparlama adımı geçmiş poza atlamamalı.
   - Bırakma ve yeni yön hemen tepki vermeli.
6. **Bilinen ve çözülmeyenler:**
   - Kesiş → S'de pivot frenin bir kısmını atlıyor.
   - Kısa dokunuşlarda ayak kayıyor (küçük adım adayı reddedildi).
   - Kesiş ortasında bırakınca sağ ayak kayıyor.
   - S-kesişte depar kavisi yavaş çekimde oynuyor.
   - 15 cm kenardan tempolu inişte sağ ayak sürükleniyor.
   - Yokuş / inişte adım uzunluğu ve yüksekliği değişmiyor; yalnız gövde tepki veriyor.
