# SPHIRUS V2.39: Komutlar arası fiziksel süreklilik, devralma ve dış etki (V2.38 c0737f9 üzerine)

Tarih: 2026-10-30.

**Kanıt:**
- 30 FPS: `data/tables_reg.md`, tek editör oturumu; o (üretim) ile tk (aday) aynı oturumda.
- FPS kipleri: `x60`, `x120`, `x20`, `xreal`.
- Temiz açılış: `VERIFY239 ALL_OK`.

**Etiketler:** teknik sonuç PASS / FAIL / PARTIAL / NOT_TESTED ile verildi. Görsel ve oyun hissi ayrı yazıldı; onların kabulü sende.

## Özet

**Kök neden bulundu ve düzeltildi.** V2.38'de ikinci komut, çalışan planın veritabanını bölüm sınıfına kaptırıyordu. V2.39'da:
- Plan, kendi klip ağırlığı sürdükçe veritabanının ve kapsül sözleşmelerinin sahibi.
- Yeni istek anında algılanıyor.
- Hareket, kesmenin gerçek durumundan sürüyor: hız, yön, destek ayağı ve döngü evresi devralınıyor; yeni plan bir sonraki planlı basışta başlıyor.
- 364 adaydan 362 devralma klibi üretildi; 2 tanesini bacak koruması reddetti.

**Gerçek dış etki ile planlı hız değişimi ilk kez ayrıldı.** Ayırım tek bir artık (residual) ölçüsüyle yapılıyor:
- Planlı hareket ≤ 9 cm/s; gerçek itme 282 cm/s.
- İtmede plan geri çekiliyor ve mevcut toparlanma adımı çalışıyor.
- V2.38 üretimi plan sırasındaki itmeyi tamamen siliyordu.

**Üretime alınmadı.** 30 ve 20 FPS'te çoğu zincir iyileşiyor. Ama 120 FPS ve gerçek zamanda devralma girişi kararsız:
- j39_rw 116 cm;
- cc90 112 cm.

Bu, "aynı fiziksel durum her FPS'de aynı aileye düşmeli" ölçütünü karşılamıyor. V2.39 kurulu ama `SHM239_Own` = 0 ile etkisiz; üretim V2.38 davranışında (`VERIFY239 ALL_OK`).

**Açık:**
- Depar 90° yapılmadı.
- Baş yönü (vendor aim offset) çözülmedi.
- mtf_jog kapanmadı.

---

## İlk sayfa: soruların cevapları (1–14)

**1. V2.38'deki ikinci komut hatasının gerçek nedeni neydi?**

Sahiplik hatası; ilk yanlış kare bulundu.
- **Kanıt (cc90, 30 FPS):** 6.17 s'de ikinci basışla bileşen bölüm sınıfı 1'den 0'a değişti. ABP bölümü yeniden başladı (`SHM_RedirectFrames` 1'e döndü) ve "ilk kare" rotası sınıf 0 için `JogSteady`'yi seçti. Fren ortasındaki kesme klibi bırakıldı.
- **60 FPS sol kesme:** aynı mekanizma, ama yeni giriş olmadan (6.05 s). Bileşen hız ile giriş arasındaki açıya göre sınıfı kendi kendine değiştirdi.
- **Üçüncü basış:** hız ile giriş arası açı yaklaşık 101° → sınıf 2 → V2.16 RevTurn → 71 m/s² patlama.
- **İkinci kusur:** yeni istekte V2.28 sözleşmesi tek kare düşüyor (`SHM228_On`). Bu, V2.38 yön kilidini yeni girişe yeniden kilitliyordu. Eski kesme klibi oynarken yön yeni isteğe göre hesaplandı: aktör yönü 0.2 s'de 42°'den −81°'ye sıçradı (1400°/s).

**2. Yeni istek mevcut hareketin hangi fiziksel durumunu devralıyor?**

