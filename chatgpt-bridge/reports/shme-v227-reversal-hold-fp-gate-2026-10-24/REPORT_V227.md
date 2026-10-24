# SPHIRUS — SHME V2.27: yazılı geri dönüş klibi sonuna kadar tutulur, FootPlacement klip içinde kapalı (2026-10-24)

Taban: V2.26 üretimi (bridge `9634d8d`). Kapsam: V2.26'nın bıraktığı iki açık kol — (a) SHM226 geri dönüş klibi pozdayken `SHM_FootPlaceOff` (düz zemin), (b) ABP yön değiştirme bölümünü / geri dönüş veritabanını klip sonuna bağlamak — aday olarak kurulup A/B, FPS taraması (20/30/60/120), gerçek zaman + soğuk başlatma ve temiz yeniden açılışta doğrulandı. Bütün koşular etkin durum kaydıyla (`_state.json`) alındı; "üretim" = kaydedilmiş durum, bayraksız. **Sonuç: mekanizmalar doğrulandı, üretime alınmadı (düğmeler 0, kurulu-kapalı); engel içerik tarafında (32 kutulu klip ailesinin ph3 60/120 FPS kapsül uyumsuzluğu).**

## 0. Üç soruya kısa cevap
1. **Tasarlanan ayak yolu oyunda korunuyor mu?** Mekanizma olarak evet: tutma ile klip 1,57–1,60 s (F_B) / 1,43–1,48 s (B_F) oynuyor (uzunluk 1,97 / 1,77; bitime 0,29 s kala döngüye), poz terimi kapsül çerçevesinde −3…−7 cm. Ama dünya çerçevesinde basılı ayak, kapsül klibin tasarım tablosundan saptığı kadar kayıyor; bu sapma MM'in giriş anında seçtiği faz kutusuna bağlı ve 60/120 FPS ph3'te (P4 kutusu) 35–42 cm (üretim 15–27). FP kapalı bunu gizlemiyor, FP açık da (rhH 41) gizlemiyor; yalnız 32 kutu (rv32) da 41–43 → sorun klip içeriği/giriş hızı, ABP değil.
2. **Çıkış sıçraması (klip → döngü) gitti mi?** Evet: tutma ile 9–12 cm → 0,5–2,7 cm (bütün FPS'lerde, exit227 çıkış penceresi). İstisna: B_F P26/P29 kutularından döngü fazı 0,90'a tek kare 21 cm (30 FPS ph3/sw_ph2, FP kapalı varyantta; FP açık varyantta 1,8).
3. **Üretime alındı mı?** Hayır. Karar kuralı "hiçbir senaryo hiçbir FPS'te üretimden belirgin kötü olmasın" idi; ph3 60 FPS 34,8/40,9 (üretim 15,4) ve 120 FPS 36,2/42,3 (üretim 26,7) bunu bozuyor; yalnız-tutma varyantında ayrıca dbl 20 FPS 37,3 (üretim 32,5). Üretim V2.26 ile aynı kaldı; V2.27 kodu ABP'de kurulu ama kapalı (`SHM227_RevHold`/`SHM227_FPOff` 0), temiz yeniden açılışta doğrulandı (§5).

## 1. Mekanizma (ABP_GR_MotionMatchingBase, SHM_Snapshot + AnimGraph MM düğümü; grafik yaması, DSL yeniden derlemesi yok)
- **Saat eğrisi:** 64 `SHM226_JogRev_*` klibine `SHM226_Rev` = kalan klip saniyesi ([0,T]→[T,0]); klip ağırlığıyla 0'a karışır, döngülerde yok → `SHM227_Rev`.
- **Tutma (`SHM227_Hold`):** RevHold>0,5 & kalan>HoldExit (0,25 s) & önceki karenin ABP bölümü & HasIntent & ¬Dead & ¬revUp → `SHM_RedirectActive` ve kare sayacı koşuluna OR. `Update_MotionMatching`'in yön değiştirme tutuşu geri dönüş veritabanını klip bitimine 0,25 s kalana kadar tutar; sonra MM tutulan DB içinde eşleşen fazda döngüye geçer.
- **FP kapısı (`SHM_FootPlaceOff`):** FPOff>0,5 & klip pozda & |TerrainSlope|<FlatMax (6°) & salınım kaldırmaları<2 cm & bölüm açık. Yalnız düz zemin.
- **Arama kısıtı (`SHM227_Thr`):** klip pozdayken MM düğümü `SearchThrottleTime` = FMax(V2.21 kurtarma kısıtı, 2,5 s). Giriş karesi (köprü DB değişimi), çıkış (DB değişimi) ve yeniden başlatma yine arar.
- **Bölüm kimliği korumaları:** `SHM227_Restart` (bileşen `RedirectTime` azaldı = yeni bileşen bölümü → `cStart`'a OR, köprü karesi DB'yi yeniden rotalar); `SHM227_Dead` mandalı (bileşen yeniden başlayana kadar): klip başına yeniden giriş (kalan >0,05 s yükseldi) VEYA `SHM227_IntentEnd` (bileşen `RedirectEnd` 3 = yeni niyet, 4 = kayıp; 1 hizalı / 2 azami bekleme tutuşu korur).
- Düğmeler ABP değişkeni; 0 = üretim davranışı değişmez. Üretime alma `promote227.py` (Reversal226 DB'leri + RevHold/FPOff 1), geri alma `req/rollback227.py`, kapı `req/verify_fin227.py` (`ALL_OK`).

## 2. Beş geçişte ölçülen kök nedenler (her geçiş öncekine karşı ölçüldü)
| Geçiş | Belirti | Kök neden (iz) | Çözüm |
|---|---|---|---|
| a | çıkış sıçraması 9–12 cm | bileşen bölümü ~0,70 s'de biter → ABP DB'den çıkar → MM döngüye başka fazda | tutma (klip sonuna) |
| b | arka arkaya bölümlerde eski aile DB'si tutuldu | rdOn hiç düşmez → köprü karesi yok | `RedirectTime` azalması = yeniden başlatma → cStart |
| c | j24_dbl 115–118 cm kilit | gövde durmuşken MM tutulan DB içinde klip başına yeniden girer, kalan süre 1,9 s'ye zıplar → tutma bırakmaz | klip ÖRNEĞİNE bağlı tutma (yeniden giriş mandalı) |
| d | 60 FPS ph0 68 cm | MM her kare arar; girişten 1 kare sonra karşı faz klibini seçti (P14 ct 0,10 → P30 ct 0,03; komşu 32 kutu başta neredeyse aynı) | klip içinde arama kısıtı |
| d→e | 60 FPS'te kısıt işe yaramadı | Thr koşulu ABP'nin KENDİ bölüm bayrağını okudu → 1 kare geç (giriş+2) | bileşen `RedirectActive` ile OR (giriş+1'den itibaren) → 60 FPS ph0 67,8 → 32,2 (üretim 32,4) |
| d→e | j24_dbl 100 cm | bileşen bölümü `RedirectEnd 3` (yeni niyet) ile bitti, kapsül ileri hızlanırken tutulan F_B klibi geriye koştu; c geçişi bunu belirti (yeniden seçim) üzerinden gizlemişti | yeni-niyet/kayıp bitişi → Dead → dbl 100,8 → 21,7 |

Kural: bir klip tutuşu (1) bileşenin bölüm kimliğine, (2) klip örneğine, (3) onu başlatan niyete bağlanır.

## 3. Sonuçlar — sabit 30 FPS (en kötü basılı ayak kayması cm; yükseklik-ölçütü | temas-başlangıçlı; `plant225` / `plant227`)
| Senaryo | Üretim V2.26 | rv32 (yalnız 32 kutu) | rh geçiş c | rh geçiş d | **rh geçiş e** | **rhH (yalnız tutma, FP açık)** |
|---|---|---|---|---|---|---|
| ph0 | 49,7 \| 49,7 | 25,1 \| 25,1 | 20,7 \| 13,8 | 17,9 \| 17,7 | 18,1 \| 17,8 | 15,1 \| 12,5 |
| ph3 | 16,6 \| 16,6 | 23,7 \| 23,7 | 14,0 \| 14,0 | 21,4 \| 14,7 | 21,5 \| 14,6 | 17,2 \| 9,1 |
| sw_ph0 | 16,7 \| 10,9 | 25,1 \| 25,1 | 12,2 \| 12,2 | 9,3 \| 9,3 | 9,4 \| 9,4 | 9,0 \| 11,3 |
| sw_ph2 | 31,2 \| 28,1 | 16,6 \| 16,6 | 32,4 \| 32,4 | 10,8 \| 9,8 | 21,5 \| 9,5 | 10,6 \| 10,6 |
| rel | 30,4 \| 30,4 | 13,9 \| 12,1 | 25,0 \| 14,4 | 22,6 \| 14,8 | 21,3 \| 13,2 | 12,1 \| 8,2 |
| dbl | 35,5 \| 5,2 | 33,7 \| 33,7 | 17,8 \| 17,2 | 100,8 \| 83,5 | 21,7 \| 17,7 | 16,2 \| 17,9 |
| ad_ph0 / m180w | 26,8 / — | klip seçilmez | klip seçilmez | — | klip seçilmez (N/A; pop'lar üretimle birebir aynı) | — |

Klip ömrü (`exitjump227`, geçiş e): F_B klipleri 1,57–1,60 s oynar, B_F 1,43–1,47 s; çıkış penceresi sıçraması ph0 1,8/2,7, ph3 1,9 (F_B), sw_ph0 2,7/1,6, sw_ph2 1,9 (F_B); B_F P26/P29 → döngü @0,90: 21,5 cm (tek kare, FP kapalı; FP açık rhH'de 1,8). rel: bırakmada klip 0,27 s sonra durma karışımına gider (17–18 cm; açık). dbl: yeni niyet karesinde tutma biter (0,50 s), Run_Start seçilir (12–13 cm başlangıç karışımı). Duruş (`posture226`): rv32 ile aynı, çökme yok. Pop'lar: m180w (291 m/s², 4) ve ad_ph0 (28, 3) üretimle aynı aşamalarda aynı değerler — adaydan bağımsız.

## 4. FPS taraması (en kötü kayma cm, yükseklik | temas-başlangıçlı)
Üretim = V2.26 kaydedilmiş durum (`v226s*`, dbl referansları bu turda `v227h60/h20_*_o`), rh = tam aday geçiş e (tutma + FP kapısı, `v227w*`), rhH = yalnız tutma (FP açık, `v227h*`). "—" = koşu yok. ✗ = üretimden belirgin kötü.

| FPS | Senaryo | Üretim | rh (tutma + FP kapısı) | rhH (yalnız tutma) | rv32 (yalnız 32 kutu, V2.26) |
|---|---|---|---|---|---|
| 20 | ph0 | 49,6 \| 49,6 | **9,6 \| 9,6** | **9,3 \| 6,3** | 11,8 |
| 20 | ph3 | 16,8 \| 13,3 | 11,5 \| 13,1 | 16,5 \| 18,1 | 15,8 |
| 20 | sw_ph2 | 25,3 \| 25,3 | **11,1 \| 11,1** | **8,3 \| 8,3** | 12,8 |
| 20 | ovl120 | 65,4 \| 24,4 | **11,1 \| 10,4** | **7,7 \| 7,7** | 11,9 |
| 20 | dbl | 32,5 \| 7,2 | 16,3 \| 15,9 | 37,3 \| 15,6 ✗ | — |
| 60 | ph0 | 32,4 \| 32,4 | 32,2 \| 16,7 | 26,7 \| 18,8 | 63,9 |
| 60 | ph3 | 15,4 \| 15,1 | 34,8 \| 34,8 ✗ | 40,9 \| 40,9 ✗ | 40,9 |
| 60 | sw_ph2 | 21,6 \| 21,6 | 21,4 \| 14,9 | **12,9 \| 12,9** | 28,1 |
| 60 | ovl120 | 23,4 \| 21,1 | 22,6 \| 22,6 | 27,4 \| 27,4 | 35,4 |
| 60 | dbl | 31,2 \| 27,8 | 30,7 \| 21,3 | 22,1 \| 19,1 | — |
| 120 | ph0 | 30,5 \| 30,5 | 25,5 \| 17,0 | 23,5 \| 19,5 | 37,2 |
| 120 | ph3 | 26,7 \| 17,7 | 36,2 \| 36,2 ✗ | 42,3 \| 42,3 ✗ | 42,8 |
| 120 | sw_ph2 | 51,6 \| 51,6 | **37,5 \| 12,5** | 35,6 \| 35,6 | 40,0 |
| 120 | ovl120 | 35,2 \| 24,7 | 29,5 \| 29,5 | 26,3 \| 25,9 | 33,5 |

Okuma: tam aday 20 FPS'te her senaryoda, 60/120'de ph0 ve sw_ph2'de üretimden iyi; **ph3 60/120 FPS'te 35–36 cm (üretim 15/27)**; yalnız-tutma orada 41–42, yalnız 32 kutu (rv32, tutmasız) 41–43 → bu kayma klip içeriğinin, tutmanın değil. `capterm` ayrışımı (w60 ph3): poz terimi düz (−3…−7 cm, tasarlanan ayak kapsül çerçevesinde gerçekleşiyor), **kapsül terimi** klip boyunca 26–37 cm'ye büyüyor: 60/120 FPS'te MM girişte başka faz kutusunu (P4; 30 FPS'te P21) seçiyor ve bu kutunun tasarım tablosu kapsülün o andaki hızıyla uyuşmuyor; FP kapalıyken fark dünya çerçevesinde basılı ayağa yansıyor. Kapsülün hız izi FPS'ten bağımsız (üretim ve aday aynı eğri); FPS'e bağlı olan MM'in giriş anındaki kutu seçimi. Çözüm ABP'de değil: giriş hızına göre tasarım tablosu (içerik) ya da kapsülün klibin tablosunu izlemesi.

## 5. Gerçek zaman, soğuk başlatma, temiz yeniden açılış, kanıt
- **Temiz yeniden açılış doğrulaması (`verify_fin227`, taze editör 22:23):** `SHM227_RevHold` 0, `SHM227_FPOff` 0, `HoldExit` 0,25, `FlatMax` 6, `ThrottleT` 2,5; 64 klipte `SHM226_Rev` eğrisi var; V2.26 üretim doğrulaması (`verify_prod226`: DB referansları V2.24 pivot, StepPrep/StepEdge/InspectZoom kapalı, sondalar var, SwingLiftMargin 6) temiz → `ALL_OK: true`. Kirli paket yok.
- **Üretim-modu kanıt (taze editör, 16 senaryo, sabit 30, bayraksız; `data/chain.out`, `state/`):** V2.26 nihai koşularıyla karşılaştırma — 14/16 senaryoda basılı kayma ve pop sayıları rakamı rakamına aynı (ph0 49,7; ph3 16,6; sw_ph0 16,7; rel 30,4; dbl 35,5; ad_ph0 26,8; m180w/j23_m180 291/292; r_cutrev 57; taps/s23_jstart 0; ter_drop_walk 260; ter_step2 190; map_r2 56). İki fark oturum düzeyinde iki-durumluluk: sw_ph2 26,1 (V2.26 nihai 31,2; V2.26'nın kendi t1 koşusu 26,1, bu turun yakalama koşusu yine 31,2) ve ins_ws 3 pop/43 (V2.26 nihai 1/40; V2.25–V2.26'nın beş koşusu 3/43). Sonuç: kurulu-kapalı V2.27 yamaları üretimi değiştirmiyor (düğme 0 → FootPlaceOff/Hold/Thr ifadeleri false, `SearchThrottleTime` = FMax(eski, 0) = eski). Hiçbir koşu `INVALID_STATE` değil.
- **Gerçek zaman (sabit adım yok), soğuk başlatma ilk koşu `j24_ph0` (ısınmasız):** ph0 52,1 cm (sabit 30: 49,7), sw_ph2 17,6, dbl 15,3, map_r2 ev–orman rotası 19,8 kare/s ortalama (5 pop, en kötü 128, montaj/klip; V2.26 ile aynı sınıf). Bu turda gerçek-zaman editörü çökmedi.
- **Yakalamalar (`vid/`, sabit 30 = gerçek hız, tam kare, kesintisiz):** üretim ve aday `rh` yan yana — tempolu S>W (yan + aday oyun kamerası), W>S>W (yan), çift geri dönüş (yan). Aday klipleri `qa_pie` aday modunda (etkin durum kayıtlı), üretim klipleri bayraksız.

## 6. Karar
**Üretime alınmadı (PROMO 0).** V2.27 kodu ABP'de kurulu ve kapalı; üretim DB'leri V2.24 pivot DB'leri, `SHM227_RevHold`/`SHM227_FPOff` 0; temiz yeniden açılışta `verify_fin227` ile doğrulandı (§5). Gerekçe: FPS sağlamlığı kabul şartı; ph3 60/120 FPS'te hem tam aday hem yalnız-tutma üretimden 2–2,7 kat kötü, ve bu kayma 32 kutulu klip ailesinin kendisinde var (rv32 aynı). Mekanizma kazanımları (çıkış sıçraması 9–12 → 1–3 cm, dbl kilidi, 60 FPS yeniden seçim, yeni-niyet bırakması) klipler düzeltildiğinde tek düğmeyle (`promote227.py`) açılabilir. Kullanıcı kabulü varsayılmadı.

## 7. Açık liste
- **Giriş hızına bağlı kapsül tablosu (içerik):** 32 kutulu kliplerin tasarım tablosu kapsülün giriş anındaki hızına göre değil, istek anındaki döngü hızına göre; MM'in seçtiği kutu FPS'e göre değişiyor (P21 vs P4) ve bazı kutularda kapsül terimi 26–37 cm. Çözüm: kutu başına giriş hızına uygun tablo ya da kapsülün klip tablosunu izlemesi (kök hareket / kapsül sürücüsü).
- B_F ailesinin P26/P29 kutularından döngü fazı 0,90'a tek kare 21 cm (FP kapalı varyant): klip sonu ↔ döngü faz eşleşmesi; aile başına HoldExit veya klip sonunun döngü fazına tasarımı.
- Geri dönüş içinde bırakma (j24_rel): klip 0,27 s'de durma karışımına gider, 17–18 cm; durma klibinin basılı ayaktan başlatılması gerekir.
- dbl: yeni niyet sonrası Run_Start karışımı 12–13 cm; yalnız-tutma 20 FPS'te 37 cm (üretim 32).
- ad_ph0 / m180w: SHM226 klibi seçilmiyor (çapraz / yürüyüş 180 ayrı aile) — N/A, mükemmel değil.
- Gerçek-zaman editörü PIE kapanışında `GameViewport.IsUnique()` iddiasıyla çöktü (d geçişi taramasında; V2.26'daki gibi); sürücü yeniden açtı, sonraki ph3 rt koşusu klip seçmedi (geçersiz sayıldı). Nihai gerçek-zaman zinciri (§5) çökmeden tamamlandı; kök neden açık.

## 8. Test aracı olayları (dürüstlük)
- Kopyalanan A/B sürücüsü eski etiket önekini taşıdı → ilk 3 koşu `v226t1_*` olarak yazıldı (bir V2.26 kanıt dosyası üzerine yazıldı); döngü durduruldu, etiket düzeltildi, dosyalar `v227t1_*` olarak yeniden adlandırıldı.
- PowerShell süreç öldürme deseni kendi kabuğumla eşleşti (iki kabuk öldü) → desenlerde `CimInstance` dışlanır, kendi komut satırı deseni kullanılmaz.
- Bayrak uygulama ile geri alma arasında öldürülen koşu editör CDO'sunda aday değerleri bıraktı → o editörde üretim-modu koşu/doğrulama geçersiz; her koşunun `_state.json`'ı doğru, üretim doğrulaması taze editörde.
- 120 FPS sw_ph2 (d geçişi) koşusu izleme hatasıyla kayıt üretmedi; MEM_RESTART (43 GB) sonrası zenserver kurtarması 2036 s sürdü (editör LogInit'te takılı göründü), bekleyen iş kuyruğu ısınma PIE'si içinde sırayla çalıştı (`revert_quit` REFUSED: PIE running) → 20 FPS aşaması koşmadı; e geçişi taramasında tekrarlandı.
- `exitjump227` FPoff penceresi c+40 kare sonraki klibi kapsıyordu → c+15.
- 60/120 FPS taramalarında editör 39–43 GB'de otomatik yeniden başlatıldı (MEM_RESTART, 3 kez); sonuçlar etkilenmedi (her koşu kendi `_state.json`'ı ile).

## 9. Dosyalar
`code/` (kurucular a–e, sürücü, zincirler, ölçümler, üretime alma/geri alma/doğrulama), `data/` (tablolar `tables227b/c/d.txt`, zincir günlüğü, sondalar, verify çıktısı), `state/` (etkin durum kayıtları), `vid/` (medya: üretim vs aday yan yana), `CHANGES_V227.md`.
