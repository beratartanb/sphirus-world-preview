# Sphirus World Art Direction & Environment Identity Pass (XR3): rapor

İzole, bellek içi deneme; hiçbir paket kaydedilmedi. Tarih: 2026-10-31 / 2026-11-01. UE 5.8.1, `L_GR_SphirusHouse`, gerçek oyuncu kamerası.

Temel: XR2 x8 dolaşım iskeleti (dünya sınırı, iki rota, odalar). Dilim: A rotası, ev → iskele → kaya sekisi → dere ağzı → karşı kıyı açıklığı.

## Kısa sonuç: Sphirus mu, deneme sahnesi mi?

**Henüz Sphirus değil.** Üç iterasyon (i1, i2, i3) sonunda dürüst değerlendirme:

| Alan | Durum | Kanıt |
|---|---|---|
| Görsel dil belgesi | **Yapıldı** | `IDENTITY_SPHIRUS.md`: tek cümle, üç okuma, palet, oluşum mantığı, yaşanmışlık izleri, bölge kimlikleri |
| Varlık kütüphanesi ölçüldü | **Yapıldı, sınırlayıcı** | 503 mesh ve 20 materyal bellekten; 25 gruplu pano gerçek oyun ışığında çekildi. Bölüm 2: kütüphane kimliği taşımıyor |
| Tek iklim (materyal dili) | **PARTIAL** | Landscape, eğrelti, çam, köknar, genç çam MI'leri proje sahipli kopyalarda soğutuldu; 127 XR2 kaya/gövde aktörü dinamik MI ile gri-yeşil tona çekildi. Kaya sekisinde fark okunuyor; uzak orman kanopisi hâlâ paket paleti |
| Kaya ailesi değişimi | **PARTIAL (i3)** | Turuncu CliffRock yerine Environment_Set Big_Rock (soğuk gri, Nanite değil). Mineral kimlik düzeldi; ama kayalar hâlâ "konmuş" okunuyor: gömülme yetersiz, toprak teması ve yosun eteği yok |
| Üç yerin kompozisyonu | P1 PASS, P2 PARTIAL, P3 FAIL | Bölüm 3 |
| Yaşanmışlık izleri | **PARTIAL** | Sandal, ip, dal yığını, el arabası; i1'deki lamba (abajur gibi okundu) çıkarıldı. Taş dizisi (tekinsiz fısıltı) yerleştirildi ama hiçbir karar noktasından okunmuyor |
| Delta tier (polish gate) | **Tier 2** | Kaya sekisinde Tier 3 (siluet ve malzeme değişti), açıklıkta Tier 1, iskelede Tier 2; bölge tier'ı ±90°'lerle 2'ye kapanıyor |
| Kesintisiz yürüyüş | **Bölüm 6** | i2 yürüyüşü gerçek zamanlı editörde 3 FPS'ye düştü ve geçersiz; i3 yürüyüşü sabit adımlı editörde yeniden alındı |
| Geri alma | **PASS** | Yükseklik sha1 aynı, foliage 57/8305 aynı, aktörler 768 aynı, 9 MI parametresi geri yazıldı, XR2/XR3 aktörü 0. Harita diskte değişmedi (`70dd481a…`) |

Başarı sorusunun cevabı: kaya sekisi karesi artık "bir orman paketinin demosu" gibi değil; ama dilim bir bütün olarak hâlâ öyle. Nedeni bölüm 2 ve 7'de.

## 1. Görsel dil (özet; tam metin `IDENTITY_SPHIRUS.md`)

**Tek cümle:** eski bir ormanın içine sığınmış, hâlâ yaşanan bir ev; orman onu kabul etmiş, ama ormanın belleği evden eski ve sessizce kıpırdıyor.

