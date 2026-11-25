# Sphirus World — Visual Fidelity 2.0, tam kapsam uygulama geçişi (C): ANA DURUM (2026-11-25)

**Genel durum: 17 başlığın hiçbiri VERIFIED değil; 9'u bu geçişte gerçek varlık değişikliği aldı, 8'i hâlâ açık.** Bu geçiş öncekinden belirgin biçimde daha geniş (yüz davranışı, hareketli deformasyon matrisi, kıyafet daraltma + ikincil hareket, bütün sıva duvarlar, atölye için 6 yeni model, harita kaydı, ışık koşulları testi, aynı oturum A/B performansı, standalone çalıştırma), ama istenen "bütün kapsam tamam" sonucuna ulaşmadı. Aşağıda neyin yapıldığı, neyin yapılmadığı ve nedenleri açıkça yazılı. AAA/kullanıcı kabulü iddia etmiyorum.

Ayrıntı: `sphirus-ue59-vf2c-character-visual-fidelity-2-full-…`, `…-character-physical-realism-2-…`, `…-house-architecture-interior-2-…`, `…-world-environment-fidelity-2-…`, `…-visual-cohesion-final-review-…` (hepsi `-2026-11-25`).

## 1. 17 başlık matrisi
| No | İş paketi | Durum | Bu geçişte yapılan | Açık kalan |
|---|---|---|---|---|
| 01 | Tüm vücut anatomisi | IN PROGRESS | Oyundan kemik ölçümü + Blender'da ağ ölçümü; insan oranlarıyla karşılaştırma. Kemik uzunlukları ağın dinlenme pozuyla birebir aynı (animasyon/retarget ölçüyü bozmuyor). Bacak, gövde, omuz yüksekliği oranları normal aralıkta | Düzeltme uygulanmadı. Bölge bölge görsel inceleme (el, ayak, köprücük, sırt) yapılmadı |
| 02 | Yüz, göz, cilt | IMPLEMENTED — UNVERIFIED | **Göz kırpma ve küçük bakış kaymaları** yüz Anim Blueprint'ine eklendi; oyunda ölçüldü (12 sn'de 5 kırpma, eğri 0→1), karelerle gösterildi | Kırpma sıklığı insan ortalamasından biraz yüksek (≈25/dk); video yok. Dudak, göz kapağı, yüz-boyun geçişi, saç çizgisi işlenmedi |
| 03 | Saç / Groom / fizik | BLOCKED (kısmen) | Yeni iş yok. Önceki sonuç geçerli: fizik reddedildi, perçem biçimi kaynak dosya olmadan düzeltilemiyor | Kök-ağırlıklı sertlik / kemik tabanlı ikincil hareket alternatifleri **denenmedi** |
| 04 | Kıyafet | IMPLEMENTED — UNVERIFIED | Üst ve şort yanlardan daraltıldı (hareket matrisinin bulgusu); etek ucu için sınırlı ikincil hareket katmanı | Kıvrım/dikiş detayı; şort oturuşu; oyun kamerasında görünür fark küçük |
| 05 | Deformasyon | IN PROGRESS | **14 hareket evresi, 42 gerçek oyun pozu** kaydedildi ve çevrimdışı deri-kumaş testiyle ölçüldü; üstte deri görünmesi −%64 | Şortta yalnız −%7 (kök neden: kol salınımı, aşağıda). Düşme/kalkma, taşıma, uzanma pozları yok. Kalça/diz esnemesi yüksek, düzeltilmedi |
| 06 | İkincil fizik | IN PROGRESS | Kıyafet etek ucu: hız gecikmesine bağlı sınırlı ofset (simülasyon değil); sürücü oyunda doğrulandı | Chaos Cloth kurulamadı (Python'da kumaş sınıfı yok; C++ modülü eklemek Blueprint-only projede ayrı karar). Saç, kemer yok |
| 07 | Ev dış mimarisi | NOT STARTED | Dış sıva materyali katmanlandı (yalnız yüzey) | Geometri, çatı, veranda, temel: iş yok |
| 08 | Ev içi | IN PROGRESS | **Bütün sıva duvarlar** (oturma odası, atölye, mutfak ana duvarları dahil) yeni katmanı aldı; iç bölme shader'ı 415 → 289 komuta indi | Mutfak, yaşam alanı kompozisyonu, geçişler: iş yok. Balkon zemini çözülemedi |
| 09 | Atölye ve maskeler | IMPLEMENTED — UNVERIFIED | Blender'da 6 yeni özgün model (kurutma askısı, kil yüz kalıbı, boya tahtası, fırça kavanozu, tutkal kabı, keten şeritler); 8 aktör amaca göre yerleştirildi, **harita kaydedildi** | Etkileşim/kamera testi yapılmadı; askı kadrajlarda kısmen kapalı; daha fazla "üretim sürüyor" izi gerekli |
| 10 | Arka bahçe | NOT STARTED | — | Tamamı |
| 11 | Orman | IN PROGRESS | Ön bahçede çim-halı görünümünü kırmak için 8 kümede 20 iğne yığını (mevcut foliage türleriyle) | Etki ince. Ağaç/çalı dağılımı, patika kenarları, arazi: iş yok |
| 12 | Göl ve kıyı | NOT STARTED | Beş ışık koşulunda göl kareleri alındı; aşırı parlama görmedim | Su materyali, kıyı, sazlar: iş yok |
| 13 | PBR materyaller | IN PROGRESS | 4 katmanlı ev materyali, 6 prop, kıyafet materyallerine hareket aşaması | Texel yoğunluğu/pürüzlülük denetimi yapılmadı |
| 14 | Işıklandırma | IN PROGRESS | **Sabah, öğle, gün batımı, gece, bulutlu** × 4 sabit bakış test edildi (yalnız PIE); iç mekân pozlama denemesi | Kayıtlı ışık değişikliği yok. Bulgular: gece dışarıda karakter kayboluyor; içeriden dışarı bakışta patlama sürüyor |
| 15 | Atmosfer | NOT STARTED | — | Tamamı |
| 16 | Görsel bütünlük | IN PROGRESS | Duvar dili iç/dış birleşti; atölye kimliği güçlendi | Ortak 8 maddelik test yapılmadı; rezonans denenmedi |
| 17 | Performans / oynanış | IN PROGRESS | Aynı oturumda dönüşümlü A/B (ev materyalleri: −0,1 fps, gürültü içinde); **standalone çalıştırıldı**, oyun kayıttan yüklendi | Paketlenmiş yapı yok; kapı/merdiven/görev rotası testi yok; ayak kayması ölçülmedi |

## 2. Dürüst bulgular (çözülmeyenler dahil)
- **Eller şortun içinden geçiyor.** Yürüyüş/koşuda bilek pelvis ekseninden 15–16 cm yana kadar yaklaşıyor; kalça yarı genişliği ~18,5 cm. Şortu daraltmak bunu çözmedi (−%7). Kök neden kol salınımının kalçaya uzaklığı — hareket sisteminin (ayrı oturum) alanı; dokunmadım, bulgu olarak iletiyorum.
- **Kalça ve diz çevresinde deri esnemesi yüksek** (sprint/çömelmede kenar uzaması p99 1,3–1,8). Düzeltici şekil eklenmedi.
- **Balkon zemini** hâlâ düz beyaz. İki materyal denemesi karede hiçbir fark yaratmadı; neden çözülmedi, hiçbir şey kaydedilmedi.
- **Zemin döküntüsünün ilk denemesi** kıyıyı ve kayığı iğne yığınına boğdu; kaydedilmeden reddedildi, alan ön bahçeyle sınırlandı.
- **Dış mekân kare hızı:** son turda göl→ev / ön / arka bahçe 30,1 / 29,7 / 29,1 fps ölçüldü (aynı noktalar bu geçişin başka bir turunda 32–39). Neden ayrıştırılmadı; 20 foliage örneği bunu açıklamaz, ama dışlayamıyorum. Dış mekân için aynı oturum A/B **yapılmadı**.
- Standalone'da ekranda motor uyarısı: "Ray tracing geometry — always resident memory exceeds 20% of the budget (136 / 400 MB)". Önceden var mıydı bilmiyorum.
- Video kanıtı yine yok; zamana bağlı her şey (kırpma, etek hareketi) eğri ölçümü ve tek karelerle belgelendi.
- StableGen/ComfyUI bu geçişte de kullanılmadı (editör sürekli açık, 8 GB VRAM; işler ölçüye dayalı ağ ve parametreli materyaldi). Blender üç gerçek üretim işinde kullanıldı.

## 3. Güvenlik ve doğrulama
Tek kilit sahibi, her yazma manifest + SHA-1 yedekli; kilit bırakıldı. Kalıcı harita `L_GR_SphirusHouse` **bir kez** yedekli kaydedildi (8 aktör + 20 foliage örneği); alt harita değişmedi. Kullanıcı kaydı her PIE ve standalone çalıştırmadan sonra aynı (`10201b8b41b7`). Temiz yeniden açılışta diskten okuma: `data/reopen_verification_c.txt` (kirli paket 0, aktör 1483 → 1491, foliage 38.474 → 38.494). `ABP_Sph_GASP`, `AC_Sph_Motion`, gövde ABP'si, veritabanları, kamera, hikâye varlıkları değişmedi. Değişen tek animasyon varlığı yüz ABP'si (`ABP_Hazel_Face`).

## 4. Değişen / yeni varlıklar
Yeni: `House/VF2_20261125/M_Sph_HL_{Plaster,Hearth,LimeOak,OuterLime}_V3`; `Props/Handmade20261112/SM_HM_{MaskDryRack,MaskForm,PaintBoard,BrushJar,GluePot,LinenStrips}`; `CharacterLab/VF2_20261124/Garments/MPC_Sph_Cloth`.
Değişen: `ABP_Hazel_Face`; `SKM_Sph_RetroTop_VF2`, `SKM_Sph_CuffedShorts_VF2`, `M_Sph_Fabric_VF2`, `M_Sph_CuffedShorts_VF2` ve iki örneği; `MI_R3_Surface_lime`, `MI_R3_hearth_OriginalAtlas`, `MI_R3_Surface_masonry`, `MI_EX_Integration_OuterLimeOak`, `MI_EX_Integration_OuterLime` (üst materyal); `L_GR_SphirusHouse.umap`.
Artık kullanılmayan (silinmedi): `M_Sph_LimePlaster_VF2`, `M_Sph_HearthStone_VF2`.

## 5. Geri alma
Manifestler: `vf2_wface025035`, `vf2_wcd030848` (yüz ABP), `vf2_wgar3030743/030804`, `vf2_wmp031215` (kıyafet), `vf2_wimp3031223` (proplar), `vf2_wh2040316` (ev materyalleri), `vf2_wlvl040341` (harita). Editör kapalıyken yedeği yerine kopyalamak yeterli. Ev materyalleri betikle: `builtins.VF2H2_REVERT=True` + `apply_house2.py`.

## 6. Yeniden başlama noktası (sıra)
1. Arka bahçe ve mutfak/yaşam alanı level art (harita yazma yolu artık kanıtlı).
2. Işık: gece dış mekân okunurluğu ve iç→dış pozlama; kaydedilecek ayar için aynı oturum A/B.
3. Dış mekân kare hızı düşüşünün aynı oturumda ayrıştırılması.
4. Kol salınımı–kalça mesafesi bulgusunun hareket çalışmasına iletilmesi; kalça/diz düzeltici şekilleri.
5. Saç için kemik tabanlı hafif ikincil hareket denemesi.
6. Göl/kıyı, orman dağılımı, dış mimari, paketlenmiş yapı.
