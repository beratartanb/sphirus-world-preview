# Sphirus World — İnsan hareketi gerçekçiliği, 2. geçiş (2026-11-24)

**Durum: KISMİ.** Bu geçişte Aşama 1 (ayak kayması), Aşama 3'ün bir kısmı (kalça–omuz–baş bütünlüğü) ve Aşama 5 (boşta duruş) uygulandı, kaydedildi, editör yeniden açılarak ölçüldü. Ağırlık/atalet (Aşama 2), kaynak klip düzeltmesi (Aşama 4), sendeleme/düşme iyileştirmesi (Aşama 6), saç fiziği, cilt/yüz, kıyafet, ışık ve kamera incelemesi **yapılmadı**. Kullanıcı kabulü yazılmadı; AAA düzeyi iddia etmiyorum.

Proje: `sphirus_UE59` (UE 5.9), oyuncu `BP_HybridA_Player`, sürücü grafiği `ABP_Sph_GASP`, görünür gövde `ABP_Sph_Body_GASP`, hareket bileşeni `AC_Sph_Motion`.

Bu raporda üç etiket kullanıyorum: **doğrulandı** (kaydedilmiş + yeniden açılmış durumda ölçüldü), **denenmedi/görsel yargı yok**, **yapılmadı**.

## 1. Teşhis ve kök nedenler

| Sorun | Kök neden | Kanıt |
|---|---|---|
| Sprint A↔D 60 Hz, 83 cm kayma | Ters komutun geldiği tek karede kapsül 1500 cm/s² ivmeyle "açılıyordu", sonraki karelerde ise fren yöneticisi çok daha yavaş bir plan uyguluyordu. Hareket eşleştirme o tek karedeki hızlı tahmine göre **yanlış ayaklı** dönüş klibini seçiyordu (`Turn_180_R_Lfoot` 0.67 sn noktasından, sol ayak zaten yerdeyken). İyi koşularda bir sonraki karede doğru klibe (`L_Rfoot` 0.50) geçiliyordu; kötü koşularda geçilmiyordu. | Faz taraması `SWs1`: 12 dönüşün 1'i 81.2 cm; ters kare tahmini dökümü |
| 135°/180° yürüyüş başlangıcı, 47.9 cm | Satıcı klibi `Walk_Reface_Start_F_R_180` ilk adımı atılmış hâlinden (0.20 sn) giriliyor; karışım ayağı ~46 cm öteye taşıyor ama temas eğrisi "yerde" diyor. Kaynak klipte dönerek başlangıç adımı yok. | `data/plans.txt`, her üç zaman adımında aynı iki temas |
| Kısa A/D dokunuşu, 22–56 cm | Aynı sınıf: dönüş ortasında ~35–100 cm/s hızla yeniden komut gelince başlangıç/dönüş klibi başka bir ayak konumundan giriliyor. | `SWt1`, `SWt2` taramaları |
| 1. geçişteki kalça düzeltmesinde kararsızlık | Düzeltme açı farkını sarmadan hesaplıyordu; 180° dönüşlerde ortalama ile anlık değer arasındaki fark ±12°'lik sıçrama üretiyordu. | Sprint A/D'de kalça dönme kare-kare sıçraması p99: katman kapalı 7.5°, 1. geçiş 33.7° |
| Koşuda baş dönmesinin artması | 1. geçişte gövdeye verilen ters dönme omuzla birlikte başı da çeviriyordu (koşuda baş sapması 2.4° → 9.6°). | `an_head2.py` |
| Boşta "manken" duruş | Hiçbir ağırlık aktarımı yoktu; tek boşta klibi simetrik. | 1. karakter raporu |

## 2. Ayak kayması düzeltmeleri ve regresyon

