# Sphirus — Final Face Identity / Head-Only Re-Conform / Native Regional Polish

28 Eylül 2026. Başarılı **Identity Pass 2 + BodyE** adayından devam edildi. Üç Blender baş iterasyonu, aynı head-only Conform, native bölgesel beden düzenlemesi ve gerçek RigLogic testleri yeni bir CharacterLab sürümünde gerçekleştirildi.

**Bu test adayı üretim karakterinin yerine geçirilmedi. “FinalIdentity” sürüm adıdır; bütün sanatsal ve deformasyon kabul kapılarının geçtiği anlamına gelmez. Kalıcı ifade kalibrasyonu yapılamadı.**

| Kabul kapısı | Sonuç | Kanıt ve kalan sınır |
|---|---|---|
| FACE SHAPE | **PARTIAL** | Burun profili uzadı, ağız genişledi ve merkez purse izlenimi azaldı. Konseptin burun ucu/alar ritmi, rahat dudak şekli ve yanak–alt yüz yumuşaklığı henüz yeterince özgül değil; tam kimlik aktarımı iddia edilmiyor. |
| METAHUMAN CONFORM | **PASS** | 24.408/24.408 UV eşleşmesi, yeniden çözülmüş HeadScale, yüz bölgesinde yaklaşık 0.0036 mm ortalama fark ve temiz native birleşim. Bu geçiş onayıdır, konsept benzerliği onayı değildir. |
| FACIAL DEFORMATION | **PARTIAL** | Maya ve MetaHuman for Maya Expression Editor yok; kalıcı ifade kalibrasyonu yapılmadı. Funnel/wide ve bazı jaw birleşimleri görsel kalite kapısından geçmiyor. QA destek eğrileriyle gizlenmedi. |
| BODY PROPORTIONS | **PARTIAL** | Native bölgesel polish, boy hedefi ve anatomik sırt korundu; bel/underbust ilişkisi sınırlı iyileşti. Referansa göre üst torso ve pelvis–uyluk dağılımı hâlâ genel bir native çözüme yakın; tam oran eşleşmesi onaylanmadı. |
| BODY DEFORMATION | **PASS** | Yalnızca 12 test pozu, 8 ek faz ve 2 görünürlük ek çekimindeki LOD0 kapsamı: büyük yeni çökme, yırtık veya baş–beden kopması görülmedi. Gameplay/root-motion/ayak teması sertifikasyonu yok. |

## Koruma ve teslim

Önceki **2150 dosya** ve **86 üretim paketi** SHA-256 karşılaştırmasında değişmedi. **5420 dosyalık** gameplay/ayar envanteri boyut/zaman damgası bakımından aynı; bu geniş envanterin tamamı için hash doğrulaması iddia edilmiyor. Orijinal, Pass 1, Pass 2, yumuşatma, beden-anatomi ve önceki başarılı MetaHuman sürümleri korundu.

- Başlangıç yedeği: `SourceAssets/Characters/SphirusFinalIdentity_20260928/CHECKPOINT_IdentityP2.blend`.
- Düzenlenebilir teslim: `Sphirus_FinalIdentity_EDITABLE.blend`; nötr sürüm: `Sphirus_FinalIdentity_Neutral.blend` (aynı klasör).
- Yeni katman: `SPH_FinalIdentity_Refinement`; baz katman: `SPH_Face_Identity_Pass2`. v1/v2/v3 ve delta dosyaları ayrı korundu; seçilen v3.
- Head-only FBX girdileri: aynı klasörde `HeadTargets/`; source-index manifesti ve round-trip kayıtları mevcut.
- Unreal düzenlenebilir aday: `/Game/Sphirus/CharacterLab/FinalIdentity_20260928/MH_Sphirus_FinalIdentity`.
- Rigli teslim meshleri: aynı kökte `FinalCandidate/`. `RegionalA`, `FinalUnitScale`, `FinalScaledNeutral` ara çıktılardır; final rig yerine kullanılmamalıdır.
- Yüz testleri ve konuşma geçişi: `Diagnostics/AS_FINAL_RigLogic_Singles_Blends`, `AS_FINAL_Speech_Transitions`; dört hareket klibi yeni `Diagnostics/Motion/` kopyalarıdır.
- Yerel kanıtlar: `Saved/Codex/CharacterFinalIdentity_20260928/`. Kaynak .blend/.uasset/FBX dosyaları herkese açık depoya yüklenmedi; teslim hashleri rapora eklendi.

