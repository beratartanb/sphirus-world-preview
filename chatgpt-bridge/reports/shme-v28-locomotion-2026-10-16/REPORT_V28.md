# SHME V2.8 — Skill altyapısı + temas planlı yürüyüş başlangıcı / duruşu (2026-10-16)

**İstek:** önce uzmanlık / skill altyapısını gerçekten güçlendir; sonra öğrendiklerinle hareket sistemini kontrollü iyileştir.
Öncelik: başlangıç, kısa hareket, duruş. Ayağını gerçekten basan bir insan; gereksiz kontrol gecikmesi, ağırlıksızlık veya kayma yok.

**Sonuç (kısa):**
- **Yürüyüş duruşu — üretime alındı.** Yeni 24 fazlı duruş klibi + giriş mantığı (`SHM28_StopMode = 1`).
  - Basan ayağın duruş girişindeki kayması **21 cm → 3 cm** (ortalama), **30–33 cm → ~5 cm** (en kötü). 6 farklı adım fazında, 2'şer tekrar.
  - Duruş sonunda yürüyüş yüksekliğinin altına inme **~3 cm → ~1 cm** (0.8–1.4).
  - Kollar ve gövde sakin; son adım kısa.
- **Yürüyüş başlangıcı — aday hazır, üretime alınmadı** (`SHM28_StartMode = 0` kaldı).
  - Normal başlangıç ve yeniden kalkışta basan ayak kayması 25–30 cm → 5–9 cm.
  - Ama çok kısa basma / iptal / tekrar basmada ölçülebilir **regresyon** var (4 tekrarda medyan 2–10 kat daha fazla zemin kayması).
  - Kuralın gereği terfi edilmedi; sıradaki iş.
- **Teknik doğrulama:**
  - Taze editörde diskten `verify_v28.py` **ALL_OK** (varsayılanlar, 26 klip referansı / uzunluğu, derleme 0 hata, pawn profilleri).
  - Override'sız üretim duman testi yeni duruşu kullanıyor, walk senaryolarında pop 0.
- **Görsel inceleme:** yan / çapraz / oyun kamerası kareleri incelendi (§7). Duruşta pop veya yana kayan ayak görülmedi.
  - Kısıt: silüet ışığı ve dönen kamera nedeniyle cm düzeyi kayma karede değil, metrikte ölçüldü.
- **His / kontrol kabulü NOT_TESTED:** oyun testi senin, bkz. `USER_PLAYTEST_V28.md`.

## 1. Nasıl ölçüldü
- **Ortam:** QA zemini, gerçek giriş yolu (IA_Move / IA_Look / gait tuşları), V2.7 üretim değerleri her koşuda açıkça veriliyor.
  - Varyantlar ABP anahtarlarıyla aynı editör sürecinde dönüşümlü.
  - Not: harness `abp_flags` değerlerini koşular arasında sıfırlamıyor. Tüm karşılaştırma varyantları her iki modu açıkça veriyor; kayıt dışı kalan 2 görüntü koşusu atıldı ve yeniden alındı.
- **Temas metriği** (`sphirus-human-motion-engine/scripts/contactslip.py`):
  - Gerçek temas penceresinde, zemine göre yükseklikle tanımlanır. Ayak önü yerdeyken top (ball), topuk fazında ayak bileği.
  - İniş / orta destek / parmak kalkışı ayrı raporlanır; doğal topuk-parmak yuvarlanması kayma sayılmaz.
  - Görünen (MetaHuman) ve sürücü (Manny) mesh ayrı ölçüldü; eşitler → retarget sorumlu değil.
- **Duruş girişi** (`stopentry.py`): bırakma anında basan ayak, seçilen klip / zaman, ilk 0.25 s ve 0.6 s'deki zemin kayması.
  - 0.6 s penceresi bir sonraki kapanış / kalkış adımının ilk kalkışını da içerebilir → üst sınır.
- **Diğer araçlar:** `stopdip.py` / `startsize.py` / `turngait.py` (V2.7); yeni: `v28_matrix.py` (tablo), `slip_owner.py` (kaymayı poz sahibine göre ayırır), `v28_sheet.py` (kare panoları).
- **Toplam:** ~110 PIE koşusu, 3 bellek-yeniden başlatması, çökme yok.

