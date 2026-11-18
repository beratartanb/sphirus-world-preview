# SPHIRUS UE 5.9 — jog duruşu seçimi (2026-11-18, ikinci tur)

Bu tur, [sphirus-ue59-fullbody-2026-11-18](../sphirus-ue59-fullbody-2026-11-18/README.md) raporunda açık kalan "jog (415) bırakışı her seferinde sprint duruşu seçiyor" sorununu ele alır. Diğer bulgular o raporda geçerliliğini korur.

Durum etiketleri: **PASS** = ölçüm hedefi karşıladı, **PARTIAL** = iyileşme var ama açık kalan var, **NOT_TESTED** = denenmedi. Kullanıcı kabulü verilmedi (USER_ACCEPTED yok). Videolar kare kare incelendi, gerçek hızda izlenerek his değerlendirmesi yapılmadı.

## 1. Kök neden

| Katman | Bulgu |
|---|---|
| Seçici (`CHT_Sph_PoseSearchDatabases_Relaxed` → alt tablo `Stand Idles`) | Durma anındaki ilk boşta karesinde duruş veritabanını **Speed2D bandıyla** seçiyor: 20–170 yürüyüş duruşu, 170–400 koşu duruşu, 400+ sprint duruşu. Bantlar GASP Relaxed hızlarına (koşu 375, sprint 585) göre ayarlanmış. |
| Sphirus hızları | Yürüyüş 180, jog 415, sprint 585. Jog bırakışında ilk boşta karesindeki hız ~396–406 cm/s, yani **400 sınırının tam üstünde**. 60 Hz'de sprint bandına (Relaxed sprint duruşu, 29–32 cm kalça çöküşü), 30 Hz video adımında ise koşu bandına düşüyor. Seçim kare zamanlamasına bağlıydı; önceki turun "v5 kazanımı" bu yüzden tekrarlanamadı. |
| Yürüyüş | 180 cm/s, 170 sınırının üstünde. Yürüyüş bırakışı da koşu duruşu bandına düşüyordu (`M_Neutral_Run_Stop_F`, 22–64 cm ayak kayması). |
| Klip–fren uyumu | Sphirus'un PhysBrake freni sabit ~600 cm/s² ile yavaşlıyor. Relaxed koşu duruşu (375 cm/s, ~0,6 s'de durur) buna uyuyor. Ancak eşleme tablosu Relaxed koşu/yürüyüş duruşlarını Dense (Neutral) kliplere yönlendiriyordu; bunlar ~0,25 s'de, ~1650 cm/s² ile duruyor. Ölçüm: `data/stop_clip_root_speed.txt`. |

Elenen adaylar:
- **T9:** yalnız eşlemeyi kaldırmak, jog'da sprint seçimini değiştirmedi; yürüyüşü iyileştirdi.
- **T10:** sprint duruşu veritabanına maliyet cezası (0,5 / 1,5 / 4,0), test kopyalarında denendi ve kaydedilmedi. Çöküşü azalttı ama ilk karede sprint klibi yine seçilip ardından koşu duruşuna geçiliyordu. Kök nedeni çözmediği için alınmadı.
- **2026-11-18'in birinci turu:** Dense sprint duruşu eşlemesi ayak kaymasını 2 katına çıkardığı için geri alınmıştı.

## 2. Uygulanan değişiklik (kalıcı, 5.9 kopyası)

1. `CHT_Sph_PoseSearchDatabases_Relaxed:Stand Idles` Speed2D bantları: **20–200 / 200–440 / 440+**. Bu, Sphirus'a ait seçici kopyası; GASP orijinali değişmedi.
2. `ABP_Sph_GASP` eşleme tablosundan iki satır çıkarıldı: `PSD_Relaxed_Stand_Run_Stops → Dense_Stand_Run_Stops` ve `PSD_Relaxed_Stand_Walk_Stops → Dense_Stand_Walk_Stops` (34 → 32 satır). Fren yavaşlamasına uyan Relaxed koşu/yürüyüş duruşları artık kullanılıyor.
3. Sprint (585) duruşu bilerek değiştirilmedi.

Geri dönüş: manifest `ue59_m19_jstop`. Yedek dosyaları `Saved/Codex/SHME_V233_20261027/checkpoint/manifests/ue59_m19_jstop/`. Önceki SHA1 değerleri: ABP `073f1ead…`, seçici `ef3a2f78…` (`changes/ue59_m19_jstop.json`). Test kopyaları (`DB/Test/PSD_Sph_R_Sprint_Stops_B*`) hiç kaydedilmedi ve bellekten atıldı. Yazımdan sonra kirli paket yok.

## 3. Doğrulama (kayıtlı durum, düz test haritası, oyuncu kaydı)

"Önce" = çalışma anında geri alma (bantlar 170/400 + Dense eşlemeleri). Bu, ilk turdaki kayıtlı durumu birebir yeniden üretiyor (T12_JSTOP_before = T9_JSTOP_J0).

Jog duruşu planı (60 Hz veri adımı). Satırlar: farklı tutma süreleri/faz, kısa bırakış, yeniden basma, yürüyüş→koşu geçişi ve dönerek durma.

