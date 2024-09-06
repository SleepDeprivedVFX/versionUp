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
#  3. The Recent Files menu is doubling up on files

"""
TODO: List - Upgrades needed
    1. Add right-click context menu for load-ref, import, update and others.
    2. Add hotkeys for Snapshot, Publish and Save.
    3. Add a playblast feature
    4. Integrate into Maya startup routine or module
    5. Make an FBX / OBJ / ABC publisher
    7. If no file exists, disable the publish button.
    8. Add an asset creation form on Assets tab
    9. Create a "Make Default Folders" button for existing projects.
"""

from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt, QSettings, QTimer)
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
import configparser

# FIXME: Add garbage for the UI to work in Maya.
script_path = "C:/Users/sleep/OneDrive/Documents/Scripts/Python/Maya/Utilities/sansPipe"
ui_path = os.path.join(script_path, 'ui')
ui_path = ui_path.replace('\\', '/')
if script_path not in sys.path:
    sys.path.append(script_path)
if ui_path not in sys.path:
    sys.path.append(ui_path)

from ui import ui_superSaver_UI as ssui

__version__ = '1.2.1'
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
        # TODO: The self.tasks should probably find their way into the config files, BUT for now, I'm leaving them here.
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
            ],
            "layout": [
                'layout',
                'Layout',
                'LayOut',
                'LAY',
                'LYO',
                'lay'
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
        # TODO: The cameraNames should probably find their way into the config files as well.
        self.cameraNames = [
            'shotcam',
            'camera',
            'shot',
            'scenecamera',
            'scenecam',
            'cam',
            'shot_cam',
            'shot_camera',
            'scene_cam',
            'scene_camera'
        ]
        self.cameraAttributes = ['translateX', 'translateY', 'translateZ', 'rotateX', 'rotateY', 'rotateZ',
                                 'scaleX', 'scaleY', 'scaleZ', 'visibility', 'centerOfInterest']
        self.root_name = None
        self.task = None
        self.ui = ssui.Ui_SaveAs()
        self.ui.setupUi(self)

        # Get basic scene information - File path, Workspace, Scene and Asset folders.
        pth = cmds.file(q=True, sn=True)
        self.current_file_path = pth
        workspace = cmds.workspace(q=True, rd=True)
        self.workspace = workspace
        scene_folder = cmds.workspace(fre='scene')
        self.scene_folder_path = os.path.join(workspace, scene_folder)
        asset_folder = cmds.workspace(fre='templates')
        self.asset_folder_path = os.path.join(workspace, asset_folder)
        # self.project_name = os.path.basename(os.path.normpath(cmds.workspace(q=True, rd=True)))

        # Set window title
        self.setWindowTitle('Sans Pipe Super Saver - v%s' % __version__)

        # Check for and load config file
        self.config_path = os.path.join(workspace, 'show_config.cfg')
        if not os.path.exists(self.config_path):
            self.build_config_file(path=self.config_path)

        self.settings = QSettings(__author__, 'Sans Pipe Super Saver')
        self.position = self.settings.value('geometry', None)
        self.appendartist = self.settings.value('appendArtist', None)
        self.recent_files = self.settings.value('recent_files', [])
        self.recent_projects = self.settings.value('recent_projects', [])
        self.bakeCamSceneName = self.settings.value('bake_cam_scene_name', None)
        self.autosave = self.settings.value('autosave', None)
        self.asset_shot_type = self.settings.value('asset_shot', None)
        self.restoreGeometry(self.position)

        if self.recent_files:
            self.populate_recent_files()
        else:
            self.recent_files = []

        if self.recent_projects:
            self.populate_recent_projects()
        else:
            self.recent_projects = []

        # Fix boolean checkboxes.
        if self.appendartist == 'true':
            self.appendartist = True
        else:
            self.appendartist = False
        if self.bakeCamSceneName == 'true':
            self.bakeCamSceneName = True
        else:
            self.bakeCamSceneName = False
        if self.autosave == 'true':
            self.autosave = True
        else:
            self.autosave = False
        self.ui.AppendArtist.setChecked(self.appendartist)
        self.ui.bakeCamSceneName.setChecked(self.bakeCamSceneName)
        self.ui.autosaver.setChecked(self.autosave)
        self.ui.assetShot_type.setCurrentText(self.asset_shot_type)

        # Check Autosave Settings
        self.set_autosave()

        # Set initial artist field
        artist = os.environ[env_user]
        first_initials = artist[0:2]
        first_initials = first_initials.upper()
        last_name = artist[2:]
        artist = first_initials + last_name
        self.ui.artistName.setText(artist)

        # Get the configurations
        config = configparser.ConfigParser()
        config.read(self.config_path)
        # show_code = self.try_to_get_show_code(path=workspace)
        self.show_code = config['Project']['Show_Code']
        show_code = self.show_code
        self.project_name = config['Project']['Show_Name']
        self.res_width = config['Camera']['resolution_width']
        self.res_height = config['Camera']['resolution_height']
        self.filmback_width = config['Camera']['filmback_width']
        self.filmback_height = config['Camera']['filmback_height']
        self.scene_scale = config['Scene']['scene_scale']
        self.recent_file_count = int(config['Project']['recent_file_count'])
        self.autosave_interval = int(config['Scene']['autosave_interval'])

        self.ui.showName.setText(self.project_name)
        self.ui.resolutionWidth.setText(self.res_width)
        self.ui.resolutionHeight.setText(self.res_height)
        self.ui.filmback_width.setText(self.filmback_width)
        self.ui.filmback_height.setText(self.filmback_height)
        self.ui.sceneScale.setText(self.scene_scale)
        self.ui.recent_file_count.setValue(self.recent_file_count)
        self.ui.autosave_count.setValue(self.autosave_interval)

        self.populate_project_settings()

        if pth:
            # Check against current project
            save_path = os.path.dirname(pth)
            save_file = os.path.basename(pth)

            if self.show_code:
                self.ui.showCode.setText(self.show_code)
                self.ui.showCodeSet.setText(self.show_code)
                show_code = '{show_code}_'.format(show_code=self.show_code)
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

            if self.show_code:
                self.ui.showCode.setText(self.show_code)
                self.ui.showCodeSet.setText(self.show_code)
                show_code = '%s_' % self.show_code

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
        self.ui.assetTree.setHeaderHidden(True)
        self.ui.snapshots.setHeaderHidden(True)
        self.ui.snapshots.itemDoubleClicked.connect(self.import_snapshot)
        self.ui.existingFile_list.itemClicked.connect(self.show_file_selection_info)
        # self.ui.existingFile_list.itemClicked.connect(self.populate_snapshots)
        self.ui.existingFile_list.itemDoubleClicked.connect(lambda: self.open_file(f=False))
        self.populate_existing_files(current_directory=self.scene_folder_path)
        self.populate_existing_files(current_directory=self.asset_folder_path)
        self.populate_publish_assets(current_directory=self.scene_folder_path)
        # self.populate_publish_assets(current_directory=self.asset_folder_path)
        self.ui.recentFilesList.itemDoubleClicked.connect(lambda: self.open_recent_file(f=False))
        self.ui.recent_projects.itemDoubleClicked.connect(lambda: self.set_project(btn=False))
        self.ui.set_proejct_btn.clicked.connect(lambda: self.set_project(btn=True))
        self.ui.new_project_folder_btn.clicked.connect(self.get_project_folder)
        self.reference_tracker()

        self.set_custom()

        self.ui.customNaming.clicked.connect(self.set_custom)
        self.ui.autoNaming.clicked.connect(self.set_custom)
        self.ui.cancel_btn.clicked.connect(self.close)
        self.ui.snap_btn.clicked.connect(self.snapshot)
        self.ui.publish_btn.clicked.connect(self.publish)
        self.ui.load_btn.clicked.connect(lambda: self.load_ref(element=self.ui.existingFile_list))
        self.ui.bakeCam_btn.clicked.connect(self.start_cam_bake)
        self.ui.import_btn.clicked.connect(lambda: self.import_object(element=self.ui.existingFile_list))
        self.ui.import_2_btn.clicked.connect(lambda: self.import_object(element=self.ui.assetTree))
        self.ui.loadRef_2_btn.clicked.connect(lambda: self.load_ref(element=self.ui.assetTree))

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
        self.ui.load_btn.setEnabled(False)
        self.ui.load_btn.setStyleSheet(
            'color: rgb(140, 140, 140);'
        )
        self.ui.import_btn.setEnabled(False)
        self.ui.import_btn.setStyleSheet(
            'color: rgb(140, 140, 140);'
        )
        self.ui.save_btn.clicked.connect(lambda: self.run(close=True))
        self.ui.folder_btn.clicked.connect(self.get_folder)
        self.ui.save_config_btn.clicked.connect(self.save_config)
        self.ui.updateRefs_btn.clicked.connect(self.update_references)
        self.ui.clear_recent_btn.clicked.connect(self.clear_recent_files)
        self.ui.create_project_btn.clicked.connect(self.create_project)
        self.ui.build_folders_btn.clicked.connect(lambda: self.create_folders(proj_path=cmds.workspace(q=True,
                                                                                                       rd=True)))
        self.ui.make_asset_btn.clicked.connect(self.create_asset_shot)

        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        self.ui.toolsGroup.setFont(title_font)

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
                    self.current_file_path = open_file
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
                    ret = pop_up.exec()
                    if ret == QMessageBox.Yes:
                        cmds.file(s=True)
                        self.open_file(f=False)
                    elif ret == QMessageBox.No:
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

    def clear_recent_files(self):
        self.ui.recentFilesList.clear()
        self.recent_files = []
        self.populate_recent_files()

    def remove_bad_characters(self):
        root_name = self.ui.filename.text()
        bad_x = [x for x in self.invalidCharacters if x in root_name]
        if bad_x:
            bad_x = bad_x[0]
            root_name = root_name.replace(bad_x, '_')
            self.ui.filename.setText(root_name)

    def make_new_filename(self, path=None, rootName=None):
        pass

    def build_config_file(self, path=None):
        if path:
            try:
                if not os.path.exists(path):
                    get_path = cmds.workspace(q=True, rd=True)
                    path = os.path.join(get_path, 'show_config.cfg')
                config = configparser.ConfigParser()
                config['Camera'] = {
                    'Resolution_Width': '2048',
                    'Resolution_Height': '1152',
                    'Filmback_Width': '23.1',
                    'Filmback_Height': '12.99'
                }
                config['Scene'] = {
                    'Scene_Scale': '10',
                    'autosave_interval': '10'
                }
                config['Project'] = {
                    'Show_Name': '%s' % self.try_to_get_project_name(),
                    'Show_Code': self.try_to_get_show_code(path=path),
                    'recent_file_count': '5'
                }
                with open(path, 'w') as configfile:
                    config.write(configfile)
            except PermissionError as e:
                cmds.error('Cannot create the Configuration file.  You may need to set folder permissions in your '
                           f'operating system to run the tool: {e}')

    def try_to_get_show_code(self, path=None):
        # This method returns a 3 letter show code either from the path, or from the workspace name.
        # It can be overridden in the configuration file.
        show_code = None
        if path:
            checked_path = path.replace('\\', '/')
            split_path = checked_path.split('/')
            for seg in split_path:
                if len(seg) == 3:
                    show_code = seg
                    break
        if not show_code:
            show_code = self.project_name[0]
            for char in self.project_name[1:]:
                if char.isupper():
                    show_code += char
                if len(show_code) == 3:
                    break
            if len(show_code) < 3:
                remaining_chars = [char for char in self.project_name[1:] if char.lower() not in show_code.lower()]
                show_code += ''.join(remaining_chars)[:3-len(show_code)]
        show_code = show_code.upper()
        return show_code

    def try_to_get_project_name(self):
        workspace = cmds.workspace(q=True, act=True)
        workspace = workspace.replace('\\', '/')
        split_ws = workspace.split('/')
        self.project_name = split_ws[-1]
        return self.project_name

    def save_config(self):
        if os.path.exists(self.config_path):
            config = configparser.ConfigParser()
            config.read(self.config_path)
            project_name = self.ui.showName.text()
            show_code = self.ui.showCodeSet.text()
            res_width = self.ui.resolutionWidth.text()
            res_height = self.ui.resolutionHeight.text()
            fb_width = self.ui.filmback_width.text()
            fb_height = self.ui.filmback_height.text()
            scale = self.ui.sceneScale.text()
            recent_file_count = self.ui.recent_file_count.value()
            as_interval = self.ui.autosave_count.value()
            config.set('Camera', 'resolution_width', res_width)
            config.set('Camera', 'resolution_height', res_height)
            config.set('Camera', 'filmback_width', fb_width)
            config.set('Camera', 'filmback_height', fb_height)
            config.set('Scene', 'scene_scale', scale)
            config.set('Scene', 'autosave_interval', str(as_interval))
            config.set('Project', 'show_name', project_name)
            config.set('Project', 'show_code', show_code)
            config.set('Project', 'recent_file_count', str(recent_file_count))

            with open(self.config_path, 'w') as configpath:
                config.write(configpath)

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

            if not show.endswith('_'):
                show = f'{show}_'
            print(f'bp: show: {show}')
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

    def check_for_latest_version(self, filename=None):
        if filename:
            # Parse the file's main info
            root_folder = os.path.dirname(filename)
            file_name = os.path.basename(filename)
            file_info = self.get_version_info(file_name)
            base_filename = file_info['base_filename']
            version = file_info['version']
            ext = file_info['extension']
            v_type = file_info['v_type']

            # make the pattern
            pattern = re.compile(rf"{base_filename}{v_type}(\d+)\.{ext}")

            latest_file = file_name

            for file in os.listdir(root_folder):
                match = pattern.match(file)
                if match:
                    # Extract the version number and convert to int
                    this_version = int(match.group(1))
                    if this_version > version:
                        latest_file = file
            latest_file = os.path.join(root_folder, latest_file)
            latest_file = latest_file.replace('\\', '/')
            return latest_file

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

    def create_note(self, notes=None, output_file=None):
        if notes and output_file:
            path = os.path.dirname(output_file)
            notes_path = self.make_db_folder(folder=path)
            notes_db = self.open_db(folder=notes_path)
            if not os.path.exists:
                os.makedirs(path)
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
        else:
            return False

    def show_file_selection_info(self, item, column):
        # Load selection info
        file_info = item.data(0, Qt.UserRole)
        file_text = item.text(0)
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

            # Setting the new file / copy to save features
            allow_file_copy = self.ui.allowFileCopy.isChecked()
            # Check if the file is saved or not
            existing_file = cmds.file(q=True, sn=True)
            # Build and update the scene file name
            if not existing_file or allow_file_copy:
                if not filename:
                    new_path = os.path.join(folder_name, file_text)
                    new_path = new_path.replace('\\', '/')
                    new_file_name = self.build_path(path=new_path, rootName=file_text,
                                                    task=self.ui.taskType.currentText(), v_type='_v', version=1,
                                                    ext=self.ui.fileType.currentText(), show=self.ui.showCode.text(),
                                                    artist=self.ui.artistName.text())
                    if new_file_name:
                        save_file = os.path.basename(new_file_name)
                        get_basename = save_file.split('_v')[0]
                        check_new_filename = self.get_save_file(save_file=save_file,
                                                                save_path=os.path.dirname(new_file_name),
                                                                basename=get_basename,
                                                                ext=self.ui.fileType.currentText())

                        update_file_name = check_new_filename[0]
                        new_version = check_new_filename[1]
                        self.ui.output_filename.setText(new_file_name)
                        self.ui.version.setValue(new_version)
                        self.ui.folder.setText(new_path)
                        if self.show_code in update_file_name:
                            get_short_filename = update_file_name.split('_', maxsplit=1)[1]
                        else:
                            get_short_filename = update_file_name
                        if self.ui.taskType.currentText() in get_short_filename:
                            get_root_name = get_short_filename.split(self.ui.taskType.currentText())[0]
                            get_root_name = get_root_name.strip('_')
                        else:
                            get_root_name = get_short_filename
                        self.ui.filename.setText(get_root_name)

            if file_text != 'scenes' and file_text != 'assets':
                if not filename:
                    selected_folder = os.path.join(folder_name, file_text)
                else:
                    selected_folder = folder_name
            else:
                selected_folder = folder_name

            # Make sure it's a file, not a folder
            if filename:
                # Make button decisions.
                if not self.ui.open_btn.isEnabled():
                    self.ui.open_btn.setEnabled(True)
                    self.ui.open_btn.setStyleSheet(
                        'color: rgb(220, 220, 220);'
                    )
                if any(pubass in folder_name for pubass in ['Publishes', 'assets']):
                    if not self.ui.load_btn.isEnabled() and not self.ui.import_btn.isEnabled():
                        self.ui.load_btn.setEnabled(True)
                        self.ui.load_btn.setStyleSheet(
                            'color: rgb(220, 220, 220);'
                        )
                        self.ui.import_btn.setEnabled(True)
                        self.ui.import_btn.setStyleSheet(
                            'color: rgb(220, 220, 220);'
                        )
                else:
                    self.ui.load_btn.setEnabled(False)
                    self.ui.load_btn.setStyleSheet(
                        'color: rgb(140, 140, 140);'
                    )
                    self.ui.import_btn.setEnabled(False)
                    self.ui.import_btn.setStyleSheet(
                        'color: rgb(140, 140, 140);'
                    )
            else:
                self.ui.open_btn.setEnabled(False)
                self.ui.open_btn.setStyleSheet(
                    'color: rgb(140, 140, 140);'
                )
                self.ui.load_btn.setEnabled(False)
                self.ui.load_btn.setStyleSheet(
                    'color: rgb(140, 140, 140);'
                )
                self.ui.import_btn.setEnabled(False)
                self.ui.import_btn.setStyleSheet(
                    'color: rgb(140, 140, 140);'
                )

            for note in notes_db['Notes']:
                if type(note) == dict and 'filename' in note.keys():
                    if filename in note['filename']:
                        user = note['user']
                        date = note['date']
                        computer = note['computer']
                        details = note['details']

                        # Set pretty date
                        d_date = datetime.strptime(date, '%Y-%m-%d | %H:%M:%S.%f')
                        date = d_date.strftime('%m/%d/%Y - %I:%M:%S%p')

                        post_note = """FILE: {filename}
USER: {user}
COMP: {computer}
DATE: {date}

NOTE: {details}""".format(filename=filename, user=user, computer=computer, date=date, details=details)
                        break
            self.ui.existing_notes.setText(post_note)
            self.populate_snapshots(item, column)

    def populate_existing_files(self, current_directory=None):
        allowed_extensions = ['ma', 'mb', 'obj', 'fbx', 'abc']
        excluded_folders = ['db', 'edits', '.mayaSwatches', 'snapshots', 'Publishes']

        if current_directory:
            if os.path.exists(current_directory):
                # Dictionary to hold the parent items for each folder path
                folder_items = {}

                # Sort folders and files first to ensure the correct order
                for folder_name, subfolders, files in os.walk(current_directory, topdown=True):
                    # Remove the root folder path from the display
                    relative_folder_name = os.path.relpath(folder_name, current_directory)

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
                        folder_item.setData(0, Qt.UserRole, {"folder": folder_name, "file": ""})
                        folder_items[relative_folder_name] = folder_item

                        # Expand the current folder or the folder of the currently opened file
                        if self.root_name.startswith(os.path.join(current_directory, relative_folder_name)):
                            folder_item.setExpanded(True)

                    # Sort subfolders and files naturally before adding them
                    subfolders.sort(key=natural_sort_key)
                    files.sort(key=natural_sort_key)

                    # Add subfolders first
                    for subfolder in subfolders:
                        subfolder_path = os.path.join(folder_name, subfolder)
                        relative_subfolder_name = os.path.relpath(subfolder_path, current_directory)

                        # Skip adding excluded folders
                        if any(excluded_folder in relative_subfolder_name.split(os.sep) for excluded_folder in
                               excluded_folders):
                            continue

                        if relative_subfolder_name not in folder_items:
                            subfolder_item = QTreeWidgetItem(folder_items[relative_folder_name])
                            subfolder_item.setText(0, os.path.basename(subfolder))
                            subfolder_item.setData(0, Qt.UserRole, {"folder": folder_name, "file": ""})
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

    def populate_publish_assets(self, current_directory=None):
        allowed_extensions = ['ma', 'mb', 'obj', 'fbx', 'abc']
        excluded_folders = ['db', 'edits', '.mayaSwatches', 'snapshots']
        allowed_folders = ['assets', 'Publishes']

        if current_directory:
            self.ui.assetTree.clear()
            if os.path.exists(current_directory):
                folder_items = {}

                for folder_name, subfolders, files in os.walk(current_directory, topdown=True):
                    relative_folder_name = os.path.relpath(folder_name, current_directory)

                    # Skip excluded folders
                    if any(excluded_folder in relative_folder_name.split(os.sep) for excluded_folder in
                           excluded_folders):
                        continue

                    # Determine parent item (to preserve full folder hierarchy)
                    if relative_folder_name == '.':
                        parent_item = self.ui.assetTree
                    else:
                        parent_item = folder_items.get(os.path.dirname(relative_folder_name), self.ui.assetTree)

                    # Add the folder to the tree (preserve the folder structure)
                    if relative_folder_name not in folder_items:
                        folder_item = QTreeWidgetItem(parent_item)
                        folder_item.setText(0, os.path.basename(folder_name))
                        folder_item.setData(0, Qt.UserRole, {"folder": folder_name, "file": ""})
                        folder_items[relative_folder_name] = folder_item

                        # Expand if it's the root directory
                        if self.root_name.startswith(os.path.join(current_directory, relative_folder_name)):
                            folder_item.setExpanded(True)

                    subfolders.sort(key=natural_sort_key)
                    files.sort(key=natural_sort_key)

                    for subfolder in subfolders:
                        subfolder_path = os.path.join(folder_name, subfolder)
                        relative_subfolder_name = os.path.relpath(subfolder_path, current_directory)

                        if any(excluded_folder in relative_subfolder_name.split(os.sep) for excluded_folder in
                               excluded_folders):
                            continue
                        if relative_subfolder_name not in folder_items:
                            subfolder_item = QTreeWidgetItem(folder_items[relative_folder_name])
                            subfolder_item.setText(0, os.path.basename(subfolder))
                            subfolder_item.setData(0, Qt.UserRole, {"folder": folder_name, "file": ""})
                            folder_items[relative_subfolder_name] = subfolder_item

                    for file_name in files:
                        file_extension = file_name.split('.')[-1].lower()
                        if file_extension not in allowed_extensions:
                            continue

                        # Check if the file is in an allowed folder ("assets" or "Publishes")
                        if any(allowed_folder in relative_folder_name.split(os.sep) for allowed_folder in
                               allowed_folders):
                            file_path = os.path.normpath(os.path.join(folder_name, file_name))
                            file_path = file_path.replace('\\', '/')

                            # Add the file to the tree if in allowed folders
                            file_item = QTreeWidgetItem(folder_items[relative_folder_name])
                            file_item.setText(0, file_name)
                            file_item.setData(0, Qt.UserRole, {'folder': folder_name, 'file': file_name})

    def message(self, text=None, ok=True, obj=None):
        self.ui.messages.setText(text)
        if ok:
            self.ui.messages.setStyleSheet(
                "color: rgb(150, 255, 150);\nfont: 9pt \"MS Shell Dlg 2;\""
            )
        else:
            self.ui.messages.setStyleSheet(
                "color: rgb(255, 150, 150);\nfont: 12pt \"MS Shell Dlg 2;\""
            )
        if obj:
            obj.setStyleSheet('border: 2px solid red;')
            QTimer.singleShot(3000, lambda: obj.setStyleSheet(''))
        QTimer.singleShot(8000, lambda: self.ui.messages.setText(''))

    def run(self, close=True):
        output_file = self.ui.output_filename.text()
        overwrite = self.ui.overwrite.isChecked()
        fileType = self.ui.fileType.currentText()
        notes = self.ui.notes.toPlainText() 
        if not notes:
            self.message(text='YOU MUST ADD A NOTE!!!', ok=False, obj=self.ui.notes)
            return False
        elif len(notes) < 10:
            self.message(text='Your note must be more elaborate.', ok=False, obj=self.ui.notes)
            return False
        else:
            self.message(text='Version up save in progress', ok=True)

        if fileType == 'ma':
            fileType = 'mayaAscii'
        else:
            fileType = 'mayaBinary'

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

        # Create Note
        self.create_note(notes=notes, output_file=output_file)

        time.sleep(3)
        print('run: close: %s' % close)
        if close:
            self.close()
        else:
            return output_file
        return True

    def snapshot(self, note=None):
        if note:
            notes = 'Automatic snapshot - update from replacement snapshot: %s' % note
        else:
            notes = self.ui.notes.toPlainText()
        if not notes:
            self.message(text='YOU MUST ADD A NOTE!!!', ok=False, obj=self.ui.notes)
            return False
        elif len(notes) < 10:
            self.message(text='Your note must be more elaborate.', ok=False, obj=self.ui.notes)
            return False
        else:
            self.message(text='Snapshot in progress', ok=True)

        current_file_path = self.current_file_path
        current_root = os.path.dirname(current_file_path)

        base_filename = os.path.basename(current_file_path)

        get_root_file_name = os.path.splitext(base_filename)
        root_file_name = get_root_file_name[0]
        file_extention = get_root_file_name[1]

        snapshot_folder = os.path.join(current_root, 'snapshots')
        if not os.path.exists(snapshot_folder):
            os.makedirs(snapshot_folder)
        date = str(datetime.date(datetime.now()))
        date_stamp = date.replace('-', '')

        hour = str(datetime.time(datetime.now()).hour)
        minute = str(datetime.time(datetime.now()).minute)
        second = str(datetime.time(datetime.now()).second)
        time_stamp = hour + minute + second
        datetime_stamp = date_stamp + time_stamp
        snapshot_filename = '%s_%s%s' % (root_file_name, datetime_stamp, file_extention)
        if file_extention == '.mb':
            file_ext_text = 'mayaBinary'
        elif file_extention == '.ma':
            file_ext_text = 'mayaAscii'
        else:
            file_ext_text = 'mayaAscii'

        snapshot = os.path.join(snapshot_folder, snapshot_filename)

        new_snap = cmds.file(snapshot, f=True, options='v=0;', type=file_ext_text, pr=True, ea=True)
        if new_snap:
            snapshots_db = os.path.join(snapshot_folder, 'snapshots.json')
            if not os.path.exists(snapshots_db) or os.path.getsize(snapshots_db) == 0:
                snap_data = {
                    'Snapshots': []
                }
                with open(snapshots_db, 'w') as snaps:
                    snap_load = json.dumps(snap_data, indent=4)
                    snaps.write(snap_load)
            else:
                with open(snapshots_db, 'r') as snaps:
                    get_snap_data = snaps.read()
                    if get_snap_data.strip() == "":
                        snap_data = {'Snapshots': []}  # Handle empty file
                    else:
                        try:
                            snap_data = json.loads(get_snap_data)
                        except json.JSONDecodeError:
                            snap_data = {'Snapshots': []}

            # Set pretty date
            d_date = datetime.now()
            date = d_date.strftime('%m/%d/%Y - %I:%M:%S%p')
            new_data = {
                'datestamp': date,
                'filename': snapshot_filename,
                'root_path': snapshot_folder,
                'original_file': cmds.file(q=True, sn=True),
                'notes': notes
            }
            snap_data['Snapshots'].append(new_data)
            with open(snapshots_db, 'w') as snaps:
                snap_load = json.dumps(snap_data, indent=4)
                snaps.write(snap_load)
        else:
            self.message(text='UNABLE TO SAVE SNAPSHOT!!', ok=False)
        self.ui.notes.clear()
        self.message(text='File snapshot --> %s' % datetime_stamp, ok=True)
        current_file_item = self.ui.existingFile_list.currentItem()
        self.ui.existingFile_list.itemClicked.emit(current_file_item, 0)

    def open_recent_file(self, f=False):
        current_item = self.ui.recentFilesList.currentItem()
        file_text = current_item.text()
        open_file = current_item.data(Qt.UserRole)
        try:
            self.hide()
            cmds.file(open_file, o=True, f=f)
            recent_file = {
                'filename': file_text,
                'path': open_file
            }
            self.current_file_path = open_file
            if recent_file in self.recent_files:
                recent_file_index = self.recent_files.index(recent_file)
                if recent_file_index:
                    self.recent_files.pop(recent_file_index)
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
            if ret == QMessageBox.Yes:
                cmds.file(s=True)
                self.open_recent_file(f=False)
            elif ret == QMessageBox.No:
                self.open_recent_file(f=True)
            else:
                self.show()

    def populate_recent_files(self):
        recent_files = self.recent_files
        for this_file in recent_files:
            filename = this_file['filename']
            file_path = this_file['path']
            file_path = file_path.replace('\\', '/')
            new_entry = QListWidgetItem()
            new_entry.setText(filename)
            new_entry.setData(Qt.UserRole, file_path)
            new_entry.setToolTip(file_path)
            self.ui.recentFilesList.addItem(new_entry)

    def populate_snapshots(self, item, column):
        self.ui.snapshots.clear()
        file_info = item.data(0, Qt.UserRole)
        if file_info:
            root_path = file_info['folder']
            snap_path = os.path.join(root_path, 'snapshots')
            if os.path.exists(snap_path):
                # Look for the database
                snap_file = os.path.join(snap_path, 'snapshots.json')
                if os.path.exists(snap_file):
                    with open(snap_file, 'r') as snaps:
                        get_snap_data = snaps.read()
                        snap_data = json.loads(get_snap_data)
                        snapshots = snap_data['Snapshots']
                        last_item = None
                        for snapshot in snapshots:
                            datestamp = snapshot['datestamp']
                            filename = snapshot['filename']
                            _root_path = snapshot['root_path']
                            notes = snapshot['notes']
                            orig_file = snapshot['original_file']
                            snapshot_path = os.path.join(_root_path, filename)
                            short_original_file = os.path.basename(orig_file)

                            base_snap = QTreeWidgetItem(self.ui.snapshots)
                            base_snap.setText(0, str(datestamp))
                            base_snap.setData(0, Qt.UserRole, snapshot_path)
                            sub_file = QTreeWidgetItem(base_snap)
                            sub_file.setText(0, filename)
                            sub_file.setData(0, Qt.UserRole, snapshot_path)
                            sub_orig = QTreeWidgetItem(base_snap)
                            sub_orig.setText(0, short_original_file)
                            sub_orig.setData(0, Qt.UserRole, snapshot_path)
                            sub_notes = QTreeWidgetItem(base_snap)
                            sub_notes.setText(0, notes)
                            sub_notes.setData(0, Qt.UserRole, snapshot_path)

                            last_item = base_snap  # Keep track of the last item created

                        if last_item:
                            last_item.setExpanded(True)  # Expand only the last item

    def populate_recent_projects(self):
        self.ui.recent_projects.clear()
        if self.recent_projects:
            for project in self.recent_projects:
                new_item = QListWidgetItem()
                new_item.setText(project)
                self.ui.recent_projects.addItem(new_item)

    def populate_project_settings(self):
        scenes = cmds.workspace(fre='scene')
        asset = cmds.workspace(fre='templates')
        images = cmds.workspace(fre='images')
        sourceimages = cmds.workspace(fre='sourceImages')
        renderdata = cmds.workspace(fre='renderData')
        clips = cmds.workspace(fre='clips')
        sounds = cmds.workspace(fre='sound')
        scripts = cmds.workspace(fre='scripts')
        diskcache = cmds.workspace(fre='diskCache')
        movies = cmds.workspace(fre='movie')
        time_editor = cmds.workspace(fre='timeEditor')
        autosave = cmds.workspace(fre='autoSave')
        scene_assembly = cmds.workspace(fre='sceneAssembly')

        self.ui.set_project.setText(cmds.workspace(q=True, act=True))
        self.ui.scenes.setText(scenes)
        self.ui.assets.setText(asset)
        self.ui.images.setText(images)
        self.ui.source_images.setText(sourceimages)
        self.ui.render_data.setText(renderdata)
        self.ui.clips.setText(clips)
        self.ui.sound.setText(sounds)
        self.ui.scripts.setText(scripts)
        self.ui.disk_cache.setText(diskcache)
        self.ui.movies.setText(movies)
        self.ui.time_editor.setText(time_editor)
        self.ui.autosave.setText(autosave)
        self.ui.scene_ass.setText(scene_assembly)

    def set_project(self, btn=False):
        if btn:
            self.hide()
            cmds.SetProject()
            self.close()
            return True
        current_item = self.ui.recent_projects.currentItem()
        path = current_item.text()
        if os.path.exists(path):
            cmds.workspace(path, openWorkspace=True)
        self.populate_project_settings()
        self.close()

    def create_project(self):
        self.message(text='', ok=True)
        project_name = self.ui.new_project_name.text()
        project_folder = self.ui.new_project_folder.text()

        if not project_name:
            self.message(text='You must have a project name!', ok=False, obj=self.ui.new_project_name)
            return False
        if not project_folder:
            self.message(text='You must have a project folder!', ok=False, obj=self.ui.new_project_folder)
        if not os.path.exists(project_folder):
            self.message(text='Not a valid project folder!', ok=False, obj=self.ui.new_project_folder)
            return False
        if any(chars in project_name for chars in self.invalidCharacters):
            self.message(text='Project Name has Invalid Characters - only allowed alphanumerics. No spaces.', ok=False,
                         obj=self.ui.new_project_name)
            return False
        new_project_path = os.path.join(project_folder, project_name)
        if not os.path.exists(new_project_path):
            os.makedirs(new_project_path)

        try:
            cmds.workspace(new_project_path, newWorkspace=True)
        except RuntimeError as e:
            self.message(text=f'Workspace Already exists! {e}', ok=False, obj=self.ui.new_project_name)
            return False

        self.create_folders(proj_path=new_project_path)

        cmds.workspace(new_project_path, openWorkspace=True)
        self.close()

    def create_folders(self, proj_path=None):
        def do_subfolders(parent_path=None):
            if parent_path:
                print(f'cf: proj_path: {parent_path}')
                for subpath in subfolders:
                    new_scene_subpath = os.path.join(parent_path, subpath)
                    if not os.path.exists(new_scene_subpath):
                        print(f'cf: making subfolder: {new_scene_subpath}')
                        os.makedirs(new_scene_subpath)

        subfolders = [
            'Chars',
            'Env',
            'Props',
            'Shots',
            'Veh',
            'Cams'
        ]
        if proj_path:
            print(f'cf: proj_path: {proj_path}')
            folder_structure = {
                'scenes': self.ui.scenes.text(),
                'assets': self.ui.assets.text(),
                'images': self.ui.images.text(),
                'sourceimages': self.ui.source_images.text(),
                'renderdata': self.ui.render_data.text(),
                'clips': self.ui.clips.text(),
                'sounds': self.ui.sound.text(),
                'scripts': self.ui.scripts.text(),
                'diskcaches': self.ui.disk_cache.text(),
                'movies': self.ui.movies.text(),
                'timeeditor': self.ui.time_editor.text(),
                'autosave': self.ui.autosave.text(),
                'sceneassembly': self.ui.scene_ass.text()
            }
            for key, path in folder_structure.items():
                if path:
                    new_subpath = os.path.join(proj_path, path)
                    if not os.path.exists(new_subpath):
                        print(f'cf: creating new folder: {new_subpath}')
                        os.makedirs(new_subpath)
                        if path == self.ui.scenes.text() and self.ui.include_subfolders.isChecked():
                            do_subfolders(parent_path=new_subpath)
                    elif path == self.ui.scenes.text() and self.ui.include_subfolders.isChecked():
                        do_subfolders(parent_path=new_subpath)
                    cmds.workspace(fileRule=[key, path])
            cmds.workspace(saveWorkspace=True)
            cmds.workspace(proj_path, openWorkspace=True)
            self.update_ui()

    def create_asset_shot(self):
        _type = self.ui.assetShot_type.currentText()
        if _type == 'Cams':
            message_type = 'Camera'
        elif _type == 'Char':
            message_type = 'Character'
        elif _type == 'Env':
            message_type = 'Environment'
        elif _type == 'Prop':
            message_type = 'Prop'
        elif _type == 'Veh':
            message_type = 'Vehicle'
        else:
            message_type = 'Shot'
        if not self.ui.asset_name.text():
            self.message(text=f'You must give the {message_type} a name!', ok=False, obj=self.ui.assetShot_type)
            return False
        if any(bad_char in self.ui.asset_name.text() for bad_char in self.invalidCharacters):
            self.message(text='Only alphanumeric characters are allowed. No spaces!', ok=False, obj=self.ui.asset_name)
            return False

        # Create folder
        root_directory = cmds.workspace(q=True, rd=True)
        scenes_folder = cmds.workspace(fre='scenes')
        scenes_path = os.path.join(root_directory, scenes_folder)
        type_path = os.path.join(scenes_path, _type)
        path = os.path.join(type_path, self.ui.asset_name.text())
        if not os.path.exists(path):
            os.makedirs(path)
        self.ui.existingFile_list.clear()
        self.populate_existing_files(current_directory=self.scene_folder_path)
        self.populate_existing_files(current_directory=self.asset_folder_path)

    def get_project_folder(self):
        self.hide()
        new_project_folder = cmds.fileDialog2(fm=3, ds=2)
        if new_project_folder:
            new_project_folder = new_project_folder[0]
            if os.path.exists(new_project_folder):
                self.ui.new_project_folder.setText(new_project_folder)
        self.show()

    def set_autosave(self):
        if self.ui.autosaver.isChecked():
            print('autosave checked')
            cmds.optionVar(intValue=('autoSaveEnabled', 1))
            cmds.optionVar(intValue=('autoSaveInterval', self.ui.autosave_count.value()))
        else:
            print('autosave unchecked')
            cmds.optionVar(intValue=('autoSaveEnabled', 0))

    def import_snapshot(self, item, column):
        snapshot_path = item.data(0, Qt.UserRole)
        snapshot_file_date = os.path.getmtime(snapshot_path)
        current_file_path = cmds.file(q=True, sn=True)
        current_file_date = os.path.getmtime(current_file_path)
        if current_file_date > snapshot_file_date:
            self.hide()
            message = QMessageBox()
            message.setProperty('Do Quick Snapshot', True)
            message.setWindowTitle('Do Snapshot?')
            message.setText('Do you want to snapshot your current file?')
            message.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            message.setDefaultButton(QMessageBox.Yes)
            get_message = message.exec()
            if get_message == QMessageBox.Yes:
                self.snapshot(note='AUTO')
                self.show()
        current_file = os.path.basename(current_file_path)
        current_ext = os.path.splitext(current_file)[-1]
        if current_ext == '.ma':
            ext = 'mayaAscii'
        else:
            ext = 'mayaBinary'
        cmds.file(save=True)
        cmds.file(snapshot_path, open=True)
        cmds.file(rename=current_file_path)
        cmds.file(save=True, type=ext)

    def publish(self):
        '''
        What it needs to do:
        1. Take the current file and version up with a PUB note, but keep the original filename
        2. Save the file out to the Publishes folder with a PUB tag in it.
        3. Remove references and namespaces for the published file
        4. Reopen the new versioned up working file.
        '''
        notes = self.ui.notes.toPlainText()
        if not notes:
            self.message(text='YOU MUST ADD A NOTE!!!', ok=False, obj=self.ui.notes)
            return False
        elif len(notes) < 10:
            self.message(text='Your note must be more elaborate.', ok=False, obj=self.ui.notes)
            return False
        else:
            self.message(text='Publish in progress', ok=True)

        current_file = self.current_file_path

        # Do the version up first
        new_version = self.run(close=False)

        # Create the publish version
        root_path = os.path.dirname(current_file)
        base_name = os.path.basename(current_file)
        if '_v' in base_name:
            split_version = base_name.split('_v')
            v = '_v'
        else:
            split_version = os.path.splitext(base_name)
            v = ''

        ext = os.path.splitext(base_name)[1]
        if ext == '.ma':
            file_type = 'mayaAscii'
        else:
            file_type = 'mayaBinary'
        root_name = split_version[0]
        end_name = split_version[1]
        pub_name = root_name + '_PUB' + v + end_name

        pub_folder = os.path.join(root_path, 'Publishes')
        if not os.path.exists(pub_folder):
            os.makedirs(pub_folder)
        publish_file = os.path.join(pub_folder, pub_name)
        self.message(text='Publishing file...', ok=True)

        # Save out the publish file
        cmds.file(rename=publish_file)
        cmds.file(s=True, type=file_type, options='v=0;')

        # Clean out the references
        clean_refs = self.import_and_clean_references()
        if clean_refs:
            new_notes = """{notes}

References Imported and Cleaned:
""".format(notes=notes)
            for ref in clean_refs:
                ref_item = ref['ref']
                namespace = ref['namespace']
                removed = ref['removed']
                if removed:
                    namespace = ''
                ref_filename = os.path.basename(ref_item)
                new_notes = """{new_notes}
{namespace}: {ref_filename}
""".format(new_notes=new_notes, namespace=namespace, ref_filename=ref_filename)
            notes = new_notes

        # create new note
        self.create_note(notes=notes, output_file=publish_file)
        # Save publish file
        cmds.file(s=True, type=file_type, options='v=0;')

        # Reopen the versioned up file
        cmds.file(new_version, o=True)
        self.message(text='File Published Successfully!', ok=True)
        time.sleep(3)
        self.close()

    def reference_tracker(self):
        """
        This function collects all the references in a scene.  It then checks each file to see if it is the most recent
        version of the reference.  If it is not, the reference is flagged as being out of date.
        The function should then populate the self.ui.referenceList with multi-select capabilities.  If a reference is
        flagged as out of date, it should be styled with a red background, and automatically selected.
        :return:
        """
        self.ui.referenceList.clear()
        references = cmds.file(q=True, reference=True)
        reference_info = {}

        light_red = QColor(255, 102, 102)
        light_green = QColor(144, 238, 144)

        # Gathering all references
        for ref in references:
            # Get the path and namespace of the reference
            out_of_date = False
            ref_file = cmds.referenceQuery(ref, filename=True, wcn=True)
            namespace = cmds.referenceQuery(ref, namespace=True)
            ref_node = cmds.referenceQuery(ref, rfn=True)

            NS_basename = cmds.namespaceInfo(namespace, bn=True)

            # Count the duplicate entries
            if ref_file in reference_info.keys():
                reference_info[ref_file]['count'] += 1
            else:
                reference_info[ref_file] = {
                    'filename': ref_file,
                    'namespace': namespace,
                    'count': 1
                }

            # get the latest version
            latest_file = self.check_for_latest_version(filename=ref_file)
            if not latest_file == ref_file:
                print(f'{ref_file} is out of date!  Latest file is {latest_file}')
                out_of_date = True

            base_name = os.path.basename(ref_file)
            root_dir = os.path.dirname(ref_file)
            data = {
                'namespace': namespace,
                'path': root_dir,
                'reference_node': ref_node,
                'latest_file': latest_file
            }
            new_entry = QListWidgetItem()
            new_entry.setText(f'{NS_basename}:{base_name}')
            new_entry.setData(Qt.UserRole, data)

            # Set checkable
            new_entry.setFlags(new_entry.flags() | Qt.ItemIsUserCheckable)
            if out_of_date:
                new_entry.setCheckState(Qt.Checked)
                new_entry.setBackground(light_red)
                new_entry.setForeground(Qt.white)
                new_entry.setToolTip(f'Out of date! Latest version: {os.path.basename(latest_file)}')
            else:
                new_entry.setCheckState(Qt.Unchecked)
                new_entry.setBackground(light_green)
                new_entry.setForeground(Qt.black)
                new_entry.setToolTip(f'Up to Date!')

            self.ui.referenceList.addItem(new_entry)

    def update_references(self):
        update_items = self.get_checked_refs()

        # get references and start updating.
        for item, data in update_items.items():
            i = int(item)
            latest_file = data['latest_file']
            ref_node = data['reference_node']
            ext = os.path.splitext(latest_file)[1]
            if ext == '.ma':
                r_type = 'mayaAscii'
            elif ext == '.mb':
                r_type = 'mayaBinary'
            elif ext == '.fbx':
                r_type = 'FBX'
            elif ext == '.obj':
                r_type = 'OBJ'
            else:
                r_type = 'mayaAscii'

            if self.ui.referenceList.item(i).checkState() == Qt.Checked:
                cmds.file(latest_file, loadReference=ref_node, type=r_type, options="v=0;")
        self.reference_tracker()

    def get_checked_refs(self):
        checked_items = {}
        for i in range(self.ui.referenceList.count()):
            item = self.ui.referenceList.item(i)
            if item.checkState() == Qt.Checked:
                checked_items[i] = item.data(Qt.UserRole)
        return checked_items

    def import_and_clean_references(self):
        references = cmds.file(q=True, reference=True)
        reference_info = {}

        # First, gather all reference information
        for ref in references:
            ref_file = cmds.referenceQuery(ref, filename=True, wcn=True)
            namespace = cmds.referenceQuery(ref, namespace=True)

            if ref_file in reference_info.keys():
                reference_info[ref_file]['count'] += 1
            else:
                reference_info[ref_file] = {
                    'filename': ref_file,
                    'namespace': namespace,
                    'count': 1
                }

        is_clean = []
        for ref in references:
            ref_file = cmds.referenceQuery(ref, filename=True, wcn=True)

            info = reference_info[ref_file]
            result = self.do_reference_cleanup(reference_file=ref_file, namespace=info['namespace'],
                                               count=info['count'])
            if result:
                is_clean.append(result)

        return is_clean

    def do_reference_cleanup(self, reference_file=None, namespace=None, count=None):
        cleaned = None
        if reference_file:
            # Import the reference
            cmds.file(reference_file, importReference=True)

            # Check if there is more than one instance of the reference
            if count == 1:
                # Remove the namespace if there's only one instance
                cmds.namespace(removeNamespace=namespace, mergeNamespaceWithRoot=True)
                cleaned = {'ref': reference_file, 'namespace': namespace, 'removed': True}
            else:
                # Keep the namespace if there are multiple instances
                cleaned = {'ref': reference_file, 'namespace': namespace, 'removed': False}

        return cleaned

    def load_ref(self, element=None):
        if not element:
            element = self.ui.existingFile_list
        current_item = element.currentItem()
        data = current_item.data(0, Qt.UserRole)
        file_name = data['file']
        file_root = os.path.splitext(file_name)[0]
        path = data['folder']
        path = path.replace('\\', '/')
        file_path = os.path.join(path, file_name)
        if os.path.exists(file_path):
            if cmds.file(file_path, q=True, exists=True):
                cmds.file(file_path, reference=True, ignoreVersion=True, gl=True, mergeNamespacesOnClash=False,
                          namespace=file_root, options='v=0;')
                self.message(text='Reference Loaded: %s' % file_name, ok=True)
            else:
                self.message(text='Maya could not find the reference: %s' % file_name)
        else:
            self.message(text='File could not be found: %s' % file_name)
        self.reference_tracker()

    def import_object(self, element=None):
        if not element:
            element = self.ui.existingFile_list
        current_item = element.currentItem()
        data = current_item.data(0, Qt.UserRole)
        file_name = data['file']
        file_root = os.path.splitext(file_name)[0]
        path = data['folder']
        path = path.replace('\\', '/')
        file_path = os.path.join(path, file_name)
        if os.path.exists(file_path):
            if cmds.file(file_path, q=True, exists=True):
                cmds.file(file_path, i=True, mergeNamespaceWithRoot=True)
                self.message(text='%s imported into scene' % file_root, ok=True)
            else:
                self.message(text='Maya could not import the file: %s' % file_name, ok=False)
        else:
            self.message(text='The file could not be found!', ok=False)

    def start_cam_bake(self):
        self.message(text='Baking Camera...', ok=True)
        bake_camera = self.cam_bake()
        if bake_camera:
            get_scene_name = cmds.file(q=True, sn=True)
            data = self.get_root_and_task(filename=get_scene_name)
            scene_name = os.path.splitext(os.path.basename(get_scene_name))[0]
            get_root_path = cmds.workspace(q=True, rd=True)
            task = data['task_name']
            if task in scene_name:
                cam_name = scene_name.replace(task, 'cam')
                cam_name = cam_name + '.fbx'
            else:
                cam_name = 'shot_cam'

            cmds.select(bake_camera, r=True)
            output_path = os.path.join(get_root_path, 'assets/Shot_Cams')
            output_file = os.path.join(output_path, cam_name)
            cmds.file(output_file, f=True,
                      options=";exportUVs=1;exportSkels=none;exportSkin=none;exportBlendShapes=0;exportDisplayColor=0;;exportColorSets=1;exportComponentTags=1;defaultMeshScheme=catmullClark;animation=0;eulerFilter=0;staticSingleSample=0;startTime=1;endTime=1;frameStride=1;frameSample=0.0;defaultUSDFormat=usdc;rootPrim=;rootPrimType=scope;defaultPrim=shotCam_baked;shadingMode=useRegistry;convertMaterialsTo=[UsdPreviewSurface];exportRelativeTextures=automatic;exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=0;worldspace=0;excludeExportTypes=[]",
                      type='FBX Export', pr=True, es=True, ex=False)
            cmds.select(bake_camera, r=True)
            cmds.delete()
            notes = (f'Automatic camera bake for {scene_name}.  Camera name: {bake_camera[0]}  '
                     f'Output filename: {os.path.basename(output_file)}')
            self.create_note(notes=notes, output_file=output_file)
            self.message(text='Camera baked successfully: %s' % cam_name, ok=True)
        else:
            self.message(text='Camera could not be baked!', ok=False)

    def cam_bake(self):
        cam_transform = None
        all_cams = cmds.ls(ca=True)
        for cam in all_cams:
            if self.ui.bakeCamSceneName.isChecked():
                if self.root_name in cam:
                    cmds.select(cam, r=True)
                    find_trans = cmds.listRelatives(cam, p=True)
                    if find_trans:
                        check_trans = cmds.objectType(find_trans[0])
                        if check_trans == 'transform':
                            cam_transform = find_trans[0]
                            break
                        else:
                            return False
                    else:
                        return False
                else:
                    for name in self.cameraNames:
                        if name in cam:
                            cmds.select(cam, r=True)
                            find_trans = cmds.listRelatives(cam, p=True)
                            if find_trans:
                                check_trans = cmds.objectType(find_trans[0])
                                if check_trans == 'transform':
                                    cam_transform = find_trans[0]
                                    break
                                else:
                                    return False
                            else:
                                return False
            else:
                for name in self.cameraNames:
                    if name in cam:
                        cmds.select(cam, r=True)
                        find_trans = cmds.listRelatives(cam, p=True)
                        if find_trans:
                            check_trans = cmds.objectType(find_trans[0])
                            if check_trans == 'transform':
                                cam_transform = find_trans[0]
                                break
                            else:
                                return False
                        else:
                            return False
        if cam_transform:
            cmds.select(cam_transform, r=True)
            # Unlock the camera
            for attr in self.cameraAttributes:
                cmds.setAttr(f'{cam_transform}.{attr}', lock=False)

            # Duplicate and bake
            if cam_transform and self.root_name not in cam_transform:
                new_cam_name = '%s_%s' % (self.root_name, cam_transform)
            else:
                new_cam_name = cam_transform
            cmds.duplicate(n='%s_baked' % new_cam_name)
            dup_cam = cmds.ls(sl=True)
            cmds.Unparent()
            cmds.select(cam_transform, r=True)
            cmds.select(dup_cam, tgl=True)
            do_constraint = cmds.parentConstraint(mo=True, weight=1)
            constraint = do_constraint[0]
            cmds.select(dup_cam, r=True)
            startFrame = cmds.playbackOptions(query=True, minTime=True)
            endFrame = cmds.playbackOptions(query=True, maxTime=True)
            cmds.bakeResults(dup_cam, sm=True, time=(startFrame, endFrame), sb=1, osr=1, dic=True, pok=True, sac=True,
                             rba=False, ral=False, bol=False, mr=True, cp=False, s=True)
            cmds.delete(constraint)

            # Relock the main cam
            for attr in self.cameraAttributes:
                cmds.setAttr(f'{cam_transform}.{attr}', lock=True)

            # Return the duplicate
            return dup_cam
        return False

    def closeEvent(self, event):
        self.settings.setValue('appendArtist', self.ui.AppendArtist.isChecked())
        # self.settings.setValue('showcode', self.ui.showCode.text())
        self.settings.setValue('bake_cam_scene_name', self.ui.bakeCamSceneName.isChecked())
        self.settings.setValue('geometry', self.saveGeometry())
        if len(self.recent_files) >= self.recent_file_count:
            self.recent_files.pop(self.recent_file_count - 1)
        this_file_data = {
            'filename': os.path.basename(self.current_file_path),
            'path': self.current_file_path
        }
        if this_file_data not in self.recent_files:
            self.recent_files.insert(0, this_file_data)
        self.settings.setValue('recent_files', self.recent_files)
        if len(self.recent_projects) >= 5:
            self.recent_projects.pop(4)
        current_project = cmds.workspace(q=True, act=True)
        if current_project not in self.recent_projects:
            self.recent_projects.insert(0, current_project)
        self.settings.setValue('recent_projects', self.recent_projects)
        self.settings.setValue('autosave', self.ui.autosaver.isChecked())
        self.settings.setValue('asset_shot', self.ui.assetShot_type.currentText())


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
    except Exception as e:
        app = QApplication.instance()
    saveas = super_saver()
    try:
        sys.exit(app.exec())
    except SystemExit as e:
        print('system exit code', e)
