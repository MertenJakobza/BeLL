import sys
import time

import cv2
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

import LabyrinthEditor
from GUI.editor import Ui_WLabyrinthEditor
from GUI.mainwindow import Ui_WMainWindow
from GUI.settings import Ui_WSettingsWindow

global img
weg = []
ablauf = []
labyrinth = []

aktuell_step = 0
labyrinth_weg = []

komplett_beendet = False
geschafft = False

varianz = 16
videoabbrechen = False
settui = Ui_WSettingsWindow
settingswin = QMainWindow
mainwin: QMainWindow
editorwin: QMainWindow
mainui: Ui_WMainWindow
editui: Ui_WLabyrinthEditor

settings_dic = {
    "UseVideo": False,
    "UseInteraction": False,
    "LiveSimulation": False
}

interpreted_array = []

GUI_label_liste = []

# Beispielergebnis der Klassifizierung als fertiges Array mit allen angepassten Daten
res = [{'height': 8, 'label': 'S01-Start', 'value': 0.941252589225769, 'width': 8, 'x': 16, 'y': 16},
       {'height': 8, 'label': 'M04-Right', 'value': 0.9913778305053711, 'width': 8, 'x': 40, 'y': 16},
       {'height': 8, 'label': 'C03-If', 'value': 0.998925507068634, 'width': 16, 'x': 64, 'y': 16},
       {'height': 8, 'label': 'C03-If', 'value': 0.9999614953994751, 'width': 8, 'x': 96, 'y': 16},
       {'height': 8, 'label': 'C03-If', 'value': 0.9995933175086975, 'width': 8, 'x': 120, 'y': 16},
       {'height': 8, 'label': 'M01-Forward', 'value': 0.9994913339614868, 'width': 8, 'x': 152, 'y': 16},
       {'height': 8, 'label': 'C03-If', 'value': 0.999528169631958, 'width': 8, 'x': 176, 'y': 16},
       {'height': 8, 'label': 'S04-Return', 'value': 0.9992904663085938, 'width': 16, 'x': 200, 'y': 16},
       {'height': 16, 'label': 'Ziel', 'value': 0.9997374415397644, 'width': 8, 'x': 176, 'y': 40},
       {'height': 8, 'label': 'M02-Backward', 'value': 0.7485865354537964, 'width': 8, 'x': 208, 'y': 40},
       {'height': 8, 'label': 'W01-Wand', 'value': 0.9949603080749512, 'width': 16, 'x': 64, 'y': 48},
       {'height': 8, 'label': 'W01-Wand', 'value': 0.9889870285987854, 'width': 8, 'x': 96, 'y': 48},
       {'height': 8, 'label': 'W01-Wand', 'value': 0.9999501705169678, 'width': 8, 'x': 120, 'y': 48},
       {'height': 8, 'label': 'CF-A', 'value': 0.9840059280395508, 'width': 16, 'x': 64, 'y': 72},
       {'height': 8, 'label': 'CF-A', 'value': 0.9991903901100159, 'width': 8, 'x': 96, 'y': 72},
       {'height': 8, 'label': 'CF-A', 'value': 0.9995256662368774, 'width': 8, 'x': 120, 'y': 72},
       {'height': 8, 'label': 'CF-Sub', 'value': 0.9929632544517517, 'width': 8, 'x': 176, 'y': 72},
       {'height': 8, 'label': 'blink', 'value': 0.9999614953994751, 'width': 8, 'x': 208, 'y': 72},
       {'height': 8, 'label': 'S02-End', 'value': 0.9999722242355347, 'width': 8, 'x': 232, 'y': 72},
       {'height': 8, 'label': 'N02', 'value': 0.8190993070602417, 'width': 8, 'x': 208, 'y': 104},
       {'height': 8, 'label': 'DF-A', 'value': 0.9998844861984253, 'width': 8, 'x': 96, 'y': 112},
       {'height': 8, 'label': 'M03-Left', 'value': 0.9973823428153992, 'width': 16, 'x': 120, 'y': 112},
       {'height': 8, 'label': 'S02-End', 'value': 0.998384952545166, 'width': 16, 'x': 144, 'y': 112}]

