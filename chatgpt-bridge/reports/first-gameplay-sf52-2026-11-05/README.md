# İlk oynanabilir akış — Story Framework 5.2

Tarih: 5 Kasım 2026 · Durum: **Oynanabilir prototip.** Final görsel kalite değil.

## Nasıl oynanır

1. `sphirus.uproject` dosyasını aç. Harita: `/Game/GraceRanger/Maps/L_GR_SphirusHouse`. Play'e bas.
2. Oyuncu evin arka kapısının önünde başlar (832, -220). Kapı açıktır.
3. Atölyedeki masaya git, maskeye bak, **E** ile incele. Fare döndürür, **Q** okur, **F** çıkar. Görev başlar.
4. Veranda masasındaki bez şeridi **E** ile al.
5. Masaya dön, maskeye bak, **E** ile bağla. Maske duvara geçer, görev biter, günlük eklenir, oyun kaydedilir.
6. İsteğe bağlı: patikadan göl kıyısına in, teknenin yanında **E** ile manzaraya bak. Bu da kayıt alır.

Tuşlar: E/Gamepad Sağ etkileşim, F ikincil/geri, J menü (F ile kapanır, A/D sekme değiştirir), G hızlı envanter, T görev, P/Esc duraklat. `I` testte görünür bir ekran açmadı.
Yükleme: P → **Load Last Save**.

### Kırılma testi (normal oyunda çalışmaz)

Play sonrası konsolda `ke * GR_DevArm` yaz, verandaya yaklaş. Masadaki `GR_BreakCup` 8 saniye başka yerde görünür ve çevre sesi hafifçe kayar. Sonra fincan biraz farklı durur, tek cümlelik günlük eklenir. Bir kez çalışır.

## Kabul tablosu

Test yöntemi: PIE, `Input.+key` ile gerçek tuş girdisi. Oyuncu adımlar arasında **test için ışınlandı**; yürüyerek baştan sona geçilmedi.

| # | Kontrol | Sonuç |
|---|---|---|
| 1 | İncele → al → kullan → gör → kaydet | PASS |
| 2 | Görevden önce şerit, şeritsiz deneme, tekrar basma | PASS (oyun içinde çift ilerleme yok). Kayıtta şerit hatası için bkz. #4 |
| 3 | İnceleme aç/kapa: kamera, IMC, FOV | PASS (klavye). Gamepad NOT_TESTED |
| 4 | Yeni PIE oturumunda Load: şerit sonrası ve iş bitince | PARTIAL: aşama, görev, günlük ve duvardaki maske doğru döndü. **Harcanan şerit iş bitince alınan kayıttan envantere geri dönüyor.** `LoadGame` doğrudan çağrıldı; menüdeki düğmeye basılmadı |
| 5 | Yeni oyunda doğaüstü olay yok | PASS |
| 6 | Kırılma bir kez; geri dönüş ve yüklemede tekrar yok | PASS |
| 7 | Derleme, Accessed None, log spam | PASS son akışta LogScript 0 (SF 122 BP 0 hata; son yamalardan sonra toplu derleme tekrarlanmadı) |
| 8 | Yürüme, koşu, kapı | PASS: yürüme 132, koşu hedefi 490, kapı E ile aç/kapa. Zıplama sonucu belirsiz, kamera collision NOT_TESTED |
| 9 | Standalone | PARTIAL: `-game` harita açıldı, LogScript 0. Oynanmadı. Packaged build NOT_TESTED |
| 10 | Önce/sonra performans | NOT_TESTED. Yeni Tick yok, ama SF her 0,01 sn iz atıyor |

| 11 | İncelemede maske parlaklığı | PASS (teknik): 5 açıda kırpılma %0, önce %94,2. Görsel kabul kullanıcıda |
| 12 | J menüsü: Tasks ve Inventory sekmesi, F ile kapanış, sonrasında etkileşim | PASS (klavye) |

Ek NOT_TESTED: yürüyerek ev→veranda→göl rotası, gerçek süre, gamepad, günlük sekmesi, hızlı envanter, olay ortasında kayıt, yeni dosyayla menüden yükleme, Standalone'da inceleme. Döndürme fareyle değil, `Anchor` döndürülerek ölçüldü.
**8–12 dakika hedefi doğrulanmadı.** Mesafeler kısa, doğal oynanış büyük olasılıkla bunun altında kalır.

