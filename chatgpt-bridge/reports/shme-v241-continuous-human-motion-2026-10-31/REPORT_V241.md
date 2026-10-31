# SPHIRUS V2.41: Sürekli İnsan Hareketi — Güvenilir Çıkış, Fiziksel Toparlanma ve Bütün Beden Sürekliliği — rapor

Temel: V2.40 (Bridge `9420bb5`). Tarih: 2026-10-31.

**Kısa sonuç:**
- **Üretim davranışı değişmedi. Üretim, V2.41 adayı için hazır değil.**
  - `SHM239_Own = 0`, `SHM240_ExtOn = 0`, `SHM240_HeadOn = 0`.
  - Yeni V2.41 anahtarlarının hepsi etkisiz değerde: `SHM241_KOn 0`, `SHM241_PushYawK 1`, `SHM241_StartOn 0`, `SHM241_BlkOnce 0`, pawn `GR241_YawRateK 1`, `GR241_StartOn false`.
  - AO düğümü hâlâ satıcı `BS_Neutral_AO_Stand`.
  - Her yapısal yamadan sonra üretim davranış kapısı koşuldu (`j38_c90r`, `j39_rl`, `j38_cc90`, `j40_wall`, `o`). Değerler önceki üretimle aynı aralıkta: c90r 10.2, j39_rl 36.5 (aynı sahip klip), cc90 5.5 cm.
- **Çözülenler (aday `tkha` = Own + HeadOn + KOn + bölgesel AO):**
  - `j39_rl`'nin ilk ayrışan karesi ve iki ayrı kök neden bulundu (§1).
  - Devralma artık sıradaki **gerçek temasın** klibine sürekli giriyor. Ölçümler:
    - 30 FPS: 12/14 doğru K.
    - 120/60/20/gerçek FPS: 22/24 doğru K.
    - Dört ıskanın dördü de aynı durum: `Cut_L_P20`, τ ≈ 0.41.
    - Zaman atlaması ±0.03 s içinde; tek istisna çok erken istek. V2.40'ta +0.19 / +0.62 s idi.
  - Üçüncü istekte en kötü kayma (30 FPS) 21.9 → 7.3 cm (`rlw`) ve 26.8 → 10.8 cm (`lrw`).
  - Bölgesel baş AO'su ortalama |baş − yön| farkını her FPS'de yarıya indiriyor: 40–55° → 17–28°. Ayak kayması artmıyor.
- **Üretime alınmayanlar ve nedenleri:**
  - Devralma sonrası yeniden kalkışı izleyen **yanal duruş** (satıcı `A_LS_Jog_Left_Stop`) hem üretimde hem adayda 16–65 cm kayıyor. Devralma bu duruşa sahip değil.
  - İtme toparlanması kısmi: yakalama adımı var, ancak 21.6 cm (30 FPS) ve itme sonrası yanal duruş 30–33 cm.
  - Duvar sonrası ayaklar boşta duruşa ~30–40 cm kayıyor. 120 FPS'de duruş bin'i atlıyor.
  - Sprint 90 adayda kötüleşiyor (6.4 → 14.0 cm).
  - 60 FPS'de üçüncü istek sonrası koşu döngüsü 24.6–28.1 cm.
  - 120 FPS'de devralma penceresinde baş ivme tepesi üretimin 2–3 katı.
  - Görsel ve oyun hissi kabulü yapılmadı. **Videolar üretildi ama gerçek zamanlı oynatılıp izlenmedi.** Yalnız zaman damgalı kare kâğıtlarının birkaçına göz atıldı; bu bir görsel kabul değildir.

Kanıt düzeni:
- `TABLES_V241.md`: bütün tablolar.
- `data/`: ham çıktılar (`entry_*.txt`, `align_*.txt`, `push_windows.txt`, `tables_*.md`, `chain.out`).
- `vid/`: videolar.
- `sheets/`: kare kâğıtları.
- `code/`: araçlar ve yamalar.
- `manifests/`: yazma manifestleri.
- Her ölçüm sabit adımlı editör PIE'si. Aday ve üretim kanıtı ayrı etiketlerde: `o` = kayıtlı üretim; `tkha` / `tkhaB` / `tkp` / `wst` / `wsto` / `aoh` = aday.

## Sorular