liste_label = ["S01-Start", "S02-End", "S04-Return",
               "blink", "C01-Loop", "C02-Wait",
               "C03-If", "W01-Wand", "Ziel",
               "CF-A", "DF-A",
               "CF-B", "DF-B",
               "CF-C", "DF-C",
               "N01", "N02", "N03", "N04", "N05", "N06", "N07", "N08", "N09",
               "M01-Forward", "M02-Backward", "M03-Left", "M04-Right",
               "CF-Sub", "Not", "Nichts"
               ]

# 0...normale Verbindung nach rechts,
# 1...normale Verbindung nach rechts eckiger Konnektor nach unten
# 2...eckiger Konnektor nach oben
# 3...eckiger Konnektor nach oben und unten
# 4...extra Nummer für Sub-Teil
liste_richtung = [0, 0, 0,
                  1, 1, 1,
                  1, 3, 3,
                  2, 0,
                  2, 0,
                  2, 0,
                  3, 3, 3, 3, 3, 3, 3, 3, 3,
                  0, 0, 0, 0,
                  4, 3]

unbenutzt_bb = []


def print_array(array):
    print("Hinweis: Das Array muss um 90° gedreht werden!")
    for a in array:
        print(a)


def cancel_video():
    global videoabbrechen
    videoabbrechen = True


def do_video():
    global videoabbrechen
    mainui.BstartVideo.setEnabled(False)
    mainui.Bcancelvideo.setEnabled(True)
    while not videoabbrechen:
        take_image()
        classify()

    videoabbrechen = False


def take_image():
    global img, mainui
    # print("test")
    img = cv2.imread("testProgramm.png")
    display_image(img)

    mainui.Bclassify.setEnabled(True)
    mainui.Bsimulate.setEnabled(False)
    LabyrinthEditor.set_classified(False)
    print("Bild aufgenommen!")


def display_image(img_neu):
    img_neu = cv2.resize(img_neu, (mainui.Lcamera_preview.height(), mainui.Lcamera_preview.height()))
    img_neu = cv2.cvtColor(img_neu, cv2.COLOR_BGR2RGB)
    mainui.Lcamera_preview.setText("")

    height, width, channel = img_neu.shape
    bytesPerLine = 3 * width
    qImg = QImage(img_neu.data, width, height, bytesPerLine, QImage.Format_RGB888)
    mainui.Lcamera_preview.setPixmap(QPixmap(qImg))


def show_simulation():
    global weg, labyrinth, aktuell_step, mainwin, mainui, labyrinth_weg
    roboter_start = [(x, y) for x in range(len(labyrinth)) for y in range(len(labyrinth[x])) if labyrinth[x][y] == 2][0]
    if aktuell_step == 0:
        labyrinth_weg = [[0 for a in range(len(labyrinth[0]))] for b in range(len(labyrinth))]
        for a in range(len(labyrinth)):
            for b in range(len(labyrinth[a])):
                labyrinth_weg[a][b] = labyrinth[a][b]
        LabyrinthEditor.update_Labyrinth_farben(labyrinth_weg, roboter_start[0], roboter_start[1], 0, False)
        aktuell_step += 1
        return

    if aktuell_step > (len(weg)):
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Information)
        dialog.setWindowTitle("Ende der Simulation")
        dialog.setText(f"Sie sind ans Ende der Simulation angelangt!")
        dialog.exec()
        aktuell_step = 0
        return

    step = weg[aktuell_step - 1]
    print(step)
    for a in range(len(labyrinth_weg)):
        for b in range(len(labyrinth_weg[a])):
            if labyrinth_weg[a][b] == 4:
                labyrinth_weg[a][b] = 5
    if labyrinth_weg[step[0]][step[1]] == 0:
        labyrinth_weg[step[0]][step[1]] = 4
    LabyrinthEditor.update_Labyrinth_farben(labyrinth_weg, step[0], step[1], step[2], False)
    print("Labyrinth angezeigt!")

    aktuell_step += 1