- Üç duygu katmanı: sığınak → zaman → fısıltı düzeyinde tekinsizlik. Fantastik nesne yok; tekinsizlik **düzen** olarak görünür (fazla düzenli taş dizisi, bir noktadan kaçar gibi büyüyen ağaçlar).
- Palet: serin, nemli yeşil-gri; kanopi koyu mavi-yeşil ve mat; kaya soğuk gri, dipleri koyu ve yosunlu; toprak koyu kahve-gri; ev ahşabı yalnız kullanılan yerlerde sıcak.
- Oluşum mantığı: kaya yalnız şev ve mahmuz ucunda, ana kaya gibi; eğrelti yalnız gölgede; çalı yalnız kenarlarda; yosun kuzey yüzlerde ve suya yakın; devrikler aynı yöne yatmış.
- Bu dünya ne değil: orman demosu, asset vitrini, turuncu-teal postkart, göl manzarası, terk edilmiş ev.

## 2. Varlık kütüphanesi: kanıtla sınırlar

Pano (`board/board_sheet_1..3.jpg`, kırpmalar `board/crop_*.jpg`): her grup oyun ışığında, aynı gün ışığında, oyuncu kamerasıyla.

| Aile | Elimizde | Pano bulgusu | Karar |
|---|---|---|---|
| Kanopi | PineForestPack PineTree01/03/05 (üretimde), 02/04/06/07; Fishermans Fir_Tree_01..08 (üretimde 03); Calysto Black_Spruce_01..05 | Çamlar kabul edilebilir siluet, iğne rengi sıcak-sarımsı; köknarlar açık sarı-yeşil ve parlak, serin paletle en çok çatışan tür; kara ladin en koyu ve en "kuzey" siluet, ama 26–62 bin üçgen ve kendi gövde materyali | Çam ailesi omurga; köknar kanopiden çıkarılır (dilimde 3 adet çıkarıldı, çamla değiştirildi); ladin yalnız koyu koru vurgusu (dilimde 8 adet) |
| Genç büyüme | Pine_Juvenile (prod), Young_Black_Spruce_01/02 (prod), SonoSapling, Xtree | Juvenile açık sarı-yeşil; genç ladin uyumlu | Juvenile MI soğutuldu |
| Çalı | Fishermans Bush_02/03/06 (prod), PF Bush/BushB/SalixElag, Calysto Bog_Laurel | Bush_02/03 geniş yapraklı ve açık; SalixElag en serin; Bog Laurel pembe çiçekli (reddedildi) | Dilimde çalı kompozisyonu değişmedi (sonraki tur) |
| Yer örtüsü | PF eğreltiler (prod), GroundCover, Calysto Bunchberry/Bluejoint/Sweetgrass/Fireweed | Eğreltiler doygun; Bunchberry tek uyumlu alçak örtü; Fireweed pembe (reddedildi) | Eğrelti MI'leri soğutuldu; derin gölgede çim halısı %55 inceltildi |
| Kaya | PF PineStone/GroundRock (prod), PF CliffRock/PineCliff (XR2), Environment_Set Big/Middle_Rock, Oak Boulder, Calysto Rock | CliffRock ve PineCliff sıcak zeytin-kahve, sahte yosun örtülü; Environment_Set Big_Rock soğuk gri ve kristal yüzeyli; Oak Boulder düz ve küçük | i2/i3: dilimdeki 6 CliffRock gizlenip Big_Rock ailesiyle değiştirildi (çarpışma XR2 aktörlerinde kaldı) |
| Ölü ahşap | PF FallenTree/DeadTrunk (XR2), Calysto Fallen_Log, Dead_Tree_01..03 | PF gövdeler soyuk ve açık; Calysto Dead_Tree dikili ölü için uygun | 3 dikili ölü ağaç eklendi; devrikler koyultuldu |
| Yaşanmışlık | Fishermans lamba, tabela, el arabası, tuzak, dal yığını, ip, sandal, iskele, kulübe | Sandal ve ip iyi; lamba 1,6 m'lik abajurlu ev lambası (iskelede yanlış okundu, çıkarıldı); tabela ve tuzak küçük ve okunmaz | Sandal + ip + dal yığını + el arabası |

