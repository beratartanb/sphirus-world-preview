# SHME V2.55 değişiklik listesi

Her yazma işlemi `Tools/SHME_V2_20261014/run_v2.sh` üzerinden, manifest ve doğrulanmış yedekle yapıldı. Bütün davranış düğmelerin arkasındadır. `SHM255_Ctl` 0 ve `GR255_RawOn` 0 iken V2.54 davranışı aynen çalışır. Satıcı varlıklarına, CoreMotion orijinallerine ve `/Game/CoreMotion_Retargeted` altına yazılmadı.

## Kontrol

| dosya | değişiklik |
|---|---|
| `install255_pawn.py` | Ham tuş değeri `IA_Move`'dan, herhangi bir çerçeveye girmeden okunuyor (`GR255_RawX/Y`, `LocoRawYaw`). V2.28'in `Velocity = ActorForward × ClipSpeed` yazımının üzerine `ClipDir` geliyor: klip süresince hareket artık gövde eksenine kilitli değil. |
| `install255_route.py` | Bütün eski ailelerin (JogRev, LoadRev, SlowRev, BackLink, geri koşular) önünde tek dönüş rotası. 20–150° arasında istenen taraf, 180° yakınında destek ayağı tarafı seçer. |
| `install255_abp.py` | Canlı hedef: plan süresince hedef her kare tuştan okunuyor, V2.54'ün 120° üstü işaret zorlaması kalktı. İptal artık 75° hataya değil niyete bağlı: tuş .1 s bırakılırsa, eski yönün 45° içine dönülürse veya klibin öbür tarafına geçilirse. Küçük düzeltme iptal etmiyor, yönlendiriyor. İptalde eski klip oynamaya devam etmiyor. |
| `install255_cut.py` | Sert 90° değişim aynı rotada. |
| `install255_v3.py`, `v5`, `v7` | Bedava hız yok: plan hiçbir evrede kapsülü hızlandıramıyor. Sınır gövde ekseni bileşenine değil doğru büyüklüğe uygulanıyor. |
| `install255_v4.py` | Fren hızı sınırı. |
| `install255_v5.py`, `v6` | Plan durumu harmanlanmış eğrilerden değil, saklı durumdan okunuyor. Plan sonu tek karelik saklı olay. Yürüyüş kademesi eklendi, ama yürüyüşte W→S davranışını değiştirmedi. |
| `shm_src.py:1493` | `lrun` eşiği 250→150. Eski eşik plan çıkış hızının üstündeydi, fare hareket ederken koşu çerçevesi düşüp strafe kliplerine geçiyordu. |
| `DA_SHM_Response_Default` | `EffortScaleMin` .70→.85. Eski değer ivmeyi %30 kesiyor, azami hızı 416'ya düşürüyordu. |

## Bacak ve animasyon

| dosya | değişiklik |
|---|---|
| `gen255_turn.py` | Sentezlenen bacak yerine gerçek kadın hareket yakalama bileşimi: `af_Loco_<Gait>_Fwd_Stop` freni + `af_Loco_<Gait>_Start_Turn<S><ANG>_<S>foot` pivot ve itiş. Geçiş pivot ayağının basışında. Ayak topu duruşta sabit, ofseti salınım taşıyor, bacaklar yeniden çözülüyor. |
| aynı dosya | `swing_clear`: salınan ayak kendi duruş seviyesinin altına inmiyor. `knee_align`: yüklü diz ayak ucunu izliyor. `arm_k`: kol taşıması. 90° kesişlerde fren klibi ortadan giriyor. |
| `build255_db.py` | `/Game/GraceRanger/SHME/Animations/V255/` altında `PSD_SHM254_T255_*` veritabanları: SprintR/L, JogR/L, JogB, CutR/L, JogCutR/L. |

Eski ters dönüş rotaları `PSD_CT_JogSteady` ve `PSD_SHM233_SprintCalm` ile emekliye ayrıldı.

## Kamera ve üst gövde

| dosya | değişiklik |
|---|---|
| `install255_frame.py` | GraceRanger donanımı içinde hız çerçevesi. Yeni kamera sistemi yok. Tek sinyal `GR255_FrameK`, mesafe (+%30), hedef noktası (−26 cm) ve lens eğimini (−8°) birlikte sürüyor. Lens eğimi denetim dönüşüne dokunmuyor, bu yüzden hareket hedefini değiştirmiyor. `GR255_FrameV1` 320. İç mekânda `CamOpenness` ile kapanıyor. |
| ABP `SHM240_HeadOn` | AO kafa ve omuz katmanı açık. Dönüşten sonra omuzların eski kamera yönüne burulması sprintte −23.5°→+.8°. |

## Araçlar

`Tools/SHME_V255_20261104/`: `dir255.py`, `dm255.py`, `dmrep255.py`, `fz255.py`, `score255.py`, `mid255.py`, `poptab255.py`, `where255.py`, `clipdump255.py`, `clipstat255.py`, `pelv255.py`, `cross255.py`, `knee255.py`, `twist255.py`, `sheet255.ps1`, `promote255.py`.

`Tools/SHME_V212_20261017/v212_run.sh`: gerçek eğim ve duvar senaryoları `t255_ramp_s`, `t255_ramp_j`, `t255_ramp90_s`, `t255_rampd_s`, `t255_wall_c`.

## Beceriler

`sphirus-motion-synthesis` (yakalama bileşimi), `sphirus-natural-motion` (V2.55 kullanıcı inceleme kuralları), `sphirus-camera-direction` (hız çerçevesi). `sync_claude_skills.py` hatasız geçti.
