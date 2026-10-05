# GD11 baş revizyonu N: m2/h48a üzerinden — kaş yerleşimi, burun formu, ana saç akışı (yüz tipi korundu)

Tarih: 2026-10-05. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Production'a hiçbir şey geçmedi.

## Başlangıç (doğrulandı) ve adaylar

| Durum | Yüz / DNA | Kaş | Saç | Bağlamalar |
|---|---|---|---|---|
| **S başlangıç** | `GD11_HeadRefinementM_20261005/Face/SKM_G11RM_Face_m2` / `MHC_G11RM_M2_Head` | `GR_GD_Eyebrows_M_SlightArch` | `GD11_HeadRefinementM_20261005/Hair/GR_LK_Hair_{Main,Loose}_h48a` | `GB_G11RM_*_m2h48a` |
| **BO yalnız kaş** | m2 | `GR_GD_Eyebrows_M_Fine` | h48a | `GB_G11RN_*_m2h48a` (N'de yeniden) |
| **NO yalnız burun** | `GD11_HeadRefinementN_20261005/Face/SKM_G11RN_Face_n1` / `MHC_G11RN_N1_Head` (yeni auto-rig) | M_SlightArch | h48a | `GB_G11RN_*_n1h48a` |
| **HO yalnız saç** | m2 | M_SlightArch | `GD11_HeadRefinementN_20261005/Hair/GR_LK_Hair_{Main,Loose}_h49a` | `GB_G11RN_*_m2h49a` |
| **C birleşik** | n1 | M_Fine | h49a | `GB_G11RN_*_n1h49a` |

Ten/göz k10/e2, kirpik S_Thin (hepsinde aynı). F4ab + h47a karşılaştırma kaynağı olarak korundu. Her çekim setinin kompozisyonu editörden okundu (`prov/*.json`). Korunan dosyalar: **84/85 grup aynı** (`data/preservation_check.json`): tek fark M kaynak verisine eklenen iki teşhis metni (`data/param_audit_unused.txt`, `data/head_source_check.txt`); hiçbir asset/kaynak değişmedi, hiçbir dosya silinmedi.

## Sorulara doğrudan cevaplar

| Soru | Cevap |
|---|---|
| m2'nin etliliği korundu mu; yeni genel dolgu yapıldı mı? | **Korundu; genel dolgu yapılmadı.** Bu turun yüz geometrisi değişikliği yalnız burun bandında (n1 = m2 + 7 yerel burun opu; burun dışı bölgelerde m2'ye göre 0,00 mm: dudak, çene, yanak, kulak, kafatası; kapaklar ≤0,27 mm). F4ab'a göre toplam fark hâlâ en çok 1,67 mm (m2'nin yanak dolguları), >1 mm 632 vertex. |
| Kaş değişikliği göz çevresini referansa yaklaştırdı mı? | **Kısmen.** Aynı m2 + h48a üzerinde: mevcut M_SlightArch (yüksek, ince, kemerli), kaş gizli (tanı), ve 4 kütüphane alternatifi (M_Natural, Soft, S_FlatThin, M_Fine) çekildi (board 02). **M_Fine** seçildi: daha dolu, daha düz, göze daha yakın oturuyor; referansın dolgun düz kaşına en yakın olan. Dürüst sınır: kütüphane kaş groom'ları ikili asset — kılavuz/kök yerleşimi düzenlenemedi; yükseklik/kuyruk yönü ancak prosedürel bir kaş groom'uyla (hair oluşturucusu yolu) değiştirilebilir; bu yapılmadı (açık iş). Göz kürelerine, kaş kemiğine, kapaklara dokunulmadı. |
| Burunda hangi gerçek biçim farkı düzeltildi? | Önden/3/4'ten **sırtın dar, keskin kolon** okuması: orta sırt yan duvarları +0,8 mm, üst yan duvar +0,5 mm, kök yanları +0,3 mm, uç lobülleri yana +0,6 mm, supratip +0,3 mm, infratip +0,2 mm, sırt gevşetme (`data/ops_N1.json`, `data/heat_N1_vs_m2.txt`). Taban, kanat kıvrımı, delik iç yüzeyleri, kolumella, filtrum, üst dudak: 0,00 mm. |
| Burun profili değişmediyse neden? | Orta çizgi (kök dibi kirişin 4,57 mm altında, kaş arasının 2,6 mm altında; düz sırt, kemer/tümsek yok; uç açısı) referansın ön ve yakın 3/4 görüntüsündeki düz, yumuşak sırt karakteriyle çelişmiyor; yardımcı profiller yalnız yön veriyor ve "kemer/kırık" göstermiyor. "Kemikli" okuma yanal darlıktan geliyordu (sıyırma ışığında dar parlak sırt çizgisi). Bu yüzden profil hattı bilerek değiştirilmedi; bir kavis eklemek "değişiklik yapmış olmak için" olurdu. |
| Ana ön/şakak akışı değişti mi, yoksa yine yalnız ek tutam mı? | **Ana kılavuzlar değişti.** 23 ana kilit merkez çizgisi (20 ön-yan + 3 kulak arkası, `prim:*`) ve 8 ense omurgası katman-2 kılavuz düzenlemesiyle (kod, `tools/blender_g11rn_guides_edit.py` → `guides/n1_guides.json`; oluşturucu 37 düzenlenmiş kılavuz raporladı) yeniden yönlendirildi: ilk %42'lik bölüm şakak üzerinden aşağı-geriye (−2,6 cm z, −0,9 cm y) süpürülüp kulak üstüne iniyor, sonra topuza çıkıyor; yoğun tel üretimi bunu izledi: 20.450 ana tel ≥0,5 cm hareket etti (front_to_bun 9.813, side_to_bun 10.560; ortalama 2,5 cm) (`data/mainflow_change.txt`). Board 04 **serbest groom gizliyken** (yalnız ana kütle) h48a/h49a farkını gösteriyor. Dürüst sınır: sonuç tam bir çapraz örtüşme değil, şakak üstünde eğik bir dip + daha geriye yatan yan kütle; ilk 10 noktanın ortalama yön vektörü büyük ölçüde geriye (−7,4 cm y) kaldı. |
| Etkin olmayan hangi parametreler tespit edildi? | `SPH_BUMP_TOP` oluşturucuda hiç okunmuyor; `LF_TOP`, `LF_FRONT`, `LF_BACK`, `LF_BASE`, `LF_TOPBACK_CUT` yalnız `lift_field()` içinde — etkin yol `SPH_FLOW_E=1` + `SPH_FIELD_PATH=1` ile `lift_field_arc()` (SPH_ARC_KNOTS); `SPH_FRONT_LIFT` yalnız `region_lift()` içinde (SPH_FIELD=1 ile kullanılmıyor). **M raporunda LF_TOP 3,0→3,3 / LF_FRONT 0,5→0,7 / BUMP_TOP 1,15 "tepe bombesi / ön kaldırma" gerekçesi geçersizdi** — tepe/ön hacmi değişmedi; h48a'daki görünür değişiklikler HL_DENS/HL_EDGE (kök yoğunluğu), BABY, FACE_MULT (0,35→0,50 artış), side_long kapatma, EDGEJAG/WISP/FREE/LIFT_VAR'dan geldi. (`data/param_audit_unused.txt`). Saç kafa kaynağı: `headC8.npy` (Guardian7) — m2'ye göre kafa derisi ortalama 0,36 mm / en çok 2,1 mm, şakak çizgisi bölgesi en çok 3,3 mm (`data/head_source_check.txt`); kökler binding ile m2/n1 yüzeyine yansıtılıyor (editörde `binding_target`/`binding_source` okundu). |
| Ense ve topuz altı, ince teller gizliyken de doğal mı? | **Kısmen.** Serbest groom gizliyken (board 05 'main only'): ense yoğun ve doğal çizgiden topuza akıyor; ince teller/kaçaklar olmadan da levha/L/ip yok; h49a'da ense omurgaları (8) yanal/kaldırma/giriş yüksekliği değişimli → arkadan bakışta alt tutamlar birbirini çaprazlıyor, tek düz yüzey okuması azaldı; ense alt kenarı ana kütlede de düzensiz (EDGEJAG ana `nape_field` köklerine uygulanıyor, serbest tellere değil). Topuz altı hâlâ düzenli ve koyu; referansın dağınıklığı yok. Topuz konumu aynı. |
| Kulak arkası hacim gerçek yapıyla mı kuruldu? | Kulak arkasındaki kütle ana groom'un `nape_field` kökleri (kulak arkası yoğunluk ×2,0) + 3 yeniden yönlendirilmiş ana kilit (`prim:6/35/63`, kulak arkasından aşağı-geriye süpürüp topuza) + serbest `ear_frame` (672 tel). Serbest groom gizliyken de kulak arkasında ana kütle var (board 05 "main only"); kulak kepçesi açık. Hacim referanstan hâlâ ince; serbest `ear_frame` gizlendiğinde kulak arkası ana kütle görünür ama daha az dolu. |
| Hangi eksikler hâlâ devam ediyor? | Kaş yerleşimi yalnız kütüphane seçimiyle (prosedürel kaş = açık iş); ana ön/şakak akışı eğik dip düzeyinde (tam çapraz örtüşme yok); topuz altı hâlâ düzenli; burun genişliği/tabanı referanstan dar (bilerek değiştirilmedi); göz açıklığı/sakin ifade geometri olarak değişmedi; aktif groom LOD indeksi Python'dan okunamıyor — `GroomComponent` yalnız HLOD/auto-LOD-generation özellikleri sunuyor, aktif LOD/`forced_lod` yok (`data/lodprobe_*.json`); iskelet mesh'lerde `forced_lod_model=1` (LOD0 zorla). Mesafe testi görsel.. |

