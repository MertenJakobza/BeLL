import pickle
import time

from PyQt5.QtWidgets import QMessageBox


def print_list(labyrinth):
    for a in labyrinth:
        print(a)


def find_path(labyrinth):
    machbar = False
    labyrinth_path = labyrinth.copy()

    # testen, ob das Labyrinth vor und nach einem Schritt gleich ist, dann nicht machbar

    for a in range(len(labyrinth_path)):
        for b in range(len(labyrinth_path[a])):
            if labyrinth_path[a][b] == 2:
                for c, d in [[0, -1], [0, 1], [-1, 0], [1, 0]]:
                    if labyrinth_path[a + c][b + d] == 0:
                        labyrinth_path[a + c][b + d] = 4

    # 4... da war ich schon einmal
    # 5... da war ich lange nicht mehr
    durchgaenge = 0
    weg = 0
    while True:
        anz_frisch = 0
        coords_4 = []
        for a in range(len(labyrinth_path)):
            for b in range(len(labyrinth_path[a])):
                if labyrinth_path[a][b] == 4:
                    coords_4.append((a, b))
        for a in coords_4:
            for c, d in [[0, -1], [0, 1], [-1, 0], [1, 0]]:
                if labyrinth_path[a[0] + c][a[1] + d] == 3:
                    machbar = True
                    weg = durchgaenge + 2
                if labyrinth_path[a[0] + c][a[1] + d] == 0:
                    labyrinth_path[a[0] + c][a[1] + d] = 4
            labyrinth_path[a[0]][a[1]] = 5

        for a in range(len(labyrinth_path)):
            for b in range(len(labyrinth_path[a])):
                if labyrinth_path[a][b] == 4:
                    anz_frisch += 1

        if machbar or anz_frisch == 0:
            break
        durchgaenge += 1
        # input("Eingabe vom Nutzer: ")
    dialog = QMessageBox()

    if machbar:
        dialog.setIcon(QMessageBox.Information)
        dialog.setWindowTitle("Information")
        dialog.setText(
            f"Der schnellste Weg ist {weg} Schritte lang!")
        dialog.exec()
        # print(f"Das Labyrinth hat mindestens {len(wege)} mögliche Wege! Der schnellste Weg ist {min(wege)} lang!")
    else:
        dialog.setIcon(QMessageBox.Critical)
        dialog.setWindowTitle("Nicht machbar!")
        dialog.setText(
            "Das Labyrinth ist nicht machbar!")
        dialog.exec()
        # print("Das Labyrinth ist nicht machbar!")

    return machbar


if __name__ == '__main__':
    start = time.time()
    labyrinth = pickle.load(open("saved_Layouts/1.dat", "rb"))
    for a in labyrinth:
        print(a)
    find_path(labyrinth)
    # print(f"Benötigte Zeit: {time.time() - start}")
