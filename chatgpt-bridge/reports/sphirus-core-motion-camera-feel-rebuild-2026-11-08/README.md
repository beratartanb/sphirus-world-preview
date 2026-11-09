# Sphirus: Core Motion hareket hissi ve yakın omuz kamerası yeniden kurulumu

Tarih: 2026-11-08 gece, 2026-11-09 sabahına kadar. Motor UE 5.8.4, harita `/Game/GraceRanger/Maps/L_GR_SphirusHouse`, oyuncu `BP_HybridA_Player`, sürücü `ABP_Sph_Driver`, görünür gövde `ABP_Sph_Body` + `RTG_Sph_Core_to_MH2`.

Kullanıcı 8 Kasım akşamı bizzat oynadı ve hareket/kamera hâlini reddetti. Bu rapor kök nedenleri, yapılan mimari değişiklikleri ve gerçek hızdaki kesintisiz oynanış videolarıyla alınan kanıtları ayrı ayrı yazar. **Teknik PASS, görsel PASS ve kullanıcı kabulü (REVIEW_REQUIRED) ayrı sütunlardır.** Yapılmayan veya görsel olarak doğrulanmayan hiçbir maddeye PASS verilmemiştir.

Geri alma noktası: `C:\Users\berat\SphirusCheckpoints\CoreMotionCamera_20261108_2000` (oyuncu, sürücü, MM, istasyonlar, haritalar, Config, kayıtlar; 125 MB). Kullanıcının kayıt dosyası her testten sonra geri konmuş, son hâli 20:03 tarihli kendi kaydıdır.

## 0. Sonuç özeti (P0)

| P0 maddesi | Teknik | Görsel / his | Not |
|---|---|---|---|
| Gait seçimi: gerçek, ayrı yürüyüş / jog / koşu | PASS | REVIEW_REQUIRED | Üç gait veritabanı + sabit hızda döngü veritabanları; yürüyüşte `Walk_Fwd`, jogda `Jog_Fwd`, koşuda `Run_Fwd` döngüleri gerçekten oynuyor (§5.1). Hız kademeleri 180/300/500 (ev içi 150). |
| "Aynı animasyonun hızlandırılması" / kukla yürüyüş | PASS (ölçüm) | REVIEW_REQUIRED | Kök neden ölçüldü: arama başlangıç kliplerinin ivmelenme penceresinde dönüyordu (§1). Döngü veritabanlarıyla sabit hızda döngü oynuyor; ayak basış hızı yürüyüşte 49–81 → 22–36 cm/s. |
| Başlangıç / duruş / fren / dönüş | PARTIAL | REVIEW_REQUIRED | Başlangıç ve duruş klipleri doğru aşamada (ilk 0,7 s başlangıç, duruşta Stop → boşta). 180° dönüşte fren-dön-başla okunuyor; pivot klibi nadir; Inertialization eklenemedi; stride warping yok. |
| Efor / nefes | PARTIAL (önceki tur) | REVIEW_REQUIRED | Nefes katmanı yalnız montaj duraklamasında; koşu sonrası nefes/efor katmanı yok. |
| Kamera yakınlığı ve hız bağlı yumuşak tepki | PASS | REVIEW_REQUIRED | Kol ev içi 85–115 / dış 105–140 (+12 hızda), konum ve dönüş gecikmesi; 180° dönüşte mesafe titremesi 17,4 → ≤1,5. |
| Yakın omuz üstü aksiyon kamerası | PASS (teknik) | REVIEW_REQUIRED | Aksiyonda kol 70, omuz 17, bakış −18; karakter sol üçte bire alındı (omuz = 0,24 × kol). `D_chop_final4`: aksiyonda kamera–baş mesafesi 144 → 110 cm (ilk kesme denemesinde E tetiklenmedi, test kurulumu düzeltildi). |
| Dar koridor kamera çarpışması | PASS (teknik) | REVIEW_REQUIRED | Gerçek ev koridorunda kamera 93–126 cm, sonda 10; titreme ≤0,5 düz yürüyüşte, girişte 1,9. Ayrı test haritası siyah render ettiği için kullanılmadı. |
| Odak: merkez net, kenar yumuşak | PARTIAL | REVIEW_REQUIRED | Cine kamera DOF (f/9 serbest, f/4 aksiyon) + EdgeSoft; köşeler %40–70 yumuşadı ama merkez de ~%20 yumuşadı (§4). |
| Gerçek hızda kesintisiz video kanıtı | PASS | — | `*_final3`, `P_steady4`: oyun adımı 0,033 s/kare. |

