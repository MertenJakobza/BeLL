# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\Merten\PycharmProjects\Auswertungs_software\GUI/editor.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WLabyrinthEditor(object):
    def setupUi(self, WLabyrinthEditor):
        WLabyrinthEditor.setObjectName("WLabyrinthEditor")
        WLabyrinthEditor.resize(796, 595)
        self.centralwidget = QtWidgets.QWidget(WLabyrinthEditor)
        self.centralwidget.setObjectName("centralwidget")
        self.Bapply = QtWidgets.QPushButton(self.centralwidget)
        self.Bapply.setGeometry(QtCore.QRect(10, 40, 101, 23))
        self.Bapply.setObjectName("Bapply")
        self.Bcancel = QtWidgets.QPushButton(self.centralwidget)
        self.Bcancel.setGeometry(QtCore.QRect(120, 40, 75, 23))
        self.Bcancel.setObjectName("Bcancel")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 71, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(160, 10, 31, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(280, 10, 47, 20))
        self.label_3.setObjectName("label_3")
        self.Bprepare = QtWidgets.QPushButton(self.centralwidget)
        self.Bprepare.setGeometry(QtCore.QRect(710, 10, 75, 23))
        self.Bprepare.setObjectName("Bprepare")
        self.Sname = QtWidgets.QSpinBox(self.centralwidget)
        self.Sname.setGeometry(QtCore.QRect(90, 10, 42, 22))
        self.Sname.setMinimum(1)
        self.Sname.setMaximum(10)
        self.Sname.setObjectName("Sname")
        self.SHeight = QtWidgets.QSpinBox(self.centralwidget)
        self.SHeight.setGeometry(QtCore.QRect(210, 10, 42, 22))
        self.SHeight.setMinimum(1)
        self.SHeight.setMaximum(30)
        self.SHeight.setProperty("value", 10)
        self.SHeight.setObjectName("SHeight")
        self.SWidth = QtWidgets.QSpinBox(self.centralwidget)
        self.SWidth.setGeometry(QtCore.QRect(320, 10, 42, 22))
        self.SWidth.setMinimum(1)
        self.SWidth.setMaximum(30)
        self.SWidth.setProperty("value", 10)
        self.SWidth.setObjectName("SWidth")
        WLabyrinthEditor.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(WLabyrinthEditor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 796, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        WLabyrinthEditor.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(WLabyrinthEditor)
        self.statusbar.setObjectName("statusbar")
        WLabyrinthEditor.setStatusBar(self.statusbar)
        self.actionLayout_speichern = QtWidgets.QAction(WLabyrinthEditor)
        self.actionLayout_speichern.setObjectName("actionLayout_speichern")
        self.actionLayout_laden = QtWidgets.QAction(WLabyrinthEditor)
        self.actionLayout_laden.setObjectName("actionLayout_laden")
        self.actionLayout_loeschen = QtWidgets.QAction(WLabyrinthEditor)
        self.actionLayout_loeschen.setObjectName("actionLayout_loeschen")
        self.actionAlles_Auflisten = QtWidgets.QAction(WLabyrinthEditor)
        self.actionAlles_Auflisten.setObjectName("actionAlles_Auflisten")
        self.actionAlles_loeschen = QtWidgets.QAction(WLabyrinthEditor)
        self.actionAlles_loeschen.setObjectName("actionAlles_loeschen")
        self.actionHilfe = QtWidgets.QAction(WLabyrinthEditor)
        self.actionHilfe.setObjectName("actionHilfe")
        self.actionHilfe_2 = QtWidgets.QAction(WLabyrinthEditor)
        self.actionHilfe_2.setObjectName("actionHilfe_2")
        self.menuFile.addAction(self.actionLayout_speichern)
        self.menuFile.addAction(self.actionLayout_laden)
        self.menuFile.addAction(self.actionLayout_loeschen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionAlles_Auflisten)
        self.menuFile.addAction(self.actionAlles_loeschen)
        self.menuFile.addSeparator()
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(WLabyrinthEditor)
        QtCore.QMetaObject.connectSlotsByName(WLabyrinthEditor)

    def retranslateUi(self, WLabyrinthEditor):
        _translate = QtCore.QCoreApplication.translate
        WLabyrinthEditor.setWindowTitle(_translate("WLabyrinthEditor", "Tools - Labyrinth-Editor"))
        self.Bapply.setText(_translate("WLabyrinthEditor", "Layout anwenden"))
        self.Bcancel.setText(_translate("WLabyrinthEditor", "Abbrechen"))
        self.label.setText(_translate("WLabyrinthEditor", "Layoutname:"))
        self.label_2.setText(_translate("WLabyrinthEditor", "Höhe:"))
        self.label_3.setText(_translate("WLabyrinthEditor", "Breite:"))
        self.Bprepare.setText(_translate("WLabyrinthEditor", "Vorbereiten"))
        self.menuFile.setTitle(_translate("WLabyrinthEditor", "File"))
        self.actionLayout_speichern.setText(_translate("WLabyrinthEditor", "Layout speichern"))
        self.actionLayout_laden.setText(_translate("WLabyrinthEditor", "Layout laden"))
        self.actionLayout_loeschen.setText(_translate("WLabyrinthEditor", "Layout löschen"))
        self.actionAlles_Auflisten.setText(_translate("WLabyrinthEditor", "Alles Auflisten"))
        self.actionAlles_loeschen.setText(_translate("WLabyrinthEditor", "Alles löschen"))
        self.actionHilfe.setText(_translate("WLabyrinthEditor", "Hilfe"))
        self.actionHilfe_2.setText(_translate("WLabyrinthEditor", "Hilfe"))
