# SPHIRUS UE 5.9 — Tur 9: Guardian hareket, geçiş ve fiziksel tepki raporu (2026-11-24)

**Durum: PARTIAL.** Birinci öncelik olan hızlı A/D ayak kayması aynı eski senaryoda giderildi ve kayıtlı + yeniden açılmış sürümde doğrulandı. Koşu→yürüyüş zinciri ve öne düşme/kalkış düzeltildi. Aşağıda "Açık kalanlar" bölümündeki maddeler çözülmedi veya hiç ele alınmadı. **USER_ACCEPTED yazılmadı**; oynayıp kabul etmen gerekiyor.

- Proje: `sphirus_UE59`, oyuncu `BP_HybridA_Player`, test haritası `L_Sph_MoveTest`, ev haritası `L_GR_SphirusHouse`.
- Başlangıç yedeği: `Saved/UE59Work/r9/ckpt0/` (dosya kopyası + sha1). Yazma manifestleri: `ue59_m29_r9save1/2/3` (`scripts/manifests.txt`).
- Kullanıcı kaydı `SFSaveSlot.sav` baştan sona aynı: `3d81ab9dc708`. Satıcı klipleri ve veritabanları değiştirilmedi.
- Diğer oturumun daha yeni değişiklikleri (kamera `HeadXTight`, ev haritası) korundu.
- Bütün sayılar son kayıttan (`r9save3`) sonra editör kapatılıp açılarak ölçüldü; aksi belirtilenler ayrıca işaretli.

## 1. Hızlı A/D ayak kayması (birinci öncelik) — ÖLÇÜLDÜ: giderildi, bir kenar durumu açık

Aynı eski senaryo (`planR1`, koşuda A↔D): **36.7 cm → 1.9–2.2 cm**.

| Senaryo | 60 Hz | 30 Hz | Değişken Hz |
|---|---|---|---|
| Eski senaryo `old_R1` | 2.2 | 1.7 | 2.0 |
| Koşu A↔D `AD_run` (2 tekrar) | 1.8 / 1.8 | 1.6 / 1.8 | 2.0 |
| Sprint A↔D `AD_sprint` | 1.8 | koşulmadı | koşulmadı |
| W+A↔W+D koşu `WAWD_run` | 1.4 | 1.3 | koşulmadı |
| W+A↔W+D sprint `WAWD_sprint` | 1.1 | koşulmadı | koşulmadı |
| Fren sırasında yeniden komut `brake_re` | 2.7 | 4.0 | koşulmadı |
| Yürüyüş A↔D `AD_walk` | 2.9 | koşulmadı | koşulmadı |
| Kısa tekrarlı dokunuş `AD_taps` (2 tekrar) | **23.3 / 23.5** | 3.1 | 3.6 |

(Değerler: temas sırasında ayağın yerde kaydığı en kötü mesafe, cm.)

**Üç gerçek kök neden ve çözümü:**

1. **Komut karesi.** Dönüş yöneticisi bir önceki karenin girdisini okuyordu; komutun geldiği karede kapsül normal ivme/sürtünmeyle "0.25 sn'de döndüm" tahmini üretiyor, hareket eşleştirme 180° dönüş klibine son basış anından hemen önce giriyordu. Çözüm: bekleyen girdi hıza tersse aynı karede yöneticinin açılış değerleri kullanılıyor (`BP_Sph_GASPCharacter.CalculateMaxAcceleration / CalculateGroundFriction`, `m_flip9`, `m_flip9b`).
2. **Erken ve kısa basış.** Komut, öndeki ayak inmek üzereyken gelirse ayak klibin geniş basışından ~30 cm kısa iniyor, ayak kilidi 45 cm'de kopuyor ve ayak yerde sürükleniyordu. Çözüm: dönüş/pivot veritabanları için ayrı kilit ayarı (`PlantSettings_Turns`, 85 cm; `ABP_Sph_GASP`, `c_plturn9`). Ayak gerçekten bastığı yerde kalıyor, pivot daha dar ve dik oluyor; klip ayağı kaldırınca serbest kalıyor.
3. **Denenip neden olmadığı gösterilenler:** karışım süresi, yörünge ağırlığı (10→4), klip hız eğrisinin karışmış/gerçek değeri. Bunlar etkisizdi ve geri alındı.