**Asıl sınır:** üç paketin (PineForestPack, Fishermans_Cabin, Calysto) renk ve parlaklık dilleri farklı ve bu fark en çok **kanopi** ve **kaya** ailelerinde görünüyor. Materyal parametresiyle (doygunluk, tint) yakınlaştırılabiliyor ama birleşmiyor: iğne yaprak dokuları ve kaya dokuları farklı "iklimde" fotoğraflanmış. Tek kimlik için ya kanopi tek pakete indirgenmeli (PineForestPack çam serisi + Calysto ladin, köknar tamamen dışarı) ya da bir kaya/toprak doku seti proje sahipli olarak yeniden boyanmalı. Bunu kanıtlamadan "asset yeterli" diyemem; bu tur kanıtı: pano ve bölüm 3'teki karşılaştırmalar.

## 3. Üç yerin kompozisyonu (kil + oyuncu kamerası)

Karşılaştırmalar `compare/`: `id_P*_clay.jpg` (ÖNCE/i1), `id_P*_lit.jpg` (ÖNCE/i1), `i2_P*_lit.jpg` (ÖNCE/i2), `i3_P*_lit.jpg` (ÖNCE/i2/i3).

**P1 İskele (sandal).** Birinci okuma sandal + su, ikinci okuma ön patika, arka plan karşı kıyı duvarı. Kilde ve ışıklıda doğru okunuyor; verandadan bakışta sandal görüş hattının ortasında. i2'de gri kaya ailesi arka planda; i3'te kayalar daha gömülü ve küçük. **PASS (kompozisyon)**; ama ışıklı karede ön plan eğrelti ve yer örtüsü hâlâ doygun ve kırmızımsı döküntü paket karışımı gösteriyor.

**P2 Kaya sekisi.** Birinci okuma kaya duvarı, ikinci okuma dar raf, arka plan su. i1'de CliffRock'un turuncu-kahve kütlesi ve "sol 90°" karesindeki çıplak zeytin yüzey sahneyi bozuyordu. i2'de gri Big_Rock ailesi siluet ve mineral kimliği değiştirdi (Tier 3); fakat kayalar yüzeye konmuş gibi ve ölçek büyüktü (bir kare kamerayı kapadı). i3'te daha gömülü ve küçük; "entry" karesinde kaya duvarı ve raf okunuyor. **PARTIAL:** kaya diplerinde toprak teması, yosun eteği ve eğrelti yok; kayanın parlak kristal dokusu nemli iklimle çatışıyor.

**P3 Karşı kıyı açıklığı.** Birinci okuma suyun üstünde ev (sığınak) — bu geri bakış XR2'den beri çalışıyor. Ama açıklığın kendisi: "arrive" karesinde ışık hüzmeleri var, ama yer örtüsü düz ve tekdüze; "back" karesinde çıplak yamaç. i1 bog laurel pembe çiçek ekledi (reddedildi); i2 yosun yastıkları neon yeşil parladı (Calysto MossPatch, reddedildi); i3 bunchberry ile sakinleşti ama boş kaldı. Taş dizisi hiçbir karede okunmuyor. **FAIL:** açıklığın kimliği yok; nedeni dekor değil, kütle ve zemin: arkadaki yamaç düz bir şev, meşe gövdesi görüş hattında değil.

## 4. Uygulanan dört katman (i3)

1. **Tek iklim:** 9 proje sahipli MI bellek içinde: landscape orman/çim/kaya/toprak renk ofsetleri soğutuldu ve makro kontrast artırıldı; eğrelti (Long/Wild) doygunluk 0,62→0,46 ve parlaklık 0,57→0,40; çam iğnesi (01/03/05) tint soğuk gri-yeşil; genç çam ve köknar yaprağı soğutuldu; yer kayası (GroundRock03) gri tona. 127 XR2 kaya ve gövde aktörüne dinamik MI (gri tint, gri-yeşil yosun, parlaklık düşük).
2. **Yer kimliği:** dilimdeki 6 sınır kayası gizlenip Environment_Set Big_Rock ailesiyle (ölçek 1,1–1,7, %38 gömülü) ve etek kayalarıyla (Middle_Rock) değiştirildi; dere ağzında 4 + kaya sekisi arkasında 4 kara ladin; 3 dikili ölü ağaç; 12 yosun yaması kayaların kuzey yanında; sedge yalnız iskele batı cebi ve dere ağzında; 10 döküntü yaması koru altında.
3. **Yaşanmışlık:** sandal (XR2) + lastikli ip + dal yığını iskelede; el arabası ev önünde; 7 taşlık düzenli dizi açıklıkta.
4. **Sessiz zemin:** derin gölgede 4 çim/örtü tipinden 121 instance çıkarıldı; dilimdeki 3 köknar çamla değiştirildi.

