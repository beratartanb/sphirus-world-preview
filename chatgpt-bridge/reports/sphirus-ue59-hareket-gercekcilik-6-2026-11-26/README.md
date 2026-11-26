# SPHIRUS UE 5.9 — Hareket gerçekçiliği, tur 6 (2026-11-26)

Başlangıç: tur 5 raporu (commit c499ab8). Oyuncu: `BP_HybridA_Player` (sürücü UEFN mankeni + görünen MetaHuman beden `Manny`). Test haritası `L_Sph_MoveTest`, performans `L_GR_SphirusHouse`.

**Bu raporda hiçbir madde kullanıcı tarafından kabul edilmiş değildir (USER_ACCEPTED yok).** Aşağıdaki PASS'ler teknik doğrulamadır; görsel / oyun hissi onayı sizin oynamanıza bağlıdır.

## Kanıt kuralları
- Son kayıtların hepsi (`pf_*`) **kaydedilmiş sürüm, editör yeniden açıldıktan sonra** alındı. af3/af4 kayıtları kanıt olarak kullanılmadı.
- Tüm temas ve düşme testleri **IMP_PLAN / FL_PLAN kapalıyken**, gerçek nesnelerle yapıldı: fırlatılan fizik kutusu, direk, 7 m platformdan düşüş, masa.
- Kayıtlar sabit 33 ms oyun adımıyla alındı; bunlar FPS ölçümü **değildir**. Performans ayrı olarak gerçek zamanlı ölçüldü (aşağıda).

## Yeniden açma doğrulaması
Editör kapatılıp açıldıktan sonra:
- `RTG_Sph_UEFN_to_MH` 'Run IK Rig' zincirleri: LeftLeg/RightLeg IK açık, **LeftArm/RightArm IK kapalı** (kalıcı).
- Oyuncu değerleri korunuyor (RC_FallV 700, RC_Mass 60, FL_GuBlend 0.1, FL_GndMax 1.6, FL_TryMax 6, LG_On 1, PS_DAMin -24, CA_Rad0 9.3).
- B14 kıyafetleri ve ledge klipleri mevcut.
- Kullanıcı kayıt dosyası değişmedi: sha1 10201b8b41b7.

## Kök nedenler ve düzeltmeler

### 1. Açık kollar (idle'da kollar gövdeden açık)
- **Kök neden:** retarget'ta kollar IK ile çözülüyordu. Hedef eller geniş omuzlu UEFN kaynağın el konumuna (omuz 35 cm, bizim beden 24.5 cm) yerleştiriliyor ve kollar dışarı açılıyordu. Ayrıca kolun FK retarget pozu hizasızdı.
- **Düzeltme:** kol zincirlerinde IK kapatıldı ve kol pozu otomatik hizalandı (`c_rtg_armfk.py`, `c_rtg_align.py`).
- **Bu turda bulunan tuzak:** zincirleri listeden *silmek* kaydı geçmiyordu (Unreal yüklerken geri ekliyor). Bu yüzden kalıcı `enable_ik=False` bayrağı kullanıldı.
- Postür kol servosunun alt sınırı -14° → -24° yapıldı. Kol–uyluk mesafesi artık ölçülen uyluk yarıçapıyla hesaplanıyor (kalçada 9.3 cm, dizde 6.0 cm). Yürüdükten sonra açık kalma süresi 14 s'den kısaldı (sönüm 6°/s).
- **Son kayıtlarda:** idle abdüksiyon 6–8°, dirsek 23–35°. Yürüyüş/tempo/koşu/geri yürüyüşte kol uyluğa girmiyor. Tek istisna yan yürüyüş (A/D): karelerin %1'inde en fazla 4.3 cm.

