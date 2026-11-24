# Sphirus World — House Architecture & Interior 2.0, devam geçişi (2026-11-25)

**Durum: KISMİ.** Evde iki gerçek, kayıtlı yüzey iyileştirmesi yapıldı (şömine isi/külü, iç bölme sıvası). Dış mimari, mutfak, yaşam alanı düzeni, atölye, geçiş alanları ve arka bahçede **değişiklik yok**. Harita dosyaları kaydedilmedi; etkileşim ve görev akışı varlıklarına dokunulmadı.

## 1. Önceki durum (bu geçişte ölçülen)
- Harita: 1.483 aktör (kalıcı harita 857, ev içeriği 618), ev mimarisi 199 parça, mobilya 198, önceki "yaşanmışlık" geçişinden 197 obje ve 39 decal, 16 gölgeli nokta ışığı. Ev boş bir prototip değil; eksik olan yüzeylerin "kullanılmış" okunması.
- İç bölme duvarları `MI_R3_Surface_lime`: normal gücü 0, pürüzlülük haritası yok, tek ton → gerçekten düz yüzey (28 duvar/tavan parçası).
- Zemin kat dış duvarlarının **iç yüzü** ayrı bir materyal kullanıyor (`MI_EX_Integration_OuterLimeOak`, dış cepheyle ortak).
- Şömine (`Furniture_R3_StoneFireplace`) ve baca taşları tertemiz; is yalnız tavanda bir decal olarak vardı.
- Oynanış ateşi mevcut (`GR_Day_Fire*`), dokunulmadı.

## 2. Yapılan gerçek değişiklikler
Yöntem: proje materyali `M_HouseSurface`'in **kopyası** alındı ve çıkışların önüne tek bir ek aşama bağlandı; böylece mevcut renk/doku birebir korunuyor. İlgili üç materyal örneği yalnızca yeni üst materyale bağlandı (`scripts/apply_house.py`).

### 2.1 Şömine — `M_Sph_HearthStone_VF2`
- Dünya konumuna bağlı iki elipsoit maske: lento/şömine rafının altı ve ocak içi; gürültüyle kırılmış, is rengi (0.035, 0.031, 0.028), pürüzlülük 0,93'e çekiliyor.
- Yukarı bakan yüzeylerde ocak taşı üstünde kül (0.33, 0.32, 0.31).
- Hem şömine gövdesine (`MI_R3_hearth_OriginalAtlas`) hem baca/ocak arka duvarına (`MI_R3_Surface_masonry`) uygulandı. Merkez, yarıçap, miktar ve renkler örnek parametresi.
- Kanıt: `evidence/somine_once_tam.jpg` → `somine_sonra_tam.jpg` (aynı nokta, aynı oyun kamerası): ocak arka duvarında yukarı doğru is lekesi, lento taşında koyulaşma. Yakın karede (`ev_once_sonra_KAYITLI.jpg`, H03) karakter ocağın önünde durduğu için etki kısmen kapalı.

### 2.2 İç bölme sıvası — `M_Sph_LimePlaster_VF2`
- Düşük frekanslı dünya-uzayı ton farkı (MacroAmount 0,5), her iki kat için süpürgelik hizasında kir bandı (FloorZ1 150, FloorZ2 490; yükseklik 40 cm; miktar 0,6), dünya hizalı sıva/mala kabartması (ReliefStrength 0,55, 150 cm).
- Kanıt: `ev_once_sonra_KAYITLI.jpg` (H08 kiler duvarı). **Dürüst değerlendirme:** renk korunuyor, yakın ışıkta yüzey artık hafif dalgalı okunuyor; ama bu karelerde fark **küçük**. Kir bandını gösteren özel bir yakın kare çekmedim. Bu madde tek başına "ev iç mekânı gelişti" demek için yeterli değil.

## 3. Denenip bırakılanlar
| Deneme | Neden bırakıldı |
|---|---|
| İs/kül ve tezgâh lekeleri için decal (sahip olunan decal paketinden) | Karelerde hiç görünmedi: `M_HouseSurface` yüzeyleri decal almıyor (tezgâhta da etkisizdi). Harita değişikliği gerektirdiği için tamamen çıkarıldı; **harita kaydedilmedi** |
| Sıfırdan kurulan sıva materyali | Tonu grileştirdi; dünya-uzayı normal ayarı duvarları kararttı. Kaydedilmedi, yöntem değişti |
| Balkon zeminini tahta dokusuna çevirmek | Zemin materyali düz renk; "beyaz" görünmesinin nedeni iç mekândan bakarken dışın patlaması. Doku değişikliği karede fark yaratmadı, **geri alındı** |

## 4. Yapılmayanlar
Dış kabuk ve cephe, çatı, kapı/pencere, veranda, temel–arazi birleşimi; mutfak; yaşam alanı kompozisyonu; atölye/maske alanı (yeni prop yok); yatak odası; koridor/merdiven ergonomisi; arka bahçe; iç/dış ölçü doğrulaması; kapı ve görev etkileşim testi (materyal değişikliği etkileşimi etkilemez, yine de test etmedim).

## 5. QA ve performans
- 10 iç nokta, oyun kamerası, PIE: önce 36,5–41,8 fps, sonra 34,1–39,9 fps (`data/perf_house_final.txt`). Farklı editör oturumları; 1–2 fps'lik materyal maliyeti olası, ayrıştırılmadı.
- Yeni materyaller: sıva 104 düğüm / 415 piksel komutu; ocak 107 düğüm / 344 komut (kaynak materyalden fazlası gürültü ve maske hesabı).
- Yeniden açılışta: üç örnek yeni üst materyale bağlı, parametreler yerinde, kirli paket 0, haritada geçici aktör 0.

## 6. Değişen varlıklar ve geri alma
Yeni: `/Game/Sphirus/House/VF2_20261125/M_Sph_LimePlaster_VF2`, `M_Sph_HearthStone_VF2`. Değişen: `MI_R3_Surface_lime`, `MI_R3_hearth_OriginalAtlas`, `MI_R3_Surface_masonry` (yalnız üst materyal + yeni parametreler).
Geri alma: `builtins.VF2H_REVERT=True` ile `apply_house.py` (üç örneği `M_HouseSurface`'e döndürür) ve kayıt; ya da editör kapalıyken `vf2_whouse014557` yedeği.

## 7. Sonraki adım
Aynı katmanı dış duvarların iç yüzünü boyayan iki materyale taşımak (oturma odası ve atölyenin ana duvarları asıl orada); ardından atölye propları ve mutfak/yaşam alanı kompozisyonu, her biri kendi önce/sonra turuyla.