| Ne | Nasıl |
|---|---|
| **Kapsül hız vektörü** | Hız ve yön; plan simülasyonu bu gerçek hızdan başlıyor |
| **Destek ayağı ve döngü evresi** | Takeover klibinin ön kısmı kaynak kesmenin birebir kopyası (ayak hedefleri t_K'ya kadar kaynağınki, fark ≤ 5 cm); MM, oynayan karenin aynısına giriyor |
| **Planlı temas saati** | Yeni `SHM239_Step` eğrisi kesin; bileşenin topuk bayrakları ~0.1 s geç kalıyor |
| **Başlamış fren/itiş planı** | Havadaki ayak eski plana göre iner (artık yönlendirilemez); o temas yeni planda fren (yeni dönüşün iç ayağı) ya da zayıf plant (dış ayak) olur |
| **Beden** | Eski planın baş/göğüs/pelvis katmanları t_K'dan itibaren söner, yenileri gelir; gövde yönü hızla birlikte sıfırdan geçmez, hız düştükçe yeni yöne döner (en fazla 330°/s) |

Efor (`EffortE`) ayrıca bağlanmadı. Planın hız düşüşü ve temas sayısı eforu içeriyor.

**3. 60 FPS'te erken kesilme giderildi mi?**
- Adayda evet: 60 FPS sol kesme 15.0 cm'den 9.1 cm'ye indi; plan sahibi sınıf değişiminde veritabanını korudu, döngüye erken düşme yok.
- **Üretimde değil** (aday üretime alınmadı).
- 120 FPS'te aday sol kesme 6.6 cm (V2.38'de 45.3).

**4. mtf_jog ve art arda dönüşlerdeki gerileme kapandı mı?**
- **Art arda (cc90):** RevTurn'e düşme yok; ikinci ve üçüncü istek devralmayla karşılanıyor.
  - 30 FPS: 11.2 → 8.9 cm, patlama 73 → 63.
  - 60 FPS: 18.8 / 128 → 11.6 / 63.
  - 120 FPS: 112 cm (FAIL).
- **mtf_jog:** 30 FPS'te 48.9 cm (o = tk). **Kapanmadı.** Titrek kesmeler artık devralmayı tetikliyor ama hâlâ eski RevTurn sonu var.
- jlean 120 FPS: 15.3 cm (o 21.2), ama patlama 294.

**5. Canlı denge değerlendirmesi hareket kararını gerçekten değiştiriyor mu?**

Kısmen; dürüst ayrım şöyle:
- **Kararı değiştiren canlı durum:**
  - yeni niyet ile planın hedefi arasındaki açı (devralma / devam);
  - Back / Opp seçimi;
  - gerçek kapsül artığı (dış etki → plan geri çekilir, toparlanma).
  - Bunlar her karede canlı veriden hesaplanıyor.
- **Hareketin kaç destek alacağı:** devralınan gerçek hızın aynı itki bütçesiyle simülasyonundan çıkıyor. Bu çevrimdışı, ama durum sınıfına göre (kaynak bölme, K, hedef). Oyunda doğru durumu MM seçiyor.
- **`SHM239_Bal` / `NeedN`:** yalnız telemetri. Canlı hız ve niyetten gereken destek sayısını açıklıyor (Stable / Controlled Redirect / Recovery Step / LoB adayı). Tam denge denetleyicisi değil.

**6. Normal destek ile ilave toparlanma adımı farklı koşullarda nasıl seçiliyor?**

Devralınan duruma göre, aynı itki bütçesiyle:

| Durum | Plan | Destek sayısı |
|---|---|---|
| Back: 58° geri dönüş, 180 cm/s | sol fren → sağ plant (123 cm/s) → transfer → itiş | normal |
| Opp: 148° karşı tarafa, aynı başlangıç | fren hızı ~20 cm/s'ye indirir → plant → pivot (≤ 330°/s) → itiş | **ilave destek** |

Aynı kesme evresinde gelen istek, hızın yönüne göre farklı plan alıyor: rl (sol) ile rw (ileri) aynı anda istendi, farklı ailelere gitti.

