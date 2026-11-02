# CHANGES V2.47 (2026-11-02)

## Üretim davranışı
Değişmedi (= V2.45). `SHM247_WalkOn` 0 (kapalı), `SHM247_WalkDB` = PSD_LB_WalkLoops, `SHM247_EntryWindow` 0,12 — kanca inert.

## Kaydedilen değişiklikler
| Asset | Ne | Durum |
|---|---|---|
| `ABP_GR_MotionMatchingBase` (+child) | Update_MotionMatching: chooser `SetDatabasesToSearch` sonrası dal (Dense ileri döngü seçiliyken bir sonraki arama yalnız `SHM247_WalkDB`), giriş penceresi koşulu | anahtar kapalı; manifestler `v247_abp`, `v247_abp4`; verify ALL_OK |
| V2.46 maliyet izleri (Ranger PureForward +2, beş Dense ileri +6) | kaldırıldı (`SHME_V246_Cost` izleri) | manifestler `v247_rcrm`, `v247_dcrm` |
| `PSD_Dense_Stand_Walk_Loops` | değişmedi (yedekle bayt-aynı, 15 giriş) | "18→15" yanlış alarmdı |

## Araçlar
`install247_walkroute.py`, `install247_walkroute2.py`, `promote247.py` (kullanılmadı), zincirler `run247_a/b/c.sh`; satıcı asset değiştirilmedi.