**Açık kenar durumu (dürüst kayıt):** `AD_taps` 60 Hz'de her iki tekrarda aynı tek örnek: 0.25 sn'lik çok kısa dokunuşta, dönüşün tam ortasında (hız ~35 cm/s) ters komut gelince başlangıç klibi seçiliyor ve basan ayak iki karede ~23 cm yer değiştiriyor. Yönetici eşiğini (250→200 cm/s) düşürmek sorunu başka bir dokunuşa taşıdı, o yüzden geri alındı. Bu örnek çözülmedi. Kare: `evidence/tap_recommand.jpg`, video `videos/r9V_AD_taps_side.mp4` (6.5 sn civarı).

Görsel: `videos/r9V_AD_run_side.mp4`, `r9V_AD_run_sh.mp4` (omuz kamerası), `r9V_AD_sprint_back.mp4`. İncelediğim karelerde pivot dar ve dik, bacak gerilmiyor (`evidence/AD_run_pivot.jpg`). Videoların tamamını kare kare izlemedim.

## 2. Koşu–tempo–yürüyüş zinciri — ÖLÇÜLDÜ: düzeldi

- Kök neden: adım düşürmede yörünge tahmini frenlemeden bağımsız ~0.25 sn'de yürüyüş hızına iniyordu; hareket eşleştirme geçiş klibini 0–0.10 sn'de bırakıp kapsül hâlâ 250–380 cm/s iken yürüyüş döngüsünü gösteriyordu.
- Çözüm: yalnız yürüyüş/tempoya inişte ve yalnız ileri harekette geçerli kademeli hız sınırı (`AC_Sph_Motion.DmCap`, `m_dm9`, `m_dmcap9/9b/9c/9d`).
- Sonuç: koşu→yürüyüş %90'a **0.36 → 0.78 sn**, geçiş klibi oynuyor, "kapsül klipten hızlı" süresi **0.20 → 0.00 sn** (`data/bob.txt`). Zincir kayması 60/30/değişken: 1.8 / 1.8 / 1.9 cm. Tempo zinciri 2.4 cm.
- Geri koşu→geri yürüyüş: bu turdaki ilk sürüm 44–56 cm kaydırıyordu (geri yönde geçiş klibi yok); rampa ileri harekete sınırlanınca **4.3 cm**.
- **Yan etki (karar senin):** Shift bırakıldıktan sonra karakter yürüyüşe ~0.4 sn daha geç iniyor; hemen ardından durulursa duruş ~60 cm daha uzun. Ev testindeki rota bu yüzden odunu ıskalıyor (bkz. 8).
- Açık: sprint→koşu geçişi tek örnekte doğrudan koşu döngüsüne gidiyor (0.84 sn); incelenmedi.

## 3. Bu turda bulunan ve düzeltilen gerilemeler

İlk kayıttan sonraki regresyonda Tur 8 kazanımı kaybolmuştu; gizlemedim, nedenini ayırdım:

- **Sprint→geri, 30 Hz: 2.2 → 16.1 cm.** Neden: 1. maddedeki "komut karesi" düzeltmesi geri komutunda da tetiklenip yanlış bir pivotu bir karelik seçtiriyordu; bırakma anında doğru pivot yerine geri başlangıç klibi geliyordu. Çözüm: oyuncu geri-fren beklemesini bildiriyor (`AC.RcNoFlip`), bekleme sırasında yalnız ivme açılışı atlanıyor (`m_holdflip9`, `m_holdflip9b`, `m_holdexit9`). Sonuç: `f9_B_30` **2.3 cm**, `f9_K_30` **1.7 cm**, `r9_old_U_B_30_F` 2.3 cm.
- Eski 24 kombinasyonun tamamı (12×60 Hz, 7×30 Hz, 5×değişken): yerde kayma en kötü **4.2 cm**, 10 cm üstü yok (`data/slide24.txt`).

