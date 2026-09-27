# Sphirus — Head-Only Conform + Native MetaHuman Body

28 Eylül 2026. Son kabul edilmiş yüz durumundan devam edildi. Blender BODY çalışması donduruldu; üretim bedeni olarak kullanılmadı. Kontrollü bir MetaHuman adayı üretildi, gerçek Unreal rig’iyle sınandı. **Üretim karakteri değiştirilmedi. Tam üretim onayı verilmedi: yüz deformasyonu aşağıdaki nedenle PARTIAL.**

| Kabul kapısı | Sonuç | Kapsam |
|---|---|---|
| FACE SHAPE | PASS | Önceki yüze göre çene, burun ve ağız geçişleri iyileşti; konsept birebir tarama değildir. |
| METAHUMAN CONFORM | PASS | Baş-only UV eşlemesi, yerel boyun uyarlaması ve baş ölçeği düzeltmesi başarılı. |
| FACIAL DEFORMATION | PARTIAL | Gerçek RigLogic çalışıyor; uç funnel pozunda ağız köşesi/perioral katlanma sıkı. Birleşik ifadeler ve konuşma teması onaylanmadı. |
| BODY PROPORTIONS | PASS | Native kadın beden tabanı, referansa göre dengeli parametreler; gerçek boy 173.418671 cm. |
| BODY DEFORMATION | PASS | İncelenen 12 poz ve ek hareket örnekleri için. Oyun içi locomotion/ayak teması veya tüm LOD’lar için onay değildir. |

## Koruma ve teslim

- Önceki **850 dosya** hash ile, **86 üretim paketi** hash ile doğrulandı. Ana MetaHuman kaynağı değişmedi. 1676 dosyalık oyun sistemi envanterinde boyut/zaman damgası farkı yok.
- Orijinal, Pass 1, Pass 2, yumuşatma ve beden-anatomi sürümleri korunuyor. `CHECKPOINT_BodyFrozen_HeadBaseline.blend` son beden çalışmasının birebir kopyasıdır.
- Blender: `SourceAssets/Characters/SphirusHeadMetaHuman_20260928/Sphirus_FinalHead_EDITABLE.blend` ve `Sphirus_FinalHead_Neutral.blend`.
- Baş girdileri: aynı klasörde `HeadTargets/SM_SPH_FinalHead.fbx`, iki göz ve diş FBX’leri. **Body Conform girdisi yok.** Donmuş BODY yalnızca referans/fallback.
- Düzenlenebilir Unreal aday: `/Game/Sphirus/CharacterLab/HeadMetaHuman_20260928/MH_Sphirus_AlignedTest`.
- Nihai rig’li geometri: `/Game/Sphirus/CharacterLab/HeadMetaHuman_20260928/FinalNativeScaled/`. `Initial`, `AlignedRigged`, `NativeBodyV*` ve `FinalNative` ara kontrollerdir; son teslimi bunlarla karıştırmayın.
- Tüm yeni Unreal varlıkları tarihli CharacterLab alanındadır. QA animasyonları ve kil malzemeleri tanılama içindir. Üretim Blueprint’i, iskelet rest matrisleri, AAMS/Core Motion, kamera, input, animasyon veritabanları ve seviye dosyaları kaydedilerek değiştirilmedi. Test dünyası geçici ve kaydedilmemiştir.

## Blender yüz geçişi

Mevcut baş üzerinde `SPH_Final_Head_Identity` katmanı oluşturuldu. Çene köşesi ve çene ucu çevresi kontrollü daraltılıp yuvarlandı; sivri bir çene yapılmadı. Burun kökü/dorsum/yan duvar–uç birleşimi yumuşatıldı, yetişkin projeksiyonu korundu. Kaş ve glabella geçişindeki sertlik azaltıldı; gözler büyütülmedi ve göz küreleri taşınmadı. Yanak–alt yüz geçişine yumuşak doku desteği, dudaklara sınırlı doğal projeksiyon ve köşelere rahatlık eklendi. İlk burun adayı yeniden gözden geçirilip supratip akışı düzeltildi.

Önceki yüze göre maksimum yer değiştirme **3.862620592 mm**, ortalama **0.588355601 mm**. Bunlar mesh karşılaştırmasıdır; konsept için sahte fiziksel ölçüler değildir. BODY yer değiştirmesi **0 mm**, yeni BODY key’i **yok**.

