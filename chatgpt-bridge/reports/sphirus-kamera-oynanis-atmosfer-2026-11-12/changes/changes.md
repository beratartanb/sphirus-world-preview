# Değişen varlıklar (2026-11-12, kamera yöneticisi)

Hepsi editör üzerinden, kapılı runner + yazma manifesti ve doğrulanmış yedekle (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/day_cam_*`). Tam geri dönüş noktası (sha1 listeli): `C:\Users\berat\SphirusCheckpoints\Camera_Pre_20261112_0215` (oyuncu, Sphirus/Player, GraceRanger haritaları, SF istasyonları, Config, kayıtlar; 215 MB). Harita dosyalarına dokunulmadı.

| Varlık | Değişiklik | Araç | Durum |
|---|---|---|---|
| `/Game/Sphirus/Player/Camera/AC_Sph_Camera` (yeni) | kamera, lens, odak ve algı katmanının tek sahibi; `CtxBegin` / `CtxHit` / `CtxEnd`, `ResPulse` / `ResStop` | `k1_comp.py` (yeniden çalıştırılabilir), `k1c_hit.py` | üretim |
| `/Game/Sphirus/Player/Camera/MPC_Sph_Perception`, `M_Sph_Resonance` (yeni) | rezonans parametreleri ve derinlikle sınırlı kırılma malzemesi | `k5a_res_mat.py` | üretim (0'da etkisiz) |
| `BP_HybridA_Player` | `SphCamera` bileşeni; Tick başında donanım ve bağlam aktarımı; eski kamera zinciri yalnız `SphCamera.Enabled = False` iken çalışır | `k2_pawn.py` | üretim |
| `BP_HybridA_Player` | `GR_Load2H` (taşıma montajı etkin): sprint yok, zıplama yok, tempo ölçeği 0,86; Cine lens bloğu: renk sapması 0,60 → 0,10, vinyet 0,38 → 0,28, gren 0,08 → 0,03, `M_Sph_Resonance` eklendi | `k6_pawn2.py` | üretim |
| `BP_GR_DayStation` | bakış kilidinden sonra `CtxBegin(self, GR_Kind, konum, GR_ContactT)`, temas dalından önce `CtxHit`, kilit kalkınca `CtxEnd` | `k3_stations.py` (day) | üretim |
| `BP_GR_DayHub` | yatak akışı: `CtxBegin(tür 9, GR_BedLoc)`, `CtxEnd` | `k3_stations.py` (hub) | üretim |
| `BP_GR_MaskBench` | `CtxBegin(tür 20)`, `CtxEnd`; ölü `GR_Hint` → `AddToViewport` çifti zincirden çıkarıldı (oyun sırasında 5115 çalışma zamanı hatası üretiyordu) | `k3_stations.py` (bench) | üretim |
| `BP_GR_MaskBench` | yerine yürürken her karede bakış yönünü yazan `SetControlRotation` düğümü zincirden çıkarıldı (etkileşim başındaki görüntü sıçraması ve ikinci yazıcı) | `k8_benchrot.py` | üretim |
| `BP_GR_SplitPiece` | `CtxBegin(tür 22)`, `CtxEnd` | `k3_stations.py` (piece) | üretim |
| `BP_GR_FirstBreak` | olay başında `ResPulse(1,0; 2,5 sn)`, sonunda `ResStop` | `k5c_break.py` | üretim |
| `SphCamera.Enabled` varsayılanı | False → True (bileşen sınıfı ve oyuncu şablonu) | `k7_promote.py` | terfi |
| `Tools/SHME_V2_20261014/v2_editor_launch.sh` | Windows eklenti DLL'ini engellediğinde (hata 4551) 15 dakika beklemek yerine hemen çıkıp yeniden denemeye izin verir; yedek `.bak_20261112` | elle | araç |
| `.agents/skills/sphirus-camera-direction/SKILL.md` | güncel kamera sahibi notu; Claude sarmalayıcıları eşitlendi | — | — |

Dokunulmayan: hareket (GASP Relaxed + sprint kilidi, `AC_Sph_Motion`, `ABP_Sph_GASP`, `ABP_Sph_Body_GASP`), karakter (baş, vücut, saç, kıyafet), Story Framework çekirdeği, kapılar, haritalar, ışık ve pozlama hacimleri, `BP_TrueLens`, `EX_Look_Resonance` hacmi (ağırlığı 0, kullanılmıyor), vendor varlıkları. Ham animasyon, satın alınmış `.uasset` ya da kayıt dosyası yayımlanmadı.

## Geri alma

1. Hızlı: `SphCamera.Enabled = False` (`Tools/Camera_20261112/_k7.txt` içine `off` yazıp `k7_promote.py`). Eski Tick zinciri kamerayı yeniden yazar. İstasyon bildirimleri etkisiz kalır.
2. Tam: iş başına manifest yedekleri (`day_cam_k1*`, `day_cam_k2*`, `day_cam_k3*`, `day_cam_k5*`, `day_cam_k6*`) ya da `Camera_Pre_20261112_0215` noktasından ilgili `.uasset` dosyaları. Yeni üç varlık (`AC_Sph_Camera`, `MPC_Sph_Perception`, `M_Sph_Resonance`) bu durumda silinir.

## Araçlar (`Tools/Camera_20261112/`)

`q_own.py`, `q_own2.py`, `q_lens.py` (sahiplik ve lens dökümü, salt okuma), `trace.py` (grafik dökümünden çalışma zinciri), `k1_comp.py` … `k7_promote.py` (kurulum), `vidc.py` + `vc55.sh` + `vcam3.sh` (oyuncu kamerasından gerçek hız kayıt; kadraj alanları), `an_cam.py` (kadraj ölçüleri), `mk_tables.py` (A/C tabloları), `sim_comp.py`, `sim_work.py` (kayıtlı pozlar üzerinde kadraj benzetimi), `lum.py` (pozlama), `perf_cam.sh` + `an_perf.py` (kare maliyeti), `q_final_cam.py` (temiz açılış denetimi).
