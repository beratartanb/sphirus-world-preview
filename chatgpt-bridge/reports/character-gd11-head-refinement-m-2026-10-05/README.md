# GD11 baş revizyonu M: F4ab + h47a başlangıcından kontrollü devam — hafif yumuşak doku (m2), daha yumuşak burun, arka saç mimarisi (h48a)

Tarih: 2026-10-05. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Production'a hiçbir şey geçmedi. Kimlik korundu (aynı karakter; K5 işlemleri tekrarlanmadı).

## Başlangıç (doğrulandı) ve yeni aday

| Durum | Yüz | DNA | Saç | Bağlamalar | Ten |
|---|---|---|---|---|---|
| **S başlangıç** | `GD11_HeadRefinementD_20261004/Face/SKM_G11RD_Face_f4ab` | `MHC_G11RD_F4AB_Head` | `GD11_HeadRefinementL_20261005/Hair/GR_LK_Hair_{Main,Loose}_h47a` | `GB_G11RL_*_f4abh47a` | k10 / e2 |
| **FO yalnız yüz** | `GD11_HeadRefinementM_20261005/Face/SKM_G11RM_Face_m2` (yeni auto-rig, 858 morph) | `MHC/DNA/MHC_G11RM_M2_Head` | h47a | `GB_G11RM_*_m2h47a` | aynı |
| **HO yalnız saç** | F4ab | F4AB | `GD11_HeadRefinementM_20261005/Hair/GR_LK_Hair_{Main,Loose}_h48a` | `GB_G11RM_*_f4abh48a` | aynı |
| **C birleşik** | m2 | M2 | h48a | `GB_G11RM_*_m2h48a` | aynı |

Her çekim setinin kompozisyonu editörden okundu (`prov/*.json`: mesh, DNA, groom, binding + hedef, anim sınıfı, forced LOD, baş soket dönüşümü, zaman). Başlangıç = L raporunun son onaylı kombinasyonu (commit `2244dbcb`). Korunan dosyalar: **81/81 grup birebir aynı** (`data/preservation_check.json`; R3…L adayları, K kaydı, production, beden, kıyafet dahil).

## Etlilik hangi bölgelerde eklendi (m2 = F4ab + `data/ops_M2.json`, 15 yerel op)

