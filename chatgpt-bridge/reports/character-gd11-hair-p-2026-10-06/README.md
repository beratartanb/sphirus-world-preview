# GD11 saç turu P: saçı referansa göre başa yeniden oturtma (h51a → h56a); yüz / burun / kaş kilitli

Tarih: 2026-10-06. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime geçirilmedi. Yeni uygulama, skill, MCP ve face auto-rig yok.

## Sabit paket ve yeni aday

| Parça | Varlık | Durum |
|---|---|---|
| Yüz / DNA | `SKM_G11RM_Face_m2` / `MHC_G11RM_M2_Head` | değişmedi (SHA1 `data/locked_package_hashes_after.json` = geri dönüş kaydı) |
| Kaş / kirpik | `GR_GD_Eyebrows_M_SlightArch`, `GR_GD_Eyelashes_S_Thin`, M bağlamaları (`GB_G11RM_*_m2h48a`) | değişmedi |
| Başlangıç saçı | `GD11_HeadRefinementO_20261005/Hair/GR_LK_Hair_{Main,Loose}_h51a` + `GB_G11RV_*_m2h51a` | değişmedi (h48a/h49a/h50a/h51a kaynakları da) |
| **Yeni saç h56a** | `GD11_HairP_20261006/Hair/GR_LK_Hair_{Main,Loose}_h56a` + `GB_G11RP_Hair{Main,Loose}_m2h56a` (hedef m2) | yeni, ayrı aday |

Ara adaylar h52a–h55a aynı klasörde saklandı (`SourceAssets/Characters/GD11_HairP_20261006/hair/*`). Her çekim setinin kompozisyonu editörden okundu (`prov/g11rpS.json`, `prov/g11rpF.json`); S ve F aynı editör oturumunda, aynı ışık rig'leri ve kurulumda sıfırlanan simülasyonla (time=0) çekildi.

## Sorulara doğrudan cevaplar

| Soru | Cevap |
|---|---|
| Kafayı boş gösteren ana sebep neydi? | **Yön, yoğunluk değil.** h51a'da bütün tepe/ön kilitleri köklerinden dümdüz geriye (ve yukarı) gidiyordu: yan bölgelerden geçen saçın tepe köklü payı %0, alın köşesi kaplaması %25, şakak %32–57, tepe kalınlığı 2,3 cm (`data/cover_h51a.json`). Referansta saç ortadan ayrılıp yanlara "perde" gibi iniyor, alın köşesi ve şakağı örtüp kulak üstünden alçak topuza toplanıyor. Kök yoğunluğu her bölgede yeterliydi (şakak 31–39, kulak üstü 175/cm²). |
| Hangi ana guide aileleri değişti? | 72 ana kilidin 69'u, köke göre 8 aileye ayrılarak **tam merkez çizgisi** olarak yeniden yazıldı (`tools/blender_g11rp_guides.py`, `data/p4_families.txt`): A ön kenar (9: saç çizgisi boyunca alın köşesinin üstünden şakağa alçak, kulak üstünde düz), B ön-tepe (13: ayrımdan çapraz yana, kulak arkasına daha dik, en dış katman), C şakak kenarı (7: perdelerin altında iç katman), D kulak üstü (9), E üst yan (8: kulak arkasına diyagonal), F tepe orta (3), G kulak arkası (6: yalnız stand-off hacmi), H arka/ense (14: yalnız yanal eğim + farklı topuz girişi). Tepe yanındaki 2 kilit (10, 71) bilerek orijinal düz-geri rotasında bırakıldı (tepe arkası açılmasın diye). Board 07 öncesi/sonrası. |
| Çapraz örtüşme gerçekten ana kütlede mi? | **Kısmen.** Serbest groom gizliyken (board 02) ön kenar ailesi şakak üstünde alçak, ön-tepe ailesi daha yüksekten ve daha dik gelip kulak arkasında onun üstünden geçiyor; 3/4'te ayrı yönlü iki akış okunuyor, fakat referanstaki kadar belirgin, ayrı tutam olarak değil. Yoğun telde ölçülen aile hareketi: şakak 1,2 cm ort. |
| Şakak ve kulak arkası doldu mu? | Şakak **evet**: kaplama %32–57 → %89–92, dış stand-off 0,5–0,7 → 1,5–1,8 cm, geçen saçın %82–100'ü tepe/ön köklü (`data/cover_table_h51a_h56a.md`). Kulak arkası **kısmen**: kulak üstü/arkası gerçek kütle (board 04 profiller), ama kulak memesi altındaki bölgenin kaplaması %60 civarında kaldı (orada kök yok; bu turda kök dağılımı değiştirilmedi). |
| Ense uzun saçtan topuza doğal mı? | **Kısmen.** Ense saç çizgisi yükseltilip genişletildi (`SPH_NAPE_ZC` 151,2 → 154,3; yan tablo); boyun ortasındaki dar "dil" 2 cm kısaldı ve W biçimli daha geniş bir ense oldu; serbest/sarkan tel payı %30 → %15. Uzun ense saçı topuza katılıyor (board 05 satır 3: A/B/C etiket grupları). Orta blok hâlâ referanstan daha düzenli. |
| Topuz altındaki düzenli koyu kütle azaldı mı? | **Kısmen.** Arka kilitlere yanal eğim ve farklı topuz girişleri verildi; ikincil derinlik/dalga artırıldı (`SPH_SEC_DS`, `SPH_WAVE2`). Topuz altı artık tek düz levha değil (board 06), ama hâlâ simetrik ve taranmış duruyor. Topuz yeri değişmedi. |
| Tepe büyütülmeden yan kaplama artırıldı mı? | **Evet.** Tepe dış stand-off 2,3 → 0,87 cm; yan üst 2,05 → 1,5; kulak üstü 1,6–1,9 → 2,3. Tepedeki yükseltme kaynakları kapatıldı (`SPH_FRONT_FILL` 0,6 → 0, `SPH_PC_LIFT` 0,5 → 0). Ayrım çevresinde kendi RNG'siyle 4.400 kısa örtü teli eklendi (`top_cover`; ayrım ve tepe arkası açıklığı için). |
| m2 yüz, M DNA ve M_SlightArch değişmeden kaldı mı? | **Evet.** 7 dosya SHA1 geri dönüş kaydıyla aynı; korunan eski adaylar 89/89. Editörden okunan yüz/DNA/kaş yolları `prov/*.json`. |

