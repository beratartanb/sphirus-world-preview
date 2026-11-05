# Claude ve Unreal araç kurulumu — 5 Kasım 2026

**Genel durum: PARTIAL.** Epic Unreal MCP üzerinden okuma, düzenleme, PCG, görsel kontrol ve kalıcılık testleri geçti. Nwiro Integration Kit kurulamadı: Fab kütüphanesinde var, ama kurulumu Epic Launcher'da bir tıklama istiyor. Yeni bir Claude sohbet oturumunda canlı çağrı denenmedi.

Motor: UE 5.8.1, CL 56057345. `EngineAssociation` özel kimlik değil, düz `5.8`. Proje: `sphirus.uproject`. Ana harita: `/Game/GraceRanger/Maps/L_GR_SphirusHouse` (MCP ile doğrulandı).

## Araç tablosu

| Araç/paket | Kurulu sürüm | Bağlantı yolu | Gerçekten yapılan işlem | Sonuç | Kanıt |
|---|---|---|---|---|---|
| Epic Unreal MCP (`ModelContextProtocol`, `AllToolsets`) | UE 5.8.1 ile gelen | `http://127.0.0.1:8000/mcp`, 3 meta araç, 53 araç seti | Keşif, okuma, düzenleme, PCG, PIE sorgusu, görüntü alma | PASS | `Saved/Codex/ClaudeUnreal_20261105/` |
| Otomatik başlatma | `bAutoStartServer=True` | Kullanıcı ayarı | Komut satırı bayrağı olmadan editör açıldı, sunucu başladı | PASS | `Saved/Logs/cut_2.log` |
| `.mcp.json` (`unreal-mcp`) | Motorun ürettiği dosya | Claude Code proje ayarı | `claude mcp list`: Connected | PASS (yalnız sağlık kontrolü) | Bu rapor |
| Yeni Claude oturumu | Claude Code 2.1.317 | `claude -p` | CLI "Not logged in" dedi, çağrı yapılamadı | NOT_TESTED | `new_session_test.json` |
| Epic Claude Code paketi | 3.1.2, proje kapsamı | `.claude/settings.json` | Kuruldu, `unreal-mcp` skill'i okundu ve iş akışı uygulandı | PASS | `claude plugin list` |
| Engine Agent Skill'leri | UE 5.8.1 | `AgentSkillToolset` | `ListSkills`, `Skill_PCGGraphGeneration` yüklendi ve izlendi | PASS | `skill_pcg_graph.json` |
| PCGToolset | UE 5.8.1 | Epic MCP | Grafik kopyası, parametre, düğüm, üretim | PASS | `evidence/pcg_*.png` |
| Nwiro Pro | 1.1.14 | Editör içi köprü, runner üzerinden | `GetPluginInfo`, `render_widget_blueprint` | PASS (MCP değil) | `nwiro_info.txt` |
| Nwiro Integration Kit | Kurulu değil (Fab'de 1.0.15 duyurulmuş) | Yok | Kütüphanede sahipliği görüldü, Launcher sayfası açıldı | BLOCKED | Aşağıda |
| Nwiro Custom Tools | Yok | C++ eklentisi gerekiyor | Mevcut araçlarda eksik çıkmadığı için eklenmedi | NOT_TESTED | Doküman okundu |
| Nwiro Biome Generator | Pro özelliği | Ücretli üretim | Kullanılmadı | NOT_TESTED | Görev dışı |
| EasyBiomes / Pine Forest PCG Biome | Kurulu değil | Yok | Fab kütüphanesinde bulunmadı | NOT_TESTED | Motor örneği ve Pine Forest Pack kullanıldı |
| Pine Forest Pack | Projede | Epic MCP | PCG'de ağaç, taş ve örtü meshleri kullanıldı | PASS | `evidence/check_*.json` |
| PBL Database, True Lens, Animated Female Locomotion Set, Blueprint Assist | Kurulu değil | Yok | Fab kütüphanesi ad aramasında çıkmadı | NOT_TESTED | Satın alma yapılmadı |

Üç seviye ayrı tutuldu:
- **Kurulu:** Epic MCP, Epic paketi, Nwiro Pro.
- **Yalnız dokümanı okunan:** Integration Kit, Custom Tools, Biome Generator, EasyBiomes.
- **Gerçek işlemle doğrulanan:** tablodaki PASS satırları.

## Bağlantı gerçeği

Bu oturum `.mcp.json` oluşmadan başladığı için `mcp__unreal-mcp__*` araçları burada görünmedi. Testler aynı uç noktaya `Tools/ClaudeUnreal_20261105/umcp.py` ile gitti. Bu, Claude Code'un doğrudan MCP aracı olarak çağırması değildir.

Nwiro Pro'da MCP sunucusu yok: `StartMCPServer` boş, `mcpRunning:false`, `mcpPort:0`. Pro'ya runner üzerinden erişmek MCP bağlantısı sayılmamalı.

## Testler

**A — Okuma: PASS.** Epic MCP ile aktif harita okundu. `/Game/GraceRanger/SF/MaskJob/BP_GR_MaskBench` için 14 değişken, 2 grafik, 10 giriş düğümü ve bağlantılı alt grafik okundu. Haritadaki örneğin 6 bileşeni okundu. `read_graph_dsl` bu grafikte hata vermeden boş döndü, bu yüzden düğüm araçları kullanıldı.

**B — Düzenleme: PASS.** `W_Sphirus_HUD` dosyası `/Game/GraceRanger/ToolTest/W_ToolTest_HUD` olarak kopyalandı. `TextBlock_191` metni `Controls:` iken `MCP TEST METNI` yapıldı, geri okundu, derlendi, görüntüde görüldü, eski değere döndürüldü ve tekrar görüldü. `create_widget_blueprint` çağrılmadı. Düzenleme Epic MCP ile, görüntü Nwiro Pro `render_widget_blueprint` ile yapıldı. Kopyadaki `SizeBox_85` görüntü için geçici açıldı ve yeniden kapatıldı.

**C — PCG: PASS (teknik).** Motorun `SimpleForestWorldRayHits` örneği `/Game/GraceRanger/ToolTest/PCG_ToolTest_Forest` olarak kopyalandı. Projedeki `PCG_C01_*` ve Calysto grafikleri Calysto aktörlerine bağlı olduğu için tek başına çalışmıyor; bu yüzden motor örneği seçildi. Satıcı ve motor kaynağı değişmedi.

İzole seviye `L_ToolTest_PCG`, 40 × 40 m hacim, düz zemin ve 14 derecelik rampa içeriyor. `TreeDensity` parametresi grafiğe eklendi ve MCP ile değiştirildi. Görüntüler aynı kamera pozundan alındı.

| Mesh | 0,01 | 0,03 |
|---|---|---|
| `SM_PineTree01` | 3 | 6 |
| `SM_PineTree02` | 8 | 13 |
| `SM_PineTree03` | 4 | 6 |
| Ağaç toplamı | 15 | 25 |
| `SM_PineStone01/02` | 2 / 3 | 2 / 3 |
| `SM_GroundCover01/02` | 172 / 157 | 171 / 156 |

- Zemin teması: örneklenen örneklerde en büyük boşluk 0,00 cm; rampada yükseklik 283 cm'e kadar çıktı.
- Ağaç sayısı parametreyle 3 kat artmadı, 15'ten 25'e çıktı. Nedeni ölçülmedi.
- Örtü 2 azaldı, çünkü ağaçların altından çıkarılıyor.
- Görsel sınır: Bu bir teknik test sahnesi. Örtü meshleri bu ölçekte seyrek ve küçük, zemin gri, sanat kalitesi değerlendirilmedi. Ana haritaya hiçbir şey taşınmadı.

Görüntüler: `evidence/pcg_before.png`, `evidence/pcg_after.png`.

**D — Görsel geri bildirim: PASS.** `L_GR_SphirusHouse` PIE'de açıldı, oyuncu kamerası görüntüsü alındı ve incelendi (`evidence/pie_player_camera.png`). Harita değiştirilmedi. Karakter sırtı dönük, bej kazak ve gri pantolonla görünüyor; kamera yakın omuz konumunda, ev sağda, orman ve eğreltiler yerinde. Bu çekimde saç koyu, kaba ve parçalı görünüyor; `HighResShot` etkisi olabilir, oyunda ayrıca bakılmalı. MCP `CaptureViewport` editör kamerasını veriyor, oyuncu kamerası için kullanılmamalı. PIE'de `LogScript` satırı çıkmadı.

**E — Kalıcılık: PASS.** Editör kapatılıp açıldıktan sonra diskten okundu: `TextBlock_0` = `E_KALICILIK_20261105`, `TextBlock_191` = `Controls:`, `SizeBox_85` = `Collapsed`, grafikte 19 düğüm ve `TreeDensity` bağlantısı, seviyede 25 ağaç. Başlatmada açılan harita ana haritaydı. Rehberin ve `CLAUDE.md` notunun yeni oturumda keşfi NOT_TESTED, dosyalar yerinde ve skill eşitlemesi 0 hata verdi.

## Değişen dosyalar

- Yeni: `.mcp.json`, `.claude/settings.json`, `.agents/skills/sphirus-editor-automation-mcp/references/claude-unreal-tooling.md`, `Tools/ClaudeUnreal_20261105/`
- Değişen: `CLAUDE.md` (Unreal tooling bölümü), `.claude/settings.local.json` (`enabledMcpjsonServers`), `.agents/skills/sphirus-editor-automation-mcp/SKILL.md`, `.agents/skills/sphirus-character-camera/references/epic-mcp.md` (güncel rehbere işaret), `Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini` (`bAutoStartServer`), `~/.claude/settings.json` (resmi eklenti pazarı)
- Yeni test assetleri: `/Game/GraceRanger/ToolTest/` altında 3 paket. Oyun bunları kullanmıyor.
- Değişmeyen: `sphirus.uproject`, ana harita, karakter, kamera, Story Framework, Nwiro eklenti dosyaları, `.codex/config.toml`, kayıt dosyaları.

## Geri alma

Yedekler: `Saved/Codex/ClaudeUnreal_20261105/checkpoint/` (`CLAUDE.md`, `AGENTS.md`, `sphirus.uproject`, `settings.local.json`, `config.toml`, kullanıcı ayarları, editör ayarları).

1. Dosyaları bu klasörden geri kopyala.
2. `.mcp.json` ve `.claude/settings.json` dosyalarını kaldır.
3. Editör kapalıyken `Content/GraceRanger/ToolTest/` klasörünü kaldır.
4. Claude tarafında: `claude plugin uninstall unreal-engine-skills-for-claude-code@claude-plugins-official --scope project`.

## Bilinen sınırlar

- Epic MCP, runner kapılarının arkasında değil. Kural: MCP belleğe yazar, kaydı `gsave.sh` yapar. `gsave.sh` denendi ve geçti.
- Kural dışı kalan işlem: `W_ToolTest_HUD` ve `PCG_ToolTest_Forest` bu kural yazılmadan önce MCP `save_assets` ile kaydedildi. Kilit ve manifest vardı, runner kapısı yoktu. Yalnız test paketlerini etkiledi.
- Sunucu yerel, kimlik doğrulamasız. Aynı kullanıcıyla çalışan her yerel işlem bağlanabilir. Otomatik başlatma açık olduğu için editör her açıldığında dinliyor.
- Nwiro belgeleri bir sayfada UE 5.5–5.7 yazıyor; changelog ve kurulu `.uplugin` 5.8 diyor. Pro ile Kit'in aynı projede birlikte çalışması belgelenmemiş.
- Önceki raporda Nwiro 229 araç listelemişti; kaynakta 227 sabit araç tanımı sayıldı. Bu oturumda canlı liste alınmadı.
- `RangerGameplayCamera` adı skill notlarından geldi, bu görevde canlı doğrulanmadı.
- Hatalı çağrıların listesi rehberde.

## Kullanıcı adımı

Kit için Launcher'daki Fab sayfası açıldı. Şunu yapman gerekiyor: **Install to Engine** (UE 5.8). Kurulunca Pro ile çakışma riskine karşı önce yedek alıp ayrı denerim. Yeni ürün satın alınmadı.

## Sonraki oturum

Proje klasörü: `C:\Users\berat\OneDrive\Documents\Unreal Projects\ActionAdventureMovementS`. Editörü aç, sonra bu klasörde yeni bir Claude Code oturumu başlat. İlk iş: `list_toolsets`, ardından `SceneTools.get_current_level`. Rehber: `.agents/skills/sphirus-editor-automation-mcp/references/claude-unreal-tooling.md`.
