# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SnapPublisher_UIamTCQw.ui'
##
## Created by: Qt User Interface Compiler version 6.7.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QHBoxLayout, QHeaderView, QLabel, QLineEdit,
    QListWidget, QListWidgetItem, QPushButton, QRadioButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTextEdit,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_SnapPublisher(object):
    def setupUi(self, SnapPublisher):
        if not SnapPublisher.objectName():
            SnapPublisher.setObjectName(u"SnapPublisher")
        SnapPublisher.resize(969, 476)
        SnapPublisher.setMinimumSize(QSize(969, 476))
        SnapPublisher.setStyleSheet(u"background-color: rgb(110, 110, 110);\n"
"color: rgb(220, 220, 220);")
        self.verticalLayout_2 = QVBoxLayout(SnapPublisher)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.Title = QLabel(SnapPublisher)
        self.Title.setObjectName(u"Title")
        self.Title.setStyleSheet(u"font: 16pt \"MS Shell Dlg 2\";")

        self.verticalLayout_2.addWidget(self.Title)

        self.output_filename = QLabel(SnapPublisher)
        self.output_filename.setObjectName(u"output_filename")
        self.output_filename.setStyleSheet(u"font: 10pt \"MS Shell Dlg 2\";")

        self.verticalLayout_2.addWidget(self.output_filename)

        self.snapshot_filename = QLabel(SnapPublisher)
        self.snapshot_filename.setObjectName(u"snapshot_filename")

        self.verticalLayout_2.addWidget(self.snapshot_filename)

        self.publish_filename = QLabel(SnapPublisher)
        self.publish_filename.setObjectName(u"publish_filename")

        self.verticalLayout_2.addWidget(self.publish_filename)

        self.messages = QLabel(SnapPublisher)
        self.messages.setObjectName(u"messages")
        self.messages.setStyleSheet(u"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 150, 150);")

        self.verticalLayout_2.addWidget(self.messages)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.saveAs_Layout = QVBoxLayout()
        self.saveAs_Layout.setObjectName(u"saveAs_Layout")
        self.name_layout = QVBoxLayout()
        self.name_layout.setObjectName(u"name_layout")
        self.naming_label = QLabel(SnapPublisher)
        self.naming_label.setObjectName(u"naming_label")

        self.name_layout.addWidget(self.naming_label)

        self.naming_layout = QHBoxLayout()
        self.naming_layout.setObjectName(u"naming_layout")
        self.autoNaming = QRadioButton(SnapPublisher)
        self.autoNaming.setObjectName(u"autoNaming")
        self.autoNaming.setChecked(True)

        self.naming_layout.addWidget(self.autoNaming)

        self.customNaming = QRadioButton(SnapPublisher)
        self.customNaming.setObjectName(u"customNaming")

        self.naming_layout.addWidget(self.customNaming)

        self.naming_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.naming_layout.addItem(self.naming_spacer)

        self.version_label = QLabel(SnapPublisher)
        self.version_label.setObjectName(u"version_label")

        self.naming_layout.addWidget(self.version_label)

        self.version = QSpinBox(SnapPublisher)
        self.version.setObjectName(u"version")

        self.naming_layout.addWidget(self.version)


        self.name_layout.addLayout(self.naming_layout)


        self.saveAs_Layout.addLayout(self.name_layout)

        self.folder_layout = QHBoxLayout()
        self.folder_layout.setObjectName(u"folder_layout")
        self.folder_label = QLabel(SnapPublisher)
        self.folder_label.setObjectName(u"folder_label")

        self.folder_layout.addWidget(self.folder_label)

        self.folder = QLineEdit(SnapPublisher)
        self.folder.setObjectName(u"folder")

        self.folder_layout.addWidget(self.folder)

        self.folder_btn = QPushButton(SnapPublisher)
        self.folder_btn.setObjectName(u"folder_btn")

        self.folder_layout.addWidget(self.folder_btn)


        self.saveAs_Layout.addLayout(self.folder_layout)

        self.taskType_layout = QHBoxLayout()
        self.taskType_layout.setObjectName(u"taskType_layout")
        self.taksType_label = QLabel(SnapPublisher)
        self.taksType_label.setObjectName(u"taksType_label")

        self.taskType_layout.addWidget(self.taksType_label)

        self.taskType = QComboBox(SnapPublisher)
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

        self.taksType_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.taskType_layout.addItem(self.taksType_spacer)

        self.fileType_label = QLabel(SnapPublisher)
        self.fileType_label.setObjectName(u"fileType_label")

        self.taskType_layout.addWidget(self.fileType_label)

        self.fileType = QComboBox(SnapPublisher)
        self.fileType.addItem("")
        self.fileType.addItem("")
        self.fileType.setObjectName(u"fileType")

        self.taskType_layout.addWidget(self.fileType)


        self.saveAs_Layout.addLayout(self.taskType_layout)

        self.filename_layout = QHBoxLayout()
        self.filename_layout.setObjectName(u"filename_layout")
        self.filename_label = QLabel(SnapPublisher)
        self.filename_label.setObjectName(u"filename_label")

        self.filename_layout.addWidget(self.filename_label)

        self.filename = QLineEdit(SnapPublisher)
        self.filename.setObjectName(u"filename")

        self.filename_layout.addWidget(self.filename)

        self.overwrite = QCheckBox(SnapPublisher)
        self.overwrite.setObjectName(u"overwrite")

        self.filename_layout.addWidget(self.overwrite)


        self.saveAs_Layout.addLayout(self.filename_layout)

        self.showArtist_layout = QHBoxLayout()
        self.showArtist_layout.setObjectName(u"showArtist_layout")
        self.showCode_label = QLabel(SnapPublisher)
        self.showCode_label.setObjectName(u"showCode_label")

        self.showArtist_layout.addWidget(self.showCode_label)

        self.showCode = QLineEdit(SnapPublisher)
        self.showCode.setObjectName(u"showCode")
        self.showCode.setMaximumSize(QSize(60, 16777215))

        self.showArtist_layout.addWidget(self.showCode)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.showArtist_layout.addItem(self.horizontalSpacer)

        self.appendArtist = QCheckBox(SnapPublisher)
        self.appendArtist.setObjectName(u"appendArtist")
        self.appendArtist.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.showArtist_layout.addWidget(self.appendArtist)

        self.artistName_label = QLabel(SnapPublisher)
        self.artistName_label.setObjectName(u"artistName_label")

        self.showArtist_layout.addWidget(self.artistName_label)

        self.artistName = QLineEdit(SnapPublisher)
        self.artistName.setObjectName(u"artistName")

        self.showArtist_layout.addWidget(self.artistName)


        self.saveAs_Layout.addLayout(self.showArtist_layout)

        self.notes_seperator = QFrame(SnapPublisher)
        self.notes_seperator.setObjectName(u"notes_seperator")
        self.notes_seperator.setFrameShape(QFrame.Shape.HLine)
        self.notes_seperator.setFrameShadow(QFrame.Shadow.Sunken)

        self.saveAs_Layout.addWidget(self.notes_seperator)

        self.notes_layout = QVBoxLayout()
        self.notes_layout.setObjectName(u"notes_layout")
        self.notes_label = QLabel(SnapPublisher)
        self.notes_label.setObjectName(u"notes_label")

        self.notes_layout.addWidget(self.notes_label)

        self.notes = QTextEdit(SnapPublisher)
        self.notes.setObjectName(u"notes")
        self.notes.setMinimumSize(QSize(0, 150))

        self.notes_layout.addWidget(self.notes)

        self.existing_notes = QTextEdit(SnapPublisher)
        self.existing_notes.setObjectName(u"existing_notes")
        self.existing_notes.setEnabled(False)
        self.existing_notes.setMinimumSize(QSize(0, 150))

        self.notes_layout.addWidget(self.existing_notes)


        self.saveAs_Layout.addLayout(self.notes_layout)


        self.horizontalLayout_3.addLayout(self.saveAs_Layout)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.existingSnapshots_layout = QVBoxLayout()
        self.existingSnapshots_layout.setObjectName(u"existingSnapshots_layout")
        self.existingSnapshotsLabel = QLabel(SnapPublisher)
        self.existingSnapshotsLabel.setObjectName(u"existingSnapshotsLabel")

        self.existingSnapshots_layout.addWidget(self.existingSnapshotsLabel)

        self.existingSnapshots = QListWidget(SnapPublisher)
        self.existingSnapshots.setObjectName(u"existingSnapshots")

        self.existingSnapshots_layout.addWidget(self.existingSnapshots)

        self.open_btn_layout = QHBoxLayout()
        self.open_btn_layout.setObjectName(u"open_btn_layout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.open_btn_layout.addItem(self.horizontalSpacer_2)

        self.load_snap_btn = QPushButton(SnapPublisher)
        self.load_snap_btn.setObjectName(u"load_snap_btn")

        self.open_btn_layout.addWidget(self.load_snap_btn)


        self.existingSnapshots_layout.addLayout(self.open_btn_layout)


        self.horizontalLayout_2.addLayout(self.existingSnapshots_layout)

        self.horizontalSpacer_4 = QSpacerItem(15, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.existingPubsLabel = QLabel(SnapPublisher)
        self.existingPubsLabel.setObjectName(u"existingPubsLabel")

        self.verticalLayout.addWidget(self.existingPubsLabel)

        self.existingPublishes = QTreeWidget(SnapPublisher)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.existingPublishes.setHeaderItem(__qtreewidgetitem)
        self.existingPublishes.setObjectName(u"existingPublishes")

        self.verticalLayout.addWidget(self.existingPublishes)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.load_pub_btn = QPushButton(SnapPublisher)
        self.load_pub_btn.setObjectName(u"load_pub_btn")

        self.horizontalLayout.addWidget(self.load_pub_btn)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.horizontalLayout_2.addLayout(self.verticalLayout)


        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setObjectName(u"buttons_layout")
        self.buttons_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttons_layout.addItem(self.buttons_spacer)

        self.snapshot_btn = QPushButton(SnapPublisher)
        self.snapshot_btn.setObjectName(u"snapshot_btn")

        self.buttons_layout.addWidget(self.snapshot_btn)

        self.publish_btn = QPushButton(SnapPublisher)
        self.publish_btn.setObjectName(u"publish_btn")

        self.buttons_layout.addWidget(self.publish_btn)

        self.cancel_btn = QPushButton(SnapPublisher)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.buttons_layout.addWidget(self.cancel_btn)


        self.verticalLayout_2.addLayout(self.buttons_layout)

        self.output_filename.raise_()
        self.Title.raise_()
        self.messages.raise_()
        self.snapshot_filename.raise_()
        self.publish_filename.raise_()
#if QT_CONFIG(shortcut)
        self.naming_label.setBuddy(self.autoNaming)
        self.version_label.setBuddy(self.version)
        self.folder_label.setBuddy(self.folder)
        self.taksType_label.setBuddy(self.taskType)
#endif // QT_CONFIG(shortcut)
        QWidget.setTabOrder(self.notes, self.publish_btn)
        QWidget.setTabOrder(self.publish_btn, self.folder_btn)
        QWidget.setTabOrder(self.folder_btn, self.taskType)
        QWidget.setTabOrder(self.taskType, self.autoNaming)
        QWidget.setTabOrder(self.autoNaming, self.customNaming)
        QWidget.setTabOrder(self.customNaming, self.version)
        QWidget.setTabOrder(self.version, self.overwrite)
        QWidget.setTabOrder(self.overwrite, self.cancel_btn)
        QWidget.setTabOrder(self.cancel_btn, self.folder)
        QWidget.setTabOrder(self.folder, self.filename)
        QWidget.setTabOrder(self.filename, self.existing_notes)

        self.retranslateUi(SnapPublisher)

        QMetaObject.connectSlotsByName(SnapPublisher)
    # setupUi

    def retranslateUi(self, SnapPublisher):
        SnapPublisher.setWindowTitle(QCoreApplication.translate("SnapPublisher", u"Snap Publisher", None))
        self.Title.setText(QCoreApplication.translate("SnapPublisher", u"Snap Publisher", None))
        self.output_filename.setText(QCoreApplication.translate("SnapPublisher", u"output filename", None))
        self.snapshot_filename.setText(QCoreApplication.translate("SnapPublisher", u"Snapshot Filename", None))
        self.publish_filename.setText(QCoreApplication.translate("SnapPublisher", u"Publish Filename", None))
        self.messages.setText(QCoreApplication.translate("SnapPublisher", u"Errors", None))
        self.naming_label.setText(QCoreApplication.translate("SnapPublisher", u"Naming", None))
        self.autoNaming.setText(QCoreApplication.translate("SnapPublisher", u"Auto", None))
        self.customNaming.setText(QCoreApplication.translate("SnapPublisher", u"Custom", None))
        self.version_label.setText(QCoreApplication.translate("SnapPublisher", u"Version", None))
        self.folder_label.setText(QCoreApplication.translate("SnapPublisher", u"Save to Folder", None))
        self.folder_btn.setText(QCoreApplication.translate("SnapPublisher", u"Browse...", None))
        self.taksType_label.setText(QCoreApplication.translate("SnapPublisher", u"Task Type", None))
        self.taskType.setItemText(0, QCoreApplication.translate("SnapPublisher", u"model", None))
        self.taskType.setItemText(1, QCoreApplication.translate("SnapPublisher", u"lookdev", None))
        self.taskType.setItemText(2, QCoreApplication.translate("SnapPublisher", u"rig", None))
        self.taskType.setItemText(3, QCoreApplication.translate("SnapPublisher", u"anim", None))
        self.taskType.setItemText(4, QCoreApplication.translate("SnapPublisher", u"sculpt", None))
        self.taskType.setItemText(5, QCoreApplication.translate("SnapPublisher", u"groom", None))
        self.taskType.setItemText(6, QCoreApplication.translate("SnapPublisher", u"fx", None))
        self.taskType.setItemText(7, QCoreApplication.translate("SnapPublisher", u"cloth", None))
        self.taskType.setItemText(8, QCoreApplication.translate("SnapPublisher", u"prototype", None))
        self.taskType.setItemText(9, QCoreApplication.translate("SnapPublisher", u"previs", None))

        self.fileType_label.setText(QCoreApplication.translate("SnapPublisher", u"File Type", None))
        self.fileType.setItemText(0, QCoreApplication.translate("SnapPublisher", u"ma", None))
        self.fileType.setItemText(1, QCoreApplication.translate("SnapPublisher", u"mb", None))

        self.filename_label.setText(QCoreApplication.translate("SnapPublisher", u"Filename", None))
        self.overwrite.setText(QCoreApplication.translate("SnapPublisher", u"Overwrite", None))
        self.showCode_label.setText(QCoreApplication.translate("SnapPublisher", u"Show Code", None))
        self.showCode.setPlaceholderText(QCoreApplication.translate("SnapPublisher", u"GCY", None))
        self.appendArtist.setText(QCoreApplication.translate("SnapPublisher", u"Append Artist", None))
        self.artistName_label.setText(QCoreApplication.translate("SnapPublisher", u"Artist Name", None))
        self.notes_label.setText(QCoreApplication.translate("SnapPublisher", u"Notes", None))
        self.existingSnapshotsLabel.setText(QCoreApplication.translate("SnapPublisher", u"Snapshots", None))
        self.load_snap_btn.setText(QCoreApplication.translate("SnapPublisher", u"Load Snapshot", None))
        self.existingPubsLabel.setText(QCoreApplication.translate("SnapPublisher", u"Publishes", None))
        self.load_pub_btn.setText(QCoreApplication.translate("SnapPublisher", u"Load Publish", None))
        self.snapshot_btn.setText(QCoreApplication.translate("SnapPublisher", u"Snapshot", None))
        self.publish_btn.setText(QCoreApplication.translate("SnapPublisher", u"Publish", None))
        self.cancel_btn.setText(QCoreApplication.translate("SnapPublisher", u"Cancel", None))
    # retranslateUi

