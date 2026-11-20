# SPHIRUS UE 5.9 — hareket hissi turu (2026-11-20, ikinci tur)

Proje: `sphirus_UE59` · harita `/Game/GraceRanger/Maps/L_GR_SphirusHouse` · oyuncu `BP_HybridA_Player`
Başlangıç: önceki rapor `sphirus-ue59-ayak-kol-kamera-2026-11-20` (commit `0e2dba3`). Rapordan sonra Content/Config altında değişiklik yoktu; editör açıktı, PIE kapalıydı, kirli paket yoktu. 5.9 test kaydı `3d81ab9d…`, 5.8.4 kullanıcı kaydı `4823d83a…`; ikisi de tur sonunda aynı.

**Durum etiketleri.** UYGULANDI = kayıtlı ve yeniden açılan editörde doğrulandı. ÖLÇÜLDÜ = sayısal kayıtla doğrulandı. GÖRÜLDÜ = kare şeritlerinde baktım (videoyu gerçek hızda izleyemem). **Hiçbir madde USER_ACCEPTED değildir**; his kararı oynayarak sizde.

Girdiler gerçek W/A/S/D/Shift/Ctrl tuşlarıyla, kamera yaw'ı sabit tutularak PIE'ye verildi (elle oynama değil, tuş enjeksiyonu). Veri kayıtları simülasyon zamanıyla 60 Hz, 30 Hz ve 22–60 Hz değişken adımda alındı; videolar 30 Hz sabit adım = 30 fps gerçek hız (`data/vtime20.txt`).

## 1. Yeniden üretilen şikâyetler ve doğrulanmış nedenler

