# Sphirus World: AI destekli Unreal geliştirme değerlendirmesi (2026-10-31)

Kapsam: Unreal Sensei'nin yaklaşımı; resmi Unreal MCP; Epic'in Claude Code eklentisi; mevcut kurulum, eksikler ve çakışmalar; sahneyi referans görüntüyle tekrar tekrar kontrol etme döngüsü.

Bu inceleme salt-okunurdu. Hiçbir kurulum, sürüm yükseltme, ayar ya da proje dosyası değişikliği yapılmadı; hareket, kamera ve çevre sistemlerine dokunulmadı. Bu rapor dosyası, kullanıcının yükleme isteği üzerine yazıldı.

Tazelik etiketleri:
- **[CANLI 2026-10-31]:** çalışan editör, süreç ve diskten okundu.
- **[KANIT 2026-09-15]:** tarihli eski kanıt.
- **[WEB]:** web kaynağı (bkz. SOURCES.md).

## 1. Mevcut durum

| Konu | Durum |
|---|---|
| Unreal sürümü | **UE 5.8.1**, CL 56057345, promoted build [CANLI]. `sphirus.uproject` EngineAssociation 5.8. |
| MCP eklentisi | **"Unreal MCP" 1.0** (`ModelContextProtocol`, motor içi `Plugins/Experimental`, **Experimental**). Projede açık. Ayrıca **AllToolsets** (Experimental), NiagaraToolsets ve PhysicsToolsets açık [CANLI]. |
| MCP sunucusu | Editör açık: PID 21712, V2.40 runner oturumu, `-UseFixedTimeStep -FPS=30`. Logda "Tool search enabled: registered 3 meta-tools (53 toolsets discoverable)". **Port 8000 dinlenmiyor**: sunucu başlatılmamış [CANLI]. |
| Claude Code ↔ MCP | **Bağlı değil.** Projede `.mcp.json` yok; `~/.claude.json` içinde Unreal MCP sunucusu yok [CANLI]. Yalnız `.codex/config.toml` Codex için `http://127.0.0.1:8000/mcp` gösteriyor. |
| Geçmiş MCP erişimi | Bir kez çalıştığı kanıtlı: özel bir HTTP istemcisi (`Saved/Codex/LookStrafe_20260915/mcp_call.py`) ile initialize, tools/list, list_toolsets / describe_toolset ve StartPIE/StopPIE [KANIT 2026-09-15]. |
| Epic Claude eklentisi | Claude Code'a **kurulu değil**. Commit `d1b0580` (2026-09-15) MIT kopyası referans olarak `.agents/skills/sphirus-character-camera/references/epic/` altında. Yukarıda son sürüm v3.1.2 (2026-10-23), yani **kopya eski** [WEB]. |
| Diğer eklentiler | PythonScriptPlugin, ModelingToolsEditorMode, PoseSearch, Chooser, MotionWarping, AnimationWarping, MetaHuman / MetaHumanCharacter / MetaHumanGenerator, HairStrands, AlembicHairImporter, LandscapePatch, MediaIOFramework. Marketplace: **Black_Eye 2.0.7** (kamera araçları), **GravityScatterTool 1.1.0** [CANLI]. |
| Görüntü kütüphaneleri | Motorun Python'unda numpy, PIL, cv2, scikit-image, imageio, torch ve lpips **yok**. PATH'te ffmpeg veya ImageMagick bulunmadı. Blender 5.2 kurulu; kendi Python'unda numpy olabilir, **doğrulanmadı**. PowerShell System.Drawing çalışıyor (`sheet240.ps1`) [CANLI]. |

## 2. Claude'un editörde gerçekten yapabildikleri

### Bugün kanıtlı kanal: gated runner + Unreal Python