### 2. Kıyafet silüeti
- İzolasyon (gri beden / kıyafetli / postür kapalı) gösterdi ki beden formu sorunlu değil. Mavi üst kürek kemiklerinden tahta gibi sarkıyordu.
- B14 kıyafetlerinde sırt ve yanlar bedene çekildi (0.7 cm ofset). Bedene dokunulmadı.
- Üstün normal sapması (p90 45°) **kaynak modelde zaten var**; keep_normals kaynaklı değil, düzeltilmedi (AÇIK).
- Görsel: `evidence/garment_b13_b14.jpg`.

### 3. Gerçek temas → bölgesel tepki
- ReceiveHit hem kapsülde hem sürücü mesh'te. Bölge şu sırayla belirleniyor:
  1. mesh kemiği;
  2. baş/göğüs/pelvisten temas noktasına çizgi yoklaması;
  3. yükseklik.
- **Yeni:**
  - Hareketli bir cismin hızı çarpışma *sonrası* okunduğu için 1400 cm/s kutu 380 cm/s görünüyordu. Artık temasın gerçek impulsu da ölçülüyor (|NormalImpulse| / 60 kg). Aynı kutu şimdi 878 olarak okunuyor.
  - 700 üstü darbe tüm bedeni etkiliyor ve düşürüyor.
  - Fizik cismi darbelerinde itme yönü cisimden uzağa (önceden kutuya doğru düşüyordu).

### 4. Düşmeler
- **Yer fazı:** sabit 0.8 s yerine gerçek temasa bağlı (pelvis veya göğüs zeminden 30 cm içinde, en az 0.15 s). Süre sadece yedek (1.6 s). Ölçülen: drop 0.17 s, kutu darbesi 0.77 s.
- **Sırt üstü kalma:** dönme denemeleri 6'ya çıktı, yön değişiyor ve her denemede %25 güçleniyor.
- **Kalkış öncesi alan kontrolü:** ayakta kapsül pelvis üstüne sığmalı.
  - Sığmazsa ileri, geri, sağ ve sol 45 cm denenir.
  - Hiçbiri boş değilse yerde bekler ve 0.5 s'de bir tekrar dener; duvara veya masanın içine kalkmaz.
- **Kalkış başlangıcı pozu (üç deneme):**
  - v1: fizik kapatılıp aynı karede omurga/bacak tekrar açılıyordu, gövde 0.2 s'de dik oturuşa kırbaçlanıyordu (`evidence/fl8_drop_sheet2.jpg`).
  - v2: fizik açık bırakıldı; pelvis kök gövde olduğu için mesh pelvisi takip etti ve karakter havada yuvarlandı (`evidence/fl9_drop_sheet.jpg`).
  - **v3 (son):** tüm gövdeler tek seferde kinematik yapılıyor, kalkış klibi 0.1 s'de karışıyor. Başlangıç pozu, yer fazında motorların zaten çektiği yüzüstü pozu. Pop yok (`evidence/pf_falls.jpg`, üst satır).
- Yerde veya asılıyken zıplama girişi hiçbir şey yapmaz.

### 5. Ledge (kenara tutunma)
- AAMS braced klipleri sürücü iskeletine retarget edildi ve kök hareketleri geri yüklendi.
- Tutunma yalnızca düşerken, 45 cm erişim içindeyse ve gövde için yer varsa olur. Ulaşılamayan kenara ışınlanma yok.
- Tırmanma, bırakma ve ulaşılamayan kenar test edildi.
- **Yeni hata bulundu ve düzeltildi:** itilip havaya kalktığında uçan kutuyu "kenar" sanıp havada asılı kalıyordu.
  - Artık yalnızca statik yüzeylere tutunuyor.
  - Asılıyken her karede duvar kontrol ediliyor; duvar yoksa bırakıyor.

### 6. Çömelme + zıplama
- Çömelikken zıplama yok. Giriş bekletilmiyor, kalkınca gecikmiş zıplama olmuyor (pf_cjump: dikey hız hep 0).

## Ortak beden durumu (veri akışı ve öncelik)

