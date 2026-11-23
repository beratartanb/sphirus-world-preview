# Reference to Game yaklaşımı ve Unreal'a uyarlanışı

Kaynak: https://github.com/gokayfem/reference-to-game (MIT, 0.1.0, commit `6a00e491f578bbfcbdba45f0c7bddf4693016e61`).
Bu yazı paketin kendisini kopyalamaz; ondan alınan çalışma biçimini ve mevcut bir Unreal Engine 5.9 projesinde nasıl kullanıldığını anlatır.
Projeye eklenen köprü beceri: `skill/sphirus-reference-review/SKILL.md`.

## Yaklaşımın özü

1. **Önce kanıta bak.** Görseli açmadan karar verme. Bağlantı kaydetmek incelemek değildir.
2. **Yetkiyi boyut boyut ata.** Bir görsel stili yönetirken başka bir kaynak kuralları yönetebilir. Çelişen kaynakların ortalaması alınmaz;
   her boyutun dayanağı yazılır.
3. **Gözlenen, çıkarılan, tasarlanan ayrı tutulur.** Tek kare gizli odayı, mesafeyi, zamanlamayı kanıtlamaz.
4. **Dünyayı büyütmeden önce küçük bir kesitte kimliği oturt.** Önce kamera ve özne ölçeği, sonra renk / ışık / malzeme, en son ayrıntı.
   Yanlış bir görüş açısı, varlık sorunu gibi görünebilir.
5. **En büyük farkı düzelt, aynı koşulda yeniden çek.** Evrensel benzerlik puanı yok; her karar için kısa gerekçe.
6. **Hükümler ayrı.** Stil, oynanabilirlik, durum / yeniden başlatma, build, performans ve varlıklar birbirini örtmez.
7. **Kanıt kaynağa bağlı.** Özetler değişen dosyayı yakalar; bir karenin iyi göründüğünü ya da bir testin gerçekten yapıldığını kanıtlamaz.

## Pakette ne var, ne yok

| Var | Yok |
|---|---|
| Alım: orijinalleri değiştirmeden kopyalama ve sha256 | Unreal / Unity / Godot proje üreticisi |
| `case / style / game / assets / review` sözleşmeleri | `.uasset` / `.umap` okuma |
| `palette`: verilen koordinattan anlamsal renk örneği | Otomatik sanat değerlendirmesi |
| `compare`: germeden, puansız yan yana karşılaştırma | Oynanış testi |
| `freeze / evidence / validate`: özet ve tazelik denetimi | "Kısmi" durum (yalnız `passed` yazabiliyor) |

Varsayılan uygulama profili Three.js'tir. Bu çalışmada o bölüm hiç kullanılmadı.

## Unreal'a uyarlama

| Paket adımı | Bu projede karşılığı |
|---|---|
| `init` | `Docs/ReferenceToGame/<kasa>/` altında ayrı klasör; oyun kökü hedeflenmedi |
| Referans yetkisi | `case.json` içinde her görsel için "neyi yönetir / neyi yönetmez" |
| Küçük sahne | Mevcut haritada sabit 15 kontrol noktası; gerçek oyuncu kamerasından 1600×900 kare |
| Eşleşen kamera karşılaştırması | Aynı nokta, aynı çözünürlük, gövde kamera yönüne dönük; `r2g compare` |
| En büyük farkı düzelt | Aday bellekte, tek değişkenle; aynı noktalardan yeniden çekim; kazanç yoksa geri alma |
| Kalıcı değişiklik | Projenin kendi kapılı yazma yolu: doğrulanmış yedek, tek kilit sahibi, derlemeden sonra temiz yeniden açma, geri okuma |
| Girdiyle oynanış | Aynı tuş planının önce / sonra kaydı; girdinin nasıl üretildiği açıkça yazılır |
| Kaynağa bağlı kanıt | Gerçek Unreal dosyalarının sha256 kaydı kasanın `app/` klasörüne yazılır, sonra `freeze` |

## Sahada öğrenilenler

- **Önce doğru projeyi bul.** Aynı oyunun iki kopyası vardı. Hangisinin canlı olduğu, çalışan editörün açtığı `.uproject` dosyasından anlaşıldı.
- **Görseli içeriğinden tanı.** Altı görsel beklenirken sekiz geldi; biri (rezonans hâli) hiç yoktu, üçü listede değildi. Eksik olan için
  karar üretilmedi, fazlalar en düşük yetkiyle kaydedildi.
- **Işınlanarak alınan kare yalnız kadrajı kanıtlar.** İlk turda gövde rastgele yöne bakıyordu; gövdeyi kamera yönüne çevirmeden kamera
  karşılaştırması anlamsızdı.
- **Tek kareden sayı türetme; ölçeği kareyle eşle.** Kamera değerleri referanstan FOV ya da kol uzunluğu çıkarılarak değil, oyun karesinde
  gövde ölçeği referansla eşlenerek seçildi. İlk bakışta saç kütlesi ölçü alınmıştı; saç referansta daha hacimli olduğu için yanıltıcıydı,
  baş–kalça yüksekliği doğru ölçüydü.
- **Etkisiz aday da sonuçtur.** Göl parlaması için dört tek değişkenli deneme görünür fark yaratmadı. Hepsi geri alındı ve "bunları tekrar
  deneme" notuyla kaydedildi. Batı kıyısından alınan kare, sorunun malzemede değil bakış yönünde olduğunu gösterdi.
- **Ölçüm aracının kendisi yanıltabilir.** Editör yeniden açıldıktan sonra ilk tur 3 fps ölçtü; neden arka plan kısıtlamasıydı. O tur atıldı.
- **`freeze` yanlış güven verebilir.** Paket yalnız sözleşmeleri ve `app/` klasörünü özetler. İçine gerçek Unreal dosyalarının özet kaydı
  konmasaydı, harita ve Blueprint hiç denetlenmeden "taze" görünürdü.
- **Aracın yazamadığı durumu elle yaz.** `evidence` komutu yalnız `passed` yazıyor. Kısmi kalan kontroller elle `partial` yapıldı ve
  `validate --release` bilerek geçmiyor.
- **Bağımlılık kurarken doğrulamayı atlama.** Pillow kurulumu sertifika hatası verdi; doğrulamayı kapatmak yerine sistem sertifika deposu kullanıldı.

## Sınırlar

- Bu tek bir kesitte, tek bir turdur; yaklaşımın başka girdilerde ya da projelerde işe yaradığını kanıtlamaz.
- Kanıtlar yazarın beyanıdır. Kayıtlar enjekte tuşlarla alındı ve gerçek hızda izlenmedi.
- Bu pakette ham referans görselleri yoktur; karşılaştırma görsellerinde küçültülmüş hâlleri yer alır.
