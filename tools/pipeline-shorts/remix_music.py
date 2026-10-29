"""Re-mix finished Shorts with the louder, ducked music bed (shortkit.mix) and swap the audio into the exports."""
import sys, os, importlib, shutil
sys.path.insert(0, "D:/why habibi/_style_kit/tools")
import shortkit as K
M = "D:/why habibi/_music_library/"
which = sys.argv[1:]
if "s02" in which:
    sys.path.insert(0, "D:/why habibi/_pipeline/shorts/s02_hypnic_jerk"); P = importlib.import_module("post")
    K.mix(P.ROOT + "vo/s02_vo_chatterbox.wav", M + "Dream Culture.mp3", P.SFX, P.END, P.B)
    ex = P.E + "Ask_Habibi_Short02_HypnicJerk.mp4"; old = P.B + "old_quiet_music.mp4"; shutil.copy(ex, old); K.remux(old, P.B + "mix.wav", ex)
if "s03" in which:
    sys.path.insert(0, "D:/why habibi/_pipeline/shorts/s03_france_debt"); R = importlib.import_module("render_s03")
    K.mix(R.VO, M + "Stay the Course.mp3", R.SFX, R.DUR, R.B); R.final()
