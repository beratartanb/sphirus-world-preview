# Sphirus World — Karakter gerçekçiliği, 1. geçiş (2026-11-24)

**Durum: KISMİ.** Cilt, göz, kaş ve dinlenme kol duruşu kaynağında düzeltildi, kaydedildi ve gerçek oyun ışığında önce/sonra görüntülerle doğrulandı. **Saç fiziği teslim edilmedi**: denendi, stabil çalıştı ama perçemi yüzün üstüne düşürdüğü için geri alındı. Saç tel yapısı, saç çizgisi, yüz ifadesi, ikincil gövde fiziği ve kıyafet bu geçişte değişmedi. AAA düzeyi iddia etmiyorum; kullanıcı kabulü yazılmadı.

Proje: `sphirus_UE59`, UE 5.9, oyuncu `BP_HybridA_Player`, harita `L_GR_SphirusHouse`. Kullanılan görsel beceri: `sphirus-reference-review` (reference-to-game köprüsü); hedef olarak `ref-001` (R01 karakter paftası: saç kütlesi, mat çilli cilt, rahat duruş) kullanıldı.

## 1. İlk teşhis — plastik/manken görünümün nedenleri

Gerçek oyun ışığında, yüz kamerası ve tam beden kamerasıyla alınan "önce" görüntülerinden:

| Neden | Kaynak | Kanıt |
|---|---|---|
| Cilt pürüzsüz ve mumsu: gözenek/mikro yansıma görünmüyor, boyun gölge kenarında turuncu saçılım | Malzeme: mikro normal 0.7, "Normal Flatten" 0.33, saçılım çarpanı 1.0 | `once_sonra_sun_f.jpg` sol |
| İris neon kehribar | Malzeme: iris doygunluğu 1.71 | aynı |
| Kaş gri, ince ve çizilmiş gibi; saçla ilgisiz | Kaş malzemesi: Desat 0.55, kızıllık 0.05 | aynı |
| Kollar gövdeden 12.5° açık, simetrik "A duruşu" | Duruş katmanı parametresi `PS_AbdBase` | `once_sonra_sun_b.jpg` sol |
| Saç hareketsiz kütle | Saç simülasyonu oyuncu bileşeninde kapalı, çarpışma varlığı yok | `data/audit1.txt` |
| Saçta "fırça darbesi" lekeleri, perçem tek gözü örtüyor, alın çizgisi sert | Saç varlığının kendisi (`001_Messy_Bob`) ve tel çizimi | `once_sonra_sun_f.jpg` |
| İç mekânda yüz neredeyse okunmuyor | Sahne pozlaması (bilerek dokunulmadı) | — |

## 2. Uygulanan değişiklikler (kaydedildi)

- **Cilt (yüz + gövde, aynı değerler):** mikro normal 0.7 → 1.2; Normal Flatten 0.333 → 0.1; saçılım mesafesi çarpanı 1.0 → 0.6; pürüzlülük çarpanı 1.0 → 1.06; oyuk yansıma çarpanı 0.6 → 0.45.
- **Göz (sol + sağ):** iris doygunluğu 1.714 → 1.0; iris parlaklığı 0.808 → 0.62; sahte yansıma 0.15 → 0.3 (gölgede gözde ışık kalsın diye).
- **Kaş:** Desat 0.55 → 0.25; kızıllık 0.05 → 0.22; melanin 0.65 → 0.72 (gri → sıcak kahve).
- **Dinlenme kol duruşu:** `PS_AbdBase` 12.5° → 8.5°; `PS_AbdRun` 9.5 → 13.5 (koşudaki toplam açı aynı kalsın diye).

Sahne ışığı, pozlama, renk düzeltme ve son işlem ayarlarına dokunulmadı.

## 3. Değişen varlıklar

