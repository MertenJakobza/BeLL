import os
from pickle import dump, load

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QPushButton, QMessageBox, QMainWindow, QLabel

from GUI.editor import Ui_WLabyrinthEditor
from GUI.mainwindow import Ui_WMainWindow
from path_finding import find_path

labyrinth = []
buttonliste = []
labelliste = []
classified = False


class mybutton(QPushButton):
    posx = 0
    posy = 0
    height = 0
    width = 0
    value = 0

    colors = [[0, "darkgrey"], [1, "grey"], [2, "green"], [3, "yellow"]]

    def __init__(self, posx, posy, width, height, editorwin: QMainWindow, px, py):
        QPushButton.__init__(self, editorwin)
        self.posx = posx
        self.posy = posy
        self.height = height
        self.width = width
        self.setGeometry(px, py, width, height)
        self.setStyleSheet(f"background-color: darkgrey")
        self.show()
        self.clicked.connect(lambda: self.anpassen())

    def anpassen(self):
        # print(self.posx, self.posy)
        if self.value == 3:
            self.value = 0
        else:
            self.value += 1
        self.update_color()

    def update_color(self):
        for i in self.colors:
            if i[0] == self.value:
                self.setStyleSheet(f"background-color: {i[1]}")
                break


class mylabel(QLabel):
    posx = 0
    posy = 0
    height = 0
    width = 0
    value = 0

    # 0...Nichts
    # 1...Wand
    # 2...Start
    # 3...Ziel

    colors = ["darkgrey", "grey", "green", "yellow", "", "orange", ""]

    def __init__(self, posx, posy, width, height, editorwin: QMainWindow, px, py, color):
        QLabel.__init__(self, editorwin)
        self.posx = posx
        self.posy = posy
        self.height = height
        self.width = width
        self.setGeometry(px, py, width, height)
        self.value = color
        self.update_color()
        self.show()

    def update_color(self):
        self.setStyleSheet(f"background-color: {self.colors[self.value]}")

    def set_image(self, img_dir, scale_by_height):
        pixmap = QPixmap(img_dir)
        if scale_by_height:
            self.setPixmap(pixmap.scaledToHeight(self.height))
        else:
            self.setPixmap(pixmap.scaledToWidth(self.height))


def set_labyrinth(labyrinth_neu):
    global labyrinth
    labyrinth = labyrinth_neu


def get_labyrinth():
    global labyrinth
    return labyrinth


def set_classified(classified_neu):
    global classified
    classified = classified_neu


def display_labyrinth(editui: Ui_WLabyrinthEditor, editorwin: QMainWindow):
    global buttonliste, labyrinth

    if not buttonliste == []:
        for a in buttonliste:
            for button in a:
                button.deleteLater()

    width = len(labyrinth) - 2
    height = len(labyrinth[0]) - 2
    buttonliste = [[0 for y in range(height)] for x in range(width)]
    # print(editorwin.width(), editui.Bcancel.x())

    y_offset = 30

    anfangspunkt = (5, editui.Bcancel.y() + editui.Bcancel.height() + y_offset + 5)
    bwidth = int((editorwin.width() - 2 * anfangspunkt[0]) / width)
    bheight = int((editorwin.height() - anfangspunkt[1]) / height)

    for a in range(width):
        for b in range(height):
            button: mybutton = mybutton(a, b, bwidth, bheight, editorwin, a * bwidth + anfangspunkt[0],
                                        b * bheight + anfangspunkt[1])
            buttonliste[a][b] = button

    for a in range(1, width + 1):
        for b in range(1, height + 1):
            buttonliste[a - 1][b - 1].value = labyrinth[a][b]
            buttonliste[a - 1][b - 1].update_color()


def update_Labyrinth_farben(labyrinth_neu, roboterx, robotery, richtung, fertig):
    global labelliste
    anfang = False
    if labyrinth_neu[roboterx][robotery] == 2:
        anfang = True
    for a in range(1, len(labyrinth_neu) - 1):
        for b in range(1, len(labyrinth_neu[a]) - 1):
            # print(a, b, labyrinth_neu[a][b])

            label: mylabel = labelliste[a][b]
            # if not labyrinth_neu[a][b] == label.value:
            #    print(labyrinth_neu[a][b], label.value)
            label.value = labyrinth_neu[a][b]
            label.update_color()
            if labyrinth_neu[a][b] in [0, 2, 5]:
                label.clear()
            if labyrinth_neu[a][b] == 3:
                # if fertig:
                #    label.set_image(f"images/Labyrinth/richtung{richtung}", True)
                # else:
                label.set_image(f"images/Labyrinth/ziel", True)
            if a == roboterx and b == robotery:
                label.set_image(f"images/Labyrinth/richtung{richtung}", True)

            # label.setVisible(False)
            # label.setVisible(True)  # Hier tritt der Fehler QObject::setParent: Cannot set parent, new parent is in a different thread auf
            # print(a, b, labyrinth_neu[a][b])


