# GD11 saç revizyonu I: ense paneli ve kulak altı saç çerçevesi (yüz sabit)

Tarih: 2026-10-05. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Production'a hiçbir şey geçmedi.

## Başlangıç (doğrulandı)

**Kaynak:** H raporu, commit `eb27b3b2`.

| Parça | Asset |
|---|---|
| Saç (başlangıç) | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementH_20261004/Hair/GR_LK_Hair_{Main,Loose}_h42d`, bağlamalar `GB_G11RH_*_f4abh42d` |
| Yüz / DNA / ten (değişmedi) | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementD_20261004/Face/SKM_G11RD_Face_f4ab`, `MHC_G11RD_F4AB_Head`, k10 / e2 / M_SlightArch / S_Thin |

- H'den daha yeni yerel çalışma yoktu.
- Kullanıcının bu tur gönderdiği **6 açılı referans sayfası** `reference/user_sheet_20261004.png` olarak saklandı ve board'larda referans olarak kullanıldı.

## Yeni aday

`/Game/Sphirus/CharacterLab/GD11_HeadRefinementI_20261004/`

| Parça | Asset / dosya |
|---|---|
| Saç | `Hair/GR_LK_Hair_{Main,Loose}_h43i` + kask; LOD tablosu ayarlı |
| Bağlamalar | `Face/Bindings/GB_G11RI_*_f4abh43i`; hepsi F4ab yüzünü hedefliyor |
| Korunan kaynak (Saved dışında) | `SourceAssets/Characters/GD11_HairI_20261004/`: `h43i/` (`build_env`, `strands`, `abc`, `guides.json`, `strand_tags.json`, `guides_edited.json`), `guides/h43i_guides.blend` (yeni `nape_lock` ve `under_ear` koleksiyonları dahil), katman 1 düzenleme ve taban JSON'ları, `tools/`, `reference/`, `README.txt` |

**Yazma yolları:** ilk çekimden önce bütün yollar I'ya yönlendirildi.

**Korunan dosyalar: 65/65 birebir aynı.** H (h42d) dahil.

## 0. Kılavuz gidiş-dönüşü

- h42d'nin kendi `.blend`'i, H'deki tek katmanlı yöntemle yeniden üretilince ana teller farklı çıktı (h43rt). Nedeni: h42d'nin topuz düzenlemesi zaten bir önceki katmanda (h42c, taban h41f) duruyordu ve "değişmemiş" sayılıp kayboldu.
- **Düzeltme: zincirleme katmanlar.**
  - Katman 1 (`SPH_GUIDES_IN` / `BASE`) önceki düzenlemeleri taşıyor.
  - Katman 2 (`SPH_GUIDES_IN2` / `BASE2`) bu turun `.blend` düzenlemeleri için.
- Değişiklik yapılmayan katmanlı gidiş-dönüş (h43rt2) h42d ile **bit bit aynı**. `guides_edited.json` yalnız katman 1'in 3 topuz düzenlemesini listeliyor.

## 1. İnce ense alanının kaynağı (board 04)

H'deki ters yamuk alan iki gruptan oluşuyordu:
- `nape_to_bun` (4 kilit, yaklaşık 4.470 tel);
- `corner_to_bun` (2.600 tel).

Her ikisi de kökten topuza yüzeye yatık, yoğun ve tek parça bir yüzey kuruyordu. Kökler alt saç çizgisine (z≈151–153) kadar iniyordu. Seyreltme yalnız tel sayısını azalttığı için **yamuk biçim kaldı**.

## 2. Ense: alan ve akış yeniden kuruldu, yalnız yoğunluk değil (board 02)

`SPH_NAPE_REPLACE`: `nape_to_bun` ve `corner_to_bun` telleri çıkarıldı. Diğer bütün teller aynı.

