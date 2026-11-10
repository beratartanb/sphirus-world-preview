# fill_readme3.py: fill measured results into the Relaxed + SHME full-body report README.
import io
R='Saved/ChatGPTBridge/reports/sphirus-gasp-relaxed-shme-fullbody-2026-11-10/'
p=R+'README.md'; s=io.open(p,encoding='utf8').read()
rep={
'{{KT_STATUS}}':'**TECH_PASS** yürüme 45/135, sprint 45/180; **PARTIAL** sprint 135 (1,5 s içinde 4–5 klip değişimi)',
'{{JUMP_STATUS}}':'Gerçek olay: yürürken küçük basamaktan 0,1 s düşüş → "boşluğa basma + hafif iniş" klibi (0,9 s); Normal set aynı yerde iniş seçmiyordu → VISUAL_REVIEW_REQUIRED. Yerdeyken zıplama-başlangıç veritabanları ayrıca filtrelendi (gerçek zıplama çalışıyor)',
'{{CHOP_STATUS}}':'**TECH_PASS** (kilit mekanizması: hareket girdisi kilitliyken 32 s\'de 0 kırılma; serbest beklemede 55 s\'de 2). Gerçek istasyonun içinde: **NOT_TESTED** (bu protokolde E istasyonu açmadı, dün de açmamıştı)',
'{{SAVE_STATUS}}':'**TECH_PASS** (oyun içi `LoadGame(IgnorePlayerLocation=False)` konum/yön birebir, sonra yürüyüş 165); menü üzerinden: NOT_TESTED',
'{{FPS_STATUS}}':'**TECH_PASS** (sabit 30 ve 60 kare/s adımda aynı klip dizisi ve duruş süreleri); gerçek kare süresi/GPU maliyeti ölçülmedi',
'{{WALK30}}':'1 başlangıç klibi 3,2 s + 26,8 s tek `M_Relaxed_Walk_Loop_F`, başa dönme 0; basan ayak kayması medyan 6,5 / p75 16,8 cm/s (Normal: 9,1 / 55,5)',
'{{EFFORT_TABLE}}':'''Plan: rested sprint → 3 ardışık sert tersleme → 2 s dur → tersleme → 5 s dinlen → sprint/tersleme. Tam tablo `data/effort_ab_pr1.md`; videolar `videos/B_final_effort_on.mp4`, `B_final_effort_off.mp4`.

| Ölçüt | Efor kapalı | Efor açık |
|---|---|---|
| 1. sert terslemeden sonra ulaşılan hız | 571 | 570 (ilk manevra kendini yavaşlatmıyor) |
| 3. ardışık terslemeden sonra ulaşılan hız | 528 | 500 |
| Bu noktada bırakma anındaki hız | 505 | 395 |
| Yorgunken sprint duruşu | 0,80 s / 248 cm | 0,90 s / 277 cm (fren gücü eforla −%15) |
| En düşük ivme çarpanı (AccScale) | 1,00 | 0,78 |
| 5 s dinlenmeden sonraki sprint | 585 | 578 (E 0,96 → 0,39) |
| Pelvis düşüşü / omuz sallanması (görünür) | 12–26 cm / 5–16 cm | benzer (fark < %10) |

Okuma: efor hız, ivme, fren süresi ve toparlanmada ölçülüyor; komut gecikmesi yok. Görünür bedende fark küçük (nefes + 2° efor eğimi): **görsel tarafı PARTIAL / VISUAL_REVIEW_REQUIRED**.''',
'{{TURNS}}':'''**Klavye (kamera sabit, düz sahne, `KT_turnsT_pr2`, `KT_turnsS_pr2` yan):**
| Dönüş | Giriş → en düşük → çıkış (cm/s) | Yeni yöne ulaşma | Seçilen klipler |
|---|---|---|---|
| Yürüme 45° | 165 → 165 → 165 | 0,13 s | döngü devam (MM yön) |
| Yürüme 135° | 165 → 81 → 165 | 0,23 s | `Walk_Turn_180_R_Lfoot` |
| Sprint 45° | 585 → 576 → 585 | 0,27 s | `Transition_Run_to_Sprint` → `Sprint_Loop_F` |
| Sprint 135° | 585 → 169 → 571 | 0,67 s | `Sprint_Turn_180` → `Run_Turn_180` → `Transition_Walk_to_Sprint` → `Sprint_Reface_090` (**PARTIAL**: değişim fazla) |
| Sprint 180° | 573 → 3 → 550 | 0,53 s | `Sprint_Turn_180_R_Rfoot` → `Run_Turn_L_180` → `Transition_Walk_to_Sprint` |
180°'de eski yön enerjisi söndürülüp (573 → 3) yeni yöne itiş geliyor; basan ayağa göre sol/sağ varyant seçiliyor. Bahçe rotasındaki ilk klavye kaydında sprint 90°'de hız 0,1 s'de 575 → 28'e düştü: bu bir engele çarpmaydı (yön tersine sekti), düz sahnede tekrarında yok.

**Fare (yürürken 360°/s ve 150° süpürme, sprintte 360°/s; `videos/B_final_mouseturns.mp4`):** yürürken Relaxed "spin" klipleri (gövde dönerken adım akışı), dururken yerinde 90/135 dönüş, sprintte `Sprint_Turn_090`. Kamera yaw'ı tek başına fren üretmiyor (efor/fren girdi–hız açısına bakıyor). Görünür pelvis–kapsül ofseti p95 23,7 / en çok 29,4 cm (GASP Offset Root Bone sınırı 30); hızlı fare dönüşünde basan ayak kayması medyan 22 cm/s (düz yürüyüşte 5–7) → **PARTIAL / açık** (ayak kilidi çıkış yolu bu turda düzeltilmedi).''',
'{{REGRESSION}}':'''| Test (gerçek oyuncu) | Sonuç | Kanıt |
|---|---|---|
| Ev içi koridor, Shift | En fazla 150 cm/s, koşu yok → TECH_PASS | `B_final_hall150` |
| Evden dışarı geçiş | NOT_TESTED (test rotası 5,6 s'de duvara çarptı; kapı rotası bulunamadı) | `data/HO_out_pr1.json` |
| Hareket kilitliyken bekleme kırılması | 32 s'de 0 → TECH_PASS | `data/IG_gate_pr2.json` |
| 55 s bekleme | 2 Relaxed kırılma (11,3 s ve 39,3 s), kapsül kayması 0 → TECH_PASS, görünüm VISUAL_REVIEW_REQUIRED | `B_final_idle55` |
| Gerçek zıplama (yürürken, sprintte) | Zıplama montajı + Relaxed havada/iniş klipleri → TECH_PASS | `B_final_jump` |
| Kayıt / yükleme (oyun içi) | Konum ve yön birebir; yükleme sonrası yürüyüş 165 → TECH_PASS | `data/reg_save_pos_pr2.txt` |
| Sola/sağa yürüme kadrajı | Görünür pelvis–kapsül p95 8,2 cm; kamera zinciri değişmedi | `B_final_strafe` |
| Kıyafet / yüz / saç | Değişmedi (aynı MetaHuman) | tüm videolar |
| Derleme | Oyuncu + 9 başvuran BP + iki AnimBP + bileşen: hatasız | `q_compile` |
| Kullanıcı kaydı | SHA1 `8622025b…` korundu (bkz. §13) | — |
| 18 iş montajı (yatak, dolap, maske, kesme, şömine, çay) gerçek girdiyle | NOT_TESTED bu turda (montaj katmanına dokunulmadı; dünkü teknik test geçerli) | — |''',
'{{FPS}}':'''Sabit adımlı kayıtlar: 30 kare/s (adım ort. 0,0345 s) ve 60 kare/s (0,0167 s) aynı girdiyle aynı klip dizisi; duruş süreleri 0,47/0,43 s (yürüme), 0,83/0,83 s (sprint). Değişen tek şey bazı geçişlerde sol/sağ ayak varyantı (faza bağlı). Gerçek zamanlı kare süresi, GPU/CPU maliyeti ve düzensiz kare (20/120) testleri yapılmadı → **NOT_TESTED**. Editör bellek kullanımı 17–22 GB (değişmedi).''',
'{{OPEN}}':'''1. Kullanıcı oynayarak kabul etmedi: Relaxed duruşu, omuz/kol görünümü, frenin ağırlığı ve sprint duruşundaki öne katlanma görsel karar bekliyor.
2. Sprint 135° dönüşlerinde klip değişimi fazla (PARTIAL).
3. Fareyle sert dönüşte kök ofseti 20–29 cm ve basan ayak kayması (PARTIAL).
4. Küçük basamaktan inişte 0,9 s'lik iniş klibi (ağır görünebilir).
5. SHME beden katmanının genliği küçük; görünür efor farkı sınırlı.
6. Önceki SHME'nin proje-sahipli fren/itiş klip üretimi ve ilk adım öncesi ağırlık aktarımı (V2.52) bu GASP mimarisinde yeniden kurulmadı; Relaxed klipleri bu rolü üstleniyor.
7. Cook/paket, gerçek FPS/performans, eğim/merdiven, kapıdan dışarı geçiş, gerçek istasyon akışı, menüden kayıt/yükleme, 18 iş montajının gerçek girdiyle testi: NOT_TESTED.
8. GASP traversal / çarpışma kanalları: dokunulmadı.
9. Koşu hızı 375 cm/s, brif bandının (280–330) üstünde (klip adım uzunluğu korunmak için).''',
'{{VIDEOS}}':'''Hepsi PIE, sabit oyun adımı, gerçek hızda kodlandı, oyun görüş alanı kırpması düzeltilmiş kodlayıcıyla (kare 5,168 → 1515,1090; sol 200 px hatası yok — `frames/` örnekleriyle aynı kadraj).
| Video | İçerik |
|---|---|
| `A_normal_*` (loco, phys, mouseturns, side, q34) | GASP Normal (bu turdan önceki üretim) |
| `C_coremotion_side`, `C_coremotion_loco` | Core Motion oyuncusu (karşılaştırma) |
| `B0_relaxed_before_clavfix_loco` | Relaxed, köprücük düzeltmesinden önce |
| `B_final_loco`, `B_final_phys` | yürüme→koşu→sprint→duruş; sprint-bırak-S-W-S (fren/tersleme) |
| `B_final_keyturns_flat`, `B_final_keyturns_side` | klavye 45/135/180, yürüme ve sprint (arka / yan kamera) |
| `B_final_mouseturns`, `B_final_strafe` | fare dönüşleri; kamera sabit A/D/W+A/W+D |
| `B_final_side`, `B_final_q34`, `B_final_front` | yakın yan / 3-4 arka / 3-4 ön beden görünümü |
| `B_final_walk30`, `B_final_sprint18`, `B_final_idle55` | uzun yürüyüş, uzun sprint, bekleme |
| `B_final_effort_on`, `B_final_effort_off` | efor A/B, aynı girdi |
| `B_final_hall150`, `B_final_jump`, `B_final_fps60` | ev içi kural, zıplama, 60 kare/s |'''}
for k,v in rep.items():
    assert k in s,k; s=s.replace(k,v)
assert '{{' not in s, s[s.index('{{'):s.index('{{')+40]
io.open(p,'w',encoding='utf8',newline='\n').write(s); print('README filled',len(s.splitlines()),'lines')
