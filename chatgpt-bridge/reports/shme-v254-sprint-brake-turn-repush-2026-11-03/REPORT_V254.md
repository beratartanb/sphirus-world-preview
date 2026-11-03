# SHME V2.54 — Hareket kimliği, fiziksel sınırlar, kamera–kontrol (2026-11-03)

## Ana kabul sorusu

> "Karakter artık yüksek hızda zor bir yön değişimi istediğimde, bunun fiziksel gereğini bedeniyle yerine getiriyor mu; yoksa hâlâ yön vektörü değişmiş bir animasyon gibi mi hareket ediyor?"

**Cevap: Kısmen.**

- **Sprintte 180° ve 135°: evet, ölçüldüğü kadarıyla.** Gövde frenliyor, bir ayağı yükleyip pivot yapıyor, aktarım adımıyla dönüyor ve yeni yöne itiyor:
  - geri geri gidiş 1,02 s → 0 s;
  - beden ~1,5 s'de yeni yöne bakıyor;
  - kapsül anında tersine dönmüyor; hız fiziksel bir frenle 0'a iniyor (0,7 g);
  - omurga birden dikleşmiyor (eğilme 28° → 22–24°; eskiden 28°'den geri geri koşu pozuna).
- **Sprintte 90°: evet.** Artık frenliyor: en düşük hız 288 → 142–173 cm/s, ivme tepesi 1,30 → 0,76–1,09 g. Atletik öne-yana atılma pozu yok.
- **Jog ve yürüyüşte ters dönüş: hayır.** Hâlâ geri geri gidiyor (1,4–1,7 s). Bu turda yalnızca sprint ailesi yazıldı.
- **180°'den sonra omuzlar kameraya doğru bükülüyor.** Kamera eski yöne bakarken vendor nişan katmanı üst gövdeyi 17–33° kameraya çeviriyor. Durum, kamera arkaya dönene kadar sürüyor.
- **Görsel kabul NOT_TESTED.** Videoları izleyemiyorum; yalnızca tek tek karelere ve ölçümlere baktım.

## Ne yapıldı

### 1. Sorunlu hareketin sahibi (ölçüldü)

**Sprintte S:**
- Oyun LookDrivenLocomotion profiliyle çalışıyor. `GR_Impl_CR_UpdateBackwardIntent` hızdayken S'yi "geri geri git" (`CR_Backpedal`) olarak yorumluyor.
- V2.34 gövde çerçevesi 120°'den büyük farkları keşfetmiyor, bu yüzden gövde hiç dönmüyor.
- Zincir şuydu: vendor `A_LR_Run_Pivot_F_B` → `A_LB_Walk_Bwd` → back-run.
- İlk fiziksel kırılma, talepten sonraki ilk fren adımında: gövde yönü değişmiyor, kapsül tersine akıyor.

**Sprintte 90°:** `SHM216_Cut_*_090` hiç frenlemeden 1,3 g'lik yana atılma oynatıyordu.

### 2. Kendi fren → yükle → dön → yeniden it zincirimiz

`gen254_rev.py` yeni klipleri ürettiyor; vendor klibi yavaşlatılmış değil, yeni içerik. Her adımın rolü, değdiği andaki hız ve yöne göre seçiliyor:
1. **Fren:** ayak yön çizgisinde önde, gövde geri yaslanıyor.
2. **Pivot:** dış ayağın topu üzerinde dönüş.
3. **Aktarım.**
4. **İtiş:** sprint döngüsüne kesintisiz bağlanıyor.

İçerik:
- **180° ters dönüş:** sağ ve sol destek, döngü evresine göre 4 klip; `PSD_SHM254_SprintRev`.
- **90° kesiş:** sağ ve sol, 2 klip; `PSD_SHM254_SprintCut`.
- Baş, göğüs ve pelvis kademeli dönüyor, yapay bekleme yok.
- Gövde eğilmesi, frenin ivmesinden alçak geçirgen filtreyle türetiliyor.

**Çalışma anı kuralları (ABP, SHM254_Turn anahtarı):**

| Yama | Ne yapıyor |
|---|---|
| install254_turn | Dönüş yönü işareti (±180° belirsizliği) ve dönüş bitince gövde çerçevesini yeni yöne devretme. Bu olmadan gövde geri dönüp yine geri geri koşuyordu. |
| install254_hold | Plan sürerken rota klibi tutuyor. Eskiden jog-ters ve yürüyüş-itiş veritabanları planı ortadan kesiyordu. |
| install254_v2 | Devir anında yön dönüş hızı 0'dan 0,2 s'de açılıyor. Eskiden tek karede 7,5° kayma, ±4° eğilme salınımı ve başta 15 cm yana savrulma oluyordu. Ayrıca iptal: girdi plan hedefinden 75°'den fazla saparsa ya da bırakılırsa plan bırakılıyor. |
| install254_v3 | İptal, klip hız sözleşmesini de bırakıyor. |
| install254_v4 | İptal anında girdi varsa ve hız 250 cm/s'nin üstündeyse MM, sprint döngüsüne geçmek zorunda. |
| install254_v5 | Plan sürerken bakış noktası = gövdenin kendi yönü. |
| add254_block / gen | Kliplere ortadan giriş engeli (0,12 s sonrası). |

**Klip sahipliği:**
- Klip, rotayı kendi sonuna kadar (−0,05 s) tutuyor; çıkış hız 400 cm/s'nin üstündeyken oluyor.
- Daha önce yürüyüş-itiş bağlantısına (`SHM218_W2S`) ortadan atlıyor ve başta 70 m/s²'lik bir sıçrama üretiyordu.

### 3. Hareket kuralları

- **Kapsül anında dönmüyor.** Hızı ve yönü klibin fiziksel planı belirliyor (V2.28 + V2.38 sözleşmeleri).
- **Hız arttıkça maliyet artıyor.** Sprint 180° tam frenle 0'dan geçiyor. Sprint 90° 460 → 142–173 cm/s'ye düşüyor; jog 90° (V2.38) 276 → 177. Sprint, yavaş hız gibi davranmıyor.
- **Sabit "bekle sonra dön" yok.** Fren ilk karede başlıyor.
- **Kısa ters dokunuş:**
  - Eskiden: aday tam 180° yapıyordu.
  - Şimdi: plan 0,27 s'de iptal oluyor ve hız 419 cm/s'de kalıyor (üretimde de 0,27 s).
- **Spam:** sağ-sol spamında klibe ortadan giriş engellendi. En kötü sıçrama 57, üretimle aynı.
- **Geri geri gitme ile dönüp koşma ayrımı:**
  - Sprintte ters yön artık dönüp koşma.
  - Jog ve yürüyüşte hâlâ geri geri gitme; ayrımın kuralı yeniden yazılmadı (açık).

### 4. Kamera (ölçüldü, üretime alınmadı)

**Sahipler:**
- GR kamera düzeneği: kol 155 / koşu 172 / sprint 184, pivot 61 cm, FOV 62/64.
- SHME kamera katmanı: CamClose, CamOrbit, CamRec, CamSwapV21.
- İkinci bir takip sistemi yok.

**Aday:** otomatik omuz değişimi kapalı; Close Stand/Walk 0,86, Jog 1,0, Sprint 1,06; Tau 1,0.
- Mesafe: jog 221 → 233 cm, sprint 223 → 237 cm.
- Ekran boyu: 0,86 → 0,82.
- Girdi yönüne etkisi yok (yol farkı 0,00 cm, kontrol yönü farkı 0,00°).
- Dokunuşlarda zoom pompası değişmedi (p95 0,34 → 0,36 /s).

**Bulgu (asıl sorun):** ayaklar her hızda ekranın çok altında (ekran y −1,5…−1,8; −1 alt kenar). Kamera pivotun 53–58 cm üstünde ve düz bakıyor; koşuda bacaklar kadrajda okunmuyor. Boom'u yüzde birkaç uzatmak bunu çözmüyor. Koşuda hedef noktasının alçalması veya hafif aşağı eğim gerekiyor. Bu GR düzeneğinde ayrı bir tasarım işi ve yapılmadı.

**180°'den sonra:**
- Kamera eski yöne bakmaya devam ediyor; karakter kameraya doğru koşuyor.
- Otomatik toplama +2 s'de, ~75°/s ile başlıyor; CamRec 110°'den büyük hatada toplamıyor.
- Dramatik bir yörünge dönüşü eklemedim. Bu bir tasarım kararı; senin onayın gerekiyor.

**Omuz bükülmesi:** vendor nişan katmanından geliyor (`Get_AOValue` = kontrol − gövde).
- V2.40 `SHM240_HeadOn` bunu dönüş sonrası −20/−33°'den −4/−6°'ye indiriyor ve regresyon seti 60 FPS'te temiz.
- Ama 120 FPS'te talep anında başta 155 m/s² sıçrama var (V2.40'tan bilinen sorun). Bu yüzden üretime alınmadı.

