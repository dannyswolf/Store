# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'store.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
# ###############################------------------NOTES--------------------###################
# Αν ο χρήστης κλείσει τα παράθυρα απο το Χ πάνω δεξιά το self.edit_spare_parts_windows δεν γίνεται None
# για αυτό βάζουμε αν είναι ορατό -->  self.edit_spare_part_window.isVisible()
# στα ανταλλακτικά (spare_parts) μπορούμε να ανοίξουμε μόνο δυο παράθυρα ταυτόχρονα + 1 για εισαγωγή νέου
# στα αναλώσιμα (consumables) μπορούμε να ανοίξουμε μόνο τρία παράθυρα ταυτόχρονα + 1 για εισαγωγή νέου
# στις παραγγελίες (orders) μπορούμε να ανοίξουμε μόνο δυο παράθυρα ταυτόχρονα + 1 για εισαγωγή νέου
# στις μελανοταινίες (melancholies) μπορούμε να ανοίξουμε μόνο δυο παράθυρα ταυτόχρονα + 1 για εισαγωγή νέου
# για να μήν μπερδευόμαστε
# για να ανοίξουμε πολλά παράθυρα βάζουμε  # self.edit_spare_part.window = self.edit_spare_part_window
# έτσι  δημιουργούμε κάθε φορά νεο παράθυρο
##############################################################################################
# Version = 1.1.3 Fix Images to Orders   8-3-2025
# Version = 1.1.2 Add quality to orders
# Version = 1.1.1 Add splitter and bold labels
# Version = 1.0.9 Search with sqlalchemy
# Version = 1.0.8 Fix closed windows with X
# Version = 1.0.7 Check for double part no + κωδικούς and search with re.sub()
# Version = 1.0.6 Διαχείριση πολλαπλών παραθύρων
# Version = 1.0.5 Close window after save
# Version = 1.0.4 Χρώματα στις παραγγελίες και πολλαπλά παράθυρα
# Version = 1.0.3 Fix Prices with "," and multiple windows in consumables
# Version = 1.0.2 Fix Prices and Readonly Total
# Version = 1.0.1 Change Colors and fix Search
# Version = 1.0.0 All ready
# VERSION = "V 0.4.1"  Κλείνει τα παραθυρα με Esc
# VERSION = "V 0.3.1"  Μελανοταινίες ready και κουμπια διαγραφών παραγγελιών
# VERSION = "V 0.2.1"  Consumables ready

import time
# Database
from db import get_spare_parts, DB, select, conn, search_on_spare_parts, search_on_consumables, search_on_orders

# Settings
from settings import VERSION, today, BASE_PATH

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFrame, QAbstractScrollArea, QTreeWidgetItem, QWidget

# Database
from db import Brother, Canon, Epson, Konica, Kyocera, Lexmark, Oki, Ricoh, Samsung, Sharp, Melanakia, Melanotainies, \
    Toner, Copiers, Orders, session

# Excel
import pandas as pd

# Για τα αρχεία
import os
import sys
import subprocess
import pathlib
import shutil

# Παράθυρα επεξεργασίας
from edit_spare_part_window import Ui_edit_spare_parts_window
from edit_consumables_window import Ui_edit_consumables_window
from edit_orders_window import Ui_edit_orders_window
from edit_malanotainies_window import Ui_edit_melanotainies_window

# ---------------SORTING----------------------
import re

# --------------Log Files----------------------
import traceback


