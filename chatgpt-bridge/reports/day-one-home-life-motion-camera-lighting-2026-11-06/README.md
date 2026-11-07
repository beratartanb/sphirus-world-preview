# SPHIRUS: ilk gün, karakter, kamera ve ışık

Tarih: 2026-11-07. Motor: UE 5.8.4-58902052. Harita: `/Game/GraceRanger/Maps/L_GR_SphirusHouse`. Oyuncu: `BP_HybridA_Player`.

## Sonuç

**İlk günün oyun zinciri ana haritada çalışıyor, ama brifin tamamı bitmedi.** Yeni oyundan uyanma, dolap, kıyafet, bitki, odun, kesme, şömine ve çay aynı koşuda E tuşuyla tamamlandı. Görevler ve kayıt doğru ilerledi.

**Görsel kalite birçok yerde taslak düzeyinde.** Şöminede alev görünmüyor. İstasyonlarda karakter duruş noktasına anında taşınıyor. Üretilen animasyonlar kısa ve geçici.

**Başlanmayan işler:** genel hareket, tezgâh çarpışması ve parmak teması, evin dış ve iç düzeni. Tam liste aşağıda.

| Başlık | Durum |
|---|---|
| Karakter gövdesi | PASS (teknik). Body Female reddedildi, tam yüzeyli Hazel kullanılıyor |
| Yüz | PARTIAL. MetaHuman içinde yeniden kuruldu, referans benzerliği kabulü sende |
| Baş ve gövde birleşimi | PASS (görüntü). Aynı karakterden kuruldu, ten tonu eşlendi |
| Ten ve doku | PARTIAL. Çil, ton ve lekelenme eklendi. Yüz ana dokusu 2048 px |
| Kıyafetler | PARTIAL. 5 set ve 18 kemer bağlı. Kumaş simülasyonu yok |
| Yakın koşu kamerası | PARTIAL. Koşuda uzaklaşma kaldırıldı, açık alanda tam koşu ölçülmedi |
| Yatak ve uyanma | PARTIAL. Yeni oyunda oynuyor, ara pozlar kaba |
| Fiziksel dolap | PARTIAL. Kapak açılıyor, askılar seçiliyor, giyinme animasyonlu |
| Odun, kesme, istif | PARTIAL. Sayılar ve görünüm çalışıyor, balta görüntüde doğrulanmadı |
| Şömine | FAIL (alev). Işık ve durum çalışıyor, alev görünmüyor |
| Bitki ve çay | PARTIAL. Zincir çalışıyor, sıvı ve fincan yok |
| Kayıt | PASS. Yeni kayıt ve eski kayıt yüklendi, çoğalma yok |
| PBL ve True Lens | PARTIAL. Sabah ışığı ve hafif profil uygulandı, PBL verisi kullanılmadı |
| Genel hareket | NOT_DONE |
| Tezgâh çarpışması, parmak teması | NOT_DONE |
| Ev içi ve dışı düzen | NOT_DONE |

## Doğrulanan paketler

| Paket | Tür | Kullanım |
|---|---|---|
| Body Female (09sats) | 6,4 milyon yüzlü heykel, rig ve UV yok | Denendi, kullanıcı bacak ve bilek yüzünden reddetti |
| Messy Bob | MetaHuman groom | Oyuncuda |
| Pants 70 | MetaHuman outfit | Oyuncuda |
| Relaxed Cuffed Shorts | MetaHuman outfit | Oyuncuda |
| Cargo pants | Downloads klasöründeki mhpkg | Oyuncuda |
| Male Tank Top | Projede kurulu | Oyuncuda. Ad "male", kadın gövdesine uyarlandı |
| Retro top blue | Projede kurulu | Oyuncuda |
| Female belt pack | 18 durağan kemer, doku dosyası yok | 18'i de projede. Proje deri malzemesi kullanıldı |

## Karakter

- **Gövde:** `SKM_MHC_SphFace_BodyMesh`, Hazel'in kıyafetsiz kurulumu. Outfit seçiliyken MetaHuman altındaki yüzeyi siliyordu; pelvis boşluğunun nedeni buydu. Eklemler önceki Hazel ile aynı.
- **Yüz:** Blender'da yapılmış GD38 yüzü kaldırıldı. Yeni yüz Hazel'in MetaHuman yüzünden başladı, `translate_face_landmarks` ile çalışıldı, Epic otomatik rig servisiyle rig'lendi. Alt yüz kısaldı, çene ve yanak inceldi, burun ve dudak yeniden şekillendi. Mesh farkı küçük: önceki denemelerde en çok 0,34 cm ölçüldü.
- **Fotoğraf:** MetaHuman yüz takipçisi Messy Bob fotoğrafında yüz bulamadı. Oranları gözle çalıştım, bindirme ölçümü yok.
- **Rig testi:** Göz kırpma, ağız ve ifade bozulması ayrıca test edilmedi. Yüz `ABP_Face` yerine gövdeyle oynuyor mu kontrolü yapılmadı.
- **Saç:** Messy Bob yüze yeniden bağlandı, ton koyulaştırıldı. LOD ve hareket maliyeti ölçülmedi.

## Kıyafetler

Beş set `GR_OutfitTop`, `GR_OutfitLow`, `GR_OutfitBody`, `GR_OutfitBelt` dizilerinde. Yeni kıyafet için yeni satır yeterli.

| No | Set | İçerik |
|---|---|---|
| 0 | Gece | Atlet ve şort. Kullanıcının gece seti gelene kadar geçici |
| 1 | Ev | Retro üst ve şort |
| 2 | Gezi | Retro üst, pantolon, kemer |
| 3 | Ev B | Atlet ve şort |
| 4 | Gezi B | Atlet ve kargo |

