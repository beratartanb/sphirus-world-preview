# SPHIRUS — Tam beden biyomekaniği, 2. tur (2026-11-15)

Kapsam: kadın yürüyüşü (duruş genişliği, pelvis salınımı, kol asimetrisi), kadın kaynak karşılaştırması, eğimli zemin,
fiziksel tepkiler, görünüm (cilt, kıyafet, saç, ışık, kamera ilişkisi). Aktif oyuncu: BP_HybridA_Player.

**Bu turun sonunda üretimde kalıcı değişiklik yok.** Tek yazma (duruş daraltma) ölçümde zararlı çıktı ve geri alındı;
retarget varlığı 1. tur sonundaki haliyle bayt bayt aynı (SHA1 98c21e995aff…). Kullanıcı görsel kabulü alınmadı.

## Durum özeti

| Konu | Durum | Sonuç |
|---|---|---|
| Duruş genişliği (retarget yan kaydırma) | TECH_TESTED → GERİ ALINDI | Yürüyüşte 14,6 → 13,0 cm; ayak kayması 3,6 → 9,7 cm, diz 170 → 167°. Zarar > kazanç. |
| Kol asimetrisi | TECH_TESTED (teşhis) | Kaynak klipte: sol 46 / sağ 30 cm. Oyunda 45,5 / 27,4. Düzeltme yapılmadı. |
| Pelvis salınımı | TECH_TESTED (teşhis) | Kaynak oyuncu tarzı (9,7 cm zıplama, 10,7 cm yanal). Düzeltme yapılmadı. |
| Kadın kaynak karşılaştırması | TECH_TESTED (yalnız ölçüm) | Core Motion kadın klipleri ölçüldü; hiçbir şey açılmadı. |
| Eğimli zemin | TECH_TESTED (gerçek harita) | Ayak zemine uyuyor; pelvis 10–14 cm alçalıyor, diz daha bükük. Sahibi doğrulanmadı. |
| Fiziksel tepkiler | TECH_TESTED (denetim) | Yeni tepki eklenmedi: ölçüm bir eksik göstermedi (aşağıda). |
| Saç fiziği | VISUALLY_INSPECTED (aday) | Açılınca çalışıyor ama koşuda saç tamamen geriye yatıyor. Üretime alınmadı. |
| Cilt baş–gövde | VISUALLY_INSPECTED | Aynı ana malzeme; üç ışıkta boyunda çizgi görülmedi. |
| Kıyafet | VISUALLY_INSPECTED | Dört parça düz kaplamalı, kumaş simülasyonu yok; durağan pozda delinme görülmedi. Hareket içinde bakılmadı. |
| Işık | VISUALLY_INSPECTED | İç mekânda pencere güneşi kolda beyaza patlıyor. Düzeltilmedi. |
| Performans | NOT_TESTED (bu tur) | Kalıcı değişiklik olmadığı için 1. tur ölçümü geçerli. |
| Kullanıcı kabulü | YOK | — |

## 1. Kadın yürüyüşü

### Duruş genişliği
Görünen beden ile sürücü iskeletin ayak aralığı aynı: ayakta 30 cm (kalça eklemleri arası 14,6 cm), yürüyüşte 14,6, koşuda
11–12 cm. Yani genişlik kaynak klipten geliyor.

Deneme: retarget varlığına bacak hedefleri için yalnız yana kaydırma (−3,5 cm) yapan işlem eklendi.

| Ölçü | Önce (B_full_C) | İşlemle (B_hairb_D) | Geri alındıktan sonra (B_full_G) |
|---|---|---|---|
| Ayakta ayak aralığı | 30,1 | 24,6 | 29,9 |
| Yürüyüş başlangıcı ayak aralığı | 14,6 | 13,0 | 14,6 |
| Yürüyüş döngüsü ayak kayması (ort. / p90) | 3,6 / 6,0 | 9,7 / 17,5 | 3,9 / 6,0 |
| Yürüyüş başlangıcı ayak kayması | 5,5 | 13,9 | 5,4 |
| Yürüyüş diz en açık | 170° | 167° | — |
| Koşu diz en açık | 160° | 151° | — |

