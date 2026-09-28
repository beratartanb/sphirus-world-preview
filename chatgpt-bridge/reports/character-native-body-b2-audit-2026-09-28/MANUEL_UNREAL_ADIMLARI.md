# B2 için eksik resmî UI adımı

Bu adımlar yalnız **yeni test kopyası** içindir. Orijinal `/Game/Character/MainCharacter/MH_MainCharacter` açılıp değiştirilmemelidir. Akış kurulu UE 5.8.1 kaynak kodundan doğrulandı; yüzün aynı kalacağı veya seam'in düzeleceği henüz test edilmedi.

## Test kopyası

1. Content Browser'da `/Game/Sphirus/CharacterLab/NativeBody_20260928/MH_B_SlightlyActive` varlığını **Duplicate** ile kopyala.
2. Kopyayı `/Game/Sphirus/CharacterLab/NativeBodyB2_20260928/MH_B2_PendingNativeWorkflow` olarak kaydet. Bu klasör/varlık bu denetim turunda oluşturulmadı; önerilen yeni test yoludur.
3. Yalnız kopyayı çift tıklayarak MetaHuman Character Editor'de aç.

## Rig yaşam döngüsü

4. Toolbar'da **Remove Rig** kullan. Bu, parametric body'nin eski DNA cache'ini kaldıran resmî yoldur. **Yüz rigini de kaldırır**; yalnız body silen bir düğme değildir. Python `remove_face_rig` bunun yerine geçmez.
5. **Head & Body → Body Params → Parametric** bölümünde B ölçülerinin durduğunu kontrol et. Global parametreleri, head/face kontrollerini, HeadScale ve boy ayarını değiştirme.
6. Yalnız dört aktif constraint hedefini gir:

| Kontrol | B2 hedefi (cm) |
|---|---:|
| Across Shoulder | 30.15 |
| Bicep | 27.00 |
| Forearm | 21.35 |
| Waist | 69.75 |

Diğer değerler [parametre planında](B2_PARAMETER_PLAN_NOT_APPLIED.json). UI bazı ölçüleri solver coupling ile değiştirirse değerleri zorla geri çekmeden kayıt altına al. Yeni B3/B4 üretme.

7. Parametric araçtan çıkıp değişikliği tamamla; test kopyasını kaydet. Yüzde belirgin bir değişim görünüyorsa devam etmeyip kopyayı inceleme için bırak.
8. Toolbar'da **Create Full Rig** kullan. Orijinal rig blend shape içerdiğinden **Create Joints Only Rig** eşdeğer değildir. Full Rig mevcut state için cloud auto-rig üretir; face DNA'yı bedenle hizalayıp native parametric body DNA'sını karakterde saklayan adım budur. Bu bir Head-Only Conform işlemi değildir.
9. İşlem başarıyla bittiğinde yalnız test kopyasını **Save** et. Character Editor sekmesini kapatıp yeniden aç. **Refresh Preview tek başına fresh reconstruction testi değildir.**

## Burada dur

Kopyayı prodüksiyona atama; orijinal karakteri değiştirme; eski adayları silme. Assembly, deformasyon paketi veya gameplay entegrasyonuna geçme.

Sonraki incelemede yeni export alınarak gerçek head mesh kimlik bölgesi, neck seam ve save/reopen body mesh kalıcılığı ölçülmelidir. “Rig başarıyla oluştu” veya “DNA hash eşit” kabul kanıtı değildir. Kimlik bölgesi değişmişse aday reddedilecek; yalnız izin verilen alt-boyun native bağlantı uyumu ayrı değerlendirilecek.

Mevcut oturumun eksik kabiliyeti native UI düğmesine erişimdir. Engine kodu değiştirmek, private API açmak, DNA buffer'ı elle yazmak veya yüzü telafi ederek düzeltmek önerilmiyor.
