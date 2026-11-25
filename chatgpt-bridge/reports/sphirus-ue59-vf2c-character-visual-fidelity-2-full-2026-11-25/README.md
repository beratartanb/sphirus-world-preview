# Character Visual Fidelity 2.0 — geçiş C (2026-11-25)

**Durum: IN PROGRESS.** Yeni: yüz davranışı (göz kırpma + bakış) ve ölçüye dayalı anatomi denetimi. Kıyafet ve hareketli deformasyon ayrıntısı fiziksel gerçekçilik raporunda.

## 1. Anatomi denetimi (ölçüm; düzeltme yok)
Yöntem: oyunda görünür bedenin kemik konumları (`scripts/anat_probe.py`) ve dışa aktarılan ağın Blender ölçümü (`scripts/bl_rest_bones.py`). Veri: `data/anatomy_measurements.txt`.
- Boy (göz yüksekliğinden tahmin) yaklaşık 172,6 cm; kalça yüksekliği/boy 0,542, uyluk 0,257, baldır 0,250, omuz yüksekliği 0,812 — yetişkin kadın referans aralığında.
- Üst kol 26,8 cm, ön kol 24,8 cm: oyun içi değerler ağın dinlenme pozuyla **birebir aynı**; animasyon/retarget kemik uzunluğunu değiştirmiyor. Sol/sağ fark 0,1 cm.
- Üst kol/boy 0,155 (referans 0,172): eklem merkezleri arası ölçü antropometrik işaret noktalarından kısa okunur; tek başına "kısa kol" kanıtı değil, ama kol toplamı da alt sınırda — inceleme adayı.
- Omuz: eklem merkezleri arası 24,7 cm, deri yüzeyinde genişlik 42,3 cm; bel en dar 21,8, kalça en geniş 37,1 cm. Omuz yüksekliği sol/sağ farkı 0,5 cm.
- Sonuç: geometri/iskelet kaynaklı kaba bir oran hatası bulmadım. El, ayak, köprücük, sırt, boyun hizası için bölgesel görsel inceleme ve hareketli duruş değerlendirmesi **yapılmadı**; düzeltme uygulanmadı.

## 2. Yüz davranışı (uygulandı, kayıtlı)
Önce: yüz Anim Blueprint'i yalnız bedenden poz kopyalayıp sabit bir dinlenme ifadesi ekliyordu; 12 saniyelik ölçümde göz kırpma eğrileri hiç değişmiyordu — karakter hiç göz kırpmıyordu.
Yapılan (`scripts/w_face_life.py`): `ABP_Hazel_Face` içine üç eğri düğümü (göz kapağı, sola bakış, sağa bakış) zincirlendi; ağırlıklarını olay grafiğinde oyun zamanından üretilen iki farklı periyotlu darbe dizisi (4,3 sn ve 7,1 sn; 0,22 sn süren kırpma) ve iki yavaş pencere (bakış, en çok %10) sürüyor.
Doğrulama (yeniden açılmış editör, PIE): `data/face_life_curves.txt` — kırpma eğrisi 0'dan 1,0'a, 12 saniyede 5 kırpma; bakış eğrisi en çok 0,055–0,10. Kareler: `evidence/yuz_goz_kirpma_bakis.jpg` (açık / kırpma anı / bakış).
Sınırlar: sıklık yaklaşık 25/dk, insan dinlenme ortalamasının (15–20) biraz üstü — periyotlar uzatılabilir; ritim rastgele değil, iki periyodun üst üste binmesi; video yok; bakış kayması karede zor seçiliyor. Duruma bağlı ifade yok.

## 3. Kıyafet görünümü
`evidence/kiyafet_once_sonra_C_KAYITLI.jpg`: yan daraltmadan sonra kayıtlı oyun. Durağan karelerde fark küçük; kazanç hareketli pozlarda ölçüldü (fizik raporu).

## 4. Yapılmayan
Dudak ve göz kapağı geometrisi, yüz-boyun materyal sürekliliği, saç çizgisi, LOD geçişleri, farklı ışıklarda yüz okunurluğu. Saç: yeni iş yok (fizik önceki geçişte reddedildi; perçem biçimi kaynak dosya olmadan engelli; kemik tabanlı alternatif denenmedi).

## 5. Geri alma
`vf2_wface025035` manifest yedeği (yüz Anim Blueprint'inin önceki hali).
