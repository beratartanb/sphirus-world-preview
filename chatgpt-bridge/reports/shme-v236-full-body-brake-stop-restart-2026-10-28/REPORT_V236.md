# SPHIRUS — SHME V2.36: tam beden fren, duruş ve yeniden hareket (2026-10-28)

Bu sürüm V2.35 üretimi (Bridge 742af76) üzerine yapıldı. Proje Blueprint-only UE 5.8; git yok, geri dönüş manifest yedekleriyle (sha1 doğrulamalı).

**Ölçüm koşulları:**
- Sayıların hepsi sabit adımlı editörde, aynı girdiyle ölçüldü. Aksi yazılmadıkça 30 FPS.
- Kayma ölçütü: `contact231`, en kötü basılı top kayması (cm).
- Gövde ölçütleri: `stop236`, görünen mesh üzerinde.
- `o` = V2.36 üretimi. `pre236` = V2.36 gruplarının hepsi V2.35 değerinde (eski CP2 duruşu, üretim başlangıç DB'leri, V2.35 ters dönüşü, V2.31 yüklü aile).

Teknik PASS, görsel ve oyun hissi kabulü değildir. Görsel yargılarım iki kaynaktan:
- normal hızlı kayıtlardan çıkardığım zaman damgalı kare şeritleri:
  - son üretim: `sheets/fin_*`;
  - aday aşaması: `sheets/cap_*`. Bunlarda `o`, o andaki üretimdir, yani V2.35.
- oyun dışında, kaynak kliplerden çizdiğim çubuk figür şeritleri (`sheets/src_*`). Yalnız resimler yayımlandı; kare kare kemik verisi yayımlanmadı.

Videoyu gerçek zamanlı oynatıp izleyemedim; normal hızdaki ritmin ve oyun hissinin kabulü sizde. PS donanımında test yapılmadı.

**Üretimde (temiz açılışta VERIFY236 ALL_OK):**

| Grup | İçerik |
|---|---|
| `stop` | 24 bırakma evreli tempolu duruş ailesi. Fren ayağı sol/sağ; bütün beden; duruş, düz kalkışın başladığı duruşta biter. |
| `start` | Sol ve sağ ayakla düz tempolu kalkış. Üretim başlangıç DB'lerinin kopyalarına eklendi. |
| `rev` | Tam beden ters dönüş freni. V2.35'in ayak planı aynen korundu. |
| `load` | Eforlu ters dönüşte iki ayakla bekleme kaldırıldı. |

**Reddedilen:** `resume` (durma sırasında yeniden basışa döngü ekleme): etkisi olmadı.

## 0. Doğrudan cevaplar

### 1. Sol/sağ destekli duruşta gerçekten hangi içerik üretildi?
Yeni bir duruş ailesi üretildi: `SHM236_JogStop_B{l|r}_P00..P23`, 24 klip. Etiketteki **B, fren ayağını** gösterir: bırakmadan sonra yere ilk basan ve yavaşlamayı karşılayan ayak. `P` ise bırakma anındaki adım evresidir.

Her klip kendi destek evresinden planlandı:
- **Giriş:** 0. kare, döngünün o evredeki pozu.
- **Kök:** oyunda ölçülen kapsül duruşu (300 → 0, sabit 410 cm/s², 0.73 s, 110 cm).
- **Fren ayağı:** döngünün kendi iniş mesafesine (31–39 cm) basar. Eski klipte bu 55–63 cm idi, yani fazla öne uzanıyordu.
- **Kalan mesafe uzunsa:** büyük bir adım yerine kısa bir ek adım atılır.
- **Arkada kalan ayak:** tabanının ön kısmına yuvarlanır, topuk kalkar.
- **Kapanış adımı:** yalnız gerekirse; alçak, en fazla 3–5 cm tepe.
- **Son duruş:** eski CP2 duruşunun son karesi. Düz kalkış bu duruştan başlıyor.

Tek temsilî sol ve sağ klip önce kaynakta değerlendirildi (aşama 1). Oyunda iki klip yetmedi: arama, girişten bir kare sonra diğer klibin 0. karesine geçti ve ayak 46 cm kaydı. Bu yüzden 24 evreye çıkıldı (bias −3). Ara adımlar bölüm 2'de.

### 2. Fren boyunca kollar, göğüs ve pelvis artık ne yapıyor?
Görünen bedendeki ölçümler (bölüm 3 tablosu):

| Ölçüt | V2.35 | V2.36 |
|---|---|---|
| Frende korunan kol salınımı (bırakmadan önceye oranla) | 0.67–1.13 | 0.35–0.55 |
| Bırakmadan 0.6 s sonra gövde eğimi | 4.8–11.4° | 0.3–1.0° |
| Duruştan sonra ayağın geri çekilmesi | 16.7–51.8 cm | 0.1–12.1 cm |
| Durduktan 0.6 s sonra açık duruş | 32.4 cm'ye kadar | ≤ 7.7 cm |

- **Kollar:** salınım genliği sönüyor; orta taşıma noktası açılıp kalçaya iniyor. Bu yaklaşık 0.95 s sürüyor, bir karede düşmüyor. Fren basışında küçük bir ileri atalet salınımı, duruşta tek bir sönen geri salınım var.
- **Göğüs ve baş:** göğüs 0.6 s içinde dikleşiyor, ani dikleşme yok. Duruşta 2.5°'lik bir "varış" öne eğilmesini boyun karşılıyor; baş düz kalıyor.
- **Pelvis:** yavaşladıkça yükseliyor; her fren basışında küçük bir sönümleme çökmesi var.
- **Kalan kusur:** pelvis çökmesi hâlâ 6–11 cm (V2.35'te 9–12). Yan kare şeridinde 5.6–5.9 s arasında dizler bükük görünüyor.
- **Ters dönüşte:** fren penceresinde kol genliği %25'e iniyor, dirsekler 18° açılıyor, kollarda 9° atalet salınımı var, boyun dengeliyor. Ancak eylem kısa (0.3–0.5 s). Görünen el, V2.35'e göre frende yalnız 4–7 cm daha aşağıda. Bu fark küçük; kare şeridinde zor seçiliyor.

### 3. Hangi gerçek hareket referansı incelendi ve ne değişti?
Ücretsiz Pexels videoları zaman damgalı kare dizilerine çevrilip kare kare incelendi. Başlık veya küçük resim incelenmiş sayılmadı; kayıt `notes236.md` §1.

| Video | Aralık | Ne için |
|---|---|---|
| `a-woman-getting-tired-of-running-4763889` | 3.6–7.5 s, 0.1 s adım | önden; tempolu koşudan yavaşlama ve durma |
| `woman-taking-a-rest-on-her-workout-5029482` | 5.8–9.0 s | önden; ayaktan tempoluya kalkış |
| `...after-jogging-3048882` | 5–11.4 s | arkadan 3/4; ağır çekim olduğu için yalnız poz |

**Sınırlama:** Normal hızda, yandan görülen bir kadının tempolu koşudan durduğu video bulunamadı. Ayak mesafeleri projenin kendi döngüsünden ve ölçülen kapsülden alındı. Videolardaki yorgunluk hareketleri (eller dizlerde) kullanılmadı.

Videolardan çıkarılan ve uygulanan tasarım:
- Duruş tek bir hamle değil, 2–3 kısalan adım.
- Eller yaklaşık 0.5 s içinde inip dirsekler açılıyor.
- Yavaşlarken göğüs yükseliyor, baş düz kalıyor.
- Kalkışta gövde ilk adımla öne giriyor, kollar taşımaya kalkıyor.

### 4. Duruş ve yeniden başlangıç birlikte çalışıyor mu?
Büyük ölçüde evet. Asıl sahip bir içerik boşluğuydu:
- Başlangıç yolu, yükü olmayan ayağın DB'sinde arama yapıyor.
- Sol ayağın DB'sinde (`PSD_SHM_JogStartS_L`) düz bir tempolu kalkış yoktu.
- Bu yüzden sol ayak boştayken her düz istek **TurnL045** ile oynuyordu: 63–92 cm sürtünme ("yanlış kalkış ailesi").

Yapılan:
- Sol ve sağ ayakla düz kalkış üretildi (`SHM236_JogStart_F_L/R`): gövde ilk adımdan önce öne giriyor, kollar artan salınımla taşımaya kalkıyor.
- Bu kalkışlar başlangıç DB'lerinin kopyalarına eklendi.
- Duruşlar, düz kalkışın başladığı duruşta bitiyor.

Sonuçlar (30 FPS, en kötü kayma):

| Senaryo | V2.35 | V2.36 |
|---|---|---|
| Durup tekrar ileri (`j36_stopr`) | 19.6 | 7.2 |
| Duruşun sonunda tekrar basış (`j36_rsl`) | 34.4 | 8.7 |
| Aday oturumunda, TurnL045 ile (`j34_chain1`) | 92.5 | 16–17 |

Açık kalanlar:
- **Yeni sol kalkışın kendi kayması** (`j36_wjs` 14.3, `j34_chain1` 17.1): kaynakta 11 cm basılı kayma var. Sağ vendor kalkıştan (6–7 cm) kötü, TurnL045'ten çok daha iyi.
- **Duruşun ortasında tekrar basış** (`j36_rsm`): eski duruşla da aynı yol 19.6 cm idi. V2.36'da 19.1–19.4 cm, son koşuda 38.4 cm.
  - Sahibi, hareket hâlindeyken ayaktan kalkış yoluna girmek. DB'ye döngü eklemek bunu değiştirmedi.
- **Durup yan/çapraz kalkış** (`j36_sside`): 20.5 cm (lateral sağ kalkış). Eski duruşla bu oturumda karşılaştırma koşusu yok.

### 5. Eforlu durumda görünen fark nedir?
`e29_load` zincirinin ikinci ters dönüşünde:
- İki ayakla bekleme **0.43 s'den 0.13 s'ye** indi (30 FPS); FPS modları bölüm 4'te. Yeni yüklü klip oynuyor (`SHM236L_LoadRev_F_B_P10`).
- Eforlu durum bir koreografi ve kapsül farkı olarak korunuyor, ağır çekim değil:
  - fren ayağı kısa basıyor;
  - diğer ayak durma noktasının ötesinde yakalıyor;
  - daha derin sönümleme;
  - itiş 150 cm/s², dinlenik hâlde 550/650.
- Bekleme kalktı; yeni yöne ilk adım yakalamadan hemen sonra geliyor.
- En kötü kayma 14.2 cm, ikisinde de aynı. Bu kayma değişmeyen V2.31 B_F klibinde.

### 6. V2.35 gerilemeleri hangi koşullarda kapandı?

**Kapandı (30 FPS, V2.36 / V2.35):**

| Senaryo | V2.35 | V2.36 |
|---|---|---|
| `j36_stop` | 11.7 | 5.9 |
| `j36_stopb` | 12.3 | 5.9 |
| `j36_stopr` | 19.6 | 7.2 |
| `j36_rsl` | 34.4 | 8.7 |
| `j30_slow` | 9.3 | 0.0 |
| `jback` | 13.4 | 0.0 |
| `e29_load` bekleme | 0.43 s | 0.13 s |

**Aynı kaldı:** `j35_rev` 8.0, `j35_rev2` 9.3, `j35_relstop` 8.6, `j30_rel_3200` 9.1, `e29_chain` 6.5, `s29_swl12` 10.3.

**Açık:**
- **Yakalama ayağının giriş karışımı** (`j35_rev` F_B_P16): 8–11 cm. İçerik değişmedi; giriş karışımı aynı.
- **`j30_rel_3450`:** 16.3 cm. V2.35 son koşusunda da 16.3; bu oturumda V2.35 değerleriyle 9.3. Aynı içerikte oturumlar arası fark.
- **`jstart`:** 50.2 cm, 45° dönüş kalkışı ve sol lateral kalkış. V2.35 değerleriyle 52.4; değişmedi.
- **`c29_combo`:** 15.4 cm, tek karelik yürüme-sol olayı. V2.35 son koşusu da 15.4.
- **`j36_wjs` / `j34_chain1`:** yeni sol kalkış (`SHM236_JogStart_F_Lfoot`, en kötü olayın sahibi bu klip), madde 4.
- **`j30_rel_3450`:** en kötü olay yeni `SHM236_JogRev_B_F_P27` içinde (16.3 cm).

**FPS modlarında açık kalanlar** (tablo bölüm 4; her hücre tek koşu):
- `j34_chain1` 60/120/20/gerçek: 27.9 / 27.6 / 17.3 / 17.4 (V2.35 değerleriyle 23.0 / 24.9 / 7.6 / 13.2). Sahibi yeni sol kalkış ve CP2 kalkışı. **Kötüleşti.**
- `jstart` 20 FPS 74.1 (V2.35 değerleriyle 47.9), gerçek zaman 48.1 (30.2). Sahibi vendor kalkışları (TurnR045, Jog_Left_Start); V2.36 bunları değiştirmedi. Ama farkı açıklayamıyorum, **kötüleşme olarak açık**.
- `e29_chain` 20 FPS 27.4 (6.0): tek kare (0.05 s) `SHM216_Cut_L_090` girişi. Gerçek zaman 22.9 (13.5): ikisinde de `SHM217_BackLink_4`. **Kötüleşti.**
- `c29_combo` gerçek zaman 13.1 (5.8): tek karelik yürüme-sol, 30 FPS'teki ile aynı olay.
- `j36_wjs` 120 FPS 20.1 (11.2): CP2 kalkışında 2 s'lik yavaş sürünme.

### 7. İlk kullanım ve eksik test kayıtları tamamlandı mı?
**İlk kullanım:**
- Aynı oturumda DB kurulduktan veya değiştirildikten sonraki ilk aramada 2 kare DB yoktu.
- Bu, ters dönüş ve yüklü yolda vendor pivota ya da döngüye düşürüyordu: 21–50 cm.
- Temiz açılıştan sonra, ısınma koşusu olmadan yapılan ilk kullanımda 4 senaryonun hiçbirinde DB'siz kare yok; değerler sıcak koşularla aynı.
- Yani kusur, yalnız oturum içinde DB düzenlemesinden hemen sonra görülüyor. Temiz açılış ve üretim durumu güvenilir.

**Eksik kayıtlar:**
- V2.35'te eksik kalan 20 FPS `j35_rev` kaydı bu sürümde tabloda; bölüm 4.
- Eksik kalan her hücre "-" yazıldı ve PASS sayılmadı.

### 8. Üretimde ne var, ne reddedildi, ne açık?
- **Üretimde:** `stop`, `start`, `rev`, `load`.
- **Reddedilen:**
  - `resume`;
  - kısa adım varyantı;
  - iki klipli duruş;
  - duruşun idle karesinde bitmesi.
- **Açık:**
  - yeni sol kalkışın kaynak kayması;
  - duruş ortasında tekrar basış;
  - `jstart` 45° ve lateral kalkışlar;
  - durup çapraz kalkış;
  - ters dönüşte görünen kol farkının küçük kalması;
  - pelvis çökmesi 6–11 cm;
  - arazi;
  - gerçek 180° (NOT_TRIGGERED);
  - kalan çapraz aileler.

Bütün locomotion sisteminin tamamlandığını iddia etmiyorum.

### 9. Kaç yeniden açılış gerekti, süreler neydi?
- Aday geliştirmesinin tamamı tek editör oturumunda yapıldı (19:48–21:34; 1 açılış).
  - Aday DB'ler ABP değişkenleri üzerinden aynı oturumda değiştirildi.
  - Yerinde düzenleme veya yedekten geri yükleme gerekmedi.
- Varlık üretimi işlerinin süreleri:

  | İş | Süre |
  |---|---|
  | 24 duruş klibi | ~1 dk |
  | 64 ters dönüş + 16 yüklü klip | ~3 dk |
  | Kalkışlar | <1 dk |
  | DB kurulumları | 1–2 dk |

- Test ve bekleme: aday aşamasında 150 PIE koşusu.
- Son zincirde sırasıyla:
  - üretime alma;
  - temiz açılış ve doğrulama;
  - soğuk ilk kullanım;
  - 30 FPS kanıtı;
  - 4 FPS modu;
  - kayıtlar.
- Toplam **8 editör açılışı**:

  | Açılış | Saat | Neden |
  |---|---|---|
  | `p1` | 19:47 | aday geliştirme |
  | `fin` | 21:42 | üretime alma ve kaydetme |
  | `finv` | 21:44 | temiz açılış, doğrulama, soğuk ilk kullanım, 30 FPS kanıtı |
  | `f60` | 22:24 | 60 FPS (FPS modu editör başlatma argümanı) |
  | `f120` | 22:49 | 120 FPS |
  | `f20` | 23:25 | 20 FPS |
  | `freal` | 23:42 | gerçek zaman |
  | `cap` | 00:12 | normal hızlı kayıtlar ve kamera açık/kapalı |

- Oturumdaki PIE koşusu toplamı 343 (ısınma koşuları dahil). 30 FPS son kanıt zinciri yaklaşık 35 dk sürdü, her FPS modu 20–35 dk, kayıtlar 10 dk, kamera 4 dk.
- İlk doğrulama `FIN_FAILED` verdi. Neden: doğrulayıcı süzgeci, kasıtlı olarak değiştirilen yüklü DB değerini tanımıyordu. Süzgeç düzeltildi ve aynı temiz editörde salt okunur olarak yeniden doğrulandı: `ALL_OK`. `ALL_OK` yalnız yapılandırma kontrolüdür.

## 1. Aşamalar ve sıra
Brief'in son sırası izlendi:
1. Aday işler bitti; kuyruk boştu.
2. `promote236.py` ile kaydedildi (manifest `promo236`).
3. Editör kapatılıp temiz açıldı (`finv`; yeniden yüklemeden sonra kirli paket yok).
4. Disk üzerindeki üretim durumu doğrulandı (`VERIFY236 ALL_OK`).
5. Son kanıt: soğuk ilk kullanım, 30 FPS, 4 FPS modu, kayıtlar, kamera.

Aday sırası:
- **Aşama 1:** sol ve sağ için birer temsilî klip, kaynakta değerlendirme.
- **Aşama 2:** oyunda A/B. İki klip yetmedi, 24 evreye çıkıldı.
- **Aşama 3:** kalkış boşluğu, pelvis yükselme, ters dönüş ve yüklü içerik.
- 32/64 klipli çoğaltma, yalnız ters dönüş ailesinde yapıldı. Bunun nedeni, o ailenin V2.35'te zaten 32 evre olması; ayak planı aynı.

## 2. Duruşu geliştirirken denenenler

| Deneme | Sonuç |
|---|---|
| Vendor fren adımı mesafesi (51–53 cm) | Fazla uzanıyor; döngü iniş mesafesine (31–39 cm) indirildi. |
| Salınım ayağı düz çizgide | Kalkışta ayak hatası; döngü yolunu izleyen salınım. |
| Pelvis çökmesiyle diz kurtarma (12 cm) | Giriş ve son pozu bozdu; topuk kalkışı ve basılı ayağa sınırlı çökme. |
| İki klip | Bir kare sonra diğer klibe atlama: 46 cm. 24 evre. |
| İdle karesinde bitiş | Sol başlangıç DB'si ve TurnL045: 85 cm. Vendor duruşun son karesi. |
| Kısa adım (step_max 30) | Çökme azalmadı; reddedildi. |
| Pelvisin yavaşlamayla yükselmesi | Üretimde; çökme 8–11 cm'den 6–11 cm'ye, gövde eğimi 0.3–1.0°. |

## 3. Tablolar
Tam tablolar `TABLES_V236.md` içinde. Gövde denetiminden (30 FPS) seçmeler:

| Koşu | Kol salınımı korunan | Geri çekme cm | Açık duruş cm @+0.6 s | Gövde ° @0 / @+0.6 | Pelvis çökmesi cm |
|---|---|---|---|---|---|
| `j36_stop` V2.36 | 0.55 | 2.7 | 0.9 | 11.9 / 0.6 | −8.5 |
| `j36_stop` V2.35 | 0.70 | 16.7 | 3.4 | 11.7 / 4.8 | −9.3 |
| `j36_stopb` V2.36 | 0.35 | 8.6 | 2.7 | 12.6 / 0.3 | −9.8 |
| `j36_stopb` V2.35 | 1.13 | 51.7 | 32.4 | 12.6 / 11.4 | −11.7 |
| `j36_wjs` (2. duruş) V2.36 | 0.45 | 12.1 | 7.7 | 15.0 / 0.9 | −10.6 |
| `j36_wjs` (2. duruş) V2.35 | 0.98 | 51.8 | 24.3 | 14.8 / 10.7 | −11.7 |

## 4. FPS modları
En kötü kayma cm, V2.36 / V2.35 değerleri. Her hücre tek koşu; gerçek zaman tekrarlanabilir değil.

| Senaryo | 30 | 60 | 120 | 20 | gerçek |
|---|---|---|---|---|---|
| `j36_stop` | 5.9 / 11.7 | 7.8 / 19.7 | 8.4 / 27.9 | 0.0 / 12.2 | 6.5 / 13.6 |
| `j36_stopb` | 5.9 / 12.3 | 8.5 / 22.9 | 15.5 / 59.5 | 0.0 / 0.0 | 6.3 / 6.1 |
| `j36_stopr` | 7.2 / 19.6 | 8.5 / 20.0 | 12.5 / 28.6 | 9.6 / 6.3 | 9.8 / 15.1 |
| `j36_wjs` | 14.3 / 6.8 | 8.6 / 15.9 | 20.1 / 11.2 | 9.5 / 14.4 | 8.9 / 17.7 |
| `j35_rev` | 8.0 / 8.0 | 8.7 / 9.3 | 9.1 / 8.3 | 7.8 / 7.1 | 5.6 / 6.9 |
| `j35_rev2` | 9.3 / 9.3 | 10.1 / 6.2 | 11.3 / 11.3 | 7.6 / 8.6 | 6.9 / 6.7 |
| `j30_rel_3200` | 9.1 / 9.0 | 14.4 / 12.0 | 10.1 / 24.9 | 7.1 / 6.7 | 6.8 / 6.5 |
| `j30_slow` | 0.0 / 9.3 | 6.8 / 8.5 | 7.3 / 7.3 | 7.6 / 7.6 | 6.5 / 7.4 |
| `j34_chain1` | 17.1 / 16.5 | 27.9 / 23.0 | 27.6 / 24.9 | 17.3 / 7.6 | 17.4 / 13.2 |
| `jstart` | 50.2 / 52.4 | 51.8 / 42.1 | 47.6 / 49.8 | 74.1 / 47.9 | 48.1 / 30.2 |
| `c29_combo` | 15.4 / 7.9 | 11.8 / 11.8 | 12.8 / 12.9 | 6.0 / 6.0 | 13.1 / 5.8 |
| `e29_chain` | 6.5 / 6.5 | 20.6 / 20.6 | 18.9 / 18.9 | 27.4 / 6.0 | 22.9 / 13.5 |
| `e29_load` | 14.2 / 14.2 | 8.7 / 12.6 | 17.9 / 15.3 | 9.0 / 26.9 | 11.1 / 8.5 |

**Eforlu ters dönüşte iki ayakla bekleme (s), V2.36 / V2.35:**

| | 30 | 60 | 120 | 20 | gerçek |
|---|---|---|---|---|---|
| `e29_load` | 0.13 / 0.43 | 0.13 / 0.15 | 0.10 / 0.37 | 0.15 / 0.40 | 0.13 / 0.41 |

Yorum:
- Duruş ailesi her FPS'te V2.35'ten iyi ya da eşit. Tek istisna `j36_stopr` 20 FPS: 9.6 / 6.3.
- Ters dönüşler V2.35 düzeyinde. `j35_rev2` 60 FPS 10.1 / 6.2.
- Kötüleşenler bölüm 0/6'da listelendi: `j34_chain1`, `jstart` 20/gerçek, `e29_chain` 20/gerçek, `c29` gerçek, `j36_wjs` 30/120.

## 5. Kamera
Yeni kamera sistemi yok; kamera kodu bu sürümde değişmedi.

**Gövde etkisi.** Kamera açık / kapalı karşılaştırması aynı V2.36 gövdesiyle yapıldı. `camoff` yalnız `CamRecEnabled=false` demek; başka bir şey kapatılmadı. Sonuç `camab234`:

| Koşu | Hız / yön / konum farkı | Kameranın kendi dönüşü |
|---|---|---|
| `cam33_sturn` | 0 | açık 85.3°, kapalı 0° |
| `j36_stopr` | 0 | 0° |
| `j35_rev` | 0 | 0° |

Kamera gövdeyi değiştirmiyor. Düz çizgideki duruş ve ters dönüşte kendiliğinden yeniden ortalama tetiklenmiyor.

**Yeniden ortalama (`rec233`):**

| Koşu | Hata | Oturma süresi |
|---|---|---|
| fare, yürüyüş dönüşü | 86 → 12.9° | 2.37 s |
| gamepad (`pad235`) | 86 → 11.5° | 1.6 s |
| koşu dönüşü, kamera açık | 63 → 15.1° | 2.17 s |
| koşu dönüşü, kamera kapalı | 66.6°'de kalıyor | — |

V2.33–V2.35 değerleriyle uyumlu.

**Gerçek 180° ters dönüşte kamera tepkisi: NOT_TRIGGERED.** Ters dönüş testlerinde kamera dönmedi (0°).

## 6. Kararlar ve geri dönüş
- Geri dönüş: `promote236.py {'rollback': True}`. Değerler `CHANGES_V236.md` içinde.
- `resume` grubu üretimde değil. ABP kancası varsayılan üretim DB'sini okuyor; davranış V2.35 ile aynı.
- Başarısız adaylar (iki klip, kısa adım, idle bitiş, resume) üretime alınmadı.
- Başarılı bağımsız onarımlar (duruş, kalkış, yüklü bekleme), başka başlıklar açık diye geri alınmadı.

## 7. Medya
`vid/` içindeki her dosya sabit adımlı 30 FPS kayıt: gerçek hız, kesintisiz, ağır çekim yok. GIF'ler küçültülmüş; `_realtime.avi` dosyaları tam kare.

| Dosya | İçerik |
|---|---|
| `stop_restart_before_side` / `_v236_side` / `_v236_game` / `_v236_diag` | tempolu → bırak → dur → ileri → dur. "Önce" kaydı, terfiden önceki aday oturumundan (`s2g`, üretim = V2.35); kayıt penceresi farklı olduğu için zamanlar eşleşmez. |
| `stop_other_foot_v236_side` | diğer fren ayağı |
| `walk_jog_stop_before_side` / `_v236_side` | yürü → tempolu → dur → ileri, aynı son kayıt oturumu |
| `late_repress_v236_side` | duruşun sonunda tekrar ileri (sol ayakla düz kalkış) |
| `reversal_before_side` / `_v236_side` / `_v236_game` | tempolu → sert S → geri → W |
| `effort_reversal_before_side` / `_v236_side` | eforlu ikinci ters dönüş |
| `chain1_restart_v236_side` | geri kalkış → ileri → dur → yeniden hareket |
| `stop_side_start_v236_game` | dur → yan kalkış → çapraz kalkış |

**Kare şeritleri (`sheets/`).** Kendi görsel değerlendirmem:
- **`fin_wjs_pre` / `fin_wjs_o`** (aynı oturum, 9.6–11.4 s):
  - V2.35'te 9.7–10.3 s arasında diz yüksekliğinde adımlar var; kollar koşu taşımasında kalıyor.
  - V2.36'da kısa adımlar var; kollar iniyor, gövde 10.3 s'de oturmuş.
  - Ama 9.8–10.2 s arasında dizler bükük ve pelvis alçak; çökme hâlâ görünüyor.
  - Duruşun süresi kısa. "Ani" görünüp görünmediğinin normal hızdaki kabulü sizde.
- **`fin_stopr_o`:** 5.0–5.5 s kısa fren ve kapanış; 6.0 s'den sonra sakin duruş.