def simulate(interpreted_array):
    global mainui, mainwin, weg, ablauf, aktuell_step, labyrinth, geschafft, komplett_beendet

    komplett_beendet = False

    weg = []
    ablauf = []

    print("Thread gestartet!")
    mainui.actionSettings.setEnabled(False)
    mainui.actionLabyrinth_Editor.setEnabled(False)

    labyrinth = LabyrinthEditor.get_labyrinth().copy()

    roboter_start = [(x, y) for x in range(len(labyrinth)) for y in range(len(labyrinth[x])) if labyrinth[x][y] == 2][0]

    for a in labyrinth:
        print(a)

    # Simulation
    # Postion des nächsten Blättchen
    # akt_pos = (0, 0)
    # Aktuelles Programm definieren
    # 0...Start bzw. Main-Programm
    # 1...A
    # 2...B
    # akt_programm = 0
    # 1. Ansatz
    # Liste mit der Reihenfolge wie das aktuelle Subprogramm aufgerufen wurde
    # wenn ein Subprogramm fertig ist kann an der Stelle weitergemacht werden, wo das Programm aufgerufen wurde
    # Bsp: [[0, (2, 0)], [1, (2, 3)]]
    # Das Programm Start hat A an Stelle (2, 0) aufgerufen, welches dann ein anderes Programm an Stelle (2, 3)
    # aufgerufen hat
    # Subs werden als Subprogramm behandelt → So sind Verkettungen möglich
    # ES MUSS IMMER VERSUCHT WERDEN DAS CALLED_BY_ARRAY AM ENDE AUFZULÖSEN!
    # called_by = []
    # 2. Ansatz
    # Ähnlich wie Umwandeln in Array -> Rekursiv schreiben -> sub ruft die Funktion wieder auf
    # Wurde jetzt genutzt
    repeat = True
    richtung = 0
    durchgaenge = 0
    labyrinth_sim = [[0 for a in range(len(labyrinth[0]))] for b in range(len(labyrinth))]
    print("Simulations_Labyrinth", labyrinth_sim)
    print(roboter_start, "\n")
    for a in range(len(labyrinth)):
        for b in range(len(labyrinth[a])):
            labyrinth_sim[a][b] = labyrinth[a][b]

    print("Simulations_Labyrinth", labyrinth_sim, labyrinth == labyrinth_sim)

    while repeat:
        durchgaenge += 1
        # Labelnummer des nächsten Blättchens herausfinden
        if durchgaenge == 1:
            roboterx, robotery, labyrinth_neu, repeat, richtung = run_program_at(interpreted_array, 0, 0,
                                                                                 roboter_start[0],
                                                                                 roboter_start[1],
                                                                                 labyrinth_sim, richtung,
                                                                                 True)
        else:
            roboterx, robotery, labyrinth_neu, repeat, richtung = run_program_at(interpreted_array, 0, 0,
                                                                                 roboterx,
                                                                                 robotery,
                                                                                 labyrinth_neu, richtung,
                                                                                 True)
        print("Durchgang:", durchgaenge)

        # if label == "C03-If":
    if labyrinth_neu[roboterx][robotery] == 3:
        geschafft = True
    else:
        geschafft = False

    LabyrinthEditor.update_Labyrinth_farben(labyrinth_neu, roboterx, robotery, richtung, geschafft)

    if geschafft:
        print("Simulation beendet! Das Labyrinth wurde geschafft!")
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Information)
        dialog.setWindowTitle("Simuation beendet")
        dialog.setText(f"Simulation beendet! Das Labyrinth wurde geschafft!")
        dialog.exec()
    else:
        print("Simulation beendet! Das Labyrinth wurde NICHT geschafft!")
        dialog = QMessageBox()
        dialog.setIcon(QMessageBox.Critical)
        dialog.setWindowTitle("Simuation beendet")
        dialog.setText(f"Simulation beendet! Das Labyrinth wurde NICHT geschafft!")
        dialog.exec()

    aktuell_step = 0

    mainui.BshowSimulation.setEnabled(True)
    mainui.actionLabyrinth_Editor.setEnabled(True)
    mainui.actionSettings.setEnabled(True)