Topoloji, vertex/polygon/loop sırası, UV’ler, kaynak indeksleri, ağırlıklar ve rig rest matrisleri değişmedi. Önceki **863 baş key’i** aynen korundu; yeni key eklendi. Önceki ifade geometrisi üzerine yazılmadı. Nötr geometride yeni dejenere veya ters dönen üçgen yok. Blender’da 93 birleşim eşleşmesinin en büyük farkı **0.000242561 mm**; kaynak yükseklik **173.40184021 cm**.

Blink, brows up/down, smile, mouth open, jaw open, purse ve funnel ham Blender problarında önceki sürüme göre ek ters üçgen **0**. Bu ham corrective kontrolü nihai RigLogic testi yerine kullanılmadı. Baş FBX round-trip’inde parça sayıları/topoloji aynı, UV hatası 0; en büyük dünya koordinatı farkı **0.000120746 mm**.

## Baş-only MetaHuman Conform

UE **5.8.1 / CL 56057345** kurulu MetaHuman araçları kullanıldı. Üretim `MH_MainCharacter` kopyalanarak izole test karakteri açıldı. `MetaHumanCharacterEditorSubsystem.import_from_template` ile baş, sol/sağ göz ve diş statik mesh’leri verildi:

- `match_vertices_by_u_vs=True`, `use_eye_meshes=True`, `use_teeth_mesh=True`.
- Hizalama: `ROTATION_TRANSLATION`; giriş eşleşmesinde ölçek fit edilmedi.
- Son ayar: `isolate_head_from_body=False` → yerel boyun uyarlaması açık. Bu baş API’sidir; hiçbir Blender BODY mesh’i verilmedi, `ConformBody` çağrılmadı.
- Son yerel `HeadScale`: **1.0579111576**. `GlobalDelta=1`, `HighFrequencyDelta=0`.
- Auto Rig: **JOINTS_AND_BLEND_SHAPES**; DNA, RigLogic ve **858 facial morph** üretildi. Parametrik beden değişimlerinden sonra rig yeniden üretildi.

İlk izole deneme yüzü korudu fakat başı şablon yüksekliğinde bıraktı; boyun kopukluğu nedeniyle reddedildi. Boyun uyarlaması bunu düzeltti, ancak yüzü yaklaşık %5.47 küçülttü. Bu sessizce kabul edilmedi: yerel baş ölçeği ve beden Height parametresi birlikte ayarlanarak yeniden rig üretildi. Ara beden export’unda görülen boyun render bozulması da yeni rig ile giderildi.

**24.408 / 24.408 UV örneği** eşleşti. Son yüz bölgesinde yalnızca rijit hizalamayla ortalama fark **0.252997 mm**, p95 **0.496209 mm**, maksimum **0.757067 mm**. Boyun dahil tüm başın rijit hizalama farkı ortalama **0.986249 mm**, maksimum **9.490649 mm**: yerel beden boyun bağlantısına adaptasyon yüz kimliği ölçümünden ayrı tutuldu. Yüz bölgesi tanımı ve hizalama verileri JSON’da açıktır.

Son yerel baş–beden birleşiminde 93 yakın yüzey örneği maksimum **0.000240764 mm** fark verdi. Bu, yeni native beden ile yüzey yakınlığı kontrolüdür; eski Blender bedeniyle aynı indeksli seam iddiası değildir.

## Gerçek yüz rig’i

Son rig üzerinde **19 durum, iki açı, 38 kayıt**: neutral; iki/sol/sağ blink; squint; dört bakış yönü; kaş yukarı/aşağı; smile; frown; mouth open; jaw open; purse; funnel; wide mouth; cheek raise. Kurulu MetaHuman Face PostProcess ve DNA/RigLogic etkin, kontrol eğrilerinin beklenen değerleri geri okunarak doğrulandı.

Göz kırpması kapatıyor, tek göz kontrolü ayrışıyor; bakış, kaş, yanak, dudak ve çene hareketleri oluşuyor. Önceki Blender blink riski doğrudan nihai başarısızlık sayılmadı. **Uç funnel’de ağız köşesi ve dudak çevresi fazla sıkı katlanıyor; bu alan yayın kalitesi için hâlâ gözden geçirilmeli.** Karma ifadelerde dudak teması, konuşma, tüm LOD’lar ve zaman içinde ifade geçişleri sertifikalanmadı. Bu nedenle FACIAL DEFORMATION = PARTIAL.

## Native MetaHuman beden

