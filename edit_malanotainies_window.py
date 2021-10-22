# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_consumables_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import sys
import subprocess
import os
import shutil
import pathlib  # Για αποθήκευση αρχείου να πάρουμε μόνο την κατάληξει .svg.png
from settings import today, root_logger, SPARE_PARTS_ROOT
import sqlalchemy
from sqlalchemy.sql import exists
import traceback
from db import Orders, session

from PyQt5 import QtCore, QtGui, QtWidgets
# --------------Log Files----------------------
# log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info

class Ui_edit_melanotainies_window(QtWidgets.QMainWindow):  # Πρέπει να κληρονομήσει απο QMainWindow for pyqtSignal to work
    window_closed = QtCore.pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self, *args, **kwargs):
        super(Ui_edit_melanotainies_window, self).__init__(*args, **kwargs)
        self.selected_id = None
        self.selected_table = None
        self.window = None
        self.item = None
        self.part_no = None
        self.description = None
        self.code = None
        self.pieces = None
        self.comments = None
        self.images_path = None
        self.files = None
        self.file = None  # αρχείο που εμφανίζεται
        self.file_index = None  # Δικτης για το ποιο αρχείο εμφανίζεται

    def setupUi(self, edit_melanotainies_window):
        edit_melanotainies_window.setObjectName("edit_melanotainies_window")
        edit_melanotainies_window.resize(1000, 535)
        self.gridLayout = QtWidgets.QGridLayout(edit_melanotainies_window)
        self.gridLayout.setObjectName("gridLayout")
        # image
        self.image_label = QtWidgets.QLabel(edit_melanotainies_window)
        self.image_label.setText("")
        self.image_label.setSizeIncrement(QtCore.QSize(1, 1))
        self.image_label.setText("")
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setObjectName("image_label")
        self.gridLayout.addWidget(self.image_label, 0, 3, 16, 4)
        # Εταιρεία
        self.company_label = QtWidgets.QLabel(edit_melanotainies_window)
        self.company_label.setObjectName("company_label")
        self.gridLayout.addWidget(self.company_label, 0, 0, 1, 1)
        self.company_lineEdit = QtWidgets.QLineEdit(edit_melanotainies_window)
        self.company_lineEdit.setObjectName("company_lineEdit")
        self.gridLayout.addWidget(self.company_lineEdit, 1, 0, 1, 1)
        # Ποιότητα
        self.quality_label = QtWidgets.QLabel(edit_melanotainies_window)
        self.quality_label.setObjectName("quality_label")
        self.gridLayout.addWidget(self.quality_label, 0, 1, 1, 1)
        self.quality_lineEdit = QtWidgets.QLineEdit(edit_melanotainies_window)
        self.quality_lineEdit.setObjectName("quality_lineEdit")
        self.gridLayout.addWidget(self.quality_lineEdit, 1, 1, 1, 2)
        # Αναλώσιμο
        self.cosumable_label = QtWidgets.QLabel(edit_melanotainies_window)
        self.cosumable_label.setObjectName("cosumable_label")
        self.gridLayout.addWidget(self.cosumable_label, 2, 0, 1, 1)
        self.consumable_lineEdit = QtWidgets.QLineEdit(edit_melanotainies_window)
        self.consumable_lineEdit.setObjectName("consumable_lineEdit")
        self.gridLayout.addWidget(self.consumable_lineEdit, 3, 0, 1, 1)
        # Τεμάχια
        self.pieces_label = QtWidgets.QLabel(edit_melanotainies_window)
        self.pieces_label.setObjectName("pieces_label")
        self.gridLayout.addWidget(self.pieces_label, 2, 1, 1, 1)
        self.pieces_lineEdit = QtWidgets.QLineEdit(edit_melanotainies_window)
        self.pieces_lineEdit.setObjectName("pieces_lineEdit")
        self.gridLayout.addWidget(self.pieces_lineEdit, 3, 1, 1, 2)
        # Περιγραφή
        self.description_label = QtWidgets.QLabel(edit_melanotainies_window)
        self.description_label.setObjectName("description_label")
        self.gridLayout.addWidget(self.description_label, 4, 0, 1, 1)
        self.description_textEdit = QtWidgets.QTextEdit(edit_melanotainies_window)
        self.description_textEdit.setObjectName("description_textEdit")
        self.gridLayout.addWidget(self.description_textEdit, 5, 0, 1, 1)
        # Πελάτες
        self.customers_label = QtWidgets.QLabel(edit_melanotainies_window)
        self.customers_label.setObjectName("customers_label")
        self.gridLayout.addWidget(self.customers_label, 4, 1, 1, 1)
        self.customers_textEdit = QtWidgets.QTextEdit(edit_melanotainies_window)
        self.customers_textEdit.setObjectName("customers_textEdit")
        self.gridLayout.addWidget(self.customers_textEdit, 5, 1, 1, 2)
        # Κωδικός
        self.code_label = QtWidgets.QLabel(edit_melanotainies_window)
        self.code_label.setObjectName("code_label")
        self.gridLayout.addWidget(self.code_label, 8, 0, 1, 1)
        self.code_lineEdit = QtWidgets.QLineEdit(edit_melanotainies_window)
        self.code_lineEdit.setObjectName("code_lineEdit")
        self.gridLayout.addWidget(self.code_lineEdit, 9, 0, 1, 1)
        # Τιμή
        self.price_label = QtWidgets.QLabel(edit_melanotainies_window)
        self.price_label.setObjectName("price_label")
        self.gridLayout.addWidget(self.price_label, 8, 1, 1, 1)
        self.price_lineEdit = QtWidgets.QLineEdit(edit_melanotainies_window)
        self.price_lineEdit.setObjectName("price_lineEdit")
        self.gridLayout.addWidget(self.price_lineEdit, 9, 1, 1, 1)
        # Σύνολο
        self.total_label = QtWidgets.QLabel(edit_melanotainies_window)
        self.total_label.setObjectName("total_label")
        self.gridLayout.addWidget(self.total_label, 10, 0, 1, 1)
        self.total_lineEdit = QtWidgets.QLineEdit(edit_melanotainies_window)
        self.total_lineEdit.setObjectName("total_lineEdit")
        self.total_lineEdit.setReadOnly(True)
        self.gridLayout.addWidget(self.total_lineEdit, 11, 0, 1, 1)
        # Παρατηρήσης
        self.comments_label = QtWidgets.QLabel(edit_melanotainies_window)
        self.comments_label.setObjectName("comments_label")
        self.gridLayout.addWidget(self.comments_label, 14, 0, 1, 1)
        self.comments_lineEdit = QtWidgets.QLineEdit(edit_melanotainies_window)
        self.comments_lineEdit.setObjectName("comments_lineEdit")
        self.gridLayout.addWidget(self.comments_lineEdit, 16, 0, 1, 3)
        # Αποθήκευση
        self.save_btn = QtWidgets.QToolButton(edit_melanotainies_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_btn.sizePolicy().hasHeightForWidth())
        self.save_btn.setSizePolicy(sizePolicy)
        self.save_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.save_btn.setMinimumSize(QtCore.QSize(16777215, 30))
        self.save_btn.setStyleSheet("background-color: rgb(0, 255, 0);")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_changes)
        self.gridLayout.addWidget(self.save_btn, 17, 0, 2, 3)
        # Προσθήκη παραγγελίας
        self.orders_btn = QtWidgets.QToolButton(edit_melanotainies_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.orders_btn.sizePolicy().hasHeightForWidth())
        self.orders_btn.setSizePolicy(sizePolicy)
        self.orders_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.orders_btn.setMinimumSize(QtCore.QSize(16777215, 30))
        self.orders_btn.setStyleSheet(
            "font: 75 14pt \"Calibri\";\n""color: rgb(255, 255, 255);\n""background-color: rgb(85, 85, 255);")
        self.orders_btn.setObjectName("orders_btn")
        self.orders_btn.clicked.connect(self.send_to_orders)
        self.gridLayout.addWidget(self.orders_btn, 19, 0, 1, 3)
        # Προηγούμενη
        self.previous_btn = QtWidgets.QToolButton(edit_melanotainies_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previous_btn.sizePolicy().hasHeightForWidth())
        self.previous_btn.setSizePolicy(sizePolicy)
        self.previous_btn.setMinimumSize(QtCore.QSize(120, 20))
        self.previous_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.previous_btn.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.previous_btn.setObjectName("previous_btn")
        self.previous_btn.clicked.connect(self.previous_file)
        self.gridLayout.addWidget(self.previous_btn, 17, 4, 1, 1)
        # Επόμενη
        self.next_btn = QtWidgets.QToolButton(edit_melanotainies_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.next_btn.sizePolicy().hasHeightForWidth())
        self.next_btn.setSizePolicy(sizePolicy)
        self.next_btn.setMinimumSize(QtCore.QSize(120, 20))
        self.next_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.next_btn.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.next_btn.setObjectName("next_btn")
        self.next_btn.clicked.connect(self.next_file)
        self.gridLayout.addWidget(self.next_btn, 17, 5, 1, 1)
        # Προσθήκη αρχείου
        self.add_file_btn = QtWidgets.QToolButton(edit_melanotainies_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_file_btn.sizePolicy().hasHeightForWidth())
        self.add_file_btn.setSizePolicy(sizePolicy)
        self.add_file_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.add_file_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "background-color: rgb(0, 170, 127);")
        self.add_file_btn.setObjectName("add_file_btn")
        self.add_file_btn.clicked.connect(self.add_file)
        self.gridLayout.addWidget(self.add_file_btn, 19, 3, 1, 1)
        # Save_file btn
        self.save_file_btn = QtWidgets.QToolButton(edit_melanotainies_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_file_btn.sizePolicy().hasHeightForWidth())
        self.save_file_btn.setSizePolicy(sizePolicy)
        self.save_file_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.save_file_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(85, 170, 0);")
        self.save_file_btn.setObjectName("save_file_btn")
        self.save_file_btn.clicked.connect(self.save_file)
        self.gridLayout.addWidget(self.save_file_btn, 19, 4, 1, 2)
        # Νεο κουμπί ανοιγμα pdf
        self.open_pdf_file_btn = QtWidgets.QToolButton(edit_melanotainies_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_pdf_file_btn.sizePolicy().hasHeightForWidth())
        self.open_pdf_file_btn.setSizePolicy(sizePolicy)
        self.open_pdf_file_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.open_pdf_file_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
                                             "color: rgb(255, 255, 255);\n"
                                             "background-color: rgb(85, 170, 0);")
        self.open_pdf_file_btn.setObjectName("open_pdf_file_btn")
        self.gridLayout.addWidget(self.open_pdf_file_btn, 19, 4, 1, 2)
        self.open_pdf_file_btn.hide()  # να είναι κρυφό το εμφανίζει το show_file οταν χρειάζεται
        # Διαγραφή αρχείου
        self.delete_file_btn = QtWidgets.QToolButton(edit_melanotainies_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delete_file_btn.sizePolicy().hasHeightForWidth())
        self.delete_file_btn.setSizePolicy(sizePolicy)
        self.delete_file_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.delete_file_btn.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.delete_file_btn.setObjectName("delete_file_btn")
        self.delete_file_btn.clicked.connect(self.delete_file)
        self.gridLayout.addWidget(self.delete_file_btn, 19, 6, 1, 1)

        # Διαγραφή προιόντος
        self.delete_spare_part_btn = QtWidgets.QToolButton(edit_melanotainies_window)
        self.delete_spare_part_btn.setMaximumSize(QtCore.QSize(16777215, 30))
        self.delete_spare_part_btn.setMinimumSize(QtCore.QSize(16777215, 30))
        self.delete_spare_part_btn.setSizePolicy(sizePolicy)
        self.delete_spare_part_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
                                                 "color: rgb(255, 0, 0);\n"
                                                 "background-color: rgb(0, 0, 0);")

        self.delete_spare_part_btn.setObjectName("delete_spare_part_btn")
        self.delete_spare_part_btn.clicked.connect(lambda: self.delete_spare_part())
        self.gridLayout.addWidget(self.delete_spare_part_btn, 20, 0, 1, 1)

        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), edit_melanotainies_window)
        self.shortcut_esc.activated.connect(self.close)

        self.retranslateUi(edit_melanotainies_window)
        QtCore.QMetaObject.connectSlotsByName(edit_melanotainies_window)

    def retranslateUi(self, edit_melanotainies_window):
        _translate = QtCore.QCoreApplication.translate
        edit_melanotainies_window.setWindowTitle(_translate("edit_melanotainies_window", "Επεξεργασία αναλώσιμου"))
        self.customers_label.setText(_translate("edit_melanotainies_window", "Πελάτες"))
        self.quality_label.setText(_translate("edit_melanotainies_window", "Ποιότητα"))
        self.code_label.setText(_translate("edit_melanotainies_window", "Κωδικός"))
        self.pieces_label.setText(_translate("edit_melanotainies_window", "Τεμάχια"))
        self.company_label.setText(_translate("edit_melanotainies_window", "Εταιρεία"))
        self.save_file_btn.setText(_translate("edit_melanotainies_window", "Αποθήκευση αρχείου"))
        self.add_file_btn.setText(_translate("edit_melanotainies_window", "Προσθήκη αρχείου"))
        self.total_label.setText(_translate("edit_melanotainies_window", "Σύνολο"))
        self.description_label.setText(_translate("edit_melanotainies_window", "Περιγραφή"))
        self.cosumable_label.setText(_translate("edit_melanotainies_window", "Αναλώσιμο"))
        self.price_label.setText(_translate("edit_melanotainies_window", "Τιμή"))
        self.previous_btn.setText(_translate("edit_melanotainies_window", "Προηγούμενη"))
        self.comments_label.setText(_translate("edit_melanotainies_window", "Παρατηρήσης"))
        self.orders_btn.setText(_translate("edit_melanotainies_window", "Προσθήκη στίς παραγγελίες"))
        self.delete_file_btn.setText(_translate("edit_melanotainies_window", "Διαγραφή αρχείου"))
        self.next_btn.setText(_translate("edit_melanotainies_window", "Επόμενη"))
        self.save_btn.setText(_translate("edit_melanotainies_window", "Αποθήκευση"))
        self.open_pdf_file_btn.setText(_translate("edit_melanotainies_window", "Ανοιγμα αρχείου pdf"))
        self.delete_spare_part_btn.setText(_translate("edit_consumables_window", "Διαγραφή προϊόντος"))

    def edit_melanotainia(self):
        """
        αυτή η συνάρτηση καλείτε απο το store.py
        Εμφανίζει τα  δεδομένα που πέρνει απο την βάση δεδομέων στις σωστές θέσης για επεξεργασία
        :return: 0
        """
        self.item = session.query(self.selected_table).get(self.selected_id)
        # Show  data
        self.company_lineEdit.setText(self.item.ΕΤΑΙΡΕΙΑ)
        self.quality_lineEdit.setText(self.item.ΠΟΙΟΤΗΤΑ)
        self.consumable_lineEdit.setText(self.item.ΑΝΑΛΩΣΙΜΟ)
        self.pieces_lineEdit.setText(self.item.ΤΕΜΑΧΙΑ)
        self.description_textEdit.setText(self.item.ΠΕΡΙΓΡΑΦΗ)
        self.customers_textEdit.setText(self.item.ΠΕΛΑΤΕΣ)
        self.code_lineEdit.setText(self.item.ΚΩΔΙΚΟΣ)
        self.price_lineEdit.setText(self.item.ΤΙΜΗ)
        self.total_lineEdit.setText(self.item.ΣΥΝΟΛΟ)
        self.comments_lineEdit.setText(self.item.ΠΑΡΑΤΗΡΗΣΗΣ)

        # Show images
        self.images_path = os.path.join(SPARE_PARTS_ROOT, f"{self.selected_table.__tablename__}",
                                        f"{self.selected_id}")
        if os.path.exists(self.images_path):
            self.files = os.listdir(self.images_path)

    def show_file(self):  # Εμφάνησει πρώτου αρχείου όταν ανοιγει το παράθυρο η συνάρτηση καλειτε απο το store.py
        try:

            if self.files[0]:  # αν δεν υπάρχει βγαζει IndexError:  δλδ δεν υπάρχει αχρείο
                self.file_index = 0  # Ορισμός οτι βλέπουμε το πρώτο αρχείο
                self.file = os.path.join(self.images_path, self.files[0])
                if pathlib.Path(self.file).suffix != ".pdf":
                    pixmap = QtGui.QPixmap(os.path.join(self.images_path, self.files[0]))
                    resized_pixmap = pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio)
                    self.image_label.setPixmap(resized_pixmap)
                    self.image_label.setScaledContents(True)
                    self.image_label.show()
                    self.open_pdf_file_btn.hide()  # Απόκρηψη ανοιγμα αρχείου pdf αφου δεν ειναι pdf
                    self.save_file_btn.show()  # Εμφάνηση αποθήκευσης αρχείου αφου δεν ειναι pdf
                else:  # "icons/pdf.png"
                    self.save_file_btn.hide()  # Απόκρηψη αποθήκευσης αρχείου αφου ειναι pdf
                    pixmap = QtGui.QPixmap("icons/pdf.png")
                    resized_pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
                    self.image_label.setPixmap(resized_pixmap)
                    self.image_label.setScaledContents(True)
                    self.image_label.show()
                    self.open_pdf_file_btn.clicked.connect(self.open_pdf)
                    self.open_pdf_file_btn.show()

            if len(self.files) == 1:  # αν υπάρχει μόνο ένα αρχείο
                self.file = os.path.join(self.images_path, self.files[0])
                # απόκρηψη κουμπιών
                self.next_btn.hide()
                self.previous_btn.hide()
                if pathlib.Path(self.file).suffix != ".pdf":
                    self.open_pdf_file_btn.hide()  # Απόκρηψη ανοιγμα αρχείου pdf αφου δεν ειναι pdf
                    self.save_file_btn.show()  # Εμφάνηση αποθήκευσης αρχείου αφου δεν ειναι pdf
                else:
                    self.open_pdf_file_btn.clicked.connect(self.open_pdf)
                    self.save_file_btn.hide()  # Απόκρηψη αποθήκευσης αρχείου αφου ειναι pdf
                    self.open_pdf_file_btn.show()

                self.delete_file_btn.show()
            if len(self.files) > 1:
                self.file = os.path.join(self.images_path, self.files[0])
                self.next_btn.show()
                self.previous_btn.show()
                # self.save_file_btn.show()
                self.delete_file_btn.show()
        except (IndexError, TypeError):  # αν δεν υπάρχει κανένα αρχείο
            # NoneType οταν ξεκοιναει απο το store.py το self.files = None
            # απόκρηψη κουμπιών
            self.image_label.hide()
            self.next_btn.hide()
            self.previous_btn.hide()
            self.save_file_btn.hide()
            self.delete_file_btn.hide()
            self.open_pdf_file_btn.hide()

    def add_file(self):
        options = QtWidgets.QFileDialog.Options()
        new_files, _ = QtWidgets.QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                              "Υποστηριζόμενα αρχεία .bmp .gif .png .jpeg .jpg .pdf ("
                                                              "*.bmp "
                                                              "*.gif *.png *.jpeg *.jpg *.pdf)", options=options)
        if new_files:
            if not os.path.exists(self.images_path):
                os.makedirs(self.images_path)

            # Εισαγωγη αρχείων
            # Αν υπάρχουν αρχεία Ελεγχος αν το αρχείο υπάρχει σε αυτο το προιόν
            for new_file in new_files:
                basename = os.path.basename(new_file).replace(" ", "_")
                if not os.path.exists(os.path.join(self.images_path, os.path.basename(new_file))):
                    shutil.copy(new_file, os.path.join(self.images_path, basename), follow_symlinks=False)
                    QtWidgets.QMessageBox.information(None, "Επιτυχία",
                                                      f'Το αρχεία {os.path.basename(new_file)} προστέθηκε '
                                                      f'επιτυχώς')
                    # Να εμφανίσει το αρχείο
                    self.files = os.listdir(self.images_path)
                    self.show_file()
                else:
                    QtWidgets.QMessageBox.warning(None, "Σφάλμα",
                                                  f"Το αρχείο {os.path.basename(new_file)} υπάρχει.\nΠαρακαλώ αλλάξτε "
                                                  f"όνομα ή "
                                                  f"επιλεξτε διαφορετικό αρχείο")

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()
        # event.ignore() # if you want the window to never be closed

    def next_file(self):
        try:
            if len(self.files) > 1:  # αν υπάρχει πάνω απο ένα αρχείο
                if self.files[self.file_index] == self.files[-1]:  # Αν είναι το τελευταίο αρχείο
                    self.file_index = 0  # να πάει πάλι απο την αρχή

                else:  # Αν δεν είναι το τελευταίο
                    self.file_index += 1  # να πάει στο επώμενο αρχείο

                self.file = os.path.join(self.images_path, self.files[self.file_index])  # να πάει στην δευτερη εικόνα
                if pathlib.Path(self.file).suffix != ".pdf":
                    self.open_pdf_file_btn.hide()  # Απόκρηψη ανοιγμα αρχείου pdf αφου δεν ειναι pdf
                    self.save_file_btn.show()  # Εμφάνηση αποθήκευσης αρχείου αφου δεν ειναι pdf
                    self.open_pdf_file_btn.hide()
                    pixmap = QtGui.QPixmap(os.path.join(self.images_path, self.files[self.file_index]))
                    resized_pixmap = pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio)
                    self.image_label.setPixmap(resized_pixmap)
                    self.image_label.setScaledContents(True)
                else:  # "icons/pdf.png"
                    self.save_file_btn.hide()  # Απόκρηψη αποθήκευσης αρχείου αφου ειναι pdf
                    pixmap = QtGui.QPixmap("icons/pdf.png")
                    resized_pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
                    self.image_label.setPixmap(resized_pixmap)
                    self.image_label.setScaledContents(True)
                    self.open_pdf_file_btn.clicked.connect(self.open_pdf)
                    self.open_pdf_file_btn.show()  # Εμφάνηση ανοιγμα pdf
            elif len(self.files) == 1:  # αν υπάρχει μόνο ένα αρχείο
                self.file = os.path.join(self.images_path, self.files[self.file_index])
                # απόκρηψη κουμπιών
                self.next_btn.hide()
                self.previous_btn.hide()
        except TypeError:  # Αν δεν υπάρχει καποιο αρχείο
            # απόκρηψη κουμπιών
            self.next_btn.hide()
            self.previous_btn.hide()

    def previous_file(self):
        try:
            if len(self.files) > 1:  # αν υπάρχει πάνω απο ένα αρχείο
                if self.files[self.file_index] == self.files[0]:  # Αν είναι το πρώτο αρχείο
                    self.file_index = -1  # να πάει πάλι απο το τέλος

                else:  # Αν δεν είναι το πρώτο
                    self.file_index -= 1  # να πάει στο προηγούμενο αρχείο

                self.file = os.path.join(self.images_path, self.files[self.file_index])  # να πάει στην δευτερη εικόνα
                if pathlib.Path(self.file).suffix != ".pdf":
                    self.open_pdf_file_btn.hide()  # Απόκρηψη ανοιγμα αρχείου pdf αφου δεν ειναι pdf
                    self.save_file_btn.show()  # Εμφάνηση αποθήκευσης αρχείου αφου δεν ειναι pdf
                    pixmap = QtGui.QPixmap(os.path.join(self.images_path, self.files[self.file_index]))
                    resized_pixmap = pixmap.scaled(500, 500, QtCore.Qt.KeepAspectRatio)
                    self.image_label.setPixmap(resized_pixmap)
                    # self.image_label.setScaledContents(True)
                else:  # "icons/pdf.png"
                    self.save_file_btn.hide()  # Απόκρηψη αποθήκευσης αρχείου αφου ειναι pdf
                    pixmap = QtGui.QPixmap("icons/pdf.png")
                    resized_pixmap = pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio)
                    self.image_label.setPixmap(resized_pixmap)
                    # self.image_label.setScaledContents(True)
                    self.open_pdf_file_btn.clicked.connect(self.open_pdf)
                    self.open_pdf_file_btn.show()  # Εμφάνηση ανοιγμα pdf
            elif len(self.files) == 1:  # αν υπάρχει μόνο ένα αρχείο
                self.file = os.path.join(self.images_path, self.files[self.file_index])
                # απόκρηψη κουμπιών
                self.next_btn.hide()
                self.previous_btn.hide()
        except TypeError:  # Αν δεν υπάρχει καποιο αρχείο
            # απόκρηψη κουμπιών
            self.next_btn.hide()
            self.previous_btn.hide()

    def open_pdf(self):
        if sys.platform == "win32":
            subprocess.Popen(self.file, shell=True)
        elif sys.platform == "linux":
            os.system("okular " + self.file)

    def save_file(self):
        pixmap = QtGui.QPixmap(os.path.join(self.images_path, self.files[self.file_index]))
        filename = os.path.basename(self.files[self.file_index])
        extension = pathlib.Path(filename).suffix
        try:
            #  file_to_save == ('/home/dannys/Desktop/add_files.png', '')
            file_to_save = QtWidgets.QFileDialog.getSaveFileName(self, 'Αποθήκευση αρχείου', f'{filename}',
                                                                 f'*{extension}')
            if file_to_save[0] == "":  # file_to_save == ('', '') αν πατήση ακυρο ο χρήστης
                return
            pixmap.save(file_to_save[0], quality=100)
            QtWidgets.QMessageBox.information(None, "Επιτυχία", f'Το αρχεία {filename} αποθηκεύτηκε '
                                                                f'επιτυχώς')
        except TypeError:  # Αν δεν πατησει αποθήκευση
            return

    def delete_file(self):
        filename = os.path.basename(self.files[self.file_index])
        answer = QtWidgets.QMessageBox.question(self, 'Quit', f"Σίγουρα θέλετε να διαγράψετε το {filename} ?",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                                QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            os.remove(os.path.join(self.images_path, self.files[self.file_index]))
            self.files.pop(self.file_index)
            QtWidgets.QMessageBox.information(None, "Επιτυχία", f'Το αρχεία {filename} διαγράφτηκε ' f'επιτυχώς')
            self.show_file()

    def save_changes(self):
        try:
            # ελεγχος αν είναι να προσθέσουμε καινούριο προιόν
            if self.pieces_lineEdit.text() == "" or self.pieces_lineEdit.text() is None:
                pieces = "0"
            else:
                pieces = self.pieces_lineEdit.text()
            price = self.price_lineEdit.text()
            price = "{:.2f}".format(float(price.replace("€", ""))) + " €"
            try:
                total = int(pieces) * int(
                    float(self.price_lineEdit.text().replace(" €", "").strip()))
                total = f"{total:.2f} €"
            except ValueError:
                total = "0.00 €"

            if self.item is None:
                # Φτιάχνουμε νέο object
                self.item = self.selected_table(ΕΤΑΙΡΕΙΑ=self.company_lineEdit.text(),
                                                ΠΟΙΟΤΗΤΑ=self.quality_lineEdit.text(),
                                                ΑΝΑΛΩΣΙΜΟ=self.consumable_lineEdit.text(),
                                                ΠΕΡΙΓΡΑΦΗ=self.description_textEdit.toPlainText(),
                                                ΚΩΔΙΚΟΣ=self.code_lineEdit.text(), ΤΕΜΑΧΙΑ=pieces,
                                                ΤΙΜΗ=price, ΣΥΝΟΛΟ=total,
                                                ΠΕΛΑΤΕΣ=self.customers_textEdit.toPlainText(),
                                                ΠΑΡΑΤΗΡΗΣΗΣ=self.comments_lineEdit.text())
                session.add(self.item)
            # set data to object
            self.item.ΕΤΑΙΡΕΙΑ = self.company_lineEdit.text()
            self.item.ΠΟΙΟΤΗΤΑ = self.quality_lineEdit.text()
            self.item.ΑΝΑΛΩΣΙΜΟ = self.consumable_lineEdit.text()
            self.item.ΠΕΡΙΓΡΑΦΗ = self.description_textEdit.toPlainText()
            self.item.ΚΩΔΙΚΟΣ = self.code_lineEdit.text()
            self.item.ΤΕΜΑΧΙΑ = pieces
            self.item.ΤΙΜΗ = price
            self.item.ΣΥΝΟΛΟ = total
            self.item.ΠΕΛΑΤΕΣ = self.customers_textEdit.toPlainText()
            self.item.ΠΑΡΑΤΗΡΗΣΗΣ = self.comments_lineEdit.text()
            # save data to db
            session.commit()
            # inform user
            QtWidgets.QMessageBox.information(None, "Αποθήκευση", "Οι αλλαγές αποθήκευτηκαν")
            self.close()  # Θέλει self.close για να στειλει signal δεν κλεινει ομως το παραθυρο
        except sqlalchemy.exc.OperationalError:
            QtWidgets.QMessageBox.critical(None, "Σφάλμα",
                                           f"Ο πίνακας: {self.selected_table} δεν βρέθηκε!\nΕλέξτε την βάση δεδομένων\n"
                                           f"Οι αλλαγές δεν αποθήκευτηκαν!")
            return
        except Exception:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα", f"Κάτι δεν πήγε καλα!\nΟι αλλαγές δεν αποθήκευτηκαν!")
            return

    def send_to_orders(self):
        try:
            if not session.query(exists().where(Orders.ΚΩΔΙΚΟΣ == self.item.ΚΩΔΙΚΟΣ)).scalar():
                new_order = Orders(ΚΩΔΙΚΟΣ=self.item.ΚΩΔΙΚΟΣ, ΗΜΕΡΟΜΗΝΙΑ=today, ΠΕΡΙΓΡΑΦΗ=self.item.ΠΕΡΙΓΡΑΦΗ,
                                   ΑΠΟΤΕΛΕΣΜΑ="", images=self.images_path)
                session.add(new_order)
                session.commit()
                QtWidgets.QMessageBox.information(None, "Αποθήκευση",
                                                  f"Ο κωδικός {self.item.ΚΩΔΙΚΟΣ} \nμπήκε για παραγγελία!")
                return
            else:
                QtWidgets.QMessageBox.warning(None, "Αποθήκευση",
                                              f"Ο κωδικός {self.item.ΚΩΔΙΚΟΣ} υπάρχει στις παραγγελίες")
                return

        except sqlalchemy.exc.OperationalError:
            QtWidgets.QMessageBox.critical(None, "Σφάλμα",
                                           f"Ο πίνακας: {self.selected_table} δεν βρέθηκε!\nΕλέξτε την βάση δεδομένων\n"
                                           f"Οι αλλαγές δεν αποθήκευτηκαν!")
            return

        except Exception:
            traceback.print_exc()
            QtWidgets.QMessageBox.critical(None, "Σφάλμα", f"Κάτι δεν πήγε καλα!\nΟι αλλαγές δεν αποθήκευτηκαν!")
            return

    def hide_buttons(self):
        # Hide buttons and show them only when we edit item not when we add new item
        self.add_file_btn.hide()
        self.orders_btn.hide()
        self.next_btn.hide()
        self.previous_btn.hide()
        self.save_file_btn.hide()
        self.delete_file_btn.hide()
        self.delete_spare_part_btn.hide()

    def delete_spare_part(self):  # Δεν σβήνει αρχεία-φωτογραφίες
        answer = QtWidgets.QMessageBox.warning(self, 'Προσοχή',
                                     f"Σίγουρα θέλετε να διαγράψετε το {self.item.ΠΕΡΙΓΡΑΦΗ}\n με κωδικό {self.item.ΚΩΔΙΚΟΣ};",
                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if answer == QtWidgets.QMessageBox.Yes:
            session.delete(self.item)
            session.commit()
            QtWidgets.QMessageBox.information(self, 'Πληροφορία',
                                    f"Το {self.item.ΠΕΡΙΓΡΑΦΗ} \n με κωδικό {self.item.ΚΩΔΙΚΟΣ} \n διαγράφτηκε επιτυχώς")
            self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    edit_melanotainies_window = QtWidgets.QWidget()
    ui = Ui_edit_melanotainies_window()
    ui.setupUi(edit_melanotainies_window)
    edit_melanotainies_window.show()
    sys.exit(app.exec_())