def classify():
    global interpreted_array, img, mainui
    print("Das Bild wird hier klassifiziert.")
    clasification_result = res
    interpreted_array = interprete(clasification_result)
    img = cv2.imread("testProgrammKlassifikation.png")
    display_image(img)
    print(interpreted_array)
    LabyrinthEditor.set_classified(True)
    if LabyrinthEditor.get_labyrinth():
        mainui.Bsimulate.setEnabled(True)
    print("Bild klassifiziert und dargestellt!")


def interprete(classification_result):
    global unbenutzt_bb, mainui, mainwin, GUI_label_liste

    for a in classification_result:
        if a["value"] < 0.75:
            print(a)
            classification_result.remove(a)

    unbenutzt_bb = classification_result.copy()
    detected_array = get_Array(classification_result)
    if not detected_array:
        print("Es gab einen Fehler beim erkennen der Blättchen!")

    y_offset = 30
    if mainui.Lpreview_classification.height() / len(detected_array[0]) > mainui.Lpreview_classification.width() / len(
            detected_array):
        size = int(mainui.Lpreview_classification.width() / len(detected_array))
        factor_height = False
    else:
        size = int(mainui.Lpreview_classification.height() / len(detected_array[0]))
        factor_height = True

    mainui.Lpreview_classification.setText("")

    if GUI_label_liste:
        for a in GUI_label_liste:
            for label in a:
                label.deleteLater()
    GUI_label_liste = [[0 for y in detected_array[0]] for x in detected_array]
    for a in range(len(detected_array)):
        for b in range(len(detected_array[a])):
            label = LabyrinthEditor.mylabel(a, b, size, size, mainwin, mainui.Lpreview_classification.x() + a * size,
                                            mainui.Lpreview_classification.y() + y_offset + b * size, -1)
            if not detected_array[a][b] == 0:
                label.set_image(f"images/Classification/{liste_label[detected_array[a][b] - 1]}", factor_height)
            GUI_label_liste[a][b] = label

    interpreted_array = detected_array.copy()
    interpreted_array.append([0 for x in range(len(interpreted_array[0]))])
    for a in interpreted_array:
        a.append(0)
    return interpreted_array


def get_Array(result_array):
    global unbenutzt_bb
    detected_array = [[]]
    # Zunächst heraus finden, wo sich der Start befindet

    start_bb = get_bb_by_label("S01-Start", result_array)
    if not len(start_bb) == 1:
        print("Es wurden zu wenige oder zu viele Starts erkannt!")
        return []

    unbenutzt_bb.remove(start_bb[0])
    start_sub_array = [[liste_label.index(start_bb[0]["label"]) + 1]]

    start_sub_programm = handle_programm_at(start_bb[0]["x"], start_bb[0]["y"])

    detected_array = insert_array(start_sub_programm, start_sub_array, 1, 0)

    for a in ["A", "B", "C"]:
        sub_process_bb_call = get_bb_by_label(f"CF-{a}", result_array)
        sub_process_bb_run = get_bb_by_label(f"DF-{a}", unbenutzt_bb)
        if len(sub_process_bb_run) == 0 and len(sub_process_bb_call) > 0:
            print(f"Die Methode {a} wird ist nicht definiert!")
            return []
        elif len(sub_process_bb_run) > 1 and len(sub_process_bb_call) > 0:
            print(f"Die Methode {a} wird ist mehrfach definiert!")
            return []
        elif not len(sub_process_bb_run) == 0 and not len(sub_process_bb_call) == 0:
            # Die Nummer des Subprogramms hinzufügen
            detected_array = insert_array([[liste_label.index(sub_process_bb_run[0]["label"]) + 1]], detected_array, 0,
                                          len(detected_array[0]) + 1)
            unbenutzt_bb.remove(sub_process_bb_run[0])
            detected_array = insert_array(
                handle_programm_at(sub_process_bb_run[0]["x"], sub_process_bb_run[0]["y"]),
                detected_array, 1, len(detected_array[0]) - 1)
        if len(sub_process_bb_call) == 0 and len(sub_process_bb_run) > 0:
            print(f"Die Methode {a} wird nicht aufgerufen!")

    return detected_array
    # raise NotImplementedError


