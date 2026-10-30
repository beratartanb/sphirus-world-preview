# SHME V2.38: değişiklikler (V2.37 fcc85e2 üzerine)

## Üretim

Temiz açılışta VERIFY238 kontrolü yapılır. Bu yalnız bir yapılandırma kontrolüdür, hareket kabulü değildir.

Bütün değişiklikler ABP sınıf varsayılanlarıdır. Grafik yamaları önce kapalı kuruldu, sonra bu düğmelerle açıldı. V2.37 klipleri ve veritabanları değişmedi.

| Grup | ABP değişkeni | Yeni değer | Geri dönüş |
|---|---|---|---|
| `cut` | `SHM210_JogCutMode` | 1: tempolu yan bölüm artık atlanmıyor | 0 |
| `cut` | `SHM_RedirectDB_JL` | `V238/PSD_SHM238_JogCut` (48 fizik planlı 90° bölmesi, bias −25) | `Redirect/PSD_SHM_Redirect_JogLateral` |
| `cut` | `SHM238_Yaw` | 1 (aşağıdaki dört davranış) | 0 |
| `cut` | `SHM238_GuardS` | 1.6 s | 0.8 |
| `gaze` | `SHM238_Gaze` | 1 (kamera arkaya dönmeyi beklerken bakış harekete) | 0 |

`SHM238_Yaw` = 1 olduğunda dört şey açılır:
- **Klibe bağlı yön:** kapsülün yönü klibin planladığı dönüşü izler (`ClipYaw` / `ClipYawOn`, GR yazar).
- **Hattın tutulması:** dönüş bitene kadar bölüm ve veritabanı tutulur.
- **Toparlanma ailesi koruması:** plan çalışırken yanlış "itilme" toparlanması devreye girmez.
- **Yürüme koruması:** yürüme yan bölümü eskisi gibi atlanır (walk / walk2 / walk3 yamaları da `SHM238_Yaw` arkasında).

Geri dönüş (tek komut): `promote238.py`, `{'rollback': True}`. Değerler `PROMO238` çıktısında.

## Yeni içerik (`/Game/GraceRanger/SHME/Animations/V238/`)

| Varlık | Kaynak | Açıklama |
|---|---|---|
| `SHM238_Cut_{R\|L}_P00..P23` | `gen238_cut.py` | Tempolu 90° sert dönüş, döngünün 24 evresinin her biri için. Kare 0 = istek anındaki döngü pozu. |
| `PSD_SHM238_JogCut` | `build238_cutdb.py` | 48 klip. Tam pencere BranchIn, continuing bias −25 (V2.37 evre sıçraması dersi). Şema `PSD_SHM_Redirect_JogLateral`'dan. |

**Klip eğrileri:**
- `SHM226_V/W`: V2.28 hız sözleşmesi.
- `SHM238_Turn/W`: V2.38 yön sözleşmesi. İkisi birlikte sıfıra iner.
- `SHM237_FPPelvisOff`: frende pelvis klipte.
- Döngünün kendi eğrileri.

### Üreteç (`gen238_cut.py`), kısa
- **Temas sırası:** isteğe en yakın iniş doğal zamanında olur, bekletme yok. Hangi ayağın indiği planı belirler.
  - Dış ayak ve yeniden hedefleme zamanı varsa: `plant` → `transfer` → `push`.
  - İç ayaksa: önce hafif çapraz bir fren adımı (`brake`), sonra `plant`.
  - Dış ayak çok erken iniyorsa: zayıf plant (`weak`), sonra `transfer`.
  - İlk inişin yeniden hedeflenme payı (`aim`), kalan salınım süresiyle 0.06 → 0.26 s arasında 0'dan 1'e çıkar.
- **Hız ve yön:** temas başına itme bütçesiyle temaslar boyunca simüle edilir.
  - Kesme 0.55 g, iç ayak freni 410 cm/s², yeniden hızlanma 300 cm/s².
  - Kuvvet yönü ayaktan kütle merkezine. Bu yüzden plant ayağı istenen ivmenin tersine, öne ve dışa konur.
