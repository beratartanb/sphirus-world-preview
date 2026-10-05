# GD11 durum notu: eski O/o6 işlerinin yeniden çalışması engellendi

Tarih: 2026-10-06 00:55. Önceki kayıt: `character-gd11-revert-to-m-2026-10-06` (`fbe2fad7`), değiştirilmedi. Yeni modelleme, auto-rig, kurulum ve üretime atama yok.

## Eski O/o6 süreci veya bekleyen iş bulundu mu?

- **Çalışan süreç: bulunmadı.** Süreç listesinde yalnız 00:31'de açılan editör ve bu kontrolün kendi kabukları var (`data/procs_before.txt`). O zincirine ait bash, bekleme, Blender ya da Python süreci yok. Zombi kabuk, son işini 2026-10-05 23:50'de gönderdikten sonra kendiliğinden bitmiş.
- **Canlı kuyruk: bekleyen iş yok** (`data/jobs_before.txt`). Editör koşucusu yalnız `jobs/*.py` dosyalarını çalıştırır.
- **Karantinada çalışmamış 8 eski iş bulundu** (`data/stale_o6.txt`). Aralarında o6 DNA bağlama, o6 rig, o6 groom bağlama ve h51a groom'unu yeniden içe aktaracak iş vardı. Karantina klasörü taranmıyor, yani kendiliğinden çalışamazlardı.
- Zamanlanmış görev ya da otomatik yeniden deneme kaydı bulunmadı.

## Ne durduruldu?

1. Karantinadaki 8 çalışmamış iş `.py.cancelled_20261006` olarak yeniden adlandırıldı (`data/cancelled_jobs.txt`). Dosyalar silinmedi, kanıt duruyor.
2. Olayın kaynağı olan `gd11ro_cycle.sh` kapatıldı. Betik artık hiçbir iş göndermeden çıkıyor (çalıştırılarak doğrulandı, çıkış kodu 3). Asıl mekanizma şuydu: rig beklemesi zaman aşımına uğrayınca betik durmadan sonraki adımlara devam ediyordu.
3. `ue_g11ro_face_setup.py` içine tek satırlık koruma eklendi. Dışa aktarım kaynağı yoksa mevcut yüz mesh'ini silmeyi reddediyor.

Değişiklik öncesi iki betiğin kopyası `Saved/Codex/GD11_RevertM_20261006/guard/` altında.

## Son kontrol

İptalden sonra süreçler ve kuyruk yeniden okundu (`data/procs_after.txt`): eski süreç yok, canlı kuyrukta bekleyen iş yok, karantinada O oturumundan çalıştırılabilir iş kalmadı.

## Paket değişmeden kaldı mı?

**Evet.** 13 dosyanın SHA1 değeri işlem öncesi ve sonrası aynı (`data/hashes_before.json`, `data/hashes_after.json`). Yüz, DNA, kaş, kaş ve kirpik bağlamaları ile h51a groom'ları geri dönüş kaydındaki değerlerle de aynı. İki yeni saç bağlamasının özeti kayıttakinden farklı: kayıt, 00:40'taki build verili yeniden kayıttan önce yazılmıştı.

Açık editörden okunan durum (`data/editor_read.json`):

| Parça | Okunan |
|---|---|
| Yüz / DNA | `SKM_G11RM_Face_m2` / `MHC_G11RM_M2_Head`, 858 morph |
| Kaş | `GR_GD_Eyebrows_M_SlightArch`, bağlama hedefi m2, materyaller `MI_Hair` + `MI_Facial_Hair` |
| Saç | `GR_LK_Hair_{Main,Loose}_h51a`, `GB_G11RV_Hair{Main,Loose}_m2h51a`, ikisinin hedefi m2 |
| Kirli paket | yok |

Aktif kompozisyon o6'ya ya da o6 bağlamalarına dayanmıyor. Korunan eski adaylar 89/89 aynı. O klasörü silinmedi, taşınmadı.

## Açık kalanlar

- `SKM_G11RO_Face_o6` diskte yok ve `GB_G11RO_*_o6h51a` bağlamalarının hedefi boş. Bilerek yeniden üretilmedi. o6 kaynakları (MHC karakteri, DNA, .dna, `head_O6.npy`) duruyor.
- Doğrulanamayan alan: başka cihazlardaki ya da buluttaki Claude oturumları ve bu makinede o an kapalı olan terminaller görülemez. Yerelde böyle bir süreç yoktu.
- Kapatılan betik yalnız O turunun zinciridir. Daha eski turların benzer betikleri aynı zayıflığı taşıyabilir. Hiçbiri çalışmıyor, dokunulmadı.
