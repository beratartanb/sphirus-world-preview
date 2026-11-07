# SPHIRUS: ilk gün, karakter, kamera ve ışık

Tarih: 2026-11-07, ikinci tur. Motor: UE 5.8.4-58902052. Harita: `/Game/GraceRanger/Maps/L_GR_SphirusHouse`. Oyuncu: `BP_HybridA_Player`.

## Sonuç

**İlk gün artık satın alınan animasyonlarla ve yanan bir şömineyle baştan sona oynanıyor, ama brifin tamamı bitmedi.** Yeni oyundan uyanma, dolap, kıyafet, bitki, odun, kesme, şömine ve çay aynı koşuda tamamlandı. Görev sırası değiştirilmiş ikinci rota, yanlış sırada E basma, iş sürerken E tekrarı ve kayıt yükleme de geçti.

**Bu turda kapanan eski hatalar:** şömine alevi, istasyona anında ışınlanma, görünmeyen balta, tezgâhın içinden geçme, kol kasılması, fincan ve sıvı eksikliği.

**Kalan büyük işler:** keskin dönüş ve pivotlar, `fz_walk_a`, evin büyük yerleşim değişikliği, PBL verisi, gerçek merdiven, gamepad, paketlenmiş oyun. Tam liste aşağıda.

E tuşu test otomasyonuyla basıldı. Test karakteri istasyonun yakınına koydu, son metreyi istasyon yürüttü. Elle oynanmadı. Ses dinlenmedi.

| Başlık | Durum |
|---|---|
| Karakter gövdesi | PASS (teknik). Tam yüzeyli Hazel |
| Yüz | PARTIAL. MetaHuman içinde kuruldu, referans kabulü sende |
| Baş ve gövde birleşimi | PASS (görüntü) |
| Ten ve doku | PARTIAL |
| Kıyafetler | PARTIAL. 5 set, 18 kemer, kumaş simülasyonu yok |
| Yataktan kalkma | PASS (görüntü). Village Life klibi, gerçek hızda video var |
| Dolap | PARTIAL. Kapak Interaction klibiyle açılıyor, kapatma da aynı klibi kullanıyor |
| Odun toplama | PARTIAL. Village Life eğilme klibi, elde odun görünmüyor |
| Odun kesme | PARTIAL. Fix & Build vuruşu, iki elde balta, yonga ve yarılan odun var. Parmak teması her karede oturmuyor |
| Şömine | PASS (görüntü). Alev, duman, ışık titremesi var. Ses bağlı, dinlenmedi |
| Bitki ve çay | PARTIAL. Demlik, fincan ve sıvı var. Pour ve Drink hâlâ üretilmiş klip |
| Tezgâh | PARTIAL. Çarpışma ve duruş düzeldi, parmak teması ölçülmedi |
| Kayıt | PASS. Oyun içi kayıt çağrısıyla. Menüden denenmedi |
| Yakın koşu kamerası | PARTIAL. Açık alanda temiz koşu ölçülmedi |
| Genel hareket | PARTIAL. Kol rahatladı, dönüş ve pivotlara dokunulmadı |
| Ev ve çevre | PARTIAL. Kesim alanına kullanım izi eklendi, büyük yerleşim yok |
| PBL ve True Lens | PARTIAL. PBL verisi kullanılmadı, lens A/B alındı |

## Kullanılan animasyon paketleri

| Paket | Nerede bulundu | Nerede kullanıldı |
|---|---|---|
| MC Village Life | Bu projede yoktu. `GameAnimationSample/Content/MC_VillageLife` içindeydi, `Content/MC_VillageLife` altına kopyalandı | Uyku ve yataktan kalkış, yerden alma |
| MC Fix & Build | `Content/MC_FixBuild_Pack` | Balta çekme, dikey vuruş, diz çökme ve vurma |
| Interaction | Bu adla ayrı paket bulunamadı. `AAMS/Animations/Interactions` kullanıldı | Dolap kapağı |
| MC Sample | Kardeş projeden kopyalandı, içki kliplerine bakmak için | Şu an kullanılmıyor |

Village Life ve Fix & Build iskeletleri `SK_Mannequin` ile aynı 91 kemik izine ve aynı kemik ofsetlerine sahip. Pozlar doğrudan oyuncu iskeletine yazıldı. Klipler eski `A_GR_Day_*` adlarını koruyor, istasyonlar değişmedi.

