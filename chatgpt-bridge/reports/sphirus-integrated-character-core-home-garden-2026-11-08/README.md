# Sphirus: yeni baş, AAMS'ten bağımsız Core Motion oyuncusu, adaptif yakın kamera

## Güncelleme 4 (2026-11-08 akşam, kullanıcı geri bildirimi)

| İstek | Yapılan | Durum |
|---|---|---|
| Baş ile gövde arasında renk farkı | Kıyafete göre takılan gövde malzemelerinde baştan farklı bir ana cilt malzemesi ve (0,78; 0,67; 0,57) kahverengi çarpan vardı. Çarpan, dikişin iki yanında ölçülerek (1,30; 1,50; 1,58) yapıldı. Gövde dokusunda omuz yanığı ve çil yumuşatıldı. | PASS (görüntü: `skin_seam_before.jpg` → `skin_seam_after.jpg`) |
| Giysi altında siyah boşluklar | Ten gizleme maskeleri eski giysilere göre çizilmişti. Kapalı delikler dolduruldu, kenarlar 16 texel geri çekildi. Göğüsten ten taşması da giderildi. | PASS (yakın çekim) |
| Kukla gibi seken, hızlandırılmış yürüyüş | Klipler 197 cm/s hızında, karakter 150–165 cm/s; Motion Matching oynatma hızı 1,0'a kilitliydi. Oynatma hızı aralığı 0,75–1,2 yapıldı. Karışım 0,45'ten 0,25 sn'ye indi, aynı klipte atlama eşiği 0,25 sn, arama aralığı 0,05 sn. Dönüş hızı 300°/s, ivme 700. | PARTIAL: kayıtta ayak yerdeyken ~1 cm sabit kalıyor. Görsel his kullanıcı tarafından denenmeli. Inertialization düğümü bu editörün paletinden eklenemedi. |
| Bekleme hareketleri çok sık | Boşta döngüsü 6 sn'lik ağırlık aktarma klibinden sakin `af_Stand_Idle_01`'e alındı. | PARTIAL (görsel kontrol yok) |
| Zıpladıktan sonra yerde kayma | Hareket halinde inişte tam gövde iniş klibi artık oynamıyor; yalnızca 60 cm/s altında. | NOT_TESTED |
| Karakter kadrajda fazla solda | Omuz ofseti 45–62'den 30–44 cm'ye indi. | PASS (görüntü) |
| Eylemde çapraz üst uzak kamera | Kesme ve şömine istasyonlarında hâlâ sabit kameraya geçiş vardı, kaldırıldı. Eylem sırasında kol 90 cm, omuz 38 cm, bakış −22°, karakterin yönüne yumuşak dönüş. | PASS (`action_camera_chop_fire.jpg`) |
| Alan derinliği, lens hissi | Oyuncu kamerasında f/5,6, odak 125 cm, hafif vinyet, renk sapması, film greni. Lens bükülmesi eklenmedi. | PARTIAL |
| Balta beklerken donma | Duraklatılan her montajda boşta klibinden türetilen nefes ve salınım katmanı devreye giriyor (baş saniyede 3–6 cm hareket ediyor). | PASS (ölçüm) |
| Odun şömineye konmuyor | Akış çalışıyor: iki parça toplanınca şömine önce odunla dolduruluyor, sonra yanıyor. Parçalar E ile tek tek toplanmazsa yığın 0 kalıyordu. Parçalar artık 80 cm yakına gelince kendiliğinden de toplanıyor. | PASS (otomatik rota: Fire 2) |
| Hafif yaşlanma | MetaHuman yüz ayrıntı ayarı (`HighFrequencyDelta` = 0) bu motor sürümünde betikten salt okunur. | FAIL (yapılamadı) |

## Güncelleme 3 (2026-11-08 öğleden sonra)

Bu turda gece kalan işler ile kullanıcının uyanınca bildirdiği titreme, ayak ve atlet sorunları ele alındı.

### Karakter gövdesi: atlet, ayaklar, titreme