| Varlık | Tür |
|---|---|
| `/Game/Sphirus/CharacterLab/Sph_20261108/Skin/MI_Sph8_Head_LOD1_VT` | yüz cildi malzeme örneği |
| `/Game/Sphirus/CharacterLab/Day_20261107/Skin/MI_Sph_Body_Home` | gövde cildi malzeme örneği |
| `/Game/Sphirus/CharacterLab/Sph_20261108/Built/MHC_Sph8/Face/Materials/MI_EyeL_Baked`, `MI_EyeR_Baked` | göz malzeme örnekleri |
| `/Game/Sphirus/CharacterLab/GD35_IdentityMaster_20261011/Looks/MI_GD35_BrowS_n4` | kaş malzeme örneği |
| `/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player` | yalnız iki duruş varsayılanı |

Yedekli yazma manifestleri: `ue59_m29_cr1save1_054832`, `ue59_m29_cr1save2_055710`. Satıcı varlıkları (`/Game/Grooms/001_Messy_Bob`, MetaHuman ana malzemeleri) değiştirilmedi. Betikler: `scripts/` (`cr_set.py` aday uygulayıcı, `cr_tour2.sh` çekim aracı, `w_save_cr1.py`, `c_cr1_defaults.py`).

## 4. Anatomi ve duruş

- Düzelen: kollar artık gövdeye daha yakın, eller kalça hizasında (`once_sonra_sun_b.jpg`). Kıyafete girme görmedim.
- Doğrulama: tam beden önden kamera (durağan) + ev haritasında yürüyüş/koşu/A-D kaydı; ayak kayması en kötü 1.6 cm (hareket bozulmadı).
- **Yapılmadı:** baş–boyun–omuz ilişkisi, omurga eğrisi, pelvis, ağırlık aktarımı ve doğal asimetri. Durağan duruş hâlâ simetrik ve dik. Bunlar boşta animasyonu ve yeniden hedefleme işidir; hareket sistemini etkilediği için bu geçişte dokunmadım.

## 5. Cilt ve yüz

- Doğrudan güneşte gözenek ve çil dokusu görünür oldu, mumsu parlaklık ve boyundaki turuncu taşma azaldı (`once_sonra_sun_f.jpg`).
- Şömine ışığında ve orman gölgesinde cilt doğal okunuyor (`once_sonra_hearth_f.jpg`, `once_sonra_shade_f.jpg`). Gölgede mikro doku biraz taneli; daha fazla artırmadım.
- Oyun kamerası mesafesinde kol/omuz cildi daha az tekdüze (`once_sonra_sun_g.jpg`).
- **Yapılmadı:** yüz ifadesi, göz kırpma/bakış davranışı, göz kapağı yerleşimi, dudak detayı, yüz–boyun geçişi incelemesi, doku çözünürlüğü/LOD incelemesi.
- **Dikkat:** kaş rengini daha önce bir geçişte reddetmiştin (ince kızıl kaş). Buradaki değişiklik biçime dokunmuyor, yalnız griyi sıcak kahveye çekiyor; beğenmezsen tek varlıkta üç değerle geri alınır.

## 6. Saç

- **Görsel:** saç varlığına dokunulmadı. Hacim arkadan iyi okunuyor; yakın planda tel lekeleri, tek gözü örten perçem ve sert alın çizgisi duruyor.
- **Fizik — denendi, reddedildi, geri alındı:**
  - Bileşende simülasyon açıldı (yerel simülasyon, hız aktarımı 0.3, hava direnci 0.02, bükülme sertliği 0.35–0.9, sönüm 0.03–0.2, yerçekimi −981 → −320 → −90, çarpışma için `PHYS_Face`).
  - Stabil: koşu, dur, A/D dönüşünde patlama, yatma veya boyna girme görmedim (`aday_sac_fizigi_acik_oyun_kamerasi.mp4`). Eski "koşuda tamamen yatma" hatası bu ayarlarla çıkmadı.
  - Reddetme nedeni: simülasyon açıkken perçem her ayarda (düşük yerçekimi, yüksek sertlik, çarpışmasız dahil) yüzün üstüne düşüp bir gözü kapatıyor (`aday_sac_fizigi_shade.jpg`). Yüz okunurluğu kötüleştiği için kapattım; bileşen ayarı ilk hâliyle birebir aynı (metin karşılaştırmasıyla doğrulandı).
  - Kök neden: bu saç varlığında ön tutamları biçimde tutan bir kısıt yok. Çözüm saç kılavuzlarında (ön tutamlara ayrı sertlik veya sabitleme) — parametreyle çözülmüyor.

