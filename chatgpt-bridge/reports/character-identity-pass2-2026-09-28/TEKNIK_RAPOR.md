# Sphirus — Face Identity Pass 2 / Head-Only Re-Conform / Native Body Pass 2

28 Eylül 2026. Önceki başarılı head-only MetaHuman adayından devam edildi. Baş yeniden şekillendirildi ve aynı UV/template yöntemiyle yeni CharacterLab adayına aktarıldı. Native beden için beş parametrik varyant değerlendirildi. Gerçek RigLogic üzerinde tekil ifadeler, birleşimler ve konuşma benzeri pozlar sınandı.

**Bu bir test adayıdır; üretim karakterinin yerine geçirilmedi. Açık kabul kapıları aşağıdadır. Teknik Conform başarısı, konsept benzerliğine veya tüm yüz deformasyonlarına PASS verilmesi anlamına gelmez.**

| Kabul kapısı | Sonuç | Değerlendirme |
|---|---|---|
| FACE SHAPE | **PARTIAL** | Çene genişliği/sertliği azaldı; göz açıklığı ve dudak desteği iyileşti. Burun, ağız ve orta yüzün konsept kimliği henüz yeterince özgül değil. |
| METAHUMAN CONFORM | **PASS** | Yeni yüz UV/template yöntemiyle korunuyor; boyun adaptasyonu ayrı ölçüldü, native birleşim temiz. Bu yalnızca Conform kabulüdür. |
| FACIAL DEFORMATION | **PARTIAL** | RigLogic çalışıyor; funnel/wide ve bazı ağız birleşimlerinde katlanma/sertlik sürüyor. Kalıcı DNA corrective düzenlemesi yapılmadı. |
| BODY PROPORTIONS | **PARTIAL** | Native bel/kol/bacak dengesi ilerledi; referanstaki daha aktif gövde ve uzuv oranları henüz yeterince yakalanmadı. |
| BODY DEFORMATION | **PASS** | Test edilen LOD0 pozları ve hareket fazlarında büyük yeni çökme, yırtılma veya boyun kopması görülmedi; gameplay/ayak teması sertifikasyonu değildir. |

## Koruma ve teslim konumu

Önceki **1474 dosya** ve **86 üretim paketi** SHA-256 ile değişmemiş olarak doğrulandı. **5420 dosyalık** gameplay/ayar envanterinin boyut/zaman damgasında fark yok; bu geniş envanter için hash kontrolü iddia edilmiyor. Orijinal, Pass 1, eski Pass 2, yumuşatma, beden-anatomi ve başarılı head-only sürümleri korunuyor.

- Blender: `SourceAssets/Characters/SphirusIdentityP2_20260928/Sphirus_IdentityP2_EDITABLE.blend`; nötr sürüm `Sphirus_IdentityP2_Neutral.blend`.
- Yeni yüz katmanı: `SPH_Face_Identity_Pass2`. Başlangıç: önceki `Sphirus_FinalHead_EDITABLE.blend / SPH_Final_Head_Identity`.
- Birebir başlangıç yedeği: `CHECKPOINT_PreviousSuccessfulHead.blend`. Bu turun v1, v2, v3 denemeleri de ayrı dosyalardır; teslim edilen sürüm v3'tür.
- Conform girdileri: `HeadTargets/SM_SPH_FinalHead.fbx`, `SM_SPH_FinalLeftEye.fbx`, `SM_SPH_FinalRightEye.fbx`, `SM_SPH_FinalTeeth.fbx`.
- Düzenlenebilir Unreal aday: `/Game/Sphirus/CharacterLab/IdentityP2_20260928/MH_Sphirus_IdentityP2`.
- Son rig'li baş ve beden: `/Game/Sphirus/CharacterLab/IdentityP2_20260928/FinalCandidate/`.
- `BodyA`–`BodyE`, `RiggedV1`, `FinalUnitScale`, `FinalScaledNeutral` ara denemelerdir; son teslim olarak kullanılmamalıdır. Ara beden görüntülerindeki eski rig/boyun birleşimi hataları son adayda yeniden rig üretimiyle giderildi.
- Yüz QA klipleri ve dört ayrı retarget test animasyonu yalnızca yeni `Diagnostics/` klasöründedir. Ana üretim Blueprint'i, üretim skeleton rest matrisleri, AAMS, Core Motion, kamera, input, locomotion veritabanı ve seviye dosyaları değiştirilmedi. Test dünyası geçicidir ve kaydedilmedi.

