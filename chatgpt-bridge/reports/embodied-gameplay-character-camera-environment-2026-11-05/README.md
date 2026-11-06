# SPHIRUS: fiziksel etkileşim, yeni karakter, yakın kamera ve orman

Tarih: 2026-11-05 / 2026-11-06. Motor: UE 5.8.4-58902052. Harita: `/Game/GraceRanger/Maps/L_GR_SphirusHouse`.

## Sonuç

**Maske işi baştan sona oynanıyor ve yeni karakter üretimde.** Yeni oyundan başlayan kesintisiz test geçti: tezgâh, elde inceleme, bırakma, verandadan şerit, bağlama, taşıma, askıya asma, dışarı çıkış, kıyı, patika, eve dönüş. Işınlama yok, çalışma hatası yok.

**Görsel kabul henüz senin.** Sayılar ve kare dizileri iyi, ama oyun hissini ben oynayarak ölçemiyorum. Saç ve kıyafet senin kararınla bekletildi, yakın kamerada kusurları görünüyor.

| Alan | Sonuç | Kısa açıklama |
|---|---|---|
| Fiziksel maske işi | PASS (teknik) | Tam zincir, iptal, geri koyma, askı. Görsel kabul sende |
| Kayıt ve eski kayıtlar | PASS | Dört eski kayıt kopyası, iki yüklemede kopyasız |
| Yeni karakter | PARTIAL | Üretimde çalışıyor. Saç ve kıyafet bekliyor |
| Yakın kamera | PARTIAL | Yakın sağ omuz kuruldu. Engel arkaya girince kamera çok kısalıyor |
| Yürüyüş W→S | PASS (ölçüm) | Geri yürüyüş 2.32 s → 0.02 s |
| Sprint 180 duruşu | PARTIAL | Pelvis 78.6 → 87.2 cm. Dizler t=6.00'da hâlâ biraz dışa açık |
| Pine Forest PCG | PARTIAL | Otomatik üretim reddedildi, seçilmiş zemin parçaları eklendi |
| PBL | PARTIAL | Değerler karşılaştırıldı, ışık değiştirilmedi |
| True Lens | Reddedildi | Oynanışta ekran kenarını bulandırıyor |
| Ses | PARTIAL | Orman rüzgârı eklendi. Kulakla dinlenmedi |
| Gamepad | NOT_TESTED | Bu turda bağlı gamepad ile denenmedi |
| Gerçek fare ile maskeyi çevirme | NOT_TESTED | Test girdisi oyuna ulaşmadı. Lütfen elle dene |
| Gerçek merdiven | NOT_TESTED | Senaryo yok |
| Paketlenmiş oyun | NOT_TESTED | Yalnız editör PIE |

## Oyunda ilk bakman gerekenler

1. Tezgâhta `E` ile maskeyi al ve fareyle çevir. Bunu otomatik doğrulayamadım.
2. Yürürken W'den S'ye geç. Doğal dönüş olup olmadığına karar ver.
3. Sprintte tam ters yöne bas. t=6.00 civarındaki diz duruşuna bak.
4. Rota dışında tepeye koşarken kamera çökmesine bak.

## Fiziksel maske işi

`BP_GR_MaskBench` var olan SF etkileşimini taşıyor. Görev, envanter, günlük ve kayıt sahipliği SF 5.2'de kaldı. İkinci bir sistem eklenmedi.

| Durum | Oyuncu | Kalıcı sonuç |
|---|---|---|
| Aşama 0 | Tezgâha yürür, `E` ile alır, inceler, `E` ile bırakır | Bırakınca aşama 1 |
| Aşama 1 | Verandadan şeridi alır, tezgâhta bağlar | Bağlama 2.9 s'de tamamlanır, şerit harcanır, aşama 3 |
| Aşama 3 | Maskeyi alır, taşır, askıya gider, asar | Asma 1.45 s'de tamamlanır, günlük yazılır, aşama 2 |
| İptal | Bağlamada `F`, 2.2 s'den önce | Şerit kaybolmaz, tekrar bağlanır |
| Taşırken | Tezgâh yakınında `E` | Maske tezgâha döner, aşama 3 kalır |
| Zıplama | Taşırken boşluk tuşu | Zincir bozulmuyor |

Tek mantıksal tamamlanma noktaları bunlar. Animasyonun rastgele karesi kayda yazılmıyor. Taşıma yürüyüşe sınırlı (en çok 80 cm/s).

**Kayıt testi** (`evidence/kayit_testi.txt`, `evidence/iptal_testi.txt`). Eski kayıtların kopyalarıyla, her biri iki kez yüklendi:

| Kayıt | Yükleme sonrası | Sonuç |
|---|---|---|
| Eski "rafa koyma" bitmiş kaydı | Aşama 2, günlük 1, maske askıda | PASS, çoğalma yok |
| Bağlanmış | Aşama 3 | PASS |
| Şerit alınmış | Aşama 1, şerit bir kez | PASS |
| Başlangıç | Aşama 0, görev listesi boş | PASS, ilk işlemde görev geri geliyor |

Kullanıcı kaydına dokunulmadı. Oturum başında `SFSaveSlot.sav` yoktu, testlerin oluşturduğu kopyalar silindi, `Reset.sav` duruyor.

## Yeni karakter

| Parça | Yol |
|---|---|
| Oyuncu | `/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player` (ebeveyn `BP_PBI_Player`) |
| Üretime bağlantı | `BP_GM_GR_GraceRanger` varsayılan piyonu |
| Hareket kaynağı | `CharacterMesh0`, `SK_Mannequin`, `ABP_GR_MotionMatching` |
| Görünen gövde | `Manny` bileşeni, `ABP_GR_MetaHuman` ve mevcut retarget zinciri |
| Yüz | `SKM_Hazel_Face_a` (onaylı GD38 yüzü, yumuşatılmış) |
| Gövde dokusu | `MI_Hazel_Body`, FF Hazel tabanı |

Karşılaştırma: eski `evidence/09b_karakter_eski.png`, yeni `evidence/09_karakter_hibrit.png` ve `evidence/09c_karakter_tam.png`.

Eski karakter silinmedi. Geri alma aşağıda.

Bekleyen kusurlar: saçta yakın planda boyalı lekeler ve bazı ışıklarda beyaz parçalar, kıyafette şort kenarı, belde gri parçalar ve yaka izi. Şerit rengi hâlâ gri yeşil.

## Kamera

Tek sahip korundu: `BP_GR_Player` `GR_UpdateRig` ve `DA_GR_LocomotionBehavior`. Grounded veya ikinci kamera yok.

| Değer | Önce | Sonra |
|---|---|---|
| Keşif mesafesi | 155 | 142 |
| Koşu / sprint mesafesi | 172 / 184 | 160 / 174 |
| İç mekân mesafesi | 145 | 128 |
| Omuz ofseti | 40 | 48 |
| İç mekân omzu | 38 | 40 |
| Pivot yüksekliği | 61 | 62 |
| FOV keşif / koşu / sprint | 62 / 62.8 / 64 | 60 / 61.5 / 63 |
| Etkileşim mesafesi, FOV | 160, 61 | 130, 58 |
| İnceleme mesafesi, FOV | 160, 61 | 125, 56 |

Hıza bağlı açılma V2.55'teki `GR255_UpdateFrame` ile aynı kaldı. Tezgâh ve askıda iki sahne kamerası `SetViewTargetWithBlend` ile 0.8 s geçiş yapıyor (FOV 46, f/2.8, odak 105). Serbest oyunda sürekli alan derinliği yok.

Görseller: `evidence/12_kamera_once.png`, `13_kamera_sonra.png`, `14_kamera_ic_mekan.png`, `01` – `05`.

Açık kusurlar:

- Rota dışında tepeye koşarken arkaya katı cisim girince kamera 30–44 cm'ye kısalıyor, sırt ekranı kaplıyor. Engel geçince 187 cm'ye dönüyor.
- Askıdan hemen sonra merdiven altında kamera başa çok yaklaşıyor.
- Dar alan ve duvar için yalnız bu ölçümler var. Merdiven test edilmedi.

## Hareket

Kök neden bulundu: W→S'de dönüş planı yalnız bir kare çalışıyordu. Hız aynı anda 100 cm/s eşiğinin altına düştüğü için plan sahipliği oturmadan yol kapanıyordu. V2.55 raporundaki "aynı kare" notu buydu.

| Değişiklik | Değer |
|---|---|
| `SHM255_RevMinV` | 190 → 60 |
| Yürüyüş dönüş veritabanı | `PSD_SHM254_T255_WalkR/L` üretime alındı |
| Plan iptalinde çıkış | Koşu yerine `PSD_LB_WalkLoops` (`SHM256_WalkExit`) |
| Sprint 180 | Yeni `SHM256_Sprint_R180/L180`, aynı gerçek hareket yakalama kaynağı |

**Yürüyüş 180, üretim, 60 FPS:**

| Ölçüm | Önce | Sonra |
|---|---|---|
| Geri yürüyüş | 2.32 s | 0.02 s (30 FPS: 0.00) |
| Gövdenin dönmesi | yok | 1.12 s |
| Yeni yöne gidiş | 0.68 s | 0.77 s |
| Yeniden hız | 1.12 s | 1.10 s |
| Tepe ivme | 0.62 g | 0.56 g |
| Ayak kayması, en çok | 4.9 cm | 2.6 cm |

Yeni yöne gidiş 0.09 s uzadı. Bu beklenen fark: önce geri geri gidiyordu, şimdi dönüyor.

