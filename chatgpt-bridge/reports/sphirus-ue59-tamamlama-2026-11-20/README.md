# SPHIRUS UE 5.9 — tamamlama turu (2026-11-20)

Proje: `sphirus_UE59` · harita `/Game/GraceRanger/Maps/L_GR_SphirusHouse` · oyuncu `BP_HybridA_Player`.
Başlangıç noktası: `sphirus-ue59-hareket-hissi-2026-11-20` (commit `1438882`). O rapordan bu tura kadar Content ve Config altında hiçbir dosya değişmemişti.
Kullanıcı kayıtları baştan sona aynı kaldı: 5.9 test kaydı `3d81ab9d…`, 5.8.4 kaydı `4823d83a…`. Testler ayrı test kayıtlarıyla yürütüldü.

**Durum etiketleri**
- UYGULANDI: değişiklik kaydedildi; editör yeniden açıldıktan sonra değerleri ve kirli paket olmadığı doğrulandı (`data/final_state_r3.txt`).
- ÖLÇÜLDÜ: sayısal kayıtla doğrulandı.
- GÖRÜLDÜ: kare şeritlerine bakıldı. Videoları gerçek hızda izleyemiyorum.

Hiçbir madde USER_ACCEPTED değildir.

Girdiler PIE'ye gerçek tuş olayı olarak verildi: W/A/S/D, Shift, Ctrl, X, E ve sol fare tuşu. Değişken atamasıyla yapılan test yok.

## 0. Ortam
- **Motor güncellemesi:** Epic Launcher bugün 07:57'de 5.9 motorunu güncelledi (derleme 60351404 → 60738873). Fab eklentisinin dosyaları eski derlemede kaldı ve editör açılırken eksik modül penceresiyle durdu. Otomasyon oturumları Fab kapalı başlatıldı; proje dosyasına bu yüzden dokunulmadı.
- **İlk açılışta donma:** güncellemeden sonra animasyon ve hareket veritabanı önbellekleri yeniden kuruldu. Kurulum bitene kadar PIE dünyası zaman ilerletmedi (karakter donuk kaldı). Ölçümlere kurulum bittikten sonra başlandı.
- **5.9 kopyası:** `sphirus.uproject` artık doğrudan "5.9" sürümüne bağlı. Smart App Control'ün engellediği 4 eklenti dosyada kapalı.
  - Proje içeriğinde PBL_Database, Nwiro ve GravityScatterTool'a hiç bağlantı yok.
  - Black_Eye'ı yalnız eski AAMS klasöründeki 3 kamera Blueprint'i kullanıyor.
  - Resmî çözüm, eklentilerin 5.9 sürümlerini Fab/Launcher'dan kurmak. Bu kurulumu ancak siz yapabilirsiniz; Windows güvenliğine dokunulmadı.
- **Sol Shift hata ayıklama bağlaması:** 5.9 motoru Sol Shift'i bir hata ayıklama komutuna bağlıyor; koşarken günlüğe saniyede onlarca satır yazılıyordu. `Config/DefaultInput.ini` içinde bu bağlama kaldırıldı.

## 1. Ölçüm yöntemi düzeltmesi
Önceki raporlarda bir ayağın basılı sayılması "top kemiği yere 5 cm'den yakın" kuralına dayanıyordu. Bu kural, yere yakın geçen salınım ayağını da basılı saydı. Bu turda temas, animasyon klibinin kendi `contact_l/r` eğrisinden alındı (`scripts/an_slide2.py`, `an_start.py`). Her temas tüm kayıt boyunca, duruşlar ve ilk adımlar dahil tek tek listelendi.

Bu yöntemle önceki sayıların bir kısmı farklı çıktı:
- Düz ilk adım kayması 14–16 değil, 2–4 cm.
- "Tempoda yana durma 51–60 cm" bir duruş değildi; 180° dönerek başlama klibindeki bir basıştı. Bu da düzeltildi (bölüm 2).

