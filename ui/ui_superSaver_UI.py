# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'superSaver_UIYDIVJp.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QFrame, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QPushButton, QRadioButton, QSizePolicy, QSpacerItem,
    QSpinBox, QTabWidget, QTextEdit, QTreeWidget,
    QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_SaveAs(object):
    def setupUi(self, SaveAs):
        if not SaveAs.objectName():
            SaveAs.setObjectName(u"SaveAs")
        SaveAs.resize(969, 698)
        SaveAs.setMinimumSize(QSize(969, 629))
        SaveAs.setStyleSheet(u"background-color: rgb(110, 110, 110);\n"
"color: rgb(220, 220, 220);")
        self.verticalLayout_3 = QVBoxLayout(SaveAs)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.saverTabs = QTabWidget(SaveAs)
        self.saverTabs.setObjectName(u"saverTabs")
        self.MainTab = QWidget()
        self.MainTab.setObjectName(u"MainTab")
        self.verticalLayout_2 = QVBoxLayout(self.MainTab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.Title = QLabel(self.MainTab)
        self.Title.setObjectName(u"Title")
        self.Title.setStyleSheet(u"font: 16pt \"MS Shell Dlg 2\";")

        self.verticalLayout_2.addWidget(self.Title)

        self.output_filename = QLabel(self.MainTab)
        self.output_filename.setObjectName(u"output_filename")
        self.output_filename.setStyleSheet(u"font: 10pt \"MS Shell Dlg 2\";")

        self.verticalLayout_2.addWidget(self.output_filename)

        self.horizontalLayout_38 = QHBoxLayout()
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.horizontalSpacer_22 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_38.addItem(self.horizontalSpacer_22)

        self.taskStatus_label = QLabel(self.MainTab)
        self.taskStatus_label.setObjectName(u"taskStatus_label")

        self.horizontalLayout_38.addWidget(self.taskStatus_label)

        self.taskStatus = QComboBox(self.MainTab)
        self.taskStatus.setObjectName(u"taskStatus")

        self.horizontalLayout_38.addWidget(self.taskStatus)

        self.horizontalSpacer_23 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_38.addItem(self.horizontalSpacer_23)


        self.verticalLayout_2.addLayout(self.horizontalLayout_38)

        self.sideBySide_layout = QHBoxLayout()
        self.sideBySide_layout.setObjectName(u"sideBySide_layout")
        self.saveAs_Layout = QVBoxLayout()
        self.saveAs_Layout.setObjectName(u"saveAs_Layout")
        self.name_layout = QVBoxLayout()
        self.name_layout.setObjectName(u"name_layout")
        self.naming_label = QLabel(self.MainTab)
        self.naming_label.setObjectName(u"naming_label")

        self.name_layout.addWidget(self.naming_label)

        self.naming_layout = QHBoxLayout()
        self.naming_layout.setObjectName(u"naming_layout")
        self.autoNaming = QRadioButton(self.MainTab)
        self.autoNaming.setObjectName(u"autoNaming")
        self.autoNaming.setChecked(True)

        self.naming_layout.addWidget(self.autoNaming)

        self.customNaming = QRadioButton(self.MainTab)
        self.customNaming.setObjectName(u"customNaming")

        self.naming_layout.addWidget(self.customNaming)

        self.naming_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.naming_layout.addItem(self.naming_spacer)

        self.version_label = QLabel(self.MainTab)
        self.version_label.setObjectName(u"version_label")

        self.naming_layout.addWidget(self.version_label)

        self.version = QSpinBox(self.MainTab)
        self.version.setObjectName(u"version")

        self.naming_layout.addWidget(self.version)


        self.name_layout.addLayout(self.naming_layout)


        self.saveAs_Layout.addLayout(self.name_layout)

        self.allowFileCopy = QCheckBox(self.MainTab)
        self.allowFileCopy.setObjectName(u"allowFileCopy")
        self.allowFileCopy.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.saveAs_Layout.addWidget(self.allowFileCopy)

        self.folder_layout = QHBoxLayout()
        self.folder_layout.setObjectName(u"folder_layout")
        self.folder_label = QLabel(self.MainTab)
        self.folder_label.setObjectName(u"folder_label")

        self.folder_layout.addWidget(self.folder_label)

        self.folder = QLineEdit(self.MainTab)
        self.folder.setObjectName(u"folder")

        self.folder_layout.addWidget(self.folder)

        self.folder_btn = QPushButton(self.MainTab)
        self.folder_btn.setObjectName(u"folder_btn")

        self.folder_layout.addWidget(self.folder_btn)


        self.saveAs_Layout.addLayout(self.folder_layout)

        self.taskType_layout = QHBoxLayout()
        self.taskType_layout.setObjectName(u"taskType_layout")
        self.taksType_label = QLabel(self.MainTab)
        self.taksType_label.setObjectName(u"taksType_label")

        self.taskType_layout.addWidget(self.taksType_label)

        self.taskType = QComboBox(self.MainTab)
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

        self.taksType_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.taskType_layout.addItem(self.taksType_spacer)

        self.fileType_label = QLabel(self.MainTab)
        self.fileType_label.setObjectName(u"fileType_label")

        self.taskType_layout.addWidget(self.fileType_label)

        self.fileType = QComboBox(self.MainTab)
        self.fileType.addItem("")
        self.fileType.addItem("")
        self.fileType.setObjectName(u"fileType")

        self.taskType_layout.addWidget(self.fileType)


        self.saveAs_Layout.addLayout(self.taskType_layout)

        self.filename_layout = QHBoxLayout()
        self.filename_layout.setObjectName(u"filename_layout")
        self.filename_label = QLabel(self.MainTab)
        self.filename_label.setObjectName(u"filename_label")

        self.filename_layout.addWidget(self.filename_label)

        self.filename = QLineEdit(self.MainTab)
        self.filename.setObjectName(u"filename")

        self.filename_layout.addWidget(self.filename)

        self.overwrite = QCheckBox(self.MainTab)
        self.overwrite.setObjectName(u"overwrite")

        self.filename_layout.addWidget(self.overwrite)


        self.saveAs_Layout.addLayout(self.filename_layout)

        self.showArtist_layout = QHBoxLayout()
        self.showArtist_layout.setObjectName(u"showArtist_layout")
        self.showCode_label = QLabel(self.MainTab)
        self.showCode_label.setObjectName(u"showCode_label")

        self.showArtist_layout.addWidget(self.showCode_label)

        self.showCode = QLineEdit(self.MainTab)
        self.showCode.setObjectName(u"showCode")
        self.showCode.setMaximumSize(QSize(60, 16777215))

        self.showArtist_layout.addWidget(self.showCode)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.showArtist_layout.addItem(self.horizontalSpacer)

        self.AppendArtist = QCheckBox(self.MainTab)
        self.AppendArtist.setObjectName(u"AppendArtist")
        self.AppendArtist.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.showArtist_layout.addWidget(self.AppendArtist)

        self.artistName_label = QLabel(self.MainTab)
        self.artistName_label.setObjectName(u"artistName_label")

        self.showArtist_layout.addWidget(self.artistName_label)

        self.artistName = QLineEdit(self.MainTab)
        self.artistName.setObjectName(u"artistName")

        self.showArtist_layout.addWidget(self.artistName)


        self.saveAs_Layout.addLayout(self.showArtist_layout)

        self.notes_seperator = QFrame(self.MainTab)
        self.notes_seperator.setObjectName(u"notes_seperator")
        self.notes_seperator.setFrameShape(QFrame.Shape.HLine)
        self.notes_seperator.setFrameShadow(QFrame.Shadow.Sunken)

        self.saveAs_Layout.addWidget(self.notes_seperator)

        self.notes_layout = QVBoxLayout()
        self.notes_layout.setObjectName(u"notes_layout")
        self.notes_label = QLabel(self.MainTab)
        self.notes_label.setObjectName(u"notes_label")
        self.notes_label.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.notes_layout.addWidget(self.notes_label)

        self.notes = QTextEdit(self.MainTab)
        self.notes.setObjectName(u"notes")
        self.notes.setMinimumSize(QSize(0, 150))

        self.notes_layout.addWidget(self.notes)

        self.recentFilesLabel = QLabel(self.MainTab)
        self.recentFilesLabel.setObjectName(u"recentFilesLabel")
        self.recentFilesLabel.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.notes_layout.addWidget(self.recentFilesLabel)

        self.recentFilesList = QListWidget(self.MainTab)
        self.recentFilesList.setObjectName(u"recentFilesList")
        self.recentFilesList.setAlternatingRowColors(True)

        self.notes_layout.addWidget(self.recentFilesList)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.clear_recent_btn = QPushButton(self.MainTab)
        self.clear_recent_btn.setObjectName(u"clear_recent_btn")

        self.horizontalLayout_11.addWidget(self.clear_recent_btn)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_11.addItem(self.horizontalSpacer_12)


        self.notes_layout.addLayout(self.horizontalLayout_11)


        self.saveAs_Layout.addLayout(self.notes_layout)


        self.sideBySide_layout.addLayout(self.saveAs_Layout)

        self.existingStack_layout = QVBoxLayout()
        self.existingStack_layout.setObjectName(u"existingStack_layout")
        self.existingFile_layout = QVBoxLayout()
        self.existingFile_layout.setObjectName(u"existingFile_layout")
        self.existingFile_label = QLabel(self.MainTab)
        self.existingFile_label.setObjectName(u"existingFile_label")
        self.existingFile_label.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.existingFile_layout.addWidget(self.existingFile_label)

        self.existingFile_list = QTreeWidget(self.MainTab)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.existingFile_list.setHeaderItem(__qtreewidgetitem)
        self.existingFile_list.setObjectName(u"existingFile_list")
        self.existingFile_list.setFrameShape(QFrame.Shape.StyledPanel)
        self.existingFile_list.setAlternatingRowColors(True)
        self.existingFile_list.header().setVisible(False)

        self.existingFile_layout.addWidget(self.existingFile_list)

        self.open_btn_layout = QHBoxLayout()
        self.open_btn_layout.setObjectName(u"open_btn_layout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.open_btn_layout.addItem(self.horizontalSpacer_2)

        self.import_btn = QPushButton(self.MainTab)
        self.import_btn.setObjectName(u"import_btn")

        self.open_btn_layout.addWidget(self.import_btn)

        self.load_btn = QPushButton(self.MainTab)
        self.load_btn.setObjectName(u"load_btn")

        self.open_btn_layout.addWidget(self.load_btn)

        self.open_btn = QPushButton(self.MainTab)
        self.open_btn.setObjectName(u"open_btn")

        self.open_btn_layout.addWidget(self.open_btn)


        self.existingFile_layout.addLayout(self.open_btn_layout)


        self.existingStack_layout.addLayout(self.existingFile_layout)


        self.sideBySide_layout.addLayout(self.existingStack_layout)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.snapshots_label = QLabel(self.MainTab)
        self.snapshots_label.setObjectName(u"snapshots_label")
        self.snapshots_label.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.verticalLayout.addWidget(self.snapshots_label)

        self.snapshots = QTreeWidget(self.MainTab)
        __qtreewidgetitem1 = QTreeWidgetItem()
        __qtreewidgetitem1.setText(0, u"1");
        self.snapshots.setHeaderItem(__qtreewidgetitem1)
        self.snapshots.setObjectName(u"snapshots")
        self.snapshots.setHeaderHidden(True)

        self.verticalLayout.addWidget(self.snapshots)

        self.existingFIle_separator = QFrame(self.MainTab)
        self.existingFIle_separator.setObjectName(u"existingFIle_separator")
        self.existingFIle_separator.setFrameShape(QFrame.Shape.HLine)
        self.existingFIle_separator.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.existingFIle_separator)

        self.version_notes_label = QLabel(self.MainTab)
        self.version_notes_label.setObjectName(u"version_notes_label")
        self.version_notes_label.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.verticalLayout.addWidget(self.version_notes_label)

        self.existing_notes = QTextEdit(self.MainTab)
        self.existing_notes.setObjectName(u"existing_notes")
        self.existing_notes.setEnabled(True)
        self.existing_notes.setMinimumSize(QSize(0, 150))

        self.verticalLayout.addWidget(self.existing_notes)


        self.sideBySide_layout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.sideBySide_layout)

        self.buttons_layout = QHBoxLayout()
        self.buttons_layout.setObjectName(u"buttons_layout")
        self.buttons_spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.buttons_layout.addItem(self.buttons_spacer)

        self.publish_btn = QPushButton(self.MainTab)
        self.publish_btn.setObjectName(u"publish_btn")

        self.buttons_layout.addWidget(self.publish_btn)

        self.snap_btn = QPushButton(self.MainTab)
        self.snap_btn.setObjectName(u"snap_btn")

        self.buttons_layout.addWidget(self.snap_btn)

        self.save_btn = QPushButton(self.MainTab)
        self.save_btn.setObjectName(u"save_btn")

        self.buttons_layout.addWidget(self.save_btn)

        self.cancel_btn = QPushButton(self.MainTab)
        self.cancel_btn.setObjectName(u"cancel_btn")

        self.buttons_layout.addWidget(self.cancel_btn)


        self.verticalLayout_2.addLayout(self.buttons_layout)

        self.saverTabs.addTab(self.MainTab, "")
        self.ToolsTab = QWidget()
        self.ToolsTab.setObjectName(u"ToolsTab")
        self.horizontalLayout_37 = QHBoxLayout(self.ToolsTab)
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.toolsGroup = QGroupBox(self.ToolsTab)
        self.toolsGroup.setObjectName(u"toolsGroup")
        self.verticalLayout_4 = QVBoxLayout(self.toolsGroup)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.bakeCam_btn = QPushButton(self.toolsGroup)
        self.bakeCam_btn.setObjectName(u"bakeCam_btn")

        self.verticalLayout_4.addWidget(self.bakeCam_btn)

        self.bakeCamSceneName = QCheckBox(self.toolsGroup)
        self.bakeCamSceneName.setObjectName(u"bakeCamSceneName")
        self.bakeCamSceneName.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.bakeCamSceneName.setChecked(True)

        self.verticalLayout_4.addWidget(self.bakeCamSceneName)

        self.createCam_btn = QPushButton(self.toolsGroup)
        self.createCam_btn.setObjectName(u"createCam_btn")

        self.verticalLayout_4.addWidget(self.createCam_btn)

        self.fbxPub_btn = QPushButton(self.toolsGroup)
        self.fbxPub_btn.setObjectName(u"fbxPub_btn")

        self.verticalLayout_4.addWidget(self.fbxPub_btn)

        self.objPub_btn = QPushButton(self.toolsGroup)
        self.objPub_btn.setObjectName(u"objPub_btn")

        self.verticalLayout_4.addWidget(self.objPub_btn)

        self.abcPub_btn = QPushButton(self.toolsGroup)
        self.abcPub_btn.setObjectName(u"abcPub_btn")

        self.verticalLayout_4.addWidget(self.abcPub_btn)

        self.playblast_btn = QPushButton(self.toolsGroup)
        self.playblast_btn.setObjectName(u"playblast_btn")

        self.verticalLayout_4.addWidget(self.playblast_btn)

        self.build_folders_btn = QPushButton(self.toolsGroup)
        self.build_folders_btn.setObjectName(u"build_folders_btn")

        self.verticalLayout_4.addWidget(self.build_folders_btn)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.horizontalLayout_37.addWidget(self.toolsGroup)

        self.verticalLayout_11 = QVBoxLayout()
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.create_Asset_label = QLabel(self.ToolsTab)
        self.create_Asset_label.setObjectName(u"create_Asset_label")
        self.create_Asset_label.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.verticalLayout_10.addWidget(self.create_Asset_label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.assetShot_type_label = QLabel(self.ToolsTab)
        self.assetShot_type_label.setObjectName(u"assetShot_type_label")

        self.horizontalLayout_3.addWidget(self.assetShot_type_label)

        self.assetShot_type = QComboBox(self.ToolsTab)
        self.assetShot_type.addItem("")
        self.assetShot_type.addItem("")
        self.assetShot_type.addItem("")
        self.assetShot_type.addItem("")
        self.assetShot_type.addItem("")
        self.assetShot_type.addItem("")
        self.assetShot_type.setObjectName(u"assetShot_type")

        self.horizontalLayout_3.addWidget(self.assetShot_type)

        self.horizontalSpacer_20 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_20)


        self.verticalLayout_10.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.asset_name_label = QLabel(self.ToolsTab)
        self.asset_name_label.setObjectName(u"asset_name_label")

        self.horizontalLayout_33.addWidget(self.asset_name_label)

        self.asset_name = QLineEdit(self.ToolsTab)
        self.asset_name.setObjectName(u"asset_name")

        self.horizontalLayout_33.addWidget(self.asset_name)


        self.verticalLayout_10.addLayout(self.horizontalLayout_33)

        self.line_7 = QFrame(self.ToolsTab)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_10.addWidget(self.line_7)

        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.bulk_add_label = QLabel(self.ToolsTab)
        self.bulk_add_label.setObjectName(u"bulk_add_label")

        self.horizontalLayout_36.addWidget(self.bulk_add_label)

        self.bulk_add = QLineEdit(self.ToolsTab)
        self.bulk_add.setObjectName(u"bulk_add")

        self.horizontalLayout_36.addWidget(self.bulk_add)

        self.bulk_add_btn = QPushButton(self.ToolsTab)
        self.bulk_add_btn.setObjectName(u"bulk_add_btn")

        self.horizontalLayout_36.addWidget(self.bulk_add_btn)


        self.verticalLayout_10.addLayout(self.horizontalLayout_36)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.horizontalSpacer_19 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_34.addItem(self.horizontalSpacer_19)

        self.make_asset_btn = QPushButton(self.ToolsTab)
        self.make_asset_btn.setObjectName(u"make_asset_btn")

        self.horizontalLayout_34.addWidget(self.make_asset_btn)


        self.verticalLayout_10.addLayout(self.horizontalLayout_34)


        self.verticalLayout_11.addLayout(self.verticalLayout_10)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.referenceListLabel = QLabel(self.ToolsTab)
        self.referenceListLabel.setObjectName(u"referenceListLabel")
        self.referenceListLabel.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.verticalLayout_5.addWidget(self.referenceListLabel)

        self.referenceList = QListWidget(self.ToolsTab)
        self.referenceList.setObjectName(u"referenceList")
        self.referenceList.setAlternatingRowColors(True)

        self.verticalLayout_5.addWidget(self.referenceList)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.updateRefs_btn = QPushButton(self.ToolsTab)
        self.updateRefs_btn.setObjectName(u"updateRefs_btn")

        self.horizontalLayout.addWidget(self.updateRefs_btn)


        self.verticalLayout_5.addLayout(self.horizontalLayout)


        self.verticalLayout_11.addLayout(self.verticalLayout_5)


        self.horizontalLayout_37.addLayout(self.verticalLayout_11)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.publishes_tree_label = QLabel(self.ToolsTab)
        self.publishes_tree_label.setObjectName(u"publishes_tree_label")
        self.publishes_tree_label.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.verticalLayout_12.addWidget(self.publishes_tree_label)

        self.publishes_tree = QTreeWidget(self.ToolsTab)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setText(0, u"1");
        self.publishes_tree.setHeaderItem(__qtreewidgetitem2)
        self.publishes_tree.setObjectName(u"publishes_tree")
        self.publishes_tree.setAlternatingRowColors(True)
        self.publishes_tree.setHeaderHidden(True)

        self.verticalLayout_12.addWidget(self.publishes_tree)

        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.horizontalSpacer_21 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_35.addItem(self.horizontalSpacer_21)

        self.loadRef_3_btn = QPushButton(self.ToolsTab)
        self.loadRef_3_btn.setObjectName(u"loadRef_3_btn")

        self.horizontalLayout_35.addWidget(self.loadRef_3_btn)

        self.import_3_btn = QPushButton(self.ToolsTab)
        self.import_3_btn.setObjectName(u"import_3_btn")

        self.horizontalLayout_35.addWidget(self.import_3_btn)


        self.verticalLayout_12.addLayout(self.horizontalLayout_35)


        self.verticalLayout_6.addLayout(self.verticalLayout_12)

        self.assetTreeLabel = QLabel(self.ToolsTab)
        self.assetTreeLabel.setObjectName(u"assetTreeLabel")
        self.assetTreeLabel.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.verticalLayout_6.addWidget(self.assetTreeLabel)

        self.assetTree = QTreeWidget(self.ToolsTab)
        __qtreewidgetitem3 = QTreeWidgetItem()
        __qtreewidgetitem3.setText(0, u"1");
        self.assetTree.setHeaderItem(__qtreewidgetitem3)
        self.assetTree.setObjectName(u"assetTree")
        self.assetTree.setAlternatingRowColors(True)
        self.assetTree.setHeaderHidden(True)

        self.verticalLayout_6.addWidget(self.assetTree)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.loadRef_2_btn = QPushButton(self.ToolsTab)
        self.loadRef_2_btn.setObjectName(u"loadRef_2_btn")

        self.horizontalLayout_2.addWidget(self.loadRef_2_btn)

        self.import_2_btn = QPushButton(self.ToolsTab)
        self.import_2_btn.setObjectName(u"import_2_btn")

        self.horizontalLayout_2.addWidget(self.import_2_btn)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)


        self.verticalLayout_13.addLayout(self.verticalLayout_6)


        self.horizontalLayout_37.addLayout(self.verticalLayout_13)

        self.saverTabs.addTab(self.ToolsTab, "")
        self.projectTab = QWidget()
        self.projectTab.setObjectName(u"projectTab")
        self.horizontalLayout_39 = QHBoxLayout(self.projectTab)
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.recent_project_label = QLabel(self.projectTab)
        self.recent_project_label.setObjectName(u"recent_project_label")
        self.recent_project_label.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.verticalLayout_8.addWidget(self.recent_project_label)

        self.recent_projects = QListWidget(self.projectTab)
        self.recent_projects.setObjectName(u"recent_projects")

        self.verticalLayout_8.addWidget(self.recent_projects)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_3)


        self.horizontalLayout_39.addLayout(self.verticalLayout_8)

        self.horizontalSpacer_15 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_39.addItem(self.horizontalSpacer_15)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.projects_label = QLabel(self.projectTab)
        self.projects_label.setObjectName(u"projects_label")
        self.projects_label.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.verticalLayout_9.addWidget(self.projects_label)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.set_project_label = QLabel(self.projectTab)
        self.set_project_label.setObjectName(u"set_project_label")

        self.horizontalLayout_13.addWidget(self.set_project_label)

        self.set_project = QLineEdit(self.projectTab)
        self.set_project.setObjectName(u"set_project")

        self.horizontalLayout_13.addWidget(self.set_project)

        self.set_proejct_btn = QPushButton(self.projectTab)
        self.set_proejct_btn.setObjectName(u"set_proejct_btn")

        self.horizontalLayout_13.addWidget(self.set_proejct_btn)


        self.verticalLayout_9.addLayout(self.horizontalLayout_13)

        self.line = QFrame(self.projectTab)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_9.addWidget(self.line)

        self.new_project_label = QLabel(self.projectTab)
        self.new_project_label.setObjectName(u"new_project_label")
        self.new_project_label.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.verticalLayout_9.addWidget(self.new_project_label)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.new_project_name_label = QLabel(self.projectTab)
        self.new_project_name_label.setObjectName(u"new_project_name_label")

        self.horizontalLayout_14.addWidget(self.new_project_name_label)

        self.new_project_name = QLineEdit(self.projectTab)
        self.new_project_name.setObjectName(u"new_project_name")

        self.horizontalLayout_14.addWidget(self.new_project_name)


        self.verticalLayout_9.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.new_project_folder_Label = QLabel(self.projectTab)
        self.new_project_folder_Label.setObjectName(u"new_project_folder_Label")

        self.horizontalLayout_15.addWidget(self.new_project_folder_Label)

        self.new_project_folder = QLineEdit(self.projectTab)
        self.new_project_folder.setObjectName(u"new_project_folder")

        self.horizontalLayout_15.addWidget(self.new_project_folder)

        self.new_project_folder_btn = QPushButton(self.projectTab)
        self.new_project_folder_btn.setObjectName(u"new_project_folder_btn")

        self.horizontalLayout_15.addWidget(self.new_project_folder_btn)


        self.verticalLayout_9.addLayout(self.horizontalLayout_15)

        self.line_2 = QFrame(self.projectTab)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_9.addWidget(self.line_2)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.scenes_label = QLabel(self.projectTab)
        self.scenes_label.setObjectName(u"scenes_label")

        self.horizontalLayout_16.addWidget(self.scenes_label)

        self.scenes = QLineEdit(self.projectTab)
        self.scenes.setObjectName(u"scenes")

        self.horizontalLayout_16.addWidget(self.scenes)

        self.include_subfolders = QCheckBox(self.projectTab)
        self.include_subfolders.setObjectName(u"include_subfolders")
        self.include_subfolders.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.include_subfolders.setChecked(True)

        self.horizontalLayout_16.addWidget(self.include_subfolders)


        self.verticalLayout_9.addLayout(self.horizontalLayout_16)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.publish_label = QLabel(self.projectTab)
        self.publish_label.setObjectName(u"publish_label")

        self.horizontalLayout_30.addWidget(self.publish_label)

        self.publish = QLineEdit(self.projectTab)
        self.publish.setObjectName(u"publish")

        self.horizontalLayout_30.addWidget(self.publish)


        self.verticalLayout_9.addLayout(self.horizontalLayout_30)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.assets_label = QLabel(self.projectTab)
        self.assets_label.setObjectName(u"assets_label")

        self.horizontalLayout_17.addWidget(self.assets_label)

        self.assets = QLineEdit(self.projectTab)
        self.assets.setObjectName(u"assets")

        self.horizontalLayout_17.addWidget(self.assets)


        self.verticalLayout_9.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.images_label = QLabel(self.projectTab)
        self.images_label.setObjectName(u"images_label")

        self.horizontalLayout_18.addWidget(self.images_label)

        self.images = QLineEdit(self.projectTab)
        self.images.setObjectName(u"images")

        self.horizontalLayout_18.addWidget(self.images)


        self.verticalLayout_9.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.source_images_label = QLabel(self.projectTab)
        self.source_images_label.setObjectName(u"source_images_label")

        self.horizontalLayout_19.addWidget(self.source_images_label)

        self.source_images = QLineEdit(self.projectTab)
        self.source_images.setObjectName(u"source_images")

        self.horizontalLayout_19.addWidget(self.source_images)


        self.verticalLayout_9.addLayout(self.horizontalLayout_19)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.render_data_label = QLabel(self.projectTab)
        self.render_data_label.setObjectName(u"render_data_label")

        self.horizontalLayout_20.addWidget(self.render_data_label)

        self.render_data = QLineEdit(self.projectTab)
        self.render_data.setObjectName(u"render_data")

        self.horizontalLayout_20.addWidget(self.render_data)


        self.verticalLayout_9.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.clips_label = QLabel(self.projectTab)
        self.clips_label.setObjectName(u"clips_label")

        self.horizontalLayout_21.addWidget(self.clips_label)

        self.clips = QLineEdit(self.projectTab)
        self.clips.setObjectName(u"clips")

        self.horizontalLayout_21.addWidget(self.clips)


        self.verticalLayout_9.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.sound_label = QLabel(self.projectTab)
        self.sound_label.setObjectName(u"sound_label")

        self.horizontalLayout_22.addWidget(self.sound_label)

        self.sound = QLineEdit(self.projectTab)
        self.sound.setObjectName(u"sound")

        self.horizontalLayout_22.addWidget(self.sound)


        self.verticalLayout_9.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.scripts_label = QLabel(self.projectTab)
        self.scripts_label.setObjectName(u"scripts_label")

        self.horizontalLayout_23.addWidget(self.scripts_label)

        self.scripts = QLineEdit(self.projectTab)
        self.scripts.setObjectName(u"scripts")

        self.horizontalLayout_23.addWidget(self.scripts)


        self.verticalLayout_9.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.disk_cache_labe = QLabel(self.projectTab)
        self.disk_cache_labe.setObjectName(u"disk_cache_labe")

        self.horizontalLayout_24.addWidget(self.disk_cache_labe)

        self.disk_cache = QLineEdit(self.projectTab)
        self.disk_cache.setObjectName(u"disk_cache")

        self.horizontalLayout_24.addWidget(self.disk_cache)


        self.verticalLayout_9.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.movies_label = QLabel(self.projectTab)
        self.movies_label.setObjectName(u"movies_label")

        self.horizontalLayout_25.addWidget(self.movies_label)

        self.movies = QLineEdit(self.projectTab)
        self.movies.setObjectName(u"movies")

        self.horizontalLayout_25.addWidget(self.movies)


        self.verticalLayout_9.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.time_editor_label = QLabel(self.projectTab)
        self.time_editor_label.setObjectName(u"time_editor_label")

        self.horizontalLayout_26.addWidget(self.time_editor_label)

        self.time_editor = QLineEdit(self.projectTab)
        self.time_editor.setObjectName(u"time_editor")

        self.horizontalLayout_26.addWidget(self.time_editor)


        self.verticalLayout_9.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.Autosave_labe = QLabel(self.projectTab)
        self.Autosave_labe.setObjectName(u"Autosave_labe")

        self.horizontalLayout_27.addWidget(self.Autosave_labe)

        self.autosave = QLineEdit(self.projectTab)
        self.autosave.setObjectName(u"autosave")

        self.horizontalLayout_27.addWidget(self.autosave)


        self.verticalLayout_9.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.scene_ass_label = QLabel(self.projectTab)
        self.scene_ass_label.setObjectName(u"scene_ass_label")

        self.horizontalLayout_28.addWidget(self.scene_ass_label)

        self.scene_ass = QLineEdit(self.projectTab)
        self.scene_ass.setObjectName(u"scene_ass")

        self.horizontalLayout_28.addWidget(self.scene_ass)


        self.verticalLayout_9.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalSpacer_14 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_14)

        self.create_project_btn = QPushButton(self.projectTab)
        self.create_project_btn.setObjectName(u"create_project_btn")

        self.horizontalLayout_29.addWidget(self.create_project_btn)


        self.verticalLayout_9.addLayout(self.horizontalLayout_29)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_4)


        self.horizontalLayout_39.addLayout(self.verticalLayout_9)

        self.horizontalSpacer_16 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_39.addItem(self.horizontalSpacer_16)

        self.saverTabs.addTab(self.projectTab, "")
        self.SettingsTab = QWidget()
        self.SettingsTab.setObjectName(u"SettingsTab")
        self.verticalLayout_7 = QVBoxLayout(self.SettingsTab)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.showName_label = QLabel(self.SettingsTab)
        self.showName_label.setObjectName(u"showName_label")

        self.horizontalLayout_4.addWidget(self.showName_label)

        self.showName = QLineEdit(self.SettingsTab)
        self.showName.setObjectName(u"showName")

        self.horizontalLayout_4.addWidget(self.showName)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_10)


        self.verticalLayout_7.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.showCodeSet_label = QLabel(self.SettingsTab)
        self.showCodeSet_label.setObjectName(u"showCodeSet_label")

        self.horizontalLayout_5.addWidget(self.showCodeSet_label)

        self.showCodeSet = QLineEdit(self.SettingsTab)
        self.showCodeSet.setObjectName(u"showCodeSet")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.showCodeSet.sizePolicy().hasHeightForWidth())
        self.showCodeSet.setSizePolicy(sizePolicy)

        self.horizontalLayout_5.addWidget(self.showCodeSet)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_5.addItem(self.horizontalSpacer_5)


        self.verticalLayout_7.addLayout(self.horizontalLayout_5)

        self.line_3 = QFrame(self.SettingsTab)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_3)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.defaultResolution_label = QLabel(self.SettingsTab)
        self.defaultResolution_label.setObjectName(u"defaultResolution_label")

        self.horizontalLayout_6.addWidget(self.defaultResolution_label)

        self.resolutionWidth_label = QLabel(self.SettingsTab)
        self.resolutionWidth_label.setObjectName(u"resolutionWidth_label")

        self.horizontalLayout_6.addWidget(self.resolutionWidth_label)

        self.resolutionWidth = QLineEdit(self.SettingsTab)
        self.resolutionWidth.setObjectName(u"resolutionWidth")
        sizePolicy.setHeightForWidth(self.resolutionWidth.sizePolicy().hasHeightForWidth())
        self.resolutionWidth.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.resolutionWidth)

        self.resolutionHeight_label = QLabel(self.SettingsTab)
        self.resolutionHeight_label.setObjectName(u"resolutionHeight_label")

        self.horizontalLayout_6.addWidget(self.resolutionHeight_label)

        self.resolutionHeight = QLineEdit(self.SettingsTab)
        self.resolutionHeight.setObjectName(u"resolutionHeight")
        sizePolicy.setHeightForWidth(self.resolutionHeight.sizePolicy().hasHeightForWidth())
        self.resolutionHeight.setSizePolicy(sizePolicy)

        self.horizontalLayout_6.addWidget(self.resolutionHeight)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer_6)


        self.verticalLayout_7.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.filmbackLabel = QLabel(self.SettingsTab)
        self.filmbackLabel.setObjectName(u"filmbackLabel")

        self.horizontalLayout_7.addWidget(self.filmbackLabel)

        self.filmback_width_label = QLabel(self.SettingsTab)
        self.filmback_width_label.setObjectName(u"filmback_width_label")

        self.horizontalLayout_7.addWidget(self.filmback_width_label)

        self.filmback_width = QLineEdit(self.SettingsTab)
        self.filmback_width.setObjectName(u"filmback_width")
        sizePolicy.setHeightForWidth(self.filmback_width.sizePolicy().hasHeightForWidth())
        self.filmback_width.setSizePolicy(sizePolicy)

        self.horizontalLayout_7.addWidget(self.filmback_width)

        self.filmback_height_label = QLabel(self.SettingsTab)
        self.filmback_height_label.setObjectName(u"filmback_height_label")

        self.horizontalLayout_7.addWidget(self.filmback_height_label)

        self.filmback_height = QLineEdit(self.SettingsTab)
        self.filmback_height.setObjectName(u"filmback_height")
        sizePolicy.setHeightForWidth(self.filmback_height.sizePolicy().hasHeightForWidth())
        self.filmback_height.setSizePolicy(sizePolicy)

        self.horizontalLayout_7.addWidget(self.filmback_height)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)


        self.verticalLayout_7.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.image_format_label = QLabel(self.SettingsTab)
        self.image_format_label.setObjectName(u"image_format_label")

        self.horizontalLayout_32.addWidget(self.image_format_label)

        self.image_format = QComboBox(self.SettingsTab)
        self.image_format.addItem("")
        self.image_format.addItem("")
        self.image_format.addItem("")
        self.image_format.addItem("")
        self.image_format.addItem("")
        self.image_format.addItem("")
        self.image_format.setObjectName(u"image_format")

        self.horizontalLayout_32.addWidget(self.image_format)

        self.horizontalSpacer_18 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_18)


        self.verticalLayout_7.addLayout(self.horizontalLayout_32)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.SceneScale_Label = QLabel(self.SettingsTab)
        self.SceneScale_Label.setObjectName(u"SceneScale_Label")

        self.horizontalLayout_8.addWidget(self.SceneScale_Label)

        self.sceneScale = QLineEdit(self.SettingsTab)
        self.sceneScale.setObjectName(u"sceneScale")
        sizePolicy.setHeightForWidth(self.sceneScale.sizePolicy().hasHeightForWidth())
        self.sceneScale.setSizePolicy(sizePolicy)

        self.horizontalLayout_8.addWidget(self.sceneScale)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_8.addItem(self.horizontalSpacer_8)


        self.verticalLayout_7.addLayout(self.horizontalLayout_8)

        self.line_4 = QFrame(self.SettingsTab)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_4)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.recent_file_count_label = QLabel(self.SettingsTab)
        self.recent_file_count_label.setObjectName(u"recent_file_count_label")

        self.horizontalLayout_10.addWidget(self.recent_file_count_label)

        self.recent_file_count = QSpinBox(self.SettingsTab)
        self.recent_file_count.setObjectName(u"recent_file_count")
        self.recent_file_count.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)

        self.horizontalLayout_10.addWidget(self.recent_file_count)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_11)


        self.verticalLayout_7.addLayout(self.horizontalLayout_10)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.autoload = QCheckBox(self.SettingsTab)
        self.autoload.setObjectName(u"autoload")
        self.autoload.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        self.horizontalLayout_12.addWidget(self.autoload)

        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_13)


        self.verticalLayout_7.addLayout(self.horizontalLayout_12)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.autosaver = QCheckBox(self.SettingsTab)
        self.autosaver.setObjectName(u"autosaver")
        self.autosaver.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.autosaver.setChecked(True)

        self.horizontalLayout_31.addWidget(self.autosaver)

        self.iterations_label = QLabel(self.SettingsTab)
        self.iterations_label.setObjectName(u"iterations_label")

        self.horizontalLayout_31.addWidget(self.iterations_label)

        self.autosave_count = QSpinBox(self.SettingsTab)
        self.autosave_count.setObjectName(u"autosave_count")
        sizePolicy.setHeightForWidth(self.autosave_count.sizePolicy().hasHeightForWidth())
        self.autosave_count.setSizePolicy(sizePolicy)
        self.autosave_count.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.autosave_count.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.PlusMinus)

        self.horizontalLayout_31.addWidget(self.autosave_count)

        self.horizontalSpacer_17 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_31.addItem(self.horizontalSpacer_17)


        self.verticalLayout_7.addLayout(self.horizontalLayout_31)

        self.line_5 = QFrame(self.SettingsTab)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_5)

        self.hotkeys_label = QLabel(self.SettingsTab)
        self.hotkeys_label.setObjectName(u"hotkeys_label")
        self.hotkeys_label.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.verticalLayout_7.addWidget(self.hotkeys_label)

        self.hotkeys = QLabel(self.SettingsTab)
        self.hotkeys.setObjectName(u"hotkeys")
        self.hotkeys.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.verticalLayout_7.addWidget(self.hotkeys)

        self.line_6 = QFrame(self.SettingsTab)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line_6)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_9)

        self.save_config_btn = QPushButton(self.SettingsTab)
        self.save_config_btn.setObjectName(u"save_config_btn")

        self.horizontalLayout_9.addWidget(self.save_config_btn)


        self.verticalLayout_7.addLayout(self.horizontalLayout_9)

        self.saverTabs.addTab(self.SettingsTab, "")

        self.verticalLayout_3.addWidget(self.saverTabs)

        self.messages = QLabel(SaveAs)
        self.messages.setObjectName(u"messages")
        self.messages.setStyleSheet(u"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 150, 150);")

        self.verticalLayout_3.addWidget(self.messages)

