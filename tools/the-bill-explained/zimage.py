"""zimage: free local AI images (Z-Image Turbo via stable-diffusion.cpp, Vulkan, AMD Radeon 780M).
No account, no credits. Files live in F:/zimage (bin/ = sd-cli.exe build, models/ = weights).
  python zimage.py out.png "prompt" [W H seed]
  from zimage import gen; gen("prompt", "out.png", 1344, 768, seed=7)
Rules: photo-real only, no women/girls, no brand logos, no readable text (we add text ourselves)."""
import subprocess, sys, os, glob, time

ROOT = "F:/zimage"
NEG_HINT = ", no text, no letters, no watermark, no logo"


def sd_exe():
    c = glob.glob(ROOT + "/bin/**/sd-cli.exe", recursive=True) + glob.glob(ROOT + "/bin/**/sd.exe", recursive=True)
    if not c: raise SystemExit("sd-cli.exe not found under F:/zimage/bin")
    return c[0]


def gen(prompt, out, w=1344, h=768, seed=42, steps=8):
    m = ROOT + "/models/"
    cmd = [sd_exe(), "--diffusion-model", m + "z_image_turbo-Q6_K.gguf", "--vae", m + "ae.safetensors",
           "--llm", m + "Qwen3-4B-Instruct-2507-Q4_K_M.gguf", "-p", prompt + NEG_HINT,
           "--cfg-scale", "1.0", "--steps", str(steps), "-W", str(w), "-H", str(h), "--seed", str(seed),
           "--offload-to-cpu", "--diffusion-fa", "-o", out]
    t = time.time()
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode or not os.path.exists(out):
        print(r.stdout[-2000:], r.stderr[-2000:]); raise SystemExit("zimage failed")
    print(f"{out}  {time.time() - t:.0f}s")
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    gen(a[1], a[0], *(int(x) for x in a[2:4]), **({"seed": int(a[4])} if len(a) > 4 else {}))