| Durum | Önce: klip / kalça çöküşü / ayak kayması | Sonra: klip / kalça çöküşü / ayak kayması |
|---|---|---|
| jog 3,00 s | Relaxed sprint duruşu / 32,3 / 12,2 | Relaxed koşu duruşu / 11,9 / 12,0 |
| jog 3,30 s | sprint / 30,5 / 76,1 | koşu / 11,9 / 30,0 |
| jog 3,65 s | sprint / 30,0 / 119,7 | koşu / 13,2 / 22,6 |
| jog 1,00 s (332 cm/s) | sprint / 20,0 / 17,5 | koşu / −1,9 / 29,7 |
| yeniden basma (0,4 s bırakış) | sprint / 22,7 / 13,6 | koşu / 12,6 / 2,5 |
| yürüyüş→koşu geçişinden duruş | sprint / 30,1 / 31,3 | koşu / 6,6 / **62,5** |
| 90° dönerek durma | sprint→Neutral koşu duruşu / 10,3 / 26,5 | koşu / 8,2 / **54,0** |
| jog 3,00 s (tekrar) | sprint / 32,4 / 15,5 | koşu / 12,8 / 7,6 |
| yürüyüş 180 | Neutral koşu duruşu / 9,6 / 33,1 | Relaxed yürüyüş duruşu / 4,6 / 30,9 |

- **30 Hz veri adımı** (`T12_JSTOP_saved30`): her jog bırakışında Relaxed koşu duruşu, kalça çöküşü 4,8–13,5 cm. Seçim artık kare adımından bağımsız. **PASS**
- **Durma planı:** jog 27,7 → 7,1 cm çöküş (kayma 73,5 → 63,7); yürüyüş kayması 21,6 → 5,6 cm; sprint 585 değişmedi (31,4 cm, Relaxed sprint duruşu).
- **Fren planı:** jog kayması 47,3 / 7,4 → 5,2 / 2,2 cm; yürüyüş 11,5 → 3,7 cm.
- **Kısa dokunuşlar:** 0,15 s'lik dokunuşta kayma 18,3 → 21,1 cm (biraz kötü); 0,6 s'lik dokunuşta 38,0 → 23,4 cm.

Değerlendirme:
- Jog duruşunun yanlış seçimi: **PASS**. Kalça çöküşü 30–32 cm'den 7–13 cm'ye indi; klip sıçraması yok.
- Ayak kayması: **PARTIAL**. Düz jog duruşlarında ve frende azaldı, ancak yürüyüş→koşu geçişinden ve 90° dönüşten duruşta arttı (31 → 62, 26 → 54 cm).

## 4. Videolar (`videos/`)

| Dosya | İçerik |
|---|---|
| `jstop60_before_left_after_right.mp4` | **Ana kanıt.** 60 Hz sabit adım, yan teşhis kamerası, solda önce sağda sonra. Videonun kendi ölçümü veriyle aynı: önce 32,2 / 30,4 cm (sprint duruşu), sonra 12,7 / 11,9 cm (koşu duruşu); yürüyüş kayması 63,8 → 5,3 cm. |
| `jstop_before_left_after_right.mp4` | 30 Hz sabit adım, yan kamera. Bu adımda "önce" durumu sprint duruşu yerine Dense koşu duruşunu seçti (13,6–16,7 cm). Fark daha küçük görünür. Bu video, eski seçimin kare zamanlamasına bağlı olduğunu da gösterir. |
| `jstop_pc_before_left_after_right.mp4` | 30 Hz, oyuncu kamerası; aynı not geçerli. |

Videolar oyun içi yavaşlatılmış zamanda (sabit adım) çekilip 30/60 fps'e birleştirildi. Gerçek zamanlı oyun akışı değil, kare zamanlaması eşleşmiş kayıtlar. Kare panosu: `evidence/jstop60_frames.jpg`. İlk jog bırakışı, −0,2 s'den +1,2 s'ye 0,2 s aralıkla; üst satır önce, alt satır sonra. Önce durumunda +0,4–0,8 s arasında gövde öne katlanıp derin çömeliyor; sonra durumunda gövde dik kalıyor, dizler orta düzeyde bükülüyor. Bu yan teşhis kamerasında ayaklar kadraj dışında; ayak teması için videolara ve `data/` ölçümlerine bakın.

## 5. Kapsam ve açık kalanlar

- **PARTIAL:** yürüyüş→koşu geçişinden ve dönerek durmada ayak kayması arttı.
- **Açık:** sprint (585) duruşu hâlâ 31 cm çöküyor ve 90–121 cm kayıyor (Relaxed sprint duruş klibi).
- **Açık:** sola 180° yürüyüş kayması; jog 135/180° alçalma; dik yokuşta ön diz; dar alanda kamera.
- **NOT_TESTED:** ev haritasında, yokuşta ve oyuncu hızı değişkenliğinde (eğim yavaşlaması 154 cm/s, tam 200 sınırına yakın değil ama denenmedi) duruş seçimi; paketlenmiş oyun.
- **Dünya önizlemesi (LATEST.json):** bu tur harita veya ışık değişmedi, yalnız animasyon seçimi değişti. Statik dünya görüntülerini etkilemediği için yeni dışa aktarım yapılmadı; LATEST.json aynı 5.9 çalışmasını (2026-11-18_102752_814812_8c909a) göstermeye devam ediyor.
- **Güvenlik:** 5.8.4 orijinaline ve gerçek kayıt dosyasına dokunulmadı. Test kaydının SHA1'i her koşudan sonra `4823d83a…` kaldı. GASP/UEFN satıcı varlıkları değişmedi.

## 6. Dosyalar

- `changes/`: yazım betiği `w_jstop19.py`, çalışma anı bant ayarı `ch_set.py`, test dizileri `seq9–13.sh`, problar, manifest.
- `data/`: tüm duruş analizleri (T9 eşleme, T10 maliyet cezası, T11 bantlar, T12 kayıtlı durum, video ölçümleri), klip kök hız profilleri, eski bant değerleri.
