# NativeWorkflow B2 — vücut oranları ve deformasyon incelemesi

NativeWorkflow'daki mevcut kullanıcı yüzü korunarak vücut incelemesi yapıldı. Mevcut kullanıcı düzenlemeli B2 oranları korundu; yeni vücut veya yüz varyantı oluşturulmadı. **Vücut oranları PASS; vücut deformasyonu PARTIAL.** Tam kol kaldırma pozundaki sert omuz geçişi nedeniyle üretim kalitesi bütünüyle onaylanmadı.

## Kabul edilen kimlik ve kapsam

Kaynak: `/Game/Sphirus/CharacterLab/NativeBody_20260928/MH_B2_PendingNativeWorkflow`.

Son kullanıcı talimatı, **bu NativeWorkflow yüzünü** yeni kimlik başlangıcı olarak kabul ediyor. Eski orijinal yüzle önceki fark ölçümleri silinmedi veya PASS olarak yeniden yazılmadı. Bu rapordaki PRESERVED, kabul edilmiş mevcut NativeWorkflow'a göre korunmayı ifade eder; eski orijinalle aynılık iddiası değildir.

Önceki kullanıcı adımları Full Rig → kaydet → yeniden aç idi. Önceki doğrulamadaki B2Fresh/B2Reload geometri eşitliği, mevcut dosya hash'i ve bu turdaki parametre okumasıyla ilişkilendirildi. Bu turda Remove Rig, rig yeniden üretimi, Conform veya body solver çalıştırılmadı.

## Son durum

| Kontrol | Sonuç |
|---|---|
| FACE IDENTITY | PRESERVED — kabul edilmiş NativeWorkflow'a göre |
| BODY PROPORTIONS | PASS — mevcut kullanıcı düzenlemeli B2 korundu |
| NEUTRAL HEAD/BODY SEAM | PASS |
| TESTED POSE SEAM | PASS — yalnız ölçülen LOD0 pozları |
| BODY PERSISTENCE | PASS — önceki fresh/reload kanıtı + aynı kaynak ve parametreler |
| BODY DEFORMATION | PARTIAL — aşırı omuz pozlarında form kalitesi |
| FACIAL DEFORMATION | NOT_RUN |
| SELECTED BODY | B2 — mevcut NativeWorkflow |
| READY FOR USER APPROVAL | NO — tüm deformasyon kalitesi için nihai üretim onayı verilmedi |
| PRODUCTION CHARACTER MODIFIED | NO |

Kanıtlar incelemeye hazır. Sonuç CharacterLab'da kaldı. Oyun karakterine aktarılmadı.

## Vücut oranları

[Beş açıdan mevcut vücut](boards/01_current_native_body.jpg): ön, yan, arka, ön 3/4, arka 3/4. Mevcut baş takılıdır.

Omuzlar başı yeterli biçimde destekliyor. Üst kol/önkol/el ilişkisi makul; el büyütme ihtiyacı görülmedi. Bel tanımlı, pelvis ve uyluk hacmiyle geçişi tutarlı. Omuz/kalça ve gövde/bacak ilişkisi yetişkin kadın anatomisi içinde makul. Sırtın doğal MetaHuman yapısı korundu. Bu değerlendirme yeni bir B/B2 üstünlük deneyi değildir: kullanıcı tarafından sonradan düzenlenen mevcut B2, son talimatla inceleme başlangıcı seçildi.

Toplam gerçek mesh yüksekliği **173.271685600 cm**. Native Height kontrolünün değeri 172.276336670; bu kontrol değeri toplam başlı mesh yüksekliğiyle aynı değildir. HeadScale **1.0653988122940063**, değişmedi.

Bu turdaki parametre değişiklikleri: **0**. Aşağıdaki değerler kullanıcı tarafından kaydedilmiş mevcut durumun tam okumasıdır. Eski B2 niyetinden farklı değerler bu turda solver değişikliği olarak sunulmuyor.