Üretim karakteri, Blueprint davranışı, skeleton mimarisi, locomotion, AAMS, Core Motion, kamera, input ve level dosyaları değiştirilmedi. Testler geçici dünyada yapıldı; dünya elle üretim level'i olarak kaydedilmedi. Unreal'ın geçici dünya autosave'i üretim level değişikliği değildir. Kaynak animasyonların okunmasıyla bellekte kirlenen PoseSearch paketi diskte hash değişmeden yeniden yüklenerek atıldı; SaveAll kullanılmadı.

## Blender yüz kimliği

Burun kökü–dorsum çizgisi uzatıldı, köprü/tip projeksiyonu ve tip rotasyonu ayrı alanlarda değiştirildi. Alar/yan duvar geçişleri ve paranasal destek yuvarlatıldı. Ağız köşeleri genişletildi, merkezdeki öne kıvrılmış dudak görünümü azaltıldı; commissure ve üst dudak desteği birlikte düzenlendi. Maxilla ve malar hacim hafifçe desteklendi. Çene köşesinde küçük yumuşatma, üst kapak eğrisinde sınırlı düzeltme yapıldı; göz küreleri ölçeklenmedi.

v1 → v2 → v3 incelemesinde burun profilinin kısa kalması ve merkez dudak çıkıntısı yeniden ele alındı. Ön, gerçek yan ve iki 3/4 görüntü değerlendirildi. Ana bakır saçlı konsept kimlik otoritesidir; dört yönlü kel baş yalnızca kranial/yan profil kontrolüdür. Kalibre edilmemiş konseptten kesin anatomik ölçüler türetilmedi.

**Görsel değerlendirme:** Üç iterasyonun ardından burun artık daha uzun ve profilde daha yetişkin; ağız köşeleri daha geniş, merkezi öne itilmiş dudak izlenimi azaltılmış. Bununla birlikte konseptin daha organik tip/alar biçimi, philtrum–dudak ritmi ve malar–çene geçişi bütünüyle yakalanmadı. Clay görünümde yanak ve perioral bölgede hâlâ yapay sertlik var; yüz bir ölçüde özelleştirilmiş MetaHuman olarak okunuyor. FACE SHAPE bu nedenle PARTIAL; yüzü tamamen bitmiş saymıyorum.

Identity P2 başına göre maksimum mesh değişimi **4.562612057 mm**, ortalama **0.709999204 mm**, 1 mm üzerinde **9350 vertex**. Bunlar gerçek meshler arası farktır.

**Blender BODY değişimi 0 mm**, yeni BODY key yok. Baş vertex/edge/polygon/loop düzeni, UV, ağırlık, source correspondence ve önceki **865 key** korundu. Mevcut rig rest matrisleri aynı. Nötr durumda yeni dejenere/ters üçgen yok. 93 Blender seam çiftinde maksimum fark **0.000242561 mm**. Donmuş Blender boyu **173.40184021 cm**; bu üretim native bedeninin ölçüsü değildir.

Sekiz ham ifade probunda önceki sonuca göre ek ters üçgen oluşmadı. Ancak önceki sorunlar sıfırlanmış değildir: **blink: ek 0, toplam 8; brows_up: ek 0, toplam 0; brows_down: ek 0, toplam 0; smile: ek 0, toplam 6; mouth_open: ek 0, toplam 0; jaw_open: ek 0, toplam 0; lip_purse: ek 0, toplam 10; lip_funnel: ek 0, toplam 13**. Bunlar legacy morph geometrisinin sınırlı problarıdır, RigLogic sertifikasyonu değildir. FBX round-trip vertex/topoloji/UV eşleşti; UV farkı 0, en büyük dünya uzayı farkı **0.000120746 mm**.

