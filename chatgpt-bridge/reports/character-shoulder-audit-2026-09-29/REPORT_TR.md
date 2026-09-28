# NativeWorkflow B2 — omuz / trapezius / koltukaltı denetimi

2026-09-29 · UE 5.8.1 · LOD0 · **Sonuç: omuz sorunu çözülmedi. Kabul edilen karakter korundu.**

Tam kaldırmada sivri omuz konturu ve sert trapezius geçişi sürüyor. Bu çalışma bir düzeltme teslimi değildir. Kaynak denetimi, PP ve resmî retarget karşılaştırması, geometri kontrolü ve ayrı native düzeltme hazırlığı yapıldı. Tek test adayının resmî RBF açılımı mevcut Python arayüzünde tamamlanamadığından kullanıcı tarafından istenen güvenli durma koşulu uygulandı.

## Kabul edilen kaynak ve kapsam

Kabul edilen kaynak: `/Game/Sphirus/CharacterLab/NativeBody_20260928/MH_B2_PendingNativeWorkflow`.
Bu B2'nin mevcut yüzü ve oranları esas alındı. Eski yüz hedefleri, Blender, Head/Body Conform, vücut parametre değişiklikleri ve yüz düzenlemesi kullanılmadı.

Kaynak B2, production `MH_MainCharacter`, kabul edilen B2Reload Head ve Body dosyalarının checkpoint kopyaları SHA-256 ile doğrulandı. Dördü de görev sonunda byte düzeyinde aynı. Önceden var olan **22.262 Content dosyasında boyut/zaman damgası değişikliği veya silinme yok**. Bu geniş kapsam kontrolü hash taraması değildir; dört kritik varlık ayrıca hash ile doğrulandı. Yeni 248 dosyanın tamamı yalnız `ShoulderFix_20260928` test klasöründedir.

## Teşhis: doğrulanan mekanizma

Body: 342 kemik, 0 morph target; varsayılan mesh deformer yok. Native `/MetaHumanCharacter/Body/ABP_Body_PostProcess`, DNA RigLogic üzerinden RBF ve swing/twist değerlendirerek yardımcı eklemleri sürüyor; son yüzey skinning ile oluşuyor. Head: 875 kemik ve 858 morph target. Başın body ile ortak eklemleri CopyPose üzerinden takip ediliyor.

| Bölge | Kaynak ağırlıklarında öne çıkan etkiler |
|---|---|
| Deltoid | `upperarm_out`, `clavicle`, `upperarm_twistCor_01`, `upperarm_fwd` |
| Koltukaltı | `spine_04`, `clavicle`, `upperarm_twistCor_01`, `upperarm_fwd` |
| Üst göğüs | `spine_04`, `clavicle_pec` |
| Skapular bölge | `spine_04`, `clavicle_scap`, `upperarm_bck` |
| Üst trapezius / baş yakası | `spine_04`, `clavicle`, `clavicle_out`, `FACIAL_*NeckBackB2` |

Ağırlık bölgeleri anatomik olarak elle segmentlenmiş kesin sınırlar değildir; geniş uzamsal tarama maskeleridir. Ayrıntılı kaynak vertex/weight dökümleri yerel kanıt klasöründe saklandı.

Tam kaldırmada PP ON/OFF karşılaştırması ana clavicle, upperarm, spine_04 ve neck_01 dönüşümlerini aynı tutuyor; yardımcı eklemlerde anlamlı fark oluşuyor:

| Sol yardımcı eklem | ON/OFF konum farkı (mm) |
|---|---:|
| clavicle_out_l | 13.169 |
| clavicle_scap_l | 13.555 |
| upperarm_out_l | 14.870 |
| upperarm_bck_l | 18.528 |
| upperarm_fwd_l | 7.317 |
| upperarm_in_l | 15.123 |
| clavicle_pec_l | 33.682 |
| latissimus_l | 15.709 |

Bu ölçüm native düzeltici eklem hareketinin aktif olduğunu gösteriyor. Body'de morph tabanlı omuz düzeltmesi saptanmadı; ilgili pose-space yanıtı DNA/RBF yardımcı eklemleriyle geliyor. PP aynı deformasyon zincirindeki vertexleri bu eklemler ve skin ağırlıkları üzerinden etkiliyor.

