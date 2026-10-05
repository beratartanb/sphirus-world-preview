# GD11 saç revizyonu J: ense, kulak arkası ve topuz bağlantısı tek akış olarak (yüz sabit)

Tarih: 2026-10-05. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Production'a hiçbir şey geçmedi.

## Başlangıç (doğrulandı)

**Kaynak:** I raporu, commit `079715c9`.

| Parça | Asset |
|---|---|
| Saç (başlangıç) | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementI_20261004/Hair/GR_LK_Hair_{Main,Loose}_h43i`, bağlamalar `GB_G11RI_*_f4abh43i` |
| Yüz / DNA / ten (değişmedi) | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementD_20261004/Face/SKM_G11RD_Face_f4ab`, `MHC_G11RD_F4AB_Head`, k10 / e2 / M_SlightArch / S_Thin |

- I'dan daha yeni yerel çalışma yoktu. I'nın çalışması (h43i) olduğu gibi duruyor.
- Kullanıcının 6 açılı referans sayfası (`data/user_sheet_20261004.png`) board 01'de referans olarak kullanıldı.

## Yeni aday

`/Game/Sphirus/CharacterLab/GD11_HeadRefinementJ_20261005/`

| Parça | Asset / dosya |
|---|---|
| Saç | `Hair/GR_LK_Hair_{Main,Loose}_h45b` + kask `SM_LK_HairHelmet_h45b`; LOD tablosu ayarlı |
| Bağlamalar | `Face/Bindings/GB_G11RJ_{HairMain,HairLoose,EyebrowsM_SlightArch,EyelashesS_Thin}_f4abh45b`; hepsi `SKM_G11RD_Face_f4ab`'i hedefliyor |
| Korunan kaynak (Saved dışında) | `SourceAssets/Characters/GD11_HairJ_20261005/`: `h45b/` (`build_env`, `strands.npz`, iki `abc`, `guides.json`, `strand_tags.json`, `guides_edited.json`), `guides/h45b_guides.blend` (yeni `nape_spine` koleksiyonu dahil), katman 1 taban ve düzenleme JSON'ları, `tools/`, `diag/`, `README.txt` |

**Yazma yolları:** ilk çekimden önce stüdyo, çekim, bağlama ve kayıt yolları J'ye yönlendirildi; J betikleri B..I adaylarına bağlama yazmayı reddediyor.

**Korunan dosyalar: 68/68 birebir aynı** (I/h43i dahil; `data/preservation_check.json`).

## Kullanıcının üç sorusuna doğrudan cevap

**1. Ense artık tıraşlanmış gibi değil, doğal köklerden toplanan uzun saç mı?**
Evet, yapı olarak. h43i'nin 13 ayrı `nape_lock` kökü saç çizgisinin 0,6–5,8 cm **üstündeydi** (çizgiye 1 cm yakın kök: %0) ve altta kısa `nape_fine` bandı vardı; bu "kısa kesilmiş ense + ayrı sivri tutamlar" okumasını veriyordu. h45b'de iki aile de kapatıldı; yerine **tek bir kök alanı** (`nape_field`, 5.400 kök) yumuşak ense saç çizgisinden başlayıp (köklerin %18'i çizgiye 1 cm içinde, %4'ü çizginin en çok 0,7 cm altında) yukarı doğru devam ediyor. 4.692 uzun tel (11–26 cm, ortanca 16,9) kökten topuzun alt yarısına kadar kesintisiz gidiyor; 691 kısa serbest tel ve 17 kenar teli ensede yumuşak kenar veriyor. Tel ortası kafatasına 0,6 cm'de; kaldırma yalnız son üçte birde, topuza girişte. Ense bandı, kök adaları, L/yamuk panel yok. **Ama** dürüst okuma: arkadan bakışta ense kütlesi referanstaki dağınık enseden daha düzenli ve alt kenarı daha net; "doğal uzun saç toplanmış" okunuyor, "dağınık" okunmuyor.