# Κανουμε sub class το QTreeWidgetItem για να κανει sort τους αριθμους που ειναι σε string μορφη
class TreeWidgetItem(QTreeWidgetItem):
    def __lt__(self, other):
        column = self.treeWidget().sortColumn()
        key1 = self.text(column)
        key2 = other.text(column)
        return self.natural_sort_key(key1) < self.natural_sort_key(key2)

    @staticmethod
    def natural_sort_key(key):
        regex = '(\d*\.\d+|\d+)'
        parts = re.split(regex, key)
        return tuple((e if i % 2 == 0 else float(e)) for i, e in enumerate(parts))


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Ui_MainWindow, self).__init__(*args, **kwargs)

        self.images_path = None

        self.selected_table = None
        self.data_to_show = None

        self.new_spare_part_window = None
        self.edit_spare_part_window = None
        self.second_edit_spare_part_window = None

        self.new_consumables_window = None
        self.edit_consumables_window = None
        self.second_edit_consumables_window = None
        self.third_edit_consumables_window = None

        self.new_melanotainies_window = None
        self.edit_melanotainies_window = None
        self.second_edit_melanotainies_window = None

        self.new_orders_window = None
        self.edit_orders_window = None
        self.second_edit_orders_window = None

        self.new_spare_part = None
        self.edit_spare_part = None
        self.second_edit_spare_part = None

        self.new_order = None
        self.edit_orders = None
        self.second_edit_orders = None

        self.new_consumable = None
        self.edit_consumable = None
        self.second_edit_consumable = None
        self.third_edit_consumable = None

        self.new_melanotainia = None
        self.edit_melanotainia = None
        self.second_edit_melanotainia = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMinimumSize(QtCore.QSize(0, 30))
        MainWindow.setWindowTitle(f"Αποθήκη {VERSION}")
        MainWindow.setWindowIcon(QtGui.QIcon('icons/icon.png'))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")

        # Brother
        self.brother_btn = QtWidgets.QToolButton(self.centralwidget)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/BROTHER.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.brother_btn.setIcon(icon8)
        self.brother_btn.setMinimumSize(QtCore.QSize(0, 50))
        # self.brother_btn.setStyleSheet("image: url(icons/BROTHER.png);""border-radius : 1; border : 1px solid black")
        self.brother_btn.setStyleSheet("background-color: #fff;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.brother_btn.setIconSize(QtCore.QSize(120, 50))
        self.brother_btn.setObjectName("brother_btn")
        self.brother_btn.clicked.connect(lambda: self.show_spare_parts(Brother))
        self.gridLayout.addWidget(self.brother_btn, 0, 0, 1, 1)

        # Canon
        self.canon_btn = QtWidgets.QToolButton(self.centralwidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/CANON.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.canon_btn.setIcon(icon3)
        self.canon_btn.setIconSize(QtCore.QSize(120, 50))
        self.canon_btn.setStyleSheet("background-color: #fff;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.canon_btn.setObjectName("canon_btn")
        self.canon_btn.clicked.connect(lambda: self.show_spare_parts(Canon))
        self.gridLayout.addWidget(self.canon_btn, 0, 1, 1, 1)

        # Epson
        self.epson_btn = QtWidgets.QToolButton(self.centralwidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/EPSON.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.epson_btn.setIcon(icon2)
        self.epson_btn.setIconSize(QtCore.QSize(120, 50))
        self.epson_btn.setStyleSheet("background-color: #fff;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.epson_btn.setObjectName("epson_btn")
        self.epson_btn.clicked.connect(lambda: self.show_spare_parts(Epson))
        self.gridLayout.addWidget(self.epson_btn, 0, 2, 1, 1)

        # Konica
        self.konica_btn = QtWidgets.QToolButton(self.centralwidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/KONICA.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.konica_btn.setIcon(icon6)
        self.konica_btn.setIconSize(QtCore.QSize(120, 50))
        self.konica_btn.setStyleSheet("background-color: #fff;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 0px;")
        self.konica_btn.setObjectName("konica_btn")
        self.konica_btn.clicked.connect(lambda: self.show_spare_parts(Konica))
        self.gridLayout.addWidget(self.konica_btn, 0, 3, 1, 1)

        # Kyocera
        self.kyocera_btn = QtWidgets.QToolButton(self.centralwidget)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/KYOCERA.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.kyocera_btn.setIcon(icon7)
        self.kyocera_btn.setIconSize(QtCore.QSize(120, 50))
        self.kyocera_btn.setStyleSheet("background-color: #fff;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.kyocera_btn.setObjectName("kyocera_btn")
        self.kyocera_btn.clicked.connect(lambda: self.show_spare_parts(Kyocera))
        self.gridLayout.addWidget(self.kyocera_btn, 0, 4, 1, 1)

        # Lexmark
        self.lexmark_btn = QtWidgets.QToolButton(self.centralwidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/LEXMARK.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lexmark_btn.setIcon(icon4)
        self.lexmark_btn.setIconSize(QtCore.QSize(120, 50))
        self.lexmark_btn.setStyleSheet("background-color: #fff;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.lexmark_btn.setObjectName("lexmark_btn")
        self.lexmark_btn.clicked.connect(lambda: self.show_spare_parts(Lexmark))
        self.gridLayout.addWidget(self.lexmark_btn, 0, 5, 1, 1)

        # Oki
        self.oki_btn = QtWidgets.QToolButton(self.centralwidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/OKI.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.oki_btn.setIcon(icon5)
        self.oki_btn.setIconSize(QtCore.QSize(120, 50))
        self.oki_btn.setStyleSheet("background-color: #fff;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.oki_btn.setObjectName("oki_btn")
        self.oki_btn.clicked.connect(lambda: self.show_spare_parts(Oki))
        self.gridLayout.addWidget(self.oki_btn, 0, 6, 1, 1)

        # Ricoh
        self.ricoh_btn = QtWidgets.QToolButton(self.centralwidget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/RICOH.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ricoh_btn.setIcon(icon)
        self.ricoh_btn.setIconSize(QtCore.QSize(120, 50))
        self.ricoh_btn.setStyleSheet("background-color: #fff;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.ricoh_btn.setWhatsThis("RICOH.png")
        self.ricoh_btn.setObjectName("ricoh_btn")
        self.ricoh_btn.clicked.connect(lambda: self.show_spare_parts(Ricoh))
        self.gridLayout.addWidget(self.ricoh_btn, 0, 7, 1, 1)

        # Samsung
        self.samsung_btn = QtWidgets.QToolButton(self.centralwidget)
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap("icons/SAMSUNG.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.samsung_btn.setIcon(icon13)
        self.samsung_btn.setIconSize(QtCore.QSize(120, 50))
        self.samsung_btn.setStyleSheet("background-color: #fff;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.samsung_btn.setObjectName("samsung_btn")
        self.samsung_btn.clicked.connect(lambda: self.show_spare_parts(Samsung))
        self.gridLayout.addWidget(self.samsung_btn, 0, 8, 1, 1)

        # Sharp
        self.sharp_btn = QtWidgets.QToolButton(self.centralwidget)
        icon14 = QtGui.QIcon()
        icon14.addPixmap(QtGui.QPixmap("icons/SHARP.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.sharp_btn.setIcon(icon14)
        self.sharp_btn.setIconSize(QtCore.QSize(120, 50))
        self.sharp_btn.setStyleSheet("background-color: #fff;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.sharp_btn.setObjectName("sharp_btn")
        self.sharp_btn.clicked.connect(lambda: self.show_spare_parts(Sharp))
        self.gridLayout.addWidget(self.sharp_btn, 0, 9, 1, 1)

        # Space
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 10)

        """ ------------------------------------- LABEL--------------------------"""
        # Label
        self.selected_table_label = QtWidgets.QLabel(self.centralwidget)
        self.selected_table_label.setMinimumSize(QtCore.QSize(0, 30))
        self.selected_table_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.selected_table_label.setStyleSheet(
            "background-color: gray;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 4px;"
            "font-style: normal;font-size: 14pt;font-weight: bold;")
        self.selected_table_label.setAlignment(QtCore.Qt.AlignCenter)
        self.selected_table_label.setObjectName("selected_table_label")
        self.selected_table_label.hide()
        self.gridLayout.addWidget(self.selected_table_label, 3, 3, 1, 5)

        """ ------------------------------- ΚΑΤΩ ΕΙΚΟΝΙΔΙΑ------------------------- """

        # Μελανάκια
        self.melanakia_btn = QtWidgets.QPushButton(self.centralwidget)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap("icons/ΜΕΛΑΝΑΚΙΑ.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.melanakia_btn.setIcon(icon11)
        self.melanakia_btn.setIconSize(QtCore.QSize(120, 50))
        self.melanakia_btn.setStyleSheet("background-color: #ffb907;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.melanakia_btn.setObjectName("melanakia_btn")
        self.melanakia_btn.clicked.connect(lambda: self.show_consumables(Melanakia))
        self.gridLayout.addWidget(self.melanakia_btn, 2, 0, 1, 2)

        # Μεαλανοταινίες
        self.melanotainies_btn = QtWidgets.QPushButton(self.centralwidget)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap("icons/ΜΕΛΑΝΟΤΑΙΝΙΕΣ.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.melanotainies_btn.setIcon(icon9)
        self.melanotainies_btn.setIconSize(QtCore.QSize(120, 50))
        self.melanotainies_btn.setStyleSheet("background-color: #ffb907;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.melanotainies_btn.setObjectName("melanotainies_btn")
        self.melanotainies_btn.clicked.connect(lambda: self.show_melanotainies(Melanotainies))
        self.gridLayout.addWidget(self.melanotainies_btn, 2, 2, 1, 2)

        # Toner
        self.toner_btn = QtWidgets.QPushButton(self.centralwidget)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap("icons/ΤΟΝΕΡ.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toner_btn.setIcon(icon10)
        self.toner_btn.setIconSize(QtCore.QSize(120, 50))
        self.toner_btn.setStyleSheet("background-color: #ffb907;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.toner_btn.setObjectName("toner_btn")
        self.toner_btn.clicked.connect(lambda: self.show_consumables(Toner))
        self.gridLayout.addWidget(self.toner_btn, 2, 4, 1, 2)

        # Φωτοτυπικά
        self.copiers_btn = QtWidgets.QPushButton(self.centralwidget)
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap("icons/ΦΩΤΟΤΥΠΙΚΑ.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.copiers_btn.setIcon(icon12)
        self.copiers_btn.setIconSize(QtCore.QSize(120, 50))
        self.copiers_btn.setStyleSheet("background-color: #ffb907;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.copiers_btn.setObjectName("copiers_btn")
        self.copiers_btn.clicked.connect(lambda: self.show_consumables(Copiers))
        self.gridLayout.addWidget(self.copiers_btn, 2, 6, 1, 2)

        # Παραγγελίες
        self.orders_btn = QtWidgets.QPushButton(self.centralwidget)
        icon15 = QtGui.QIcon()
        icon15.addPixmap(QtGui.QPixmap("icons/ΠΑΡΑΓΓΕΛΙΕΣ.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.orders_btn.setIcon(icon15)
        self.orders_btn.setIconSize(QtCore.QSize(120, 50))
        self.orders_btn.setStyleSheet("background-color: #ffb907;" "color: white;" "border-style: outset;" "border-width: 2px;" \
            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.orders_btn.setObjectName("orders_btn")
        self.orders_btn.clicked.connect(lambda: self.show_orders(Orders))
        self.gridLayout.addWidget(self.orders_btn, 2, 8, 1, 2)

        # Search line
        self.search_line_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.search_line_edit.setMinimumSize(QtCore.QSize(0, 50))
        self.search_line_edit.setObjectName("search_line_edit")
        self.search_line_edit.setStyleSheet("color: gray;" "border-style: outset;" "border-width: 2px;"
                                            "border-radius: 15px;" "border-color: black;" "padding: 2px;")
        self.search_line_edit.returnPressed.connect(self.search)
        self.search_line_edit.hide()
        self.gridLayout.addWidget(self.search_line_edit, 9, 3, 1, 2)

        # Search btn
        self.search_btn = QtWidgets.QToolButton(self.centralwidget)
        self.search_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.search_btn.setToolTip("Κουμπή αναζήτησης")
        self.search_btn.setLayoutDirection(QtCore.Qt.LeftToRight)

        # self.search_btn.setStyleSheet("border-radius : 1; border : 2px solid green")
        # self.search_btn.setStyleSheet(
        #     "background-color: gray;" "color: white;" "border-style: outset;" "border-width: 2px;" \
        #     "border-radius: 15px;" "border-color: black;" "padding: 4px;"
        #     "font-style: normal;font-size: 14pt;font-weight: bold;")
        self.search_btn.setStyleSheet("background-color: gray;" "color: white;" "border-style: outset;"
                                      "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                                      "font-style: normal;font-size: 14pt;font-weight: bold;"
                                      "qproperty-iconSize: 40px")
        self.search_btn.setText(f"Αναζήτηση")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_btn.setIcon(icon)
        self.search_btn.setIconSize(QtCore.QSize(30, 50))
        # self.search_btn.setAutoRepeatDelay(300)
        self.search_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.search_btn.setObjectName("search_btn")
        self.search_btn.hide()
        self.search_btn.clicked.connect(lambda: self.search())
        self.gridLayout.addWidget(self.search_btn, 9, 5, 1, 1)

        # Delete All Btn
        self.del_all_btn = QtWidgets.QPushButton(self.centralwidget)
        self.del_all_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.del_all_btn.setStyleSheet(
            "background-color: rgb(255, 85, 127);""border-radius : 1; border : 1px solid black")
        self.del_all_btn.setStyleSheet("background-color: gray;" "color: white;" "border-style: outset;"
                                       "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                                       "font-style: normal;font-size: 14pt;font-weight: bold;"
                                       "qproperty-iconSize: 40px")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/delete_all.png"))
        self.del_all_btn.setIcon(icon2)
        self.del_all_btn.setIconSize(QtCore.QSize(30, 50))
        # self.del_all_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.del_all_btn.setObjectName("del_all_btn")
        self.del_all_btn.hide()
        self.del_all_btn.clicked.connect(self.delete_orders)
        self.gridLayout.addWidget(self.del_all_btn, 9, 7, 1, 1)

        # Delete Selected btn
        self.del_selected_btn = QtWidgets.QPushButton(self.centralwidget)
        self.del_selected_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.del_selected_btn.setStyleSheet("background-color: gray;" "color: white;" "border-style: outset;"
                                            "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                                            "font-style: normal;font-size: 14pt;font-weight: bold;"
                                            "qproperty-iconSize: 50px")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/delete_selected.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.del_selected_btn.setIcon(icon1)
        self.del_selected_btn.setIconSize(QtCore.QSize(30, 50))
        # self.del_selected_btn.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.del_selected_btn.setObjectName("del_selected_btn")
        self.del_selected_btn.hide()
        self.del_selected_btn.clicked.connect(self.delete_selected_orders)
        self.gridLayout.addWidget(self.del_selected_btn, 9, 9, 1, 1)

        """------------------------------- Menu----------------------------"""
        # Menu
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1117, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menuBackup = QtWidgets.QMenu(self.menubar)
        self.menuBackup.setObjectName("menuBackup")
        self.menuInfo = QtWidgets.QMenu(self.menubar)
        self.menuInfo.setObjectName("menuInfo")
        MainWindow.setMenuBar(self.menubar)
        # statusbar
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # Ανοιγμα αρχείου
        # self.action = QtWidgets.QAction(MainWindow)
        # self.action.setObjectName("action")
        # self.action.triggered.connect(self.open_data_base)
        # Προσθήκη
        self.action_F1 = QtWidgets.QAction(MainWindow)
        self.action_F1.setObjectName("action_F1")
        self.action_F1.triggered.connect(self.add_spare_part)
        # Επεξεργασία
        self.actionEdit = QtWidgets.QAction(MainWindow)
        self.actionEdit.setObjectName("actionEdit")
        self.actionEdit.triggered.connect(self.show_edit_from_menu_or_F3)
        # Διαργαφή
        self.action_3 = QtWidgets.QAction(MainWindow)
        self.action_3.setObjectName("action_3")
        self.action_3.triggered.connect(self.delete_selected_item)
        # Εξοδος
        self.action_Esc = QtWidgets.QAction(MainWindow)
        self.action_Esc.setObjectName("action_Esc")
        self.action_Esc.triggered.connect(self.quit)
        # Backup
        self.actionBackup_Database = QtWidgets.QAction(MainWindow)
        self.actionBackup_Database.setObjectName("actionBackup_Database")
        self.actionBackup_Database.triggered.connect(self.backup)
        # Excel
        self.action_Excel = QtWidgets.QAction(MainWindow)
        self.action_Excel.setObjectName("action_Excel")
        self.action_Excel.triggered.connect(self.to_excel)
        # Info
        self.action_4 = QtWidgets.QAction(MainWindow)
        self.action_4.setObjectName("action_4")
        self.action_4.triggered.connect(self.info)

        # self.menu.addAction(self.action)
        self.menu.addAction(self.action_F1)
        self.menu.addAction(self.actionEdit)
        self.menu.addSeparator()
        self.menu.addAction(self.action_3)
        self.menu.addAction(self.action_Esc)
        self.menuBackup.addAction(self.actionBackup_Database)
        self.menuBackup.addAction(self.action_Excel)
        self.menuInfo.addAction(self.action_4)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menuBackup.menuAction())
        self.menubar.addAction(self.menuInfo.menuAction())
        # Keys  F1
        self.shortcut_f1 = QtWidgets.QShortcut(QtGui.QKeySequence('F1'), self.centralwidget)
        self.shortcut_f1.activated.connect(self.add_spare_part)
        # Key F3
        self.shortcut_f3 = QtWidgets.QShortcut(QtGui.QKeySequence('F3'), self.centralwidget)
        self.shortcut_f3.activated.connect(self.show_edit_from_menu_or_F3)
        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), self.centralwidget)
        self.shortcut_esc.activated.connect(self.quit)

        # Status Bar
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        self.statusBar.showMessage(f"{today}")
        MainWindow.setStatusBar(self.statusBar)
        # progressBar
        self.progressBar = QtWidgets.QProgressBar(MainWindow)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setMinimum(0)
        self.progressBar.hide()
        self.statusBar.addPermanentWidget(self.progressBar)

        self.grouping_btn()
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def show_spare_parts(self, table):
        self.selected_table_label.show()
        self.del_selected_btn.hide()
        self.del_all_btn.hide()
        self.selected_table = table
        self.btn_grp.buttonClicked.connect(self.change_colors_of_pressed_btn)  # αλλαγή χρώματος
        self.data_to_show = get_spare_parts(table)

        self.selected_table_label.setText(f"{table.__tablename__}")
        self.search_line_edit.show()
        self.search_btn.show()
        self.search_btn.setMinimumSize(QtCore.QSize(0, 50))
        # treeWidget

        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setFrameShape(QFrame.WinPanel)
        self.treeWidget.setFrameShadow(QFrame.Plain)

        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setAutoFillBackground(True)
        self.treeWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        # self.treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.treeWidget.setLineWidth(14)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setHeaderLabels(["ID", "Part No", "Περιγραφή", "Κωδικός", "Τεμάχια", "Παρατηρήσεις"])
        # self.treeWidget.setAnimated(True)
        self.treeWidget.header().setStyleSheet(u"background-color: gray;" "color: white;"
                                               "font-style: normal;font-size: 14pt;font-weight: bold;")
        for index, item in enumerate(self.data_to_show):
            self.qitem = TreeWidgetItem(self.treeWidget,
                                        [str(item.ID), str(item.PARTS_NR), item.ΠΕΡΙΓΡΑΦΗ, str(item.ΚΩΔΙΚΟΣ),
                                         str(item.ΤΕΜΑΧΙΑ), item.ΠΑΡΑΤΗΡΗΣΗΣ])
            self.treeWidget.setStyleSheet("QTreeView::item { padding: 10px }")
            self.treeWidget.addTopLevelItem(self.qitem)

        self.treeWidget.setColumnWidth(2, 500)
        # self.treeWidget.resizeColumnToContents(index)
        self.treeWidget.itemDoubleClicked.connect(self.show_edit_spare_part_window)
        self.gridLayout.addWidget(self.treeWidget, 11, 0, 1, 10)

    def show_melanotainies(self, table):
        self.selected_table_label.show()
        self.del_selected_btn.hide()
        self.del_all_btn.hide()
        self.selected_table = table
        self.btn_grp.buttonClicked.connect(self.change_colors_of_pressed_btn)  # αλλαγή χρώματος
        self.data_to_show = get_spare_parts(table)

        self.selected_table_label.setText(f"{table.__tablename__}")
        self.search_line_edit.show()
        self.search_btn.show()
        self.search_btn.setMinimumSize(QtCore.QSize(0, 50))
        # treeWidget
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setFrameShape(QFrame.StyledPanel)
        self.treeWidget.setFrameShadow(QFrame.Sunken)
        self.treeWidget.setLineWidth(2)
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setWordWrap(True)

        self.treeWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setHeaderLabels(["ID", "Εταιρεία", "Ποιότητα", "Αναλώσιμο", "Περιγραφή", "Κωδικός", "Τεμάχια",
                                         "Τιμή", "Σύνολο", "Πελάτες", "Παρατηρήσεις"])
        self.treeWidget.header().setStyleSheet(u"background-color: gray;" "color: white;"
                                               "font-style: normal;font-size: 14pt;font-weight: bold;")
        for index, item in enumerate(self.data_to_show):
            self.qitem = TreeWidgetItem(self.treeWidget,
                                        [str(item.ID), str(item.ΕΤΑΙΡΕΙΑ), item.ΠΟΙΟΤΗΤΑ, str(item.ΑΝΑΛΩΣΙΜΟ),
                                         str(item.ΠΕΡΙΓΡΑΦΗ), item.ΚΩΔΙΚΟΣ, item.ΤΕΜΑΧΙΑ, item.ΤΙΜΗ, item.ΣΥΝΟΛΟ,
                                         item.ΠΕΛΑΤΕΣ, item.ΠΑΡΑΤΗΡΗΣΗΣ])
            self.treeWidget.setStyleSheet("QTreeView::item { padding: 10px }")
            self.treeWidget.addTopLevelItem(self.qitem)
        self.treeWidget.setColumnWidth(4, 500)
        # self.treeWidget.resizeColumnToContents(index)
        self.treeWidget.itemDoubleClicked.connect(self.show_edit_melanotainies_window)
        self.gridLayout.addWidget(self.treeWidget, 11, 0, 1, 10)

    def show_consumables(self, table):
        self.selected_table_label.show()
        self.del_selected_btn.hide()
        self.del_all_btn.hide()
        self.selected_table = table
        self.btn_grp.buttonClicked.connect(self.change_colors_of_pressed_btn)  # αλλαγή χρώματος
        self.data_to_show = get_spare_parts(table)
        self.selected_table_label.setText(f"{table.__tablename__}")
        self.search_line_edit.show()
        self.search_btn.show()
        self.search_btn.setMinimumSize(QtCore.QSize(0, 50))

        # treeWidget

        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setFrameShape(QFrame.StyledPanel)
        self.treeWidget.setFrameShadow(QFrame.Sunken)
        self.treeWidget.setLineWidth(2)
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setAutoFillBackground(True)
        self.treeWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setHeaderLabels(["ID", "Εταιρεία", "Ποιότητα", "Αναλώσιμο", "Περιγραφή", "Κωδικός", "Τεμάχια",
                                         "Τιμή", "Σύνολο", "Σελίδες", "Πελάτες", "Παρατηρήσεις"])
        self.treeWidget.setAnimated(True)
        self.treeWidget.header().setStyleSheet(u"background-color: gray;" "color: white;"
                                               "font-style: normal;font-size: 14pt;font-weight: bold;")
        for index, item in enumerate(self.data_to_show):
            self.qitem = TreeWidgetItem(self.treeWidget,
                                        [str(item.ID), item.ΕΤΑΙΡΕΙΑ, item.ΠΟΙΟΤΗΤΑ, item.ΑΝΑΛΩΣΙΜΟ,
                                         item.ΠΕΡΙΓΡΑΦΗ, item.ΚΩΔΙΚΟΣ, item.ΤΕΜΑΧΙΑ, item.ΤΙΜΗ, item.ΣΥΝΟΛΟ,
                                         item.ΣΕΛΙΔΕΣ, item.ΠΕΛΑΤΕΣ, item.ΠΑΡΑΤΗΡΗΣΗΣ])
            if "C/M/Y" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(4, QtGui.QColor('green'))
                self.qitem.setForeground(4, QtGui.QColor('white'))
            elif "CYAN" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(4, QtGui.QColor('#0517D2'))
                self.qitem.setForeground(4, QtGui.QColor('white'))
            elif "MAGENTA" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(4, QtGui.QColor('#D205CF'))
                self.qitem.setForeground(4, QtGui.QColor('white'))
            elif "YELLOW" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(4, QtGui.QColor('yellow'))
                self.qitem.setForeground(4, QtGui.QColor('black'))
            elif "GRAY" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(4, QtGui.QColor("gray"))
                self.qitem.setForeground(4, QtGui.QColor('white'))
            elif "BLACK" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(4, QtGui.QColor("black"))
                self.qitem.setForeground(4, QtGui.QColor('white'))
            self.treeWidget.setStyleSheet("QTreeView::item { padding: 10px }")
            self.treeWidget.addTopLevelItem(self.qitem)
        self.treeWidget.setColumnWidth(4, 500)
        # self.treeWidget.resizeColumnToContents(index)
        self.treeWidget.itemDoubleClicked.connect(self.show_edit_consumables_window)
        self.gridLayout.addWidget(self.treeWidget, 11, 0, 1, 10)

    def show_orders(self, table):
        self.selected_table_label.show()
        self.selected_table = table
        self.btn_grp.buttonClicked.connect(self.change_colors_of_pressed_btn)  # αλλαγή χρώματος
        self.del_selected_btn.show()
        self.del_all_btn.show()
        self.data_to_show = get_spare_parts(table)
        self.selected_table_label.setText("ΠΑΡΑΓΓΕΛΙΕΣ")
        self.search_line_edit.show()
        self.search_btn.show()
        self.search_btn.setMinimumSize(QtCore.QSize(0, 50))
        # treeWidget
        self.treeWidget = QtWidgets.QTreeWidget(self.centralwidget)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.setFrameShape(QFrame.StyledPanel)
        self.treeWidget.setFrameShadow(QFrame.Sunken)
        self.treeWidget.setLineWidth(2)
        self.treeWidget.setSortingEnabled(True)
        self.treeWidget.setWordWrap(True)
        self.gridLayout.addWidget(self.treeWidget, 11, 0, 1, 10)
        self.treeWidget.setWordWrap(True)
        self.treeWidget.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.treeWidget.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.treeWidget.setAlternatingRowColors(True)
        self.treeWidget.setHeaderLabels(["ID", "Κωδικός", "Ημερομηνία", "Περιγραφή", "Ποιότητα", "Αποτέλεσμα", "Παρατηρήσεις"])
        self.treeWidget.header().setStyleSheet(u"background-color: gray;" "color: white;"
                                               "font-style: normal;font-size: 14pt;font-weight: bold;")
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        for index, item in enumerate(self.data_to_show):
            self.qitem = TreeWidgetItem(self.treeWidget,
                                        [str(item.ID), str(item.ΚΩΔΙΚΟΣ), item.ΗΜΕΡΟΜΗΝΙΑ, str(item.ΠΕΡΙΓΡΑΦΗ),
                                         str(item.ΠΟΙΟΤΗΤΑ), str(item.ΑΠΟΤΕΛΕΣΜΑ), item.ΠΑΡΑΤΗΡΗΣΕΙΣ])
            if "C/M/Y" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(3, QtGui.QColor('green'))
                self.qitem.setForeground(3, QtGui.QColor('white'))
            elif "CYAN" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(3, QtGui.QColor('#0517D2'))
                self.qitem.setForeground(3, QtGui.QColor('white'))
            elif "MAGENTA" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(3, QtGui.QColor('#D205CF'))
                self.qitem.setForeground(3, QtGui.QColor('white'))
            elif "YELLOW" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(3, QtGui.QColor('yellow'))
                self.qitem.setForeground(3, QtGui.QColor('black'))
            elif "GRAY" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(3, QtGui.QColor("gray"))
                self.qitem.setForeground(3, QtGui.QColor('white'))
            elif "BLACK" in item.ΠΕΡΙΓΡΑΦΗ:
                self.qitem.setBackground(3, QtGui.QColor("black"))
                self.qitem.setForeground(3, QtGui.QColor('white'))
            self.qitem.setTextAlignment(4, QtCore.Qt.AlignmentFlag.AlignCenter)
            self.treeWidget.setStyleSheet("QTreeView::item { padding: 10px }")
            self.treeWidget.addTopLevelItem(self.qitem)
        self.treeWidget.setColumnWidth(3, 500)
        self.treeWidget.itemDoubleClicked.connect(self.show_edit_orders_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        self.del_selected_btn.setText(_translate("MainWindow", "Διαγραφή\nεπιλεγμένων"))
        self.selected_table_label.setText(_translate("MainWindow", "Επιλεγμένος Πίνακας"))
        self.del_all_btn.setText(_translate("MainWindow", "   Διαγραφή\n        όλων"))
        self.menu.setTitle(_translate("MainWindow", "Αρχείο"))
        self.menuBackup.setTitle(_translate("MainWindow", "Backup"))
        self.menuInfo.setTitle(_translate("MainWindow", "Info"))
        # self.action.setText(_translate("MainWindow", "Άνοιγμα αρχείου"))
        self.action_F1.setText(_translate("MainWindow", "Προσθήκη  F1"))
        self.actionEdit.setText(_translate("MainWindow", "Επεξεργασία  F3"))
        self.action_3.setText(_translate("MainWindow", "Διαγραφή"))
        self.action_Esc.setText(_translate("MainWindow", "Έξοδος  Esc"))
        self.actionBackup_Database.setText(_translate("MainWindow", "Backup Database"))
        self.action_Excel.setText(_translate("MainWindow", "Εξαγωγή Excel"))
        self.action_4.setText(_translate("MainWindow", "Πληροφορίες"))

    def search(self):
        text_to_search = self.search_line_edit.text()
        if text_to_search == "" or text_to_search == " ":
            return
        self.search_line_edit.clear()
        self.treeWidget.clear()
        if self.selected_table.__tablename__ == "ΜΕΛΑΝΑΚΙΑ" or self.selected_table.__tablename__ == "ΤΟΝΕΡ" \
                or self.selected_table.__tablename__ == "ΦΩΤΟΤΥΠΙΚΑ" or self.selected_table.__tablename__ == "ΜΕΛΑΝΟΤΑΙΝΙΕΣ":
            self.data_to_show = search_on_consumables(self.selected_table, text_to_search)
        elif self.selected_table.__tablename__ == "ΧΧΧ":
            self.data_to_show = search_on_orders(text_to_search)
        else:
            self.data_to_show = search_on_spare_parts(self.selected_table, text_to_search)
        for index, item in enumerate(self.data_to_show):
            if self.selected_table.__tablename__ == "ΜΕΛΑΝΑΚΙΑ" or self.selected_table.__tablename__ == "ΤΟΝΕΡ" \
                    or self.selected_table.__tablename__ == "ΦΩΤΟΤΥΠΙΚΑ":
                self.qitem = TreeWidgetItem(self.treeWidget,
                                                       [str(item.ID), str(item.ΕΤΑΙΡΕΙΑ), item.ΠΟΙΟΤΗΤΑ,
                                                        str(item.ΑΝΑΛΩΣΙΜΟ),
                                                        str(item.ΠΕΡΙΓΡΑΦΗ), item.ΚΩΔΙΚΟΣ, item.ΤΕΜΑΧΙΑ, item.ΤΙΜΗ,
                                                        item.ΣΥΝΟΛΟ,
                                                        item.ΣΕΛΙΔΕΣ, item.ΠΕΛΑΤΕΣ, item.ΠΑΡΑΤΗΡΗΣΗΣ])
                if "C/M/Y" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(4, QtGui.QColor('green'))
                    self.qitem.setForeground(4, QtGui.QColor('white'))
                elif "CYAN" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(4, QtGui.QColor('#0517D2'))
                    self.qitem.setForeground(4, QtGui.QColor('white'))
                elif "MAGENTA" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(4, QtGui.QColor('#D205CF'))
                    self.qitem.setForeground(4, QtGui.QColor('white'))
                elif "YELLOW" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(4, QtGui.QColor('yellow'))
                    self.qitem.setForeground(4, QtGui.QColor('black'))
                elif "GRAY" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(4, QtGui.QColor("gray"))
                    self.qitem.setForeground(4, QtGui.QColor('white'))
                elif "BLACK" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(4, QtGui.QColor("black"))
                    self.qitem.setForeground(4, QtGui.QColor('white'))
                self.treeWidget.addTopLevelItem(self.qitem)
                self.treeWidget.setColumnWidth(4, 500)
                self.treeWidget.resizeColumnToContents(index)
                # Για να μήν ψάχνει το ιδιο string στα επομενα πεδια του ιδου προιόντος
                # πχ αν βρει την λεξει "brother" στο πεδιο ΠΕΡΙΓΡΑΦΗ αν το αφήσουμε να ψαξει και στις
                # ΠΑΡΑΤΗΡΗΣΕΙΣ θα μας βγαλει δυο φορές το ιδιο προιόν στο treeWidget
                # για αυτο κανουμε break το εσωτρεικό loop
                # break
                # ΜΕΛΑΝΟΤΑΙΝΙΕΣ
            elif self.selected_table.__tablename__ == "ΜΕΛΑΝΟΤΑΙΝΙΕΣ":
                self.qitem = TreeWidgetItem(self.treeWidget,
                                                       [str(item.ID), str(item.ΕΤΑΙΡΕΙΑ), item.ΠΟΙΟΤΗΤΑ,
                                                        str(item.ΑΝΑΛΩΣΙΜΟ),
                                                        str(item.ΠΕΡΙΓΡΑΦΗ), item.ΚΩΔΙΚΟΣ, item.ΤΕΜΑΧΙΑ, item.ΤΙΜΗ,
                                                        item.ΣΥΝΟΛΟ,
                                                        item.ΠΕΛΑΤΕΣ, item.ΠΑΡΑΤΗΡΗΣΗΣ])
                self.treeWidget.addTopLevelItem(self.qitem)
                self.treeWidget.setColumnWidth(4, 500)
                self.treeWidget.resizeColumnToContents(index)
                # Για να μήν ψάχνει το ιδιο string στα επομενα πεδια του ιδου προιόντος
                # πχ αν βρει την λεξει "brother" στο πεδιο ΠΕΡΙΓΡΑΦΗ αν το αφήσουμε να ψαξει και στις
                # ΠΑΡΑΤΗΡΗΣΕΙΣ θα μας βγαλει δυο φορές το ιδιο προιόν στο treeWidget
                # για αυτο κανουμε break το εσωτρεικό loop
                # break
            elif self.selected_table.__tablename__ == "ΧΧΧ":
                self.qitem = TreeWidgetItem(self.treeWidget,
                                            [str(item.ID), str(item.ΚΩΔΙΚΟΣ), item.ΗΜΕΡΟΜΗΝΙΑ,
                                             str(item.ΠΕΡΙΓΡΑΦΗ), str(item.ΠΟΙΟΤΗΤΑ), str(item.ΑΠΟΤΕΛΕΣΜΑ), item.ΠΑΡΑΤΗΡΗΣΕΙΣ])
                if "C/M/Y" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(3, QtGui.QColor('green'))
                    self.qitem.setForeground(3, QtGui.QColor('white'))
                elif "CYAN" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(3, QtGui.QColor('#0517D2'))
                    self.qitem.setForeground(3, QtGui.QColor('white'))
                elif "MAGENTA" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(3, QtGui.QColor('#D205CF'))
                    self.qitem.setForeground(3, QtGui.QColor('white'))
                elif "YELLOW" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(3, QtGui.QColor('yellow'))
                    self.qitem.setForeground(3, QtGui.QColor('black'))
                elif "GRAY" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(3, QtGui.QColor("gray"))
                    self.qitem.setForeground(3, QtGui.QColor('white'))
                elif "BLACK" in item.ΠΕΡΙΓΡΑΦΗ:
                    self.qitem.setBackground(3, QtGui.QColor("black"))
                    self.qitem.setForeground(3, QtGui.QColor('white'))
                self.qitem.setTextAlignment(4, QtCore.Qt.AlignCenter)
                self.treeWidget.setStyleSheet("QTreeView::item { padding: 10px }")
                self.treeWidget.addTopLevelItem(self.qitem)
                self.treeWidget.setColumnWidth(3, 500)
                # self.treeWidget.itemDoubleClicked.connect(self.show_edit_orders_window)
            else:
                self.qitem = TreeWidgetItem(self.treeWidget,
                                                       [str(item.ID), str(item.PARTS_NR), item.ΠΕΡΙΓΡΑΦΗ,
                                                        str(item.ΚΩΔΙΚΟΣ),
                                                        str(item.ΤΕΜΑΧΙΑ), item.ΠΑΡΑΤΗΡΗΣΗΣ])
                self.treeWidget.addTopLevelItem(self.qitem)
                self.treeWidget.setColumnWidth(2, 500)
                self.treeWidget.resizeColumnToContents(index)
                # Για να μήν ψάχνει το ίδιο string στα επόμενα πεδία του ιδίου προϊόντος
                # πχ αν βρει την λεξει "brother" στο πεδιο ΠΕΡΙΓΡΑΦΗ αν το αφήσουμε να ψαξει και στις
                # ΠΑΡΑΤΗΡΗΣΕΙΣ θα μας βγαλει δυο φορές το ιδιο προιόν στο treeWidget
                # για αυτο κανουμε break το εσωτρεικό loop
                # break

    def show_edit_spare_part_window(self, item, column):  # column ειναι η στήλη που πατησε κλικ
        item_id = item.text(0)  # item.text(0)  == ID
        # Αν δεν υπάρχει edit_spare_part_window ή αν ο χρήστης εχει κλεισει το παράθυρο απο το Χ πανω δεξια
        # ελεγχουμε αν ειναι ορατο
        if self.edit_spare_part_window is None or not self.edit_spare_part_window.isVisible():
            self.edit_spare_part_window = QWidget()
            self.edit_spare_part_window.setWindowTitle("Επεξεργασία πρώτου ανταλλακτικού")
            self.edit_spare_part = Ui_edit_spare_parts_window()
            self.edit_spare_part.setupUi(self.edit_spare_part_window)  # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
            self.edit_spare_part.selected_id = item_id
            self.edit_spare_part.selected_table = self.selected_table
            self.edit_spare_part.edit_spare_part()  # Εμφάνηση δεδομένων απο την βάση δεδομένων
            self.edit_spare_part.show_file()  # Εμφάνηση Αρχείων
            self.edit_spare_part.window = self.edit_spare_part_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
            self.edit_spare_part_window.show()
            self.edit_spare_part.window_closed.connect(self.refresh_spare_parts)
        elif self.second_edit_spare_part_window is None or not self.second_edit_spare_part_window.isVisible():
            self.second_edit_spare_part_window = QWidget()
            self.second_edit_spare_part_window.setWindowTitle(f"Επεξεργασία δεύτερου ανταλλακτικού")
            self.second_edit_spare_part = Ui_edit_spare_parts_window()
            self.second_edit_spare_part.setupUi(self.second_edit_spare_part_window)  # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
            self.second_edit_spare_part.selected_id = item_id
            self.second_edit_spare_part.selected_table = self.selected_table
            self.second_edit_spare_part.edit_spare_part()  # Εμφάνηση δεδομένων απο την βάση δεδομένων
            self.second_edit_spare_part.show_file()  # Εμφάνηση Αρχείων
            self.second_edit_spare_part.window = self.second_edit_spare_part_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
            self.second_edit_spare_part_window.show()
            self.second_edit_spare_part.window_closed.connect(self.second_refresh_spare_parts)
        else:
            QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Παρακαλώ κλείστε ενα απο τα ανοιχτά παράθυρα "
                                                            f"ανταλλακτικών.")
            return

    def refresh_spare_parts(self):
        self.show_spare_parts(self.selected_table)
        self.edit_spare_part_window.close()
        self.edit_spare_part_window = None

    def second_refresh_spare_parts(self):
        self.show_spare_parts(self.selected_table)
        self.second_edit_spare_part_window.close()
        self.second_edit_spare_part_window = None

    def new_refresh_spare_parts(self):
        self.show_spare_parts(self.selected_table)
        self.new_spare_part_window.close()
        self.new_spare_part_window = None

    def show_edit_consumables_window(self, item, column):
        item_id = item.text(0)  # item.text(0)  == ID# column ειναι η στήλη που πατησε κλικ
        if self.edit_consumables_window is None or not self.edit_consumables_window.isVisible():
            self.edit_consumables_window = QWidget()
            self.edit_consumables_window.setWindowTitle(f"Επεξεργασία πρώτου αναλώσιμου")
            # self.edit_consumables_window.setStyleSheet(u"font: 75 13pt \"Calibri\";") # το παίρνει απο το edit_consumables_window
            self.edit_consumable = Ui_edit_consumables_window()
            # Αρχικοποίηση των κουμπιών, γραμμών επεξεργασίας κτλ π
            self.edit_consumable.setupUi(self.edit_consumables_window)
            self.edit_consumable.selected_id = item_id
            self.edit_consumable.selected_table = self.selected_table
            self.edit_consumable.edit_consumable()  # Εμφάνιση δεδομένων απο τη βάση δεδομένων
            self.edit_consumable.show_file()  # Εμφάνιση Αρχείων
            self.edit_consumable.window = self.edit_consumables_window  # Αν θέλουμε να ανοίγουν πολλά παράθυρα
            self.edit_consumables_window.show()
            self.edit_consumable.window_closed.connect(self.refresh_consumables)
        elif self.second_edit_consumables_window is None or not self.second_edit_consumables_window.isVisible():
            self.second_edit_consumables_window = QWidget()
            self.second_edit_consumables_window.setWindowTitle(f"Επεξεργασία δεύτερου αναλώσιμου")
            # self.second_edit_consumables_window.setStyleSheet(u"font: 75 13pt \"Calibri\";")
            self.second_edit_consumable = Ui_edit_consumables_window()
            # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
            self.second_edit_consumable.setupUi(self.second_edit_consumables_window)
            self.second_edit_consumable.selected_id = item_id
            self.second_edit_consumable.selected_table = self.selected_table
            self.second_edit_consumable.edit_consumable()  # Εμφάνηση δεδομένων απο την βάση δεδομένων
            self.second_edit_consumable.show_file()  # Εμφάνηση Αρχείων
            self.second_edit_consumable.window = self.second_edit_consumables_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
            self.second_edit_consumables_window.show()
            self.second_edit_consumable.window_closed.connect(self.second_refresh_consumables)
        elif self.third_edit_consumables_window is None or not self.third_edit_consumables_window.isVisible():
            self.third_edit_consumables_window = QWidget()
            self.third_edit_consumables_window.setWindowTitle(f"Επεξεργασία τρίτου αναλώσιμου")
            # self.third_edit_consumables_window.setStyleSheet(u"font: 75 13pt \"Calibri\";")
            self.third_edit_consumable = Ui_edit_consumables_window()
            # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
            self.third_edit_consumable.setupUi(self.third_edit_consumables_window)
            self.third_edit_consumable.selected_id = item_id
            self.third_edit_consumable.selected_table = self.selected_table
            self.third_edit_consumable.edit_consumable()  # Εμφάνηση δεδομένων απο την βάση δεδομένων
            self.third_edit_consumable.show_file()  # Εμφάνηση Αρχείων
            self.third_edit_consumable.window = self.third_edit_consumables_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
            self.third_edit_consumables_window.show()
            self.third_edit_consumable.window_closed.connect(self.third_refresh_consumables)
        else:
            QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Παρακαλώ κλείστε ενα απο τα ανοιχτά παράθυρα\n απο τα "
                                                            f"αναλώσιμα")
            return

    def refresh_consumables(self):
        self.show_consumables(self.selected_table)
        self.edit_consumables_window.close()
        self.edit_consumables_window = None

    def second_refresh_consumables(self):
        self.show_consumables(self.selected_table)
        self.second_edit_consumables_window.close()
        self.second_edit_consumables_window = None

    def third_refresh_consumables(self):
        self.show_consumables(self.selected_table)
        self.third_edit_consumables_window.close()
        self.third_edit_consumables_window = None

    def new_refresh_consumables(self):
        self.show_consumables(self.selected_table)
        self.new_consumables_window.close()
        self.new_consumables_window = None

    def show_edit_melanotainies_window(self, item, column):  # column ειναι η στήλη που πατησε κλικ
        item_id = item.text(0)  # item.text(0)  == ID
        if self.edit_melanotainies_window is None or not self.edit_melanotainies_window.isVisible():
            self.edit_melanotainies_window = QWidget()
            self.edit_melanotainies_window.setWindowTitle("Επεξεργασία πρώτης μελανοταινίας")
            # self.edit_melanotainies_window.setStyleSheet(u"font: 75 13pt \"Calibri\";")
            self.edit_melanotainia = Ui_edit_melanotainies_window()
            self.edit_melanotainia.setupUi(
                self.edit_melanotainies_window)  # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
            self.edit_melanotainia.selected_id = item_id
            self.edit_melanotainia.selected_table = self.selected_table
            self.edit_melanotainia.edit_melanotainia()  # Εμφάνηση δεδομένων απο την βάση δεδομένων
            self.edit_melanotainia.show_file()  # Εμφάνηση Αρχείων
            self.edit_melanotainia.window = self.edit_melanotainies_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
            self.edit_melanotainies_window.show()
            self.edit_melanotainia.window_closed.connect(self.refresh_melanotainies)
        elif self.second_edit_melanotainies_window is None or not self.second_edit_melanotainies_window.isVisible():
            self.second_edit_melanotainies_window = QWidget()
            self.second_edit_melanotainies_window.setWindowTitle("Επεξεργασία δεύτερης μελανοταινίας")
            self.second_edit_melanotainies_window.setStyleSheet(u"font: 75 13pt \"Calibri\";")
            self.second_edit_melanotainia = Ui_edit_melanotainies_window()
            self.second_edit_melanotainia.setupUi(
                self.second_edit_melanotainies_window)  # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
            self.second_edit_melanotainia.selected_id = item_id
            self.second_edit_melanotainia.selected_table = self.selected_table
            self.second_edit_melanotainia.edit_melanotainia()  # Εμφάνηση δεδομένων απο την βάση δεδομένων
            self.second_edit_melanotainia.show_file()  # Εμφάνηση Αρχείων
            self.second_edit_melanotainia.window = self.second_edit_melanotainies_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
            self.second_edit_melanotainies_window.show()
            self.second_edit_melanotainia.window_closed.connect(self.second_refresh_melanotainies)
        else:
            QtWidgets.QMessageBox.warning(None, "Προσοχή!", f"Παρακαλώ κλείστε ενα απο τα ανοιχτά παράθυρα\n απο τις "
                                                            f"μελανοταινίες.")
            return

    def refresh_melanotainies(self):
        self.show_melanotainies(self.selected_table)
        self.edit_melanotainies_window.close()
        self.edit_melanotainies_window = None

    def second_refresh_melanotainies(self):
        self.show_melanotainies(self.selected_table)
        self.second_edit_melanotainies_window.close()
        self.second_edit_melanotainies_window = None

    def new_refresh_melanotainies(self):
        self.show_melanotainies(self.selected_table)
        self.new_melanotainies_window.close()
        self.new_melanotainies_window = None

    def show_edit_orders_window(self, item, column):  # column ειναι η στήλη που πατησε κλικ
        item_id = item.text(0)
        if self.edit_orders_window is None or not self.edit_orders_window.isVisible():
            self.edit_orders_window = QWidget()
            self.edit_orders_window.setWindowTitle("Επεξεργασία πρώτης παραγγελίας")
            self.edit_orders = Ui_edit_orders_window()
            self.edit_orders.setupUi(self.edit_orders_window)  # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
            self.edit_orders.selected_id = item_id
            self.edit_orders.selected_table = self.selected_table
            self.edit_orders.edit_order()  # Εμφάνηση δεδομένων απο την βάση δεδομένων
            self.edit_orders.show_file()  # Εμφάνηση Αρχείων
            self.edit_orders.window = self.edit_orders_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
            self.edit_orders_window.show()
            self.edit_orders.window_closed.connect(self.refresh_orders)
        elif self.second_edit_orders_window is None or not self.second_edit_orders_window.isVisible():
            self.second_edit_orders_window = QWidget()
            self.second_edit_orders_window.setWindowTitle("Επεξεργασία δεύτερης παραγγελίας")
            self.second_edit_orders = Ui_edit_orders_window()
            self.second_edit_orders.setupUi(
                self.second_edit_orders_window)  # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
            self.second_edit_orders.selected_id = item_id
            self.second_edit_orders.selected_table = self.selected_table
            self.second_edit_orders.edit_order()  # Εμφάνηση δεδομένων απο την βάση δεδομένων
            self.second_edit_orders.show_file()  # Εμφάνηση Αρχείων
            self.second_edit_orders.window = self.second_edit_orders_window  # Αν θέλουμε να ανοιγουν πολλα παράθυρα
            self.second_edit_orders_window.show()
            self.second_edit_orders.window_closed.connect(self.second_refresh_orders)
        else:
            QtWidgets.QMessageBox.warning(None, "Προσοχή!", f"Παρακαλώ κλείστε ενα απο τα ανοιχτά παράθυρα\n απο τις "
                                                            f"παραγγελίες.")
            return

    def refresh_orders(self):
        self.show_orders(self.selected_table)
        self.edit_orders_window.close()  # Να μήν κλείνει το παράθυρο γιατι κλεινει λαθος παράθυρο καμια φορά
        self.edit_orders_window = None

    def second_refresh_orders(self):
        self.show_orders(self.selected_table)
        self.second_edit_orders_window.close()  # Να μήν κλείνει το παράθυρο γιατι κλεινει λαθος παράθυρο καμια φορά
        self.second_edit_orders_window = None

    def new_refresh_orders(self):
        self.show_orders(self.selected_table)
        self.new_orders_window.close()  # Να μήν κλείνει το παράθυρο γιατι κλεινει λαθος παράθυρο καμια φορά
        self.new_orders_window = None

    def delete_orders(self):
        answer = QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Σίγουρα θέλετε να διαγράψετε όλες τις παραγγελίες;",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            all_orders = session.query(Orders)
            for order in all_orders:
                session.delete(order)
            session.commit()
            QtWidgets.QMessageBox.information(None, 'Πληροφορία', f"Όλες οι παραγγελίες διαγράφηκαν!")
            self.show_orders(self.selected_table)

    def delete_selected_orders(self):
        items = self.treeWidget.selectedItems()
        items_ids = []
        for item in items:
            items_ids.append(item.text(0))  # item.text(0) ==> ID
        answer = QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Σίγουρα θέλετε να διαγράψετε αυτές τις παραγγελίες;",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:

            for item_id in items_ids:
                item_to_delete = session.get(Orders, item_id)
                session.delete(item_to_delete)

                # Διαγράφει αρχείων απο προϊόντα που δεν είναι στην αποθήκη
                # shutil.rmtree(path, ignore_errors=False, onerror=None,  dir_fd=None)
                try:
                    self.images_path = os.path.abspath(os.path.join(BASE_PATH, f"2.  ΑΠΟΘΗΚΗ\\SpareParts_images\\ΧΧΧ\\{item_id}"))
                    shutil.rmtree(str(self.images_path), ignore_errors=True, onerror=None, dir_fd=None)
                    self.images_path = None
                except Exception as error:
                    QtWidgets.QMessageBox.critical(None, 'Προσοχή', f"Δεν διαγράφτηκαν τα αρχεία απο το {self.images_path}!\n{error}")

            session.commit()

            QtWidgets.QMessageBox.information(None, 'Πληροφορία', f"Oι παραγγελίες διαγράφηκαν!")
            self.show_orders(self.selected_table)

    def grouping_btn(self):

        up_btn = [self.brother_btn, self.canon_btn, self.epson_btn, self.konica_btn, self.kyocera_btn, self.lexmark_btn,
                  self.oki_btn, self.ricoh_btn, self.samsung_btn, self.sharp_btn]
        down_btn = [self.melanakia_btn, self.melanotainies_btn, self.toner_btn, self.copiers_btn, self.orders_btn]
        all_btn = up_btn + down_btn
        # Grouping buttons
        self.btn_grp = QtWidgets.QButtonGroup()
        self.btn_grp.setExclusive(True)
        for btn in all_btn:
            self.btn_grp.addButton(btn)

    def change_colors_of_pressed_btn(self, pressed_btn):
        up_btn = [self.brother_btn, self.canon_btn, self.epson_btn, self.konica_btn, self.kyocera_btn, self.lexmark_btn,
                  self.oki_btn, self.ricoh_btn, self.samsung_btn, self.sharp_btn]
        down_btn = [self.melanakia_btn, self.melanotainies_btn, self.toner_btn, self.copiers_btn, self.orders_btn]
        all_btn = up_btn + down_btn

        # pressed_btn.setStyleSheet(
        #     f"image: url(icons/{self.selected_table_label.text()}.png);" "background-color: #aaff7f;" "color: white;" "border-style: outset;" "border-width: 2px;" \
        #     "border-radius: 15px;" "border-color: black;" "padding: 4px;")
        pressed_btn.setStyleSheet(
            f"background-color: #50f333;" "color: white;"
            "border-style: outset;" "border-width: 2px;" "border-radius: 15px;" "border-color: black;" "padding: 4px;")

        # self.selected_table_label.setStyleSheet(f"image: url(icons/{self.selected_table_label.text()}.png);"
        # "background-color: #aaff7f;" "color: white;" "border-style: outset;" "border-width: 2px;" \ "border-radius:
        # 15px;" "border-color: black;" "padding: 4px;") self.selected_table_label.setText("") needed
        for btn in all_btn:
            if btn in up_btn and btn != pressed_btn:

                # btn.setStyleSheet(
                #     f"image: url(icons/{btn.whatsThis()});" "background-color: #fff;" "color: white;" "border-style: outset;" "border-width: 2px;" \
                #     "border-radius: 15px;" "border-color: black;" "padding: 4px;")
                btn.setStyleSheet(
                    f"background-color: #fff;" "color: white;"
                    "border-style: outset;" "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                    "padding: 4px;")
            elif btn in down_btn and btn != pressed_btn:
                # btn.setStyleSheet(
                #     f"image: url(icons/{btn.whatsThis()});" "background-color: #ffb907;" "color: white;" "border-style: outset;" "border-width: 2px;" \
                #     "border-radius: 15px;" "border-color: black;" "padding: 4px;")
                btn.setStyleSheet(
                    f"background-color: #ffb907;" "color: white;"
                    "border-style: outset;" "border-width: 2px;" "border-radius: 15px;" "border-color: black;"
                    "padding: 4px;")

    def add_spare_part(self):
        if self.selected_table is None:
            QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Πρέπει πρώτα να επιλέξετε πίνακα!")
            return
        if self.selected_table_label.text() == "ΠΑΡΑΓΓΕΛΙΕΣ":
            if self.new_orders_window is not None and self.new_orders_window.isVisible():
                QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Έχετε ήδη ανοιχτό παράθυρο προσθήκης παραγγελίας\n"
                                                                f"Παρακαλώ κλείστε πρώτα το παράθυρο προσθήκης "
                                                                f"παραγγελίας")
                return
            else:
                self.new_orders_window = QWidget()
                self.new_orders_window.setWindowTitle(f"Προσθήκη παραγγελίας")
                self.new_order = Ui_edit_orders_window()
                self.new_order.setupUi(self.new_orders_window)  # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
                self.new_order.selected_table = self.selected_table
                self.new_order.hide_buttons()  # Απόκρυψη κουμπιών αρχείου
                # self.edit_orders.show_file()  # Εμφάνιση Αρχείων
                self.new_order.window = self.new_orders_window
                self.new_orders_window.show()
                self.new_order.window_closed.connect(self.new_refresh_orders)

        elif self.selected_table_label.text() == "ΜΕΛΑΝΑΚΙΑ" or self.selected_table_label.text() == "ΤΟΝΕΡ" \
                or self.selected_table_label.text() == "ΦΩΤΟΤΥΠΙΚΑ":
            if self.new_consumables_window is not None and self.new_consumables_window.isVisible():
                QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Έχετε ήδη ανοιχτό παράθυρο προσθήκης αναλώσιμου\n"
                                                                f"Παρακαλώ κλείστε πρώτα το παράθυρο προσθήκης "
                                                                f"αναλώσιμου")
                return
            else:
                self.new_consumables_window = QWidget()
                self.new_consumables_window.setWindowTitle(f"Προσθήκη {self.selected_table_label.text()}")
                # self.new_consumables_window.setStyleSheet(u"font: 75 13pt \"Calibri\";")
                self.new_consumable = Ui_edit_consumables_window()
                self.new_consumable.setupUi(self.new_consumables_window)  # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
                self.new_consumable.selected_table = self.selected_table
                self.new_consumable.hide_buttons()  # Εμφάνηση δεδομένων απο την βάση δεδομένων
                self.new_consumable.window = self.new_consumables_window
                self.new_consumables_window.show()
                self.new_consumable.window_closed.connect(self.new_refresh_consumables)

        elif self.selected_table_label.text() == "ΜΕΛΑΝΟΤΑΙΝΙΕΣ":
            if self.new_melanotainies_window is not None and self.new_melanotainies_window.isVisible():
                QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Έχετε ήδη ανοιχτό παράθυρο προσθήκης "
                                                                f"μελανοταινίας\n"
                                                                f"Παρακαλώ κλείστε πρώτα το παράθυρο προσθήκης "
                                                                f"μελανοταινίας")
                return
            else:
                self.new_melanotainies_window = QWidget()
                self.new_melanotainies_window.setWindowTitle("Προσθήκη μελανοταινίας")
                self.new_melanotainies_window.setStyleSheet(u"font: 75 13pt \"Calibri\";")
                self.new_melanotainia = Ui_edit_melanotainies_window()
                self.new_melanotainia.setupUi(self.new_melanotainies_window)  # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
                self.new_melanotainia.selected_table = self.selected_table
                self.new_melanotainia.hide_buttons()  # Hide buttons
                # self.edit_melanotainia.show_file()  # Εμφάνηση Αρχείων
                self.new_melanotainia.window = self.new_melanotainies_window
                self.new_melanotainies_window.show()
                self.new_melanotainia.window_closed.connect(self.new_refresh_melanotainies)
        else:
            # Αν δεν είναι None και είναι ορατό τοτε ο χρήστης πρεπει να κλεισει το παράθυρο πριν ανοιξει αλλο
            if self.new_spare_part_window is not None and self.new_spare_part_window.isVisible():
                # Ελεγχος αν υπαρχει και δεν ειναι ορατό --> οταν ο χρήστης παταει Χ πανω δεξια
                QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Έχετε ήδη ανοιχτό παράθυρο προσθήκης ανταλλακτικού\n"
                                                                f"Παρακαλώ κλείστε πρώτα το παράθυρο προσθήκης "
                                                                f"ανταλλακτικού")
                return
            else:
                self.new_spare_part_window = QWidget()
                self.new_spare_part_window.setWindowTitle(f"Προσθήκη {self.selected_table_label.text()} ανταλλακτικού")
                self.new_spare_part = Ui_edit_spare_parts_window()
                self.new_spare_part.setupUi(self.new_spare_part_window)  # Αρχικοποιηση των κουμπιων, γραμμων επεξεργασίας κτλπ
                self.new_spare_part.selected_table = self.selected_table
                self.new_spare_part.hide_buttons()  # Hide buttons
                # self.edit_spare_part.show_file()  # Εμφάνηση Αρχείων
                self.new_spare_part.window = self.new_spare_part_window
                self.new_spare_part_window.show()
                self.new_spare_part.window_closed.connect(self.new_refresh_spare_parts)

    def quit(self, *args):
        answer = QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Σίγουρα θέλετε να κλείσεται την αποθήκη;",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            # self.close()
            sys.exit(app.exec_())
        else:
            return

    def show_edit_from_menu_or_F3(self, *args):  # args ==> (False,)
        if self.selected_table is None:
            QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Πρέπει πρώτα να επιλέξετε πίνακα!")
            return
        elif self.treeWidget.currentItem() is None:
            QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Παρακαλώ επιλέξτε πρώτα αντικείμενο!")
            return
        elif self.selected_table is Melanotainies:
            self.show_edit_melanotainies_window(self.treeWidget.currentItem(), 0)  # 0 ==> column
        elif self.selected_table is Melanakia or self.selected_table is Toner or self.selected_table is Copiers:
            self.show_edit_consumables_window(self.treeWidget.currentItem(), 0)
        elif self.selected_table is Orders:
            self.show_edit_orders_window(self.treeWidget.currentItem(), 0)
        else:
            self.show_edit_spare_part_window(self.treeWidget.currentItem(), 0)

    def backup(self):
        filename = os.path.basename(DB)
        file_whithout_extension = os.path.splitext(filename)
        extension = pathlib.Path(filename).suffix
        today_str = today.replace('/', '-')
        try:
            #  file_to_save == ('/home/dannys/Desktop/add_files.png', '')
            file_to_save = QtWidgets.QFileDialog.getSaveFileName(self, 'Αποθήκευση αρχείου',
                                                                 f'{file_whithout_extension[0]}'
                                                                 + '_backup_' + f"{today_str}" + f'{extension}')

            if file_to_save[0] == "":  # file_to_save == ('', '') αν πατήση ακυρο ο χρήστης
                return

            shutil.copy(os.path.abspath(DB), file_to_save[0], follow_symlinks=False)
            QtWidgets.QMessageBox.information(None, "Επιτυχία", f'Το αρχεία {file_to_save[0]} αποθηκεύτηκε '
                                                                f'επιτυχώς')
        except TypeError:  # Αν δεν πατησει αποθήκευση
            return

    def info(self):
        QtWidgets.QMessageBox.about(None, 'Σχετικά',
                                    f"""Author     : Jordanis Ntini<br>
                                    Copyright  : Copyright © 2021<br>
                                    Credits    : ['Athanasia Tzampazi']<br>
                                    Version    : '{VERSION}'<br>
                                    Maintainer : Jordanis Ntini<br>
                                    Email      : ntinisiordanis@gmail.com<br>
                                    Status     : Development<br>
                                    Language   : <a href='https://www.python.org/'>Python</a><br>
                                    Gui        : <a href='https://pypi.org/project/PyQt5/'>PyQt5</a>""")

    def delete_selected_item(self):
        if self.selected_table is None:
            QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Πρέπει πρώτα να επιλέξετε πίνακα!")
            return
        elif self.treeWidget.currentItem() is None:
            QtWidgets.QMessageBox.warning(None, 'Προσοχή!', f"Παρακαλώ επιλέξτε πρώτα αντικείμενο!")
            return
        elif self.selected_table is Melanotainies:
            item = self.treeWidget.selectedItems()
            item_id = item[0].text(0)  # item[0].text(0) ==> ID  item[0].text(5) ==> Κωδικός απο το treewidget
            answer = QtWidgets.QMessageBox.warning(None, 'Προσοχή!',
                                                   f"Σίγουρα θέλετε να διαγράψετε τον κωδικό {item[0].text(5)}\n "
                                                   f"{item[0].text(4)}\n"
                                                   f"απο τον πίνακα {self.selected_table_label.text()};",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                item_to_delete = session.get(self.selected_table, item_id)
                session.delete(item_to_delete)
                session.commit()
                QtWidgets.QMessageBox.information(None, 'Πληροφορία', f"O κωδικός {item[0].text(5)}\n"
                                                                      f" διαγράφηκε!"
                                                                      f"απο τον πίνακα {self.selected_table_label.text()}")
                self.show_melanotainies(self.selected_table)

        elif self.selected_table is Melanakia or self.selected_table is Toner or self.selected_table is Copiers:
            item = self.treeWidget.selectedItems()
            item_id = item[0].text(0)  # item[0].text(0) ==> ID  item[0].text(5) ==> Κωδικός απο το treewidget
            answer = QtWidgets.QMessageBox.warning(None, 'Προσοχή!',
                                                   f"Σίγουρα θέλετε να διαγράψετε τον κωδικό {item[0].text(5)}\n "
                                                   f"{item[0].text(4)}\n"
                                                   f"απο τον πίνακα {self.selected_table_label.text()};",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                item_to_delete = session.get(self.selected_table, item_id)
                session.delete(item_to_delete)
                session.commit()
                QtWidgets.QMessageBox.information(None, 'Πληροφορία', f"O κωδικός {item[0].text(5)}\n"
                                                                      f" διαγράφηκε!"
                                                                      f"απο τον πίνακα {self.selected_table_label.text()}")
            self.show_consumables(self.selected_table)
        elif self.selected_table is Orders:
            item = self.treeWidget.selectedItems()
            item_id = item[0].text(0)  # item[0].text(0) ==> ID  item[0].text(5) ==> Κωδικός απο το treewidget
            answer = QtWidgets.QMessageBox.warning(None, 'Προσοχή!',
                                                   f"Σίγουρα θέλετε να διαγράψετε τον κωδικό {item[0].text(1)}\n "
                                                   f"{item[0].text(3)}\n"
                                                   f"απο τον πίνακα {self.selected_table_label.text()};",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                item_to_delete = session.get(self.selected_table, item_id)
                session.delete(item_to_delete)
                session.commit()
                QtWidgets.QMessageBox.information(None, 'Πληροφορία', f"O κωδικός {item[0].text(1)}\n"
                                                                      f" διαγράφηκε!"
                                                                      f"απο τον πίνακα {self.selected_table_label.text()} και τα αρχεία")

            self.show_orders(self.selected_table)

        else:
            item = self.treeWidget.selectedItems()
            item_id = item[0].text(0)  # item[0].text(0) ==> ID  item[0].text(5) ==> Κωδικός απο το treewidget
            answer = QtWidgets.QMessageBox.warning(None, 'Προσοχή!',
                                                   f"Σίγουρα θέλετε να διαγράψετε τον κωδικό {item[0].text(3)}\n "
                                                   f"{item[0].text(2)}\n"
                                                   f"απο τον πίνακα {self.selected_table_label.text()};",
                                                   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                   QtWidgets.QMessageBox.No)
            if answer == QtWidgets.QMessageBox.Yes:
                item_to_delete = session.get(self.selected_table, item_id)
                session.delete(item_to_delete)
                session.commit()
                QtWidgets.QMessageBox.information(None, 'Πληροφορία', f"O κωδικός {item[0].text(3)}\n"
                                                                      f" διαγράφηκε!"
                                                                      f"απο τον πίνακα {self.selected_table_label.text()}")
            self.show_spare_parts(self.selected_table)

    def to_excel(self):

        needed_tables = [Brother, Canon, Epson, Konica, Kyocera, Lexmark, Oki, Ricoh, Samsung, Sharp, Melanakia,
                         Melanotainies, Toner, Copiers]
        data_frames = []

        filename = os.path.basename(DB)
        file_whithout_extension = os.path.splitext(filename)
        today_str = today.replace('/', '-')
        # try:
        #  file_to_save == ('/home/dannys/Desktop/add_files.png', '')
        file_to_save = QtWidgets.QFileDialog.getSaveFileName(self, 'Αποθήκευση αρχείου',
                                                             f'{file_whithout_extension[0]}'
                                                             + f"_{today_str}" + '.xlsx')
        if file_to_save[0] == "":  # file_to_save == ('', '') αν πατήση ακυρο ο χρήστης
            return
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter(file_to_save[0], engine="xlsxwriter")
        for table in needed_tables:
            df_query = select([table])
            df_data = pd.read_sql(df_query, con=conn)
            df_data.to_excel(writer, sheet_name=table.__tablename__, index=False)
        writer.save()
        QtWidgets.QMessageBox.information(None, "Επιτυχία", f'Το αρχεία {file_to_save[0]} αποθηκεύτηκε '
                                                            f'επιτυχώς')
        if sys.platform == "win32":
            os.startfile(file_to_save[0])
        else:
            file_to_open = str(file_to_save[0])
            subprocess.Popen(['libreoffice', file_to_open])


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setStyleSheet(u"font: 75 13pt \"Calibri\";")
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