## 2. Güçlendirilen skill'ler (A–J) ve doğrulama
Kanonik dosyalar `.agents/skills/`.
- Claude sarmalayıcıları `Tools/SkillSystem/sync_claude_skills.py` ile üretildi: 71 skill, 0 hata / 0 uyarı, `--check` temiz, tüm yeni bağlantılar mevcut.
- SKILL.md dosyaları kısa (42–88 satır). Ayrıntı `references/`, çalışan araçlar `sphirus-human-motion-engine/scripts/` altında.

| | Dosya | Doğrulama |
|---|---|---|
| A Teşhis | `sphirus-human-motion-engine/references/motion-diagnosis.md` | Bu görevin gerçek hatalarında kullanıldı (§3); 3 hipotez tek değişkenli koşularla reddedildi (FootPlacement, faz sayısı, MM DB geçişi) |
| B Destek ayağı / momentum niyetleri | `sphirus-character-camera/references/support-momentum-intents.md` | Başlangıç / kısa giriş / normal duruş ölçüldü; sert fren, viraj, kesiş, 180° testleri tanımlı, bu görevde yalnız regresyon olarak koşuldu |
| C Temas koruyan üretim + retarget | `.../references/contact-authoring.md` | 26 klip bu yöntemle üretildi ve oyunda ölçüldü; 8 doğrulanmış hata örneği eklendi |
| D MM kapsama / geçiş kalitesi | `.../references/mm-coverage.md`, `scripts/clip_inventory.py` | Envanter 134 DB / 1048 klip; dört durum sınıflandırması §4 |
| E Arazi / denge / çevre tepkileri | `.../references/environment-reactions.md` | Kapsama dosya adından; çevre senaryosu koşulmadı → NOT_TESTED |
| F Görsel kalite / regresyon | `sphirus-qa-regression/references/locomotion-visual-qa.md`, `scripts/contactslip.py`, `scripts/stopentry.py` | Metrik ham karelerle doğrulandı (eski hız-eşikli metrik 21–26 cm kaymaları kaçırıyordu) |
| G Hareketten alan tasarımı | `sphirus-level-design-player-flow/references/motion-metrics-space.md` | Duruş / dönüş mesafeleri gerçek koşulardan (yürüme 33 cm, tempolu 115 cm, depar ~2.4 m; depar 90° ~1.9 m taşma); sahnede denenmedi |
| H Kompozisyon / yön bulma / ritim | Mevcut `sphirus-level-art-direction` sahibi; G ona bağlanır (kopya yok) | Salt-okuma |
| I Yaşanmışlık + çevre sanat yönetimi | `sphirus-environment-art/references/lived-in-exterior.md` | AGENTS.md kimlik kuralları test edilebilir kontrol listesi; salt-okuma, oyunda NOT_TESTED; sahne değiştirilmedi |
| J Oyun kamerası + performans kabulü | G dosyası "Traversal acceptance" | Salt-okuma; rota yürüyüşü bu görevde yok |

- Yönlendirme: `sphirus-game-dev-director` kompozisyon tablosuna 5 satır eklendi.
- Kaynaklar `Saved/Codex/SHME_V28_20261015/research_sources.md`:
  - Epic belgeleri ve API: DOCS_PAGE düzeyi.
  - Biyomekanik: ÖZET düzeyi.
  - Videolar (V1–V3): yalnız başlık; "öğrenildi" sayılmadı.
- Gözlem / kaynak / öneri dosyada ayrı etiketli.