## 2. Hareket: bulunan nedenler ve uygulanan düzeltmeler
| Sorun | Kaynak | Düzeltme (varlık) |
|---|---|---|
| Tempo ve geri tempo duruşunda ayak kayması (19–25 cm) | Fren profili tek bir hız eşiğinde ölçekleniyordu. 278 ve 234 cm/s'lik tempo, 375 cm/s'lik duruş klibinin içinde kayıyordu. | `AC_Sph_Motion`: fren ölçeği her duruşta, duruş klibinin kendi hızından ve bırakma hızından hesaplanıyor; pencere içindeki en düşük oran kullanılıyor. Tempo duruşları Relaxed koşu duruşuna eşlendi (`ABP_Sph_GASP`). |
| Yürüyüşte S ile başlama (26 cm) | `GR_Back` girdi vektörünü bir sonraki karede okuyordu. İlk arama "arkaya dönüp yürü" klibini seçiyor ve 0,4 s onda kalıyordu. | `BP_HybridA_Player`: tuş girdisi aynı karede (`GR_RawIn`); piyon kontrolcüden sonra işleniyor. `ABP_Sph_GASP`: dönüş modu değişince hareket araması yeniden yapılıyor. Yeni `PSD_Sph_N_Walk_S_Starts` ve `PSD_Sph_N_Run_S_Starts` (geri/yan başlangıçlar, arkaya dönme klipleri yok). |
| Sprintte W→S (50 cm) | Sprint hızında koşu pivotu oynuyordu; sprint için pivot klibi yok. | `GR_StopHold`: 470 cm/s üstünde S'ye basılınca hareket girdisi 80 cm/s'nin altına inene kadar bekletiliyor. Önce sprint duruşu, sonra geri başlangıç geliyor. W, A veya D bekletmeyi hemen iptal ediyor. |
| Tempoda ileri başlangıç (75 cm) | Core Motion'ın 180° dönerek başlama klibi kendi içinde kayıyordu. | Tempo ileri başlangıçları Neutral koşu başlangıçlarına eşlendi. |
| Geri tempo → ileri koşu (21–30 cm) | Shift basılıyken koşu kademesi hemen devreye girdi; 375 cm/s'lik pivot 234 cm/s'den oynadı. | Ters dönüş bitene kadar tempo kademesi korunuyor (aynı ailenin pivotu). |
| Koşuda A↔D (21 cm) | Önceki turdaki "yumuşak ters dönüş" sürtünmesi. | `RevOn` kapatıldı. Dönüş süresi yine 0,22 s. |
| Dönerek başlamada "başlangıç kapağı" denemesi | – | Reddedildi (yavaşlattı, kaymayı 42 cm'ye çıkardı). Kod duruyor ama kapalı. |

**Son durumdaki kayma ölçümleri** (editör yeniden açıldıktan sonra kaydedilmiş durumda; `data/verification_final_reopened.txt`). Her hücre: tüm basışların ortalaması / %90'lık dilimi / en kötü tek basış (cm).

| Plan | 60 Hz | 30 Hz | 22–60 Hz değişken |
|---|---|---|---|
| A: koşu yön değişimleri (ileri/geri/yan/çapraz, tempo-geri) | 1,6 / 2,6 / 13,1 | 1,9 / 5,0 / **22,8** | 1,8 / 2,7 / 15,1 |
| B: sprint, yürüyüş, kısa dokunuşlar | 1,9 / 2,6 / 16,7 | 1,9 / 4,1 / 15,6 | – |
| S: başlangıçlar (dönerek başlama ve gerçek X ile tempo dahil) | 1,6 / 2,9 / 15,5 | – | – |
| Q: tempo duruş ve dönüşleri (gerçek X) | 1,7 / 2,8 / 14,0 | 1,5 / 2,8 / 14,2 | – |
| X: gerçek X ile tempo akışı | 1,9 / 2,8 / 16,5 | – | – |

- **10 cm üstünde kalan tek basışlar:**
  - koşu W→S pivotu 13 cm
  - koşu A→D 180° 10–13 cm
  - sprint D→A 17 cm
  - yürüyüş S→W pivotu 15 cm
  - tempo/koşu duruşlarında 14–17 cm
  - **30 Hz'de koşu duruşu 22,8 cm.** Kapsül, klibin hızına uyuyor (0,40 s / 69 cm); ayak kaymasının kaynağı klip pozunun kendisi. Düzelmedi.
- **Duruş süreleri / yolları:**
  - yürüyüş 0,38–0,55 s / 34–60 cm
  - tempo 0,38–0,62 s / 51–106 cm
  - koşu 0,55–0,67 s / 96–155 cm
  - sprint 0,58–0,63 s / 137–163 cm
  - 30 Hz'de bir koşu duruşu 0,40 s / 69 cm (aynı 30 Hz örneği)
- **Ani poz kopması (kare başına 14° veya 6 cm üstü):** 12 kayıtta toplam 4 tek kare.

**Gerçek X tuşu akışı (yeniden açılmış durumda):** kaydedilen karakter tempo kapalı başlıyor. Sırayla: X ile tempo açılıyor (278) → Shift ile koşu (415) → Shift bırakılınca tempo (278) → dur → başla → S ile geri tempo (234) → yan ve çapraz yönler → X ile tempo kapanıyor → yürüyüş (180) → geri yürüyüş (150).
- Geri yürüyüşte 150 ile 127,5 farkının kaynağı: karakter hareket bileşeninin en düşük analog yürüyüş hızı 150. Geri çarpanı 1,0 yapıldı; ayar ve gerçek hız artık ikisi de 150.
- Gamepad (sağ omuz) bağlı, ama gamepad ile hiç denenmedi.

**İlk adım ağırlık aktarımı:** yürüyüş başlangıçlarında pelvis destek ayağına ilk adımdan önce 1–2 cm, dönerek başlamalarda 3–5 cm kayıyor; bunlar GASP kliplerinin kendi içeriği. Ayrı bir APA katmanı eklenmedi.

## 3. Ev içi akışlar (hepsi gerçek E / fare girdisiyle)
| Akış | Sonuç | Düzeltme |
|---|---|---|
| Depo / WC kapısı | ÖLÇÜLDÜ: depoya nişan alınınca depo, WC'ye nişan alınınca WC açılıyor | İki kapının etkileşim küresi menteşe hattından kendi açıklığının ortasına taşındı (`L_GR_CurrentHouseContent`) |
| Şömine | GÖRÜLDÜ: alev kütüklerin üstünde. Yandıktan sonra "Odun koy / Yak" istemi artık çıkmıyor. | Alev efektleri yaklaşık 40 cm aşağı çizim farkına göre yeniden yerleştirildi (`L_GR_SphirusHouse`). Hub, ateş ve çay bittiğinde istasyon etkileşimini kapatıyor (`BP_GR_DayHub` + `GR_FireSt/GR_TeaSt`). |
| Odun akışı | ÖLÇÜLDÜ: tam akış PASS (odun al, taşı, yar, 2 parçayı topla, şömineye koy, yak) | – |
| Çay | ÖLÇÜLDÜ: önceki akıştan kalan kayıt yüklendi → ot toplandı (Herb 1) → mutfağa yürüyüp demlendi (Herb 0, Tea 1) → içildi (Tea 2) → kontrol geri geldi | **Hata bulundu ve düzeltildi:** içme animasyonundan sonra istasyon zinciri tamamlanmıyor, karakter kalıcı olarak kilitli kalıyordu (`BP_GR_DayStation`) |
| Gardırop | GÖRÜLDÜ/ÖLÇÜLDÜ: kapı açıldı, ikinci kıyafet seçildi; karakter mavi üst ve uzun pantolonla göründü | – |
| Kayıt / yükleme | ÖLÇÜLDÜ: gardıroptan sonraki kayıt yeni bir oyunda yüklendi; kıyafet 2, Woke 2, ateş 2, çay 2 korundu, ateş istasyonu kapalı | – |
| Yatak ve gün geçişi | ÖLÇÜLDÜ/GÖRÜLDÜ: E ile yatılıyor, fare ile kalkılıyor/uyunuyor. Ekran kararıyor; yeni gün başlıyor (ateş söndü, çay 0, gardırop kapalı, gün sayacı +1, kıyafet 0). Uyanma yatak odasında görünüyor, kontrol geri geliyor. | **Gün geçişi yoktu, eklendi:** `GR_Sleep` (`BP_GR_DayHub`). **Uyanma kamerası** (0,0,3000) noktasında kalmıştı; oyunun ilk açılışında da orman tepesini gösteriyordu. Kamera artık yatağın yanına konumlanıyor. |
| Maske | ÖLÇÜLDÜ: E ile alındı, ele bağlandı, incelendi, E ile aynı yere (397,226,244.5) bırakıldı, aşama 1, kontrol geri geldi | Omuz kamerasından inceleme sırasında maske iyi görünmüyor (düzeltilmedi) |
| Bekleme | ÖLÇÜLDÜ: 160 s'de 7 mola, aralıklar 14–26 s; eller her an göğsün en az 36 cm altında. Harekete geçince ilk adım 0,5 s'de 180 cm/s. | – |

**Açılış görünümü:** "Gri üst" çıplak bir mesh hatası değil, günün başındaki kıyafet 0 (tank üst ve şort). Saç her testte görünür (groom açık).

## 4. Performans
- **Ölçüm koşulu:** editör PIE, ev haritasında önceki turla aynı rota, RTX 4060 Laptop, oyun görüntüsü 1510×922. TSR'nin iç çözünürlüğü ölçülmedi.
- **Sonuç:** kare süresi medyan 31,8 ms (~31 fps), GPU 30,4 ms. En büyük kalemler ShadowDepths 8,3 ms ve NaniteVisBuffer 3,5 ms. Önceki turda aynı rota 28,5 ms ölçülmüştü; editör oturumları arasındaki fark bu düzeyde oynuyor.
- Bu turda grafik ayarı değiştirilmedi. Standalone oyunda ve paketlenmiş sürümde ölçüm yapılmadı.

## 5. Doğrulanamayan ya da açık kalanlar
- **30 Hz koşu duruşu:** en kötü tek basış 22,8 cm. 10–17 cm'lik tek basışlar (yukarıda listeli) sürüyor.
- **Ham kaynak ve retarget karşılaştırması:** bu turda yeniden yapılmadı. Önceki turun sürücü (kaynak) ve görünür beden karşılaştırması geçerli; saç ve kıyafet gizlenerek eklem incelemesi yapılmadı.
- **Kamera:** dar alan, merdiven ve etkileşim kamerası ayrıca ölçülmedi. Maske incelemesinde nesne görünmüyor.
- **Eğim, merdiven ve iniş pozu:** bu turda yeni ölçüm yok. Zıplama (3 hızda) ve çömelme çalışıyor.
- **Standalone ve paketleme:** bu turda yapılmadı.
- **4 eklenti:** 5.9 sürümlerinin kurulması gerekiyor (kullanıcı işlemi).
- **Görev sırası:** gardıroptan sonra eklenen görev metni, çay zaten içilmiş olsa da "Bitki topla ve çayı hazırla" diyor.

## 6. Geri dönüş
- Her yazımdan önce yedekli manifest alındı (`data/manifests_20261120.txt`, `ue59_m23_*`).
- Tur başındaki dosya yedeği: `Saved/UE59Work/checkpoints/20261120_round3_start/`.
- `Config/DefaultInput.ini`'nin önceki hâli aynı klasörde (`DefaultInput.ini.pre_shift`).

## 7. İçerik
- `scripts/`: düzenleme, yazım ve ölçüm betikleri
- `data/`: tablolar, planlar, son durum ve Blueprint dökümleri
- `raw/`: ham kayıtlar (gz)
- `evidence/`: kare şeritleri
- `videos/`: çay, şömine, gardırop, yatak/gün geçişi, maske ve tam ev akışı. Videolar 30 Hz sabit adımla kaydedildi; birkaç kare düşebildiği için oynatma ±%5 sapabilir.

Dünya görseli değişti (şömine alevi), ancak Bridge dışa aktarımı bu turda yapılmadı.