- **Beden katmanları:**
  - baş yeni yöne önden döner;
  - göğüs pelvisi önden götürür;
  - fren payıyla gövde geriye, yanal ivmeyle içe eğilir (`atan(a/g)` × 0.55);
  - fren payıyla kol salınımı söner;
  - katman girdileri ±0.13 s merkezli yumuşatılır.
- **Pelvis:** yalnız bacak erişimi kadar iner, plant'ta ≤ 1.8 cm sönümleme var.

## Grafik yamaları (`Tools/SHME_V238_20261030`, hepsi knob arkasında)

| Kurulum | Varlık | İş |
|---|---|---|
| `install238_yaw.py` | Bileşen, ABP `SHM_Snapshot`, `BP_GR_Player.GR_Impl_CP_PhysicalRedirect` | Klibin `SHM238_Turn` eğrisi aktör yönüne yazılır. İlk karede başlangıç yönü ve istenen açı alınır, sonra bir kare ileriye bakılır. GR, V2.28 hız dalında hız yazımından önce bunu `SetActorRotation` ile uygular. |
| `install238_fam.py` | ABP | Planlı klip pozdayken toparlanma aileleri 1/6 yok sayılır. |
| `install238_hold.py` | ABP | Dönüş bitene kadar bölüm ve veritabanı tutulur. Klipten sonra `SHM238_GuardS` boyunca aile koruması sürer. |
| `install238_walk.py`, `install238_walk2.py`, `install238_walk3.py` | ABP | Yürüme yan bölümü eskisi gibi atlanır. Koşul: yalnız bileşen bölümü aktifken, sınıfı yan (≤ 1.5, ters dönüş değil), ABP bölümü henüz başlamamış ve başlangıç hızı < 220 cm/s. İlk iki sürüm geniş kaldı: ters dönüşü (j35_rev 34 cm) ve bölüm dışı döngü girişlerini bozdu. Final kanıtı walk3 ile. |
| `install238_gaze.py`, `install238_gaze2.py` | ABP | Kamera arkaya dönmeyi beklerken (`CamRecState` 1–3), inceleme hedefi yokken ve 150 cm/s üstünde, mevcut LookAt zinciri harekete bakar. Ağırlık yumuşatılır (4/s). Vendor `LookAtAimOffset` katmanına dokunulmadı. |

## Reddedilen / üretime alınmayan
- **Depar 90° ailesi:** aynı plan depar (494 cm/s) için 8 temas ve ~2 s istiyor, pelvis 10–15 cm iniyor. Deparın kendi önce-fren tasarımı gerekiyor. Üretilmedi.
- **NVIDIA modelleri (MotionBricks / Kimodo / ARDY / ProtoMotions):** indirilmedi, denenmedi. Gerekçe `research/research_v238.md` ve raporda.

## Araçlar

| Araç | İş |
|---|---|
| `balance238.py` | Tek koşudan, aynı karelerde ağırlık merkezi (Dempster/Winter), XCoM, destek, temas başına dv, pelvis/göğüs/baş yönü |
| `gen238_cut.py`, `stick238.ps1` | Fizik planlı kesme üreteci; oyun dışı çubuk/üst görünüm |
| `build238_cutdb.py` | Kesme veritabanı |
| `install238_*.py` | Yamalar (yukarıda) |
| `promote238.py`, `verify238.py` | Üretime alma, doğrulama |
| `tables238.py`, `media238.sh`, `manifest238.py`, `v238_ab.sh`, `ab_safe238.sh` | Tablolar, kayıt, manifest, A/B |

## Geri dönüş
- **Düğmeler:** `promote238.py`, `{'rollback': True}`.
- **İkili yedekler:** `Saved/Codex/SHME_V238_20261030/checkpoint/manifests/<ad>/`, yayımlanmadı.
  - `yaw1`, `fam1`, `hold1`, `gaze1`, `gaze2`, `walk1`, `walk2`, `walk3`, `promo1`: ABP / bileşen / GR, her kurulumdan önce.
  - `cut1..cut4`, `db1`: klipler ve veritabanı.