**PP gerçekten kapalıyken de kanat benzeri kontur kalıyor.** Native RetargetComponent + `RTG_MH_IKRig` kontrolü de sorunu kaldırmadı. Aynı tam kaldırma karesinde ana kol açıları direct yolda 158.36° / 157.29°, native retarget yolunda 158.29° / 156.67°. Hareket aralığını düşüren bir çözüm uygulanmadı.

Üst trapezius/yaka yüzeyinin bir kısmı HEAD mesh'ine ait. Head-only ve body-only görüntülerinde ilgili kontur iki yüzeyde de görülüyor. Ortak yardımcı eklemler başta gövdeyle eşleşiyor. Bu yüzden yalnız body ağırlıklarını körlemesine yumuşatmak, bütün bölgeyi veya seam'i güvenle çözmüş sayılmaz.

**Kesinlik sınırı:** temel eklem/skinning ile native pose-corrective yanıtının birleşimi doğrulandı; tek bir hatalı RBF hedefi veya tek bir yanlış skin ağırlığı izole edilmedi. Omuz problemi bir boyun ayrılması olarak teşhis edilmedi.

## Denenen desteklenen yol ve durma nedeni

Tek aday oluşturuldu:
`/Game/Sphirus/CharacterLab/ShoulderFix_20260928/MH_SHOULDER_FIX_NATIVE`

Native body post-process'in proje kopyası:
`/Game/Sphirus/CharacterLab/ShoulderFix_20260928/ABP_ShoulderFixNative_PostProcess`

Amaç native RBF'yi düzenlenebilir PoseAsset/PoseDriver verisine açıp önce eşdeğerliği ölçmekti. Kopyanın editor pipeline BodyProperties alanında RBF açılımı ayarlandı; swing/twist ve finger-half açılımı kapalı tutuldu. Public `BuildMetaHuman` ile Cinematic assembly test alanına üretildi.

Ancak kurulu kaynakta `BuildMetaHuman`, `PipelineOverride` verilmezse yeni varsayılan pipeline kuruyor. Kopyada ayarlanan özel BodyProperties bu çağrıda kullanılmadı. Python'da `PipelineOverride` ayarlama girişimi açıkça **protected and cannot be set** hatası verdi. Sonuç standart RigLogic assembly; **Body/RBF açılmış varlık sayısı 0**. `ASSEMBLY_DISPATCHED` başlangıç kaydı, RBF açılımının başarılı olduğu anlamına gelmez.

Bu nedenle hiçbir corrective hedefi veya skin ağırlığı değiştirilmedi. İkinci LOCAL aday yaratılmadı. Engine/plugin kodu, özel DNA buffer veya korumalı API erişimi değiştirilmedi. Standart assembly bağımlılık kopyaları oluşturdu; yeni saç veya kıyafet tasarımı yapılmadı. Bu assembly kabul edilmiş bir omuz düzeltmesi değildir.

İncelenen kurulu kaynaklar:

- `MetaHumanCharacterEditorSubsystem.cpp`: public BuildMetaHuman varsayılan pipeline seçimi.
- `MetaHumanCharacterBuild.h`: PipelineOverride ve Python erişim sınırı.
- `MetaHumanDefaultEditorPipelineBase.h/.cpp`: BodyProperties ve RBF unpack assembly dalı.
- `MetaHumanRigLogicUnpackLibrary.h/.cpp`: PoseAsset/PoseDriver üretimi; unpack fonksiyonları Python UFUNCTION olarak sunulmuyor.
- `AnimNode_RigLogic.cpp`: DNA neutral/delta yardımcı eklem değerlendirmesi.
- `MetaHumanCharacterEditorActor.cpp`, `RetargetComponent.cpp`: resmî editör animasyon sürme yolu.
- `SkinWeightModifier.h`: desteklenen weight commit davranışı; kullanılmadı.

Sonraki desteklenen adım [ayrı arayüz talimatında](MANUAL_NEXT_STEP.md). UI'da RBF açılması yalnız düzeltme hazırlığıdır; başarı garantisi değildir.

## Omuz QA: kabul edilen B2, düzeltme sonrası değil