#if QT_CONFIG(shortcut)
        self.naming_label.setBuddy(self.autoNaming)
        self.version_label.setBuddy(self.version)
        self.folder_label.setBuddy(self.folder)
        self.taksType_label.setBuddy(self.taskType)
        self.filename_label.setBuddy(self.filename)
        self.showCode_label.setBuddy(self.showCode)
        self.artistName_label.setBuddy(self.artistName)
        self.notes_label.setBuddy(self.notes)
        self.recentFilesLabel.setBuddy(self.recentFilesList)
        self.existingFile_label.setBuddy(self.existingFile_list)
        self.snapshots_label.setBuddy(self.snapshots)
        self.version_notes_label.setBuddy(self.existing_notes)
        self.assetShot_type_label.setBuddy(self.assetShot_type)
        self.asset_name_label.setBuddy(self.asset_name)
        self.referenceListLabel.setBuddy(self.referenceList)
        self.publishes_tree_label.setBuddy(self.publishes_tree)
        self.assetTreeLabel.setBuddy(self.assetTree)
        self.set_project_label.setBuddy(self.set_project)
        self.new_project_name_label.setBuddy(self.new_project_name)
        self.new_project_folder_Label.setBuddy(self.new_project_folder)
        self.scenes_label.setBuddy(self.scenes)
        self.assets_label.setBuddy(self.assets)
        self.images_label.setBuddy(self.images)
        self.source_images_label.setBuddy(self.source_images)
        self.render_data_label.setBuddy(self.render_data)
        self.clips_label.setBuddy(self.clips)
        self.sound_label.setBuddy(self.sound)
        self.scripts_label.setBuddy(self.scripts)
        self.disk_cache_labe.setBuddy(self.disk_cache)
        self.movies_label.setBuddy(self.movies)
        self.time_editor_label.setBuddy(self.time_editor)
        self.Autosave_labe.setBuddy(self.autosave)
        self.scene_ass_label.setBuddy(self.scene_ass)
        self.showName_label.setBuddy(self.showName)
        self.showCodeSet_label.setBuddy(self.showCodeSet)
        self.resolutionWidth_label.setBuddy(self.resolutionWidth)
        self.resolutionHeight_label.setBuddy(self.resolutionHeight)
        self.filmback_width_label.setBuddy(self.filmback_width)
        self.filmback_height_label.setBuddy(self.filmback_height)
        self.image_format_label.setBuddy(self.image_format)
        self.SceneScale_Label.setBuddy(self.sceneScale)
        self.recent_file_count_label.setBuddy(self.recent_file_count)
        self.iterations_label.setBuddy(self.autosave_count)
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

        self.retranslateUi(SaveAs)

        self.saverTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SaveAs)
    # setupUi

    def retranslateUi(self, SaveAs):
        SaveAs.setWindowTitle(QCoreApplication.translate("SaveAs", u"Super Saver", None))
        self.Title.setText(QCoreApplication.translate("SaveAs", u"Save As...", None))