**2. Kulak arkası gerçek kök ve hacimle kuruldu mu, kulağı kapatmadan?**
Kısmen. Yeni `ear_frame` ailesi (315 tel, serbest groom) köklerini kulağın **arkasındaki** kafa derisinden alıyor (kulak kutusu içinde kök yok; kök yüksekliği çizginin −0,1…6,4 cm üstü), kulağın arkasından/altından iniyor ve çene–üst boyun hizasında bitiyor. İlk sürüm (h45a) iniş sırasında kulak kepçesine yapışıyordu; h45b'de kulaksız yüzeye yansıtma ve kulak arkası sınırlaması eklendi (kulak kutusuna giren nokta: h43i `under_ear` 10.989 → h45b 94). Kulak kepçesi profilde ve önden okunuyor. Ek olarak ense alanı kulak arkası bölgesinde ×1,45 yoğunlaştırıldı ve hafifçe (0,16) kaldırıldı. **Eksik:** kulak arkası kütle hâlâ referanstan ince; önden kulak altında yalnız ince teller görünüyor. Kulak üstü `temple_veil` perdesi kaldırılmadı, yarıya indirildi (832 → 309 tel) ve kulağın üstünden geçen tutam kapatıldı; board 03 son sütun bu perde gizliyken yapıyı gösteriyor.

**3. Ense–yan–topuz arasında sürekli, doğal bir toplanma ilişkisi var mı?**
Evet. Her ense teli 9 omurga çizgisinden birinin (`nape_spine:0..8`, düzenlenebilir kılavuz) karışımını izleyerek topuzun alt yarısına kendi x konumuna göre dağılarak giriyor (uç–topuz merkezi 1,07 ± 0,28 cm). Arka 3/4 görünümlerde ense ve kulak arkası aynı yöne, topuza doğru akıyor; dar boğaz veya kuyruk yok. Bağlantı üst kısımda yüzeyde yatık; kulak arkası ile ense arasında belirgin bir kütle sınırı kalmıyor.

## 0. Teşhis (board 03)

h43i'de sivri tutamları yapan gruplar, renk kodlu katmanlarla doğrulandı:

| Grup | Sorun |
|---|---|
| `nape_lock` (13 kilit, 2.860 tel) | Kökler saç çizgisinin 2–3 cm üstünde yama yama adalar; yakınsamış demetler; uçlar aynı seviyede (std 0,34) → **sivri tutamlar** |
| `under_ear` (746 tel) | Kökler kulağın üstünde/kenarında; kulak kutusuna 10.989 nokta; yüzeyden 2 cm → kulağa yapışık kalın yan tutamlar |
| `behind_ear`, `ear_lock` | Kanca biçimli, yüzeyden 3,7–4 cm uzak |
| `nape_fine` | Kısa (1 cm) dikey teller; 24'ü saç çizgisinin altında → tıraşlı bant okuması |

## 1. Yeni kurulum (board 02, 04)