## Kanıtlanmış head-only Conform

UE 5.8.1 / CL 56057345 kurulu MetaHuman araçları kullanıldı. Baş, iki göz ve diş girdileriyle aynı `import_from_template` yolu:

- Head Only; `match_vertices_by_u_vs=True`, `use_eye_meshes=True`, `use_teeth_mesh=True`.
- `ROTATION_TRANSLATION`; `isolate_head_from_body=False` ile native yerel boyun uyarlaması.
- Custom BODY girdisi ve Body Conform yok. `GlobalDelta=1`, `HighFrequencyDelta=0` stratejisi korundu.
- Önceki çarpan temizlenip HeadScale=1 ile yeniden çözüldü; **1.0691862106 → 1.0675376654**. Yeni yüz için eski değer otomatik taşınmadı.
- AutoRig `JOINTS_AND_BLEND_SHAPES`; **858 facial morph** ve native DNA/RigLogic üretildi. Bu otomatik rig üretimi, elle yapılmış expression corrective kalibrasyonu değildir.

**24.408 / 24.408 UV örneği eşleşti.** Yüz bölgesinde yalnızca rijit hizalama sonrası ortalama **0.003590 mm**, p95 **0.003835 mm**, maksimum **0.004189 mm**. Teslim meshine hata küçültmek için ek ölçek fit uygulanmadı. Bağımsız tanısal similarity ölçeği yaklaşık 1.

| Bölge — aynı yüz hizalama çerçevesi | Ortalama mm | Maksimum mm |
|---|---:|---:|
| jaw_chin | 0.171520 | 3.009233 |
| nose | 0.003585 | 0.004075 |
| mouth | 0.003592 | 0.004076 |
| eyes_brow | 0.003585 | 0.004189 |
| cheeks | 0.003596 | 0.004077 |
| skull | 0.014766 | 0.077285 |
| neck_adaptation | 9.253407 | 24.547363 |

Boyun/omuz tabanı native bedene adapte edildiği için tüm başta tek düşük hata sayısı sunulmuyor. Çene-altı bölgesindeki 3 mm uç değer boyun adaptasyonuna yakın; burun, ağız, göz ve yanak farkları ayrı tabloda. Bütün baş üzerinden rijit hizalama ortalaması **1.463325 mm**, maksimum **22.297493 mm**. Bu geniş adaptasyon bölgesi yüz kimliği sapmasıyla karıştırılmamalı.

Native nötr seam komşuluğunda 93 örnek, maksimum **0.000357938 mm**. Bu en yakın yüzey kontrolüdür; native beden ile donmuş Blender bedeninin aynı indekslerde olduğu iddiası değildir. Rigli pozlarda ayrıca görsel boyun ve baş/body head-bone eşleşmesi kontrol edildi.

## Kalıcı facial corrective — yapılamadı

**Eksik bağımlılıklar: Autodesk Maya / mayapy çalışma ortamı ve MetaHuman for Maya Expression Editor entegrasyonu.** PATH, standart Program Files dizinleri ve kullanıcı Maya dizinleri tarandı; erişilemeyen ilgisiz korumalı alt dizinler kayıtlıdır. Tüm diskin eksiksiz tarandığı iddia edilmiyor. Kurulu Unreal editöründe ifade-pozu sculpt/kalibrasyonu sağlayan Expression Editor API'si bulunmadı; DNA import ve AutoRig bu işlemin yerine geçmiyor.

