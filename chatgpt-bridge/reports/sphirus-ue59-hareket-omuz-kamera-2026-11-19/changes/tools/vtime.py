# vtime.py (Blender background): -- <out.txt> <video.mp4> [rec.json] ... : per video: encoded fps, frame count, duration; with the
# recorder json: simulated duration (last t - first t), data/sim step, captured frame count -> REAL_SPEED / SLOW xN / FAST xN.
import bpy, sys, json, os
a = sys.argv[sys.argv.index('--') + 1:]; out = a[0]; pairs = a[1:]; rows = []
sc = bpy.context.scene; sc.sequence_editor_create(); S = sc.sequence_editor.strips if hasattr(sc.sequence_editor, 'strips') else sc.sequence_editor.sequences
for i in range(0, len(pairs), 2):
    v, j = pairs[i], pairs[i + 1]
    m = S.new_movie(name='m%d' % i, filepath=v, channel=1 + i, frame_start=1); fps = float(m.fps); n = m.frame_final_duration; dur = n / fps
    line = '%s: video %d frames @ %.2f fps = %.2f s' % (os.path.basename(v), n, fps, dur)
    if j != '-':
        d = json.load(open(j)); R = d['rows']; sim = R[-1]['t'] - R[0]['t'] + (R[1]['t'] - R[0]['t']); step = R[1]['t'] - R[0]['t']
        k = dur / sim
        line += ' | sim %.2f s step %.4f s (%.0f Hz) rows %d | %s' % (sim, step, 1 / step, len(R), 'REAL_SPEED' if abs(k - 1) < 0.03 else ('SLOW x%.2f' % k if k > 1 else 'FAST x%.2f' % (1 / k)))
    rows.append(line)
open(out, 'w').write('\n'.join(rows) + '\n')
