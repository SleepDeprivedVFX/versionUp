
from PySide2.QtCore import (QCoreApplication, QMetaObject, QSize, Qt)
from PySide2.QtWidgets import *
from PySide2.QtGui import *
# from maya import cmds
import os
import sys
import re
import json
import time
from datetime import datetime
import platform


class test_saver(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.pattern = r'(_v\d+)|(_V\d+)'
        self.ui = Ui_SaveAs()
        self.ui.setupUi(self)
        self.ui.cancel_btn.clicked.connect(self.close)

        self.path = r'C:\Users\sleep\OneDrive\Documents\Clients\Marvel\GCY\assets\characters\memnon\scenes'
        # print(self.path)
        self.ui.folder.setText(self.path)
        latest_folder = self.get_latest_local_files(folder=self.path)
        print(latest_folder)

        self.show()

    def get_latest_local_files(self, folder=None):
        if folder:
            if not os.path.exists(folder):
                return False
        else:
            folder = self.path

        get_files = os.listdir(folder)
        get_files = sorted(get_files, reverse=True)
        ext_ui = self.ui.fileType.currentText()
        shortList = []
        for x in get_files:
            test = re.findall(self.pattern, x)
            if test:
                if x.endswith(ext_ui):
                    split_version = x.split(test[0][0])
                    v_name = split_version
                    if v_name not in shortList:
                        shortList.append(x)

        # print(v_name)
        return shortList[0]


class Ui_SaveAs(object):
    def setupUi(self, SaveAs):
        if not SaveAs.objectName():
            SaveAs.setObjectName(u"SaveAs")
        SaveAs.resize(1049, 527)
        SaveAs.setMinimumSize(QSize(969, 385))
        SaveAs.setStyleSheet(u"background-color: rgb(110, 110, 110);\n"
"color: rgb(220, 220, 220);")
        self.verticalLayout = QVBoxLayout(SaveAs)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.Title = QLabel(SaveAs)
        self.Title.setObjectName(u"Title")
        self.Title.setStyleSheet(u"font: 16pt \"MS Shell Dlg 2\";")

        self.verticalLayout.addWidget(self.Title)

        self.output_filename = QLabel(SaveAs)
        self.output_filename.setObjectName(u"output_filename")
        self.output_filename.setStyleSheet(u"font: 12pt \"MS Shell Dlg 2\";")

        self.verticalLayout.addWidget(self.output_filename)

        self.messages = QLabel(SaveAs)
        self.messages.setObjectName(u"messages")
        self.messages.setStyleSheet(u"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 150, 150);")

        self.verticalLayout.addWidget(self.messages)

        self.sideBySide_layout = QHBoxLayout()
        self.sideBySide_layout.setObjectName(u"sideBySide_layout")
        self.saveAs_Layout = QVBoxLayout()
        self.saveAs_Layout.setObjectName(u"saveAs_Layout")
        self.name_layout = QVBoxLayout()
        self.name_layout.setObjectName(u"name_layout")
        self.naming_label = QLabel(SaveAs)
        self.naming_label.setObjectName(u"naming_label")

        self.name_layout.addWidget(self.naming_label)

        self.naming_layout = QHBoxLayout()
        self.naming_layout.setObjectName(u"naming_layout")
        self.autoNaming = QRadioButton(SaveAs)
        self.autoNaming.setObjectName(u"autoNaming")
        self.autoNaming.setChecked(True)

        self.naming_layout.addWidget(self.autoNaming)

        self.customNaming = QRadioButton(SaveAs)
        self.customNaming.setObjectName(u"customNaming")

        self.naming_layout.addWidget(self.customNaming)

        self.naming_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.naming_layout.addItem(self.naming_spacer)

        self.version_label = QLabel(SaveAs)
        self.version_label.setObjectName(u"version_label")

        self.naming_layout.addWidget(self.version_label)

        self.version = QSpinBox(SaveAs)
        self.version.setObjectName(u"version")

        self.naming_layout.addWidget(self.version)


        self.name_layout.addLayout(self.naming_layout)


        self.saveAs_Layout.addLayout(self.name_layout)

        self.folder_layout = QHBoxLayout()
        self.folder_layout.setObjectName(u"folder_layout")
        self.folder_label = QLabel(SaveAs)
        self.folder_label.setObjectName(u"folder_label")

        self.folder_layout.addWidget(self.folder_label)

        self.folder = QLineEdit(SaveAs)
        self.folder.setObjectName(u"folder")

        self.folder_layout.addWidget(self.folder)

        self.folder_btn = QPushButton(SaveAs)
        self.folder_btn.setObjectName(u"folder_btn")

        self.folder_layout.addWidget(self.folder_btn)


        self.saveAs_Layout.addLayout(self.folder_layout)

        self.taskType_layout = QHBoxLayout()
        self.taskType_layout.setObjectName(u"taskType_layout")
        self.taksType_label = QLabel(SaveAs)
        self.taksType_label.setObjectName(u"taksType_label")

        self.taskType_layout.addWidget(self.taksType_label)

        self.taskType = QComboBox(SaveAs)
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.setObjectName(u"taskType")

        self.taskType_layout.addWidget(self.taskType)

        self.taksType_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.taskType_layout.addItem(self.taksType_spacer)

        self.fileType_label = QLabel(SaveAs)
        self.fileType_label.setObjectName(u"fileType_label")

        self.taskType_layout.addWidget(self.fileType_label)

        self.fileType = QComboBox(SaveAs)
        self.fileType.addItem("")
        self.fileType.addItem("")
        self.fileType.setObjectName(u"fileType")

        self.taskType_layout.addWidget(self.fileType)


        self.saveAs_Layout.addLayout(self.taskType_layout)

        self.filename_layout = QHBoxLayout()
        self.filename_layout.setObjectName(u"filename_layout")
        self.filename_label = QLabel(SaveAs)
        self.filename_label.setObjectName(u"filename_label")

        self.filename_layout.addWidget(self.filename_label)

        self.filename = QLineEdit(SaveAs)
        self.filename.setObjectName(u"filename")

        self.filename_layout.addWidget(self.filename)

        self.overwrite = QCheckBox(SaveAs)
        self.overwrite.setObjectName(u"overwrite")

        self.filename_layout.addWidget(self.overwrite)


        self.saveAs_Layout.addLayout(self.filename_layout)

        self.notes_seperator = QFrame(SaveAs)
        self.notes_seperator.setObjectName(u"notes_seperator")
        self.notes_seperator.setFrameShape(QFrame.HLine)
        self.notes_seperator.setFrameShadow(QFrame.Sunken)

        self.saveAs_Layout.addWidget(self.notes_seperator)

        self.notes_layout = QVBoxLayout()
        self.notes_layout.setObjectName(u"notes_layout")
        self.notes_label = QLabel(SaveAs)
        self.notes_label.setObjectName(u"notes_label")

        self.notes_layout.addWidget(self.notes_label)

        self.notes = QTextEdit(SaveAs)
        self.notes.setObjectName(u"notes")

        self.notes_layout.addWidget(self.notes)


        self.saveAs_Layout.addLayout(self.notes_layout)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setObjectName(u"buttons_layout")
        self.buttons_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.buttons_layout.addItem(self.buttons_spacer)

        self.save_btn = QPushButton(SaveAs)
        self.save_btn.setObjectName(u"save_btn")

        self.buttons_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton(SaveAs)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.buttons_layout.addWidget(self.cancel_btn)


        self.saveAs_Layout.addLayout(self.buttons_layout)


        self.sideBySide_layout.addLayout(self.saveAs_Layout)

        self.existingStack_layout = QVBoxLayout()
        self.existingStack_layout.setObjectName(u"existingStack_layout")
        self.existingFile_layout = QVBoxLayout()
        self.existingFile_layout.setObjectName(u"existingFile_layout")
        self.existingFile_label = QLabel(SaveAs)
        self.existingFile_label.setObjectName(u"existingFile_label")

        self.existingFile_layout.addWidget(self.existingFile_label)

        self.existingFile_list = QListWidget(SaveAs)
        self.existingFile_list.setObjectName(u"existingFile_list")

        self.existingFile_layout.addWidget(self.existingFile_list)


        self.existingStack_layout.addLayout(self.existingFile_layout)

        self.existingFIle_separator = QFrame(SaveAs)
        self.existingFIle_separator.setObjectName(u"existingFIle_separator")
        self.existingFIle_separator.setFrameShape(QFrame.HLine)
        self.existingFIle_separator.setFrameShadow(QFrame.Sunken)

        self.existingStack_layout.addWidget(self.existingFIle_separator)

        self.existing_notes = QTextEdit(SaveAs)
        self.existing_notes.setObjectName(u"existing_notes")
        self.existing_notes.setEnabled(False)

        self.existingStack_layout.addWidget(self.existing_notes)

        self.existingFile_spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.existingStack_layout.addItem(self.existingFile_spacer)


        self.sideBySide_layout.addLayout(self.existingStack_layout)


        self.verticalLayout.addLayout(self.sideBySide_layout)

#if QT_CONFIG(shortcut)
        self.naming_label.setBuddy(self.autoNaming)
        self.version_label.setBuddy(self.version)
        self.folder_label.setBuddy(self.folder)
        self.taksType_label.setBuddy(self.taskType)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.notes, self.save_btn)
        QWidget.setTabOrder(self.save_btn, self.folder_btn)
        QWidget.setTabOrder(self.folder_btn, self.taskType)
        QWidget.setTabOrder(self.taskType, self.autoNaming)
        QWidget.setTabOrder(self.autoNaming, self.customNaming)
        QWidget.setTabOrder(self.customNaming, self.version)
        QWidget.setTabOrder(self.version, self.overwrite)
        QWidget.setTabOrder(self.overwrite, self.cancel_btn)
        QWidget.setTabOrder(self.cancel_btn, self.folder)
        QWidget.setTabOrder(self.folder, self.filename)
        QWidget.setTabOrder(self.filename, self.existing_notes)

        self.retranslateUi(SaveAs)

        QMetaObject.connectSlotsByName(SaveAs)
    # setupUi

    def retranslateUi(self, SaveAs):
        SaveAs.setWindowTitle(QCoreApplication.translate("SaveAs", u"Super Saver", None))
        self.Title.setText(QCoreApplication.translate("SaveAs", u"Save As...", None))
        self.output_filename.setText(QCoreApplication.translate("SaveAs", u"output filename", None))
        self.messages.setText(QCoreApplication.translate("SaveAs", u"Errors", None))
        self.autoNaming.setText(QCoreApplication.translate("SaveAs", u"Auto", None))
        self.customNaming.setText(QCoreApplication.translate("SaveAs", u"Custom", None))
        self.version_label.setText(QCoreApplication.translate("SaveAs", u"Version", None))
        self.folder_label.setText(QCoreApplication.translate("SaveAs", u"Save to Folder", None))
        self.folder_btn.setText(QCoreApplication.translate("SaveAs", u"Browse...", None))
        self.taksType_label.setText(QCoreApplication.translate("SaveAs", u"Task Type", None))
        self.taskType.setItemText(0, QCoreApplication.translate("SaveAs", u"Model", None))
        self.taskType.setItemText(1, QCoreApplication.translate("SaveAs", u"LookDev", None))
        self.taskType.setItemText(2, QCoreApplication.translate("SaveAs", u"Rig", None))
        self.taskType.setItemText(3, QCoreApplication.translate("SaveAs", u"Animation", None))
        self.taskType.setItemText(4, QCoreApplication.translate("SaveAs", u"Lighting", None))
        self.taskType.setItemText(5, QCoreApplication.translate("SaveAs", u"Sculpt", None))
        self.taskType.setItemText(6, QCoreApplication.translate("SaveAs", u"Groom", None))
        self.taskType.setItemText(7, QCoreApplication.translate("SaveAs", u"FX", None))
        self.taskType.setItemText(8, QCoreApplication.translate("SaveAs", u"Cloth", None))
        self.taskType.setItemText(9, QCoreApplication.translate("SaveAs", u"Prototype", None))
        self.taskType.setItemText(10, QCoreApplication.translate("SaveAs", u"", None))

        self.fileType_label.setText(QCoreApplication.translate("SaveAs", u"File Type", None))
        self.fileType.setItemText(0, QCoreApplication.translate("SaveAs", u"ma", None))
        self.fileType.setItemText(1, QCoreApplication.translate("SaveAs", u"mb", None))

        self.filename_label.setText(QCoreApplication.translate("SaveAs", u"Filename", None))
        self.overwrite.setText(QCoreApplication.translate("SaveAs", u"Overwrite", None))
        self.notes_label.setText(QCoreApplication.translate("SaveAs", u"Notes", None))
        self.save_btn.setText(QCoreApplication.translate("SaveAs", u"Save", None))
        self.cancel_btn.setText(QCoreApplication.translate("SaveAs", u"Cancel", None))
        self.existingFile_label.setText(QCoreApplication.translate("SaveAs", u"Existing Files", None))
    # retranslateUi


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
    except Exception as e:
        app = QApplication.instance()
    saveas = test_saver()
    try:
        sys.exit(app.exec_())
    except SystemExit as e:
        print(e)