#if QT_CONFIG(tooltip)
        self.output_filename.setToolTip(QCoreApplication.translate("SaveAs", u"This is the output filename and path for what's going to be saved.", None))
#endif // QT_CONFIG(tooltip)
        self.output_filename.setText(QCoreApplication.translate("SaveAs", u"output filename", None))
        self.taskStatus_label.setText(QCoreApplication.translate("SaveAs", u"Task Status", None))
        self.naming_label.setText(QCoreApplication.translate("SaveAs", u"Naming", None))
#if QT_CONFIG(tooltip)
        self.autoNaming.setToolTip(QCoreApplication.translate("SaveAs", u"Auto Naming (Recommended)", None))
#endif // QT_CONFIG(tooltip)
        self.autoNaming.setText(QCoreApplication.translate("SaveAs", u"Auto", None))
#if QT_CONFIG(tooltip)
        self.customNaming.setToolTip(QCoreApplication.translate("SaveAs", u"Custom Naming - Only if the auto naming isn't right, or you want a special name", None))
#endif // QT_CONFIG(tooltip)
        self.customNaming.setText(QCoreApplication.translate("SaveAs", u"Custom", None))
#if QT_CONFIG(tooltip)
        self.version_label.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>Sets the version number</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.version_label.setText(QCoreApplication.translate("SaveAs", u"Version", None))
