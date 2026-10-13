# GD46 — Henley'nin oyun duruşunda yeniden oturtulması (omuz kalıbı / yerçekimi)

Tarih: 2026-10-13 · Durum: **PARTIAL** — oyuna uygulandı (`SKM_GD46_Henley_f5`), PIE doğrulandı; omuz düzeldi, etek arkasında küçük şort taşması kaldı · Üretim değişikliği: `BP_Player_MM` Henley bileşeni

Kullanıcı isteği: *"Kıyafet karakterin üzerine tam oturmamış gibi duruyor, özellikle omuzlarda; üstünde yerçekimine karşı sallanan bir şey gibi değil şu an."*

## 1. Teşhis

- Henley (`SKM_LK_Henley_g17e`) bir **kalıp (pattern) giysisi**: Blender'da **A-pozundaki** vücut üzerine kumaş simülasyonuyla düşürüldü (kollar 45° açık), sonra vücut ağırlıklarıyla skin edildi. Oyunda karakter kolları aşağıda duruyor; A-pozu drapesinin omuz/kol başı hacmi skinning ile olduğu gibi taşınıyor → "omuz vatkası" gibi yuvarlak, şişkin omuzlar; sırt ve gövde kumaşı şişirilmiş bir kabuk gibi vücuttan 2–4 cm ayrık duruyor, hiçbir şey sarkmıyor.
- Çevrimdışı yeniden üretim: LK vücut (sculpt paketi `br_neutral` + `LK_Neutral` deltaları) ve Henley, aynı iskeletle oyun duruşuna (kollar aşağı) çevrimdışı LBS ile pozlandığında oyundaki görüntü birebir çıkıyor (`boards/gd46_offline_s5_start_vs_settled.png`, üst sıra). Gövde açıklığı başlangıçta medyan 1.9 cm, p95 3.4 cm; omuz kapağı medyan 0.95 cm, maks 2.0 cm.

## 2. Yöntem (`tools/gd46_settle.py`, Blender 5.2 + numpy)

