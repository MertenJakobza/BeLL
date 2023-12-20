import random as rn
import PIL
from PIL import Image


def insert(background: PIL.Image.Image, image: PIL.Image.Image, listecoords, height):
    # print(f"Koordinaten-Liste: {listecoords}")
    stop = False
    while (not stop):
        stop = True
        ratio = image.width / image.height

        # anteil = 0.1
        # rand = rn.randint(int(-image.width * anteil), int(image.width * anteil))

        img = image.resize((int(height * ratio), height), resample=Image.BOX)
        # Etwas gegen Überschneidungen
        coords = (rn.randint(0, background.width - img.width), rn.randint(0, background.height - img.height))

        points = [coords,
                  (coords[0] + img.width, coords[1]),
                  (coords[0], coords[1] + img.height),
                  (coords[0] + img.width, coords[1] + img.height),
                  (int((2 * coords[0] + img.width) / 2), int((2 * coords[1] + img.height) / 2)),
                  (int((2 * coords[0] + img.width) / 2), coords[1]),
                  # Seitenhalbierenden, theoretisch noch deutlich mehr nötig, jedoch praktisch nicht
                  (coords[0], int((2 * coords[1] + img.height) / 2)),
                  (int((2 * coords[0] + img.width) / 2), coords[1] + img.height),
                  (coords[0] + img.width, int((2 * coords[1] + img.height) / 2))
                  ]
        # print(points)
        # print(durchgaenge, points[0])

        if not listecoords == []:
            for a in range(len(points)):
                if (stop):
                    for b in range(len(listecoords)):
                        if points[a][0] >= listecoords[b][0] and points[a][0] <= listecoords[b][2]:
                            # print("X-Wert liegt im Bereich")
                            # print(points[a], listecoords[b])
                            if points[a][1] >= listecoords[b][1] and points[a][1] <= listecoords[b][3]:
                                # print("Y-Wert liegt auch im Bereich")
                                # print(points[a], listecoords[b])
                                # print("Box liegt innerhalb einer Anderen. Sie wird neu generiert...")
                                stop = False

    background.paste(img, coords, img)
    return background, coords, img.size