- Editör, `-ExecCmds="py …runner.py"` ile açılıyor.
- İşler dosya kuyruğuna yazılıyor (`run_v2.sh`). Her işin türü belli: measure, write, pie ya da control.
- `write` işleri manifest ve doğrulanmış yedek olmadan reddediliyor. Kilidin tek sahibi var (`lock233.sh`). PIE sırasında yazma, DB yeniden kurma ve PIE başlatma yok.
- V2.30–V2.40 boyunca kanıtlanan işler:
  - Animation Blueprint düğüm ekleme ve bağlama;
  - PoseSearch veritabanı kurma;
  - asset yazma ve kaydetme;
  - PIE + enjekte girdi;
  - 20/30/60/120 FPS sabit adım;
  - telemetri, 30 FPS kare yakalama, kare kâğıtları;
  - Bridge/GitHub yayını.

### MCP kanalı (sunucu açılırsa)

Kaynak: motor kaynak başlıkları ve Python araç setleri [CANLI, disk].

- **`EditorAppToolset.CaptureViewport(CaptureTransform?, Annotations?, bShowUI=false)`**
  - Base64 PNG ile kamera konumu ve yönünü döndürür.
  - İsteğe bağlı olarak dünya ızgarası ve aktör etiketleri çizer.
- `GetCameraTransform` / `SetCameraTransform`, `FocusOnActors`, `GetVisibleActors`.
- `WorldPosToScreenCoords` / `ScreenCoordsToWorld`.
- `CaptureAssetImage`, `CaptureEditorImage`.
- `StartPIE` / `StopPIE` / `IsPIERunning`.
- `SlateInspector.Screenshot`: editör arayüzünün görüntüsü.
- `EditorToolset.LogsToolset`: logları okur.
- `AutomationTestToolset`: otomasyon testlerini listeler ve çalıştırır.
- `ProgrammaticToolset`: Python betiğiyle araç zinciri çalıştırır.
- `SceneTools`: `load_level`, `find_actors`, `trace_world`; ekleme ve silme de içerir.
- Blueprint, Material, MaterialInstance, Niagara, PCG, Sequencer, ControlRig, StateTree, BehaviorTree ve UMG araç setleri.

### Yapamadıklarım

- Videoyu gerçek zamanlı oynatıp izleyemiyorum; yalnız kareleri okuyabiliyorum.
- Oyun hissini ve görsel kabulü ben veremem.

## 3. Karşılaştırma

| Yaklaşım | Ne sunuyor | Bize katkısı |
|---|---|---|
| **Unreal Sensei** | "AI for Unreal Engine Development" kursu **yapım aşamasında**; müfredat ve çıkış tarihi yok. Site yöntemi "araçtan bağımsız" diye tanımlıyor: AI taslak çıkarır, insan yönetir, AI'ya Blueprint ekran görüntüsü ve log verilir. Kullandığı araçlar (Claude, Cursor, MCP), sınırları ve yaratıcının adı **doğrulanamadı** [WEB]. | İlke bizimkiyle aynı; alınacak somut bir araç yok. |
| **Epic Unreal MCP** (UE 5.8, Experimental) | Motora gömülü; en geniş kapsamlı sunucu. Streamable HTTP / SSE (stdio ve WebSocket yok). Kimlik doğrulaması yok; çağrılar oyun thread'inde sırayla çalışıyor. Tool search açık: 3 meta-araç (`list_toolsets`, `describe_toolset`, `call_tool`). Yeni araç için editör yeniden başlatılmalı [WEB + CANLI]. | Zaten kurulu. Asıl değeri kamera ayarlama, viewport çekimi ve log okuma. |
| **Epic Claude eklentisi** (`EpicGames/unreal-engine-skills-for-claude-code-plugin`, MIT) | Tek skill (`unreal-mcp`), SessionStart hook'u (`unreal-context.sh`, bash) ve `.mcp.json` / proxy kurulum talimatları [WEB]. | **Kurulmasını önermiyorum** (bkz. 4.2). |
| **Projedeki `ue-*` skill'leri** | Epic'in değil. Yerelde uyarlanmış; Epic belgelerine atıf veriyor, UE 5.8.1 düzeltme notları içeriyor. Kökenleri **doğrulanamadı**; üçüncü taraf `quodsoler/unreal-engine-skills`'e benziyor [WEB]. | Kalabilirler; "Epic seti" diye anılmamalılar. |
| Topluluk sunucuları (chongdashu/unreal-mcp, runreal/unreal-mcp, flopperam…) | Ayrı TCP portu veya Python uzaktan yürütme; çoğu resmi sunucudan önce çıktı [WEB]. | Resmi sunucuyla gereksiz çakışır; **önerilmez**. |

