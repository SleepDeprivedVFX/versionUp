# Maya Super Saver

"""
This is a new approach to the Maya_VersionUp.py system.
This one will start with a UI that always runs, instead of just as a pop up if there is
no file.
"""

from maya import cmds
import os
import sys
import re
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

__version__ = '0.0.1'
__author__ = 'Adam Benson'

class super_saver(QWidget):
    def __init__(self, paremt=None):
        QWidget.__init__(self, paremt)
        pth = cmds.file(q=True, sn=True)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.ui = Ui_SaveAsForm()
        self.ui.setupUi(self)
        self.show()


class Ui_SaveAsForm(object):
    def setupUi(self, SaveAsForm):
        if not SaveAsForm.objectName():
            SaveAsForm.setObjectName(u"SaveAsForm")
        SaveAsForm.resize(450, 385)
        SaveAsForm.setMinimumSize(QSize(450, 385))
        SaveAsForm.setMaximumSize(QSize(988, 385))
        SaveAsForm.setStyleSheet(u"background-color: rgb(110, 110, 110);\n"
"color: rgb(235, 235, 235);")
        self.verticalLayout = QVBoxLayout(SaveAsForm)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(SaveAsForm)
        self.label.setObjectName(u"label")
        self.label.setStyleSheet(u"font: 14pt \"MS Shell Dlg 2\";")

        self.verticalLayout.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.folder_label = QLabel(SaveAsForm)
        self.folder_label.setObjectName(u"folder_label")

        self.horizontalLayout.addWidget(self.folder_label)

        self.folder = QLineEdit(SaveAsForm)
        self.folder.setObjectName(u"folder")

        self.horizontalLayout.addWidget(self.folder)

        self.browse_btn = QPushButton(SaveAsForm)
        self.browse_btn.setObjectName(u"browse_btn")

        self.horizontalLayout.addWidget(self.browse_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.taskType_Label = QLabel(SaveAsForm)
        self.taskType_Label.setObjectName(u"taskType_Label")

        self.horizontalLayout_2.addWidget(self.taskType_Label)

        self.taskType = QComboBox(SaveAsForm)
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.addItem("")
        self.taskType.setObjectName(u"taskType")

        self.horizontalLayout_2.addWidget(self.taskType)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.namingGroup = QGroupBox(SaveAsForm)
        self.namingGroup.setObjectName(u"namingGroup")
        self.horizontalLayout_4 = QHBoxLayout(self.namingGroup)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.automaticNaming = QRadioButton(self.namingGroup)
        self.automaticNaming.setObjectName(u"automaticNaming")
        self.automaticNaming.setChecked(True)

        self.horizontalLayout_3.addWidget(self.automaticNaming)

        self.customNaming = QRadioButton(self.namingGroup)
        self.customNaming.setObjectName(u"customNaming")

        self.horizontalLayout_3.addWidget(self.customNaming)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_3)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.version_label = QLabel(self.namingGroup)
        self.version_label.setObjectName(u"version_label")

        self.horizontalLayout_6.addWidget(self.version_label)

        self.version = QSpinBox(self.namingGroup)
        self.version.setObjectName(u"version")
        self.version.setMinimumSize(QSize(0, 0))

        self.horizontalLayout_6.addWidget(self.version)

        self.customVersion = QCheckBox(self.namingGroup)
        self.customVersion.setObjectName(u"customVersion")

        self.horizontalLayout_6.addWidget(self.customVersion)


        self.horizontalLayout_4.addLayout(self.horizontalLayout_6)


        self.verticalLayout.addWidget(self.namingGroup)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.filename_label = QLabel(SaveAsForm)
        self.filename_label.setObjectName(u"filename_label")

        self.horizontalLayout_5.addWidget(self.filename_label)

        self.filename = QLineEdit(SaveAsForm)
        self.filename.setObjectName(u"filename")

        self.horizontalLayout_5.addWidget(self.filename)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_2)

        self.overwrite = QCheckBox(SaveAsForm)
        self.overwrite.setObjectName(u"overwrite")

        self.horizontalLayout_7.addWidget(self.overwrite)


        self.verticalLayout.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_3)

        # Added manually
        self.notes_layout = QVBoxLayout()
        self.notes_layout.setObjectName(u"notes_layout")
        self.notes_layout.setContentsMargins(0, 0, 0, 0)
        self.notes_label = QLabel()
        self.notes_label.setObjectName(u"notes_label")

        self.notes_layout.addWidget(self.notes_label)

        self.notes = QTextEdit()
        self.notes.setObjectName(u"notes")

        self.notes_layout.addWidget(self.notes)

        self.verticalLayout.addLayout(self.notes_layout)
        # End manual build

        self.save_btn = QPushButton(SaveAsForm)
        self.save_btn.setObjectName(u"save_btn")

        self.horizontalLayout_8.addWidget(self.save_btn)

        self.cancel_btn = QPushButton(SaveAsForm)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.horizontalLayout_8.addWidget(self.cancel_btn)


        self.verticalLayout.addLayout(self.horizontalLayout_8)


        self.retranslateUi(SaveAsForm)

        QMetaObject.connectSlotsByName(SaveAsForm)
    # setupUi

    def retranslateUi(self, SaveAsForm):
        SaveAsForm.setWindowTitle(QCoreApplication.translate("SaveAsForm", u"Save As...", None))
        self.label.setText(QCoreApplication.translate("SaveAsForm", u"Save As...", None))
        self.folder_label.setText(QCoreApplication.translate("SaveAsForm", u"Save To Folder", None))
        self.browse_btn.setText(QCoreApplication.translate("SaveAsForm", u"Browse...", None))
        self.taskType_Label.setText(QCoreApplication.translate("SaveAsForm", u"Task Type", None))
        self.taskType.setItemText(0, QCoreApplication.translate("SaveAsForm", u"Model", None))
        self.taskType.setItemText(1, QCoreApplication.translate("SaveAsForm", u"LookDev", None))
        self.taskType.setItemText(2, QCoreApplication.translate("SaveAsForm", u"Sculpt", None))
        self.taskType.setItemText(3, QCoreApplication.translate("SaveAsForm", u"Rig", None))
        self.taskType.setItemText(4, QCoreApplication.translate("SaveAsForm", u"Animation", None))
        self.taskType.setItemText(5, QCoreApplication.translate("SaveAsForm", u"Groom", None))
        self.taskType.setItemText(6, QCoreApplication.translate("SaveAsForm", u"FX", None))
        self.taskType.setItemText(7, QCoreApplication.translate("SaveAsForm", u"Cloth", None))

