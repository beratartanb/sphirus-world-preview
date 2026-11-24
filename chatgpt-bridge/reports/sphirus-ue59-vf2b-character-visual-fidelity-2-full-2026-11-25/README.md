# Sphirus World — Character Visual Fidelity 2.0, devam geçişi (2026-11-25)

**Durum: KISMİ.** Bu geçişte karakterin **kıyafetleri** gerçek ağ ve materyal düzeyinde değişti ve oyuncuya kalıcı bağlandı. Anatomi, yüz ifadesi/göz davranışı ve saç biçimi **yapılmadı / engelli**. Kimlik, MetaHuman temeli, cilt/göz/kaş ayarları ve saçın çizim düzeltmesi korunuyor.

## 1. Önceki durum (denetim)
Canlı oyunda (PIE'deki piyondan okundu): üst `SKM_Sph_RetroTop` + satıcı materyali `Disco_Top`; alt `SKM_Sph_CuffedShorts` + `MI_Relaxed_Cuffed_Shorts`; saç `GR_Sph_MessyBob_VF2` (fizik kapalı). Hiçbir giyside kumaş simülasyonu yok.

| Sorun | Kaynak (ölçülerek) |
|---|---|
| Üst giysi arkadan yamuk/çan gibi | Satıcı kalıbı göğüs altından dışa açılıyor: etek ucunda bedene uzaklık ortalama 5,4 cm, en çok 9,2 cm (Blender, en yakın yüzey) |
| Üst kumaş havlu gibi, tek tip | Kaba normal haritası tek katman; kumaş gölgelemesi yok; açık, doygun mavi |
| Kenarlar kâğıt gibi | Tek katmanlı ağ: 1.176 açık kenar, kalınlık yok |
| Şortta parlak lavanta bel ve paça bantları | Materyal parametresi `COLOR2` (0.263, 0.284, 0.413) |
| (Gizli) şort paketlenmiş oyunda bozulabilir | Satıcı taban materyalinde `used_with_skeletal_mesh=False` |

## 2. Yapılan gerçek değişiklikler
### 2.1 Üst giysi ağı — Blender 5.3 (`scripts/bl_refit_top.py`)
1. Unreal'dan giysi + beden FBX dışa aktarımı (varlık değişmeden).
2. Yan/arka dikiş daraltma: z < 1,30 m bölgesinde her köşe en yakın beden noktasına doğru çekildi (arka %50, ön %15'e kadar; en az 1,4 cm boşluk korunarak).
3. Kumaş simülasyonu (45 kare; göğüs/yaka sabit, etek serbest; beden çarpışmalı) ile yerçekimi dökümü; ardından hafif gevşetme ve bedene girme onarımı (217 köşe, en az 5 mm).
4. İçe doğru 1,6 mm kalınlık (kenarlar artık kapalı). Deri ağırlıkları korunur.

| Bant (z, m) | Önce ort./en çok (cm) | Sonra |
|---|---|---|
| 1,20 | 4,1 / 8,6 | 3,6 / 7,9 |
| 1,15 | 4,8 / 9,2 | 3,9 / 8,3 |
| 1,10 | 4,9 / 6,9 | 2,6 / 4,0 |
| 1,05 (etek ucu) | 5,4 / 6,2 | 2,5 / 3,1 |

Bedene giren köşe: 0. Köşe sayısı 6.876 → 13.752 (Unreal'da 14.618). Kanıt: `evidence/blender_top_before_*.png`, `blender_top_after_*.png`.
İlk denemede simülasyon göğüs üstünü buruşturdu; iğneleme sınırı aşağı alınarak (1,21 m) ön yüz satıcı halinde bırakıldı.

### 2.2 Materyaller
- `M_Sph_Fabric_VF2` (yeni): Cloth gölgeleme modeli, satıcı dokuları, kaba normal %45 düzleştirildi, üstüne ince dokuma normali (36×), pürüzlülük tabanı 0,72, hafif tüy rengi, ton ve doygunluk parametreleri. Örnek `MI_Sph_RetroTop_VF2`: ton (0.60, 0.67, 0.72), doygunluk −%25.
- `M_Sph_CuffedShorts_VF2` (satıcı taban materyalinin proje kopyası, iskelet ağı kullanım bayrağı diskte açık) + `MI_Sph_CuffedShorts_VF2`: bantlar (0.070, 0.078, 0.058) koyu zeytin, pürüzlülük 0,88, leke 0,16.
- İlk şort örneği dama desenli varsayılan materyalle çıktı (kullanım bayrağı); bu hata bulunup kopyada giderildi.

### 2.3 Oyuncuya bağlama
`BP_HybridA_Player`: `GR_OutfitTop` ve `GR_OutfitLow` dizilerinde eski ağlar yenileriyle değişti, `Henley` bileşeninin varsayılan ağı güncellendi. Başka değişken, grafik, hareket katmanı değişmedi. Yedek: manifest `vf2_wirechar011507`.

## 3. Önce/sonra — kayıtlı durum, aynı nokta ve kamera
`evidence/kiyafet_once_sonra_KAYITLI.jpg` (üst sıra: satıcı ağ/materyal; alt sıra: temiz yeniden açılıştan sonraki kayıtlı oyun). Gördüğüm: arkadan etek ucu bedene oturuyor, yamuk silüet azalmış; kumaş havludan dokumaya yaklaşmış; şort bantları artık giysinin parçası gibi okunuyor. **Sınırlar:** ön görünümde fark küçük (ön yüz bilinçli olarak korundu); kumaş hareket etmiyor (simülasyon yok); kıvrım hiyerarşisi hâlâ zayıf; koşu/eğilme pozlarında deformasyon **denetlenmedi** — yalnız durağan A-pozu ölçümü ve durağan oyun kareleri var.

## 4. Saç ve yüz
- `evidence/yuz_son_durum_KAYITLI.jpg`: son kayıtlı durumda üç ışıkta yüz. Saç taranmış biçimde, iki göz de bu açıdan görünür.
- Saç fiziği: denendi ve geri alındı (ayrıntı: fiziksel gerçekçilik raporu).
- Perçemin 3/4 açıdan sağ gözü örtmesi: **ENGELLİ.** `scripts/probe_groom.py`: bu motor sürümünde groom için Alembic/USD dışa aktarımı yok (üç biçim de başarısız), Python'da tel verisine erişim yok; kaynak dosya yolu `W:/R&D/001_MessyBob/Export/Messy_Bob.abc` bu makinede değil. Kaynak dosya gelirse Blender'da ön tutam ayrılabilir.
- Karanlık üst kat odasında saçta benekli parlamalar hâlâ görülüyor (ev raporu sayfasındaki yatak odası karesi) — **açık kusur**.
- Göz kırpma, bakış, dinlenme ifadesi, dudak/göz kapağı incelemesi: **yapılmadı.**

## 5. Anatomi (YAPILMADI)
Baş/beden oranı, boyun, omuz, köprücük, pelvis, el/ayak incelemesi ve düzeltmesi yapılmadı. İskelet, ağırlıklar, `GR_Posture`/`GR_Bob`/`GR_Foot` katmanlarına dokunulmadı. Tek ilgili veri: dışa aktarılan beden ağında kıyafet altı yüzeyler maskeli/kesik; giysi ölçümleri bu ağa göre yapıldı.

## 6. QA
| Denetim | Sonuç |
|---|---|
| Yeni ağ iskeleti | `metahuman_base_skel`, ağırlıksız köşe 0 |
| Sınır kutusu (yeni/eski, cm) | merkez (0.1, 3.3, 127.3) / (0.1, 2.6, 127.6) — ölçek/eksen doğru |
| Bedene giren köşe (A-pozu) | 0 |
| Yeniden açılışta okuma | `data/reopen_verification.txt` |
| Hareket regresyonu, ayak kayması | **ölçülmedi** (kıyafet ataması hareketi etkilemez; yine de ölçmedim) |
| Performans | Köşe sayısı +7,7 bin (üst); ayrı ölçüm yok, dünya turu ana raporda |

## 7. Değişen varlıklar ve geri alma
Yeni: `/Game/Sphirus/CharacterLab/VF2_20261124/Garments/` altında 6 varlık. Değişen: `BP_HybridA_Player`. Satıcı kıyafet ve materyalleri değişmedi.
Geri alma: `builtins.VF2B_WIRE='revert'` ile `scripts/wire_char.py` (dizileri ve bileşeni eski ağlara çevirir) veya editör kapalıyken `vf2_wirechar011507` yedeği.

## 8. Kalan eksikler
Oyun içi kumaş hareketi; kıvrım/dikiş detayı; şort ağının oturuşu; hareketli pozlarda giysi–beden taraması; anatomi; yüz davranışı; perçem; karanlık iç mekânda saç benekleri; standalone test; senin görsel kabulün.