## 4. Eksikler ve çakışmalar

### 4.1 İki editör kanalı (en büyük risk)

- MCP çağrıları runner kapılarının hiçbirinden geçmiyor: manifest, kilit, PIE reddi, iş türü.
- Canlı editörde, oyun thread'inde çalışıyorlar; runner işleriyle iç içe geçebilirler.
- "Salt-okunur" görünen çağrı bile asset'i kirletebilir: `find_node_types` daha önce Blueprint'i dirty yaptı.
- **Kural önerisi:** MCP yalnız okuma ve çekim için kullanılsın; runner kilidi alınmışken ve sırayla. Her çağrıdan önce ve sonra dirty paket kontrolü yapılsın.

### 4.2 Epic eklentisi proje kurallarıyla çelişiyor

- Skill "her çağrı değişiklik yapar, önce kaydet, commit et" diyor. Bizde git yok; inceleme ve araştırma görevleri kayıt yetkisi vermiyor.
- SessionStart hook'u her oturumda çalışıyor.
- `.mcp.json` ve proxy kurulumu yapılandırmayı değiştiriyor.
- `sphirus-editor-automation-mcp` ile rakip bir talimat yüzeyi oluşturuyor.
- README'sinin kendi uyarıları:
  - "Localhost is not a trust boundary";
  - `execute_tool_script` içerik silebilir;
  - izinleri atlayan çalışma modu kullanılmamalı.

### 4.3 Diğer çakışmalar

- **Codex ve Claude** aynı 8000 portunu gösterirse aynı editörde iki ajan olur; tek sahip kuralı bozulur.
- **`AgentSkillToolset`** editöre genel skill'ler kaydediyor (`blueprint_basics`, `material_basics`, `default_outdoor_lighting`). `default_outdoor_lighting` izlenirse çevre ve aydınlatma sahibini ezebilir; projede yok sayılmalı.
- **Black_Eye** kamera eklentisi GraceRanger kamerasına paralel bir sahip olabilir. Kullanımı incelenmedi (**NOT_TESTED**).

### 4.4 Eksik yetenekler

- MCP sunucusu kapalı; Claude Code bağlantısı yok.
- Sayısal görüntü karşılaştırma yok (SSIM ya da NVIDIA FLIP).
- Çevre için kayıtlı ve tekrarlanabilirliği ölçülmüş referans kamera seti yok. Bridge'in `camera_plan.json` dosyası var, ama tekrarlanabilirliği ölçülmedi.
- FunctionalScreenshotTest aktörü ve onaylı "doğru görüntü" seti yok. Motor modülleri mevcut: FunctionalTesting, ScreenShotComparison, ScreenShotComparisonTools, AutomationController.

### 4.5 Kritik ayrım

Referans görüntüler (A Plague Tale: Requiem vb., `reference-authority.md`) **stil referansı**, piksel hedefi değil. Onlara piksel farkı uygulamak anlamsız. İki ayrı döngü gerekiyor:

- **Regresyon:** kendi önceki çekimimizle, aynı kamerada sayısal karşılaştırma.
- **Referans niyeti:** değer yapısı, palet, kompozisyon, yoğunluk bantları. Sabit bir rubrikle görsel puanlanır; son kabul kullanıcıdadır.

## 5. Önerilen güvenli doğrulama döngüsü

1. **Kilit al.** Editörü temiz aç; açık bir PIE ya da kuyrukta eski iş olmasın.
2. **Sahneyi sabitle.** Pozlama, günün saati ve rüzgâr tohumunu sabitle. TAA/Lumen/VSM gürültüsü için N kare ısındır.
3. **Çek.** Kayıtlı kamera setinden çek: runner + HighResShot (bugün çalışıyor) veya MCP `CaptureViewport`.
4. **Regresyon.** Önceki çekimle SSIM/FLIP ve fark ısı haritası; eşik T1'de ölçülen gürültü tabanından gelir.
5. **Referans paneli.** Yan yana kâğıt: referans | önce | sonra. Sabit rubrikle (`sphirus-visual-art-direction` / `sphirus-aaa-environment-polish`) görsel puan, sonra kullanıcı onayı.
6. **Kirlilik kontrolü.** Dirty paket listesi önce ve sonra boş olmalı. Sonra kilidi bırak.

