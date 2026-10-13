# REPRODUCE — aynı testleri yeni bilgisayarda tekrar kurma

Bu klasör **değiştirilmeyecek başlangıç kaydıdır**. Yeni bilgisayarda yeni bir klasör açın: `Saved/ChatGPTBridge/reports/hardware-quality-baseline-<YYYYMMDD_HHMM>/`, sonra iki raporu karşılaştırın.

Araçlar proje içinde: `Tools/HardwareQualityBaseline_20261013/` (salt ölçüm; hiçbir asset kaydetmez). Tüm yollar proje köküne göredir.

## 0. Karşılaştırılabilirlik ön koşulları (önce bunları kaydedin)
1. **Proje sürümü:** Content/Config/Plugins manifestini çıkarın ve bu kayıttakiyle karşılaştırın:
   `"<UE>/Engine/Binaries/ThirdParty/Python3/Win64/python.exe" Tools/HardwareQualityBaseline_20261013/manifest.py <yeni_rapor>/raw/preserve_manifest.json`
   ve `manifest.py --diff <bu_rapor>/raw/preserve_manifest_before.json <yeni>.json`. Fark varsa sonuçları **yalnızca donanıma bağlamayın**. (Bu manifest büyük ve kişisel yollar içermediği hâlde yerelde tutulur; GitHub'a yayımlanmadı.)
2. **Motor:** UE 5.8.1 (CL 56057345), Development Editor, DX12 SM6. Sürüm farklıysa not edin.
3. **Arka plan uygulamaları:** Bu kayıtta iki koşul var. **Faz 1** (18:20–19:17): Photoshop (Beta), Edge, 6× Fotoğraflar, Steam vb. açık; masaüstü uygulamaları GPU'da ~2.5 GB VRAM kullanıyordu, UE'nin VRAM bütçesi ~6.5 GB idi. **Faz 2** (19:17 sonrası): bu uygulamalar kapalı. Yeni makinede iki koşulu da ayrı ölçün ya da hangisinin geçerli olduğunu yazın.
4. **Güç:** prize takılı, Windows güç planı "Turbo" (ASUS), ekran 1920×1200 @165 Hz, DPI %125. Dizüstünde aynı güç modunu seçin.
5. **Ayarlar:** proje config dosyalarında değişiklik yok. Başlangıç cvar dökümü `inventory/cvars_A_initial.json` (215 cvar): sg.* = 3 (Epic), r.ScreenPercentage 0, TSR (AA 4), Lumen GI+Reflections (HW RT açık), VSM, Nanite, t.MaxFPS 0, VSync kapalı, dinamik çözünürlük kapalı, streaming pool 1000 MB.

## 1. Editörü başlatma (açılış süresi ayrı kaydedilir)
```
UnrealEditor.exe "<proje>/sphirus.uproject" -ExecCmds="py <scratch>/hqb_runner.py" -log=HQB_<tarih>.log
```
`hqb_runner.py` = `Tools/HardwareQualityBaseline_20261013/` altındaki işlerin çalıştırıcısı (oturumluk; kurulmaz). Bu kayıtta açılış 18:20:14 → motor hazır 18:22:38 → harita + runner hazır 18:24:21 (≈4 dk 7 s; DDC sıcak, shader derleme kuyruğu yoktu).
- Arka planda iki izleyici çalıştırın: `nvidia-smi --query-gpu=... -l 1 > raw/gpu_monitor_nvsmi.csv` ve 2 sn'lik sistem/UE bellek izleyicisi (`raw/sys_memory_monitor.csv` başlıkları). Komutlar README'de var.
- Editör görüntü alanı boyutunu kaydedin (`UnrealEditorSubsystem.get_level_viewport_size()`). **Bu kayıtta 1523×587 idi**; yeni makinede pencere düzeni farklıysa piksel sayısı farkı GPU süresini doğrudan değiştirir. Aynı boyutu ayarlayın ya da farkı raporlayın.

## 2. Statik kamera noktaları (editör görüntü alanı, oyun görünümü, PIE yok)
Noktalar `Tools/HardwareQualityBaseline_20261013/poses.json` (konum cm, pitch/yaw derece, FOV):
| Ad | Konum | Dönüş (P,Y) | FOV |
|---|---|---|---|
| P1_interior | (400, 700, 320) | (-8, -30) | 80 |
| P2_house_to_pond | (920, 2090, 238) | (-7, 120) | 78 |
| P3_pond_shore | (1500, 2810, 152) | (-6, 131) | 75 |
| P4_rear_trail | (2960, -1730, 419) | (10, -115) | 72 |
| P5_uphill_lookback | (3070, -2350, 540) | (-5, 122) | 68 |

Komut: `Tools/HardwareQualityBaseline_20261013/static.sh <A|C> <r1|r2|r3> <warm_s> <True|False>`. Her nokta için ısınma (ilk geçişte 15–20 s, sonra 12 s), ardından 12 s `csvprofile`. Ekran görüntüleri ayrı bir geçişte alınır (perf bittikten sonra, 1920×1080 HighResShot, force game view). Bu kayıtta A ve C üçer kez ölçüldü. B'nin editör görüntü alanında **uygulanamadığı doğrulandı** (aşağıya bakın).

## 3. PIE oturumları (gerçek oyun modu, gerçek karakter/kamera)
`pie.sh j_pie_<label>.py <label>`. İşler `mkjob.py <label> <A|B|C> perf` ile üretilir: 5 statik nokta (oyun dünyasında geçici CameraActor, 8 s ısınma + 10 s CSV), ardından iki rota × 3 tekrar:
- **R1_house_to_pond:** ev içinden (700, 850, zemin 150) başlar, veranda kapısından çıkar, verandadan iner, göl kıyısından (2620, 3900) noktasına gider. Yürüme, ~31.7 s.
- **R2_side_rear_trail:** evin yanından (1150, 1900) başlar, arka bahçeden yokuşa, (3110, -1800) noktasına gider. Yürüme, ~39.6 s.
Ara noktalar `routes.json` dosyasında. IA_Move ileri basılı tutulur; yön, kontrol yaw'u ile ara noktaya döndürülerek verilir. Kapılar haritada açık durumdadır.
- **B (yalnız iç çözünürlük):** PIE'de `r.Editor.Viewport.OverridePIEScreenPercentage 0` + `r.ScreenPercentage 50`. Oturum sonunda geri alınır.
- **C (hedef kalite):** `sg.GlobalIllumination/Reflection/Shadow/ViewDistance/AntiAliasing/PostProcess/Effects/Shading/Foliage/Landscape = 4`. Texture 3'te kalır. Uygulanan 74 cvar farkı `raw/static_C_r1.json` → `cvars_applied` alanında.
- **Kontroller:** `mkctrl.py` (`ctrl_B_uncapped`, `ctrl_A_sp100`, `ctrl_A_uncapped`, `diag_A_nofoliage`, `diag_A_novsm`).
- **Hareket paketi:** `mkmotion.py <label> <scen> <x> <y> <yaw0> [cvar_değer…]`; sabit giriş dizileri `motion_suite.py` dosyasında (M1–M9).

Her oturum sonunda betik tüm cvar'ları başlangıç dökümüne geri yazar ve farkı `cvars_after_restore_diff_vs_A` alanına kaydeder; bu alan boş olmalıdır.

## 4. Analiz
- `parse_csv.py <csv…>`: ortalama, medyan, p95, p99 kare/GPU/GT süreleri, takılmalar, VRAM ve streaming, GPU geçişleri.
- `analyze_motion.py raw/pie_<label>.json`: hız, durma, posture, ayak kayması, kamera.
- `summarize_env.py <rapor>`: her ölçüm penceresine GPU sıcaklık/güç/saat ve RAM bilgisini ekler.

## 5. Dikkat
- **PIE'de ~60 FPS sınırı gözlendi;** t.MaxFPS=0 iken de oluşuyor. Bu sınıra yaklaşan ölçümleri "sınırlanmış" olarak işaretleyin (kontrol oturumu sonuçları README'de).
- Editör RenderThreadTime CSV sütunu bu sürümde 0 okunuyor; kullanmayın.
- Uzun yol + uzun dosya adı MAX_PATH'i aştığında CSV kopyası başarısız olur; `hqb_common.P` mutlak yol kullanır.
- Görsel çiftler yalnızca aynı yakalama yöntemiyle karşılaştırılır.