Karar: geri alındı. Ayakta duruş iyileşiyordu, ama yürüyüşte kazanç 1,6 cm, bedeli ayak kaymasının yaklaşık üç katına
çıkması. İşlemli halde depar, eğilme, geri yürüme ve zıplama hiç ölçülmedi.

### Kol asimetrisi
12 saniyelik düz yürüyüşte (B_long_G, birkaç tam döngü): sol el 45,5 cm, sağ el 27,4 cm ileri–geri salınım. Aynı fark
kaynak klibin kendisinde var (M_Relaxed_Walk_Loop_F: 46,0 / 29,7); nötr klipte kollar dengeli (38,1 / 41,5). Retarget ya
da duruş katmanı üretmiyor. Düzeltme yapılmadı: klibe dokunmak ya da kola sabit açı eklemek gerekir.

### Pelvis salınımı
Yürüyüşte dikey 10,3 cm, yanal 11,3 cm, kalça çizgisi dönüşü 19°. Core Motion kadın yürüyüşü daha uzun adımla (88 cm)
5,6 cm zıplıyor; demek ki 10 cm adım geometrisinin zorunlu sonucu değil, kaynak oyuncunun tarzı. (1. turdaki "geometriye
bağlı" açıklaması bu ölçümle düzeltilmiştir.)

## 2. Kadın kaynak karşılaştırması (yalnız ölçüm)

Sürücü iskelet üzerinde klip düzeyinde ölçüm; hiçbir klip oyuna bağlanmadı, reddedilen Core Motion profili açılmadı.

| Klip | Hız | Adım | Ayak aralığı (ort./en dar) | Pelvis zıplama | Yanal salınım | El salınımı S / Sğ |
|---|---|---|---|---|---|---|
| Mevcut yürüyüş (Relaxed) | 165 | 84,6 | 12,5 / 8,3 | 9,7 | 10,7 | 46,0 / 29,7 |
| Nötr yürüyüş | 200 | 100,0 | 14,8 / 10,7 | 10,7 | 6,8 | 38,1 / 41,5 |
| Core Motion kadın yürüyüş | 186 | 88,2 | 5,3 / 1,5 | 5,6 | 3,9 | 61,7 / 72,0 |
| Mevcut koşu (Relaxed) | 375 | 135,9 | 11,6 / 5,4 | 11,5 | 5,0 | 38,8 / 37,5 |
| Core Motion kadın hafif koşu | 278 | 104,1 | 7,9 / 5,1 | 10,1 | 2,2 | 43,0 / 39,0 |
| Mevcut ayakta duruş | — | — | 30,2 | — | — | — |
| Core Motion kadın ayakta duruş | — | — | 23,0 | — | — | — |

Okuma: Core Motion yürüyüşü daha dar, daha az zıplayan ve yanal salınımı az; ama ayaklar neredeyse tek çizgide (en dar
1,5 cm) ve kol salınımı 62–72 cm — belirgin "stilize" bir yürüyüş. Mevcut klip ise geniş duruşlu, yanal salınımı büyük
ve kolları dengesiz. İkisi de hedefin tam karşılığı değil. Core Motion ayakta duruşu (23 cm) tek başına en az riskli
aday: hareket içermiyor.

## 3. Eğimli zemin (gerçek harita, 3–10° yokuş)

- Ayaklar zemine uyuyor: ayak bileği kapsül tabanına göre −7…+16 cm aralığında yer değiştiriyor.
- Pelvis düz zemine göre alçak: yürüyüşte 80 cm (düzde 91), yokuş yukarı koşuda 75–78 cm (düzde 87–90).
- Diz daha bükük: yürüyüşte 151° (düzde 157°), koşuda 127° (düzde 132–140°).
- Gövde eğimi düz zemindekiyle aynı aralıkta; yokuşa özel bir gövde tepkisi yok.
- Kayıt başındaki durağan noktada ayaklar kapsül tabanının 9 cm altındaydı: kapsül o noktada görünen zeminin üstünde
  duruyor. Bunun harita çarpışmasından mı ayak yerleştirmeden mi geldiği doğrulanmadı.
- Bu kayıt duruş işlemi açıkken alındı; yokuştaki ayak kayması (12 cm) bu yüzden temiz bir ölçüm değil.

## 4. Fiziksel tepkiler

Mevcut sinyaller gerçek hareketle karşılaştırıldı (B_full_G):

- Hızlanma sinyali gerçek ivmeyi izliyor (ilişki +0,42); yalnız hızlanmada çalışıyor, frende sıfır.
- Dönüş sinyali 60°/sn yürüyüş dönüşlerinde hiç tetiklenmiyor.
- Efor, yorgunluk ve nefes sinyalleri depardan sonra yükseliyor.
- Yürüyüşten duruşta gövde değişimi en çok 2,7°; depardan duruş zaten klipten gelen büyük bir fren içeriyor.

Yeni prosedürel tepki eklenmedi. Gerekçe: yürüyüş freninde küçük gövde tepkisi insan için de olağan, depar freninde
klip zaten fazla; üstüne prosedürel eğim eklemek aynı tepkiyi iki kez vermek olurdu. Aday (uygulanmadı): hızlanma
sinyalinin eksi yöne de açılmasıyla hafif koşu freninde küçük karşı eğim.

## 5. Görünüm

- **Cilt:** baş ve gövde aynı ana malzemeden; fark yalnız mikro doku ölçeği (gövde 70, yüz 44) ve mikro maske seçimi.
  Gün ışığı, orman gölgesi ve iç mekân sıcak ışıkta boyun–göğüs geçişinde çizgi görülmedi. Gölgede gövde cildi düz ve
  az ayrıntılı okunuyor.
- **Kıyafet:** üst, şort, iç çamaşırı, kemer — hepsi tek LOD, düz kaplamalı, kumaş varlığı yok. Durağan pozda delinme
  görülmedi; üst, sırtın alt kısmında bedenden ayrık duruyor. Hareket içinde kıyafet oturması bu tur incelenmedi.
- **Saç:** fizik çalışma anında açılabiliyor (varlıkta ayarlı, bileşende kapalı). Yürüyüşte hafif hareket veriyor;
  koşuda ve dönüşte saç tamamen geriye yatıp alnı ve yüzü açıyor, sonra dağınık kalıyor. Ayar gerektirir; maliyeti
  ölçülmedi.
- **Işık:** iç mekânda pencereden gelen doğrudan güneş kol ve omuzda beyaza patlıyor. Orman gölgesinde yüz karanlık
  ama okunur.
- **Kamera:** bu turda oyun kamerası değiştirilmedi. İç mekân arka omuz karesi inceleme kamerasının duvara girmesi
  yüzünden kullanılamaz; oyun kamerası için kanıt değildir.

## 6. Hâlâ yapay olanlar

- Kol salınımı dengesiz (sol 45 / sağ 27 cm).
- Ayakta duruş geniş (30 cm).
- Yürüyüşte pelvis zıplaması ve yanal salınımı büyük.
- Gerçek haritada alçak pelvis ve bükük diz.
- 1. turdan açık kalanlar: yürürken dönüşte basan ayağın 13–36° dönmesi, depar frenindeki derin çöküş, eğilerek
  yürüyüşte 46–51° gövde.

## 7. Bu turda yaşanan ortam sorunları

- Saat 20:20 civarında motorun türetilmiş veri önbelleği, geçici çalışma klasörleri ve Blender 5.2 kurulumu makineden
  kalktı. Önbellek dolmadan alınan dört kayıt bozuk çıktı (karakter referans pozda, klip yok) ve analizde kullanılmadı.
- Blender 5.3 (Store sürümü) ile pano ve video üretimi yeniden kuruldu.
- Kullanıcı kaydı her adımda doğrulandı: SHA1 4823d83a03259aafa78ad4ecbe56c14986ac8879.

## Dosyalar

- `evidence/look_*.jpg` — üç ışık koşulu (soldan sağa: gün ışığı, orman gölgesi, iç mekân)
- `evidence/hair_off_on.jpg` — üst sıra saç fiziği kapalı, alt sıra açık
- `evidence/slope.jpg` — gerçek haritada yokuş kareleri
- `videos/uzun_yuruyus_yan.mp4` — 12 sn düz yürüyüş, yandan (geri alma sonrası)
- `data/` — ham ölçüm çıktıları
- `changes/degisiklik_manifesti.md` — yazma ve geri alma kayıtları
