# İlk oynanış tamamlama raporu — Story Framework 5.2

Tarih: 5 Kasım 2026 · Karşılaştırma dayanağı: `de00d66` · Önceki rapor korundu.

**Sonuç: Genel teslim tam kabul değil.** Kayıt/envanter hatası kapandı ve akış baştan sona çalışıyor. Ama gerçek fare, gerçek gamepad ve gerçek insan oynanışı denenmedi; ses dinlenmedi; video yok. Maskeyi bağlama temiz bir geçici sunum, el animasyonu değil.

## Nasıl oynanır

Harita: `/Game/GraceRanger/Maps/L_GR_SphirusHouse` (açık projede doğrulandı; proje git kullanmıyor).

1. Play. Sağ üstte `Yarım kalan maskeye bak` görevi çıkar.
2. Eve gir, atölyedeki masada maskeye bak, **E** ile incele. Görev `Maskenin bağını tamamla` olur.
3. Veranda masasındaki `Bez Şerit`i **E** ile al. Oyun kaydeder.
4. Masaya dön, **E** ile `Şeridi bağla`. Şerit maskeye iner, oyun kaydeder.
5. **E** ile `Yerine koy`. Maske rafa gider, görev biter, günlük eklenir, oyun kaydeder.
6. İsteğe bağlı: göl kıyısında **E** ile `Manzaraya bak`.

| İşlev | Klavye/fare | Gamepad eşlemesi (denenmedi) |
|---|---|---|
| Etkileşim | E | Sağ yüz tuşu |
| İncelemede döndür / oku / geri | Fare / Q / F | Sağ çubuk / Sol yüz / Sağ yüz |
| Menü (görev, envanter, günlük) | J, sekmeler A ve D, geri F | D-pad yukarı |
| Hızlı envanter | G veya I | D-pad aşağı |
| Görev satırı | T | D-pad sol |
| Duraklat | P veya Esc | Menü tuşu |
| Yükleme | P → Son kaydı yükle | |

## Kök neden → düzeltme → sonuç

| # | Kök neden | Düzeltme | Sonuç |
|---|---|---|---|
| 1 | Doğrulandı: `HasItemInteraction`, `InteractWith("Found")` çağrısını yapıp şeridi ondan sonra siliyordu. Masa kaydı bu çağrının içindeydi | SF'nin otomatik tüketimi kapatıldı (`ConsumeItems=False`). Masa şeridi kendisi siler, sonra kaydeder. Yeni aşama 3 eklendi: 0 başlamadı, 1 görev açık, 3 bağlı masada, 2 rafta | Biten kayıtta şerit 0, iki yüklemede de |
| 2 | SF varsayılanı zamanlı otomatik kayıttı. Yeni oturum son kaydı sessizce eziyordu | `SaveMethod` elle kayda alındı. Kayıtlar güvenilir noktalarda: şerit alma, bağlama, yerine koyma, göl molası | Kayıt dosyası yeni oturumda değişmiyor |
| 3 | Şeridi aldıktan sonra kayıt alınmıyordu | `BP_GR_StripPickup` yok olunca kaydediyor; yalnız oyuncu gerçekten almışsa. Yüklemede SF'nin aktörü silmesi kayıt tetiklemez | Yeni oturumda şerit envanterde, dünyada yok |
| 4 | `DestroyPreviouslyDestroyedActorsOnLoad` boş dizide -1 okuyordu | `Find` bağlantısı doğrudan seviye adına alındı | Uyarı kalktı |
| 5 | Eski hatalı kayıtlar şeridi taşıyordu | Yalnız aşama 2 yüklenirse `Bez Şerit` bir kez silinir; başka eşyaya dokunmaz | Eski test kaydında envanter boş |
| 6 | Demo HUD `W_Sphirus_HUD` içinde görünürdü | Kontrol listesi, can çubuğu, sürüm ve karakter etiketi gizlendi; SF FPS sayacı da. HUD nesnesi duruyor, AAMS bağları bozulmadı | Oyuncu ekranında yok |
| 7 | SF ipucu TAB gösteriyordu | `UMCPromptInput` J yapıldı. TAB eşlemesine dokunulmadı | HUD J gösteriyor |
| 8 | Bu akışta İngilizce metin vardı | Menü, inceleme, pause, sekmeler, açılır bildirimler Türkçe | Bkz. görseller |
| 9 | Maske anında duvara geçiyordu; şeritsiz E inceleme açmıyordu | Şerit 0,6 saniyede maskeye iner, ayrı `Yerine koy` ile maske 0,9 saniyede rafa gider. Şeritsiz E incelemeyi açar | Bkz. 07, 08, 09 |
| 10 | Yeni oyunda oyuncunun nereye gideceği yazmıyordu | Başlangıç görevi eklendi, inceleme onu kapatır | Bkz. 01 |
| 11 | Şerit ikonu bant rulosuydu; önizleme küçük ve koyuydu | Yeni beyaz bez ikonu, önizleme mesafesi 75 → 38 | Okunuyor, hâlâ gri kumaş |
| 12 | Kırılma `SetGlobalPitchModulation` ile bütün sesleri etkiliyordu | Kaldırıldı. Yalnız olaya ait düşük sesli 2D katman çalıyor ve bitince sönüyor | Oyun sesi durumu değişmiyor |

