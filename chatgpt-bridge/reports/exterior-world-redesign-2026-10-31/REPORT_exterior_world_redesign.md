# Exterior World Redesign — masterplan + R1 rear-region macro trial

İzole deneme, kaydedilmedi.

Tarih: 2026-10-31 · UE 5.8.1 · `L_GR_SphirusHouse` · Gerçek oyuncu kamerası: BP_PBI_Player + GraceRanger, FOV 60, kol 300 cm.

## Sonuç: önce bunu okuyun

Bu turun başarı ölçütü obje sayısı değil, mekânın tasarım kalitesiydi. Buna göre değerlendirme şöyle:

| Alan | Değerlendirme |
|---|---|
| Bütün dış alan için masterplan | **Yapıldı (tasarım belgesi).** Zonlar, görüş hatları, kütle ve açıklık planı, arazi hamleleri, dolaşım. R1 dışında motorda **test edilmedi**. |
| R1: arka patikanın yeniden kurgusu (rota) | **Belirgin kazanım.** Patika 90 m boyunca 0,84 m'den 9,93 m'ye tırmanıyor ve bir hedefe varıyor. Eski "arka patika" 55 m'de yalnızca 1,9 m'den 4 m'ye çıkan bir vadi tabanı yürüyüşüydü (AGENTS "uphill forest trail" sözleşmesine aykırıydı). Oyuncu kamerasıyla kesintisiz yürüyüş 68 s sürdü; takılma yok. |
| Sıkışma (compression) | **İyileşti, kil ve ışıklıda görünür.** Sağda sık çam kütlesi ve yükselen şev var, ileride patikanın etrafından kıvrıldığı bir kaya çıkıntısı var, sol açık. Asimetrik sıkışma. |
| Sırttan geriye bakış (refuge reveal) | **Yeni ve çalışıyor.** Sırt açıklığından aşağı bakınca ev, iki ağaç kütlesi arasından çerçeveli görünüyor. Önceden hiç görünmüyordu. Kilde de okunuyor. |
| Doğu duvarının kırılması (iki çıkıntı, koy, etek yamacı) | **PARTIAL.** Plan ve kesitlerde gerçek. Oyuncu yüksekliğinde zayıf okunuyor (`gate_right90` neredeyse aynı). |
| Tırmanış ve sırt ön planı | **Önceki halinden ZAYIF.** Yeni patika, oradaki doğal çalı/genç ağaç kütlesinin içinden geçiyor. Kütle taşındı ve tırmanış yamacı çıplak okunuyor. |
| Bütünsel "AAA dönüşüm" | **Ulaşılmadı.** Rota, sıkışma ve geri bakış ilişkileri gerçekten değişti. Bölgenin oyuncu yüksekliğindeki genel görünümü ise çoğu istasyonda büyük ölçüde aynı. |
| Geri alma | **PASS.** Yükseklik haritası bayt bayt aynı. 8305 foliage instance ve 768 aktör orijinalle aynı. Dirty içerik yok. Diskteki harita sha1 `70dd481a…` değişmedi. |
| Performans | **Anlamlı fark yok.** GPU medyanı 42,0 / 42,2 ms. Instance sayısı sabit, yeni obje eklenmedi. |

Videolar gerçek zamanlı izlenmedi. Değerlendirme kare örnekleri ve istasyon görüntüleriyle yapıldı.

---

## 1. Kök neden teşhisi: bütün dış alan

Tepeden render ve ölçüm: `maps/before_*.png`, 1 m ızgara.

1. **Kâse ve duvar.** Oyun alanı 0,3–3,5 m'lik düz bir taban. Çevresinde 10–15 m yüksek, düz ve tekdüze sırtlar var (doğu sırtı 20 m'de 11 m yükseliyor, yaklaşık 28°). Krater ya da oyun kutusu gibi okunuyor.
2. **Ev "knoll" üstünde değil.** Ev 16×16 m'lik kusursuz düz bir pedde duruyor (1,05 m).
   - Arkası daha alçak (0,6–0,9 m).
   - Batısında bir hendek var (−0,16 m).

   AGENTS'ın "rear rising woodland → house on knoll → descent → pond" yapısı arazide yok.
3. **Arka patika** sırtın dibinde bir oluk boyunca neredeyse düz gidiyor. Hemen kuzeyinde doğal bir vadi ve sırt (5 → 10 m) var, ama patika oraya hiç girmiyor.
4. **Orman tekdüze serpilmiş.** Ağaç aralığı yaklaşık 7 m.
   - Evin ve gölün çevresinde düzgün, boş bir dışlama halkası var.
   - Koru, kasıtlı açıklık ya da siluet hiyerarşisi yok.