## 7. Işık koşulları

| Koşul | Bakıldı mı | Sonuç |
|---|---|---|
| Doğrudan gün ışığı | evet | cilt ve göz belirgin iyileşti |
| Orman gölgesi (arkadan kenar ışığı) | evet | cilt doğal; saç kenar ışığı iyi; göz artık tamamen siyah değil |
| Sıcak iç ışık (şömine/mutfak tarafı) | evet | yüz okunuyor, ten sıcak ve doğal |
| Veranda (yarı gölge) | evet | iyi |
| Pencereden gün ışığı (atölye) | **hayır** | o noktada yüz kamerası masaya takıldı; çekim kullanılamadı |
| Bulutlu dış ışık, hareket halinde değişen ışık | **hayır** | haritada o koşul yok / çekilmedi |

## 8. Performans

Editörde PIE, 4 sn'lik örnekler, dört noktada önce → sonra: 44.0 → 44.0, 34.2 → 35.1, 35.8 → 36.3, 32.6 → 33.1 fps (`data/perf_before.txt`, `perf_after.txt`). Fark ölçüm gürültüsü içinde; "son" ölçüm saç fiziği açıkken alındı, yani kayıtlı durum bundan pahalı değil. Standalone ve paketlenmiş ölçüm yapılmadı.

## 9. Gerileme kontrolleri

- Ev haritasında yürüyüş → koşu → dur → A/D: ayak kayması en kötü 1.6 cm, 10 cm üstü yok.
- Kullanıcı kaydı bu çalışma boyunca değişmedi (`10201b8b41b7`).
- **Yapılamayanlar:** test haritasındaki Tur 9 hareket regresyonu ve "kaydet → editörü yeniden aç → tekrar ölç" adımı. Neden: ev alt haritası `L_GR_CurrentHouseContent` editörde kaydedilmemiş değişiklik taşıyor ve bunu ben yapmadım (04:54–05:00 arasında benim başlatmadığım dört oyun oturumu var; kayıt dosyası da o sırada değişti). Harita değiştirmek veya editörü kapatmak o değişikliği silerdi, o yüzden dokunmadım. Değerler aynı oturumda diskten geri okunarak doğrulandı.

## 10. Kalan sorunlar

Saç fiziği ve saç tel kalitesi; perçem ve alın çizgisi; durağan duruşun simetrisi ve boyun–omuz ilişkisi; yüz ifadesi ve göz davranışı; ikincil gövde hareketi (yalnız mevcut nefes katmanı var, yeni bir şey eklenmedi); kıyafetlerin sertliği ve referanstaki kıyafetle uyuşmaması; iç mekânda yüzün karanlık kalması (sahne pozlaması — senin kararın).

## 11. Kanıt

`evidence/once_sonra_*.jpg` (aynı nokta, aynı kamera, aynı ışık; sol önce, sağ kayıtlı durum), `aday_sac_fizigi_shade.jpg`, `aday_sac_fizigi_acik_oyun_kamerasi.mp4`. Yüz ve tam beden görüntüleri PIE içinde geçici bir kamerayla alındı (yalnız alan derinliği kapalı); `_g` görüntüleri gerçek oyun kamerasıdır.

## 12. Sonraki geçiş için öncelikler

1. Saç: ön tutamları sabitleyen kılavuz düzenlemesi, ardından fiziği yeniden açmak (ayarlar hazır: `scripts/set_h1.json`–`set_h3.json`).
2. Durağan duruş: hafif ağırlık aktarımı ve omuz asimetrisi olan bir boşta katmanı (hareket sistemine dokunmadan, eklemeli).
3. Yüz: göz kırpma/bakış ve dinlenme ifadesi.
4. İç mekânda yüz okunurluğu için karakter düzeyinde çözüm veya pozlama kararı.