**Eylem kuralları.** Hareket sürerken E yok sayılır. Oyuncu uzaklaşabilir ve menü açabilir, hiçbir şey kilitlenmez. Kayıt hareketten önce alınır, bu yüzden yarım kalan görünüm yüklemede son duruma oturur. Aşama 3 kaydı `Yerine koy` ile devam eder.

**Karakterin eli.** Eldeki kapı ve düğme montajlarını masada denedim, kullanmadım. Bu yüzden animasyon eklenmedi. Şeridin inişi **geçici sunumdur**.

## A–H test tablosu

Girdi türleri: `Enjekte` = editörde `Input.+key`; `Mesaj` = Standalone penceresine Windows tuş mesajı. Masaüstü oturumu ön plan vermediği için fiziksel fare/klavye kullanılamadı.

| Test | Sonuç | Kanıt ve sınır |
|---|---|---|
| A. Baştan sona yürüyüş | **PARTIAL** | Işınlama, konsol veya doğrudan yükleme yok. Yürüyüşü betik yaptı: W enjekte, yön programla verildi. Takılma 0. Gerçek insan testi değil |
| B. Şerit önce, şeritsiz deneme, tekrar basma, iptal | **PASS** | Enjekte. Şerit bir kez tüketilir, görev ve günlük tek |
| C. Şerit kaydı, yeni oturum, menüden yükleme | **PASS** | Standalone, gerçek `Son kaydı yükle` düğmesi, Mesaj. Şerit envanterde, dünyada yok (10, 11) |
| D. İş bitince aynı yükleme, iki kez | **PASS** | Şerit 0, görevler tamam, günlük tek kayıt (13–17). Rafta maske ayrı oynanış görüntüsünde (09) |
| E. Menü sonrası hareket, bakış, kamera | **PARTIAL** | İnceleme ve menü sonrası hareket, FOV, mesafe döndü. Pause sonrası hareket Standalone'da döndü. Gerçek fareyle bakış ve duvar dibi elle denenmedi |
| F. Kırılma ayrı ve temiz | **PARTIAL** | Yeni oyunda yok, bir kez çalışıyor, dönüş ve yüklemede tekrar yok. Olay ortası kayıt yarım durum bırakmıyor: yüklenince olay başlamamış haliyle gelir. Ses dinlenmedi. Sonraki aşama hâlâ `ke * GR_DevArm` geliştirici girişi, oyuncu yolu yok |
| G. Standalone gerçek akış | **PARTIAL** | Yeni oyun, inceleme, okuma, menü, pause, yüklemeler ve yerine koyma geçti. Baştan sona tek oturumda yürüyüş Standalone'da yapılmadı |
| H. Derleme ve log | **PASS** | 124 Blueprint 0 hata. Son Standalone oturumlarında LogScript 0, Accessed None 0 |

Ek sonuçlar:

| Konu | Sonuç |
|---|---|
| Gamepad | **NOT_TESTED.** Bağlı cihaz yok, klavye sonucundan çıkarım yapılmadı |
| Gerçek fareyle döndürme | **NOT_TESTED.** `Rotate_IA` eylemi enjekte edildi ve maske iki eksende döndü. Anchor'a yazmaktan daha gerçek, ama fiziksel fare değil |
| Ses dinleme | **NOT_TESTED.** Ses cihazı açık çalıştırıldı, katmanın başlayıp bittiği ölçüldü, kulakla değerlendirilmedi |
| İç merdiven, zıplama, kapıyı E ile açma | **NOT_TESTED** bu turda. Rota dış basamağı ve eşikleri geçti |
| Promptu bilmeyen oyuncu | **NOT_TESTED.** Görev metni var, kimse denemedi |
| Video | **Yok.** Araç bulunmadı; adım görüntüleri, süre ve log verildi |
| Packaged build | **NOT_TESTED.** 13 GB boş alan yetersiz; kullanıcı dosyası silinmedi |

## Gerçek süre

Betikli tur: **3 dk 49 sn.** Bunun 74 saniyesi yürüyüş, kalanı inceleme ve ekran görüntüsü beklemesi. 8–12 dakika hedefine ulaşılmadı. Yapay bekleme veya mesafe eklenmedi. Gerçek süreyi yalnız insan oynanışı gösterir.

## Karakter ve kamera: önce–sonra

SF öncesi yedek (controller, kamera, HUD, harita, Config) geçici geri yüklendi, aynı rota koşuldu, sonra son yapı hash ile geri kondu (6/6 dosya).

| Ölçüm | SF öncesi | Son yapı |
|---|---|---|
| Yürüme / ivme / fren / sürtünme | 132 / 130 / 174 / 2,3 | Aynı |
| Yürüme rotası süresi | 10,8 sn | 10,8 sn |
| Koşu rotası süresi, en yüksek hız | 7,9 sn, 488 | 7,8 sn, 488 |
| Uzun rota süresi | 42,0 sn | 42,0 sn |
| FOV aralığı | 60–63,6 | Aynı |
| Kamera mesafesi ortanca (yürüme / koşu / uzun) | 163 / 166 / 180 | 164 / 165 / 180 |
| Kamera mesafesi en düşük (koşu) | 69 | 66 |

## Performans

Editör PIE, 1 oturum, aynı rota. Ön planda değilken editör 3 FPS'e kısıldığı için kısıtlama test süresince kapatıldı.

| Rota | Önce ortanca / p95 ms | Sonra ortanca / p95 ms |
|---|---|---|
| Yürüme | 31,9 / 44,3 | 32,8 / 41,7 |
| Koşu | 33,1 / 48,5 | 33,3 / 45,0 |
| Uzun rota | 36,8 / 44,0 | 36,6 / 43,4 |

- **0,01 saniyelik SF zamanlayıcısı:** 8 saniyelik beş aç/kapa çiftinde açıkken 32,1–33,6 ms, kapalıyken 32,5–33,9 ms. Ölçülebilir maliyet yok, değiştirilmedi.
- **Ray tracing uyarısı:** Değer yaklaşık 124 MiB, bütçe 400 MiB, uyarı eşiği %20. SF öncesinde de 123,9 MiB vardı. Sebep SF değil, uyarı gizlenmedi.
- **VRAM uyarısı:** 8 GB kartta iç mekânda 26–226 MB bütçe aşımı görülüyor. Önce–sonra karşılaştırılmadı, çözülmedi.

## Nwiro

- **Sürüm:** Nwiro Pro 1.1.14, proje eklentisi olarak yükleniyor.
- **Bağlantı:** Pro'da MCP sunucusu yok; `StartMCPServer` boş, `mcpRunning:false`. Integration Kit makinede bulunmadı. Aktif AI istemcisi yapılandırması bulunmadı.
- **Çalışan yol:** Editör içinden `UNwiroBridge::ExecuteTool`. 229 araç listelendi.
- **Geri alınabilir test:** Geçici widget kopyasında metin değiştirildi, okundu, eski haline alındı, doğrulandı, kopya kaydedilmedi.
- **Gerçek işlem:** SF ekranları ve HUD ağacı Nwiro ile okundu. Demo HUD gizleme ve 40'tan fazla Türkçe metin `set_widget_property` ile yapıldı.
- **Engel:** `create_widget_blueprint` editörü çökertti (`InitializeWidgetBlueprintRoot`, erişim hatası). Ücretli üretim kullanılmadı. Pro ve runner aynı anda yazmadı.