1. Vücut + kafa oyun pozuna LBS ile pozlanır (bileşen-uzayı kemikler); Henley kendi g17e ağırlıklarıyla aynı şekilde pozlanır (= oyundaki hal).
2. Ana kumaş (`SPH_Henley`, 6368 kaynak köşe) UV dikişlerinde kaynaklanır; kenar uzunlukları **kalıp (bağ pozu) uzunluklarına** PBD ile ön-gevşetilir (skinning germe/sıkışmalarını kaldırır).
3. **Yaka açıklığı ve manşet sınırları sabitlenir** (rib bant/manşet vücuda tutunur; sabitlenmezse gömlek omuzlardan kayıp düşüyor — s1 denemesi).
4. Blender cloth: yerçekimi + vücut çarpışması (0.35 cm boşluk), self-collision **kapalı** (1 cm'lik ağda 0.25–0.5 cm self-collision patlıyor: e3/e5), tension/compression 30 / shear 15 / bending 2.0 / air 2.5, 80 kare (40 karede yakınsıyor).
5. Sonrası: kat (fold) onarımı + kenar gevşetme + boşluk; **yer değiştirme alanı düzleştirme** (14 iterasyon; kalıp drapesinin kendi kırışık detayını korur, simülasyonun sub-cm kırışık gürültüsünü siler).
6. Pozlu delta → karışık skinning matrisinin tersiyle **bağ-pozu deltası** → yeni rest pozisyonları (LOD1/2: en yakın LOD0 köşe deltası). Çıktı: `build/s5/outfit_geometry.json.gz` (+ ağırlıklar kopyası) — mevcut UE zinciri (`ue_lk_j4_meshes.py` kopyası) ile `SKM_GD46_Henley_<tag>` üretimi için.

## 3. Aday s5 (yaklaşık idle pozu) — ölçümler

| Ölçüm | Başlangıç (oyundaki) | s5 oturmuş |
|---|---|---|
| Omuz kapağı açıklık (z 128–136, |x|>12) medyan / p95 / maks | 0.95 / 1.73 / 2.03 cm | 0.86 / 1.51 / 2.18 cm |
| Gövde açıklık (z<122) medyan / p95 | 1.90 / 3.36 cm | 1.49 / 4.13 cm (kumaş sırttan sarkıyor; ön/yan vücuda yaklaştı) |
| Üst gövde (z 122–136) ortalama düşey hareket | — | −0.69 cm (aşağı) |
| Yaka bölgesi (z>136) / kollar | — | −0.37 / −0.43 cm |
| Kenar germe p05 / p50 / p95 (kalıp = 1.0) | 0.94 / 1.00 / 1.07 | 0.92 / 0.99 / 1.05 |
| Vücuda giren köşe | 10 | 3 (≤0.1 cm) |
| Ters üçgen (ana kumaş 12 511) | 34 (koltuk altı) | 89 (hepsi koltuk altı/kol başı; görünmez bölge) |

Görsel (clay önizleme): omuzlar deltoid üzerine inen kumaş ve kol başı kıvrımları; sırt kürek kemiklerinden sarkıyor; ön V/plaket korunuyor. **Yaklaşık poz** (kollar 8° açık, 6° önde, dirsek 12°) kullanıldı; PIE'den okunacak gerçek idle pozuyla son koşu yapılacak.

## 4. UE tarafı (bekliyor)

`tools/gd46_ue_chain.sh`: `pose before` (PIE: tüm Manny kemikleri bileşen uzayında + 4 kamera ekranı) → `gd46_settle.py` gerçek pozla → `build <dir> <tag>` (`SKM_GD46_Henley_<tag>`, izole GD46 klasörü, g17e MI'ları) → `swap <tag>` (checkpoint3 + `BP_Player_MM` Henley bileşeni yeni mesh) → `pose after` (aynı 4 kamera) → kapat. **Koruma:** zincir, otomasyon runner'ı olmadan açık bir UnrealEditor (kullanıcı oturumu) görürse çalışmayı reddeder; kullanıcı editörü hiçbir zaman otomasyonla kapatılmaz.

## 5. Dürüst notlar / açık kalanlar

- Bu statik bir oturtma: giysi idle pozunda yerçekimiyle oturmuş gibi görünür, ama hareket halinde **sallanmaz**. Sallanma için Chaos Cloth gerekir; ayrı bir iş olarak önerilecek (lookdev'de kabul edilen Chaos şort `CA_CR_Shorts_m1` de oyuna taşınmadı).
- g17e'nin 17 poz düzeltici morph'u yeni rest için yeniden çözülmedi (yeni SKM'de olmayacak); idle'da etkileri sıfıra yakın, ekstrem pozlarda (çömelme, kol kaldırma) koltuk altı/yaka davranışı eski kadar iyi olmayabilir.
- Self-collision kapalı olduğundan kol-gövde teması küçük girişimler içerebilir (s5: 0.4 cm'den yakın 41 köşe); oyunda görünürlüğü PIE'de kontrol edilecek.
- Önizlemeler Blender Workbench clay; kumaş malzemesi ve oyun ışığındaki son görünüm kullanıcı kararı.

## 6. UE uygulaması (2026-10-14)

Kullanıcı: *"Editörü kapat devam et."* Kullanıcı editörü kapatıldı, otomasyon editörü açıldı.

1. **Gerçek idle pozu** PIE'den okundu (342 kemik, bileşen uzayı). Çevrimdışı LBS ile oyundaki Henley/vücut örtüşmesi: Henley p95 0.065 cm, vücut p95 0.042 cm → çevrimdışı model oyunu birebir temsil ediyor. Gerçek poz asimetrik, kollar gövdeye yakın.
2. Gerçek pozla oturtma varyantları f1–f4: 80 kare yakınsamadı (etek +2.6 cm yukarı); f4 (30 kare, air 4) en iyisi. `SKM_GD46_Henley_f4` üretildi ve oyuna kondu → PIE'de **şortun bel bandı Henley'nin alt sırtından taştı** (oturtmada şort çarpışma nesnesi yoktu).
3. Şort (g16c, aynı pozla LBS, 0.25 cm şişirilmiş) çarpışma nesnesi olarak eklendi → **f5**. f6 (0.6 cm pay) etekte bant çizgisi yarattı, geri alındı.
4. **Son durum: `SKM_GD46_Henley_f5`** oyunda. PIE: hata yok, lider Manny; oyundaki Henley ile f5 rest'in aynı pozla çevrimdışı pozlanmış hali arasında medyan 0.024 cm, p95 0.27 cm.

**Görsel (`boards/gd46_pie_before_after_f5.png`, oyuncu kamerası):** omuz tepesindeki sivri vatka çıkıntıları gitti, omuz hattı eğimli iniyor, sırt kumaşı aşağı sarkıyor. **Kusur:** etek arka-solda iki küçük şort lekesi; etek bandı biraz daha geniş/dışa açık okunuyor.

**Geri alma:** pawn için `Henley` bileşenini `SKM_LK_Henley_g17e`'ye döndürmek yeterli (tek fark bu). Not: `checkpoint3/` ilk değişim öncesi kopya değil (ikinci değişim üzerine yazdı; f4 sonrası hali tutar) — hata, betik düzeltildi (`checkpoint_swap_<tag>`). GD45 öncesi orijinaller `GD45_Promote_20261013/checkpoint/`.

**Değişen paketler:** `BP_Player_MM`, `BP_GR_Player`, `BP_PBI_Player` + yeni `SKM_GD46_Henley_f4/f5/f6` (izole GD46 klasörü). Harita dokunulmadı.
