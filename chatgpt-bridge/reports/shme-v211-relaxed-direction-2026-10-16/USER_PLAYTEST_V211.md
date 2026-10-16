# SHME V2.11 — Oyun testi rehberi

Teknik ölçümler QA zemininde, gerçek IA_Move / IA_Look yoluyla enjekte girişle yapıldı. His, görünüm ve kontrol kabulü senin oyun testine bağlı; ben kabul vermedim.
- V2.11 kayıtlı varsayılan:
  - kol bake'i (başlangıçlar, yürüyüş döngüsü, yerinde dönüşler);
  - idle kamera tutması kapalı (`CameraIdleOrbitMaxYaw` 180);
  - depara itiş rotası açık (`SHM211_PushMode` 1).
- V2.10'un diz ve kesiş onarımları yerinde.
- Her madde için "doğal / hâlâ X / fazla Y" notu yeterli.

## 1. Yürüme başlangıcında kollar (ilk kabul koşulu)
- **Nasıl:** dört başlangıcı önden-çaprazdan ve yandan izle:
  - uzun idle (5+ sn) → W;
  - yürü → dur → hemen W;
  - W'ye kısa bas → bırak → tekrar bas;
  - fareyle yerinde 90° dön → W.
- **Beklenen:**
  - Kollar ilk adımda kalçaya yapışmıyor, içe kapanıp "orada kalmıyor".
  - Kol idle'daki gibi yanda asılı başlıyor ve salınıma yumuşakça geçiyor.
  - Kol geriye doğru tutulmuyor.
- **Bilinen kalıntı:** "dur → W" ve "dönüş → W"de başlangıçtan ~0.5 sn sonra sağ kol kısa süre (~0.3 sn) gövdeye yaklaşabilir. Bu yürüyüş döngüsünün bir turundan geliyor (rapor §2.4).
  - Görürsen "evet, hâlâ fark ediliyor" ya da "fark etmiyorum" yaz.

## 2. Yerinde dönüşte kollar
- **Nasıl:** dur, fareyle yavaş ve hızlı sola/sağa 45–180° dön. Önden ve yandan bak.
- **Beklenen:**
  - Dönüşte kollar yana savrulmuyor ("aksiyon pozu" yok).
  - Küçük doğal kol hareketi var, donuk değil. Adımlar ve dönüş hızı öncekiyle aynı.

## 3. Kamera dönerken W/A/S/D
- **Nasıl:**
  - Dururken fareyle hızlıca 90° / 180° bak ve hemen W'ye bas.
  - Yürürken, tempoluda, deparda fareyle dönerken W'yi bırakma.
  - S, A, D ile de dene.
- **Beklenen:**
  - W her zaman ekranın baktığı yöne gidiyor.
  - Önceden dururken hızlı dönüşte kamera gövdeden 55°'den fazla açılmıyordu, W ise farenin yönüne gidiyordu (ekranla 125°'ye kadar fark).
- **Yeni yan etki:** dururken kamera artık karakterin etrafında serbest dönüyor. Yerinde 180 dönüşte karakterin önünü kısa süre görebilirsin.
  - "Eski tutma hissi daha iyiydi" dersen geri alınabilir (`CameraIdleOrbitMaxYaw` 55). O zaman ekran–W farkı geri gelir.

## 4. Yürüyüş → Shift (depara itiş)
- **Nasıl:** W ile yürürken Shift'e bas ve tut. Yandan ve oyun kamerasından bak. Ayrıca dururken Shift+W.
- **Beklenen:**
  - Dik tempolu koşuyla 0.5 sn beklemek yerine öne eğilen, sürücü adımlı bir hızlanma; sonra depar.
  - Dururken Shift+W zaten koşu başlangıcıyla başlıyordu.
- **Not et:**
  - "İtiş fazla derin / az."
  - "Yürüyüşten itişe geçişte kısa hızlı yürüyüş adımı" (bilinen, ~0.2 sn).
  - Tempoludan Shift'e geçişte itiş yok (bilinçli).

## 5. Shift+W → W bırak → Shift+S
- **Nasıl:** deparda W'yi bırak, Shift'i tutarken S'ye bas. S+A ve S+D ile de dene.
- **Beklenen:**
  - Önce fren pivotu, sonra gövde ileri bakarken geri koşu, en fazla tempolu hızında.
  - Geri depar yok; hız birden kesilmiyor (~0.6 sn fren).

## 6. Shift+W + kamerayı 180° çevir
- **Beklenen:** fren → dönüş → yeni yöne itiş (artık koşu başlangıcı itişiyle) → depar.
- **Bilinen:** tam 180 fare dönüşünde dönüş içinde üst gövdede kısa sarsıntı olabilir (rapor §7 PARTIAL).

## 7. Ardışık sert dönüşler ve ikinci ters dönüş
- **Nasıl:**
  - Deparda D-A-D hızlıca.
  - Deparda S'ye bas, itiş bitmeden tekrar W.
  - Fareyle 180 ve hemen geri.
- **Beklenen:** her ters dönüşte fren ve destek; yeniden hızlanmada itiş. Küçük yön değişikliklerinde ve W+A ↔ W+D'de itiş tekrar tetiklenmiyor.

## 8. Eğim / tek ayak yükseltide dur → dön → başla; normal viraj
- **Beklenen:**
  - Ayaklar yüzeyde, V2.10 ile aynı.
  - Normal depar virajında sendeleme yok.
  - Sert dönüşte gerçek bir yakalama adımı yok. İçerik eksiği; rapor §8 brifi.