**`nape_lock` (yeni, ana groom)**
- 13 ayrı kilit; kök konumu, yama boyutu (0,6–0,65 cm), tel sayısı (190–250) ve yüksekliği farklı.
- Kökler **gerçek arka kafa yüzeyine** yerleştirildi (`SPH_NLOCK_SURF`): o x/z civarındaki en arkadaki kafa noktası.
- Kökler yumuşatılmış saç çizgisinin yaklaşık 2–3,4 cm üstünde. Toplanan saç alt saç çizgisinden değil, kulak memesi hizasının biraz altından başlıyor.
- Yakınsama 0,38; kilitler okunuyor ama ip gibi değil.
- Girişler topuzun alt yarısına yayılmış (`SPH_NLOCK_SPREAD` 0,8). Kılavuzlar düzenlenebilir: `nape_lock:0..12`.

**`nape_fine`:** saç çizgisi bandında (yaklaşık 1,8 cm) 750 kısa ince saç; uzunluk 0,5–1,1 cm, yön dağılımlı, uçları kıvrık.

**Serbest ense tutamları:** `nape_free_g` aynen kaldı.

**Reddedilen denemeler:**

| Deneme | Neden |
|---|---|
| h43n | 11 yüksek yakınsamalı kilit, tek giriş noktası. Topuzdan sarkan iki dar şerit gibi okundu. |
| h43g | Daha çok kilit, ama kökler hâlâ alt saç çizgisindeydi ve yanlış yüzeye yansıyordu. Profilde boynun arkasında sarkan bir kuyruk oluştu. |
| h43h | Kökler yukarıda ve yüzeyde; panel gitti. İnce saçlar eşit aralıklı dikey çubuk gibi duruyordu; h43i'de düzeltildi. |

**Sonuç:** ters yamuk panel ve sarkan şerit yok. Ense saç çizgisi ile toplanan saç arasında açık ten ve ince saçlar var. Kilitlerin alt ucu boyun ortasında hâlâ belirgin, hafif yatay bir yoğunluk sınırı oluşturuyor; ince saçlar da yakından kısa çizgiler gibi okunuyor. Referanstaki tamamen dağınık ense kadar doğal değil.

## 3. Kulak altı çerçevesi (board 03)

**H'deki durum:** sağdaki uzun yan tutam ailesinin üç seçeneği de kapalıydı (`SPH_SIDE_SKIP_R=0,1,2`), solda yalnız biri açıktı (`SPH_SIDE_SKIP_L=0,1`). Önden kulak altında yalnız birkaç ince tel kalıyordu.

**Eski uzun grup geri açılmadı.** Yerine yeni **`under_ear`** ailesi (serbest groom, simülasyonlu) kuruldu:
- **Kulak arkasından** veya **kulak kenarının üstünden** çıkan tutamlar.
- Kulak memesinin arkasından ve dışından geçiyor (|x| ≥ 8,2–9,3).
- Çene ve üst boyun hizasında, boyun hattının yanında bitiyor (|x| 7,0–7,8).

| Taraf | Tutam | Uç yükseklikleri (z) |
|---|---|---|
| Karakter solu | 3 | 156,2 / 153,0 / 150,8 |
| Karakter sağı | 4 | 156,8 / 155,4 / 152,2 / 151,0 |

- Kalınlık 0,30–0,44, tel sayısı ×1,3. Kulak, yanak ve boyun içinden geçmiyor.
- **Sonuç:** önden iki tarafta da kulak memesi altında saç okunuyor. Etki ölçülü; referanstaki dolgun, dağınık yan saç kadar hacimli değil.

## 4. Topuz, ön–tepe, ten

| Bölge | Durum |
|---|---|
| Topuz | Konum ve h42d'nin topuz düzenlemesi aynen. Ense kilitleri topuzun alt yarısına yayılarak giriyor. |
| Ön–tepe, alın, ayrım, renk | Değişmedi. |
| Ana groom simülasyonu | Kapalı (statik görüntü = render). |
| Serbest tellerin simülasyonu | Açık; `under_ear` ve `nape_free_g` dahil. |

## 5. Teknik (board 06)

