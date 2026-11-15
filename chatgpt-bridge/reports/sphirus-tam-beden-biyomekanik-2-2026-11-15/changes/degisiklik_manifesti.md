# Değişiklik manifesti — 2. tur (2026-11-15)

Net sonuç: üretim varlıklarında kalıcı değişiklik yok.

| # | Varlık | İşlem | Manifest | Sonuç |
|---|---|---|---|---|
| 1 | /Game/Sphirus/Player/GASP/Rig/RTG_Sph_UEFN_to_MH | "Stride Warp IK Goals" işlemi eklendi (yalnız bacaklar, yan kaydırma −3,5 cm) | day_bio_apply2_120056 | Ölçümde zararlı |
| 2 | aynı varlık | İşlem kaldırıldı | day_bio_revert3_224752 | SHA1 98c21e995affb034946bb5d647feb60f099200fa = 1. tur sonu |

Geri alma noktaları:
- Her iki yazmadan önce doğrulanmış yedek: `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/<manifest>/`
- 1. tur öncesi tam nokta: `%USERPROFILE%\SphirusCheckpoints\Bio_Pre_20261115\`

Yalnız çalışma anında (kaydedilmeyen) denemeler: saç fiziğinin açılması (probe_hair.py).

Araç değişiklikleri (varlık değil):
- `Tools/Camera_20261112/vc55.sh` video adımı Blender 5.3 sarmalayıcısına yönlendirildi (`Tools/Bio_20261115/bl.sh`).
- Yeni: `Tools/Bio_20261115/` altında an_slope.py, an_react.py, q_female.py, q_look.py, b_apply2.py, b_revert3.py,
  sheet.sh, sheet_full.py, bl.sh, bio4.sh, chain4–8.sh.

Kullanıcı kaydı: SHA1 4823d83a03259aafa78ad4ecbe56c14986ac8879 (değişmedi).
