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

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt, QSettings)
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from maya import cmds
import os
import sys
import re
import json
import time
from datetime import datetime
import platform
import subprocess

# FIXME: Add garbage for the UI to work in Maya.
script_path = "C:/Users/sleep/OneDrive/Documents/Scripts/Python/Maya/Utilities/versionUp"
ui_path = os.path.join(script_path, 'ui')
ui_path = ui_path.replace('\\', '/')
if script_path not in sys.path:
    sys.path.append(script_path)
if ui_path not in sys.path:
    sys.path.append(ui_path)

from ui import ui_superSaver_UI as ssui

__version__ = '0.4.1'
__author__ = 'Adam Benson'

if platform.system() == 'Windows':
    env_user = 'USERNAME'
    computername = 'COMPUTERNAME'
else:
    env_user = 'USER'
    computername = 'HOSTNAME'


def natural_sort_key(s):
    """Sort key for natural sorting, handling both numbers and letters."""
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]


class super_saver(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.pattern = r'(_v\d+)|(_V\d+)'
        self.tasks = {
            "model": [
                'model',
                'MDL',
                'mdl',
                'Model',
                'MODEL'
                ],
            "lookdev": [
                'lookdev',
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
                'Lookdev',
                'LOOKDEV',
                'VisDev',
                'visdev',
                'vsd',
                'VSD'
                ],
            "rig": [
                'rig',
                'Rig',
                'RIG',
                'rigging',
                'Rigging',
                'RIGGING'
                ],
            "anim": [
                'anim',
                'Animation',
                'ANIM',
                'animation',
                'anm',
                'ANM',
                'Anim',
                ],
            "lighting": [
                'lighting',
                'Lighting',
                'LGT',
                'Light',
                'lgt',
                'light',
                'LIGHT',
                'LIGHTING',
                'Lgt'
            ],
            "sculpt": [
                'sculpt',
                'Sculpt',
                'SCPT',
                'scpt',
                'sclpt',
                'spt',
                'scl'
                'SCLPT',
                'SPT',
                'SCL'
                ],
            "groom": [
                'groom',
                'Groom',
                'GRM',
                'grm',
                'hair',
                'Hair',
                'HAIR',
                'fur',
                'FUR',
                'Fur'
            ],
            "fx": [
                'fx',
                'Dynamics',
                'FX',
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
            "cloth": [
                'cloth',
                'Cloth',
                'CLTH',
                'clth',
                'CTH',
                'cth'
                ],
            "prototype": [
                'prototype',
                'Prototype',
                'PROTO',
                'Proto',
                'prt',
                'PRT',
                'proto'
            ],
            "previs": [
                'previs',
                'Previs',
                'PreVis',
                'PRV',
                'PVS',
                'pre'
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
        self.ui = ssui.Ui_SaveAs()
        self.ui.setupUi(self)

        self.settings = QSettings(__author__, 'Super Saver')
        self.position = self.settings.value('geometry', None)
        self.showcode = self.settings.value('showcode', None)
        self.appendartist = self.settings.value('appendArtist', None)
        self.restoreGeometry(self.position)

        pth = cmds.file(q=True, sn=True)
        print('scene path: %s' % pth)
        self.current_file_path = pth

        workspace = cmds.workspace(q=True, act=True)
        scene_folder = cmds.workspace(fre='scene')
        self.scene_folder_path = os.path.join(workspace, scene_folder)
        print(scene_folder)

        # Set initial artist field
        print(self.appendartist)
        if self.appendartist == 'true':
            self.appendartist = True
        else:
            self.appendartist = False
        self.ui.AppendArtist.setChecked(self.appendartist)
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

            if self.appendartist:
                base_filename = '{bfn}_{artist}'.format(bfn=version_info['base_filename'], artist=artist)
            else:
                base_filename = '{bfn}'.format(bfn=version_info['base_filename'])
            version = version_info['version']
            extension = version_info['extension']
            v_len = version_info['v_len']
            v_type = version_info['v_type']
        elif workspace:
            save_path = os.path.join(workspace, scene_folder)
            if '\\' in workspace:
                workspace = workspace.replace('\\', '/')
            if '\\' in save_path:
                save_path = save_path.replace('\\', '/')

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
            base_filename = '{show}{root_name}_{task}'.format(show=show_code, root_name=project_name,
                                                                       task=self.task)
            if self.appendartist:
                base_filename = base_filename + '_{artist}'.format(artist=artist)

            v_type = '_v'
            v_len = 3
            extension = self.ui.fileType.currentText()
            save_file = self.format_name(basename=base_filename, _v=v_type, v=version, l=v_len, ext=extension)

        else:
            save_path = cmds.file(q=True, dir=True)
            version = 1
            base_filename = 'default'
            save_file = self.format_name(basename=base_filename)
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

        self.ui.existingFile_list.setHeaderHidden(True)
        self.ui.existingFile_list.itemClicked.connect(self.show_existing_note)
        self.populate_existing_files(root_directory=self.scene_folder_path, current_folder=os.path.dirname(save_path))

        self.set_custom()

        self.ui.customNaming.clicked.connect(self.set_custom)
        self.ui.autoNaming.clicked.connect(self.set_custom)
        self.ui.cancel_btn.clicked.connect(self.close)
        self.ui.snap_pub_btn.clicked.connect(self.open_snapub)

        self.ui.folder.textChanged.connect(self.update_ui)
        self.ui.taskType.currentTextChanged.connect(lambda: self.reset_version(v=1))
        self.ui.version.valueChanged.connect(self.update_ui)
        self.ui.fileType.currentTextChanged.connect(self.update_ui)
        self.ui.filename.textChanged.connect(self.remove_bad_characters)
        self.ui.filename.textChanged.connect(self.update_ui)
        self.ui.showCode.textChanged.connect(self.update_ui)
        self.ui.artistName.textChanged.connect(self.update_ui)
        self.ui.open_btn.clicked.connect(self.open_file)
        self.ui.open_btn.setEnabled(False)
        self.ui.open_btn.setStyleSheet(
            'color: rgb(140, 140, 140);'
        )

        self.ui.save_btn.clicked.connect(self.run)
        self.ui.folder_btn.clicked.connect(self.get_folder)

        self.show()

    def open_file(self, f=False):
        # get_filename = self.ui.existingFile_list.currentItem()
        current_item = self.ui.existingFile_list.currentItem()
        if current_item:
            file_info = current_item.data(0, Qt.UserRole)
            if file_info:
                folder = file_info['folder']
                filename = file_info['file']
                open_file = os.path.join(folder, filename)
                try:
                    self.hide()
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

    def format_name(self, basename=None, _v='_v', v=1, l=3, ext='ma'):
        if basename:
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
        # FIXME: I'm going to add a sort of show data config file as an option here.  It needs to be secondary, but
        #  look for a config file if show_code returns false.  Only then, if it still can't find the config, will it
        #  return an empty string.  Now, since Maya's python doesn't have configuration built in, I'll use a simple txt
        show_code = None
        if path:
            checked_path = path.replace('\\', '/')
            split_path = checked_path.split('/')
            for seg in split_path:
                if len(seg) == 3:
                    show_code = seg
                    break
        if not show_code:
            project_root = cmds.workspace(q=True, rd=True)
            config_path = os.path.join(project_root, 'config.txt')
            if os.path.exists(config_path):
                with open(config_path, "r") as config:
                    data = config.readlines()
                    for line in data:
                        if 'show_code' in line:
                            break_line = line.split(':')
                            code = str(break_line[1]).strip()
                            show_code = code
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

    def build_path(self, path=None, rootName=None, task=None, v_type='_v', v_len=3, version=0, ext=None, show='',
                   artist=None):
        output_path = None
        if path and rootName and ext:
            try:
                if rootName.startswith(show):
                    show = ''
            except TypeError as e:
                print('ERROR: %s' % e)
                show = ''
            if task:
                if self.appendartist:
                    filename = '{show}{base}_{task}_{artist}{_v}{v:0{l}d}.{ext}'.format(base=rootName, task=task, _v=v_type,
                                                                                        l=v_len, v=version, ext=ext,
                                                                                        show=show, artist=artist)
                    basename = '{show}{base}_{task}_{artist}'.format(base=rootName, task=task, show=show, artist=artist)
                else:
                    filename = '{show}{base}_{task}{_v}{v:0{l}d}.{ext}'.format(base=rootName, task=task, _v=v_type,
                                                                                        l=v_len, v=version, ext=ext,
                                                                                        show=show)
                    basename = '{show}{base}_{task}'.format(base=rootName, task=task, show=show)
            else:
                if self.appendartist:
                    filename = '{show}{base}_{artist}{_v}{v:0{l}d}.{ext}'.format(base=rootName, _v=v_type, l=v_len,
                                                                                 v=version, ext=ext, show=show,
                                                                                 artist=artist)
                    basename = '{show}{base}_{artist}'.format(base=rootName, show=show, artist=artist)
                else:
                    filename = '{show}{base}{_v}{v:0{l}d}.{ext}'.format(base=rootName, _v=v_type, l=v_len,
                                                                        v=version, ext=ext, show=show)
                    basename = '{show}{base}'.format(base=rootName, show=show)
            check_filename = self.get_save_file(save_file=filename, save_path=path, basename=basename)
            filename = check_filename[0]
            # Do I add the version update here?  Nope

            next_version = int(check_filename[1])
            print('shit', next_version)  # What is this for?

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

    def show_existing_note(self, item, column):
        if not self.ui.open_btn.isEnabled():
            self.ui.open_btn.setEnabled(True)
            self.ui.open_btn.setStyleSheet(
                'color: rgb(220, 220, 220);'
            )
        # get_filename = self.ui.existingFile_list.currentItem()
        file_info = item.data(0, Qt.UserRole)
        if file_info:
            folder_name = file_info['folder']
            filename = file_info['file']
            folder = self.make_db_folder(folder_name)
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

    def populate_existing_files(self, root_directory=None, current_folder=None):
        allowed_extensions = ['ma', 'mb', 'obj', 'fbx', 'abc']
        excluded_folders = ['db', 'edits', '.mayaSwatches']

        if root_directory:
            if os.path.exists(root_directory):
                # Dictionary to hold the parent items for each folder path
                folder_items = {}

                # Sort folders and files first to ensure the correct order
                for folder_name, subfolders, files in os.walk(root_directory, topdown=True):
                    # Remove the root folder path from the display
                    relative_folder_name = os.path.relpath(folder_name, root_directory)

                    # Skip adding excluded folders
                    if any(excluded_folder in relative_folder_name.split(os.sep) for excluded_folder in
                           excluded_folders):
                        continue

                    # Determine the parent folder item
                    if relative_folder_name == ".":
                        parent_item = self.ui.existingFile_list
                    else:
                        parent_item = folder_items.get(os.path.dirname(relative_folder_name), self.ui.existingFile_list)

                    # Create a tree item for the current folder, avoid adding the same folder twice
                    if relative_folder_name not in folder_items:
                        folder_item = QTreeWidgetItem(parent_item)
                        folder_item.setText(0, os.path.basename(folder_name))
                        folder_items[relative_folder_name] = folder_item

                        # Expand the current folder or the folder of the currently opened file
                        if self.root_name.startswith(os.path.join(root_directory, relative_folder_name)):
                            folder_item.setExpanded(True)

                    # Sort subfolders and files naturally before adding them
                    subfolders.sort(key=natural_sort_key)
                    files.sort(key=natural_sort_key)

                    # Add subfolders first
                    for subfolder in subfolders:
                        subfolder_path = os.path.join(folder_name, subfolder)
                        relative_subfolder_name = os.path.relpath(subfolder_path, root_directory)

                        if relative_subfolder_name not in folder_items:
                            subfolder_item = QTreeWidgetItem(folder_items[relative_folder_name])
                            subfolder_item.setText(0, os.path.basename(subfolder))
                            folder_items[relative_subfolder_name] = subfolder_item

                    # Add files after subfolders, filtering by allowed extensions
                    for file_name in files:
                        file_extension = file_name.split('.')[-1].lower()
                        if file_extension not in allowed_extensions:
                            continue

                        file_path = os.path.normpath(os.path.join(folder_name, file_name))
                        file_path = file_path.replace('\\', '/')
                        file_item = QTreeWidgetItem(folder_items[relative_folder_name])
                        file_item.setText(0, file_name)
                        file_item.setData(0, Qt.UserRole, {"folder": folder_name, "file": file_name})

                        # Highlight the currently opened file
                        if file_path == self.current_file_path:
                            file_item.setSelected(True)
                            self.ui.existingFile_list.scrollToItem(file_item)
                            folder_items[relative_folder_name].setExpanded(True)
                            self.ui.existingFile_list.itemClicked.emit(file_item, 0)

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

    def open_snapub(self):
        # attempt to open the snap publisher
        snapub_path = os.path.join(script_path, 'snap_publisher.py')
        with open(snapub_path) as snp:
            code = snp.read()
            exec(code)

    def closeEvent(self, event):
        self.settings.setValue('appendArtist', self.ui.AppendArtist.isChecked())
        self.settings.setValue('showcode', self.ui.showCode.text())
        self.settings.setValue('geometry', self.saveGeometry())


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
    except Exception as e:
        app = QApplication.instance()
    saveas = super_saver()
    try:
        sys.exit(app.exec())
    except SystemExit as e:
        print(e)
