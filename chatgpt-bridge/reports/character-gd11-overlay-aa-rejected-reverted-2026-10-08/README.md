# GD11 tur AA: referans bindirmesiyle eşleme denemesi — KULLANICI REDDETTİ, GERİ ALINDI

Tarih: 2026-10-08. Durum: **GERİ ALINDI.** Aday tekrar ww5b (cilt x19a, saç h72d). Üretime geçirilmedi.

## İstek

"Mevcut karakterin her bölgesini referans ile aynı çizgiye gelecek şekilde eşle, üst üste koyarak."

## Ölçüm (ww5b, çözülmüş referans kameralarında)

Ölçüm iki yolla yapıldı:
- **Kontur noktaları:** ön ve 3/4 referans kameralarında, gözler hizalı.
- **MetaHuman izleyici eğrileri:** aynı izleyici hem referans fotoğrafta hem bizim render'da çalıştırıldı.

| Bölge | Sonuç |
|---|---|
| Gözler, ağız, filtrum, burun-dudak hattı (önden, gözlere göre) | 0–1 mm içinde örtüşüyor |
| Yanaklar (önden) | ±2 mm. Sol üst yanak +8,7 mm; o noktada referansta saç ve kulak var, ölçüm güvenilir değil. |
| Çene ve çene altı noktası | Ön kamerada 7–11 mm, 3/4 kamerada 12–14 mm yukarıda (çene kısa). Baş eğimi ±8° değiştirilince de aynı. |
| Alt çene hattı | 10–15 mm içeride |
| 6 görüntülü profil | dudak 0, burun −2 mm, çene +1,3 mm |
| Kel profil | Hizalamaya çok duyarlı (alın −13 mm); şekil için kullanılmadı. |

## Deneme

- **aa1:** alt yüz 1 cm aşağı kaydırıldı. Ağız köşelerinden inen kırışık çizgiler oluştu (maske hatası). **Elendi.**
- **aa3:** çene yüksekliği doğrusal olarak gerildi, alt çene 3 mm genişletildi, çene önü 4,5 mm geri alındı. Önden çene ve çene altı noktası referans noktalarıyla örtüştü; yeni katlanma yok; rig pozları ve hareket kareleri temiz.

## Sonuç

Kullanıcı: "Referans ile örtüşmüyor, bu denemeyi geri al."

- Aday ww5b'ye geri döndürüldü; önizleme yapılandırması tekrar `SKM_G11RR_Face_ww5b`, `m3w5`, `h72d`, `gqx19a`.
- `SKM_G11RR_Face_aa1` ve `aa3` elenmiş ara varlık olarak duruyor; silinmedi.
- **Ders:** çözülmüş kameralardaki çene noktaları ~1 cm uzatma istese de kullanıcı bunu referansa benzer bulmuyor. Bu, daha önceki çene uzatma retleriyle (K5, X) aynı yönde.

Kilitli dosyalar geri dönüş kaydıyla aynı (7); korunan adaylar 89/89.

**ÜRETİME GEÇİRİLMEDİ.**