| Kontrol | Sonuç |
|---|---|
| Bağlama | 4 bağlamanın hepsi `SKM_G11RD_Face_f4ab`'i hedefliyor. Yüz auto-rig yok. |
| Baş eğimi / dönüşler / koşu-durma / nötre dönüş | Temiz. Ense telleri boyna girmiyor; kulak altı tutamları kulak ve yanakla kesişmiyor. |
| LOD | Temiz editörde ayarlandı, yeniden açılışta korunmuş. Mesafe testi 1,25–25 m önden / 45° / arkadan. **Mesafe testi; aktif LOD indeksi okunamıyor.** |
| Yeniden açılış | Temiz editörde yüz, DNA, 858 morph, h43i, materyaller, kask ve 4 bağlama yüklendi; kaydedilmemiş paket yok. |
| Korunan dosyalar | **65/65** |

## Sorulara cevaplar

- **İnce ense alanının kaynağı?** `nape_to_bun` ve `corner_to_bun` gruplarının alt saç çizgisine kadar inen, yüzeye yatık tek parça yüzeyi.
- **Yalnız yoğunluk mu değişti?** Hayır. İki grup çıkarıldı; yerine farklı kök alanı, yönü, yüksekliği ve girişi olan 13 ayrı kilit ile ince saç bandı kuruldu.
- **Önden kulak altı görünürlüğü hangi gruplarla?** Yeni `under_ear` ailesi.
- **Sağdaki kapalı uzun grubun yerine ne kuruldu?** 4 `under_ear` tutamı. Eski uzun yan grup kapalı kaldı.
- **Solda ne yapıldı?** Solda da 3 `under_ear` tutamı eklendi; L'deki diğer saç değişmedi.
- **Topuz ve ön–tepe korundu mu?** Evet.
- **Yüz, DNA ve ten aynı mı?** Evet (65/65).
- **Devam eden eksikler:**
  - Ense kilitlerinin alt uçlarında hafif bir yoğunluk sınırı ve çizgi gibi okunan ince saçlar.
  - Kulak altı saç hacmi referanstan az.
  - Saç genel olarak referansa göre hâlâ düzenli.

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| ENSEDEKİ PANEL OKUMASI | KISMEN (yamuk panel ve sarkan şerit yok; kilit alt uçlarında hafif sınır kalıyor) |
| DOĞAL ENSE KÖK–TUTAM GEÇİŞİ | KISMEN |
| ÖNDEN KULAK ALTI ÖRTÜCÜLÜĞÜ | KISMEN (iki tarafta okunuyor, hacim az) |
| SAĞ/SOL SAÇ ÇERÇEVESİ | KISMEN |
| ÖN–YAN–ARKA SÜREKLİLİĞİ | KISMEN |
| TOPUZ–ENSE BÜTÜNLÜĞÜ | BAŞARILI |
| ÖN–TEPE KORUNUMU | BAŞARILI |
| ORİJİNAL SAÇ KARAKTERİNE BENZERLİK | KISMEN |
| YÜZ/DNA/TEN KORUNUMU | BAŞARILI |
| BINDING | BAŞARILI |
| HAREKET | BAŞARILI |
| LOD/MESAFE | BAŞARILI (mesafe testi) |
| YENİDEN AÇILIŞ | BAŞARILI |

**Yöntem:** bütün değişiklikler kodla yapıldı (oluşturucunun I kopyası, yeni tutam aileleri, düzenlenebilir kılavuzlar ve tablolar). Serbest elle groom yapılmadı.

## Board'lar

| Board | İçerik |
|---|---|
| 01 | Bütün baş: referans sayfası / h42d / h43i; ön ve iki 3/4 |
| 02 | Ense: h42d / reddedilen h43n / yalnız ense h43h / final h43i; referans arka |
| 03 | Kulak altı: h42d / yalnız kulak altı h43e / final |
| 04 | Kaynak ve kılavuzlar: grup renkli katmanlar ve düzenlenen kılavuzlar |
| 05 | İki profil |
| 06 | Teknik |