Epic'in [Expression Editor belgeleri](https://dev.epicgames.com/documentation/metahuman/expression-editor) desteklenen Maya ortamında rigli karakterin ifadelerini kalibre eden iş akışını açıklıyor. Bu ortam mevcut olmadığından funnel, wide, smile, purse veya jaw birleşimleri için kalıcı corrective sculpt/DNA değişikliği **yapılmadı**. AutoRig yeni nötr hedef için DNA üretti; expression bazlı kalıcı düzenleme yapılmış gibi raporlanmıyor. QA support eğrileri, runtime remap veya tüm ifadeleri zayıflatma kullanılmadı.

**FACIAL DEFORMATION = PARTIAL.** Eksik ortam sağlandıktan sonra aynı adayın DCC Export'u üzerinden ifade kalibrasyonu ve bu test setinin tekrarı gerekir.

## Gerçek RigLogic testi

19 tekil + 8 birleşik + 6 konuşma benzeri durum = **33 durum / 66 görüntü**, ön ve 3/4 açılar. Native post-process ve gerçek curve readback kullanıldı. Her yakalamada beklenen kontrol değerleri ile okunan değerler 0.01 toleransta doğrulandı. Eski Identity P2 ham ifadeleriyle aynı birincil değerler karşılaştırıldı; destek eğrisi eklenmedi.

| Durum | Sonuç | Görsel bulgu |
|---|---|---|
| neutral | PARTIAL | Nötr ağız daha geniş; merkez dudak rulosu ve perioral sertlik hâlâ konseptten farklı. Büyük geometri kopması yok. |
| blink | PARTIAL | İki kapak kapanıyor, göz küresi dışarı taşmıyor; iç üst kapak kıvrımı sert. Temasın bütün aralıkta üretim kalitesi onaylanmadı. |
| blink_left | PARTIAL | Tek taraflı kapanma çalışıyor; iç kapak kıvrımının yumuşatılması gerekir. |
| blink_right | PARTIAL | Tek taraflı kapanma çalışıyor; iç kapak kıvrımının yumuşatılması gerekir. |
| squint | PASS | Test uç değerinde kapak ve yanak birlikte hareket ediyor; büyük kopma veya göz küresi penetrasyonu görünmüyor. Yalnızca bu örnek. |
| look_up | PARTIAL | Bakış/üst kapak takibi çalışıyor; uç bakışta alt kapak göz ilişkisi ve sklera açıklığı ayrıca kalibre edilmeli. |
| look_down | PARTIAL | Üst kapak bakışı takip ediyor; alt kapak çizgisi belirgin kararıyor. Sürekli göz-kapak temas onayı verilmedi. |
| look_left | PASS | Yatay bakış takibi mevcut; incelenen iki açıda belirgin küre penetrasyonu yok. |
| look_right | PASS | Yatay bakış takibi mevcut; incelenen iki açıda belirgin küre penetrasyonu yok. |
| brows_up | PASS | Kaş/alın hareketi sürekliliğini koruyor; incelenen örnekte büyük çökme yok. |
| brows_down | PASS | Glabella/kaş aşağı hareketi çalışıyor; büyük geometri kopması görünmüyor. |
| smile | PARTIAL | Köşeler yükseliyor, yanak katılımı var; commissure çizgisi fazla keskin ve mekanik, alt dudak geriliyor. |
| frown | PARTIAL | Köşeler aşağı hareket ediyor; perioral gerilim sert ve simetrik. Uç poz doğal ifade kalitesi olarak onaylanmadı. |
| mouth_open | PARTIAL | Ağız açıklığı, diş ve çene devamlılığı korunuyor; alt dudak kenarı fazla düz/kalın. |
| jaw_open | PARTIAL | Çene bağlantısı korunuyor; dudak halkası ve alt dudak düzlüğü üretim polish gerektiriyor. |
| lip_purse | PARTIAL | Merkez öne geliyor; köşe sıkışması ve silindirik dudak izlenimi sürüyor. |
| lip_funnel | FAIL | Kalın halka, köşe sıkışması ve radyal katlanma belirgin. Kalıcı corrective yapılmadı. |
| wide_mouth | FAIL | Yatay bant görünümü, sert commissure ve doğal dudak şekli kaybı sürüyor. |
| cheek_raise | PASS | Yanak/alt kapak katılımı görünür; bu örnekte büyük çökme yok. |
| smile_jaw | PARTIAL | Açıklık ve yanak katılımı sürüyor; ağız köşeleri ve alt dudak çizgisi mekanik. |
| funnel_jaw | FAIL | Çene açılınca kalın halka uzuyor; köşe/radyal sıkışma çözülmedi. |
| purse_jaw | PARTIAL | Kontroller birlikte çalışıyor; dudaklar fazla sıkışık ve öne itilmiş görünüyor. |
| brow_squint | PASS | Kaş ve kapak birlikte çalışıyor; incelenen durumda büyük geometri kopması yok. |
| smile_cheek | PARTIAL | Yanak katılımı artıyor ancak commissure sertliği kalıyor. |
| browup_smile | PARTIAL | Kaş hareketi stabil; smile kaynaklı dudak/köşe sertliği devam ediyor. |
| squint_smile | PARTIAL | Üst/alt yüz birleşimi çalışıyor; ağız köşesi gerilimi çözülmüyor. |
| wide_jaw | FAIL | Alt dudak yatay bandı ve dikdörtgene yaklaşan ağız açıklığı belirgin. |
| speech_MBP | PARTIAL | Dudak kapanması okunuyor; merkez/köşe sıkılığı ve tüm geçişte temas henüz kalibre değil. |
| speech_AH | PARTIAL | Çene açıklığı okunabilir; alt dudak konturu fazla bant biçimli. |
| speech_EE | PARTIAL | Yatay açıklık okunuyor; köşeler sert ve dudak incelmesi doğal değil. |
| speech_OH | FAIL | Funnel kaynaklı kalın dudak halkası ve yan köşe sıkışması sürüyor. |
| speech_OO | PARTIAL | Yuvarlanma mevcut; perioral bölge hâlâ fazla sıkı ve öne itilmiş. |
| speech_FV | PARTIAL | Alt dudak hareketi mevcut; üst diş-alt dudak temasını üretim düzeyinde doğrulayan görünür kanıt yeterli değil. |