## Değişenler

Eklenen: `T_GR_BezSerit_Icon`; haritada `GR_BoundRag`.

Değişen proje assetleri: `BP_GR_MaskBench` (aşama 3, `GR_PlaceData`, `GR_StartTaskData`, `GR_InspectData`, `GR_RepairStale`, `GR_StartHint`, hareket adımları), `BP_GR_StripPickup` (kayıt, ikon), `BP_GR_FirstBreak` (ses katmanı, `GR_Audio`), `W_Sphirus_HUD` (görünürlük), `L_GR_SphirusHouse` (bitmiş maske rafa alındı, şerit maskeye bağlandı).

Değişen SF kopyaları: `SFSaveManager_AC`, `StoryFrameworkValues` (`SaveMethod`, sekmeler), `SFInventoryManager_AC`, `SFInteractionManager_AC`, `GeneralHud_W`, `GenericInventory_W` (boş envanter koruması), `Inspect_W`, `UnifiedMenuContainer_W`, `TaskManager_W`, `Inventory_W`, `Journal_W`, `Memoir_W`, `PopupMaster_W`, `PauseMenu_W`.

Geri alma: `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/` altında `sf52_m1113523`, `sf52_m2114221`, `sf52_m4121448`, `sf52_g1133538`, `sf52_g2133830`, `sf52_g3134353`, `sf52_k3121515`, `sf52_s2115437`, `sf52_u1115324`, `sf52_u2115945`, `sf52_u3120631`, `sf52_u4133529`, `sf52_u5134909`, `sf52_v1124650`, `sf52_v2124946`, `sf52_v3131616`, harita `sf52_map6`, `sf52_map8`. Editör kapalıyken geri yüklenir. Kullanıcı kaydı silinmedi: test kayıtları `Saved/Codex/SF52_20261105/save_aside/` ve `slots/` içinde.

## Geçici görseller ve animasyonlar

- Maske bağlama: el teması yok, bez şerit inişi ve kayma hareketi.
- Bağlı şerit: kırışık `SM_Rag_01`, gerçek bir bağ gibi sarılı değil.
- Şerit mesh'i ve önizlemesi: gri kumaş; görevdeki "şerit" sözüne tam uymuyor.
- Sesler: SF örnekleri (`PaperSound_Cue`, `ObjectMove_Cue`, `LightAmbient_Cue`).
- İkon: elle çizilmiş geçici beyaz siluet.

## Gerçek kusurlar

- Başlangıç görevi ile asıl görev, görev listesinde iki kayıt olarak görünür. Bilinçli, ama oyuncuya fazla gelebilir.
- Editörden Standalone yüklemesi 40–65 saniye sürüyor ve ilk kareler donuyor. Packaged süre bilinmiyor.
- İpuçları aktif eşlemeden üretilmiyor: SF `InputKey_W` sabit tuş adı kullanıyor. Şu an eşlemeyle uyumlu, tuş değişirse elle güncellenmeli.
- `I` hızlı envantere eşli, ama önceki testte görünür ekran açmadı. HUD `G` gösteriyor.
- `ActorReference` inceleme yolu bu görevde kullanılmıyor. Işık kanalı düzeltmesi o yolu kapsamaz.
- Tüm SF çevrilmedi: yalnız bu akışın ekranları.
- İç mekânda VRAM bütçe aşımı uyarısı duruyor.

## Kanıt

`evidence/` içinde 19 görüntü. 02, 03, 07, 08 ve 18 son küçük düzeltmelerden önceki Standalone oturumundan; C ve D görüntülerinin geri kalanı son yapıdan.