| Aile | Sahip | Ne yapar |
|---|---|---|
| `PS_*` / `CA_*` | postür / kol | Kol abdüksiyonu, kol–uyluk mesafesi |
| `CT_*` | temas öngörüsü | Duvar/masa öncesi fren, el desteği, eğilme |
| `RC_*` | gerçek temas | Bölge, hız/impuls, darbe yönü |
| `IMP_*` | darbe tepkisi | Bölgesel fizik karışımı, destek adımı itişi |
| `FL_*` | düşme | Ragdoll, yer fazı, dönme, alan kontrolü, kalkış |
| `LG_*` | ledge | Tutunma, asılma, tırmanma, bırakma |
| `SphMotion` | `E` / `Fat` | Efor, yorgunluk, hız ve fizik gücü çarpanı |

Öncelik kuralları:
- `FL_State > 0` iken yeni temas tepkisi ve ledge algılama kapalı. Zıplama da kapalı.
- `LG_State > 0` iken zıplama sadece "tırman" anlamına gelir.
- Yorgunluk düşme motor gücünü (`FL_Str`), darbe direncini (`IMP_FatK`) ve kalkış hızını (`FL_Rate`) düşürür.

Tek bir ortak bileşen henüz yok; kurallar oyuncu Blueprint'inde. **KISMİ.**

## Performans (gerçek zamanlı, PIE, kayıt aracı kapalı, CSV profiler)

Ev haritası patika rotası: idle 3 s → yürüme 6 s → koşu 4 s → duruş 3 s. Tur-6 sistemleri (gerçek temas + ledge) açık/kapalı olarak karşılaştırıldı.

| Çalışma | Kare süresi p50 / p95 | GPU p50 |
|---|---|---|
| açık (a2) | 28.8 / 32.2 ms | 27.5 ms |
| kapalı (b1) | 27.8 / 30.1 ms | 26.4 ms |
| kapalı (b2) | 29.7 / 33.1 ms | 27.8 ms |

- Fark ölçüm gürültüsünün içinde. Yaklaşık 34–36 fps, GPU sınırlı; tur 5 ile aynı seviye (28.5 ms).
- a1 ilk ısınma koşusu (GPU 3.7 ms, sahne normal çizilmiyordu) ve yeniden açılış sonrası ilk deneme (4 CSV'den 2'si) geçersiz sayıldı.

