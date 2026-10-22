# V2.23 değişiklik özeti (kod / graf / içerik / araç)

Bütün ikili varlık değişiklikleri editör üzerinden yapıldı. Her değişiklikten önce dosya kopyası alındı (`Saved/Codex/SHME_V223_20261022/checkpoint/`):
- `pre_a1/` — ABP'ler;
- `pre_gr/` — `BP_GR_Player`, profil, DA, `BP_PBI_Player`;
- `pre_cam/` — SHME bileşeni ve DA'lar;
- `pre_jr/` — dört döngü klibi;
- `pre_promo/` — üretime almadan hemen önceki durum;
- `tools/`, `tools_v1/*.v223a` — harness ve DSL kaynakları;
- `*.md.pre223` — skill dosyaları.

## Üretimde (V2.23)

### A1 — Tempolu geri koşu → ileri ters dönüş
- **`ABP_GR_MotionMatchingBase` / `SHM213_MontTick`** (DSL kaynağı `install_route_src.lisp`):
  - Yeni anahtar `SHM223_RevRearGate` (üretimde 1). Karakter kendi yüzüne göre geriye koşarken (hız·aktör ileri < −0.5) ileri koşu ters dönüş rotası (`SHM216_RevTurn_*`, depar için yazılmış koşu dönüş kavisi) devreye girmez.
  - Yeniden kurulumdan sonra V2.21 `LastHitBy` onarımı tekrar uygulandı.
- **ABP CDO:** `SHM_RedirectDB_JR` = `PSD_SHM_Redirect_JogReversalQ`. Bu V2.2 veritabanı geri→ileri tempolu pivotu (`SHM_DPP_Jog_Bwd_Pivot`) içerir, ileri koşu döngüsünü içermez.
- **İçerik:** `/Game/GraceRanger/SHME/Animations/Redirect/SHM_DPP_Jog_Bwd_Pivot` duruşu yerinde yeniden işlendi.
  - Sahip olunan kopya; yalnız P/Q veritabanlarında kullanılıyor.
  - Kaynak, satıcı orijinali `A_DPP_Jog_Bwd_Pivot` (değiştirilmedi).
  - Gövde eğimi fazlası 11° tabana kadar sınırlandı (klipte tepe 30.6° → 11.2°); itiş penceresinde kol sürüşü ×0.6; ayaklar ve kök birebir korundu (ayak hatası 0.0 cm).
  - Veritabanı önbellek anahtarı yenilendi: `PSD_SHM_Redirect_JogReversalQ` / `P` etiketi `SHME_V223_BWD2`.
  - Geri alma: `checkpoint/SHM_DPP_Jog_Bwd_Pivot.pre223.uasset`.
- **Kurulu ama kapalı:** `SHM223_JrHold` 0, tutma penceresi.

### C — Kamera: üretimde değişiklik YOK (V2.22 davranışı)
- **`BP_GR_Player.GR_CameraSafeOrigin`:** yatay ofset geçişi kuruldu ama anahtarı `GR223_PivotXY` 0. Bu fonksiyon önceden yalnız `(0, 0, Z)` döndürüyordu; 0 değeri bu davranışı aynen korur.
- **SHME (`SHM_UpdateCameraV21`):** algısal takip ve görüş yönlü look-ahead kodu kurulu, ama `CamFollowEnabled` false olduğu için etkisiz.
- **`DA_SHM_Response_Default`:** `CamBrakeCarry` 6 / `CamAccelCarry` 8 değişmedi.

## Kurulu ama kapalı adaylar (üretimde etkisiz)
- **Kamera adayı C** (`GR223_PivotXY` 1 + `CamFollowEnabled` + `CamBrakeCarry`/`CamAccelCarry` 0): ölçüldü, üretime alınmadı. Bkz. rapor bölüm 3.
- **`BP_GR_Player.GR_Impl_CP_PhysicalRedirect`:** `GR223_RevPushAccel` (0). Ters dönüşte sıfır geçişinden sonra ek itiş ivmesi; pencere ve tempolu hız sınırı `GR223_RevPushWin` / `VMin` / `VMax`. Pawn değişkeni: `GR223_RevAgainstT`.
- **İçerik:**
  - `/Game/GraceRanger/SHME/Animations/V223/SHM223_JogPiv_F_B`, `SHM223_JogPiv_B_F`, `SHM223_JogPiv_B_F_tw`.
  - `PSD_SHM223_JogReversal`.
  - Klipler 420 cm/s² itişli kapsül yoluna oturtuldu (timewarp + remap216).
  - Üretim veritabanlarına sızan miras BranchIn notify'ları temizlendi.
  - Dört döngü klibine (`A_CT_Jog_Bwd`, `A_RB_Jog_Rear`, `A_RB_Jog_RearLeft`, `A_RB_Jog_RearRight`) yalnız bu yeni veritabanı için bir BranchIn izi eklendi.

## Araçlar (`Tools/SHME_V223_20261022/`)
- **Tanı:**
  - `trace223.py`: kapsül / mesh / root / pelvis / görünür gövde / kamera konum yetkisi izi.
  - `rev223.py`, `win223.py`, `cad223.py` (hız–ritim–adım), `cam223.py` (kamera dünya yolu, ekran konumu, gecikme), `clipspeed223.py`, `paths223.py`.
- **Kurulum:**
  - `install_v223_reargate.py` (tutma penceresi dahil; LastHitBy onarımını otomatik uygular), `install_v223_revpush.py`, `install_v223_pivotxy.py`.
  - `v223_patch.py`, `v223_patch2.py`, `v223_build.sh`, `only_v223.py`.
  - `author223_jrev.py`, `promote223.py`, `verify_prod223.py`.
- **Harness:**
  - `qa_pie.py`: konum yetkisi alanları eklendi (`ax`, `avx`/`avy`, `mwl`/`mrl`/`mry`, `vwl`/`vwy`, `rmp`, `apv`).
  - `v212_run.sh`: yeni senaryolar `j23_*`, `c23_*`, `s23_*`; kamera cvar'ları.
  - `v223_ab.sh`: taban = V2.22 üretimi.
  - `lib223.sh`: bellek koruması yeniden başlatsa da sabit adım korunuyor; her grupta en yeni günlük okunuyor.

## Geri alma
- **A1:** ABP CDO'da `SHM223_RevRearGate` 0 ve `SHM_RedirectDB_JR` = `PSD_SHM_Redirect_JogReversal`. Ya da `checkpoint/pre_promo/ABP_GR_MotionMatching*.uasset` dosyasını editör kapalıyken geri kopyalayın.
- **C:** üretimde değişiklik yok. Adayı denemek için `GR223_PivotXY` 1 ve `CamFollowEnabled` true yapın.
- **Graf değişikliklerinin tamamı:** `checkpoint/pre_a1`, `pre_gr`, `pre_cam` (editör kapalıyken dosya kopyası).
