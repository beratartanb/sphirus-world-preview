# Sphirus World — AI destekli 3D üretim hattı, 1. tur (2026-11-24)

**Durum: KISMİ.** Blender Skills, tek Blender MCP, statik varlık hattı (Test A) ve otomatik rig/skin/animasyon hattı (Test C) gerçekten kuruldu ve ölçüldü. StableGen/ComfyUI arka ucu gerçek bir SDXL üretimiyle doğrulandı; Blender içi çok açılı projeksiyon **denenmedi**. **Test B (giyilebilir aksesuar) yapılmadı.** Mixamo LLM Mocap pilotu **yapılmadı** (araştırıldı, gerekçe §3). Hiçbir sonuç için AAA veya kullanıcı kabulü iddia etmiyorum.

Etiketler: **DOĞRULANDI** (çalıştırıldı ve ölçüldü), **KISMİ**, **DENENMEDİ**, **ARAŞTIRILDI** (kurulmadı), **REDDEDİLDİ**.
Proje: `C:\Users\berat\Documents\Unreal Projects\sphirus_UE59` (UE 5.9.0-60738873). Hareket sistemi, GASP veritabanları, MetaHuman iskeleti/materyalleri, kamera ve seviyeler **değiştirilmedi** (Unreal yazma günlüğünde yalnız `/Game/Sandbox/AIPipeline_TEST/...` var).

> ⚠️ **Açık iş — sizin müdahalenizi bekliyor:** Unreal Editor'de 22:28'den beri modal bir **"Mesaj"** penceresi açık (Test C sandbox varlıklarını bellekten silmek için gönderdiğim `aip_dropC` işi `EditorAssetLibrary.delete_asset` çağırdı). Runner bu pencereye takıldı. Editör kilidi bilerek `aip` adına **tutuluyor** (`Saved/Codex/EDITOR_LOCK.txt` nedenini yazıyor) ki başka oturum bloke runner'a iş kuyruklamasın. Pencereyi yanıtladıktan sonra: `bash Tools/SHME_V233_20261027/lock233.sh release aip`. Bekleyen diğer üç işimi kuyruktan aldım (`Tools/AssetPipeline_20261124/unreal/parked_jobs/`). **Güncelleme (kullanıcı, aynı gün):** editör donmuş ve yanıt vermiyor; pencere şimdilik bırakıldı, Test C'nin Unreal adımı askıda. Test C'nin Unreal'daki varlıkları **kaydedilmedi** (yalnız bellekte; kapanışta "kaydet?" sorulursa kaydetmeyin — çift-kök iskelet içeriyor, §7).

## 1. Başlangıçtaki gerçek durum

