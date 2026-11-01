# SHME V2.42 — Reliable Human Motion Foundation & Locomotion Identity (2026-11-01)

Taban: V2.41 üretimi (`VERIFY241 ALL_OK`, temiz editör). **Üretim davranışı değişmedi**: her yeni parça bir anahtarın arkasında, varsayılanı V2.41 (son kurulumdan sonra `VERIFY241 ALL_OK`, CDO probları). Hiçbir satıcı asset'i düzenlenmedi; yalnız yeni paketler (`/Game/GraceRanger/SHME/Animations/V242/*`) ve ABP/pawn anahtar yamaları (manifest + doğrulanmış yedek). Harness: `lib242.sh` / `vars242.sh` / `vars242_cap.sh`, senaryolar `w42_id`, `j42_lr_p10`. Detay: `CHANGES_V242.md`, sayılar: `TABLES_V242.md`.

Bu tur **sonuç odaklı** kuruldu: önce tek bir kırık hareket (yanal fren/duruş) kaynaktan oyuna kadar tamamlandı, sonra FPS matrisine genişletildi; identity için üretim önce ölçüldü, sonra içerik üretildi ve entegrasyon sahibi bulundu.

---

## AŞAMA A — Güvenilirlik: doğrudan cevaplar

**1. Yanal fren/duruş için hangi yeni gerçek hareketler üretildi?**
`gen242_latstop.py`: V2.37 temas-planlı duruş yöntemi (fren saati, duruş ötesine basma, klip sahipli pelvis, `SHM237_FPPelvisOff`), bedenin gerçekten oynattığı yanal döngülerde (`A_CT_Jog_Left` 266 cm/s, `A_CT_Jog_Right` 249 cm/s), kök profili kapsülün fren giriş hızına uydurulmuş (v0 200 cm/s, 410 cm/s² → 0,49 s / 48,8 cm). Aşamalar: mevcut yanal momentum → ilk fren desteği (döngüde ilk basan ayak) → pelvis yük karşılama (diz marjı, iniş çukuru) → gövde/omuz fren tepkisi (varış başı eğimi, kol sönümü) → gerekirse kısa yerleşme adımı → kontrollü duruş (son duruş = `SHM_A_CP2_Jog_Fwd_Stop` son karesi, böylece sonraki kalkış ailesi aynı). Kollar koşu döngüsünü sürdürmüyor (üstel sönüm). Aile: sol 15/24, sağ 20/24 bin; 13 bin diz-ekseni koruması (çapraz adımda 60–94° düzlem atlaması; zamansal diz ipucu işe yaramadı) nedeniyle atlandı, 3 sağ bin klip içi kayma >8 cm nedeniyle DB dışı. `PSD_SHM242_LatStop` (32 klip, şema/bias satıcı DB'den, tam pencere BranchIn, continuing bias −3). Kanca: ABP `SHM242_DB_LatStop` (`Select_3` Option 1; varsayılan satıcı).
Kaynak doğruluğu: giriş hatası 0, son duruş hatası 0, klip içi basılı-ayak kayması ≤ 2,2 cm (sol), penetrasyon 0.

**2. A_LS_Jog_Left_Stop kaynaklı kayma giderildi mi?**
Evet, duruş klibi düzeyinde: en kötü kayma j41_rl_p04 **39,2 → 8,1 cm** (30 FPS), **59,3 → 9,0** (60), **39,0 → 6,2** (120); kalan 6–9 cm'lik değerler fren klibinde değil, yeniden kalkış klibinde (`A_LS_Jog_Left_Start`) veya DRAG sınıfı. Sağ ayna (j42_lr_p10) 0,0 (×2). Gerçek zamanda 22,4 cm DRAG (değişken kare süresinde klip kökü ile CMC fren profili ayrışıyor; V2.28 klip-bağlı kapsül bu aileye uygulanmadı) — **gerçek zaman PARTIAL**. Üretimin gerçek zaman koşusu karşılaştırılamadı (yeniden kalkışta `TurnL045` rotasına girdi, 92 cm — bilinen jstart sorunu).

**3. Sol P20 yanlış temas seçimi ve erken zaman sıçraması kapandı mı?** **Hayır, bu turda ele alınmadı** (A1 ve A2 kökü önceliklendirildi). Durum V2.41'deki gibi.

**4. İkinci ve üçüncü komut bütün FPS koşullarında güvenilir mi?** **Test edilmedi** (60 FPS 24–28 cm üçüncü istek kayması açık).

**5. İtme sonrası yakalama, çıkış ve duruş doğal mı?** **Ele alınmadı.**

**6. Duvar temasında ayaklar ve kamera doğru davranıyor mu?** **Ele alınmadı.**

**7. Bölgesel AimOffset üretime alınabildi mi?** **Hayır; değerlendirilmedi.**

**8. Hangi üretim anahtarları açıldı, hangileri kapalı?** Hiçbiri açılmadı. Yeni anahtarlar (hepsi üretim varsayılanında): ABP `SHM242_DB_LatStop` = satıcı DB; `SHM242_IdleOn` 0 / `SHM242_IdleDB` None; pawn `GR242_TurnSettleGate` False. V2.41 anahtarları aynen (KOn 0, PushYawK 1, StartOn 0).

**9. Aşama A kabul şartları karşılandı mı?** **Hayır.** Yanal fren/duruş (A1) sabit adımda güvenilir ve gerçek içerikle çözüldü; duruş sonrası yeniden yönelme (A2) sahibi bulundu ve kapı ile ertelendi ama kaldırılmadı; A3–A7 açık. Aşama B'ye geçilmedi; güvensiz bir sistem açılmadı.

### A2 — duruşun ardından 90° "savrulma": sahip ve kapı
LTP izi (j41_rl_p10): girdi hâlâ basılıyken (188 cm/s) V2.34 loco çerçevesi keşfe giriyor; bırakmada `GR234_LocoYaw` ilerleme yönüne (−160,8°) kilitleniyor, kontrol yaw'ı −71. Kapsül ≤ 5 cm/s olunca `BP_GR_Player.GR_UpdateIdleTurn` 90° dönüş montajını (`SHM_M_Neutral_Stand_Turn_090_L`, root motion) başlatıyor — duruş klibi hâlâ oynarken, ayak basılıyken (dyaw 101°, 32 cm). Hiçbir pawn yaw yazıcısı `SHM_StopSettle` eğrisini okumuyor; üretimde aynı (38 cm + görünür savrulma). Kapı: `GR242_TurnSettleGate` → dönüşü başlatan AND'in serbest `A=true` pini = NOT(kapı ∧ `GetCurveValue('SHM_StopSettle')` ∈ [0,5, 2]). Etki: montaj kapsül durduktan +0,37…0,60 s sonra (yerleşme bitince) başlıyor; P23 girişlerinde ayak salınımda olduğu için kayma yok, P21 girişlerinde basılı ayağı montaj hâlâ sürüklüyor (32 cm, kapıdan sonra). Yeniden yönelmenin kendisi V2.34 tasarımı (`lhold`); kaldırmak için strafe-bırakmada keşfi bastırmak gerekir (yapılmadı — tasarım kararı size ait).

---

## Character Locomotion Identity & Embodied Weight (depar 90° öncesi)

### Üretim ölçümü (w42_id: yürü → dur → yürü → dur → 30° → dur; yan / üç çeyrek / oyun kamerası, `gait242.py`)
| | Üretim | İnsan referansı (173 cm, 1,32 m/s) |
|---|---|---|
| hız / adım / kadans | 125,6 cm/s / 72,9 cm / ~1,7–1,8 adım/s | 132 / ~70 / ~1,9 |
| MM oynatma hızı | 1,245 (`A_LB_Walk_Fwd` 106 cm/s döngüsü hızlandırılıyor) | 1,0 |
| pelvis yanal / dikey, baş dikey (p2p) | 3,7 / 5,5 / 5,6 cm | 4–6 / 4–5 / ~4 |
| pelvis–göğüs karşı dönüşü | 23° p2p | 8–12° |
| kol salınımı (öne-arkaya) | 29 / 35 cm | 25–35 |
| duruş (bırakma → kapsül 0 / ayaklar sabit / pelvis yerleşme) | 0,53 / 0,80 / 0,90 s, 33,7 cm | |
| kalkış (basma → ilk kaldırma / %90 hız) | 0,33 / 0,73 s; ilk adım 72 cm | |
| **idle** pelvis / göğüs / baş p2p | **0,09 / 0,2 / 1,7 cm** | pelvis 1–3, göğüs 0,5–1 (nefes) |

Okuma (karelerden, gerçek hızda izlenmedi): yürüyüş adım uzunluğu ve kadansı insana yakın; gövde dik ve sert, kollar bedene yakın küçük salınımlı, pelvis/gövde karşı dönüşü yüksek ("döner üst beden"); duruş yumuşak ama sonunda **tamamen donmuş, simetrik "hazır poz"**; idle'da yalnız baş (bakış) hareket ediyor. İleri yürüyüş kalkışı `A_SHM222_WalkStart_L/R` (CP start evaluator; telemetrideki MM DB adı arka plan aramasıdır) — ağırlık aktarımı içeriği zaten var.

### Üretilen içerik ve bulunan entegrasyon sahibi
- `gen242_idle.py` → **`SHM242_Idle_Weighted`** (11,2 s, açık uçlu): ağırlık sağ ayağa (+3,8 cm pelvis, −0,7 cm, 2,5° yuvarlanma, 2° yaw; omurga karşı 1,5°), 3,2 s tutuş, nötr, sola; nefes 15/dk (spine_04/05 0,5°, klavikula, boyun karşı); mikro salınım 0,35/0,25 cm; baş ±1°. Ayaklar dünyada sabit, bacaklar menteşe-güvenli çözücü (ayak hatası 0, diz ekseni ≤ 2,1°). Kare 0 = üretim idle'ı (duruş klipleri bu poza geliyor).
- Entegrasyon denemeleri: (i) PoseSearch DB üyeliği 5.8'de bellek içinde değiştirilemiyor → `PSD_SHM242_Idle` + ABP kancası; (ii) kanca v1 (fonksiyon girişi) chooser'ın `SetDatabasesToSearch` çağrısı tarafından ezildi; (iii) kanca v2 (çağrı sonrası dal) MM'ye klibi seçtirdi — önce son karede tuttu (BranchIn girişleri döngü değil), klip açık uçlu yapıldı, 0,0'dan girdi.
- **Kök neden:** görünür idle MM değil. `SHM_IdleHold` her yürüyüş duruşundan sonra True (stance hatası > `IdleStanceTolerance` 6 cm) → AnimGraph `BlendListByBool_21`: alt beden = `PoseSnapshot 'SHM_StanceHold'` (durduğu an dondurulmuş), spine_01'den yukarısı = `SequencePlayer 'A_Ranger_Idle_Neutral_CWF'` (satıcı). MM idle DB'si bu yolda görünmez (`Phase27_SelectedTime` donuk). **"Donmuş manken" idle'ın sahibi V1.x stance-hold + Ranger idle üst-beden katmanıdır.** Ağırlıklı idle bu nedenle oyunda görünmedi (pelvis p2p 0,02 cm).
- Tur 8 deneyi (`IdleStanceTolerance` 30, `idlh` / `oh`): `SHM_IdleHold` yine True, hareket yok (pelvis p2p 0,02 / 0,09) → DA'daki tolerans canlı hold kararını değiştirmiyor (başka bir kapı/alan: `StanceIdleGateEnabled`, `SHM_UpdateSettle`); hold kuralının gerçek sahibi bir sonraki turun ilk iş paketi.

**Somut oyun içi iyileştirme (identity):** bu turda **uygulanamadı** — içerik hazır, sahip belirlendi, kancalar kuruldu; görünür değişiklik için `SequencePlayer_2/_5` varlığının değiştirilmesi ve hold kuralının (tolerans/gevşeme) yeniden tasarımı gerekir. Yürüyüş döngüsü/duruş içeriği bu turda değiştirilmedi.

---

## AŞAMA B — Genel gelişim
**Geçilmedi** (A kapısı karşılanmadı). Depar 90°, hareket dilleri, orman rotası: yapılmadı.

---

## Kanıt
- Önce/sonra yan yana gerçek hız (30 FPS sabit adım, aynı kare = aynı oyun zamanı; **videolar izlenmedi**, kare şeritleri incelendi): `vid/latstop_p04_o_vs_latg_side_realtime_part1.avi`, `vid/latstop_p04_o_vs_latg_game_realtime_part1.avi` (oyun kamerası), `vid/latstop_p10_o_vs_lat_side_realtime_part1.avi`.
- Kare şeritleri (`sheets/`): `lat_p04_oS_stop_crop.png` / `lat_p04_latgS_stop_crop.png` (üretim: bacak çaprazlı bükülme ve hemen savrulma; latg: dışa basan fren bacağı, yerleşme, sonra dönüş), `lat_p10_*`, `base_w42_oS_*` (yürüyüş/duruş/kalkış şeritleri).
- Kayıtlar: `v242cap_w42_id_{oS,oD,oG}`, `v242r7cap_w42_id_{oS,oG,idlS,idlG}`, `v242latcap_j41_rl_p10_{oS,latS,latD,latG}`, `v242r4lat/r7lat_j41_rl_p04_{oS,latgS,oG,latgG}`.
- Kare gözlemi (latg, yan): fren bacağı dışa basıyor, gövde ilerleme yönünde kalıyor, 0,5 s'de yerleşiyor; ardından 90° dönüş montajı (tasarım) geniş/bükük bir duruşla bitiyor — bu son poz üretimde de var, kaynağı dönüş montajı. Fren kendisi "frenliyor" okunuyor (Tier 2–3); dönüş sonrası Tier 1–2.

## Açık kusurlar (saklanmadı)
1. Duruş sonrası 90° yeniden yönelme (V2.34 LocoYaw, strafe bırakmadan bir kare önce keşif) — montaj basılı ayağı sürüklüyor (P21 bin'lerinde 32 cm); kapı erteliyor, kaldırmıyor.
2. Gerçek zamanda yanal fren 22 cm DRAG (klip-bağlı kapsül yok).
3. 13 bin diz-ekseni koruması (çapraz adım) — aile eksik fazlarda komşu bin'e düşüyor.
4. Idle: içerik görünmez (stance-hold + Ranger idle katmanı); walk stop sonunda simetrik hazır poz.
5. A3–A7 (P20 K, 3. komut 60 FPS, itme, duvar/kamera, AO) ele alınmadı.
6. Jeneratörde yeni bulunan tuzaklar (FWD, yarım-anahtar örnekleme) V2.37 ileri ailesini etkilemiyor (ileri döngü +Y), ama lateral/diğer eksenler için düzeltildi.

## Geri alma / durum
Anahtarlar varsayılanda = üretim. ABP/pawn yedekleri `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/v242_*` (sha1 doğrulanmış). Editör temiz (kirli paket yok); kilit bırakıldı.
