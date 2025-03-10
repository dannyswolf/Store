# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_spare_part_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
import re
import sys
import subprocess
import os
import shutil
import pathlib  # Για αποθήκευση αρχείου να πάρουμε μόνο την κατάληξει .svg.png
from settings import today, SPARE_PARTS_ROOT
import sqlalchemy
from sqlalchemy.sql import exists
import traceback
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QFileDialog
from db import Brother, Canon, Epson, Konica, Kyocera, Lexmark, Oki, Ricoh, Samsung, Sharp, Orders, session

# --------------Log Files----------------------



class Ui_edit_spare_parts_window(QMainWindow):  # Πρέπει να κληρονομήσει απο QMainWindow for pyqtSignal to work
    window_closed = pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self, *args, **kwargs):
        super(Ui_edit_spare_parts_window, self).__init__(*args, **kwargs)
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
        self.file_index = None  # Δεικτης για το ποιο αρχείο εμφανίζεται
        self.font_14_bold = QtGui.QFont()
        self.font_12 = QtGui.QFont()

    def setupUi(self, edit_spare_parts_window):
        edit_spare_parts_window.setObjectName("edit_spare_parts_window")
        edit_spare_parts_window.resize(1200, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        # Splitter
        self.splitter = QtWidgets.QSplitter(edit_spare_parts_window)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.gridLayout = QtWidgets.QGridLayout(edit_spare_parts_window)
        self.gridLayout.setObjectName("gridLayout")

        # Left Frame
        self.left_frame = QtWidgets.QFrame(self.splitter)
        self.left_frame.setObjectName(u"left_frame")
        self.left_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        # Left Frame Grid
        self.left_frame_gridLayout = QtWidgets.QGridLayout(self.left_frame)
        self.left_frame_gridLayout.setObjectName(u"left_frame_gridLayout")
        # Right Frame
        self.right_frame = QtWidgets.QFrame(self.splitter)
        self.right_frame.setObjectName(u"right_frame")
        self.right_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        # Right frame Grid
        self.right_frame_gridLayout = QtWidgets.QGridLayout(self.right_frame)
        self.right_frame_gridLayout.setObjectName(u"right_frame_gridLayout")

        # ------------------------------------------ Fonts -----------------------
        self.font_14_bold.setFamily("Calibri")
        self.font_14_bold.setPointSize(14)
        self.font_14_bold.setBold(True)
        self.font_14_bold.setWeight(85)

        self.font_12.setFamily("Calibri")
        self.font_12.setPointSize(12)
        self.font_12.setBold(False)
        self.font_12.setWeight(50)

        # Image
        self.image_label = QtWidgets.QLabel(self.right_frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(True)
        sizePolicy.setVerticalStretch(True)
        sizePolicy.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())
        self.image_label.setSizePolicy(sizePolicy)
        self.image_label.setSizeIncrement(QtCore.QSize(1, 1))
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.image_label.setObjectName("image_label")
        self.right_frame_gridLayout.addWidget(self.image_label, 0, 0, 1, 3)

        # Part no
        self.part_no_label = QtWidgets.QLabel(self.left_frame)
        self.part_no_label.setSizePolicy(sizePolicy)
        self.part_no_label.setObjectName("part_no_label")
        self.part_no_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.part_no_label.setFont(self.font_14_bold)
        self.part_no_label.setMaximumSize(QtCore.QSize(16777215, 30))
        self.part_no_label.setMinimumSize(QtCore.QSize(0, 30))
        self.left_frame_gridLayout.addWidget(self.part_no_label, 0, 0, 1, 2)

        self.lineEdit_part_no = QtWidgets.QLineEdit(self.left_frame)
        self.lineEdit_part_no.setSizePolicy(sizePolicy)
        self.lineEdit_part_no.setFont(self.font_12)
        self.lineEdit_part_no.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lineEdit_part_no.setMinimumSize(QtCore.QSize(0, 30))
        self.lineEdit_part_no.setObjectName("lineEdit_part_no")
        # sizePolicy.setHeightForWidth(self.lineEdit_part_no.sizePolicy().hasHeightForWidth())
        self.left_frame_gridLayout.addWidget(self.lineEdit_part_no, 1, 0, 1, 2)
        # Περιγραφή
        self.description_label = QtWidgets.QLabel(self.left_frame)
        self.description_label.setSizePolicy(sizePolicy)
        self.description_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.description_label.setFont(self.font_14_bold)
        self.description_label.setObjectName("description_label")
        self.left_frame_gridLayout.addWidget(self.description_label, 2, 0, 1, 2)

        self.textEdit_description = QtWidgets.QTextEdit(self.left_frame)
        self.textEdit_description.setSizePolicy(sizePolicy)
        self.textEdit_description.setFont(self.font_12)
        self.textEdit_description.setMinimumSize(QtCore.QSize(550, 200))
        self.textEdit_description.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextEditable | QtCore.Qt.TextEditorInteraction | QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.textEdit_description.setPlaceholderText("")
        self.textEdit_description.setObjectName("textEdit_description")
        self.left_frame_gridLayout.addWidget(self.textEdit_description, 3, 0, 2, 2)
        # Κωδικός
        self.code_label = QtWidgets.QLabel(self.left_frame)
        self.code_label.setSizePolicy(sizePolicy)
        self.code_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.code_label.setFont(self.font_14_bold)
        self.code_label.setObjectName("code_label")
        self.left_frame_gridLayout.addWidget(self.code_label, 5, 0, 1, 1)
        self.lineEdit_code = QtWidgets.QLineEdit(self.left_frame)
        self.lineEdit_code.setSizePolicy(sizePolicy)
        self.lineEdit_code.setFont(self.font_12)
        self.lineEdit_code.setObjectName("lineEdit_code")
        self.left_frame_gridLayout.addWidget(self.lineEdit_code, 6, 0, 1, 1)
        # Τεμάχια
        self.pieces_label = QtWidgets.QLabel(self.left_frame)
        self.pieces_label.setSizePolicy(sizePolicy)
        self.pieces_label.setFont(self.font_14_bold)
        self.pieces_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.pieces_label.setObjectName("pieces_label")
        self.left_frame_gridLayout.addWidget(self.pieces_label, 5, 1, 1, 1)
        self.lineEdit_pieces = QtWidgets.QLineEdit(self.left_frame)
        self.lineEdit_pieces.setSizePolicy(sizePolicy)
        self.lineEdit_pieces.setFont(self.font_12)
        self.lineEdit_pieces.setObjectName("lineEdit_pieces")
        self.left_frame_gridLayout.addWidget(self.lineEdit_pieces, 6, 1, 1, 1)
        # Σχόλια - παρτατηρήσης
        self.comments_label = QtWidgets.QLabel(self.left_frame)
        self.comments_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.comments_label.setSizePolicy(sizePolicy)
        self.comments_label.setFont(self.font_14_bold)
        self.comments_label.setObjectName("comments_label")
        self.left_frame_gridLayout.addWidget(self.comments_label, 7, 0, 1, 2)
        self.textEdit_comments = QtWidgets.QTextEdit(self.left_frame)
        self.textEdit_comments.setSizePolicy(sizePolicy)
        self.textEdit_comments.setFont(self.font_12)
        self.textEdit_comments.setObjectName("textEdit_comments")
        self.left_frame_gridLayout.addWidget(self.textEdit_comments, 8, 0, 1, 2)

        # Αποθήκευση
        self.save_btn = QtWidgets.QToolButton(self.left_frame)
        self.save_btn.setSizePolicy(sizePolicy)
        self.save_btn.setFont(self.font_14_bold)
        self.save_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.save_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.save_btn.setStyleSheet("background-color: rgb(0, 255, 0);" "font-weight: bold")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(self.save_changes)
        self.left_frame_gridLayout.addWidget(self.save_btn, 9, 0, 1, 1)
        # Προσθήκη παραγγελίας
        self.orders_btn = QtWidgets.QToolButton(self.left_frame)
        self.orders_btn.setSizePolicy(sizePolicy)
        self.orders_btn.setFont(self.font_14_bold)
        self.orders_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.orders_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.orders_btn.setStyleSheet(
            "font: 75 14pt \"Calibri\";\n""color: rgb(255, 255, 255);\n""background-color: rgb(85, 85, 255);" "font-weight: bold")
        self.orders_btn.setObjectName("orders_btn")
        self.orders_btn.clicked.connect(self.send_to_orders)
        self.left_frame_gridLayout.addWidget(self.orders_btn, 9, 1, 1, 1)
        # Προηγούμενο αρχείο
        self.previous_btn = QtWidgets.QToolButton(self.right_frame)
        self.previous_btn.setFont(self.font_14_bold)
        self.previous_btn.setSizePolicy(sizePolicy)
        self.previous_btn.setMinimumSize(QtCore.QSize(0, 40))
        self.previous_btn.setMaximumSize(QtCore.QSize(16777215, 40))
        self.previous_btn.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.previous_btn.setObjectName("previous_btn")
        self.previous_btn.clicked.connect(self.previous_file)
        self.right_frame_gridLayout.addWidget(self.previous_btn, 1, 0, 1, 1)
        # Επόμενη
        self.next_btn = QtWidgets.QToolButton(self.right_frame)
        self.next_btn.setFont(self.font_14_bold)
        self.next_btn.setSizePolicy(sizePolicy)
        self.next_btn.setMinimumSize(QtCore.QSize(0, 40))
        self.next_btn.setMaximumSize(QtCore.QSize(16777215, 40))
        self.next_btn.setStyleSheet("background-color: rgb(255, 255, 0);")
        self.next_btn.setObjectName("next_btn")
        self.next_btn.clicked.connect(self.next_file)
        self.right_frame_gridLayout.addWidget(self.next_btn, 1, 1, 1, 1)
        # Προσθήκη αρχείου
        self.add_file_btn = QtWidgets.QToolButton(self.right_frame)
        self.add_file_btn.setSizePolicy(sizePolicy)
        self.add_file_btn.setFont(self.font_14_bold)
        self.add_file_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.add_file_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.add_file_btn.setStyleSheet("font: 75 14pt  \"Calibri\";\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "background-color: rgb(0, 170, 127);" "font-weight: bold")
        self.add_file_btn.setObjectName("add_file_btn")
        self.add_file_btn.clicked.connect(self.add_file)
        self.right_frame_gridLayout.addWidget(self.add_file_btn, 2, 0, 1, 1)
        # Save_file btn
        self.save_file_btn = QtWidgets.QToolButton(self.right_frame)
        self.save_file_btn.setSizePolicy(sizePolicy)
        self.save_file_btn.setFont(self.font_14_bold)
        self.save_file_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.save_file_btn.setStyleSheet("font: 75 14pt bold \"Calibri\";\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(85, 170, 0);")
        self.save_file_btn.setObjectName("save_file_btn")
        self.save_file_btn.clicked.connect(self.save_file)
        self.right_frame_gridLayout.addWidget(self.save_file_btn, 2, 1, 1, 1)
        # Νεο κουμπί ανοιγμα pdf
        self.open_pdf_file_btn = QtWidgets.QToolButton(self.right_frame)
        self.open_pdf_file_btn.setFont(self.font_14_bold)
        self.open_pdf_file_btn.setSizePolicy(sizePolicy)
        self.open_pdf_file_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.open_pdf_file_btn.setStyleSheet("font: 75 14pt bold \"Calibri\";\n"
                                             "color: rgb(255, 255, 255);\n"
                                             "background-color: rgb(85, 170, 0);")
        self.open_pdf_file_btn.setObjectName("open_pdf_file_btn")
        self.right_frame_gridLayout.addWidget(self.open_pdf_file_btn, 2, 1, 1, 1)
        self.open_pdf_file_btn.hide()  # να είναι κρυφό το εμφανίζει το show_file οταν χρειάζεται
        # Διαγραφή αρχείου
        self.delete_file_btn = QtWidgets.QToolButton(self.right_frame)
        self.delete_file_btn.setFont(self.font_14_bold)
        self.delete_file_btn.setMaximumSize(QtCore.QSize(16777215, 50))
        self.delete_file_btn.setStyleSheet("background-color: rgb(255, 0, 0);")
        self.delete_file_btn.setObjectName("delete_file_btn")
        self.delete_file_btn.clicked.connect(self.delete_file)
        self.right_frame_gridLayout.addWidget(self.delete_file_btn, 2, 2, 1, 1)

        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)

        # Διαγραφή προιόντος
        # self.delete_spare_part_btn = QtWidgets.QToolButton(edit_spare_parts_window)
        # self.delete_spare_part_btn.setMaximumSize(QtCore.QSize(16777215, 30))
        # self.delete_spare_part_btn.setMinimumSize(QtCore.QSize(16777215, 30))
        # self.delete_spare_part_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
        #                                          "color: rgb(255, 0, 0);\n"
        #                                          "background-color: rgb(0, 0, 0);")
        # self.delete_spare_part_btn.setObjectName("delete_spare_part_btn")
        # self.delete_spare_part_btn.clicked.connect(self.delete_spare_part)
        # self.delete_spare_part_btn.hide()
        # self.gridLayout.addWidget(self.delete_spare_part_btn, 11, 0, 1, 1)
        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), edit_spare_parts_window)
        self.shortcut_esc.activated.connect(lambda: self.close())

        self.retranslateUi(edit_spare_parts_window)
        QtCore.QMetaObject.connectSlotsByName(edit_spare_parts_window)

    def retranslateUi(self, edit_spare_parts_window):
        _translate = QtCore.QCoreApplication.translate
        # if self.selected_id is None:
        #     edit_spare_parts_window.setWindowTitle(_translate("edit_spare_parts_window", "Προσθήκη ανταλλακτικού"))
        # else:
        #     edit_spare_parts_window.setWindowTitle(_translate("edit_spare_parts_window", "Επεξεργασία ανταλλακτικού"))
        self.previous_btn.setText(_translate("edit_spare_parts_window", "Προηγούμενο"))
        self.next_btn.setText(_translate("edit_spare_parts_window", "Επόμενο"))
        self.comments_label.setText(_translate("edit_spare_parts_window", "Σχόλια"))
        self.save_file_btn.setText(_translate("edit_spare_parts_window", "Αποθήκευση αρχείου"))
        self.open_pdf_file_btn.setText(_translate("edit_spare_parts_window", "Άνοιγμα αρχείου pdf"))
        self.pieces_label.setText(_translate("edit_spare_parts_window", "Τεμάχια"))
        self.orders_btn.setText(_translate("edit_spare_parts_window", "Προσθήκη στις παραγγελίες"))
        self.description_label.setText(_translate("edit_spare_parts_window", "Περιγραφή"))
        self.code_label.setText(_translate("edit_spare_parts_window", "Κωδικός"))
        self.add_file_btn.setText(_translate("edit_spare_parts_window", "Προσθήκη αρχείου"))
        self.delete_file_btn.setText(_translate("edit_spare_parts_window", "Διαγραφή αρχείου"))
        self.part_no_label.setText(_translate("edit_spare_parts_window", "Part No"))
        self.save_btn.setText(_translate("edit_spare_parts_window", "Αποθήκευση"))
        # self.delete_spare_part_btn.setText(_translate("edit_spare_parts_window", "Διαγραφή προϊόντος"))

    def edit_spare_part(self):
        """
        αυτή η συνάρτηση καλείτε απο το store.pyw
        Εμφανίζει τα  δεδομένα που πέρνει απο την βάση δεδομέων στις σωστές θέσης για επεξεργασία
        :return: 0
        """

        self.item = session.query(self.selected_table).get(self.selected_id)
        # Show  data
        self.lineEdit_part_no.setText(self.item.PARTS_NR)
        self.lineEdit_code.setText(self.item.ΚΩΔΙΚΟΣ)
        self.lineEdit_pieces.setText(self.item.ΤΕΜΑΧΙΑ)
        self.textEdit_description.setText(self.item.ΠΕΡΙΓΡΑΦΗ)
        self.textEdit_comments.setText(self.item.ΠΑΡΑΤΗΡΗΣΗΣ)
        # Show images
        self.images_path = os.path.join(SPARE_PARTS_ROOT, f"{self.selected_table.__tablename__}",
                                        f"{self.selected_id}")
        if os.path.exists(self.images_path):
            self.files = os.listdir(self.images_path)

    def save_changes(self):
        if self.lineEdit_code.text() is None or self.lineEdit_code.text() == "":
            QtWidgets.QMessageBox.warning(None, "Προσοχή!", "Ο κωδικός δεν μπορεί να είναι κενός!")
            return
        if self.lineEdit_pieces.text() == "" or self.lineEdit_pieces.text() is None:
            pieces = "0"
        else:
            pieces = self.lineEdit_pieces.text()
        try:
            # get data from edit lines
            self.part_no = self.lineEdit_part_no.text()
            self.description = self.textEdit_description.toPlainText()
            self.code = self.lineEdit_code.text()
            self.pieces = pieces
            self.comments = self.textEdit_comments.toPlainText()
            # set data to object
            # ελεγχος αν είναι να προσθέσουμε καινούριο προιόν
            if self.item is None:
                # Ελεγχος αν υπάρχει ο κωδικός
                if session.query(exists().where(self.selected_table.ΚΩΔΙΚΟΣ == self.code)).scalar():
                    QtWidgets.QMessageBox.critical(None, "Σφάλμα", f"O κωδικός {self.code} υπάρχει")
                    return
                # Ελεγχος αν υπάρχει το part no
                all_parts = session.query(self.selected_table.PARTS_NR).all()  # [('14501',), ('LU7179001',)]
                for part in all_parts:

                    if re.sub('[^A-Za-z0-9]+', '', part[0].lower()) == re.sub('[^A-Za-z0-9]+', '', self.part_no.lower()):
                        QtWidgets.QMessageBox.critical(None, "Σφάλμα", f"Το Part Nr {re.sub('[^A-Za-z0-9]+', '', self.part_no.lower())} υπάρχει")
                        return
                self.item = self.selected_table(PARTS_NR=self.part_no.replace(" ", ""), ΠΕΡΙΓΡΑΦΗ=self.description,
                                                ΚΩΔΙΚΟΣ=self.code, ΤΕΜΑΧΙΑ=self.pieces, ΠΑΡΑΤΗΡΗΣΗΣ=self.comments)
                session.add(self.item)

            else:
                self.item.PARTS_NR = self.part_no.replace(" ", "")  # Remove Spaces
                self.item.ΠΕΡΙΓΡΑΦΗ = self.description
                self.item.ΚΩΔΙΚΟΣ = self.code
                self.item.ΤΕΜΑΧΙΑ = self.pieces
                self.item.ΠΑΡΑΤΗΡΗΣΗΣ = self.comments
            # save data to db
            session.commit()
            # inform user
            QMessageBox.information(None, "Αποθήκευση", "Οι αλλαγές αποθήκευτηκαν")
            self.close()  # Θέλει self.close για να στειλει signal δεν κλεινει ομως το παραθυρο
        except sqlalchemy.exc.OperationalError:
            QMessageBox.critical(None, "Σφάλμα",
                                 f"Ο πίνακας: {self.selected_table} δεν βρέθηκε!\nΕλέξτε την βάση δεδομένων\n"
                                 f"Οι αλλαγές δεν αποθήκευτηκαν!")
            return
        except Exception:
            traceback.print_exc()
            QMessageBox.critical(None, "Σφάλμα", f"Κάτι δεν πήγε καλα!\nΟι αλλαγές δεν αποθήκευτηκαν!")
            return

    def closeEvent(self, event):
        self.window_closed.emit()
        event.accept()


        # event.ignore() # if you want the window to never be closed

    def send_to_orders(self):
        try:
            if not session.query(exists().where(Orders.ΚΩΔΙΚΟΣ == self.item.ΚΩΔΙΚΟΣ)).scalar():
                new_order = Orders(ΚΩΔΙΚΟΣ=self.item.ΚΩΔΙΚΟΣ, ΠΟΙΟΤΗΤΑ="", ΗΜΕΡΟΜΗΝΙΑ=today, ΠΕΡΙΓΡΑΦΗ=self.item.ΠΕΡΙΓΡΑΦΗ,
                                   ΑΠΟΤΕΛΕΣΜΑ="", images=self.images_path)
                session.add(new_order)
                session.commit()
                QMessageBox.information(None, "Αποθήκευση", f"Ο κωδικός {self.item.ΚΩΔΙΚΟΣ} \nμπήκε για παραγγελία!")
                return
            else:
                QMessageBox.warning(None, "Αποθήκευση", f"Ο κωδικός {self.item.ΚΩΔΙΚΟΣ} υπάρχει στις παραγγελίες")
                return

        except sqlalchemy.exc.OperationalError:
            QMessageBox.critical(None, "Σφάλμα",
                                 f"Ο πίνακας: {self.selected_table} δεν βρέθηκε!\nΕλέξτε την βάση δεδομένων\n"
                                 f"Οι αλλαγές δεν αποθήκευτηκαν!")
            return

        except Exception:
            traceback.print_exc()
            QMessageBox.critical(None, "Σφάλμα", f"Κάτι δεν πήγε καλα!\nΟι αλλαγές δεν αποθήκευτηκαν!")
            return

    def add_file(self):
        options = QFileDialog.Options()
        new_files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                                    "Υποστηριζόμενα αρχεία .bmp .gif .png .jpeg .jpg .pdf (*.bmp "
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
                    QMessageBox.information(None, "Επιτυχία", f'Το αρχεία {os.path.basename(new_file)} προστέθηκε '
                                                              f'επιτυχώς')
                    # Να εμφανίσει το αρχείο
                    self.files = os.listdir(self.images_path)
                    self.show_file()
                else:
                    QMessageBox.warning(None, "Σφάλμα",
                                        f"Το αρχείο {os.path.basename(new_file)} υπάρχει.\nΠαρακαλώ αλλάξτε όνομα ή "
                                        f"επιλεξτε διαφορετικό αρχείο")

    def show_file(self):  # Εμφάνησει πρώτου αρχείου όταν ανοιγει το παράθυρο η συνάρτηση καλειτε απο το store.pyw
        try:

            if self.files[0]:  # αν δεν υπάρχει βγαζει IndexError:  δλδ δεν υπάρχει αχρείο
                self.file_index = 0  # Ορισμός οτι βλέπουμε το πρώτο αρχείο
                self.file = os.path.join(self.images_path, self.files[0])
                if pathlib.Path(self.file).suffix != ".pdf":
                    pixmap = QtGui.QPixmap(os.path.join(self.images_path, self.files[0]))
                    resized_pixmap = pixmap.scaled(500, 500, aspectRatioMode = 2)
                    self.image_label.setPixmap(resized_pixmap)
                    # self.image_label.setScaledContents(True)
                    self.image_label.show()
                    self.open_pdf_file_btn.hide()  # Απόκρηψη ανοιγμα αρχείου pdf αφου δεν ειναι pdf
                    self.save_file_btn.show()  # Εμφάνηση αποθήκευσης αρχείου αφου δεν ειναι pdf
                else:  # "icons/pdf.png"
                    self.save_file_btn.hide()  # Απόκρηψη αποθήκευσης αρχείου αφου ειναι pdf
                    pixmap = QtGui.QPixmap("icons/pdf.png")
                    resized_pixmap = pixmap.scaled(200, 200, aspectRatioMode = 2)
                    self.image_label.setPixmap(resized_pixmap)
                    # self.image_label.setScaledContents(True)
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
            # NoneType οταν ξεκοιναει απο το store.pyw το self.files = None
            # απόκρηψη κουμπιών
            self.image_label.hide()
            self.next_btn.hide()
            self.previous_btn.hide()
            self.save_file_btn.hide()
            self.delete_file_btn.hide()
            self.open_pdf_file_btn.hide()

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
                    resized_pixmap = pixmap.scaled(500, 500, aspectRatioMode = 2)
                    self.image_label.setPixmap(resized_pixmap)
                    # self.image_label.setScaledContents(True)
                else:  # "icons/pdf.png"
                    self.save_file_btn.hide()  # Απόκρηψη αποθήκευσης αρχείου αφου ειναι pdf
                    pixmap = QtGui.QPixmap("icons/pdf.png")
                    resized_pixmap = pixmap.scaled(200, 200, aspectRatioMode = 2)
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
                    resized_pixmap = pixmap.scaled(500, 500, aspectRatioMode = 2)
                    self.image_label.setPixmap(resized_pixmap)
                    # self.image_label.setScaledContents(True)
                else:  # "icons/pdf.png"
                    self.save_file_btn.hide()  # Απόκρηψη αποθήκευσης αρχείου αφου ειναι pdf
                    pixmap = QtGui.QPixmap("icons/pdf.png")
                    resized_pixmap = pixmap.scaled(200, 200, aspectRatioMode = 2)
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

    def save_file(self):
        pixmap = QtGui.QPixmap(os.path.join(self.images_path, self.files[self.file_index]))
        filename = os.path.basename(self.files[self.file_index])
        extension = pathlib.Path(filename).suffix
        try:
            #  file_to_save == ('/home/dannys/Desktop/add_files.png', '')
            file_to_save = QFileDialog.getSaveFileName(self, 'Αποθήκευση αρχείου', f'{filename}', f'*{extension}')
            if file_to_save[0] == "":  # file_to_save == ('', '') αν πατήση ακυρο ο χρήστης
                return
            pixmap.save(file_to_save[0], quality=100)
            QMessageBox.information(None, "Επιτυχία", f'Το αρχεία {filename} αποθηκεύτηκε '
                                                      f'επιτυχώς')
        except TypeError:  # Αν δεν πατησει αποθήκευση
            return

    def delete_file(self):
        filename = os.path.basename(self.files[self.file_index])
        answer = QMessageBox.question(self, 'Quit', f"Σίγουρα θέλετε να διαγράψετε το {filename} ?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer == QMessageBox.Yes:
            os.remove(os.path.join(self.images_path, self.files[self.file_index]))
            self.files.pop(self.file_index)
            QMessageBox.information(None, "Επιτυχία", f'Το αρχεία {filename} διαγράφτηκε ' f'επιτυχώς')
            self.show_file()

    def open_pdf(self):
        if sys.platform == "win32":
            subprocess.Popen(self.file, shell=True)
        elif sys.platform == "linux":
            os.system("okular " + self.file)

    def hide_buttons(self):
        # Hide buttons and show them only when we edit item not when we add new item
        self.add_file_btn.hide()
        self.orders_btn.hide()
        self.next_btn.hide()
        self.previous_btn.hide()
        self.save_file_btn.hide()
        self.delete_file_btn.hide()
        # self.delete_spare_part_btn.hide()

    def delete_spare_part(self):  # Δεν σβήνει αρχεία-φωτογραφίες
        answer = QMessageBox.warning(self, 'Προσοχή',
                                     f"Σίγουρα θέλετε να διαγράψετε το {self.item.ΠΕΡΙΓΡΑΦΗ}\n με κωδικό {self.item.ΚΩΔΙΚΟΣ};",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if answer == QMessageBox.Yes:
            session.delete(self.item)
            session.commit()
            QMessageBox.information(self, 'Πληροφορία',
                                    f"Το {self.item.ΠΕΡΙΓΡΑΦΗ} \n με κωδικό {self.item.ΚΩΔΙΚΟΣ} \n διαγράφτηκε επιτυχώς")
            self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    edit_spare_parts_window = QtWidgets.QWidget()
    ui = Ui_edit_spare_parts_window()
    ui.setupUi(edit_spare_parts_window)
    edit_spare_parts_window.show()
    sys.exit(app.exec_())
