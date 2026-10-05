# GD11 K — referans manifesti (2026-10-05)

| Kaynak | Dosya | Tür | Güvenilir gösterdiği | Dikkat |
|---|---|---|---|---|
| Orijinal ön (Tier A) | `Saved/Codex/CharacterIdentity_20260930/track/ref_front_x4.png` (800×960, ×4 büyütme; `concept_guardian_approved.png` sol figürün yüzü) | kullanıcı referansı | yüz genişliği/yüksekliği oranları, göz–burun–ağız–çene dikey oranı, elmacık/alt yanak/çene konturu, burun tabanı genişliği, kaş yerleşimi, sakin ifade | küçük kaynak (≈200 px yüz) büyütülmüş; keskin detay yok; kamera: `camfit_front` (göz+dudak eğrileriyle çözüldü) |
| Orijinal yakın 3/4 (Tier A) | `.../track/ref_close_x2.png` (794×940; `concept_guardian_approved.png` sağ panel) | kullanıcı referansı | burun kökü–sırt–uç ilişkisi, elmacık öne çıkışı, çene–alt dudak geçişi, göz çukuru derinliği, kulak önü saç çerçevesi, ense–topuz toplanması | kamera yaw ≈ −60°, pitch 11° (`camfit_close`; önceki pasta 14° aşırı yaw düzeltildi); baş hafif eğik; ifade hafif gergin |
| 6 açılı sayfa | `Saved/Codex/GD11_HeadRefinementI_20261004/reference/user_sheet_20261004.png` (+ `sheet_*.png`) | üretilmiş yardımcı | saç silüeti ve akış yönü, genel profil karakteri, arka topuz | üretilmiş; açılar birbiriyle kesin uyumlu değil; "LEFT/RIGHT 3/4" etiketleri doğrulanmadı (ikisi de aynı yüz yarısını gösterebilir); profil geometrisi için **tahmin** |
| Üretilmiş profil / turnaround / yüz etüdü | `Saved/Codex/CharacterGuardian_20261001/ref*/` (`sheet_turnaround.png`, `face_study_p*.png`) | üretilmiş yardımcı | profil burun/çene eğilimi (yalnız yön) | ölçü için kullanılmaz |
| Ölçüm işaretleri | `Saved/Codex/CharacterIdentity_20260930/ref_picks.json` (ön + yakın: kaş, burun, elmacık/çene konturları, kulak tragus/lob) ve MetaHuman tracker eğrileri `Saved/Codex/CharacterGuardian_20261001/track/ref_{front,close}.json` (göz kapağı, dudak, filtrum, nazolabial) | ölçüm | 2D karşılaştırma; birim = referansın göz-merkezi aralığı (IPD) | picks el ile %5 ızgaralı zoom üzerinde okundu; ±3 px belirsizlik |

Çelişki kuralı: ön ve yakın 3/4 çelişirse ön öncelikli (ön kamera roll/pitch dahil çözüldü); 3/4 yalnız derinlik/öne çıkış için. Yardımcı sayfalar sadece yön verir.

Kamera/ışık ayrımı: referans çerçevesi karşılaştırmaları hep aynı çözülmüş kameralarla (`gd_common.VIEWS`), göz-merkezi hizalı; UE çekimleri kilitli kameralarla (`gd11rk_caps.sh`), dengeli tanı ışığı (`front`) + stüdyo.