## Blender yüz değişiklikleri ve görsel değerlendirme

Mandibular köşe ve çene ucu ayrı alanlar halinde daraltılıp yuvarlandı. Yanak/maxilla desteği öne alındı; zygomatik geçişin sertliği azaltıldı. Glabella ve kaş rafı yumuşatıldı. Burun kökü–dorsum ilişkisi, supratip, tip rotasyonu ve alar geçiş yeniden düzenlendi. Dudak kenarları ve perioral desteği, üst/alt dudak yüksekliği ve projeksiyonu ayrı ele alındı. Üst göz kapağının eğriliği ve dikey açıklığı bir miktar geri açıldı; göz küreleri büyütülmedi veya rastgele taşınmadı.

Üç görsel iterasyon yapıldı. İkinci denemenin profilde fazla öne çıkan dudakları üçüncü sürümde azaltıldı; dudak yüksekliği ve köşe desteği korundu. Ön, gerçek yan, iki 3/4 ve tarihçe karşılaştırmaları alındı. Ana bakır saçlı konsept kimlik referansıdır; son eklenen dört yönlü kel baş görseli ikincil yapısal referanstır.

**Görsel sınır:** Yeni alt yüz daha az kare; kapak açıklığı ve yanak desteği daha doğal. Dudaklar önceki hedefe göre hacimli, fakat nötr ağız çizgisi hâlâ sıkı. Burun–orta yüz–ağız ilişkisi ve tüm yüz kimliği ana konseptteki kadını henüz güçlü biçimde tanımlamıyor. Üç iterasyona rağmen genel MetaHuman izlenimi tamamen kalkmadı; FACE SHAPE için PASS verilmedi.

Önceki başa göre maksimum yer değiştirme **4.163321495 mm**, ortalama **0.810890853 mm**; 1 mm üzerinde değişen vertex sayısı **11668**. Bunlar iki mesh arasındaki ölçümlerdir; referans fotoğrafından uydurulmuş anatomik ölçüler değildir.

Blender **BODY değişimi 0 mm**, yeni BODY shape key'i yok. Donmuş beden üretim Body Conform girdisi olarak kullanılmadı. Başın topolojisi, vertex/polygon/loop sırası, UV, ağırlık, kaynak karşılıkları ve eski **864 key** aynen korundu. Mevcut rig rest matrisleri değişmedi. Nötr başta yeni dejenere veya ters dönen üçgen yok. Blender birleşiminde 93 eşleşmenin maksimum farkı **0.000242561 mm**; donmuş Blender karakter yüksekliği **173.40184021 cm**.

Sekiz ham Blender ifade probunda ek ters üçgenler: blink 0, brows up 0, brows down 0, smile **1**, mouth open 0, jaw open 0, purse 0, funnel **3**. Bu sonuç gizlenmedi; eski Blender corrective sisteminin sınırlı probudur, nihai RigLogic onayı değildir. FBX export/reimport parça vertex/topoloji eşleşmesi başarılı; UV farkı **0**; en büyük dünya koordinatı farkı **0.000120722 mm**.

## Aynı head-only MetaHuman yöntemi

UE 5.8.1 / CL 56057345 kurulu araçları kullanıldı. Önceki başarılı aday kopyalandı; üretim karakterine yazılmadı. `MetaHumanCharacterEditorSubsystem.import_from_template` aynı baş + iki göz + diş girdileriyle çalıştırıldı:

- `match_vertices_by_u_vs=True`, `use_eye_meshes=True`, `use_teeth_mesh=True`.
- `alignment_options=ROTATION_TRANSLATION`.
- `isolate_head_from_body=False`: native yerel boyun uyarlaması açık. Çağrı baş-only API'dir; Blender BODY verilmedi, Body Conform yapılmadı.
- HeadScale eşleme öncesinde 1'e alınarak çarpanların birikmesi önlendi. Yeni yüz/boyut yeniden ölçüldü; eski değer otomatik kabul edilmedi.
- Önceki **1.0579111576** yerine son native `HeadScale` **1.0691862106**. `GlobalDelta=1`, `HighFrequencyDelta=0` stratejisi korundu.
- AutoRig **JOINTS_AND_BLEND_SHAPES**: native DNA, RigLogic ve **858 facial morph**. Son parametrik beden seçimi ardından baş tekrar Conform edildi ve rig yeniden üretildi.