| Sorun | Neden | Düzeltme | Durum |
|---|---|---|---|
| Atlet dize kadar uzuyor, şort taşıyor | Retarget'taki Root Motion işleminde `TargetRoot = pelvis` ayarlıydı. Kaynağın kök kemiği (0,0,0) her karede MetaHuman leğenine yazılıyor, leğen yere iniyordu. Leğene bağlı giysi kenarları aşağı çekiliyordu. | `TargetRoot = root`. Leğen 0'dan 94 cm'ye çıktı (sürücü 95). | PASS (ölçüm ve görüntü) |
| Ayak parmak ucunda, parmak zeminin içinde | Kaynak rig'de bacak uyluk→bilek ve ayrı parmak zinciri, hedefte uyluk→parmak. IK hedefleri de farklı kemiklerdeydi. | Kaynak rig'in proje kopyası `IK_Sph_CoreSrc`: bacak uyluk→parmak, IK hedefi parmakta. Hedef poz yeniden hizalandı. Parmak artık bileğin 10 cm önünde. | PASS (ölçüm ve görüntü) |
| Dururken yerinde yürüme ve titreme | Dönerek yürüyüp durunca Motion Matching adım döngüsünde kalıyordu: hız 0, ayaklar ±50 cm. | Sürücü animasyonuna boşta kapısı: 0,35 sn hareketsiz kalınca 0,3 sn'de Core boşta döngüsüne geçiyor. | PASS (kayıt: ayaklar 0,6 sn'de sabitleniyor) |
| Mesaj günlüğünde binlerce hata | `BP_GR_AtticContext` eski AAMS merdivenine bağlıydı, bağ kopunca her karede hata yazıyordu (oturum başına ~6.500). | Yeni `SPH_AtticLadder`'a dünya konumu korunarak bağlandı. | PASS (sonraki oturumda 0 hata) |
| Kamera konumunda küçük sarsıntı | Yay kolunun sondası çalılara değince kol boyu anında kısalıyor. Editördeki kare süreleri 11–125 ms arasında dalgalanıyor. | Düzeltilmedi. Bitkilerin kamera kanalı tüm ormanı etkilediği için ayrı karar gerekiyor. | PARTIAL |

Atlet ayrıca Sph8 gövdesiyle MetaHuman gardırobundan yeniden derlendi (`Out_S8Tank`). Asıl uzama nedeni leğen hatasıydı.

Kanıt: `evidence/body_before_retarget_fix.jpg`, `evidence/body_after_retarget_fix.jpg`.

### Kamera ışınları hiç çalışmıyordu

UE 5.8'de `Multiply_VectorFloat` düğümü "vector*vector" olarak oluşuyor ve sayı değeri kayboluyor (B = 0). Kameranın beş açıklık ışını bu yüzden sıfır uzunluktaydı: açıklık ve duvar mesafesi hep "açık alan" çıkıyordu. 48 düğüm `MakeVector(k,k,k)` ile düzeltildi. Kesme istasyonu ve maske tezgâhında kalan altı görüş hedefi değişimi (`CameraActor` (0,0,3000)) kaldırıldı. Kamera artık iş sırasında da oyuncuda kalıyor.

### Yatak ve uyanış

- Uzanma ve kalkma: karakter yatağın doğu yarısında boylu boyunca, başı yastıkta yatıyor. Tıklayınca kalkıp yatağın yanında ayağa kalkıyor. PASS. `evidence/bed_lie_rise.jpg`
- Yeni oyun uyanışı artık aynı yatak montajının uyku ve kalkış kısmını kullanıyor: yatakta yatarak başlıyor, root motion ile dışarı çıkıyor. PASS. `evidence/new_game_wake.jpg`
- Yorgan yok. Karakter yorganın üstünde uzanıyor.

### Odun kesme