| Native kontrol | Mevcut değer (ölçüler cm) | Aktif |
|---|---:|---|
| Height | 172.276336670 | Evet |
| Chest | 87.794998169 | Evet |
| Bust Span | 24.373832703 | Evet |
| Underbust | 72.000000000 | Evet |
| Waist | 69.750000000 | Evet |
| Rise | 77.948295593 | Hayır |
| Inseam | 73.537879944 | Evet |
| Hip | 94.000000000 | Evet |
| High Hip | 78.500000000 | Evet |
| Neck Base | 31.854972839 | Evet |
| Neck | 35.623378754 | Evet |
| Thigh | 49.000000000 | Evet |
| Knee | 32.306930542 | Evet |
| Calf | 33.000000000 | Evet |
| Front Interscye Length | 32.392608643 | Evet |
| Upper Arm Length | 31.836093903 | Evet |
| Lower Arm Length | 26.921340942 | Evet |
| Bicep | 28.282756805 | Evet |
| Elbow | 20.814056396 | Evet |
| Wrist | 13.118677139 | Evet |
| Neck to Waist | 35.885467529 | Evet |
| Across Shoulder | 30.149999619 | Evet |
| Shoulder Height | 147.223785400 | Hayır |
| Shoulder to Apex | 26.096359253 | Evet |
| Neck Length | 8.294302940 | Evet |
| Forearm | 21.350000381 | Evet |
| Hand Circumference | 19.127319336 | Evet |
| Fat | -0.836524010 | Evet |
| Masculine/Feminine | 0.007542372 | Evet |
| Muscularity | -0.483775139 | Evet |

## Yüz ve teknik korunma

[Mevcut kabul edilmiş yüz — dört açı](boards/accepted_current_face.jpg).

Kaynak karakter dosyası byte düzeyinde aynı. Face katsayıları, HeadScale ve bütün native vücut kontrol değerleri başlangıçla aynı. Ölçüm ayrıca gerçek LOD0 mesh pozisyonları üzerinden yapıldı; DNA hash'i tek başına kanıt olarak kullanılmadı.

Geometri karşılaştırması: kabul edilen B2Reload render mesh'i → bu turun son nötr CPU-skinned mesh'i. Material + UV örnek eşleşmesi; aynı uzay/transform, ölçek veya rigid düzeltme gerekmiyor. Head 34,343 ve body 32,334 UV örneği. Head en büyük sayısal fark 0.000310210 mm, body 0.000232822 mm. Bunlar kayan noktalı render okuma farklarıdır; sanatsal geometri düzenlemesi değildir.

| Bölge | Örnek | Ortalama mm | P95 mm | Maks mm |
|---|---:|---:|---:|---:|
| face_identity_combined | 15835 | 0.000117 | 0.000156 | 0.000307 |
| forehead | 881 | 0.000118 | 0.000161 | 0.000310 |
| brow | 655 | 0.000099 | 0.000156 | 0.000157 |
| eyelids_orbits | 3522 | 0.000120 | 0.000158 | 0.000305 |
| nose | 3540 | 0.000103 | 0.000155 | 0.000160 |
| midface | 486 | 0.000071 | 0.000154 | 0.000155 |
| cheeks | 2001 | 0.000129 | 0.000158 | 0.000305 |
| lips_mouth | 4619 | 0.000128 | 0.000155 | 0.000162 |
| jaw | 723 | 0.000134 | 0.000158 | 0.000162 |
| chin | 628 | 0.000134 | 0.000156 | 0.000158 |
| neck_attachment | 1784 | 0.000033 | 0.000154 | 0.000157 |
| upper_jaw_neck_transition | 834 | 0.000099 | 0.000156 | 0.000158 |
| whole_skin_head | 24408 | 0.000093 | 0.000156 | 0.000310 |

Bölge maskeleri önceki çalışmadaki örtüşen uzamsal tarama maskeleridir, kesin anatomik segmentasyon değildir. Kaynak asset değişmediği için topoloji, UV, ağırlık, rest matrisleri, DNA ve mevcut shape/morph verileri bu turda korunmuştur. Teşhis mesh'inde üçgen indeksleri ve UV örnekleri ayrıca aynı bulundu.

## Boyun birleşimi ve kalıcılık

Önceden izlenen **93 sınır örneği** kullanıldı. Son nötr ölçüm ortalama **0.000091516 mm**, maksimum **0.000308510 mm**. 12 pozdaki en büyük mesafe **0.000386474 mm** (sprint). Görsel boyun açıklığı/penetrasyonu saptanmadı.

Nötr, kollar yukarı, kollar öne, omuz rotasyonu ve derin çömelmede normal karşılaştırması da yapıldı; en büyük sınır normal açısı **0.000001479°**. Bu sayısal süreklilik omuzun tüm anatomik formunun kusursuz olduğunu göstermez.