Görüntüler gerçek Unreal yakalamalarıdır. Sabit kameralar ve clay gösterim kullanıldı; kaynak materyaller değişmedi. Native ROM gövdeyi de yatırıp döndürür; kamera adları dünya yönünü belirtir. **30–120° örnekleri gövdeye göre ölçülen kol açılarıdır; izole kol abduksiyon merdiveni değildir.** Bu nedenle bunlar tam ROM kabul testi sayılmadı.

| Örnek | Görsel bulgu / sınır | Body koltukaltı alan oranı p99 |
|---|---|---:|
| Nötr A-pose | Kabul edilen biçim ve seam korunuyor | 1.00 |
| ~30° | Belirgin tam-kaldırma kanadı yok; eşlik eden gövde hareketi var | 1.36 |
| ~60° | Omuz geçişi değerlendirildi; bağımsız elevasyon kabulü yapılamaz | 2.72 |
| ~90° | Omuz/koltukaltı gerilimi artıyor; gövde eğimi karşılaştırmayı sınırlıyor | 4.22 |
| ~120° | Gerilme sürüyor; gerçek izole 120° doğrulaması eksik | 5.69 |
| Tam native kaldırma ~157–158° | Sivri yükselen omuz kenarı, sert boyun/trapezius geçişi; FAIL | 6.67 |
| Arms forward | Ön/arka inceleme; koltukaltı gerilimi kalıyor | 4.13 |
| Shoulder rotation | Sert arka trapezius bandı; düzeltme yok | 3.50 |
| Torso twist | Çok açılı tanısal kontrol; düzeltme sonrası regresyon testi değil | 3.42 |
| Crouch | Yeniden kadrajlanan ön/arka görüntüler incelendi | 1.22 |
| Sprint | Geometri ölçüldü; görsel kadraj yetersiz, görsel QA kabul edilmedi | 1.35 |

Alan oranları aynı native nötr üçgene göre deforme alan / nötr alan oranıdır; geniş maskelerdeki p99 değerlerdir. Anatomik doğruluk eşiği değildir. Tam kaldırmada PP OFF koltukaltı p99 6.84, native retarget kontrolünde 6.63; PP'yi kapatmak sorunu çözmüyor. Tam kaldırma body trapezius p99 1.10 olması da sivri konturun görsel olarak kabul edilebilir olduğunu kanıtlamaz.

19 geometri durumunun tamamı sonlu; yeni degenerate üçgen sayısı 0. Bu test alan ölçümüyle normal inversion veya bütün self-intersection'ların yokluğunu kanıtlamaz. Görünen sert katlanmalar/kenarlar devam ettiği için geometri kabulü verilmedi. Ayrı izole internal/external rotation testleri **NOT_RUN**. 180° son nokta ve düzeltme sonrası ROM sürekliliği de doğrulanmadı.

Tam kaldırma ve shoulder rotation için ön, yan, arka, arka 3/4 ve yakın plan yayımlandı. Bütün stres pozlarında eksiksiz üç kamera kabulü sağlanmadı; eksik/boş kadrajlar başarı olarak sunulmadı.

## Koruma ve seam

HeadScale **1.0653988122940063**; kabul edilen ölçülmüş toplam yükseklik **173.2716856 cm**. Tüm mevcut native parametreler aynen kaldı. Kullanıcının son manuel değerleri esas alındı; eski B varsayımlarına geri dönülmedi. Ayrıntılı kayıt [locked_parameters.json](locked_parameters.json).

Kaynak mesh dosyalarının hash'i aynı. Ayrıca kabul edilen dışa aktarım ile yeni nötr CPU-skinned geometri, material/UV eşlemesiyle karşılaştırıldı. Üçgen dizileri aynı. Yeniden çıkarımın çok küçük sayısal kalıntıları aşağıdadır; bunlar sanatsal displacement olarak yorumlanmadı.

| Geometri | Ortalama mm | p95 mm | Maksimum mm |
|---|---:|---:|---:|
| Head | 0.000149171 | 0.000204552 | 0.000333241 |
| Body | 0.000051041 | 0.000153775 | 0.000232822 |

Yüz kimliği için bölge kontrolü (örtüşebilen tarama maskeleri):