**Kalan yüz deformasyonu:** Funnel kalın halka ve köşe sıkışması oluşturuyor; wide-mouth alt dudağı yatay bir banda yaklaştırıyor. Smile ve jaw-open birleşimleri kopmuyor fakat köşe yörüngesi ve alt dudak konturu mekanik. Purse öne çıkan sıkı bir merkez üretmeye devam ediyor. Blink kapanıyor ancak iç üst kapak kıvrımı sert; dikey bakışta kapak teması ayrıca kalibre edilmeli. Bu sorunların kalıcı corrective düzeltmesi yapılmadı.

MBP → AH → EE → OH → OO → FV → MBP geçişleri başta/sonda nötr ile **8 saniyelik, 30 fps** yerel QA animasyonunda oluşturuldu. 10 fps aralığında 81 ön örnek ve 8 ara 3/4 örnek: **89 görüntü**. GIF bu gerçek örneklerden oluşur. 81 ön ara örnek ve 8 ara 3/4 görüntü incelendi. Kontroller değişirken ani mesh kopması görülmedi; fakat yaklaşık 2.7–3.3 saniyede EE benzeri yataylaşma, 3.6–4.4 saniyede OH/funnel halkası belirginleşiyor. MBP kapanması okunabilir; FV diş/dudak temasının doğruluğu bu görüntülerle üretim düzeyinde onaylanamıyor. Akıcı kontrol interpolasyonu, doğal konuşma deformasyonu ile eş tutulmadı. Ses eşzamanlama, tüm ara 30 fps karelerin bağımsız denetimi veya tam diyalog sertifikasyonu iddia edilmiyor.

## Native beden — sınırlı bölgesel polish

