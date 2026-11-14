# Değişiklik manifestosu ve geri alma (2026-11-13)

Proje git kullanmıyor. Her ikili varlık yazımı kapılı çalıştırıcıdan (manifest233 + lock233) geçti; her biri için yazmadan önce
SHA1 doğrulamalı yedek alındı. Manifestler: `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/<ad>.json`.

## Toplu geri alma noktası
- `C:\Users\berat\SphirusCheckpoints\P0_Pre_20261113_1426` (+ `_sha1.txt`): P0 işi başlamadan önce oyuncu, ABP, giriş, gün
  istasyonu varlıkları.
- Harita yedekleri: `Saved/Codex/Motion_20261112/map_backup_p0w1/L_GR_SphirusHouse.umap` (kütük yüksekliği öncesi),
  `Saved/Codex/Motion_20261112/map_backup_atmo/L_GR_SphirusHouse.umap` (atmosfer adayı kurulmadan önce).

## Varlık değişiklikleri (sırasıyla)
| Manifest | Varlık | Betik | Ne değişti |
|---|---|---|---|
| day_p0_g4i_160833 | IA_Sph_Sprint (yeni), IMC_GR_SFGameplay | g4_input.py | Koşu/depar tuşları: Ctrl + gamepad LB yeni Sprint eylemine; eski Pace eşlemeleri boşaltıldı |
| day_p0_g4g_160837 | BP_HybridA_Player | g4_gait.py | Shift = gerçek jog (GASP Run), Ctrl = sprint; ev içi / iki el yükünde tempo yürüyüş; GR_RunBlock (0/1/2/3) okunur neden |
| day_p0_b1_161852 | BP_HybridA_Player | b1_back.py | S = kameraya dönmeden geri yürüyüş (GR_Back, strafe, dönüş hızı 150, hız ×0.85); havada durum korunur |
| day_p0_k15_162059 | AC_Sph_Camera | k15_headmargin.py | Eğilme/alma kadrajında baş kenar payı 4° / baş üstü 14 cm |
| day_p0_cr1_162259 | ABP_Sph_Body_GASP | cr1_crouch.py | Çömelme duruş katmanı (sırt yuvarlanır, kollar öne ve bükülü) |
| day_p0_cr2_173750, day_p0_cr2b_175053 | ABP_Sph_Body_GASP | cr2_values.py | Kol işaretleri (öne) düzeltildi |
| day_p0_cr3_190132 | ABP_Sph_Body_GASP | cr3_values.py | Çömelmede boyun −9°, baş −12° (göz hattı) |
| day_p0_l1_163626 | 6 yeni PSD_Sph_Stand_*_Lands_*_F + 12 klip kopyası (`/Game/Sphirus/Player/GASP/Lands/`) | l1_lands.py | İniş veritabanları yalnız ileri inişlerle; vendor DB'lere dokunulmadı (sayılar doğrulandı) |
| day_p0_w2_163843 | BP_GR_DayStation, BP_GR_SplitPiece | w2_firewood.py | Şömine kapısı Split ≥ 1; yerleştirme Split−2; parça otomatik alma yatay mesafe 70 cm |
| day_p0_w1_164056 (+harita yedeği) | L_GR_SphirusHouse (GR_Day_BlockLog z 165.2) | w1_blocklog.py | Kütük kütük üstüne oturur (alt 149.8 / kütük yüzeyi 149.5) |
| day_p0_d1_185937 | ABP_Sph_GASP | d1_dir.py | Update_MovementDirection deneysel olmayan dalda da çağrılır (geri yürüyüş seçici girişi) |
| day_p0_w3_205415 | BP_GR_SplitPiece | w3_piecetick.py | Parça görünür olduğunda aktör tick açılır (0.1 s) — otomatik alma artık çalışıyor |
| (atmosfer) bkz. README | L_GR_SphirusHouse (EX_Atmo_C1 klasörü, KAPALI) | atmo_c1.py build | Aday aktörler KAPALI kaydedildi; `atmo_c1.py remove` + harita yedeği ile geri alınır |

## Geri alma
- Tek varlık: manifestteki `backup` dosyasını editör kapalıyken `file` yoluna kopyala (SHA1 `sha1_before` ile doğrula).
- Atmosfer adayı: `ATMO_MODE='remove'` kapılı yazma işi (aktörleri siler, sis katmanı 2'yi yedekten geri yazar) ya da
  `map_backup_atmo` haritasını geri koy.
- Rejected Core Motion C profili yeniden açılmadı; iniş eşlemesi ABP'nin SphCM anahtarlarıyla yapıldı (önceki eşleme
  `Tools/Motion_20261112/l1_prev_map.json`).