def handle_programm_at(x, y):
    global unbenutzt_bb
    sub_programm_array = [[]]
    bbs_x = get_bb_by_y(y, unbenutzt_bb, x)
    for bb in bbs_x:
        if bb["label"] == "CF-Sub":
            break
        unbenutzt_bb.remove(bb)
        # sub_programm_array.append([])
        if get_richtung_by_label(bb["label"]) == 1:
            unten_sub_array = [[liste_label.index(bb["label"]) + 1]]
            bbs_y = get_bb_by_x(bb["x"], unbenutzt_bb, y)
            for bb_nested in bbs_y:
                # Das sind dann Überschneidungen mit anderen Ketten
                if get_richtung_by_label(bb_nested["label"]) == 0:
                    break
                # Anfügen der neuen Blättchen an das array was nach unten verläuft
                unten_sub_array[0].append(liste_label.index(bb_nested["label"]) + 1)
                unbenutzt_bb.remove(bb_nested)
                if bb_nested["label"] == "CF-Sub":
                    # Wenn das If wiederum einen Sub aufruft, wird diese Funktion für den Sub neu aufgerufen
                    # print(unten_sub_array)
                    cf_sub_array = handle_programm_at(bb_nested["x"], bb_nested["y"])
                    # print(cf_sub_array, bbs_y.index(bb_nested), bbs_y)
                    # das array vom sub-Blättchen an das array, das nach unten läuft anfügen
                    unten_sub_array = insert_array(cf_sub_array, unten_sub_array, 1,
                                                   bbs_y.index(bb_nested) + 1)
                    # print(unten_sub_array)
            # print("Subarray", unten_sub_array)
            # das untensubarray an das insgesamt zielprogramm anfügen
            sub_programm_array = insert_array(unten_sub_array, sub_programm_array, bbs_x.index(bb), 0)
        else:
            # einfach anweisungen einfach direkt anfügen
            sub_programm_array = insert_array([[liste_label.index(bb["label"]) + 1]], sub_programm_array,
                                              bbs_x.index(bb), 0)

    return sub_programm_array


