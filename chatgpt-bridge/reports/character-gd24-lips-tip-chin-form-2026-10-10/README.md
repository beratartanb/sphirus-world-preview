# GD24 — Dudak kenarı, burun ucu ve çene formu (GD23 incelemesi üzerine)

Tarih: 2026-10-10. Başlangıç ve geri dönüş noktası GD23 G23; GD23'e dokunulmadı.

Final aday **G24** (sculpt adı D4 = C + ikinci burun notun). Durum: **PARTIAL**. Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED).

**Üretim karakterine uygulanmadı.** UE varlıkları `/Game/Sphirus/CharacterLab/GD24_IdentityMaster_20261010` altında, yalnız test amaçlı. Kaynaklar `SourceAssets/Characters/GD24_IdentityMaster_20261010` altında (sculpt verisi, op'lar, araçlar, blend/GLB/OBJ).

## 1. İsteklerin ve teşhis

Üç işaretli görsel (`process/00a–00c`): burun ucu birazcık daha yukarı ve yumuşak; çene çizdiğin gibi daha yumuşak ve biraz daha hacimli (tek sürekli yay); dudaklar uçları yukarı bükülmüş değil, referanstaki gibi doğal çıkan ve birazcık önde.

6x profil satır zoom'ları (REF | GD23 gerçek | GD23 kil, `process/01–03`) ne olduğunu gösterdi:

- **Dudak:** GD23'te üst vermilyonun alt kenarı yukarı doğru açılmıştı (GD20–GD23'teki öne itmeler vermilyonu öne alırken ağız çizgisi yerinde kaldığından kenar yukarı döndü) ve alt dudağın üst yüzeyi ağız çizgisinin 2 mm önüne çıkıyordu. Referansta üst dudağın tüberkülü aşağı-öne sarkıyor ve ağız çizgisi öne doğru hafifçe iner.
- **Burun ucu:** GD23'te lobülü 1,4 mm aşağı kaydırmıştım; uç referanstan düşük sarkıyor, kolumella uzun ve dik, kanat kenarı kolumella seviyesinde (burun deliği yandan ince bir çizgi).
- **Çene:** oluk referanstan derin, yastık önü düz, çene altı köşeli dönüyor; referansta dudağın hemen altından başlayan yuvarlak bir yay var.

İkinci burun notun (`process/00d`, C adayının kil ucu üzerine): yuvarlak bir uç — altı dolgun, dışbükey bir kıvrımla kolumellaya inen — ve daha uzun, daha belirgin bir kanat lobu, "referanstaki gibi".

## 2. Müdahale (`tools/build_gd24.sh`, G23S'ten 14 adım, 0,000000 mm farkla yeniden üretilir)

1. **Dudak** (`gd24_profield2.py`, tek alan, menteşe sürekli): ağız çizgisi ve üst vermilyonun alt kenarı dış ciltte + temas halkalarında 1,0 mm aşağı kayar, üst vermilyonun alt yarısı +0,9 mm öne, alt dudağın üst yüzeyi −0,5 mm geri; dişler sabit. Yukarı açılan kenar yerine aşağı sarkan tüberkül; ağız çizgisi referans gibi öne doğru iniyor.
2. **Burun ucu** (profield2, burun bölgesi): infratip/kolumella 1,2 mm yukarı, uç +0,4 mm öne, kolumella tabanı −0,3 mm; kanat kenarının alt ucu 0,6 mm yukarı (`gd24_normal_push.py`, yöne göre süzülmüş öteleme). Pronasale z 158,72 → 158,83.
3. **Çene**: yastık yayı + yuvarlak çene altı (tam kalınlık, +0,5…1,1 mm; menton z sabit — uzatma yok), oluk tabanı +1,3 mm (yalnız dış cilt), yastık yumuşatma (dış cilt, z 151,8–153,4), hafif burun zımparası.

4. **Burun ucu ve kanat, ikinci not** (adım 9–14): uç altı / infratip lobülü normal yönünde 0,8 mm dışarı (aşağı-öne bakan yüzeyler; bölge ince burun deliği çatısı birleşiminden uzak tutuldu), kanat oluğu +0,8 mm daha yukarı, kanat lobu +0,5 mm dışarı (yalnız dış-yan yüzeyler, eşik 0,3), hafif zımpara.

Elenen adaylar: **A** — dudaklar temas çizgisinin iki yanında zıt yönde hareket etti (alt dudak üstü −1,0 / üst kenar +2,0): ağız çizgisinde 32 ters üçgen (`process/10`). **B** — aynı tasarım menteşe sürekli ama kayma tam kalınlıkta: vestibülde 1 ters üçgen. **C** — kayma dış cilt + temas halkaları, z ≥ 155,0: 0 ters üçgen (ilk üç isteğin tamamı; `process/11`). **D** — C + uç altı 1,0 mm: burun deliği çatısı birleşiminde üçgen alan oranı 0,05 (ezilme). **D2/D3** — daha küçük uç bölgesi, kanat tabanı 0,4 mm aşağı: burun deliği iç duvarında alan oranı 0,10/0,12. **D4** (final) — kanat tabanı indirme kaldırıldı, lob itmesi iç duvardan uzak: 0 ters üçgen, alan oranı min 0,17.

Orta hat profili (y, cm): 155,6: 13,33 → 155,4: 13,45 → 155,0: 13,58 → 154,8: 13,61 → 154,4: 13,30 → 154,0: 13,02 → 153,8: 12,94 → 153,6: 12,99 → 153,2: 13,05 (GD23: 155,6: 13,38 → 155,4: 13,57, oluk tabanı 12,91).