Spawn sayıları ve foliage farkları: `data/id_i3.json`, `data/id_apply_i3.json`.

## 5. Yöntem

- Varlık panosu: editör aktörleri olarak harita dışında bir plakaya dizildi (x −200 m, y +200 m, z +60 m), oyuncu kamerasıyla çekildi, sonra 98 aktör yok edildi. Pano aktörleri hiçbir zaman harita içeriğine girmedi.
- Materyal değişiklikleri yalnız `/Game/GraceRanger/...` altındaki proje sahipli MI'lerde; satıcı MI'leri değişmedi. Spawn edilen aktörlerde dinamik MI kullanıldı. Her değişiklik yedeklendi ve restore'da geri yazıldı.
- Kil: `viewmode lightingonly` + nötr ışık; ışıklı: üretim ışığı. Aynı pawn konumu ve kamera açısı.
- Gated runner, tek kilit (`xr3`), map manifesti, PIE sırasında yazma yok.

## 6. Hareketli kamera ve performans

- **i2 yürüyüşü (geçersiz):** editör bu turda yeniden başlatılmıştı ve sabit adım olmadan açıldı; MediaCapture ile 3 FPS'ye düştü (323 kare / 107 s). Video `video/XR3_routeA_i2_identity_part1.avi` 10,8 s'lik hızlandırılmış bir özet; gerçek hız değildir, yalnız bakılabilir.
- **i3 yürüyüşü:** editör `-UseFixedTimeStep -FPS=30` ile yeniden açıldı; ısınma yürüyüşü + kayıtlı yürüyüş + CSV. Sonuç bölüm 6.1.

### 6.1 i3 yürüyüş ve performans

- `video/XR3_routeA_i3_identity_part1..3.avi`: 107 s gerçek hız (sabit adım 30 FPS, ikide bir kare, 15 FPS oynatma), 3221 kare, ev → iskele → kaya sekisi → dere ağzı → karşı kıyı. Yürüyüş rota çizgisini izleyen sürücüyle (görüntüleme amaçlı). **Videoyu gerçek zamanlı izlemedim**; t=30/60/90 s karelerine baktım.
- Kare gözlemleri: t≈60 s dere ağzında ladin korusu ve ışık hüzmesi okunuyor, ama ön plan eğrelti ve kırmızı döküntü hâlâ paket karışımı; t≈90 s karşı kıyı tırmanışında sarmaşıklı çam gövdeleri ve seyreltilmiş zemin sakin, soğuk tonda; aynı karede sağ alt köşede gri etek kayası "konmuş" okunuyor (bölüm 7, madde 2).

| Koşu (A rotası, ışıklı, pass B) | Kare p50/p95 ms | Oyun iş parçacığı | GPU | VRAM MB | Instance |
|---|---|---|---|---|---|
| x8 (XR2, giydirme dahil) | 39,4 / 52,7 | 17,1 / 20,2 | 37,7 / 50,5 | 7046 | 9788 |
| i3 (kimlik) | 37,6 / 52,3 | 15,9 / 19,3 | 36,4 / 50,6 | 6668 | 9732 |

Fark ölçüm gürültüsü içinde. 121 instance çıkarıldı, 72 aktör eklendi (8 ladin 26–62 bin üçgen; Nanite dışı Big_Rock 6 adet). VRAM düşüşü yeni editör oturumunun kaynak durumundan; iddia edilmiyor.