def run_program_at(interpreted_array, x, y, roboterx, robotery, labyrinth_sim, richtung, hauptprogramm: bool):
    global weg, ablauf, komplett_beendet
    sleep_time = 0.5
    # Bei Aufruf der Funktion müssen die RandWände = 1 gesetzt werden!
    # x, y... Koordinaten in interpreted_array, wo der Lauf startet
    richtungen = [[1, 0], [0, 1], [-1, 0], [0, -1]]
    repeat = False

    print(f"Neues Programm an Stelle {x}, {y} gestartet. Der Roboter ist an Stelle {roboterx}, {robotery}")
    print(labyrinth)

    roboterx_neu = roboterx
    robotery_neu = robotery
    labyrinth_neu = [a for a in labyrinth_sim]

    for a in range(x, len(interpreted_array)):
        bb_num = interpreted_array[a][y] - 1
        bb_label = liste_label[bb_num]
        print("Hauptblättchen", bb_label)
        if bb_num == -1:
            break
        # Wenn es ein If oder eine Loop ist
        if liste_richtung[bb_num] == 1:
            liste_zahlen_bedingungen = []
            for b in range(y + 1, len(interpreted_array[a])):
                bb_sub_num = interpreted_array[a][b] - 1
                print("Sub-Blättchen:", liste_label[bb_sub_num])
                if bb_sub_num == -1:
                    # Die Blättchenreihe endet hier
                    if bb_label == "C02-Wait":
                        anz = sum([int(liste_label[x][1:]) for x in liste_zahlen_bedingungen])
                        # Alles anz Sekunden anhalten -> eventuell thread -> könnte schwierig werden
                        time.sleep(anz)
                    elif bb_label == "blink":
                        anz = sum([int(liste_label[x][1:]) for x in liste_zahlen_bedingungen])
                        for i in range(anz):
                            print("Blink!")
                    break
                if liste_richtung[bb_sub_num] == 3:
                    # Das Blättchen hier ist nur eine Bedingung
                    liste_zahlen_bedingungen.append(bb_sub_num)
                    print("Bedingung", liste_label[bb_sub_num], "hinzugefügt!")
                elif liste_richtung[bb_sub_num] in [2, 4]:
                    # Das Blättchen hier ist ein Methodenaufruf
                    # alle Bedingungen abgehen und auf Warheit überprüfen
                    if bb_label == "C03-If":
                        wahrheit = True
                        print("Bedingungen:", [liste_label[i] for i in liste_zahlen_bedingungen])
                        for i in liste_zahlen_bedingungen:
                            if liste_label[i] == "W01-Wand":
                                if not get_value_in_richtung(richtungen[richtung], roboterx_neu, robotery_neu,
                                                             labyrinth) == 1:
                                    wahrheit = False
                            if liste_label[i] == "Ziel":
                                if not labyrinth[roboterx_neu][robotery_neu] == 3:
                                    wahrheit = False
                        if "Not" in liste_zahlen_bedingungen:
                            wahrheit = not wahrheit
                        print("Die Bedingungen sind", wahrheit)
                        if wahrheit:
                            print("Das unter Programm wird gestartet!")
                            # Die Koordinaten des Startblättchens des aufgerufenen Programms
                            if liste_richtung[bb_sub_num] == 4:
                                print("Ein Sub erkannt!")
                                roboterx_neu, robotery_neu, labyrinth_neu, repeat, richtung = run_program_at(
                                    interpreted_array, a,
                                    b, roboterx_neu,
                                    robotery_neu,
                                    labyrinth_neu,
                                    richtung, hauptprogramm)
                            else:
                                repeat = True
                                while repeat:
                                    coords = get_start_coords_sub("D" + liste_label[bb_sub_num][1:], interpreted_array)
                                    print(f"Methode D{liste_label[bb_sub_num][1:]} aufgerufen")
                                    roboterx_neu, robotery_neu, labyrinth_neu, repeat, richtung = run_program_at(
                                        interpreted_array, coords[0], coords[1], roboterx_neu, robotery_neu,
                                        labyrinth_neu,
                                        richtung, False)

                    elif bb_label == "C01-Loop":
                        # Zahlen werden zusammenaddiert (2, 5 könnte man statt 7 auch als 25 werten)
                        anz = sum([int(liste_label[x][1:]) for x in liste_zahlen_bedingungen])
                        for i in range(anz):
                            # Starte das Programm anz-mal
                            if liste_richtung[bb_sub_num] == 4:
                                print("Ein Sub erkannt!")
                                roboterx_neu, robotery_neu, labyrinth_neu, repeat, richtung = run_program_at(
                                    interpreted_array, a,
                                    b, roboterx_neu,
                                    robotery_neu,
                                    labyrinth_neu,
                                    richtung, hauptprogramm)
                            else:
                                repeat = True
                                coords = get_start_coords_sub("D" + liste_label[bb_sub_num][1:], interpreted_array)
                                print(f"Methode D{liste_label[bb_sub_num][1:]} aufgerufen")
                                while repeat:
                                    roboterx_neu, robotery_neu, labyrinth_neu, repeat, richtung = run_program_at(
                                        interpreted_array, coords[0], coords[1], roboterx_neu, robotery_neu,
                                        labyrinth_neu,
                                        richtung, False)
                # Das Blättchen ist ein Sub

        if liste_richtung[bb_num] == 0:
            # Normale Anweisung / Return / Break
            if bb_label == "M01-Forward":
                old_value = labyrinth_neu[roboterx_neu][robotery_neu]
                if get_value_in_richtung(richtungen[richtung], roboterx_neu, robotery_neu, labyrinth_neu) == 1:
                    # bei einer Wand wird die Anweisung einfach übersprungen
                    continue
                if old_value not in [2, 3]:
                    labyrinth_neu[roboterx_neu][robotery_neu] = 5

                roboterx_neu += richtungen[richtung][0]
                robotery_neu += richtungen[richtung][1]

                if labyrinth_neu[roboterx_neu][robotery_neu] not in [2, 3]:
                    labyrinth_neu[roboterx_neu][robotery_neu] = 4
                print(f"Eins nach vorne Bewegt! Neue Koordinaten: {roboterx_neu}, {robotery_neu}")
                ablauf.append([roboterx_neu, robotery_neu, richtung])
            elif bb_label == "M02-Backward":
                old_value = labyrinth_neu[roboterx_neu][robotery_neu]
                if get_value_in_richtung(richtungen[richtung], roboterx_neu, robotery_neu, labyrinth_neu) == 1:
                    continue
                if old_value not in [2, 3]:
                    labyrinth_neu[roboterx_neu][robotery_neu] = 5

                roboterx_neu -= richtungen[richtung][0]
                robotery_neu -= richtungen[richtung][1]
                if labyrinth_neu[roboterx_neu][robotery_neu] not in [2, 3]:
                    labyrinth_neu[roboterx_neu][robotery_neu] = 4
                print(f"Eins nach vorne Bewegt! Neue Koordinaten: {roboterx_neu}, {robotery_neu}")
                ablauf.append([roboterx_neu, robotery_neu, richtung])
            elif bb_label == "M03-Left":
                if richtung > 0:
                    richtung += - 1
                else:
                    richtung = 3
                print(f"Nach links gedreht, neue Richtung: {richtung}")
                ablauf.append([roboterx_neu, robotery_neu, richtung])
            elif bb_label == "M04-Right":
                if richtung < 3:
                    richtung += 1
                else:
                    richtung = 0
                print(f"Nach rechts gedreht, neue Richtung: {richtung}")
                ablauf.append([roboterx_neu, robotery_neu, richtung])
            elif bb_label == "S02-End":
                print("Das (Sub-)Programm ist komplett beendet")
                repeat = False
                if hauptprogramm:
                    komplett_beendet = True
                    print("Hauptprogramm wird beendet!!!")
                    weg.append([roboterx_neu, robotery_neu, richtung])
                break
            elif bb_label == "S04-Return":
                if [roboterx_neu, robotery_neu, richtung] in weg and hauptprogramm:
                    weg.append([roboterx_neu, robotery_neu,
                                richtung])  # Aufzeichnen des aktuellen Schrittes, zur späteren Anzeige
                    komplett_beendet = True
                    print("Hauptprogramm wird beendet!!!")
                    break
                if hauptprogramm:  # Wenn sich die Simulation im Hauptprogramm befindet
                    weg.append([roboterx_neu, robotery_neu, richtung])  # Aufzeichnen des akutellen Schrittes
                print(f"Die aktuelle Funktion {liste_label[interpreted_array[x][y] - 1]} wird wiederholt!")
                repeat = True
        if komplett_beendet:
            print("Hauptprogramm wurde beendet!!!")
            break
    print("Return back!")
    return roboterx_neu, robotery_neu, labyrinth_neu, repeat, richtung


