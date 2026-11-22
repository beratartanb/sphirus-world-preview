# mk_readme.py: assemble the final round-6 README from the interim one (sections 1, 3, 6 kept with small updates) + final data
import io
R = 'chatgpt-bridge/reports/sphirus-ue59-hareket-carpisma-2026-11-23/README.md'
s = io.open(R, encoding='utf8').read()
def cut(a, b):
    i = s.index(a); j = s.index(b, i) if b else len(s); return s[i:j]
sec1 = cut('## 1. Şikâyet', '## 2. Önce'); sec3 = cut('## 3. Değişen varlıklar', '## 4. Videolar'); sec6 = cut('## 6. Yeniden üretim', None)
tab = io.open('Saved/UE59Work/r6/slide_table_final.md', encoding='utf8').read().strip()

a = "→ `m_gov6c_mcp.py`, `m_gov6d_mcp.py` (`BP_Sph_GASPCharacter.CalculateGroundFriction`, o karenin bekleyen girdisini kullanır; ters dönüş etkinken 500 cm/s² taban fren uygulanmaz)."
assert a in sec1
sec1 = sec1.replace(a, "→ `m_gov6c_mcp.py`, `m_gov6d_mcp.py`, `m_gov6e_mcp.py` (`BP_Sph_GASPCharacter.CalculateGroundFriction`, o karenin bekleyen girdisini kullanır; ters dönüş etkinken 500 cm/s² taban fren uygulanmaz). Bu sürtünme hafifletmesi yalnız 480 cm/s üstünde (sprint) geçerlidir: koşu hızında da devreye girdiğinde planC1'deki bir A↔D dönüşü 28–66 cm kaydı (son zincirde yakalandı, düzeltildi).")
a = "sonra istenen hız yürüyüş→koşu geçiş klipleriyle devralınır; sprint 250 cm/s'den sonra devreye girer."
assert a in sec1
sec1 = sec1.replace(a, a + " Yalnız **düz kalkışta** uygulanır: kalkış anında gövde zaten gidiş yönüne bakmıyorsa (90° / 180° dönerek kalkış) eski davranış kalır, çünkü geçiş klibi o durumda kapsülle uyuşmuyordu (30 Hz'de 39–43 cm; son zincirde yakalandı, `m_softstart6c_mcp.py`).")
a = "- **Sıyırma.** Duvar tarafındaki kol gövdeye çekilir."
assert a in sec1
sec1 = sec1.replace(a, a + "\n- **Merdiven temposu** da bu olayda hesaplanır (aşağıda).")

sec3 = sec3.replace("Kaydetme ve yeniden açma: değerler yeniden açılan editörde diskten okundu (`data/saved6.txt`).",
                    "Kaydetme ve yeniden açma: editör bu turda dört kez kapatılıp açıldı; değerler diskten okundu (`data/saved6.txt`) ve aşağıdaki son sayılar son açılıştan sonra ölçüldü.")

