# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_spare_part_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
import datetime
import sys
import subprocess
import os
import shutil
import pathlib  # Για αποθήκευση αρχείου να πάρουμε μόνο την κατάληξει .svg.png
import sqlalchemy
import traceback
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSignal, QDate
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QFileDialog, QCalendarWidget
from db import Orders, session
from settings import today, root_logger

# --------------Log Files----------------------
# log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
sys.stderr.write = root_logger.error
sys.stdout.write = root_logger.info


class Ui_edit_orders_window(QMainWindow):  # Πρέπει να κληρονομήσει απο QMainWindow for pyqtSignal to work
    window_closed = pyqtSignal()  # Το Signal πρεπει να είναι εκτός __init__ δεν δουλευει αλλιως

    def __init__(self, *args, **kwargs):
        super(Ui_edit_orders_window, self).__init__(*args, **kwargs)
        self.selected_id = None
        self.selected_table = None
        self.window = None
        self.item = None
        self.date = today
        self.description = None
        self.code = None
        self.status = None
        self.comments = None
        self.images_path = None
        self.files = None
        self.file = None  # αρχείο που εμφανίζεται
        self.file_index = None  # Δεικτης για το ποιο αρχείο εμφανίζεται

    def setupUi(self, edit_orders_window):
        edit_orders_window.setObjectName("edit_orders_window")
        edit_orders_window.resize(400, 600)
        self.gridLayout = QtWidgets.QGridLayout(edit_orders_window)
        self.gridLayout.setObjectName("gridLayout")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # Image
        self.image_label = QtWidgets.QLabel(edit_orders_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(True)
        sizePolicy.setVerticalStretch(True)
        sizePolicy.setHeightForWidth(self.image_label.sizePolicy().hasHeightForWidth())

        self.image_label.setSizePolicy(sizePolicy)
        self.image_label.setSizeIncrement(QtCore.QSize(1, 1))
        self.image_label.setText("")
        self.image_label.setAlignment(QtCore.Qt.AlignCenter)
        self.image_label.setObjectName("image_label")
        self.gridLayout.addWidget(self.image_label, 0, 2, 6, 4)
        # ΗΜΕΡΟΜΗΝΙΑ
        # self.date_label = QtWidgets.QLabel(edit_orders_window)
        # self.date_label.setSizePolicy(sizePolicy)
        # self.date_label.setStyleSheet("font: 75 14pt \"Calibri\";")
        # self.date_label.setObjectName("date_label")
        # self.gridLayout.addWidget(self.date_label, 0, 0, 1, 1)
        # Calendar
        self.calendarWidget = QCalendarWidget(edit_orders_window)
        self.calendarWidget.setObjectName(u"calendarWidget")
        font = QtGui.QFont()
        font.setFamily(u"Calibri")
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        font.setStyleStrategy(QtGui.QFont.PreferAntialias)
        self.calendarWidget.setFont(font)
        self.calendarWidget.setGridVisible(True)
        self.calendarWidget.setHorizontalHeaderFormat(QCalendarWidget.ShortDayNames)
        self.calendarWidget.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(True)
        self.gridLayout.addWidget(self.calendarWidget, 0, 0, 1, 2)

        # Περιγραφή
        self.description_label = QtWidgets.QLabel(edit_orders_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.description_label.sizePolicy().hasHeightForWidth())
        self.description_label.setSizePolicy(sizePolicy)
        self.description_label.setStyleSheet("font: 75 14pt \"Calibri\";")
        self.description_label.setObjectName("description_label")
        self.gridLayout.addWidget(self.description_label, 1, 0, 1, 1)
        self.textEdit_description = QtWidgets.QTextEdit(edit_orders_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_description.sizePolicy().hasHeightForWidth())
        self.textEdit_description.setSizePolicy(sizePolicy)
        self.textEdit_description.setStyleSheet("font: 75 12pt \"Calibri\";")
        self.textEdit_description.setDocumentTitle("")
        self.textEdit_description.setMarkdown("")
        self.textEdit_description.setTextInteractionFlags(
            QtCore.Qt.LinksAccessibleByMouse | QtCore.Qt.TextEditable | QtCore.Qt.TextEditorInteraction | QtCore.Qt.TextSelectableByKeyboard | QtCore.Qt.TextSelectableByMouse)
        self.textEdit_description.setPlaceholderText("")
        self.textEdit_description.setObjectName("textEdit_description")
        self.gridLayout.addWidget(self.textEdit_description, 2, 0, 1, 2)
        # Κωδικός
        self.code_label = QtWidgets.QLabel(edit_orders_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.code_label.sizePolicy().hasHeightForWidth())
        self.code_label.setSizePolicy(sizePolicy)
        self.code_label.setStyleSheet("font: 75 14pt \"Calibri\";")
        self.code_label.setObjectName("code_label")
        self.gridLayout.addWidget(self.code_label, 3, 0, 1, 1)
        self.lineEdit_code = QtWidgets.QLineEdit(edit_orders_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_code.sizePolicy().hasHeightForWidth())
        self.lineEdit_code.setSizePolicy(sizePolicy)
        self.lineEdit_code.setStyleSheet("font: 75 12pt \"Calibri\";")
        self.lineEdit_code.setObjectName("lineEdit_code")
        self.gridLayout.addWidget(self.lineEdit_code, 4, 0, 1, 1)
        # ΑΠΟΤΕΛΕΣΜΑ
        self.status_label = QtWidgets.QLabel(edit_orders_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_label.sizePolicy().hasHeightForWidth())
        self.status_label.setSizePolicy(sizePolicy)
        self.status_label.setStyleSheet("font: 75 14pt \"Calibri\";")
        self.status_label.setObjectName("status_label")
        self.gridLayout.addWidget(self.status_label, 3, 1, 1, 1)
        self.status_lineEdit = QtWidgets.QLineEdit(edit_orders_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status_lineEdit.sizePolicy().hasHeightForWidth())
        self.status_lineEdit.setSizePolicy(sizePolicy)
        self.status_lineEdit.setStyleSheet("font: 75 12pt \"Calibri\";")
        self.status_lineEdit.setObjectName("status_lineEdit")
        self.gridLayout.addWidget(self.status_lineEdit, 4, 1, 1, 1)
        # Σχόλια - παρτατηρήσης
        self.comments_label = QtWidgets.QLabel(edit_orders_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(True)
        sizePolicy.setVerticalStretch(False)
        sizePolicy.setHeightForWidth(self.comments_label.sizePolicy().hasHeightForWidth())
        self.comments_label.setSizePolicy(sizePolicy)
        self.comments_label.setStyleSheet("font: 75 14pt \"Calibri\";")
        self.comments_label.setObjectName("comments_label")
        self.gridLayout.addWidget(self.comments_label, 5, 0, 1, 1)
        self.textEdit_comments = QtWidgets.QLineEdit(edit_orders_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit_comments.sizePolicy().hasHeightForWidth())
        self.textEdit_comments.setSizePolicy(sizePolicy)
        self.textEdit_comments.setStyleSheet("font: 75 12pt \"Calibri\";")
        self.textEdit_comments.setObjectName("textEdit_comments")
        self.gridLayout.addWidget(self.textEdit_comments, 6, 0, 1, 2)
        # Αποθήκευση αλλαγών
        self.save_btn = QtWidgets.QToolButton(edit_orders_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_btn.sizePolicy().hasHeightForWidth())
        self.save_btn.setSizePolicy(sizePolicy)
        self.save_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.save_btn.setStyleSheet("font: 95 14pt \"Calibri\";\n"
                                    "background-color: rgb(0, 255, 0);")
        self.save_btn.setObjectName("save_btn")
        self.save_btn.clicked.connect(lambda: self.save_changes())
        self.gridLayout.addWidget(self.save_btn, 7, 0, 1, 2)
        # Προηγούμενο αρχείο
        self.previous_image_btn = QtWidgets.QToolButton(edit_orders_window)
        self.previous_image_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n" "background-color: rgb(255, 255, 0);")
        self.previous_image_btn.setObjectName("previous_image_btn")
        self.previous_image_btn.clicked.connect(self.previous_file)
        self.gridLayout.addWidget(self.previous_image_btn, 6, 3, 1, 1)
        # Επόμενο αρχείο
        self.next_image_btn = QtWidgets.QToolButton(edit_orders_window)
        self.next_image_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n" "background-color: rgb(255, 255, 07);")
        self.next_image_btn.setObjectName("next_image_btn")
        self.next_image_btn.clicked.connect(self.next_file)
        self.gridLayout.addWidget(self.next_image_btn, 6, 4, 1, 1)
        # Προσθήκη αρχείου
        self.add_file_btn = QtWidgets.QToolButton(edit_orders_window)
        self.add_file_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
                                        "color: rgb(255, 255, 255);\n"
                                        "background-color: rgb(0, 170, 127);")
        self.add_file_btn.setObjectName("add_file_btn")
        self.add_file_btn.clicked.connect(self.add_file)
        self.gridLayout.addWidget(self.add_file_btn, 7, 2, 1, 1)
        # Αποθήκευση αρχείου
        self.save_file_btn = QtWidgets.QToolButton(edit_orders_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_file_btn.sizePolicy().hasHeightForWidth())
        self.save_file_btn.setSizePolicy(sizePolicy)
        self.save_file_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
                                         "color: rgb(255, 255, 255);\n"
                                         "background-color: rgb(85, 170, 0);")
        self.save_file_btn.setObjectName("save_file_btn")
        self.save_file_btn.clicked.connect(self.save_file)
        self.gridLayout.addWidget(self.save_file_btn, 7, 3, 1, 2)
        # Διαγραφή αρχείου
        self.delete_file_btn = QtWidgets.QToolButton(edit_orders_window)
        self.delete_file_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
                                           "color: rgb(255, 255, 255);\n"
                                           "background-color: rgb(255, 0, 0);")
        self.delete_file_btn.setObjectName("delete_file_btn")
        self.delete_file_btn.clicked.connect(self.delete_file)
        self.gridLayout.addWidget(self.delete_file_btn, 7, 5, 1, 1)

        # Νεο κουμπί ανοιγμα pdf
        self.open_pdf_file_btn = QtWidgets.QToolButton(edit_orders_window)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding,
                                           QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.open_pdf_file_btn.sizePolicy().hasHeightForWidth())
        self.open_pdf_file_btn.setSizePolicy(sizePolicy)
        self.open_pdf_file_btn.setStyleSheet("font: 75 14pt \"Calibri\";\n"
                                             "color: rgb(255, 255, 255);\n"
                                             "background-color: rgb(85, 170, 0);")
        self.open_pdf_file_btn.setObjectName("open_pdf_file_btn")
        self.gridLayout.addWidget(self.open_pdf_file_btn, 7, 3, 1, 2)
        self.open_pdf_file_btn.hide()   # να είναι κρυφό το εμφανίζει το show_file οταν χρειάζεται

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.date_label.sizePolicy().hasHeightForWidth())

        # Esc
        self.shortcut_esc = QtWidgets.QShortcut(QtGui.QKeySequence('Escape'), edit_orders_window)
        self.shortcut_esc.activated.connect(self.close)

        self.retranslateUi(edit_orders_window)
        QtCore.QMetaObject.connectSlotsByName(edit_orders_window)

    def retranslateUi(self, edit_orders_window):
        _translate = QtCore.QCoreApplication.translate
        edit_orders_window.setWindowTitle(_translate("edit_orders_window", "Επεξεργασία παραγγελίας"))
        self.previous_image_btn.setText(_translate("edit_orders_window", "Προηγούμενη"))
        self.next_image_btn.setText(_translate("edit_orders_window", "Επόμενη"))
        self.comments_label.setText(_translate("edit_orders_window", "Σχόλια"))
        self.save_file_btn.setText(_translate("edit_orders_window", "Αποθήκευση αρχείου"))
        self.open_pdf_file_btn.setText(_translate("edit_orders_window", "Ανοιγμα αρχείου pdf"))
        self.status_label.setText(_translate("edit_orders_window", "Αποτέλεσμα"))
        self.description_label.setText(_translate("edit_orders_window", "Περιγραφή"))
        self.code_label.setText(_translate("edit_orders_window", "Κωδικός"))
        self.add_file_btn.setText(_translate("edit_orders_window", "Προσθήκη αρχείου"))
        self.delete_file_btn.setText(_translate("edit_orders_window", "Διαγραφή αρχείου"))
        # self.date_label.setText(_translate("edit_orders_window", "Ημερομηνία"))
        self.save_btn.setText(_translate("edit_orders_window", "Αποθήκευση"))

    def edit_order(self):
        """
        αυτή η συνάρτηση καλείτε απο το store.py
        Εμφανίζει τα  δεδομένα που πέρνει απο την βάση δεδομέων στις σωστές θέσης για επεξεργασία
        :return: 0
        """

        self.item = session.query(self.selected_table).get(self.selected_id)
        # Show  data
        self.lineEdit_code.setText(self.item.ΚΩΔΙΚΟΣ)
        item_date = self.item.ΗΜΕΡΟΜΗΝΙΑ
        date_obj = datetime.datetime.strptime(item_date, '%d/%m/%Y').date()
        self.calendarWidget.setSelectedDate(QDate(date_obj))
        self.status_lineEdit.setText(self.item.ΑΠΟΤΕΛΕΣΜΑ)
        self.textEdit_description.setText(self.item.ΠΕΡΙΓΡΑΦΗ)
        self.textEdit_comments.setText(self.item.ΠΑΡΑΤΗΡΗΣΕΙΣ)
        # Show images
        if self.item.images is not None:  # Οταν βάζουμε παραγγελία χειροκινιτα και οχι απο υπαρχον προιον
                                     # το πεδίο images του item ειναι None στην Βάση δεδομένων ειναι Null
            self.images_path = os.path.abspath(self.item.images)
            # Μετατροπή των directories αναλογα με το λειτουργεικό συστημα
            if sys.platform == "win32":
                self.images_path = self.images_path.replace("/", "\\")
            elif sys.platform == "linux":
                self.images_path = self.images_path.replace("\\", "/")

            if os.path.exists(self.images_path):
                self.files = os.listdir(self.images_path)

    def save_changes(self):
        try:
            # get data from edit lines
            self.date = self.calendarWidget.selectedDate().toString('dd/MM/yyyy')
            self.description = self.textEdit_description.toPlainText()
            self.code = self.lineEdit_code.text()
            self.status = self.status_lineEdit.text()
            self.comments = self.textEdit_comments.text()
            # set data to object
            # ελεγχος αν είναι να προσθέσουμε καινούριο προιόν
            if self.item is None:
                # Φτιάχνουμε νέο object
                self.item = self.selected_table(ΗΜΕΡΟΜΗΝΙΑ=self.date, ΠΕΡΙΓΡΑΦΗ=self.description,
                                                ΚΩΔΙΚΟΣ=self.code, ΑΠΟΤΕΛΕΣΜΑ=self.status, ΠΑΡΑΤΗΡΗΣΕΙΣ=self.comments)

                session.add(self.item)
            else:
                self.item.ΗΜΕΡΟΜΗΝΙΑ = self.date  # Remove Spaces
                self.item.ΠΕΡΙΓΡΑΦΗ = self.description
                self.item.ΚΩΔΙΚΟΣ = self.code
                self.item.ΑΠΟΤΕΛΕΣΜΑ = self.status
                self.item.ΠΑΡΑΤΗΡΗΣΕΙΣ = self.comments
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

    def show_file(self):  # Εμφάνησει πρώτου αρχείου όταν ανοιγει το παράθυρο η συνάρτηση καλειτε απο το store.py

        try:

            if self.files[0]:  # αν δεν υπάρχει βγαζει IndexError:  δλδ δεν υπάρχει αχρείο
                self.file_index = 0  # Ορισμός οτι βλέπουμε το πρώτο αρχείο
                self.file = os.path.join(self.images_path, self.files[0])
                if pathlib.Path(self.file).suffix != ".pdf":
                    pixmap = QtGui.QPixmap(os.path.join(self.images_path, self.files[0]))
                    resized_pixmap = pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
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
                self.next_image_btn.hide()
                self.previous_image_btn.hide()
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
                self.next_image_btn.show()
                self.previous_image_btn.show()
                # self.save_file_btn.show()
                self.delete_file_btn.show()
        except (IndexError, TypeError):  # αν δεν υπάρχει κανένα αρχείο
            # NoneType οταν ξεκοιναει απο το store.py το self.files = None
            # απόκρηψη κουμπιών
            self.image_label.hide()
            self.next_image_btn.hide()
            self.previous_image_btn.hide()
            self.save_file_btn.hide()
            self.delete_file_btn.hide()
            self.open_pdf_file_btn.hide()

    def next_file(self):
        try:
            if len(self.files) > 1:  # αν υπάρχει πάνω απο ένα αρχείο
                if self.files[self.file_index] == self.files[-1]:  # Αν είναι το τελευταίο αρχείο
                    self.file_index = 0   # να πάει πάλι απο την αρχή

                else:  # Αν δεν είναι το τελευταίο
                    self.file_index += 1  # να πάει στο επώμενο αρχείο

                self.file = os.path.join(self.images_path, self.files[self.file_index])  # να πάει στην δευτερη εικόνα
                if pathlib.Path(self.file).suffix != ".pdf":
                    self.open_pdf_file_btn.hide()  # Απόκρηψη ανοιγμα αρχείου pdf αφου δεν ειναι pdf
                    self.save_file_btn.show()  # Εμφάνηση αποθήκευσης αρχείου αφου δεν ειναι pdf
                    self.open_pdf_file_btn.hide()
                    pixmap = QtGui.QPixmap(os.path.join(self.images_path, self.files[self.file_index]))
                    resized_pixmap = pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
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
                self.next_image_btn.hide()
                self.previous_image_btn.hide()
        except TypeError:  # Αν δεν υπάρχει καποιο αρχείο
            # απόκρηψη κουμπιών
            self.next_image_btn.hide()
            self.previous_image_btn.hide()

    def previous_file(self):
        try:
            if len(self.files) > 1:  # αν υπάρχει πάνω απο ένα αρχείο
                if self.files[self.file_index] == self.files[0]:  # Αν είναι το πρώτο αρχείο
                    self.file_index = -1   # να πάει πάλι απο το τέλος

                else:  # Αν δεν είναι το πρώτο
                    self.file_index -= 1  # να πάει στο προηγούμενο αρχείο

                self.file = os.path.join(self.images_path, self.files[self.file_index])  # να πάει στην δευτερη εικόνα
                if pathlib.Path(self.file).suffix != ".pdf":
                    self.open_pdf_file_btn.hide()  # Απόκρηψη ανοιγμα αρχείου pdf αφου δεν ειναι pdf
                    self.save_file_btn.show()  # Εμφάνηση αποθήκευσης αρχείου αφου δεν ειναι pdf
                    pixmap = QtGui.QPixmap(os.path.join(self.images_path, self.files[self.file_index]))
                    resized_pixmap = pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio)
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
                self.next_image_btn.hide()
                self.previous_image_btn.hide()
        except TypeError:  # Αν δεν υπάρχει καποιο αρχείο
            # απόκρηψη κουμπιών
            self.next_image_btn.hide()
            self.previous_image_btn.hide()

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
        # self.add_to_orders_btn.hide()
        self.next_image_btn.hide()
        self.previous_image_btn.hide()
        self.save_file_btn.hide()
        self.delete_file_btn.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    edit_orders_window = QtWidgets.QWidget()
    ui = Ui_edit_orders_window()
    ui.setupUi(edit_orders_window)
    edit_orders_window.show()
    sys.exit(app.exec_())
