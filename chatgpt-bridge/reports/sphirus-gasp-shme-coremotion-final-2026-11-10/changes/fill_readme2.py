# fill_readme2.py: 2026-11-10 afternoon continuation (indoor 150, chooser context copies, idle breaks, LoadGame finding).
import io
R='Saved/ChatGPTBridge/reports/sphirus-gasp-shme-coremotion-final-2026-11-10/'; p=R+'README.md'; s=io.open(p,encoding='utf8').read()
rep=[
("| Bekleme (50 s) | **PARTIAL**: tek uzun döngü + nefes, hızlı tekrar yok; seyrek idle break kapalı | §5 |",
 "| Bekleme (50 s) | **PASS (ölçüm)**: tek uzun döngü + nefes + seyrek GASP idle break (14–26 s arayla), girdiyle anında kesiliyor; görsel REVIEW_REQUIRED | §5, §11 |"),
("| Story Framework / istasyon / kayıt regresyonu | **PARTIAL**: istasyon/ev kuralı/kamera/kayıt yazma çalışıyor; oyun içi `LoadGame` konum geri yüklemiyor (öncekiyle aynı açık risk); ev içi yürüme 150 → 200 cm/s | §7 |",
 "| Story Framework / istasyon / kayıt regresyonu | **PASS (teknik)**: istasyon/ev kuralı/kamera/kayıt yazma/yükleme çalışıyor; ev içi yürüme yeniden 150 cm/s; `LoadGame(IgnorePlayerLocation=False)` konumu ve yönü birebir geri yüklüyor (önceki \"yüklemiyor\" bulgusu test hatasıydı, §11) | §7, §11 |"),
("| Relaxed GASP seti | **BLOCKED (araç)** | §2.4 |",
 "| Relaxed GASP seti | Araç engeli kalktı (§11), **uygulanmadı** | §2.4 |"),
("| Seçim tablosu bağlam hatası | Her karede `LogChooser: Error ... expects SandboxCharacter_CMC_ABP_C` — seçim çalışıyor ama günlük doluyor. Python'dan düzeltilemiyor (bağlam yapısı API'ye açık değil); editörde tablonun Context Data sınıfı `ABP_Sph_GASP_C` yapılmalı → **AÇIK** | editör günlüğü |",
 "| Seçim tablosu bağlam hatası | **Düzeltildi (§11)**: Sphirus kopyası tablolar, bağlam `ABP_Sph_GASP_C`; aynı girdide günlükte 2359 → 0 hata, klip/veritabanı seçimi birebir aynı | `data/chooser_fix.txt` |"),
("| Ev içi kuralı (koridorda Shift) | Koşu yok: en fazla 200 cm/s. Fark: eskiden ev içi 150, şimdi GASP yürüyüşü 200 → PARTIAL | `videos/H_hall_prod.mp4` |",
 "| Ev içi kuralı (koridorda Shift) | Koşu yok; ev içi yürüme 150 cm/s (eski tempo; §11), basan ayak kayması medyan 11 → 9 cm/s | `videos/H_hall_i1.mp4` (önce: `H_hall_prod.mp4`) |"),
("2. Relaxed set (BLOCKED), seyrek idle break (deneysel durum makinesi kapalı).",
 "2. Relaxed set: bağlam aracı artık çalışıyor (§11) ama set bağlanmadı; seçim tablosu Mover AnimBP özelliklerine bağlı, ayrı iş."),
("Tümü PIE, 30 kare/s,","Tümü PIE, 30 kare/s,"),
]
for a,b in rep:
    assert a in s,a[:80]; s=s.replace(a,b)