| Şikâyet | Yeniden üretim (taban, 60 Hz) | Doğrulanmış neden (sahip) |
|---|---|---|
| İleri koşu → S: fren görülmeden geri yürüyüş | S'den 0,12 s sonra Gait = WALK, klip `M_Neutral_Walk_Pivot_F_B`, kapsül 415 → 48 cm/s 0,3 s'de, ardından 127–150 cm/s geri yürüyüş | `BP_HybridA_Player` tick: `GR_Back` doğruyken `GR_GaitSel` koşulsuz 0 ve `WantsToWalk` doğru. Koşu hızındaki fren, yürüyüş pivot klibinin altında oynuyordu |
| Geri tempolu hareket yok | Shift+S = S: aynı geri yürüyüş | Aynı satır; geri yönde yürüyüş dışında kademe tanımlı değildi |
| Yürüyüş–koşu arası tempolu kademe yok | Yalnız 180 / 415 / 585 cm/s | `IA_Sph_Pace` hiçbir tuşa bağlı değildi ve olayı boş atamaydı (`GR_Pace = GR_Pace`). `GR_Tempo` yalnız ev içi/yük durumunda hız çarpanıydı |
| Koşuda kollar gövdeye yapışık | Üst kol açıklığı görünür / sürücü: yürüyüş 8,9 / 17,8°, koşu 21,5 / 31,1°, sprint 22,2 / 38,4°; koşuda el orta hattı 2,3 cm geçiyor | `ABP_Sph_Body_GASP`: `VR_Arm` ∓7° × RunA (11-12) + `VW_Arm` ∓3° × MoveA (11-19). MoveA 150 cm/s üstünde her hızda 1 → yürüyüş düzeltmesi koşu ve sprintte tam ağırlıkla uygulanıyordu. Kaynak ve retarget temiz: sürücü (UEFN) açıklığı geniş, daralma yalnız son beden katmanında |
| Baş öne düşüyor / ense bükülü | Boyun hattı (neck_01→baş) dikeyden: bekleme 12°, yürüyüş 22,6°, koşu 37,4°; koşuda göğüs beklemeye göre 19,6° önde | (a) Yürüyüşte göğüs beklemedeki gibi, ama neck_01 20° öne dönük; yürüyüş için boyun kanalı yoktu. (b) Koşu klibi (Neutral run, 500 cm/s için yazılmış, 415'te oynuyor) güçlü öne eğimli; gövde düzeltmesi `VR_Spine` × RunA, RunA 415'te yalnız 0,57 idi. Baş bakışı düz kalıyor (−4…−7°), yani görüntü "öne itilmiş boyun + geri kırılmış baş" |
| Fren çok sert | Sprint duruşu 0,32–0,35 s, 89–102 cm (≈1,7 g) | Sprint duruşu Dense koşu duruş klibine eşliydi (klip 500 → 0, 0,35 s); klibe bağlı fren kapsülü bu profile uyduruyordu |
| İvme hissedilmiyor | 0 → 415: %95'e 0,80 s; 165 cm/s'den sonra sabit 440 cm/s² | `AC_Sph_Motion.GaitUpAcc` 0,55, düz hızlanmanın neredeyse tamamında ivmeyi 800 → 440'a indiriyordu (başlangıç klibi ≈700 cm/s²) |
| Sağ–sol değişiminde atlama | Kare başına poz kopması **ölçülmedi** (60/30/değişken: omuz/kalça hattı ≤ 14°/kare, pelvis ≤ 6 cm/kare). Koşuda A→D: kapsül 0,18–0,22 s'de ters yönde, kalça hattı 500–620°/s | Poz atlaması değil, çok ani yön çevirme: ilk ~0,1 s'de CMC sürtünme terimi hız vektörünü ≈4000 cm/s² ile girdiye çeviriyor, sonra dönüş freni (SpeedScale 0,05) |
| Bekleme: bilek açma, hazırlanma | 5 moladan 3'ü: bilek 21–33°, dirsek 54–88°, eller göğüs hizasına | `AC_Sph_Motion` Idle2–4 = `Relaxed_Stand_Idle_Break_v03 / v05 / v07` |
| Koşarken yan/keskin yön tepkisi kayıp | W→A koşu: `Run_Turn_L_090` oynuyor, hız 415 → 304 → 0,5 s'de 400 | Tepki klibi oynuyor; ayrı bir kayıp sahibi bulunmadı (bkz. açık kalanlar) |

Hareket zinciri (gerçek adlarla): `IA_Sph_*` (IMC_GR_SFGameplay) → `BP_HybridA_Player` tick (`GR_Back`, `GR_GaitSel`, `CharacterInputState`, `SphContextSpeedScale`) → `BP_Sph_GASPCharacter` (`CalculateMaxSpeed/MaxAcceleration/BrakingDeceleration/GroundFriction`, hepsi `AC_Sph_Motion` çıktılarıyla çarpılıyor) → CMC → `ABP_Sph_GASP` (chooser + `CM_Keys/CM_Vals` veritabanı eşlemesi, Motion Matching) → `RTG_Sph_UEFN_to_MH` → `ABP_Sph_Body_GASP` (duruş katmanı) → yüz/kamera. Hız, ivme, fren ve sürtünmeyi tek sahip (`AC_Sph_Motion`) yazıyor; çift yazan bulunmadı. Eski AAMS/SHME çalışma zamanı etkin değil ve geri yüklenmedi.

## 2. Yapılan değişiklikler

| # | Varlık | Değişiklik | Durum |
|---|---|---|---|
| 1 | `BP_HybridA_Player` | Kademe merdiveni: yürüyüş / **tempo** / koşu (Shift) / sprint (Ctrl). `GR_TempoOn` anahtarı; tempo = Gait RUN + Core Motion jog veritabanları (`GR_TempoVals` → `ABP_Sph_GASP.CM_Vals`), hız RunSpeeds × 0,67 (ileri 278), geri × 0,78 (234) | UYGULANDI, ÖLÇÜLDÜ |
| 2 | `IMC_GR_SFGameplay` | `IA_Sph_Pace` = **X** (klavye) ve **gamepad sağ omuz**; oyun bağlamında boş tuşlardı | UYGULANDI (gamepad NOT_TESTED) |
| 3 | `BP_HybridA_Player` | S artık yürüyüşe zorlamıyor: geri kademe = Shift/Ctrl/tempo açıkken tempo (234), değilse yürüyüş (127). S'de 180° dönüp ileri koşma yok; bakış yönü korunuyor | UYGULANDI, ÖLÇÜLDÜ |
| 4 | `BP_HybridA_Player` | **Fren tutma** (`GR_BrakeHold`): hız > 200 ve girdi hıza karşıyken S basılırsa, hız yeni yöne dönene kadar (en çok 0,9 s) Gait RUN kalıyor → koşu pivotu (fren–basış–geri itiş) oynuyor. Kilit değil: W/A/D'ye dönülürse `GR_Back` düşer, tutma biter | UYGULANDI, ÖLÇÜLDÜ, GÖRÜLDÜ |
| 5 | `ABP_Sph_GASP` + oyuncu | Tempo ve sprint duruşları Relaxed koşu duruş klibine eşlendi (CM jog duruşu faza göre 72–145 cm sürüyordu) | UYGULANDI, ÖLÇÜLDÜ |
| 6 | `AC_Sph_Motion` | Fren profili ölçeği: bırakma hızı > 470 ise kapsül klip profilini `hız / 375` ile ölçekli izliyor (`ClipHiRef`, `ClipHiMin`). Sprint duruşu 0,32–0,35 s → 0,54–0,63 s | UYGULANDI, ÖLÇÜLDÜ |
| 7 | `AC_Sph_Motion` | Ters dönüş yumuşatma (`RevOn`, sürtünme × 0,25) yalnız koşu hız bandında (250–470). Yürüyüş ve sprintte aynı anahtar kaymayı artırdığı için bant dışı bırakıldı | UYGULANDI, ÖLÇÜLDÜ |
| 8 | `AC_Sph_Motion` | `GaitUpAcc` 0,55 → 0,8: 0 → 415 %95'e 0,80 s → 0,62 s | UYGULANDI, ÖLÇÜLDÜ |
| 9 | `ABP_Sph_Body_GASP` | `RunA = clamp((hız−200)/(415−200))` (koşuda tam gövde düzeltmesi); `VR_Arm` ∓7 → ±5 (koşuda kolu açar), `VW_Arm` ∓3 → ∓1,5; yeni `VW_Neck1` −6° (hareket hâlinde boyun tabanını geri alır), `VW_Head` (0) | UYGULANDI, ÖLÇÜLDÜ, GÖRÜLDÜ |
| 10 | `AC_Sph_Motion` | Bekleme molaları: v01, v02, v04, v06 (bilek ≤ 13°, dirsek ≤ 13°, eller aşağıda). Aralık 14–26 s aynı | UYGULANDI (klip ölçümü; uzun bekleme izlenmedi) |

**Tempo nasıl açılıp kapanır:** **X** (gamepad sağ omuz) tempoyu açar/kapatır. Açıkken W = tempolu koşu (278 cm/s, kendi klipleri ve ritmi), Shift basılıyken koşu (415), Shift bırakılınca yine tempo. Kapalıyken W = yürüyüş (180). Ev içinde ve iki elle yük taşırken koşu/tempo kapalı kalır (önceki kural).

Kademelerin ayrımı (60 Hz): yürüyüş 180 cm/s `M_Neutral_Walk_Loop_F`; tempo 278 `CM_af_Loco_Jog_Fwd` (kadın jog klibi; 8 yön + başlangıç + pivot); koşu 415 `M_Neutral_Run_Loop_F`; sprint 585 `M_Relaxed_Sprint_Loop_F`. Hızlar kliplerin kök hızlarından seçildi (`data/clipspeed.txt`).

## 3. Önce / sonra

Videolar (gerçek hız, sol = önce, sağ = sonra; "önce" için tur öncesi dosyalar yedekten geçici olarak geri kondu, kayıt sonrası son dosyalar SHA1 ile doğrulanarak geri yüklendi):
- `videos/cam_before_left_after_right.mp4` — gerçek omuz kamerası: yürüyüş → koşu → sprint → dur → koşu → Shift+S → dur → koşu → A → D → dur
- `videos/side_before_left_after_right.mp4` — aynı plan, ayakları gösteren yan kamera
- `videos/tempo_on_shoulder_camera.mp4` — tempo açık, omuz kamerası
- `videos/flow_house_final.mp4` — gerçek haritada tam akış (son durum)
- `evidence/G_runS_before_after.jpg` — koşu → S, 0,17 s aralıklı kareler; `evidence/G_after_cam_gaits.jpg` — omuz kamerasından dört kademe

| Ölçü (60 Hz) | Önce | Sonra |
|---|---|---|
| Koşu → Shift+S: gait / klip | WALK, yürüyüş pivotu, geri 127–150 | RUN tutulur, `M_Neutral_Run_Pivot_F_B`, sonra `CM_af_Loco_Jog_Bwd` 234 |
| Koşu → S: yön dönme süresi / en kötü ayak kayması | 0,37 s / 0,6 cm | 0,35–0,38 s / 2,4 cm |
| Geri → ileri (S → W, koşu tuşu basılı) en kötü kayma | 64 cm | 2,7 cm |
| Koşu A ↔ D: yön dönme süresi | 0,22 s | 0,38–0,40 s |
| 0 → 415 hızlanma (%95) | 0,80 s | 0,62–0,65 s (60/30/değişken) |
| Sprint duruşu: süre / yol / pelvis çökmesi | 0,32–0,35 s / 89–102 cm / 11–13 cm | 0,54–0,63 s / 175–192 cm / 6–9 cm |
| Koşu duruşu | 0,55 s / 110 cm | 0,47–0,63 s / 87–146 cm |
| Tempo duruşu | – | 0,42–0,60 s / 59–105 cm |
| Üst kol açıklığı görünür (sürücü): yürüyüş / tempo / koşu / sprint | 8,9 (17,8) / – / 21,5 (31,1) / 22,2 (38,4)° | 10,4 / 15,9 (18,3) / 31,0 / 35,7° |
| Koşuda elin orta hatta en yakın konumu | −2,3 cm (karşıya geçiyor) | +0,7 cm |
| Boyun hattı: bekleme / yürüyüş / koşu / sprint | 12 / 22,6 / 37,4 / 31,1° | 12 / 16,6 / 26,2 / 25,3° |
| Koşuda göğüs eğimi (beklemeye göre) | −19,6° | −17,9° (fin) / −14,4° (ilk ölçüm) |

Tablolar: `data/final_verification_60_30_var.txt`, `data/carry_*.txt`, `data/head_*.txt`, `data/revslide_base_*.txt`, `data/dir_*.txt`.

### 60 / 30 / değişken adım (son kayıtlı durum)
| Plan | 60 Hz en kötü / ort. kayma | 30 Hz | 22–60 Hz değişken |
|---|---|---|---|
| A: koşu yön değişimleri (14 olay) | 21,2 / 6,8 cm | 21,3 / 8,7 | 17,5 / 6,6 |
| B: sprint + yürüyüş + kısa dokunuşlar | **49,6** / 13,1 | 32,5 / 12,1 | 27,4 / 8,7 |
| C: sabit kademeler + duruşlar | 14,8 / 6,5 | 19,0 / 8,2 | 11,0 / 5,2 |
| V: tempo | 14,2 / 5,6 | 16,2 / 5,5 | 15,3 / 6,1 |

Duruş süreleri üç zaman tabanında aynı karakterde: koşu 0,47–0,63 s, sprint 0,54–0,63 s. Kare başına sıçrama eşiğini (14° veya 6 cm) aşan kare: 12 kayıtta toplam 5 tek kare.

## 4. Baş–boyun–gövde: kaynak / retarget / son karakter

Aynı kayıtta, aynı karede sürücü (UEFN iskeleti = kaynak animasyon) ve görünür MetaHuman eklem konumlarından (`data/carry_*.txt`, `data/head_*.txt`):

| | Sürücü (kaynak) | Önce (retarget + eski katmanlar) | Sonra |
|---|---|---|---|
| Boyun hattı, bekleme | 19,7° | 12,0° | 12,0° |
| Boyun hattı, yürüyüş (beklemeye göre fark) | 25,9° (+6,2) | 22,6° (+10,6) | 16,6° (+4,6) |
| Boyun hattı, koşu | 46,7° (+27,0) | 37,4° (+25,4) | 26,2° (+14,2) |
| Üst kol açıklığı, koşu | 31,1° | 21,5° | 31,0° |

Sonuç: öne eğim büyük ölçüde **kaynak klipte** (Neutral koşu klibi sürücüde de +27°). Retarget bunu olduğu gibi taşıyor (iki iskelet farkı 1–2°). Yürüyüşteki fazladan +4,4° ve koşu/sprintteki kol daralması **sonradan eklenen beden katmanından** geliyordu; düzeltme o katmanda yapıldı. Kemik oranı farkı yüzünden iki iskeletin mutlak açıları doğrudan kıyaslanmaz; beklemeye göre farklar kıyaslanır. Saç/kıyafet gizlenerek eklem incelemesi ve skinning/düzeltici deformasyon denetimi bu turda yapılmadı (NOT_TESTED).

## 5. Gerileme kontrolleri
- Gerçek harita tam akış `F19_flow_F21` (yürüyüş, koşu, kapı, bahçe, odun al–taşı–yar, iki parça, şömineye koy–yak): **PASS** (parça 2/2, ateş durumu 2). Kullanıcı kaydı değişmedi.
- Zıplama (koşu 415 / yürüyüş 180 / durarak): havada 0,63–0,65 s, tepe 54–59 cm; çömelme ve çömelerek yürüme (165 cm/s) çalışıyor.
- Kayıt + yeniden açma: editör son yazımdan sonra üç kez yeniden açıldı; değerler `data/final_state20.txt`, kirli paket yok.
- NOT_TESTED: `loadfire` (bu turdaki deneme, test kaydı henüz yokken çalıştı; geçersiz), eğim/basamak ayrı ölçümü, maske/çay/yatak/kapı etkileşimleri, gamepad, standalone/paketli, performans.

## 6. Eski SHME davranışları
Eski raporlar ve notlardan (V2.29, V2.38, V2.52, V2.53) doğrulanan davranışlar ile bugünkü karşılıkları:

| Eski davranış | Eski sahibi | Bugünkü durum |
|---|---|---|
| Ters komutta fren–basış–yeniden itiş (V2.38 fizik planlı jog kesmesi, 48 klip) | `BP_GR_Player` + `PSD_SHM238_JogCut` | Koşu pivotu + fren tutma ile karşılandı (madde 4, 7); klip ailesi farklı |
| İlk adım öncesi ağırlık aktarımı (V2.52 APA: pelvis destek ayağına 8 cm) | APA klip kopyaları | **Yok.** GASP başlangıç klipleri kullanılıyor; yeniden üretilmedi |
| Duruş sonrası yerleşme (V2.53 settle) | Jog duruş klipleri | `AC_Sph_Motion` SetX yayı etkin (BodyOn); klip düzeyinde settle yok |
| Efor/yorgunluk ölçekleri (V2.29) | Efor bileşeni | `AC_Sph_Motion` E/EUse/Fat etkin |

Eski SHME çalışma zamanı 5.8.4 projesindeki AAMS oyuncusuna ait; aynı girdilerle yan yana kayıt alınmadı (NOT_TESTED). Bu tabloda "karşılandı" yazan satırlar bugünkü sistemin ölçümüne dayanır, eskiyle eşdeğerlik iddiası değildir.

## 7. Açık kalanlar
1. **Sprintten ters yöne dönüş (Ctrl+W → S, sprint A ↔ D): basan ayak 27–50 cm kayıyor** (önce 50 cm; değişmedi). Sprint için strafe pivot klibi yok; koşu pivotu 585'te oynuyor.
2. Koşu A → D'de tek ayakta 21 cm kayma (yumuşatma öncesi 1,5–2,5 cm). Yumuşak dönüşün bedeli; geri almak için `RevOn = false`.
3. Yürüyüş W → S 60 Hz'de 20 cm (30/değişkende ≤ 6); dönerek duruşta 30 Hz/değişken adımda 20–23 cm (önceki 33 cm açığı sürüyor, küçüldü).
4. Koşu başlangıcında ilk ayak 14–16 cm kayıyor (önce de aynı).
5. Tempo: baş beklemeye göre 5° yukarıda, el orta hattı 3,6 cm geçiyor (CM jog klibinin kol taşıması); Core Motion klipleri daha önce tam set olarak "katı" bulunmuştu, bu kez yalnız tempo kademesinde. Tempoda keskin dönüşler Relaxed koşu dönüş kliplerini (375) kullanıyor.
6. Pivot sırasında baş 10–15° öne iniyor (klip içeriği).
7. "Yan momentum tepkisi kayıp" şikâyeti için dönüş kliplerinin oynadığı dışında ayrı bir sahip bulunamadı; gövde yan yatış/karşı dönüş miktarı ölçülmedi.
8. İlk adım ağırlık aktarımı (APA) yok; yürüyüş başlangıcı değişmedi.
9. Önceki listeden: şömine alevi, kapıda yanlış kapının açılması, etkileşim kamerası, dolap, yatak sonrası gün geçişi, 4 eklentinin SAC engeli — dokunulmadı, görev listesinde.

## 8. Geri dönüş
Her yazım öncesi yedekli manifest (`data/manifests_20261120.txt`, yedekler `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/ue59_m22_*`). Tur öncesine tam dönüş: editör kapalıyken `scripts/swap_state.sh before` (son dosyaları `Saved/UE59Work/checkpoints/20261120_after` altına alır). Tek tek kapatma: `GR_TempoOn` kapalı = eski üç kademe; `AC_Sph_Motion.RevOn=false`, `ClipHiMin` büyük değer, `GaitUpAcc=0.55`; beden değerleri `scripts/p6_values.py`.

## 9. İçerik
`scripts/` (düzenleme, yazım, ölçüm ve çözümleme betikleri; `recorder/` kaydedici), `data/` (tablolar, planlar, klip/idle/tuş dökümleri, son durum), `raw/` (ham kayıtlar, gz), `evidence/`, `videos/`. Dünya görseli değişmedi; Bridge yeniden dışa aktarılmadı.
