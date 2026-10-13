# Geçmişte performans için kaliteden vazgeçilmiş mi? (dosya kanıtlı denetim)

Kaynak: `Saved/Codex/**`, `Tools/**`, `Config/*.ini`, `Saved/Config/WindowsEditor/*.ini`, kök `CH01_CORRECTION_CHECKLIST.md`, Bridge özetleri. Proje git kullanmıyor; geçmiş yalnızca bu rapor/script/JSON dosyalarından okunabildi. Salt-okuma denetimi, 2026-10-13. Dosya yolları proje köküne göredir. Tarihler 2026'dır. Üç kaynak dosyanın varlığı (PostRain `optimization_applied.json`, WoodlandRefuge `optimization.json`, RefugeProduction `juvenile_optimization.json`) ayrıca doğrulandı; diğer satırlar denetim ajanının dosya okumalarına dayanır.

**Önemli bağlam:** 2026-09-21'e kadar üretim haritası `L_Chapter01_RangerHome` idi; bugünkü harita `L_GR_SphirusHouse` (GameDefaultMap). Chapter01'deki içerik/aktör kısıtlamaları bugünkü haritaya taşınmaz; config düzeyindekiler taşınır.

## (a) Açıkça performans/bellek gerekçeli azaltmalar

| Tarih | Kaynak | Değişiklik (eski → yeni) | Belgelenmiş gerekçe | Bugünkü haritayı etkiler mi |
|---|---|---|---|---|
| 09-05 | `Saved/Codex/Chapter01_EnvironmentQualityPass_20260905/Reports/working_audit.md` | Küçük bireysel gölge yayıcılar 179 → 165 | "PERFORMANCE … first safe waste targets" | Hayır (Ch01) |
| 09-06 | `Saved/Codex/IntegratedCompletion_20260906/Reports/Checkpoint_TR.md` | Alt bitki gölgeleri kapalı, mesafe culling, uzak ağaç gölgeleri kapalı | Performans/VRAM bölümü (7.2–7.4 / 8 GiB) | Hayır (Ch01) |
| 09-07 | `Saved/Codex/MissionIntegration_20260907/ENVIRONMENT_HANDOFF.md` | ~1.130 uzak taç proxy çamında WPO, dinamik gölge, DF, GI kapalı | "Distant WPO, unnecessary dynamic shadows … suppressed" | Hayır (Ch01) |
| 09-07 | `Saved/Codex/VisualMotionAcceptance_20260907/Diagnostics/MEMORY_RESTART_HANDOFF_20260907_133012.md` | 12 arka plan landscape dokusu 4K → 2K; 10 destek normal/ORM 2K | Streaming havuz açığı 762 → 279 MiB | Hayır (Ch01 assetleri) |
| 09-07 | Aynı + **`Config/DefaultEngine.ini` (VirtualTexturePoolConfig)** | VT havuzları sabitlendi: FloatRGBA 4 MB, G16 8 MB, DXT5 16 MB, `bAllowSizeScale=False` (toplam ≈374 → 216 MiB) | "measured sparse VT pools" | **Evet — config hâlâ aktif** |
| 09-09 | `Saved/Codex/TurnWorld_20260909/FAR_TREE_WIND_BUDGET_NATIVE_PLAN.md` | 5 ladin HISM WPO kapanma mesafesi 0 → 14000 cm (~0.37 ms kazanç) | "small view-specific GPU benefit" | Hayır (Ch01) |
| 09-22 | `Saved/Codex/PostRain20260922/optimization_applied.json` | **48 çevre dokusu kopyası 4K (bazıları 8K×4K) → 2048; çim/sazlık 1024** | "1–2K limit and streaming" | **Evet** |
| 09-22 | `Saved/Codex/WoodlandRefuge20260922/optimization.json` | **Ana PineTree01/03/05 (505 örnek), meşe, genç ladin WPO bitiş 11000 → 6500; SweetGrass/GroundCover WPO 3200 → 1800, cull başlangıç 2600 → 2200; kaya/kütük/yosun/yaprak WPO kapalı** | Yazılı gerekçe yok, dosya adı "optimization"; ölçüm GPU 20.9 → 20.0 ms | **Evet** |
| 09-22 | `Saved/Codex/RefugeProduction20260922/juvenile_optimization.json` | 91 genç çam WPO 6500; iğne dokuları 2048, gövde 1024; landscape materyali 106 → 91 örnekleme | "Optimization: … WPO/culling/shadow … texture limits" | **Evet** |
| 09-22 | `Saved/Codex/RefugeArtDirection20260922/PRODUCTION_REVIEW.md` | Çalı kabuk dokusu 1024, **kabuk POM kapalı** | "Measured performance" altında | **Evet** |
| 09-23 | `Saved/Codex/WoodlandFinal20260923/FINAL_REPORT.md` | Dış çamlar: WPO yok, 430 m cull | Gerekçe yazılmamış | **Evet** |

