import math
import random as rn
import cv2 as cv
from tqdm import tqdm


def blur(img_list):
    wahrscheinlichkeit_blur = 20
    for a in tqdm(range(len(img_list)), desc="Unschärfe: "):
        img = img_list[a]
        rows, cols, ch = img.shape
        if rn.randint(0, 100) <= wahrscheinlichkeit_blur:
            rand = rn.randint(math.ceil(rows / 400), int(rows / 80))
            img = cv.blur(img, (rand, rand))
            # print(f"Bild Nr. {a + 1} um {rand} geblurred.")
        # else:
        # print(f"Bild Nr. {a + 1} nicht geblurred.")
        cv.imwrite(f"fertig/fertig{a}.png", img)
