# B → B2: native beden kalıcılığı ve yüz koruma denetimi

**Sonuç: teknik engel nedeniyle karakter düzenlemesi durduruldu. B2 uygulanmadı; final karakter terfi ettirilmedi.** B / SlightlyActive sanatsal beden tabanı olarak tutuluyor. Kullanıcının özgün MetaHuman karakteri, yüzü ve B dosyası değiştirilmedi.

Bu rapor yeni bir başarılı beden sonucu değildir. Kurulu **UE 5.8.1-56057345** kaynak kodu, canlı Python API erişimi ve önceki ölçüm kayıtları incelendi. Kullanıcının “gerekli desteklenen işlem otomasyondan erişilemiyorsa dur ve manuel UI adımını bildir” koşulu işletildi.

## 1. Korunan varlıklar

- Özgün karakter: `/Game/Character/MainCharacter/MH_MainCharacter`.
- B: `/Game/Sphirus/CharacterLab/NativeBody_20260928/MH_B_SlightlyActive`.
- Yeni çalışma/evidence klasörü: `Saved/Codex/CharacterNativeBodyB2_20260928`.
- B için yeni dosya checkpoint'i alındı; kaynak ve kopyanın SHA256 değerleri eşit.
- Özgün karakterin önceki tam checkpoint'i tekrar doğrulandı; kaynakla byte düzeyinde eşit.
- Karakter paketlerine edit/save/delete işlemi yapılmadı. Yeni B2 `.uasset` oluşturulmadı.
- CharacterLab dışındaki 22.178 mevcut Content dosyasının boyut/zaman kayıtlarında fark bulunmadı. Canlı editörde dirty Content listesi boş. Yalnız önceden var olan geçici QA dünyası dirty.
- Engine/plugin kaynakları yalnız okundu. Gameplay, locomotion, kamera, input, animasyon veritabanları ve seviyeler değiştirilmedi.

[Koruma kanıtı](preservation.json), [canlı API denetimi](live_api_audit.json).

Bu dosya eşitliği özgün varlığın korunduğunu gösterir. **Yeniden üretilmiş bir B2 başının aynı kaldığını göstermez; böyle bir baş bu turda üretilmedi.**

## 2. B2 ölçü planı — UYGULANMADI

Tek bir B2 için önerilen dört küçük değişiklik:

| Native kısıt | B hedefi (cm) | B2 planı (cm) | Fark |
|---|---:|---:|---:|
| Across Shoulder | 29,50 | 30,15 | +0,65 |
| Bicep | 26,50 | 27,00 | +0,50 |
| Forearm | 21,00 | 21,35 | +0,35 |
| Waist | 69,00 | 69,75 | +0,75 |

B'nin Chest 88,3; Underbust 72; High Hip 78,5; Hip 94; Thigh 49; Calf 33 değerleri korunacak. Fat 0,05; Muscularity −0,25; Masculine/Feminine 0,15 sabit kalacak. Eller, uzuv/torso/boyun uzunlukları ve HeadScale değiştirilmeyecek. HeadScale mevcut değeri **1,0653988122940063**.

