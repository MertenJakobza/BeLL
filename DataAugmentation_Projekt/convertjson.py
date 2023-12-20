import json


def convert_to_json(bounding_list, bg_size):
    # Eine Liste von Bildern, bestehend aus Liste von Labels, welche einen Namen eine x und y Koordinate und eine Höhe und Breite haben
    # test = [["test.jpg", ["label1", 100, 100, 120, 112],["label2", 132, 254, 300, 298]], ["test2.jpg", ["label1", 100, 100, 120, 112],["label2", 132, 254, 300, 298]]]

    # list = test

    # print(list)

    dictionary = {
        "version": 1,
        "type": "bounding-box-labels",
        "boundingBoxes": {
        }
    }

    dictionaryBilder = {}

    fehler = []

    max_nicht_sichtbar = 0.45

    for a in range(len(bounding_list)):
        dictionaryBilder[bounding_list[a][0]] = []
        for b in range(1, len(bounding_list[a])):
            label = bounding_list[a][b]
            if label[1] + max_nicht_sichtbar * (label[3] - label[1]) < 0 \
                    or label[2] + max_nicht_sichtbar * (label[4] - label[2]) < 0 \
                    or label[1] > bg_size[0] \
                    or label[2] > bg_size[1] \
                    or label[3] - ((1 - max_nicht_sichtbar) * (label[3] - label[1])) > bg_size[0] \
                    or label[4] - ((1 - max_nicht_sichtbar) * (label[4] - label[2])) > bg_size[1]:
                fehler.append(bounding_list[a][0])
                continue
            # print(label)
            dictionaryLabel = {"label": label[0], "x": label[1], "y": label[2], "width": label[3] - label[1],
                               "height": label[4] - label[2]}
            dictionaryBilder[bounding_list[a][0]].append(dictionaryLabel)

        if dictionaryBilder[bounding_list[a][0]] == []:
            print(
                f"\033[93mWarning: Das Bild {bounding_list[a][0]} ist leer. Bitte manuell überprüfen und eventuell "
                f"löschen!\033[0m")

    dictionary["boundingBoxes"] = dictionaryBilder
    print(
        f'\033[92mAlle Bounding-Boxen auf Fehler überprüft.\033[0m '
        f'\033[93mEs wurden {len(fehler)} Fehler gefunden.\033[0m')
    # print(dictionary)

    if not len(fehler) == 0 and input("Fehler anzeigen? [Y] ") == "Y":
        print(fehler)

    with open("fertig/bounding_boxes.labels", "w") as outfile:
        json.dump(dictionary, outfile, indent=4)
        print("\033[92mJSON-Datei generiert.\033[0m")
        # print(outfile)