Yapılmayan / açık: Inertialization, stride/orientation warping, koşu-sonrası efor katmanı, kesme aksiyonunun 3. tur videosu (yeniden kayıt), P1/P2 maddelerinin çoğu (§7), kullanıcı kabulü.

## 1. Audit: kullanıcının yaşadığı sorunun kök nedenleri

Ölçüm yöntemi: `Tools/Day_20261107/vid.py` her oyun karesinde kapsül, hız, yaw, kamera, görünür ve gizli sürücü kemiklerini kaydeder; `an_clip.py` gizli sürücünün o karede oynattığı klibi, 45 klibin 3.732 karelik poz kütüphanesine (`cliplib.json`, altı kemik, kök-göreli) en yakın komşuyla bulur. Eşleşme mesafesi 1–5 cm; başlangıç ve döngü kliplerinin birbirine çok benzediği karelerde klip adı değişebilir, aile (yürüyüş/jog/koşu) güvenilirdir.

| Kullanıcının gördüğü | Ölçülen kök neden | Kanıt |
|---|---|---|
| Hız artınca aynı yürüyüşün hızlandırılmışı | Tek veritabanı (`PSD_Sph_Loco2`, 44 klip) jog ve koşu hızında bile **yürüyüş** kliplerini seçiyordu: 221 cm/s'de `Walk_Fwd_Start/Stop`, 331 cm/s'de `Walk_Fwd_Stop/Start/Fwd`; jog ve koşu klipleri hiç seçilmedi. Oynatma hızı 1,2'ye kadar yükseliyor, ayaklar kayıyordu. | `data/A_loco_before.json`, `an_clip_before.txt`: SEG 2 (221 cm/s) {Walk_Fwd_Start 20, Walk_Fwd_Stop 4}, SEG 4 (331 cm/s) {Walk_Fwd_Stop 19, Walk_Fwd_Start 18, Walk_Fwd 8} |
| Yürüyüş kesik kesik, kukla gibi | Sabit yürüyüşte seçim her saniye 15–19 kez başlangıç/duruş/dönüş-başlangıç klipleri arasında değişiyor, yürüyüş döngüsü (`Walk_Fwd`) nadiren seçiliyordu. Karışım 0,25 s, devam eden poz yanlılığı −0,01 (çok küçük). | `an_clip_before.txt` SEG 1 (124 cm/s): {Walk_Fwd_Start 48, Walk_Fwd 9, Walk_Fwd_Stop 7}, 19 değişim/s |
| Dönüşler yapay | Dönüşlerde de aynı aile karışımı; 180° dönüşte `Walk_Start_TurnL/R180` nadiren; pivot klibi hiç. Dönüş hızı 300°/s (akşam 0'dan geri getirilmişti) karakteri hızla çeviriyor, animasyon yetişmiyor. | `B_turns_before.json` SEG 2/4 |
| Kamera uzak ve cansız | Kol 120–165 cm dış, +18 hızda; konum gecikmesi 10/s, dönüş gecikmesi kapalı; 180° dönüşte kol mesafesi karede 17 cm sıçrıyordu. | `an_vid` B_turns_before SEG 4: cam jit 17,4 |
| Aksiyon kamerası kötü | Kesme ve şömine istasyonlarında hâlâ sabit `CameraActor`'a geçiş vardı (akşam kaldırıldı); kalan yakın mod kol 90, omuz 38, bakış −22 ile hâlâ uzaktı. | `D_chop_before.mp4` |
| Kenar yumuşatma gerçek odak değil | `M_Sph_EdgeSoft` radyal 9 örnekli post-process; gerçek alan derinliği yoktu. | önceki rapor |

**Gait veritabanlarından sonra ikinci audit (MM sondası, gerçek zamanlı koridor kaydı `CA_loco_final`):** sürücüdeki `MM_Asset` sondası artık geçerli (PoseHistory etiketi eklendikten sonra). Düz yürüyüşte (165 cm/s) seçim saniyede **7,0 kez** klip değiştiriyor: `Walk_Fwd_Start` 59, `Walk_Fwd_Stop` 25, dönüş-başlangıç 6 kare; yürüyüş döngüsü `Walk_Fwd` 402 karenin yalnız 4'ünde. Koşuda ise `Run_Fwd_Start` 74 kare, 1,7 değişim/s. Kök neden: her klip veritabanına **tüm süresiyle** (BranchIn 0–son) girmişti; başlangıç kliplerinin sabit hızlı kuyruğu ve duruş kliplerinin hâlâ yürüyen başı döngüyle aynı pozları sunuyor, arama sürekli bunlar arasında atlıyor (kullanıcının "kesik, hızlandırılmış klip" hissi). Çözüm §2'de (klip aralıklarının kırpılması). Duruşta da `Stand_Idle_Turn*` kliplerinin boşta kuyrukları seçiliyordu (SEG 4: 11,9 değişim/s).

**Üçüncü audit — asıl kök neden (gövde pozunun klip zamanı, `an_times.py`):** görünür gövdenin her karesi poz kütüphanesinde klip **ve klip zamanı** ile eşlendi. Düz yürüyüşte (170 cm/s) gövde yalnız `Walk_Fwd_Start` 0,7–1,2 s (kök hızı 133–194) ve `Walk_Fwd_Stop` 1,9–2,1 s (156–133) pencerelerinde; 1,3 s sonrası ve `Walk_Fwd` döngüsü hiç yok. Koşuda (393–480 cm/s) gövde `Run_Fwd_Start` 0,6–1,2 s (255–411 cm/s) penceresinde: kapsül 480 giderken 255–411'lik ivmelenme karelerinin oynatılması, kullanıcının "koşu yürüyüşün hızlandırılmış hâli" dediği görüntünün ölçülmüş karşılığıdır. Sürücüdeki sıfırdan arama sondası da aynı pencereleri seçiyor (Start 0,2–0,7). Neden: şemanın (`PSS_Sph_Loco`, UEFN `PSS_Default`'tan türetilmiş) tek geçmiş yörünge örneği −0,05 s (ağırlık 0,3); arama "yürümekteyim" ile "yeni başladım"ı ayıramıyor, poz kanalı (devam eden poz sorgusu) aramayı başlangıç penceresine kilitliyor. Klip kırpma bunu çözmez (pencere kırpılan aralığın içinde).

