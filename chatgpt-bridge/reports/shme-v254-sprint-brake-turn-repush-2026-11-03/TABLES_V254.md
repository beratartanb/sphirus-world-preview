# V2.54 tabloları

Kaynak: LTP günlükleri `Saved/Codex/SHME_V1_20260925/LTP/<etiket>.ltp`. Araçlar: `redir254.py`, `cam254.py`, `pop_report.py` (V2.1), `contact231.py`.

## Sütun ve etiket anlamları

| Sütun | Anlamı |
|---|---|
| min v | En düşük hız (cm/s) |
| tepe a | En yüksek ivme (g) |
| yol %80 | Yolun dönüşün %80'ine ulaştığı an (s) |
| yüz yeni | Beden yeni yöne 30° içinde baktığı an (s) |
| geri | Geri geri gidiş süresi (s) |
| eğilme 0,3 s | Talepten sonraki 0,3 s içinde eğilme değişimi (°) |
| en kötü sıçrama | m/s² |

- **Etiketler:** `a60_*_o` V2.54 öncesi üretim; `p60_*_o` V2.54 üretimi; `q60_*_o` V2.54 üretimi, ek kapsam.
- **Aday:** p60/q60 ile aynı (doğrulandı).
- 60 FPS ve sabit adım.

## Yön değişimi (60 FPS)

| senaryo | min v | tepe a | yol %80 | yüz yeni | geri | eğilme 0,3 s | en kötü sıçrama |
|---|---|---|---|---|---|---|---|
| sprint 180 R, önce | 0 | 0,82 | 1,02 | — | 1,02 | 27,9 → 27,8 | 48 |
| sprint 180 R, V2.54 | 2 | 0,73 | 1,18 | 1,52 | 0 | 27,9 → 22,4 | 53 |
| sprint 180 L, V2.54 | 3 | 0,74 | 1,15 | 1,48 | 0 | 28,6 → 24,3 | 48 |
| sprint 135 R, önce | 129 | 0,76 | 0,95 | — | 1,07 | 27,8 → 27,2 | — |
| sprint 135 R, V2.54 | 2 | 0,69 | 1,50 | 1,52 | 0 | 27,8 → 22,1 | 48 |
| sprint 90 R, önce | 288 | 1,30 | 0,82 | 0,62 | 0 | 27,7 → 27,2 | 64 |
| sprint 90 R, V2.54 | 173 | 1,09 | 0,78 | 0,73 | 0 | 27,7 → 22,0 | 51 |
| sprint 90 L, V2.54 | 142 | 0,76 | 1,13 | 1,07 | 0 | 27,7 → 22,0 | 52 |
| kısa ters dokunuş, önce | 291 | 0,82 | — | — | 0 | — | 48 |
| kısa ters dokunuş, V2.54 | 419 | 0,53 | — | — | 0 | — | 48 |
| dönüş ortasında komut, V2.54 | 203 | 1,39 | — | — | 0 | — | 50 |
| sağ-sol spamı, önce / V2.54 | 380 / 142 | 0,84 / 1,02 | — | — | 0 | — | 57 / 57 |
| jog 180 (değişmedi) | 4 | 0,82 | 0,45 | — | 1,72 | — | 49 |
| jog 135 (değişmedi) | 4 | 0,82 | 1,67 | — | 1,70 | — | 55 |
| yürüyüş 180 (değişmedi) | 1 | 0,62 | 0,57 | — | 1,43 | — | 37 |

- Kısa ters dokunuşta (V2.54) MM 0,27 s'de sprint döngüsüne dönüyor; üretimde de 0,27 s.
- Sağ-sol spamı: V2.54'te 45°/67° komutlar fren kesişine giriyor (bedeli var). Önceki üretim hızı koruyordu.

## FPS taraması (sprint 180 R)

| FPS | yüz yeni (önce → V2.54) | geri (önce → V2.54) | en kötü sıçrama (önce → V2.54) |
|---|---|---|---|
| 20 | — → 1,50 | 1,15 → 0 | 27 → 0 |
| 30 | — → 1,50 | 1,07 → 0 | 31 → 31 |
| 60 | — → 1,52 | 1,02 → 0 | 48 → 53 |
| 120 | — → 1,49 | 0,99 → 0 | 86 → 86 |
| gerçek zaman | — → 1,48 | 1,04 → 0 | 35 → 31 |

Sprint 90 R, 120 FPS: tepe ivme 1,66 g, en kötü sıçrama 114 (üretim 101). PARTIAL.

## Ayak kayması (`contact231`, 5,0–7,8 s)

| senaryo | önce | V2.54 |
|---|---|---|
| sprint 180 R | 33,6 cm (vendor pivot) | 17,2 cm (aktarım, `SHM254_Rev_R_T186` @ 1,46) |
| sprint 135 R | 8,1 cm (geri geri koşarken) | 11,4 cm |

## Regresyon (60 FPS; sıçrama sayısı / en kötü; üretim = aday)

| senaryo | önce | V2.54 |
|---|---|---|
| wstart | 5 / 33 | 5 / 33 |
| w42_id | 2 / 33 | 2 / 33 |
| taps | 7 / 47 | 7 / 47 |
| jstart | 14 / 47 | 14 / 47 |
| j36_stop | 6 / 32 | 6 / 32 |
| j45_sl2 | 18 / 51 | 16 / 52 |
| gait | 21 / 52 | 21 / 52 |
| w43_idle | 4 / 39 | 4 / 39 |
| j40_rlw | 13 / 40 | 13 / 40 |

## Kamera (`cam254`; gait senaryosu, mesafe cm)

| durum | üretim: mesafe / boy / ayak y / baş y | aday: mesafe / boy / ayak y |
|---|---|---|
| duruş | 195 / 1,14 / −1,73 / +0,55 | 192 / 1,16 / −1,75 |
| yürüyüş | 200 / 1,08 / −1,77 / +0,40 | 201 / 1,08 / −1,77 |
| jog | 221 / 0,94 / −1,58 / +0,31 | 233 / 0,90 / −1,51 |
| sprint | 223 / 0,86 / −1,51 / +0,22 | 237 / 0,82 / −1,43 |

- Ayak y −1 = ekranın alt kenarı; değer −1'den küçükse ayaklar kadraj dışında.
- Boy p95 değişim hızı: gait 1,05 → 1,01 /s; taps 0,34 → 0,36 /s.
- Yol ve kontrol yönü farkı (aday − üretim): 0,00 cm / 0,00° (gait, taps, cam32_wallturn, s54_revR).

## Omuz–kalça bükülmesi, 180 sonrası (°; 0 = düz sprintteki gibi)

| zaman (s) | V2.54 | + HeadOn (üretimde değil) |
|---|---|---|
| 6,5–7,1 | −17 | −17 |
| 7,1–7,7 | −21 | −4 |
| 7,7–8,0 | −33 | −6 |

HeadOn 120 FPS'te talep anında baş sıçraması üretiyor (155, HeadOn olmadan 86). Bu yüzden üretime alınmadı.
