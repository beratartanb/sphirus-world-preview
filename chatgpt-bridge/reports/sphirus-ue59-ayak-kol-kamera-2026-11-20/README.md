# SPHIRUS 5.9 — ayak teması, koşudan yürümeye kol, dar alan kamerası, zaman tabanı (2026-11-19 gece / 11-20)

Başlangıç: `beratartanb/sphirus-world-preview` @ `58fdeacca29f8f2b2b7cb755e9e67e9f4e56fe43` (rapor `sphirus-ue59-hareket-omuz-kamera-2026-11-19`).
Yerel proje: `sphirus_UE59` (UE 5.9), ev haritası `/Game/GraceRanger/Maps/L_GR_SphirusHouse`, oyuncu `BP_HybridA_Player`.

Durum etiketleri bu raporda ayrı tutulur: **UYGULANDI+KAYDEDİLDİ**, **TEKNİK DOĞRULANDI** (ölçüm), **GÖRSEL İNCELENDİ** (kareler/videolar kare kare), **GERÇEK OYNANIŞ** (oyuncu kamerası, gerçek girdi enjeksiyonu), **AÇIK / TEST EDİLEMEDİ**. **KULLANICI KABULÜ: hiçbir madde için yok** (senin açık geri bildirimin olmadan verilmiş sayılmadı).

Videoları gerçek hızda izleyemiyorum; videoların hızı `vtime.py` ile (simülasyon süresi / kare / FPS) doğrulandı, içerik kare kare incelendi. "İzleyip doğal buldum" yargısı yok.

---

## 0. Başlangıç doğrulaması ve çalışma ortamı

