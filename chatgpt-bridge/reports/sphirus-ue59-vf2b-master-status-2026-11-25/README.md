# Sphirus World — Visual Fidelity 2.0, devam geçişi: ANA DURUM RAPORU (2026-11-25)

**Genel durum: KISMİ.** Bu geçişte karakterde, evde ve dünyada **kalıcı, kayıtlı ve yeniden açılışta doğrulanmış** değişiklikler yapıldı; ancak Visual Fidelity 2.0 kapsamının büyük bölümü hâlâ açık. Hiçbir ana bölümü (Karakter / Ev / Çevre / Görsel Bütünlük) DONE olarak işaretlemiyorum. AAA düzeyi veya kullanıcı kabulü iddia etmiyorum; bütün kareler editör içi PIE'dir, paketlenmiş/standalone test **yapılmadı**.

Ayrıntı raporları (aynı klasör düzeyi):
`sphirus-ue59-vf2b-character-visual-fidelity-2-full-2026-11-25`, `…-character-physical-realism-2-…`, `…-house-architecture-interior-2-…`, `…-world-environment-fidelity-2-…`, `…-visual-cohesion-final-review-…`.

## 1. Bu geçişte oyunda gerçekten değişenler (kayıtlı)
| # | Alan | Değişiklik | Kanıt |
|---|---|---|---|
| 1 | Karakter — üst giysi | Blender'da yeniden oturtulmuş proje sahipli ağ (`SKM_Sph_RetroTop_VF2`): yan/arka dikiş daraltma + kumaş simülasyonuyla döküm + 1,6 mm kumaş kalınlığı. Etek ucunun bedene ortalama uzaklığı 5,4 → 2,5 cm | karakter raporu, `kiyafet_once_sonra_KAYITLI.jpg` |
| 2 | Karakter — üst kumaş | Yeni kumaş materyali (`M_Sph_Fabric_VF2`, Cloth gölgeleme, ince dokuma normali, havlu görünümlü kaba normalin yumuşatılması, soluk mavi ton) | aynı |
| 3 | Karakter — şort | Lavanta bel/paça bantları giysinin kendi zeytin ailesine alındı; proje sahipli taban materyali. **Bulunan gizli hata:** satıcı taban materyalinde `used_with_skeletal_mesh=False` idi (paketlenmiş oyunda varsayılan materyale düşme riski) — kopyada düzeltildi | aynı |
| 4 | Ev — şömine | Ocak içinde ve lento taşında is, ocak taşında kül (materyal içinde, dünya konumuna bağlı maske) | ev raporu, `somine_once_tam.jpg` / `somine_sonra_tam.jpg` |
| 5 | Ev — iç bölme sıvası | Tamamen düz olan kireç sıvaya makro ton farkı, süpürgelik hizasında kir bandı, mala kabartması (28 duvar parçası; renk korunarak) | ev raporu |
| 6 | Dünya — zemin otu | Güneşte "çim halı" gibi okunan zemin otlarının sarı-yeşil geçirgenlik/varyasyon renkleri kısıldı (10 materyal örneği) | dünya raporu |

