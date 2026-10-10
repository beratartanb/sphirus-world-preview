# GD23 — Dudak–çene çizgisi, dış hat eşleme ve burun anatomisi (yan görünüm formu dahil)

Tarih: 2026-10-10. Başlangıç ve geri dönüş noktası GD22 G22; GD22'ye dokunulmadı.

Final aday **G23** (sculpt adı E5). Durum: **PARTIAL**. Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** UE varlıkları `/Game/Sphirus/CharacterLab/GD23_IdentityMaster_20261010` altında, yalnız test amaçlı. Kaynaklar `SourceAssets/Characters/GD23_IdentityMaster_20261010` altında (sculpt verisi, op'lar, araçlar, blend/GLB/OBJ).

## 1. İstekler ve teşhis

İstekler (sırayla): dudak ile çene arasındaki yeni çizgiyi yumuşat ve ana hattı referans üzerinden eşleştir; burun anatomisini yeniden çalış (GD22'de burun ezik büzük duruyordu); yan görünümde burun kanatları küçük ve hacimsiz, burun sırtının kıvrımı referansa göre kötü, burun ucu ve ucundan dudağa inen bölüm ezilmiş, çene yandan basılmış — çeneden dudağa gelen içe kıvrımı yay yap; son olarak iki çizim (`process/00a`, `process/00b`): yumuşak geçişler, sürekli yay şeklinde çene, daha büyük ve yuvarlak burun ucu, daha yüksek ve dolgun kanat, düz burun sırtı.

**a) "Yeni çizgi" neydi.** GD22'nin tam-kalınlık dolgusu (F alanı) dudağın altına bir *cilt rafı* koymuştu: dudak kısa kalmış, raf ±2 cm boyunca yatay bir çizgi olarak bitiyordu (`process/01`, orta panel). Referansta alt dudağın kütlesi ~4 mm daha aşağıda sarkıyor (everte, altı kutu gibi dolgun; ön yüzü z ≈ 154,6'ya kadar iniyor), oluk sığ (dudak önü → oluk tabanı 9–10 px, modelde 14 px), ağız çizgisi çentiği aynı derinlikte (5 px). Çene yastığındaki 0,11 mm yüksek frekans pürüzü (GD20'den beri) dudak altındaki kıvrımda değil, oluk tabanı / yastık üstü dalgalanmasında (z 153,1–153,7) yaşıyordu; dudak altını yuvarlamak (adaylar A–C) onu değiştirmiyordu.

**b) Ölçüm sınırları.** Çözülmüş profil kamerası tam yan değil (`cam_dir_yaw_deg` 72,6°): silüet, çene/yastık ve kolumella satırlarında orta hat dışından geliyor (orta hatta dudak–yastık basamağı 10 px iken silüette 7 px). Referans profil paneli alt yüzde render'dan ~%9 büyük ve ağız çizgisi 3,5 satır aşağıda; bu yüzden satır-satır değil, ağız çizgisine hizalayıp ölçekleyerek karşılaştırdım (±2–3 px gürültü). GD20'den beri kullanılan burun sırtı kalibrasyonu (−2,81 px) başka bir landmark ile doğrulanamıyor (alın/kaş = saç); ham kalıntılar senin gördüğünle (çene ve kolumella geride) örtüştüğü için alt yüzde ham değerler + senin gözün esas alındı.

**c) Burun.** GD22'nin buruşuk yüzeyi üst üste binmiş yerel op'lardan geliyordu. Yüzey, GD17'nin temiz burnu + GD22'nin büyük ölçekli şekil değişiminin alçak geçirgen (Laplace, 20 iterasyon) süzülmüş hali olarak yeniden kuruldu; burun deliği çatısı ve eşikleri ham bırakıldı (eşiklerde sert kutu kenarı bir üçgeni ters çeviriyordu → yumuşak kenar + eşik koruma küreleri).

## 2. Müdahale (sculpt zinciri `tools/build_gd23.sh`, 17 adım, G19S'ten 0,000000 mm farkla yeniden üretilir)

