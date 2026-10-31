"""xr2_labels.py <out.json>: Turkish place / decision labels of the XR2 masterplan for label_map.ps1 (world cm)."""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import xr2_layout as LY
L = [['EV (sığınak)', [300, 300], [120, 40, 0]], ['Veranda', [700, 1450], [120, 40, 0]],
     ['İSKELE (göl kenarı)', [-200, 2350], [0, 70, 160]], ['A: GÖL YOLU', [2750, 3600], [0, 70, 160]], ['Taş sekisi (sıkışma)', [2750, 4900], [0, 70, 160]],
     ['Dere geçidi', [2000, 7150], [0, 70, 160]], ['Kuru dere cebi', [3300, 7600], [0, 110, 50]], ['KARŞI KIYI AÇIKLIĞI', [-2200, 8900], [0, 70, 160]],
     ['Sazlık (zor iz)', [-4700, 5200], [90, 90, 160]], ['B: SIRT PATİKASI', [2950, 300], [170, 0, 90]], ['Bahçe kapısı', [2750, -250], [170, 0, 90]],
     ['Kaya boğazı', [3100, -1950], [170, 0, 90]], ['Çukur geçişi', [2350, -3300], [170, 0, 90]], ['Tırmanış', [1850, -4800], [170, 0, 90]],
     ['SIRT AÇIKLIĞI', [800, -6550], [170, 0, 90]], ['Doğu koyu cebi', [3700, -1300], [0, 110, 50]], ['Eski kesim açıklığı', [-2700, -350], [0, 110, 50]],
     ['Ana koru', [400, -2700], [0, 90, 0]], ['Bahçe şevi', [-300, -1950], [150, 0, 0]], ['Vadi duvarı (kaya)', [-2600, -3300], [150, 0, 0]],
     ['DÜNYA SINIRI: şev + kaya + devrik', [-5600, -1800], [150, 0, 0]], ['Sığ su sınırı', [-1600, 5300], [0, 120, 140]]]
for nm, (p, f) in LY.DECISIONS.items():
    L.append([nm.split('_')[0], [p[0] + 120, p[1] - 220], [0, 0, 0]])
json.dump(L, open(sys.argv[1], 'w'), ensure_ascii=False)