def get_start_coords_sub(sub_name, interpreted_array):
    return [(x, y) for x in range(len(interpreted_array)) for y in range(len(interpreted_array[x])) if
            liste_label[interpreted_array[x][y] - 1] == sub_name][0]


def get_value_in_richtung(richtung, x, y, labyrinth_neu):
    return labyrinth_neu[x + richtung[0]][y + richtung[1]]


def insert_array(source_array, ziel_array, x, y):
    # Array 1 wird in Array 2 ab der Startstelle (x, y) eingefügt
    # dabei soll Array2 in der Größe angepasst werden

    # print("Insert Eingabekoordinaten: ", x, y)

    # Überprüfen, ob die Sourcearray breiter ist als die Zielarray
    if x + len(source_array) > len(ziel_array):
        # print("Die Liste ist breiter als die Zielliste!")
        for a in range((x + len(source_array)) - len(ziel_array)):
            # Anfügen so vieler Arrays, die so groß sind wie der bisherige Y-Wert der Zielarray
            ziel_array.append([0 for x in range(len(ziel_array[0]))])
    # Überprüfen, ob die Sourcearray höher ist als die Zielarray
    if y + len(source_array[0]) > len(ziel_array[0]):
        # print("Die Liste ist höher als die Zielliste!")
        # in jede Spalte so viele Zeilen hinzufügen bis die Größe gleich ist
        for b in ziel_array:
            for a in range((y + len(source_array[0]) - len(b))):
                b.append(0)

    # print("Insert Zwischenarray: ", ziel_array)

    # time.sleep(0.1)
    for a in range(len(source_array)):
        for b in range(len(source_array[a])):
            if ziel_array[a + x][b + y] == 0:
                ziel_array[a + x][b + y] = source_array[a][b]
            else:
                print("Hier steht schon etwas!")
    # print("Insert Ergebnis: ", ziel_array)
    return ziel_array