1. Perioral tam-kalınlık dolgu (GD22 F + 0,2–0,6 mm), infratip +1,3 mm, dudak altı yuvarlama (GD22 ile aynı yaklaşım).
2. **Alt dudak eversiyonu** (`tools/gd23_profield2.py`): tek bir alan — ileri yer değiştirme dy(z) tam kalınlık (dişler sabit) + dış ciltte aşağı kayma dz(z) (vermilyon sınırında −1,5 mm; iç mukoza, vestibül ve dişler yüksekliğini korur). Kontrol noktaları arka plan anahtarlı silüet kalıntılarından türetildi (`tools/_lipfield_design.py`). Sonuç: dudağın ön yüzü z 155,4 → 154,6 arasında dik (kütle aşağıda), altında 43° eğim, geniş sığ oluk.
3. Üst vermilyon +1,4 mm (dış cilt): üst/alt dudak ilişkisi referans gibi.
4. Oluk tabanı / yastık üstü konumsal yumuşatma (dış cilt, z 152,8–154,4): V çentiği kalktı, yastık pürüzü 0,107 → 0,069.
5. Burun yüzeyi yeniden kurma + zımpara (yukarıda).
6. Yan görünüm formu (senin notların ve çizimlerin): çene yastığı sürekli yay (alt yastık +2,2 mm, çene ucu z sabit, menton +0,9 mm — uzatma yok), oluk tabanı +1,3 mm (yalnız dış cilt; tam-kalınlık sürümü vestibülde 3 üçgeni ters çevirdi), burun sırtı düzleştirme (orta/alt sırt +2,8 mm, kök ~0), infratip/kolumella +2,4 mm ve uç lobülü 1,4 mm aşağı kaydırma (yuvarlak, sarkan uç), kanat oluğu 1,8 mm yukarı (dış yüzeyler) + kanat hacmi 1,5 mm normal itme, hafif zımpara.

Elenen adaylar: A/B/C (yalnız kıvrım yumuşatma: çizgi kalıyor veya iç mukozada ters üçgen), D/D2 (eversiyon; eşik üçgeni ters), E/E2/E3/E4 (yan görünüm turları: uç lobülü şişirme 4 ters üçgen + pürüz 0,065 → bırakıldı; tam-kalınlık oluk dolgusu 3 ters üçgen → dış cilt). Final **E5**: 0 ters üçgen.

Orta hat profili (y, cm): 155,4: 13,57 → 155,0: 13,58 → 154,8: 13,61 → 154,6: 13,52 → 154,4: 13,30 → 154,2: 13,11 → 154,0: 12,93 → 153,8: 12,91 → 153,6: 12,92 → 153,2: 12,96 → yastık önü ≈ 13,2 (z 152,2) — dudak önde, tek yumuşak S, çene yayı.

Rölyef (yüksek frekans pürüz, mm, sculpt): uç lobülü GD21 0,084 → **0,040** (W9 0,051), kanatlar 0,072 → **0,038** (W9 0,039), sırt 0,041 → 0,028, çene yastığı 0,114 → **0,07** (W9 0,038). Pronasale y 15,46 → 15,52, z 159,0 → 158,7 (lobül aşağı); burun deliği çatısı z 158,49 → 158,39.

Arka plan anahtarlı profil bantları, sculpt (kalibre px; + = model önde; ham değer = kalibre − 2,8):

| Bant | GD17 | GD22 | **GD23 sculpt** |
|---|---|---|---|
| Burun ucu | +0,4 | +1,7 | +2,5 |
| Infratip / kolumella | +1,6 | −0,5 | +2,9 |
| Üst vermilyon | +3,0 | +0,5 | +0,2 |
| Alt dudak (üst satırlar) | +5,5 | +2,1 | +3,6 |
| Oluk / alt dudak gövdesi | −4,7 | −5,5 | **−1,0** |
| Yastık üstü | +3,1 | −0,8 | +4,4 |
| Yastık ortası | +1,7 | +0,6 | +4,6 |

Ham değerlerle: oluk −3,8, yastık +1,6/+1,8, burun sırtı 0…+1,5, uç 0…+2, kolumella −2,5 (silüet burada kanat kenarından geliyor), alt çene ucu −2 (menton bilinçli olarak itilmedi). Çizimindeki oranlar: oluk derinliği GD22'nin ~%63'ü (hedef 0,7 cm → sonuç 0,70 cm), dudak–çene basamağı GD22'nin ~%65'i (hedef 4,5 px → sonuç 4,5–5 px).

