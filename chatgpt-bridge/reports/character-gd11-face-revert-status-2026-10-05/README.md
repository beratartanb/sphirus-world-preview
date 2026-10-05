# GD11 — son durum / geri dönüş raporu: K5 yüz varyantı reddedildi, F4ab + h45b + k10 aktif

Tarih: 2026-10-05. Durum: **KULLANICI İNCELEMESİ İÇİN DURDURULDU.** Bu raporda yeni modelleme yok: yeni sculpt, yeni face auto-rig, üretime atama yapılmadı. J raporu (`character-gd11-head-refinement-j-2026-10-05`, commit `49d9f568`) değiştirilmedi.

## 1. Son reddedilen yüz (K5) ve karşılaştırma görsellerinin kaynağı

Kullanıcının gördüğü karşılaştırmalar K çalışma klasöründeki `pv/wip_FO.png` (3 çift: ön, 3/4 R, profil R) ve `pv/wip_FOfc.png` (yalnız K5 yakın planları) idi. Capture kayıtlarına göre:

| Taraf | Capture seti (zaman) | Yüz mesh | DNA | Kaynak / düzeltme katmanı | Nötr durum | Saç + binding |
|---|---|---|---|---|---|---|
| **Başlangıç (sol)** | `g11rjF_h45b_*` (J pası, 03:02, K'dan önce) | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementD_20261004/Face/SKM_G11RD_Face_f4ab` | `.../GD11_HeadRefinementD_20261004/MHC/DNA/MHC_G11RD_F4AB_Head` | D pasının F4ab nötrü (`Saved/Codex/GD11_HeadRefinementD_20261004/head_F4ab.npy`); K'da değiştirilmedi | rig nötr, morph/animasyon yok, çene kapalı | h45b (`.../GD11_HeadRefinementJ_20261005/Hair/GR_LK_Hair_{Main,Loose}_h45b`), bağlamalar `GB_G11RJ_*_f4abh45b` (hedef F4ab) |
| **Reddedilen aday (sağ)** | `g11rkFO_*` / `g11rkFOfc_*` (K zinciri, ~04:40) | `/Game/Sphirus/CharacterLab/GD11_HeadRefinementK_20261005/Face/SKM_G11RK_Face_k5` | `.../GD11_HeadRefinementK_20261005/MHC/DNA/MHC_G11RK_K5_Head` (yeni auto-rig, 858 morph) | `head_F4ab.npy` + `ops/K5.json` (25 yerel op, `blender_gd15_ops.py`) → `head_K5.npy` → MetaHumanCharacter fit (0,020 mm) → auto-rig | rig nötr, morph/animasyon yok | h45b aynı; bağlamalar `GB_G11RK_*_k5h45b` (hedef K5) |

Kamera, ışık (stüdyo), ölçek ve ifade iki tarafta aynı (`*_results.json`: aynı `cam`/`fov`/`light`, `animation: null`). **Dürüst sınır:** capture `results.json` dosyaları kompozisyonu (yüz/groom yolu) kaydetmiyor; eşleme komut günlüklerinden (`data/chainK_h46a_stopped_log.txt`, `data/cycle_k5_log.txt`: `COMP4 … h45b` satırları ve bağlama önekleri) ve binding hedeflerinin editörde okunmasından yapıldı.

**Son denemede gerçekten değişenler (F4ab → K5, `data/ops_K5_rejected.json`, `data/K5_delta_regions.txt`):**
- Çene: mandibula önü/çene gövdesi aşağı (z alanı, −8 mm), çene ucu geri (−5 mm), alt çene önü geri (−2 mm), çene yanları +1 mm, çene köşesi dolgunluğu +3,4 mm, yanal +3,5 mm → ortalama 1,85 mm / en çok 8 mm (çene bölgesi).
- Yanak: elmacık altı dolgu (≤1,5 mm), bukkal dolgunluk +1,1 mm, elmacık öne +1,5 / yana +1,2 mm → ortalama 1,5 mm.
- Ağız: dudaklar birlikte ≤0,9 mm yukarı (burun tabanı grab'inin kenarı); alt dudak altı geçişi +0,5 mm; ağız–çene mesafesi çene inişiyle büyüdü.
- Burun: kolumella/taban +3 mm yukarı, kanatlar +0,9 mm, uç +0,5 mm, sırt yan +0,4 mm.
- Göz çevresi: kaş arası/kaş kemeri öne +2,2 mm, kaş altı +0,7 mm, üst kapak derisi −0,8 mm aşağı / +0,5 mm, göz altı dolgu ≤1 mm. Göz küreleri, kulaklar, kafatası değişmedi.

Kullanıcı okuması: uzamış/öne çıkarılmış çene, sivri alt yüz, oyulmuş yanak, sert/aşağı çekilmiş ağız. Bu değerlendirme kabul edildi; K5 savunulmuyor ve aktif değil.

## 2. Geri dönüşün durumu: YAPILDI (kaynak değiştirilmemişti)

F4ab K çalışmasında hiç değiştirilmedi; K ayrı adaydı. Doğrulama (bu rapordan önce, aynı editör oturumunda):

| Kontrol | Sonuç | Kayıt |
|---|---|---|
| Korunan dosya karşılaştırması (SHA) | **72/72 grup birebir aynı**; D/F4ab grubu 42 dosya, J/h45b grubu 26 dosya dahil | `data/preservation_check.json` |
| Editörde F4ab okuma | `SKM_G11RD_Face_f4ab`: 858 morph; DNA `MHC_G11RD_F4AB_Head`; J bağlamaları h45b/kaş/kirpik groom'larını F4ab'a bağlıyor; kirli paket yok | `data/f4ab_check.json` |
| Aktif kompozisyon (QA config anlık görüntüsü) | face = F4ab; HairMain/HairLoose = h45b + `GB_G11RJ_*_f4abh45b`; kaş/kirpik = `GB_G11RJ_*_f4abh45b`; face ABP = plugin `ABP_Face` | `data/qa_config_active_snapshot.json` |
| Ten / göz | k10 (`gck10`) ve e2; değişmedi (kompozisyon parametreleri) | zincir günlükleri |

Aktif paket: **F4ab yüz + `MHC_G11RD_F4AB_Head` DNA + nötr rig (morph/animasyon yok) + h45b saç (J bağlamaları) + k10 ten.** K bağlamaları (`GB_G11RK_*`) F4ab'a takılmadı.

## 3. Saç çalışması (ayrı saklandı, silinmedi)

- Yeni sürüm **h46a** (`/Game/Sphirus/CharacterLab/GD11_HeadRefinementK_20261005/Hair/GR_LK_Hair_{Main,Loose}_h46a`; kaynak `Saved/Codex/GD11_HeadRefinementK_20261005/hair/h46a`, kopya `SourceAssets/Characters/GD11_HeadK_20261005/hair_h46a`).
- h45b'den farkları (`data/hair_h45b_to_h46a_env_diff.txt`): `SPH_TV_TABLE` ile her tarafta 2 yeni çapraz şakak tutamı (kök 31–44°, alın köşesinden kulak üst arkasına), `SPH_TEMPLE_VEIL` 0,7 → 1,0 (kulak üstü perde kapalı), `SPH_FSF` 1,0 → 1,25, `ear_frame` 150 → 260 (315 → 546 tel), ense kulak arkası yoğunluk 1,45 → 1,8 ve kaldırma 0,16 → 0,22, ense alt tutam 0,22 → 0,40, yama 0,25 → 0,45, yeni `SPH_NFIELD_LIFT_VAR` 0,55 (katmanlı kütle). Oluşturucu K kopyası `blender_g11rk_hair.py` (`SPH_TV_TABLE`, `SPH_NFIELD_LIFT_VAR` eklendi).
- Bağlamalar: `GB_G11RK_*_k5h46a` (hedef K5) ve `GB_G11RK_*_f4abh46a` (hedef F4ab) — ikisi de K klasöründe, aktif değil.
- Yüz karşılaştırmasında saç farkı karıştırılmadı: A, B ve C hep **h45b** ile.
- h46a'nın sanatsal değerlendirmesi yapılmadı (K zinciri durduruldu); yalnız kaynak ve grup teşhisleri saklı.

## 4. Üçlü karşılaştırma (board 00 ve 01)

| | A | B | C |
|---|---|---|---|
| Ne | K yüz çalışmasından önceki gerçek F4ab | Reddedilen K5 | Şu an aktif yüz (F4ab), yeniden çekildi |
| Capture | `g11rjF_h45b_*` (03:02) + yakın plan `g11rkSfc_*` (F4ab, K zincirinde) | `g11rkFO_*` + `g11rkFOfc_*` | `g11rkREV_*` + `g11rkREVfc_*` (red sonrası) |
| Mesh / DNA | F4ab / F4AB | K5 / K5 | F4ab / F4AB |
| Saç / binding | h45b / `GB_G11RJ_*_f4abh45b` | h45b / `GB_G11RK_*_k5h45b` | h45b / `GB_G11RJ_*_f4abh45b` |
| Nötr | rig nötr, animasyon yok | aynı | aynı |

Aynı kameralar (`cam` [0,125,159,−90,0] ön; [−64.468,113.297,160.141,−58,1] 3/4; [−125,3,160,0,0] profil; yakın plan dudak-çene kamerası), aynı stüdyo ışığı, fov 15 / 8. Çene yüksekliği/projeksiyonu, ağız–çene mesafesi, yanak doluluğu ve nötr ifade board'larda görülebilir.

**C = A kanıtı (görsel + kaynak):** aynı mesh (`SKM_G11RD_Face_f4ab`, SHA aynı), aynı DNA (`MHC_G11RD_F4AB_Head`, SHA aynı), aynı bağlamalar (J), aynı nötr durum; piksel farkı (`data/revert_pixel_diff.txt`): ön A–C 0,0044 (saç simülasyonu + TAA gürültüsü) vs B–C 0,0170; 3/4 A–C 0,0036 vs B–C 0,0157; profil A–C 0,0024 vs B–C 0,0124.

## 5. Açık kalan belirsizlikler / notlar

- Capture `results.json` kompozisyonu kaydetmiyor; görüntü–varlık eşlemesi komut günlüğü + binding hedefleri + zaman damgalarıyla yapıldı (yukarıda).
- K zinciri yeniden açılış kontrolünden sonra durduruldu: K5+h46a için "after restart" çekimleri ve LOD mesafe testi yapılmadı; K raporu taslağı yayımlanmadı (yerelde "REDDEDİLDİ" notuyla duruyor).
- Oturum içinde C: diski 1,1 GB boşa düştü ve editör auto-rig sırasında iki kez bellek hatasıyla çöktü; motor `DerivedDataCache`'inin 27 Eylül öncesi girdileri (26,7 GB, yeniden üretilebilir önbellek) silindi, başka dosyaya dokunulmadı. J'nin `data/checkpoint_hashes.json` kaydı K betiği hazırlanırken yanlışlıkla yeniden yazıldı (J'nin korunan asset'leri değişmedi; SHA kontrolünde 26/26).
- Referansa benzerlik hedefi iptal edilmedi; bir sonraki adım için kural: "gömülü göz" ≠ yanak oymak, "çene geçişi" ≠ çene uzatmak, "dengeli yüz" ≠ alt yüzü sivriltmek; küçük (≤~2 mm) yumuşak doku değişiklikleri, dokulu render üzerinde ve aynı A/B/C geri dönüş kanıtıyla.

## Dosyalar

`boards/00_FACE_REVERT_PROOF.jpg` (A/B/C: ön, iki 3/4, iki profil + yüz yakın planları), `boards/01_ABC_COMPACT.jpg`, `data/` (koruma kontrolü, editör okuması, aktif QA config, piksel farkı, reddedilen op JSON'u, bölge deltaları, ölçüm tablosu, saç env farkı, günlükler, reddedilen K5'in referans çerçevesindeki render'ları), `tools/` (kontrol/çekim/ölçüm betikleri).