Rölyef (yüksek frekans pürüz, mm, sculpt): uç lobülü 0,040 → **0,032**, kanatlar 0,038 → 0,036, çene yastığı 0,068 → **0,058**, üst dudak köşeleri 0,029 → 0,030. Üçgen alan oranı min 0,17 (burun deliği çatısı birleşimi; GD23 0,18).

Arka plan anahtarlı profil bantları, sculpt (kalibre px; + = model önde; ham = kalibre − 2,8):

| Bant | GD17 | GD23 | **GD24 sculpt** |
|---|---|---|---|
| Burun ucu | +0,4 | +2,5 | +2,9 |
| Infratip / kolumella | +1,6 | +2,7 | +2,2 |
| Üst vermilyon | +3,0 | +0,2 | +1,1 |
| Alt dudak (üst satırlar) | +5,5 | +3,5 | +3,3 |
| Oluk / alt dudak gövdesi | −4,7 | −1,7 | **−0,8** |
| Yastık üstü / ortası / altı | +3,1 / +1,7 / −1,4 | +3,9 / +4,1 / +1,9 | +5,3 / +5,1 / +3,0 |

Çene ham ölçümde referans silüetinin ~1,5–2 mm önünde (senin "biraz daha hacimli" isteğin); oluk ham −3,6 (satır hizası nedeniyle; orta hatta derinlik 0,67 cm).

## 3. Teknik testler

| Test | Sonuç |
|---|---|
| Fit (2 rezidüel geri besleme) → sculpt | **PASS** (ortalama 0,039 mm, p95 0,20, p99 0,49, en fazla 1,19 mm) |
| Otomatik rig, DNA, 858 morph | **PASS** (otomatik rig ok, DNA bağlı, 858 morph, blendshape'li DNA) |
| Rig sonrası mesh ↔ sculpt | **PASS** (ortalama 0,039 mm, en fazla 1,19 mm; GD23 → GD24 rig sonrası ortalama 0,10 mm, p99 1,13, en fazla 1,26 mm) |
| Ters üçgen (sculpt ve rig sonrası) | **PASS** (0 / 0) |
| Keskin kıvrım | **PARTIAL** (42; E'ye göre 9 sınırda: ağız köşesi iç yüzü, vestibül, burun eşiği — GD23'tekilerle aynı yerler) |
| Üçgen alan oranı min | 0,17 (burun deliği çatısı birleşimi; GD23 0,18) |
| Göz kapağı / göz küresi | **PASS** (değişmedi) |
| Çene alt kenarı satırı (ön, 2x) | **PASS** (rig sonrası 764 = GD23, referans 761 — uzatma yok) |
| Rölyef rig sonrası (mm): uç lobülü / kanat / sırt / çene yastığı | 0,042 → **0,034** / 0,035 → **0,032** / 0,023 → 0,023 / 0,039 → 0,038 |
| Profil bantları rig sonrası (kalibre px, GD23 → GD24) | uç +2,5 → +2,8, infratip +2,7 → +2,2, üst vermilyon +0,2 → +1,1, alt dudak +3,5 → +3,2, oluk −1,7 → **−0,8**, yastık üstü/ortası/altı +3,9/+4,1/+1,9 → +5,3/+5,0/+3,0 (ham = −2,8) |
| Kaş-kirpik bağlama, göz kırpma, RigLogic ifadeleri | **PASS** (19 RigLogic ifadesi × 2 görünüm; `F1`, `F2`) |
| LOD | **PARTIAL** (LOD0–3 yakalandı, `F3`; LOD4–7 NOT_TESTED) |
| PIE, animasyon, saç sim. | **NOT_TESTED** (C: ~2,3 GB boş) |
| Yeniden üretim | **PASS** (`tools/build_gd24.sh` G23S'ten G24S'i 0,000000 mm farkla üretir) |
| Üretim değişmedi | **PASS** (GD24 klasörleri dışında proje dosyası değişmedi — lookdev araçlarının `Saved/Codex/CharacterFaceMatch_20260930/` altına yazdığı iki GD24 bağlama kaydı JSON'u ve editörün kendi `Saved/` durum dosyaları hariç; qa_config geri yüklendi; editör kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 4. Panolar

`O1–O3` teşhis (GD23 gerçek/kil overlay'leri), `O4_*` sonuç overlay'leri (REF | aday | %50 | fark; GD23 / GD24 gerçek ve kil), `O5`–`O6` burun ve çene yakın plan overlay'leri, `C2`–`C6` kil ve UE yakın planlar (C4 burun, C5 dudak, C6 çene), `D1`–`D4` tam yüz, `E` deformasyon GD23 → GD24, `F1`–`F3` rig/ifade/LOD, `G1` adaylar (GD23 / C / D4 kil overlay). `process/00a–00d` senin işaretlerin, `01–03` teşhis zoom'ları, `04–09` sonuç zoom'ları ve şeritler (`08b` 3/4 burun), `10` elenen A, `11` ara aday C'nin burun ucu (ikinci nottan önce).

## 5. Açık kalanlar

- Profilde mutlak konum ±2 px belirsiz (kamera yaw'ı, panel ölçeği); çene ham ölçümde referansın önünde — görsel karar senin.
- Üst vermilyonun alt kenarı referansın tüberkülü kadar belirgin değil (daha fazla öne alma menteşede katlanıyor; topoloji sınırı).
- Burun ucu döndürülünce ön görünümde burun delikleri biraz daha görünür (referansta da öyle).
- Sınırda iç katlanmalar (ağız köşesi iç yüzü, vestibül, burun eşiği: 120–156°) GD23'tekilerle aynı yerlerde.
