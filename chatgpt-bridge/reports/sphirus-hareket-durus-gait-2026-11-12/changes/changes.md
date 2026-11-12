# Değişiklik listesi — hareket, duruş, gait (2026-11-12)

Checkpoint (dosya kopyası, git yok): `C:\Users\berat\SphirusCheckpoints\Motion_Pre_20261112_1200` (352 dosya, SHA1 listesi yanında).
Her yazma işi ayrıca kapılı çalıştırıcının manifest yedeğiyle alındı (`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/day_mot_*`).

## Değişen varlıklar

| Varlık | Değişiklik | Betik |
|---|---|---|
| `/Game/Sphirus/Player/Input/IA_Sph_Pace` (yeni) | Yürüme modu ↔ koşu modu anahtarı (Boolean) | `Tools/Motion_20261112/i1_input.py` |
| `/Game/GraceRanger/Input/IMC_GR_SFGameplay` | `IA_Sph_Pace` → Sol Ctrl, gamepad sol omuz (ikisi de boştu) | `i1_input.py` |
| `BP_HybridA_Player` (etkin oyuncu) | Gait merdiveni (GR_Pace, GR_Tempo, GR_GaitSel yeniden), bağlam hız ölçeği tablosu, zıplama: gait'e göre kalkış hızı + ileri taşıma, CMC yerçekimi ölçeği 1.0 → 1.25 | `g2_gait.py` |
| `BP_HybridA_Player` | `GR_Load2H` = odun kucağı **veya** maske taşıma (iki elli yük: koşu ve zıplama yok) | `g3_maskload.py` |
| `/Game/Sphirus/Player/Motion/AC_Sph_Motion` | Yavaş yorgunluk `Fat` (uzun koşu), yorgunken ivme ×(1−0.15·Fat), iniş anında göğüs yayına tekme; düz giderken üst gait'e geçişte ivme ×0.55 | `m1_fat.py`, `m2_gaitup.py` |
| `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP` (görünen beden) | Duruş katmanı (13 kemik, bileşen uzayında toplamsal), havada adım katmanı (6 kemik), iniş/duruş eğim sınırlayıcı (2 kemik), baş bakış dengesi (LookAt), yorgunlukla nefes genliği/hızı; değerler sınıf varsayılanı | `p1_posture.py`, `p3_air.py`, `p4_land.py`, `p4b_land.py`, `p5_headlevel.py` (baş düzleme), `p2_values.py` (+`cand_C3.py`) |
| `/Game/Sphirus/Player/Camera/AC_Sph_Camera` | Havadayken dikey izleme hızlı (pivot 5 → 25/sn, baş yüksekliği 2,5 → 8/sn); yerde değişiklik yok | `k9_jumpcam.py` |

Değişmeyenler: klipler, Motion Matching veritabanları, retarget varlığı (`RTG_Sph_UEFN_to_MH`), sürücü ABP (`ABP_Sph_GASP`), istasyonlar, satıcı (vendor) dosyaları. Core Motion C profili kapalı kaldı. Yeni animasyon paketi yok.

## Geri alma
- Tek varlık: ilgili `day_mot_*` manifestindeki yedek, editör kapalıyken geri kopyalanır.
- Tümü: `Motion_Pre_20261112_1200` checkpoint'i (Content/Sphirus/Player, Hazel Playable, GraceRanger/SF); giriş eşlemesi `IMC_GR_SFGameplay` için `day_mot_i1` manifest yedeği (yeni `IA_Sph_Pace` silinebilir).
- Duruş katmanını kapatmak için tüm `VI_/VR_/VA_/VE_/VJ_` vektörlerini sıfırlamak ve `HeadIdle/HeadWalk/HeadRun` = 0 yeterli (katman nötr).

## Araçlar (`Tools/Motion_20261112/`)
`an_body.py`, `an_post.py` (duruş ölçüleri), `an_effort.py` (efor), `vmot3.sh` (düz harita: yan/ön/arka/gait/zıplama/efor), `vflow.sh` (gerçek harita akışları), `vmask.sh` + `vc55s.sh` (maske taşıma, eski test kaydından), `reg_save_m.sh` (kayıt/yükleme sonrası hareket), `q_ref2.py` (referans poz), `cand_C1..C3.py` (aday değerler).