s=s.replace("| `EF_on_c2` | bahçede efor açık (nefes ve fren) |",
"| `EF_on_c2` | bahçede efor açık (nefes ve fren) |\n| `H_hall_i1` | ev içi kural, 150 cm/s (§11) |\n| `A_loco_n1` | seçim tablosu kopyalarıyla aynı yürüme→sprint→duruş protokolü (§11) |\n| `I_idle50_n1` | 50 s bekleme, iki idle break (§11) |\n| `IO_idlecut_n1` | idle break başladıktan 3,3 s sonra W: kırılma anında kesiliyor (§11) |")
s=s.rstrip('\n')+r'''

## 11. Devam (2026-11-10 öğleden sonra): açık maddeler
Her adım manifest yedekli tek yazma işi + editör yeniden açılışı; sonra gerçek oyuncuyla PIE testi.

**11.1 Ev içi tempo 150 cm/s.** `BP_Sph_GASPCharacter`'a `SphContextSpeedScale` (varsayılan 1) eklendi; `CalculateMaxSpeed` sonucu `SphMotion.SpeedScale` ile birlikte bununla da çarpılıyor (`changes/i1_ctxspeed.py`). Oyuncu, `CharacterInputState`'i yazdığı yerde `GR_HomeContext > 0,5 ? 0,75 : 1` yazıyor (`changes/i2_indoor_speed.py`). Koridor testi: en yüksek 150 cm/s, Shift koşturmuyor; dışarıda yürüme 200 / koşu 500 / sprint 700 değişmedi (`A_loco_i1`). Basan ayağın yatay hızı (sabit yürüyüş, iki ayaktan küçüğü) medyan 11,3 → 9,2 cm/s: yavaşlatma kayma eklemedi.

**11.2 Seçim tablosu bağlam hatası.** Kök neden: kopyalanan AnimBP'nin sınıfı (`ABP_Sph_GASP_C`) satıcı tablolarının bağlam sınıfıyla eşleşmiyor (doğrulama yalnız editörde çalışıyor; paketlenmiş oyunda bu günlük yok). Önceki "Python'dan yapılamaz" sonucu yanlıştı: `InstancedStruct.import_text`, `ContextObjectTypeClass(...)` biçimindeki metni kabul ediyor. Çözüm (`changes/n1_choosers.py`): `CHT_PoseSearchDatabases_Dense` ve `CHT_CMCCharacterAnimations`, `/Game/Sphirus/Player/GASP/Choosers/` altına kopyalandı; kopyaların bağlamı `ABP_Sph_GASP_C` yapıldı (CMC tablosunun ikinci, struct bağlamı korunarak); `ABP_Sph_GASP`'taki iki `Evaluate Chooser` düğümü kopyalara bağlandı ve bağlam pini `self`'e yeniden bağlandı. Satıcının kök tablosu `CHT_PoseSearchDatabases` yalnız `MMDatabaseLOD` değerine göre Dense/Sparse/ExtremeSparse seçiyor; Sphirus'ta bu değer 0, yani her zaman Dense. Bu yüzden ABP artık Dense kopyasını doğrudan değerlendiriyor (LOD geçişi bilerek bırakıldı). Satıcı dosyalarına dokunulmadı. Sonuç: aynı girdide `LogChooser: Error` 2359 → 0; klip ve veritabanı dizisi (`A_loco_i1` ile `A_loco_n1`) birebir aynı, hız profili ±5 cm/s.

**11.3 Seyrek bekleme hareketleri (idle break).** GASP bunları yalnız deneysel durum makinesinde oynatıyor; o yol tüm hareketi değiştirdiği için açılmadı. Sahip `AC_Sph_Motion` (`changes/k1_idle.py`). Hız < 3 cm/s, girdi yok, yerde, başka montaj yok ve `IdleEnabled` koşullarında süre birikiyor. Süre `IdleNext`'i (rastgele 14–26 s) geçince 5 GASP `M_Neutral_Stand_Idle_Break` klibinden biri `DefaultSlot`'ta dinamik montaj olarak oynuyor (giriş 0,5 s, çıkış 0,6 s). Girdi gelirse yalnız kendi klibi hâlâ oynuyorsa 0,3 s'de kesiliyor; etkileşim montajı başlarsa onun yerine geçiyor. Ölçüm: 50 s beklemede iki kırılma (5,3 s ve 6,3 s), arada 24,8 s; kapsül kayması 0 cm. Kırılmanın 3,3. saniyesinde W'ye basınca 0,07 s içinde yürüme başladı ve montaj kesildi. Risk: montajsız etkileşim beklemelerinde (ör. istasyonda 15 s+ beklerken) de bir kırılma oynayabilir → REVIEW_REQUIRED.

**11.4 Kayıt yükleme.** Önceki regresyon testi `LoadGame`'i `IgnorePlayerLocation=True` ile çağırmıştı; Story Framework (`SFSaveManager_AC.LoadPlayerData`) bu durumda konumu bilerek uygulamıyor. Bu yüzden "konum geri yüklenmiyor" bir test hatasıydı. `False` ile: kayıt (1225, −696, yön 180°) → 7 m uzağa ışınla → yükle → (1225, −696, 180°) birebir; ardından yürüyüş 200 cm/s (`data/reg_save_pos.txt`). Kullanıcı kaydı test sonunda bayt bayt aynı (cmp).

**11.5 Derleme.** `BP_HybridA_Player`, ona başvuran 9 Blueprint, `ABP_Sph_GASP`, `ABP_Sph_Body_GASP`, `AC_Sph_Motion`: hatasız, güncel. Editör temiz yeniden açıldı.

Hâlâ açık: kamera süpürmesinde kök ofseti 20–27 cm; Relaxed set bağlanmadı; traversal/çarpışma kanalları; kamera yapraklardan geçiyor; cook/paket, 60 FPS, eğim/merdiven NOT_TESTED; görsel/his kabulü kullanıcıda.
'''
io.open(p,'w',encoding='utf8',newline='\n').write(s); print('README',len(s.splitlines()),'lines')