| Bölge | İşlem | Büyüklük |
|---|---|---|
| Göz altı / infraorbital | çukur dolgusu (hfill, kapak kenarının altında sönüyor) + göz altı–yanak geçişi | ≤0,5 mm / +0,5 mm |
| Malar / elmacık çevresi | yumuşak doku (normal yönünde, burun dondurulmuş) | +1,4 mm |
| Orta yüz | geniş, çok yumuşak öne alan (nazolabial bölge hariç değil, burun dondurulmuş) | +0,9 mm |
| Yan yüz → kulağa doğru | yanal alan (kulak önü y>3,6'da sönüyor) | +1,1 mm |
| Elmacık altı / bukkal | çukur dolgusu (hfill) | ≤1,0 mm |
| Pre-jowl | çok hafif yumuşatma | +0,35 mm |
| Gevşetme | yanak ve sırt geçişleri (1 tur) | — |

Toplam (`data/heat_M2.txt`): en büyük yer değişimi **1,67 mm** (x 5,0 / y 9,4 / z 158,3 — sol elmacık altı). Korunanlar: dudaklar 0,00 / 0,01 mm, filtrum–burun tabanı 0,00, çene (z<153) ≤0,34, çene köşesi ≤0,6 mm, alt kapak kenarı ≤0,60, üst kapak ≤0,24, kulaklar ≤0,86 (kulak önü deri), kafatası 0,00, göz küreleri 0,000. Çene büyütülmedi, alt yüz uzatılmadı, jaw sertleştirilmedi, ağız–çene mesafesi değişmedi (orta çizgi profili aynı: `data/nose_profile_metrics.txt`).

## Burunda hangi ilişki yumuşatıldı

Orta çizgi profili (kök dibi 4,57 mm, kaş arası, sırt eğimi) **değişmedi**; yumuşatma yanal: üst/orta sırt yan duvarları +0,7 mm (dar, keskin kolon → daha dolu, yumuşak sırt), kök yanları +0,4 mm (kök–göz çukuru geçişi), uç yuvarlaklık +0,5 mm, supratip +0,3 mm, sırt gevşetme. Taban, kanatlar, delikler, kolumella, filtrum ve üst dudak değişmedi (kanat bölgesi ≤0,7 mm = yan duvar devamı, delik iç yüzeyleri 0). Sonuç board 04'te: önden daha az keskin kolon, 3/4'te daha rafine, profilde aynı çizgi (kırık/kemer yok).

## Saçta arka yapıda ne değişti (h47a → h48a; `data/hair_h47a_to_h48a_env_diff.txt`)

- **Uzun yan ipler kaldırıldı**: `side_long` ailesi tamamen kapalı (`SPH_SIDE_SKIP_L=0,1,2`) — "iki dekoratif ip / 3 çizgi gibi inen saç" kaynağı buydu.
- **Ense alt kenarı düzensiz**: yeni `SPH_NFIELD_EDGEJAG` 0,45 (kök çizgisi eşiğine tutarlı gürültü) + daha fazla kısa serbest tel ve kenar teli (`FREE` 0,30, `WISP` 0,30, `RAMP` 1,1) → düz çizgi / levha kenarı yok; kökler yine doğal ense çizgisinde (%16 çizgiye 1 cm içinde, uzunluk 11–25 cm).
- **Katmanlama**: kaldırma varyasyonu 1,0 (tutarlı alt tutam kümeleri farklı mesafede) → topuz altı blok/panel azaldı.
- **Kulak arkası**: `ear_frame` 672 tel korundu (kulak kutusu nokta 216; kepçe açık); kulak üstü perde yok.
- **Ön saç çizgisi / tepe**: kök yoğunluğu 1,1 → 1,3, kenar yoğunluğu 0,22 → 0,34 (kel/seyrek bant okuması azaldı), ön kaldırma 0,9 → 1,1 ve LF_FRONT 0,5 → 0,7 (yapışık değil), bebek saçı 3.600 → 4.200, yüz çerçevesi tutamları ×0,5 (0,35), tepe bombe LF_TOP 3,0 → 3,3 ve BUMP_TOP 1,15.
- Topuz konumu/boyutu aynı; arka kütle büyütülmedi (ana tel sayısı 67.965 → 69.282; artış ön/tepe).

Görsel (board 02/05): **yan ipler gitti** (profil/3/4'te omuza inen tek tel yok); **ense alt kenarı** artık düzensiz ve tüylü, düz çizgi/levha/L okuması yok; kökler ense çizgisinde; ense–topuz akışı sürekli; **kulak arkası** dolu, kepçe okunuyor; **saç çizgisi** önden biraz daha dolu ve daha az yapışık; tepe bombesi hafif daha yuvarlak. Topuz altı daha katmanlı ama hâlâ düzenli (referansın dağınıklığı yok). Ana tel sayısı 67.965 → 69.282 (artış ön/tepe ve ense serbest teller), kulak arkası aynı (672).

## Değişiklik ayrımı (board 03)

Başlangıç | yalnız yüz | yalnız saç | birleşik — aynı kameralar ve ışık; yüz etkisi (yanak/burun yumuşaklığı) saçtan bağımsız, saç etkisi (arka kenar, ipler, saç çizgisi) yüzden bağımsız görünür.

## Teknik (board 07)

| Kontrol | Sonuç | Kayıt |
|---|---|---|
| Rig (m2: yeni auto-rig, fit ortalama 0,017 mm, p95 0,067, 858 morph; 54 çekim, saç gizli: göz kırpma tek/çift, bakış 4 yön, kaş, gülümseme, dudak kapama, çene/ağız, vizemler, üst dudak, burun deliği, yanak) | Temiz; dudak ayrılması, kapak açıklığı, nostril çökmesi yok | `g11rmrig_*`, `data/rig_MHC_G11RM_M2.json` |
| Bağlamalar | `GB_G11RM_*_m2h48a` → hedef `SKM_G11RM_Face_m2` (yeniden açılışta okundu); yalnız-saç durumu `GB_G11RM_*_f4abh48a` → F4ab; başlangıç `GB_G11RL_*_f4abh47a` → F4ab | `data/reopen_check.json`, `prov/*.json` |
| Hareket (27) + baş eğimi (7) + ışık setleri (10) | Temiz; kulak/boyun kesişmesi, kök kopması yok | `g11rmmot_*`, `g11rmP_*`, `g11rmRL_*` |
| Groom LOD | Temiz editörde ayarlandı; yeniden açılışta tablo aynı; mesafe 1,25–25 m (24 çekim) **görsel**; aktif LOD indeksi okunamıyor | `G11RM_LOD`, `g11rmlod_*` |
| Yeniden açılış | m2 (858 morph, DNA `MHC_G11RM_M2_Head`), h48a groom'ları, MI'lar, kask, 4 bağlama yüklendi; kirli paket yok | `data/reopen_check.json` |
| Kaynak/bellek | Zincir öncesi C: 21,8 GB boş; editör çökmesi yok; 1 auto-rig | — |
| Korunan dosyalar | 81/81 | `data/preservation_check.json` |

## Hâlâ kalan eksikler

- Yüz: etlilik ölçülü (≤1,7 mm); referansın yumuşak, dolgun orta yüzüne göre hâlâ daha ince bir yüz. Göz çevresi/sakin ifade ve kaş groom yerleşimi değiştirilmedi (açık iş). Çene/alt yüz bilerek dokunulmadı.
- Burun: yalnız yan duvar/uç yumuşatması; genişlik ve taban aynı — referanstan hâlâ daha dar.
- Saç: ana ön/şakak kütlesinin yönü oluşturucuda hâlâ topluca geriye; çaprazlık ek tutamlarla. Topuz altı daha katmanlı ama hâlâ düzenli; referansın tamamen dağınık topuzu yok. Aktif groom LOD indeksi Python'dan okunamıyor (mesafe testi görsel).
- Aktif LOD indeksi doğrulanamadı; oyun ışığında (gün ışığı rigi) kontrol bu turda yapılmadı.

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| BAŞLANGIÇ DOĞRULAMA / KİMLİK KORUNUMU | BAŞARILI |
| ORTA YÜZ / YANAK ETLİLİĞİ | KISMEN (ölçülü, görünür; referanstan az) |
| GÖZ ALTI–YANAK GEÇİŞİ | KISMEN |
| ALT YÜZ / ÇENE KORUNUMU | BAŞARILI (≤0,34 mm) |
| BURUN YUMUŞAKLIĞI (kök–sırt–uç) | KISMEN |
| BURUN TABANI / DELİKLER / ÜST DUDAK KORUNUMU | BAŞARILI |
| SAÇ: ENSE (yoğun, doğal kökten topuza, levha/L/ip yok) | BAŞARILI (yoğun, doğal kökten topuza; levha/L/ip yok) |
| SAÇ: KULAK ARKASI | KISMEN |
| SAÇ: TOPUZ ALTI | KISMEN (daha katmanlı; hâlâ düzenli) |
| SAÇ: ÖN SAÇ ÇİZGİSİ / TEPE | KISMEN (daha dolu, daha az yapışık; referansın dağınık ön tutamları yok) |
| REFERANSA GENEL BENZERLİK | KISMEN |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (aktif LOD indeksi TEST EDİLMEDİ) |
| ESKİ KAYNAKLARIN KORUNUMU | BAŞARILI (81/81) |

## Board'lar

01 yüz önce/sonra (7 görünüm + referans çerçeveleri) · 02 saç önce/sonra (7 görünüm + arka ışık) · 03 birleşik final + ayrıştırma · 04 burun/orta yüz yakın plan · 05 ense/kulak arkası/topuz altı/saç çizgisi yakın plan · 06 korunan bölgeler (ısı haritası + clay) · 07 teknik.