## 4. Düşme, destek ve kalkış — ÖLÇÜLDÜ + GÖRSEL: öne düşme düzeldi

- Belirti: yüzüstü düşüşte eller 36 / 62 cm, baş 53 cm havada kalıyordu.
- İlk teşhisim (duruş katmanı) yanlıştı: katman tamamen kapalıyken poz aynı kaldı. Gerçek sahibi görünür gövdedeki **öne eğilme sınırlayıcısı** (`PL_Spine3/5`): yatay gövdeyi 90° eğilme sanıp omurgayı 40° geri büküyordu.
- Çözüm: sınırlayıcının tavanı ve duruş çıkışları düşme/yatma sırasında 0'a iniyor, kalkışta pelvis yükseldikçe geri geliyor (`m_fallposture9`, `m_fallposture9b`).
- Sonuç (4 kayıt, 60 ve 30 Hz): yatışta eller **3.5–6 cm**, baş 36–39 cm; görünür gövde sürücü pozla örtüşüyor. Önce/sonra: `evidence/fall_before_lying.jpg`, `fall_after_lying.jpg`, `fall_after_getup.jpg`; video `r9V_fall_side.mp4`, `r9V_fall_sh.mp4`.
- Açık: takılma anında ayak ucu engelin içinde 30 Hz'de 3.4–4.8 cm (1–2 kare), kalkışta 2.0 cm. Yan ve arkaya düşme klibi yok; yapılmadı. Kalkış klibi çevreye/alana göre seçilmiyor.

## 5. Yorgunluk — ÖLÇÜLDÜ: kademeli

Sabit değer verilmeden, tek zincir (`r9_fatigue_chain_60_F`, `data/fatigue.txt`): sprintte yorgunluk 0 → 0.17 → 0.57 → 0.99; hız 556 → 526 → 515 cm/s; adım süresi 0.60 → 0.66 sn; boyun/gövde eğimi artıyor. Durunca 8 sn'de 0.56, yürüyüş + dinlenmeyle 0; sonraki sprint yeniden 571 cm/s. Video `r9V_fatigue_sh.mp4` 60 MB olduğu için depoya yüklenemedi; yerelde `Saved/Codex/Day_20261107/videos/` altında. Bu turda yorgunluk mantığına dokunulmadı; yalnız ölçüldü. Yorgunluğun dengeye/sendelemeye etkisi ölçülmedi.

## 6. Başlangıçlar — açık

- Dönerek koşu başlangıcı (90°): baş düşmesi hâlâ **16.9 cm** (`data/starts.txt`). Kaynak satıcı klibi (`Run_Reface_Start`: gövde 39° eğim, pelvis −11 cm). Dalış sınırlayıcı ~−2.5 cm kazandırdı (BOB_Dip 0.8/3/12); omurga denetleyicisini hızlandırmak ve ek eğim sınırı etkisizdi, reddedilip kaldırıldı. Gerçek çözüm (yürüyüş dönüş klibiyle başlayıp hızlanmak) denenmedi.
- 180° yürüyüş başlangıcı: iki örnekte ayak 47–48 cm yere çok yakın (1–1.5 cm) ilerliyor (`r9_starts_turn_walk_60_F`). Karede arka ayağın parmak ucuyla öne çekildiği görülüyor (`evidence/walk180_start_drag.jpg`, `r9V_starts_walk_side.mp4`); kayan basış mı alçak adım mı kesin ayıramadım. Çözülmedi.
- Sabit döngülerde zıplama (pelvis tepe-tepe): yürüyüş 4.8, koşu 5.6, sprint 3.3 cm; kamera 1.0–1.2 cm (`data/bob.txt`). Eski SHMS/SHME ile karşılaştırma yapılmadı.

## 7. Hiç ele alınmayan veya değişmeyen maddeler

