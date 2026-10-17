# SHME V2.12 — Oyun testi rehberi

Teknik ölçümleri QA zemininde, harness üzerinden gerçek tuş girdisiyle yaptım: `Input.+key` / `Input.-key`, IA_Move / IA_Look yolu. His, görünüm ve kontrol kabulü sende; ben kabul vermedim.

**V2.12 kayıtlı varsayılan:**
- yürüyüş döngüsü kol bake'i ve veritabanı temizliği;
- yürüyüşten depara itiş: yeni içerik (satıcı yürüme→depar geçişi, duruşu yumuşatılmış), niyet şartı, tek itiş, 490'a kadar.

**Kapalı (uyuyor):** toparlanma adayı.

**Korunanlar:**
- V2.11 dönüş kolları, ekran = W eşleşmesi, idle kamera serbestliği;
- V2.10 diz ve kesiş onarımları.

Her madde için "doğal / hâlâ X / fazla Y" notu yeterli.

## 1. Yürüme başlangıcında kollar (ilk kabul koşulu)
**Nasıl:** önden-çaprazdan ve yandan bak. Dört başlangıcı her iki ayakla da birkaç kez dene:
- uzun idle (5+ sn) → W;
- yürü → dur → hemen W, sonra 1–2 sn bekleyip W;
- W'ye kısa bas → bırak → tekrar bas;
- fareyle yerinde sola ve sağa 90° dön → W.
- Ayrıca 10+ sn düz yürü (döngünün bütün turları).

**Beklenen:**
- Kol ilk adımda gövdeye yaklaşmıyor, orada kalmıyor, sonra yeniden açılmıyor.
- Sağ kol yürüyüşte ~1 sn içinde idle'dan biraz daha kapalı bir salınıma kademeli geçiyor (~3°).
- Her adımda kol kalçanın yanından geçerken en yakın noktasında; bu doğal salınım.

**Bilinen:** kısa basışın durma anında sağ kol bir an daha açık (durma klibi).

## 2. Yerinde dönüş
**Nasıl:** dur, fareyle yavaş ve hızlı sola/sağa 45–180° dön. Ayrıca:
- dönüş bitmeden W'ye bas;
- dönüş sırasında fareyi geri çevir.

**Beklenen:** kollar V2.11'deki gibi sakin; dönüş bitmeden W'de başlangıç bozulmuyor.

**Bilinen kalıntılar:**
- Ters dönüş isteği ilk dönüşün bitmesini bekliyor (~1.8 s). Fark edersen yaz.
- Gövdenin dönüşe yana yatması (4–10°) AAMS içeriğinden. "Aksiyon pozu" bu mu, söyle.

## 3. Geri (S)
**Nasıl:**
- Deparda W'yi bırak → S.
- Deparda W'yi bırakmadan S'ye bas, sonra W'yi bırak.
- S+A, S+D.
- Shift'i bırakıp S, sonra Shift'i tekrar bas.
- S basılıyken fareyi çevir.
- S'den hemen sonra yeniden W.
- Deparda D'ye kesip hemen S.

**Beklenen:**
- Fren pivotu, sonra yüz ileri bakarken geri koşu (en çok tempolu hızında).
- Geri depar yok; ileri depar klibi geriye taşınmıyor.
- **Önemli eşleme bilgisi:** W ve S birlikte basılıysa oyun S kabul ediyor (girdi sıfır değil).

**Bilinen kusurlar:**
- Deparda S'ye basılan ilk karede küçük bir hız kesiği var; sahibi bulunamadı.
- **Depar kesişi sırasında S:** kesiş ~0.4 sn daha sürüyor ve pelviste bir sarsıntı oluyor. Değiştirilmedi.

Fark ettiğin başka bir dizi varsa tuş sırasını yaz.

## 4. Yürüyüş → Shift (depara itiş)
**Nasıl:**
- W ile yürürken Shift'e bas ve tut. Yandan ve oyun kamerasından bak.
- Ayrıca:
  - dururken Shift+W;
  - deparda S → W;
  - deparda Shift'i kısa bırak-bas;
  - W+A ↔ W+D;
  - tempoluyken (Shift dokunuşu) Shift'i tut.

**Beklenen:**
- Yürüyüşten itişe hızlanmış yürüme adımı olmadan geçiş.
- Son yürüme adımından öne eğilen itiş, sonra depar.
- Dururken Shift+W eskisi gibi koşu başlangıcıyla başlıyor.
- Kısa bırak-bas ve W+A↔W+D itişi tekrar tetiklemiyor; ters dönüşten sonra tek itiş var.

**Not et:**
- **"İtiş duruşu fazla / az / iyi":** tepe öne eğilme ~36°, pelvis ~12 cm iniyor. V2.11 yürüyüş itişi ~35° / ~10 cm, dururken başlangıç ~37° / ~17 cm. Ham satıcı klibi 50° / 22 cm ile koşucu blok çıkışı gibiydi; o hali üretimde değil.
  - Beğenmezsen tek ayar grubuyla eski itişe dönülür.
- **Tempolu → Shift:** hâlâ itişsiz (bilinen kalıntı).
- **Ters dönüş sonrası itiş:** artık tek itiş var, ama koşu başlangıcının ortasından giriyor ve kısa. Hâlâ "ikinci başlangıç" gibi görünüyorsa yaz.

## 5. Sert ters dönüş (toparlanma)
**Nasıl:** deparda D'ye sert kes, kesişin hemen ardından A'ya bas. Sol aynasıyla da dene.

**Beklenen (bu sürümde):** üretim davranışı V2.11 ile aynı. Toparlanma adayı denendi ama ayaklar kaydığı için kapalı.

Görünen kusuru (ayak kayması / sarsıntı / ikinci başlangıç) not et; yeni içerik isteği için girdi olur.

## 6. Kamera dönerken W/A/S/D
**Beklenen:** W her zaman ekranın baktığı yöne (V2.11 ile aynı). Dururken kamera karakterin etrafında serbest dönüyor.

## 7. Eğim / tek ayak yükselti
**Beklenen:** dur → dön → başla sırasında ayaklar yüzeyde (V2.10 ile aynı).