#if QT_CONFIG(tooltip)
        self.taskType.setToolTip(QCoreApplication.translate("SaveAsForm", u"The kind of task that you are working on.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(statustip)
        self.taskType.setStatusTip(QCoreApplication.translate("SaveAsForm", u"The kind of task that you are working on.", None))
#endif // QT_CONFIG(statustip)
#if QT_CONFIG(whatsthis)
        self.taskType.setWhatsThis(QCoreApplication.translate("SaveAsForm", u"The kind of task that you are working on.", None))
#endif // QT_CONFIG(whatsthis)
#if QT_CONFIG(accessibility)
        self.taskType.setAccessibleName(QCoreApplication.translate("SaveAsForm", u"Task Type", None))
#endif // QT_CONFIG(accessibility)
        self.namingGroup.setTitle(QCoreApplication.translate("SaveAsForm", u"Naming", None))
        self.automaticNaming.setText(QCoreApplication.translate("SaveAsForm", u"Automatic", None))
        self.customNaming.setText(QCoreApplication.translate("SaveAsForm", u"Custom", None))
        self.version_label.setText(QCoreApplication.translate("SaveAsForm", u"Version", None))
        self.customVersion.setText(QCoreApplication.translate("SaveAsForm", u"Custom Version", None))
        self.filename_label.setText(QCoreApplication.translate("SaveAsForm", u"Filename", None))
        self.overwrite.setText(QCoreApplication.translate("SaveAsForm", u"Overwrite", None))
        self.save_btn.setText(QCoreApplication.translate("SaveAsForm", u"Save", None))
        self.cancel_btn.setText(QCoreApplication.translate("SaveAsForm", u"Cancel", None))
        self.notes_label.setText(QCoreApplication.translate("SaveAsForm", u"Notes", None))


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
    except Exception as e:
        app = QApplication.instance()
    saveas = super_saver()
    sys.exit(app.exec_())
