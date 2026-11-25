# Visual Cohesion — geçiş C (2026-11-25)

**Durum: IN PROGRESS.** Bu geçişte ışık koşulları ilk kez test edildi ve oyun standalone çalıştırıldı; kayıtlı ışık/atmosfer değişikliği yok.

## 1. Işık koşulları testi (yalnız PIE, kaydedilmedi)
`scripts/tod.sh`: güneş açısı, şiddeti, sıcaklığı ve gökyüzü ışığı beş koşula ayarlandı; dört sabit bakış (ön cephe, göl, şömine, orman). `evidence/isik_kosullari_testi.jpg`.

| Koşul | Gözlem |
|---|---|
| Sabah | Göl ve orman iyi okunuyor; ön cephede duvarda iki parlak leke — kusur |
| Öğle | Dengeli; zemin otu doygun |
| Gün batımı | Gölde sıcak ışık etkileyici; iç mekân tutarlı |
| Gece | **Dış mekânda karakter ve zemin neredeyse kayboluyor**; iç mekân sıcak ve okunur. Ay/dolgu ışığı gerekli |
| Bulutlu | Yumuşak, en tutarlı koşul; cilt ve kıyafet doğal |

İç mekân beş koşulda da benzer görünüyor: iç aydınlatma yapay ışıklara dayanıyor, pencereden gelen gün ışığı katkısı zayıf. Işık dökümü: `data/lights_audit.txt` (30 ışık; `ReviewOnly` ışıkları görünmez durumda).

## 2. İç → dış pozlama
İç mekân hacminde vurgu sıkıştırması (0,5), detay 1,15, eğilim +0,15 denendi: `evidence/ic_mekan_pozlama_denemesi.jpg` — pencere ve balkon patlamasında ayırt edilebilir kazanç yok. Kaydedilmedi. Sorun açık.

## 3. Standalone çalıştırma
Editör kapatılıp oyun `-game` ile başlatıldı: harita yüklendi, kayıttan devam etti (arka bahçe), görev metni ve arayüz geldi, yeni kıyafet ağları ve materyalleri doğru çizildi (`evidence/standalone_oyun_penceresi.jpg`). Kullanıcı kaydı değişmedi. Ekranda motor uyarısı: ışın izleme geometrisi belleği bütçenin %20'sini aşıyor (136/400 MB). Kare süresi kaydı alınamadı; **paketlenmiş yapı denenmedi**.

## 4. Bütünlük değerlendirmesi
İyileşen: iç ve dış sıva aynı yüzey diline geçti; atölye üretim hikâyesini daha iyi taşıyor; karakter artık göz kırpıyor.
Açık: gece okunurluğu, iç/dış pozlama, balkon zemini, karanlık odada saç benekleri, ellerin kalçadan geçmesi, zemin otu, rezonansın yeni yüzeylerle denenmemesi, ortak 8 maddelik test.

## 5. Araç kullanımı
Blender 5.3: rest ölçümü, 42 pozluk derileme/penetrasyon analizi, kıyafet daraltma, 6 prop üretimi. StableGen, ComfyUI, Blender MCP, Jiggle: kullanılmadı. Epic Unreal MCP: bu oturumda yüklü değil; bütün işler kapılı çalıştırıcıdan.