**Sprint 180:** en düşük pelvis 78.6 → 87.2 cm. Ölçülen en kötü sıçrama 61 → 57 m/s². Yön süresi korundu.

**Üretim turu, 60 FPS, sıçrama sayısı (en kötü m/s²) ve en çok ayak kayması:**

| Senaryo | Sıçrama | Ayak |
|---|---|---|
| Yürüyüş 180 | 2 (45) | 2.6 cm |
| Koşu 180 | 11 (59) | 2.6 cm |
| Sprint 180 sağ / sol | 16 (57) / 19 (51) | 2.8 / 2.4 cm |
| Sprint 90 sağ / sol | 13 (50) / 18 (48) | 2.9 / 2.7 cm |
| Koşu 90 | 8 (54) | 7.1 cm |
| Yürüyüş başlangıcı | 5 (32) | 6.6 cm |
| Sprint dokunuş / orta komut / sağ-sol | 17 (46) / 19 (51) / 16 (46) | 2.8 / 3.1 / 2.0 cm |
| Eğimde sprint 180 | 15 (64) | 2.2 cm |
| Duvar yakınında sprint 180 | 16 (58) | 2.8 cm |
| Rastgele girdi: yürüyüş / koşu / sprint | 23 (52) / 68 (75) / 78 (138) | 11.9 / 7.1 / 7.1 cm |

30 FPS: yürüyüş 180 0 sıçrama, koşu 180 3 (34), sprint 180 6 (32).

Açık kusurlar:

- Rastgele yürüyüş testinin bir tohumunda (`fz_walk_a`) tuş bırakıp hemen başka tuşa basınca tek karelik baş sıçraması kaldı: 193 m/s², 4 cm. Üretimde bu tohumun en kötüsü 38'di. Düzeltmeyi denedim, kalktı değil.
- Sıra 3–6'ya (sert sağ-sol, ters istek, düşük hız sprint pivotu, çapraz salınım) bu turda yeni iş yapmadım. V2.55 kazanımları korundu.
- Animated Female Locomotion Set ve Grounded alınmadığı için kaynaklar projede olanlar.

Gerçek hız videosu: `evidence/20_yuruyus_sprint_gercek_hiz.avi` (60 fps, 3.2 s). Kareler: `10_yuruyus_WS_yan.png`, `11_sprint180_yan.png`.

## Çevre

**Pine Forest PCG:** küçük alanda denendi, kaydedilmedi.

| Deneme | Sonuç | Karar |
|---|---|---|
| Büyük bitki katmanı, göl kıyısı | 6.711 örnek, +53 MB. İnce sopa gövdeler, canlı yeşil, gölü kapatıyor | Reddedildi (`17_...png`) |
| Zemin örtüsü, yükselen orman | 6.092 örnek, +130 MB. Yine sopa gövdeler ve sarkan perde | Reddedildi (`18_...png`) |
| Seçilmiş zemin parçaları | 108 örnek, çarpışmasız, 45 m'de kesilir | Üretime alındı |

Son karar çift ormanı da önledi. Mevcut 22.302 örneklik ormana dokunmadım. Yalnız iğne yaprak, kabuk ve dal yığınları ev–göl ve arka patika kenarlarına, patikadan 1.3–4.2 m uzağa eklendi. Eğimli yerlere ve zemin dışına konmadı. Ev, iskele ve görev alanları dışarıda kaldı. Araziye, gölete ve mevcut bitkilere dokunulmadı.

Görsel: `15_zemin_once.png`, `16_zemin_sonra.png`, `06_kiyi.png`, `07_patika.png`.

Yapılmadı: arazi boyasının yeniden kontrolü, proje PCG preseti. PCG üretimde kullanılmadığı için preset gerekmedi. Boyama kontrolü açık kaldı.

**PBL Database:** motor eklentisi olarak yüklü. Referans: kapalı havada öğlen yaklaşık 9.000 lux, EV 10–11. Haritada güneş 1500, pozlama sapması −0.45. Proje fiziksel ölçek yerine göreli değer kullanıyor. Kabul edilmiş görüntüyü bozmamak için değiştirmedim. Değerler `evidence/pbl_referans.txt`.

**True Lens:** karşılaştırıldı (`19_truelens_kapali_acik.png`). Kare hızı etkisi ölçülebilir değil, ama varsayılan ayar kenarları bulandırıyor. Brief "yürürken görüşü sürekli bulandırma" dediği için haritaya eklenmedi.

**Ses:** haritada hiç ses aktörü yoktu. Beş `EX_Audio_ForestAir` rüzgâr kaynağı eklendi, uzaklıkla sönüyor, evin içine az ulaşıyor. Paket su sesi içermiyor, göl sessiz. Temas sesleri ve ayak sesi kulakla kontrol edilmedi.

