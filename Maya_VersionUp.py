# Maya Version Up

"""
Beta - pipeline free version up tool.
Simply run this script, or save it as a shelf button to quickly version up a file.
The script is looking for '_v###' or '_V####' and will compare with other files in the same folder to version up to the
next available number.
If there is no '_v##' on the current filename, then one will be created as '_v001'
Currently, this script does not work with unsaved files.  You must start with a properly saved file.

TODO:
    - Allow for initial file saving - creating the version 1
    - Require version notes
    - Make a UI for reading previous notes, saving as specific versions, or even overwriting a file.
"""
from maya import cmds
import os
import sys
import re
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
# from ui import ui_saveas_dialog as svas


__version__ = '0.2.0'
__author__ = 'Adam Benson'


# class save_popup(QWidget):
#     def __init__(self, parent=None):
#         QWidget.__init__(self, parent)
#         self.setWindowFlags(Qt.WindowStaysOnTopHint)
#         self.ui = Ui_SaveAsForm()
#         self.ui.setupUi(self)
#         self.ui.setupUi(self)
#         answer = self.show()
#         print(answer)


class versionUp(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        pth = cmds.file(q=True, sn=True)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.ui = Ui_SaveAsForm()
        self.ui.setupUi(self)
        if pth:
            dir = os.path.dirname(pth)
            fn = os.path.basename(pth)
            self.pattern = r'(_v\d+)|(_V\d+)'
            self.hide()
            self.main(path=pth, dir=dir, filename=fn)
        else:
            project_path = cmds.workspace(q=True, rd=True)
            if '\\' in project_path:
                project_path = project_path.replace('\\', '/')
            print(project_path)
            if project_path.endswith('/'):
                rem = -2
            else:
                rem = -1
            split_proj_path = project_path.split('/')
            project_name = split_proj_path[rem]
            print(project_name)
            self.ui.folder.setText(project_path)
            answer = self.show()
        
    def collect_files(self, path=None):
        files = []
        if path:
            if os.path.exists(path):
                list_files = os.listdir(path)
                for f in list_files:
                    if os.path.isfile(os.path.join(path, f)):
                        files.append(f)
        return files
        
    def get_version_info(self, filename=None, default_len=3, default_version=0):
        file_info = None
        if filename:
            # Get current filename details.
            filename_parts = filename.split(os.path.extsep)
            root_filename = filename_parts[0]
            extension = filename_parts[1]
            find_version = re.findall(self.pattern, root_filename)
            if find_version:
                ver = find_version[0][0]
                splits = ver.lower().split('_v')
                if '_v' in root_filename:
                    base_filename = root_filename.split('_v')[0]
                    v_type = '_v'
                elif '_V' in root_filename:
                    base_filename = root_filename.split('_V')[0]
                    v_type = '_V'
                else:
                    base_filename = root_filename
                    v_type = '_v'
                split_v = splits[1]
                version = int(split_v)
                v_len = len(split_v)
            else:
                base_filename = root_filename
                version = default_version
                v_len = default_len
                v_type = '_v'
            
            # Add to the details package
            file_info = {
                'base_filename': base_filename,
                'version': version,
                'v_len': v_len,
                'extension': extension,
                'v_type': v_type
            }
        return file_info
        
    def save_up(self, new_filename=None, path=None):
        if new_filename and path:
            saveas = os.path.join(path, new_filename)
            print('SAVEAS: %s' % saveas)
            if not os.path.exists(saveas):
                cmds.file(rename=saveas)
                cmds.file(s=True)
                return 'New File Saved {}'.format(saveas)
        return False
        
    def main(self, path=None, dir=None, filename=None):
        if filename and path:
            # # Get current filename details.
            filename_parts = filename.split(os.path.extsep)
            root_filename = filename_parts[0]
            file_info = self.get_version_info(filename=filename)
            if file_info:
                version = file_info['version']
                extension = file_info['extension']
                v_len = file_info['v_len']
                v_type = file_info['v_type']
                base_filename = file_info['base_filename']
            else:
                return False
            
            # Get most recent version in folder
            all_files = sorted(self.collect_files(dir), reverse=True)
            new_filename = filename
            next_version = version
            while new_filename in all_files:
                next_version += 1
                new_filename = '{basename}{_v}{v:0{l}d}.{ext}'.format(basename=base_filename, _v=v_type, v=next_version, l=v_len, ext=extension)
            
            # Save new file names
            new_file = self.save_up(new_filename=new_filename, path=dir)
            print(new_file)


class Ui_SaveAsForm(object):
    def setupUi(self, SaveAsForm):
        if not SaveAsForm.objectName():
            SaveAsForm.setObjectName(u"SaveAsForm")
        SaveAsForm.resize(450, 245)
        SaveAsForm.setMinimumSize(QSize(450, 285))
        SaveAsForm.setMaximumSize(QSize(988, 285))
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


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        saveas = versionUp()
        # saveas.show()
        sys.exit(app.exec_())
    except Exception as e:
        app = QApplication.instance()
        saveas = versionUp()
        # saveas.show()