- Tıklayınca vuruşta kütükten iki yarık parça fizikle iki yana düşüyor: biri ileri, biri oyuncuya doğru. Parçalar oyuncu kapsülünü yok sayıyor ve CCD açık.
- Her parça E ile toplanıyor: oyuncu eğiliyor, parça yığına ekleniyor, kucağa dokulu bir odun demeti geliyor.
- Yerde duran parçalar kayıtta yığına sayılıyor, yükleyince kaybolmuyor.
- Kesim sesi projede yoktu. Sentezlenmiş bir balta vuruşu (`SW_Sph_ChopHit`) bağlandı. Ses kulakla dinlenmedi.
- Test: odun al, kes, iki parçayı topla, yığın 2. PASS. `evidence/chop_pieces_carry.jpg`
- Bir denemede geriye savrulan parça zeminin altına düştü. Düzeltmeden sonraki denemede iki parça da zeminde kaldı. Tek deneme, tekrar sayısı az.

### Bilinen eksikler (bu tur)

- Çay alt adımları (kapak, ot, su), EnviroSense, vault/mantle, ayak IK (eğimli zemin), yorgan, ev ve bahçe yerleşimi yapılmadı.
- Paketleme, performans ve kaydet/yükle testi yapılmadı.
- Editör her derleme veya harita işinden sonra yeniden başlatılmazsa çöküyor. Bu yüzden tüm testler taze editörde koşuldu.

## Güncelleme 2 (2026-11-08 sabahı, kullanıcının elle testinden sonra)

Kullanıcı şunları bildirdi: hareket edince karakter kameradan fırlıyor ve köşede koşu animasyonunda takılıyor, fare ile karakter ekranda kayıyor, eller arkada, baş–gövde renk geçişi var. Ayrıca iki set referans kare gönderdi (Plague Tale ve Alone in the Dark tarzı yakın omuz kamerası). Bu turda yapılanlar:

| Konu | Sonuç | Kanıt |
|---|---|---|
| Gövde kapsülden kopuyordu (Motion Matching kliplerinin kök hareketi) | PASS: sürücü animasyonunda kök hareketi yok sayılıyor, kemik kilitli. Fareyle dönerken yürüme, koşu ve geri gitmede 513 karede gövde–kapsül sapması 0 cm | `evidence/walk_turn_camera_body_attached.jpg` |
| Eller arkada | PASS (görsel): Core Motion IK rig'inden MetaHuman eklentisinin kendi `IK_MH_IKRig`'ine sıfırdan retargeter (`RTG_Sph_Core_to_MH2`), varsayılan işlemler, otomatik zincir eşleme, otomatik hizalanmış hedef poz. Eller iki yanda | `evidence/arms_natural_retarget.jpg` |
| Kamera | PARTIAL: referanslara göre baş hizasında, karakter sol üçte birde. Ev içinde 0,85–1,25 m, dışarıda 1,20–1,65 m. Omuz ofseti 45–62 cm, FOV 62/66. Sağ duvar yakınsa omuz, arka duvar yakınsa mesafe kısalıyor, kamera yükseliyor. Dar koridorda hâlâ kesin doğrulanmadı | `evidence/camera_alone_style_views.jpg` |
| Baş–gövde renk geçişi | PASS (görsel): gövdedeki iri çiller inceltildi, boyunda 24 cm'lik ton geçişi. Gövde malzemesindeki fazladan mikro normal, roughness ve specular ayarları kaldırıldı, başla aynı | `evidence/neck_seam_before.jpg`, `evidence/neck_seam_after.jpg` |
| AAMS bağımlılığı | PASS: harita + oyuncu + oyun modu kapanışında 0 AAMS paketi (önce 2.366) | aşağıda |
| Paketleme kuralları | `MapsToCook` = `L_GR_SphirusHouse`; `DirectoriesToNeverCook` = `/Game/AAMS`, `/Game/CoreMotion_Retargeted` | `Config/DefaultGame.ini` |
| Kapılar | PASS (otomasyon): AAMS etkileşim tabanından türeyen 6 kapı (balkon, mutfak arka, veranda, üst banyo, alt WC, kiler) Story Framework `GenericDoor_BP`'ye çevrildi; E ile açılıyor. Sandık kapağı, çatı penceresi ve çekme kolu artık statik | `evidence/door_sf_open.jpg` |
| Tavan arası merdiveni | AAMS'e bağlı Blueprint kaldırıldı, yerinde projenin kendi merdiven mesh'i (statik). Tırmanma yok | — |
| Maske işi klipleri | 6 klip (Carry, Hang, Inspect, Put, Take, Tie) Core Motion iskeletine taşındı, tezgâh yeni klipleri kullanıyor | — |
| Maske ipucu katmanı | AAMS HUD kopyası olduğu için tezgâhın açtığı sağ üst ipucu kaldırıldı; görev metni Story Framework görev listesinde (T) | — |
| Dolap kapağı klibi | AAMS kapı klibi yerine Core Motion iskeletindeki `AM_GR_Day_Reach` | — |
| İstasyon sesleri | AAMS sesleri yerine proje foley'i ve Story Framework kapı sesi. Odun vuruşu için uygun ses yok, geçici olarak `foley_punch_02` | — |
| Çay | PASS (otomasyon + görsel): çay istasyonu, çaydanlık, buhar ve fincan mutfaktaki dökme demir ocağa taşındı; evdeki eski çaydanlık kaldırıldı | `evidence/chore_route_tea_kitchen.jpg` |
| Ev işi rotası (yeni oyun) | PASS (otomasyon): uyanma, giyinme, odun, kesme (2 parça), şömine (2), çay (2) | aynı |
| Mouse ile odun kesme | PASS (otomasyon): E ile kütüğe gelinir, kesme klibi hazır duruşta (3,05 sn) durur ve bekler. Sol tık (`IA_Sph_Use`) tek vuruşu sürdürür, gerçek vuruş anında parçalanma olur. Bekleme yokken tık hiçbir şey yapmaz; basılı tutma ve hızlı tık kuyruk biriktirmez, ikinci tık çoğaltmaz. Bekleme süresi istasyon başına ayarlı (`GR_AwaitAt`). Kusurlar: taşınan odun demeti kesme sırasında kollarda görünmeye devam ediyor; parçalar fizikle düşmüyor, eski betikli yarılma görseli kullanılıyor; parçalar tek tek toplanamıyor | `evidence/chop_click_ready_swing.jpg` |
| Zıplama, düşme, iniş | PASS (otomasyon): zıplamada Core Motion kalkış montajı, havada düşme döngüsü (Motion Matching'den 0,2 sn geçiş), yere değince toparlanma montajı. Yürürken ve dururken denendi. Not: Core Motion zıplama klipleri erkek seti | `evidence/jump_fall_land.jpg` |
| Çömelme | PASS (otomasyon + görsel): C ile çömelme. 18 Core Motion çömelme klibiyle ikinci veritabanı (`PSD_Sph_Crouch`); sürücü her karede çömelme durumuna göre veritabanını seçiyor. Çömelik yürüme 110 cm/s, C ile kalkış. Klipler erkek setinden, poz derin. Alçak tavan altında kalkışın engellenmesi motorun varsayılanı, ayrıca test edilmedi | `evidence/crouch_idle_walk_stand.jpg` |
| Yatak ve battaniye | NOT_DONE: Village Life yatağa girme/kalkma klipleri kök hareketiyle yatağa giriyor. Kök hareketi gövdenin kopmaması için kapalı; yatakta güvenle açmak ve kapsül–yatak çarpışmasını çözmek bu turda yapılmadı. Battaniye için bez simülasyonu veya rig yok | — |


Hâlâ yapılmayanlar: fizikle düşen ve toplanan odun parçaları, çayın kapak, bitki ve su adımları, yatak ve battaniye, vault/mantle, EnviroSense, zıplama/engel aşma/merdiven tırmanma, ayak IK'sı, ev ve bahçe yerleşimi, kıyafet düzeltmesi, cook denemesi, performans, kayıt/yükleme testi.

---


Tarih: 2026-11-08 (görev 7 Kasım akşamı başladı). Proje: UE 5.8.4, harita `/Game/GraceRanger/Maps/L_GR_SphirusHouse`.
Bu rapor genişletilmiş görev promptunun yapılan kısmını ve yapılmayan kısmını ayrı yazar. Teslim **kısmidir**.

## Durum özeti

| Alan | Sonuç | Kanıt |
|---|---|---|
| `MHC_HazelM` başı oyunda | PASS (teknik + görsel) | `evidence/face_skin_hair.jpg` |
| Ten: gövde başa eşlendi, çil, hafif yaş izi | PASS (portrede görüldü), hareket/LOD içinde NOT_TESTED | aynı |
| Saç rengi doğal bakıra | PARTIAL (önceki saç referansına göre ayarlandı, kullanıcı onayı yok) | aynı |
| Saç simülasyonu | Kapatıldı (açıkken tutamlarda iz ve titreme vardı) | `evidence/hair_sim_on_off.jpg` |
| Oyuncu ve oyun modu zincirinde AAMS | PASS: bağımlılık kapanışında 0 AAMS paketi | aşağıda |
| Haritanın geri kalanında AAMS | FAIL: tavan arası merdiveni, kollu kapılar, maske ipucu widget'ı | aşağıda |
| Core Motion Motion Matching hareketi | PASS (teknik): yürüme 165, jog 330, koşu 466–478 cm/s, dönüşler | kayıtlar `rec/cm3`, `cm4`, `cm8` |
| Ev içinde jog/koşu kapalı | PASS (teknik): ev içinde Shift ile en fazla 150 cm/s | `rec/cm8b` |
| İstasyon kamera devirleri kaldırıldı | PASS | `evidence/chore_route_new_player.jpg` |
| Yeni oyun ev işi rotası yeni oyuncuyla | PASS (otomasyon): giyinme, odun, kesme 2 parça, şömine 2, çay 2 | aynı |
| Adaptif yakın omuz kamerası | PARTIAL: oda, yatak odası, bahçe referansa yakın; dar koridorda kamera başa giriyor | `evidence/adaptive_camera_views*.jpg`, `evidence/camera_yard_close.jpg` |
| El ve kol pozu (retarget) | FAIL: idle ve yürüyüşte eller gövdenin arkasında görünüyor | aynı kareler |
| Mutfakta ocakta çay, mouse ile odun kesme, düşen parçalar, yatak ve battaniye, EnviroSense, zıplama/engel aşma/merdiven, ev ve bahçe yerleşimi, kıyafet düzeltmesi, cook, performans, save/load | NOT_DONE | — |

## 1. Baş, ten ve saç

- Kaynak: `/Game/EditableCharacters/HazelM/MHC_HazelM` (kullanıcı 7 Kasım 22:26'da yüz için otomatik rig istedi ve kaydetti). Kaynağa dokunulmadı; kopyası `/Game/Sphirus/CharacterLab/Sph_20261108/MHC/MHC_Sph8` derlendi (Optimized, High) ve çıktısı `.../Sph_20261108/Built/MHC_Sph8` (48 paket). Kıyafet seçilmeden derlendi, gövde yüzeyi kapalı.
- Oyuncu: yüz `SKM_MHC_Sph8_FaceMesh`, gövde `SKM_MHC_Sph8_BodyMesh`. Saç Messy Bob, kaş ve kirpikler yeni yüze yeniden bağlandı (`GB_Sph_Hair_81`, `GB_Sph_Brow_81`, `GB_Sph_Lash_81`).
- Ten: baş ve gövde renk dokuları MetaHuman çıktısından türetildi; çil, güneş izi ve göz altında hafif yaş tonu eklendi. Gövde, boyun dikişinde başa eşlendi (oran medyanı 0,985). LOD3 ve sonrası baş dokusu çilsiz kaldı.
- Saç: `hairMelanin` 0,74 → 0,60, `hairRedness` 0,60 → 0,47, `HairRoughness` 0,40. Önceki saç referansı (Ekim, kızıl kahve) esas alındı. Saç simülasyonu bileşen üzerinde kapatıldı.

## 2. AAMS'ten kopuş

- `BP_HybridA_Player` artık doğrudan `Character` sınıfından türüyor (eskiden `BP_PBI_Player > BP_GR_Player > BP_Player_MM > BP_ExampleCharacter_MotionMatching`). Bileşenler yeniden kuruldu: gizli sürücü mesh `SKM_MCPaul` (Core Motion iskeleti), görünen gövde, yüz, saç, kaş, kirpik, kıyafetler, yay kolu ve kamera.
- `BP_GM_GR_GraceRanger` → `GameModeBase`. `BP_PC_GR_GraceRanger` → Story Framework'ün `SFDemoPlayerController_BP` sınıfı (Story Framework yöneticileri ve arayüzü oradan geliyor). Kamera yöneticisi `/Game/Sphirus/Player/BP_Sph_CameraManager` (bakış açısı sınırları −62/+42).
- Girdi: AAMS giriş eylemleri `IMC_GR_SFGameplay` içinden çıkarıldı (23 eşleme). Projeye ait `/Game/Sphirus/Player/Input/IA_Sph_*` eklendi: Move, Look, Gait (Shift), Jump, Crouch, Use (sol tık, henüz bir işe bağlı değil).
- Eski oyuncuya yapılan cast'ler (`DayHub`, `DayStation`, `MaskBench`, `HomeContext`, `AtticContext`) yeni oyuncuya bağlandı.
- Ölçüm (asset registry bağımlılık kapanışı): oyuncu ve oyun modu → **0 AAMS paketi**. Harita → hâlâ 2.366 AAMS paketi, şu yollardan:
  - `L_GR_CurrentHouseContent > BP_GR_AtticLadder > ABP_GR_MotionMatchingBase > ...` (eski tavan arası merdiveni, ayrıca her karede çalışma zamanı hatası üretiyor)
  - `L_GR_CurrentHouseContent > BP_BaseInteractable` (`BP_GR_LeverDoor`, `BP_SphirusLeverDoor`)
  - `L_GR_SphirusHouse > BP_GR_MaskBench > W_GR_MaskHint > AC_State_AAMS`
  - Bu üç yol kapanmadan paketlenen oyun AAMS içeriğini cook'a taşır. Cook denenmedi.

## 3. Core Motion hareketi

- Motion Matching: `/Game/Sphirus/Player/Anim/ABP_Sph_Driver` (MCPaul iskeleti), sırasıyla poz geçmişi + Motion Matching, `DefaultSlot`, `UpperBody` slotu (spine_01 üstü). Yörünge `PoseSearchGenerateTrajectory (for Character)` ile üretiliyor.
- Veritabanı `/Game/Sphirus/Player/MM/PSD_Sph_Loco2`, 44 klip: kadın idle (02), 8 yerinde dönüş, yürüme ve jog için ileri, başlama, durma, pivot, ileri-sol/sağ ve 8 dönerek başlama; koşu için ileri, başlama, durma ve 4 dönerek başlama. Klipler Core Motion'dan `/Game/Sphirus/Player/Anim/Core` altına kopyalandı; satıcı dosyaları değişmedi.
- Şema: Epic GameAnimationSample `PSS_Default` (AAMS kopyası değil), iskeleti MCPaul olarak değiştirildi: `/Game/Sphirus/Player/MM/PSS_Sph_Loco`.
- Gövde: `ABP_Sph_Body` → `RTG_Sph_Core_to_MH` ile sürücüden pozu alıyor. Eski kurulumdan kalan el ve bacak temas işlemleri ile "Run IK Rig" kapalı (eller ve gövde bozuluyordu). Ayak IK şu an yok.
- Kök kemik ofseti kaldırıldı: ışınlanma ve kayıt yüklemesinden sonra gövde kapsülün gerisinde ve ters yönde kalıyordu. Kapsül hareketin tek sahibi.
- Hız ve tempo, oyuncunun tick'inde tek yerden belirleniyor: dışarıda yürüme 165, Shift ile jog 330, Shift 1,2 sn basılı ve hızlıyken koşu 480; ev içinde (`GR_HomeContext`) her durumda 150.
- Ev işi klipleri (Uyanma, Kesme, Toplama, Diz çökme, Taşıma, Dökme, İçme, Giyinme, Uzanma) Village Life ve Fix & Build pozlarından MCPaul iskeletine yeniden yazıldı (`/Game/Sphirus/Player/Anim/Day`). 17 harita istasyonu ve hub bunlara bağlandı. Diz çökme montajı çalışırken pelvis 48 cm iniyor.

## 4. Kamera

- Tek hat: oyuncunun yay kolu ve kamerası. İstasyon ve uyanma sırasındaki `SetViewTargetWithBlend` devirleri `DayHub` ve `DayStation` içinden kaldırıldı. İstasyon kamera aktörünün konum yazımları graf içinde kaldı ama görüş hedefi olmadığı için ekrana etkisi yok.
- Adaptif davranış (kullanıcının gönderdiği referans karelerine göre): her karede karakter çevresine 5 kısa ışın atılıyor. Açıklık değeri; kol mesafesini (ev içi 0,90–1,40 m, dışarıda 1,50–2,05 m, hızla +0,20 m), sağ omuz ofsetini (38–56 cm), kamera yüksekliğini ve FOV'u (ev içi 66, dışarıda 70, hızla +3) yumuşak geçişle değiştiriyor. `GR_CamFocus` değişkeni etkileşimde yaklaşmak için hazır, ama henüz bir yere bağlı değil.
- Görsel sonuç: oturma odası, yatak odası ve bahçede karakter sol üçte birde, omzun arkasından yakın; referans karelerine yakın. Dar koridorda yay kolu çarpışması kamerayı başın içine çekiyor. Bu kusur açık.
- Kanıt notu: Epic Launcher editörün önündeyken editör arka planda kare yenilemiyor; bu yüzden bazı çekimler bir önceki kareyi gösteriyor. `HighResShot` bu turda oyuncu kamerasını değil başka bir görünümü verdi; kanıt oyun penceresinden alınan ekran görüntüleridir.

## 5. Kalan somut kusurlar

1. Eller ve kollar: idle'da ve yürüyüşte eller gövdenin arkasında görünüyor. Kaynak kliplerde eller iki yanda; sorun retarget pozunun Core Motion ↔ MetaHuman uyumunda. Otomatik hizalama denendi, sonuç görsel olarak doğrulanmadı.
2. Dar alanda kamera başa giriyor.
3. Ayak IK'sı yok; basamak ve eğimde ayak teması doğrulanmadı.
4. Tavan arası merdiveni her karede hata üretiyor ve AAMS'e bağlı.
5. Eski `PSD_Sph_Loco` veritabanı kullanılmıyor, silinmedi.
6. Ses, gamepad, 30/60 FPS, performans, save/load, pause ve cook test edilmedi.

## Değişen önemli varlıklar ve geri alma

- Başlangıç checkpoint'i: `C:\Users\berat\SphirusCheckpoints\Integrated_20261107_Start` (GraceRanger, Hazel_20261106, Day_20261107, EditableCharacters, StoryFramework, Config, SaveGames; 11,8 GB). Her yazma işinin doğrulanmış yedeği `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/day_*` altında.
- Değişenler: `BP_HybridA_Player`, `BP_GM_GR_GraceRanger`, `BP_PC_GR_GraceRanger`, `IMC_GR_SFGameplay`, `BP_GR_DayHub`, `BP_GR_DayStation`, `BP_GR_MaskBench`, `BP_GR_HomeContext`, `BP_GR_AtticContext`, `MI_Sph_Hair`, `MI_Sph_Body_*`, harita `L_GR_SphirusHouse` (istasyon klipleri). Yeni: `/Game/Sphirus/Player/*`, `/Game/Sphirus/CharacterLab/Sph_20261108/*`, `/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/{Schemas,Channels}` (GameAnimationSample'dan kopya).
- Kullanıcının kendi kayıt dosyası her testten sonra geri yüklendi.

## Kontrol yöntemi

Bütün testler gerçek haritada PIE içinde, otomasyonla (tuş enjeksiyonu, ışınlama, ekran görüntüsü) yapıldı. Elle oynanmadı. Video ve ses incelenmedi.