**Performans**, editör PIE, göreli:

| Nokta | FPS önce | FPS sonra | GPU belleği önce | Sonra |
|---|---|---|---|---|
| Ön patika | 28–29 | 27–28 | 6782 MB | 6862 MB |
| Arka patika | 29–32 | 26–29 | 6721 MB | 6673 MB |

Bütçe yükseltilmedi. Tüm rota ortalaması yaklaşık 30 FPS. Arka patikanın belleği düştü görünmesi ölçüm oynaklığı, gerçek kazanç değil. Bu iki ölçüm tek örnek.

## Kabul testleri

| Test | Sonuç | Kanıt |
|---|---|---|
| A. Yeni oyundan kesintisiz rota | PASS | `rota_testi.txt`. Aşama 0→1→3→2, şerit harcandı, günlük 1 |
| B. Kayıt ve yükleme, eski kayıtlar | PASS | `kayit_testi.txt`, `iptal_testi.txt` |
| C. Hareket, 30 ve 60 FPS | PASS teknik, PARTIAL görsel | Yukarıdaki tablolar |
| D. Kamera ve sanat | PARTIAL | Görseller. Saç, kıyafet bekliyor |
| E. Kalıcılık | PASS | `son_durum.txt`, temiz açılış, kirli paket yok |

Test yürüyücüsü iki noktada kayaya takıldı (`r_pond`, `r_up`). Bunlar düz çizgi yürüyen test aracının sınırı. Eklediğim parçalarda çarpışma yok, doğruladım.

## Nwiro

Integration Kit 1.0.15 kurulu, ama Windows Smart App Control imzasız DLL'i engelliyor (hata 4551) ve etkinleştirince editör açılmıyor. `sphirus.uproject`'ten çıkarıldı. Güvenlik ayarı senin kararın olduğu için dokunmadım. Epic Unreal MCP bu oturumda bağlanamadı, işler proje koşucusuyla yapıldı.

## Varlıklar

| Kaynak | Hedef | Kullanım |
|---|---|---|
| FF Hazel (Fab) | `Content/EditableCharacters/HazelM` | Gövde tabanı |
| Pine Forest PCG Biome | `Content/EasyBiomes`, 14 GB | 7 zemin parçası, rüzgâr sesi. Demo haritalar alınmadı |
| True Lens | `Content/TrueLens` | Kullanılmıyor |
| PBL Database | Motor eklentisi, `sphirus.uproject` | Referans |

İlk taşımada 174 yumuşak referanslı dosya eksik kalmıştı, kaynaktan kopyalandı. Liste: `Saved/Codex/Embodied_20261105/easybiomes_added.txt`. Paketler 14 GB yer tutuyor, ham satın alınmış varlıklar bu rapora konmadı.

## Değişen dosyalar

- Harita: `L_GR_SphirusHouse`.
- Oyun: `BP_GM_GR_GraceRanger`, `DA_GR_LocomotionBehavior`, `ABP_GR_MotionMatchingBase` ve `ABP_GR_MotionMatching`.
- Yeni: `/Game/GraceRanger/SF/MaskJob/*`, `/Game/Sphirus/CharacterLab/Hazel_20261106/*`, `/Game/GraceRanger/SHME/Animations/V256/*`, `/Game/GraceRanger/Environment/PineCover/*`.
- Ayar: `sphirus.uproject`, `Config/DefaultEngine.ini` (EasyBiomes kanalları).
- Belge: `CLAUDE.md`, `claude-unreal-tooling.md`.
- Araçlar: `Tools/Embodied_20261105/`.

Bir hata notu: testlerin geçici oyun modu ayarı ve bir yardımcı kamera iki harita kaydına karıştı. Yakaladım, temizledim, temiz açılışta doğruladım (`son_durum.txt`).

## Geri alma

Yedekler: `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/`.

| Ne | Nasıl |
|---|---|
| Karakter | `BP_GM_GR_GraceRanger` varsayılan piyonunu `BP_PBI_Player` yap |
| Yürüyüş ve sprint | `promote256.py`, `mode: rollback`. Eski değerler `loco/data/promote256_before.json` |
| Kamera | `emb_camda` yedeği veya `cam/da_before.json` |
| Harita, zemin parçaları ve ses | `emb_map_075302` yedeği, parçalardan öncesi |
| Harita, maske düzeni öncesi | `emb_map_*` yedeklerinin ilki |
| Oyun modu | `emb_map_075815` içindeki `BP_GM_GR_GraceRanger` yedeği |

## Sonraki iş

1. Yukarıdaki dört oyun içi kontrol.
2. Saç ve kıyafet, sen açtığında.
3. Kamera engel çökmesi ve `fz_walk_a` tek karelik sıçrama.
4. Gamepad ve gerçek merdiven testi, arazi boyası kontrolü.