| Öğe | Bulunan |
|---|---|
| Blender | Yalnız Microsoft Store **Blender 5.3.0** (WindowsApps). `blender.exe` betikten çalıştırılamıyor (Erişim engellendi), başlatıcı çıktı vermiyor. Kullanıcı ayarı yalnız 5.2 klasöründe; 5.3'te yalnız varsayılan eklentiler. |
| Blender MCP / eklentiler | Yok |
| Claude | `.mcp.json`: yalnız `unreal-mcp` (127.0.0.1:8000). 56 proje skill'i (`.agents/skills` kanonik + `.claude/skills` sarmalayıcı); `sphirus-asset-pipeline` "Meshy yapılandırılmadı" diyordu. Eklentiler: `unreal-engine-skills-for-claude-code`, `reference-to-game`. |
| Codex | `~/.codex/config.toml`: Blender ile ilgili MCP yok (yalnız kendi node_repl'i). Codex skill'leri aynı `.agents/skills` klasöründen. |
| ComfyUI / Tripo / Meshy / Hunyuan | Hiçbiri kurulu değildi |
| Donanım | RTX 4060 Laptop 8 GB (sürücü 616.56), 32 GB RAM, C: 81 GB boş |
| Güvenlik | **Smart App Control: Açık** (daha önce Nwiro DLL'ini de engellemiş) |
| Unreal | 5.9 kopya açık, `L_GR_SphirusHouse` yüklü, kirli paket 0, PIE yok; kilit boştu (son sahip `emb`, 20:31) |
| Çakışma | 5.8 orijinali (`OneDrive\...\ActionAdventureMovementS`) ayrı ve dokunulmadı; çalışma 5.9 kopyasında. |

## 2. Yeni kurulanlar ve sürümler (DOĞRULANDI = gerçek çalıştırma ile)

| Sistem | Sürüm / yer | Kanıt |
|---|---|---|
| Blender 5.3.0 taşınabilir (resmî zip, SHA-256 eşleşti) | `C:\Users\berat\Tools\Blender\...`, kullanıcı değişkeni `BLENDER_EXE` | DOĞRULANDI — tüm başsız işler bununla koştu. Store kopyası duruyor; ikisi aynı kullanıcı ayarını paylaşıyor. |
| blender-skills 1.3.3 (MIT, 28 skill) | `.agents/skills/blender-*` + Claude sarmalayıcıları (sync betiğiyle) | DOĞRULANDI — kendi testleri **79/79 PASS** (129 sn), `data/blender_skills_tests.txt`. Kod taraması: ağ çağrısı, pip, otomatik çalıştırma yok. |
| MCP for Blender 2.3.1 (Aday A) | eklenti 5.3 kullanıcı eklentilerinde; `.mcp.json` → `blender` (uvx, sürüm sabit) | DOĞRULANDI — uçtan uca **10/10** (`data/mcp_smoke.json`): yalnız 127.0.0.1:9876, telemetri kapalı, güvenli mod `import os`'u reddetti, nesne oluştur/oku/sil, `look` ekran görüntüsü. |
| uv 0.13.9 | winget | DOĞRULANDI |
| Jiggle Physics 4.5.3 (GPL-3.0) | extensions.blender.org | KURULDU, etkin — **testte kullanılmadı** (Test B yapılmadı) |
| StableGen 0.5.0 (GPL-3.0, imza SHA-256 eşleşti) + kendi ComfyUI v0.43.0 + SDXL paketi 4 (17 bileşen) | `C:\Users\berat\Tools\StableGen` | KISMİ — arka uç gerçek üretimle doğrulandı (§5); Blender içi projeksiyon DENENMEDİ |
| PyTorch 2.7.1+cu128 (ComfyUI ortamında) | 2.9.0+cu130 yerine | DOĞRULANDI — Smart App Control 2.9.0'ın `c10_cuda.dll`'ini engelledi (WinError 4551); 2.7.1 CUDA ile açıldı. SAC'a dokunulmadı. |

## 3. Kurulmayan / elenen araçlar

| Araç | Karar | Neden (kaynak doğrulandı) |
|---|---|---|
| PoBruno/mcp-blender-agent (Aday B) | ARAŞTIRILDI, etkin değil | Tasarımı iyi (tipli araçlar, undo, görsel karşılaştırma, exec kapalı) ama 2026-07'den beri güncellenmedi, 5.3 kanıtı yok, skill paketiyle eşleşmiyor. İkisini aynı anda açmadım. |
| SkinTokens (doğrudan / StableGen paket 14) | KURULMADI | ≥14 GB VRAM ister; bu GPU 8 GB. StableGen zaten entegre ediyor, ayrı kurulum gereksiz. |
| StableGen TRELLIS.2 / LATO.2 | sonra | VRAM belgelenmemiş, ~13 GB indirme |
| mixamo-llm-mocap | ARAŞTIRILDI, pilot yapılmadı | Metinden değil **videodan** hareket (GVHMR→SMPL-X→Mixamo FK); SMPL-X kaydı (sizin hesabınız) ve Mixamo FBX gerekir; ~8 GB VRAM; SMPL-X/GVHMR lisansları ticari kullanım için kontrol edilmeli. Üç örnek hareket (uzanma, denge toparlama, yavaştan duruşa) için video kaynağı da gerekir. |
| Hunyuan3D 2.1 | REDDEDİLDİ | Lisans bölgesi AB, Birleşik Krallık ve Güney Kore'yi hariç tutuyor; çıktıların bölge dışı kullanımı da lisanssız (Bölüm 1.l, 5.c). Şekil+doku 29 GB VRAM. |
| AnimalLift, NI-Tex | park (yalnız araştırma) | Lisans dosyası yok (varsayılan telif = ticari hak yok) |
| GameRig | aday, önce test | Blender 4.5/5.0 belirtilmiş, 5.3 denenmemiş |
| FreeMoCap | park | AGPL, v2 alfa, 1–3 webcam; blokaj için |
| Rokoko Studio Live | park | Canlı yakalama Rokoko donanımı ister; yalnız ücretsiz retarget paneli işe yarar |
| Meshy (Pro) | tercih edilen bulut üretici (kurulmadı) | En açık ticari şartlar, resmî Blender eklentisi (5.3 listede değil) |
| Tripo | yalnız ücretli plan, şartları okuduktan sonra | Ücretsiz plan çıktı hakları belirsiz |

## 4. MCP ve skill bağlantı sonuçları
- 28 Blender skill'i proje düzeninde (kanonik `.agents/skills`, Claude sarmalayıcıları sync betiğiyle; Codex aynı klasörü okur). `sphirus-asset-pipeline` güncellendi: sahiplik/izolasyon/kabul bu skill'de, teknik (modelleme/UV/bake/rig/export) `blender-*` skill'lerine yönleniyor. Sync tek hata verdi: `gasp-motion-matching` içindeki eski token — **önceden vardı, dokunmadım** (hareket kapsam dışı).
- MCP araçları yalnız bu klasörde **yeni başlatılan** bir Claude oturumunda görünür (bu oturumda Claude MCP araçlarını yükleyemedi; test, aynı `uvx` komutunu çalıştıran bağımsız bir MCP istemcisiyle yapıldı — §2).
- Güvenlik ayarları: `DISABLE_TELEMETRY=true`, `BLENDER_MCP_SAFE_MODE=1`, `BLENDER_HOST=127.0.0.1`; eklentide Telemetri ve Uzak Bağlantı kapalı. Güvenli mod: yalnız bpy/bmesh/mathutils + saf stdlib; os/subprocess/ağ/open/exec/handler/harici .blend yok. Kaydet/render/içe-dışa aktar serbest → canlı düzenlemeden önce .blend kopyası alın; `execute_code` kendi undo adımını atmaz.

## 5. StableGen / ComfyUI testi
- ComfyUI yalnız 127.0.0.1:8188, `--disable-api-nodes`; tüm özel düğümler (IPAdapter Plus, Marigold, StableDelight) yüklendi.
- **Gerçek üretim** (`data/comfy_test.json`): RealVisXL V5 + derinlik ControlNet, Test A modelinin derinlik haritasından, 1024², 25 adım → **404 sn, tepe VRAM 7,47 / 8 GB**. Başlangıçta Unreal açık olduğu için 6,4 GB zaten doluydu → model RAM'e taşındı, yavaş. Çok açılı dokulama için Unreal kapatılmalı veya Lightning LoRA kullanılmalı.
- Görsel (`evidence/stablegen_sdxl_depth_maskstand.png`): eskimiş meşe, aşınmış kenarlar, dövme bilezik — prosedürel v3'ten açıkça daha inandırıcı; geometriyi izliyor. **Ama** ışık/gölge görüntüye pişmiş; doğrudan albedo olamaz. Hatta baş formunu maske yüzü olarak yorumladı (projeksiyonda istenmeyen detay üretebilir).
- DENENMEDİ: StableGen'in Blender içi çok açılı projeksiyon/bake'i. Üretim operatörü Blender'ın UI zamanlayıcılarına bağlı; başsız modda sürülemiyor. Sonraki adım: GUI Blender'da (MCP ile veya elle) Test A üzerinde 4–6 kamera, StableDelight + Marigold IID, ardından aynı QA kapıları.
- Lisans notu: paket 4'teki Hyper-SDXL LoRA'larının lisansı "Bilinmiyor"; üretim dokularında kullanmayın. Qwen Image 2.1 / Bria FIBO (ticari değil) kurulmadı.

## 6. Rigging ve mocap testleri (Test C — ayrı test mankeni, MetaHuman'a dokunulmadı)
- Model: deri-değiştirici iskelet grafiğinden 1,70 m insansı manken (1652 üçgen).
- Rigify metarig → eklem yerleşimi (dirsek/diz hafif bükük) → kontrol rigi (222 kemik) → oyun iskeleti (36 kemik, tek kök) → **UE Mannequin adları** (eksik isim 0, IK Retargeter otomatik eşleyebilir).
- Bone-heat skinning: ağırlıksız köşe 0, en çok 4 etki, normalize. `rig_check --profile unreal` **PASS**.
- Deformasyon stres metriği (kenar uzama p99.5): dirsek, diz, boyun, omurga burulması **PASS**; **omuz kaldırma 0,365 ve kalça fleksiyonu 0,364 WARN**. Stres pozu görüntüleri (`evidence/testC_stress_poses.png`) bunu doğruluyor: kollar yukarıda omuz kütlesi boyna çöküyor, çömelmede kalça hacmi kayboluyor. **Otomatik rig + otomatik skin üretime hazır değil**; omuz/kalça elle ağırlık veya düzeltici şekil ister.
- Animasyon: 6 anahtar pozlu 50 karelik `QA_Stress` klibi oyun iskeletine bake edildi; Unreal'da 2,042 sn olarak geldi. Bu bir **deformasyon test klibi**, özgün/doğal hareket değil. Mocap pilotu yapılmadı (§3).

## 7. Pilot varlıklar
**Test A — `SM_SPH_TEST_MaskStand` (statik, eskimiş maske sergileme standı)** — teknik DOĞRULANDI, görsel REVIEW_REQUIRED
| Sürüm | Sonuç | Kanıt |
|---|---|---|
| v0 (ilk model) | QA **FAIL 3**: 6 n-gon, 21 ters UV yüzü, texel yoğunluk sapması p90 1,89 | `data/testA_v0_qa_before.md` |
| v1 | Teknik geçti ama **görsel başarısız**: halka desenli tahıl yanlış yönde, bulut gibi toz; yeni metrik `flat_block_share` BC %72,7 / ORM %72 → **FAIL**. Ayrıca skill QA: 4 z-fighting + 8 gömülü yüz → düzeltildi | `evidence/testA_v1_lookdev_FAIL_flat.png` |
| v2 | skill'in "wear" katmanı yüzeyi düz boya ile kaplıyordu (gövde tek renk) | `evidence/testA_v2_lookdev_paintcoat.png` |
| **v3** | **46 PASS / 3 WARN / 0 FAIL**; skill QA PASS (z-fighting 0). 1350 üçgen, 30×26×63,7 cm, pivot tabanda, 1K BC/N(DirectX)/ORM, 2 UCX çarpışma. WARN'lar: gömülü yüzlerin açık kenarları (bilinçli), UV kaplama %50, pürüzlülük değişimi sınırda | `evidence/testA_v3_lookdev_final.png`, `data/testA_v3_qa.md` |
Dürüst görsel yargı: tahıl artık parçanın uzunluğu boyunca, renk/pürüzlülük çeşitli; ama "bakımlı yeni mobilya" gibi duruyor — ev kimliğindeki "eski, yaşanmış" yaşlanma eksik; demir bilezik fazla temiz/krom gibi; form basit (yumurta baş). Bu bir hat kanıtıdır, kahraman varlık değil.

**Test B — giyilebilir aksesuar: YAPILMADI.** Plan: Test C mankeninin kalçasına kemer (ağırlık aktarımı `garment.py`), sarkan kese için 2 kemiklik jiggle zinciri (bake), `garment.py --check` ile 0 penetrasyon, Chaos Cloth karşılaştırması. Ana karakter mesh'i yerine önce manken; MetaHuman ölçüleri için gövde dışa aktarımı ayrıca izin ister.

**Test C — `SK_SPH_TEST_Dummy`**: §6.

## 8. Unreal içe aktarma ve materyal doğrulaması (yalnız `/Game/Sandbox/AIPipeline_TEST/`)
- Kilit `aip`, her yazma işi için doğrulanmış manifest; kapı günlüğü yalnız sandbox paketlerini yazdı.
- **Test A — DOĞRULANDI (kaydedildi):** async Interchange içe aktarma → ölçek 30,0×26,0×63,7 cm (Blender ile aynı), pivot z=0, 2 dışbükey çarpışma, Nanite açık. Bulunan iki hata düzeltildi: Interchange **eski Phong** MI üretti → PBR ana materyale (`M_SPH_TEST_PBR_Master`) bağlandı; **ORM sRGB/Default** geldi → doğrusal/Masks. 6 paket kaydedildi, sonra kirli paket 0. Bilinen kusur: MI'nin adı `M_` (Interchange verdi; `MI_` olmalı).
- **Test C — KISMİ (kaydedilmedi):** ölçek 169,6 cm, fizik varlığı oluştu, anim 2,04 sn. **Hata bulundu:** Blender armatür nesnesi `Armature` adında olmadığı için iskelette fazladan kök (`SKEL_SPH_TEST_Dummy` → `root`), 37 kemik. Düzeltilmiş FBX dışa aktarıldı; aynı ada yeniden içe aktarma eski iskelete **birleşti** (iskelet kemik kaybetmez). Temiz yeniden içe aktarma için bellekten silme işi modal pencereye takıldı (üstteki uyarı).
- DENENMEDİ: gerçek sahne ışığında görsel kontrol ve oynanış testi. Ev seviyesine aktör eklemek haritayı kirletirdi; sandbox seviyesi açmak başka oturumun açık seviyesini değiştirirdi. Editör yeniden açılarak okuma da yapılmadı.

## 9. Performans, VRAM, disk
- Disk: başlangıç 81 GB boş → **39,1 GB boş**. StableGen+ComfyUI+modeller 43,1 GB (torch test ortamı silindi), taşınabilir Blender 1,34 GB, hat + kaynak dosyalar 0,44 GB, Unreal sandbox ~2,6 MB (Test A).
- VRAM: SDXL tek görüntü tepe 7,47 GB (Unreal açıkken). Cycles/OptiX bake 1K: birkaç saniye.
- Test A oyun maliyeti: 1350 üçgen, 3×1K doku (~2,4 MB uasset).

## 10. Lisans ve güvenlik kontrolleri
- Üçüncü taraf kurulum betikleri çalıştırılmadan önce okundu: blender-skills `install.ps1` (kullanılmadı — aynı adlı klasörü siliyor; elle kopyalandı), MCP eklentisi (bağlama/telemetri/güvenli mod kodu okundu), StableGen yükleyicisi (yalnız GitHub/HuggingFace/Astral kaynakları).
- İndirmeler SHA-256 ile doğrulandı (Blender zip, StableGen zip).
- Ağ: Blender MCP 127.0.0.1:9876, ComfyUI 127.0.0.1:8188, Unreal MCP 127.0.0.1:8000 — dışa açık yok.
- Smart App Control açık kaldı; engeli dolaşmak için ayarı değil, engellenmeyen PyTorch sürümünü kullandım.
- Lisanslar: blender-skills MIT, MCP MIT, StableGen GPL-3.0 (araç; çıktılar değil), Jiggle GPL-3.0, RealVisXL/SDXL Lightning OpenRAIL++, ControlNet depth/IP-Adapter/StableDelight Apache-2.0. Hunyuan3D 2.1 reddedildi (bölge). Bu hukuki görüş değildir.

## 11. Kalan eksikler ve sonraki aşama
1. **Unreal'daki "Mesaj" penceresini yanıtlayın**, kilidi bırakın; Test C'yi yeni bir adla (`TestC_v2`) temiz içe aktarın, 36 kemik + anim'i doğrulayıp kaydedin.
2. StableGen Blender içi projeksiyon (GUI): Test A'yı yeniden dokulayıp v3 ile aynı QA ve lookdev'de karşılaştırma.
3. Test B (kemer + jiggle kese, penetrasyon 0) ve Chaos Cloth karşılaştırması.
4. Test C omuz/kalça ağırlık düzeltmesi; WARN'ları PASS'e çekmek.
5. Mocap: video kaynağı + SMPL-X kaydı sizdense mixamo-llm-mocap izole pilotu; GASP veritabanına ekleme yok.
6. Test A görsel: yaşlanma (gri ağarma, tutma bölgeleri koyulaşması), demirde oksit tabakası; ev ışığında oyun mesafesinden kontrol.

## 12. Tekrar kullanılabilir komutlar
```powershell
# Test A uçtan uca (inşa → UV → yaşlandırma → bake → materyal → 2×QA → FBX → lookdev); hata olursa durur
powershell -File "Tools/AssetPipeline_20261124/pilots/run_test_a.ps1" -Tag v4
# Herhangi bir varlığa QA (profil: static | organic | wearable | skeletal)
& $env:BLENDER_EXE -b <dosya.blend> -P Tools/AssetPipeline_20261124/qa/sph_asset_qa.py -- --profile static --texture-px 1024 --out <rapor.json>
# Lookdev görüntüleri (poz için --frame N)
& $env:BLENDER_EXE -b <dosya.blend> -P Tools/AssetPipeline_20261124/qa/sph_lookdev.py -- --out <klasör> --objects <Mesh>
# MCP uçtan uca test (Blender açık, eklenti etkin)
python Tools/AssetPipeline_20261124/mcp/mcp_smoke_test.py <çıktı klasörü>
# ComfyUI (yalnız localhost)
C:\Users\berat\Tools\StableGen\ComfyUI\.venv\Scripts\python.exe -s C:\Users\berat\Tools\StableGen\ComfyUI\main.py --listen 127.0.0.1 --port 8188 --disable-api-nodes --disable-auto-launch
# Unreal sandbox işi (kilit sahibi aip; sandbox dışı yolu reddeder)
bash Tools/AssetPipeline_20261124/unreal/aip_job.sh <betik.py> <ad> <zamanaşımı> write|measure --new /Game/Sandbox/AIPipeline_TEST/...
```
Tam hat belgesi, reçeteler (A/B/C/D), kalite kapıları ve geri alma: `Docs/AssetPipeline/README.md`.

## Değişen dosyalar (tam liste)
- Yeni: `.agents/skills/blender-*` (28), `.claude/skills/blender-*` (28 sarmalayıcı), `Tools/AssetPipeline_20261124/**`, `SourceAssets/AIPipeline_TEST/**`, `Docs/AssetPipeline/README.md`, `Content/Sandbox/AIPipeline_TEST/TestA/*` (6 paket), bu rapor.
- Değişen: `.mcp.json` (+`blender`; yedek `Tools/AssetPipeline_20261124/rollback/mcp.json.before_20261124`), `.agents/skills/sphirus-asset-pipeline/SKILL.md` (+ sarmalayıcı sync), `Saved/Codex/EDITOR_LOCK.txt` (kilit, yukarıdaki not).
- Proje dışı: `C:\Users\berat\Tools\Blender`, `C:\Users\berat\Tools\StableGen`, Blender 5.3 kullanıcı ayarları (MCP eklentisi, Jiggle, StableGen), kullanıcı ortam değişkeni `BLENDER_EXE`, winget `astral-sh.uv`.
- Yayımlanmadı: GitHub'a / ChatGPTBridge `latest`'e hiçbir şey gönderilmedi.
