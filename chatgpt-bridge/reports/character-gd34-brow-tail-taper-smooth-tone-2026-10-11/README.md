# GD34 — Kaş kuyruğu doğal bitiş, dalgalanma ve ton

Tarih: 2026-10-11. Başlangıç: GD33 kaşı c7u3. Yüz mesh'i (GD31 G31) ve sakin göz pozu (`AS_GD33_Rest_lid60`) değişmedi.

Durum: **PARTIAL.** Teknik testler geçti; görsel kabul senin incelemene bağlı (NOT_TESTED). Üretim karakterine uygulanmadı. Yeni varlıklar yalnız `/Game/Sphirus/CharacterLab/GD34_IdentityMaster_20261011` altında.

## 1. İsteğin

"Şakaklardaki kaş ucunu incelterek doğal şekilde bitir. Ayrıca dalgalanması var, bunu düzelt; renk farkı var gibi, bunu da doğallaştır."

## 2. Teşhis (GD33 c7u3, `process/00`)

- **Uç:** Kuyruk son birkaç milimetrede birden inceliyordu: kalınlık 4,2 mm'den önce 1,7, sonra 1,2 mm'ye düşüyordu. Bu yüzden önden kalın ve koyu bir çizgi gibi aniden aşağı kıvrılıyordu. q3R'da da uç ikiye ayrılmış görünüyordu.
- **Dalgalanma:** Üretici istasyonlar arasında doğrusal enterpolasyon yapıyor; her istasyonda küçük bir köşe oluşuyordu. Kuyruk da gövdeye S biçiminde bağlanıyordu: önce düz gidip sonra geç ve dik dönüyordu. Dış yarıda dikey eğriliğin yönü 4 kez değişiyordu.
- **Renk farkı:** Kuyruk gövdeden çok daha koyuydu. Sol kaşta ölçülen koyuluk kuyrukta 0,82, gövdede 0,54; referansta ikisi eşit. Kuyruk şakağın arkasına dolandığı için önden kısalmış görünüyor ve teller üst üste biniyor. Bunun yanında kaşın rengi referanstan biraz daha sıcak.

## 3. Yapılanlar (`tools/gd34_browsmooth.py`, `tools/gd34_brow.py`)

1. **Kaş yolu yumuşatıldı.**
   - Merkez çizgi 0,5 mm aralıklarla yeniden örneklendi ve 5 mm'lik bir Gauss filtresiyle yumuşatıldı.
   - Uçlar korundu: iç baş en fazla 0,26 mm kaydı, işaretli kuyruk ucu yerinde kaldı.
   - Yol 28 istasyona eşit aralıklarla dağıtılıp deriye izdüşürüldü.
   - Dış yarıda eğrilik yönü artık 4 değil, 1 kez değişiyor; S kıvrımı ortadan kalktı.
2. **Kuyruk düzgün inceltildi.** Kalınlık, kaşın son %38'lik bölümünde yumuşak bir eğriyle yaklaşık 6,5 mm'den 1,1–1,2 mm'ye iniyor.
3. **Kuyruk kılları sönümleniyor.**
   - Kuyruk bölgesi kaşın son %45'inde başlıyor.
   - Yoğunluk ortada 0,45'e, uçta 0,06'ya iniyor.
   - Uçtaki kıl uzunluğu ×0,6 yerine ×0,35.
   - Toplam tel sayısı 4995'ten 4368'e düştü.
4. **Ton dengesi.**
   - İç uç yoğunluğu 0,36'dan 0,45'e çıkarıldı; baş ile gövde arasındaki ton farkı azaldı.
   - Renk için nötr kahve bir MI eklendi (`MI_GD34_BrowS_l1n`): kızıllık 0,45 → 0,30, melanin 0,65 aynı.

Adaylar: ds3 ve ds5 (yumuşatma 3 ve 5 mm), ds6 (sönümlü kuyruk), **ds6n (ds6 + nötr ton, final)**.

| Ölçüm, önden, saç gizli | GD33 c7u3 | **GD34 ds6n** | Referans |
|---|---|---|---|
| Sol kaş koyuluk: baş / gövde / kuyruk | 0,59 / 0,54 / **0,82** | 0,59 / 0,53 / **0,66** | 0,54 / 0,42 / 0,42 |
| Kuyruk − gövde (sol) | +0,28 | **+0,13** | +0,01 |
| Gövde renk oranı R/G (sol / sağ) | 1,80 / 2,23 | 1,75 / 2,20 | 1,59 / 1,58 |
| Kuyruk kalınlığı: inceltme başı → uç | 4,2 → 1,2 mm, son 2 istasyonda | 6,5 → 1,2 mm, son %38 boyunca | — |

## 4. Editörde değerlendirme

1. Şu haritayı aç: `/Game/Sphirus/CharacterLab/GD34_IdentityMaster_20261011/Maps/L_GD34_Eval_G31`. Kameralar ve ışık GD32/GD33 ile aynı.
2. Sakin göz pozu yalnız **Simulate (Alt+S) veya PIE** sırasında görünür.

## 5. Panolar

- `T1`: kuyruk ucu, dalgalanma ve ton, saç gizli (REF | GD33 c7u3 | GD34 ds6n).
- `F2`: kaş yakın plan, saçlı (REF | GD33 | GD34).
- `M1`: işaretlediğin bölge (kırmızı); ds6n hâlâ bu bölgenin içinde.
- `F1`: genel sonuç. `C1`: baş-omuz dönüşü (kayıtlı Blueprint).
- `process/01`–`03`: ara adaylar (ds3, ds5, ds6, ds6n).

## 6. Teknik testler

| Test | Sonuç |
|---|---|
| GD34 üreticisi varsayılan ayarlarla c7u3'ü üretiyor | **PASS** (fark 3e-14) |
| Yumuşatma: uç ve iç baş korundu, S kıvrımı kalktı | **PASS** (kayma ≤ 0,26 mm; dış yarıda eğrilik yön değişimi 4 → 1) |
| İşaretli bölgeye uygunluk (q3R, profil) | **PASS** (`M1`) |
| Blueprint: 4 groom bağlaması, temiz yükleme, PIE (ds6n bağlı, `eyeUpperLidUp` 0,6) | **PASS** |
| Kayıtlı Blueprint ile çekim düzeninin birebirliği | **PASS** (yüz bölgesinde ortalama fark 0,013–0,016, yalnız gürültü) |
| Yüz mesh'i değişmedi | **PASS** |
| Üretim değişmedi | **PASS** (`data/outside_change_scan.txt`; qa_config geri yüklendi; editör kaydetmeden kapatıldı) |
| Görsel kabul | **NOT_TESTED** (senin incelemen) |

## 7. Açık kalanlar

- **Kuyruk hâlâ gövdeden biraz koyu** (+0,13). Bunun nedeni önden bakınca kuyruğun kısalmış görünmesi. Saçlı görünümde fark belirgin değil (`F2`). Daha da açmak gerekirse kuyruk yoğunluğu biraz daha azaltılabilir.
- **Renk:** Nötr MI'nın ölçülen renge etkisi küçük (R/G 1,80 → 1,75). Kaşın sıcak görünmesinin büyük kısmı seyrek tellerin arasından görünen turuncu tenden ve ışıktan geliyor. Ten rengi ayrı bir geçişte ele alınırsa kaş da kendiliğinden nötrleşir.
- **Sol ve sağ kaş farkı:** Sağ kaş gövdesi ışık yönü nedeniyle soldan koyu ölçülüyor (0,65'e karşı 0,53). Bu geometrik değil, aydınlatmadan kaynaklı.