Başlangıç, mevcut karakterin düzenlenebilir kadın native beden durumudur (`fixed_body_type=False`); bağımsız Blender bedeninin üretim topolojisi kullanılmadı. Native anatomik taban sırt/kürek kemiği/omurga/lomber ve posterior pelvis için esas alındı. Ön referanstan görünmeyen sırt ayrıntıları uydurulmadı. Göğüs desteği fotoğraftaki sütyen sıkıştırması olarak kopyalanmadı.

Bel daralması azaltıldı, alt kaburga çevresi desteklendi; göğüs baskınlığı kontrollü azaltılırken hip/high-hip geçişi dengelendi. Kol, önkol, uyluk ve baldır hacimleri aktif bir yetişkin silüetine yaklaştırıldı. Yerel modelin anatomisi korundu; yeni çıplak yüzey mikro-heykeli yapılmadı.

Aşağıdakiler **MetaHuman hedef parametreleridir**, referanstan ölçülmüş antropometrik gerçekler değildir. Çevre/uzunluk kontrolleri sistemin cm birimindedir; Fat, Muscularity ve Masculine/Feminine model koordinatlarıdır.

| Parametre | Başlangıç | Son |
|---|---:|---:|
| Height | 172.27634 | 171.75000 |
| Chest | 89.64314 | 88.50000 |
| Underbust | 70.63282 | 73.00000 |
| Waist | 66.27908 | 69.80000 |
| Hip | 94.94785 | 93.50000 |
| High Hip | 76.38291 | 79.00000 |
| Across Shoulder | 29.12338 | 29.80000 |
| Bicep | 25.27611 | 26.50000 |
| Forearm | 21.52770 | 21.50000 |
| Thigh | 47.76723 | 49.00000 |
| Calf | 32.19025 | 33.30000 |
| Fat | 0.40517 | 0.30000 |
| Muscularity | -1.20102 | -0.75000 |
| Masculine/Feminine | 0.03127 | 0.03127 |

Diğer aktif kol/bacak/neck kısıtları korundu; Forearm etkinleştirildi. Native Height hedefi **171.75 cm**, baş ölçeği uyarlaması nedeniyle toplam yüzey boyuyla aynı sayı değildir. FBX geometri üzerinden ölçülen nihai toplam boy **173.41867065 cm**; Blender referansından fark **+0.01683044 cm**. Referansın genel hacim ilişkisine yaklaşım amaçlandı; fotoğrafla milimetrik anatomik aynılık iddia edilmiyor.

## Unreal beden doğrulaması

Nihai `FinalNativeScaled` geometri ve gerçek MetaHuman Body PostProcess kullanıldı. Baş, native `ABP_Face` Copy Pose ile bedene bağlandı. **Idle, walk, jog, sprint, crouch, jump, kollar yukarı, kollar öne, omuz dönüşü, torso twist, hip flexion, deep knee bend** üç açıdan; dört hareketin iki ek evresiyle toplam **44 kare** incelendi.

Native idle/walk ve BodyROM klipleri kullanıldı. Jog/sprint/crouch/jump için mevcut retarget reçetesi salt okunarak yeni CharacterLab QA klipleri üretildi. Kaynak animasyon/retargeter/veritabanı düzenlenmedi. Kayıtta gerçek animasyon zamanı, post-process örneği ve baş kemiği eşleşmesi kontrol edildi. Tüm örneklerde baş/body kemik konumu farkı 0.001 cm sınırının altında. Yatay pelvis hareketi yalnızca kamera kadrajı için QA aktörü üzerinde ortalandı; kaynak animasyon değişmedi.

Omuz/koltuk altı, göğüs, bel, sırt, pelvis, diz ve boyunda büyük yeni yırtılma/kopma görülmedi. Sıkışma pozlarında native hacim daralması var; kumaş temasları henüz sınanmadı. Bu kayıtlar oyun sistemi, ayak kayması, retarget animasyon estetiği veya packaged performans onayı değildir.

## Kalanlar ve sınır

Uç dudak pozları, birleşik yüz ifadeleri/konuşma ve düşük LOD’lar ayrı yüz doğrulaması gerektiriyor. Son görünüş için skin/hair/garment yok; mevcut miras alınan saç/wardrobe üretimi yapılmadı, değerlendirme çekimlerinde gösterilmedi. Üretim karakteri yerine geçiş yapılmadı. **Blender beden heykeline, Body Conform’a, kıyafete, Groom’a veya gameplay değişikliğine devam edilmedi.**