## (b) Sanat/düzen gerekçeli azaltmalar (donanım gerekçesi DEĞİL)
- 09-22 PostRain declutter (`declutter_plan.json`): foliage **9.316 → 2.560** örnek; gerekçe "remote non-silhouette cards removed; selective opening" (sanat), yan etki olarak draw call 1.737 → 920. Karma gerekçe.
- 09-22: 12 ReviewOnly RectLight kapatıldı (aydınlatma kimliği); height fog volumetrik değil bırakıldı.
- 09-23/24: geometri-çim ve ForestFloor pilotları kaldırıldı (görsel), 1.211 kopya genç çam silindi (hata), 6 patina dekalı gizlendi (görsel).
- Ch01 dönemi: ağaç/çalı/eğrelti silmeleri (destek, rota okunabilirliği, kompozisyon).

## (c) Gerekçesi bilinmeyen
- WoodlandRefuge WPO/cull değişiklikleri ve WoodlandFinal dış çam ayarları: yalnız dosya adı/rapor satırı var; **"donanım yüzünden yapıldı" olarak sunulmamalı**.
- 09-21 ExteriorWorld ilk foliage LOD/cull değerleri: önceki değerler kaydedilmemiş; azaltma olup olmadığı kanıtlanamıyor.

## (d) Kalıcılaşmış olabilecek geçici ayarlar
- Kalıcı olan tek config değişikliği VT havuz satırlarıdır (yukarıda). Bugünkü haritada VT havuz taşması doğrulanmadı (NOT_TESTED).
- `Config/DefaultScalability.ini` Epic gölge SMRT 12/8 — kaliteyi **artırır**.
- `Saved/Config/WindowsEditor/GameUserSettings.ini`: FrameRateLimit=0, dinamik çözünürlük kapalı; sg.*/t.MaxFPS/ScreenPercentage kalıcı override bulunmadı. Bu denetimin canlı cvar dökümü de sg.*=3 (Epic), t.MaxFPS=0, r.ScreenPercentage=0 gösterdi.
- QA Blueprint'lerinde (`BP_PBI_QA` vb.) `t.MaxFPS 30` konsol düğümleri var; yalnız bu aktörler spawn edilirse etkili. Bu denetimin PIE oturumlarında t.MaxFPS=0 okundu.

## (e) Çökme/OOM olayları
- 09-06 D3D12 `E_OUTOFMEMORY` + pagefile fatal (yüksek çözünürlüklü yakalama sırasında); kök neden kanıtlanmadı; sonrasında kalite azaltması yapılmadı.
- 09-16, 09-19, 09-27, 10-05: sistem commit/pagefile OOM (karakter/rig işleri); "kanıtlanmış GPU OOM" denmemiş.
- Hiçbir kayıtta GPU device-lost/TDR bulunmadı.
- 09-21 ve 09-22 raporlarında ~1.3 GB VRAM bütçe aşımı uyarısı görünür bırakılmış.

## Sahnede gerçekten olmayan vs görünmeyen içerik
- **Gerçekten kaldırılmış:** PostRain declutter (9.316 → 2.560), kopya genç çamlar, pilot çim/ForestFloor, YARD_AccessStep aktörleri.
- **Mevcut ama mesafe/ayar nedeniyle görünmeyebilir:** foliage cull mesafeleri (ör. GroundCover cull başlangıcı 2200), dış çamlar 430 m cull; bu denetimde C profilinde `r.ViewDistanceScale` 1 → 10 yapıldı (bkz. README, A/C görüntü çiftleri).
- **Gizli:** canlı haritada HiddenInGame 4 aktör: `ReviewOnly_Ground`, `ReviewOnly_NeutralSky`, `GR_HomeIdentityVolume`, `AtticLadder_AAMS` (hacim/yardımcı aktörler; görsel içerik eksikliği değil).

## Boşluklar
- Kullanıcı istemleri/sohbetler saklanmadığından gerekçesiz değişikliklerin niyeti doğrulanamaz.
- 09-25 sonrası çevre raporu yok (Ekim işleri karakter odaklı); Bridge dışa aktarımları cull/WPO/doku boyutunu kaydetmiyor.
- Hedef FPS veya VRAM bütçesi hiçbir yerde belgelenmemiş. Paketli ölçüm hiç yok.
- **Geçmişin eksik olması hiçbir kısıtlama yapılmadığını kanıtlamaz.**