head = u'''# SPHIRUS UE 5.9 — Tur 6: ayak kayması kök nedeni, çarpışma v2, düşme/kalkma, yumuşak başlangıç (2026-11-23)

**Durum: son rapor.** Bütün değişiklikler Unreal projesine kaydedildi; aşağıdaki sayılar **kaydedilmiş ve yeniden açılmış** durumda ölçüldü. Önceki commit'teki ara rapor (`8540e45`) bu sürümle değiştirildi.

Ölçümlerin hangi çalıştırmadan geldiği:

| Etiket | Çalıştırma | Kapsam |
|---|---|---|
| **f8** | son kayıt + yeniden açılış (`scripts/final8.sh`) | tam kayma regresyonu (29 kayıt: 60 / 30 / değişken Hz), 5 temas senaryosu, duruş / başlangıç, başlangıç videosu |
| **f7** | bir önceki kayıt + yeniden açılış (`scripts/final7.sh`) | temas alt kümesi (17 senaryo + 30 Hz), duruş, yorgunluk, bekleme, arazi, 21 video, ev akışları. f7'den sonra yalnız iki şey değişti: yumuşak başlangıcın düz kalkışa sınırlanması ve sprint sürtünme hafifletmesinin 480 cm/s üstüne alınması |
| **c6** | kaydetmeden önce, tam 25 senaryoluk temas matrisi | `data/ct_c6.txt` |

Görsel / oynanış kabulü kullanıcıya aittir; bu raporda **USER_ACCEPTED yoktur**. Başlangıç: commit `9765db9` (tur 5). Proje: `C:\\Users\\berat\\Documents\\Unreal Projects\\sphirus_UE59`, oyuncu `BP_HybridA_Player`, test haritası `L_Sph_MoveTest`, ev haritası `L_GR_SphirusHouse`.

Test ortamı (bu oturumda okundu): Intel i7-13650HX, 32 GB RAM, NVIDIA RTX 4060 Laptop 8 GB (sürücü 616.56), 1920×1200. Hareket testleri editör içi PIE'dir; girdi simüle klavye planlarıdır. Gerçek gamepad (DualSense bağlı) **test edilmedi** — fiziksel çubuk girdisi bir insan gerektirir.

---

'''

