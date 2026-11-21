# SPHIRUS UE 5.9 — hareket, anatomi, çarpışma ve ev akışları turu 5 (2026-11-22)

Başlangıç: `da958b49` ve `reports/sphirus-ue59-hareket-anatomi-2026-11-21`. Proje: `sphirus_UE59` (UE 5.9, GASP Motion Matching, oyuncu `BP_HybridA_Player`).
Bu rapordaki bütün sayılar **kaydedilip editör iki kez yeniden açıldıktan sonra** alınmıştır (`scripts/final5.sh`, ham çıktılar `data/final5_*.txt`). Girdiler gerçek tuşlardır. Kullanıcı kaydı `SFSaveSlot.sav` tur başındaki sha1 ile aynıdır (3d81ab9d…).

**Kabul durumu:** aşağıdaki PASS/PARTIAL/FAIL yalnızca teknik ölçümdür. Görsel/oynanış onayı kullanıcıya aittir; **USER_ACCEPTED yazılmamıştır.**

| Konu | Teknik durum | Kısa sonuç |
|---|---|---|
| Kol açıklığı (fazla açık → orta) | PASS (ölçüm) | El bileği–kalça hattı: bekleme 21,4 / yürüyüş 19,9 / tempo 19,5 / koşu 18,4 / sprint 21,2 cm (tur 4: 23,7 / 22,1 / 23,1 / 21,6 / 23,9; tur 3: 18,8 / 17,6 / 15,8 / 22,1 / 24,8). 60, 30 ve 22–60 Hz'de aynı (±0,5). |
| Baş/boyun/omuz taşıması | PASS (ölçüm) | Klipteki duruşun bir kısmı korunuyor (dünya açısına kilit yok); omuz yüksekliği sol/sağ farkı ≤0,4 cm; baş eğimi bekleme −1,6°, yürüyüş −4,3°, tempo −5,6°. |
| Yorgunluk | PASS (ölçüm) | 14 sn sprintte Fat 0→0,63, dinlenmede tepe 0,82, ~12 sn'de 0,04. Omuz düşüşü ≤2 cm (önce görünür çöküş), gövde eğimi dinç duruştan 0,5° farklı. |
| Dönüşte hız kaybı / başlangıç-fren ağırlığı | PASS (ölçüm) | 45° → %90, 90° → %68–71 (0,47–0,58 sn'de geri), 135° → %27, sprint 90° → %64. İlk adımda yumuşak ivme. |
| Ayak kayması | **PARTIAL** | Ortalama 0,9–3,5 cm, %90 1,6–9,5 cm. 22 cm'lik 135° dönüş, kamera+duruş, sprint başlangıcı düzeldi. ≥20 cm kalanlar bölüm 5'te tek tek. |
| Çarpışma bağlamı ve duruma bağlı tepki | PASS (ölçüm), kapsam PARTIAL | Önceden yavaşlama + el desteği, sıyırma, engellenme, sendeleme, diz çöküp kalkma; 60 ve 30 Hz'de aynı. Yüzüstü düşüş yok (bölüm 5). |
| Rampa / merdiven / zıplama / çömelme | PARTIAL | Yanlış çarpışma olayı yok; merdivende leğen gecikmesi 66 → 43 cm (yürüyüşle aynı). Çömelme duruşunda 22 cm kayma açık. |
| Yatak yazısı | PASS | Yatarken, kararmada ve kalkarken "Uzan / Kalk" ve işaret görünmüyor. |
| Maske | PASS (ölçüm/görüntü) | Maske iki elle kenarlarından tutuluyor, yüzü omuz üstünden kadrajın ortasında. Yayınlanan video yenilendi. |
| Performans, standalone/paket, gamepad | **NOT_TESTED** | Bölüm 5. |

## 1. Katman teşhisi — hangi kusuru hangi katman üretiyordu

| Şikâyet | Üreten katman (ölçümle) | Kanıt |
|---|---|---|
| Kollar fazla açık, baş/boyun dik ve önde, omuzlar dengesiz | Tur 4 duruş denetleyicisi (`GR_Posture` v1): gövde/baş açılarını sabit hedefe çekiyor, kol açıklığını sabit yanal bilek mesafesine zorluyordu. Ham klip ve yalnız-retarget katmanında bu yok. | `data/final5_posture.txt` (BIND satırı = MetaHuman referansı) |
| Yorgunlukta omuz çöküşü, öne yığılma | Gövde ABP'sindeki sabit efor vektörleri (VE_*) doğrudan Fat ile çarpılıyordu (gövde + omuz + baş aynı anda). | `scripts/c_bodyspace2.py` |
| 135° koşu dönüşünde 22 cm kayma | Hareket bileşeni: girdi basılıyken hız sınırı düşünce kapsül **girdi anına** bağlı sabit ~870 cm/s² ile frenliyor ve sınırın altına inene kadar dönmüyor; klip ise ayak evresinden giriyor, basışı 0,15 sn önde → ayak kilidi kopuyor. | `data/rootpath.txt`, `scripts/m_dm_mcp.py` başlığı |
| Yürüyüş + kamera 90° + duruşta 19–27 cm | (a) Motion Matching altındaki Steering düğümünün **açık pini** 0,4 sn: gövde kapsülün 50° gerisinde kalıyor; (b) Relaxed duruş veritabanında düz duruş dışında yalnız 90°/180° "reface" duruşları var → gövde yerinde 90° dönüp 42° fazla gidiyor, sonraki başlangıçta geri çekiliyor. | `scripts/c_steerpin5.py`, `c_stopdb5.py` |
| Sprint duruştan başlarken 15–19 cm | Oyuncu BP: sprint yürüyüşü yalnız 250 cm/s üstünde devreye giriyordu; koşu başlangıç klibinden sprint geçiş klibine ilk sol basışın ortasında geçiliyordu. | `scripts/m_sprintmin_mcp.py` |
| Geri tempo duruşunda "13–16 cm" | **Ham klip**: `M_Relaxed_Run_Stop_B_L/Rfoot` temas eğrisi ayak 12–14 cm havadayken "temas" diyor (36–64 cm). Oyun içi kayma değil; ölçümde ayrı sütun. | `data/rawfoot.txt` |
| Merdivende gövdenin gömülmesi | Sürücü ABP FootPlacement leğen yayı (sertlik 100): gecikme 2v/ω. | `scripts/c_pelvis5.py` |
| Maskede yukarı bakan kamera | Kamera bileşeni: "baş kadrajda kalsın" eğim sınırı; maske baştan 36 cm aşağıda. | `scripts/m_camaim_mcp.py` |

İskelet/retarget/Physics Asset: bu turda beden oranı, kemik taşıma veya retarget zinciri **değiştirilmedi** (tur 4'teki parent-space düzeltmesi ve güncelleme sırası korunuyor). Physics Asset (`PHYS_MHC_Sph8`) incelenmedi/kullanılmadı.

## 2. Uygulanan değişiklikler (hepsi kaydedildi; manifestler `ue59_m25_r5a…r5g`, geri dönüş noktası `Saved/UE59Work/checkpoints/20261121_round5_start`)

| Varlık | Değişiklik | Betik |
|---|---|---|
| `BP_HybridA_Player` | Duruş denetleyicisi v2 (klip duruşunun bir kısmını korur, kol başına ölçülen abdüksiyon hedefi, ivmeye bağlı gövde yayı, yorgunluk payı denetleyicide); `GR_SprintMinSp`; **`GR_Contact`** çarpışma olayı; hareket girdisi kilidi | `m_posture2_mcp.py`, `c_posture2_defaults.py`, `m_sprintmin_mcp.py`, `m_contact_mcp.py`, `c_player5_defaults.py` |
| `ABP_Sph_Body_GASP` | Ön kol düğümleri üst kol uzayına; efor vektörleri sıfır; nefes genliği | `c_bodyspace2.py` |
| `AC_Sph_Motion` (+ `BP_Sph_GASPCharacter` şablonu) | Dönüş hız kaybı (TurnLoss), yumuşak ilk itiş, girdi basılıyken klibe bağlı fren (Dm), çarpışma hız sınırı/freni ve el uzatma girişi | `m_turnloss_mcp.py`, `m_turnloss2_mcp.py`, `m_dm_mcp.py`, `m_ctbrake_mcp.py`, `c_motion5_defaults.py` |
| `ABP_Sph_GASP` | Steering_1 pini 0,4 → 0,2 sn (Steering_0 kapalı kaldı); boşta yörüngede kamera dönüş hızı tahmini 100 → 0; duruş veritabanı eşlemesi; leğen yayı 100 → 600 | `c_steerpin5.py`, `c_steerfix5.py`, `c_traj5.py`, `c_stopdb5.py`, `c_pelvis5.py` |
| Yeni: `PSD_Sph_R_Walk_Stops`, `PSD_Sph_R_Run_Stops` + 16 Relaxed duruş klibine `SphR_*` iz | Reface'siz duruş veritabanları | `c_stopdb5.py` |
| `BP_GR_DayStation`, `BP_GR_DayHub` | İstasyon sırası boyunca yazı/işaret gizli; yatakta uyanış bitene kadar | `m_prompt_mcp.py` (+2, 3 ve satır içi düzeltmeler) |
| `BP_GR_MaskBench`, `AC_Sph_Camera`, `L_GR_SphirusHouse` | Maske iki bilek arasına yerleşir; omuz yanı kadraj (14/30/30, hedefe tam bakış); tam bakışta baş-kadraj sınırı atlanır | `m_maskgrip_mcp.py`, `m_camaim_mcp.py` |
| `L_Sph_MoveTest` | Temas parkuru: duvar, bel ve diz yüksekliğinde blok, yan duvar, 45° duvar, 30 cm basamak, 15° rampa, 8 basamak merdiven (`MT_CT_*`) | `w_ctcourse.py`, `w_ctcourse2.py` |

## 3. Çarpışma sistemi (yeni)

Tek sahip: oyuncu Blueprint'indeki `GR_Contact`. Çıkışlar mevcut sahipler üzerinden: hareket bileşeni (hız sınırı, fren, el uzatma IK'sı), duruş yayları (gövde itkisi, kol açma), sürücü slotu (diz çökme/kalkma klipleri).

- **Algı:** her karede son hareket yönünde 3 çizgi (göğüs 138, bel 92, diz 52 cm) + her yana birer yanal çizgi. Sınıf: duvar / bel yüksekliği / diz yüksekliği / yalnız göğüs; yüzeye mesafe, normal, yaklaşma hızı.
- **Önceden yavaşlama + destek:** girdi basılıyken karşıdan duvar/bel engeli: hız ≤ 60 + √(2·600·(d−10)); 55 cm içinde yakın el yüzeye uzanır; yüzeye dayanınca duvara doğru girdi düşer (el duvarda durur).
- **Sıyırma:** yan yüzey 3–12 cm (hıza göre): yakın el yüzeye, gövde 3° uzağa yatar, hız son tepe hızın %80–100'ü.
- **Çarpma şiddeti:** S = v/330 × yükseklik (duvar 1, bel 1,15, diz 1,5, göğüs 0,8) × (1 + 0,5·yorgunluk + 0,25 taşıma + 0,2 iki ayak havada) × (öngörülmüşse 0,75'e kadar).
  S<0,35 yalnız gövde itkisi · <0,9 engellendi (geri adım, 0,16 sn girdi yok) · <1,5 sendeleme (daha büyük geri itki, kollar açılır, 0,45 sn + yorgunluk, 1,2 sn yavaş) · ≥1,5 denge kaybı: tek dize çöker, bekler (yorgunken daha uzun), kalkar.

| Senaryo (`data/final5_contact.txt`) | 60 Hz | 30 Hz |
|---|---|---|
| Duvara yürüyüş / koşu / sprint, bel bloğuna koşu | Çarpma olayı yok: 127–192 cm'den fren, ~100 cm/s ile varış, el duvarda (1,00) | aynı |
| Diz bloğu, yürüyüş 180 | S 0,82 → engellendi | S 0,82 → engellendi |
| Diz bloğu, tempo 278 | S 1,26 → sendeleme (0,45 sn kilit) | aynı |
| Diz bloğu, koşu 415 | S 2,26 → diz çökme 0,97 sn, bekleme 0,6 sn, kalkış 1,76 sn (leğen 48 cm) | aynı |
| Diz bloğu, yürüyüş 180, yorgunluk 0,9 (zorlanmış girdi) | S 1,35 → sendeleme (0,72 sn kilit) — dinçken aynı çarpma "engellendi" | — |
| Yan duvar, koşu | 3,5 sn sıyırma, el 0,70, yatış −3° | — |
| 45° duvar | fren + yüzey boyunca kayma + sıyırma | — |
| 30 cm basamak, rampa, merdiven, zıplama | çarpma olayı yok | — |

## 4. Ölçümler

### 4.1 Duruş (`data/final5_posture.txt`, 60 Hz; 30 Hz ve 22–60 Hz değerleri ±0,5 içinde aynı)

| | Omuz yüksekliği S/Sğ (cm) | Kol abdüksiyonu S/Sğ (°) [en az..en çok] | Bilek–kalça hattı (cm) | Boyun açısı (°) | Baş öne (cm) | Baş eğimi (°) | Gövde eğimi (°) |
|---|---|---|---|---|---|---|---|
| MetaHuman referans pozu | 7,0 / 7,0 | 37,6 | — | 21,7 | 5,3 | 0 | −9,9 |
| Bekleme | 5,4 / 5,4 | 11,0 / 12,3 | 21,4 | 19,9 | 4,4 | −1,6 | −6,8 |
| Yürüyüş 180 | 6,1 / 5,8 | 12,5 [3..21] / 11,5 [4..22] | 19,9 | 21,8 | 4,5 | −4,3 | −5,9 |
| Tempo 278 | 5,8 / 5,5 | 16,6 [3..26] / 15,8 [2..27] | 19,5 | 16,8 | 3,5 | −5,6 | 1,6 |
| Koşu 415 | 6,0 / 5,9 | 23,1 / 21,4 | 18,4 | 15,5 | 2,8 | −2,4 | 3,9 |
| Sprint 585 | 6,6 / 6,3 | 25,7 / 24,3 | 21,2 | 16,2 | 2,8 | −5,7 | 3,2 |
| Yana 180 / geri 150 | 6,2 / 5,8 · 5,4 / 5,3 | 12,7 / 11,4 · 12,8 / 12,1 | 20,1 · 21,5 | 21,3 · 22,7 | 4,2 · 4,7 | −5,3 · −4,4 | −4,5 · −5,3 |

Tempoda eller önde hâlâ orta hatta buluşuyor (en az −1,8 / 0,4 cm; tur 3'te −4,2).

### 4.2 Yorgunluk (`final5_posture.txt`, `f5_F_60`)

Sprint 14 sn: efor 0,43 → 0,84, Fat 0,00 → 0,63; duruşta tepe 0,82; yürüyüşte 0,79 → 0,49; ~12 sn sonra 0,04. Omuz eklemi (üst sırta göre): dinç 5,8 cm, Fat 0,75–0,82'de 3,8–5,1 cm. Gövde eğimi yorgun bekleme −7,3°, dinç bekleme −6,8°.

### 4.3 Dönüş ağırlığı (`final5_slide.txt` sonu, plan T)

| Dönüş | En düşük hız | %95'e dönüş | Tepe yavaşlama |
|---|---|---|---|
| Koşu 45° | %90 | 0,25–0,28 sn | 300 cm/s² |
| Koşu 90° | %68–71 | 0,47–0,58 sn | 780–1260 |
| Koşu 135° (çapraz geri) | %27 | 0,93 sn (geri tempo hızına) | 1590 |
| Sprint 90° | %64 | 0,83 sn | 920 |
| Yürüyüş 45° | %100 | — | — |

### 4.4 Ayak kayması (`final5_slide.txt`)

İki okuma: **eğri** = sürücü klibin temas eğrisine göre (tur 2–4 ile aynı ölçüt, eşik değişmedi); **yerde** = aynı temasın yalnız ayak gerçekten yerdeyken (≤6,5 cm) kısmı. İkincisi birinciyi küçültmek için kullanılmadı; ikisi de veriliyor.

| Plan | 60 Hz eğri ort / %90 / en kötü (≥10, ≥20) | 60 Hz yerde en kötü | 30 Hz eğri ort / %90 / en kötü | 22–60 Hz en kötü |
|---|---|---|---|---|
| A koşu zincirleri | 2,0 / 2,1 / 16,4 (4, 0) | 16,4 | 1,5 / 2,5 / **21,3** | 13,3 |
| B sprint + yürüyüş | 2,2 / 3,4 / **29,8** (2, 2) | 29,8 | 2,9 / 4,7 / **44,9** | — |
| S başlangıç/duruş | 2,0 / 4,0 / 11,3 (2, 0) | 11,3 | 1,6 / 2,7 / 10,0 | — |
| Q tempo | 1,5 / 2,4 / 9,9 (0, 0) | 5,6 | — | — |
| K geri zincir | 1,3 / 1,6 / **24,2** (1, 1) | 24,2 | 0,9 / 1,7 / 4,4 | — |
| T dönüşler | 2,0 / 2,7 / 16,7 (3, 0) | 16,7 | — | — |
| C bilinen kötü örnekler | 1,8 / 3,4 / **20,4** (2, 2) | 20,4 | 2,3 / 6,1 / **26,4** | **32,6** |
| W yürüyüş + kamera | 3,4 / 9,5 / 19,0 (5, 0) | 19,0 | 2,9 / 8,3 / 18,5 | 17,2 |
| D 135° dönüş, 8 evre | 2,0 / 3,1 / 16,8 (4, 0) | 4,5 | — | — |
| P sprint başlangıçları | 1,1 / 1,7 / 3,3 (0, 0) | 3,3 | — | — |
| R tekrarlı ters dönüş | 2,9 / 6,2 / **22,6** (4, 2) | 22,6 | — | — |

Üst beden sıçrama karesi (aynı eşik: >120 cm/s ve yerel ortancanın 6 katı): plan başına 0–8; en büyük üst beden adımı 3,6 cm.

Kullanıcının saydığı örneklerin durumu:

| Örnek | Önce | Şimdi | |
|---|---|---|---|
| 135° çapraz dönüş | 22 cm | 3 cm (8 evrede yerde ≤4,5) | düzeldi |
| Yürüyüş + kamera 90° + duruş | 19–27 cm, gövde 59° ters dönüyor | 2–3 cm, düz duruş klibi | düzeldi |
| Dönerek başlangıç (reface) | 13–22 cm | listede yok (<10) | düzeldi |
| Sprint duruştan | 15–19 cm | ≤3,3 cm | düzeldi |
| Kısa geri komut sonra ileri | 23–33 cm | 60 Hz 5 cm; değişken Hz'de **20,6** | kısmen |
| A→D→bırak | ~51 cm | kısa D: 1 cm; 0,45 sn D: **20,4** | kısmen |
| 30 Hz koşu duruşu | ~22 cm | C planında ≤3; A planında **21,3** (evreye bağlı) | **açık** |
| Tekrarlı ters dönüş | ~38 cm | 60 Hz 7–22,6; 30 Hz **26,4**; değişken **32,6** | **açık** |
| Sprint → geri | ~38 cm | **20–25** (üç planda aynı yer) | **açık** |

### 4.5 Arazi (`data/final5_terrain.txt`)

Rampa 15°: kayma %90 ≤3,5 cm, leğen adımı ≤2,6 cm/kare. Merdiven (18/30): yürüyüşte leğen kapsüle göre 43 cm aşağıda — ayaklar basamaklarda (`evidence/stairs5w.jpg`); koşuda 66 → 43 cm (yay 600 + merdivende hız 260 cm/s'ye iner), üst basamakta derin diz bükülmesi sürüyor (`evidence/stairs5.jpg`). Zıplama (koşu, yürüyüş, yerinde): 0,27–0,28 sn havada, olay yok. Çömelme yürüyüşü duruşunda **22,3 cm** kayma (açık).

### 4.6 Ev akışları

| Akış (yeniden açılmış durum, gerçek tuşlar) | Sonuç | Kanıt |
|---|---|---|
| Yatak: yatış → bekleme → uyku → gün değişimi → uyanış | Akış tamamlanıyor; "Yatak / Uzan / Kalk" yazısı ve gri işaret yatarken, kararma karesinde ve kalkarken **görünmüyor** (önce hepsinde vardı). Şilte yerleşimi (tur 4) korunuyor. Uyanış sonrası yazının yatağa dönünce geri geldiği ayrı kareyle **doğrulanmadı** (geri açan kod: `GR_PromptOn`). | `evidence/00–01`, `videos/10` |
| Maske: alma → inceleme → bırakma | İncelemede maske iki elle yan kenarlarından tutuluyor, yüzü kadrajın ortasında, kamera sağ omuz yanında (önce: parmaklar yüzü kapatıyor, baş kadrajı dolduruyordu). İncelemeye girerken bir an omuz kadrajı kapatıyor (geçiş karesi). | `evidence/02–03`, `videos/11` |
| Odun: toplama → taşıma → yarma → iki parça → arka kapı → şömine → yakma | `CHECK wood picked True, split pieces 4 (need 2) PASS, fire state 2 PASS` — çarpışma sistemi açıkken (kapılar, ev içi yürüyüş, bahçe yolu aynı akışta). | `data/final5_house.txt` |
| Kullanıcı kaydı | sha1 değişmedi (3d81ab9d…); testler ayrı yuvada. | `data/final5_house.txt` |

## 5. Açık kalanlar (dürüst liste)

1. **Ayak kayması ≥20 cm kalan örnekler** (hepsi klip–klip karışımında destek ayağının yeniden yerleşmesi; kapsül–klip hızı uyumlu):
   sprint → geri (20–25 cm, `Run_Stop_F_Rfoot` → `Run_Start_B_Lfoot`), sprint D↔A (29,8; 30 Hz 44,9; `Sprint_Turn_180`), koşu A↔D 180° dönüş klipleri (20–26; değişken Hz 32,6), yürüyüş S→W pivotu (22–23), 30 Hz koşu duruşu bir evrede 21,3, çömelme duruşu 22,3. Bunlar bu turda **düzelmedi**.
2. Duruş sonu yerleşme adımları 10–19 cm (duruş klibinden bekleme döngüsüne geçiş), koşu duruşunda `Run_Stop_F_Rfoot` 14 cm.
3. **Yüzüstü düşüş ve yerden kalkış yok.** Denge kaybı tek dize çökme + kalkma olarak uygulanır. Projedeki düşme/kalkma klipleri (`MC_Sample`: Knockdown, DropToFloor_GetUp, ProneCrawl_Trans_Stand) `SKM_MCUE5v2_Skeleton` üzerindedir; sürücü iskeletin uyumlu listesi yalnız `SK_MCPaul_Skeleton` içerir (`data/fallclips.txt`). Retarget edilmedi; ragdoll denenmedi.
4. Çarpışmada taşıma durumu (0,25 payı) formülde var, **test edilmedi**. Hareketli/itilebilir cisimler, başka karakterler ve tavan/alçak geçit için tepki yok. El desteği yalnız konum IK'sıdır (avuç yüzeye hizalanmıyor).
5. Merdivende koşu: üst basamakta derin diz bükülmesi (PARTIAL).
6. Maske: bırakma/alma anında varsayılan istasyon kadrajına dönülüyor; yalnız inceleme evresi omuz yanı.
7. Şömine sağındaki parlak nokta: bu turda **incelenmedi**. Çay, gardırop, kapılar, tam kayıt/yükleme ve gün değişimi sonrası yeniden yükleme: bu turda **koşturulmadı** (görev sırası çay → gardırop oyun içi testi dahil).
8. **Performans ölçülmedi** (yeni sorgular: kare başına 5 çizgi izi + ~200 Blueprint düğümü). Standalone/paket, gamepad, PIE dışı doğrulama **yapılmadı**.
9. Diz çökme sırasında diz/baldır engelin içine giriyor (`evidence/08`): geri itki 40 cm/s, çökme klibi dizi öne taşıyor. Duvara dayanınca omuz kamerası yalnız baş/sırtı gösteriyor, el desteği kadrajda görünmüyor (`evidence/09`).
10. **Disk:** C: sürücüsü doğrulama sırasında tamamen doldu (şu an ~1,7 GB boş). Bu yüzden yorgunluk videosu yok ve PIE dışı ek kayıt yapılmadı. Hiçbir şey silinmedi; yer açma kararı kullanıcıya ait.
11. Bekleme el duruşu (yumruk/bilek hazırlığı), bekleme molası seti: bu turda değişmedi, ayrıca ölçülmedi.
12. Kamera: dar alanda sağ omuz kamerası için yeni ölçüm yok; yalnız maske bağlamı değişti.

## 6. Yeniden üretim

```
bash Saved/UE59Work/r5/final5.sh slide|posture|contact|terrain|house|video
```
Betikler `scripts/`, planlar `scripts/plans/`, analizler `scripts/an_*.py` (`an_slide3.py` iki okumalı kayma, `an_ct.py` çarpışma, `an_carry5.py` duruş, `an_fat5.py` yorgunluk, `an_turn5.py` dönüş, `an_terr.py` arazi). Eşikler betik başlıklarında; tur 4 eşikleri değiştirilmedi.

## 7. Videolar

Hepsi son kayıtlı durumdan (editör yeniden açıldıktan sonra), gerçek hızda, hareket bulanıklığı/alan derinliği eklenmeden. "omuz" = oyundaki gerçek yakın omuz kamerası, "yan/arka" = tam beden teşhis görünümü.

| Dosya | İçerik |
|---|---|
| `01_omuz_…`, `02_yan_…`, `03_arka_…` | Aynı plan üç görünüm: bekleme → yürüyüş → tempo → koşu |
| `04_omuz_donusler_45_90_135` | Koşu/yürüyüş/sprint dönüşleri, 135° çapraz dönüş, duruşlar |
| `05_omuz_yuruyus_kamera90_durus` | Yürüyüş + kamera 90° + duruş, ardından düz yürüyüş + duruş, duruşta kamera dönüşü |
| `06_omuz_duvara_kosu_…` | Duvara koşu: önden fren, el desteği, dayanma, geri çekilme |
| `07_omuz_diz_engeli_yuruyus_…` | Diz yüksekliğinde engele yürüyüş: engellendi |
| `08_yan_diz_engeli_tempo_…` | Tempo ile çarpma: sendeleme |
| `09a/09b_…diz_engeli_kosu…` | Koşarak çarpma: denge kaybı, tek dize çökme, kalkma (omuz + yan) |
| `09c_arka_yan_duvar_siyirma` | Yan duvar boyunca koşu: sıyırma, el, yatış |
| `10_yatak_…`, `11_maske_…` | Ev akışları (yeni yatak yazısı davranışı, yeni maske kavrama/kadraj; **tur 4'teki maske videosunun yerini alır**) |
| `12_…`, `13_…` | Merdiven yürüyüş / koşu (yan) |

Üretilemeyenler: **yorgunluk videosu** (kayıt sırasında C: diski tamamen doldu — 0 bayt boş; dosya 48 baytlık kaldı; sayısal veri `data/final5_posture.txt` içinde tam). Ev akışı (odun → şömine) videosu 100 MB olduğu için yayınlanmadı; yerelde `Saved/Codex/Day_20261107/videos/F19_flow_R5.mp4`. Her kritik senaryo için iki görünüm koşulu yalnız 01–03 ve 09a/09b'de sağlandı; diğerleri tek görünümdür.
