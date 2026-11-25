# Character Physical Realism 2.0 — geçiş C (2026-11-25)

**Durum: IN PROGRESS.** İlk kez ana karakter gerçek oyun hareketinde ölçüldü; bulguya göre kıyafet ağları düzeltildi ve sınırlı bir ikincil hareket katmanı eklendi. Gerçek kumaş simülasyonu yok.

## 1. Hareketli deformasyon matrisi
`scripts/pose_rec.py`: PIE'de gerçek oyuncu hareket girdisiyle sürüldü — boşta, yürüyüş (150 cm/s), koşu (178), ani duruş, 180° dönüş, sprint (400), duruş, 90° yan dönüş, geri adım, çömelme, çömelerek yürüme, kalkma, zıplama, yatışma. 14 evre, **42 poz**, 342 kemiğin bileşen-uzayı dönüşümleri. Kareler: `evidence/hareket_matrisi_kareler.jpg`.
`scripts/bl_pose_qa.py`: beden, üst ve şort bu pozlarda Blender'da yeniden derilendi; kıyafet maskesinden **görünen** deri köşeleri için "kumaş derinin altında mı" testi ve omuz/dirsek/kalça/diz/boyun deri esnemesi.
Yöntem notu: iskelet varlığının referans pozu bu karakterin ağından 16,6 cm'ye kadar farklı; referans olarak ağın kendi eklem konumları kullanıldı.
Kapsanmayan: düşme/kalkma, nesne taşıma, uzanma, eğilme.

## 2. Bulgular ve düzeltme
| | Önce (VF2 ağları) | Sonra (yan daraltma) |
|---|---|---|
| Üst: kumaştan geçen deri köşesi, 42 poz toplamı | 5.227 | **1.876 (−%64)** |
| Üst: en derin (boşta) | 2,16 cm | 1,14 cm |
| Şort: toplam | 20.137 | 18.809 (−%7) |

Tam tablo: `data/deformation_matrix_summary.txt`.
Düzeltme (`scripts/bl_refit2.py` — karakter raporu klasöründe): yana bakan köşelerde bedenle boşluk üstte ortalama 2,4 → 1,7 cm, şortta 2,1 → 1,4 cm; ağlar aynı adla yeniden içe aktarıldı (şort yarı genişliği 21,1 → 19,4 cm).

**Çözülmeyen kök neden:** şorttaki geçişlerin çoğu kumaş bolluğundan değil, **elin ve bileğin kalçanın içinden geçmesinden**. Yürüyüş ve koşuda bilek pelvis ekseninden 15–16 cm yana kadar geliyor; kalça yarı genişliği yaklaşık 18,5 cm. Bu, kol salınımının bedene uzaklığıdır ve hareket sisteminin alanıdır; o sisteme dokunmadım, bulgu olarak iletiyorum.

**Deri esnemesi:** sprint ve çömelmede kalça çevresi p99 1,3–1,8, diz 0,6–0,7, omuz 0,3–0,5. Kalça ve diz için düzeltici şekil eklenmedi.

## 3. Kıyafet ikincil hareketi (uygulandı; simülasyon değil)
Chaos Cloth: bu derlemede Python'a açık hiçbir kumaş sınıfı yok; editör arayüzünü otomatikleştiremiyorum; C++ modülü eklemek Blueprint-only projeyi derlenen projeye çevirir — senin kararın olmadan yapmadım. **Chaos Cloth: BLOCKED (araç erişimi).**
Alternatif (`scripts/w_garment3.py`, `scripts/w_cloth_drive.py`): yüz Anim Blueprint'inin güncelleme olayı piyonun hızını ve yumuşatılmış kopyasını bir materyal parametre koleksiyonuna yazar; iki kumaş materyali giysinin alt bölümünde hız gecikmesi kadar küçük bir kayma ve hafif titreşim uygular. Üst en çok 2,4 cm, şort 1,4 cm ile sınırlı.
Doğrulama: sürücü oyunda çalışıyor (`data/hem_motion_driver.txt`: koşuya geçişte ve duruşta gerçek hız ile yumuşatılmış hız ayrışıyor). **Görsel etki küçük** ve tek karelerle kanıtlanamıyor (`evidence/kiyafet_ikincil_hareket.jpg` — fark göremedim); video yok. Bu madde "kumaş fiziği" sayılmaz.

## 4. Saç, kemer, aksesuar
Yeni iş yok.

## 5. Geri alma
`vf2_wgar3030743`, `vf2_wgar3030804`, `vf2_wmp031215`, `vf2_wcd030848`. Hareket katmanını kapatmak için iki materyal örneğinde `MotionInertia`, `MotionDrag`, `MotionFlutter` sıfırlanır.
