# Sphirus World — World & Environment Fidelity 2.0, devam geçişi (2026-11-25)

**Durum: KISMİ — küçük.** Dünyada tek kayıtlı değişiklik var: zemin otu renklerinin kısılması (10 materyal örneği). Orman dağılımı, arazi, patikalar, göl, kıyı ve arka bahçede **değişiklik yapılmadı**. Bir materyal rengi değiştirmek çevrenin geliştiği anlamına gelmez; bu bölümü uygulanmış saymıyorum.

## 1. Denetim (bu geçişte ölçülen)
- Foliage: **38.474 örnek**, yaklaşık 140 bileşen; ağaçlar (çam 7 tür + ladin, meşe, fidanlar), çalı 6, eğrelti 7, ot/saz 20+, yosun 6, ölü yaprak/iğne/dal/kozalak, mantar, kök, kütük, taş. Tür çeşitliliği ve yer örtüsü zengin; "aynı varlığın tekrarı" yapısal bir sorun olarak görünmüyor. Bölge bazlı yoğunluk/boşluk haritası **çıkarılmadı**.
- Gölgeli ışık: 16 nokta + 12 dikdörtgen (çoğu `ReviewOnly` klasöründe) + güneş.
- Kareler (8 dış nokta): göl ve orman genel olarak inandırıcı; en belirgin kusur ön bahçede güneş alan otların doygun sarı-yeşil, bakımlı çim gibi okunması; ikinci olarak bazı saz öbeklerinin ağarmış görünmesi.

## 2. Yapılan değişiklik
`GroundLayer20261111` altındaki 10 ot/yer örtüsü örneğinde `Translucency Color`, `Color Variation 2/3`: saklanan taban değerlerden doygunluk −%62, kazanç ×0,72 (önceki geçiş −%45 / ×0,85 idi). Örnek: orta ot geçirgenliği taban (0.546, 0.734, 0.053) → (0.437, 0.489, 0.302). Mevcut proje aracı kullanıldı (taban dosyası korunuyor, işlem tekrarlanabilir ve geri alınabilir).

Kanıt: `evidence/dunya_once_sonra_KAYITLI.jpg` (aynı dört nokta, aynı oyun kamerası; alt sıra temiz yeniden açılıştan sonra). **Dürüst değerlendirme:** ot biraz daha az "limon"; fark **incedir** ve güneş lekesinin konumuna göre değişiyor. Yama dağılımı (çıplak toprakla keskin geçiş) değişmedi — o, foliage dağılımının işi.

## 3. Yapılmayanlar
Ağaç ölçek/silüet dağılımı; alt bitki örtüsü yeniden dağıtımı; kök, taş, toprak geçişleri; nemli yüzeyler; patika kenarları; arazi eğimleri; göl kıyı çizgisi, su materyali, yansıma/parlama ölçümü; kıyı bitkileri; arka bahçe tasarımı; sabah/akşam/gece koşulları; AGENTS.md'nin istediği yeni ChatGPTBridge dışa aktarımı (anlamlı çevre değişikliği olmadığı için yapılmadı).

## 4. Performans (PIE, aynı editör derlemesi, farklı oturumlar)
| Nokta | Önce fps | Sonra fps |
|---|---|---|
| Göl→ev | 34,2 | 36,2 |
| Ön | 41,6 | 38,4 |
| Arka bahçe | 40,9 | 37,9 |
| Kıyı | 35,3 | 34,2 |
| Yokuş | 31,6 | 31,5 |
| Patika başı | 32,4 | 32,0 |
| Göl | 34,9 | 34,4 |
| Doğu | 36,5 | 35,9 |

Renk parametresi değişikliğinin maliyeti olamaz; farklar oturum oynamasıdır (ön/arka bahçedeki −3 fps dahil; karede karakterin yeni üst giysisi de var). En kötü nokta 31,5 fps ile aynı. Paketlenmiş oyun ölçümü yok.

## 5. Geri alma
`builtins.R2G_GRASS={'desat':0.45,'gain':0.85}` ile `Tools/R2G2_20261123/apply_grass.py` + kayıt (önceki geçişin değeri), ya da `vf2_wgrass020041` yedeği.

## 6. Sonraki adım
Ön bahçedeki ot yamalarının dağılımını (yoğunluk ve çıplak toprak geçişi) ele almak; göl için su odaklı kare seti ve parlama ölçümü; ardından arka bahçe.