Denenen ve **işe yaramayan** düzeltmeler (her biri yazıldı, editör yeniden açıldı, 7,7 s'lik sonda videosu ile gövde pozu ölçüldü; `P_traj*.json`): (1) şemaya geçmiş yörünge örnekleri −0,6/−0,3 s eklemek (ilk deneme `ObjectTools.set_properties` dizi yazamadı, ikinci deneme yapı olarak yazdı); (2) poz geçmişi düğümünün dışarıdan bağlı `Trajectory` pinini ayırıp düğümün kendi yörünge üretimine bırakmak (önceki oturumda olay grafiğinde üretilen yörünge bağlanmıştı); (3) poz geçmişi derinliğini 2 → 24 poz (0,96 s) yapmak. Üçünde de seçim birebir aynı kaldı. Ayırıcı deney: **poz kanalları 0, yalnız yörünge** ile arama sabit 165 cm/s'de yine `Walk_Fwd_Start@0,5 s`'yi (90 karenin 74'ü) seçti; **yörünge 0, yalnız poz** ile boşta dönüş kliplerini seçti. Motorun yörünge üretme fonksiyonu doğrudan çağrılınca (`trajprobe.py`) geçmiş −0,3 s'de −55 cm, gelecek +1 s'de +180 cm veriyor, yani üretilen yörünge doğru; yürüyen sorgunun neden döngü yerine ivmelenme penceresini seçtiği bu turda kanıtlanamadı (REVIEW: şema özellik bayrakları, DDC indeks önbelleği). Çözüm mimariye alındı: §2 "sabit hız döngü veritabanları".

Ek bulgu (kayıt aracı): editör PIE'de `t.FixedFrameRate` uygulanmıyor; ekran görüntüsü yazan karelerde oyun adımı ~0,115 s oluyordu. İlk "önce" videoları bu yüzden gerçek zamanın ~3,4 katı hızlı oynar; ilk sürüm `videos/*_before.mp4` yalnızca karşılaştırma içindir. Sonraki kayıtlarda kare başına zaman ölçeği (1/30)/gerçek kare süresi olarak ayarlanır ve her karenin oyun adımı `gdt` olarak kaydedilir.

## 2. Hareket mimarisi değişiklikleri