`GR_SetBelt` 18 kemerden birini seçer. Dolapta kemer seçimi yok. Kıyafetler gövdeyle aynı iskelette, kumaş simülasyonu kapalı. Eğilme ve oturma pozlarında kumaş batması taranmadı.

## Kamera

`DA_GR_LocomotionBehavior`: yürüyüş kolu 128, koşu 124, sprint 120, omuz 44, FOV 60/63/66. V2.55 koşu açılması sıfırlandı.

Ölçüm: durağan 175 cm, yürüyüş 159 cm, koşu anı 153 cm, FOV 66. Koşu ölçümü sırasında karakter bir ağaca takıldı, yani temiz bir açık alan koşusu değil. Gerçek kol uzunluğu profil değerinin üstünde kaldı. Bunun sahibi bulunmadı.

## İlk gün

Yeni parçalar `/Game/GraceRanger/SF/Day/` altında: `BP_GR_DayHub`, `BP_GR_DayStation`, `BP_GR_DayBoot`, 8 klip, dolap ve askı modelleri.

Son rota, yeni oyun, gerçek E girdisi (action injection). Karakteri istasyona test komutu götürdü, yürüyüş test edilmedi.

| Adım | Sonuç |
|---|---|
| Uyan | Görev "Güne hazırlan" eklendi |
| Dolabı aç, Gezi setini seç | Kıyafet değişti, görevler eklendi |
| Dolabı kapat | Kapak kapandı |
| Bitki topla | Herb 1 |
| Odun topla | Wood 1 |
| Kes | Wood 0, Split 2 |
| Şömine: odun koy, yak | Split 0, Fire 2 |
| Çay: demle, iç | Herb 0, Tea 2 |

Kayıt: yarım ilerlemeli kayıt sayıları geri getirdi, toplanan nesneler geri gelmedi. Eski maske kaydında maske aşaması 2 korundu, oyuncu yatağa dönmedi.

Bilinen sorunlar:

- İstasyona geçişte karakter duruş noktasına anında taşınıyor. Brifte istenmeyen bir şey.
- Kapıya uzanma klibi elle kulp temasını doğrulamadı.
- Balta `hand_r` bağlı, ama çekimde görünmedi. Kesme anında yonga yok, ses geçici.
- Odun kesilince parçalanma nesnesi yok; sadece istif artıyor.
- Şömine: Niagara etkin görünüyor, ama iki farklı alev sistemiyle de görüntüde alev çıkmadı. Duman ve buhar sistemi çalışıyor.
- Çayda bardak, sıvı ve su adımı yok. Tek bitki türü olarak çiçek modeli kullanıldı.
- Yeni oyun uyanması yalnızca kayıt dosyası yoksa başlıyor. Menüden "yeni oyun" yolu test edilmedi.

## Işık ve performans

Sabah ışığı: güneş açısı -24, sıcaklık 4700 K, şiddet 1450, gökyüzü 1,15. Değerleri gözle seçtim, PBL veritabanından sayı almadım.

True Lens: yalnız vignette ve hafif grain açık. Ayrı lens A/B görüntüsü yok; karşılaştırma ışık ve lensi birlikte gösteriyor.

**Önemli bulgu:** True Lens'in Tick'i `t.MaxFPS 24` yazıyor ve oyunu 24 FPS'e kilitliyordu. Tick açılışta kapatıldı. Bu, zamana bağlı lens etkilerini durdurabilir.

| Nokta | Kare süresi | VRAM |
|---|---|---|
| Oda | 23,8 ms | 6837 MB |
| Ön | 36,0 ms | 6802 MB |
| Kıyı | 35,4 ms | 6775 MB |
| Arka | 34,0 ms | 6775 MB |

Önceki ölçüm 22,6-34,7 ms ve yaklaşık 6530 MB idi. Tek koşu; sonraki küçük ışık ve kütük değişikliklerinden önce alındı. Disk boşluğu 48 GB'a düştü.

## Yapılmayanlar

- Genel hareket: kol salınımı, ağırlık, pivotlar, `fz_walk_a`.
- Tezgâh çarpışması, duruş noktası, başparmak teması.
- Ev dış ve iç düzeni, patikalar, kullanım izleri, PCG dışlama.
- İç ve dış ses, kıyafet sesleri.
- Gamepad, gerçek merdiven, tepe rotası, 30/60 FPS taşıma testi, paketlenmiş oyun.
- Görev sırası değiştirilmiş ikinci rota, menüden kayıt, iptal ve hızlı tuş testleri.
- Video kanıtı ve Bridge siyah kameraları.

## Satın alma ihtiyacı

Şimdilik yok. Gece seti için kullanıcının eklemesi beklenen kıyafet hâlâ geçici atletle gidiyor.

## Geri alma

- Oyuncu: `day_*` manifestleri, `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/`.
- Harita ve ev alt seviyesi: `grip_maps_084604` ve `grip_map_*`.
- Kamera profili: `day_cam3_070627`.
- Kullanıcı kaydı: `Saved/Codex/Day_20261107/SFSaveSlot_user.sav`. Çalışma sonunda aynı dosya yerine kondu.
- Eski dolap ve `HearthGlow` silinmedi, gizlendi.
- `Content/Sphirus/CharacterLab/Day_20261107` içinde kullanılmayan denemeler var (Body Female kurulumları). Silinmedi.

## Kanıt

`evidence/`: yüz, oyuncu kamerası, dolap, rota, ışık öncesi ve sonrası, kıyafetler, yatak.
