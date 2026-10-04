# GD11 saç revizyonu E: alın–tepe–arka–topuz akışı (yüz sabit)

Tarih: 2026-10-04. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Production'a hiçbir şey geçmedi.

## Başlangıç paketi (doğrulandı)

Kaynak: rapor `character-gd11-head-refinement-d-2026-10-04`, commit `19c13857`.

| Parça | Asset |
|---|---|
| Yüz | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementD_20261004/Face/SKM_G11RD_Face_f4ab` |
| DNA | `MHC/DNA/MHC_G11RD_F4AB_Head` |
| Saç | `Hair/GR_LK_Hair_{Main,Loose}_h38d`; kaynak `Saved/Codex/GD11_HeadRefinementD_20261004/hair/h38d/strands.npz` |
| Bağlamalar | `Face/Bindings/GB_G11RD_*_f4abh38d` |
| Ten | k10 (C) |
| Göz / kaş / kirpik | e2 / M_SlightArch / S_Thin |

Yerelde D'den daha yeni bir çalışma yoktu. h37'ye geri dönülmedi.

## Yeni aday

`/Game/Sphirus/CharacterLab/GD11_HeadRefinementE_20261004/`

| Parça | Asset |
|---|---|
| Saç | `Hair/GR_LK_Hair_{Main,Loose}_h39i` + kask (LOD3); LOD tablosu ayarlı |
| Bağlamalar | `Face/Bindings/GB_G11RE_*_f4abh39i`, D'nin F4ab yüzünü hedefliyor |
| Test animasyonu | `Anim/AS_G11RE_HeadPitch` (baş eğimi) |
| Saç kaynakları (kalıcı) | `Saved/Codex/GD11_HeadRefinementE_20261004/hair/h39*/` (`strands.npz`, `.abc`, `build_env.txt`); oluşturucu `tools/blender_g11re_hair.py` |
| Ham render'lar | `frames/raw/` |

**Değiştirilmedi:** yüz, DNA, kafatası, ten, göz/kaş/kirpik. Yeni yüz auto-rig çalıştırılmadı.

**Yazma yolları:** bu turun ilk çekiminden önce bütün çekim, stüdyo ve bağlama yolları E'ye yönlendirildi.
- `gd11re_caps.sh`, stüdyo klasörü E değilse veya bir bağlama eksikse çekimi reddediyor.
- Koruma doğrulaması: **54/54 grup birebir aynı**. D, C, B, GD11 ve production dahil; bu turda eski adaylara hiçbir yazma olmadı.

## 1. Tanı: yapışık başlangıç, tepe bombesi, arka kanca (board 04, 07)

**Yöntem:** `blender_g11re_flow.py`.
- Orta hat ve ayrım yanı şeritlerinden köklenen ana teller profilde çizildi; renk kök konumuna göre (kırmızı = alın kökleri, mavi = arka kökler).
- Baş merkezi etrafındaki açıya göre saç zarfının kafatasına uzaklık eğrisi çıkarıldı: 0° = verteks, + = ön, − = arka.

**h38d, ayrım yanı şeridi** (`data/flow_standoff_side.json`):

| Açı | +50 | +40 | +30 | +20 | +10 | 0 | −10 | −20 | −30 | −40 | −50 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| h38d (cm) | 0,06 | 0,28 | 1,12 | 0,91 | 1,84 | 2,56 | 3,18 | 3,42 | 3,44 | 3,21 | 2,94 |
| h39i (cm) | 0,06 | 0,33 | 1,84 | 2,53 | 2,45 | 2,45 | 2,64 | 2,40 | 2,30 | 2,50 | 2,33 |

**Kodda bulunan nedenler** (`blender_g11rd_hair.py`):

1. **Yapışık başlangıç**
   - Ön kilitlerin yükselme rampası yolun %44'üne yayılmıştı (yol oranına göre).
   - Kök çıkış yönü arkaya yatıktı (NB_UP 0,2, NB_BACK 0,6).
   - Saç çizgisinde köklenen teller, kökü daha geride olan kilidin düşük başlangıç bölümünü izliyordu.
2. **Tepe bombesi**
   - Kaldırma alanı yükseklik (z) eşiği ve ön-kesim çarpanıyla kurulmuştu.
   - Ön kenarda yaklaşık 2 cm, hemen arkasında 3,45 cm. Hacmin tepesi verteksin 25–35° gerisinde toplanıyordu.
3. **Arka duvar ve topuza kanca**
   - Yükseklik yolun %82'sine kadar tam kalıp sonra hızla düşüyordu.
   - Son nokta topuz girişine tek adımda çekiliyordu.

## 2. Yapısal değişiklikler (h38d → h39i)

Oluşturucunun E kopyası `blender_g11re_hair.py`; `SPH_FLOW_E=1`. Tam parametre farkı: `data/hair_h38d_to_h39i_env_diff.txt`.

| Bölge | Ne değişti |
|---|---|
| Kaldırma alanı | Z eşikli tepe/ön/arka terimleri yerine **başın orta hattı boyunca tek, yumuşak bir açı profili** (`SPH_ARC_KNOTS`): alın kenarı 1,4 → ön-üst 2,45 → tepe 2,8 → 2,75 → arka 2,25 → 1,45 → topuz seviyesi 0,9 cm. Ön/tepe/arka ayrı kontrol ediliyor, aralarında yumuşak geçiş var. |
| Kök sonrası yükseliş | Rampa santimetre cinsinden mesafeye bağlandı (`SPH_RAMP_CM` 3,2). Kök yüzeyde (ROOT_H 0,07), ilk bölüm yerel yüzeye uygun açıyla çıkıyor (NB_UP 0,3 / NB_BACK 0,5), sonra kademeli yükseliyor. |
| Ön dolgu | Kilit telleri, kendi kökünden itibaren yay uzunluğuyla artan bir miktarda dışa itiliyor (`SPH_FRONT_FILL` 0,6, rampa 3,5 cm). Kökte sıfır. Yalnız alın arkası bandında (14–54°, tepe 30°). Yanal itme yok (`SPH_FILL_LAT` 0), ayrım kapalı kalıyor. |
| Ayrım | Ayrım çizgisinin hemen yanında kaldırma yumuşakça azaltıldı (`SPH_ARC_PARTDIP` 0,45). İki yan ayrıma doğru yatıyor, koyu V daralıyor. Sağ/sol farkı 0. |
| Tepe → arka | Yükseklik yolun son %40'ında kademeli azalıyor (`SPH_END_TAPER` 0,6); ani iniş ve duvar yok. |
| Topuz girişi | Giriş noktasına yaklaşım yolun son yaklaşık %38'ine dağıtıldı (`SPH_ENTRY_T0` 0,62); birkaç kontrol noktası birlikte kayıyor, 4 tur yumuşatma. Topuzun konumu (161,6 / −8,6) ve D'deki kaçan uç ve eksen sınırları aynı. |
| Kulak arkası | Tutamlar ikiye ayrıldı. **Katılanlar:** kulak arkasından hafif gevşeklikle çıkıp ense/topuz akışına kavisle katılıyor (U-kanca yok). **Serbest olanlar:** dışa açılıp kendi ağırlığıyla düşüyor, geri dönmüyor. Karakter solunda 2 katılan + 1 serbest, sağında 1 katılan + 1 serbest. |

**Değişmeyenler:** renk ve materyal (h38d değerleri), saç çizgisinin yeri, alın yüksekliği, topuz konumu, arka uzunluk.
- En arka nokta: h38d −13,67, h39i −13,60 cm.
- Arka-üst uzaklık: aynı veya daha az (`data/back_layers_*.json`).

## 3. Reddedilen denemeler

| Deneme | Neden reddedildi |
|---|---|
| h39a | Bombe gitti ama alın arkası hâlâ yapışık (kök rampası yol oranına bağlıydı). |
| h39b / h39c | Mesafe tabanlı rampa +20…+30°'yi düzeltti; saç çizgisinin hemen arkası (+40°) hâlâ yaklaşık 0,3 cm. |
| h39d / h39f | Ön dolgu saç çizgisine çok yakın tepe yapıyordu (40°), rampa kısaydı ve yanal itme vardı. Sonuç: **koyu, kalın peruk kenarı ve ayrımda V** (board 05'te gösteriliyor). |
| h39e | Fazla dolgu: önde tepeden yüksek, kabarık kütle. |
| h39g | Peruk kenarı gitti; ayrımda V hâlâ belirgindi. |
| h39h (kontrol, dolgusuz) | V'nin dolgudan değil, ayrımın iki yanının yükselmesinden geldiğini gösterdi. Ayrım çukuru buna göre h39i'ye eklendi. |

## 4. Teknik

| Kontrol | Sonuç |
|---|---|
| Bağlama | 4 f4abh39i bağlaması `SKM_G11RD_Face_f4ab`'i hedefliyor; temiz editörde yeniden okundu. |
| Baş eğimi | Gerçek test klibi (yaklaşık 26° öne, 30° yukarı, dinamik saç). Kökler kopmuyor; topuz ve ense saçı boyuna yaklaşıyor ama girmiyor; topuz bağlantısı bozulmuyor; nötr poza temiz dönüş. |
| Hareket (27 çekim) | Dönüşler, koşu-durma, etrafa bakma. Kulak, ense, boyun çakışması görülmedi. |
| LOD | Temiz editörde ayarlandı (LOD1 %65 ×1,25 / LOD2 %40 ×1,7 / LOD3 kask), yeniden açılışta korunmuş. Önden ve 45°'den 1,25 / 3 / 6 / 9 / 12 / 16 m'de alın örtüsü, ayrım, tepe silüeti, arka ve topuz sıçramıyor; kask yakında görünmüyor. **20 m: TEST EDİLMEDİ.** Kamera stüdyo kapanının dışında kalıp yalnız arka plan yüzeyini görüyor; ayrı test sahnesi kurulmadı. Aktif LOD indeksi bu build'de Python'dan okunamıyor. |
| Yeniden açılış | Temiz editörde yüz (D), DNA, 858 morph, h39i groom'ları, materyaller, kask ve 4 bağlama yüklendi. Önce ve sonra kaydedilmemiş paket yok. |
| Korunan dosyalar | **54/54 birebir aynı.** |

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| YÜZ / DNA / TEN KORUNUMU | BAŞARILI |
| KÖKLERİN YÜZEYE BAĞLANTISI | BAŞARILI (kökte itme 0; yakın planda yüzen kök yok) |
| ALIN ÖRTÜCÜLÜĞÜ | BAŞARILI (seyrek bant yok; hairline h38d'ye göre biraz daha belirgin) |
| KÖKTEN SONRA DOĞAL YÜKSELİŞ | BAŞARILI (+30°: 1,1 → 1,8 cm, +20°: 0,9 → 2,5 cm; dik tel duvarı yok) |
| ÖN–TEPE HACİM DAĞILIMI | BAŞARILI |
| AYRI BOMBE GÖRÜNÜMÜNÜN GİDERİLMESİ | BAŞARILI (tepe 3,4–3,6 cm'lik arka tepe noktası yerine +20…−50° arasında 2,3–2,6 cm'lik tek kubbe) |
| TEPE–ARKA GEÇİŞİ | BAŞARILI |
| ARKA SİLÜET | BAŞARILI (D'nin kısalmış arka profili korundu) |
| TOPUZ GİRİŞLERİ | KISMEN (tek kavisle giriş, kanca yok; topuzun kendisi yeniden tasarlanmadı) |
| KULAK ARKASI DOĞAL AKIŞ | KISMEN (katılan/serbest ayrımı var; stüdyo ışığında arka taraf karanlık ve etki ölçülü, zor seçiliyor) |
| ORİJİNAL SAÇ KARAKTERİNE BENZERLİK | KISMEN (hacim dağılımı daha doğal; referansın dağınık, gevşek, şakağı örten karakteri hâlâ yok) |
| BÜTÜN BAŞIN GERÇEKÇİLİĞİ | KISMEN |
| BINDING | BAŞARILI |
| HAREKET | BAŞARILI (güçlü baş eğimi dahil) |
| LOD | KISMEN (16 m'ye kadar BAŞARILI; 20 m TEST EDİLMEDİ) |
| YENİDEN AÇILIŞ | BAŞARILI |
| KORUNAN DOSYALAR | BAŞARILI (54/54) |

## Açık kalanlar

- **Ayrım:** önde ince bir koyu çizgi kalıyor. h39f/g'deki V'den çok daha dar, h38d'ye yakın.
- **Alın kenarı:** h38d'ye göre biraz daha tanımlı (daha iyi örtü, biraz daha az yumuşak).
- **Profilde şakak/favori açık ve saç karakteri düzenli:** elle yazılmış rehber groom gerekiyor (önceki raporlardaki sınır).
- **20 m LOD:** ayrı sahnede test edilmeli.
- **Yöntem notu:** bütün değişiklikler kodla, oluşturucunun E kopyasında yapıldı. Serbest elle groom yapılmadı.

## Board'lar

| Board | İçerik |
|---|---|
| 01 | Bütün baş, ön ve 3/4: orijinal / h38d / h39i |
| 02 | İki profil: h38d / h39i; üretilmiş profiller yalnız YARDIMCI |
| 03 | Alın → tepe: kökten sonraki yükseliş, yakın plan ve bütün baş |
| 04 | Tepe → arka → topuz: ana teller ve uzaklık eğrisi; üst, profil, arka 3/4 |
| 05 | Alın kökleri / örtücülük: nötr ve yan ışık; reddedilen h39f |
| 06 | Kulak arkası ve topuz girişi, iki taraf |
| 07 | Silüet ve katmanlar: saçsız / ana saç (topuz dahil) / tam saç ve tel katmanları |
| 08 | Teknik: baş eğimi, hareket, LOD, yeniden açılış |
