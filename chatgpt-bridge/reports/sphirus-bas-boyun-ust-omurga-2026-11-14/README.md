# SPHIRUS — Baş, boyun ve üst omurga anatomik düzeltme — 2026-11-14

Şikâyet: "Karakterin boynu garip şekilde öne uzanıyor. Önden bakıldığında boyun bölgesinde belirgin bir çizgi/iz görülüyor."

**Durum etiketleri:** IMPLEMENTED · TECH_TESTED (oyun içinde ölçüldü) · VISUALLY_INSPECTED (kareler tarafımdan incelendi) ·
PERFORMANCE_TESTED · USER_ACCEPTED. **Hiçbir başlık USER_ACCEPTED değildir** — görsel kabul sizin denemenizle verilir.
NOT_TESTED / PARTIAL açıkça yazıldı. Tüm ölçümler aktif oyuncu `BP_HybridA_Player` üzerinde, PIE içinde, gerçek karakterden
(görünür beden `Manny` = SKM_MHC_Sph8_BodyMesh + yüz SKM_MHC_Sph8_FaceMesh) alındı. Kullanıcı kayıt dosyası (SFSaveSlot, SHA1
4823d83a…) her batch'te kenara alındı ve aynı dosya geri kondu; her batch sonunda SHA1 doğrulandı (değişmedi).

---

## 1. Kök neden — katman katman (`data/katman_olcumleri.txt`, `evidence/katmanlar_*.jpg`)

Ölçüler (yan düzlemde, + = öne): **boyun eğimi** = neck_01→head doğrusunun dikeyden açısı; **boyun tabanı bükümü** = (neck_01→neck_02
eğimi) − (spine_05→neck_01 eğimi); **baş-köprücük** = başın köprücük orta noktasının ne kadar önünde olduğu (cm).

| Katman (idle, ayakta) | boyun eğimi | spine_05→neck_01 | boyun tabanı bükümü | baş-köprücük |
|---|---|---|---|---|
| Referans/bind pozu (mesh'in kendi duruşu) | 11.9° | −9.2° | **+21°** | 1.6 cm |
| Ham retarget (UEFN → MetaHuman, beden katmanları kapalı) | 12.9–15.3° | +5…+8° | **+2…+4°** | 3.0–3.7 cm |
| + eski duruş katmanı (VI_Spine5 −9°, VI_Head +8°) | 7.1–7.5° | −1…+2° | **0…+3°** | 1.4–1.7 cm |
| + LookAt / baş seviyeleme / tam üretim (eski) | 2.3–7.6° | −5…+1.5° | **~+2°** | 0.2–1.7 cm |

- **İlk ortaya çıktığı katman: ham retarget.** RTG_Sph_UEFN_to_MH (Spine spine_01→05, Neck neck_01→02, Head; hedef retarget-poz
  ofsetleri sıfır, yalnız köprücükler 5°) alt boyun segmentini bind eğriliğinin ~17° önüne bırakıyor ve boyun tabanını
  **düzleştiriyor** (bind 21° → 2–4°).
- Eski duruş katmanı (VI_Spine5 −9 / VI_Head +8, 2026-11-12) göğsü geri yatırdı ama boyun tabanı eğriliğini geri getirmedi; baş
  geriye bükülerek "düz" gösterildi. Yani boyun aslında bind'den **daha dik** duruyordu; "öne uzanma" görünümü boyun açısından
  değil, aşağıdaki şişlikten geliyordu.
- Yüz rig'i (ABP_Face_PostProcess, RigLogic) düz boyun tabanını güçlü boyun ekstansiyonu olarak okuyup **gırtlak düzeltici
  şeklini** (corrective) tetikliyor → alt boyun önünde şişlik ve üstünde çizgi/kıvrım. Yandan bakınca şişlik boğaz konturunu öne
  itiyor; önden bakınca köprücük çukurunun üstünde koyu bir yatay bant olarak okunuyor.
- **Kanıt:** yalnız yüz post-process'i kapatıldığında (aynı poz) şişlik ve çizgi kayboluyor (`evidence/katmanlar_bind_yuzPPkapali_eski_yeni.jpg`:
  satır 1 bind / yüz-PP kapalı, satır 2 eski / yeni). Beden post-process'i kapatmak çizgiyi gidermiyor.