Kurulu Epic kaynakları ve [MetaHuman Python scripting](https://dev.epicgames.com/documentation/metahuman/metahuman-creator-python-scripting-in-unreal-engine?lang=en-US), [custom mesh workflow](https://dev.epicgames.com/documentation/metahuman/metahuman-creator-from-custom-mesh-tool-in-unreal-engine) davranışı esas alındı. Kurulu sürümün enum/API imzaları doğrudan doğrulandı.


## Karşılaştırma kanıtları

Tüm model panelleri gerçek Blender veya Unreal geometri görüntüleridir. Referanslar kullanıcının sağladığı görsellerdir. Karşılaştırma panoları yalnızca yerleştirme/ölçekleme/kırpma ve etiketleme içerir; model görüntüsü üretilmedi veya rötuşlanmadı. Işık motorları farklı olduğundan yüz tonu/gölgeyi şekil değişimiyle karıştırmayın.

### HEAD | Previous accepted face to final Blender target

![HEAD | Previous accepted face to final Blender target](01_blender_head_before_after.jpg)

### HEAD | Identity history and primary concept

![HEAD | Identity history and primary concept](02_head_history.jpg)

### HEAD | Blender target versus actual Unreal MetaHuman

![HEAD | Blender target versus actual Unreal MetaHuman](03_blender_vs_metahuman.jpg)

### FACE IDENTITY | Target, conformed head, concept

![FACE IDENTITY | Target, conformed head, concept](04_head_concept.jpg)

### FINAL METAHUMAN | Neutral clay head

![FINAL METAHUMAN | Neutral clay head](05_unreal_head_four_views.jpg)

### BODY | Initial native MetaHuman to parametric candidate

![BODY | Initial native MetaHuman to parametric candidate](06_native_body_before_after.jpg)

### BODY | Native before / after and supplied references

![BODY | Native before / after and supplied references](07_body_reference.jpg)

### NATIVE ANATOMY | Back and torso continuity

![NATIVE ANATOMY | Back and torso continuity](08_native_back.jpg)

### NATIVE BODY | Ribcage, waist and pelvis

![NATIVE BODY | Ribcage, waist and pelvis](09_torso_detail.jpg)

### REAL RIGLOGIC | Expression probes 1

![REAL RIGLOGIC | Expression probes 1](10_facial_1.jpg)

### REAL RIGLOGIC | Expression probes 2

![REAL RIGLOGIC | Expression probes 2](10_facial_2.jpg)

### REAL RIGLOGIC | Expression probes 3

![REAL RIGLOGIC | Expression probes 3](10_facial_3.jpg)

### REAL RIGLOGIC | Expression probes 4

![REAL RIGLOGIC | Expression probes 4](10_facial_4.jpg)

### REAL METAHUMAN | Body deformation probes 1

![REAL METAHUMAN | Body deformation probes 1](11_body_poses_1.jpg)

### REAL METAHUMAN | Body deformation probes 2

![REAL METAHUMAN | Body deformation probes 2](11_body_poses_2.jpg)

### REAL METAHUMAN | Body deformation probes 3

![REAL METAHUMAN | Body deformation probes 3](11_body_poses_3.jpg)

### UNREAL | Additional locomotion samples

![UNREAL | Additional locomotion samples](12_locomotion_samples.jpg)

## Teknik kayıtlar

- [head_validation.json](head_validation.json)
- [v2_change_metrics.json](v2_change_metrics.json)
- [head_fbx_roundtrip.json](head_fbx_roundtrip.json)
- [ue_head_alignment_correction.json](ue_head_alignment_correction.json)
- [ue_native_head_scale_adjustment.json](ue_native_head_scale_adjustment.json)
- [head_final_conform_deviation.json](head_final_conform_deviation.json)
- [ue_body_parameters_v2.json](ue_body_parameters_v2.json)
- [ue_final_facial_tests.json](ue_final_facial_tests.json)
- [ue_body_validation.json](ue_body_validation.json)
- [ue_qa_retarget_results.json](ue_qa_retarget_results.json)
- [ue_final_asset_audit.json](ue_final_asset_audit.json)
- [ue_production_database_readonly_check.json](ue_production_database_readonly_check.json)
- [preservation_final.json](preservation_final.json)
- [final_review.json](final_review.json)
- [boards_manifest.json](boards_manifest.json)
- [delivery_hashes.json](delivery_hashes.json)

[Önceki Blender beden-anatomi raporu — dondurulmuş referans](../character-body-anatomy-2026-09-27/TEKNIK_RAPOR.md)
