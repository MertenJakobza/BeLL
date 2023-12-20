import sys
import time

import numpy
from tqdm import tqdm

import brightness
import convertjson, background, perspective, blur, save
from PIL import Image
import random as rn
import os
import gc

# ursprungsnamen = ["N02", "N03"]

ursprungsnamen = ["M01-Forward", "M02-Backward", "M03-Left", "M04-Right", "S01-Start", "S02-End", "C01-Loop",
                  "C02-Wait", "C03-If", "CF-A", "CF-B", "CF-C",
                  "DF-A", "DF-B", "DF-C", "S04-Return", "W01-Wand", "CF-Sub", "Ziel", "blink",
                  "N01", "N02", "N03", "N04",
                  "N05", "N06", "N07", "N08", "N09", "Not"
                  ]
img_list = [[], []]

ursprung_dir = "ursprung2"
bg_dir = "bg"


def main(anzbilder, anzbackground, img_list, save_b):
    if save_b:
        save.save()

    bounding_list = []
    groesse_bilder = 0
    anteil = 0.1
    bg_size = (512, 512)
    count = 0

    img_height = int(bg_size[0] / 8.5)

    for path in os.listdir("bg"):
        if os.path.isfile(os.path.join("bg", path)):
            count += 1
    # print(count)

    img_list_cv = []

    bg_buffer = [[], []]

    for a in tqdm(range(anzbackground), desc="Hintergründe und Helligkeit: "):
        bounding_list.append([f"bg_fertig{a}.png"])
        ran_bg = rn.randint(0, count - 1)
        # bg = Image.open(f"{bg_dir}/bg{ran_bg}.jpg")

        # Buffern der Hintergründe für bessere Performance
        if ran_bg in bg_buffer[0]:
            bg = bg_buffer[1][bg_buffer[0].index(ran_bg)]
        else:
            bg = Image.open(f"{bg_dir}/bg{ran_bg}.jpg").resize(bg_size)
            bg_buffer[0].append(ran_bg)
            bg_buffer[1].append(bg)

        listecoords = []
        anzbilderran = rn.randint(int(anzbilder / 2), anzbilder)
        if anzbilderran == 0:
            bg_fertig = bg.copy()
        for b in range(anzbilderran):
            pict = rn.choice(ursprungsnamen)

            # Buffern der Blättchen für bessere Performance
            if pict in img_list[0]:
                img = img_list[1][img_list[0].index(pict)]
            else:
                img = Image.open(f"{ursprung_dir}/{pict}.png")
                if not img.height == img_height:
                    img = img.resize((int(img.width / img.height * img_height), img_height), resample=Image.BOX)
                img_list[0].append(pict)
                img_list[1].append(img)

            if b == 0:
                groesse_bilder = rn.randint(img.height + int(-img.height * anteil),
                                            img.height + int(img.height * anteil))
                bg_fertig, coords, size = background.insert(bg.copy(), img, listecoords, groesse_bilder)
            else:
                bg_fertig, coords, size = background.insert(bg_fertig, img, listecoords, groesse_bilder)
            # print(f"Bild Nr. {len(listecoords) + 1} von {anzbilderran} auf Hintergrund geladen.")
            listecoords.append([coords[0], coords[1], coords[0] + size[0], coords[1] + size[1]])
            bounding_list[a].append([pict, coords[0], coords[1], coords[0] + size[0], coords[1] + size[1]])
        # print(listecoords)
        # bg_fertig.save(f"zwischen/bg_fertig{a}.png", "PNG")
        bg_fertig = brightness.brightness(bg_fertig)
        img_list_cv.append(numpy.array(bg_fertig)[:, :, ::-1].copy())

        del bg_fertig
        gc.collect()
        # print(f"Hintergrund Nr. {a + 1} fertig.")
    # print("\n\n")
    # print(bounding_list)
    # bounding_list_verzerrung, img_list = perspective.verzeerung(anzbackground, bounding_list)
    print("\033[92mHintergründe und Helligkeit fertig!\033[0m")
    time.sleep(0.1)
    bounding_list_verzerrung, img_list = perspective.verzeerung(img_list_cv, bounding_list)

    del img_list_cv
    gc.collect()
    print("\033[92mVerzerrung fertig!\033[0m")
    time.sleep(0.1)
    blur.blur(img_list)

    del img_list
    gc.collect()
    # 512x512
    # Ohne garbage Collection: 3GB
    # Mit Garbage Collection: 2GB
    # 1200x1200
    # Ohne: 14GB
    # Mit: 5GB
    print("\033[92mUnschärfe fertig!\033[0m")
    time.sleep(0.1)
    print("\033[92mBounding-Box Liste fertig.\033[0m")

    convertjson.convert_to_json(bounding_list_verzerrung, bg_size)


def help():
    print("Arguments:\nnum_Blättchen_pro_Bild num_Bilder [aktuelle_Bilder_speichern] ")


if __name__ == '__main__':
    save_b = True
    argv = sys.argv
    if argv[1:] == []:
        eingabe = int(input("Die Anzahl der Eingabe-Bilder pro Bild eingeben: "))
        eingabe2 = int(input("Die Anzahl der zu generierenden Bilder eingeben: "))
    else:
        if len(argv) < 3:
            help()
            sys.exit(1)
        elif len(argv) == 4:
            if int(argv[3]) == 0:
                save_b = False
            elif int(argv[3]) == 1:
                save_b = True
            else:
                help()
                sys.exit(1)
        eingabe = int(sys.argv[1])
        eingabe2 = int(sys.argv[2])

    if len(argv) == 3 or len(argv) == 1:
        num_files = len(next(os.walk("fertig"))[2])

        if not num_files == 0:
            eingabe3 = input("Sollen die bisherigen Daten in Dauer verschoben werden? [Y] ")
            if eingabe3 == "Y" or eingabe3 == "y":
                save_b = True
            else:
                if os.path.exists("fertig/bounding_boxes.labels"):
                    os.remove("fertig/bounding_boxes.labels")
                for i in range(num_files):
                    if os.path.exists(f"fertig/fertig{i}.png"):
                        os.remove(f"fertig/fertig{i}.png")
                save_b = False
        else:
            save_b = False

    main(eingabe, eingabe2, img_list, save_b)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