- Çömelmede eski VC_Neck1 −9 / VC_Head −12 boyun tabanını daha da düzleştiriyordu (büküm 8–9°) → şişlik çömelmede de vardı.

## 2. Çizgi nedir? (`data/dikis_analizi.json`, `evidence/malzeme_ab_*.jpg`)

| Aday | Test | Sonuç |
|---|---|---|
| Mesh dikişi (baş/beden kaynağı) | FBX dışa aktarımı + Blender (salt okuma): 92 köşeli kaynak halkası z 137.9 (jugular çentik) … 147.2 cm (ense), x ±13.4 cm | Konum farkı 0 mm, normal açısı 0°, deri ağırlıkları özdeş (L1 = 0). Halka omuz/köprücük çizgisinde, görülen çizgiden aşağıda → **dikiş değil** |
| Malzeme / normal farkı | Gövde M_Sph_Skin_Masked vs baş M_skin_unified_baked anahtarları (Micro Skin, Bent Normal, AO farklı) — gönderilen / orijinal gövde+baş / normal haritası kapalı / AO kapalı / düz malzeme × 3 güneş yönü (eski poz) | Dört varyantta da bant aynı yerde ve aynı biçimde (`evidence/malzeme_ab_gunes0_orijinal_normalsiz_AOsuz_duz.jpg`: sol üst orijinal, sağ üst normalsiz, sol alt AO'suz, sağ alt düz) → doku/normal/AO kaynaklı değil, **şekil kaynaklı** |
| Gölge | Güneş 0° / 90° / 180° | Bant ışıkla şiddet değiştiriyor ama her yönde aynı yerde → gölge, şeklin sonucu |
| **Deformasyon kıvrımı** | Yüz PP kapalı / açık; duruş adayları | Yüz rig düzelticisi açıkken var, kapalıyken yok; boyun tabanı bükümü ≥ ~14° olunca kayboluyor → **kök neden** |

Not: Önden bakınca köprücük çentiğinin üstünde kalan **hafif** yatay çukur bind pozunda da var (mesh anatomisi: suprasternal
çentik); bu korunmalı, saklanmadı.

## 3. Düzeltme — eski ofsetlerin üstüne ekleme değil, değiştirme (`changes/degisiklik_manifesti.md`)

ABP_Sph_Body_GASP (görünür bedenin anim blueprint'i, aktif `BP_HybridA_Player`) duruş katmanının değerleri **yerine** bind
eğriliğini geri getiren değerler yazıldı (yeni katman, yeni node, yeni sistem yok; yüz/saç/kirpik/beden varlıkları değişmedi):

| Değişken (roll, + = öne büküm) | Eski | Yeni | Amaç |
|---|---|---|---|
| VI_Spine3 | 0 | −4 | üst göğüs hafif açılır |
| VI_Spine5 | −9 | −12 | alt boyun segmenti bind eğimine döner |
| VI_Neck1 | 0 | **+12** | boyun tabanı eğriliği geri gelir (düzelticiyi tetikleyen düzlük kalkar) |
| VI_Neck2 | 0 | 0 | — |
| VI_Head | +8 | −2 | baş geriye bükülmüyor; göz hattı seviyede |

Çömelme taşıması ayrı ölçüldü (aynı PIE oturumunda adaylar sırayla, 5 örnek × 2 tekrar; tek örnek gürültülü). Bu turdaki ilk
tahmin (g1) başı sarkıttığı için **değiştirildi**, üstüne eklenmedi (`data/comelme_olcumleri.txt`):

| Değişken | Eski (2026-11-12) | g1 (reddedildi) | Yeni (t1) |
|---|---|---|---|
| VC_Spine5 | +7 | +4 | −8 |
| VC_Neck1 | −9 | +6 | 0 |
| VC_Neck2 | 0 | −6 | −6 |
| VC_Head | −12 | −14 | +2 |

| Çömelik ölçü (düz harita) | Eski | g1 | Yeni (t1) |
|---|---|---|---|
| idle boyun eğimi | 41° | 50° | **32°** |
| idle boyun tabanı bükümü (≥ ~14 hedef) | 9° | — | **18°** |
| idle baş-köprücük | 9.9 cm | — | **7.3 cm** |
| idle göz hattı | 32 | — | 31 |
| çömelik yürüyüş boyun eğimi / büküm | 62° / −10° | — | 54° / −2° |


Ayakta idle sonuç (gerçek harita, aynı oturum, aynı ışık): boyun eğimi 6.0° → 9.5° (bind 11.9), boyun tabanı bükümü 2° → 16° (bind
21), baş-köprücük 1.2 → 1.1 cm, CVA 84 → 80.5 (bind 78.1), göz hattı 30.2 → 33.3 (bind 33.4). **Baş göğse yaklaştırılmadı**; baş
aynı yerde, boyun bind eğriliğiyle taşınıyor.

## 4. Görsel kanıt (önce = eski değerler çalışma anında uygulanmış, sonra = kaydedilen değerler; aynı PIE oturumu, aynı ışık)

- `evidence/ayakta_once_sonra_yenidenbaslatma_sonrasi_on_yan_yakin.jpg` — **editör yeniden başlatıldıktan sonra** (kayıtlı
  değerler diskten okundu): üst satır önce, alt satır sonra; ön, yan (saçsız), boyun önü yakın, 3/4 yakın (güneş 90°).
- `evidence/onde_yanda_once_sonra_sacsiz_ve_sacli_yan.jpg` — yan (saçsız / saçlı) ve ön, önce | sonra.
- `evidence/yakin_boyun_onden_3_isik.jpg` — çizgi bölgesi yakın, güneş 0° / 90° / 180°, önce | sonra.
- `evidence/yakin_boyun_34_3_isik.jpg` — 3/4 yakın, 3 ışık, önce | sonra.
- `evidence/sacli_34_ve_on.jpg` — saç görünür, 3/4 ve ön.
- `evidence/katmanlar_bind_yuzPPkapali_eski_yeni.jpg` — bind | yüz-PP kapalı | eski | yeni (ön + yan).
- `evidence/comelik_gercek_harita_34_once_sol_sonra_sag.jpg` — gerçek harita, çömelik idle, 3/4.
  - Sol, eski (head_z 244, boyun 41.6°, büküm 8.6°, baş-köprücük 10.0 cm): çene kalkık, baş geriye bükük, çene altında şişlik.
  - Sağ, yeni (head_z 246, boyun 31.5°, büküm 18.1°, baş-köprücük 7.2 cm, göz hattı 31.2): baş seviyede, boyun eğriliği doğal.
  - İki kare editör yeniden başlatıldıktan sonra, iki ayrı PIE oturumunda, aynı kamera tanımı ve aynı yerde alındı. Aynı oturumda
    tekrarlanan denemede ilk C basışı bazen çömelmeye girmiyor ya da karakter kalkıyor; bu kareler baş yüksekliğiyle elendi
    (`data/comelik_gercek_harita_sonra_olcum.jsonl`).
  - Gerçek haritada çömelik **ön / yakın boyun** karesi için kamera kadrajı tutmadı (yaprak / gövde). Bu kareler rapora konmadı.
    Çömelik ön görünüm için düz haritadaki kayıtlar kullanıldı.
- `evidence/comelik_yuruyus_yan_sacsiz_once_sonra.jpg` — düz harita, çömelik yürüyüş yan (saçsız), önce | sonra.
- `evidence/hareket_eski_ust_yeni_alt_idle_comelik_yuruyus_ziplama.jpg` — düz harita, aynı plan:
  - üst satır eski, alt satır yeni;
  - sütunlar: idle, çömelik idle, çömelik yürüyüş, zıplama.
- `evidence/comelik_yuz_kirpilmasi_once_sonra.jpg` — sınır kutusu düzeltmesi öncesi çömelik yakın kadrajda yüz ve saç
  çizilmiyordu (başsız gövde); düzeltme sonrası çiziliyor. Yalnız kırpılma gösterimidir; duruş karşılaştırması değildir.
- `evidence/sac_gorunumu_sinir_duzeltmesi_once_sonra.jpg` — sınır kutusu düzeltmesi saçın görünümünü değiştirmiyor.
- `evidence/odun_alma_eski_ust_yeni_alt.jpg` — gerçek harita, odun alma. Baş her karede çiziliyor (iki kayıtta da sınır kutusu düzeltmesi açık; 2026-11-13 şikâyetindeki kaybolma bu kayıtlarda görülmedi).

## 5. Hareket içinde doğrulama (`data/hareket_boyun_30_60hz.txt`, `videos/`)

Gerçek tuş girdisi, düz test haritası, yandan izleyen kamera boyna nişanlı, kare başı boyun ölçümü (30 Hz sabit adım; aynı plan
60 Hz'de de):

Kayıtlar editör yeniden başlatıldıktan sonra alındı. **Eski** = eski değerler çalışma anında uygulanmış (30 Hz). **Yeni** =
kaydedilen değerler, 30 Hz ve 60 Hz (aynı plan).

| Bölüm | boyun eğimi eski → yeni 30 / 60 Hz (ort.) | baş-köprücük cm eski → yeni 30 / 60 | göğüs (s5→n1) eski → yeni |
|---|---|---|---|
| idle | 6.2 → 10.7 / 11.2 | 1.1 → 1.4 / 1.5 | −2 → −9 |
| yürüyüş | 13.0 → 18.2 / 18.3 | 2.3 → 2.6 / 2.6 | −4 → −11 |
| jog | 14.2 → 19.3 / 19.2 | 3.0 → 3.3 / 3.3 | 3 → −4 |
| sprint | 27.4 → 32.4 / 32.5 | 6.0 → 6.2 / 6.2 | 14 → 7 |
| fren / duruş | 23.6 → 28.6 / 28.2 | 5.3 → 5.5 / 5.4 | 13 → 6 |
| ±60° dönüşlü yürüyüş | 11.2 / 16.1 → 16.3 / 21.1 (60 Hz 16.0 / 21.2) | 2.0 / 3.0 → 2.2 / 3.3 | −3 / −1 → −10 / −8 |
| çömel + çömelik idle | **38.3 → 30.1 / 30.2** | **9.0 → 6.6 / 6.6** | 28 → 13 |
| çömelik yürüyüş | **61.3 → 52.2 / 52.4** | **13.8 → 12.3 / 12.4** | 70 → 55 |
| çömelik duruş | 65.0 → 56.1 / 55.4 | 13.8 → 12.4 / 12.3 | 68 → 53 |
| kalkış | 22.5 → 26.5 / 26.4 | 5.0 → 5.0 / 5.0 | 10 → 2 |
| zıplama + iniş | 25.6 → 31.7 / 31.8 | 5.5 → 6.0 / 6.0 | 11 → 5 |
| koşu sonrası idle (nefes) | 10.8 → 15.8 / 15.5 | 2.2 → 2.5 / 2.4 | 1 → −6 |
| odun alma (eğilme, max) | 73 → 81 | 14.2 → 14.3 | 51 → 47 |
| iki elle odun taşıma (idle) | 14.5 → 19.7 | 1.8 → 2.1 | −13 → −20 |

Okuma:
- **30 Hz ile 60 Hz aynı** (fark ≤ 0.7°, ≤ 0.1 cm) → kare hızına bağlı bir davranış yok.
- Ayakta ve hareket hâlinde, neck_01→head doğrusu eskisinden ~5° daha eğik. Bunun nedeni boyun tabanının bind eğriliğine
  (bind 11.9°) dönmesi ve göğsün ~7° geri açılması. **Başın köprücüğe göre konumu yalnız 0.2–0.5 cm değişti**: baş öne
  uzatılmadı, boyun kilitlenip dikleştirilmedi. Boyun hareketle birlikte bükülmeye devam ediyor (min–max aralıkları eskisi kadar
  geniş, `data/hareket_boyun_30_60hz.txt`).
- Çömelmede baş belirgin biçimde geri geldi (idle 9.0 → 6.6 cm, yürüyüş 13.8 → 12.3 cm). Çömelik yürüyüşte boyun eğiminin hâlâ
  52° olmasının nedeni gövdenin 55° öne eğilmesi (GASP çömelik yürüyüş animasyonunun kendisi). Boyun gövdeye göre artık geriye
  bükülmüyor. Gövde eğimi bu işin kapsamı dışında bırakıldı → **PARTIAL**.
- Odun almada eğilmenin dibinde boyun eğimi 73° → 81°. Montaj pozu, ve baş konumu aynı (14.3 cm). Taşıma sırasında göğüs daha
  geride (−20°). Kareler: `evidence/odun_alma_eski_ust_yeni_alt.jpg`. Belirgin bir görsel fark görmedim → **PARTIAL**: odun
  alma ve taşıma pozu bu işte ayrıca ayarlanmadı.
- Videolar (`videos/`): yandan eski / yeni 30 Hz, yeni 60 Hz, 3/4 yeni ve odun alma eski / yeni (küçültülmüş).

## 6. Durum

| Başlık | IMPLEMENTED | TECH_TESTED | VISUALLY_INSPECTED | PERFORMANCE_TESTED | USER_ACCEPTED |
|---|---|---|---|---|---|
| Kök neden + çizgi sınıflandırması (dikiş / malzeme / gölge / kıvrım) | — (analiz) | EVET | EVET | — | HAYIR |
| Ayakta boyun taşıması (VI_*) | EVET | EVET (idle, yürüyüş, jog, sprint, fren, dönüş, zıplama, nefes) | EVET (ön / yan / 3/4 / yakın, 3 ışık) | NOT_TESTED* | HAYIR |
| Çömelme boyun taşıması (VC_*) | EVET | EVET (idle + yürüyüş, düz + gerçek harita) | EVET (çömelik yürüyüş PARTIAL, gövde eğimi animasyonda) | NOT_TESTED* | HAYIR |
| Yüz / saç sınır kutusu (başsız çizim hatası) | EVET | EVET (çömelik / eğik bakış: yüz `rendered = True`) | EVET | NOT_TESTED* | HAYIR |
| Editör yeniden başlatma sonrası aynı sonuç | — | EVET (değerler diskten, kirli paket yok, BP / ABP güncel) | EVET | — | HAYIR |
| 30 / 60 FPS | — | EVET (aynı plan, fark ≤ 0.7°) | EVET | — | HAYIR |
| Odun alma / taşıma | dolaylı | EVET | PARTIAL (eğilmede boyun +8°, poz montajın) | — | HAYIR |
| Maske inceleme | dolaylı | PARTIAL (önceki turda nefes / maske kareleri; bu turda ayrı ölçüm yok) | PARTIAL | — | HAYIR |
| Vault / tırmanma, gamepad | — | NOT_TESTED | NOT_TESTED | — | HAYIR |

\* Değişiklik yalnız mevcut bir anim düğümündeki sabit değerleri ve 4 bileşende "ebeveyn sınır kutusunu kullan" bayrağını
değiştiriyor: yeni düğüm veya tick yok. Ebeveyn sınır kutusu, kendi kutusunu hesaplamaktan daha ucuz. Yine de kare süresi
ölçülmediği için **NOT_TESTED**.

Bilinen sınırlar (gizlenmedi):
- Önden bakınca köprücük çentiğinin üstünde kalan **hafif** yatay çukur bind pozunda da var (anatomi). Saklanmadı, koyu bant
  hâline gelen şişlik giderildi.
- Çömelik yürüyüşte gövde 55° öne eğik (animasyonun kendisi); boyun buna göre artık doğal bükülüyor ama genel duruş değişmedi.
- Yüz / saç sınır kutusu hatası büyük olasılıkla 2026-11-13'teki "odun alırken baş kayboluyor" şikâyetinin de kaynağı: düzeltme
  sonrası odun alma kayıtlarında baş her karede görünüyor. Bu bağlantı, sizin oyun içi denemenizle doğrulanmalı.

## 7. Geri alma

- Manifestler (kapılı çalıştırıcının doğrulanmış yedekleri):
  - `day_neck_apply2_230222`: adım 2'yi geri almak için ABP + BP_HybridA_Player;
  - `day_neck_apply_201111`: adım 1 için ABP.
- Ek kopyalar:
  - `%USERPROFILE%\SphirusCheckpoints\Neck_Step2_20261114\`: adım 2 öncesi;
  - `%USERPROFILE%\SphirusCheckpoints\Neck_Pre_20261114\`: bu işten önceki ABP.
- Yalnız değer düzeyinde dönüş: `changes/degisiklik_manifesti.md` tablolarındaki "Önce" değerlerini ABP_Sph_Body_GASP
  varsayılanlarına yazmak ve BP_HybridA_Player'da 4 bileşenin `Use Attach Parent Bound` değerini kapatmak yeterli.
- Dosya geri koyma işi editör kapalıyken yapılmalı (binary varlık).
