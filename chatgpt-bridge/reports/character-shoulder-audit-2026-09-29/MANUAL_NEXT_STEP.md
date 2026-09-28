# Desteklenen Unreal arayüz adımı — henüz omuz düzeltmesi değildir

**Kabul edilen B2 değişmedi. Omuz sorunu çözülmedi.** Hazırlanan ayrı test kopyasında resmî RBF açılımının arayüzden yapılması gerekiyor. Bu işlem düzeltilebilir PoseAsset verisini üretir; tek başına anatomiyi düzeltmez.

Bu oturumda yerel Unreal penceresini çalıştıran UI otomasyonu kullanılamıyor. Public Python `BuildMetaHuman`, override verilmediğinde yeni varsayılan pipeline kuruyor; `PipelineOverride` Python tarafından korumalı. Bu sınır aşılmadı ve engine/plugin değiştirilmedi.

1. Yalnızca şu test MetaHuman'ı aç:
   `/Game/Sphirus/CharacterLab/ShoulderFix_20260928/MH_SHOULDER_FIX_NATIVE`
2. Gerekirse **Edit → Project Settings → MetaHuman Character → Enable Experimental Workflows** seçeneğini arayüzden etkinleştir. Denetim sonunda bu ayar hâlâ kapalıydı. Bu, Epic'in deneysel Body RigLogic Unpacking yoludur; üretim kabulü anlamına gelmez.
3. MetaHuman Character Editor **Assembly** bölümünde test çıktısının CharacterLab altında kaldığını doğrula. Hedef klasör:
   `/Game/Sphirus/CharacterLab/ShoulderFix_20260928/Assembly`
   Ortak test çıktıları:
   `/Game/Sphirus/CharacterLab/ShoulderFix_20260928/Common`
4. Body assembly gelişmiş seçeneklerinde **Post Process Anim BP** için proje kopyasını seç:
   `/Game/Sphirus/CharacterLab/ShoulderFix_20260928/ABP_ShoulderFixNative_PostProcess`
5. **Unpack RigLogic = açık**, **Unpack RBF to Pose Assets = açık** yap. **Unpack Finger Half Rotations to Control Rig = kapalı**, **Unpack Swing Twist to Control Rig = kapalı** kalsın. Böylece ilk deneme RBF açılımıyla sınırlanır; native swing/twist yolu korunur.
6. **Assemble** çalıştır. Var olan yalnızca bu test assembly çıktıları yenilenebilir; kabul edilen B2 veya production karakter hedef olmamalı. Body Params, HeadScale, Remove Rig, Conform veya yüz araçlarını kullanma.
7. Tamamlandığında test çıktısında **Body/RBF** altında `AS_*` ve `PA_*` varlıklarını ve test post-process içinde PoseDriver düğümlerini doğrula. Mevcut otomatik denemede bunların sayısı **0**; aynı sonuç alınırsa işlem başarılı sayılmaz.
8. Yalnız test varlıklarını kaydet. İlk sonraki kontrol, açılmış rig'in B2 ile nötr ve pozlu eşdeğerliğidir. Eşdeğerlik kanıtlanmadan düzeltici pozları düzenleme.

Sonraki çalışma; ilgili shoulder helper hedeflerini belirleme, test kopyasında kontrollü düzeltme, izole 30/60/90/120/tam kaldırma ve iç/dış rotasyon testleri, 93 nokta seam testi ve kaydet/kapat/aç doğrulamasıdır. Bu aşamalar henüz yapılmadı. Üretime aktarma yetkisi verilmedi.

Resmî açıklama: [Epic — MetaHuman Body RigLogic Unpacking](https://dev.epicgames.com/documentation/metahuman/metahuman-body-riglogic-unpacking-in-unreal-engine). Bu özellik deneysel ve performans maliyeti taşıyabilir.