sec2 = u'''## 2. Önce → sonra

### 2.1 Ayak kayması — f8 (son durum), aynı planlar, aynı ölçüm (`an_slide3.py`, değiştirilmedi)

Sütunlar: ortalama / p90 / en kötü (≥10 cm sayısı, ≥20 cm sayısı), cm. "Zeminde en kötü" = ayak gerçekten yerdeyken ölçülen kayma. Tur 5 değerleri tur 5'in `final5_slide.txt` dosyasından; tur 6 değerleri `data/final8_slide.txt`.

''' + tab + u'''

- 29 kaydın hepsinde **zeminde en kötü kayma ≤ 7,7 cm**, ≥ 20 cm temas **yok**.
- "Eğri" sütununda 10 cm'yi aşan 4 temasın 3'ü `M_Relaxed_Run_Stop_B_Rfoot` klibindedir: klibin temas bayrağı ayak 11,5 cm havadayken açılıyor (zemin okuması 0,0 cm); biri yürüyüş→koşu geçiş klibinde aynı türden (zemin 0,7 cm). Bunlar klip verisi kusurudur, filtrelenmedi, ayrı işaretlendi.
- Tur 5 raporunda açık kalan değerlerin karşılığı: planU_B 30 Hz 44,9 → **2,1**; 60 Hz 29,8 → **2,0**; değişken Hz koşu sağ↔sol 32,6 → **4,5** (planC1); sprintten geriye 24,2 → **7,8** eğri / 1,7 zemin (planK1 60 Hz); 30 Hz koşudan duruş 21,3 → **2,1** (planU_A); kısa geri → ileri (tur 5'te değişken Hz 20,6; o kaydın planı yeniden çalıştırılan sette ayrı durmuyor, en yakın karşılık planK1 değişken Hz) → **3,6**; çömelerek duruş 22,3 → **2,4**.
- Gerileme denetimi: tur 5'te iyi olan satırlar (planSp, planQt, planK1 30 Hz) iyi kaldı. Ara rapordaki planK1 30 Hz 27,1 cm'lik temas son durumda yok (zeminde en kötü 2,7).
- Yan etki denetimi: yerdeki ayağın kilit bırakılırken çekilmesi (`an_snap6.py`) bütün kayıtlarda 0; bacak uzaması ve kalça yüksekliği değişmedi.
- Dönüş ağırlığı (`an_turn5.py`, f8): tur 5 ile aynı aralıkta (koşuda 45° → hızın ~%90'ı, 90° → ~%70, 135° → ~%30); ayrıntı `data/final8_slide.txt` sonunda.

Bu turun kendi içinde yakalanıp düzeltilen gerilemeler (kanıt dosyaları `data/` altında):

| Bulgu | Nerede görüldü | Neden | Düzeltme sonrası |
|---|---|---|---|
| 30 Hz koşu 90° dönüş 38,7 cm | ilk regresyon | kilit eşiği 40 ayağı karışımda erken kilitledi | eşik 25 → 2,1 cm |
| sprint 180°: 30 Hz 28 cm, değişken Hz 58–76 cm | f6 | ilk karede tam sürtünme | 2,1 / 2,7 cm |
| dönerek kalkış 30 Hz: 43 ve 39 cm | f7 | yumuşak başlangıç + dönerek kalkış | 4,0 / 2,4 cm |
| koşu A↔D 61–66 cm (planC1 60 Hz) | f7 | sürtünme hafifletmesi koşu hızında da açıktı | 4,7 cm |

### 2.2 Çarpışma — f7 / f8 (60 Hz; `data/final7_contact.txt`, `data/final8_contact.txt`)

Gövde–engel çakışması yeni bir ölçümdür (`an_ct6.py`): görünür bedenin diz, baldır (3 nokta), uyluk, ayak, ayak ucu, kalça, el, dirsek ve baş noktaları, uzuv yarıçapı düşülerek engel kutusuna karşı sınanır. Tur 5 kayıtlarında bu ölçüm yoktu; tur 5 için tek kanıt videodur (09b, 4–5. saniye).

| Senaryo | Sonuç | Çakışma |
|---|---|---|
| Diz engeli, koşu 415 (zorunlu kabul testi) | denge kaybı → 44 cm geri adım → diz çökme → kalkma | yalnız çarpma anında ayak ucu 8,9 cm; geri adım, çökme, bekleme ve kalkma boyunca **yok** (30 Hz: aynı) |
| Diz engeli, tempo 278 | sendeleme | ayak ucu 10,7 cm (sendeleme adımında) |
| Diz engeli, yürüyüş 180 | engelin önünde durur (60 ve 30 Hz) | yok |
| Diz engeli, yorgun (0,9) | 162 cm/s'de sendeleme (dinç yürüyüşte tepki yok) | yok |
| Diz engeli, taşırken (gerçek taşıma bayrağı, hız 187) | c6: sendeleme, el desteği yok; f7: engelin önünde durdu | yok |
| Duvar: yürüyüş / koşu / sprint | 20 cm önce durur, el yüzeyde | yok |
| Kütük (25 cm), sprint 585 | takılma → öne düşme → yatma → kalkma (30 Hz: aynı) | düşerken arkadaki ayak ucu 8,9 cm |
| Kütük, dinç koşu 415 | takılma → sendeleme | ayak ucu 9,1 cm |
| Basamak (30 cm × 60 cm), sprint | sendeleme (ilerisi düz değil → düşme yok) | ayak ucu 5,5 cm |
| Dar alan (arkada 40 cm, zorlanmış eşikler) | c6: geri adım kısalır → diz çökmez, ayakta destek; f7: yürüme hızında engelin önünde durdu, çarpma oluşmadı | yok |
| Merdiven sprint, merdiven koşu, rampa koşu | tepki yok (yanlış takılma yok) | — |
| Yan duvar sıyırma | hız düşer, kol çekilir | dirsek 5,2 cm, el 7,0 cm (tur 6 başı: 11,3 / 13,5) |
| Alçak kiriş (alt yüz 150 cm), yürüyüş ve koşu | çömelip geçer, sonra doğrulur | yok (baş en fazla 113 cm) |
| Temas sistemi kapalı, diz engeli koşu (karşılaştırma) | tepki yok, yerinde koşar | ayak ucu 9,4 cm |

Avuç hizalama (`an_palm6.py`, f7): destek elinin avuç yönü ile yüzeye dik yön arasındaki açı yürüyüş / koşu / sprintte ortalama **3–4°** (hizalama yokken 83–86°), parmak yükselişi 84–85°. Görüntü: `evidence/03_duvar_avuc.jpg`, video 10a.

Not: taşıma ve dar alan satırlarında f7 sonuçları c6'dan farklıdır, çünkü arada "yürüme hızında diz hizasındaki engel önceden görülür" kuralı eklendi; taşırken hız 187 cm/s ile sınırlı olduğundan engel artık çarpılmadan fark ediliyor. Dar alanda ayakta destek dalı bu yüzden yalnız c6'da (zorlanmış eşiklerle) gözlendi.

### 2.3 Başlangıç, merdiven, yorgunluk

| Ölçüm | Tur 6 başı | Son durum |
|---|---|---|
| Koşu başlangıcı (düz): baş alçalması / gövde eğimi en fazla | 32,3 cm / 26° | **12,7 cm / 14,8°** (f8) |
| Tempo başlangıcı: baş alçalması | 32,9 cm | 19,6 cm (f8) |
| Sprint başlangıcı: baş alçalması / gövde eğimi | 28,5 cm / 28° | 20,9 cm / 19,6° (f8) |
| Koşuda hızın %90'ına ulaşma | 0,67 s | 0,43 s (f8) |
| Merdiven yürüyüş: hız / diz açısı en düşük / %5 | 158 cm/s / 45° / 54° | 102 cm/s / **60° / 71°** (f7) |
| Merdiven yürüyüş: kalça, öndeki ayağın üstünde (ortalama) | 52 cm | 62 cm (f7) |
| Merdiven koşu: kalça, öndeki ayağın üstünde (ortalama) | 38 cm | 47 cm (f7) |
| Merdiven / rampa: en kötü kayma | 2,1–3,9 cm | 1,4–3,9 cm (f7) |

Yorgunluk (f7, `data/final7_posture.txt`): 14 s sprintte 0 → 0,64'e kademeli artış, duruşta 0,83 tepe, ~12 s'de sönüm; duruşta gövde eğimi dinç duruştan ≤ 1° farklı, omuz yüksekliği en fazla 2 cm düşüyor. Videolar 14a / 14b.

Geçiş anları artık ayrı raporlanıyor (`an_post6.py`: her bölümün ilk 1,2 s'si ve kararlı kısmı; tepe değerler ve 0,1 s içindeki en büyük değişim). Zıplamada havada kalma süresi gerçek yer boşluğundan ölçülüyor (`an_terr6.py`): koşarak 0,62 s / 284 cm, yürüyerek 0,60 s / 153 cm, yerinde 0,62 s.

### 2.4 Ev akışları — f7 (yeni sistem açık, `data/final7_house.txt`)

- Yatak (yatış → uyku → gün değişimi → uyanış): çalıştı, video 17.
- Maske (alma → inceleme → bırakma): çalıştı, video 18.
- Odun toplama → taşıma → yarma → parçaları alma → şömineye götürme → yakma: `CHECK wood picked True | split pieces 2/2 PASS | fire state 2 (lit) PASS`.
- Kullanıcı kaydı her kayıttan sonra `SLOT_OK 3d81ab9d…`.

Çay, gardırop, kapılar, görev sırası, kayıt/yükleme ve gün değişimi sonrası yeniden yükleme bu turda **çalıştırılmadı**.

### 2.5 Performans (`data/perf6.txt`)

| Ölçüm | Kare p50 / p95 / p99 / en fazla (ms) | Oyun iş parçacığı p50 / p95 (ms) | GPU p50 (ms) | Ort. fps |
|---|---|---|---|---|
| Ev haritası, eşleştirilmiş rota (bekleme → yürüyüş → sprint → duruş), editör PIE 1920×1200, tur 3 referansı | 28,5 / 30,6 / 31,2 / 63,3 | 13,0 / 15,2 | 27,0 | 35,2 |
| Aynı rota, tur 6 son durum, 1. koşu | 29,5 / 31,2 / 31,9 / 72,2 | 13,4 / 14,7 | 28,0 | 33,9 |
| Aynı rota, tur 6 son durum, 2. koşu | 29,9 / 31,6 / 32,2 / 35,1 | 13,4 / 15,0 | 28,3 | 33,5 |
| Aynı rota, temas sistemi kapalı (2 koşu) | 23,5–23,8 / 26,5–27,4 / … / 30,0 | 13,6–13,9 / 17,0–17,5 | 21,8–22,2 | 40,8–41,7 |
| Standalone (`-game`, 1280×720 pencere, ev haritası, girdi yok, 2.400 kare) | 20,6 / 21,3 / 21,6 / 63,6 | 6,3 / 9,7 | 19,5 | 48,6 |

- Oyun iş parçacığı maliyeti tur 3 referansına göre p50'de +0,4 ms; temas sistemi açık / kapalı arasında oyun iş parçacığında ölçülebilir fark yok (13,4 ve 13,6–13,9 ms). Sahne GPU'ya bağlı.
- Temas sistemi kapalıyken GPU süresinin 6 ms düşük çıkması sistemin maliyeti **değildir**: kapalıyken yokuş hız kuralı da kapanıyor, karakter rotada daha ileri gidiyor ve kamera başka bir görüntüye bakıyor. Bu karşılaştırma eşit görüntüde yapılmadı; GPU maliyeti için sonuç çıkarılamaz.
- Tek kare sıçraması: 1. koşuda bir kez 72 ms (oyun iş parçacığı 68 ms); 2. koşuda yok. Nedeni ayrıştırılmadı.
- Test haritasındaki hareket kayıtlarında kare süresi 41,7 ms'de sabit (kayıt aracının kare sınırı); çarpışma tepkisi sırasında sıçrama yok (en fazla 43,2 ms).
- Standalone: oyun açıldı, ev haritası 30,8 s'de yüklendi, kendi kayıt dosyasını ayrı bir kullanıcı klasörüne yazdı (kullanıcı kaydına dokunulmadı), günlükte ölümcül hata yok. Girdi verilmediği için standalone'da **hareket ve temas denenmedi**; paketleme yapılmadı.

---

'''

