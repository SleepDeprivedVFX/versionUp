# Maya Super Saver

"""
The SUPER SAVER is a pipeline-free versioning and saving system for Maya.
It is intended to be a stand-alone shelf button for quickly versioning up files and saving notes with them.
Simple click the button on the shelf or run the script.  A UI will pop up that attempts to name your script based on
the project folder, but can be customized to save the name as anything.
Notes can be reviewed on the right side by clicking on existing files.
"""

# FIXME: There are a few issues that I've discovered so far.
#  1. The version number is not properly changing when the task type is changed.  It still saves the version shown up
#  top.
#  2. The Overwrite function won't work due to the issue with the first fix me

from PySide2.QtCore import (QCoreApplication, QMetaObject, QSize, Qt, QSettings)
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from maya import cmds
import os
import sys
import re
import json
import time
from datetime import datetime
import platform

__version__ = '0.3.2'
__author__ = 'Adam Benson'

if platform.system() == 'Windows':
    env_user = 'USERNAME'
    computername = 'COMPUTERNAME'
else:
    env_user = 'USER'
    computername = 'HOSTNAME'


class super_saver(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.pattern = r'(_v\d+)|(_V\d+)'
        self.tasks = {
            "Model": [
                'Model',
                'MDL',
                'mdl',
                'model',
                'MODEL'
                ],
            "Surfacing": [
                'Surfacing',
                'SRF',
                'surface',
                'surfacing',
                'Surface',
                'SUR',
                'srf',
                'sur',
                'LookDev',
                'LKD',
                'lkd',
                'lookdev',
                'Lookdev',
                'LOOKDEV',
                'VisDev',
                'visdev',
                'vsd',
                'VSD'
                ],
            "Rig": [
                'Rig',
                'RIG',
                'rig',
                'rigging',
                'Rigging',
                'RIGGING'
                ],
            "Animation": [
                'Animation',
                'ANIM',
                'animation',
                'anim',
                'anm',
                'ANM',
                'Anim',
                ],
            "Lighting": [
                'Lighting',
                'LGT',
                'Light',
                'lgt',
                'light',
                'lighting',
                'LIGHT',
                'LIGHTING',
                'Lgt'
            ],
            "Sculpt": [
                'Sculpt',
                'SCPT',
                'sculpt',
                'scpt',
                'sclpt',
                'spt',
                'scl'
                'SCLPT',
                'SPT',
                'SCL'
                ],
            "Groom": [
                'Groom',
                'GRM',
                'groom',
                'grm',
                'hair',
                'Hair',
                'HAIR',
                'fur',
                'FUR',
                'Fur'
            ],
            "FX": [
                'Dynamics',
                'FX',
                'fx',
                'dyn',
                'DYN',
                'DYNAMICS',
                'dynamics',
                'Fluids',
                'Fluid',
                'FLD',
                'fld',
                'fluid',
                'fluids',
                'smoke',
                'Smoke',
                'SMOKE',
                'smk',
                'SMK',
                'Fire',
                'fire',
                'Particles',
                'particles',
                'ptl',
                'PTL',
                'SIM',
                'sim'
                ],
            "Cloth": [
                'Cloth',
                'CLTH',
                'cloth',
                'clth',
                'CTH',
                'cth'
                ],
            "Prototype": [
                'Prototype',
                'PROTO',
                'prototype',
                'Proto',
                'prt',
                'PRT'
            ]
        }
        self.invalidCharacters = [
            ' ',
            '+',
            '=',
            '@',
            '-',
            '&',
            '*',
            '!',
            '#',
            '$',
            '%',
            '^',
            '(',
            ')',
            '|',
            '\\',
            '/',
            '?',
            ':',
            ';',
            '<',
            '>',
            ',',
            '[',
            ']',
            '{',
            '}',
            '`',
            '~',
            '\'',
            '"'
        ]
        self.root_name = None
        self.task = None
        self.ui = Ui_SnapPublisher()
        self.ui.setupUi(self)

        self.settings = QSettings(__author__, 'Snap Publisher')
        self.position = self.settings.value('geometry', None)
        self.restoreGeometry(self.position)

        pth = cmds.file(q=True, sn=True)
        workspace = cmds.workspace(q=True, act=True)
        scene_folder = cmds.workspace(fre='scene')

        # Set initial artist field
        artist = os.environ[env_user]
        first_initials = artist[0:2]
        first_initials = first_initials.upper()
        last_name = artist[2:]
        artist = first_initials + last_name
        self.ui.artistName.setText(artist)

        if pth:
            # Check against current project
            save_path = os.path.dirname(pth)
            save_file = os.path.basename(pth)

            snapshot_folder = os.path.join(save_path, 'snapshots')
            publish_folder = os.path.join(save_path, 'publish')

            show_code = self.try_to_get_show_code(path=save_path)
            if show_code:
                self.ui.showCode.setText(show_code)
                show_code = '{show_code}_'.format(show_code=show_code)
            root_task_data = self.get_root_and_task(save_file)
            self.root_name = root_task_data['root_name']
            self.task = root_task_data['task_abbr']
            task = root_task_data['task_name']
            self.ui.taskType.setCurrentText(task)
            version_info = self.get_version_info(save_file)

            base_filename = '{bfn}_{artist}'.format(bfn=version_info['base_filename'], artist=artist)
            version = version_info['version']
            extension = version_info['extension']
            v_len = version_info['v_len']
            v_type = version_info['v_type']

            snapshot_file = self.format_name(basename=base_filename, _v=v_type, v=version, l=v_len, ext=extension,
                                             snap=True)
            print(snapshot_file)
        elif workspace:
            save_path = os.path.join(workspace, scene_folder)
            if '\\' in workspace:
                workspace = workspace.replace('\\', '/')
            if '\\' in save_path:
                save_path = save_path.replace('\\', '/')

            snapshot_folder = os.path.join(save_path, 'snapshots')
            publish_folder = os.path.join(save_path, 'publish')

            if workspace.endswith('/'):
                rem = -2
            else:
                rem = -1
            split_project_path = workspace.split('/')
            project_name = split_project_path[rem]
            version = 1

            show_code = self.try_to_get_show_code(path=save_path)
            if show_code:
                self.ui.showCode.setText(show_code)
                show_code = '%s_' % show_code

            self.root_name = project_name
            self.task = self.tasks[self.ui.taskType.currentText()][0]
            base_filename = '{show}{root_name}_{task}_{artist}'.format(show=show_code, root_name=project_name,
                                                                       task=self.task, artist=artist)

            v_type = '_v'
            v_len = 3
            extension = self.ui.fileType.currentText()
            save_file = self.format_name(basename=base_filename, _v=v_type, v=version, l=v_len, ext=extension)
            snapshot_file = self.format_name(basename=base_filename, _v=v_type, v=version, l=v_len, ext=extension,
                                             snap=True)
            publish_file = self.format_name(basename=base_filename, _v=v_type, v=version, l=v_len, ext=extension,
                                             pub=True)
            print(snapshot_file)
            print(publish_file)

        else:
            save_path = cmds.file(q=True, dir=True)

            snapshot_folder = os.path.join(save_path, 'snapshots')
            publish_folder = os.path.join(save_path, 'publish')

            version = 1
            base_filename = 'default'
            save_file = self.format_name(basename=base_filename)
            snapshot_file = self.format_name(basename=base_filename, snap=True)
            publish_file = self.format_name(basename=base_filename, pub=True)
            print(snapshot_file)
            print(publish_file)
            v_len = 3
            extension = 'ma'
            v_type = '_v'

        self.ui.filename.setText(self.root_name)
        self.ui.messages.setText('')
        # The following get_save_file() also needs to be double checked if the overwrite checckbox become active
        get_save = self.get_save_file(save_file=save_file, save_path=save_path, basename=base_filename, _v=v_type,
                                      l=v_len, ext=extension)
        save_file = get_save[0]
        next_version = get_save[1]

        self.ui.version.setValue(next_version)
        new_path = self.build_path(path=save_path, rootName=self.root_name, task=self.task, v_type=v_type,
                                   v_len=v_len, version=next_version, ext=extension, show=show_code, artist=artist)

        self.ui.output_filename.setText(new_path)
        # self.reset_version(v=next_version)

        self.ui.folder.setText(save_path)
        self.populate_existing_files(folder=save_path)

        self.set_custom()

        self.ui.customNaming.clicked.connect(self.set_custom)
        self.ui.autoNaming.clicked.connect(self.set_custom)
        self.ui.cancel_btn.clicked.connect(self.close)

        self.ui.folder.textChanged.connect(self.update_ui)
        self.ui.taskType.currentTextChanged.connect(lambda: self.reset_version(v=1))
        self.ui.version.valueChanged.connect(self.update_ui)
        self.ui.fileType.currentTextChanged.connect(self.update_ui)
        self.ui.filename.textChanged.connect(self.remove_bad_characters)
        self.ui.filename.textChanged.connect(self.update_ui)
        self.ui.showCode.textChanged.connect(self.update_ui)
        self.ui.artistName.textChanged.connect(self.update_ui)
        self.ui.existingFile_list.clicked.connect(self.show_existing_note)
        self.ui.open_btn.clicked.connect(self.open_file)
        self.ui.open_btn.setEnabled(False)
        self.ui.open_btn.setStyleSheet(
            'color: rgb(140, 140, 140);'
        )

        self.ui.save_btn.clicked.connect(self.run)
        self.ui.folder_btn.clicked.connect(self.get_folder)

        self.show()

    def open_file(self, f=False):
        get_filename = self.ui.existingFile_list.currentItem()
        folder = self.ui.folder.text()
        filename = get_filename.text()
        open_file = os.path.join(folder, filename)
        try:
            cmds.file(open_file, o=True, f=f)
            self.close()
        except RuntimeError as e:
            msg = str(e)
            self.message(text=msg, ok=False)
            self.hide()
            pop_up = QMessageBox()
            pop_up.setProperty('Save Error', True)
            pop_up.setWindowTitle(msg)
            pop_up.setText('Unsaved Changes detected!  Save before opening a new file?')
            pop_up.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
            pop_up.setDefaultButton(QMessageBox.Yes)
            ret = pop_up.exec_()
            if ret == pop_up.Yes:
                cmds.file(s=True)
                self.open_file(f=False)
            elif ret == pop_up.No:
                self.open_file(f=True)
            else:
                self.show()

    def format_name(self, basename=None, _v='_v', v=1, l=3, ext='ma', snap=False, pub=False):
        if basename:
            if not snap or pub:
                save_file = '{basename}{_v}{v:0{l}d}.{ext}'.format(basename=basename, _v=_v, v=v, l=l, ext=ext)
                return save_file
            elif snap:
                dt = datetime.now()
                adjusted_dt = dt.strftime("%m%d%y%H%M%S")
                save_file = '{basename}{_v}{v:0{l}d}_{stamp}.{ext}'.format(basename=basename, _v=_v, v=v, l=l,
                                                                           stamp=adjusted_dt, ext=ext)
                return save_file
            elif pub:
                save_file = '{basename}{_v}{v:0{l}d}.{ext}'.format(basename=basename, _v=_v, v=v, l=l, ext=ext)
                return save_file
        return False

    def reset_version(self, v=1):
        self.ui.version.valueChanged.disconnect(self.update_ui)
        self.ui.version.setValue(v)
        self.update_ui()
        self.ui.version.valueChanged.connect(self.update_ui)

    def remove_bad_characters(self):
        root_name = self.ui.filename.text()
        bad_x = [x for x in self.invalidCharacters if x in root_name]
        if bad_x:
            bad_x = bad_x[0]
            root_name = root_name.replace(bad_x, '_')
            self.ui.filename.setText(root_name)

    def try_to_get_show_code(self, path=None):
        show_code = None
        if path:
            checked_path = path.replace('\\', '/')
            split_path = checked_path.split('/')
            for seg in split_path:
                if len(seg) == 3:
                    show_code = seg
                    break
        return show_code

    # def check_version(self):
    #     # This would partially replace the update_ui() routine.  The idea here being that it would collect the UI
    #     # information and get the latest version info and then use that to update the UI.
    #     path = self.ui.folder.text()
    #     root_name = self.ui.filename.text()
    #     version = self.ui.version.value()
    #     taskType = self.ui.taskType.currentText()
    #     task = self.tasks[taskType][0]
    #     ext = self.ui.fileType.currentText()
    #     overwrite = self.ui.overwrite.isChecked()
    #     get_output_path = self.build_path(path=path, rootName=root_name, task=task, v_type='_v', v_len=3,
    #                                       version=version, ext=ext)
    #     save_file = os.path.basename(get_output_path)
    #     file_info = self.get_save_file(save_file=save_file, save_path=path, basename=)

    def update_ui(self):
        path = self.ui.folder.text()
        root_name = self.ui.filename.text()
        version = self.ui.version.value()
        taskType = self.ui.taskType.currentText()
        task = self.tasks[taskType][0]
        ext = self.ui.fileType.currentText()
        show_code = self.ui.showCode.text()
        artist = self.ui.artistName.text()

        if show_code:
            if not show_code.endswith('_'):
                show_code = '{show_code}_'.format(show_code=show_code)

        new_output_file = self.build_path(path=path, rootName=root_name, task=task, v_type='_v', v_len=3,
                                          version=version, ext=ext, show=show_code, artist=artist)
        if new_output_file:
            self.ui.output_filename.setText(new_output_file)
            # self.reset_version(v=version)

    def get_root_and_task(self, filename=None):
        root_name = None
        task_name = None
        task_abbr = None
        data = None
        show_code = self.ui.showCode.text()
        artist = self.ui.artistName.text()
        if filename:
            # Check against current project
            save_file = filename
            for task in self.tasks.keys():
                for abbr in self.tasks[task]:
                    if abbr in save_file:
                        root_name = save_file.split(abbr)[0]
                        task_abbr = abbr
                        task_name = task
                        if root_name.endswith('_'):
                            root_name = root_name.rstrip('_')
                        if root_name.startswith(show_code):
                            root_name = root_name.replace(show_code, '')
                        if root_name.startswith('_'):
                            root_name = root_name.lstrip('_')
                        artist_ = '{artist}_'.format(artist=artist)
                        if artist_ in root_name:
                            root_name = root_name.replace(artist_, '')
                        break
        if root_name and task_name and task_abbr:
            # EXAMPLE:
            # root_name = Asset1
            # task_name = Model
            # task_abbr = MDL
            data = {
                'root_name': root_name,
                'task_name': task_name,
                'task_abbr': task_abbr
            }
        else:
            file_data = self.get_version_info(filename=filename)
            data = {
                'root_name': file_data['base_filename'],
                'task_name': None,
                'task_abbr': None
            }
        return data
    
    def set_custom(self):
        auto = self.ui.autoNaming.isChecked()
        if auto:
            self.ui.filename.setEnabled(False)
            self.ui.version.setEnabled(False)
            self.ui.fileType.setEnabled(False)
            self.ui.folder.setEnabled(False)
            self.ui.folder_btn.setEnabled(False)
            self.ui.showCode.setEnabled(False)
            self.ui.artistName.setEnabled(False)
        else:
            self.ui.filename.setEnabled(True)
            self.ui.version.setEnabled(True)
            self.ui.fileType.setEnabled(True)
            self.ui.folder.setEnabled(True)
            self.ui.folder_btn.setEnabled(True)
            self.ui.showCode.setEnabled(True)
            self.ui.artistName.setEnabled(True)

    def build_path(self, path=None, rootName=None, task=None, v_type='_v', v_len=3, version=0, ext=None, show=None,
                   artist=None):
        output_path = None
        if path and rootName and ext:
            if rootName.startswith(show):
                show = ''
            if task:
                filename = '{show}{base}_{task}_{artist}{_v}{v:0{l}d}.{ext}'.format(base=rootName, task=task, _v=v_type,
                                                                                    l=v_len, v=version, ext=ext,
                                                                                    show=show, artist=artist)
                basename = '{show}{base}_{task}_{artist}'.format(base=rootName, task=task, show=show, artist=artist)
            else:
                filename = '{show}{base}_{artist}{_v}{v:0{l}d}.{ext}'.format(base=rootName, _v=v_type, l=v_len,
                                                                             v=version, ext=ext, show=show,
                                                                             artist=artist)
                basename = '{show}{base}_{artist}'.format(base=rootName, show=show, artist=artist)
            check_filename = self.get_save_file(save_file=filename, save_path=path, basename=basename)
            filename = check_filename[0]
            # Do I add the version update here?  Nope

            next_version = int(check_filename[1])
            print('shit', next_version)

            # self.reset_version(v=next_version)
            output_path = os.path.join(path, filename)
            if '\\' in output_path:
                output_path = output_path.replace('\\', '/')
        return output_path

    def get_folder(self):
        pth = self.ui.folder.text()
        self.hide()
        if pth:
            getFolder = cmds.fileDialog2(dir=pth, fm=3)
        else:
            getFolder = cmds.fileDialog2(fm=3)
        self.show()
        if getFolder:
            self.ui.folder.setText(getFolder[0])

    def get_save_file(self, save_file=None, save_path=None, basename=None, _v='_v', v=1, l=3, ext='ma'):
        # This finds the next available version.  It needs to have the overwrite check in it
        next_version = v
        overwrite = self.ui.overwrite.isChecked()
        if not overwrite:
            if save_file and save_path and basename:
                all_files = sorted(self.collect_files(path=save_path))
                while save_file in all_files:
                    next_version += 1
                    save_file = self.format_name(basename=basename, _v=_v, v=next_version, l=l, ext=ext)
        else:
            save_file = self.format_name(basename=basename, _v=_v, v=next_version, l=l, ext=ext)

        return save_file, next_version

    def get_version_info(self, filename=None, default_len=3, default_version=0):
        # This function gets the version in an existing filename, or creates a default version
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
                # splits outputs: ('', '001')
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

    def collect_files(self, path=None):
        files = []
        if path:
            if os.path.exists(path):
                list_files = os.listdir(path)
                for f in list_files:
                    if os.path.isfile(os.path.join(path, f)):
                        files.append(f)
        return files

    def make_db_folder(self, folder=None):
        db_folder = None
        if folder:
            db_folder = os.path.join(folder, 'db')
            if not os.path.exists(db_folder):
                os.makedirs(db_folder)
        return db_folder

    def create_db(self, folder=None):
        if folder:
            if not os.path.exists(folder):
                data = {
                    "Notes": []
                }
                save_data = json.dumps(data, indent=4)
                with open(folder, 'w+') as save:
                    save.write(save_data)
                    save.close()

    def open_db(self, folder=None):
        notes_db = None
        if folder:
            notes_db_file = os.path.join(folder, 'notes_db.json')
            if not os.path.exists(notes_db_file):
                # create an empty file
                self.create_db(folder=notes_db_file)
            with open(notes_db_file, 'r+') as open_notes:
                notes_db = json.load(open_notes)
                open_notes.close()
        return notes_db

    def save_db(self, folder=None, data=None):
        if data and folder:
            notes_file = os.path.join(folder, 'notes_db.json')
            save_data = json.dumps(data, indent=4)
            with open(notes_file, 'r+') as save:
                save.write(save_data)
                save.close()

    def show_existing_note(self):
        if not self.ui.open_btn.isEnabled():
            self.ui.open_btn.setEnabled(True)
            self.ui.open_btn.setStyleSheet(
                'color: rgb(220, 220, 220);'
            )
        get_filename = self.ui.existingFile_list.currentItem()
        folder = self.make_db_folder(self.ui.folder.text())
        filename = get_filename.text()
        notes_db = self.open_db(folder=folder)
        post_note = """FILE: {fn}
USER: None
COMP: None
DATE: None

NOTE: None
""".format(fn=filename)
        for note in notes_db['Notes']:
            if type(note) == dict and 'filename' in note.keys():
                if filename in note['filename']:
                    user = note['user']
                    date = note['date']
                    computer = note['computer']
                    details = note['details']
                    post_note = """FILE: {filename}
USER: {user}
COMP: {computer}
DATE: {date}

NOTE: {details}""".format(filename=filename, user=user, computer=computer, date=date, details=details)
                    break

        self.ui.existing_notes.setText(post_note)

    def populate_existing_files(self, folder=None):
        filetypes = ['ma', 'mb']
        if folder:
            if os.path.exists(folder):
                existing_files = os.listdir(folder)
                for filename in existing_files:
                    if os.path.isfile(os.path.join(folder, filename)):
                        file_separator = filename.split(os.path.extsep)
                        ext = file_separator[1]
                        if ext in filetypes:
                            new_entry = QListWidgetItem(filename)
                            self.ui.existingFile_list.addItem(new_entry)

    def message(self, text=None, ok=True):
        self.ui.messages.setText(text)
        if ok:
            self.ui.messages.setStyleSheet(
                "color: rgb(150, 255, 150);\nfont: 9pt \"MS Shell Dlg 2;\""
            )
        else:
            self.ui.messages.setStyleSheet(
                "color: rgb(255, 150, 150);\nfont: 12pt \"MS Shell Dlg 2;\""
            )

    def run(self):
        output_file = self.ui.output_filename.text()
        overwrite = self.ui.overwrite.isChecked()
        fileType = self.ui.fileType.currentText()
        notes = self.ui.notes.toPlainText()
        if not notes:
            self.message(text='YOU MUST ADD A NOTE!!!', ok=False)
            return False
        elif len(notes) < 10:
            self.message(text='Your note must be more elaborate.', ok=False)
            return False

        if fileType == 'ma':
            fileType = 'mayaAscii'
        else:
            fileType = 'mayaBinary'

        path = os.path.dirname(output_file)
        notes_path = self.make_db_folder(folder=path)
        notes_db = self.open_db(folder=notes_path)
        if not os.path.exists:
            os.makedirs(path)
        if overwrite:
            self.message(text='Saving...', ok=True)
            cmds.file(rename=output_file)
            cmds.file(s=True, type=fileType, options='v=0;')
        else:
            if os.path.exists(output_file):
                self.message(text='FILE ALREADY EXISTS!  Choose "Overwrite" to save anyway', ok=False)
                return False
            else:
                # Make a JSON entry
                self.message(text='Saving...', ok=True)
                cmds.file(rename=output_file)
                cmds.file(s=True, type=fileType, options='v=0;')

        self.message(text='Writing Notes...', ok=True)
        date_now = datetime.now()
        date = '{d} | {t}'.format(d=date_now.date(), t=date_now.time())
        new_note = {
            'filename': os.path.basename(output_file),
            'user': os.environ[env_user],
            'computer': os.environ[computername],
            'date': date,
            'details': notes
        }
        notes_db['Notes'].append(new_note)
        self.save_db(folder=notes_path, data=notes_db)
        self.message(text='Saved Successfully!!', ok=True)
        print('FILE SAVED: %s' % output_file)
        time.sleep(1)
        self.close()

    def closeEvent(self, event):
        self.settings.setValue('geometry', self.saveGeometry())


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

        self.naming_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

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
        self.taskType.setObjectName(u"taskType")

        self.taskType_layout.addWidget(self.taskType)

        self.taksType_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

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

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.showArtist_layout.addItem(self.horizontalSpacer)

        self.artistName_label = QLabel(SnapPublisher)
        self.artistName_label.setObjectName(u"artistName_label")

        self.showArtist_layout.addWidget(self.artistName_label)

        self.artistName = QLineEdit(SnapPublisher)
        self.artistName.setObjectName(u"artistName")

        self.showArtist_layout.addWidget(self.artistName)


        self.saveAs_Layout.addLayout(self.showArtist_layout)

        self.notes_seperator = QFrame(SnapPublisher)
        self.notes_seperator.setObjectName(u"notes_seperator")
        self.notes_seperator.setFrameShape(QFrame.HLine)
        self.notes_seperator.setFrameShadow(QFrame.Sunken)

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
        self.existingFile_layout = QVBoxLayout()
        self.existingFile_layout.setObjectName(u"existingFile_layout")
        self.existingFile_label = QLabel(SnapPublisher)
        self.existingFile_label.setObjectName(u"existingFile_label")

        self.existingFile_layout.addWidget(self.existingFile_label)

        self.existingFile_list = QListWidget(SnapPublisher)
        self.existingFile_list.setObjectName(u"existingFile_list")

        self.existingFile_layout.addWidget(self.existingFile_list)

        self.open_btn_layout = QHBoxLayout()
        self.open_btn_layout.setObjectName(u"open_btn_layout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.open_btn_layout.addItem(self.horizontalSpacer_2)

        self.load_snap_btn = QPushButton(SnapPublisher)
        self.load_snap_btn.setObjectName(u"load_snap_btn")

        self.open_btn_layout.addWidget(self.load_snap_btn)


        self.existingFile_layout.addLayout(self.open_btn_layout)


        self.horizontalLayout_2.addLayout(self.existingFile_layout)

        self.horizontalSpacer_4 = QSpacerItem(15, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_4)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(SnapPublisher)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.listWidget = QListWidget(SnapPublisher)
        self.listWidget.setObjectName(u"listWidget")

        self.verticalLayout.addWidget(self.listWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

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
        self.buttons_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

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
        self.label.raise_()
        self.listWidget.raise_()
        self.load_pub_btn.raise_()
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
        self.taskType.setItemText(0, QCoreApplication.translate("SnapPublisher", u"Model", None))
        self.taskType.setItemText(1, QCoreApplication.translate("SnapPublisher", u"Surfacing", None))
        self.taskType.setItemText(2, QCoreApplication.translate("SnapPublisher", u"Rig", None))
        self.taskType.setItemText(3, QCoreApplication.translate("SnapPublisher", u"Animation", None))
        self.taskType.setItemText(4, QCoreApplication.translate("SnapPublisher", u"Sculpt", None))
        self.taskType.setItemText(5, QCoreApplication.translate("SnapPublisher", u"Groom", None))
        self.taskType.setItemText(6, QCoreApplication.translate("SnapPublisher", u"FX", None))
        self.taskType.setItemText(7, QCoreApplication.translate("SnapPublisher", u"Cloth", None))
        self.taskType.setItemText(8, QCoreApplication.translate("SnapPublisher", u"Prototype", None))

        self.fileType_label.setText(QCoreApplication.translate("SnapPublisher", u"File Type", None))
        self.fileType.setItemText(0, QCoreApplication.translate("SnapPublisher", u"ma", None))
        self.fileType.setItemText(1, QCoreApplication.translate("SnapPublisher", u"mb", None))

        self.filename_label.setText(QCoreApplication.translate("SnapPublisher", u"Filename", None))
        self.overwrite.setText(QCoreApplication.translate("SnapPublisher", u"Overwrite", None))
        self.showCode_label.setText(QCoreApplication.translate("SnapPublisher", u"Show Code", None))
        self.showCode.setPlaceholderText(QCoreApplication.translate("SnapPublisher", u"GCY", None))
        self.artistName_label.setText(QCoreApplication.translate("SnapPublisher", u"Artist Name", None))
        self.notes_label.setText(QCoreApplication.translate("SnapPublisher", u"Notes", None))
        self.existingFile_label.setText(QCoreApplication.translate("SnapPublisher", u"Snapshots", None))
        self.load_snap_btn.setText(QCoreApplication.translate("SnapPublisher", u"Load Snapshot", None))
        self.label.setText(QCoreApplication.translate("SnapPublisher", u"Publishes", None))
        self.load_pub_btn.setText(QCoreApplication.translate("SnapPublisher", u"Load Publish", None))
        self.snapshot_btn.setText(QCoreApplication.translate("SnapPublisher", u"Snapshot", None))
        self.publish_btn.setText(QCoreApplication.translate("SnapPublisher", u"Publish", None))
        self.cancel_btn.setText(QCoreApplication.translate("SnapPublisher", u"Cancel", None))
    # retranslateUi


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
    except Exception as e:
        app = QApplication.instance()
    saveas = super_saver()
    try:
        sys.exit(app.exec_())
    except SystemExit as e:
        print(e)