- **Gait'e göre ayrılmış veritabanları** (`Tools/Day_20261107/cm_gaitdb.py`): `PSD_Sph_Walk` (boşta + 8 boşta dönüş + 14 yürüyüş klibi = 23), `PSD_Sph_Jog` (boşta + 14 jog = 15), `PSD_Sph_Run` (boşta + 7 koşu = 8). Aynı şema (`PSS_Sph_Loco`). Klipler ikinci bir `BranchIn` izi ile gait veritabanına bağlı; `PSD_Sph_Loco2` dokunulmadan duruyor (`ForceLegacy` anahtarıyla karşılaştırma için).
- **Gait seçimi** (`cm_gait1.py`): oyuncu her tikte `GR_GaitSel` yazar (0 yürüyüş, 1 jog = Shift, 2 koşu = Shift 0,9 s + hız > 250). Sürücü çömelme yoksa `GaitSel`'e göre veritabanını seçer.
- **Hız–klip kalibrasyonu**: Core Motion klip kök hızları yürüyüş 197, jog 294, koşu 532 cm/s. Kapsül hızları 165/330/480 → **180 / 300 / 500** (ev içi 150). Oynatma hızı aralığı 0,7–1,25 → doğal hızın %91 / %102 / %94'ü. İvme 900 → 450, fren 700 → 650, dönüş hızı 300 → 260°/s.
- **Yörünge tahmini**: 8 × 0,4 s → 6 × 0,25 s (1,5 s ileri).
- **Seçim kararlılığı** (`cm_mm4.py`): devam eden poz yanlılığı −0,12, döngü yanlılığı −0,15, karışım 0,3 s.
- **Klip aralıklarının kırpılması** (`q_trim.py` ölçer, `cm_trim1.py` uygular; `data/trim_plan.json`): her klibin kök hız / kök yaw profili root kemiğinden 0,1 s adımla çıkarıldı. Gait veritabanı BranchIn aralıkları: başlangıç klipleri 0 → (hızın %90'ına ulaştığı an + 0,25 s) (ör. `Walk_Fwd_Start` 2,50 s'nin 0–1,45 s'si; `Run_Fwd_Start` 0–1,65); duruş klipleri (yavaşlamanın başladığı an − 0,25) → (durduktan 0,4 s sonra) (`Walk_Fwd_Stop` 1,25–3,30 / 4,27; `Jog_Fwd_Stop` 0,05–1,70; `Run_Fwd_Stop` 0,05–1,80); boşta dönüşler 0 → (yaw hareketi bittikten 0,3 s sonra). Döngüler, pivotlar ve boşta klibi tam kalır. `PSD_Sph_Loco2` (eski) kendi tam aralıklı izini korur. 34 klip, proje kopyaları (`/Game/Sphirus/Player/Anim/Core/`); satıcı dosyalarına dokunulmadı.
- **Sabit hız döngü veritabanları — durum güdümlü veritabanı seçimi** (`cm_steady1.py`): `PSD_Sph_WalkLoop` (Walk_Fwd, FwdLeft, FwdRight), `PSD_Sph_JogLoop` (Jog_*), `PSD_Sph_RunLoop` (Run_Fwd). Oyuncu her tikte `GR_Steady` hesaplar: hız, hareket bileşeninin azami hızının ±%15'i içinde, hız yönü ile yüz yönü arası < ~12°, hız > 60 ve bu koşul ≥ 0,35 s sürmüş (`GR_SteadyT`). Sürücü `Steady` iken gaitin döngü veritabanına geçer (arama yalnız döngü pozları arasından faz eşleştirir, 0,3 s karışım); başlangıç, duruş ve dönüşler tam gait veritabanlarından gelir; `ForceLegacy` yolu dokunulmadı. **Sonda ölçümü** (`P_steady4.json`, gerçek zamanlı): düz yürüyüşte gövde 90 karenin 47'sinde `Walk_Fwd` döngüsünde (önce 0), geri kalan başlangıç (ilk ~0,7 s) ve dönüş-başlangıç; sıfırdan arama sondası `Walk_Fwd@0,0/0,2` 64 kare. Koşuda `RunLoop` 59 kare seçili; gövde Jog_Fwd / Run_Fwd / koşu başlangıcı karışımı (Shift'in ilk 0,9 s'i jog gaitinde geçiyor).
- Şema (`PSS_Sph_Loco`) bu turda: yörünge kanalı ağırlığı 1,0 → 1,3, örnekler −0,6/−0,3/−0,05/0/0,35/0,7/1,0 s; poz geçmişi 24 poz × 0,04 s, yörünge geçmişi 26 × 0,04 s, tahmin 6 × 0,25 s; poz geçmişi düğümünün dış yörünge pini ayrıldı (düğüm kendi üretir).
- Korunanlar: `IK_Sph_CoreSrc`, `RTG_Sph_Core_to_MH2` (TargetRoot=root), kök hareketi yok sayma, gizli MCPaul sürücü, boşta kapısı, nefes katmanı, yatak modu.
- Yapılmayan: Inertialization düğümü bu editörün yerelleştirilmiş paletinden eklenemiyor; stride/orientation warping eklenmedi (ölçüm sonrası karar).

## 3. Kamera

`cm_cam7.py`: kol ev içi 85–115, dış 105–140 (önce 85–125 / 120–165); hızda +12 (önce +18); kol yumuşatma 2,2/s; yay kolu konum gecikmesi 7/s (45 cm), **dönüş gecikmesi 14/s açıldı**; sonda 10. Aksiyon (bakış girdisi kapalı): kol 70, omuz 34, yükseklik +8, bakış −18. Omuz ofseti 30–38 / 36–44 (akşam değeri).

**Omuz ofseti kol uzunluğuyla orantılı** (`cm_cam8.py`): sabit 30–44 cm omuz, kol kısalınca karakteri kare kenarına itiyordu (kesme videosunda kol 70 ile karakter merkezi genişliğin ~%13'ünde, gövde kenardan kesik; `evidence/D_chop_final_12.png`). Hedef her kolda sol üçte bir: omuz ≈ 0,24 × kol → ev içi 21–27, dış 26–33, aksiyon 17.

## 4. Odak ve kenar

Post-process yapı pinleri bu editörün Python'unda çöküyor; alan derinliği için `cm_dof1.py` görünür kamerayı `CineCameraComponent`'a taşır: f/9 serbest dolaşım, f/4 aksiyon; odak mesafesi kamera ekseni boyunca görünürlük ışını (120–3000 cm, boşta 1500) veya aksiyonda sağ el; yumuşatma 5/s. `M_Sph_EdgeSoft` hafif (%10–30 köşe) kalır.

Ölçüm (aynı konumda boşta duran karakter, Cine öncesi `A_loco_after` / `D_chop_after` ile Cine sonrası `A_loco_final` / `D_chop_final` kayıtlarının 6–18. kareleri, Laplace keskinliği ×1e4, beş kare ortalaması; `sharp.py`):

| Bölge | Bahçe önce → sonra | Kesme önce → sonra |
|---|---|---|
| merkez (bakış noktası) | 50,2 → 41,1 (−18 %) | 11,9 → 9,2 (−22 %) |
| sol üst | 15,2 → 16,2 (+7 %) | 60,3 → 59,9 (0 %) |
| sağ üst | 10,9 → 9,9 (−9 %) | 13,9 → 14,5 (+4 %) |
| sol alt (yakın zemin) | 18,2 → 5,2 (−71 %) | 4,1 → 1,9 (−54 %) |
| sağ alt | 2,0 → 1,2 (−39 %) | 1,0 → 1,0 (0 %) |

Yorum: yumuşama derinliğe bağlı (yakın zemin ve uzak köşe), radyal değil; merkez de ~%20 yumuşamış, bu istenmeyen bir yan etki (odak mesafesi izleme/yumuşatma ya da sensör boyutu). Teknik PASS (Cine kamera etkin, odak ve diyafram her karede güncelleniyor), görsel **PARTIAL / REVIEW_REQUIRED**: "göz gibi merkez net, çevre hafif yumuşak" hissi EdgeSoft + bu DOF ile oyunda izlenmeli; gerekirse serbest dolaşım f/9 → f/11 ve odak yumuşatma 5 → 8.

## 5. Önce / sonra ölçüm tabloları

Kaynaklar: önce = `data/A_loco_before.json`, `B_turns_before.json` (eski yapı, 8 Kasım 21:35, oyun adımı 0,115 s — hız ve kamera sayıları geçerli, saniye bazlı oranlar değil); ara = `CA_loco_final.json` (gait veritabanları, kırpma ve döngü veritabanları olmadan, gerçek zamanlı koridor); sonra = `*_final3.json` (gerçek zamanlı, adım 0,033 s; `data/an_final_round3.txt`, `an_times_round3.txt`). "Gövde" sütunu görünür gövdenin poz kütüphanesinde eşlendiği klipleri verir (başlangıç kuyruğu ile döngü birbirine çok benzediği için koşuda `Run_Fwd_Start` etiketi `Run_Fwd` döngüsünü de kapsar).

### 5.1 Hangi klipler oynuyor

| Durum | Önce (eski yapı) | Ara (gait DB) | Sonra (döngü DB) |
|---|---|---|---|
| Düz yürüyüş ~160 cm/s | 124 cm/s: Walk_Fwd_Start 48, Walk_Fwd 9, Stop 7 (saniyede 19 değişim) | 165 cm/s: Start 59, Stop 24, pivot 4; gövde Start 0,7–1,2 s penceresinde döner, döngü 0 | A: 60 karenin 22'si `Walk_Fwd`, 18 başlangıç (ilk ~0,7 s), 5 dönüş-başlangıç; H (koridor): 75 karenin 35'i `Walk_Fwd`; veritabanı 0,7 s sonra WalkLoop |
| Jog ~260–300 | jog klibi hiç seçilmedi (221 cm/s'de Walk_Fwd_Start/Stop) | Jog_Fwd_Start 0,7–1,2 s | A SEG 2 (ivmelenirken 260): Jog_Fwd 12, Walk_Fwd 9; H SEG 2 (150, ev içi): JogLoop 42 kare |
| Koşu ~460–500 | koşu klibi hiç seçilmedi (331 cm/s'de Walk_Fwd_Stop/Start) | Run_Fwd_Start 0,6–1,2 s (kök hızı 255–411) | A SEG 4 (499): RunLoop 39 karenin 28'i, sonda Run_Fwd 27; gövde koşu döngüsü/kuyruğu 29 |
| Koşudan yürüyüşe (Shift bırak) | — | — | A SEG 5 (284→180): Walk_Fwd 13, dönüş-başlangıç 9 |
| Duruş | Walk_Fwd_Stop kuyruğu + boşta dönüş klipleri | aynı | boşta kapısı 0,35 s sonra `af_Stand_Idle_01`; önce Walk_Fwd_Stop 7–8 kare |
| 180° kamera dönüşü yürürken (B SEG 2–3) | Walk_Fwd_Start/Stop karışımı | — | dönüşte Walk_Fwd/FwdRight/Pivot, ardından hız 180 → 77'ye düşüp yeniden ivmelenme (`Walk_Fwd_Start`, `Start_TurnR045`): fren-dön-başla okunuyor |

### 5.2 Ayak, hız, kamera

| Ölçüm | Önce | Ara | Sonra |
|---|---|---|---|
| Basılı ayak hızı p20, yürüyüş (cm/s; düşük iyi) | ölçüm 0,115 s adımla şişkin | 49–81 (CA SEG 1/3) | A: 28–34, B: 22, H: 36 |
| Basılı ayak hızı p20, koşu | — | 83 | 106–139 (kısa basış fazı: metrik kaymayı tek başına ölçmez) |
| Kapsül hızları yürüyüş / jog / koşu | 124–331 (tek veritabanı, hız kademesi yok) | 165 / 413 / — | 158 / 260–300 / 499; ev içi 136–150 |
| Kamera–baş mesafesi boşta / yürüyüş / koşu | 147 / 170–175 / 195 (önce kol 120–165) | 147 / 171 / 193 | 121–147 / 153–164 / 193–196; ev koridoru 93–126 |
| Kamera mesafe titremesi 180° dönüşte | 17,4 | 0,67–1,5 | 0,23 (yürüyüş B SEG 2), 1,07–1,49 (koşu dönüşü B SEG 15–16) |
| Karakterin karede yeri | sol kenar, aksiyonda kesik | aksiyonda ~%13 (`evidence/D_chop_final_12.png`) | sol üçte bir (`evidence/A_loco_final3_f120.png`, `D_chop_final3_f240.png`, `H_hall_final3_f090.png`) |
| Oyun adımı / kare (video gerçek zamanlı mı) | 0,115 s (3,4× hızlı) | 0,033 (koridor), 0,10 (bahçe, 3×) | 0,033 ± 0,001 tüm videolarda |

Not: `*_legacy3` kayıtları `ForceLegacy` bayrağı çalışma zamanında etkili olmadığı için (`db` alanı her ikisinde de Walk/WalkLoop) final ile aynıdır; karşılaştırma değeri yoktur, videoları rapora konmadı (`data/*_legacy3.json` kanıt olarak duruyor). Gerçek "önce", eski yapının `*_before` videolarıdır.

## 6. Videolar

Tümü gerçek oyun (PIE), kesintisiz, 30 kare/s; `*_final3` ve `P_steady4` gerçek zamanlı (her karede oyun adımı 0,033 s). `*_before` eski yapıdır ve ~3,4× hızlı oynar (kayıt aracı hatası, §1); yalnız klip seçimi ve kamera davranışı karşılaştırması içindir.

| Video | İçerik | Durum |
|---|---|---|
| `videos/A_loco_final3.mp4` (11 s) | Bahçe: yürüyüş → jog → koşuya 180° dönüş → koşu → yürüyüş → duruş → yeniden yürüyüş → duruş | Teknik PASS (döngüler, gait kademeleri, gerçek zaman); görsel REVIEW_REQUIRED |
| `videos/B_turns_final3.mp4` (15 s) | Bahçe: 180° ×2, 45° zikzak, duruş, yerinde dönüş, jog/koşu dönüşü | Teknik PASS; 180° sonrası fren-dön-başla görünür; görsel REVIEW_REQUIRED |
| `videos/H_hall_final3.mp4` (10 s) | Ev alt kat koridoru: yürüyüş, jog, duruş, 180°, geri yürüyüş; dar geçitte kamera 93–126 cm | Teknik PASS; görsel REVIEW_REQUIRED |
| `videos/D_chop_final4.mp4` (11 s) | Kesme istasyonu: yaklaş, E, baltayı bekle, vur; aksiyon kamerası (kamera–baş 144 → 110 cm, bakış −18, omuz 17) | Teknik PASS; görsel REVIEW_REQUIRED (`evidence/D_chop_final4_f120.png`, `_f240.png`) |
| `D_chop_final3` (yalnız `data/D_chop_final3.json`) | İlk 3. tur kesme denemesi | **FAIL (test kurulumu)**: 0,8 s yaklaşma gerçek hızda istasyon menziline yetmedi, E tetiklenmedi; 1,15 s ile yeniden kaydedildi (final4). |
| `videos/P_steady4.mp4` (7,7 s) | Sonda: 3 s yürüyüş + 3 s koşu, döngü veritabanlarının ilk doğrulaması | Teknik PASS |
| `videos/A_loco_before.mp4`, `B_turns_before.mp4`, `D_chop_before.mp4` | Eski yapı (karşılaştırma; 3,4× hızlı) | referans |

Kare örnekleri: `evidence/A_loco_final3_f120.png` (yürüyüş, omuz üstü), `A_loco_final3_f240_run.png` (koşu), `B_turns_final3_f090.png`, `H_hall_final3_f090.png` (koridor), `D_chop_final3_f240.png` (istasyon önü, aksiyon kamerası yok).

## 7. P1 ve P2 maddeleri: durum

P0 bu turun tamamını aldı; P1/P2'de yalnız önceki turlarda yapılanlar korunmuştur, yeni iş yapılmamıştır.

| Madde | Durum | Not |
|---|---|---|
| E hedefleme (hysteresis, görünürlük) | NOT_DONE | Story Framework etkileşim yöneticisi değiştirilmedi. Parçalar E ile veya 80 cm yakınlıkta toplanıyor (önceki tur). |
| Odun kesme: fizikli parçalar, elle toplama, demet | PARTIAL (önceki tur) | 80 cm otomatik toplama hâlâ açık; kullanıcı niyeti açısından gözden geçirilmedi. Yonga zemini/bahçe yerleşimi yapılmadı. |
| Mutfakta çay alt adımları | NOT_DONE | Tek klip, kapak/ot/su yok. |
| Yatak örtüsü | NOT_DONE | Karakter örtünün üstünde yatıyor. |
| Vault / mantle / merdiven | NOT_DONE | Core Motion'da vault/mantle yok; başka paket aranmadı. |
| EnviroSense el teması | NOT_DONE | |
| Crouch / jump / land | PASS (önceki tur, kayıt) | Yerinde zıplamada toparlanma klibi yalnız gerçek düşüşte. |
| Giysi deformasyonu, kumaş görünümü | NOT_DONE | Atlet/şort oturuyor, kumaş materyali değişmedi. |
| Yaş / cilt detayı | FAIL | MetaHuman yüz ayrıntı ayarı betikten salt okunur; doku yolu denenmedi. |
| Ev–orman–bahçe yerleşimi | NOT_DONE | |
| Cook / paketlenmiş oyun | NOT_TESTED | |
| 30/60 FPS performans | NOT_TESTED | Editör kare süreleri 70–120 ms (ekran görüntüsü yazarken), oyun ölçümü yapılmadı. |
| Menüden save/load | NOT_TESTED | Kullanıcı kaydı korunuyor; yükleme testi yapılmadı. |

## 8. Dayanıklılık, kayıt, performans, geri alma

| Konu | Durum | Not |
|---|---|---|
| Derlenmiş, yeniden açılmış proje | PASS (teknik) | Her yazma işinden sonra editör kapatılıp yeniden açıldı (`relaunch.sh`); son video seti yeniden açılmış editörde kaydedildi. Derleme hatası yok (`errs()` kontrolleri). |
| Kullanıcı kaydı | PASS | Her test kaydı `SFSaveSlot.sav`'ı kenara alır ve geri koyar; son durum 20:03 tarihli kullanıcı kaydıyla bayt bayt aynı (zincir sonunda `cmp`). Yedekler: `Saved/Codex/Day_20261107/slot_user_backup_*.sav`. |
| Geri alma noktası | PASS | `C:\Users\berat\SphirusCheckpoints\CoreMotionCamera_20261108_2000` (125 MB) + her yazma işinin manifest yedeği (`Saved/Codex/SHME_V233_20261027/checkpoint/`). |
| Satıcı dosyaları | PASS | Core Motion klipleri yalnız proje kopyalarında (`/Game/Sphirus/Player/Anim/Core/`) değişti; satıcı paketi, Story Framework, AAMS dokunulmadı. AAMS geri gelmedi (oyuncu Character'dan türer; yeni AAMS referansı eklenmedi). |
| Menüden save/load | NOT_TESTED | |
| Cook / paketlenmiş oyun | NOT_TESTED | |
| 30/60 FPS performans | NOT_TESTED | Editörde ekran görüntüsü yazarken kare süresi 0,3–1,5 s; oyun içi ölçüm yapılmadı. MM sondası (`MM_Probe`) açık; kapatılması önerilir (küçük CPU maliyeti). |
| Çift orman / sahne mutasyonu | PASS | Ana haritada sahne eklenmedi/çoğaltılmadı; test koridoru ayrı harita (`/Game/Sphirus/Test/L_Sph_MoveTest`, PIE'de siyah render ediyor — kullanılmadı, silinmedi). |
| Günlük hataları (son PIE) | PASS | Son kayıt günlüğünde proje kaynaklı hata yok; `LogPoseSearch` "AsyncBuildIndex in progress" uyarıları PIE'nin ilk karelerinde (indeks yeniden kuruluyor), motorun kendi `UnifiedErrorTest` satırları bize ait değil. |
| MM sondası | AÇIK | `MM_Probe` (sıfırdan arama) ölçüm için açık bırakıldı; oyun sürümünde kapatılmalı (küçük CPU maliyeti). |

## Kontrol yöntemi

- Oyunda: `L_GR_SphirusHouse` açılır, PIE; W ile düz yürüyüş 2 s sonra ayaklar yere basan döngü, Shift ile jog, Shift 0,9 s + hız > 250 ile koşu; Shift bırakınca yürüyüşe iniş; W bırakınca duruş klibi → 0,35 s sonra boşta. Evin alt kat koridorunda (giriş → veranda kapısı) kamera 1 m'ye iner, duvara çarpmaz.
- Ölçümle: `Tools/Day_20261107/v55.sh <etiket> x y z yaw "<plan>"` gerçek zamanlı video + `Saved/Codex/Grip_20261106/rec/<etiket>.json`; `an_final.py` (hız, basış, kamera, MM sondası), `an_times.py` (gövdenin eşlendiği klip ve klip zamanı, veritabanı alanı). `db` alanı Walk/WalkLoop/Jog/JogLoop/Run/RunLoop geçişlerini gösterir.
- Geri alma: `C:\Users\berat\SphirusCheckpoints\CoreMotionCamera_20261108_2000` veya iş başına manifest yedekleri (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/day_*.json`).
- Değiştirilen varlıklar (hepsi proje kopyası): `BP_HybridA_Player` (GR_GaitSel, GR_Steady/GR_SteadyT, Cine kamera, omuz/kol değerleri), `ABP_Sph_Driver` (GaitSel, Steady, ForceLegacy, MM sondası, poz geçmişi ayarları), `PSS_Sph_Loco`, `PSD_Sph_Walk/Jog/Run`, `PSD_Sph_WalkLoop/JogLoop/RunLoop`, 41 Core Motion klip kopyasındaki `SphDB_*` notify izleri, `L_Sph_MoveTest` (test haritası).
