# cmap.py (PIE prelude data): profile C 'Sphirus Curated' = GASP Normal walk + run locomotion families, Relaxed idle / sprint /
# stops-from-sprint / lands / traversal / crouch. Uses the existing SphCM remap in ABP_Sph_GASP (keys = Relaxed DB, vals = Dense DB).
import builtins
R_ = '/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Relaxed/PSD_Relaxed_Stand_'
D_ = '/Game/Characters/UEFN_Mannequin/Animations/MotionMatchingData/Databases/Dense/PSD_Dense_Stand_'
m_ = {}
for g_ in getattr(builtins, 'C_GAITS', ('Walk', 'Run')):
    for d_ in ('F', 'B', 'LL', 'RL'):
        for k_, v_ in (('Loops', 'Loops'), ('Pivots', 'Pivots'), ('Starts', 'Starts'), ('Spins', 'SpinTransition')):
            m_[R_ + '%s_%s_%s' % (g_, d_, k_)] = D_ + '%s_%s' % (g_, v_)
    m_[R_ + '%s_F_Turns' % g_] = D_ + '%s_Pivots' % g_
    m_[R_ + '%s_Stops' % g_] = D_ + '%s_Stops' % g_
builtins.SPH_MAP = m_
builtins.SPH_SPEEDS = getattr(builtins, 'C_SPEEDS', ((180, 170, 150), (430, 350, 300), (585, 585, 585)))
# C_FWD (2026-11-16 hip-swing fix): forward databases use the forward-only Sphirus Normal sets (no strafe loops / arcs / strafe pivots).
#   1 = F_Loops only, 2 = F_Loops + F_Turns + F_Pivots + F_Starts
F_ = int(getattr(builtins, 'C_FWD', 0) or 0); N_ = '/Game/Sphirus/Player/GASP/DB/PSD_Sph_N_'
for g_ in getattr(builtins, 'C_GAITS', ('Walk', 'Run')):
    for k_ in (('Loops',) if F_ == 1 else ('Loops', 'Turns', 'Pivots', 'Starts') if F_ >= 2 else ()):
        m_[R_ + '%s_F_%s' % (g_, k_)] = N_ + '%s_F_%s' % (g_, k_)
builtins.SPH_MAP = m_
# C_FWD 3 = as 2, but jog turns / pivots stay on the Relaxed clips (Neutral run turns measured 12-14 cm lateral pelvis throw at 90 deg, Relaxed 7-9)
if F_ == 3:
    for k_ in ('Turns', 'Pivots'): m_.pop(R_ + 'Run_F_' + k_, None)
    builtins.SPH_MAP = m_
# C_STOP 1 (2026-11-17): sprint-stop database -> Sphirus combined sprint + forward run stops, so a 430 jog stop can pick a run stop
if int(getattr(builtins, 'C_STOP', 0) or 0) == 1:
    m_[R_ + 'Sprint_Stops'] = '/Game/Sphirus/Player/GASP/DB/PSD_Sph_SprintJog_Stops'; builtins.SPH_MAP = m_