## Bilinen kusurlar

- **Şerit yüklemede geri dönüyor.** SF önce `InteractWith` çağırıyor, şeridi sonra siliyor (`HasItemInteraction`). Masanın kaydı bu çağrının içinde çalıştığı için dosyaya şerit de yazılıyor. Ölçüm: iş bitince 0 eşya, yüklenince 1. Masa şeridi tekrar kabul etmiyor, ilerleme bozulmuyor, ama envanterde boşta bir `Bez Şerit` kalıyor.
- `InspectActor_BP` düzeltmesi yalnız `RootStM` ve `RootSkM` yolunu kapsıyor. `ActorReference` yolunu (child actor) kullanan bir nesne eklenirse güneşten ayrılmaz, yine beyaz çıkabilir. Bu akışta öyle bir nesne yok.
- Envanter önizlemesinde bez şerit koyu görünüyor; okunuyor, ama aydınlık değil.
- **AAMS demo HUD duruyor** (`Controls`, `Retarget Example Motion Matching`, `v2.0.16`). Listesi yanlış tuşlar içeriyor. Önceden vardı, dokunulmadı.
- Sol altta SF ipucu `TAB` gösteriyor, menü J ile açılır. Tab AAMS `IA_Aiming` olduğu için değiştirilmedi.
- İnceleme ipuçları ve pause menüsü İngilizce (SF metinleri).
- Maske bağlama için animasyon yok; anında olur. Oyuncu el teması prototip dışı.
- Kırılmada ses `SetGlobalPitchModulation` ile kayıyor; duyularak değerlendirilmedi. Editör testleri `-nosound` değildi ama dinlenmedi.
- Şerit ikonu geçici: SF `DuctTapeIcon_T`. Şerit mesh'i: `SM_Rag_01`.
- Şerit dışında mevcut mesh kullanıldı; yeni ücretli asset yok.
- Oyuncunun görevi hatırlaması için ek rehber yok; görev satırı ve T var.

## Mimari

| Sahip | Karar |
|---|---|
| Hareket | AAMS/Core Motion. SF `GenericMovement` ve `CameraInputs` projedeki kopyadan silindi (ham LeftShift `SetMaxWalkSpeed` çağırıyordu) |
| Kamera | Tek kamera `RangerGameplayCamera`. `BP_PCM_GR_Camera` artık `SFPlayerCamera_PCM` altında, `BlueprintUpdateCamera` korunuyor. `SFDefaultCamera_CC` eklenmedi çünkü spring arm ve FOV'u kendi yönetiyor |
| Controller | PlayerController → SFDemoPlayerController_BP → BP_GR_InputBase → BP_PC_GR_GraceRanger. 5 SF component kalıtımla geliyor |
| Input | SF her geçişte `ClearAllMappings` yaptığı için tek IMC: `IMC_GR_SFGameplay` (AAMS + SF, 50 eşleme). Hareket kilidi inceleme IMC'siyle kendiliğinden gelir |
| Save | Tek sahip `SFSaveManager_AC`. Durum `AddInteractActors(Actor, DataString)` ile yazılır, `LoadFromDataString` ile kurulur |
| Doğruluk kaynağı | `BP_GR_MaskBench.GR_Stage` (0/1/2), `BP_GR_FirstBreak` DataString (Armed/Done). Görünüş `GR_ApplyStage`/`GR_Apply` ile üretilir |
| Hikâye aşaması | "Sonraki aşama" = `BP_GR_FirstBreak` armed durumu. Oyun içinde bunu açan olay yok, kasıtlı |
| Nwiro | Kullanılmadı. Pro 1.1.14 kurulu, Integration Kit bağlantısı NOT_TESTED. Motor MCP'si 8000'de açıldı, kullanılmadı. Tüm işler kapılı Python runner ile yapıldı |

Kanon: promptun 2. bölümü esas alındı. `oyun_ilk_bolum_asset_ve_teknik_plan(1).md` makinede bulunamadı.