- **Sendeleme (madde 6):** destek ayağına göre seçim, yorgunluk/yük etkisi, güvenli fazda çıkış — çalışılmadı. Mevcut davranış Tur 8 ile aynı.
- **Kalan temaslar (madde 8):** yük taşırken el–duvar 5.4 cm, 30 cm basamakta kaval 5.0 cm, 30 Hz'de 4.1 cm — aynı duruyor (`data/contact.txt`).
- **Guardian anatomisi (madde 4):** ham klip / yeniden hedefleme / düzeltilmiş karşılaştırması yapılmadı. Yalnız yatış pozundaki omurga bükülmesi düzeldi.
- **Kamera (madde 10):** hiçbir kamera değişikliği yok; koridor, maske inceleme, düşme kadrajı çalışılmadı. Düşmede omuz kamerası videosu var ama değerlendirmedim.
- **Performans (madde 13):** bu turda ölçülmedi. Eklenenler birkaç matematik düğümü ve iki değişken; ölçüsüz "maliyet yok" demiyorum. Standalone, paketleme ve ev performansı test edilmedi.
- **Gamepad/analog:** fiziksel cihaz yok, test edilmedi.

## 8. Ev etkileşimleri — tam akış geçti, kısa rota testi başarısız

- Tam akış (`F19_flow_R9`: mutfak → kapı → odun al → taşı → kes → iki parçayı topla → şömineyi kur ve yak): **PASS**.
- Kısa rota (`F19_pieces_R9/R9b/R9c`) ve onun kaydını yükleyen `loadfire`: **3/3 FAIL** (odun alınmadı). Tur 8'de geçiyordu. Neden: 2. maddedeki daha uzun koşu→yürüyüş inişi yüzünden karakter odun noktasını ~75 cm geçip duruyor, E menzil dışında kalıyor. Etkileşim kodu bozulmadı ama bu, kontrolde hissedilecek bir değişiklik; testi geçirmek için rotayı veya eşiği değiştirmedim.
- Yatak, maske, dolap, çay videoları çekildi (`f9h_*`, bu rapora eklenmedi); içeriklerini izleyip değerlendirmedim.

## 9. Testlerin gerçek dağılımı

Her kaydın benzersiz kimliği var (`r9_<plan>_<hz>_<etiket>`, eski set `f9_<plan>_<hz>`); aynı etiket yeniden kullanılmıyor. Hangi planın hangi kare koşulunda gerçekten koştuğu: **`data/hz_matrix.md`** ("koşulmadı" açıkça yazılı). Eski 24'lük set 12 plan×60 Hz, 7×30 Hz, 5×değişken Hz'dir; bütün planlar üç koşulda koşmadı.

Süreyi kısaltmak için sonradan çıkardıklarım: Tur 8'den kalan 9 tekrar videosu, Tur 9 videolarının ikinci/üçüncü açıları, 30 Hz ve değişken Hz'de birkaç plan (tabloda "koşulmadı").

Videolar gerçek hızda, sabit tam beden yan/arka kamera veya gerçek omuz kamerası. Yan kamera gölge tarafından çekildi; aşırı pozlama yok ama karakter arkadan ışıklı ve biraz koyu.

## 10. Değişen varlıklar

| Varlık | Değişiklik |
|---|---|
| `ABP_Sph_GASP` | `PlantSettings_Turns` (85 cm) + "Pivots" etiketine göre seçim; `SphSelTime` |
| `AC_Sph_Motion` | `RcOpen`, `RcKMax`, `RcNoFlip`, `DmMin`, `DmOpen`, `DmCap`, `DmRate`, `DmRateK`, `DmWalkV`, `GaitV`, `ClipSp` |
| `BP_Sph_GASPCharacter` | ivme/sürtünme/fren/azami hız hesapları (komut karesi açılışı, kademeli hız sınırı) |
| `BP_HybridA_Player` | düşme ağırlığı `PS_FW`, eğilme sınırlayıcı tavanı, bekleme bildirimi; dalış sınırlayıcı 0.8/3/12 |

Bilinen artıklar: oyuncuda kullanılmayan 5 değişken (`PS_LC`, `PS_LnFree`, `PS_LnK`, `PS_LnMax`, `PS_LnW`; araç değişken silemiyor), nötr kalan `ClipSp` hesabı. Betikler `scripts/` altında.
