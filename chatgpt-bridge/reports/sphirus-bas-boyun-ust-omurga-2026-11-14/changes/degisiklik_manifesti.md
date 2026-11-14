# Değişiklik manifesti — baş/boyun/üst omurga (2026-11-14)

Tüm yazmalar kapılı çalıştırıcıdan (manifest233 doğrulanmış yedek + tek kilit sahibi, PIE kapalıyken) yapıldı. Vendor kaynakları,
yüz/beden mesh'leri, saç/kirpik/kaş groom'ları, malzemeler ve harita değişmedi. Yeni sistem, node veya kamera eklenmedi.

## Adım 1 — ayakta boyun taşıması (manifest `day_neck_apply_201111`)
Varlık: `/Game/Sphirus/Player/GASP/ABP_Sph_Body_GASP` (aktif `BP_HybridA_Player`'ın görünür beden anim blueprint'i)

| Değişken | Önce | Sonra |
|---|---|---|
| VI_Spine3 | (0,0,0) | (−4,0,0) |
| VI_Spine5 | (−9,0,0) | (−12,0,0) |
| VI_Neck1 | (0,0,0) | (12,0,0) |
| VI_Neck2 | (0,0,0) | (0,0,0) |
| VI_Head | (8,0,0) | (−2,0,0) |

SHA1 fc723769… → f2cfcfc6…  ·  Ek kopya: `%USERPROFILE%\SphirusCheckpoints\Neck_Pre_20261114\ABP_Sph_Body_GASP.uasset`

## Adım 2 — çömelme boyun taşıması + yüz/saç sınır kutusu (manifest `day_neck_apply2_230222`)
1. `ABP_Sph_Body_GASP` çömelme taşıması (ilk turdaki g1 tahmini de dahil, ölçülerek **değiştirildi**):

| Değişken | 2026-11-12 değeri | adım 1 sırasında (g1) | Sonra (t1) |
|---|---|---|---|
| VC_Spine5 | (7,0,0) | (4,0,0) | (−8,0,0) |
| VC_Neck1 | (−9,0,0) | (6,0,0) | (0,0,0) |
| VC_Neck2 | (0,0,0) | (−6,0,0) | (−6,0,0) |
| VC_Head | (−12,0,0) | (−14,0,0) | (2,0,0) |

2. `/Game/Sphirus/CharacterLab/Hazel_20261106/Playable/BP_HybridA_Player`: `Face`, `HairMain2`, `Eyebrows2`, `Eyelashes2`
   bileşenlerinde `Use Attach Parent Bound = true` (yalnız aktif oyuncu; üst sınıf BP_Sph_GASPCharacter değişmedi).
   Neden: bu bileşenlerin kendi sınır kutusu pozdan bağımsız olarak ayakta baş yüksekliğinde kalıyor (z 129–187 cm); çömelik /
   eğik baş (~100 cm) yakın kadrajda kamera görüş hacminin dışında kalan bu kutu yüzünden **yüz ve saç çiziminden düşüyordu**
   (başsız gövde). Artık beden kutusunu (−42…+194 cm, ölçek 1.6) kullanıyorlar.

SHA1: ABP f2cfcfc6… → d7305875…; BP_HybridA_Player 5431900f… → aafc4cef…  ·  Ek kopya:
`%USERPROFILE%\SphirusCheckpoints\Neck_Step2_20261114\` (adım 2 öncesi iki dosya + sha1.txt)

## Geri alma
- Editör kapalıyken (veya kapılı çalıştırıcının geri yükleme yoluyla) manifest yedeklerini geri koyun:
  - adım 2'yi geri almak: `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/day_neck_apply2_230222/Content/...` altındaki iki dosya;
  - adım 1'i de geri almak: `.../day_neck_apply_201111/Content/Sphirus/Player/GASP/ABP_Sph_Body_GASP.uasset`
    (= `SphirusCheckpoints\Neck_Pre_20261114`).
- Yalnız değer düzeyinde geri dönüş: yukarıdaki tablolardaki "Önce" değerlerini ABP varsayılanlarına yazmak yeterli.

## Çalışma anı / test araçları (oyuna girmez)
- `Tools/Neck_20261114/` (nk.py, nk3–nk10, q_*.py, bl_seam*.py, n_apply*.py), çıktılar `Saved/Codex/Neck_20261114/`.
- `Tools/Camera_20261112/vidc_neck.py` + `vidc.py` (kayıt aracı: kare başı boyun satırı, yan kamera hedef yüksekliği / kemik takibi).
  Önceki hâli: `Saved/Codex/Neck_20261114/vidc_before_neck.py`, `vidc_neck_before_bone.py`.
- Kullanıcı kayıt dosyası her batch'te kenara alınıp geri kondu: SHA1 4823d83a… değişmedi.