Başlangıç **Identity P2 / BodyE**. Fat −0.90, Muscularity +1.00 ve Masculine/Feminine +0.35 aynen korundu. Native arka anatomi referans olarak tutuldu. Underbust +0.6 cm; chest −0.4, waist −0.4, high hip −0.2, hip −0.1, bicep −0.2, calf −0.2; thigh +0.2 cm. Bunlar solver hedefleridir, fotoğraftan ölçülmüş çevreler değildir. Height kontrolü −0.3 cm. Omuz, ön kol ve boyun çevresi hedefleri değişmedi. Serbest uzunlukların solver kaynaklı değişimleri de aşağıda gösterilir.

| Native parametre | Önceki BodyE | Son aday |
|---|---:|---:|
| Height | 171.75000 | 171.45000 |
| Fat | -0.90000 | -0.90000 |
| Muscularity | 1.00000 | 1.00000 |
| Masculine/Feminine | 0.35000 | 0.35000 |
| Across Shoulder | 29.80000 | 29.80000 |
| Chest | 89.00000 | 88.60000 |
| Underbust | 72.50000 | 73.10000 |
| Waist | 68.30000 | 67.90000 |
| High Hip | 78.00000 | 77.80000 |
| Hip | 93.50000 | 93.40000 |
| Bicep | 27.00000 | 26.80000 |
| Forearm | 21.80000 | 21.80000 |
| Thigh | 51.00000 | 51.20000 |
| Calf | 34.20000 | 34.00000 |
| Neck | 34.80000 | 34.80000 |
| Neck Length | 9.44593 | 9.41467 |
| Neck to Waist | 36.45204 | 36.40238 |
| Inseam | 74.20964 | 73.91662 |
| Upper Arm Length | 31.57521 | 31.47725 |
| Lower Arm Length | 24.96209 | 24.89420 |

Son birleşik mesh yüksekliği **173.36935425 cm**; 173.4 cm hedefinden yaklaşık **0.306 mm** fark. Yalnızca native Height ve yeniden ölçülmüş HeadScale kullanıldı; yüz/uzuvlar sayısal hedefe uymak için ayrı bozulmadı. Native beden exportlarının topoloji/UV düzeni aynı; geometri farkının maksimumu **3.434061 mm**, ortalaması **1.802781 mm**. Bu ölçüm Height değişiminin koordinat etkisini de içerir; yalnızca yerel doku değişimi diye yorumlanmamalıdır.

**Beden görsel değerlendirmesi:** Bel ile alt kaburga arasındaki kontrast hafif arttı; kol/baldır aşırılığı artırılmadı, uyluk doluluğu ve native arka yapı korundu. Beş nötr açı anatomik süreklilik gösteriyor. Referanstaki üst torso genişliği, abdominal geçiş ve pelvis–uyluk kütle dağılımıyla fark sürüyor. Bu kontrollü küçük pass referansa tam benzerlik sağlamadı; BODY PROPORTIONS PARTIAL. Görünmeyen arka anatomi fotoğraftan uydurulmadı.

## Unreal beden deformasyonu

Idle, walk, jog, sprint, crouch, jump, arms raised, arms forward, shoulder rotation, torso twist, hip flexion ve deep knee bend üç açıdan; walk/jog/sprint/jump için iki ek faz: **44 görüntü**. Native body post-process ve face Copy Pose çalıştı. Head-bone eşleşme farkı her örnekte 0.001 cm altında. Kaynak retarget tarifi salt okunur kullanıldı; dört QA kopyası yeni CharacterLab alanına yazıldı.

Ön/yan/arka 3/4 kayıtlarda omuz ve koltuk altı bağlantısı, spine/bel sürekliliği, kalça/uyluk ve diz hacmi korunuyor. Crouch/hip flexion sırasında doğal hacim sıkışması var; büyük yeni yırtık veya çökme görülmedi. Boyun birleşimi pozlarda ayrılmıyor. Güçlü gölge bazı ön bükülme yüzeylerini sınırlar; yan/arka açılarla çapraz kontrol edildi. Sprint yan çekimi düşük ışık yoğunluğuyla ve hip-flexion yan çekimi elleri içeren kadrajla tekrar alındı. Jump %75 örneğinin root Z hareketi karakteri ilk sabit kadrajın altına taşıdı; test aktörünün pelvis yüksekliği yalnızca görünürlük için Z=100 cm seviyesine taşınıp aynı animasyon zamanı yeniden çekildi. İlk başarısız kadraj saklandı. Bu düzeltme root-motion veya iniş/ayak teması doğrulaması değildir.