- `SPH_NAPE_REPLACE` + `SPH_NAPE_FIELD`: `nape_lock`, `nape_fine`, `nape_free_g`, `behind_ear`, `ear_lock` ve `under_ear` kapalı; eski `nape_to_bun`/`corner_to_bun` zaten kapalıydı.
- **`nape_field`**: kök alanı, yumuşak ense çizgisinden (merkezde z≈151, yanlarda 161'e yükselen) açıya bağlı üst sınıra kadar; kenar yoğunluğu 0,95 (kök adası/sıra yok), yama gürültüsü 0,25. Her tel komşu omurgaların Gauss karışımı + yavaş akış gürültüsü (0,7) + alt tutam gürültüsü (0,22); yakınsama 0,25 (ip yok). Kaldırma: kafatasına yatık (0,03→0,08) ve ancak t>0,62'den sonra topuza doğru 0,22. Topuza giriş: `bun_loop` ile mevcut topuz halkalarına.
- **`ear_frame`**: kulak arkası kafa derisi üçgenleri; kısa/orta/uzun uç sınıfları (%55/%45/kalan); kümelenmiş hedefler, S dalgası, uç dağılımı; kulaksız BVH ile iniş; kulak kutusu önüne geçiş engeli.
- Ön–tepe, ayrım, alın çizgisi, şakak tutamları, topuz konumu ve halkaları, renk: değişmedi. Katman 1 kılavuz düzenlemeleri (bun 6/7/9) taşındı; `guides_edited.json` yalnız bunları listeliyor. Bu turda `.blend` üzerinden el düzenlemesi **yapılmadı**; `nape_spine` kılavuzları kodla üretildi ve `.blend`'de düzenlenebilir durumda.

**Reddedilen ara sürümler:**

| Sürüm | Neden |
|---|---|
| h44a | Kaldırma t=0,5'ten başlıyordu, sert bant kenarları → kafadan ayrık kalkık levha |
| h44b | Üst sınır kademeli → arkadan dikey "sütun" kenarları |
| h44c (UE'de çekildi) | Profiller sivri tutamsız, ense sürekli; kulak arkası zayıf ve `ear_frame` dar şerit |
| h44d | Saç çizgisi inceltme / kök yükseltme yönü; kullanıcı yönergesiyle **reddedildi**, içe alınmadı |
| h45a | `ear_frame` inişte kulak kepçesine yapıştı |

## 2. Üretim kontrolü (board 05, `data/strand_control.json`)

Kılavuz biçimini yoğun telde bozan dört etki ölçüldü: yakınsama (uç–topuz std 0,28; kök komşu aralığı 0,05/0,09 cm düzgün), aynı seviyeli uç (serbest tellerde std 2,3 → dağılmış; topuza girenlerde 0,49 = aynı giriş bölgesi, beklenen), yüzey düzleşmesi (q1/orta 0,30/0,62 cm; levha yok), itme ayrışması (kulak kutusu 94 nokta, kafa içine giriş yok). Ana groom simülasyonsuz (statik görüntü = render); serbest groom (`ear_frame`, `side_long`, `temple_veil`) simülasyonlu.

## 3. Teknik (board 06)

| Kontrol | Sonuç |
|---|---|
| Bağlama | 4 bağlama `SKM_G11RD_Face_f4ab`; yüz auto-rig yok |
| Hareket (bakınma, dönüşler, durma), baş eğimi | Temiz; ense telleri boyna, kulak arkası telleri kulak/yanağa girmiyor |
| LOD | Temiz editörde ayarlandı, yeniden açılışta korunmuş; mesafe testi 1,25–25 m ön / 45° / arka. **Aktif LOD indeksi okunamıyor; mesafe testi görsel.** |
| Yeniden açılış | Temiz editörde yüz, DNA, 858 morph, h45b groom'ları, MI'lar, kask ve 4 bağlama yüklendi; kaydedilmemiş paket yok |
| Korunan dosyalar | **68/68** |

## Değerlendirmeler (teknik ve sanatsal ayrı)

| Başlık | Sonuç |
|---|---|
| ENSE: DOĞAL KÖKTEN UZUN SAÇ (tıraşlı bant yok) | BAŞARILI (teknik) / KISMEN (sanatsal: alt kenar referanstan düzenli) |
| AYRI SİVRİ TUTAM / İP / DİŞ YOK | BAŞARILI |
| L / YAMUK / PANEL YOK | BAŞARILI (teknik) / KISMEN (arkadan yoğun blok okuması hafif) |
| KULAK ARKASI GERÇEK KÖK VE HACİM | KISMEN (kökler doğru; hacim referanstan az) |
| KULAK KEPÇESİ OKUNUR, YAN PERDE YOK | KISMEN (`temple_veil` yarıya indirildi, kaldırılmadı) |
| ENSE–YAN–TOPUZ TEK AKIŞ | BAŞARILI |
| ÜRETİM KILAVUZ BİÇİMİNİ KORUYOR | BAŞARILI |
| ÖN–TEPE, TOPUZ KONUMU, RENK KORUNUMU | BAŞARILI |
| YÜZ/DNA/TEN/BEDEN KORUNUMU | BAŞARILI (68/68) |
| BINDING / HAREKET / YENİDEN AÇILIŞ | BAŞARILI |
| LOD/MESAFE | BAŞARILI (görsel mesafe testi) |
| REFERANSA GENEL BENZERLİK (saç) | KISMEN |

"Daha çok tel" veya "panel inceldi" başarı sayılmadı; yapı değişikliği kök alanı, kök yüksekliği ve akış ölçümleriyle gösterildi.

## Board'lar

| Board | İçerik |
|---|---|
| 01 | Bütün baş: referans / h43i / h45b; ön, iki 3/4, iki profil, arka |
| 02 | Ense–kulak arkası–topuz: arka ve iki arka 3/4 (önce/sonra), ense kırpımları (h43i / h44c / h45b), yakın çekimler |
| 03 | Renk kodlu grup teşhisi h43i vs h45b; kök/akış görselleştirmesi; perde gizli |
| 04 | Kılavuzlar (h45b, h43i hayalet), ucuz ön izlemeler h44a/b/c/h45b, UE yoğun sonuç |
| 05 | Üretim kontrol tablosu; katman çekimleri; kulak arkası/altı (h43i / h44c / h45b) |
| 06 | Teknik: hareket, baş eğimi, yeniden açılış, LOD mesafe |

**Yöntem:** bütün değişiklikler kodla (oluşturucunun J kopyası `tools/blender_g11rj_hair.py`, yeni aileler, ortam tablosu `data/hair_h45b_build_env.txt`, fark `data/hair_h43i_to_h45b_env_diff.txt`). Serbest elle groom yapılmadı. Yeniden üretim: `tools/build_hair.sh h45b`.