## Üretime alınan (promote254.py, geri alma hazır)

| Ayar | Değer |
|---|---|
| `SHM254_Turn` | 1 |
| `SHM_RedirectDB_SR`/`_SRL`/`_SRR`, `SHM212_RouteSRL`/`_SRR` | `PSD_SHM254_SprintRev` |
| `SHM_RedirectDB_SL` | `PSD_SHM254_SprintCut` |
| Kamera | Değişmedi |

**Doğrulama:** p60 ve gerçek zamanda üretim, adayla birebir aynı.

**Geri alma:** `Saved/Codex/SHME_V254_20261104/req/rollback_req.py`. `promote254_before.json` içindeki değerleri geri yüklüyor. Manifest yedeği: `v254_promote`.

## Testler (sayılar TABLES_V254.md'de)

| Test | Sonuç |
|---|---|
| Sprint 180 R/L, 90 R/L, 135, kısa ters dokunuş, dönüş ortasında yeni komut, sağ-sol spamı (60 FPS) | PASS (teknik) |
| 20 / 30 / 120 FPS ve gerçek zaman | PASS: davranış tutarlı (yüz yeni yöne 1,48–1,52 s, geri gidiş 0). PARTIAL: 120 FPS'te 90° kesişte ivme tepesi 1,66 g, en kötü sıçrama 114 (üretim 101). |
| Regresyon (wstart, w42_id, taps, jstart, j36_stop, j45_sl2, gait, w43_idle, j40_rlw) | PASS (üretimle aynı; j45_sl2 16/52 ve 18/51) |
| Sıçrama: sprint 180 | Sağ 53, sol 48 (üretim 48; eski aday 88/72) |
| Ayak kayması: sprint 180 | 33,6 → 17,2 cm |
| Jog ve yürüyüş 180/135 | FAIL: değişmedi, geri geri gidiş |
| Duvar yanında dönüş | Yalnızca kamera adayıyla, yürüyüş ölçeğinde: hareket ve kamera üretimle aynı. Sprintte duvar yanında dönüş NOT_TESTED. |
| Kamera kabulü | FAIL: bacaklar kadrajda okunmuyor |
| Görsel ve oyun hissi kabulü | NOT_TESTED, karar senin |