Kapsam yalnızca kaydedilen LOD0 poz/geçiş örnekleridir. Alt LOD, tüm olası hareketler, cloth/hair, gameplay, ayak teması ve üretim locomotion sertifikasyonu yapılmadı. Engine'in AutoRig sırasında verdiği `PotentialDegenerateTriangles` uyarısı saklandı; Blender nötr testindeki sıfır dejenere sonucuyla aynı kapsam değildir. İşlem başarıyla rig üretti, uyarı genel kalite onayı olarak yok sayılmadı.

## Durma noktası

Yeni sürüm ve kanıtlar korundu; üretim karakterine geçilmedi. Saç/kıyafet/texture üretilmedi, Blender beden sculpt'u yapılmadı. Kalıcı facial corrective ortamı eksikliği ve tabloda belirtilen sanatsal açıklar nedeniyle bütün karakter için genel üretim onayı verilmez. Sonraki kontrollü adım, açık yüz kimliği değerlendirmesi ve desteklenen Expression Editor ortamında kalıcı ifade kalibrasyonudur.

## Karşılaştırma kanıtları

Model panelleri gerçek Blender/Unreal geometri görüntüleridir. Panolar orantılı ölçekleme, kırpma ve etiketleme içerir; geometri görüntüleri rötuşlanmadı. Ana konsept kalibre edilmemiş 3/4 referanstır. Farklı render motorlarının ton/gölge farkını form değişimiyle karıştırmayın. Ham görüntüler yerel kanıt klasöründe korunur.

### FINAL IDENTITY | Previous P2 Blender / new Blender / previous MetaHuman

![FINAL IDENTITY | Previous P2 Blender / new Blender / previous MetaHuman](01_head_multi_view.jpg)

### IDENTITY | Previous P2 / new Blender / new MetaHuman / concept

![IDENTITY | Previous P2 / new Blender / new MetaHuman / concept](02_identity_concept.jpg)

### HEAD-ONLY CONFORM | New Blender / new MetaHuman

![HEAD-ONLY CONFORM | New Blender / new MetaHuman](03_conform.jpg)

### IDENTITY DETAIL | nose_profile

![IDENTITY DETAIL | nose_profile](04_nose_profile.jpg)

### IDENTITY DETAIL | mouth

![IDENTITY DETAIL | mouth](04_mouth.jpg)

### IDENTITY DETAIL | midface

![IDENTITY DETAIL | midface](04_midface.jpg)

### NATIVE BODY | P2 BodyE / regional polish

![NATIVE BODY | P2 BodyE / regional polish](05_body.jpg)

### BODY | Previous / final / body reference / concept

![BODY | Previous / final / body reference / concept](06_body_reference.jpg)

### NATIVE BACK | Previous / final

![NATIVE BACK | Previous / final](07_back.jpg)

### NATIVE RIGLOGIC | Single expressions

![NATIVE RIGLOGIC | Single expressions](08_singles_1.jpg)

### NATIVE RIGLOGIC | Single expressions

![NATIVE RIGLOGIC | Single expressions](08_singles_2.jpg)

### NATIVE RIGLOGIC | Single expressions

![NATIVE RIGLOGIC | Single expressions](08_singles_3.jpg)

### NATIVE RIGLOGIC | Single expressions

![NATIVE RIGLOGIC | Single expressions](08_singles_4.jpg)

### NATIVE RIGLOGIC | Single expressions

![NATIVE RIGLOGIC | Single expressions](08_singles_5.jpg)