**24.408 / 24.408 UV örneği eşleşti.** Yüz bölgesinde yalnızca rijit hizalamayla ortalama fark **0.014792 mm**, p95 **0.015022 mm**, maksimum **0.015380 mm**. Ölçümü iyileştirmek için son çıktıya yeniden ölçek fit edilmedi. Tanısal benzerlik ölçeği yaklaşık 1'dir.

Aynı yüz hizalama çerçevesindeki bölgesel farklar:

| Bölge | Ortalama mm | Maksimum mm |
|---|---:|---:|
| jaw_chin | 0.178228 | 3.049488 |
| nose | 0.014791 | 0.015379 |
| mouth | 0.014779 | 0.015261 |
| eyes_brow | 0.014803 | 0.015380 |
| cheeks | 0.014800 | 0.015380 |
| skull | 0.020587 | 0.059401 |
| neck_adaptation | 9.366071 | 24.360252 |

Çene altındaki en büyük sapma hedef koordinatında yaklaşık (-0,009; -0,065; 1,504) metrededir; boyun adaptasyonuna yakın alt yüz bölgesidir. Burun, ağız, orbit ve yanaklar ayrı ölçüldü. Boyun/omuz tabanı native bedene uyarlandığından bütün baş için tek bir düşük hata sayısı iddia edilmiyor. Nötr native birleşimde 2 mm komşuluğa düşen 93 örneğin en büyük mesafesi **0.000239580 mm**. Bu, yerel en yakın yüzey kontrolüdür; native beden ile Blender bedeninin aynı indekslere sahip olduğu iddiası değildir.

## Gerçek RigLogic ve yüz polish sonucu

**19 tekil durum + 6 birleşik durum + 6 konuşma benzeri durum = 31 durum**, ön ve 3/4 açıdan **62 doğrulanmış görüntü**. Native face post-process ve gerçek animasyon eğrileri kullanıldı; her kayıt istenen kontrol değerleriyle gerçek okunmuş değerlerin eşleşmesini kontrol eder. İlk yakalamada başka editör işlemi değerlendirmeyi geciktirdi; o eksik seri kabul edilmedi ve tamamı yeniden alındı.

Ek olarak 16 köşe/dudak destek denemesi yapıldı. Seçilen ikincil kontroller yeni `AS_IDP2_FacialSupport_Singles_Blends` QA klibine yazıldı; 14 durum iki açıdan tekrar çekildi (**28 görüntü**). Funnel için köşe yuvarlatma ve sınırlı köşe genişliği, wide için köşe daraltma ve dudak kalınlığı, smile için yanak katılımı denendi. **Ana funnel/stretch/pull değerleri azaltılmadı.** İkincil kontrol değerleri `facial_support_plan.json` içindedir.