## 3. Kök nedenler (kanıtla)
| Şikâyet | Kök neden | Kanıt |
|---|---|---|
| Yürüyüş duruşu büyük, ayak kayıyor | CP "relaxed" duruş klibi adım fazından bağımsız hep ~1.29–1.33 s'den giriyor (sabit tahmini mesafe). Taraf yalnız soket karşılaştırmasıyla seçiliyor. Klip 170 cm/s'den duruyor, bizim yürüyüş 132 cm/s. | Basan ayak her duruşta 10–37 cm kayıyor, 3–5 cm zemine giriyor (6 faz × 2). vb = mx → retarget değil |
| Yürüyüş başlangıcı büyük | Eski başlangıç klibi ayakları kapsülün önüne atıyor. Kapsül ilk 0.3 s'de yalnız ~5.6 cm ilerliyor. | Başlangıçta basan ayak 25–30 cm kayıyor; ilk adım uzun (§7 başlangıç panosu) |
| Kısa basma / iptal | Çok kısa girişte tam CP başlangıcı + 105 cm/s altında eski duruş yolu; ayrıca ince bir "dokunma" tepkisi (ağırlık aktarımı + tek küçük adım) klibi yok | Pencere ölçümü §6.3 |
| Duruş sonunda "bir tık aşağı inme" (yürüme) | Eski klip son çift destek çukurunda bitiyor (V2.7). Yeni klip pelvisi yürüyüş yüksekliğinden doğrudan ayakta durma yüksekliğine taşıyor. | Yürüyüş yüksekliği altına inme 2.8–3.4 → 0.8–1.4 cm |
| Yeni klipler ilk denemede yine kaydı | Dört ayrı teknik tuzak, tek tek ölçülerek bulundu (aşağıdaki liste) | `motion-diagnosis.md` / `contact-authoring.md` hata örnekleri |

Yeni kliplerin ilk denemede kaymasının nedenleri:
1. Başlangıç değerlendiricisinin zaman pini `CP_StartEvalTime` değil, iç içe bir seçim (V2.7 `SHM_StartRightRelaxed` yolu).
2. CP başlangıcı eski "plant" mesafesinde (~51 cm) bırakıyordu; yeni klip döngüyle ancak sonunda eşleşiyor.
3. Kök eğrisi gürültülü 30 fps ölçüm tablosundan üretilmişti (kare kare 93–144 cm/s). Oyun içi konumlara frenleme modeli oturtuldu: dv/dt = −(195 + 1.2·v), 29.5 cm, rms 0.15 cm.
4. ABP'de soket konumları bir kare eski; eşleşen poz klibin 0. karesi, bu yüzden klip 1 kare içeriden (T0 = dt) giriyor.

Ek bulgu: kliplerin bitiş pozu bir sonraki girişi etkiliyor. İlk seçilen bekleme karesi (7.0 s, 3 cm kaçık) sonraki kısa basmalarda kaymayı artırdı. MM'nin kendi oturduğu duruşa (57.8 s) geçince geriledi.