## Değişen ve eklenen

Eklenen: `Content/StoryFramework/` (849 dosya), `/Game/GraceRanger/SF/MaskJob/{BP_GR_MaskBench,BP_GR_StripPickup,BP_GR_LakeRest}`, `/Game/GraceRanger/SF/Break/BP_GR_FirstBreak`, `/Game/GraceRanger/Input/IMC_GR_SFGameplay`, `Config/DefaultGameplayTags.ini`.

Değişen proje assetleri: `BP_GR_InputBase` (üst sınıf + BeginPlay'de `UpdateInputMappingContext`), `BP_PC_GR_GraceRanger` (derleme), `BP_PCM_GR_Camera` (üst sınıf), `L_GR_SphirusHouse` (yeni aktörler), `L_GR_CurrentHouseContent` (`Furniture_CR_MaskWorkInProgress` oyunda gizli), `Config/DefaultEngine.ini` (GameInstance, kanal 4, redirect).

Değişen SF kopyaları: `InspectActor_BP` (bkz. aşağıdaki parlaklık düzeltmesi), `SFDemoPlayerController_BP`, `SFInteractionManager_AC` (trace kanalı, `SetCameraVariables`), `GeneralHud_W`, `SFCameraGeneralFunctions_BFL`, `SFGameplayFunctions_BFL`, `SFSaveManager_AC`, `StoryFrameworkValues`, üç font (Roboto; ğ/ı/ş eksikti). SF demo haritası bu projede artık yürümez. Kaynak proje `StoryFramework52Interac` değişmedi.

## İnceleme parlaklığı düzeltmesi

Neden: SF capture'ı (`SCS_SceneColorHDR`) ton eşlemesiz ham ışık değerini 8 bit hedefe yazıyor. SF'nin kendi demo sahnesi için kurulu bu yapıda haritanın 1500 lux güneşi maskeye ulaşınca değer 1'i aşıyor ve maske beyaza doyuyordu. Bu yüzden önceki pozlama denemeleri işe yaramamıştı.

Çözüm, `InspectActor_BP` şablonunda: `RootStM`, `RootSkM` ve `RectLight` ışık kanalı 1'e alındı; güneş kanal 0'da kaldığı için incelenen nesneye ulaşmıyor. `RectLight` 0,2 → 0,7 cd. Capture ayarlarına dokunulmadı. Işık artık dünyadaki nesneleri de etkilemiyor.

| Durum | Ortalama (0–255) | Kırpılan piksel |
|---|---|---|
| Önce | 246 | %94,2 |
| Sonra, ilk açı | 132 | %0 |
| Sonra, 4 döndürülmüş açı | 80–98 | %0 |

Ölçüm ekranın maske bölgesinden alındı; değerler arka plan ve maske kenarını da içerebilir. Görseller: `evidence/06` (önce), `07` ve `08` (sonra), `09` (envanter).
Temiz açılışta diskten doğrulandı: tam iş zinciri, 2. aşamadan yükleme, oturum boyunca LogScript 0.

## Geri alma

Her yazma işinin doğrulanmış yedeği: `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/sf52_*`.
Harita: `sf52_map1` SF öncesi hal. Alt seviye: `sf52_sub1`. Config: `Saved/Codex/SF52_20261105/checkpoint/`.
Parlaklık düzeltmesinin yedeği: `sf52_light103447`. Editör kapalıyken geri yükle. Test kayıtları: `Saved/Codex/SF52_20261105/save_aside/` (silinmedi; oyun temiz başlar).

## Kanıt

`evidence/` klasöründe ekran görüntüleri. `03` eski fontla çekildi, sahneyi göstermek için duruyor. Video kaydı yok.

## Disk

15 GB boş (931 GB). Ölçülenler: OneDrive 256 GB (`Saved/Codex` 99, `Content` 97, `SourceAssets` 16), AppData\Local 163 GB (Temp 60, NVIDIA 42, UnrealEngine 41), Steam 140 GB, `SphirusCheckpoints` 35 GB, Downloads 12 GB. Dosya silinmedi; `SphirusCheckpoints` sıkıştırıldı.
