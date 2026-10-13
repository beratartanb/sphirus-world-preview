# Makine / proje / ayar envanteri (2026-10-13, gerçek sistemden okundu)

## Donanım ve işletim sistemi
| Alan | Değer | Kaynak |
|---|---|---|
| Model | ASUSTeK ROG Strix G614JV (dizüstü) | Win32_ComputerSystem |
| CPU | 13th Gen Intel Core i7-13650HX, 14 çekirdek / 20 iş parçacığı | Win32_Processor |
| RAM | 31.63 GB kullanılabilir; 2 × 16 GB SK Hynix DDR5-4800 | Win32_PhysicalMemory |
| GPU 0 (UE'nin kullandığı, ekranı süren) | NVIDIA GeForce RTX 4060 Laptop GPU, DeviceId 28e0, FL 12_2, SM 6.7 | UE log (D3D12 adapter 0, 1 çıkış) |
| GPU 1 | Intel UHD Graphics (iGPU, çıkışı yok) | UE log |
| Fiziksel VRAM | 8188 MiB (nvidia-smi); kayıt defteri qwMemorySize 8.585.740.288 B; D3D12 "dedicated" 7956 MB | nvidia-smi / registry / UE log |
| Paylaşılan sistem belleği (GPU) | 16192 MB (WDDM'in izin verdiği; fiziksel VRAM değil) | UE log |
| UE'ye verilen VRAM bütçesi | Faz 1: 6.51–6.58 GB; Faz 2: 7.03–7.19 GB | CSV `GPUMem/LocalBudgetMB` |
| GPU sürücüsü | 616.56 (32.0.16.1656), 2026-08-20 | nvidia-smi / UE log |
| GPU güç sınırı | Geçerli 140 W, varsayılan 100 W, en yüksek 140 W | nvidia-smi -q |
| GPU saati | Yükte 2520 MHz (en yüksek desteklenen 3105). Bellek 8101 MHz | nvidia-smi |
| PCIe | Yükte Gen4 x8 (boşta Gen1/2) | nvidia-smi |
| Disk | Crucial CT1000P3SSD8 1 TB NVMe. C: 930.3 GB, başta 176.7 GB boş. Proje, DDC ve pagefile aynı diskte | Get-PhysicalDisk / Get-Volume |
| Pagefile | Otomatik yönetilen; 20 GB → commit sınırı 51.7 → 62.3 GB'a büyüdü | Win32_PageFileUsage / izleyici |
| İşletim sistemi | Windows 11 Pro 10.0.26300 (26H2) | Win32_OperatingSystem |
| Güç planı | "Turbo" (ASUS) | powercfg |
| Ekran | 1920×1200 @165 Hz, DPI 120 (%125) | WMI / registry |
| Unreal | 5.8.1-56057345 (Release-5.8), Development Editor | CSV metadata / log |

## Eşzamanlı uygulamalar (test başı, 18:17)
- **RAM (private) toplamı ~30.9 GB**, UE kapalıyken. En büyükler:
  - Photoshop (Beta) 6.4 GB
  - msedge (36 süreç) 6.0 GB
  - claude (15) 4.7 GB
  - Fotoğraflar (6) 1.8 GB
  - Steam webhelper 1.1 GB
  - Kaspersky (avp) 0.9 GB
- **GPU'daki masaüstü süreçleri:** Photoshop, Fotoğraflar ×6, Edge, NVIDIA Overlay, Armoury Crate, ChatGPT, Spotify widget vb. UE kapalıyken GPU bellek kullanımı **2.5 GB**.
- **19:17 civarında** Photoshop, Edge ve Fotoğraflar kapandı (Faz 2). `inventory/machine_snapshot_midrun.json` dosyasında UE dışı en büyük süreç claude 3.9 GB.

## UE süreci belleği (UE ile sistem ayrı ayrı)
| An | UE working set | UE private commit | Sistem boş fiziksel | Sistem boş commit |
|---|---|---|---|---|
| Editör boşta (18:27) | 9.5 GB | 16.2 GB | ~4.2 GB | ~4.7 GB |
| C PIE rotaları (19:13–19:17) | — | 21.7–22.7 GB | 0.8–2.0 GB | 2.5–3.4 GB |
| Kapanıştan önce (20:16) | 6.1 GB | 23.8 GB | — | — |
| Standalone oyun (CSV PhysicalUsedMB) | 14.3–14.4 GB | — | — | — |

Ayrıntı: `raw/sys_memory_monitor.csv` (2 sn) ve `raw/gpu_monitor_nvsmi.csv` (1 sn).

## Proje
| Alan | Değer |
|---|---|
| Proje | `sphirus.uproject`; EngineAssociation 5.8; yalnız Blueprint (Black_Eye eklentisinde C++) |
| Eklentiler (uproject) | PythonScriptPlugin (Editor), ModelingToolsEditorMode, MotionWarping, AnimationWarping, PoseSearch, Chooser, MetaHuman, MetaHumanCharacter, MetaHumanGenerator, ModelContextProtocol, AllToolsets, NiagaraToolsets, PhysicsToolsets, LandscapePatch, MediaIOFramework, HairStrands, AlembicHairImporter |
| Varsayılan harita | `/Game/GraceRanger/Maps/L_GR_SphirusHouse` (+ alt seviyeler `L_SphirusHouse_ASSET_YARD`, `L_GR_CurrentHouseContent`) |
| GameMode | `BP_GM_GR_GraceRanger` |
| Haritadaki aktörler | 768; StaticMeshActor 670, PointLight 15, RectLight 12, Decal 13, Niagara 11, BP_SphirusHinged 8, Landscape 1, InstancedFoliageActor 1 |
| Foliage | 8.305 örnek (mesh bazında `inventory/editor_state.json`) |
| HiddenInGame aktörler | 4: `ReviewOnly_Ground`, `ReviewOnly_NeutralSky`, `GR_HomeIdentityVolume`, `AtticLadder_AAMS` |
| Content/Config/Plugins | 27.157 dosya, 96.1 GiB |

## Render ayarları (A)
Kalıcı ayarlar `Config/DefaultEngine.ini`'de:
- r.DynamicGlobalIlluminationMethod=1 (Lumen), r.ReflectionMethod=1, r.RayTracing=True, r.Shadow.Virtual.Enable=1, r.GenerateMeshDistanceFields=True, r.AllowStaticLighting=False.
- DX12 SM6, Desktop/Maximum.
- VT havuzları sabit (4/8/16 MB). `DefaultScalability.ini`: ShadowQuality@3 SMRT 12/8.

Canlı (editör) değerler:
- sg.* = 3, r.ScreenPercentage 0, r.Editor.Viewport.ScreenPercentage 100.
- r.AntiAliasingMethod 4 (TSR), r.TSR.History.ScreenPercentage 200, r.DynamicRes.OperationMode 0, t.MaxFPS 0, r.VSync 0.
- r.Nanite 1, r.Lumen.HardwareRayTracing 1, r.Lumen.ScreenProbeGather.DownsampleFactor 16.
- r.Streaming.PoolSize 1000 (LimitPoolSizeToVRAM 0), foliage.DensityScale 1, r.ViewDistanceScale 1.
- r.VolumetricFog 1 (grid 8), r.MaxAnisotropy 8, r.HairStrands.Enable 1.

Diğer:
- GameUserSettings: 1536×960 pencereli tam ekran, VSync kapalı, dinamik çözünürlük kapalı, FrameRateLimit 0.
- Editör görüntü alanı 1523×587; PIE görüntü alanı aynı (seçili görüntü alanında oynatma). PIE dünyası "max tick rate 60".
- Tam döküm: `inventory/cvars_A_initial.json`; C'de uygulanan farklar: `raw/static_C_r1.json` (`cvars_applied`).

## Profil farkları
README §4 tablosuna bakın.
