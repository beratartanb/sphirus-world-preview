# V2.20 oyun testi (kullanıcı kabulü)

Harita: `L_GR_SphirusHouse`. Oyun kamerası, normal Shift ve WASD. Teknik ölçümler raporda; aşağıdakiler gözle değerlendirilecek.

1. **Depar duruşu (yan yön).**
   - Shift + W ile koş, D ile sağa kesiş yap.
   - Gövde koştuğu yöne döndükten sonra, ~1 s sonra tüm tuşları bırak.
   - Beklenen: gövde koştuğu yöne bakarak, ayakları altında durur; ardından yerinde bir dönüşle kameraya döner. Bırakırken yana kayarak kameraya dönmemeli.
2. **İleri depar duruşu.** Düz depar koşarken bırak. Arkadaki ayak sürtünmeden öne gelmeli.
3. **Shift'e kısa dokun.**
   - Depar koşarken Shift'i çok kısa bırak ve yeniden bas.
   - Beklenen: tempolu koşuya düşmeden küçük bir yavaşlamayla deparda kalır.
   - Shift'i bırakıp tutarsan ~0.8 s içinde tempoya iner.
4. **Geç ters dönüş (diz).**
   - Depar → D kesiş → ~0.6 s sonra A.
   - Basılı dizin içe burkulması V2.19'a göre azalmış olmalı.
5. **Yerinde ters dönüş.**
   - Dururken fareyi 90° sağa çevir; gövde dönmeye başlayınca hemen geri sola çevir.
   - Beklenen: gövde dönüşü bitirmeden, olduğu pozdan yeni yöne döner; arada boşta durma olmaz.
   - 180° ile de dene.
6. **Bilinen ve çözülmeyenler:**
   - Kesiş → S'de pivot klibi atlıyor (frenin bir kısmı görünmüyor).
   - Kesişin ortasında bırakınca duruşta sağ ayak kayıyor.
   - Yerinde dönerken W'ye basınca sol ayak kayıyor.
   - Oyun takılırsa (≥ 0.1 s), erken ters dönüşteki toparlama adımı geçmiş poza atlayabilir.