5. **Gölet havzası** eş merkezli kontur halkalarıyla dairesel bir çanak.
6. Eski düzenlemelerden kalma basamaklı terasçık izleri var (eski patika bandında).

## 2. Referans çalışması: mekân inşası

Bu bölüm bir alt ajan araştırmasının özetidir. Erişim etiketleri her kaynak için ayrı tutuldu; tam liste `SOURCES` tablosunda.

- **TLOU2 (80.lv, Naughty Dog ekibi; ARTICLE_READ + DEVELOPER_STATEMENT):**
  - Yerleşim önce blockmesh'te kuruluyor.
  - Oyun alanları oynanış testi onaylayana kadar az detaylı kalıyor.
  - Görüş engelleri bir sonraki dönüşü gizliyor.
  - Bitki örtüsü ışık, toprak ve suya göre konuyor; yaşlı ağaçlar yenileri bastırıyor.
  - Manzaralar ilerlemeyi gösteriyor.
  - Bir yer işareti, görüş hatlarıyla tekrar tekrar çerçeveleniyor.
- **TLOU2 (Blocktober, Licea; ARTICLE_READ):** "play as you build": düz zemin, kutular ve tümseklerle hemen test.
- **A Plague Tale: Requiem:**
  - Choteau röportajları (ARTICLE_READ) "geniş ama tek okunur akış" diyor.
  - Blocktober görseli (STILL_IMAGES_VIEWED) dokusuz bir blockout gösteriyor. Ancak ışık **nötr değil**, anahtar güneş zaten var.
- **Alan Wake 2:** Orman yerleşimine dair kaynak bulunamadı. Yalnızca transkriptten bir not var: tür araştırması yapılmış, Cauldron Lake daha açık tutulmuş.
- **Doğrulanamayanlar:**
  - Hiçbir kaynak makro arazi formunu (çıkıntı, çukur, kâse kaçınma) anlatmıyor; arazi ilkeleri bizim çıkarımımız.
  - GDC Vault içeriği (giriş gerekiyor), Remedy GDC slaytları (indirilmedi) ve Requiem orman bölümleri erişilemedi.

**Uygulanan ilkeler:** önce kil (blockout) oyuncu kamerasıyla, tek okunur omurga, görüş engelleriyle sıkışma, ilerlemeyi gösteren geri bakış, ekolojik nedenli kütleler.

## 3. Masterplan: bütün dış alan

Görsel: `maps/MASTERPLAN.png`. Gri diskler mevcut kanopi. Yeşil koru kütleleri, sarı halkalar açıklıklar, turuncu çizgiler görüş hatları, mor alanlar arazi hamleleri.

| Zon | Karar |
|---|---|
| **Ev knoll'u** | Batı hendeği doldurulur. Önde göle doğru 1,2–1,8 m doğal düşüş. Arkada ev üstünde koruluk bir sırt (ana koru). Düz ped kenarları yumuşatılır; temel desteği korunur. |
| **S1 veranda → gölet** | Batı ön omzundaki koru ile doğudaki kütle arasından çerçeveli bir aralık. Geniş ön açıklık olmaz. |
| **Gölet havzası** | Asimetri: dik ve ağaçlı doğu kıyısı (yol buna tırmanır), güneybatıda alçak, sazlı çıkış, ağaçların suya kadar indiği batı korusu. Dairesel kenar halkası kırılır. Gölet **büyütülmez** (AGENTS). |
| **Göl kıyısı yolu** | Dik kıyıda sıkışma, ardından kıyı cebinde açılma. S2: uzak kıyıdan knoll üzerindeki eve geri bakış. |
| **R1 arka bölge** | Bu turda uygulandı (bölüm 4). |
| **Batı ormanı** | Alçak, dalgalı zemin. Batıyı kapatan sık bir koru ve küçük bir isteğe bağlı cep. |
| **Dış çevre** | Sırtlar kalır ama tepe çizgileri çıkıntı ve semerlerle kırılır. Tepe ağaç bantlarıyla açık ufuk kapatılır. |
| **Dolaşım** | Ev doğu köşesindeki merkez iniş yolu, göl kıyısı yolu ve arka patikayı bağlar. İsteğe bağlı döngü (gölet GD → doğu çıkıntısı → kapı) önerildi, **yapılmadı**. |

## 4. R1 tasarımı: uygulanan

Yalnızca bellekte. Bölge 90 × 114 m (x −15..75 m, y −82..32 m).

- **Korunan alanlar (sıfır değişiklik):**
  - ev artı 3,5 m;
  - arka bahçe (basamaklar, odun kütüğü, odun yığını, çit ve kapı);
  - ön taraf, iniş yolu, gölet havzası ve göl kıyısı yolu.

