# GD11 geri dönüş: burun ve kaş M'ye (m2 + M_SlightArch), saç korundu

Tarih: 2026-10-06. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Üretime atama yok, eski raporların üzerine yazılmadı. Yeni sculpt, auto-rig ya da kaş tasarımı yapılmadı.

## Geri getirilen paket (M, `b02afe39`)

| Parça | Varlık |
|---|---|
| Yüz | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementM_20261005/Face/SKM_G11RM_Face_m2` |
| DNA | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementM_20261005/MHC/DNA/MHC_G11RM_M2_Head` |
| Kaş | `GR_GD_Eyebrows_M_SlightArch` + `GB_G11RM_EyebrowsM_SlightArch_m2h48a` (hedef m2) + materyaller `MI_Hair` / `MI_Facial_Hair` (M kaydıyla aynı) |
| Kirpik | `GR_GD_Eyelashes_S_Thin` + `GB_G11RM_EyelashesS_Thin_m2h48a` |
| Ten / göz | k10 / e2 |

Dosya SHA1 değerleri ve editörden okunan kompozisyon `data/revert_record.json` dosyasında. Kayıt diskten yeniden okunarak doğrulandı.

## Saç

En son saç **h51a korundu**, yeniden üretilmedi (`GD11_HeadRefinementO_20261005/Hair/GR_LK_Hair_{Main,Loose}_h51a`). m2'yi hedefleyen bir h51a bağlaması yoktu. Bu yüzden yalnız iki bağlama, ayrı aday klasöründe oluşturuldu. Yüz rig'i çalıştırılmadı.

- `/Game/Sphirus/CharacterLab/GD11_RevertM_20261006/Face/Bindings/GB_G11RV_HairMain_m2h51a`
- `/Game/Sphirus/CharacterLab/GD11_RevertM_20261006/Face/Bindings/GB_G11RV_HairLoose_m2h51a`

Her ikisinin hedefi m2, kaynağı M/N/O bağlamalarıyla aynı P yüzü. Build verisiyle yeniden kaydedildiler (7,4 KB). h48a yalnız M kaynağını göstermek için kullanıldı.

## Doğrulama

- **Burun dışında beklenmeyen değişiklik yok** (`data/heat_m2_vs_o6.txt`). o6 ile m2 farkı dudak, çene, yanak, kulak ve kafatasında 0,00 mm. Göz kapağı ve kök bandındaki 0,27–0,36 mm, N'nin burun kökü yan oplarının kenar yayılması. Bu yüzden m2 paketinin kendisi kullanıldı.
- **Nötr durum:** çene, gözler, göz kapakları, kaş, dudak ve burun kemikleri referans pozda (konum ve döndürme farkı 0). ABP_Face aktif, animasyon yok (`prov/g11rvRV_pose.json`). NasolabialBulge1 satırı okuma hatasıdır: soket çözülmüyor, iki durumda da aynı.
- **Karşılaştırma koşulları:** M kaynağı ve geri dönüş aynı editör oturumunda, aynı kamera ve stüdyo ışığında, kurulumda sıfırlanan simülasyonla ve time=0 ile çekildi.
- **Kısa hareket kontrolü** (yeni bağlamalar için 6 kare, `data/motion_check.jpg`): saç başla birlikte hareket ediyor, kök kopması ve kesişme yok.

## Pano

`boards/GD11_REVERT_M.jpg`. Satır 1–2 saç gizli: M kaynağı ile geri dönüş, yüz ve kaş birebir aynı. Satır 3–4 saçlı: M kaynağı (h48a) ile geri dönüş (h51a). Görünümler: ön, 3/4 sağ, profil, yakın ön ve yakın 3/4.

## Bildirilen sorun (geri dönüşle ilgisiz)

O turundaki durdurulmuş bir o6 rig zincirinin zombi kabuğu, O zinciri bittikten sonra 2026-10-05 23:34'te iki iş kuyruğa attı. Yüz kurulumu işi `SKM_G11RO_Face_o6` dosyasını sildi. DNA bağlama işi ise editörü çökertti (RigLogicEditor erişim hatası). Bu yüzden reddedilen O kaydının o6 mesh'i diskte yok ve `GB_G11RO_*_o6h51a` bağlamalarının hedefi boş. o6 kaynakları duruyor: `MHC_G11RO_O6` karakteri, `MHC_G11RO_O6_Head` DNA'sı, .dna dosyası ve `head_O6.npy`. Mesh bunlardan yeni auto-rig olmadan yeniden dışa aktarılabilir. Kapsam dışı olduğu için yapılmadı. Korunan M, N, L, K ve J kaynakları sağlam (89/89).
