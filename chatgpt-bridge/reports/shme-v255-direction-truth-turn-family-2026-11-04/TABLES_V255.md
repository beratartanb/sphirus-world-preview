# SHME V2.55 ölçüm tabloları

Üretim = V2.54 kayıtlı değerler (`o`). Aday = `c7h`. Bütün ölçümler 2026-11-04 tarihli. Sabit adımlı editör, aksi yazılmadıkça 60 FPS. Süreler tuş değişiminden itibaren saniyedir.
Bu tablolar teknik ölçümdür. Hiçbiri görsel kabul değildir.

## 1. Zor dönüş karnesi, 60 FPS

Dört şey ayrı ölçülür: ilk tepki (ivme komuta dönüyor), yüz (gövde komuta 30° yakın), yön (hareket komuta 30° yakın), yeniden hız (dönüş öncesi hızın %80'i).

| senaryo | yapı | v0 | ilk tepki s | yüz s | yön s | yeniden hız s | en düşük v | tepe g | geri s |
|---|---|---|---|---|---|---|---|---|---|
| s54_revR | üretim | 490 | 0.18 | 1.55 | 1.23 | 2.72 | 1 | 0.71 | 0.07 |
| s54_revR | aday | 490 | 0.00 | 0.98 | 0.93 | 1.72 | 6 | 1.00 | 0.00 |
| s54_revL | üretim | 490 | 0.18 | 1.52 | 1.20 | 2.68 | 1 | 0.70 | 0.07 |
| s54_revL | aday | 490 | 0.00 | 0.98 | 0.90 | 1.93 | 9 | 1.04 | 0.00 |
| s54_r135 | üretim | 490 | 0.18 | 1.52 | 1.52 | - | 2 | 0.68 | 0.07 |
| s54_r135 | aday | 490 | 0.00 | 1.05 | 0.98 | 2.02 | 7 | 1.06 | 0.00 |
| s54_r90 | üretim | 490 | 0.00 | 0.77 | 0.77 | 1.88 | 170 | 1.06 | 0.00 |
| s54_r90 | aday | 490 | 0.00 | 0.58 | 0.63 | 1.35 | 209 | 1.09 | 0.00 |
| s54_l90 | üretim | 490 | 0.00 | 1.10 | 1.10 | 1.98 | 141 | 0.64 | 0.00 |
| s54_l90 | aday | 490 | 0.00 | 0.83 | 0.85 | 1.83 | 211 | 1.00 | 0.00 |
| j54_rev | üretim | 300 | 0.00 | - | 0.50 | 1.53 | 0 | 0.89 | 2.50 |
| j54_rev | aday | 300 | 0.00 | 1.00 | 0.92 | 1.33 | 5 | 1.04 | 0.00 |
| j54_r135 | üretim | 300 | 0.03 | - | 1.67 | 1.65 | 1 | 0.89 | 1.98 |
| j54_r135 | aday | 300 | 0.00 | 0.95 | 0.92 | 1.33 | 5 | 1.08 | 0.00 |
| j54_r90 | üretim | 300 | 0.18 | 0.72 | 0.72 | 1.05 | 175 | 0.56 | 0.00 |
| j54_r90 | aday | 300 | 0.25 | 0.47 | 0.50 | 0.82 | 143 | 0.89 | 0.00 |
| j38_c90l | üretim | 300 | 0.42 | 0.92 | 0.92 | 1.33 | 162 | 0.58 | 0.00 |
| j38_c90l | aday | 300 | 0.37 | 0.62 | 0.67 | 1.15 | 142 | 0.86 | 0.00 |
| w54_rev | üretim | 132 | 0.00 | - | 0.68 | 1.12 | 0 | 0.62 | 2.32 |
| w54_rev | aday | 132 | 0.00 | - | 0.68 | 1.12 | 0 | 0.62 | 2.32 |

## 2. Yön matrisi

W→S, A→D, çapraz→ters çapraz; kamera açısı 0, 60, −120; farklı destek ayakları; yürüyüş, koşu, sprint.

| yapı | olay | hatalı | not |
|---|---|---|---|
| üretim | 144 | 21 | hepsi koşuda (jog) |
| aday | 144 | 0 | t30 medyan/en kötü: yürüyüş .57/.70, koşu .67–.68/.92, sprint .82–.88/1.00–1.02; kamera açısına göre değişmiyor |

## 3. Rastgele tuş testi (fuzz), 60 FPS, üretim→aday

WRONG: ivme komutun tersine. STALL: komuta doğru hiçbir şey olmuyor. FRAME: tuşun ekrandaki anlamı ile uygulanan yön ayrı. OSC: yön sıçraması. Uzun yanlış: 0,15 s'den uzun WRONG.

| senaryo | WRONG s | STALL s | FRAME s | OSC | uzun yanlış |
|---|---|---|---|---|---|
| sprint, otomatik kamera | .73→.08 | 2.22→2.73 (kötüleşti) | .82→.05 | 149→38 | 0→0 |
| sprint, fare | 1.03→.42 | 3.78→2.64 | | | 2→0 |
| koşu, otomatik kamera | 1.18→.61 | 4.75→3.11 | .80→.05 | 66→38 | 2→0 |
| koşu, fare | .53→.65 (biraz kötüleşti) | 4.29→2.61 | | | 1→1 |
| yürüyüş, otomatik kamera | .05→0 | 1.18→.68 | .42→.03 | 75→36 | |

Koşu faresindeki kalan tek olay: t 23.20, v 53, A>D, başlangıç klibi kuyruğunda, en çok .18 s.

## 4. Dönüş ortasında yeni komut (60 FPS)

| senaryo | yapı | t | yeni tuş | v0 | ilk tepki | yüz | yön | en düşük v | 1.2 s tepe v | tepe g |
|---|---|---|---|---|---|---|---|---|---|---|
| s54_tap | üretim | 5.00 | +180 | 490 | 0.18 | - | - | 409 | 498 | 0.54 |
| s54_tap | üretim | 5.25 | +0 | 470 | 0.12 | 0.00 | 0.00 | 409 | 490 | 0.42 |
| s54_tap | aday | 5.00 | +180 | 490 | 0.00 | - | - | 317 | 490 | 0.77 |
| s54_tap | aday | 5.25 | +0 | 356 | 0.10 | 0.00 | 0.00 | 317 | 490 | 0.29 |
| s54_mid | üretim | 5.00 | +90 | 490 | 0.00 | - | - | 190 | 494 | 0.62 |
| s54_mid | üretim | 5.50 | +0 | 338 | 0.12 | 0.00 | 0.00 | 190 | 417 | 0.75 |
| s54_mid | aday | 5.00 | +90 | 490 | 0.00 | - | - | 209 | 490 | 0.83 |
| s54_mid | aday | 5.50 | +0 | 209 | 0.08 | 0.15 | 0.00 | 214 | 473 | 0.41 |
| s54_lr | üretim | 4.50 | +45 | 490 | 0.12 | 0.20 | 0.23 | 293 | 490 | 0.68 |
| s54_lr | üretim | 4.85 | -45 | 448 | 0.07 | - | - | 141 | 454 | 0.74 |
| s54_lr | üretim | 5.20 | +45 | 385 | 0.05 | 0.25 | 0.30 | 139 | 422 | 0.57 |
| s54_lr | üretim | 5.55 | -45 | 413 | - | - | - | 139 | 422 | 0.92 |
| s54_lr | üretim | 5.90 | +0 | 209 | 0.48 | 0.00 | 0.00 | 139 | 396 | 0.86 |
| s54_lr | aday | 4.50 | +45 | 490 | 0.12 | 0.20 | 0.23 | 218 | 490 | 0.68 |
| s54_lr | aday | 4.85 | -45 | 448 | - | - | - | 218 | 454 | 1.01 |
| s54_lr | aday | 5.20 | +45 | 243 | 0.08 | 0.00 | 0.00 | 218 | 352 | 0.35 |
| s54_lr | aday | 5.55 | -45 | 267 | 0.17 | - | - | 229 | 441 | 0.58 |
| s54_lr | aday | 5.90 | +0 | 229 | 0.00 | 0.00 | 0.00 | 229 | 490 | 0.37 |

## 5. Pop tablosu, 60 FPS

`exc_cm` karşılaştırılır. m/s² tepe değeri kare hızıyla büyür ve yavaş büyük harekette de tetiklenir.

| senaryo | sayı A→B | en yüksek m/s² A→B | en yüksek exc cm A→B | exc>1.5 A→B | B en kötü exc nerede |
|---|---|---|---|---|---|
| s54_revR | 18→16 | 53→61 | 0.82→1.38 | 0→0 | t 5.37 mv_sprint_180_1 +0.37 v295 sh_r |
| s54_revL | 18→20 | 48→65 | 0.69→1.49 | 0→0 | t 5.63 mv_sprint_180_1 +0.33 v298 sh_l |
| s54_r135 | 14→20 | 48→62 | 0.81→1.21 | 0→0 | t 5.77 mv_sprint_135_1 +0.77 v168 pelvis |
| s54_r90 | 17→14 | 51→55 | 0.92→0.79 | 0→0 | t 5.33 mv_sprint_90_1 +0.33 v297 sh_r |
| s54_l90 | 18→20 | 52→54 | 0.92→1.06 | 0→0 | t 5.15 mv_sprint_-90_1 +0.15 v420 head |
| j54_rev | 9→12 | 49→64 | 1.09→1.21 | 0→0 | t 5.15 mv_jog_180_1 +0.15 v254 head |
| j54_r135 | 10→11 | 55→74 | 1.27→1.18 | 0→0 | t 5.22 mv_jog_135_1 +0.22 v241 head |
| j54_r90 | 9→9 | 52→55 | 0.84→0.88 | 0→0 | t 5.15 mv_jog_90_1 +0.15 v231 head |
| j38_c90l | 13→10 | 39→64 | 0.64→1.29 | 0→0 | t 5.45 mv_kb_-90_5_A +0.15 v258 head |
| w54_rev | 2→2 | 37→37 | 0.61→0.61 | 0→0 | t 2.93 mv_walk_0_0 +0.93 v132 sh_r |
| s54_tap | 21→18 | 48→51 | 0.82→1.08 | 0→0 | t 5.35 mv_sprint_0_2 +0.10 v331 sh_r |
| s54_mid | 22→19 | 48→48 | 0.78→0.79 | 0→0 | t 5.33 mv_sprint_90_1 +0.33 v297 sh_r |
| s54_lr | 18→18 | 57→48 | 1.11→0.82 | 0→0 | t 6.93 mv_sprint_0_5 +1.03 v488 chest |
| fz_sprint_a | 89→91 | 174→227 | 3.59→1.28 | 4→0 | t 44.33 v_kbs_135_103_SD +0.43 v295 sh_r |
| fz_sprint_m | 81→84 | 78→154 | 1.71→1.78 | 2→3 | t 30.83 mv_kbs_135_77_SD +0.23 v130 sh_r |
| fz_jog_a | 77→71 | 82→133 | 1.39→1.31 | 0→0 | t 29.00 mv_kb_-90_61_A +0.05 v2 sh_r |
| fz_jog_m | 52→70 | 96→98 | 2.17→1.57 | 1→1 | t 16.37 +mv_kb_135_48_SD +0.22 v52 head |
| fz_walk_a | 23→15 | 38→38 | 0.65→0.64 | 0→0 | t 2.32 mv_kb_0_1_W +0.02 v0 sh_l |
| fz_walk_m | 13→13 | 37→37 | 0.79→0.79 | 0→0 | t 3.75 _osc+mv_kb_0_1_W +1.25 v132 sh_r |
| wstart | 5→4 | 33→33 | 0.79→0.61 | 0→0 | t 2.93 mv_walk_0_0 +0.93 v132 sh_r |
| w42_id | 2→2 | 33→33 | 0.64→0.64 | 0→0 | t 8.93 mv_walk_0_2 +0.93 v132 sh_r |
| taps | 7→7 | 47→47 | 0.88→0.88 | 0→0 | t 3.77 mv_walk_rel_3 +0.02 v16 head |
| jstart | 14→14 | 47→47 | 0.77→0.77 | 0→0 | t 9.03 mv_jog_-45_4 +1.03 v226 head |
| j36_stop | 6→6 | 32→32 | 0.64→0.64 | 0→0 | t 2.32 mv_kb_0_3_W +0.02 v0 sh_l |
| j45_sl2 | 16→18 | 52→55 | 0.84→0.88 | 0→0 | t 5.45 mv_kb_90_5_D +0.15 v231 head |
| gait | 25→21 | 49→52 | 1.00→0.94 | 0→0 | t 14.83 mv_walk_0_0 +12.83 v444 pelvis |
| w43_idle | 4→4 | 39→39 | 1.05→1.05 | 0→0 | t 16.15 mv_walk_rel_3 +0.15 v93 sh_r |
| j40_rlw | 13→13 | 40→50 | 0.64→0.88 | 0→0 | t 5.45 mv_kb_90_5_D +0.15 v231 head |

## 6. Ayak temasları, t 5–8 (üretim→aday, cm)

`contact231` SLIP etiketi alçak salınan ayağı da sayabilir. Rakamlar kayma kanıtı olarak değil, karşılaştırma olarak okunmalıdır.

| senaryo | en kötü |
|---|---|
| s54_revR | 12.1→8.4 |
| s54_revL | 8.1→13.3 (sprint döngüsünde) |
| s54_r135 | 9.9→11.9 (döngüde) |
| s54_r90 | 11.5→8.4 |
| s54_l90 | 11.6→11.7 |
| j54_rev | 7.2→10.0 |
| j54_r135 | 6.0→10.6 |
| j54_r90 | 17.4→8.7 |
| j38_c90l | 27.6→17.5 |

Klip kalitesi (8 klip, 90° kesiş klipleri yeniden üretilmeden önce ölçüldü, yeniden koşulmadı): yüklü dizin ayak ucundan sapması 35°→5–7°, salınım tabanı −5.2→+2.4 cm, çapraz basış 0.

## 7. FPS taraması

### Karne

**20 FPS**

| senaryo | yapı | v0 | ilk tepki s | yüz s | yön s | yeniden hız s | en düşük v | tepe g | geri s |
|---|---|---|---|---|---|---|---|---|---|
| s54_revR | üretim | 490 | 0.10 | 1.60 | 1.30 | 2.80 | 7 | 0.56 | 0.05 |
| s54_revR | aday | 490 | 0.00 | 0.90 | 1.00 | 2.20 | 26 | 0.76 | 0.05 |
| j54_rev | üretim | 300 | 0.00 | - | 0.55 | 1.65 | 8 | 0.80 | 2.45 |
| j54_rev | aday | 300 | 0.00 | 0.60 | 0.70 | 1.20 | 40 | 0.77 | 0.10 |
| s54_revL | aday | 490 | 0.00 | 1.05 | 1.00 | 2.20 | 17 | 0.71 | 0.05 |
| s54_r90 | aday | 490 | 0.00 | 0.70 | 0.80 | 1.90 | 116 | 0.66 | 0.00 |
| j54_r90 | aday | 300 | 0.25 | 0.50 | 0.55 | 0.90 | 121 | 0.64 | 0.00 |

**30 FPS**

| senaryo | yapı | v0 | ilk tepki s | yüz s | yön s | yeniden hız s | en düşük v | tepe g | geri s |
|---|---|---|---|---|---|---|---|---|---|
| s54_revR | üretim | 490 | 0.10 | 1.57 | 1.27 | 2.77 | 2 | 0.57 | 0.07 |
| s54_revR | aday | 490 | 0.00 | 0.87 | 0.90 | 2.10 | 17 | 0.90 | 0.03 |
| j54_rev | üretim | 300 | 0.00 | - | 0.53 | 1.57 | 3 | 0.89 | 2.47 |
| j54_rev | aday | 300 | 0.00 | 1.07 | 1.00 | 1.40 | 8 | 0.79 | 0.00 |
| s54_revL | aday | 490 | 0.00 | 1.03 | 0.97 | 2.10 | 8 | 0.80 | 0.00 |
| s54_r90 | aday | 490 | 0.00 | 0.60 | 0.67 | 1.40 | 197 | 0.80 | 0.00 |
| j54_r90 | aday | 300 | 0.27 | 0.47 | 0.53 | 0.80 | 129 | 0.70 | 0.00 |

**120 FPS**

| senaryo | yapı | v0 | ilk tepki s | yüz s | yön s | yeniden hız s | en düşük v | tepe g | geri s |
|---|---|---|---|---|---|---|---|---|---|
| s54_revR | üretim | 490 | 0.00 | 1.51 | 1.19 | 2.62 | 0 | 1.06 | 0.05 |
| s54_revR | aday | 490 | 0.00 | 0.93 | 0.87 | 1.65 | 5 | 1.08 | 0.00 |
| j54_rev | üretim | 300 | 0.00 | - | 0.47 | - | 2 | 0.88 | 2.53 |
| j54_rev | aday | 300 | 0.00 | 0.97 | 0.89 | 1.32 | 1 | 1.16 | 0.00 |
| s54_revL | aday | 490 | 0.00 | 0.96 | 0.86 | 1.92 | 3 | 1.09 | 0.00 |
| s54_r90 | aday | 490 | 0.00 | 0.58 | 0.62 | 1.34 | 215 | 1.31 | 0.00 |
| j54_r90 | aday | 300 | 0.00 | 0.48 | 0.51 | 0.83 | 147 | 1.07 | 0.00 |

**real FPS**

| senaryo | yapı | v0 | ilk tepki s | yüz s | yön s | yeniden hız s | en düşük v | tepe g | geri s |
|---|---|---|---|---|---|---|---|---|---|
| s54_revR | üretim | 490 | 0.28 | 1.59 | 1.27 | 2.82 | 3 | 0.61 | 0.06 |
| s54_revR | aday | 490 | 0.00 | 1.01 | 0.96 | 1.78 | 17 | 0.99 | 0.03 |
| j54_rev | üretim | 300 | 0.02 | - | 0.51 | 1.54 | 7 | 0.88 | 2.46 |
| j54_rev | aday | 300 | 0.00 | 1.02 | 0.97 | 1.38 | 6 | 0.89 | 0.00 |
| s54_revL | aday | 490 | 0.00 | 1.02 | 0.91 | 1.97 | 13 | 1.01 | 0.00 |
| s54_r90 | aday | 490 | 0.00 | 0.58 | 0.66 | 1.38 | 203 | 0.86 | 0.00 |
| j54_r90 | aday | 300 | 0.25 | 0.45 | 0.50 | 0.82 | 139 | 0.78 | 0.00 |

`s54_l90` ve `j38_c90l` bu turda yalnızca ısınma geçişinde koştu, karneye girmedi.

### Rastgele tuş testi, fare (üretim→aday)

| FPS | sprint WRONG | sprint STALL | sprint uzun yanlış | koşu WRONG | koşu STALL | koşu uzun yanlış |
|---|---|---|---|---|---|---|
| 20 | .90→.10 | 3.65→1.65 | 2→0 | .20→.35 | 3.00→1.85 | 0→1 |
| 30 | .83→.07 | 2.34→1.41 | 2→0 | .20→.43 | 4.20→2.04 | 0→1 |
| 120 | .79→.33 | 2.52→2.77 | 2→0 | .62→.26 | 4.10→1.54 | 1→0 |
| gerçek zaman | 1.52→.03 | 3.66→1.45 | 3→0 | .37→.27 | 3.41→2.01 | 0→0 |

### Pop

=== pops 20
| senaryo | sayı A→B | en yüksek m/s² A→B | en yüksek exc cm A→B | exc>1.5 A→B | B en kötü exc nerede |
|---|---|---|---|---|---|
| s54_revR | 0→1 | 0→26 | 0.00→3.62 | 0→1 | t 6.65 mv_sprint_180_1 +1.65 v257 sh_l |
| j54_rev | 0→1 | 0→26 | 0.00→3.06 | 0→1 | t 6.20 mv_jog_180_1 +1.20 v244 sh_r |
| fz_sprint_m | 17→27 | 44→64 | 4.96→9.15 | 17→25 | t 19.20 +mv_kbs_rel_55_0 +0.10 v270 sh_r |
| fz_jog_m | 18→11 | 62→79 | 9.47→10.98 | 17→11 | t 36.40 +mv_kb_180_101_S +0.10 v160 head |
| wstart | 1→1 | 27→27 | 3.36→3.40 | 1→1 | t 17.75 mv_walk_135_10 +0.75 v97 sh_l |
=== pops 30
| senaryo | sayı A→B | en yüksek m/s² A→B | en yüksek exc cm A→B | exc>1.5 A→B | B en kötü exc nerede |
|---|---|---|---|---|---|
| s54_revR | 1→4 | 31→33 | 1.48→1.58 | 0→1 | t 6.60 mv_sprint_180_1 +1.60 v267 sh_l |
| j54_rev | 0→4 | 0→34 | 0.00→1.77 | 0→1 | t 6.17 mv_jog_180_1 +1.17 v157 sh_r |
| fz_sprint_m | 28→33 | 90→83 | 6.22→3.46 | 20→16 | t 19.20 +mv_kbs_rel_55_0 +0.10 v252 sh_r |
| fz_jog_m | 25→15 | 102→48 | 6.67→3.00 | 10→7 | t 35.50 +mv_kb_-45_98_WA +0.20 v52 head |
| wstart | 0→0 | 0→0 | 0.00→0.00 | 0→0 |  |
=== pops 120
| senaryo | sayı A→B | en yüksek m/s² A→B | en yüksek exc cm A→B | exc>1.5 A→B | B en kötü exc nerede |
|---|---|---|---|---|---|
| s54_revR | 7→5 | 155→126 | 0.71→0.85 | 0→0 | t 5.32 mv_sprint_180_1 +0.32 v298 sh_r |
| j54_rev | 10→8 | 163→160 | 0.97→0.80 | 0→0 | t 5.12 mv_jog_180_1 +0.12 v252 head |
| fz_sprint_m | 70→35 | 180→375 | 1.14→1.72 | 0→1 | t 30.79 mv_kbs_135_77_SD +0.19 v124 head |
| fz_jog_m | 63→44 | 195→367 | 1.24→2.48 | 0→1 | t 36.73 +mv_kb_180_101_S +0.43 v67 head |
| wstart | 21→19 | 56→56 | 0.32→0.32 | 0→0 | t 2.92 mv_walk_0_0 +0.92 v132 sh_r |
=== pops real
| senaryo | sayı A→B | en yüksek m/s² A→B | en yüksek exc cm A→B | exc>1.5 A→B | B en kötü exc nerede |
|---|---|---|---|---|---|
| s54_revR | 2→6 | 29→46 | 1.68→2.83 | 1→4 | t 3.76 mv_sprint_0_0 +1.75 v490 sh_l |
| j54_rev | 1→2 | 33→45 | 1.66→1.56 | 1→1 | t 5.20 mv_jog_180_1 +0.18 v244 head |
| fz_sprint_m | 29→38 | 126→72 | 9.56→3.19 | 17→16 | t 19.21 +mv_kbs_rel_55_0 +0.10 v253 sh_r |
| fz_jog_m | 21→21 | 89→40 | 5.95→5.47 | 15→8 | t 44.99 +mv_kb_rel_112_0 +0.05 v292 sh_r |
| wstart | 0→1 | 0→30 | 0.00→1.13 | 0→0 | t 17.73 mv_walk_135_10 +0.72 v96 sh_l |

Düşük kare hızında `exc_cm` kendiliğinden büyür. 20 FPS'te bir kare 3 kat uzun olduğu için rakamlar 60 FPS ile karşılaştırılmaz, aynı FPS'teki üretimle karşılaştırılır.

## 8. Gerçek rampa ve duvar, 60 FPS

Dönüşün gerçekten eğimde olduğu `where255.py` ile doğrulandı: rampa z 133→166, iniş z 131→94.

| senaryo | yapı | v0 | ilk tepki s | yüz s | yön s | yeniden hız s | en düşük v | tepe g | geri s |
|---|---|---|---|---|---|---|---|---|---|
| t255_ramp_s | üretim | 490 | 0.05 | 1.48 | 1.17 | 2.65 | 1 | 0.70 | 0.07 |
| t255_ramp_s | aday | 490 | 0.00 | 1.08 | 1.00 | 2.03 | 7 | 1.07 | 0.00 |
| t255_ramp_j | üretim | 300 | 0.00 | - | 0.50 | 1.52 | 0 | 0.89 | 2.50 |
| t255_ramp_j | aday | 300 | 0.00 | 1.00 | 0.92 | 1.33 | 5 | 1.04 | 0.00 |
| t255_ramp90_s | üretim | 490 | 0.00 | 0.80 | 0.80 | - | 139 | 1.05 | 0.00 |
| t255_ramp90_s | aday | 490 | 0.00 | 0.68 | 0.73 | 1.72 | 211 | 1.09 | 0.00 |
| t255_rampd_s | üretim | 490 | 0.00 | 1.43 | 1.12 | 2.55 | 2 | 0.74 | 0.07 |
| t255_rampd_s | aday | 490 | 0.00 | 1.08 | 1.00 | 2.03 | 7 | 1.07 | 0.00 |
| t255_wall_c | üretim | 490 | 0.18 | 1.57 | 1.27 | 2.73 | 0 | 0.70 | 0.05 |
| t255_wall_c | aday | 490 | 0.00 | 1.00 | 0.93 | 1.70 | 2 | 2.21 | 0.00 |

| senaryo | sayı A→B | en yüksek m/s² A→B | en yüksek exc cm A→B | exc>1.5 A→B | B en kötü exc nerede |
|---|---|---|---|---|---|
| t255_ramp_s | 20→16 | 51→66 | 0.98→1.45 | 0→0 | t 4.73 mv_sprint_180_1 +0.43 v296 sh_l |
| t255_ramp_j | 11→13 | 76→62 | 1.48→1.11 | 0→0 | t 5.10 mv_jog_180_1 +0.15 v254 head |
| t255_ramp90_s | 15→16 | 319→61 | 7.39→1.19 | 1→0 | t 4.45 mv_sprint_90_1 +0.15 v420 head |
| t255_rampd_s | 20→21 | 51→67 | 0.89→1.51 | 0→1 | t 6.68 mv_sprint_180_1 +0.43 v295 sh_l |
| t255_wall_c | 20→15 | 48→56 | 0.81→0.84 | 0→0 | t 9.28 mv_sprint_rel_2 +1.28 v0 head |

`t255_wall_c`: duvar 150 cm ileride. İki yapı da duvara çarpıyor (x 8155). Üretimde konum t 5.30'da durduğu hâlde bildirilen hız .8 s boyunca 420'den düşüyor, yani karakter duvara karşı koşuyor. Adayda hız 304'ten 3 karede sıfırlanıyor ve t 6.00'da yeni yöne çıkıyor. Tepe g 2.21 bu duvar duruşudur, gövde pop'u değildir (en kötü exc .84).

`contact231` eğimde anlamlı değil: zemini sabit seviye sayıyor ve neredeyse hiç temas bulamıyor. Rampa teması bu yüzden ölçülmedi, yalnızca kare dizisinden görsel olarak bakıldı.

## 9. Diğer zeminler (önceki tur, 60 FPS)

| senaryo | yapı | v0 | ilk tepki s | yüz s | yön s | yeniden hız s | en düşük v | tepe g | geri s |
|---|---|---|---|---|---|---|---|---|---|
| t255_hill_s | üretim | 490 | 0.18 | 1.55 | 1.23 | 2.72 | 1 | 0.71 | 0.07 |
| t255_hill_s | aday | 490 | 0.00 | 0.98 | 0.93 | 1.72 | 6 | 1.00 | 0.00 |
| t255_hill_j | üretim | 300 | 0.00 | - | 0.50 | 1.27 | 0 | 0.89 | 2.50 |
| t255_hill_j | aday | 300 | 0.00 | 0.65 | 0.57 | 1.00 | 5 | 1.02 | 0.00 |
| t255_hill90_s | üretim | 490 | 0.00 | 0.77 | 0.77 | - | 139 | 1.06 | 0.00 |
| t255_hill90_s | aday | 490 | 0.00 | 0.58 | 0.63 | 1.63 | 209 | 1.09 | 0.00 |
| t255_bump_s | üretim | 490 | 0.18 | 1.52 | 1.20 | 2.68 | 1 | 0.70 | 0.07 |
| t255_bump_s | aday | 490 | 0.00 | 0.98 | 0.90 | 1.93 | 9 | 1.04 | 0.00 |
| t255_step_j | üretim | 300 | 0.00 | - | 0.50 | 1.77 | 0 | 0.89 | 2.50 |
| t255_step_j | aday | 300 | 0.00 | 1.00 | 0.92 | 1.33 | 5 | 1.04 | 0.00 |
| t255_step_s | üretim | 490 | 0.18 | 1.55 | 1.23 | 2.72 | 1 | 0.71 | 0.07 |
| t255_step_s | aday | 490 | 0.00 | 0.98 | 0.93 | 1.72 | 6 | 1.00 | 0.00 |
| t255_wall_s | üretim | 490 | 0.00 | 0.77 | 0.77 | 2.38 | 0 | 2.90 | 0.00 |
| t255_wall_s | aday | 490 | 0.00 | 0.58 | 0.63 | - | 0 | 1.68 | 0.00 |
| t255_wall_b | üretim | 68 | 0.00 | - | 0.00 | 0.00 | 83 | 0.25 | 3.00 |
| t255_wall_b | aday | 68 | 0.00 | - | 0.00 | 0.00 | 83 | 0.25 | 3.00 |
| j40_wall | üretim | 300 | 0.18 | 0.72 | 0.72 | - | 0 | 1.77 | 0.00 |
| j40_wall | aday | 300 | 0.25 | 0.47 | 0.50 | - | 0 | 1.65 | 0.00 |
| cam32_wallturn | üretim | 490 | 0.00 | 1.13 | 1.13 | 1.98 | 141 | 0.70 | 0.00 |
| cam32_wallturn | aday | 490 | 0.00 | 0.63 | 0.65 | 1.62 | 211 | 1.07 | 0.00 |

| senaryo | sayı A→B | en yüksek m/s² A→B | en yüksek exc cm A→B | exc>1.5 A→B | B en kötü exc nerede |
|---|---|---|---|---|---|
| t255_hill_s | 18→15 | 53→61 | 0.82→1.38 | 0→0 | t 5.37 mv_sprint_180_1 +0.37 v295 sh_r |
| t255_hill_j | 14→13 | 74→57 | 1.61→0.82 | 1→0 | t 6.33 mv_jog_180_1 +0.13 v256 head |
| t255_hill90_s | 16→18 | 242→51 | 5.77→0.79 | 1→0 | t 5.33 mv_sprint_90_1 +0.33 v297 sh_r |
| t255_bump_s | 17→19 | 92→80 | 2.26→1.82 | 2→2 | t 8.57 mv_sprint_rel_2 +0.27 v360 sh_r |
| t255_step_j | 14→15 | 438→438 | 11.48→11.45 | 4→3 | t 4.67 mv_jog_0_0 +2.67 v300 sh_r |
| t255_step_s | 15→16 | 754→754 | 19.83→19.83 | 4→6 | t 4.88 mv_sprint_0_0 +2.88 v490 sh_l |
| t255_wall_s | 17→15 | 48→48 | 0.82→0.86 | 0→0 | t 5.92 mv_sprint_90_1 +0.92 v9 head |
| t255_wall_b | 20→20 | 212→212 | 1.62→1.62 | 1→1 | t 5.05 mv_sprint_180_1 +0.05 v92 head |
| j40_wall | 9→10 | 40→65 | 0.64→1.54 | 0→1 | t 6.95 mv_kb_90_5_D +1.65 v1 sh_r |
| cam32_wallturn | 13→14 | 66→66 | 1.49→1.49 | 0→0 | t 3.25 mv_kbs_0_2_W +1.20 v318 head |

## 10. 120 FPS baş pop'u: kafa katmanı açık ve kapalı

| senaryo | katman açık tepe / exc | katman kapalı tepe / exc | üretim tepe / exc |
|---|---|---|---|
| fz_sprint_m | 375 / 1.72 | 364 / 1.45 | 180 / 1.14 |
| fz_jog_m | 367 / 2.48 | 367 / 2.48 | 195 / 1.24 |

Kaynak kafa katmanı değildir. Olaylar plan girişindeki klip geçişindedir.

## 11. Terfi doğrulaması

Temiz yeniden açılıştan sonra `o` varyantı (kayıtlı değerler) ile `c7h`, 10 senaryoda aynı: s54_revR, s54_revL, s54_r135, s54_r90, s54_l90, j54_rev, j54_r135, j54_r90, j38_c90l, w54_rev. Isınma geçişi önce koştu.