**Arazi.** Son hali r5; arazi r2/r4 ile aynı, yalnızca eğim yumuşatması daha uzun. Değişim aralığı −1,3 ile +3,3 m, değişen örnek sayısı 2917 (yaklaşık 0,29 ha). Kesitler: `maps/R1_sections_before_vs_final.png`.

| Form | Ne yapıyor |
|---|---|
| `spur_north` | Doğu duvarından vadiye uzanan çıkıntı. Duvarda +0,8 m, uçta +3,6 m. Sıkışmanın sağ duvarı. |
| `spur_south` | +0,6 → +2,8 m. Kapıyı doğudan çerçeveler. |
| `bay_gully` | İki çıkıntı arasında içbükey koy (−0,6 → −1,5 m). İsteğe bağlı cep. |
| Etek yamacı | Duvar dibi çizgisi boyunca, 50 m'de +1,2 m'ye kadar. Taban ile duvar arasındaki keskin açı uzun içbükey bir geçişe döner; basamak yok. |
| `house_spur` | Bahçenin arkasında +2,3–2,6 m, geniş koruluk sırt. Ev onun altında kalır. |
| `hollow` | Vadiden aşağı inen −0,9/−1,1 m'lik drenaj çukuru. |
| `valley_shoulder` | Vadinin batı yanında +1,2–1,6 m omuz. |
| Eski terasçıklar | Eski patika bandındaki basamak izleri geniş bir bulanıklaştırmayla silindi. |
| Patika setti | ±1,5 m enine düzleştirme, 9 cm aşınmış iz. |

**Yeni patika (90,4 m).** Durakları sırayla:
1. ev doğu merkezi;
2. bahçe kapısı (kapı patikaya açılıyor);
3. çıkıntı + kaya + koru sıkışması;
4. çukur geçişi;
5. vadide tırmanış;
6. sırt açıklığı ve evin çatısına geri bakış.

En dik kısım 11,5 m boyunca 15–20,8°.

**Kütleler: yalnız yeniden dağıtım.** Yeni obje eklenmedi; bileşen başına instance sayısı aynı (8305).

- **Büyük ağaçlar:** bölgedeki 207 büyük ağaçtan 34'ü taşındı.
  - Kaynaklar: açıklıklar (sırt açıklığı, geri bakış koridoru, çukur ışık bandı, koy cebi), seyreltilen bölgeler (bahçe doğusu düzlüğü, çukur yatağı) ve tekdüze matristen toplananlar (11).
  - Gittikleri yer 12 sık kütle: ana koru, iki doğu sırtı yüzü, çıkıntı korusu, iki kapı korusu, vadinin iki yanı, tepe bandı ve tırmanış, geçiş ve sırt çerçeveleri.
- **Genç ağaçlar:** 66 taşındı. Patika kenarında 12 kümede toplandılar (her küme 3–5 ağaç, patikadan 3,8–6,5 m uzakta, dönüşümlü taraflarda); 5 küme elle konumlandı.
- **Çalı ve yer örtüsü:** 54 öğe tread'den çıkarıldı.
- **Sert kütleler:** 12 taşındı. Kaya ve set mesh'leri çıkıntı ucunda bir çıkıntı (outcrop) oluşturdu; taşlar geçişi çerçeveliyor (tread'den ≥2 m). Tampon bölgede kalmış 4 sert obje (taş, gövde) tread'den alındı.
- **Yeniden zeminlenen:** 1368 instance, gömülme payı korunarak.

## 5. Doğrulama yöntemi ve yinelemeler

Önce nötr ışık ve kil kullanıldı. Kil, PIE'de `viewmode lightingonly`: malzeme ve renk yok, form yalnız ışık ve gölgeyle okunuyor. Nötr ışık:
- güneş −40°, 2000 lux, 6500 K, açı 2;
- gök 1,6;
- sis 0,004, 25 m'den başlıyor.

Her sürüm aynı istasyon pozlarında kil ve ışıklı olarak çekildi, ardından kesintisiz yürüyüş.

