import cv2, numpy as np, mediapipe as mp, sys
cap = cv2.VideoCapture(sys.argv[1]); out = sys.argv[2]; prev = None; n = 0
with mp.solutions.selfie_segmentation.SelfieSegmentation(model_selection=0) as s:
    while True:
        ok, f = cap.read()
        if not ok: break
        m = s.process(cv2.cvtColor(f, cv2.COLOR_BGR2RGB)).segmentation_mask.astype(np.float32)
        prev = m if prev is None else 0.6 * m + 0.4 * prev   # temporal smoothing, less flicker
        mm = np.clip((cv2.GaussianBlur(prev, (0, 0), 2) - 0.35) / 0.3, 0, 1)
        cv2.imwrite(f"{out}/{n:04d}.png", (mm * 255).astype(np.uint8)); n += 1
print("frames", n)