sec4 = u'''## 4. Videolar

Gerçek hızda, 30 kare/s, hareket bulanıklığı veya alan derinliği eklenmeden. "omuz" = oyundaki gerçek yakın omuz kamerası; "yan / arka" = tam beden teşhis görünümü. Her videodan saniyede bir kare saklandı ve içerik bu karelerden denetlendi (`evidence/` altındaki şeritler); 03 dışındaki videolar f7, 03 f8 durumundandır.

| Dosya | İçerik |
|---|---|
| `01_omuz_…`, `02_yan_…` | aynı plan iki görünüm: bekleme → yürüyüş → tempo → koşu |
| `03_yan_baslangiclar_…` | düz kalkışlar: koşu, sprint, yürüyüş, geri (yumuşak başlangıç) |
| `04_omuz_donusler_…` | koşu / yürüyüş / sprint dönüşleri 45° / 90° / 135° |
| `05_yan_ters_yon_…` | koşu ve sprintte sağ↔sol ters dönüşler (planR1) |
| `06a`, `06b` | diz engeline koşu: geri adım → diz çökme → kalkma (yan + omuz) — tur 5'teki 09b'nin karşılığı |
| `07_…tasirken` | aynı engele taşıma durumunda yaklaşma |
| `08a`, `08b` | kütüğe sprint: takılma → düşme → yatma → kalkma (yan + omuz) |
| `09_…sendeleme` | kütüğe dinç koşu: takılma → sendeleme |
| `10a`, `10b` | duvara koşu / sprint: mesafeli duruş, el desteği, avuç hizalama |
| `11_…dar_alan` | arkası kapalı diz engeli (zorlanmış eşikler) |
| `12_…siyirma` | yan duvar boyunca koşu |
| `13_…alcak_kiris` | baş hizasındaki kirişin altından eğilerek geçiş |
| `14a`, `14b` | yorgunluk: 14 s sprint → duruş → yürüyüş → toparlanma → koşu (omuz + yan) |
| `15_…bekleme_45s` | 45 s bekleme (bekleme hareketleri) |
| `16a`, `16b` | merdiven yürüyüş / koşu |
| `17`, `18` | ev: yatak; maske alma → inceleme → bırakma |

Odun → şömine akışının videosu 99 MB olduğu için yayınlanmadı (yerelde `Saved/Codex/Day_20261107/videos/F19_flow_R6.mp4`). Kritik olaylardan diz engeli, düşme ve duvar iki görünümle kayıtlıdır; diğerleri tek görünümdür.

---

'''