| Bölge | Ortalama mm | p95 mm | Maksimum mm |
|---|---:|---:|---:|
| face_identity_combined | 0.000144001 | 0.000204151 | 0.000326557 |
| forehead | 0.000160768 | 0.000220997 | 0.000245930 |
| brow | 0.000151863 | 0.000203016 | 0.000204763 |
| eyelids_orbits | 0.000148424 | 0.000205109 | 0.000244829 |
| nose | 0.000147810 | 0.000205109 | 0.000326418 |
| midface | 0.000178650 | 0.000205023 | 0.000229984 |
| cheeks | 0.000140685 | 0.000197528 | 0.000216633 |
| lips_mouth | 0.000130449 | 0.000197125 | 0.000326557 |
| jaw | 0.000134101 | 0.000197125 | 0.000219656 |
| chin | 0.000120048 | 0.000196966 | 0.000215891 |
| neck_attachment | 0.000107673 | 0.000182511 | 0.000191271 |
| upper_jaw_neck_transition | 0.000121115 | 0.000192099 | 0.000215891 |
| whole_skin_head | 0.000153415 | 0.000206807 | 0.000333241 |

93 tarihsel boundary örneği UV/material eşlemesiyle tekrar ölçüldü. Yeni nötr seam **ortalama 0.000156824 mm**, **maksimum 0.000466448 mm**. Önceki 0.0000915 / 0.0003085 mm ile fark, değişmeyen dosyalardan farklı geometri çıkarımının sayısal hassasiyeti düzeyinde. En kötü pozlu ölçüm 0.000387 mm'nin altında. Görünür açıklık/penetrasyon görülmedi; mevcut anatomik trapezius sırtı bir seam boşluğu değildir. Nicel vertex-normal eşleşmesi ayrıca sertifikalanmadı.

## Persistence ve proje güvenliği

**BODY PERSISTENCE = PASS yalnız değişmeyen kabul edilmiş B2 içindir.** Önceki fresh/reload baş ve gövde karşılaştırmaları 0 mm idi; kaynak hash ve parametreler şimdi de aynı. Başarılı bir kalıcı omuz düzeltmesi oluşmadığından düzeltilmiş rig için save/close/reopen testi yoktur. Bu ayrım yeni test adayına PASS aktarmak için kullanılamaz.

Tanısal aktörlerin bulunduğu geçici sahne bırakıldı; önceki `L_GR_SphirusHouse` dünyası geri açıldı. Son kontrolde dirty Content ve map listeleri boş, native PP geri yüklenmiş ve kaynak/test edit kayıtları kapalı. Map dönüş çağrısı test assembly'nin kopyaladığı ARKit ControlRig/skeleton uyumsuzluğu mesajını verdi; takip kontrolü dünyanın gerçekten geri açıldığını doğruladı. Test assembly üretime uygun ilan edilmedi.

AAMS, Core Motion, locomotion, Pose Search, camera/input, gameplay Blueprint ve production level dosyaları değiştirilmedi. Animasyon klipleri ve ana eklem hareketleri düzenlenmedi. Hareket aralığı azaltılmadı.

## Nihai durum

| Kabul kapısı | Durum |
|---|---|
| BODY PROPORTIONS | PASS — mevcut kabul korunuyor |
| FACE IDENTITY | PRESERVED |
| NEUTRAL HEAD/BODY SEAM | PASS |
| BODY PERSISTENCE | PASS — yalnız kabul edilmiş değişmeyen B2 |
| SHOULDER DEFORMATION | FAIL — sivri form devam ediyor |
| ARMPIT DEFORMATION | PARTIAL — iyileştirme teslim edilmedi |
| BODY DEFORMATION | PARTIAL |
| PRODUCTION CHARACTER MODIFIED | NO |
| READY FOR USER APPROVAL | NO |

**Burada duruldu.** Güvenli desteklenen arayüz adımı tamamlanmadan başka aday, ağırlık müdahalesi veya prosedürel telafi yapılmadı.

## Kanıt dosyaları

[Görsel galeri](README.md) · [Arayüz adımı](MANUAL_NEXT_STEP.md) · [Durum](final_status.json) · [Geometri / seam](geometry_validation.json) · [Yüz koruma](face_geometry_preservation.json) · [Dosya koruma özeti](preservation_summary.json).

Ham kaynak mesh, DNA, ağırlık dizileri, uasset dosyaları ve checkpoint'ler yerel tutuldu. Yayımlananlar yalnız rapor, ölçüm özetleri ve gerçek Unreal QA görüntüleridir. Görsellerdeki clay yüz görünümü yüz/ifade kalite sertifikası değildir.