Önceki fresh/reload karşılaştırmasında hem head hem body pozisyon farkı **0 mm**; üçgenler, UV, loop normalleri ve material indeksleri birebir aynıydı. Parametreler ve rig verileri de kalmıştı (head 875 bone/858 morph; body 342 bone/0 morph). Bu turda aynı B2 dosyası kullanıldı ve parametreler değişmeden tekrar okundu. Yeni bir body edit/save/rebuild döngüsü yapıldığı iddia edilmiyor.

## Gerçek native deformasyon testi

Kaynak mesh'ler doğrulanmış B2Reload Full Rig çıktılarıdır. Head, body'ye component olarak bağlı; native ABP_Face Copy Pose ve native Body/Face PostProcess animasyonları kullanıldı. LOD0 zorlandı. Geometri, Unreal `GetCPUSkinnedVertices` yolunu kullanan GeometryScript component okumasından alındı. Çevrimdışı uydurma skinning kullanılmadı.

Her ana poz ön, yan, arka 3/4 açıdan incelendi. Kol kaldırma, öne uzatma ve omuz rotasyonu için ek yakın planlar var. Kamera ve ışıklar bir pozun karşılaştırmalı görüntülerinde aynı; tam gövde kadrajı için bazı pozların merkez/FOV'u ayrıca ayarlandı. Kamera değerleri her görüntünün JSON dosyasında kayıtlı.

| Poz | Klip zamanı s | Birleşim ort/maks mm | Görsel bulgu |
|---|---:|---:|---|
| idle | 0.50 | 0.000172 / 0.000323 | Belirgin yeni çökme veya birleşim açılması görülmedi. |
| walk | 0.50 | 0.000164 / 0.000341 | Ana poz ve iki ek döngü örneğinde gövde/pelvis bağlantısı tutarlı. |
| jog | 0.25 | 0.000173 / 0.000345 | Ana poz ve iki ek örnekte omuz, bel ve kalça bağlantısı tutarlı. |
| sprint | 0.50 | 0.000192 / 0.000386 | Ana poz ve iki ek örnekte kopma görülmedi; hareket/ayak teması sertifikasyonu değildir. |
| crouch | 1.00 | 0.000151 / 0.000362 | Ön, yan ve arka 3/4 görünüşte diz/kalça sürekliliği kabul edilebilir. |
| jump | 0.65 | 0.000202 / 0.000342 | Ana poz üç açıdan tam kadrajla incelendi. Ek 1.0 s karesinde baş üstü kadraj dışında; bu ek kare baş değerlendirmesinde kullanılmadı. |
| arms_raised | 16.20 | 0.000167 / 0.000346 | PARTIAL: omuz üstü / trapez-üst göğüs geçişi sert, kanat benzeri çıkıntı yapıyor. Yırtık veya boyun açıklığı değil. |
| arms_forward | 21.50 | 0.000161 / 0.000331 | Kollar öne uzanmış gerçek ROM pozu (21.5 s); ön/yan/arka 3/4, omuz ve sırt yakın planları incelendi. |
| shoulder_rotation | 26.00 | 0.000189 / 0.000359 | PARTIAL: arka boyun/trapezde düzlemsel bant hissi. Sınır pozisyonu ve normalleri uyuşuyor; yüzey formu kalite sınırı. |
| torso_twist | 24.50 | 0.000162 / 0.000346 | Bel, kaburga ve pelvis sürekliliğinde belirgin yeni kopma/çökme görülmedi. |
| hip_flexion | 15.00 | 0.000157 / 0.000337 | Derin gövde/kalça fleksiyonunda ön/yan/arka 3/4 incelendi; birleşim temiz. |
| deep_squat | 0.50 | 0.000157 / 0.000317 | Gerçek derin çömelme; diz ve kalça yüksek fleksiyonda. Görünür büyük yırtık, kopma veya pelvis çökmesi yok. |

Tüm 12 ana pozda sonlu mesh koordinatları ve **0 yeni dejenere üçgen**. Alan oranı testi öz-kesişme olmadığını ispatlamaz. Dark/clay görüntüler ince kırışıklık değerlendirmesini sınırlıyor. Bu, LOD0 seçilmiş poz ve birkaç döngü örneği taramasıdır; tam klip blend'leri, daha düşük LOD'lar, cloth, collision, ayak teması, locomotion veya gameplay sertifikasyonu değildir.

## Gerçek derin çömelme

