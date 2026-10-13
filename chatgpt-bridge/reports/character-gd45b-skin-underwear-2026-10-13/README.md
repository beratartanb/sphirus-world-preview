# GD45 — Oyundaki karaktere aktarım: üretim vücudu (LK) + son kafa (GD38) + giysiler

Tarih: 2026-10-13 · Durum: **PASS (teknik) / kullanıcı incelemesi bekliyor (görsel)** · İlk üretim değişikliği (GD12–GD44 pasları aday olarak kaldı) · **GD45b eki:** iç çamaşırı kaldırıldı (ten malzeme override'ları, aşağıda)

Kullanıcı isteği: *"Bu vücut ayarlamalarını geri al, buna başlamadan önceki vücuda; ve kafayla kıyafetleri ile birlikte oyundaki karakterimize geçir."* + *"Kafa ayarlarımızda son güncel halini geçiriyorsun değil mi?"* → evet: GD38 T38.

## Ne yapıldı

- **Vücut:** GD39–GD44 vücut adayları **terk edildi** (hiçbiri üretime alınmamıştı; CharacterLab klasörleri ve raporlar duruyor). Oyun karakterinin vücudu = üretim/lookdev vücudu `SKM_LK_BodyMesh` (kabul edilen B2 + BR_Neutral + LK_Neutral; post-process `ABP_LK_Body_PostProcess` ile her zaman açık şekil eğrileri + SHC/RV düzeltmeleri). Oyun daha önce ham `MH_MainCharacter` MetaHuman vücudunu kullanıyordu.
- **Kafa:** `SKM_GD38_Face_t38` (oyunun `ABP_Face` anim sınıfı; MetaHumanCharacter eklentisi post-process'i mesh ile gelir).
- **Groom'lar:** saç ana + gevşek `GR_LK_Hair_Main/Loose_h75c`, GD38 özel kaş `GR_GD38_BrowCustom_ds8s`, GD31 ince kirpik; hepsi GD38 bağlarıyla (`GB_GD38_*_t38*`). Eski MetaHuman groom bileşenleri (Hair/Eyebrows/Eyelashes) PIE'de bağı düşürdüğü için yeni bileşenler eklendi (HairMain2/Eyebrows2/Eyelashes2/HairLoose), eskileri boşaltılıp gizlendi.
- **Giysiler:** `SKM_LK_Henley_g17e` + `SKM_LK_Shorts_g16c` (skinned) Manny altında; **Construction Script**'te `SetLeaderPoseComponent(Manny)` ile vücudu birebir takip ederler (şablon üstündeki LeaderPose örneklenmiyor; retarget ABP ile sürmek 6 cm sapma veriyordu).

## Sahip ve zincir

GameMode `BP_GM_GR_GraceRanger` → pawn `BP_PBI_Player` → `BP_GR_Player` → **`BP_Player_MM`** (`/Game/ActionAdventureMovementS/Animations/Locomotion/CoreMotionAAMS/Integrated/`) — Manny/Face/groom bileşenlerinin sahibi; tek mutasyon sahibi bu Blueprint. Çocuk BP'ler yeniden derlenip kaydedildi. Anim sınıfları değişmedi (`ABP_GR_MetaHuman` retarget, `ABP_Face`). İskeletler: oyun `metahuman_base_skel` ile ShoulderFix iskeleti 342 kemikle birebir aynı; yüz iskeletleri 875.

## Doğrulama (PIE, L_GR_SphirusHouse, son koşu)

1 pawn instance (`BP_PBI_Player_C`), hata yok. `Manny` = `SKM_LK_BodyMesh`, anim `ABP_GR_MetaHuman_C`, post-process `ABP_LK_Body_PostProcess_C` çalışıyor (eğriler BR_Neutral 1.0, LK_Neutral 1.0, RV/SHC canlı), LOD0. `Face` = `SKM_GD38_Face_t38`, anim `ABP_Face_C`, post-process `ABP_Face_PostProcess_C`. `Henley` / `Shorts`: lider = `Manny` (örnek), kemik dönüşümleri Manny ile birebir (spine_03 / thigh_l / hand_l aynı), kendi anim örneği yok. Groom'lar: HairMain2 / HairLoose / Eyebrows2 / Eyelashes2 bağlı ve görünür; eski 6 MetaHuman groom bileşeni boş/gizli. Kaydedilen paketler: yalnız `BP_Player_MM`, `BP_GR_Player`, `BP_PBI_Player`; harita kaydedilmedi; dirty paket yok (`process/*.json`).

Ekran görüntüsü: `boards/gd45_pie_player.png` (oyuncu kamerası).

## Geri alma

`Saved/Codex/GD45_Promote_20261013/checkpoint/` — `BP_Player_MM.uasset`, `BP_GR_Player.uasset`, `BP_PBI_Player.uasset` hash doğrulanmış kopyalar (değişiklik öncesi) + `owner.json`/`pawn2.json` (orijinal bileşen değerleri). Geri almak için editör kapalıyken üç dosyayı yerine kopyala.

## GD45b — Vücuttaki MetaHuman iç çamaşırının kaldırılması (ten malzemesi)

Kullanıcı isteği: *"Karakterin vücudunda klasik MetaHuman iç çamaşırı kalmış gibi, onu kaldır."*

- **Neden görünüyordu:** `SKM_LK_BodyMesh`'in varsayılan malzemesi `MI_RV_Body_Skin` MetaHuman'ın pişirilmiş (baked) vücut dokularını taşır; iç çamaşırı bu dokulara boyalıdır. Lookdev'de kabul edilen görünüm bileşen düzeyinde malzeme override'larıyla elde ediliyordu (`qa_config_after_gd38_chain.json` → `material_overrides`); GD45 aktarımında bunlar oyun pawn'ına taşınmamıştı. Yüz de aynı sebeple varsayılan MetaHuman baked ten/göz malzemeleriyle geliyordu.
- **Yapılan (`jobs/skin_overrides.py`):** `BP_Player_MM` içinde `Manny` ve `Face` şablonlarına `override_materials`: Manny slot 0 → `MI_GD15_Body_s1` (iç çamaşırsız ten, GD15 Looks); Face slot 0/9/10/12/13/14 → `MI_GD31_Face_LOD{0,1,2,3,4,5to7}_s1t6n_n3` (GD31 n3 ten), slot 3/4 → `MI_GD15_EyeL_h6` / `MI_GD15_EyeR_h6`. Derlendi; `BP_Player_MM`, `BP_GR_Player`, `BP_PBI_Player` kaydedildi, dirty paket yok. Öncesi kopyalar: `checkpoint2/` (GD45 aktarımı sonrası, ten değişikliği öncesi).
- **Doğrulama:** PIE koşu 6 — 1 pawn instance, hata yok; Manny `SKM_LK_BodyMesh` LOD0, Face `SKM_GD38_Face_t38`, Henley/Shorts lideri Manny (değişmedi). Kaydedilen `BP_Player_MM` paketinde yeni MI adları var (`MI_GD15_Body_s1`, GD31 LOD MI'ları, GD15 gözler), `checkpoint2` kopyasında yok → değişiklik diske yazıldı. Ekran: `boards/gd45b_pie_player_skin.png`; yaka kırpması önce/sonra `boards/gd45b_neckline_before_after.png` (sol = önce, Henley yakasının içinde gri iç çamaşırı bandı; sağ = sonra, sadece ten).
- **Dürüst sınır:** Oyuncu kamerası arkadan; göğüs/kalça bölgesi giysi altında olduğundan önden ten görüntüsü alınmadı. Ten tonu/yüz malzemesinin oyun ışığındaki görünümü senin kararın.

## Dürüst notlar / açık kalanlar

- Haritaya dokunulmadı (bir denetim işinin bıraktığı geçici pawn aktörü silindi, harita kaydedilmedi).
- Giysi deformasyonu oyunda: lider-poz ile RV düzeltme eğrileri vücuttan geçer; Chaos cloth şort (`CA_CR_Shorts_m1`) kullanılmadı (skinned).
- Görsel kabul: ten/saç/giysi oyun ışığında senin kararın; hatlar/anatomi işi (GD41–44) üretimde değil.
- Eski `Hair/Eyebrows/Eyelashes/Fuzz/Mustache/Beard` bileşenleri boş ve gizli olarak duruyor (silinmedi; kolay geri dönüş).