| Klip | Kaynak | Süre |
|---|---|---|
| Wake | `am_BedSingleB_Idle_01_Sleep` + `am_BedSingleB_Trans_GetOutLeft_Stand` | 10,3 s |
| Chop | `am_Stand_Trans_Axe` + `am_Axe_05_ChopVertical` + `am_Axe_Trans_Stand` | 6,9 s |
| Pick | `am_Stand_Trans_CarryInArms_PickUpFloor` en alçak noktaya kadar, sonra geri | 3,0 s |
| Kneel | `am_Stand_Trans_KneelHammerFloor` + `am_KneelHammerFloor_01_Hit` + `Trans_Stand` | 6,2 s |
| Kapak | `AM_Interact_Door_OpenPull_RightHand` | 2,7 s |

Üretilmiş olarak kalanlar: Pour, Drink, Dress. Village Life `CookPot` klipleri bel hizasında bir tencere bekliyor, demlik şömine basamağında alçakta.

**Çözülmemiş ayrıntı:** yatarken vücut klipten 97 cm yukarıda duruyordu. Nedeni bulunmadı. Yatış süresince kök 81 cm indirilerek düzeltildi, kalkarken sıfıra iniyor.

## Bu turda düzeltilenler

### Şömine

Alev iki ayrı nedenle görünmüyordu.

1. `N_CampFire` seyrek, tek tek alev parçaları üretiyor. Çoğu kütüklerin arkasında kalıyordu.
2. Alev dokusu 15×12 karelik bir atlas. Doku akışı düşük çözünürlükte bırakınca alev siliniyordu.

Düzeltme: ocağa beş alev kaynağı dizildi. `BP_GR_DayBoot` alev malzemesini açılışta bellekte tam tutuyor. Işık yanarken hafifçe titriyor. `SC_Campfire` sesi ateşle başlıyor. İlk denediğim kart alevi kaldırıldı, gizli duruyor.

### İstasyonlara geçiş

Karakter artık ışınlanmıyor. `BP_GR_DayBoot` zorlanmış hareket girdisiyle gerçek yürüyüş animasyonunu çalıştırıyor, sonra yöne dönüyor. 90 cm'den yaklaşım ölçüldü. Yol 3,5 saniyede biterse karakter olduğu yerde işe başlıyor, ışınlanma yok.

### Odun kesme

- Balta iki elde ve ağzı aşağıda. Dinlenirken kütüğe saplı duruyor, iş sırasında ele geçiyor.
- Kütükte kesilecek odun görünüyor. Vuruş anında kayboluyor.
- Aynı anda 8 yonga ve 2 yarım odun fizikle dağılıyor.
- Duruş noktası 18 cm geri alındı, çünkü vuruş kütüğü geçiyordu. Son konumda vuruş anı ayrıca çekilmedi.

### Çay

Demlik şömine basamağına taşındı. Şöminenin çarpışma kutusu etkileşimi kesiyordu, istasyon demliğin önüne görünmez bir noktaya alındı. İlk kullanımda sağ elde demlik, sol elde fincan, vuruş anında akan çay. İkinci kullanımda fincan sağ elde. Fincanda çay yüzeyi yalnız çay hazırken görünüyor. Demliğin kulpu yok, el gövdesinden tutuyor. Demlik ele anında geçiyor.

### Tezgâh

`GR_Day_BenchBlock` yalnız karakteri durduruyor. Etkileşim ve kamera içinden geçiyor. Duruş noktası 192'den 170'e alındı. Maske ve tezgâh etkileşimi aynı 22 cm kadar öne alındı, böylece el hedefleri bozulmadı.

Test: karakter masaya yürüdü, y=171'de durdu. Maskeyi masanın dışından aldı. Evdeki alt seviyede duran `Furniture_CR_MaskWorkInProgress` kaydı dosyaya yazılmadı. Oyunda görülen maske etkilenmedi.

### Kol rahatlığı

Yürürken dirsek neredeyse tam düzdü. `ABP_GR_MetaHuman` sonuna dört kemik ofseti eklendi. Etkisi hızla geliyor, montaj sırasında ve koşuda sıfıra iniyor.

| Ölçüm, yürüyüş | Önce | Sonra (dirsek değişikliği) |
|---|---|---|
| Sağ dirsek | 151–178° | 137–174° |
| Sol dirsek | 155–178° | 135–171° |