## 2. Denenip GERİ ALINAN / reddedilen (dürüst kayıt)
| Deneme | Sonuç |
|---|---|
| Saç fiziği (aday H6; H5'in daha yumuşağı) Blueprint'e bağlandı | **Geri alındı.** Aynı oturumda üç durum karşılaştırıldı: fizik açıkken perçem yüze düşüyor ve sarsıntıdan sonra geri dönmüyor; fizik kapalı hali belirgin biçimde daha iyi. Kare hızı maliyeti yoktu (30,7 ↔ 30,8 fps), ret nedeni yalnız görünüm. `hair_variants.jpg` |
| Şömineye is/kül için decal | Çalışmadı: `M_HouseSurface` yüzeyleri decal almıyor. Yöntem materyal içi maskeye çevrildi |
| Sıva materyalinin ilk sürümü (sıfırdan kurulan graf) | Duvarları kararttı ve tonu kaydırdı; kaydedilmedi. İkinci sürüm mevcut materyalin kopyasına ek katman olarak kuruldu |
| Balkon zemini "beyaz" | Materyal değil pozlama kaynaklı çıktı (iç mekândan bakınca dış zemin patlıyor); materyal değişikliği kaydedilmedi |
| Pozlama: vurgu kontrastı 0,78 → 0,66 | PIE'de denendi, yüzde net kazanç görmedim; **kaydedilmedi** |
| Gerçek zamanlı video kaydedici (yeni araç) | Çalışır hale getiremedim (kare zamanlaması / girdi). Bu geçişte **video kanıtı yok** |
| Perçemin sağ gözü örtmesi (saç modelinin biçimi) | **ENGELLİ:** UE 5.9'da groom dışa aktarımı yok, kaynak `.abc` bu makinede değil (varlık `W:/R&D/001_MessyBob/Export/Messy_Bob.abc` yolunu kaydediyor) |

## 3. Kapsam durumu (istenen 17 başlık)
| Başlık | Durum | Not |
|---|---|---|
| Karakterin tüm vücut anatomisi | NOT STARTED | Sistematik inceleme yapılmadı; iskelet/ağırlıklara dokunulmadı |
| Yüz, gözler ve cilt | PARTIAL | Önceki cilt/göz/kaş işleri korunuyor; bu geçişte yeni iş yok. Göz kırpma/bakış/ifade **yapılmadı** |
| Saç geometrisi, Groom ve fiziği | PARTIAL | Çizim düzeltmeli kopya canlı (önceki geçiş). Fizik: test edildi, reddedildi. Perçem biçimi: ENGELLİ |
| Kıyafet geometrisi ve Cloth | PARTIAL | Üst giysi yeniden oturtuldu + kalınlık; şort ağı aynı. Oyun içi kumaş simülasyonu (Chaos Cloth) **yok** |
| Vücut deformasyonları | NOT STARTED | Ana karakterde 14 durumluk tarama yapılmadı |
| İkincil fizik | NOT STARTED | Kemer/aksesuar gecikmesi yok; saç fiziği reddedildi |
| Ev dış mimarisi | NOT STARTED | Bu geçişte değişiklik yok |
| Ev iç mekânları | PARTIAL | Sıva + şömine. Mutfak, yaşam alanı, geçişler: değişiklik yok |
| Atölye ve maskeler | NOT STARTED | Tezgâh lekesi denemesi görünür sonuç vermedi, bırakıldı |
| Küçük arka bahçe | NOT STARTED | Önceki geçişin bahçesi duruyor; yeni iş yok |
| Orman ve bitki örtüsü | PARTIAL | Yalnız zemin otu rengi. Sayım yapıldı (38.474 foliage örneği, ~140 tür/bileşen); yeniden dağıtım yok |
| Göl ve kıyı | NOT STARTED | Denetim karesi alındı; değişiklik yok |
| PBR materyaller | PARTIAL | 5 yeni proje materyali (kumaş, şort tabanı, sıva, ocak taşı) |
| Işıklandırma | NOT STARTED | Değerler okundu; kayıtlı değişiklik yok. Sabah/akşam/gece turu yapılmadı |
| Atmosfer | NOT STARTED | — |
| Genel görsel bütünlük | PARTIAL | Kıyafet paleti ve ev izleri bütünlüğe katkı; ortak 8 maddelik test yapılmadı |
| Performans ve oynanış doğrulaması | PARTIAL | Nokta başına fps ölçüldü (aşağıda); hareket regresyonu, çarpışma, etkileşim testi **yapılmadı** |

## 4. Performans (editör içi PIE, RTX 4060 Laptop 8 GB — paketlenmiş oyun değeri değildir)
- Dış mekân 8 nokta, aynı editör derlemesi: önce 31,6–41,6 fps → sonra 31,5–38,4 fps (`data/perf_world_before.txt`, `perf_world_final.txt`). Noktaların çoğu ±1 fps; ön bahçe ve arka bahçe 3 fps düşük ölçüldü. Bu ölçümler farklı editör oturumlarında alındı; oturumlar arası oynama bu büyüklükte olduğu için farkı değişikliklere bağlayamıyorum, **dışlayamıyorum da**.
- İç mekân 10 nokta: önce 36,5–41,8 → sonra 34,1–39,9 fps (`data/perf_house_final.txt`). Yeni sıva/ocak materyalleri piksel başına gürültü hesabı içeriyor (415 / 344 komut); 1–2 fps'lik maliyet olası. Aynı oturumda dönüşümlü A/B **yapılmadı**.

## 5. Güvenlik ve doğrulama
- Tek kilit sahibi (`aip`), her yazma işi manifest + doğrulanmış yedekle; oturum sonunda kilit bırakıldı.
- **Hiçbir harita kaydedilmedi** (iki `.umap` dosyasının özeti oturum boyunca aynı). Değişiklikler yalnız varlık düzeyinde.
- Kullanıcı kaydı değişmedi (`SFSaveSlot.sav` SHA-1 `10201b8b41b7`, her PIE turundan sonra denetlendi).
- Kaydet → editörü kapat → aç → diskten oku: `data/reopen_verification.txt` (kirli paket 0).
- GASP / Motion Matching, `ABP_Sph_GASP`, `AC_Sph_Motion`, hareket veritabanları, kamera, hikâye ve etkileşim varlıklarına dokunulmadı. `BP_HybridA_Player` içinde yalnız kıyafet dizileri ve `Henley` bileşeninin varsayılan ağı değişti (saç simülasyon metni önceki haline birebir döndü).
- Satıcı (vendor) varlıkları değiştirilmedi.

## 6. Değişen / yeni varlıklar
Yeni: `/Game/Sphirus/CharacterLab/VF2_20261124/Garments/` → `SKM_Sph_RetroTop_VF2`, `SKM_Sph_CuffedShorts_VF2`, `M_Sph_Fabric_VF2`, `MI_Sph_RetroTop_VF2`, `M_Sph_CuffedShorts_VF2`, `MI_Sph_CuffedShorts_VF2`; `/Game/Sphirus/House/VF2_20261125/` → `M_Sph_LimePlaster_VF2`, `M_Sph_HearthStone_VF2`.
Değişen: `BP_HybridA_Player`; `MI_R3_Surface_lime`, `MI_R3_hearth_OriginalAtlas`, `MI_R3_Surface_masonry` (yalnız üst materyal); `GroundLayer20261111/Materials/MI_GL_*` (10 örnek, renk).

## 7. Geri alma
Yazma manifestleri (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/`): `vf2_impg005103`, `vf2_fixmi005645`, `vf2_fixmi2005715`, `vf2_wirechar011507`, `vf2_whouse014557`, `vf2_wgrass020041`, `vf2_whairoff020048`. Her biri değişen dosyaların önceki halini SHA-1 ile saklıyor; editör kapalıyken yedeği yerine kopyalamak yeterli. Betikle: kıyafet için `builtins.VF2B_WIRE='revert'` + `wire_char.py`; ev için `builtins.VF2H_REVERT=True` + `apply_house.py`; ot için `R2G_GRASS={'desat':0.45,'gain':0.85}` + `apply_grass.py` (önceki geçişin değeri).

## 8. Sıradaki uygulama adımları (öneri sırası)
1. Dış duvarların iç yüzü (oturma odası, atölye): ayrı materyal kullandığı için bu geçişteki sıva katmanı oraya ulaşmadı — aynı katmanın `M_EX_Integration_ExposureLime*` kopyalarına eklenmesi.
2. Üst giysiye oyun içi ikincil hareket (etek ucuna 4–6 kemik + AnimDynamics); Chaos Cloth bu Python yüzeyiyle kurulamıyorsa bu yol.
3. Işık koşulları turu (sabah/akşam/gece) + aynı oturumda dönüşümlü performans A/B.
4. Atölye için gerçek proplar (StableGen hibrit hattı) ve mutfak/yaşam alanı kompozisyon geçişi.
5. Saç: kaynak `.abc` sağlanırsa perçemin Blender'da ayrılması; sağlanamazsa farklı bir saç varlığı kararı senin.
6. Ana karakter deformasyon taraması ve paketlenmiş oyun testi.