## Videolar (`vid/`, 30 fps gerçek hız)

| Dosya | İçerik |
|---|---|
| `a_sprint180_yan` | Eski ve yeni hareket, aynı sabit yan kamera |
| `b_sprint180_oyunkamerasi` | Eski hareket + oyun kamerası, yeni hareket + yeni kamera |
| `c_sprint90_yan`, `d_sprint90_oyunkamerasi` | Sprint 90° için aynı iki karşılaştırma |
| `e_kisa_ters_dokunus_yan` | Kısa ters dokunuş |

## Açık işler (öncelik sırasıyla)

1. **Jog ve yürüyüş 180/135:** aynı üreteçle jog/yürüyüş döngüsüne bağlanacak (`LOOP=A_CT_Jog_Fwd`, rota `SHM224_DB_JR*`). Geri geri gitme ile dönüp koşma ayrımının kuralı (`CR_Backpedal`, LookDriven) da yeniden yazılacak.
2. **180° sonrası omuz bükülmesi:** nişan katmanının talep anındaki 120 FPS sıçraması giderilip `HeadOn` alınabilir, ya da klip boyunca `Disable_AO` eğrisi kullanılabilir.
3. **Kamera:** koşuda hedef noktası ve eğim (bacaklar okunsun), otomatik omuz değişimini kapatma, 180° sonrası toplama politikası.
4. **120 FPS sprint 90°:** ivme tepesi ve sıçrama 114.
5. **Diğer açık işler:** ağırlıklı idle (V2.53'ten beri kapalı), sprint 180 ayak kayması (17 cm, aktarım adımında).
