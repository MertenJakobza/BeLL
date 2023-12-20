import os
import shutil, json


def save():
    num_files = len(next(os.walk("fertig"))[2])

    num_dir = len(next(os.walk("dauer"))[1])
    if not num_dir == 0:
        num = max([int(x) for x in next(os.walk("dauer"))[1]]) + 1
    else:
        num = 0

    dictionary = json.load(open("fertig/bounding_boxes.labels"))

    dictionaryneu = {
        "version": 1,
        "type": "bounding-box-labels",
        "boundingBoxes": {
        }
    }
    dictionaryBilderneu = {}

    for i in range(num_files - 1):
        dictionaryBilderneu[f"{num}fertig{i}.png"] = dictionary["boundingBoxes"][f"fertig{i}.png"]
    dictionaryneu["boundingBoxes"] = dictionaryBilderneu

    with open("fertig/bounding_boxes.labels", "w") as outfile:
        json.dump(dictionaryneu, outfile, indent=4)

    # Überarbeiten der JSON-Datei, weil damit in der JSON-Datei noch die alte Version der Bildnamen enthalten ist

    dauerdir = str(num)
    parent_dir = "dauer"

    os.mkdir(os.path.join(parent_dir, dauerdir))

    source = "fertig/"
    destination = f"dauer/{num}/"
    for i in range(num_files - 1):
        source_file = source + f"fertig{i}.png"
        destination_file = destination + f"{num}fertig{i}.png"
        shutil.move(source_file, destination_file)
    # print(os.path.join(parent_dir, dauerdir))

    shutil.move("fertig/bounding_boxes.labels", f"dauer/{num}/bounding_boxes.labels")

    print("Die Daten wurden gespeichert.")


if __name__ == '__main__':
    save()