### 1. j39_rl'nin devralma sonrası yanlış kalkış nedeni (ilk ayrışan kare)

V2.40'ın "aynı build'de 26.6 / 78.9 cm" çifti **aynı fiziksel durum değildi**. `diverge231` bunu gösterdi:
- İki sabit adımlı koşu 2.733 s'de ayrışıyor (ilk adımlarda temas / FootPlacement durumu: ContactL, CaptureError farklı).
- 5.3 s'deki D tuşu bu yüzden koşu döngüsünün başka fazına düşüyor:
  - kötü koşu: döngü zamanı 0.47 → kesme bin'i P10;
  - iyi koşu: 1.24 → P21.

Bu ayrışma birbirine bağlı iki kusur açığa çıkardı.

**(a) Devralma girişi — kategori B, yanlış giriş zamanı.**
- P10'da istek, kesme zamanı 0.41'de geliyor; K2 klibinin penceresi [0.338, 0.698].
- MM ise K3 @0.667'ye girdi (+0.19 s ileri). Yeni plan 0.4 s geç başladı ve beden eski sağ dönüşü 49° fazladan sürdürdü.
- Neden: V2.40'ın (kaynak, hedef) giriş DB'sinde K1..K4 klipleri **aynı önekin kopyası**. Poz özellikleri fazı ayıramıyor, gelecekteki yörünge özelliği zamanı öne çekiyordu.
- Ayırt edici deney (`diag241_win.py`): K3'ün penceresi kuyruğuna daraltıldı. Aynı arama K2 @0.467'ye sürekli girdi: 25°, 0.30 s.
- **Düzeltme** (tek sahip, yeni bias / blend / bekleme yok):
  - (kaynak, hedef, K) başına **tek klipli** giriş DB'si: `PSD_SHM240_Eee_Kk`, 362 adet.
  - K = `SHM239_Step` eğrisinden, oynayan kesmenin o ana kadar yaptığı temas sayısı.
  - Yörünge ağırlığı 0 olan giriş şeması `PSS_SHM241_TkEntry`.
  - Anahtar `SHM241_KOn`.