| Sürüm | Bulgu | Neden | Düzeltme |
|---|---|---|---|
| r1 (yalnız plan) | Formlar çekingen; çıkıntı yapay yuvarlak bir tümsek; terasçıklar duruyor. 75 ağaç yer bulamadı. | Küçük ölçek; koru alanı yetersiz | r2: gerçek çıkıntılar + koy + etek yamacı + terasçık silme; geniş meşcereler |
| r2 | Etek yamacında sert basamak (plan) | İtme maskesi tek taraflı | Her iki yana yumuşak sönüm |
| r2 (motor) | Karakter 58 m'de **takıldı** | "Geçiş taşlarını" tread'in **üstüne** koymuşum (çarpışma kapsülü durdurdu) | r3: taşlar tread'den ≥2 m |
| r2/r3 | Tırmanış ve sırt yamacı çıplak, sırt açıklığı çerçevesiz | Seyrek vadi bölgesi patikayı boşalttı | r3: çerçeve koruları + matristen toplama |
| r3 | Tırmanış **daha kötü**: itilen çalılar patika kenarında **çit** dizisi oluşturdu; 36 m'de 1,5 s yavaşlama | Paralel itme; tampon bölgede kalan bir taş tread üstünde | r4: kümeler; tampon dahil sert obje temizliği |
| r4 | Tırmanış hâlâ çıplak | "Genç ağaç matrisinin %40'ı kenarlara" kuralı tırmanış yanındaki **mevcut doğal kütleyi** götürdü | r5: patikaya 12 m içindeki genç ağaçlar yerinde kalır; tırmanış ve sırt yaklaşımına elle küme |
| **r5 (son)** | 68 s kesintisiz yürüyüş. Sıkışma ve geri bakış güçlü. Tırmanış hâlâ BEFORE'dan zayıf. | Patika, oradaki büyük çalı kütlesinin tam içinden geçiyor | Bölüm 9 |

Not: kuralla dağıtım hiyerarşi kurdu, ama kahraman görünümlerde iki kez mevcut iyi meso yapıyı bozdu. Proje kuralı doğrulandı: giriş, dönüş, reveal ve ön plan elle yönetilmeli.

## 6. İstasyon sonuçları

`compare/final_r5_2x2/`: üst satır CLAY BEFORE | CLAY AFTER, alt satır LIT BEFORE | LIT AFTER; aynı oyuncu kamerası pozu.

| İstasyon | Kil (form) | Işıklı |
|---|---|---|
| hub | Aynı (korunan alan) | Aynı |
| gate | Sağda hafif yükselen şev; okuma zayıf | Neredeyse aynı |
| compression | **Belirgin:** sağ kütle + şev + ileride outcrop, sol açık | Belirgin sıkışma |
| crossing | Çukur hafif okunuyor; kaya çerçeve | Sınırlı fark |
| climb | Yamaç çıplak; sağda küme | **Önceden zayıf** |
| saddle (ileri) | Açıklık daha boş | Daha boş |
| saddle → ev | **Yeni geri bakış:** ev, iki kütle arasında | Aynı |

İterasyon özetleri `compare/iterations/` altında (r2, r3, r4).

## 7. Kesintisiz oynanış videoları

Sabit adımlı 30 FPS, kare numarası oyun zamanını gösterir. **Gerçek zamanlı izlenmedi.**

- `video/XR_after_r5_walk_clay_lit_part1.avi` + `part2.avi`: yeni rota, 90 m, 68 s. Solda kil, sağda üretim görünümü; aynı kare aynı an.
- `video/XR_before_oldroute_walk_clay_lit_part1.avi` + `part2.avi`: eski rota, 60 m, 45 s, kil | ışıklı.
- `video/XR_after_r5_pan_compression.avi`, `XR_after_r5_pan_saddle.avi`: ±100° kamera panı.

## 8. Performans

CSV profiler, pass B, ayrı yürüyüş. Değerler p50 / p95, ms.

| Koşu | Kare | Oyun iş parçacığı | GPU | VRAM MB |
|---|---|---|---|---|
| BEFORE, eski rota 60 m | 43,7 / 48,7 | 16,4 / 20,1 | 42,0 / 46,7 | 6788 |
| AFTER r5, yeni rota 90 m | 43,5 / 47,7 | 17,3 / 21,8 | 42,2 / 45,6 | 6585 |

Rotalar ve görüş yönleri farklı olduğu için bu birebir karşılaştırma değil. "Anlamlı maliyet yok" diye okunmalı. r2'nin 37,5 ms'lik değeri takılmalı koşudandır (az görüş değişimi), geçersiz sayılmalı.

## 9. Asset ve mevcut arazi yeterliliği

