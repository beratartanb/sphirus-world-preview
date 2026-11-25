# House Architecture & Interior 2.0 — geçiş C (2026-11-25)

**Durum: IN PROGRESS.** Yapılan: bütün sıva duvarlar, daha ucuz shader, atölye için özgün modeller ve yerleşim (harita kaydı). Yapılmayan: dış mimari geometrisi, mutfak, yaşam alanı, geçişler, arka bahçe.

## 1. Bütün sıva duvarlar ve shader maliyeti
Önceki katman yalnız iç bölmelere ulaşıyordu ve pahalıydı. Yeni sürüm (`scripts/apply_house2.py`) üç gürültü düğümü ve üç örneklemeli dünya-hizalı normal yerine **tek** döşenen gürültü dokusu ve **tek** düzlemsel sıva normali kullanıyor; ayrıca zemin katın dış duvarlarını (iç yüzleri oturma odası, atölye ve mutfağın ana duvarı) boyayan iki materyale de eklendi.

| Materyal | Kaynak | Önceki katman | Yeni katman |
|---|---|---|---|
| İç bölme sıvası | 231 komut | 415 | **289** |
| Şömine/baca taşı | 231 | 344 | **311** |
| Dış duvar (sıva + meşe) | 381 | — | 438 |
| Üst dış duvar | 370 | — | 427 |

Veri: `data/house_shader_cost.txt`. İlk derleme örnekleyici türü yüzünden başarısız oldu (duvarlar dama desenine düştü); düzeltilip temiz oturumda kaydedildi.

**Aynı oturumda dönüşümlü A/B** (katmanlı / kaynak / katmanlı / kaynak, 6 bakış): ortalama 34,6 ↔ 34,7 fps, fark −0,1 fps — ölçülebilir maliyet yok (`data/perf_house_AB_same_session.txt`).

Görsel: `evidence/atolye_ve_duvarlar_sonra_KAYITLI.jpg` — oturma odası, atölye ve mutfak duvarlarında hafif ton dalgası ve mala dokusu. **Dürüstçe: etki incedir**; bu bir duvar yenilemesi değil, düzlüğün kırılmasıdır.

## 2. Maske atölyesi (yeni modeller ve yerleşim, harita kayıtlı)
Mevcut durum: tezgâhlar, maskenin dört aşaması, yonga, tokmak, pigment kapları vardı; eksik olan, maskenin nasıl yapıldığını anlatan istasyondu.
Blender'da üretilen 6 model (`scripts/gen_handmade3.py`, 364–960 üçgen, evin mevcut meşe/kil/demir/keten materyalleri): kurutma askısı, tahta üstünde kil yüz kalıbı, toprak boyalı boya tahtası, fırça kavanozu, tutkal kabı ve fırçası, yırtılmış keten şeritler. Önizleme: `evidence/atolye_yeni_parcalar_blender.jpg`.
Yerleşim (`scripts/apply_dress.py`, konumlar izlemeyle doğrulandı): batı duvarında kurutma askısı ve üstünde yapım aşamasındaki iki maske; çekmeceli dolabın üstünde kil kalıp, tutkal kabı ve keten şeritler (kaplama istasyonu); yan masada fırça kavanozu; ana tezgâhta boya tahtası. 8 aktör, klasör `LIVED/VF2C_20261125/workshop`.
Sınırlar: askı sabit kadrajlarda kısmen bitkinin ve dolabın arkasında kalıyor; boya tahtası tezgâh karesinde seçilmiyor (konumu yeniden ele alınmalı); etkileşim (maske tezgâhı, inceleme kamerası) ve çarpışma **test edilmedi** — askı tek çarpışmalı parça, duvar dibinde.

## 3. Çözülemeyen: balkon zemini
İçeriden bakınca düz beyaz görünen balkon zemini için iki materyal denemesi (tahta örneği; dünya-hizalı tahta materyali) karede hiçbir fark yaratmadı (`evidence/balkon_zemin_once_sonra.jpg`). İzlemeler görünen yüzeyin doğru aktör ve örnek olduğunu gösteriyor; neden tepki vermediğini bulamadım. Kaydedilmedi.

## 4. Yapılmayan
Dış kabuk, çatı, veranda ve temel geometrisi; iç-dış ölçü karşılaştırması; mutfak; şömine çevresi ve yaşam alanı yerleşimi; kişisel eşyalar; koridor/merdiven ergonomisi; arka bahçe.

## 5. Performans
İç mekân 15 nokta, kayıtlı durum: 31,0–42,2 fps (`data/perf_house_c_final.txt`); önceki geçişle aynı aralıkta.

## 6. Geri alma
`vf2_wh2040316` (materyaller; betikle `builtins.VF2H2_REVERT=True` + `apply_house2.py`), `vf2_wimp3031223` (proplar), `vf2_wlvl040341` (harita). Atölye aktörleri `VF2C_` önekiyle seçilip silinebilir.