## 3. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0,037 mm, p95 0,19, p99 0,46, en fazla 1,15 mm) |
| Otomatik rig, DNA, 858 morph | **PASS** (otomatik rig ok, DNA bağlı, 858 morph, blendshape'li DNA) |
| Rig sonrası mesh ↔ sculpt | **PASS** (ortalama 0,037 mm, en fazla 1,15 mm; GD22 → GD23 rig sonrası ortalama 0,25 mm, p99 3,0, en fazla 3,6 mm dudak altı / çene) |
| Ters üçgen (sculpt ve rig sonrası) | **PASS** (0 / 0) |
| Keskin kıvrım | **PARTIAL** (43; E'ye göre 11 sınırda: ağız köşesi iç yüzü, vestibül, burun eşiği — GD22'dekilerle aynı yerler, 120–154°) |
| Üçgen alan oranı min | 0,18 (vestibül; GD22 0,22) |
| Göz kapağı / göz küresi | **PASS** (değişmedi) |
| Çene alt kenarı satırı (ön, 2x) | **PASS** (rig sonrası 764, GD22 762–764, referans 761 — uzatma yok) |
| Rölyef rig sonrası (mm): uç lobülü / kanat / sırt / çene yastığı | 0,083 → **0,042** / 0,058 → **0,035** / 0,026 → 0,023 / 0,042 → 0,039 (üst dudak köşesi 0,028 → 0,031) |
| Profil bantları rig sonrası (kalibre px, GD22 → GD23) | oluk −5,5 → **−1,7**, infratip −0,5 → +2,7, sırt +0,5 → +3,4, yastık üstü −0,8 → +3,9, yastık ortası +0,6 → +4,1, alt yastık −1,0 → +1,9 (ham = −2,8) |
| Kaş-kirpik bağlama, göz kırpma, RigLogic ifadeleri | **PASS** (19 RigLogic ifadesi × 2 görünüm; `F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3 yakalandı, `F3`; LOD4–7 NOT_TESTED) |
| PIE, animasyon, saç sim. | **NOT_TESTED** (C: 2,7 GB boş) |
| Yeniden üretim | **PASS** (`tools/build_gd23.sh` G19S'ten G23S'i 0,000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (GD23 klasörleri dışında dosya değişmedi; qa_config geri yüklendi; editör kaydetmeden kapatıldı; ham yakalama klasöründen yalnız bayt-bayt özdeş kopyası pass klasörlerinde bulunan 763 dosya manifestle silindi) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 4. Panolar

`O1–O3` teşhis (GD22 gerçek/kil overlay'leri; profilde turuncu = gerçek silüet), `O4_*` sonuç overlay'leri (REF | aday | %50 | fark; GD22 / GD23 gerçek ve kil), `O5`–`O6` burun ve çene yakın plan overlay'leri, `C2`–`C6` kil ve UE yakın planlar (C4 burun, C5 dudak, C6 çene), `D1`–`D4` tam yüz, `E` deformasyon GD22 → GD23, `F1`–`F3` rig/ifade/LOD, `G1` adaylar (GD22 / D3 / E5 kil overlay). `process/00a–00b` senin çizimlerin, `process/01–12` sculpt aşaması şeritleri ve 6x profil satır zoom'ları.

## 5. Açık kalanlar

- Profilde mutlak konum ±2 px belirsiz (kamera yaw'ı, panel ölçeği, kalibrasyon): dudak ucu ve yastık ham ölçümde 1–2 px önde, kolumella 2–3 px geride okunuyor; görsel karar senin.
- Çenenin en alt ön yüzü referansta daha aşağıya kadar dik iniyor (menton bilinçli olarak yerinde bırakıldı; çizimindeki alt yay bunu ister, "çene uzatma yok" kuralıyla çelişmemesi için +0,9 mm ile sınırlandı).
- Burun delikleri: lobül aşağı kaydırıldığı için çatı 1 mm indi; büyüklük hâlâ referanstan biraz fazla olabilir.
- Alt dudak iç mukozası z 154,8'de diş etinin 0,5 mm önünde (dişler sabit tutulduğu için; kapalı ağızda görünmez).
- Sınırda iç katlanmalar (ağız köşesi iç yüzü 120–131°, burun eşiği 121–130°) GD22'dekilerle aynı yerlerde.
