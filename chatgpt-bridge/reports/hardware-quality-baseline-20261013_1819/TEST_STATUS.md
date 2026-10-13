# Test / eksik listesi

Teknik durum etiketleri. Hissel ve sanatsal onay ayrıdır ve kullanıcıya aittir. Özet: BLOCKED 3, FAIL 2, NOT_IMPLEMENTED 2, NOT_TESTED 5, PARTIAL 8, PASS 36, SEE_PUBLISH 1

| # | Test | Durum | Kanıt / not |
|---|---|---|---|
| 1.1 | Proje/motor/harita/karakter zinciri canlı editörden doğrulandı | **PASS** | inventory/editor_state.json; README §1 |
| 1.2 | Başlangıç ayar/config anlık görüntüsü + Content/Config/Plugins manifesti | **PASS** | config_snapshot/ (yerel), raw/preserve_manifest_before.json (yerel) |
| 1.3 | Test sonunda geçici değişiklikler geri alındı, proje korundu | **PASS** | raw/preserve_manifest_diff.json (0 fark), raw/final_editor_state.json, README §10 |
| 1.4 | Kullanıcı dosyası korunması: <kullanıcı>/OneDrive/Documents/Unreal.png | **FAIL** | HighResShot yol hatası dosyanın üzerine yazdı; OneDrive sürüm geçmişinden geri alınabilir (README §10) |
| 2.1 | CPU/GPU/fiziksel VRAM/RAM/disk/OS/sürücü/UE envanteri | **PASS** | INVENTORY.md |
| 2.2 | Çözünürlük, iç render %, yükseltme, dinamik çöz., VSync, FPS sınırı | **PASS** | INVENTORY.md; README §3 |
| 2.3 | Scalability/Lumen/Nanite/gölge/streaming/foliage ayarları | **PASS** | inventory/cvars_A_initial.json |
| 2.4 | Eşzamanlı uygulamalar ve shader derleme durumu | **PASS** | INVENTORY.md; README §1 (Faz 1/2) |
| 2.5 | GPU sıcaklık/güç/saat kısıtı (sensör) | **PASS** | raw/gpu_monitor_nvsmi.csv, raw/env_by_window.json |
| 2.6 | CPU sıcaklık/güç kısıtı | **NOT_TESTED** | CPU sensörü okunmadı; hüküm verilmedi |
| 2.7 | Süreç başına GPU belleği | **BLOCKED** | nvidia-smi WDDM altında süreç belleğini N/A gösteriyor; UE kendi yerel kullanımını CSV ile raporladı |
| 3.1 | Geçmiş kalite azaltmalarının dosya kanıtlı denetimi | **PASS** | HISTORY_QUALITY_REDUCTIONS.md |
| 3.2 | Gerekçesi bilinmeyen azaltmaların ayrılması | **PASS** | HISTORY_QUALITY_REDUCTIONS.md (c) |
| 3.3 | Değişiklik geçmişinin eksiksizliği | **PARTIAL** | Git yok, sohbetler yok; 09-25 sonrası çevre raporu yok |
| 4.1 | A editör statik 5 nokta × 3 tekrar | **PASS** | raw/measurements.csv (editor_viewport_static A) |
| 4.2 | B editör görüntü alanında | **BLOCKED** | r.ScreenPercentage/r.Editor.Viewport.ScreenPercentage editör görüntü alanına uygulanmadı (geçiş maliyetleri birebir aynı) |
| 4.3 | B PIE (5 nokta + 2 rota × 3) ve standalone 1080p | **PASS** | raw/measurements.csv (PIE B, SA_B_1080) |
| 4.4 | C editör statik 5 nokta × 3 tekrar | **PASS** | raw/measurements.csv (editor_viewport_static C) |
| 4.5 | C PIE rotaları kararlılık | **FAIL** | VRAM bütçe aşımı; rota başına 42–341 >50 ms takılma (Faz 1 ve 2) |
| 4.6 | C standalone 1080p | **PASS** | 22.5 FPS, takılma 0, VRAM 6.0/7.04 GB |
| 4.7 | A/B/C PIE rotaları R1, R2 × 3 tekrar (Faz 1) + A/C Faz 2 | **PASS** | raw/measurements.csv |
| 4.8 | D hafif kontrol ortamı (hareket/kamera) | **PASS** | raw/pie_lab_D_*.json, MOTION_CAMERA.md |
| 4.9 | FPS sınırı/VSync/dinamik çözünürlük maskeleme kontrolü | **PASS** | PIE world max tick rate 60 tespit edildi; ctrl_B_uncapped, ctrl_A_uncapped, ctrl_A_sp100 |
| 4.10 | Darboğaz atfetme (bitki/VSM tanıları) | **PASS** | diag_A_nofoliage, diag_A_novsm |
| 4.11 | Editörden bağımsız standalone ölçüm | **PASS** | SA_A_1080, SA_B_1080, SA_C_1080, SA_A_1523x587 (tek poz, rota değil) |
| 4.12 | Paketli Development build ölçümü | **BLOCKED** | Paket/cook çıktısı ve yapılandırması yok; proje onarımına girilmedi |
| 4.13 | Unreal Insights / Memory Insights izi | **NOT_TESTED** | CSV profiler + GPU CSV istatistikleri kullanıldı |
| 4.14 | Texture streaming durumu | **PASS** | CSV TextureStreaming/* (bütçe aşımı görülmedi; WantedMips ≈ pool) |
| 4.15 | Isınma/ilk yükleme beklemeleri ayrı | **PASS** | Editör açılışı 4 dk 7 s; standalone harita 70–86 s; ilk 1800 kare ayrı |
| 5.1 | Yerinde fare dönüşü postürü | **PASS** | Ölçüldü; dört ortamda aynı (MOTION_CAMERA H1). Hissel onay kullanıcıda |
| 5.2 | Kısa yürüyüş ilk/son adım | **PASS** | MOTION_CAMERA H2 |
| 5.3 | Walk/tempo/sprint ayrımı | **PASS** | 132/245/490 cm/s |
| 5.4 | 45/90/180 dönüş frenleme ve ağırlık aktarımı | **PARTIAL** | 180° roll farkı kare hızına duyarlı olabilir; tek örnek |
| 5.5 | İleri–geri zıt yön | **PASS** | MOTION_CAMERA H5 |
| 5.6 | Sprint + art arda sağ–sol donması | **PASS** | Ölçüldü: hafif ortamda yok; evde kapı direği çarpışması (H6) |
| 5.7 | Çaprazda ikinci launch / yanlış eğilme | **PARTIAL** | Bu girişlerle gözlenmedi; kanıt yetersiz (H7) |
| 5.8 | Ayak kayması | **PARTIAL** | Yaklaşık ölçüt; görünen ve sürücü iskelette benzer |
| 5.9 | Yerinde zıplama vs ileri atlayış | **PASS** | MOTION_CAMERA H9 |
| 5.10 | Kamera iç/dış mesafe, duvar, kapı, merdiven (lab), eğim | **PASS** | MOTION_CAMERA Kamera tablosu |
| 5.11 | Kamera ev içi merdiven / alçak tavan / tavan arası | **NOT_TESTED** | Yalnız lab merdiveni |
| 5.12 | Karakter görünürlüğü (bitki örtmesi) | **PARTIAL** | İz ölçütü çarpışmasız bitkiyi görmüyor; klipte örtme görüldü |
| 5.13 | Farklı gerçekleşen kare hızlarında karşılaştırma | **PASS** | 60 / 30 (gerçek) / 47–54 / 27–33 FPS |
| 6.1 | Karakter önden/yandan/arkadan/¾/oyun kamerası | **PASS** | images/charshots_lab_* |
| 6.2 | Karakter oranları sayısal (boy, baş/vücut) | **PARTIAL** | Kemik ölçüleri var; kafatası tepesi/boy ölçülemedi |
| 6.3 | Onaylı referansla benzerlik | **NOT_TESTED** | Onaylı referans bulunamadı; puan uydurulmadı |
| 6.4 | Çevre A↔C eşleştirme ve ayardan bağımsız eksikler | **PASS** | CHARACTER_ENVIRONMENT_GAMEPLAY §2; images/diff |
| 6.5 | Rotanın tamamının görsel değerlendirmesi | **PARTIAL** | 5 nokta + R1 klibi |
| 6.6 | Ev–gölet rotası oynanabilirliği | **PASS** | 20/20 R1, 15/15 R2 varış |
| 6.7 | Etkileşimler (kapı/kol kapı/tavan arası/vent/sandık) | **NOT_TESTED** | Aktörler mevcut; giriş denenmedi |
| 6.8 | Başlangıç/yeniden başlatma | **PARTIAL** | Başlangıç noktası kaydedildi; yeniden başlatma denenmedi |
| 6.9 | Kayıt/yükleme | **NOT_IMPLEMENTED** | Proje SaveGame sistemi yok |
| 6.10 | Maske/algı/görev | **NOT_IMPLEMENTED** | Henüz uygulanmamış |
| 7.1 | Tarih-saatli rapor klasörü ve README | **PASS** | Bu klasör |
| 7.2 | Ham ölçüm CSV/JSON | **PASS** | raw/measurements.csv + raw/*.json; ham CSV profilleri yerelde |
| 7.3 | Eşleştirilmiş görüntüler ve kısa klipler | **PASS** | images/, clips/ |
| 7.4 | REPRODUCE.md | **PASS** | REPRODUCE.md |
| 7.5 | GitHub yayını ve doğrulama | **SEE_PUBLISH** | Bu klasör yayının kendisidir; blob hash ve LATEST.json değişmedi doğrulaması yerel publish_status.json dosyasında |