**Sprint A↔D — kaynağında düzeltildi (doğrulandı).** `AC_Sph_Motion.RcOpen` 1500 → 150: ters komut karesindeki tahmin artık sonraki karelerle tutarlı; tek ve doğru giriş (0.50) seçiliyor. Yeniden açılan durumda sprint dönüşlerini içeren tüm planlar:

| Plan | 60 Hz | 30 Hz | değişken |
|---|---|---|---|
| AD_sprint | 1.6 cm | 3.6 | 1.9 |
| SWs1 (faz taraması) | 1.6 | 1.3 | 1.7 |
| SWs2, SWs3 | 1.6, 1.6 | — | — |
| WAWD_sprint | 1.2 | — | — |

(yerde ölçülen en kötü kayma; eğri okuması da en çok 6.5 cm, WAWD_sprint'te havadaki ayakta 10.1). Kayıt öncesi 30 koşuluk ek tarama da 0 hata verdi.

**Dönerek yürüyüş başlangıcı ve kısa dokunuş — kaynağında ÇÖZÜLMEDİ, yalnız hafifletildi.** Ayak "yerde" sayılırken yatay olarak 70 cm/s'den hızlı hareket ediyorsa görünür ayak en çok 6 cm kaldırılıyor; yani sürüklenme alçak bir adıma çevriliyor. Sonuç:

- Yerde ölçülen kayma: 0.9–1.6 cm (başlangıç), 2.4 cm (dokunuş).
- **Ama ayak hâlâ aynı yolu alıyor:** eğri okumasıyla 47.1 / 47.2 / 44.9 cm (60/30/değişken), `SWt2` 56.3 cm (60 Hz), 36.7 cm (değişken). Bu bir maskeleme riskidir ve öyle değerlendirilmeli; gerçek çözüm o başlangıç için doğru ilk adımı olan bir klip.
- Tam beden yan kamerada önce/sonra kareleri arasında farkı gözle ayırt edemedim (`evidence/*starts_walk_side_9_85.jpg`).

**10 cm üstü tüm okumalar (yeniden açılmış durum, 49 kayıt + eski 24'lük set):**

| Kayıt | Eğri | Yerde | Ne |
|---|---|---|---|
| starts_turn_walk 60/30/var | 43–47 (×2) | 0.9–1.6 | yukarıdaki başlangıç adımı |
| SWt2 60 | 56.3 | 2.4 | dokunuşta yeniden komut |
| SWt2 var | 36.7 | 1.5 | aynı, `Run_Start_F_Lfoot` |
| planC1 var (eski set) | 33.8 | 0.2 | yürüyüş→sprint geçişi, ayak %78 havada |
| planT1 60 (eski set) | 32.9 | 0.7 | dönerek koşu başlangıcı |
| planR1 60 (eski set) | 25.6 | **6.0** | A↔D koşu sonrası başlangıç |
| SWr1 30 | 23.6, 14.0 | 1.3, 2.0 | koşu dönüşü, ayak havada |
| brake_re 30 | 21.7 | **9.8** | geri→ileri koşu pivotu (`CM_af_Loco_Jog_Fwd_Pivot`); en kötü gerçek yer kayması |
| SWt1 60 | 11.4–15.4 (×4) | 0.5–1.1 | ayak %50–77 havada, 14–16 cm kalkmış |
| AD_taps 60 / 30 | 13.7, 14.5 / 13.7 | 0.3–1.4 | aynı |
| old_K1, brake_re, planQt, planDm, planK1 | 10.5–13.1 | 0.0 | geri duruşta ayak %100 havada (temas eğrisi erken) |

Yerde ölçülen kayma hiçbir kayıtta 10 cm'yi geçmedi; en kötü 9.8 cm (30 Hz, tek örnek). Eğri okuması 10 cm'yi 20'den fazla temasta geçiyor. Bu yüzden **"ayak kayması bitti" demiyorum**: sprint sınıfı bitti, dönerek başlangıç/dokunuş sınıfı hafifletildi, 30 Hz geri→ileri pivotu açık.

Regresyon: önceki tur finalinde 23.5 cm veren `AD_taps_60` şimdi yerde 3.6 cm. Sürekli yürüyüş/koşu/sprint ve geçiş zinciri: en kötü 1.4–2.4 cm.

## 3. Yapılan değişiklikler (tam liste)

- `AC_Sph_Motion`: `RcOpen` 1500 → 150.
- `BP_HybridA_Player.GR_Foot`: yer değiştirme adımı (`SL_On 1`, `SL_V0 70`, `SL_K 0.06`, `SL_Max 6`).
- `BP_HybridA_Player.GR_Bob` (kalça katmanı): açı sarması; dönüş kapısı (ortalama sıçrayınca düzeltme sıfıra iner, 2.5/sn ile döner); düzeltme hızı sınırı `HIP_Rate 150°/sn`; kazançlar `HIP_GY 22`, `HIP_GO 14`, `SH_G 34`.
- `BP_HybridA_Player.GR_Posture`: omuz ters dönmesi kadar baş hedefi geri çevriliyor (`HD_B 1`).
- `GR_Bob`: boşta ağırlık aktarımı (`ID_*`), ayrıntı bölüm 6.
- `ABP_Sph_GASP`: iki yeni değişken ve düğüm (`SphNeckRot`, `SphSpineTr`). **İkisi de etkisiz bırakıldı** (`HD_K 0`, `HD_T 0`): boyun ters dönmesi baş yatmasını ikiye katladı (7.0° → 14.5°), omurga ötelemesi görünür gövdeye hiç yansımadı. Grafikte duruyorlar ama sıfır değerle çalışıyorlar.

Hepsi parametreyle kapatılabilir (`SL_On 0`, `ID_On 0`, `HD_B 0`, `RcOpen 1500`) veya yedekten geri alınabilir.

## 4. Ağırlık, momentum, hızlanma, yavaşlama

**Değiştirilmedi — yalnız ölçüldü.** Başlangıç ve duruşlar kliplere bağlı; keyfî gecikme eklemek istemedim, kliplere dokunmak ise Aşama 4 işi.

| Olay | Ölçüm |
|---|---|
| Yürüyüş başlangıcı | hızın %90'ı 0.32 sn, tepe ivme 645 cm/s² |
| Dönerek yürüyüş başlangıcı | %90'ı **0.15–0.18 sn**, tepe ivme 1229–1400 — fazla ani, ağırlıksız |
| Koşu başlangıcı | %90'ı 0.57–0.62 sn (dönerek 0.42–0.45) |
| Yürüyüş duruşu | 0.40 sn / 37 cm (dönüş sonrası 0.60 sn / 63 cm) |
| Koşu duruşu | 0.53 sn / 100 cm |
| Sprint duruşu | 0.60 sn / 134 cm |
| Yürüyüş→koşu / koşu→yürüyüş | 0.37 / 0.78 sn |
| Yürüyüş→sprint / sprint→yürüyüş | 0.75 / 1.18 sn |
| 90° koşu dönüşü | hız %72'ye düşüyor, 0.52 sn'de toparlıyor |

En zayıf nokta dönerek başlangıç (0.15 sn'de tam hız). Sprint 180° dönüşünde ayrıca aşağıda yazdığım "havada dönüş" var.

## 5. Pelvis, gövde, omuz, boyun, baş

Yeniden açılmış durumda, 60 Hz (30 Hz aynı; `data/hip.txt`):

| | Kalça eğilme | Kalça dönme | Omuz dönme | Baş sapma | Baş yatma | Baş yanal |
|---|---|---|---|---|---|---|
| Yürüyüş 180 | 8.9° | 9.7° | 16.3° | 2.1° | 2.7° | 4.7 cm |
| Koşu 415 | 8.8° | 9.3° | 29.0° | 2.1° | 7.5° | 6.9 cm |
| Sprint 569 | 10.9° | 17.4° | 27.9° | 3.1° | 7.6° | 5.3 cm |

- 1. geçişin kazanımları korundu (koşu omuz 44° → 29°, sprint kalça 17.4°).
- **Düzelen:** baş sapması koşuda 9.6° → 2.1°, sprintte 8.1° → 3.1°.
- **Düzelen:** kalça düzeltmesinin dönüşlerdeki sıçraması (60 Hz sprint A/D, p99): 33.7° → 7.5° (katman kapalıyken 7.5°), eğilme 5.6° → 3.3°. 30 Hz ve değişken kayıtlarda bu yüzdelik 180° kapsül dönüş karelerini içerdiği için karşılaştırılabilir değil.
- **DÜZELMEDİ:** koşuda yanal baş hareketi. Sürücüde 8.2 cm, görünür gövdede 5.8 cm (1. geçiş öncesi 6.9 / 5.0; 1. geçiş sonrası 8.3 / 5.9). İstenen gerileme düzeltmesi yapılamadı; denediğim iki yol (boyun, omurga ötelemesi) işe yaramadı.
- Koşu ve sprintte baş yatması 7.5° hâlâ yüksek (klipten geliyor).
- Kol salınımı, omuz gevşekliği, göğüs kafesi hareketi: dokunulmadı.

## 6. Boşta duruş

1.2 sn hareketsizlikten sonra pelvis ~3 cm bir yana kayıyor ve hafifçe çöküyor, kalça hattı 3–6° eğiliyor, omuz ters yönde dengeliyor; ~14 sn'de bir taraf değişiyor. Ayaklar sabit kalıyor. Mevcut boşta klibinin üstüne eklemeli; ayrı bir duruş denetleyicisi yok.

Görsel: `evidence/mr2V_idle_front2_1_0.jpg` (simetrik) ve `_8_0.jpg` (yerleşmiş). İki kareye baktım; fark hafif ama okunuyor, bir diz gevşek duruyor. Taraf değişimi anını ve döngü hissini videoda sürekli izleyerek değerlendirmedim. Baş/bakış hareketi, kol asimetrisi ve nefes değişikliği eklenmedi.

## 7. Kaynak animasyon değerlendirmesi

**Yapılmadı.** Kaynak / yeniden hedeflenmiş / grafik çıkışı / son poz karşılaştırması sistematik olarak yapılmadı ve hiçbir klip değiştirilmedi. Bu geçişte kaynağa işaret eden bulgular:

- `Walk_Reface_Start_F_*_180` ve `Run_Reface_Start_*`: dönerek başlangıçta ilk adım yok / yanlış fazdan giriliyor (bölüm 2).
- `M_Relaxed_Run_Stop_B_Rfoot`: temas eğrisi ayak havadayken "yerde" diyor (5 kayıtta).
- `M_Relaxed_Sprint_Loop_F`: gövde dik, kollar alçak; sprint gibi değil hızlı koşu gibi okunuyor (`evidence/mr2V_gait_chain_front34_25_6.jpg`).
- Sprint 180° dönüş klipleri: aşağıdaki havada dönüş.

## 8. Sendeleme, düşme, kalkma

**Değiştirilmedi.** Çalışan düşme/kalkma korundu ve yeniden ölçüldü: 60 ve 30 Hz'de düşme → yatma → kalkma → normal zinciri tamam (5.0 sn), eller yerde 2.2–6.5 cm, engele girme en çok 3.6 cm (30 Hz, 2 kare). Destek ayağına göre sendeleme, yan/arka düşme, yön değiştirirken denge kaybı: denenmedi.

## 9. Saç fiziği ve görsel gerçekçilik

**Hiçbiri yapılmadı.** Saç fiziği kapalı (1. karakter geçişinde perçem yüzü kapattığı için reddedilen ayarları yeniden açmadım; proje sahipli saç kopyası ve ön tutam sabitlemesi yapılmadı). Cilt, yüz, göz, kıyafet ve ışık bu geçişte değişmedi ve incelenmedi. Karelerde gördüğüm: üst kıyafet sert bir kabuk gibi duruyor, koşuda hareket etmiyor; saç tek kütle.

## 10. Değişen varlıklar

| Varlık | Değişiklik |
|---|---|
| `/Game/Sphirus/Player/Motion/AC_Sph_Motion` | `RcOpen` varsayılanı |
| `/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player` | `GR_Foot`, `GR_Bob`, `GR_Posture` + yeni değişken varsayılanları |
| `/Game/Sphirus/Player/GASP/ABP_Sph_GASP` | iki değişken, iki düğüm (etkisiz değerle) |

Yazma manifesti `ue59_m29_mr2save1_174705`; başlangıç yedeği `Saved/UE59Work/mr2/ckpt0/` (5 varlık + SHA). Satıcı klipleri, `ABP_Sph_Body_GASP`, `BP_Sph_GASPCharacter`, haritalar ve kullanıcı kaydı değişmedi. Betikler: `scripts/`.

## 11. Önce/sonra ölçümler

| | Önce (1. geçiş sonu) | Sonra | Durum |
|---|---|---|---|
| Sprint A↔D 60 Hz (yerde, en kötü) | 83 cm | 1.6 cm | doğrulandı, faz taramalı |
| Kısa A/D dokunuşu 60 Hz (yerde) | 22.4–23.5 cm | 3.6 cm | hafifletme; eğri 14.5–56 |
| Dönerek yürüyüş başlangıcı (yerde) | 47.9 cm | 0.9–1.6 cm | hafifletme; eğri 47 |
| Koşu baş sapması | 9.6° | 2.1° | doğrulandı |
| Sprint baş sapması | 8.1° | 3.1° | doğrulandı |
| Koşu baş yanal (sürücü / görünür) | 8.3 / 5.9 cm | 8.2 / 5.8 cm | **düzelmedi** |
| Kalça düzeltmesi sıçraması (sprint A/D, p99) | 33.7° | 7.5° | doğrulandı (60 Hz) |
| Koşu omuz dönme | 29.0° | 29.0° | korundu |
| Sürekli yürüyüş/koşu kayması | 1.6 cm | 1.4–2.4 cm | korundu |

Ortalama temas kayması tüm kayıtlarda 0.5–1.3 cm (yerde), p90 0.7–2.8 cm.

## 12. Önce/sonra oyun kanıtı ve neyi gerçekten izledim

Videolar `videos/` içinde (gerçek hız, aynı girdi planı):

| Sonra | Önce (aynı kamera) |
|---|---|
| `mr2V_gait_chain_side` (yan) | `r9V_gait_chain_side` |
| `mr2V_starts_walk_side` (yan) | `r9V_starts_walk_side` |
| `mr2V_house_walk_rear`, `mr2V_house_run_rear` (ev haritası, arka) | `mr1V_walk_rear_on`, `mr1V_run_rear_on` |
| `mr2V_house_walk_game` (ev haritası, omuz kamerası) | `mr1V_walk_game_on` |
| `mr2V_AD_sprint_side`, `mr2V_gait_chain_front34` (ön-çapraz), `mr2V_idle_front2` | **öncesi yok** |

**Dürüst sınır:** videoları baştan sona oynatarak izleyemiyorum; videolardan kare çıkarıp tek tek bakıyorum. Bu geçişte ~20 kareye baktım. Bu, poz ve temas hatalarını gösterir; ritim, akıcılık, ağırlık hissi ve titreme gibi zamana bağlı şeyleri **göstermez**. Dolayısıyla hareketin görsel kabulünü vermiyorum; o yargı senin oynamana kalıyor.

Karelerde gördüklerim:

- Koşu, yan: önce ve sonra pozları neredeyse aynı (beklenen; sürekli koşu değişmedi).
- **Sprint 180° dönüşü: karakter ardışık üç karede (≥0.2 sn) iki ayağı yerden belirgin yüksekte, havada dönüyor** (`evidence/mr2V_AD_sprint_side_5_3/5_4/5_5.jpg`). Kayma ölçümü bunu yakalamıyor çünkü ayak yerde değil. Gerçekçilik açısından açık bir sorun; öncesiyle karşılaştırmadım, bu geçişte mi başladı bilmiyorum.
- Sprint, ön-çapraz: duruş dik, kollar alçak; sprint eforu okunmuyor.
- Yan kamera arkadan ışıklı (siluet), ön-çapraz kamerada güneşli taraf patlak; yüz ve cilt bu videolardan yargılanamaz.
- Ev haritası (arka ve omuz kamerası): iki kareye baktım; poz doğal, zemine gömülme veya havada kalma görmedim. Test şeridindeki kayıtlarla kıyafet farklı (ev haritasında uzun atlet).
- Ön-çapraz ve yan kamera için bütün senaryoların "önce" videosu yok; önden tam karşı kamera hiç çekilmedi.

## 13. Performans

Kayıt sırasında (video yakalama açık) gerçek kare süresi: orta 46.6 ms, p95 52.1, p99 54.3, en uzun 122.8 ms; 60 ve 30 Hz kayıtlarında aynı. **Aynı koşulda "önce" ölçümüm yok**, bu yüzden bu geçişin maliyetini sayıyla gösteremiyorum. Eklenenler kare başına birkaç skaler işlem; yeni iz sürme, yeni bileşen veya yeni fizik yok. Standalone ve paketlenmiş ölçüm yapılmadı.

## 14. Kalıcı kayıt ve yeniden açma doğrulaması

- Kayıt sonrası editör kapatılıp açıldı; değerler diskten okundu (`data/reopen_read.txt`): `RcOpen 150`, `SL_*`, `HD_B 1`, `HIP_G*`, `ID_*`, grafikteki yeni değişkenler yerinde; kirli paket yok.
- Bölüm 2, 5, 8 ve 11'deki tüm "sonra" sayıları bu yeniden açılmış durumda ölçüldü.
- Kullanıcı kaydı baştan sona aynı (`10201b8b41b7`).
- Not: üç etiket (`AD_run` 60/30, `AD_taps` 60) önceki turdan kalma eski kayıtlara denk geldiği için atlanmıştı; fark edip `F3` etiketiyle yeniden kaydettim (`data/plans_f3.txt`). `data/hipstab.txt` içindeki `AD_taps_60_F2` satırı o eski kayda aittir, dikkate alınmamalı.

## 15. Kalan sorunlar

1. Dönerek yürüyüş/koşu başlangıcı ve kısa dokunuş: ayak hâlâ 37–56 cm yer değiştiriyor (alçak adım olarak). Kaynak klip işi.
2. 30 Hz geri→ileri koşu pivotu: 9.8 cm gerçek yer kayması (tek örnek, incelenmedi).
3. Sprint 180° dönüşünde havada dönüş.
4. Koşuda yanal baş hareketi (5.8 cm görünür) ve baş yatması (7.5°).
5. Dönerek başlangıç 0.15 sn'de tam hız: ağırlık yok. Ağırlık/atalet aşamasının tamamı.
6. Kaynak klip karşılaştırması ve düzeltmesi (Aşama 4).
7. Sendeleme/düşme çeşitliliği (Aşama 6).
8. Saç fiziği, cilt/yüz, kıyafet, ışık, kamera (Aşama 7 ve kamera bölümü) — hiç başlanmadı.
9. Performans karşılaştırması; standalone/paket; gamepad/analog girdi — denenmedi.
10. Önceki turdan açık karar: koşu→yürüyüş inişi 0.78 sn kalsın mı, kısalsın mı.