## Teknik (board 06)

| Kontrol | Sonuç | Kayıt |
|---|---|---|
| n1 auto-rig (burun için; kaş/saç için rig çalıştırılmadı) | fit ortalama 0.017 mm; 858 morph; DNA `MHC_G11RN_N1_Head` kalıcı | `data/cycle_n1_log.txt`, `data/rig_MHC_G11RN_N1.json` |
| Rig (54 çekim, saç gizli; n1 + M_Fine) | Temiz: kırpma, bakış, kaş hareketi (M_Fine kaş groom'u bağlı), dudak kapama, gülümseme, çene/ağız, vizemler, burun deliği | `g11rnrig_*` |
| Hareket 27 + eğim 7 + ışık 10 | Temiz; kulak/boyun kesişmesi, kök kopması, topuz girişi açılması yok | `g11rnmot_*`, `g11rnP_*`, `g11rnRL_*` |
| Oyun ışığı (harness 'sky' sun+sky rigi) | **TEST EDİLMEDİ**: harness'in sky modu siyah kare üretti (pozlama/ışık rigi açılmıyor); üretim haritası/ışığı değiştirilmedi. Dengeli ön ışık ve stüdyo setleri var | `g11rnSsky_*`, `g11rnCsky_*` (siyah) |
| Groom LOD | Temiz editörde ayarlandı, yeniden açılışta tablo aynı; mesafe 1,25–25 m görsel (24 çekim); aktif LOD indeksi Python'dan okunamıyor (probe: yalnız HLOD özellikleri) | `G11RN_LOD`, `data/lodprobe_*.json` |
| Yeniden açılış | n1 (858 morph, DNA), h49a groom'ları, MI'lar, kask, 4 bağlama (`GB_G11RN_*_n1h49a`, kaş M_Fine) yüklendi; kirli paket yok | `data/reopen_check.json` |
| Kaynak/bellek | Zincir öncesi C: 18,5 GB boş; çökme yok; 1 auto-rig | — |
| Korunan dosyalar | 84/85 (yalnız iki eklenen teşhis metni) | `data/preservation_check.json` |

## Değerlendirmeler (teknik / benzerlik / gerçekçilik ayrı)

| Başlık | Sonuç |
|---|---|
| m2 ETLİLİĞİNİN KORUNMASI (yeni dolgu yok) | BAŞARILI |
| KAŞ: GÖZ ÇERÇEVESİ | KISMEN (daha dolu/düz/alçak kütüphane kaşı; yerleşim düzenlenemedi) |
| BURUN: YÜZEY GEÇİŞİ (ön / 3/4) | KISMEN |
| BURUN: SIRT–KEMER–UÇ KARAKTERİ | KISMEN (profil bilerek korundu; gerekçe yukarıda) |
| BURUN TABANI / DELİK / ÜST DUDAK KORUNUMU | BAŞARILI (0,00 mm) |
| ANA ÖN/ŞAKAK AKIŞI (ana kılavuzlarla) | KISMEN (ana kütle değişti; tam çapraz değil) |
| ENSE: YOĞUN, DOĞAL KÖKTEN TOPUZA | BAŞARILI (ana kütlede de levha/L/ip yok) |
| TOPUZ ALTI KATMANLAMA (ince teller gizli) | KISMEN |
| KULAK ARKASI GERÇEK YAPI | KISMEN |
| OYUN IŞIĞINDA GÖRÜNÜM | TEST EDİLMEDİ (sky çekimi siyah) |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (oyun ışığı ve aktif LOD indeksi TEST EDİLMEDİ) |
| REFERANSA GENEL BENZERLİK | KISMEN |
| GERÇEKÇİLİK | KISMEN |
| ESKİ KAYNAKLARIN KORUNUMU | BAŞARILI (asset düzeyinde 100%) |

## Board'lar

01 bütün baş (referans | başlangıç | aday; ön, iki 3/4, iki profil) · 02 kaş (mevcut/gizli/alternatifler, yakın + bütün yüz) · 03 burun (önce/sonra; taban/delik/üst dudak korunumu) · 04 ana saç akışı (serbest groom gizli; düzenlenen ana kılavuzlar + yoğun saç) · 05 ense–kulak arkası–topuz (arka, iki arka 3/4, iki profil; ana/ince ayrı) · 06 ayrıştırma + oyun ışığı + teknik.