def update_main_win(mainwin: QMainWindow, mainui: Ui_WMainWindow):
    global labelliste, buttonliste, labyrinth

    mainui.Lsimulation.setText("")

    if not labelliste == []:
        for a in labelliste:
            for b in a:
                b.deleteLater()

    y_offset = 30

    avail_width = mainui.Lsimulation.width()
    avail_height = mainui.Lsimulation.height()

    width = len(labyrinth)
    height = len(labyrinth[0])

    labelliste = [[0 for y in range(height)] for x in range(width)]

    if avail_width / width > avail_height / height:
        size = int(avail_height / height)
    else:
        size = int(avail_width / width)

    anfangspunkt = (mainui.Lsimulation.x(), mainui.Lsimulation.y() + y_offset)

    for a in range(width):
        for b in range(height):
            label: mylabel = mylabel(a, b, size, size, mainwin, a * size + anfangspunkt[0],
                                     b * size + anfangspunkt[1], labyrinth[a][b])
            if label.value == 1:
                pixmap = QPixmap('images/Labyrinth/wall.png')
                label.setPixmap(pixmap.scaledToHeight(label.height))
            if label.value == 2:
                pixmap = QPixmap('images/Labyrinth/richtung0.png')
                label.setPixmap(pixmap.scaledToHeight(label.height))
            if label.value == 3:
                pixmap = QPixmap('images/Labyrinth/ziel.png')
                label.setPixmap(pixmap.scaledToHeight(label.height))
            labelliste[a][b] = label


def check_labyrinth():
    global buttonliste
    start_exists = False
    start_exists_double = False
    end_exists = False
    for a in buttonliste:
        for b in a:
            if b.value == 2 and start_exists:
                start_exists_double = True
            elif b.value == 3:
                end_exists = True
            elif b.value == 2 and not start_exists:
                start_exists = True

    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Critical)
    dialog.setWindowTitle("Fehler!")
    if start_exists_double:
        dialog.setText("Es gibt zu viele Starts im Labyrinth!")
        dialog.exec()
        return False
    if not start_exists:
        dialog.setText("Es gibt keine Start im Labyrinth!")
        dialog.exec()
        return False
    if not end_exists:
        dialog.setText("Es gibt keine Ende im Labyrinth!")
        dialog.exec()
        return False
    return True


def cancel(editui: Ui_WLabyrinthEditor, editorwin: QMainWindow):
    editorwin.close()
    print("Editor geschlossen!")


def setup_rand(labyrinth_neu):
    for i in [0, len(labyrinth_neu) - 1]:
        for a in range(len(labyrinth_neu)):
            labyrinth_neu[a][i] = 1
        for b in range(len(labyrinth_neu)):
            labyrinth_neu[i][b] = 1
    return labyrinth_neu


def apply(editui: Ui_WLabyrinthEditor, editorwin: QMainWindow, mainwin: QMainWindow,
          mainui: Ui_WMainWindow):
    global labyrinth, buttonliste
    if not buttonliste:
        return
    labyrinth = [[0 for y in range(len(buttonliste[0]) + 2)] for x in range(len(buttonliste) + 2)]
    if check_labyrinth():
        vor_labyrinth = [[0 for y in range(len(buttonliste[0]) + 2)] for x in range(len(buttonliste) + 2)]
        for a in range(len(buttonliste)):
            for b in range(len(buttonliste[a])):
                vor_labyrinth[a + 1][b + 1] = buttonliste[a][b].value

        vor_labyrinth = setup_rand(vor_labyrinth)  #
        for a in vor_labyrinth:
            print(a)
        if find_path(vor_labyrinth):
            labyrinth = vor_labyrinth.copy()
            for a in range(len(labyrinth)):
                for b in range(len(labyrinth[a])):
                    if labyrinth[a][b] in [4, 5]:
                        labyrinth[a][b] = 0
            editorwin.close()
            update_main_win(mainwin, mainui)
            mainui.BshowSimulation.setEnabled(False)
            if classified:
                mainui.Bsimulate.setEnabled(True)


def vorbereiten(editui: Ui_WLabyrinthEditor, editorwin: QMainWindow):
    global labyrinth, buttonliste
    height = editui.SHeight.value()
    width = editui.SWidth.value()

    if not buttonliste == []:
        for a in buttonliste:
            for b in a:
                b.deleteLater()

    # Fehlerbehandlung
    buttonliste = [[0 for y in range(height)] for x in range(width)]
    # print(editorwin.width(), editui.Bcancel.x())

    y_offset = 30

    anfangspunkt = (10, editui.Bcancel.y() + editui.Bcancel.height() + y_offset + 5)
    bwidth = int((editorwin.width() - 2 * anfangspunkt[0]) / width)
    bheight = int((editorwin.height() - anfangspunkt[1]) / height)

    # print(bwidth, bheight, anfangspunkt, editui.Bcancel.y(), editui.Bcancel.height())

    # print(bwidth)
    for a in range(width):
        for b in range(height):
            button: mybutton = mybutton(a, b, bwidth, bheight, editorwin, a * bwidth + anfangspunkt[0],
                                        b * bheight + anfangspunkt[1])
            buttonliste[a][b] = button

    # print(height, width)


