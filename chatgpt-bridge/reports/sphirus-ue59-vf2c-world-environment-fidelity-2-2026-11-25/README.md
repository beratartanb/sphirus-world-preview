# World & Environment Fidelity 2.0 — geçiş C (2026-11-25)

**Durum: IN PROGRESS — küçük.** Tek kayıtlı dünya değişikliği: ön bahçede zemin döküntüsü. Orman dağılımı, patikalar, arazi, göl, kıyı ve arka bahçe hâlâ yapılmadı.

## 1. Yapılan
Sorun: ev ile göl arasındaki güneşli zemin tek tür ot, eşit yoğunluk ve keskin toprak sınırıyla bakımlı çim gibi okunuyor; önceki geçişte yalnız renk kısılmıştı.
`scripts/apply_world.py`: çam altına ait döküntü (iğne yığınları) **kümeler halinde**, projenin mevcut foliage türleriyle, patikanın 95 cm uzağında ve yalnız arazi üzerinde. Kayıtlı sonuç: 8 küme, 20 örnek (foliage 38.474 → 38.494).
Kanıt: `evidence/dunya_once_sonra_C_KAYITLI.jpg`. **Dürüstçe: fark incedir**; ot yoğunluğu ve yama sınırı değişmedi (ot örneklerini foliage defteri dışında silmek güvenli değil, yapmadım).

## 2. Reddedilen ilk deneme
İlk sürüm alanı kıyıya kadar aldı ve ölçekleri büyük tuttu: kayık ve kıyı taşları iğne yığınına gömüldü (`evidence/ilk_deneme_kiyi_REDDEDILDI.jpg`, alt sıra). Kaydedilmedi; alan ön bahçeyle sınırlandı, kayık ve kıyı için yasak bölge eklendi, ölçek düşürüldü.

## 3. Göl
Beş ışık koşulunda göl kareleri alındı (bütünlük raporu). Bu karelerde aşırı su parlaması görmedim; gün batımında sıcak yansıma hoş, gece göl okunmuyor. Su materyali, kıyı çizgisi ve sazlara dokunulmadı.

## 4. Performans
Kayıtlı durum (`data/perf_world_c_final.txt`): göl→ev 30,1, ön 29,7, arka bahçe 29,1, kıyı 34,1, yokuş 31,1, patika 31,9, göl 34,0, doğu 36,4 fps. İlk üç nokta bu geçişin başka bir turunda 32–39 ölçülmüştü; neden ayrıştırılmadı (dış mekân için aynı oturum A/B yapılmadı). 20 örneğin bunu açıklaması beklenmez, ama kanıtım yok.

## 5. Yapılmayan
Ağaç/çalı katmanları, patika kenarları, kök-taş-kütük kompozisyonu, nemli/kuru bölgeler, arazi, göl suyu ve kıyı, sazlar, arka bahçe. AGENTS.md'nin istediği ChatGPTBridge dışa aktarımı yapılmadı.

## 6. Geri alma
`vf2_wlvl040341` harita yedeği.