**(b) Yeniden kalkış — kategori A + ownership.**
- Asıl 78.9 cm devralma çıkışında değil, duruştan 1.2 s sonraki kalkışta.
- Kamera yeniden merkezlemesi önceki devralmaya göre farklı ilerlemişti: −54° (kötü) / −68..−72° (iyi).
- A tuşu bedene göre 54° solda kaldı. Kalkış DB'si satıcının **dönen** kalkışını seçti (`TurnL045`, kök −45°).
- GR'nin yön yazıcısı (`GR_Impl_CP_PhysicalRedirect`) ise kapsülü kamera girdi çerçevesine, yani 37° sağa çevirdi.
- Klip ve kapsül zıt yönlere döndü → 78.9 cm DRAG.
- **Düzeltme adayı:** başlangıç yön sözleşmesi `SHM241_StartOn`.
  - Kökü dönen 8 kalkış kopyasına `SHM241_SYaw` / `SHM241_SW` eğrileri işlendi.
  - Bu kliplerden biri pozdayken kapsül, klibin kendi kök yönünü izliyor (`SYaw / SW`, V2.38'deki `Turn / W` gibi).
  - Sonuç: aynı yeniden kalkış 78.9 → 9 cm.
  - Üretime alınmadı: `jstart`'ta satıcı `TurnR045` klibi 1.87 s DRAG ile 48–83 cm. Bu içerik sınırı; koşudan koşuya 48–83 cm arasında değişiyor.

**Şimdiki en kötü değer (`j39_rl` / `j41_rl_*`) başka bir sahibe ait** (§2).

### 2. Devralmadan sonra gerçek ilk adım ve yanal kalkışın yerine ne geçti

- Devralma çıkışında ilk adım artık gerçek sıradaki temas: K klibi, kesmenin aynı karesinden devam ediyor.
  - Çıkış ayağı oynayan kesmenin destek ayağı.
  - L ve R için de doğru: `j41_lr_p10` ve `j41_rl_p10` her FPS'de doğru K (§3).
- Duruştan sonraki yeniden kalkışta hem üretim hem aday satıcı `A_LS_Jog_Left_Start` klibini seçiyor (yanal kalkış; aktör yönü −68..−70°, hız −158°). Bu klip 8.8 cm ile sorunsuz.
- **Yanal kalkışın yerine yeni bir klip konmadı.** Ölçüm sorunun kalkış değil, onu izleyen satıcı yanal duruşu olduğunu gösterdi:
  - `PSD_LS_CoreLateralStop` → `A_LS_Jog_Left_Stop`, klip zamanı 1.30 s'den giriliyor.
  - O anda kapsül hâlâ 184–200 cm/s.
  - Sonuç: 16–65 cm SLIP. FPS'ler: üretim 30.6 / 64.7 / 60.6 / 15.9; aday 31.3 / 57.1 / 61.2 / 33.6 (120 / 60 / 20 / gerçek).
- V2.37'nin faz planlı duruşları yalnız ileri koşuyu kapsıyor. Yanal koşu duruşu **açık boşluk**. Sahibi: duruş DB'si seçimi + içerik (yanal faz planlı duruş ailesi yok).

### 3. Giriş / çıkış güvenilirliği — 20 / 30 / 60 / 120 / gerçek FPS

`entry241.py`: istek anındaki kesme zamanı τ, beklenen K, girilen K ve atlama. Tablo: `TABLES_V241.md` §3.

| FPS | doğru K | atlama aralığı | eski yöne taşma | geri dönüş gecikmesi |
|---|---|---|---|---|
| 30 (reg) | 12/14 (iki ıska: `L_P20`, K1 yerine K2) | −0.012..−0.008 s (erken istek `rl_e`: −0.203 s) | 9–43° | 0.13–0.63 s |
| 120 | 6/6 | −0.019..+0.014 s | 16–41° | 0.30–0.38 s |
| 60 | 6/6 | −0.002..+0.013 s | 13–41° | 0.30–0.37 s |
| 20 | 6/6 | −0.030..+0.010 s | 12–32° | 0.15–0.40 s |
| gerçek | 4/6 | −0.021..+0.017 s | 8–59° | 0.12–0.36 s |
| V2.40 tkh (30) | P10 K3, P02 K4 yanlış | +0.19 / +0.62 s | 49 / 80° | 0.73 / 0.87 s |

- Dört ıskanın dördü de aynı durum: `Cut_L_P20`, τ 0.411–0.421. İkisi 30 FPS'de, ikisi gerçek FPS'de.
  - Klip sürekli (atlama −0.011..−0.015 s) ama bir temas geç.
  - Taşma 30 FPS'de 25°, gerçek FPS'de 52–59°.
  - Bu bin'de `SHM239_Step` eğrisi ile gen239 temas tablosunun K1/K2 sınırı uyuşmuyor gibi görünüyor. Neden ayrıştırılmadı. Açık.
- Erken istek (`j39_rl_e`, τ 0.204): K1 klibinin 0.133 s'sine giriliyor, yani klip saati 0.2 s geri gidiyor.
  - Klipler aynı önekin kopyası olduğu için poz yakın; ayak kayması 7.0 cm.
  - Yine de bu bir zaman sıçraması. K1 penceresi istek zamanından önce başlamamalı. Açık.
- Aynı zaman ile aynı fiziksel durum ayrı tutuldu. V2.41'in `move.gates`'i isteği koşu döngüsü zamanına bağlıyor (`j41_*`). Kapısız `j39_*` koşuları farklı bin'lere düşebilir; tablolarda ayrı.
- 120 FPS: türev gürültüsü yüksek. Pop sayıları 30 FPS ile doğrudan karşılaştırılamaz.

### 4. Üçüncü istek ve hız sınırı

İstek dizisi: ileri → sağ 90 → fren ortasında sol → ileri → dur (`j40_rlw` / `j41_rlw_p10`; ayna `j40_lrw`).
- 30 FPS: en kötü kayma `rlw` 21.9 → 7.3, `lrw` 26.8 → 10.8 cm. Üçüncü istekte ilk destek 0.03 s, sabit yön 0.9–1.03 s.
- FPS (aday): 120 → 8.7–9.1; 20 → 6.7; gerçek → 10.6 cm.
- **60 FPS'de 24.6 / 28.1 cm** (`A_CT_Jog_Fwd` @7.2 s, üçüncü istekten sonraki koşu döngüsü). Sahibi çözülmedi, açık.
- **Hız sınırı:**
  - Koşu (250 cm/s) çalışıyor.
  - Sprint 90 (`s38_c90r`) adayda 6.4 → 14.0 cm (`SHM216_Cut_R_090_Lfoot`).
  - Sprint hızında takeover DB'si yok (V2.39 klipleri koşu kaynaklı). Sprintte üçüncü istek desteklenmiyor, dürüst sınır budur.

### 5. mtf_jog ve uzun zincirler (ad_jog / mt_jog)

- `mtf_jog`: 30 FPS üretim 50.7, aday 48.9 cm. FPS'lerde 17–23 cm.
  - İkisinde de sahip `SHM216_RevTurn_R_Lfoot`: V2.16 dönüş içeriği.
  - Devralma bu klibe girmiyor; içerik sınırı.
- `ad_jog` / `mt_jog` farkının gerçek nedeni: **aynı fiziksel durum değil.**
  - Bütün o-aday çiftleri ilk adımda (2.13–2.53 s) ayrışıyor. Neden: `SHM_PelvisOffset` iki değer arasında gidip geliyor (0.435 / 0.441).
  - Aynı build'deki o-o çifti de 2.4 s'de ayrışıyor.
  - Yani `jstart`, `j35_rev`, `jlean`, `mt_jog` ve `ad_jog` farkları adayın etkisi olarak okunamaz.
  - `j35_rev` adayda 34.5 cm: farklı ters dönüş bin'inden (P19) sonra `RecoveryDemand` toparlanma ailesi 6'ya girişte tek karelik ayak sıçraması. Bu da farklı fiziksel giriş.

### 6. İtme toparlanması

`push_windows.txt`, 300 cm/s sola itme, planlı sağ 90 sırasında:

| varyant | yakalama [5.55, 6.10) | çıkış [6.10, 6.90) | not |
|---|---|---|---|
| o (üretim) | 0 | 0 | itme etkisi yok sayılıyor; bu toparlanma değil |
| tkk | 22.6 | 8.2 | yakalama ailesi seçiliyor; kapsül eski plana dönüyor |
| tkp (`PushYawK` 0.15) | 0 | 25.6 | gövde yakalarken dönmüyor; çıkışta `RevPush` yeniden girişi |
| ext (yalnız `ExtOn`) | 19.3 | 9.4 | |

- Kök neden (V2.40 `tkh`): dış etki planı geri çekiyor, yakalama klibi seçiliyor. Ama GR'nin yön yazıcısı kapsülü **eski planın hedefine** 280 → 40 °/s ile çevirmeye devam ediyor: 0.4 s'de 21 → 84°, hız ise −45 → +5°.
- `SHM241_PushYawK`, dış etki süresince bu dönüş hızını ölçekliyor:
  - yakalama penceresindeki kaymayı 0'a indiriyor;
  - ama çıkışta 25.6 cm (`RevPush` yeniden girişi).
- Tam zincir (30 FPS `j39_push_plan`): aday 21.6 cm. Tek karelik `A_CP2_Jog_Left_Pivot`.
- FPS'lerde en kötü değer itmeden sonraki yanal duruş: `A_LS_Jog_Right_Stop` @8.2 s, 29.7–33.5 cm (§2 ile aynı sahip).
- **Sonuç: PARTIAL.** Doğal bir yakalama adımı var. Ama kaymasız tam bir toparlanma yok, üretime alınmadı.

### 7. Duvar

- **30 FPS üretim:**
  - Kapsül tek karede duruyor (283 → 2 cm/s) ve sonra hızı 0. **Yerinde koşma yok.**
  - Kapsül duvara girmiyor. Ama ayak kemiği 6.6 s'de duvar yüzünün ~8 cm ötesinde (y 148, yüz 140).
  - İki ayak 0.8 s içinde boşta duruşa ~40 cm geri kayıyor (y 140 → 100).
- **wst (V2.37 JogStop DB'si) ve wsto (`BlkOnce`):** 30 FPS'de birebir aynı, 23 cm + boşta 25.7 cm.
- **120 FPS bin atlaması** (V2.37 duruş girişi atlamasıyla karşılaştırma):
  - Atlama dizisi Br_P03 → Bl_P16 → Bl_P05 → Bl_P17, hepsi t 0.00, 1–3 kare arayla. wst ve wsto aynı.
  - Ardından Dense kalkış/döngü klibine çıkış: 30–44 cm SLIP.
  - `BlkOnce` hipotezi çürüdü: throttle'ı yalnız zorlanan karede bırakmak atlamayı gidermiyor.
  - Sahip sorgunun kendisi: kapsül hızı duvarda 0.13 s'de 39'dan 24'e düşüyor, her kare başka bir faz bin'i en yakın oluyor.
  - V2.37 duruş girişi atlamasının biçimi aynıydı. Orada sürekli bias atlamayı yalnız gizliyordu, o yüzden bias körü körüne kopyalanmadı.
- FPS'ler: üretim 29.6 / 38.1; wst 31–44; wsto 30–43 cm. **FAIL / açık.**
- **Kamera bulgusu** (üretimde de var), `sheets/wall_prod_game.png` ve `wall_v241_game.png`:
  - Duvarda oyun kamerası çarpışma nedeniyle karakterin ensesine kadar giriyor.
  - 6.4 s'den sonra kadrajda yalnız baş, boyun ve saç var; ayaklar görünmüyor.
  - Bu yüzden duvardaki ayak kayması videoda görülemiyor; yalnız LTP ölçümü var.
  - Sabit yan kamera da duvarın arkasında kaldı ve kullanılamadı, video seti dışında bırakıldı.
  - Sahibi kamera çarpışma / çerçeveleme (`sphirus-camera-direction`). Açık.

### 8. Baş / boyun ve göğüs / pelvis sahipliği

- Yeni varlık `BS_SHM241_AO_Head`: satıcı AO'nun bölgesel kopyası, 9 örnek + 6 yardımcı = 15 sekans kopyası. Orijinallere dokunulmadı.
  - Kök, pelvis ve bacak kemiklerinin ofseti 0.
  - Omurga örneğe göre 0.3 oranında karışık.
  - Boyun ve baş tam.
- Böylece baş, gövdeden ayrı sahiplenebiliyor. V2.40'ın sorunu: AO'yu plan içinde soldurmak pelvis payıyla basılı topu bir karede 3 cm oynatıyordu.
- Aday ölçümleri, ortalama |baş − yön| / |göğüs − yön| (+0.3..+2.0 s, ikinci istekten sonra):

| senaryo | o 30 | tkha 30 | o 120 | tkhaB 120 | o 60 | tkhaB 60 | o 20 | tkhaB 20 | o gerçek | tkhaB gerçek |
|---|---|---|---|---|---|---|---|---|---|---|
| j41_rl_p10 | 52 / 17 | 27 / 12 | 52 / 16 | 23 / 12 | 55 / 17 | 28 / 13 | 53 / 19 | 28 / 13 | 54 / 17 | 21 / 12 |
| j41_lr_p10 | 54 / 40 | 29 / 16 | 40 / 38 | 19 / 12 | 48 / 25 | 19 / 12 | 49 / 24 | 18 / 11 | 47 / 25 | 24 / 13 |
| j38_cc90 | 39 | 15 | 29 / 43 | 14 / 17 | 33 / 45 | 14 / 19 | 40 / 20 | 13 / 21 | 23 / 22 | 16 / 21 |

- Yalnız AO (`aoh`, `j39_lr` 30 FPS): 23.1 / 9.1, üretimde 47.5 / 31.2. Devralmasız da işe yarıyor.
- Basılı ayaklar oynamıyor: ayak kayması tabloları AO'lu ve AO'suz aynı aralıkta (`TABLES_V241.md` §1).
- **Açık risk:** 120 FPS'de devralma penceresinde (istekten 0.3 s sonra) baş ivme tepesi 186–251 m/s², üretimde 82–102.
  - 60 FPS: 115–133 / 40–83. 30 FPS: 56–75 / 25–67.
  - V2.40 `tk` (AO yokken) 120 FPS'de aynı mertebedeydi: 117–307. Bu yüzden büyük olasılıkla devralma girişi.
  - AO'suz V2.41 120 FPS koşusu yapılmadı. **AO payı NOT_TESTED.**

### 9. Canlı destek kararı

- Devralma, kesmenin **o ana kadar gerçekleştirdiği temas sayısına** (`SHM239_Step`) ve kesmenin kaynak bin'ine bakarak hangi temastan devam edeceğine karar veriyor. Hangi ayağın gerçekten serbest olduğunu ve kesmenin aynı karesini kullanıyor.
- İtmede `SHM239_Ext` destek planını geri çekiyor. `PushYawK`, gövdeyi yakalarken çevirmiyor.
- Bu bir **durum eşlemesi**. Ağırlık merkezi / XCoM (capture point) denetleyicisi değil, öyle iddia edilmiyor. Ayak yerleşimi kuvvet yönünden hesaplanmıyor; klip içeriğinden geliyor.

### 10. Korunan kazanımlar

- **V2.38 fizik planlı 90:**
  - `j38_c90r` üretim 8.4 / 8.5 cm (120 / 60), 30 FPS 9.7.
  - Kapı koşusu 10.2.
  - Aday 8.1 / 5.9 / 0.0.
- **V2.37 kalkış / duruş:** `j36_stop`, `j36_stopr`, `j36_rsm` ve `wstart` üretimde değişmedi (0–14 cm, önceki aralıkta).
- **V2.40 deterministik devralma:** V2.40 yolu (`KOn 0`) olduğu gibi duruyor. V2.41 yolu her FPS'de sürekli giriyor.
- **Kamera:** `cam32_j90` 10.2 / 10.8.
- **Diğer:** e29 11.1 / 11.1, c29 15.4 / 15.5.

### 11. Üretime alınanlar ve deneysel kalanlar

- **Üretime alınan davranış: yok.**
- Kurulu ama etkisiz (anahtar kapalı, varsayılan = V2.40 davranışı):
  - `SHM241_KOn`: K başına giriş DB'si.
  - `SHM241_PushYawK`: itme yön tutma.
  - `SHM241_StartOn`: kalkış yön sözleşmesi.
  - `SHM241_BlkOnce`: tek karelik throttle bırakma; çürüdü, kapalı kalıyor.
  - `GR241_YawRateK` / `GR241_StartOn`: pawn tarafı.
- Bağlanmamış yeni varlık: `BS_SHM241_AO_Head`. Yalnız PRE/POST bellek içi takasla denendi, hiç kaydedilmedi.
- Değişen aday verisi: V2.40'ın 96 `PSD_SHM240_E*` giriş DB'si artık `PSS_SHM241_TkEntry` şemasını kullanıyor (yörünge ağırlığı 0). Bu yalnız `SHM239_Own 1` yolunu etkiliyor; üretim bu DB'lere girmiyor.

### 12. Sayılar

- **Yeni hareket animasyonu: 0.**
  - 15 AO sekans kopyası + 1 blend space.
  - 8 kalkış kopyasına 2 eğri işlendi (poz değişmedi).
  - 362 tek klipli giriş DB'si + 1 şema.
  - 362 V2.39 takeover klibine yeni BranchIn izi (`SHME_V241_K`).
- **Test koşuları:** ~268 V2.41 LTP etiketi (`v241*`).
  - 30 FPS regresyon (o + aday, ~38 senaryo).
  - 120 / 60 / 20 / gerçek FPS blokları.
  - 20 + 10 video çekimi.
  - Kapı koşuları.
- **Editör yeniden başlatma:** 6 zincir yeniden başlatması + 1 çökme sonrası kurtarma. Çökme: Python'dan PoseSearch kanalı eklemek indeksleyiciyi düşürdü; manifest yedeğinden geri yüklendi.

### 13. Açık boşluklar ve nedenleri

| boşluk | ölçüm | neden (sahip) |
|---|---|---|
| Devralma sonrası yanal duruş | 16–65 cm (o ve aday) | satıcı `A_LS_Jog_*_Stop` 1.30 s'den, 184–200 cm/s'de giriliyor; yanal faz planlı duruş ailesi yok |
| İtme toparlanması | 21.6 cm (30), çıkış 25.6 (`tkp`), sonrası 30–33 | yön yazıcısı eski plana dönüyor; `PushYawK` sonrası `RevPush` yeniden girişi; itme sonrası yanal duruş |
| Duvar | 30–44 cm ayak kayması, ayak 8 cm duvar ötesinde | duvarda hız çökerken her kare başka faz bin'i; ayak IK duvarı bilmiyor |
| Sprint 90 | 14.0 cm aday | sprint kaynaklı takeover içeriği yok |
| 60 FPS üçüncü istek | 24.6–28.1 cm `A_CT_Jog_Fwd` | sahip ayrıştırılmadı |
| `L_P20` K sınırı | 4 koşuda bir temas geç (25–59°) | `Step` eğrisi / temas tablosu sınırı; ayrıştırılmadı |
| Erken istek geri sarma | `rl_e` −0.203 s | K1 penceresi istek zamanından önce başlıyor |
| 120 FPS baş ivmesi | 186–251 m/s² | devralma girişi (V2.40 ile aynı mertebe); AO payı ölçülmedi |
| `jstart` | 48–83 cm | satıcı `TurnR045` içerik sınırı |
| `mtf_jog` | 49–51 cm (30) | V2.16 `RevTurn` içeriği |
| Aynı fiziksel durum | o-o ilk adımda ayrışıyor | `SHM_PelvisOffset` iki değer arasında gidip geliyor; kapılı senaryo gerekli |
| Duvarda kamera | kamera enseye giriyor | kamera çarpışma / çerçeveleme |
| Görsel / oyun hissi kabulü | — | yapılmadı; videolar izlenmedi |

## Doğrulama durumu

- **Teknik:**
  - Derleme, kayıt ve manifest kontrolleri PASS.
  - Üretim kapısı PASS (değişmedi).
  - Son editörde `VERIFY241 ALL_OK`, ölçüm işi, yazma yok (`data/verify241.out`):
    - V2.40 doğrulaması ALL_OK;
    - `KOn 0`, `PushYawK 1`, `StartOn 0`;
    - pawn `GR241_YawRateK 1` / `GR241_StartOn False`;
    - 362 K-DB, bozuk 0;
    - AO düğümü `BS_Neutral_AO_Stand`;
    - 15 AO örneği;
    - snapshot öksüzü 0;
    - kirli paket yok.
  - `BlkOnce` varsayılanı 0, kurulumda ayarlandı. Üretim kapısının duvar koşusu V2.40 ile aynı.
- **Aday hareket kabulü: PARTIAL.** Giriş sürekliliği ve baş hizası PASS; yanal duruş, itme ve duvar FAIL.
- **Görsel / oyun hissi kabulü: NOT_TESTED.**

## Videolar ve kare kâğıtları

Videolar `vid/` klasöründe.
- Her biri sabit adımlı 30 FPS çekim, yani oyun zamanı gerçek hız. Kareler tam ve kurgusuz, yavaş çekim yok.
- Her sahne için `*_realtime.avi` (normal hız) ve küçültülmüş `.gif` var.
- `o` = üretim, `v241` = aday `tkha`.
- AO'lu aday çekimleri (`v241cap2_*`) her koşuda `PREAO241 set 1` ile doğrulandı. İlk K çekimlerinde PRE reddedilmişti ve AO yoktu; o çekimler yayımlanmadı.
- **Hiçbiri gerçek zamanlı oynatılıp izlenmedi.**

| sahne | videolar | kamera |
|---|---|---|
| Üçüncü istek (ileri > sağ 90 > fren ortasında sol > ileri > dur) | `third_request_prod_side`, `_v241_side`, `_v241_diag`, `_v241_game`, `_prod_game` | yan / dörtte üç / oyun |
| Sola 90 > fren ortasında sağ | `left_then_right_prod_side`, `_v241_side` | yan |
| Ardışık kesmeler (W > D > W > A) | `consecutive_cuts_prod_side`, `_v241_side` | yan |
| Planlı sağ 90 sırasında itme | `shove_prod_side`, `shove_v241_side`, `shove_v241_yawhold_side` (`tkp`) | yan |
| Sert sağ 90 sonrası baş | `head_after_cut_prod_game`, `_v241_game`, `_aoonly_game` | oyun |
| Duvar | `wall_prod_game`, `wall_v241_game`; kamera enseye giriyor, §7 | oyun |
| Kapılı sağ > sol > dur > yeniden kalkış | `right_left_gated_prod_side`, `_v240_side` (yanlış K), `_v241_side` (doğru K) | yan |

Kare kâğıtları `sheets/` klasöründe (zaman damgalı, kurgusuz):
- `third_request_*`
- `right_left_gated_*`
- `restart_lateral_stop_prod/v241_side`: yanal duruş, iki varyantta da aynı sahip.
- `shove_*`
- `wall_*_game`
