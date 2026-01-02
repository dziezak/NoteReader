import cv2
import numpy as np

def resize_with_padding(img, target_size=(128,128), bg_color=255):
    h, w = img.shape[:2]
    th, tw = target_size

    scale = min(tw / w, th / h)
    new_w = int(w * scale)
    new_h = int(h * scale)

    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

    canvas = np.ones((th, tw), dtype=np.uint8) * bg_color

    x_offset = (tw - new_w) // 2
    y_offset = (th - new_h) // 2

    canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
    return canvas