## Uzun koşu: yorgunluk ve kamera (oyun kamerası, telemetri)
- 22 s sprint: `Fat` 0 → 1 (yaklaşık 17 s'de doluyor). Hız 584 → 515 cm/s (-%12).
- Gövde eğimi yorgunlukla **değişmiyor** (~20°). Yorgunluk şu an sadece hızda görünüyor.
- Kamera:
  - FOV 66° → 72° (sprintte);
  - mesafe 193 → 184 cm;
  - yan ofset sabit 44 cm;
  - titreşim ~0.05 cm (pratikte yok).
- Bu kayıt aracı oyun kamerasından görüntü alamıyor (video siyah). Kamera hissi için **görsel kanıt yok**.

## Kabul maddeleri

| # | Madde | Durum |
|---|---|---|
| 1 | Başlangıç doğrulaması (c499ab8), denetim bulguları | PASS (FL_GndT süre koşulu ve enjeksiyonlu testler bu turda giderildi) |
| 2 | Beden/kıyafet/poz izolasyonu, kıyafet sırt/yan hacmi | Teknik PASS, görsel onay bekliyor; üstün kaynak normalleri AÇIK |
| 3 | Rahat idle: omuz/kol yanda, hafif dirsek, hareket sonrası sönüm | Teknik PASS (kalıcı, yeniden açmada doğrulandı) |
| 4 | Ortak beden durumu | KISMİ (kurallar + belge, ortak bileşen yok) |
| 5a | Kol yolu yürüme/tempo/koşu/geri | PASS (yan yürüyüşte %1 kare ≤4.3 cm) |
| 5b | Tam duruş sonrası kayma / ek adım (20–33 cm) | ENGELLİ (satıcı PoseSearch DB'leri Python'dan düzenlenemiyor; 3 alternatif denendi, sonuç yok) |
| 5c | 90°/180° dönüş, sprint baş/boyun, zıplama/kayma | Bu turda yeniden çalışılmadı — AÇIK |
| 6a | Gerçek temasla bölgesel tepki (enjeksiyonsuz) | PASS (direk, fırlatılan kutu, duvar) |
| 6b | Dar geçit / bakış farkındalığı | NOT_TESTED |
| 7a | Gerçek temasla düşme, temas bazlı yer fazı | PASS |
| 7b | Yanlış pozdan kalkma yok, pop yok, uzuv savrulması yok | Teknik PASS (v3); görsel onay bekliyor |
| 7c | Kalkış alanı kontrolü, yer değiştirme veya bekleme | PASS (45 cm komşu ile yer değiştirme, yoksa bekleme). Masa altından **sürünerek çıkma yok** — KISMİ |
| 7d | Sırt üstü kalkış klibi | Yok; sırt üstü → 6 dönme denemesi → yüzüstü kalkış. AÇIK |
| 8a | Ledge tutunma / asılma / tırmanma / bırakma / ulaşılamayan kenar | PASS |
| 8b | Duvardan ayak desteği, uzak atlama | GASP traversal mevcut; MantleJumpUp entegre edilmedi — AÇIK |
| 8c | Çömelikken zıplama yok, gecikmiş zıplama yok | PASS |
| 9a | Normal koşuda görünür yorgunluk | KISMİ (yalnız hız düşüşü; postür değişmiyor) |
| 9b | Kamera hız hissi | Telemetri ölçüldü; görsel NOT_TESTED. Ragdoll kamerası NOT_TESTED |
| 10 | Kaydet, yeniden aç, son kayıtlar, performans | PASS |

## Değiştirilen varlıklar (kaydedildi, manifest + yedek ile)
- `/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player`: temas, düşme, ledge, zıplama korumaları, tur-6 değerleri.
- `/Game/Sphirus/Player/Motion/AC_Sph_Motion`: derleme ile kaydedildi.
- `/Game/Sphirus/Player/GASP/Rig/RTG_Sph_UEFN_to_MH`: kol IK kapalı, kol retarget pozu hizalı.
- Yeni: `/Game/Sphirus/CharacterLab/B14_20261126/Garments/SKM_Sph_RetroTop_B14`, `Pants70_B14`.
- Yeni: `/Game/Sphirus/Player/Anim/Ledge/SphL_*` (13 klip, AAMS kopyaları; orijinaller değişmedi).

Manifestler: `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/ue59_m29_p15save2_180504.json` ve öncekiler.

## Dosyalar
- `evidence/`:
  - `pf_falls.jpg`: yeniden açma sonrası 7 m düşüş ve masa senaryosu;
  - `pf_misc.jpg`: ledge, idle/koşu kolları, direk teması (uzun koşu satırı siyah: kayıt aracı oyun kamerasını yakalayamıyor);
  - `fl8_drop_sheet2.jpg` / `fl9_drop_sheet.jpg`: kalkış v1/v2 hataları (önce);
  - `fl8_throw_sheet.jpg`: havada ledge hatası (önce);
  - `ledge_board.jpg`, `garment_b13_b14.jpg`.
- `videos/pf_*.mp4`: yeniden açma sonrası son kayıtlar (sabit yan kamera).
- `data/*_telemetry.csv`: kare bazında konum, hız, kamera, düşme/temas/ledge durumu, yorgunluk.
- `data/final_summary.txt`, `data/perf_summary.txt`.
- `scripts/`: bu turun MCP/Python düzenleme ve analiz betikleri.
