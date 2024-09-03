# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'superSaver_UIdhafPF.ui'
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
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QRadioButton, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QTableWidget, QTableWidgetItem, QTextEdit,
    QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget)

class Ui_SaveAs(object):
    def setupUi(self, SaveAs):
        if not SaveAs.objectName():
            SaveAs.setObjectName(u"SaveAs")
        SaveAs.resize(969, 722)
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

        self.messages = QLabel(self.MainTab)
        self.messages.setObjectName(u"messages")
        self.messages.setStyleSheet(u"font: 75 9pt \"MS Shell Dlg 2\";\n"
"color: rgb(255, 150, 150);")

        self.verticalLayout_2.addWidget(self.messages)

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

        self.notes_layout.addWidget(self.recentFilesList)


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
        self.existing_notes.setEnabled(False)
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
        self.horizontalLayout_3 = QHBoxLayout(self.ToolsTab)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
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

        self.verticalLayout_4.addWidget(self.bakeCamSceneName)

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

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer)


        self.horizontalLayout_3.addWidget(self.toolsGroup)

        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.referenceListLabel = QLabel(self.ToolsTab)
        self.referenceListLabel.setObjectName(u"referenceListLabel")
        self.referenceListLabel.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.verticalLayout_5.addWidget(self.referenceListLabel)

        self.referenceList = QTableWidget(self.ToolsTab)
        self.referenceList.setObjectName(u"referenceList")

        self.verticalLayout_5.addWidget(self.referenceList)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_3)

        self.updateAllRefs_btn = QPushButton(self.ToolsTab)
        self.updateAllRefs_btn.setObjectName(u"updateAllRefs_btn")

        self.horizontalLayout.addWidget(self.updateAllRefs_btn)

        self.updateRefs_btn = QPushButton(self.ToolsTab)
        self.updateRefs_btn.setObjectName(u"updateRefs_btn")

        self.horizontalLayout.addWidget(self.updateRefs_btn)


        self.verticalLayout_5.addLayout(self.horizontalLayout)


        self.horizontalLayout_3.addLayout(self.verticalLayout_5)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.assetTreeLabel = QLabel(self.ToolsTab)
        self.assetTreeLabel.setObjectName(u"assetTreeLabel")
        self.assetTreeLabel.setStyleSheet(u"font: 700 12pt \"Segoe UI\";")

        self.verticalLayout_6.addWidget(self.assetTreeLabel)

        self.assetTree = QTreeWidget(self.ToolsTab)
        __qtreewidgetitem2 = QTreeWidgetItem()
        __qtreewidgetitem2.setText(0, u"1");
        self.assetTree.setHeaderItem(__qtreewidgetitem2)
        self.assetTree.setObjectName(u"assetTree")

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


        self.horizontalLayout_3.addLayout(self.verticalLayout_6)

        self.saverTabs.addTab(self.ToolsTab, "")
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

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_9)

        self.save_config_btn = QPushButton(self.SettingsTab)
        self.save_config_btn.setObjectName(u"save_config_btn")

        self.horizontalLayout_9.addWidget(self.save_config_btn)


        self.verticalLayout_7.addLayout(self.horizontalLayout_9)

        self.verticalSpacer_2 = QSpacerItem(20, 477, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_2)

        self.saverTabs.addTab(self.SettingsTab, "")

        self.verticalLayout_3.addWidget(self.saverTabs)

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

        self.retranslateUi(SaveAs)

        self.saverTabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(SaveAs)
    # setupUi

    def retranslateUi(self, SaveAs):
        SaveAs.setWindowTitle(QCoreApplication.translate("SaveAs", u"Super Saver", None))
        self.Title.setText(QCoreApplication.translate("SaveAs", u"Save As...", None))
        self.output_filename.setText(QCoreApplication.translate("SaveAs", u"output filename", None))
        self.messages.setText(QCoreApplication.translate("SaveAs", u"Errors", None))
        self.naming_label.setText(QCoreApplication.translate("SaveAs", u"Naming", None))
        self.autoNaming.setText(QCoreApplication.translate("SaveAs", u"Auto", None))
        self.customNaming.setText(QCoreApplication.translate("SaveAs", u"Custom", None))
        self.version_label.setText(QCoreApplication.translate("SaveAs", u"Version", None))
        self.allowFileCopy.setText(QCoreApplication.translate("SaveAs", u"Allow File Copy From --> To", None))
        self.folder_label.setText(QCoreApplication.translate("SaveAs", u"Save to Folder", None))
        self.folder_btn.setText(QCoreApplication.translate("SaveAs", u"Browse...", None))
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

        self.fileType_label.setText(QCoreApplication.translate("SaveAs", u"File Type", None))
        self.fileType.setItemText(0, QCoreApplication.translate("SaveAs", u"ma", None))
        self.fileType.setItemText(1, QCoreApplication.translate("SaveAs", u"mb", None))

        self.filename_label.setText(QCoreApplication.translate("SaveAs", u"Filename", None))
        self.overwrite.setText(QCoreApplication.translate("SaveAs", u"Overwrite", None))
        self.showCode_label.setText(QCoreApplication.translate("SaveAs", u"Show Code", None))
        self.showCode.setPlaceholderText(QCoreApplication.translate("SaveAs", u"ABC", None))
        self.AppendArtist.setText(QCoreApplication.translate("SaveAs", u"Append Artist", None))
        self.artistName_label.setText(QCoreApplication.translate("SaveAs", u"Artist Name", None))
        self.notes_label.setText(QCoreApplication.translate("SaveAs", u"Notes", None))
        self.recentFilesLabel.setText(QCoreApplication.translate("SaveAs", u"Recent Files", None))
        self.existingFile_label.setText(QCoreApplication.translate("SaveAs", u"Existing Files", None))
        self.import_btn.setText(QCoreApplication.translate("SaveAs", u"Import", None))
        self.load_btn.setText(QCoreApplication.translate("SaveAs", u"Load Ref", None))
        self.open_btn.setText(QCoreApplication.translate("SaveAs", u"Open", None))
        self.snapshots_label.setText(QCoreApplication.translate("SaveAs", u"Snapshots", None))
        self.version_notes_label.setText(QCoreApplication.translate("SaveAs", u"Version Note", None))
        self.publish_btn.setText(QCoreApplication.translate("SaveAs", u"Publish", None))
        self.snap_btn.setText(QCoreApplication.translate("SaveAs", u"Snapshot", None))
        self.save_btn.setText(QCoreApplication.translate("SaveAs", u"Save V Up", None))
        self.cancel_btn.setText(QCoreApplication.translate("SaveAs", u"Cancel", None))
        self.saverTabs.setTabText(self.saverTabs.indexOf(self.MainTab), QCoreApplication.translate("SaveAs", u"Save - Publish - Snap", None))
        self.toolsGroup.setTitle(QCoreApplication.translate("SaveAs", u"Tools", None))
        self.bakeCam_btn.setText(QCoreApplication.translate("SaveAs", u"Bake Camera", None))
        self.bakeCamSceneName.setText(QCoreApplication.translate("SaveAs", u"Use Shot/Asset as Cam Name", None))
        self.fbxPub_btn.setText(QCoreApplication.translate("SaveAs", u"Publish Selection as FBX", None))
        self.objPub_btn.setText(QCoreApplication.translate("SaveAs", u"Publish Selection as OBJ", None))
        self.abcPub_btn.setText(QCoreApplication.translate("SaveAs", u"Publish Selection as Alembic", None))
        self.playblast_btn.setText(QCoreApplication.translate("SaveAs", u"Playblaster", None))
        self.referenceListLabel.setText(QCoreApplication.translate("SaveAs", u"Loaded References", None))
        self.updateAllRefs_btn.setText(QCoreApplication.translate("SaveAs", u"Update All", None))
        self.updateRefs_btn.setText(QCoreApplication.translate("SaveAs", u"Update Selected", None))
        self.assetTreeLabel.setText(QCoreApplication.translate("SaveAs", u"Assets", None))
        self.loadRef_2_btn.setText(QCoreApplication.translate("SaveAs", u"Load Ref", None))
        self.import_2_btn.setText(QCoreApplication.translate("SaveAs", u"Import", None))
        self.saverTabs.setTabText(self.saverTabs.indexOf(self.ToolsTab), QCoreApplication.translate("SaveAs", u"Tools - Reference - Publish Tracking", None))
        self.showName_label.setText(QCoreApplication.translate("SaveAs", u"Show Name", None))
        self.showCodeSet_label.setText(QCoreApplication.translate("SaveAs", u"Show Code", None))
        self.defaultResolution_label.setText(QCoreApplication.translate("SaveAs", u"Default Resolution:  ", None))
        self.resolutionWidth_label.setText(QCoreApplication.translate("SaveAs", u"Width", None))
        self.resolutionHeight_label.setText(QCoreApplication.translate("SaveAs", u"Height", None))
        self.filmbackLabel.setText(QCoreApplication.translate("SaveAs", u"Default Filmback:  ", None))
        self.filmback_width_label.setText(QCoreApplication.translate("SaveAs", u"width (mm)", None))
        self.filmback_height_label.setText(QCoreApplication.translate("SaveAs", u"height (mm)", None))
        self.SceneScale_Label.setText(QCoreApplication.translate("SaveAs", u"Scene Scale", None))
        self.save_config_btn.setText(QCoreApplication.translate("SaveAs", u"Save Configuration", None))
        self.saverTabs.setTabText(self.saverTabs.indexOf(self.SettingsTab), QCoreApplication.translate("SaveAs", u"Settings - Configuration", None))
    # retranslateUi

