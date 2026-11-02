# SHME V2.48 — bakışa duyarlı dönüşlü kalkış sahipliği + klip-bağlı dönüş; temizlik (2026-11-02)

Taban: V2.47 (= V2.45 üretimi). Sayılar `TABLES_V248.md`, değişiklikler `CHANGES_V248.md`. Video: `vid/turnstart_D_realtime_part1.avi` (60 fps yakalama, gerçek hız; sol = üretim, sağ = V2.48). **Videoyu izleyemiyorum**; 0,13 s kare dizileri (`sheets/turnstart_final_*.png`) incelendi; oyun hissi NOT_TESTED.

## 1. Çözülen sorun: gerçek zamanda yanlış geriye kalkış
**Kök neden (telemetriyle):** sağ yanal koşudan sonra beden +90°'ye bakıyor; bakış yaw'ı gerçek zamanda 0–63° arasında kalıyor (kamera yeniden ortalaması zamana bağlı). SOL istek beden-göreli −120…−180° düşüyor. −115°'nin ötesinde LS yanal rotası (65–115°) devreye girmez; jog kalkış veritabanı (PSD_SHM237_JogStartS_L/R) içinde yörüngeye en ucuz klip **af_Loco_Jog_Bwd_Start** (geriye koşarak kalkış) ya da −170°'de V2.33 StandBack rotasıdır. V2.46'nın "bakış-göreli LS rotası" fikri yanlıştı: LS klipleri beden-göreli yan adımlardır. Doğru insan davranışı: basılı ayak üzerinde dönüp gitmek (TurnL/R 135/180). Bu klipler projede vardı (SHM_JogQ kopyaları) ama kalkış veritabanlarında yalnız 045'ler kayıtlıydı.

**Çözüm (yeni yöntem, maliyet yok):**
1. **Veritabanı sahipliği:** `PSD_SHM248_JogStartT2_L/R` = üretim kalkış DB'si − geriye kalkışlar + 6 dönüşlü kalkış (her iki yön; MM dönüş yönünü yörüngeden seçer).
2. **Karar (ABP `SHM_Snapshot`, oyun iş parçacığı):** pawn `GetControlRotation` → gerçek bakış yaw'ı (V2.46'nın `PreviousDesiredControllerYaw`'u değildi). `SHM248_TurnStart` = jog ∧ istek bedenin 115°'den fazla arkasında ∧ bakışın 135°'den fazla arkasında DEĞİL (S tuşu = gerçek geriye isteği StandBack'e kalır). Rota: jog kalkış aramasının yerine T2 DB; LS yanal rotası tutma sırasında kapalı.
3. **Klip-bağlı dönüş:** dönüş kliplerine kök hız eğrileri (`SHM226_V` ileri, **`SHM226_VL` yanal** – yeni, pawn `Velocity = Fwd·V + Right·VL`), işaretli dönüş ilerlemesi (`SHM238_Turn` sonda ±90, `Delta := |Delta|`) → V2.28/V2.38 sözleşmeleri kapsülü klibin kök yoluna bağlar; yön istenen başlığa tam oturur (−138 isteğe 135 klibi, −162'ye 180).
4. **İçerik:** 2,3 s'lik AAMS dönüş kalkışları dönüş bitimi + 0,25 s'de kırpıldı (0,93–1,0 s): MM dönüşten sonra kendi maliyetiyle faz-eşleşmeli koşu döngüsüne geçiyor.
5. **Lokomotif çerçeve:** dönüş bitince bileşen `LocoYaw/LocoState/LocoExplore` gövde yönüne alınıyor (aksi hâlde pawn gövdeyi bakışa geri çeviriyordu, çift dönüş).

**Sonuç (gerçek zaman, TABLES §6–7, duruştan itibaren ölçülen pivot sürüklenmesi):** −136/−137 isteklerde TurnL135: en kötü ayak 22,6–26,2 cm (4 koşu); V2.45 üretimi aynı isteklerde geriye koşarak kalkıyor ve 36,8 / 40,9 / 55,3 cm sürüklüyor. −119…−123 istekler eşik (130°) altında kalıp kanıtlı LS yanal kalkışını alıyor (5,2–12,0). 30 FPS taps/wstart/gait/w42/w43 üretimle birebir; jstart 30 FPS 57,4 → 33,9. **Açık:** pivot sürüklenmesi klipte yazılı 0,4 cm'e karşı 22–30 cm (kapsül pivot yolunu tam izlemiyor: sözleşme 0,12 s geç devreye giriyor, yön hızı Delta/klip ölçeklemesi); tam −180 istek (kamera hiç ortalanmamışken) 49 cm (üretim 55); jstart 60 FPS'te 90° segment devrinde pop 74 (önce 47); wstart gerçek-zaman varyansı 22–53. Görsel (çapraz kamera şeritleri): ağırlık aktarımı → pivot → itiş → kesintisiz koşu; üretimde geriye koşma + yan adım karışımı.

**Yol boyunca değişen kök nedenler (dürüst kayıt):** A) rota tek başına: klip yerinde dönerken kapsül CMC ile ilerledi (31–39 cm); C) sözleşme: ileri-only hız (yanal kök hareketi kayıp, 20–25 cm; klipte yazılı pivot 0,4 cm); H) 2,3 s klibin koşu adımları + devirde başka kalkış klibi (30–47); I) orta-klip sözleşme bırakma → ABP redirect episodu yaw'ı devraldı (60 cm, geri alındı); L) kırpma sonrası loco çerçevesi bakışa dönüş (30 cm) → M.

## 2. Idle–kalkış ve yürüyüş aileleri
Bu turda kapsam dışı bırakıldı (öncelik sırası: önce 1. madde uçtan uca). Yürüyüş: V2.47 ölçümü geçerli — Ranger/LB döngü farkı oyunda görünmüyor; vakit harcanmadı.

## 3. Gerçekçilik
Entegre edilen yeni davranış: istek bedenin arkasındayken basılı ayak üzerinde ağırlık aktarımlı 135/180° dönüş ve itişle kalkış (AAMS yakalama klipleri, kapsül klibe bağlı). Rastgele sallanma/efekt yok.

## 4. Temizlik
18 GB → 93 GB boş (CHANGES §Temizlik; `cleanup/summary.md`, `delete_plan.tsv`, `delete_log.txt`). Proje açılıp PIE koşuyor (tüm A/B zincirleri temizlik sonrası koştu).

## 5. Üretim kararı
**ALINDI** (`promote248.py`: `SHM248_On` := 1.0; `set248_backcos.py`: `SHM248_BackCos` := −0,64; manifestler v248_prom / v248_backcos; `verify241 ALL_OK`; temiz oturum 30 / gerçek zaman / 60 FPS üretim koşuları TABLES §5–7). Gerekçe: istenen davranış (bedenin arkasına istekte dönerek kalkış) artık oyunda; aynı isteklerde ayak sürüklenmesi üretimin geriye kalkışından 10–30 cm daha az; eşik altı istekler ve diğer senaryolar (taps, wstart, gait, w42, w43, j42) değişmedi. Teknik PASS; görsel inceleme kare dizileriyle (şeritler); video izlenmedi → oyun hissi NOT_TESTED. Geri alma: `promote248.py` `V248_PROMOTE_ROLLBACK` (knob 0 → V2.45 davranışı; eklenen DB/klip/değişkenler inert kalır).
**Sonraki tur için gerçek açık nokta:** pivot fazında kapsülün klip kök yolunu tam izlemesi (sözleşmenin ilk karede devreye girmesi, Delta yerine klip dönüş hızı) ve tam-arkaya istek; ardından idle–kalkış.
