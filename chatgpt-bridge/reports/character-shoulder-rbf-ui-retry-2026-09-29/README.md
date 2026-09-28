# B2 omuz RBF — resmî UI yeniden denemesi

Windows kontrolü bu denemede çalıştı. Mevcut izole omuz test karakterinde resmî MetaHuman Assembly işlemi arayüzden yürütüldü. Unreal Assembly'nin başarıyla tamamlandığını bildirdi.

Bu, omuz deformasyonunun düzeltildiği veya RBF açılımının doğrulandığı anlamına gelmiyor.

## Uygulanan işlem

- Önce kabul edilen karakter ve mevcut test alanı yedeklendi.
- Resmî Enable Experimental Workflows seçeneği arayüzden açıldı.
- Assembly ve Common çıktıları mevcut omuz test alanına yönlendirildi.
- Test PostProcess kopyası seçildi.
- Unpack RigLogic ve Unpack RBF to Pose Assets açıldı.
- Finger-half ve swing/twist Control Rig açılımı kapalı tutuldu.
- Bu ayarlar Assembly öncesinde editörden salt okunur teknik sorguyla doğrulandı.
- Assembly çalıştırıldı; editör başarı mesajı verdi.

## Şu anki engel

Assembly sonrasında Unreal **Bellek Baskısı Uyarı** penceresini açtı. Otomasyonun Yok Say tıklamaları ve Enter işlemi bu pencereyi kapatmadı. Editörün salt okunur envanter kuyruğu da ilerlemedi.

Kullanıcıdan yalnızca bu uyarıdaki **Yok Say** düğmesine basması istendi. Uyarı kapanınca test varlıklarının kaydı ve RBF envanteri doğrulanacak. Bu aşamada editörü zorla kapatmak veya kaydedilmemiş test çıktısını kaybetmek tercih edilmedi.

## Kanıtın sınırı

Gerçek PA/AS varlık sayısı ve PoseDriver bağlantıları henüz doğrulanmadı. Assembly başarı mesajı bu ilk kapının yerine geçirilmedi. Açılmış rig / native B2 geometrik eşdeğerliği, izole omuz ROM'u, düzeltici düzenleme ve save/reopen QA **NOT_RUN**.

Kabul edilen B2 ve orijinal üretim karakterinin dosyaları başlangıç checkpoint'iyle aynı bulundu. Yüz, vücut ölçüleri ve HeadScale için düzenleme yapılmadı. Engine/plugin kodu, özel DNA tamponları ve korumalı API'ler değiştirilmedi. Oynanış varlıkları hedef alınmadı. Hiçbir eski kanıt silinmedi.

## Durum

| Kontrol | Sonuç |
|---|---|
| Windows / Unreal UI erişimi | ÇALIŞTI |
| Resmî UI Assembly | Editör başarı bildirdi |
| RBF açılım doğrulaması | BEKLİYOR — varlık sayısı/düğümler okunamadı |
| Açılmış rig eşdeğerliği | NOT_RUN |
| Omuz düzeltmesi | UYGULANMADI |
| Omuz deformasyonu | Önceki FAIL çözülmedi |
| Koltuk altı / genel deformasyon | Önceki PARTIAL çözülmedi |
| Kabul edilen B2 oran/yüz/seam/persistence | Önceki kabul geçerli; yeni canlı QA yapılmadı |
| Üretim karakteri değiştirildi | NO |
| Kullanıcı onayına hazır düzeltme | NO |

Sonraki adım: bellek uyarısını kapatmak, yalnız test çıktısını kaydetmek, gerçek RBF varlıkları ve PoseDriver bağlantılarını doğrulamak; ardından herhangi bir corrective düzenlemeden önce eşdeğerlik testi. Başarısız kapılar atlanmayacak.

Bu rapor bir ara engel kaydıdır; karakterin veya omuz düzeltmesinin tamamlandığı iddiası değildir. Ham karakter varlıkları, DNA, özel dosya yolları veya ekran görüntüleri bu genel rapora yüklenmedi.
