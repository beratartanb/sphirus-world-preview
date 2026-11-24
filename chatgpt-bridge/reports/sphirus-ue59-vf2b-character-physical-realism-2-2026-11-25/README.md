# Sphirus World — Character Physical Realism 2.0, devam geçişi (2026-11-25)

**Durum: KISMİ — net kazanç yok.** Bu geçişte ana karaktere **kalıcı bir fizik katmanı eklenmedi.** Saç fiziği oyuncuya bağlandı, ölçüldü ve görünümü bozduğu için **geri alındı**. Kıyafetin durağan dökümü Blender kumaş simülasyonuyla üretildi (karakter raporu); oyun içinde kumaş hareket etmiyor. GASP, `ABP_Sph_GASP`, `AC_Sph_Motion`, veritabanları ve klipler değişmedi.

## 1. Saç fiziği — aday H6 (bağlandı → reddedildi → geri alındı)
Önceki geçişin H5 adayı "çok sert, hareket belli değil" olarak kalmıştı. H6: aynı kök neden düzeltmesi (`GravityPreloading 1.0`, proje kopyasında) + daha yumuşak ayar: bükülme sertliği 0,6 → 0,4, sönüm 0,2 → 0,15, hız aktarımı 0,3 → 0,45 / açısal 0,6 → 0,75, çarpışma `PHYS_Face` (`data/hair_h6_cfg.txt`).

| Test | Sonuç |
|---|---|
| Kare hızı, aynı PIE oturumunda dönüşümlü (kapalı/açık/kapalı/açık) | 30,7 / 30,8 / 30,5 / 30,5 fps — **ölçülebilir maliyet yok** (`data/hair_h6_perf.txt`) |
| Zamanlanmış koşu–dur–dön kareleri | Biçim çökmedi; kontrolle benzer (`evidence/hair_h6_ab.jpg`). Not: bu dizide karakterin gerçekten yer değiştirip değiştirmediğini karelerden doğrulayamadım; kanıt değeri sınırlı |
| **Ardışık ışınlanma (sarsıntı) sonrası yüz kareleri, üç durum** | **Başarısız.** Fizik açıkken (çarpışmalı ve çarpışma hacmi kaldırılmış halde) perçem alnın ortasından burna doğru sarkıyor, saç hacmini kaybediyor ve 15 sn sonra da geri dönmüyor. Fizik kapalıyken saç taranmış biçimde ve iki göz görünür (`evidence/hair_variants.jpg`: sol = fizik açık + çarpışma, orta = kapalı, sağ = açık, çarpışmasız) |

**Karar:** "yüzü kapatmadan" koşulunu sağlamadığı için `BP_HybridA_Player` → `HairMain2` simülasyon metni, bağlamadan önce alınan kopyadan **birebir** geri yüklendi (betik metin eşitliğini doğruladı), fizik varlığı ataması kaldırıldı. Yeniden açılışta: `bEnableSimulation=False`.

**Öğrenilen:** sorun yalnız parametre değil. Çarpışma hacmini kaldırmak sonucu değiştirmedi; yani teller çarpışmaya takılmıyor, kılavuz tellerin dinlenme biçimi sarsıntıdan sonra korunmuyor (173 kılavuz, 68.523 tel). Güvenli alternatifler (denenmedi): yalnız uçları serbest bırakan kök-ağırlıklı sertlik eğrisi; ışınlanma/büyük ivmede simülasyonu sıfırlayan bir koruma; ya da simülasyon yerine kemik tabanlı hafif ikincil hareket.

## 2. Kıyafet fiziği
- **Durağan döküm (yapıldı):** üst giysinin serbest bölümü Blender'da 45 karelik kumaş simülasyonuyla oturtuldu ve ağa işlendi (karakter raporu §2.1).
- **Oyun içi simülasyon (YAPILMADI):** hiçbir giyside Chaos Cloth varlığı yok (`mesh_clothing_assets = 0`). Bu Python yüzeyinden kumaş varlığı oluşturma yolunu bu geçişte denemedim. Giysi bileşenleri bedeni lider poz olarak izliyor; kendi animasyon grafiği olmadığı için AnimDynamics eklemek bileşen kurulumunu değiştirmeyi gerektiriyor — ayrı, dikkatli bir iş.
- Kemer/aksesuar gecikmesi: "Home" kıyafetinde kemer zaten kapalı; iş yapılmadı.

## 3. Önceki raporun açık maddeleri
| Madde | Durum |
|---|---|
| Test B (giyilebilir aksesuar) | Önceki geçişte yapıldı, kemer alt adımı başarısız kaldı; bu geçişte **tekrar ele alınmadı** |
| Omuz/kalça QA uyarıları (test mankeni) | Önceki geçişte giderilmişti; ana karakterde doğrulama **yapılmadı** |
| Ana karakter 14 durumluk deformasyon taraması | **Yapılmadı** |
| Çevre teması (masa/kapı/duvar) | **Yapılmadı** |

## 4. Video
Zamana bağlı sorunlar için gerçek zamanlı video istenmişti. Yeni bir kaydedici yazdım (`scripts/rec_motion.py`, `rec.sh`) ama güvenilir hale getiremedim: yüksek çözünürlüklü çekim kare başına ~1 sn sürdü, hızlı çekimde ise girdi karaktere ulaşmadı (hız 0 okundu). **Bu geçişte video kanıtı yok**; saç kararı durağan karelere ve aynı oturum karşılaştırmasına dayanıyor. Projedeki eski video hattı (`vc59.sh`) kullanıcı kayıt dosyasını geçici olarak taşıdığı için kullanmadım.

## 5. Kabul ölçütü
"Yeni fizik katmanı karakteri daha kötü göstermemeli": sağlandı, çünkü kötüleştiren katman kaldırıldı. "İnandırıcı saç ve kıyafet fiziği": **sağlanmadı.**

## 6. Geri alma
Saç için yapılacak bir şey yok (zaten önceki halinde). İlgili manifestler: `vf2_wirechar011507` (bağlama), `vf2_whairoff020048` (geri kapatma).