### NATIVE RIGLOGIC | Combined expressions

![NATIVE RIGLOGIC | Combined expressions](09_combined_1.jpg)

### NATIVE RIGLOGIC | Combined expressions

![NATIVE RIGLOGIC | Combined expressions](09_combined_2.jpg)

### NATIVE RIGLOGIC | Speech-like endpoints

![NATIVE RIGLOGIC | Speech-like endpoints](10_speech_1.jpg)

### NATIVE RIGLOGIC | Speech-like endpoints

![NATIVE RIGLOGIC | Speech-like endpoints](10_speech_2.jpg)

### MOUTH DEFORMATION | Previous P2 / new neutral geometry

![MOUTH DEFORMATION | Previous P2 / new neutral geometry](11_mouth_before_after.jpg)

### SPEECH TRANSITIONS | Intermediate shapes

![SPEECH TRANSITIONS | Intermediate shapes](12_speech_transitions.jpg)

### NATIVE BODY | Deformation tests

![NATIVE BODY | Deformation tests](13_body_poses_1.jpg)

### NATIVE BODY | Deformation tests

![NATIVE BODY | Deformation tests](13_body_poses_2.jpg)

### NATIVE BODY | Deformation tests

![NATIVE BODY | Deformation tests](13_body_poses_3.jpg)

### NATIVE BODY | Additional movement phases

![NATIVE BODY | Additional movement phases](14_motion_phases.jpg)

### NATIVE BODY | Supplementary pose visibility

![NATIVE BODY | Supplementary pose visibility](14b_pose_details.jpg)

### STRUCTURE | Secondary head sheet / final profile

![STRUCTURE | Secondary head sheet / final profile](15_secondary_structure.jpg)

### Konuşma benzeri geçiş dizisi

30 fps yerel QA animasyonundan 10 fps aralıklarla alınmış gerçek RigLogic görüntüleri; 8 saniye, 81 ön örnek. Sesli diyalog sertifikasyonu değildir. GIF renk paleti sınırlıdır; tam renkli PNG kaynakları yerelde korunur.

![RigLogic geçiş dizisi](speech_transitions.gif)

## Teknik kayıtlar

- [head_validation.json](head_validation.json)
- [v3_change_metrics.json](v3_change_metrics.json)
- [head_fbx_roundtrip.json](head_fbx_roundtrip.json)
- [head_final_conform.json](head_final_conform.json)
- [head_final_scale_decision.json](head_final_scale_decision.json)
- [head_final_deviation.json](head_final_deviation.json)
- [ue_initial_probe.json](ue_initial_probe.json)
- [regional_body_parameters.json](regional_body_parameters.json)
- [native_body_geometry_delta.json](native_body_geometry_delta.json)
- [permanent_corrective_tooling.json](permanent_corrective_tooling.json)
- [permanent_corrective_editor_probe.json](permanent_corrective_editor_probe.json)
- [face_test_plan.json](face_test_plan.json)
- [face_final_raw_tests.json](face_final_raw_tests.json)
- [speech_transition_plan.json](speech_transition_plan.json)
- [speech_transition_tests.json](speech_transition_tests.json)
- [ue_body_validation.json](ue_body_validation.json)
- [ue_qa_retarget_results.json](ue_qa_retarget_results.json)
- [ue_final_asset_audit.json](ue_final_asset_audit.json)
- [ue_production_database_readonly_check.json](ue_production_database_readonly_check.json)
- [preservation_final.json](preservation_final.json)
- [final_review.json](final_review.json)
- [boards_manifest.json](boards_manifest.json)
- [session_closed.json](session_closed.json)
- [body_detail_tests.json](body_detail_tests.json)
- [face_visual_review.json](face_visual_review.json)
- [jump_reframing.json](jump_reframing.json)
- [delivery_hashes.json](delivery_hashes.json)

[Önceki Identity Pass 2 raporu](../character-identity-pass2-2026-09-28/TEKNIK_RAPOR.md)