[B'nin kaydedilmiş 30 kısıtı ve B2 planı](B2_PARAMETER_PLAN_NOT_APPLIED.json) aktif bayraklarını da içerir. B değerleri önceki yeniden açılış kaydından gelir; B paketinin değişmediği bu turda yeniden doğrulandı. Bunlar solver hedefleridir; gerçekleşmiş çevre/uzunluk ölçümleri değildir.

Solver coupling, nihai B2 ölçüleri, B2 toplam boyu ve el/önkol görsel sonucu **ölçülmedi**. Özgün karakterin önceki ölçülmüş toplam boyu **173,401840 cm**; native Height hedefi **172,276337**. Bu iki sayıyı eşitlemek için baş ölçekleme yapılmadı.

## 3. Kurulu resmî akışta bulunan neden

### Eski beden neden geri geliyor?

`SetBodyConstraints` body state'i çözer ve canlı body mesh yanında `UpdateFaceFromBodyInternal` çağırır. `CommitBodyState` parametre durumunu serialize eder; tam güncellemede canlı mesh'in DNA/verilerini de günceller. Ancak bu çağrı **MetaHuman Character içindeki eski BodyDNABuffer'ı yenisiyle değiştirmez**.

Yeniden açılışta `SetupEditorDataSKMsFromCharacter`, non-fixed gövdede kayıtlı body DNA varsa pozisyonları/joint/weight verisini bu buffer'dan yükler. Önceki B testinde parametreler B olarak kalırken bedenin eski geometriye dönmesi bununla tutarlıdır.

### Resmî UI ne yapıyor?

1. Rigli karakterde body editing tool kapalıdır (`CanBuildTool`, `!IsCharacterRigged`).
2. Toolbar **Remove Rig** işlemi, non-fixed gövde için önce `RemoveBodyRig`, ardından `RemoveFaceRig` çağırır.
3. Body Params / Parametric düzenlemeleri rig kaldırılmış native state üzerinde yapılır.
4. **Create Full Rig** auto-rig yanıtı geldiğinde yüz DNA'sını mevcut bedenle hizalar; parametric `BodyState::StateToDna` sonucunu yeni **BodyDNABuffer** içine, hizalanmış yüz DNA'sını da yüz buffer'ına kaydeder.
5. Ardından Save ve yeniden açılış doğrulaması gerekir.

Dolayısıyla resmî akış yalnız “ölçüyü gir ve Save” değildir. Rig geçersiz kılma ve yeniden üretme yaşam döngüsü vardır. Toolbar komutları [Epic'in editör belgesinde](https://dev.epicgames.com/documentation/metahuman/navigating-metahuman-creator-in-unreal-engine) de açıklanıyor. Genel Python beden kısıtı/commit adımları [Epic'in scripting belgesinde](https://dev.epicgames.com/documentation/metahuman/metahuman-creator-python-scripting-in-unreal-engine?lang=en-US) yer alıyor; bu örnekler mevcut rigli B'nin eski body DNA'sı sorununu tek başına çözmüş sayılmadı.

### Otomasyon engeli

| İşlem | Kurulu Python erişimi | Sonuç |
|---|---|---|
| `set_body_constraints`, `commit_body_state` | Var | Önceki başarısız yolu tek başına tekrar etmedim. |
| `remove_body_rig` | **Yok** | Toolbar'ın beden rigini geçersiz kılma adımını desteklenen Python çağrısıyla çalıştıramıyorum. |
| `commit_body_dna` | **Yok** | Yeni body DNA'yı karakter buffer'ına bağımsız kaydetme çağrısı yok. |
| `align_face_dna_with_body` | **Yok** | İç hizalama metodunu Python'dan ayrı kullanamıyorum. |
| `remove_face_rig` | Var | **Toolbar Remove Rig ile eşdeğer değil.** Yalnız bunu çağırmak body buffer'ını temizlemez. |
| `request_auto_rigging` | Var | Yüz auto-rig çağrısı; beden-only cache yenileme işlemi değil. Körlemesine çalıştırılmadı. |
| `build_meta_human`, `assemble_for_preview` | Var | Assembly/preview; incelemede eski body buffer invalidation yerine geçtiği gösterilmedi. Çalıştırılmadı. |

Mevcut oturumda native masaüstü UI kontrol aracı da yok. Hidden API açma, C++ eklenti yazma, engine patch, binary/DNA buffer hilesi, Conform veya elle baş/beden bağlama uygulanmadı.

[Dosya/satır/versiyon bazlı kaynak denetimi](installed_source_audit.json). Kamuya Engine kaynak kodu yüklenmedi; yalnız bulgular ve kaynak dosya hash'leri yayımlandı.

## 4. Yüz ve boyun: doğrulanmış sınırlar

**Özgün karakterin yüzü korunuyor.** Bununla birlikte resmî Remove Rig işlemi test kopyasının yüz DNA'sını ve morph rigini de kaldırır. Create Full Rig bunları yeniden üretir. Bu akışın B2 üzerinde yüzün gerçek geometrisini sıfır değişimle koruduğu henüz kanıtlanmadı.

İç body→face yolu yalnız seam'e dokunacağı varsayılabilecek basit bir bağlantı işlemi değildir: core API body-face state ve body scale hesaplarına katılır. Yüz katsayılarının sabit olması değerlendirilmiş mesh'in sabit olduğunu kanıtlamaz.

Önceki ölçümler (yeni B2 sonucu DEĞİL):

| Ölçüm | Sonuç |
|---|---:|
| Canlı B generated head, 150 cm üzeri bölge max | 1,669049 mm |
| Aynı bölge mean | 1,124629 mm |
| Orijinal baş + B body, 93 sınır örneğinde seam max | 6,792291 mm |
| Aynı seam mean | 4,575759 mm |
| B yeniden açılınca baş ve body vs özgün mesh | 0 mm / 0 mm: beden değişikliği kayboluyor |

150 cm maskesi geçmişte kullanılan kaba üst-baş/neck ayrımıdır; göz, dudak, çene gibi ayrı anatomik maskelerle yeni B2 testi yapılmış gibi sunulmaz. [Önceki ayrıntılı geometri ve seam kaydı](historical_B_blockers.json).

## 5. Gereken manuel adım ve sonraki kabul kontrolü

[MANUEL_UNREAL_ADIMLARI.md](MANUEL_UNREAL_ADIMLARI.md), yalnız ayrı CharacterLab test kopyası için tam UI sırasını ve dört B2 değerini içerir. **Bu bir doğrulanmış yüz-koruma çözümü değil, eksik resmî UI akışının kontrollü testidir.** Özgün/prodüksiyon karakter üzerinde uygulanmamalıdır.

UI adımları tamamlanırsa kabul hâlâ şu ölçümlere bağlıdır:

- Orijinal baş ile yeni generated head'in gerçek geometry karşılaştırması: facial identity bölgesi ile alt boyun/seam ayrı. DNA hash tek başına yeterli değil.
- Aynı 93 boundary örneğiyle seam max/mean ve görünür normal sürekliliği.
- Save, editörü kapatıp açma/fresh reconstruction, tekrar export ve geometri/parametre/rig karşılaştırması.
- Yalnız bu üç gate geçerse aynı kamera/ışık/LOD/pozla B–B2 ön, yan, arka, ön 3/4, arka 3/4 değerlendirmesi.

B2 bu turda üretilmediğinden yeni B–B2 karşılaştırması veya kabul edilmiş görsel sonucu yoktur. B sanatsal tercihtir; teknik final değildir. [Önceki B ve özgün yüzle görüntüler](https://github.com/beratartanb/sphirus-world-preview/blob/main/chatgpt-bridge/reports/character-native-body-2026-09-28/TEKNIK_RAPOR.md) tarihsel kanıttır.

## 6. Deformasyon

Kullanıcının sıralamasına uyuldu: face/seam/persistence geçmeden yeni tam deformasyon testi yapılmadı.

Bu turda idle, walk, jog, sprint, crouch, jump, arms raised, arms forward, shoulder rotation, torso twist, hip flexion ve **gerçek derin squat**: **NOT_RUN**. Yeni çok açılı stres çekimleri de NOT_RUN. Önceki kısmi knee-bend karesi derin squat kanıtı olarak tekrar kullanılmadı.

## 7. Nihai durum

| Gate | Durum | Kapsam |
|---|---|---|
| BODY PROPORTIONS | **PARTIAL** | B tercih ediliyor; B2 henüz uygulanmadı/karşılaştırılmadı. |
| BODY DEFORMATION | **PARTIAL** | Önceki sınırlı B QA var; bu tur yeni test yok, final kabul yok. |
| FACE IDENTITY | **PRESERVED** | Dokunulmamış kullanıcı-orijinal varlığı. Yeniden üretilmiş B2 kabulü anlamına gelmez. |
| NEUTRAL HEAD/BODY SEAM | **FAIL** | Son ölçülmüş original-head + B-body bağlantısı. B2 NOT_RUN. |
| BODY PERSISTENCE | **FAIL** | Son B yeniden açılışında geometri eski hâline dönüyor. B2 NOT_RUN. |
| FINAL BODY PROMOTED | **NO** | Prodüksiyon değişmedi. |

FACE MODIFIED = NO (bu tur). BLENDER BODY SCULPT = NO. CUSTOM BODY CONFORM = NO. PRODUCTION GAMEPLAY MODIFIED = NO.

Geçmiş denemeler silinmedi: kullanıcı temizliği başarılı final sonrasına bağladı; bu eşik geçilmedi. Karakter düzenlemesi, talep edilen UI erişim engeli durma koşulunda sona erdi.