sec5 = u'''## 5. Yapılmayanlar ve açık kalanlar

1. **Gamepad test edilmedi**; standalone'da hareket ve temas denenmedi (girdi yok); paketleme yapılmadı.
2. **Merdiven**: diz açısı 60–71°; doğal değer ~95°. Koşarak çıkışta diz açısı ölçütü ayırt edici değil (düz koşuda da 48°). Merdiven **inişi ölçülmedi** (test şeridinde iniş planı yok).
3. **Engelin üstünden yürüme**: yürürken ve tempoda ayak ucu 25 cm'lik kütüğe 10–13 cm giriyor. Yavaşlatma denendi, işe yaramadı, geri alındı; savrulan ayağı engele göre kaldıran bir katman yok.
4. **Çarpma anında ayak ucu**: koşarak diz engeline çarpma karesinde ayak ucu 9 cm, takılmada 8–9 cm engelin içinde (tek kare / kısa an). Çökme, yatma ve kalkma boyunca çakışma yok.
5. **Sıyırmada** dirsek 5 cm, el 7 cm duvarın içinde (kapsül duvara 6 cm mesafede).
6. **Tempo / sprint başlangıcı**: baş alçalması 20–21 cm; koşudaki kadar düşmedi. Dönerek kalkışlarda (90° / 180°) yumuşak başlangıç uygulanmıyor, eski atletik hamle duruyor.
7. **Taşırken yere düşme** oyunda oluşamıyor (taşırken hız 187, takılma eşiği 330 cm/s). Tek elle taşımada boştaki elin desteği uygulanmadı.
8. **Destek ayağına göre tepki**: çarpma anındaki destek ayağı kaydediliyor ve raporlanıyor, ama tepkinin yönünü değiştirmiyor. Toparlanma adımının basacağı zemin yalnız düşme için sondalanıyor.
9. **Düşme tek yönlüdür** (öne). Yana / arkaya düşme ve yerdeki poza göre farklı kalkış yok. Kullanılan klipler "karnını tutarak çökme" kökenlidir; eller karında.
10. **Yürüme hızında engelin önünde durma kuralı** (duvar 20 cm, diz hizası) ev içindeki istasyonlarla yalnız yatak, maske ve odun akışında denendi; çay, gardırop, kapılar denenmedi.
11. **Süreklilik işaretleri** görüntüyle eşleştirilmedi (bazı planlarda yalnız bacak kaynaklı işaretli kare sayısı arttı).
12. **Bekleme hareketleri değiştirilmedi** (ölçüm: en sakin dört hareket). Bekleme videosu kullanıcı değerlendirmesi içindir.
13. Performansta eşit görüntüde açık / kapalı karşılaştırması yapılmadı; bir kez görülen 72 ms'lik sıçramanın nedeni bilinmiyor.
14. Kamera listesi (dar alanda kadraj, duvara dayanınca omuz kadrajı, maske incelemede omuz), zıplamada duruş, çömelme geçişleri, taşıma duruşu, hareketli / itilebilir nesnelerle ayrıntılı test (itilebilir kutu yalnız "takılma → sendeleme" verdi), başka karakterle temas, şömine yanındaki parlak nokta: bu turda **ele alınmadı**.
15. Ham kayıtlardan 24'ü yayınlandı (`raw/*.json.xz`, kayıpsız); geri kalan ~90 kayıt yereldedir (`Saved/Codex/Grip_20261106/rec`).

---

'''
io.open(R, 'w', encoding='utf8').write(head + sec1 + sec2 + sec3 + sec4 + sec5 + sec6)
print('README', len(head + sec1 + sec2 + sec3 + sec4 + sec5 + sec6))