## 7. Neden hâlâ "deneme sahnesi" ve sırada ne var

Kök neden sırası (polish hiyerarşisi):
1. **Kanopi paleti.** Uzak ve orta katmanda köknar ve çam karışımı; iğne dokuları iki ayrı iklimden. MI tint'i yetmiyor. Karar gerekli: kanopi tek aileye (çam + ladin) indirgenir, köknar yalnız genç büyüme olarak kalır. Bu bütün haritada 808 köknar instance'ı etkiler; dilimde yalnız 3'ü vardı.
2. **Kaya-toprak teması.** Big_Rock ailesi doğru renk ama "konmuş". Gerekli: her kaya dibinde toprak yığını (landscape yükseklik yaması), yosun eteği ve eğrelti; kaya üstü kuru ve açık. Bu bir yerleşim işi değil, arazi+materyal işi.
3. **Açıklık kütlesi.** P3'ün arkası düz şev; meşe görüş hattı dışında. Gerekli: meşeyi girişe taşımak, arkaya kademeli kaya-ağaç kütlesi, zemin için yosun/ot mozaiği (neon olmayan).
4. **Yer örtüsü doygunluğu.** Eğrelti ve kırmızı döküntü (DeadLeaves02 broadleaf) çam ormanında yanlış; döküntü iğne yaprak olmalı (FallenNeedle MI var, mesh yok).
5. **Işık.** Üretim ışığı hüzmeleri açıklıkta güzel ama kaya sekisinde düz. Sinematik öneri XR2'de (TRIAL2) var; bu tur ışık değiştirilmedi.

Sonraki tur için önerim: önce 1 ve 2 (kanopi kararı + kaya teması), sonra 3; dekor ekleme yok.

## 8. Güvenlik ve geri alma

- Sıra: x8 uygula → giydir → i1 → geri al → i2 → geri al → i3 → geri al → x8 geri al → yeniden ölçüm.
- Doğrulama: yükseklik sha1 `207f04e4…` aynı; foliage 57 bileşen / 8305 instance, 0 fark; aktörler 768, etiket/sınıf/konum/gizlilik aynı; XR2/XR3 aktörü 0; 9 MI'nin parametreleri yedekten geri yazıldı, dosyaları diskte 2026-09-23 tarihli.
- Harita bellekte "dirty" ama içerik orijinal. **Editörü kapatırken "Don't Save" seçin.** Dirty listedeki 9 MI de kaydedilmemeli.
- Bu turda bir runner tuzağı bulundu ve belgelendi: iş içinde `SystemExit` runner'ı kilitliyor; editör iki kez yeniden başlatıldı.

## 9. Kalıcı kayıt

Bu turun hiçbir parçası kaydedilmeye hazır değil (Tier 2). Onay sorusu şu an "kaydet / kaydetme" değil, **yön** sorusu: kanopiyi tek aileye indirgeme kararı ve kaya teması için arazi yamasına izin. Bunlar onaylanırsa bir sonraki tur aynı dilimde i4 olarak koşar; kabul Tier ≥ 3 ve üç yerin ±90° kareleriyle olur.

## Dosyalar

| Klasör | İçerik |
|---|---|
| `IDENTITY_SPHIRUS.md` | görsel dil belgesi |
| `board/` | varlık panosu sayfaları ve kırpmaları |
| `compare/` | P1/P2/P3 önce/sonra (kil, ışıklı; i1, i2, i3) |
| `stills/` | ham oyuncu kamerası kareleri |
| `video/` | i2 (geçersiz, özet) ve i3 yürüyüşleri |
| `data/` | tasarım ve uygulama/geri alma kayıtları, materyal yedekleri, kütüphane ölçümü, performans |
| `tools/` | `xr3_design.py`, `xr3_apply.py` (MI + DMI + gizleme + geri alma), `xr3_board_spawn.py`, `probe_library.py`, `xr3_chain.sh` |
