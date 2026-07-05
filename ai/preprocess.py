import cv2

def enhance(frame):
    wb = cv2.xphoto.createSimpleWB().balanceWhite(frame)
    # dehaze/CLAHE/bilateral as separate helper functions
    lab = cv2.cvtColor(wb, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l = cv2.createCLAHE(clipLimit=2.0).apply(l)
    merged = cv2.merge((l, a, b))
    out = cv2.cvtColor(merged, cv2.COLOR_LAB2BGR)
    return cv2.bilateralFilter(out, 5, 50, 50)
