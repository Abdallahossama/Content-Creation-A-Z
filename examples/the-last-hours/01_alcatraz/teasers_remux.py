import sys, subprocess
sys.argv = ["x", "none"]
SRC = open("teasers.py", encoding="utf-8").read()
exec(SRC[: SRC.rindex("if __name__ ==")])
for n in TEASERS:
    audio(n); v = TZ + "TheLastHours_Short_" + n + ".mp4"; o = TZ + "TheLastHours_Short_" + n + "_v2.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", v, "-i", TZ + "build/" + n + ".wav", "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", o], check=True)
    print("ok", o)