def save_layout(editui: Ui_WLabyrinthEditor, editorwin: QMainWindow):
    global buttonliste
    name = editui.Sname.value()
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Critical)
    dialog.setWindowTitle("Fehler!")

    if not buttonliste:
        dialog.setText("Du hast kein Labyrinth gebaut!")
        dialog.exec()
        return
    labyrinth1 = [[0 for y in range(len(buttonliste[0]) + 2)] for x in range(len(buttonliste) + 2)]

    if check_labyrinth():
        for a in range(len(buttonliste)):
            for b in range(len(buttonliste[a])):
                labyrinth1[a + 1][b + 1] = buttonliste[a][b].value

    labyrinth1 = setup_rand(labyrinth1)

    if f"{name}.dat" in next(os.walk("saved_Layouts"))[2]:
        dialog2 = QMessageBox()
        res = dialog2.question(dialog2, "Überschreiben?", f"Das Layout {name} wirklich überschreiben?",
                               dialog2.Yes | dialog2.No)
        if res == dialog2.Yes:
            dump(labyrinth1, open(f"saved_Layouts/{name}.dat", "wb"))
            dialog.setIcon(QMessageBox.Information)
            dialog.setWindowTitle("Speichern erfolgreich!")
            dialog.setText(f"Das Speichern von {name} war erfolgreich!")
            dialog.exec()
    else:
        dump(labyrinth1, open(f"saved_Layouts/{name}.dat", "wb"))
        dialog.setIcon(QMessageBox.Information)
        dialog.setWindowTitle("Speichern erfolgreich!")
        dialog.setText(f"Das Speichern von {name} war erfolgreich!")
        dialog.exec()


def load_layout(editui: Ui_WLabyrinthEditor, editorwin: QMainWindow):
    global labyrinth
    name = editui.Sname.value()
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Critical)
    dialog.setWindowTitle("Fehler!")

    if f"{name}.dat" not in next(os.walk("saved_Layouts"))[2]:
        dialog.setText(f"Das Layout {name} existiert noch nicht!")
        dialog.exec()
        return
    labyrinth = load(open(f"saved_Layouts/{name}.dat", "rb"))
    display_labyrinth(editui, editorwin)

    dialog.setIcon(QMessageBox.Information)
    dialog.setWindowTitle("Öffnen erfolgreich!")
    dialog.setText(f"Das Öffnen von Layout {name} war erfolgreich!")
    dialog.exec()


def delete_layout(editui: Ui_WLabyrinthEditor, editorwin: QMainWindow):
    name = editui.Sname.value()
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Critical)
    dialog.setWindowTitle("Fehler!")

    if not f"{name}.dat" in next(os.walk("saved_Layouts"))[2]:
        dialog.setText(f"Das Layout {name} existiert noch nicht!")
        dialog.exec()
        return
    dialog2 = QMessageBox()
    # dialog2.show()
    res = dialog2.question(dialog2, "Löschen?", f"Das Layout {name} wirklich löschen?", dialog2.Yes | dialog2.No)
    if res == dialog2.Yes:
        os.remove(f"saved_Layouts/{name}.dat")
        dialog.setIcon(QMessageBox.Information)
        dialog.setWindowTitle("Löschen erfolgreich!")
        dialog.setText(f"Das Löschen von Layout {name} war erfolgreich!")
        dialog.exec()


def delete_all_layout(editui: Ui_WLabyrinthEditor, editorwin: QMainWindow):
    dialog2 = QMessageBox()
    # dialog2.show()
    res = dialog2.question(dialog2, "Löschen?", f"Wirklich alles löschen?", dialog2.Yes | dialog2.No)
    if res == dialog2.Yes:
        liste = next(os.walk("saved_Layouts"))[2]
        for a in liste:
            if a.index(".dat") == len(a) - 4:
                os.remove(f"saved_Layouts/{a}")
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Information)
        dialog.setWindowTitle("Löschen erfolgreich!")
        dialog.setText(f"Das Löschen war erfolgreich!")
        dialog.exec()


def list_all_layout(editui: Ui_WLabyrinthEditor, editorwin: QMainWindow):
    liste = [x for x in next(os.walk("saved_Layouts"))[2] if x.index(".dat") == len(x) - 4]
    text = ""
    for a in liste:
        text += (str(a)[:-4] + ", ")
    dialog = QMessageBox()
    dialog.setIcon(QMessageBox.Information)
    dialog.setWindowTitle("Auflistung Dateien")
    dialog.setText(f"Die Dateien:\n{text[:-2]}")
    dialog.exec()