## Yöntem notları

- Önce tanı: `tools/blender_g11rp_cover.py` bölge başına kaplama / katman / stand-off / akış yönü / kök kaynağı ölçtü; "seyrek → density" denmedi.
- Kılavuz kimliği: h51a ile **aynı örnekleme** (kilit kümeleme ve kök dağılımı değişmedi); katman-3 kılavuzlar yalnız saklanan kök konumu eşleşince uygulandı (0 uyumsuzluk; `h56a/build_log`). Kilit telleri h53a/h54a arasında bit-bit aynıydı (ense alanı bağımsız RNG).
- Her turda Blender'da kılavuz görünümü (7 kamera) ve tel geometrisi, sonra Unreal'da aynı kameralar. 4 yoğun üretim (h52a ilk perde; h53a hacim+dalga+kulak; h54a ense çizgisi; h55a ayrım örtüsü; h56a tepe arkası + ense yüksekliği). Etkin olmayan parametre kullanılmadı; her değişiklik tel geometrisinde doğrulandı.
- Tel kontrolü: 0 anormal segment, yüz kutusundan geçen 238 tel (alın üstü perde kenarı; h51a'da 0, h50a hatasıyla karıştırılmamalı).

## Teknik (board 08, `data/tech_h56a.jpg`)

| Kontrol | Sonuç |
|---|---|
| Bağlama | iki yeni bağlama hedef m2, kaynak P yüzü; yüz rig'i çalıştırılmadı |
| Hareket 27 (bak 10–85°, dönüş L/R, koş-dur) + eğim 7 | Temiz: kökler scalp'ta, kulak/boyun kesişmesi yok, topuz açılmıyor, nötre dönüş var |
| Simülasyon koşulu | S ve F aynı oturum, kurulumda sıfırlama, time=0; uzun süre simüle olmuş kareyle karşılaştırılmadı |
| LOD | h56a için LOD'lar üretildi; mesafe/kalınlık tablosu ayarı ve aktif LOD indeksi **TEST EDİLMEDİ** |
| Korunan dosyalar | 89/89 |

## Değerlendirmeler

| Başlık | Sonuç |
|---|---|
| SAÇIN BAŞI DOĞAL KAPLAMASI | BAŞARILI (ölçülen kaplama) / görsel: KISMEN (hâlâ referanstan daha düzgün taranmış) |
| ÖN/ŞAKAK ÇAPRAZ AKIŞ | KISMEN |
| ŞAKAK DOLULUĞU | BAŞARILI |
| KULAK ÜSTÜ KAPLAMA | KISMEN (saç kulağın üstünden geçiyor; referanstaki kısmi kulak örtüsü yok) |
| KULAK ARKASI GERÇEK HACİM | KISMEN (üst/arka kütle var; meme altı bölge boş) |
| ENSEDEN TOPUZA UZUN SAÇ AKIŞI | KISMEN |
| TOPUZ ALTININ DOĞALLIĞI | KISMEN |
| TEPE HACMİNİN DENGESİ | BAŞARILI |
| SAÇ ÇİZGİSİ | KISMEN (konum değişmedi; perde kenarı temiz, bebek saçı yalnız son katman) |
| REFERANS SAÇ KARAKTERİ | KISMEN |
| YÜZ/BURUN/KAŞ KORUNUMU | BAŞARILI |
| TEKNİK ÇALIŞIRLIK | BAŞARILI (LOD mesafe ayarı TEST EDİLMEDİ) |

## Board'lar

`boards/01_REF_START_NEW.jpg` referans | h51a | h56a · `02_MAIN_FLOW.jpg` yalnız Main groom + kilit telleri · `03_TEMPLE_SIDE.jpg` şakak/yan · `04_EAR.jpg` kulak üstü/arkası iki taraf · `05_NAPE.jpg` ense + A/B/C etiket grupları · `06_BUN.jpg` topuz bağlantısı · `07_GUIDES.jpg` kılavuz öncesi/sonrası · `08_UNREAL_FINAL.jpg` final + teknik. Ham kareler `captures/g11rp*` (yayımlanmadı).

**ÜRETİME GEÇİRİLMEDİ. KULLANICI İNCELEMESİ İÇİN DUR.**