- **Arazi çözünürlüğü yeterli:** 1 m ızgara, tek edit layer. Asıl yetersizlik **mevcut makro tasarım**: kâse ve düz duvarlar. Bu turda yalnız R1'de kırıldı ve değişiklikler (≤3,3 m) oyuncu yüksekliğinde çoğu yerde zayıf okunuyor. Gerçek dönüşüm için daha cesur formlar gerekiyor: 4–8 m'lik çıkıntı uçları, patikaya yakın kesik şevler.
- **Kaya kütleleri:**
  - Kullanılanlar küçük. En büyüğü 2,8 m'lik SM_ForestEmbankment01 (3 adet); PineGroundRock'lar ~1,5 m.
  - Projede **kullanılmayan büyük kaya mesh'leri var:** `PineForestPack/Meshes/Cliffs/SM_CliffRock01/02`, `SM_CliffRockCurve01/02`, `SM_PineCliff02/03`, `OakForestEnv/Meshes/ScanAssets/SM_Boulder_1/2`. Çıkıntı uçları ve sıkışma için asıl yapısal kütle bunlarla kurulmalı. Bu "dekor" değil, makro kütle; az sayıda ve büyük.
- **Ağaç paleti:** 3 çam ve 3 köknar mesh'inin siluetleri birbirine çok benziyor. Kahraman ağaç ve siluet çeşitliliği zayıf. Koru düzeni kurulsa da tepe çizgisi tekdüze kalıyor. Bu bir asset sınırı.
- **Patika malzemesi:** landscape boya katmanındaki eski patika izi eski rotayı izliyor. Kil aşamasında bilerek dokunulmadı; yeni rota malzemede henüz yok. **NOT_TESTED.**

## 10. Sonraki adım: r6 önerisi (onay gerekmez, izole)

1. Çıkıntı uçlarına ve sıkışmaya 3–4 büyük CliffRock/PineCliff kütlesi. Çıkıntı uçları +4–6 m.
2. Tırmanışı yeniden rotalamak. Mevcut büyük çalı kütlesini koruyup patikayı onun yanından geçirmek (dirsek), yani kütleyi taşımak yerine patikayı oynatmak.
3. Sırt açıklığına bir kahraman ağaç ve çerçeve.
4. Ardından landscape boya katmanında yeni patika ve eski izin silinmesi (malzeme aşaması).

**Kalıcı uygulama için onayınız gerekiyor.** Önerilen sıra:
1. R1'i (r5 ya da r6) ayrı bir manifest ve yedekle kaydetmek. Landscape ve foliage ana haritada olduğu için ana harita paketine yazılır.
2. Bridge export + LATEST.json doğrulaması (AGENTS).
3. Masterplan'ın diğer zonları için aynı yöntemle ayrı denemeler.

## 11. Güvenlik ve geri alma

- **Kayıt:** hiçbir paket kaydedilmedi. Map manifesti `vmp_map` (sha1 `70dd481a…`) yedekli.
- **Snapshot:** recon + `recon_backup` (yükseklik ve foliage hash'leri doğrulandı).
- **Uygula/geri al:**
  - her uygulama ve geri alma yazma iş olarak tek kilit sahibiyle çalıştı;
  - yükseklik haritası örnek bazında decode ve geri okuma doğrulamasından geçti;
  - foliage tipi eşleşmesi (mesh + cull) benzersiz bulundu (dry-run).
- **Son durum:**
  - yükseklik haritası bayt bayt orijinal;
  - foliage (57 bileşen, 8305) ve aktörler (768) birebir;
  - ışık ve sis orijinal (`look_restore`);
  - dirty içerik yok, PIE kapalı, kilit bırakıldı.
- **Harita durumu:** yalnızca bellekte dirty, içerik orijinal. Editör kapanırken **"Don't Save"** seçin.
- **Bir hata:** ilk kil istasyon koşusu, çıktı yolundaki boşluk yüzünden "HighResShot timeout" verdi. Yol düzeltildi, koşu tekrarlandı.

## Dosyalar

- `maps/`:
  - `MASTERPLAN.png`;
  - `R1_FINAL_before_vs_r5.png` (kil, kütle, plan: önce ve sonra);
  - `R1_sections_before_vs_final.png`;
  - iterasyon haritaları.
- `compare/final_r5_2x2/`: 26 poz, kil ve ışıklı, önce ve sonra.
- `compare/iterations/`: r2–r4 özetleri.
- `stills/`: ham kareler (JPEG q90) — before/after × clay/lit.
- `video/`: 6 AVI.
- `data/`:
  - plan JSON'ları (r1–r5);
  - apply/restore kayıtları;
  - `foliage_r5.json` (değişen bileşenler);
  - yükseklik PNG'leri (önce ve r5);
  - perf, yürüyüş ve istasyon logları.
- `tools/`: `xr_design.py`, `xr_apply.py`, `xr_walk.py`, `xr_maps.py`, `xr_sections.py`, `xr_compare.ps1`, `recon.py`, `height_export.py`, `label_map.ps1`, `pack_xr.ps1`, `triptych.ps1`.