def get_bb_by_label(label, bbarray):
    return [bb for bb in bbarray if bb["label"] == label]


def get_richtung_by_label(label):
    global liste_richtung, liste_label
    return liste_richtung[liste_label.index(label)]


def get_bb_by_y(y, bbarray, minx):
    global varianz
    return sorted([bb for bb in bbarray if
                   y + varianz >= bb["y"] >= y - varianz and get_richtung_by_label(bb["label"]) not in (2, 3) and bb[
                       "x"] > minx],
                  key=lambda d: d["x"])
    # sorted_list = sorted(array, key=lambda d: d['x'])


def get_bb_by_x(x, bbarray, miny):
    global varianz
    return sorted([bb for bb in bbarray if
                   x + varianz >= bb["x"] >= x - varianz and bb["y"] > miny],
                  key=lambda d: d["y"])


def init_windows():
    global mainwin, editorwin, mainui, editui, settui, settingswin

    mainwin = QMainWindow()
    mainui = Ui_WMainWindow()
    mainui.setupUi(mainwin)
    mainwin.show()

    editorwin = QMainWindow()
    editui = Ui_WLabyrinthEditor()
    editui.setupUi(editorwin)

    settingswin = QMainWindow()
    settui = Ui_WSettingsWindow()
    settui.setupUi(settingswin)


def use_video():
    if settui.CUseVideo.isChecked():
        settui.CUseInteraction.setEnabled(True)
        settui.CSimulateLive.setEnabled(True)
    else:
        settui.CUseInteraction.setEnabled(False)
        settui.CSimulateLive.setEnabled(False)
        settui.CUseInteraction.setChecked(False)
        settui.CSimulateLive.setChecked(False)


def apply_settings():
    print("Einstellungen haben noch keine Effekte!")
    settingswin.close()


def connect_Buttons():
    global mainui, editorwin, editui, mainwin, settingswin, interpreted_array, settui
    mainui.Bclassify.clicked.connect(classify)
    mainui.Bsimulate.clicked.connect(
        lambda: simulate(interpreted_array))
    mainui.Bretakeimage.clicked.connect(take_image)

    mainui.actionLabyrinth_Editor.triggered.connect(lambda: editorwin.show())

    editui.Bprepare.clicked.connect(lambda: LabyrinthEditor.vorbereiten(editui, editorwin))
    editui.Bcancel.clicked.connect(lambda: LabyrinthEditor.cancel(editui, editorwin))
    editui.Bapply.clicked.connect(lambda: LabyrinthEditor.apply(editui, editorwin, mainwin, mainui))

    editui.actionLayout_speichern.triggered.connect(lambda: LabyrinthEditor.save_layout(editui, editorwin))
    editui.actionLayout_laden.triggered.connect(lambda: LabyrinthEditor.load_layout(editui, editorwin))
    editui.actionLayout_loeschen.triggered.connect(lambda: LabyrinthEditor.delete_layout(editui, editorwin))
    editui.actionAlles_loeschen.triggered.connect(lambda: LabyrinthEditor.delete_all_layout(editui, editorwin))
    editui.actionAlles_Auflisten.triggered.connect(lambda: LabyrinthEditor.list_all_layout(editui, editorwin))
    mainui.actionSettings.triggered.connect(lambda: settingswin.show())

    settui.CUseVideo.stateChanged.connect(lambda: use_video())
    settui.Bcancel.clicked.connect(lambda: settingswin.close())
    settui.Bapply.clicked.connect(lambda: apply_settings())
    mainui.BshowSimulation.clicked.connect(lambda: show_simulation())


if __name__ == '__main__':
    # print(len(liste_richtung), len(liste_label))
    app = QApplication(sys.argv)

    init_windows()
    connect_Buttons()

    sys.exit(app.exec_())