Son değerler: dirsek 13°, üst kol 6° geri, 4° dışarı. Son değerlerin tek koşusu yok, sayılar 14° dirsek denemesinden. Taşıma sırasında etkisi kapalı.

### Kullanım izleri ve ses

Kesim alanına 22'ye kadar yonga, 3 kesilmiş parça, el arabası, arka kapıya kova eklendi. Bu küçük bir iş, brifin istediği ev yerleşimi değil. Dolaba kapı sesi, toplamaya el sesi bağlandı. Hiçbir ses dinlenmedi.

## Testler

| Test | Sonuç |
|---|---|
| Yeni oyun rotası | PASS. Herb 1, Wood 1, Split 2, Fire 2, Tea 2 |
| Odunsuz şömine, bitkisiz çay | PASS. Sayılar değişmedi |
| Önce bitki, sonra odun | PASS |
| İş sürerken üç kez E | PASS. Çift sonuç yok |
| Kayıt ve yeniden açma | PASS. Fire 2 ve Tea 1 geri geldi |
| Tezgâh çarpışması | PASS. y=171'de durdu |
| Yüklemeden sonra alev görüntüsü | NOT_TESTED. Son alev düzeninden önce çekildi |
| Pause, menü kaydı, iptal | NOT_TESTED |
| Eski maske kaydı | Önceki turda PASS, bu turda tekrar edilmedi |

Görülen uyarı: `BP_TrueLens` içinde `TrueLensDynmaicMat` dizisinde 6 öğelik dizide 7. indeks hatası. Lens paketinden geliyor, düzeltilmedi.

## Performans

Aynı koşu, tek ölçüm. Ek dört alev kaynağından önce alındı.

| Nokta | Ortalama | p95 |
|---|---|---|
| Oda | 24,5 ms | 29,3 ms |
| Arka kapı | 28,2 ms | 30,6 ms |
| Kesim alanı | 29,0 ms | 31,3 ms |
| Orman | 29,7 ms | 32,0 ms |

Video belleği 6712 MB. Noktalar önceki turdakilerle aynı değil, doğrudan karşılaştırılamaz. Disk boşluğu 42 GB.

## Yapılmayanlar

- Keskin dönüş, 45–180° pivot, sprint dönüşü, fren ve yeniden hızlanma.
- `fz_walk_a` baş sıçraması.
- Taşıma demeti ve sepet. Village Life `CarryInArms` ve `CarryBasket` klipleri hazır, bağlanmadı.
- Village Life yürüyüşleri (`am_Loco_WalkA/B`) denenmedi. Genel yürüyüş için aday.
- Kapatma klibi (`AM_Interact_Door_ShutPull`), oturma, dinlenme.
- Evin dış ve iç büyük yerleşimi, patikalar, PCG dışlama.
- PBL verisiyle ışık.
- İç ve dış ses geçişi, kıyafet sesi.
- Gamepad, gerçek merdiven, tepe rotası, 30/60 FPS, paketlenmiş oyun.
- Yüz rig'i ifade testi.
- Bridge siyah kameraları.

## Satın alma ihtiyacı

Yok. Eksik animasyonlar projedeki paketlerde var.

## Geri alma

- Blueprint ve klipler: `day_*` manifestleri, `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/`.
- Harita: `grip_map_*` manifestleri.
- Kullanıcı kaydı: `Saved/Codex/Day_20261107/SFSaveSlot_user.sav`. Testlerden sonra aynı dosya yerine kondu.
- Kopyalanan paketler yeni klasörlerde: `Content/MC_VillageLife`, `Content/MC_Sample`.
- `ABP_MH_Ranger_Retarget_V2` yanlışlıkla değişti, yedekten geri kondu. Oyunda çalışan ABP `ABP_GR_MetaHuman`.

## Kanıt

`evidence/` içinde:

- `wake.mp4`, `chop.mp4`: gerçek hızda pencere kaydı, 12 FPS. Şömine videosu yok.
- `wake.jpg`: yataktan kalkış kareleri.
- `chop.jpg`: balta vuruşu kareleri, ağır çekimle alındı.
- `fire_lit.jpg`: istasyonlardan yakılmış ateş.
- `bench.jpg`: tezgâh ve maske.
- `tea.jpg`: demlik ve fincan.
- `lens_on.jpg`, `lens_off.jpg`: aynı kamera, lens açık ve kapalı.
- Önceki turun görüntüleri: yüz, kıyafetler, dolap, ışık öncesi ve sonrası.
