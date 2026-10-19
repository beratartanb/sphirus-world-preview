# V2.16 oyun içi kontrol listesi (senin kabulün için)

Harita `L_GR_SphirusHouse`, normal PIE, oyun kamerası. Her maddeyi her iki yöne en az 3 kez dene; "evet / hayır / nerede" not et.

## Üretimde olan (Hedef 1)
1. **Shift+W depar → D (sağ kesiş) → 0.3 s sonra A (sola ters, ileri koşmaya devam).** Ters istekte gövde yeni yöne dönüp ileri
   hızlanmalı; basılı ayak yerde süpürülmemeli, ayak zemine batmamalı. Bilinen kalan: dönüşün ilk adımında sağ ayak bir kez kısa kayabilir.
2. Aynası: depar → A → D. Bilinen kalan: depar döngüsüne dönerken sol ayak kayabilir (ölçümde 42–49 cm) — bunu özellikle bak.
3. **Çok erken** (D'den hemen sonra A) ve **geç** (kesiş bitince A) ters istekler.
4. **Depar → D → S (geri):** kesiş derin çömelme / büyük öne eğilme olmadan frenlemeli; S'de geri gidiş korunmalı.
   Bilinen kalan: geri koşuya geçişte ayak kayması 3 koşunun 2'sinde ölçüldü (V2.14'te de vardı).
5. **Hızlı S-kesişler** (D, A, D …): ikinci kesişte pelvis düşüşü (ölçüm 71.9 cm) hâlâ fazla mı?
6. Kesiş sırasında tuşu bırakma, itiş bitmeden ikinci yön değişimi.

Genel his: omuz/kollar rahat mı, adımlar ölçülü mü, geniş yanal açılma var mı, ağırlık aktarımı görünüyor mu?

7. **Yürüyüş → Shift (Hedef 2, üretimde):** yürürken farklı anlarda Shift'e bas. Adımlar hızla birlikte sıklaşmalı (yarım saniye
   yürüme ritminde kalmamalı), basılı ayak kaymamalı, kollar içe kapanmamalı; kısa Shift dokunuşlarında ikinci kalkış olmamalı.
   Bilinen: "standart" ve "yarım adım sonra" zamanlamasında giriş teması V2.15'ten biraz kötü ölçüldü. Beğenmezsen geri alma:
   ABP `SHM211_DB_Push` ve `SHM214_DB_GaitPush` = `PSD_SHM215_WalkPush`.

## Üretimde OLMAYAN aday (istersen dene, kayıt `pub/vid/tiprev_candidate_diag.*`)
- **Yerinde dönüş başlangıcı**: `Saved/Codex/SHME_V216_20261018/checkpoint/tipstart_candidate/` (editör kapalıyken
  `Content/GraceRanger/SHME/Animations/Turns/` üzerine kopyalanır; geri: `baseline_v215/clips/SHME/Animations/Turns/`).

## Bildirirken
Senaryo, yön, kaçıncı deneme, "kayma / batma / çömelme / gecikme / ikinci kalkış" hangisi; mümkünse ekran kaydı saniyesi.