Depar veritabanı eşikleri (V2.7: 230 cm/s, ±110°):
- Bu görevde eşik A/B'si koşulmadı → NOT_TESTED.
- Gözlem: depar dönüşlerinde orta destek kayması p50/p90 ≈ 0 (adım–öteleme uyumu bozulmuyor), ama nadir 36–73 cm olaylar her iki varyantta da var (V2.7'den açık madde).

## 4. Animasyon envanteri — dört durum (yürüyüş kapsamı)
| İhtiyaç | Durum | Ne yapıldı |
|---|---|---|
| Her adım fazında 132 cm/s'den yürüyüş duruşu | Klip var ama uygun değil (giriş zamanı sabit, giriş hızı 170) | 24 faz klibi üretildi → **var ve kullanılıyor** |
| Beklemeden yürüyüş başlangıcı | Klip var ama uygun değil (ayak kapsülün önünde) | L / R aday üretildi; kısa girişte regresyon → üretimde değil |
| Çok kısa basma (ağırlık + tek küçük adım) | Uygun klip yok. `am_Stand_Idle_Step_*` ad olarak var, seçilmiyor, uygunluğu doğrulanmadı | Açık |
| Başlangıç iptali / tekrar basma | Mantık + klip yok | Açık (§8) |
| Tempolu / depar duruşu | Var ve seçiliyor. Tempolu giriş kayması 9–17 cm, depar çökmesi 9–11 cm | Açık (V2.8 kapsamı dışı bırakıldı) |
| Yürüyüş döngüsü | Var ve kullanılıyor; orta destek p90 1.5–2 cm | Değişmedi |
| Dönüşler / çevre | Dosya adına göre geniş içerik | §9 |

## 5. Yapılanlar, dosyalar, geri alma
- **Yeni assetler:**
  - `/Game/GraceRanger/SHME/Animations/V28/A_SHM28_WalkStop_P00..P23` (24 adet).
  - `A_SHM28_WalkStart_L / _R`.
  - Hiçbir veritabanında değiller; yalnız ABP üyelerinden referanslı.
  - Yöntem: üretim döngüsü `A_LB_Walk_Fwd` + bekleme pozu `af_Stand_Idle_NaturalBaseline_Phase275@57.8`; ayak adımları planlı; basan ayak sabit; IK ile bacak. Kaynak klipler değişmedi.
  - Üretici: `Tools/SHME_V28_20261015/v28_gen_startstop.py`.
  - Klip kontrolleri: giriş / bitiş poz hatası 0. Ayak IK hatası ≤ 1.1 cm (3 geç-salınım fazında 4–5 cm, 2–3 kare). Zemine girme ≤ 0.6 cm.
- **Değişen asset:** `ABP_GR_MotionMatchingBase` (+ çocuk `ABP_GR_MotionMatching` yeniden derlendi).
  - `SHM28_*` üyeleri ve `SHM28_StartStop` fonksiyonu (DSL, `SHM_StopTimeLimit`'ten sonra).
  - `CT_GetCPStopSequence` / `CT_GetCPStartSequence` seçici sarmalayıcıları; AnimGraph başlangıç değerlendiricisinin zaman pini sarmalayıcısı.
  - Varsayılanlar: `SHM28_StopMode = 1`, `SHM28_StartMode = 0`. Mod 2 / 3 yalnız karşılaştırma için.
  - Kurucu (idempotent): `install_v28_startstop.py`; terfi: `promote_v28.py`; doğrulama: `verify_v28.py`.
- **Geri alma:**
  - Anında: ABP varsayılanında `SHM28_StopMode = 0` (davranış V2.7'ye döner).
  - Tam: editör kapalıyken `Saved/Codex/SHME_V28_20261015/checkpoint/baseline_v27/ABP_GR_MotionMatching*.uasset` geri kopyalanır (SHA256SUMS mevcut).
  - Ara durumlar `checkpoint/v28*` klasörlerinde.
- **Yaşanmışlık / sahne:** hiçbir sahne, karakter, kamera, kıyafet değişmedi.

## 6. Sonuçlar (senaryo başına)

### 6.1 2×2: klip × mantık (yürüyüş duruşu, 6 faz, 2 tekrar)
| Hücre | İlk 0.25 s giriş kayması ort. / en kötü (cm) |
|---|---|
| Eski klip + eski mantık (V2.7) | 21.1 / 32.6 · 20.9 / 30.4 |
| Eski klip + yeni mantık (faz eşleşmeli seçim, zaman tablosu) | 8.6 / 16.2 · 9.1 / 14.6 |
| Yeni klip + eski mantık (yalnız sol / sağ kuralı) | 13.3 / 20.9 · 11.2 / 22.3 |
| **Yeni klip + yeni mantık** | **2.9 / 4.9 · 3.2 / 4.7** |

Kaynak asset sessizce ezilmedi: dört hücre aynı süreçte anahtarla seçildi.

### 6.2 Üretim (yeni duruş, eski başlangıç) — V2.7'ye karşı
| Senaryo | V2.7 | V2.8 | Not |
|---|---|---|---|
| 3 düz duruş (giriş ort. / en kötü) | 16.5 / 25.0 | 3.2 / 4.4 | taze editör, override'sız |
| Başla-dur ×4 (giriş) | 17.3–17.8 / 24.9–29.3 | 2.6–3.9 / 4.0–5.0 | |
| Faz duruşları ×6 (giriş) | 21 / 30–33 | 3.3–3.7 / 4.5–4.9 | |
| Yeniden kalkış (orta destek p90 / en kötü) | 22.0 / 27.4 | 5.0–5.1 / 6.4–6.7 | |
| Kısa basmalar (giriş, 3 tekrar) | 25.4–25.9 / 26 | 1.5–4.1 / 3–4 | |
| Duruş sonu yürüyüş yüksekliği altı (cm) | 2.8–3.4 | 0.8–1.4 | faz duruşlarında 2.7 (fazdan bağımsız değil) |
| Parmak kalkışı kayması p90 (başla-dur) | 6.3–8.0 | 1.6–4.1 | |
| Düz yürüyüş (regresyon) orta destek p90 / en kötü | 1.95 / 6.4 | 1.52 / 4.4 | regresyon yok |
| ~19 fps (`t.MaxFPS 20`) 3 duruş | 7.5 / 16.0 | 4.4 / 4.7 | gerçekleşen 18.8 fps |
| 60 fps | — | — | **NOT_TESTED**: editör PIE ~35 fps'te kaldı |

### 6.3 Kısa basma / iptal / tekrar basma (pencere başına zemin kayması, 4 tekrar, medyan cm)
| Pencere | V2.7 | V2.8 üretim | Başlangıç adayı (ek) |
|---|---|---|---|
| 0.12 s basma | 10.9 | 14.2 | 21.8 |
| 0.35 s basma | 0.4 | 8.6 | 4.3 |
| 0.6 s basma | 10.9 | 8.8 | 15.0 |
| Yürüyüş duruşu | 26.6 | 10.3 | 11.0 |
| Basma + tekrar basma | 23.8 | 24.7 | 29.4 |
| Çapraz kısa basma | 7.8 | 9.8 | 22.4 |
| 0.3 s basma | 1.3 | 1.7 | 9.1 |

- Duruştan önceki basmalar üretimde V2.7 ile **aynı kod yolu** (yeni duruş 105 cm/s altında devre dışı); farklar tekrardan tekrara değişkenlik (V2.7'nin kendi aralığı 0–47 cm).
- Duruştan sonraki basmalar, bitiş pozu düzeltmesinden sonra V2.7 düzeyinde.
- Başlangıç adayı kısa girişlerde açıkça kötüleştiriyor → terfi edilmedi.

### 6.4 Regresyon (değişmeyen yollar)
- Tempolu / depar duruşu, depar A/D kesişi, hızlı fare dönüşü, W↔W+D, tempolu dönüş: bu senaryolarda `SHM28` hiç devreye girmiyor (telemetri: 0 giriş) → yol aynı.
- Tek koşulu farklar MM seçim değişkenliği. Depar dönüşlerindeki nadir büyük kaymalar (36–73 cm) her iki varyantta var → açık.

## 7. Görseller (`img/`) ve görsel inceleme
| Dosya | Ne gösteriyor |
|---|---|
| `stop_side_base.jpg` / `stop_side_v28.jpg` | Yandan duruş, 0.1 s aralık |
| `stop_side_base_slow.jpg` / `stop_side_v28_slow.jpg` | Aynı duruş, ~22 fps her kare |
| `stop_feet_base.jpg` / `stop_feet_v28.jpg` | Bacak / ayak yakın plan, her kare |
| `stop_diag_base.jpg` / `stop_diag_v28.jpg` | Ön-çapraz sabit kamera |
| `game_base.jpg` / `game_v28.jpg` | Oyun kamerası (kırpma nedeniyle yalnız üst gövde) |
| `start_feet_base.jpg` / `start_feet_candidate.jpg` | Başlangıç: V2.7 vs **üretilmeyen aday** |

Görsel değerlendirme (benim; his kabulü değil):
- **V2.8 duruş:**
  - Son fren adımında hafif diz bükümü.
  - Kısa kapanış adımı; ayaklar ~0.2 s'de yan yana, simetrik duruş.
  - Kollar yanlarda; pop, yana kayan ayak veya ikinci çökme görülmedi.
- **V2.7 duruş:** bir koşuda kollar duruş boyunca belirgin açılıyor. Çapraz görünümde iki varyant kaba hatlarıyla benzer; asıl fark giriş anındaki ayak kayması ve bu dönen kamerada karede zor görülüyor (metrik birincil kanıt).
- **Başlangıç adayı:**
  - Önce ~0.3 s ağırlık aktarımı, sonra normal ilk adım.
  - V2.7'de ilk adım hemen ve çok uzun.
  - Kapsül hızı iki durumda aynı (kontrol gecikmesi eklenmedi), ama ilk görünür adım ~0.3 s sonra. His kararı senin.
- **Kısıtlar:**
  - Gün ışığına karşı silüet.
  - Oyun kamerası kırpması bacakları dışarıda bırakıyor.
  - Yavaş çekim = görüntü dizisi (video dosyası yok).

## 8. Çözülen / kısmi / açık
- **Çözüldü (teknik PASS, his NOT_TESTED):**
  - Yürüyüş duruşunda giriş kayması ve duruş sonu çökme.
  - Duruştan sonra gelen kısa basmalarda V2.7 düzeyi korundu.
- **Kısmi:**
  - Yürüyüş başlangıcı: aday hazır ve normal başlangıçta iyi, ama kısa girişte regresyon.
  - Gerekli olan: "dokunma" yolu (ağırlık aktarımı + tek küçük adım + dönüş) ve başlangıç iptali için ayrı mantık. Ancak giriş taahhüt edilince (≥ ~0.25 s) yeni başlangıç klibi devreye girmeli.
- **Açık:**
  - Tempolu / depar duruşu (giriş kayması, 9–11 cm çökme).
  - Depar dönüşlerinde nadir büyük kaymalar.
  - 60 fps testi; depar DB eşik A/B'si.
  - Kısa basmaların kendi yüksek değişkenliği (V2.7'de de 0–47 cm).

## 9. Sıradaki adım: dönüşler ve çevre tepkileri (kapsama, uygulanmadı)
| Niyet | Projede ne var (ada göre, uygunluk doğrulanmadı) | Sıradaki test |
|---|---|---|
| Geniş viraj | Döngüler + V2.5 CurveLean, V2.7 dönüş sınırları | `mt_*` eğilme + kayma; ayak fazı henüz girdi değil |
| Destek ayağıyla kesiş 45–90° | 85 pivot klibi, `PSD_*_Pivots`, `PSD_DPP_SmallTurn` | Dört duruma göre sınıflandırma; spin vs step turn öndeki ayağa göre [M8] |
| Fren–pivot–hızlanma 180° | `PSD_SHM_Redirect_SprintReversal(_L/_R)`, `PSD_LR_ReversePivots`, 40 reversal klibi | Depar 180° ~1.3 m taşma ölçüldü; giriş fazı + nadir kaymalar |
| Yumuşak / sert iniş | 39 iniş klibi, `am_Jump_LandRecovery` | Ölçülmedi |
| Planlı basamak inişi | Ad olarak yok → "klip yok" adayı | Önce FootPlacement ile basamak / eğim merdiveni |
| Kayma + toparlanma adımı | `SHM_Rec_*` toparlanma adımları var; kayma yok | — |
| Yürürken çarpma | Yalnız ayakta hafif çarpma (6 yön) | Yürüme / tempolu duvar temasında sendeleme olmamalı |

Depar ailesini korumak tam hızı korumak değil; dönüş seçimi açı + hız + giriş değişim hızı + destek ayağı + alan.

## 10. Asset / animasyon önerisi
- Bu görevin ihtiyaçları kendi içeriğimizden üretilen kliplerle karşılandı. Satın alma yok, ücretli servis yok, kaynak dosya dışarı yüklenmedi.
- Sıradaki çevre tepkileri için (yalnız mağaza / belge sayfaları; hiçbir hareket izlenmedi):
  - **GASP** (ücretsiz, yalnız Unreal içinde): önce editörde açıp veritabanlarını listelemek gerek.
  - **Motorica veri seti:** içerik / lisans doğrulanamadı.
  - **MoCap Online Mobility:** ücretli, UE4 iskeleti, tökezleme yok → önerilmiyor.
  - **Simple Bump Reactions:** yalnız Unity → kullanılamaz.
- **Hedefli animatör / mocap brief'i** (SK_Mannequin, kök hareketli, 30 fps, sol / sağ ayak):
  - Yürürken tökezleme-toparlanma (erken / geç salınım).
  - 132 / 300 cm/s'de planlı 15 / 30 cm basamak inişi.
  - Yürürken / tempoluda omuz çarpması.
  - Islak zeminde kısa kayma + toparlanma.
  - Bekleme pozundan çok kısa "dokunma" tepkisi (ağırlık aktarımı + tek küçük adım + dönüş).
