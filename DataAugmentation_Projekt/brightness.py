import random

from PIL import ImageEnhance


def brightness(img):
    enhancerb = ImageEnhance.Brightness(img)

    ranb = random.randint(80, 120)
    factorb = ranb / 100
    enhanced_img = enhancerb.enhance(factorb)

    enhancerc = ImageEnhance.Contrast(enhanced_img)
    ranc = random.randint(80, 120)
    factorc = ranc / 100
    enhanced_img2 = enhancerc.enhance(factorc)

    return enhanced_img2