- Repo HEAD = `58fdeac` (yerel rapor ile aynı). Rapordan sonra `Content/` ve `Config/` altında değişen dosya yoktu.
- Kayıt dosyaları (başlangıç hash'leri, bu turda **ayrı ayrı** alındı): 5.9 kopyası `SFSaveSlot.sav` = `3d81ab9d…` (her koşudan sonra kontrol edildi, değişmedi); orijinal 5.8.4 projesi `SFSaveSlot.sav` = `4823d83a…` (dokunulmadı). Testler kendi test kaydıyla (`slot_test.sav`, `slot_f19_F20.sav`) yürüdü.
- **Eklenti engeli sürüyor.** `Black_Eye`, `Nwiro`, `PBL_Database`, `GravityScatterTool` DLL'leri 2026-11-15'te bu makinede yerelde derlenmiş ve **imzasız** (`Get-AuthenticodeSignature`: NotSigned); Akıllı Uygulama Denetimi açık (`VerifiedAndReputablePolicyState=1`). Windows güvenliğine dokunulmadı, DLL zorla yükletilmedi. Editör bu turda da yalnız oturum için `-DisablePlugins=…` ile açıldı (proje dosyası değişmedi). Desteklenen çözüm yolu: bu eklentilerin UE 5.9 sürümlerini Epic Launcher/Fab üzerinden kurmak (dağıtılmış ikili) — bu senin hesabınla yapılmalı. **Bu nedenle doğrulanamayan:** bu dört eklentinin özellikleri, paketlenmiş/bağımsız oyun (bkz. §9). Ev haritası bunlara başvurmuyor; bu raporun sonuçları "eklentiler kapalı editör PIE" sonuçlarıdır, tam entegrasyon kabulü değildir.

## 1. Zaman tabanı (ilk öncelik) — KÖK NEDEN BULUNDU, DÜZELTİLDİ

**Kusur:** veri modunda 30 Hz koşularında süre ~2 kat çıkıyordu (jog 1,03 s / sprint 1,13 s, 60 Hz'de 0,55 / 0,62 s; hız ve mesafe aynı).

**Doğrulanmış neden (kaydedici, oyun değil):** `vid.py` her kare zaman genişlemesini `(1/FPS)/gerçek kare süresi` ile hedefliyor, ama genişlemeyi **≤1,0** ile sınırlıyordu. Ekran görüntüsüz veri modunda editör ~60 fps koştuğu için "30 Hz" koşu 1/30 s adıma inemiyor, oyun her karede **1/60 s** ilerliyordu; `row.t` ise `kare/FPS` olarak (1/30) yazılıyordu. Kanıt: `Z_SP_30` etiket süresi 30,73 s, gerçek simülasyon (Σ gdt) **16,93 s**; 60 Hz'de 30,73 / 30,68 s (`data/02_…`). Yani yayımlanmış "30 Hz" veri koşuları **gerçekte ~60 Hz adımla** oynanmış; plan bölümleri oyun zamanında yarıya inmiş; dikey ayak hızı (temas eşiği) yarıya düşük hesaplanmış. Video modu (`VID_DIL=False`, ekran görüntüsüyle) etkilenmiyordu (kare süresi >1/30, genişleme <1).

**Düzeltme (kaydedici, `scripts/recorder/vidm_patch.py` #8–#10, `run2.sh`):**
- genişleme 4'e kadar çıkabilir → veri modunda gerçek 1/30 adım;
- `row.t` = **simülasyon zamanı** (Σ dünya deltası), `tf` = eski kare etiketi, `tw` = duvar saati, `dil` = etkin genişleme, `tstep` = hedef adım; her kayıtta aynı karede birlikte;
- `VID_VARDT=(25,90)` = her kare rastgele (tohumlu) adım → **değişken kare süresi** testi; `VID_NODIL` = gerçek zaman;
- `fix_t.py` eski kayıtları Σgdt ile yeniden zamanlıyor (yayımlanmış kötü örnekler yeniden hesaplandı, `data/02_…`).

**Doğrulama (`data/01_time_base_reference.txt`, kısa referans koşuları):** 30 Hz: sim 13,47 s = Σgdt, gdt medyan 0,0332, genişleme 0,63–2,57; 60 Hz: 13,52 s, 0,0166; değişken 25–90 Hz: 13,48 s, gdt 0,0096–0,0448; gerçek zaman: 13,49 s. Plan bölümleri dört modda da istenen sürede (±0,01 s). Durma süresi artık her modda aynı: jog 0,54–0,56 s / 113–117 cm, sprint 0,60–0,63 s / 175–184 cm.

**Bu turda bulunan iki test-düzeneği tuzağı (sonuçları geçersiz kılar, düzeltildi):** (a) aynı etiketle yeniden kayıtta eski JSON dosyası duruyorsa sarmalayıcı PIE'yi hemen durduruyor, kaydedici geri çağrısı kayıtlı kalıyor ve sonraki PIE'de eski planıyla (tuşlar + zaman genişlemesi) yeniden çalışıyordu → `run2.sh` önce JSON'u siliyor, patch #10 her yeni kayıtta önceki tüm kaydedicileri kapatıyor. Bu yüzden `R_CB_*` (Python kancalı fren) koşuları **geçersiz** sayıldı ve kullanılmadı. (b) `execute_console_command(None,…)` ile başlayan ön-kod, aynı DX ön-kodunun kalanını sessizce bozuyordu → cvar'lar ayrı ölçüm işiyle ayarlandı ve okunarak doğrulandı.

**Ölçüm yöntemi (`an_stop3.py`, simülasyon zamanı):** anlık giriş hızı (`v_in`) ve bırakıştan önceki 0,5 s ortalaması (`v_win`) ayrı; durma = hız <5 cm/s olan **ilk** an ve o ana kadarki kapsül **yol** uzunluğu; "held" = hız 0,30 s boyunca <5 kalıyor (toparlanma tek kare değil); temas = top (ball) kemiği zemin izinin <5 cm üstünde ve |dikey hız| <20 cm/s, **≥0,10 s** sürüyor; kayma = temas boyunca yalnız topun yatay yolu (topuk–parmak yuvarlanması bilek/topuğu hareket ettirir, topu değil; havadaki ayak sayılmaz); sol/sağ ayrı, toplam yol ve **tek temas içindeki en büyük uzaklaşma (drift)** ayrı. Sorunlu örnekler kare dökümleriyle (top yüksekliği, top uzaklaşması, klip) doğrulandı (`data/04_…`, §2).

## 2. Ayak kayması — klip-bağlı duruş freni (UYGULANDI+KAYDEDİLDİ, TEKNİK DOĞRULANDI, GÖRSEL İNCELENDİ)

**Doğrulanmış neden.** En kötü sprint örneğinin kare dökümü: sağ top 0,20 s'de zemine iniyor; FootPlacement onu kilitliyor; kapsül klibin kök hareketinden daha uzun gittiği için animasyondaki ayak 20 cm `UnplantRadius` sınırını aşıyor → kilit kopuyor, ayak basamak basamak sürükleniyor (170→197→213→230 cm). Yani kayma **kapsül freni ile duruş klibinin kök hızı arasındaki uyumsuzluk**; L/R klip fazına göre değişmesinin nedeni plantasyon anının kapsül yavaşlamasına göre nerede düştüğü. Eski fren (380/1100, giriş hızına göre sabit ivme) klibin "sabit hız → sert fren" profilini izlemiyor.

**Reddedilen adaylar (bellekte denendi, kalıcılaştırılmadı):**
- Duruşta `RootMotionFromEverything`: MM blend-stack çıkışında kök hareket özniteliği yok → kapsül anında 0 (karakter çakılıyor). RED.
- GASP kök kemik ofseti: `OffsetRootBoneEnabled` açık ama `DDCvar.OffsetRootBone.TranslationRadius`=0. 45 cm'ye çıkarıldı (cvar okunarak doğrulandı): sprint 66→75/30/37 cm — etkisiz (aynı neden: kök hareket özniteliği yok). RED.
- Python'dan kare başı hız yazma: kararsız (ve zombi kaydedici ile karıştı). RED.

**Uygulanan (sahibi `AC_Sph_Motion`, fren değerinin üretildiği yer):** her GASP klibinde bulunan `movedata_speed` eğrisi (klibin yazılı kök hızı) sürücü pozundan (blend-stack harmanlı) okunuyor. Duruşta (girdi yok, PhysBrake, montaj yok, eğri kök hızı taşıyorsa ya da hız <60) fren:
`BrakeDecel = clamp((hız − (2c − c_önceki)·ClipK) / dt, ClipMin 100, ClipMax 3000)`.
Eğri bir kare ileriye kestiriliyor, çünkü karakter BP'si `BrakeDecel`'i bir kare sonra uyguluyor (30 Hz okumada `bdw` = önceki `bd`, `data/04_…`). Kök hızı olmayan klipte (yerinde dönüş seçildiyse eğri 0) eski frene dönülüyor. `ClipBrakeOn=false` eski davranışı birebir geri getirir. Genel fren artırılmadı; jog/yürüyüş klipleri kendi profillerini izliyor.

**Sonuç (son kayıtlı durum, çalışma anı geçersiz kılma yok; `data/12_final_stops.txt`).** Duruş kontrol seti: yürüyüş ×2, jog 3,0/3,3/3,65 s, sprint 4,0/4,3/4,6 s, yürüyüş→jog→duruş, jog ve yürüyüşte 90° dönüp durma (360°/s × 0,25 s = 90° dönüş isteği), en kötü tek temas uzaklaşması (cm):

| Duruş | 19 Kas 60 Hz | **20 Kas 60 Hz** | 19 Kas gerçek 30 Hz | **20 Kas 30 Hz** | 19 Kas değişken | **20 Kas değişken** |
|---|---|---|---|---|---|---|
| Yürüyüş (faz 1 / faz 2) | 0,4 / 8,6 | **0,3 / 1,5** | 43,4 / 19,7 | **25,9 / 0,6** | 2,1 / 8,5 | **0,7 / 16,6** |
| Jog (3 faz) | 0,9 / 1,2 / 0,8 | **0,9 / 0,5 / 0,9** | 0,6 / 2,2 / 0,6 | **0,6 / 0,4 / 0,6** | 0,8 / 1,2 / 0,7 | **0,6 / 0,8 / 0,7** |
| Sprint (3 faz) | **66,4** / 22,5 / 34,2 | **1,6 / 0,6 / 1,7** | 54,6 / 32,7 / 21,9 | **9,0 / 0,6 / 0,1** | **79,1** / 21,5 / 35,8 | **24,5 / 4,5 / 0,1** |
| Yürüyüş→jog→duruş | 0,7 | **4,1** | 1,7 | **2,4** | 0,5 | **0,8** |
| Jog'da 90° dönüp durma | 9,5 | **9,6** | 36,6 | **8,9** | 25,3 | **4,9** |
| Yürüyüşte 90° dönüp durma | 2,5 | **2,5** | 9,5 | **33,3** | 3,0 | **0,8** |

"19 Kas" sütunları bu turun başındaki kayıtlı durumdur (`R_V0_*`, aynı yöntem; o andan geri alınan **yalnız** fren değildir — o koşular değişiklikten önceki proje durumudur).
**Kalan kötü örnekler, gizlenmedi:** gerçek 30 Hz'de bir yürüyüş fazı 25,9 cm (eski 43,4; sağ ayak `Relaxed_Walk_Stop_F_Rfoot` girişte zaten basılı, kapsülle birlikte sürükleniyor; 60 Hz'de aynı klip 0,3 cm); gerçek 30 Hz'de **yürürken 90° dönüp durma 33,3 cm (eski 9,5 — GERİLEME)**: MM bu durumda kök hızı olmayan `Relaxed_Stand_Turn_090_R` klibini seçiyor; değişken adımda bir sprint fazı 24,5 cm, bir yürüyüş fazı 16,6 cm. Sprint kalça çöküşü korunuyor (10–12 cm). **Bedel:** duruşlar klibin kendi yavaşlamasını izlediği için yürüyüş duruşu 42→61–69 cm, jog 116→122–149 cm uzadı; sprint 179→89–115 cm kısaldı (klip daha sert duruyor).
Yayımlanmış başlangıç bulguları (Z_SP_60 66,5 cm toplam; Z_ST_30 47,3; jog 43,3; video yürüyüş 44,7, dönerek durma 41,8) yeni zamanla yeniden hesaplandı (`data/02_…`): 60 Hz değerleri aynı kalıyor (zaman zaten doğruydu); "30 Hz" veri koşuları gerçekte 60 Hz olduğu için 30 Hz kanıtı sayılmaz — gerçek 30 Hz bu turda ilk kez ölçüldü (`R_V0_30`, yukarıdaki tablo).

Görsel: `videos/stops_fullbody_1119_left_1120_right.mp4` (baştan ayağa, zemin görünür, aynı plan/kamera; sol 19 Kas, sağ 20 Kas; GERÇEK HIZ).

## 3. Omuz–kol: koşudan yürümeye geçiş (UYGULANDI+KAYDEDİLDİ, TEKNİK DOĞRULANDI, GÖRSEL İNCELENDİ)

**Doğrulanmış neden (kaynak katmanı).** Yürüyüş veritabanı `PSD_Sph_N_Walk_F_Loops`, `M_Neutral_Transition_Run_to_Walk_L/Rfoot` kliplerini **tamamıyla** (4,4 s) içeriyordu. Oyunda MM bırakıştan 0,05 s sonra bu klibi seçip 3,8 s oynatıyordu. Kapsül 0,5 s'de yürüyüş hızındayken (180) klibin kökü 0,7 s'de hâlâ ~400 cm/s; yani yürüyüş hızında koşu kol taşıması (dirsek 87–112°) ve ardından büyük öne salınım (el 43 cm önde, göğüs hizasının 4 cm altına kadar) oynuyordu. Klip zaman çizelgesi (`data/05_…`): Lfoot'ta göğüs tepe noktası 1,1–1,35 s (el +2,6 cm spine_05 üstü, dirsek 64°); Rfoot'ta 1,2–1,3 ve 1,6–1,8 s. Relaxed geçiş klibinde de aynı salınım var (değiştirmek çözmüyor). Dirsek bu anda düz (143°): sorun ön kol değil üst kolun öne salınımı → ön kol açma terimi kullanılmadı (eklendi ama 0).

**Uygulanan:**
1. **Geçiş klibinin seçilebilir aralığı** (klip içeriği değişmedi; 16 Kasım'da projede eklenmiş `SphN_Walk_F_Loops` BranchIn izinin aralığı): Lfoot `[0–0,6]+[1,4–son]`, Rfoot `[0–0,6]+[1,9–son]`. İlk aralık kapsül yavaşlamasına denk, ikinci aralık yürüyüş dönüşlerinin kullandığı "yavaş yürüyüş çukuru" (kollar zaten yürüyüş taşımasında). Tek aralık `[0–0,6]` adayı yürüyüşte −90° dönüşü bozdu (4→25–33 cm; 3 tekrar) → RED; tam aralık analizinde −90°'nin klibin 1,45 s civarından girdiği bulundu ve ikinci aralık buna göre seçildi.
2. **Kapsam:** `RelA` (yavaşlama gevşemesi) artık yalnız *girdi tutulurken ve hız girdi yönündeyken* (dönüş/geri dönme/duruş/iniş hariç) ve havada değilken çalışıyor; `MoveA` havada 0. Geçiş kısalınca üst kol yavaşlama terimi gereksizleşti ve kolları yürüyüşten fazla kapatıyordu (abdüksiyon 3° vs 9) → `VD_Arm` 0. Genel yürüyüş taşıması (`MoveA`: köprücük hafif aşağı-öne, üst kol ±3) korunuyor.

**Sonuç (son kayıtlı durum, `data/13_final_arms.txt`, jog→ileri girdi sürerken yürüyüş):**

| Pencere (bırakıştan sonra) | el yüksekliği (spine_05'e göre) 19 Kas → **20 Kas** | dirsek 19 → 20 | üst kol abdüksiyonu 19 → 20 |
|---|---|---|---|
| 0,0–0,5 s (yavaşlama) | −8,5 → **−14,7** | 87 → 116° | 14,3 → 12,0° |
| 0,5–1,0 s | −10,3 → **−35,5** | 106 → 159° | 14,8 → 3,8° |
| 1,0–1,5 s (eski göğüs salınımı) | **−4,4** → **−35,8** | 143 → 159° | 12,1 → 7,5° |
| 1,5–2,5 s | −30,9 → −33,3 | 154 → 161° | 11,3 → 8,9° |
| doğrudan yürüyüş (referans, 20 Kas) | −33,3 | 159° | 9,6° |

10 s jog → ileri girdiyle yürüyüş; 19 Kas = o turun son kaydı `Z_jw10` (simülasyon zamanıyla), 20 Kas = son kayıtlı durum `A_jw10_f`. 2 s jog aynı eğilimde (göğüs penceresi −3,7 → −35,0). Öne salınım (el önde) 1,0–1,5 s'de 42,9 → 27,2 cm. Kısa (2 s) ve uzun (10 s) jog aynı davranıyor; geçişte ayak kayması 0,4–5,5 cm. **Kalan:** 0,5–1,0 s'de abdüksiyon kısa süre 4–5° (yürüyüş 9°) — kollar bir an gövdeye yakın; bu, yürüyüş döngüsüne harmanlamanın ilk karesi. Kapsam ölçümü (`RelA`, son kayıtlı durum): hedef durum jog→ileri girdiyle yürüyüşte en fazla 0,98; sprint tutulurken 0,00; girdisiz duruşlarda en fazla 0,27 (ortalama 0,01 — önceki yavaşlamadan kalan sönüm); jog dönüşlerinde en fazla 0,29 (ort. 0,03); yürüyüş dönüşlerinde en fazla 0,12. Yani geniş kapsam büyük ölçüde daraldı, sıfırlanmadı. Zıplama/iniş ve geri/yan hareket bu turda ayrıca ölçülmedi. Etkileşimlerde ArmW=0 koruması değişmedi; odun taşıma karelerinde el–nesne teması yerinde (`evidence/flow_carry_two_pieces.png`).
Görsel: `videos/shoulder_a35|a90|a150_1119_left_1120_right.mp4` (önden üç çeyrek / yandan / arkadan üç çeyrek; GERÇEK HIZ) ve `evidence/shoulder_*_1119_top_1120_bottom.jpg` (geçişten 1, 2, 4 s sonra). Yandan 9,0 s karesinde 19 Kas'ta ön kol göğüs hizasında öne kalkık; 20 Kas'ta kol gövde yanında aşağıda.

## 4. Keskin dönüşler ve yokuş

**Yürüyüş dönüşleri (son kayıtlı durum, `data/14_final_turns.txt`; 0,25 s içinde 180/360/540/720°/s = 45/90/135/180° istek):** ±45 4,5–5,3; ±90 **4,5–4,6**; +135 16,1; −135 16,3; +180 6,7; **−180 41,9** cm toplam yol. 
**Sola 180° (AÇIK):** 090→180 orta-klip geçişi hâlâ var (`Walk_Turn_L_090 → L_180`), tek temas 25,7 cm. BlockTransition/devam pozu adayı bu turda **denenmedi** (zaman kayma/kol işine gitti). 
**Jog 135/180° (AÇIK):** kalça alçalması 12–19 cm (`Relaxed_Run_Turn_*` klip içeriği, 19 Kas teşhisiyle aynı); +180 kaymada 34,8 cm. Klip kopyası düzenlemesi yapılmadı.
**Yokuş (AÇIK — uygulama yok, teşhis sağlamlaştırıldı, `data/08_…`):** düz 101 cm (n=17, kadans 109/dk); yukarı 6–15° 96 cm (n=7, 112/dk); yukarı >15° 91 cm (n=5, 103/dk, hız 155). Adım yalnız hızla %5–10 kısalıyor; insan yürüyüşünde dik yokuşta daha kısa adım + korunan kadans beklenir. Stride Warping'i doğru kurmak için adım ölçeği küçültülürken klip oynatma hızının da artırılması gerekiyor; MM düğümü oynatma hızını hız eşleşmesinden kendisi seçiyor (0,85–1,15) ve dışarıdan sürülemiyor. Yalnız adım ölçeği basılı ayağı geriye kaydırırdı → uygulanmadı.

## 5. Dar alan kamerası (UYGULANDI+KAYDEDİLDİ, TEKNİK DOĞRULANDI, GÖRSEL İNCELENDİ — gerçek oyuncu kamerası)

**Ölçüm (`an_camocc.py`):** baş+saç küresi (13 cm, baş ekleminin 6 cm üstü) kamera pozu/FOV ile 1509×920 görünüme izdüşürülüyor; alt-orta bölgenin (orta üçte bir, alt %60) örtülme oranı ve merkezin (gidilecek yön) örtülmesi kare kare. Kamera hareketi karaktere **göre** (ofset değişimi) ve açı adımı olarak ayrı; dünya konumundaki 12 cm adım sarsıntı ölçüsü sayılmadı.
**Neden:** dar alanda boom kısalınca (`SafeFrac`) omuz (yanal) ofseti de aynı oranda küçülüyor, kamera başın tam arkasına geçiyor; `TightRaise` ile yükselince baş/saç kadrajın alt-ortasına iniyor (19 Kas tr45: alt-ortanın >%25'i örtülü 12 kare, en fazla %50; tr0'a göre artmış).
**Uygulanan (`AC_Sph_Camera`):** `Y = Y × max(SafeFrac, YKeep)`, `YKeep = 1,0`. Yanal ofset zaten yan boşluk izleriyle sınırlı (`Yf ≤ yan mesafe − 28 cm`); kısalma yalnız geri mesafeye uygulanıyor. `TightRaise 45` korunuyor.
**Sonuç (mutfak geçişi, son kayıtlı durum `C_cam_video`):** alt-orta >%25 örtülme 12 → **0** kare (en fazla %50 → %24), merkez örtülmesi 6 → **1** kare, karaktere göre ofset adımı p99 14,9 → 15,0 cm (değişmedi), açı adımı en fazla 8°. Aday taraması: YKeep 0/0,6/0,8/1,0 → 32/31/14/0 kare.
**Kalan/sınır:** düşük tavan ve duvar köşesi için ayrı senaryo koşulmadı (mutfak geçişi dar kapı + köşe içeriyor). Atölye penceresi noktasında büyük saksı bitkisi kameranın hemen önüne giriyor (gölge karşılaştırması karesinde görüldü) — dış mekân yapraklarındaki yakın-solma iç bitkilerde yok; AÇIK. Etkileşim başlangıç/bitiş kadrajı: akış videosunda (§7) kare kare incelendi.
Görsel: `videos/camera_tight_kitchen_1120.mp4` (oyuncu kamerası, GERÇEK HIZ). Son kayıtlı durum ölçümü `data/09_…` sonunda.

## 6. Performans ve gölge kalitesi (ÖLÇÜLDÜ; yorum düzeltildi)

**Düzeltilen açıklama:** `r.Shadow.Virtual.ResolutionLodBiasDirectional=0` güneşin VSM çözünürlüğünü **karakter dahil** gölgelediği her şey için düşürür; `…DirectionalMoving` **hareket eden ışık** içindir, hareket eden karakter için ayrı bir koruma değildir. `Config/DefaultScalability.ini` yorumu buna göre düzeltildi (yedek `Saved/UE59Work/checkpoints/20261119_config/`).
**GPU A/B (aynı yol, PIE 1509×920, sırayla −1,5 / 0 / −1,5 / 0; `data/10_…`):** ShadowDepths 28,1 / 8,1 / 27,5 / ~8 ms; GPU kare p50 49,9 / 29,9 / 49,1 ms; 19,0 / 31,6 / 19,4 fps. GPU saati 2295–2340 MHz, 86 °C her iki durumda aynı. Ortam: TSR, `r.ScreenPercentage.Default.Desktop.Mode=1` (otomatik), Default 100, dinamik çözünürlük kapalı, Lumen HWRT, VSM, Nanite; **iç render yüzdesi doğrudan okunamadı**. Bağımsız/paketlenmiş ölçülmedi.
**Görsel (aynı kamera, konum, ışık; `evidence/shadow_bias_*`):** karakterin yere düşen gölgesinin kenarı bias 0'da biraz daha yumuşak, saç siluetinin gölgedeki ayrıntısı azalıyor; yüz/omuz öz-gölgesi ve yaprak gölgelerinde belirgin kayıp seçilmedi; iki karede boşta-salınım nedeniyle poz farkı var. İç mekân karesi bitki kadrajı kapattığı için geçersiz. Hareket sırası (`videos/shadow_bias_trail_ab_1120.mp4`, `videos/shadow_bias_face_ab_1120.mp4`; ilk 1,5 s −1,5, sonraki 1,5 s 0, yürürken yine aynı sıra) titreşim farkı için kare kare incelendi; belirgin titreşim farkı seçilmedi. **Karar:** 20 ms kazanç karşısında fark küçük → 0 korunuyor. Ek kalite düşürmesi yapılmadı.
**Işık:** iç mekân güneş düzeni bu turda değişmedi.

## 7. Etkileşimler ve oyun akışı (GERÇEK OYNANIŞ — son kayıtlı durum)

Etkileşim doğrulaması gerçek kurulumlar üzerinden, doğru hedefe nişan alarak (oyuncu kamerası, E tuşu) ve doğruluk değişkenleri okunarak (`hk_interact.py`: SF `TargetInteractionActor`, `CanInteract`, gün merkezi, kapı `IsOpen?`, montaj) yapıldı (`data/11_interactions.txt`):
- **Çay** (`GR_Day_Tea`, önkoşul ateş 2 + bitki 1): 1. E → `AM_GR_Day_Pour`, bitki 1→0, çay 0→1; 2. E → `AM_GR_Day_Drink`. **PASS.**
- **Maske** (`GR_MaskBench`): `AM_GR_Mask_Take` → `Inspect` → `Put`. **PASS.**
- **Yatak** (`GR_Day_Bed`): `AM_Sph_Bed`, karakter meşgul durumda. **PASS** (sonraki gün geçişi bu kısa testte izlenmedi).
- **Kapı (alt kat depo/WC, 77 cm arayla) — KUSUR, AÇIK:** depo kapısı 244 karenin 233'ünde `TargetInteractionActor` iken E **WC kapısını** açıyor; depo kapısı ikinci E'de açılıyor. İki kapının 60 cm'lik etkileşim küreleri örtüşüyor. Örtüşmeyi kaldıran aday (yarıçap 36) sorunu çözmedi ve WC kapısını hedeflenemez yaptı → dosya yedekten geri yüklendi (sha1 `e033e798`, küreler yeniden 60 cm doğrulandı). Neden StoryFramework etkileşim dağıtımında (E hedefe değil örtüşen kapıya gidiyor); satıcı koduna bu turda dokunulmadı.
- **Dolap:** haritada dolap/çekmece tipi bir etkileşim aktörü bulunamadı (etkileşim listesi: maske tezgâhı/askısı, 6 kapı, gün istasyonları). "Oyunda yok" sonucu çıkarılmadı; adı farklı bir kurulum olabilir — AÇIK.

**Tam akış (son kayıtlı durum, oyuncu kamerası, 30 Hz video):** ev → jog → ileri girdi sürerken yürüyüş → dar kapı → patika → duruş/dönüş → odun alma → kesme → iki parçayı toplama → eve dönüş → şömineye yerleştirme → yakma; ardından ayrı test kaydıyla kayıt yükleme ve odunsuz şömine reddi.
- **Akış (F19_flow_F20, 93,3 s simülasyon, video 92,4 s @30 fps = GERÇEK HIZ):** odun alındı → kesildi → iki parça toplandı (`Split` 2, `Loose` 0) → eve taşındı (`AM_GR_Day_CarryArms`, ellerde iki yarım odun, el teması karelerde yerinde) → şömineye yerleştirildi (ateş 1) → yakıldı (ateş 2). **PASS.** Ayrı parça koşusu (`F19_pieces_F20`) da PASS.
- **Kayıt yükleme (F19_loadfire_F20, test kaydı `slot_f19_F20.sav`):** yüklenen durumda (2 parça) şömine yakıldı. **PASS.** Odunsuz şömine (`emptyfire`) yakılmıyor — beklenen ret.
- **Toplanan parçalar dünyada kalıyor mu?** Kayıt verisinde iki parça toplandıktan sonra eski yerlerinde "görünür" görünüyordu; parça başına bayrak okuyan koşu (`F19_pieces_PV`, `hk_pieces.py`) her parçanın alındığı anda **aktör düzeyinde gizlendiğini** gösterdi (`hidden`=1; mesh bayrakları değişmiyor). Yani sahnede kalmıyorlar; kaydedicinin kök-görünürlük süzgeci yanıltıcıydı. **Kusur bulunmadı.** (Karedeki yerdeki açık renkli kütük havuz parçası değil, sahne dekoru.)
- **Şömine görseli — AÇIK KUSUR:** sayaç, ışık (`GR_Day_FireLight`, `HearthGlow`), ses (`SC_Campfire`), duman ve `Şömine / E Odun koy / Yak` istemi çalışıyor; **belirgin alev görünmüyor**. Odadan bakış (`videos/fireplace_lit_view_1120.mp4`, `evidence/fireplace_lit_room_view.png`, yakarken `evidence/fireplace_lighting_close_player_camera.png`, reddedilen PIE adayı `evidence/fireplace_lit_room_view_PIE_candidate_fx_on_logs_REJECTED.png`): kütüklerin altında aşırı pozlanmış turuncu-beyaz parıltı var, alev biçimi okunmuyor; ocak ağzının sağında taş yüzeyin önünde ayrıca beyaz bir leke duruyor. Kurulumda 5 `N_CampFire` Niagara efekti kütüklerin (x≈1462) 24–32 cm önünde (x 1430–1438). Efektleri kütüklerin üstüne taşıyan aday yalnız PIE'de denendi: parıltı da kayboldu, yani `N_CampFire` burada okunur alev üretmiyor. Bir şey kaydedilmedi. Ayrıca diz çöküp yakarken kamera taş duvara/rafa bakıyor: istasyonun kendi kamera kurgusu (`GR_CamLoc/Aim/Fov` tanımlı) bu sırada kullanılmıyor. Gerçek alev görseli Niagara düzeyinde ayrı bir çalışma gerektiriyor. Ekranı parlatan ışık tamamlanmış ateş görseli sayılmadı.

## 8. Geri dönüş yolları (değişen her varlığın değişiklikten önceki doğrulanmış yedeği)

`Saved/Codex/SHME_V233_20261027/checkpoint/manifests/<ad>/…` (sha1 doğrulamalı):
- `ue59_m21_clipbrake_215213` (AC_Sph_Motion, fren grafiği öncesi), `ue59_m21_clipbrake2_*`, `ue59_m21_clipdef_221817` (AC_Sph_Motion + BP_Sph_GASPCharacter varsayılanlar öncesi);
- `ue59_m21_armscope_222911` (ABP_Sph_Body_GASP kapsam/ön kol öncesi), `ue59_m21_vdarm_225520`, `ue59_m21_vdarm0_232504`;
- `ue59_m21_r2w_223619` (iki geçiş klibi + PSD_Sph_N_Walk_F_Loops, **tam aralık = 19 Kas hali**), ara adaylar `_r2w2_`, `_r2wfull_`, `_r2w3_`, `_r2w4_231721` (son yazma öncesi);
- `ue59_m21_camykeep_*`, `ue59_m21_camykdef_*` (AC_Sph_Camera);
- `ue59_m21_doorrad_005410` (L_GR_CurrentHouseContent orijinali — geri yüklendi; şu anki dosya bu yedekle aynı).
Hızlı kapatma anahtarları: `ClipBrakeOn=false` (eski fren), `YKeep=0` (eski kamera), geçiş aralığı için `w_r2w_full.py` (tam aralık).

## 9. Kayıtlı durum, yeniden açılış, bağımsız oyun

Tüm değişiklikler kaydedildi (manifestler §8). Editör 2026-11-20 ~01:05'te yeniden açıldı (`emb_1120a`, UE 5.9.0, eklentiler yalnız oturum için kapalı). Son kanıtlar (§2–§7 "20 Kas" sütunları, videolar) **bu açılıştan sonra, çalışma anı geçersiz kılma olmadan** üretildi. Kayıtlı değerler okunarak doğrulandı (`data/17_…`): fren CDO ve şablonda açık; kamerada `TightRaise` 45, `YKeep` 1; kol terimleri; BranchIn aralıkları; gölge bias 0; kirli paket yok. 5.9 kaydı `3d81ab9d…` ve 5.8.4 kaydı `4823d83a…` değişmedi.
**Bağımsız oyun:** `UnrealEditor.exe … -game` (pişirilmemiş, eklentiler kapalı) ev haritasını 48,7 s'de yükledi, `BP_GM_GR_GraceRanger` oyun modu başladı, ölümcül hata yok. Yalnız iki hata var: açık editörle MCP portu çakışması. **Girdiyle oynanış bu açılışta test edilmedi; paketleme yapılmadı** (eklenti engeli ve süre).

## 10. Özet durum tablosu

| Konu | Uygulandı+kaydedildi | Teknik doğrulandı | Görsel incelendi | Gerçek oynanış | Açık / sınır |
|---|---|---|---|---|---|
| Zaman tabanı (kaydedici) | evet (araç) | evet (4 mod) | – | – | eski "30 Hz" veri kanıtları geçersiz |
| Duruş kayması (klip-bağlı fren) | evet | evet (60/30/değişken) | evet (yan video) | ev akışında duruşlar | 30 Hz yürüyüş fazı 26, 30 Hz yürürken dönüp durma 33 (gerileme), değişken sprint 24,5 cm; duruşlar daha uzun |
| Koşudan yürümeye kol | evet | evet | evet (3 açı) | akış videosu | 0,5–1,0 s abdüksiyon 4° |
| Kol terimlerinin kapsamı | evet | evet (hedef 0,98; sprint 0; duruş/jog dönüşü ≤0,29) | – | – | zıplama, geri/yan ölçülmedi |
| Keskin dönüşler | – (aralık seçimi −90'ı korudu) | evet | – | – | −180 yürüyüş 42 cm, jog 135/180 alçalma 12–19, +180 jog 35 cm |
| Yokuş adımı | – | evet (teşhis) | – | – | uygulanmadı (oynatma hızı kontrolü yok) |
| Dar alan kamerası | evet | evet | evet | evet (mutfak) | düşük tavan senaryosu ayrı koşulmadı; atölyede bitki kadrajı kapatıyor |
| Gölge bias / performans | yorum düzeltildi | evet (A/B ×2) | evet | – | iç render yüzdesi okunamadı; bağımsız ölçülmedi |
| Çay / maske / yatak | – (çalışıyordu) | evet | evet | evet | yatak sonrası gün geçişi izlenmedi |
| Kapı (depo/WC) | – (aday geri alındı) | kusur doğrulandı | evet | evet | E yanlış kapıyı açıyor (SF dağıtımı) |
| Dolap | – | bulunamadı | – | – | açık |
| Tam akış + kayıt yükleme | – | evet | evet | evet | şömine alev görseli eksik |
| Eklentiler / paket | – | engel doğrulandı | – | – | Fab/Launcher 5.9 kurulumu gerekli |
| Kullanıcı kabulü | **yok** (hiçbir madde) | | | | |

## Klasör

- `data/` — tüm tablolar ve ham analiz çıktıları (numaralı). `raw/` — sorunlu örnekleri yeniden hesaplamaya yetecek kayıtlar (`.json.gz`, simülasyon zamanlı). `scripts/` — analiz, kanca, yazma, sıra betikleri; `scripts/recorder/` — kaydedicinin kullanılan sürümleri (+ akşam öncesi `vidm_patch`).
- `videos/` — GERÇEK HIZ (vtime ile doğrulandı, `data/15_video_timing.txt`). `evidence/` — durağan karşılaştırmalar.

## Bridge dünya önizlemesi

Bu turda dünya görüntüsünü değiştiren kalıcı bir değişiklik yok (gölge ayarı 19 Kasım'daki gibi; kapı alt seviyesi orijinaline döndü; kamera ve hareket değişiklikleri dünya görüntüsü değil). Bu nedenle Bridge önizlemesi yeniden dışa aktarılmadı; `chatgpt-bridge/latest` ve `chatgpt-world-latest` sürümü 19 Kasım dışa aktarımıyla (`2026-11-19_174051_964355_346de9`) tutarlı.