Ağır seçenekler gerekmedikçe kullanılmaz:
- Movie Render Queue: gürültüsüz, birikimli çekim.
- FunctionalScreenshotTest: geçti/kaldı ve onaylı doğru görüntü.
- Gauntlet: CI sarmalayıcısı.
- LPIPS: torch gerektirir.

## 6. Test planı

| # | Test | Geçme ölçütü | Onay gerekir mi? |
|---|---|---|---|
| T1 | Çekim tekrarlanabilirliği: aynı kamera, aynı oturumda 3 kez ve editör yeniden açıldıktan sonra 3 kez | Gürültü tabanı ölçülür; tekrarlar arası fark eşiğin altında | Runner ölçüm işi: hayır. Editör yeniden başlatma: evet |
| T2 | MCP salt-okunur erişim: `list_toolsets`, `IsPIERunning`, `GetCameraTransform`, `CaptureViewport` | Yanıtlar geliyor, dirty paket 0 | **Evet:** sunucuyu başlatmak + bağlantı ayarı (`.mcp.json` veya `claude mcp add`) |
| T3 | Runner ile MCP aynı kamerada | İki çekim eşleşiyor | T2'ye bağlı |
| T4 | Ölçüt aracı: aynı görüntü = 1.0, bilinen değişiklik yakalanıyor | Doğru sonuç | **Evet:** proje dışında bir venv'e numpy/scikit-image (FLIP isteğe bağlı) ya da Blender Python'u |
| T5 | Referans paneli: tek görünüm (ör. ev önü, oyuncu kamerası) | Rubrik puanı iki tekrarda tutarlı; son karar kullanıcıda | Hayır |
| T6 | Güvenlik: PIE sırasında runner'ın yazmayı reddetmesi; MCP ile hiçbir yazma aracı çağrılmaması | Red loglanıyor; dirty paket 0 | Hayır |

## 7. Riskler

- **MCP Experimental:** API ve veri formatları değişebilir. Kimlik doğrulaması yok, loopback'e açık.
- **Kapıların atlanması:** MCP çağrıları runner kapılarını atlıyor. Oyun thread'inde işler iç içe geçerse çökme riski var; daha önce runner'a yeniden giriş kaynaklı çökme yaşandı.
- **Dirty paketler:** okuma araçları bile Blueprint'i kirletebilir.
- **Gürültü:** Lumen/TAA sahte fark üretebilir; T1 olmadan eşik koyulamaz.
- **Görsel puan:** deterministik değil; insan kabulünün yerini tutmaz.
- **Telif:** referans görüntüler yayımlanmamalı. Yalnız kendi çekimlerimiz Bridge'e gider.
- **Yapılandırma:** Epic eklentisinin hook'u ve otomatik `.mcp.json` yazımı yapılandırmayı sessizce değiştirebilir.
- **Disk ve bellek:** ek çekimler ve kütüphaneler C: sürücüsünü doldurabilir (önceden yaşanan OOM).

## 8. Onay bekleyen kararlar

1. **MCP'yi açmak.**
   - Öneri: yalnız okuma ve çekim için, açıkça başlatılsın; otomatik başlatma olmasın.
   - Bağlantı ayarı nereye yazılsın: proje içi `.mcp.json` mı, kullanıcı ayarı mı?
2. **Görüntü karşılaştırma aracı.**
   - Öneri: proje dışında, ayrı bir venv'e numpy ve scikit-image.
   - Alternatif: önce Blender'ın Python'u denenir; o zaman kurulum gerekmez.
3. **Epic referans kopyasını v3.1.2'ye güncellemek** (`.agents` altında tek dosya değişikliği).
4. **Epic Claude eklentisini kurmamak** (öneri). MCP bilgisi mevcut proje skill'inde (`sphirus-editor-automation-mcp`) kalır.