[Üç açıdan derin çömelme](boards/13_deep_squat.jpg). Diz fleksiyonu sol **145.376°**, sağ **144.580°**; kalça sol **106.299°**, sağ **107.239°**. Bunlar kemik segmentlerinden hesaplanan QA açılarıdır.

Yeni teşhis animasyonu: `/Game/Sphirus/CharacterLab/NativeWorkflowQA_20260928/QA_DeepSquat`. Public AnimationDataController ile native ROM tabanlı sabit QA pozu oluşturuldu. Klip retarget source asset'i kabul edilmiş body mesh'iyle eşleştirildi; böylece teşhis klibinin ikinci kez uzunluk uyarlaması yapması düzeltildi. Karakter iskelet/rest matrislerine dokunulmadı. Poz fiziksel denge veya oyun animasyonu olarak onaylanmadı.

## Açık deformasyon sorunu

[Omuz yakın planları](boards/detail_arms_raised.jpg) ve [PostProcess karşılaştırması](boards/diagnostic_postprocess.jpg).

Tam kol kaldırmada omuz üstünde sert, sivri bir hacim geçişi kalıyor. Omuz rotasyonunda arka boyun/trapez bölgesinde de düzlemsel bir bant hissi var. Sınır pozisyonları ve normalleri uyumlu; sorun salt head/body açıklığı değil.

Native Body PostProcess yalnız geçici test component'inde `disable_post_process_blueprint=True` ile gerçekten kapatılarak kontrol edildi. Sert omuz konturu yine kalıyor; göğüs ve koltuk altı biçimi de değişiyor. **PostProcess kapatmak üretim çözümü olarak uygulanmadı**, bitişte tekrar etkin olduğu doğrulandı. İlk `override=None` denemesi sistemi gerçekten kapatmadığı için OFF kanıtı sayılmadı; galeride yalnız doğrulanmış ON/OFF çifti kullanıldı.

Bu test tek başına hatayı belirli bir ağırlık/bone/corrective'ye bağlamaz. Tam kaldırma formu için desteklenen native düzeltme/rig incelemesi gerekiyor. Bu turda unsupported DNA, plugin patch, elle kaynak ağırlık değişikliği veya ifadeleri zayıflatma yapılmadı. Bu bulgu giderilmeden BODY DEFORMATION tam PASS değildir.

## Korunan dosyalar ve kapanış

- `Content\Character\MainCharacter\MH_MainCharacter.uasset` — SHA256 `45d4d909ff9e8b49765ca14f56634e9044c1a6df250b2547993778562943c705` — değişmedi.
- `Content\Sphirus\CharacterLab\NativeBody_20260928\MH_B_SlightlyActive.uasset` — SHA256 `f77fac5a96ef777b74aeaf50a4eaa2c7c156049d0a43e91c226a1bfc07a5e442` — değişmedi.
- `Content\Sphirus\CharacterLab\NativeBody_20260928\MH_B2_PendingNativeWorkflow.uasset` — SHA256 `59d604a404ba5b9840a7c684f48ae6e8f5e3eaf8bfb8df4e8a1aaf98fefa2fa7` — değişmedi.

Önceden var olan **22,261 Content dosyasının** boyut/mtime karşılaştırmasında değişiklik veya silinme yok. Tek yeni Content asset'i QA_DeepSquat. Checkpoint kopyaları hash ile doğrulandı. Eski denemeler silinmedi; henüz üretime onaylı bir son karaktere geçiş yapılmadı.

Geçici QA level kaydedilmedi. Önceki `L_GR_SphirusHouse` yeniden açıldı; dirty content/map listeleri boş. Level, camera, locomotion, AAMS, Core Motion, PoseSearch, input ve üretim Blueprint'lerine dokunulmadı. Blender, Body Conform, Head Conform, saç, kıyafet ve yüz ifadesi düzeltmesi yapılmadı.

## Kanıt dosyaları

- [Görsel galeri](README.md)
- [Makine tarafından okunabilir son durum](final_status.json)
- [Bölgesel yüz korunma ölçümü](accepted_face_geometry_preservation.json)
- [Poz geometri ölçümleri](posed_geometry_validation.json)
- [Tam native parametreler ve son editör durumu](final_editor_state.json)
- [Hash ve dosya korunma denetimi](final_preservation.json)
- [Animasyon kaynakları ve zamanları](final_pose_plan.json)
- [Önceki kalıcılık ölçümleri](persistence_evidence.json)