**7. Karakterin bütün bedeni momentum değişimine katılıyor mu?**
- **İçerikte:** evet. Fren eğilmesi a/g'den, kol sönümü fren payıyla, göğüs/pelvis öncüsü yeni plana göre, pelvis inişi ≤ 5.4 cm (önceki kuralla 15 cm idi; düzeltildi).
- **Oyunda baş:** vendor aim offset yüzünden yeni niyete dönmüyor (rl'de 2.07 s gecikme). Bkz. 8.
- **Görsel:** NOT_TESTED. Sabit yan kamera karakteri çoğunlukla arkadan görüyor. Sayfalarda fren duruşu var ama oyun hissini ben doğrulayamadım.

**8. Baş, göğüs ve pelvisin dönüş sonu uyumu düzeldi mi?**
- **Hayır (FAIL).** 1.8 s sonra (yön − hız yönü) baş adayda 56–83°, üretimde 42–82°. Pelvis ve göğüs çoğunlukla ≤ 15°.
- Üretilen klipte baş katmanı yeni yöne öncü olarak yazıldı (`gen239_tk`, ±30°). Oyunda görünen baş kamera yönüne yakın kalıyor. V2.38'de bunun sahibi vendor `LookAtAimOffset` olarak bulunmuştu. Ara katmanlar (MM sonucu, retarget, post-process) bu turda ayrı ayrı ölçülmedi; ilk ayrışan katman kesin olarak belirlenmedi.
- Bu turda değiştirilmedi: sahiplik çözümü, oyuncu manuel bakışını bozmayan bir öncelik kuralı istiyor. **Açık.**

**9. Planlı hızlanma ile gerçek dış kuvvet ayrıldı mı?**

**Evet (adayda, PASS 30 FPS).**
- Klip-hız sözleşmesiyle kapsül hızını plan tanımlıyor; artık = |ölçülen − komut|.

| Durum | Artık |
|---|---|
| Planlı kesme | ≤ 9 cm/s |
| Plansız tempolu koşu | 0 |
| Gerçek 300 cm/s itme | 282 cm/s |

- 80 cm/s üstünde plan geri çekiliyor: sözleşmeler, sahip ve aile koruması bırakılıyor.
- Paralel dedektör eklenmedi; mevcut `pushRaw` çalışıyor.

**10. Dış etki sırasında gerçek toparlanma hareketi tetiklenebiliyor mu?**
- **Evet (adayda).** Plan sırasındaki itme taşındı (vy −209 cm/s), aile 6 (`SHM_Rec_FL_Rfoot`) ve ardından aile 3 çalıştı.
- **V2.38 üretiminde:** itme bir sonraki karede siliniyordu, toparlanma hiç yoktu.
- Bedel: itmeden sonraki duruşta kayma 17–34 cm. İtme gerçekten taşındığı için durma ailesi zorlanıyor; **açık**.

**11. Depar 90° için nasıl bir fiziksel ön-fren hareketi üretildi?**
- **Üretilmedi (NOT_TESTED).** Brif, ilk art arda jog devralma ve canlı devralma kararlı olmadan depara geçilmemesini istiyor; ben de bu sırayı izledim.
- Devralma 120 FPS'te kararlı değil, bu yüzden depar ön-fren prototipi ertelendi.
- V2.38'in reddi korunuyor: aynı plan depar için 8 temas ve ~2 s istiyor.

**12. Duruş, başlangıç, kamera ve geri hareket kazanımları korundu mu?**
- **Üretimde evet.** Üretim V2.38: `VERIFY239 ALL_OK`, `SHM239_Own` = 0; tüm V2.39 grafik yamaları bu düğmeye bağlı ve etkisiz.
- Üretim (o) koşuları V2.38'in son değerleriyle aynı: jlean 11.8, j34 7.5, mtf 48.9, e29 11.1, c29 15.4.
- Adayda durma, başlangıç ve geri hareket büyük ölçüde aynı. Farklar:
  - j36_stopr 0 → 5.5 cm;
  - jstart (vendor) 53.7 → 63.8 cm;
  - wstart 14.2 → 16.7 cm;
  - takeover sonrası lateral durma: rl 24.9, lr 26.3, 60 FPS'te 57.5 cm.
- S tuşu ve çift pelvis korunuyor.

**13. Ne üretimde, ne deneysel, ne reddedildi, ne açık?**
- **Üretimde (V2.39'dan):**
  - yalnız etkisiz kurulum ve doğrulama;
  - 48 kesme klibine eklenen `SHM239_Step` / `StepN` eğrileri (poz verisi değişmedi; davranış değişmez).
- **Deneysel aday** (`SHM239_Own` = 1, düğme kapalı):
  - plan sahibi;
  - yön kilidi koruması;
  - 362 devralma klibi ve 8 taraflı veritabanı;
  - istek anında geçiş (arama freni açılır);
  - dış etki artığı;
  - canlı denge okuması.
- **Reddedilen:**
  - takeover klipleri kesme veritabanına karıştırmak: kesme girişinde istenmemiş geri dönüş (`PSD_SHM239_JogCutTk`, kullanılmıyor);
  - düşük trajectory ağırlıklı şema (`PSS_SHM239_Takeover`, eski birleşik veritabanlarında; etkisiz);
  - tek-kare zorlama, alternatif zorlama, kısa blend;
  - 2 klip bacak koruması tarafından.
- **Açık:**
  - 120 FPS / gerçek zaman devralma girişi;
  - devralma sonrası lateral durma;
  - mtf_jog;
  - baş yönü;
  - depar 90°;
  - devralmanın devralması (üçüncü istek şimdilik normal rotaya düşüyor);
  - Seviye 3 içeriği.

**14. Test ve yeniden açılış sayısı**
- 257 ölçüm koşusu + 14 ısınma koşusu.
- 8 editör yeniden açılışı (FPS kipleri ve temiz açılış).
- Süre ~4.3 saat (14:46–19:03).
- Teşhis tek bozuk/sağlam çiftle başladı (cc90 ve j38_c90r). Geniş regresyon (73 koşu) ve FPS kipleri (4 × 19) yalnız aday kararlı göründüğünde koşuldu.

---

## Neler denendi ve öğrenildi (sıra ile)

1. **Plan sahibi:** `Update_MotionMatching` girişinde tek dal; sınıf değişimi artık veritabanını değiştiremiyor.
2. **Yön kilidi koruması:** V2.28'in tek karelik düşüşü kilidi yenileyemiyor.
3. **Devralma klipleri:**
   - önce yalnız t_K'dan başlayan klipler → MM yanlış kareye girdi;
   - ön kısımlı (prefix) klipler + ayakların kaynakla birebir olması.
4. **MM girişi:**
   - trajectory her zaman "zaten dönmüş" kareyi seçiyordu;
   - giriş veritabanı (prefix pencereleri) + oynatma veritabanı (tam pencere) + arama freni.
5. **Asıl engel arama freniydi:** `SearchThrottleTime` (yönlendirme tutması) zorlanmış veritabanı geçişini, bir sınıf değişimi freni bir kareliğine bırakana kadar engelliyordu. Devralma latch'i boyunca fren 0 → geçiş istek karesinde.
6. **Taraf ayrımı:** sağ kesme, sol kesmenin "Opp" klibine giriyordu → 8 taraflı veritabanı.
7. **Karışan eğri:** oynatma veritabanı seçimi karışan `SHM239_Tgt` eğrisini okuyordu → kilitli hedef `TkTgt`.
8. **Dış etki** snapshot'ın başına taşındı; aksi halde klip yazımı itmeyi siliyordu.

## Dosyalar
- `CHANGES_V239.md`: kurulumlar, düğmeler, geri dönüş.
- `data/tables_reg.md`: 30 FPS o / tk, kontrol aşamaları, beden hizası, dış etki, FPS kipleri.
- `code/`: üreteç `gen239_tk.py`, kurulumlar, araçlar (`tk239.py`, `tables239.py`, `verify239.py`).
- `skills/`: güncellenen `sphirus-motion-synthesis`, `sphirus-balance-recovery`, `sphirus-human-motion-engine`, `sphirus-safe-unreal-iteration`.
- `vid/`: 30 FPS sabit adımlı, normal hızda, kesilmemiş çekimler. V2.38 ve V2.39 aday; sabit yan, çapraz ve oyun kamerası.

## Kabul
- **Teknik:**
  - Sahiplik kökü ve dış etki ayrımı: **PASS** (30 FPS).
  - Devralma: **PARTIAL** (30 / 20 FPS çoğu zincirde iyi; 120 FPS ve gerçek zamanda FAIL).
  - Depar: **NOT_TESTED**.
  - Baş: **FAIL**.
- **Görsel ve oyun hissi:** gerçek zamanlı videoyu oynatıp izleyemiyorum. Zaman damgalı kareleri ve verileri gördüm; fren duruşu ve yön değişimi görünüyor. Akıcılık ve doğallık senin kabulün.
- **Üretim kararı:** devralma üretime alınmadı.