**Bu bir kalıcı DNA corrective düzeltmesi değildir.** RigLogic DNA'sına expression sculpt yazılmadı, runtime graph'a otomatik bir remap eklenmedi. Destek eğrileri yalnızca bu yeni QA klibinde etkindir. Görsel iyileşme sınırlıdır; ham rig'in sorunları “düzeldi” diye sunulmuyor. Kurulu araçlarda ayrı Expression Editor/Maya ortamı bulunmadığı doğrulandı; destek kontrolleri DNA poz kalibrasyonunun yerine geçmez. Epic'in [Expression Editor](https://dev.epicgames.com/documentation/metahuman/expression-editor) akışı ifade düzeyinde kalibrasyonu destekler; bu turda o DCC aşaması çalıştırılmadı.

| Test | Sonuç | Görsel bulgu / kapsam |
|---|---|---|
| neutral | PASS | Nötr mesh bütün; bu sonuç konsept kimliğine PASS anlamına gelmez. |
| blink | PASS | İki kapak kapanıyor; incelenen ön ve 3/4 görüntülerde büyük katlanma veya açıkta kalan göz küresi yok. |
| blink_left | PASS | Tek taraflı kapanma çalışıyor; karşı göz korunuyor. |
| blink_right | PASS | Tek taraflı kapanma çalışıyor; karşı göz korunuyor. |
| squint | PASS | Kapak/orbit sıkışması okunuyor; büyük yırtılma görülmedi. |
| look_up | PASS | Göz yönü ve kapak takibi test edilen pozda makul. |
| look_down | PASS | Alt kapak gölgesi belirgin; büyük göz küresi penetrasyonu görülmedi. Temas sayısal ölçülmedi. |
| look_left | PASS | Test edilen yatay bakışta büyük kapak sorunu görülmedi. |
| look_right | PASS | Test edilen yatay bakışta büyük kapak sorunu görülmedi. |
| brows_up | PASS | Kaş/alın hareketi çalışıyor; yeni büyük yüzey kırılması yok. |
| brows_down | PASS | Glabella sıkışması mevcut; büyük yüzey kopması yok. |
| smile | PARTIAL | Yanak katılımı var; ağız köşesi çizgisi ve genişleme hâlâ mekanik. İkincil destek sınırlı iyileştiriyor. |
| frown | PASS | Test edilen aşağı köşe hareketinde büyük geometrik hata görülmedi. |
| mouth_open | PASS | Test edilen açıklıkta dudak/çene bağlantısı korunuyor. |
| jaw_open | PASS | Çene açılmasında yüzey sürekliliği korunuyor; üretim konuşma onayı değildir. |
| lip_purse | PARTIAL | Dudak büzülmesi çalışıyor; köşelerde sıkı geçiş sürüyor. |
| lip_funnel | PARTIAL | Perioral halka ve köşe katlanması belirgin. Destek eğrileri ağır katlanmayı tamamen gidermiyor. |
| wide_mouth | PARTIAL | Yatay uzama fazla düz bir bant oluşturuyor; köşe geçişi ve dudak kalınlığı yeterince doğal değil. |
| cheek_raise | PASS | Yanak/alt kapak katılımında büyük yeni hata görülmedi. |
| smile_jaw | PARTIAL | Açılan çene ile gülüş çalışıyor; köşe sertliği devam ediyor. |
| funnel_jaw | PARTIAL | Çene açılmasıyla funnel çevresinde kalın halka ve köşe sıkışması sürüyor. |
| purse_jaw | PARTIAL | Çene/dudak birleşimi yırtılmıyor; köşe ve dudak temasının üretim kalitesi doğrulanmadı. |
| brow_squint | PASS | Birleşik üst yüz pozunda büyük katlanma veya kopma görülmedi. |
| smile_cheek | PARTIAL | Yanak katılımı daha organik; ağız köşelerinin sertliği tamamen çözülmedi. |
| wide_jaw | PARTIAL | Açık ağızda yatay bant etkisi ve köşe sertliği devam ediyor. |
| speech_MBP | PARTIAL | Dudak kapanmasına yaklaşım mevcut; çizgi düzensiz. Tam dudak teması/ara kareler sayısal doğrulanmadı. |
| speech_AH | PASS | Bu temsilî açık ağız pozunda büyük geometrik hata görülmedi. |
| speech_EE | PARTIAL | Yatay ağız şekli düzleşiyor; köşe geçişi üretim kalitesinde değil. |
| speech_OH | PARTIAL | Funnel kaynaklı halka/köşe sıkışması bu birleşime de taşınıyor. |
| speech_OO | PARTIAL | Düşük genlikte daha sakin görünüm; temas ve geçiş sürekliliği tam doğrulanmadı. |
| speech_FV | PARTIAL | Alt dudak/diş ilişkisi temsilî olarak çalıştırıldı; gerçek fonetik diş-dudak teması onaylanmadı. |

**Kalan yüz sorunu:** Funnel köşelerinde ve halka biçiminde perioral kıvrım, wide-mouth pozunda düz bant etkisi, bazı gülüşlerde mekanik köşe hareketi devam ediyor. İkincil native kontrol kalibrasyonu küçük bir iyileşme sağladı; bunu kalıcı rig düzeltmesi olarak sunmuyoruz. Blend geçişleri ve dudak teması tüm karelerde ölçülmedi.

MBP, AH, EE, OH, OO ve FV birleşimleri gerçek rig'de sınandı. Bu, konuşma benzeri poz setidir; sesle eşzamanlı sürekli diyalog, tüm geçiş kareleri, bütün olası kontrol birleşimleri veya alt LOD'lar için sertifikasyon değildir.

## Native MetaHuman Body Pass 2

Başlangıç yeni bir preset değildir: önceki başarılı adayın parametrik bedeni devam ettirildi. A/B denemelerinde Masculine/Feminine +0,55 ve -0,55 karşılaştırıldı; C'de doku/uzuv dengesi, D'de fazla sabitlenmiş uzunlukların serbest bırakılması, E'de daha aktif native form denendi. Seçilen E varyantında **Masculine/Feminine +0,35**, **Fat -0,90**, **Muscularity +1,00**. Bu sayılar model koordinatlarıdır; biyolojik cinsiyet oranı, yağ yüzdesi veya kas kütlesi yüzdesi değildir.

Önce geniş kontroller, ardından bölgesel çevreler düzenlendi. Önceki çok sayıdaki uzunluk kilidi serbest bırakıldı; bağlı ölçülerin doğal biçimde çözülmesine izin verildi. Bu sıra [Epic Body Params](https://dev.epicgames.com/documentation/metahuman/metahuman-creator-body-params-tool-in-unreal-engine) aracının bağlı parametre davranışıyla uyumludur. Beden üzerinde Blender sculpt'u veya yeni custom body mesh yapılmadı.

| Native ölçü / kontrol | Önceki değer | Son değer |
|---|---:|---:|
| Height | 171.75000 | 171.75000 |
| Fat | 0.30000 | -0.90000 |
| Muscularity | -0.75000 | 1.00000 |
| Masculine/Feminine | 0.03127 | 0.35000 |
| Across Shoulder | 29.80000 | 29.80000 |
| Chest | 88.50000 | 89.00000 |
| Underbust | 73.00000 | 72.50000 |
| Waist | 69.80000 | 68.30000 |
| High Hip | 79.00000 | 78.00000 |
| Hip | 93.50000 | 93.50000 |
| Bicep | 26.50000 | 27.00000 |
| Forearm | 21.50000 | 21.80000 |
| Thigh | 49.00000 | 51.00000 |
| Calf | 33.30000 | 34.20000 |
| Neck | 35.62338 | 34.80000 |
| Neck Length | 8.29430 | 9.44593 |
| Neck to Waist | 35.88547 | 36.45204 |
| Inseam | 73.53788 | 74.20964 |
| Upper Arm Length | 31.83609 | 31.57521 |
| Lower Arm Length | 25.16401 | 24.96209 |

Tablodaki değerler native constraint okumasıdır; fotoğraf üzerinde kesin antropometrik ölçü alındığı anlamına gelmez. Serbest/pinli durumların tamamı JSON'dadır. Native dışa aktarımların topoloji ve UV düzeni aynı; bedenler arası en büyük geometri farkı **18,440985 mm**, ortalama **4,545762 mm**. Kaynak fotoğraftaki sütyen desteği kopyalanmadı; görünmeyen sırt anatomisi native modelden korundu.

Son baş + bedenin gerçek mesh yüksekliği **173.69676208 cm**. Önceki başarılı MetaHuman **173,41867065 cm** idi; yeni sonuç yaklaşık 173,4 cm hedefinden **2,968 mm** uzun. Yüzü sıkıştırarak hedef sayıya zorlamak yerine bu küçük fark kaydedildi. Blender'ın donmuş kaynak yüksekliği değişmedi.

**Beden görsel değerlendirmesi:** Beş native varyant içinden seçilen E, bel/üst kalça geçişini belirginleştiriyor ve kol-uyluk-baldır hacmini daha aktif bir dengeye taşıyor. Ön/yan/arka ve iki 3/4 görünüşte native sırt anatomisi bütün. Ancak gövde ve uzuvların genel yumuşaklığı, referansın daha belirgin ribcage/waist/limb ilişkisine hâlâ tam yaklaşmıyor. Bu nedenle referans eşleşmesi PARTIAL; native anatominin çalışması tek başına sanat kabulü değil.

## Unreal beden deformasyonu

Idle, walk, jog, sprint, crouch, jump, arms raised, arms forward, shoulder rotation, torso twist, hip flexion, deep knee bend: **12 poz × 3 açı**, ayrıca walk/jog/sprint/jump için sekiz faz örneği, toplam **44 görüntü**. Native body post-process ve native Face Copy Pose kullanıldı. Doğrudan uyumlu native kliplerin yanında jog/sprint/crouch/jump için mevcut retarget tarifi salt okunarak yeni QA kopyaları üretildi; kaynak tarif/animasyon değişmedi.

44 ana görüntünün tamamı incelendi. Sprint yan görünüşündeki parlaklığı ve kalça bükülmesindeki el kadrajını açıklığa kavuşturan iki ek görüntü daha alındı (toplam 46). Bu ikisinde yalnızca geçici QA ışık şiddeti/kadraj değişti; pozlar aynı kaldı. Büyük yeni yırtılma, pelvis/diz çökmesi veya baş-boyun kopması görülmedi. Sıkışmış koltukaltı/torso temas bölgeleri görsel olarak kontrol edildi; tüm yüzeyler için çarpışma çözümü veya üretim locomotion doğrulaması yapılmadı.

Baş/beden head-bone konumu tüm kayıtlarda 0,001 cm toleransı içinde. Birleşim nötr ve hareket görüntülerinde görsel kontrol edildi. Bu kemik konumu testi tek başına tüm cilt vertex'lerinin çakışma testi değildir. Omuz, koltukaltı, gövde, bel, sırt, pelvis, kalça, uyluk, diz ve boyun görüntüleri incelendi. Gerçek gameplay locomotion kalitesi, kök hareketi/ayak teması, çarpışma veya tüm LOD'lar için PASS iddiası yoktur.

## Açık kalanlar ve durdurulan kapsam

Yüz kimliği, bazı ağız deformasyonları ve bedenin tam referans eşleşmesi açık. Üretime geçiş için yüzün konsept kimliği üzerinde daha nitelikli form değerlendirmesi, expression düzeyinde kalıcı corrective kalibrasyonu ve sürekli konuşma/temas testi gerekiyor. Native bedenin parametre eşleşmesi de henüz final sanat kabulü almıyor. Yeni aday korunmuş bir çalışma sonucudur; üretim karakterini değiştirmek için onaylanmış final değildir.

Yeni üretim saç/Groom, kıyafet, cilt detayı, materyal/texture üretimi veya gameplay değişikliği yapılmadı. Önceki tüm kaynaklar ve başarılı aday geri alınabilir durumda. Yeni aday ve QA kanıtları yayımlanıyor; açık kapılar kapanmış gibi genel bir “tamamlandı” onayı verilmiyor.


## Karşılaştırma kanıtları

Tüm model panelleri gerçek Blender veya Unreal geometri görüntüleridir. Referanslar kullanıcının sağladığı görsellerdir. Panolar yalnızca yerleştirme, orantılı ölçekleme, kırpma ve etiketleme içerir; geometri görüntüleri üretilmedi veya rötuşlanmadı. Blender ve Unreal ışık motorları farklıdır; yüz tonu/gölge değişimini şekil değişimiyle karıştırmayın. Tam ham görüntüler yerel doğrulama klasöründe korunuyor. Beden pozlarının boş siyah kenarları okunabilirlik için kırpıldı; poz panelleri ölçek ölçümü amacı taşımaz.

### FACE IDENTITY PASS 2 | Previous accepted target / new target

![FACE IDENTITY PASS 2 | Previous accepted target / new target](01_blender_identity.jpg)

### HEAD | Preserved identity history

![HEAD | Preserved identity history](02_face_history.jpg)

### HEAD-ONLY CONFORM | New Blender target / native MetaHuman

![HEAD-ONLY CONFORM | New Blender target / native MetaHuman](03_blender_conformed.jpg)

### FACE IDENTITY | Previous MetaHuman / new MetaHuman / concept

![FACE IDENTITY | Previous MetaHuman / new MetaHuman / concept](04_primary_concept.jpg)

### NEW METAHUMAN | Four neutral clay views

![NEW METAHUMAN | Four neutral clay views](05_new_head_views.jpg)

### NATIVE BODY PASS 2 | Previous / selected parametric result

![NATIVE BODY PASS 2 | Previous / selected parametric result](06_native_body.jpg)

### BODY | Previous / new / supplied body reference / concept

![BODY | Previous / new / supplied body reference / concept](07_body_reference.jpg)

### NATIVE BACK | Preserve anatomical coherence

![NATIVE BACK | Preserve anatomical coherence](08_native_back.jpg)

### NATIVE TORSO | Shoulder, ribcage, waist, pelvis

![NATIVE TORSO | Shoulder, ribcage, waist, pelvis](09_torso.jpg)

### RIGLOGIC | All single-expression probes

![RIGLOGIC | All single-expression probes](10_singles_1.jpg)

### RIGLOGIC | All single-expression probes

![RIGLOGIC | All single-expression probes](10_singles_2.jpg)

### RIGLOGIC | All single-expression probes

![RIGLOGIC | All single-expression probes](10_singles_3.jpg)

### RIGLOGIC | All single-expression probes

![RIGLOGIC | All single-expression probes](10_singles_4.jpg)

### RIGLOGIC | All single-expression probes

![RIGLOGIC | All single-expression probes](10_singles_5.jpg)

### RIGLOGIC | Combined expression probes

![RIGLOGIC | Combined expression probes](11_combined_1.jpg)

### RIGLOGIC | Combined expression probes

![RIGLOGIC | Combined expression probes](11_combined_2.jpg)

### RIGLOGIC | Speech-like blends

![RIGLOGIC | Speech-like blends](12_speech_1.jpg)

### RIGLOGIC | Speech-like blends

![RIGLOGIC | Speech-like blends](12_speech_2.jpg)

### MOUTH SUPPORT | Raw / secondary native-control calibration

![MOUTH SUPPORT | Raw / secondary native-control calibration](13_support_1.jpg)

### MOUTH SUPPORT | Raw / secondary native-control calibration

![MOUTH SUPPORT | Raw / secondary native-control calibration](13_support_2.jpg)

### UNREAL BODY | Real deformation probes

![UNREAL BODY | Real deformation probes](14_body_poses_1.jpg)

### UNREAL BODY | Real deformation probes

![UNREAL BODY | Real deformation probes](14_body_poses_2.jpg)

### UNREAL BODY | Real deformation probes

![UNREAL BODY | Real deformation probes](14_body_poses_3.jpg)

### UNREAL BODY | Additional motion-phase samples

![UNREAL BODY | Additional motion-phase samples](15_motion_samples.jpg)

### HEAD | Supplied four-view reference and final profile

![HEAD | Supplied four-view reference and final profile](16_secondary_head.jpg)

### BODY DETAILS | Supplemental side views

![BODY DETAILS | Supplemental side views](17_pose_detail.jpg)

## Teknik kayıtlar

- [head_validation.json](head_validation.json)
- [v3_change_metrics.json](v3_change_metrics.json)
- [head_fbx_roundtrip.json](head_fbx_roundtrip.json)
- [head_final_conform.json](head_final_conform.json)
- [head_final_scale_decision.json](head_final_scale_decision.json)
- [head_final_deviation.json](head_final_deviation.json)
- [ue_initial_probe.json](ue_initial_probe.json)
- [BodyA_parameters.json](BodyA_parameters.json)
- [BodyB_parameters.json](BodyB_parameters.json)
- [BodyC_parameters.json](BodyC_parameters.json)
- [BodyD_parameters.json](BodyD_parameters.json)
- [BodyE_parameters.json](BodyE_parameters.json)
- [native_body_geometry_delta.json](native_body_geometry_delta.json)
- [face_test_plan.json](face_test_plan.json)
- [face_final_raw_tests.json](face_final_raw_tests.json)
- [facial_support_plan.json](facial_support_plan.json)
- [face_final_support_tests.json](face_final_support_tests.json)
- [mouth_probe_plan.json](mouth_probe_plan.json)
- [mouth_probe2_plan.json](mouth_probe2_plan.json)
- [ue_body_validation.json](ue_body_validation.json)
- [body_detail_tests.json](body_detail_tests.json)
- [ue_qa_retarget_results.json](ue_qa_retarget_results.json)
- [ue_final_asset_audit.json](ue_final_asset_audit.json)
- [ue_production_database_readonly_check.json](ue_production_database_readonly_check.json)
- [preservation_final.json](preservation_final.json)
- [final_review.json](final_review.json)
- [boards_manifest.json](boards_manifest.json)
- [session_closed.json](session_closed.json)
- [delivery_hashes.json](delivery_hashes.json)

[Önceki başarılı head-only MetaHuman raporu](../character-head-metahuman-2026-09-28/TEKNIK_RAPOR.md)