#if QT_CONFIG(tooltip)
        self.version.setToolTip(QCoreApplication.translate("SaveAs", u"File Version Number", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.allowFileCopy.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>This function overrides the default file naming. </p><p>By checking this option you make it so that the current file can be &quot;saved as&quot; another asset or shot. </p><p>Check this box to copy the current file to a new asset or shot by also selecting the folder you want to save it to in the Existing FIles list</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.allowFileCopy.setText(QCoreApplication.translate("SaveAs", u"Allow File Copy From --> To", None))
#if QT_CONFIG(tooltip)
        self.folder_label.setToolTip(QCoreApplication.translate("SaveAs", u"This is the folder that the file will be saved into", None))
#endif // QT_CONFIG(tooltip)
        self.folder_label.setText(QCoreApplication.translate("SaveAs", u"Save to Folder", None))
#if QT_CONFIG(tooltip)
        self.folder.setToolTip(QCoreApplication.translate("SaveAs", u"This is the folder that the file will be saved into", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.folder_btn.setToolTip(QCoreApplication.translate("SaveAs", u"Browse for a file location", None))
#endif // QT_CONFIG(tooltip)
        self.folder_btn.setText(QCoreApplication.translate("SaveAs", u"Browse...", None))
#if QT_CONFIG(tooltip)
        self.taksType_label.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>Choose the task type for the file.  This will be appended to the filename.  </p><p>Changing this at any time will rename the file to the latest version of that Task Type</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.taksType_label.setText(QCoreApplication.translate("SaveAs", u"Task Type", None))
        self.taskType.setItemText(0, QCoreApplication.translate("SaveAs", u"model", None))
        self.taskType.setItemText(1, QCoreApplication.translate("SaveAs", u"sculpt", None))
        self.taskType.setItemText(2, QCoreApplication.translate("SaveAs", u"lookdev", None))
        self.taskType.setItemText(3, QCoreApplication.translate("SaveAs", u"rig", None))
        self.taskType.setItemText(4, QCoreApplication.translate("SaveAs", u"groom", None))
        self.taskType.setItemText(5, QCoreApplication.translate("SaveAs", u"layout", None))
        self.taskType.setItemText(6, QCoreApplication.translate("SaveAs", u"previs", None))
        self.taskType.setItemText(7, QCoreApplication.translate("SaveAs", u"anim", None))
        self.taskType.setItemText(8, QCoreApplication.translate("SaveAs", u"fx", None))
        self.taskType.setItemText(9, QCoreApplication.translate("SaveAs", u"cloth", None))
        self.taskType.setItemText(10, QCoreApplication.translate("SaveAs", u"prototype", None))

#if QT_CONFIG(tooltip)
        self.taskType.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>Choose the task type for the file.  This will be appended to the filename.  </p><p>Changing this at any time will rename the file to the latest version of that Task Type</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.fileType_label.setToolTip(QCoreApplication.translate("SaveAs", u"Maya file type.  Either Ascii or Binary", None))
#endif // QT_CONFIG(tooltip)
        self.fileType_label.setText(QCoreApplication.translate("SaveAs", u"File Type", None))
        self.fileType.setItemText(0, QCoreApplication.translate("SaveAs", u"ma", None))
        self.fileType.setItemText(1, QCoreApplication.translate("SaveAs", u"mb", None))

#if QT_CONFIG(tooltip)
        self.fileType.setToolTip(QCoreApplication.translate("SaveAs", u"Maya file type.  Either Ascii or Binary", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.filename_label.setToolTip(QCoreApplication.translate("SaveAs", u"The base name is typically the asset or shot name", None))
#endif // QT_CONFIG(tooltip)
        self.filename_label.setText(QCoreApplication.translate("SaveAs", u"Base Name", None))
#if QT_CONFIG(tooltip)
        self.filename.setToolTip(QCoreApplication.translate("SaveAs", u"The base name is typically the asset or shot name", None))
#endif // QT_CONFIG(tooltip)
        self.overwrite.setText(QCoreApplication.translate("SaveAs", u"Overwrite", None))
#if QT_CONFIG(tooltip)
        self.showCode_label.setToolTip(QCoreApplication.translate("SaveAs", u"The Show Code can be created automatically, or changed in the Settings - Configuration tab", None))
#endif // QT_CONFIG(tooltip)
        self.showCode_label.setText(QCoreApplication.translate("SaveAs", u"Show Code", None))
#if QT_CONFIG(tooltip)
        self.showCode.setToolTip(QCoreApplication.translate("SaveAs", u"The Show Code can be created automatically, or changed in the Settings - Configuration tab", None))
#endif // QT_CONFIG(tooltip)
        self.showCode.setPlaceholderText(QCoreApplication.translate("SaveAs", u"ABC", None))
        self.AppendArtist.setText(QCoreApplication.translate("SaveAs", u"Append Artist", None))
        self.artistName_label.setText(QCoreApplication.translate("SaveAs", u"Artist Name", None))
        self.notes_label.setText(QCoreApplication.translate("SaveAs", u"Notes", None))
#if QT_CONFIG(tooltip)
        self.notes.setToolTip(QCoreApplication.translate("SaveAs", u"Notes must be added to all Save V Up, Publish and Snapshot actions", None))
#endif // QT_CONFIG(tooltip)
        self.recentFilesLabel.setText(QCoreApplication.translate("SaveAs", u"Recent Files", None))
#if QT_CONFIG(tooltip)
        self.recentFilesList.setToolTip(QCoreApplication.translate("SaveAs", u"Recently Opened Files List.  Double click to quick re-open", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.clear_recent_btn.setToolTip(QCoreApplication.translate("SaveAs", u"Clears the recent file history", None))
#endif // QT_CONFIG(tooltip)
        self.clear_recent_btn.setText(QCoreApplication.translate("SaveAs", u"Clear Recent History", None))
#if QT_CONFIG(tooltip)
        self.existingFile_label.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>These are the existing files in your project.  </p><p>Double click or use the open command to open them.  </p><p>You can also use this list to set the name of a new file or a file with Allow File Copy From --&gt; To checked.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.existingFile_label.setText(QCoreApplication.translate("SaveAs", u"Existing Files", None))
#if QT_CONFIG(tooltip)
        self.existingFile_list.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>These are the existing files in your project.  </p><p>Double click or use the open command to open them.  </p><p>You can also use this list to set the name of a new file or a file with Allow File Copy From --&gt; To checked.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.import_btn.setText(QCoreApplication.translate("SaveAs", u"Import", None))
        self.load_btn.setText(QCoreApplication.translate("SaveAs", u"Load Ref", None))
        self.open_btn.setText(QCoreApplication.translate("SaveAs", u"Open", None))
#if QT_CONFIG(tooltip)
        self.snapshots_label.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>Snapshots are quick saves that store a date stamped sub-version of your current file without having to version up. </p><p>You can double click a snapshot to reload it into the current scene.  </p><p>Unsaved changes will be prompted to auto-snapshot before loading a previous snapshot</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.snapshots_label.setText(QCoreApplication.translate("SaveAs", u"Snapshots", None))
#if QT_CONFIG(tooltip)
        self.snapshots.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>Snapshots are quick saves that store a date stamped sub-version of your current file without having to version up. </p><p>You can double click a snapshot to reload it into the current scene.  </p><p>Unsaved changes will be prompted to auto-snapshot before loading a previous snapshot</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.version_notes_label.setToolTip(QCoreApplication.translate("SaveAs", u"This shows notes for the current file selected in the Existing Files list", None))
#endif // QT_CONFIG(tooltip)
        self.version_notes_label.setText(QCoreApplication.translate("SaveAs", u"Version Note", None))
#if QT_CONFIG(tooltip)
        self.existing_notes.setToolTip(QCoreApplication.translate("SaveAs", u"This shows notes for the current file selected in the Existing Files list", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.publish_btn.setToolTip(QCoreApplication.translate("SaveAs", u"Ctrl + P", None))
#endif // QT_CONFIG(tooltip)
        self.publish_btn.setText(QCoreApplication.translate("SaveAs", u"Publish", None))
#if QT_CONFIG(tooltip)
        self.snap_btn.setToolTip(QCoreApplication.translate("SaveAs", u"Ctrl + T", None))
#endif // QT_CONFIG(tooltip)
        self.snap_btn.setText(QCoreApplication.translate("SaveAs", u"Snapshot", None))
#if QT_CONFIG(tooltip)
        self.save_btn.setToolTip(QCoreApplication.translate("SaveAs", u"Ctrl + Enter", None))
#endif // QT_CONFIG(tooltip)
        self.save_btn.setText(QCoreApplication.translate("SaveAs", u"Save V Up", None))
#if QT_CONFIG(tooltip)
        self.cancel_btn.setToolTip(QCoreApplication.translate("SaveAs", u"Esc", None))
#endif // QT_CONFIG(tooltip)
        self.cancel_btn.setText(QCoreApplication.translate("SaveAs", u"Cancel", None))
        self.saverTabs.setTabText(self.saverTabs.indexOf(self.MainTab), QCoreApplication.translate("SaveAs", u"Save - Publish - Snap", None))
        self.toolsGroup.setTitle(QCoreApplication.translate("SaveAs", u"Tools", None))
        self.bakeCam_btn.setText(QCoreApplication.translate("SaveAs", u"Bake Camera", None))
#if QT_CONFIG(tooltip)
        self.bakeCamSceneName.setToolTip(QCoreApplication.translate("SaveAs", u"Renames the baked camera to include the shot or asset name", None))
#endif // QT_CONFIG(tooltip)
        self.bakeCamSceneName.setText(QCoreApplication.translate("SaveAs", u"Use Shot/Asset as Cam Name", None))
        self.createCam_btn.setText(QCoreApplication.translate("SaveAs", u"Create Camera", None))
        self.fbxPub_btn.setText(QCoreApplication.translate("SaveAs", u"Publish Selection as FBX", None))
        self.objPub_btn.setText(QCoreApplication.translate("SaveAs", u"Publish Selection as OBJ", None))
        self.abcPub_btn.setText(QCoreApplication.translate("SaveAs", u"Publish Selection as Alembic", None))
        self.playblast_btn.setText(QCoreApplication.translate("SaveAs", u"Playblaster", None))
        self.build_folders_btn.setText(QCoreApplication.translate("SaveAs", u"Build Default Folders", None))
        self.create_Asset_label.setText(QCoreApplication.translate("SaveAs", u"Create Asset / Shot", None))
#if QT_CONFIG(tooltip)
        self.assetShot_type_label.setToolTip(QCoreApplication.translate("SaveAs", u"Create a new Asset or Shot.  Adding an asset or shot here creates a folder and a base model or layout file.  In assets it will also create lookdev and rig files and reference the model file into it.", None))
#endif // QT_CONFIG(tooltip)
        self.assetShot_type_label.setText(QCoreApplication.translate("SaveAs", u"Type", None))
        self.assetShot_type.setItemText(0, QCoreApplication.translate("SaveAs", u"Cams", None))
        self.assetShot_type.setItemText(1, QCoreApplication.translate("SaveAs", u"Char", None))
        self.assetShot_type.setItemText(2, QCoreApplication.translate("SaveAs", u"Env", None))
        self.assetShot_type.setItemText(3, QCoreApplication.translate("SaveAs", u"Prop", None))
        self.assetShot_type.setItemText(4, QCoreApplication.translate("SaveAs", u"Shots", None))
        self.assetShot_type.setItemText(5, QCoreApplication.translate("SaveAs", u"Veh", None))

#if QT_CONFIG(tooltip)
        self.assetShot_type.setToolTip(QCoreApplication.translate("SaveAs", u"Create a new Asset or Shot.  Adding an asset or shot here creates a folder and a base model or layout file.  In assets it will also create lookdev and rig files and reference the model file into it.", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.asset_name_label.setToolTip(QCoreApplication.translate("SaveAs", u"The name or the asset or shot.  Do not add show codes or other details that you don't want added to the name", None))
#endif // QT_CONFIG(tooltip)
        self.asset_name_label.setText(QCoreApplication.translate("SaveAs", u"Name", None))
#if QT_CONFIG(tooltip)
        self.asset_name.setToolTip(QCoreApplication.translate("SaveAs", u"The name or the asset or shot.  Do not add show codes or other details that you don't want added to the name", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.bulk_add_label.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>You can add a bulk of items from a CSV file. </p><p>The CSV file must not have a header.</p><p>The first column must be the asset or shot name.</p><p>The second column must be the Type (Cams, Char, Env, Prop, Veh,, or Shot).</p><p>If the second column is blank, the root scenes folder will be used.</p><p>Do not add a Name in the Name field if using this option.</p><p>Bulk item add only creates the folder structures and not new files.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.bulk_add_label.setText(QCoreApplication.translate("SaveAs", u"Bulk Add from CSV", None))
#if QT_CONFIG(tooltip)
        self.bulk_add.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>You can add a bulk of items from a CSV file. </p><p>The CSV file must not have a header.</p><p>The first column must be the asset or shot name.</p><p>The second column must be the Type (Cams, Char, Env, Prop, Veh,, or Shot).</p><p>If the second column is blank, the root scenes folder will be used.</p><p>Do not add a Name in the Name field if using this option.</p><p>Bulk item add only creates the folder structures and not new files.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.bulk_add_btn.setText(QCoreApplication.translate("SaveAs", u"Browse...", None))
#if QT_CONFIG(tooltip)
        self.make_asset_btn.setToolTip(QCoreApplication.translate("SaveAs", u"Creates the asset or shot", None))
#endif // QT_CONFIG(tooltip)
        self.make_asset_btn.setText(QCoreApplication.translate("SaveAs", u"Make Asset/Shot", None))
#if QT_CONFIG(tooltip)
        self.referenceListLabel.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>This is a list of references that have been added to your scene.  </p><p>Green references are up to date.  </p><p>Red references are out of date</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.referenceListLabel.setText(QCoreApplication.translate("SaveAs", u"Loaded References", None))
#if QT_CONFIG(tooltip)
        self.referenceList.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>This is a list of references that have been added to your scene.  </p><p>Green references are up to date.  </p><p>Red references are out of date</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.updateRefs_btn.setText(QCoreApplication.translate("SaveAs", u"Update Selected", None))
#if QT_CONFIG(tooltip)
        self.publishes_tree_label.setToolTip(QCoreApplication.translate("SaveAs", u"The list of items that have been published for the project", None))
#endif // QT_CONFIG(tooltip)
        self.publishes_tree_label.setText(QCoreApplication.translate("SaveAs", u"Publishes", None))
#if QT_CONFIG(tooltip)
        self.publishes_tree.setToolTip(QCoreApplication.translate("SaveAs", u"The list of items that have been published for the project", None))
#endif // QT_CONFIG(tooltip)
        self.loadRef_3_btn.setText(QCoreApplication.translate("SaveAs", u"Load Ref", None))
        self.import_3_btn.setText(QCoreApplication.translate("SaveAs", u"Import", None))
#if QT_CONFIG(tooltip)
        self.assetTreeLabel.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>The list of assets in the assets folder.  </p><p>This is usually just FBX, OBJ or Alembic files but can be other items as well.  </p><p>These files are not considered Published.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.assetTreeLabel.setText(QCoreApplication.translate("SaveAs", u"Assets", None))
#if QT_CONFIG(tooltip)
        self.assetTree.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>The list of assets in the assets folder.  </p><p>This is usually just FBX, OBJ or Alembic files but can be other items as well.  </p><p>These files are not considered Published.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.loadRef_2_btn.setText(QCoreApplication.translate("SaveAs", u"Load Ref", None))
        self.import_2_btn.setText(QCoreApplication.translate("SaveAs", u"Import", None))
        self.saverTabs.setTabText(self.saverTabs.indexOf(self.ToolsTab), QCoreApplication.translate("SaveAs", u"Tools - Reference - Assets", None))
#if QT_CONFIG(tooltip)
        self.recent_project_label.setToolTip(QCoreApplication.translate("SaveAs", u"A list of recently opened projects.  Double click a project to make it the default project.", None))
#endif // QT_CONFIG(tooltip)
        self.recent_project_label.setText(QCoreApplication.translate("SaveAs", u"Recent Projects", None))
#if QT_CONFIG(tooltip)
        self.recent_projects.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>A list of recently opened projects.  </p><p>Double click a project to make it the default project.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.projects_label.setToolTip(QCoreApplication.translate("SaveAs", u"Quickly set a project.  This works the same as the default Maya Set Project feature", None))
#endif // QT_CONFIG(tooltip)
        self.projects_label.setText(QCoreApplication.translate("SaveAs", u"Project", None))
        self.set_project_label.setText(QCoreApplication.translate("SaveAs", u"Set Project", None))
        self.set_proejct_btn.setText(QCoreApplication.translate("SaveAs", u"Set Project", None))
#if QT_CONFIG(tooltip)
        self.new_project_label.setToolTip(QCoreApplication.translate("SaveAs", u"Create a new project.  This works the same as the Maya default, with the added feature that it adds basic task organization folders under the scene folder.", None))
#endif // QT_CONFIG(tooltip)
        self.new_project_label.setText(QCoreApplication.translate("SaveAs", u"New Project", None))
        self.new_project_name_label.setText(QCoreApplication.translate("SaveAs", u"New Project Name", None))
        self.new_project_folder_Label.setText(QCoreApplication.translate("SaveAs", u"New Project Folder", None))
        self.new_project_folder_btn.setText(QCoreApplication.translate("SaveAs", u"Browse...", None))
        self.scenes_label.setText(QCoreApplication.translate("SaveAs", u"Scenes", None))
#if QT_CONFIG(tooltip)
        self.include_subfolders.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>Typical Project Subfolders: Cams, Chars, Veh, Props, Env, Shots</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.include_subfolders.setText(QCoreApplication.translate("SaveAs", u"Include Subfolders", None))
        self.publish_label.setText(QCoreApplication.translate("SaveAs", u"Publish", None))
        self.assets_label.setText(QCoreApplication.translate("SaveAs", u"Assets", None))
        self.images_label.setText(QCoreApplication.translate("SaveAs", u"Images", None))
        self.source_images_label.setText(QCoreApplication.translate("SaveAs", u"Source Images", None))
        self.render_data_label.setText(QCoreApplication.translate("SaveAs", u"Render Data", None))
        self.clips_label.setText(QCoreApplication.translate("SaveAs", u"Clips", None))
        self.sound_label.setText(QCoreApplication.translate("SaveAs", u"Sound", None))
        self.scripts_label.setText(QCoreApplication.translate("SaveAs", u"Scripts", None))
        self.disk_cache_labe.setText(QCoreApplication.translate("SaveAs", u"Disk Cache", None))
        self.movies_label.setText(QCoreApplication.translate("SaveAs", u"Movies", None))
        self.time_editor_label.setText(QCoreApplication.translate("SaveAs", u"Time Editor", None))
        self.Autosave_labe.setText(QCoreApplication.translate("SaveAs", u"AutoSave", None))
        self.scene_ass_label.setText(QCoreApplication.translate("SaveAs", u"Scene Assembly", None))
        self.create_project_btn.setText(QCoreApplication.translate("SaveAs", u"Create Project", None))
        self.saverTabs.setTabText(self.saverTabs.indexOf(self.projectTab), QCoreApplication.translate("SaveAs", u"Project Settings", None))
#if QT_CONFIG(tooltip)
        self.showName_label.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>This is the name of the show.  </p><p>By default it is the same as the root folder name of the project, but can be changed to anything</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.showName_label.setText(QCoreApplication.translate("SaveAs", u"Show Name", None))
#if QT_CONFIG(tooltip)
        self.showName.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>This is the name of the show.  </p><p>By default it is the same as the root folder name of the project, but can be changed to anything</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.showCodeSet_label.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>The Show Code is a 3 letter code that is generated automatically and becomes the prefix for all files.  </p><p>It can be changed here to anything you like</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.showCodeSet_label.setText(QCoreApplication.translate("SaveAs", u"Show Code", None))
#if QT_CONFIG(tooltip)
        self.showCodeSet.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>The Show Code is a 3 letter code that is generated automatically and becomes the prefix for all files.  </p><p>It can be changed here to anything you like</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.defaultResolution_label.setToolTip(QCoreApplication.translate("SaveAs", u"The default rendering resolution for the project.  Setting it here also sets your render settings in the project", None))
#endif // QT_CONFIG(tooltip)
        self.defaultResolution_label.setText(QCoreApplication.translate("SaveAs", u"Default Resolution:  ", None))
#if QT_CONFIG(tooltip)
        self.resolutionWidth_label.setToolTip(QCoreApplication.translate("SaveAs", u"The default rendering resolution for the project.  Setting it here also sets your render settings in the project", None))
#endif // QT_CONFIG(tooltip)
        self.resolutionWidth_label.setText(QCoreApplication.translate("SaveAs", u"Width", None))
#if QT_CONFIG(tooltip)
        self.resolutionWidth.setToolTip(QCoreApplication.translate("SaveAs", u"The default rendering resolution for the project.  Setting it here also sets your render settings in the project", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.resolutionHeight_label.setToolTip(QCoreApplication.translate("SaveAs", u"The default rendering resolution for the project.  Setting it here also sets your render settings in the project", None))
#endif // QT_CONFIG(tooltip)
        self.resolutionHeight_label.setText(QCoreApplication.translate("SaveAs", u"Height", None))
#if QT_CONFIG(tooltip)
        self.resolutionHeight.setToolTip(QCoreApplication.translate("SaveAs", u"The default rendering resolution for the project.  Setting it here also sets your render settings in the project", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.filmbackLabel.setToolTip(QCoreApplication.translate("SaveAs", u"The default camera film back for new cameras.  Setting this here will automatically set your new cameras to this setting if the new camera button on the Tools tab is used", None))
#endif // QT_CONFIG(tooltip)
        self.filmbackLabel.setText(QCoreApplication.translate("SaveAs", u"Default Filmback:  ", None))
#if QT_CONFIG(tooltip)
        self.filmback_width_label.setToolTip(QCoreApplication.translate("SaveAs", u"The default camera film back for new cameras.  Setting this here will automatically set your new cameras to this setting if the new camera button on the Tools tab is used", None))
#endif // QT_CONFIG(tooltip)
        self.filmback_width_label.setText(QCoreApplication.translate("SaveAs", u"width (mm)", None))
#if QT_CONFIG(tooltip)
        self.filmback_width.setToolTip(QCoreApplication.translate("SaveAs", u"The default camera film back for new cameras.  Setting this here will automatically set your new cameras to this setting if the new camera button on the Tools tab is used", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.filmback_height_label.setToolTip(QCoreApplication.translate("SaveAs", u"The default camera film back for new cameras.  Setting this here will automatically set your new cameras to this setting if the new camera button on the Tools tab is used", None))
#endif // QT_CONFIG(tooltip)
        self.filmback_height_label.setText(QCoreApplication.translate("SaveAs", u"height (mm)", None))
#if QT_CONFIG(tooltip)
        self.filmback_height.setToolTip(QCoreApplication.translate("SaveAs", u"The default camera film back for new cameras.  Setting this here will automatically set your new cameras to this setting if the new camera button on the Tools tab is used", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.image_format_label.setToolTip(QCoreApplication.translate("SaveAs", u"This sets the default render output file type", None))
#endif // QT_CONFIG(tooltip)
        self.image_format_label.setText(QCoreApplication.translate("SaveAs", u"Default Render Format", None))
        self.image_format.setItemText(0, QCoreApplication.translate("SaveAs", u"jpeg", None))
        self.image_format.setItemText(1, QCoreApplication.translate("SaveAs", u"png", None))
        self.image_format.setItemText(2, QCoreApplication.translate("SaveAs", u"deepexr", None))
        self.image_format.setItemText(3, QCoreApplication.translate("SaveAs", u"tif", None))
        self.image_format.setItemText(4, QCoreApplication.translate("SaveAs", u"exr", None))
        self.image_format.setItemText(5, QCoreApplication.translate("SaveAs", u"maya", None))

#if QT_CONFIG(tooltip)
        self.image_format.setToolTip(QCoreApplication.translate("SaveAs", u"This sets the default render output file type", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.SceneScale_Label.setToolTip(QCoreApplication.translate("SaveAs", u"The Scene Scale sets the default size of the \"One Meter Cube\" that gets injected into new model files created by the New Asset feature", None))
#endif // QT_CONFIG(tooltip)
        self.SceneScale_Label.setText(QCoreApplication.translate("SaveAs", u"Scene Scale", None))
#if QT_CONFIG(tooltip)
        self.sceneScale.setToolTip(QCoreApplication.translate("SaveAs", u"The Scene Scale sets the default size of the \"One Meter Cube\" that gets injected into new model files created by the New Asset feature", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.recent_file_count_label.setToolTip(QCoreApplication.translate("SaveAs", u"This sets the number of Recent Files listed in the Recent File history", None))
#endif // QT_CONFIG(tooltip)
        self.recent_file_count_label.setText(QCoreApplication.translate("SaveAs", u"Recent File Count", None))
#if QT_CONFIG(tooltip)
        self.recent_file_count.setToolTip(QCoreApplication.translate("SaveAs", u"This sets the number of Recent Files listed in the Recent File history", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.autoload.setToolTip(QCoreApplication.translate("SaveAs", u"<html><head/><body><p>Auto Load on Startup makes Sans Pipe open when Maya opens and replaces the default Ctrl + Shift + S hotkey command with the Sans Pipe version up utility.  </p><p>Unchecking this resets the hotkey to its default setting</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.autoload.setText(QCoreApplication.translate("SaveAs", u"Auto Load on Startup", None))
#if QT_CONFIG(tooltip)
        self.autosaver.setToolTip(QCoreApplication.translate("SaveAs", u"Turns on Autosave for Maya and sets the time interval", None))
#endif // QT_CONFIG(tooltip)
        self.autosaver.setText(QCoreApplication.translate("SaveAs", u"Autosave", None))
#if QT_CONFIG(tooltip)
        self.iterations_label.setToolTip(QCoreApplication.translate("SaveAs", u"Turns on Autosave for Maya and sets the time interval", None))
#endif // QT_CONFIG(tooltip)
        self.iterations_label.setText(QCoreApplication.translate("SaveAs", u"Interval", None))
#if QT_CONFIG(tooltip)
        self.autosave_count.setToolTip(QCoreApplication.translate("SaveAs", u"Turns on Autosave for Maya and sets the time interval", None))
#endif // QT_CONFIG(tooltip)
        self.hotkeys_label.setText(QCoreApplication.translate("SaveAs", u"Hokeys", None))
        self.hotkeys.setText(QCoreApplication.translate("SaveAs", u"Open Sans Pipe = Ctrl + Shift + S (Only if Auto Load on Startup is enabled)\n"
"Save Version Up = Ctrl + Enter\n"
"Snapshot Version = Ctrl + t\n"
"Publish Version = Ctrl + p\n"
"Close = Esc", None))
        self.save_config_btn.setText(QCoreApplication.translate("SaveAs", u"Save Configuration", None))
        self.saverTabs.setTabText(self.saverTabs.indexOf(self.SettingsTab), QCoreApplication.translate("SaveAs", u"Settings - Configuration", None))
        self.messages.setText(QCoreApplication.translate("SaveAs", u"Errors", None))
    # retranslateUi

