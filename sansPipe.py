# Sans-Pipe Maya Light Pipeline Utility - MAYA 20xx +

"""
The SANS-PIPE LIGHT PIPELINE UTILITY is a pipeline-free versioning and saving system for Maya.
It is a stand-alone utility for quickly versioning up files and saving notes with them, publishing file, saving
Snapshots, Reference Tracking and overall scene settings.
The utility can be configured to open automatically when Maya opens, making opening of files and saving new files a
snap.
It saves notes and information with every file that is created.  It can also be used to build new projects, create
new assets and folder structures on the fly.
"""

"""
Version 1.3 Goals:
    1. Create a dynamically loading toolset:
        This would add buttons to the tools, menu and shelf based on tools added to either A) a sansPipe_tools.py script
        or B) by searching for and dynamically adding tools added to a bin folder.
                    2. Split all existing tools into a separate file that could be accessed either by the UI or by the shelf or menu.
                    3. Add Playblast record keeping, and perhaps organize playblasts into their own folder.
                        It would also be great if these could be played from a specific shot.
                    4. May want to add task folders to better organize how each section is delineated.
                        Scenes > Char > CharacterName > Model
                        Scenes > Char > CharacterName > LookDev
                        Scenes > Char > CharacterName > Rig
    5. Add some Project Level collection system.  
        This would go through the root project, look for database JSON files and output an Excel sheet that would list
        all existing projects and their current statuses.
                    6. Add task statuses.
                        This could be a really good one to add.
                    6.5. Add an "Add Note" button, or a feature that would request a note on task change, if it was triggered by the 
                        button.  This way a note would accompany a revision.  The system should probably archive the previous database 
                        entry with a flag of some sort (Filename_v001_RR1) or something like that, where RR# would be like saying 
                        "Revision Required Version 1" -> RR1.  Each version would get its own number RR2, RR3.
    7. UI enhancements (Related to some of the above):
                         a. Add Task Statuses
                         b. Add a Playblasts section to... somewhere.
        c. Add a reports section.
    8. Make the UI stay opened if references are out of date on a recently opened file
    9. Filtering on trees:
        Task filtering for both Existing File and Publishes. Only show Chars.  Only show Rigs
                    10. Rework #6 Task statuses.  Needs to be in the note and not a separate tag.  Each save as should have it's own 
                        note and be tallied up by that instead of an overall tag.
                    11. Add a "Blow away Snapshots" function for project cleanup.  The button would exist on the settings page, and 
                        there could also be a right-click context for individual elements
                    12. Rearrange the Tasks and Publishes.  Put publishes in their own folder either in the root of Scenes, or outside
                        of the scene folder.  TBD
    13. Move the system from a JSON database setup to a SQL database - either per asset - like the JSONs, or as a global
        database for everything.
    14. Make sure there are both Mac and Windows hotkeys
    15. Improve playblast settings.  Adjust what the viewport sees and try to put some burn-ins on there.
    16. Rework the Status notes to use the Notes window instead of the pop up.

"""

from maya import cmds
import maya.OpenMaya as om_old  # Old API for MObject
import maya.OpenMayaMPx as om_mpx  # Old API for MFnPlugin
import maya.api.OpenMaya as om  # New API for other operations

try:
    from PySide6.QtCore import (QCoreApplication, QMetaObject, QSize, Qt, QSettings, QTimer)
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    print('PySide6 detected.')
except ImportError:
    try:
        from PySide2.QtCore import (QCoreApplication, QMetaObject, QSize, Qt, QSettings, QTimer)
        from PySide2.QtWidgets import *
        from PySide2.QtGui import *
        print('PySide2 detected.')
    except ImportError:
        raise RuntimeError('Neither PySide 6 or PySide 2 detected!')
import os
import sys
import re
import json
import time
from datetime import datetime
import platform
import configparser
import csv
import inspect
import subprocess

import sp_tools as sptk
from ui import ui_superSaver_UI as ssui


def initializePlugin(mobject):
    mplugin = om_mpx.MFnPlugin(mobject)  # Use MFnPlugin from maya.OpenMayaMPx
    try:
        om.MGlobal.displayInfo("sansPipe plugin loaded")
    except:
        om.MGlobal.displayError("Failed to register sansPipe plugin")


def uninitializePlugin(mobject):
    mplugin = om_mpx.MFnPlugin(mobject)  # Use MFnPlugin from maya.OpenMayaMPx
    try:
        om.MGlobal.displayInfo("sansPipe plugin unloaded")
    except:
        om.MGlobal.displayError("Failed to deregister sansPipe plugin")


__version__ = '1.3.7'
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


class CustomMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Export Name')
        self.setText('What is the name of the object you are exporting?')
        self.text_input = QLineEdit(self)
        self.layout().addWidget(self.text_input, 1, 1)
        self.addButton(QMessageBox.Ok)
        self.addButton(QMessageBox.Cancel)
        self.button(QMessageBox.Ok).setEnabled(False)
        self.text_input.textChanged.connect(self.validate_input)

    def validate_input(self):
        if re.match(r'^\w+$', self.text_input.text()):
            self.button(QMessageBox.Ok).setEnabled(True)
        else:
            self.button(QMessageBox.Ok).setEnabled(False)

    def get_input(self):
        if self.exec() == QMessageBox.Ok:
            return self.text_input.text()
        return None

class CustomNotesBox(QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Status Update Note')
        self.setText('Why are you changing the status?  Leave a note!')
        self.text_input = QPlainTextEdit(self)
        self.layout().addWidget(self.text_input, 1, 1)
        self.addButton(QMessageBox.Ok)
        self.addButton(QMessageBox.Cancel)
        self.button(QMessageBox.Ok).setEnabled(False)
        self.text_input.textChanged.connect(self.validate_input)

    def validate_input(self):
        if len(self.text_input.toPlainText()) > 10:
            self.button(QMessageBox.Ok).setEnabled(True)
        else:
            self.button(QMessageBox.Ok).setEnabled(False)

    def get_input(self):
        if self.exec() == QMessageBox.Ok:
            return self.text_input.toPlainText()
        return None

class sansPipe(QWidget):
    """
    Main SansPipe utility.  This class runs all the functions of the SansPipe utility.
    """
    def __init__(self, parent=None):
        """
        Initialize the tool.  This runs all the basic setup and has most of the functionality created here.
        :param parent:
        """
        # Initialize the QWidget
        QWidget.__init__(self, parent)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.pattern = r'(_v\d+)|(_V\d+)'

        # Initialize the root and task variables
        self.root_name = None
        self.task = None

        # Initialize plug-in path settings
        plugin_name = 'sansPipe'
        plugin_path = cmds.pluginInfo(plugin_name, query=True, path=True)
        self.plugin_folder = os.path.dirname(plugin_path)
        self.icons = os.path.join(self.plugin_folder, 'icons')

        # Initialize the UI
        self.ui = ssui.Ui_SaveAs()
        self.ui.setupUi(self)

        # Get basic scene information - File path, Workspace, Scene and Asset folders.
        pth = cmds.file(q=True, sn=True)
        self.current_file_path = pth
        workspace = cmds.workspace(q=True, rd=True)
        self.workspace = workspace
        scene_folder = cmds.workspace(fre='scene')
        self.scene_folder_path = os.path.join(workspace, scene_folder)
        publish_folder = cmds.workspace(fre='publish')
        self.publish_folder_path = os.path.join(workspace, publish_folder)
        asset_folder = cmds.workspace(fre='templates')
        self.asset_folder_path = os.path.join(workspace, asset_folder)

        # Set window title
        self.setWindowTitle('SansPipe Light Pipeline Utility - v%s' % __version__)

        # Check for and load config file.  Build one if it does not exist.
        self.config_path = os.path.join(workspace, 'show_config.cfg')
        if not os.path.exists(self.config_path):
            self.build_config_file(path=self.config_path)

        # Get Global Variables from JSON
        current_file_path = inspect.getfile(inspect.currentframe())
        plugin_dir = os.path.dirname(os.path.abspath(current_file_path))
        sp_global_vars = os.path.join(plugin_dir, 'sp_global_vars.json')
        if os.path.exists(sp_global_vars):
            with open(sp_global_vars, 'r') as global_vars:
                globVars = json.load(global_vars)
        else:
            cmds.error('Cannot open the sp_global_vars db')
            globVars = {'tasks': None, 'invalidCharacter': None, 'cameraNames': None, 'cameraAttributes': None,
                        'asset_tasks': None, 'shot_tasks': None }
        # Set the project constants.
        self.tasks = globVars['tasks']
        self.invalidCharacters = globVars['invalidCharacters']
        self.cameraNames = globVars['cameraNames']
        self.cameraAttributes = globVars['cameraAttributes']
        self.asset_tasks = globVars['asset_tasks']
        self.shot_tasks = globVars['shot_tasks']

        # Set initial artist field
        artist = os.environ[env_user]
        first_initials = artist[0:2]
        first_initials = first_initials.upper()
        last_name = artist[2:]
        artist = first_initials + last_name
        self.ui.artistName.setText(artist)

        # Create the QSettings for information storage.  This information gets accessed by the userSetup.py as well.
        self.settings = QSettings(__author__, 'Sans Pipe Super Saver')
        self.position = self.settings.value('geometry', None)
        self.appendartist = self.settings.value('appendArtist', None, type=bool)
        self.recent_files = self.settings.value('recent_files', [], type=list)
        self.recent_projects = self.settings.value('recent_projects', [], type=list)
        self.bakeCamSceneName = self.settings.value('bake_cam_scene_name', None, type=bool)
        self.autosave = self.settings.value('autosave', None, type=bool)
        self.asset_shot_type = self.settings.value('asset_shot', None, type=str)
        self.render_output = self.settings.value('render_output', None, type=str)
        self.auto_load_on_startup = self.settings.value('autoload', None, type=bool)
        self.artist = self.settings.value('artist_name', None, type=str)
        self.restoreGeometry(self.position)

        # Create SP Tool Kit
        self.sptk = sptk.sp_toolkit()

        # Populate the Recent Files list
        if self.recent_files:
            self.populate_recent_files()
        else:
            self.recent_files = []

        # Populate the recent projects list
        if self.recent_projects:
            self.populate_recent_projects()
        else:
            self.recent_projects = []

        # Set the boolean checkboxes
        self.ui.AppendArtist.setChecked(self.appendartist)
        self.ui.bakeCamSceneName.setChecked(self.bakeCamSceneName)
        self.ui.autosaver.setChecked(self.autosave)
        self.ui.assetShot_type.setCurrentText(self.asset_shot_type)
        self.ui.image_format.setCurrentText(self.render_output)
        self.ui.autoload.setChecked(self.auto_load_on_startup)

        # Check Autosave Settings
        self.set_autosave()

        # Get the configurations from the show_config.cfg file.
        config = configparser.ConfigParser()
        config.read(self.config_path)
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

        # Set the fields for the Settings tab from the config file.
        self.ui.showName.setText(self.project_name)
        self.ui.resolutionWidth.setText(self.res_width)
        self.ui.resolutionHeight.setText(self.res_height)
        self.ui.filmback_width.setText(self.filmback_width)
        self.ui.filmback_height.setText(self.filmback_height)
        self.ui.sceneScale.setText(self.scene_scale)
        self.ui.recent_file_count.setValue(self.recent_file_count)
        self.ui.autosave_count.setValue(self.autosave_interval)

        # Populate the project settings
        self.populate_project_settings()

        # Check for an existing path, and if it's not set, use the workspace path instead.
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
            base_filename = 'default'
            save_file = self.format_name(basename=base_filename)
            v_len = 3
            extension = 'ma'
            v_type = '_v'

        # Set the filename, which is a misnomer.  This is actually the asset or shot root name, not including the show
        # code or the version name, et cetera.
        self.ui.filename.setText(self.root_name)

        # Set the default UI message to nothing.
        self.ui.messages.setText('')

        # Set up the task statuses
        task_statuses = self.ui.taskStatus
        model = QStandardItemModel()

        # Add the drop-down items
        self.add_colored_item(task_statuses, model, '-')
        self.add_colored_item(task_statuses, model, 'Ready', 'black', 'ghostwhite')
        self.add_colored_item(task_statuses, model, 'Waiting', 'darkorchid', 'lavender')
        self.add_colored_item(task_statuses, model, 'Needs Revision', 'brown', 'orange')
        self.add_colored_item(task_statuses, model, 'In Progress', 'darkblue', 'lightskyblue')
        self.add_colored_item(task_statuses, model, 'For Review', 'darkcyan', 'lightyellow')
        self.add_colored_item(task_statuses, model, 'Done', 'darkgreen', 'palegreen')
        self.add_colored_item(task_statuses, model, 'Omit', 'red', 'black')
        task_statuses.setModel(model)

        # Set the top level color of the drop-down box.
        self.ui.taskStatus.currentIndexChanged.connect(self.status_changed)

        # Get the probable name of the next file to be saved.  Either from the project settings or the currently opened
        # file.  Use this to set the version number.
        get_save = self.get_save_file(save_file=save_file, save_path=save_path, basename=base_filename, _v=v_type,
                                      l=v_len, ext=extension)
        next_version = get_save[1]

        self.ui.version.setValue(next_version)

        # Create the file output path for the next save function.
        new_path = self.build_path(path=save_path, rootName=self.root_name, task=self.task, v_type=v_type,
                                   v_len=v_len, version=next_version, ext=extension, show=show_code, artist=artist)

        self.ui.output_filename.setText(new_path)

        # Set the folder save path.
        self.ui.folder.setText(save_path)

        # Hide the overwrite function since it currently does nothing and isn't necessarily needed.
        self.ui.overwrite.hide()
        self.ui.existing_notes.setReadOnly(True)

        # Start connecting list functionality to their appropriate functions.
        self.ui.existingFile_list.setHeaderHidden(True)
        self.ui.assetTree.setHeaderHidden(True)
        self.ui.snapshots.setHeaderHidden(True)
        self.ui.snapshots.itemDoubleClicked.connect(self.import_snapshot)
        self.ui.existingFile_list.itemDoubleClicked.connect(lambda: self.open_file(f=False))
        self.ui.existingFile_list.itemClicked.connect(self.show_file_selection_info)
        self.populate_existing_files(current_directory=self.scene_folder_path)
        self.populate_publish_assets(tree=self.ui.assetTree, root=self.ui.assets.text(),
                                     current_directory=self.asset_folder_path)
        self.populate_publish_assets(tree=self.ui.publishes_tree, root=self.ui.publish.text(),
                                     current_directory=self.publish_folder_path)
        self.ui.recentFilesList.itemDoubleClicked.connect(lambda: self.open_recent_file(f=False))
        self.ui.recent_projects.itemDoubleClicked.connect(lambda: self.set_project(btn=False))
        self.ui.set_proejct_btn.clicked.connect(lambda: self.set_project(btn=True))
        self.ui.new_project_folder_btn.clicked.connect(self.get_project_folder)
        self.reference_tracker()

        self.set_custom()

        # CONNECT BUTTONS
        self.ui.customNaming.clicked.connect(self.set_custom)
        self.ui.autoNaming.clicked.connect(self.set_custom)
        self.ui.cancel_btn.clicked.connect(self.close)
        self.ui.snap_btn.clicked.connect(self.snapshot)
        self.check_button_state(btn=self.ui.snap_btn)
        self.ui.publish_btn.clicked.connect(self.publish)
        self.check_button_state(btn=self.ui.publish_btn)
        self.ui.load_btn.clicked.connect(lambda: self.load_ref(element=self.ui.existingFile_list))
        self.ui.bakeCam_btn.clicked.connect(self.run_cam_bake)
        self.ui.import_btn.clicked.connect(lambda: self.import_object(element=self.ui.existingFile_list))
        self.ui.import_2_btn.clicked.connect(lambda: self.import_object(element=self.ui.assetTree))
        self.ui.loadRef_2_btn.clicked.connect(lambda: self.load_ref(element=self.ui.assetTree))
        self.ui.import_3_btn.clicked.connect(lambda: self.import_object(element=self.ui.publishes_tree))
        self.ui.loadRef_3_btn.clicked.connect(lambda: self.load_ref(element=self.ui.publishes_tree))
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
        self.ui.load_btn.hide()
        self.ui.load_btn.setStyleSheet(
            'color: rgb(140, 140, 140);'
        )
        self.ui.import_btn.setEnabled(False)
        self.ui.import_btn.hide()
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
        self.ui.fbxPub_btn.clicked.connect(lambda: self.export_selection(export_type='FBX export'))
        self.ui.objPub_btn.clicked.connect(lambda: self.export_selection(export_type='OBJexport'))
        self.ui.abcPub_btn.clicked.connect(lambda: self.export_selection(export_type='abc'))
        self.check_button_state(btn=self.ui.fbxPub_btn)
        self.check_button_state(btn=self.ui.objPub_btn)
        self.check_button_state(btn=self.ui.abcPub_btn)
        self.check_button_state(btn=self.ui.playblast_btn)
        self.check_button_state(btn=self.ui.bakeCam_btn)
        # self.check_button_state(btn=self.ui.build_folders_btn)
        self.ui.playblast_btn.clicked.connect(self.playblast)
        self.ui.createCam_btn.clicked.connect(self.create_camera)
        self.ui.bulk_add_btn.clicked.connect(self.get_csv)
        self.ui.blowAwaySnaps_btn.clicked.connect(self.blow_away_snaps)

        # Set the font for the Tools Group.
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        self.ui.toolsGroup.setFont(title_font)

        # SETUP HOTKEYS
        self.shortcut_save = QShortcut(QKeySequence('Ctrl+Return'), self)
        self.shortcut_save.activated.connect(self.run)
        self.shortcut_exit = QShortcut(QKeySequence('Esc'), self)
        self.shortcut_exit.activated.connect(self.close)
        self.shortcut_publish = QShortcut(QKeySequence('Ctrl+p'), self)
        self.shortcut_publish.activated.connect(self.publish)
        self.shortcut_snapshot = QShortcut(QKeySequence('Ctrl+t'), self)
        self.shortcut_snapshot.activated.connect(self.snapshot)

        # SETUP RIGHT-CLICK CONTEXT MENUS
        self.enable_context_menu(self.ui.existingFile_list, 'Existing Files')
        self.enable_context_menu(self.ui.assetTree, 'Assets')
        self.enable_context_menu(self.ui.publishes_tree, 'Publishes')

        # Set Scene Settings
        try:
            self.render_settings()
        except RuntimeError as e:
            cmds.warning(f'Cannot load render settings: {e}')

        # Load up and show the UI.
        self.show()

    def enable_context_menu(self, widget=None, widget_name=None):
        """
        This function sets the Right-Click functionality for whichever list is run through it, allowing for the context
        menu to appear when a right-click is activated.
        :param widget: The UI element that is being enabled.
        :param widget_name: The name of the UI widget.
        :return:
        """
        if widget and widget_name:
            widget.setContextMenuPolicy(Qt.CustomContextMenu)
            widget.customContextMenuRequested.connect(lambda position: self.create_tree_context_menu(widget,
                                                                                                     widget_name,
                                                                                                     position))

    def add_colored_item(self, task_statuses, model, text, text_color=None, background_color=None):
        """
        This populates the Task Status drop-down list with colors
        :param task_statuses: self.ui.taskStatus
        :param text: The Dropdown selection text
        :param text_color: the color of the text
        :param background_color: the background color of the drop-down item
        :return:
        """
        item = QStandardItem(text)
        if text_color:
            item.setForeground(QColor(text_color))
        if background_color:
            item.setBackground(QColor(background_color))
        model.appendRow(item)

    def status_changed(self, status=None):
        """
        This updates the stylesheet of the top level of the taskStatus drop-down menu
        :return:
        """
        selected_index = self.ui.taskStatus.currentIndex()
        background_color = 'dimgrey'
        text_color = 'gainsboro'
        default_text_color = text_color
        default_background_color = background_color

        if selected_index == 0:
            text_color = default_text_color
            background_color = default_background_color
        elif selected_index == 1 or status == 'Ready':
            text_color = 'black'
            background_color = 'ghostwhite'
        elif selected_index == 2 or status == 'Waiting':
            text_color = 'darkorchid'
            background_color = 'lavender'
        elif selected_index == 3 or status == 'Needs Revision':
            text_color = 'brown'
            background_color = 'orange'
        elif selected_index == 4 or status == 'In Progress':
            text_color = 'darkblue'
            background_color = 'lightskyblue'
        elif selected_index == 5 or status == 'For Review':
            text_color = 'darkcyan'
            background_color = 'lightyellow'
        elif selected_index == 6 or status == 'Done':
            text_color = 'darkgreen'
            background_color = 'palegreen'
        elif selected_index == 7 or status == 'Omit':
            text_color = 'red'
            background_color = 'black'
        self.ui.taskStatus.setEditable(True)
        line_edit = self.ui.taskStatus.lineEdit()
        self.ui.taskStatus.setStyleSheet(f"""
QComboBox {{
    color: {text_color};
    background-color: {background_color};
}} 
""")
        line_edit.setReadOnly(True)
        self.change_task_status()

    def change_task_status(self):
        selected_file = self.ui.existingFile_list.selectedItems()
        current_status = self.ui.taskStatus.currentText()

        if selected_file:
            selected_file = selected_file[0]
            data = selected_file.data(0, Qt.UserRole)
            folder = data['folder']
            filename = data['file']

            path = folder
            path = path.replace('\\', '/')
            # path = os.path.dirname(path)
            db_path = os.path.join(path, 'db')
            file_path = os.path.join(folder, filename)
            try:
                get_db = self.open_db(db_path)
                notes = get_db['Notes']
                if filename:
                    found_note = False
                    for note in notes:
                        if filename == note['filename']:
                            if 'status' in note.keys():
                                status = note['status']
                                if status != current_status:
                                    self.hide()
                                    pop_note = self.pop_up_note()
                                    self.show()
                                    self.create_note(notes=pop_note, output_file=file_path, status=current_status,
                                                     task_note=True)
                            else:
                                self.hide()
                                pop_note = self.pop_up_note()
                                self.show()
                                self.create_note(notes=pop_note, output_file=file_path, status=current_status,
                                                 task_note=True)
                            found_note = True
                            break

                    # Create note if none found
                    if not found_note:
                        self.hide()
                        pop_note = self.pop_up_note()
                        self.show()
                        self.create_note(notes=pop_note, output_file=file_path, status=current_status, task_note=True)
                else:
                    note = notes[-1]
                    if 'status' in note.keys():
                        status = note['status']
                        if status != current_status:
                            self.hide()
                            pop_note = self.pop_up_note()
                            self.show()
                            self.create_note(notes=pop_note, output_file=path, status=current_status, task_note=True)
                    else:
                        self.hide()
                        pop_note = self.pop_up_note()
                        self.show()
                        self.create_note(notes=pop_note, output_file=path, status=current_status, task_note=True)
                #
                # self.update_ui()
                # self.populate_existing_files(current_directory=self.scene_folder_path)
            except RuntimeError as e:
                cmds.warning(f'Cannot open this database: {path}, {e}')

    def get_item_status(self, folder=None, filename=None):
        """
        This method looks for a current status to set it on the tree.
        :param folder:
        :param filename:
        :return:
        """

        status = '-'
        if folder:

            db_folder = os.path.join(folder, 'db')
            if os.path.exists(db_folder):
                data = self.open_db(db_folder)
                notes = data['Notes']

                if notes and not filename:

                    last_note = notes[-1]

                    if type(last_note) == dict and 'status' in last_note.keys():

                        status = last_note['status']

                elif notes and filename:

                    for note in notes:
                        if filename == note['filename']:

                            if type(note) == dict and 'status' in note.keys():

                                status = note['status']

                            break
        return status

    def set_item_status(self, status=None):
        if status:
            if status == 'Ready':
                return 'black', 'ghostwhite'
            elif status == 'Waiting':
                return 'darkorchid', 'lavender'
            elif status == 'Needs Revision':
                return 'brown', 'orange'
            elif status == 'In Progress':
                return 'darkblue', 'lightskyblue'
            elif status == 'For Review':
                return 'darkcyan', 'lightyellow'
            elif status == 'Done':
                return 'darkgreen', 'palegreen'
            elif status == 'Omit':
                return 'red', 'black'
            else:
                return 'gainsporo', 'dimgrey'

    def create_tree_context_menu(self, widget, widget_name, position):
        """
        Creates the actual context menu and sets the function for what to do when it is triggered
        :param widget: The UI widget being activated
        :param widget_name: The name of the UI widget - currently not used here.
        :param position: The mouse position for the context menu
        :return:
        """
        # Get the mouse position
        current_item = widget.itemAt(position)
        if not current_item:
            return False

        # Collect data from the context.  If none exists do not show the context menu.
        data = current_item.data(0, Qt.UserRole)
        if not data['file']:
            return False

        # Create the context menu
        context_menu = QMenu(self)

        # Make the settings
        open_action = QAction('Open', self)
        ref_action = QAction('Reference', self)
        import_action = QAction('Import', self)
        playblast_action = QAction('View Playblast', self)
        delete_snapshots = QAction('Blow Away Snapshots', self)

        # Setup the trigger actions.
        open_action.triggered.connect(lambda: self.open_file(f=False))
        ref_action.triggered.connect(lambda: self.load_ref(element=widget))
        import_action.triggered.connect(lambda: self.import_object(element=widget))
        playblast_action.triggered.connect(lambda: self.playblast_player(element=widget))
        delete_snapshots.triggered.connect(lambda: self.blow_away_snaps(element=widget))

        if widget == self.ui.existingFile_list:
            context_menu.addAction(open_action)
            context_menu.addAction(playblast_action)
            context_menu.addSeparator()
            context_menu.addAction(delete_snapshots)
        else:
            context_menu.addAction(ref_action)
            context_menu.addAction(import_action)

        context_menu.exec(widget.mapToGlobal(position))

    def open_file(self, f=False):
        """
        This opens a file on a double click or button press
        :param f: Whether the file open command should force the file to open.
        :return:
        """
        # Get the item currently selected in the Existing File list
        current_item = self.ui.existingFile_list.currentItem()
        if current_item:
            # Collect the data
            file_info = current_item.data(0, Qt.UserRole)
            if file_info:
                folder = file_info['folder']
                filename = file_info['file']
                open_file = os.path.join(folder, filename)
                try:
                    self.hide()
                    cmds.file(open_file, o=True, f=f)
                    self.current_file_path = open_file
                    self.create_note(output_file=open_file, status='In Progress')
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
                        self.create_note(output_file=open_file, status='In Progress')
                    elif ret == QMessageBox.No:
                        self.open_file(f=True)
                        self.create_note(output_file=open_file, status='In Progress')
                    else:
                        self.show()

    def format_name(self, basename=None, _v='_v', v=1, l=3, ext='ma'):
        """
        Creates the proper naming format for a save function
        :param basename: The root name of the asset or shot
        :param _v: The version tag, as in _v001
        :param v: The version number
        :param l: The length of the version number, the default is 3
        :param ext: The extention of the filename
        :return:
        """
        if basename:
            save_file = '{basename}{_v}{v:0{l}d}.{ext}'.format(basename=basename, _v=_v, v=v, l=l, ext=ext)
            return save_file
        return False

    def reset_version(self, v=1):
        """
        Resets the version number when called.  The default is 1, but can be sent a "latest" version number.
        :param v: Version number being sent.
        :return:
        """
        self.ui.version.valueChanged.disconnect(self.update_ui)
        self.ui.version.setValue(v)
        self.update_ui()
        self.ui.version.valueChanged.connect(self.update_ui)

    def clear_recent_files(self):
        """
        This clears out the recently opened files list.  It has no effect on Maya's default "Recently Opened >" list.
        :return:
        """
        self.ui.recentFilesList.clear()
        self.recent_files = []
        self.populate_recent_files()

    def remove_bad_characters(self):
        """
        Cleans up and replaces bad characters with underscores '_'
        :return:
        """
        root_name = self.ui.filename.text()
        bad_x = [x for x in self.invalidCharacters if x in root_name]
        if bad_x:
            bad_x = bad_x[0]
            root_name = root_name.replace(bad_x, '_')
            self.ui.filename.setText(root_name)

    def build_config_file(self, path=None):
        """
        This method creates the initial configuration file if none exists.  It is necessary for SansPipe to operate.
        If it is deleted, a new one should be created on startup.
        :param path: The path where the config file should be created.  The project root by default.
        :return:
        """
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
        """
        This method tries to find a show code in the main path attempting to see if the user already created it from
        their initial project creation.  Some shows automatically put 3-letter codes in their root path.  If none can
        be found, then it creates a 3-letter code from the project name itself.
        :param path: Root path for the project
        :return:
        """
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
        """
        Attempts to get the project name from the path.  This should always work.
        :return:
        """
        workspace = cmds.workspace(q=True, act=True)
        workspace = workspace.replace('\\', '/')
        split_ws = workspace.split('/')
        self.project_name = split_ws[-1]
        return self.project_name

    def save_config(self):
        """
        Saves the configuration file when called by the user.
        :return:
        """
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

    def update_ui(self):
        """
        Really, this creates a new output filename path from the data updated in the UI
        :return:
        """
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
        """
        Gets and parses out the Root name, task name and other information from the filename
        :param filename:
        :return:
        """
        try:
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
                                root_name = root_name.lstrip('_')
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
        except TypeError as e:
            cmds.warning(f'Could not get root and task! {e}')

    def set_custom(self):
        """
        Switches the UI from automatic naming to custom naming setup
        :return:
        """
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
        """
        This function builds the proper path and filename for an object
        :param path: The base path, usually starts with the Maya project scene file.
        :param rootName: The name of the asset or shot
        :param task: Kind of task
        :param v_type: How the version number is parsed, usually '_v'
        :param v_len: The number of zeros in the version number.  Usually 3
        :param version: The version number
        :param ext: The file extention
        :param show: The 3-letter show code
        :param artist: The artist name - First initial and Last name
        :return:
        """
        output_path = None
        if path and rootName and ext:
            try:
                if rootName.startswith(show):
                    show = ''
            except TypeError as e:
                cmds.warning('ERROR: %s' % e)
                show = ''

            if not show.endswith('_'):
                show = f'{show}_'
            elif show.startswith('_'):
                show = show.lstrip('_')
            if task:
                # FIXME: Adding the task path here is problematic.  NOTE: Why?  Why did I leave this note?
                all_tasks = self.shot_tasks + self.asset_tasks
                for task_type in all_tasks:
                    if task_type in path and task not in path:
                        path = path.replace(task_type, task)
                        break
                if task not in path:
                    path = os.path.join(path, task)
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

            output_path = os.path.join(path, filename)
            if '\\' in output_path:
                output_path = output_path.replace('\\', '/')
        return output_path

    def get_folder(self):
        """
        This method simply gets the folder path for a custom file name
        :return:
        """
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
        """
        This method finds the next available version number and filename for a file based on the task and folder.
        :param save_file: The current filename
        :param save_path: Path to the filename
        :param basename: The root name of the asset or shot
        :param _v: The format of the version separator
        :param v: Version number
        :param l: Number of zeros in the version
        :param ext: File extension
        :return:
        """
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
        """
        This method parses out the data of a file based on the filename.  It can be used to repopulate the UI
        :param filename: Filename being parsed
        :param default_len: Number of zeros in the version number
        :param default_version: Version number
        :return:
        """
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
        """
        Check to see if a file is the latest version number
        :param filename: File being tested
        :return:
        """
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
        """
        Gets a list of files within a folder
        :param path: Folder being looked at.
        :return:
        """
        files = []
        if path:
            if os.path.exists(path):
                list_files = os.listdir(path)
                for f in list_files:
                    if os.path.isfile(os.path.join(path, f)):
                        files.append(f)
            else:
                os.makedirs(path)
        return files

    def make_db_folder(self, folder=None):
        """
        Creates a db folder to store a local JSON database file
        :param folder:
        :return:
        """
        db_folder = None
        if folder:
            db_folder = os.path.join(folder, 'db')
            if not os.path.exists(db_folder):
                os.makedirs(db_folder)
        return db_folder

    def create_db(self, folder=None):
        """
        Creates a blank notes database for a particular folder
        :param folder:
        :return:
        """
        if folder:
            if not os.path.exists(folder):
                data = {
                    "Notes": [],
                    "Status": None
                }
                save_data = json.dumps(data, indent=4)
                with open(folder, 'w+') as save:
                    save.write(save_data)
                    save.close()

    def open_db(self, folder=None):
        """
        Opens a database file for a particular folder
        :param folder: The root folder for the asset/shot in question
        :return:
        """
        notes_db = None
        try:
            if folder:
                notes_db_file = os.path.join(folder, 'notes_db.json')
                if not os.path.exists(notes_db_file):
                    # create an empty file
                    self.create_db(folder=notes_db_file)
                with open(notes_db_file, 'r') as open_notes:
                    notes_db = json.load(open_notes)
                    open_notes.close()
        except RuntimeError as e:
            cmds.warning(f'Unable to open {notes_db_file} because {e}')
        return notes_db

    def save_db(self, folder=None, data=None):
        """
        Saves the database for a particular folder
        :param folder: The folder for the asset or shot in question
        :param data: The data being added to the database.
        :return:
        """
        if data and folder:
            notes_file = os.path.join(folder, 'notes_db.json')
            save_data = json.dumps(data, indent=4)
            with open(notes_file, 'w') as save:
                save.write(save_data)
                save.close()

    def create_note(self, notes=None, output_file=None, status=None, task_note=False):
        """
        Creates a new note for a project asset or shot
        :param notes: The note being added to the database.
        :param output_file: The output file from which to parse the data and determine where to send the note.
        :param status: The status of the note being said.
        :return:
        """
        """
        FIXME: I'm adding task_note=False to add some functionality so that it can process task revisions with notes.
        """
        try:
            if os.path.isfile(output_file):
                path = os.path.dirname(output_file)
                file_name = os.path.basename(output_file)
            elif os.path.isdir(output_file):
                path = output_file
                file_name = None
            else:
                path = output_file
                file_name = None

            if notes and output_file and not task_note:
                notes_path = self.make_db_folder(folder=path)
                notes_db = self.open_db(folder=notes_path)
                if not os.path.exists(path):
                    os.makedirs(path)
                self.message(text='Writing Notes...', ok=True)
                if not status:
                    # FIXME: I'm unsure at this juncture if this should auto-set to "In Progress"
                    status = 'In Progress'
                date_now = datetime.now()
                date = '{d} | {t}'.format(d=date_now.date(), t=date_now.time())
                new_note = {
                    'filename': file_name,
                    'user': os.environ[env_user],
                    'computer': os.environ[computername],
                    'date': date,
                    'status': status,
                    'details': notes
                }

                update = False
                for note in notes_db['Notes']:
                    if note['filename'] == file_name:
                        note.update(new_note)
                        update = True
                        break
                if not update:
                    notes_db['Notes'].append(new_note)

                self.save_db(folder=notes_path, data=notes_db)
                self.message(text='Saved Successfully!!', ok=True)
            elif status and output_file and not notes and not task_note:
                notes_path = self.make_db_folder(folder=path)
                notes_db = self.open_db(folder=notes_path)
                if not os.path.exists(path):
                    os.makedirs(path)

                date_now = datetime.now()
                date = '{d} | {t}'.format(d=date_now.date(), t=date_now.time())
                notes = 'Status update'

                update = False
                for note in notes_db['Notes']:
                    if note['filename'] == file_name:
                        new_note = {
                            'user': os.environ[env_user],
                            'computer': os.environ[computername],
                            'date': date,
                            'status': status
                        }

                        note.update(new_note)
                        update = True
                        break
                if not update:
                    new_note = {
                        'filename': file_name,
                        'user': os.environ[env_user],
                        'computer': os.environ[computername],
                        'date': date,
                        'status': status,
                        'details': notes
                    }
                    notes_db['Notes'].append(new_note)

                self.save_db(folder=notes_path, data=notes_db)
                self.message(text='Status updated', ok=True)
            elif notes and output_file and status and task_note:
                notes_path = self.make_db_folder(folder=path)
                notes_db = self.open_db(folder=notes_path)
                # NOTE: I'm not sure if os.path.exists(path) is the right path to look at.  Double check this
                if not os.path.exists(path):
                    os.makedirs(path)

                date_now = datetime.now()
                date = '{d} | {t}'.format(d=date_now.date(), t=date_now.time())

                update = False
                for note in notes_db['Notes']:
                    if note['filename'] == file_name:
                        update = True
                        original_notes = note['details']
                        update_notes = f"""ORIGINAL NOTE BY: {note['user']}:
{original_notes}
on: {note['date']}

STATUS REPLY:
{notes}
"""
                        new_note = {
                            'user': os.environ[env_user],
                            'computer': os.environ[computername],
                            'date': date,
                            'details': update_notes,
                            'status': status
                        }

                        note.update(new_note)
                        break
                if not update:
                    new_note = {
                        'filename': file_name,
                        'user': os.environ[env_user],
                        'computer': os.environ[computername],
                        'date': date,
                        'details': notes,
                        'status': status
                    }
                    notes_db['Notes'].append(new_note)
                self.save_db(folder=notes_path, data=notes_db)
                self.message(text='Status Updated', ok=True)
            else:
                return False
        except RuntimeError as e:
            cmds.warning(f'Unable to create note for {notes_path} because {e}')

    def create_camera(self):
        """
        Creates a new camera using the film back and scene scale settings from the UI.  Asks for a focal length.
        :return:
        """
        self.hide()
        create_cam = self.sptk.create_camera()
        self.show()
        if create_cam:
            self.message(text=f'{create_cam} Camera created', ok=True)
        else:
            self.message(text='Unable to create camera!', ok=False)

    def playblast_player(self, element=None):
        if element:
            current_item = element.currentItem()
            data = current_item.data(0, Qt.UserRole)
            if data:
                filename = data['file']
                if filename:
                    get_root_name = os.path.splitext(filename)
                    root_name = get_root_name[0]
                    root_path = cmds.workspace(q=True, rd=True)
                    movies_folder = cmds.workspace(fre='movie')
                    movie_path = os.path.join(root_path, movies_folder)
                    if os.path.exists(movie_path):
                        movie_filename = root_name + '.mov'
                        movie_file = os.path.join(movie_path, movie_filename)
                        if os.path.exists(movie_file):
                            try:
                                self.message(text=f'Playing movie {movie_file}', ok=True)
                                if platform.system() == 'Windows':
                                    subprocess.run(['start', '', movie_file], shell=True)
                                else:
                                    subprocess.run(['open', movie_file])
                            except Exception as e:
                                self.message(text=f'The movie {movie_file} could not be played', ok=False)
                                cmds.warning(f'Unable to open the file {movie_file}')
                        else:
                            self.message(text=f'Playblast could not be found for {movie_file}', ok=False)

    def blow_away_snaps(self, element=None):
        if element:
            current_item = element.currentItem()
            data = current_item.data(0, Qt.UserRole)
            folder = data['folder']
        else:
            folder = None
        self.hide()
        blow_away = self.sptk.blow_away_snapshots(folder=folder)
        self.show()
        if blow_away:
            self.message(text='Snapshots have been erased.', ok=True)
        else:
            self.message(text='Unable to remove snapshots', ok=False)

    def show_file_selection_info(self, item, column):
        """
        This function does a few things.  It checks to see what object is selected in the Existing file list, and if
        it is a legitimate file than it reads and posts a note in the notes output window.  Otherwise, it posts a blank
        note.  It also checks button states for the Load Ref and Import buttons and makes sure they are only active
        when an asset or Published item is selected.  This functionality has actually been removed from the UI, but
        the pieces still exist, they're just hidden.  That functionality has been moved to the Publishes/Assets tab.
        :param item:
        :param column:
        :return:
        """
        # Load selection info
        try:
            file_info = item.data(0, Qt.UserRole)
        except AttributeError as e:
            item = self.ui.existingFile_list.currentItem()
            file_info = item.data(0, Qt.UserRole)
        file_text = item.text(0)
        if file_info:
            folder_name = file_info['folder']
            filename = file_info['file']
            folder = self.make_db_folder(folder_name)
            notes_db = self.open_db(folder=folder)
            if not notes_db:
                return False
            post_note = """FILE: {fn}
USER: None
COMP: None
DATE: None
STATUS: -

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
                        if 'status' in note.keys():
                            status = note['status']
                        else:
                            status = '-'

                        # Set pretty date
                        d_date = datetime.strptime(date, '%Y-%m-%d | %H:%M:%S.%f')
                        date = d_date.strftime('%m/%d/%Y - %I:%M:%S%p')

                        post_note = """FILE: {filename}
USER: {user}
COMP: {computer}
DATE: {date}
STATUS: {status}

NOTE: {details}""".format(filename=filename, user=user, computer=computer, date=date, status=status, details=details)

                        if status and status != '-':
                            self.ui.taskStatus.blockSignals(True)
                            self.ui.taskStatus.setCurrentText(status)
                            self.ui.taskStatus.blockSignals(False)
                            self.status_changed(status)
                            QApplication.processEvents()
                        else:
                            self.ui.taskStatus.blockSignals(True)
                            self.ui.taskStatus.setCurrentText('-')
                            self.ui.taskStatus.blockSignals(False)
                            self.status_changed(status)
                            QApplication.processEvents()
                        break

            self.ui.existing_notes.setText(post_note)
            self.populate_snapshots(item, column)
            self.ui.snapshots.scrollToBottom()

    def populate_existing_files(self, current_directory=None):
        """
        This function populates the existing files list based on the folder structure and files found within.
        :param current_directory: Usually the root scenes directory for a project.
        :return:
        """
        self.ui.existingFile_list.clear()
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
                        status = self.get_item_status(folder=folder_name)
                        if status:
                            colors = self.set_item_status(status=status)
                            fg = colors[0]
                            bg = colors[1]
                            folder_item.setForeground(0, QColor(fg))
                            folder_item.setBackground(0, QColor(bg))
                        folder_items[relative_folder_name] = folder_item
                        if relative_folder_name == ".":
                            folder_items[relative_folder_name].setExpanded(True)

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
                            status = self.get_item_status(folder=folder_name)
                            if status:
                                colors = self.set_item_status(status=status)
                                fg = colors[0]
                                bg = colors[1]
                                subfolder_item.setForeground(0, QColor(fg))
                                subfolder_item.setBackground(0, QColor(bg))
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
                        status = self.get_item_status(folder=folder_name, filename=file_name)
                        if status:
                            colors = self.set_item_status(status=status)
                            fg = colors[0]
                            bg = colors[1]
                            file_item.setForeground(0, QColor(fg))
                            file_item.setBackground(0, QColor(bg))

                        movie_filename = file_name.replace('.ma', '.mov')
                        movie_filename = movie_filename.replace('.mb', '.mov')
                        movie_folder = cmds.workspace(fre='movie')
                        movie_path = os.path.join(self.workspace, movie_folder)
                        movie_file = os.path.join(movie_path, movie_filename)
                        if os.path.exists(movie_file):
                            icon_path = os.path.join(self.icons, 'cam_icon.png')
                            icon = QIcon(icon_path)
                            file_item.setIcon(0, icon)

                        # Highlight the currently opened file
                        if file_path == self.current_file_path:
                            file_item.setSelected(True)
                            folder_items[relative_folder_name].setExpanded(True)
                            self.ui.existingFile_list.scrollToItem(file_item)
                            self.ui.existingFile_list.itemClicked.emit(file_item, 0)
                            self.ui.existingFile_list.verticalScrollBar().setValue(
                                self.ui.existingFile_list.verticalScrollBar().value() + 20
                            )

    def populate_publish_assets(self, tree=None, root=None, current_directory=None):
        """
        This function populates several trees looking for either asset saves or file publishes. It keeps them
        separate for better organization. Assets are kept separate from working file publishes.
        :param tree: The QTreeWidget item being populated.
        :param root: The root folder. This is primarily to separate out assets from publishes.
        :param current_directory: The root scene folder
        :return:
        """
        allowed_extensions = ['ma', 'mb', 'obj', 'fbx', 'abc']
        excluded_folders = ['db', 'edits', '.mayaSwatches', 'snapshots']
        allowed_folders = ['assets', 'Publishes', self.ui.publish.text()]

        if current_directory and tree:
            tree.clear()
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
                        parent_item = tree
                    else:
                        parent_item = folder_items.get(os.path.dirname(relative_folder_name), tree)

                    # Add the folder to the tree (preserve the folder structure)
                    if relative_folder_name not in folder_items:
                        folder_item = QTreeWidgetItem(parent_item)
                        folder_item.setText(0, os.path.basename(folder_name))
                        folder_item.setData(0, Qt.UserRole, {"folder": folder_name, "file": ""})
                        folder_items[relative_folder_name] = folder_item
                        status = self.get_item_status(folder=folder_name)
                        if status:
                            colors = self.set_item_status(status=status)
                            fg = colors[0]
                            bg = colors[1]
                            folder_item.setForeground(0, QColor(fg))
                            folder_item.setBackground(0, QColor(bg))
                        if relative_folder_name == '.':
                            folder_items[relative_folder_name].setExpanded(True)

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
                            status = self.get_item_status(folder=folder_name)
                            if status:
                                colors = self.set_item_status(status=status)
                                fg = colors[0]
                                bg = colors[1]
                                subfolder_item.setForeground(0, QColor(fg))
                                subfolder_item.setBackground(0, QColor(bg))
                            folder_items[relative_subfolder_name] = subfolder_item

                    for file_name in files:
                        file_extension = file_name.split('.')[-1].lower()
                        if file_extension not in allowed_extensions:
                            continue

                        # Check if the file is in an allowed folder ("assets" or "Publishes")
                        if any(allowed_folder in relative_folder_name.split(os.sep) for allowed_folder in
                               allowed_folders) or root in folder_name:
                            file_path = os.path.normpath(os.path.join(folder_name, file_name))
                            file_path = file_path.replace('\\', '/')

                            # Add the file to the tree if in allowed folders
                            file_item = QTreeWidgetItem(folder_items[relative_folder_name])
                            file_item.setText(0, file_name)
                            file_item.setData(0, Qt.UserRole, {'folder': folder_name, 'file': file_name})
                            status = self.get_item_status(folder=folder_name, filename=file_name)
                            if status:
                                colors = self.set_item_status(status=status)
                                fg = colors[0]
                                bg = colors[1]
                                file_item.setForeground(0, QColor(fg))
                                file_item.setBackground(0, QColor(bg))

    def message(self, text=None, ok=True, obj=None):
        """
        This function displays a message at the bottom of the UI and highlights problem fields if there are any
        :param text: The message being displayed
        :param ok: Whether the information is good or bad.  True dispays a green message, False displays a red message.
        :param obj: Red messages will highlight this object: QLineEdit, QTreeWidget, QListWidget or other object.
        :return:
        """
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

    def pop_up_message(self):
        """
        Pops up a simple message box for quick inputs.
        :return:
        """
        msg_box = CustomMessageBox(self)
        result = msg_box.get_input()
        if result:
            return result
        return False

    def pop_up_note(self):
        """
        Pops up a simple Text editor to add a note in for status changes.
        :return:
        """
        note_box = CustomNotesBox()
        result = note_box.get_input()
        if result:
            return result
        return False

    def run(self, close=True, status=None):
        """
        This is the main 'Save As' feature and makes up the primary function of the tool.  It gets the next version
        for a file and saves it up with a note.
        :param close: Whether to keep the UI opened or close it.
        :return:
        """
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
        if not status:
            status = 'In Progress'
        self.create_note(notes=notes, output_file=output_file, status=status)

        time.sleep(3)
        self.check_button_state(btn=self.ui.snap_btn)
        self.check_button_state(btn=self.ui.publish_btn)
        if close:
            self.close()
        else:
            return output_file
        return True

    def snapshot(self, note=None):
        """
        Creates a Snapshot file.  Snapshots are sub-versions of files that are saved with a date-stamp that can be
        accessed at any time in the future.  Allowing for a layer of projection between versioning up.
        :param note: The note associated with the snapshot.  Say what you did!
        :return:
        """
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
        self.check_button_state()

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
        current_file_item = self.ui.existingFile_list.selectedItems()[0]
        current_file_column = self.ui.existingFile_list.currentColumn()
        self.ui.existingFile_list.itemClicked.emit(current_file_item, current_file_column)

    def open_recent_file(self, f=False):
        """
        This function opens a recent file from the Recent Files list
        :param f: Whether to force open the file or not.
        :return:
        """
        current_item = self.ui.recentFilesList.currentItem()
        file_text = current_item.text()
        open_file = current_item.data(Qt.UserRole)
        try:
            self.hide()
            cmds.file(open_file, o=True, f=f)
            self.create_note(output_file=open_file, status='In Progress')
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
        """
        Populates the recent files list.  This list is updated when the UI is closed and will show the latest file the
        next time it is opened.
        :return:
        """
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
        """
        This function populates the Snapshots list and saves the data there for quick access.  Double clicking one of
        these will load that snapshot as the latest version.
        :param item:
        :param column:
        :return:
        """
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
        self.ui.snapshots.scrollToBottom()

    def populate_recent_projects(self):
        """
        This method populates the recent projects list on the Projects tab.
        :return:
        """
        self.ui.recent_projects.clear()
        if self.recent_projects:
            for project in self.recent_projects:
                new_item = QListWidgetItem()
                new_item.setText(project)
                self.ui.recent_projects.addItem(new_item)

    def populate_project_settings(self):
        """
        This method gets its information from Maya and fills in the "New Project" defaults.  Changing them in the new
        project will update them here as well.
        :return:
        """
        # Make sure and then build the publish file rule.
        publish_rule_name = 'publish'
        publish_folder_path = 'publish'
        existing_rules = cmds.workspace(fileRuleList=True)
        if publish_rule_name not in existing_rules:
            cmds.workspace(fileRule=[publish_rule_name, publish_folder_path])
            cmds.workspace(saveWorkspace=True)

        scenes = cmds.workspace(fre='scene')
        publish = cmds.workspace(fre='publish')
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
        self.ui.publish.setText(publish)
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
        """
        Mirrors Maya's set project feature and sets the current project.
        :param btn: If the btn is true, it hides the UI while the set project window is opened.
        :return:
        """
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

    def check_button_state(self, btn=None):
        """
        Checks the button state for objects that either need to be disabled or enabled.
        :param btn: The button being checked
        :return:
        """
        if btn:
            if cmds.file(q=True, sn=True):
                btn.setEnabled(True)
                btn.setStyleSheet(
                    'color: rgb(220, 220, 220);'
                )
            else:
                btn.setEnabled(False)
                btn.setStyleSheet(
                    'color: rgb(140, 140, 140);'
                )

    def create_project(self):
        """
        This method creates a new project and makes it the set project in the UI and in Maya.
        :return:
        """
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
        """
        This method creates a default Maya project folder path and then updates and saves the workspace
        :param proj_path:
        :return:
        """
        def do_subfolders(parent_path=None):
            """
            This sub-function adds and creates sub-folders to the scenes file if that checkbox is set.
            :param parent_path:
            :return:
            """
            if parent_path:
                for subpath in subfolders:
                    new_scene_subpath = os.path.join(parent_path, subpath)
                    if not os.path.exists(new_scene_subpath):
                        os.makedirs(new_scene_subpath)

        subfolders = [
            'Char',
            'Env',
            'Props',
            'Shots',
            'Veh',
            'Cams'
        ]
        if proj_path:
            folder_structure = {
                'scenes': self.ui.scenes.text(),
                'publish': self.ui.publish.text(),
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
                        os.makedirs(new_subpath)
                        if (path == self.ui.scenes.text() and self.ui.include_subfolders.isChecked()
                                or path == self.ui.publish.text() and self.ui.include_subfolders.isChecked()):
                            do_subfolders(parent_path=new_subpath)
                    elif (path == self.ui.scenes.text() and self.ui.include_subfolders.isChecked()
                          or path == self.ui.publish.text() and self.ui.include_subfolders.isChecked()):
                        do_subfolders(parent_path=new_subpath)
                    cmds.workspace(fileRule=[key, path])
            cmds.workspace(saveWorkspace=True)
            cmds.workspace(proj_path, openWorkspace=True)
            self.update_ui()

    def get_csv(self):
        """
        Opens a dialog to get a CSV file and then populates it in the UI
        :return:
        """
        self.hide()
        file_path = cmds.fileDialog2(fileFilter='CSV Files (*.csv)', dialogStyle=2, fileMode=1)[0]
        if os.path.exists(file_path):
            self.ui.bulk_add.setText(file_path)
        self.show()

    def bulk_add(self):
        """
        This function adds folders from a CSV file.  This allows for bulk creation of a folder tree without having to
        manually create them.  It should follow the following form in the CSV file:
        NO HEADERS.
        Column1 = Asset or Shot Name  |  Column2 = Subfolder name
        Subfolders are typically:
        Cams = Cameras - this is for specialty camera rigs.
        Char = Characters
        Env = Environments
        Props = Props
        Shots = Shots
        Veh = Vehicles

        Thus, a typical CSV file would read like this:
        Bob, Char
        Truck, Veh
        Shot_0010, Shots
        Shot_0020, Shots
        :return:
        """
        csv_file_path =  self.ui.bulk_add.text()
        if not os.path.exists(csv_file_path) or os.path.splitext(csv_file_path)[1] != '.csv':
            self.message(text='CSV file is not valid', ok=False, obj=self.ui.bulk_add)
            return False
        with open(csv_file_path, mode='r', newline='', encoding='utf-8') as bulk:
            csv_reader = csv.reader(bulk)
            # Create folder
            root_directory = cmds.workspace(q=True, rd=True)
            scenes_folder = cmds.workspace(fre='scenes')
            scenes_path = os.path.join(root_directory, scenes_folder)
            for row in csv_reader:
                asset_shot_name = row[0]
                asset_shot_folder = row[1]
                if asset_shot_folder:
                    new_root_folder_path = os.path.join(scenes_path, asset_shot_folder)
                else:
                    new_root_folder_path = scenes_path
                new_asset_shot_folder = os.path.join(new_root_folder_path, asset_shot_name)
                if not os.path.exists(new_asset_shot_folder):
                    os.makedirs(new_asset_shot_folder)
                    self.create_note(notes='Auto-created using Bulk Add CSV feature', output_file=new_asset_shot_folder,
                                     status='Ready')

        self.ui.existingFile_list.clear()
        self.populate_existing_files(current_directory=self.scene_folder_path)
        self.ui.saverTabs.setCurrentIndex(0)

    def create_asset_shot(self):
        """
        This function creates a regular new asset or shot.  If it detects anything in the Bulk Add from CSV field, it
        will trigger that function instead.
        When creating an asset or shot, you add a simple name for the new asset or shot, select what kind of thing it
        is from the drop-down list and hit "Create Asset/Shot".
        The Name of the thing should only be a simple root name and not mirror a full file name.  For instance:
        Name = Sarah
        Type = Char
        or
        Name = Speedboat
        Type = Veh

        It should NOT be:
        Name = PRJ_Sarah_model_v001
        Type = Char
        This will create a super long, and very bad name like "PRJ_PRJ_Sarah_model_v001_model_v001" and you don't want
        that.

        Once the new asset or shot is created a new Maya file will be created and opened with a default One Meter Cube
        loaded for scene scale.  This scene scale is taken from the UI Settings Scene Scale.  The cube can be deleted
        once the proper scale is understood for an object.
        :return:
        """
        _type = self.ui.assetShot_type.currentText()
        asset_shot_name = self.ui.asset_name.text()
        bulk_add = self.ui.bulk_add.text()
        if bulk_add:
            self.bulk_add()
            return False
        if _type == 'Cams':
            message_type = 'Camera'
        elif _type == 'Char':
            message_type = 'Character'
        elif _type == 'Env':
            message_type = 'Environment'
        elif _type == 'Props':
            message_type = 'Props'
        elif _type == 'Veh':
            message_type = 'Vehicle'
        else:
            message_type = 'Shots'
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
        path = os.path.join(type_path, asset_shot_name)
        if not os.path.exists(path):
            os.makedirs(path)

        # Create task sub-folders.
        if _type != 'Cams' and _type != 'Shots':
            for task_type in self.asset_tasks:
                task_path = os.path.join(path, task_type)
                if not os.path.exists(task_path):
                    os.makedirs(task_path)
        elif _type == 'Shots':
            for task_type in self.shot_tasks:
                task_path = os.path.join(path, task_type)
                if not os.path.exists(task_path):
                    os.makedirs(task_path)
        elif _type == 'Cams':
            task_path = os.path.join(path, 'rig')
            if not os.path.exists(task_path):
                os.makedirs(task_path)

        close_previous = self.create_new_file_with_prompt()
        if close_previous:
            if message_type == 'Shots':
                task_type = 'layout'
            else:
                task_type = 'model'
            file_name = self.build_path(path=path, rootName=asset_shot_name, task=task_type,
                                        ext=self.ui.fileType.currentText(), show=self.ui.showCode.text(),
                                        artist=self.ui.artistName.text(), version=1)
            scale = float(self.ui.sceneScale.text())
            scale_mult = scale * 10
            cmds.polyCube(n='_SCENE_SCALE_1_MeterCube', sx=scale, sy=scale, sz=scale, w=scale_mult, d=scale_mult,
                          h=scale_mult, fzn=True, cuv=1)
            cmds.file(rename=file_name)
            cmds.file(save=True, f=True)

            self.create_note(notes=f'Automatically generated {task_type} file for {asset_shot_name}',
                             output_file=file_name, status='Ready')

            self.ui.folder.setText(path)
            self.ui.filename.setText(asset_shot_name)
            self.ui.version.setValue(1)
            self.ui.taskType.setCurrentText(task_type)
            self.update_ui()
            self.current_file_path = file_name

        self.ui.existingFile_list.clear()
        self.populate_existing_files(current_directory=self.scene_folder_path)
        self.ui.saverTabs.setCurrentIndex(0)

    def create_new_file_with_prompt(self):
        """
        This method just attempts to create the new Maya file.  It will prompt you to save any existing work.
        :return:
        """
        # Check if there are unsaved changes
        if cmds.file(q=True, modified=True):
            # Hide the UI
            self.hide()
            # Prompt the user to save changes manually
            result = cmds.confirmDialog(
                title='Save Changes?',
                message='You have unsaved changes. Do you want to save them?',
                button=['Save', 'Don\'t Save', 'Cancel'],
                defaultButton='Save',
                cancelButton='Cancel',
                dismissString='Cancel'
            )

            if result == 'Save':
                # Save the current file
                cmds.file(save=True)
            elif result == 'Cancel':
                # Cancel the operation
                self.show()
                return
            self.show()

        # Now create the new file
        cmds.file(new=True, force=True)
        return True

    def get_project_folder(self):
        """
        This method populates the new project folder for the new project function.
        :return:
        """
        self.hide()
        new_project_folder = cmds.fileDialog2(fm=3, ds=2)
        if new_project_folder:
            new_project_folder = new_project_folder[0]
            if os.path.exists(new_project_folder):
                self.ui.new_project_folder.setText(new_project_folder)
        self.show()

    def set_autosave(self):
        """
        This method sets the Autosave functionality in Maya.  This can be a handy way to set this without having to go
        into Maya's settings and will help save you from crashes.
        :return:
        """
        if self.ui.autosaver.isChecked():
            cmds.optionVar(intValue=('autoSaveEnabled', 1))
            cmds.optionVar(intValue=('autoSaveInterval', self.ui.autosave_count.value()))
        else:
            cmds.optionVar(intValue=('autoSaveEnabled', 0))

    def import_snapshot(self, item, column):
        """
        This function restores a Snapshot to your current file.  It replaces what is in your current file with what was
        in the Snapshot that you saved earlier.  Before it loads a snapshot, it will ask if you want to do a protective
        snapshot of what's currently in your file so that you don't lose anything if you change your mind.
        If you do not accept the Auto-Snapshot, the imported Snapshot will replace all of your current work and there
        won't be any way to get it back.
        :param item:
        :param column:
        :return:
        """
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
        """
        This function publishes your current file and versions it up to protect the publish.  It does several things.
        It versions up your current file.  It saves a copy of your current file into a Publishes folder and adds the
        tag "PUB" to the published file.
        It imports references and removes the namespaces unless several copies of a reference exist.
        Lastly it adds a note to the publish so that you know what was done to it.
        This publish then will show up in the Publishes Tree on the Assets - Publishes tab and can be imported or
        referenced into your scene.
        :return:
        """
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
        new_version = self.run(close=False, status='For Review')

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

        publish_folder = self.ui.publish.text()
        scene_folder = self.ui.scenes.text()
        pub_folder = root_path.replace(scene_folder, publish_folder)
        if not os.path.exists(pub_folder):
            os.makedirs(pub_folder)

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
        self.create_note(notes=notes, output_file=publish_file, status='Done')
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
        Any out of date references will force the UI to open to the References tab for review.
        :return:
        """
        self.ui.referenceList.clear()
        references = cmds.file(q=True, reference=True)
        reference_info = {}

        light_red = QColor(255, 102, 102)
        light_green = QColor(144, 238, 144)

        # Gathering all references
        for ref in references:
            # Check that a reference is loaded
            is_loaded = cmds.referenceQuery(ref, isLoaded=True)
            if not is_loaded:
                cmds.warning(f'Reference file {ref} is unloaded.  Skipping.')
                continue

            try:
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
                    cmds.warning(f'{ref_file} is out of date!  Latest file is {latest_file}')
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
                    self.ui.saverTabs.setCurrentIndex(1)
                else:
                    new_entry.setCheckState(Qt.Unchecked)
                    new_entry.setBackground(light_green)
                    new_entry.setForeground(Qt.black)
                    new_entry.setToolTip(f'Up to Date!')

                self.ui.referenceList.addItem(new_entry)
            except Exception as e:
                cmds.warning(f'Failed to process reference file {ref}: {e}')

    def update_references(self):
        """
        This function updates an out-of-date reference to the latest version in the path.
        :return:
        """
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
        """
        This method collects a list of Publishes that have been checked.  If an out-of-date publish is not checked,
        it will not get updated.
        :return:
        """
        checked_items = {}
        for i in range(self.ui.referenceList.count()):
            item = self.ui.referenceList.item(i)
            if item.checkState() == Qt.Checked:
                checked_items[i] = item.data(Qt.UserRole)
        return checked_items

    def import_and_clean_references(self):
        """
        This is the function that does the importing and cleaning of references for a Publish function.
        :return:
        """
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
        """
        This function counts the number of reference copies in a scene to decide whether is should remove the namespaces
        or not.
        :param reference_file: File being referenced in
        :param namespace: The current namespace for that file
        :param count: Number of times a file exists in a scene.
        :return:
        """
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
        """
        This function loads in a reference from one of the QTreeWidgets: Existing Files, Publishes or Assets.
        :param element: The Tree from which the reference call is being made.
        :return:
        """
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
        """
        This function imports a file from the tree being called from
        :param element: The tree from which the import call was made
        :return:
        """
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

    def run_cam_bake(self):
        """
        This function starts the process of baking out the current scene camera and saves out an FBX into the Assets
        folder in a Shot_Cams sub-folder.
        :return:
        """
        data = self.get_root_and_task(filename=cmds.file(q=True, sn=True))
        self.hide()
        cam_bake = self.sptk.start_cam_bake(data=data)
        self.show()
        if cam_bake:
            notes = cam_bake['notes']
            output_file = cam_bake['output']
            cam_name = cam_bake['cam_name']
            self.create_note(notes=notes, output_file=output_file, status='For Review')
            self.message(text='Camera baked successfully: %s' % cam_name, ok=True)
        else:
            self.message(text='Camera could not be baked!', ok=False)

    def export_selection(self, export_type=None):
        """
        This function looks to see if an object is selected and decides whether to export selection or export all.
        It then saves out the selection or entire scene file as an FBX, OBJ or Alembic ABC file.
        :param export_type: Kind of file to write out, FBX, OBJ, or ABC
        :return:
        """
        if export_type:
            selection = cmds.ls(sl=True)
            if export_type == 'FBX export':
                ext = '.fbx'
                options = ''
            elif export_type == 'OBJexport':
                ext = '.obj'
                options = 'groups=1;ptgroups=1;materials=1;smoothing=1;normals=1'
            else:
                start_frame = cmds.playbackOptions(q=True, minTime=True)
                end_frame = cmds.playbackOptions(q=True, maxTime=True)
                root_node = '|NonRefThing'
                ext = '.abc'
            if export_type != 'abc':
                if not selection:
                    filename = cmds.file(q=True, sn=True, shn=True)
                    base_filename = os.path.splitext(filename)[0]
                    filename = base_filename + ext
                    output_filename = os.path.join(self.asset_folder_path, filename)
                    cmds.file(output_filename, f=True, options=options, type=export_type, pr=True, ea=True)
                else:
                    get_filename = self.pop_up_message()
                    if get_filename:
                        filename = get_filename + ext
                        output_filename = os.path.join(self.asset_folder_path, filename)
                        cmds.file(output_filename, f=True, options=options, typ=export_type, pr=True, es=True)
                    else:
                        return False
            else:
                if not selection:
                    filename = cmds.file(q=True, sn=True, shn=True)
                    base_filename = os.path.splitext(filename)[0]
                    filename = base_filename + ext
                    output_filename = os.path.join(self.asset_folder_path, filename)
                    options = (
                        f"-frameRange {start_frame} {end_frame} "
                        "-stripNamespaces "
                        "-uvWrite "
                        "-writeColorSets "
                        "-writeFaceSets "
                        "-wholeFrameGeo "
                        "-worldSpace "
                        "-writeVisibility "
                        "-eulerFilter "
                        "-autoSubd "
                        "-writeUVSets "
                        "-dataFormat ogawa "
                        f"-root {root_node} "
                        f"-file {output_filename}"
                    )
                    cmds.AbcExport(j=options)
                else:
                    get_filename = self.pop_up_message()
                    if get_filename:
                        filename = get_filename + ext
                        output_filename = os.path.join(self.asset_folder_path, filename)
                        options = (
                            f"-frameRange {start_frame} {end_frame} "
                            "-stripNamespaces "
                            "-uvWrite "
                            "-writeColorSets "
                            "-writeFaceSets "
                            "-wholeFrameGeo "
                            "-worldSpace "
                            "-writeVisibility "
                            "-eulerFilter "
                            "-autoSubd "
                            "-writeUVSets "
                            "-dataFormat ogawa "
                            f"-root {root_node} "
                            f"-file {output_filename}"
                        )
                        cmds.AbcExport(j=options)

    def playblast(self):
        """
        Creates a playblast based on the UI Project settings and saves it with the current filename into the Movies
        folder.
        :return:
        """
        self.hide()
        # FIXME: Add some viewer functionality here.  Like, removing all but the GEO
        playblast = self.sptk.playblast()
        self.close()

    def render_settings(self):
        """
        This method attempts to set the Maya render settings based on the information in the UI Settings Tab.
        It has an issue with Arnold if the Render Settings dialog in Maya has not been physically opened yet.
        :return:
        """
        try:
            res_width = int(self.ui.resolutionWidth.text())
            res_height = int(self.ui.resolutionHeight.text())
            render_output = self.ui.image_format.currentText()
            cmds.setAttr('defaultResolution.width', res_width)
            cmds.setAttr('defaultResolution.height', res_height)
            cmds.setAttr('defaultArnoldDriver.aiTranslator', render_output, type='string')
            cmds.setAttr('defaultArnoldDriver.mergeAOVs', 1)
        except RuntimeError as e:
            cmds.warning(f'Arnold render settings have not loaded.  '
                       f'Make sure the plugin is loaded and run this again: {e}')

    def closeEvent(self, event):
        """
        This method collects all the objects that need to get saved into the QSettings and writes them out for
        future use.  This is where the Recent Files and Recent Projects lists get parsed.  It also saves any user UI
        settings for the next time the window is opened.  Including where the window is placed, and how it is expanded.
        :param event:
        :return:
        """
        self.settings.setValue('appendArtist', self.ui.AppendArtist.isChecked())
        # self.settings.setValue('showcode', self.ui.showCode.text())
        self.settings.setValue('bake_cam_scene_name', self.ui.bakeCamSceneName.isChecked())
        self.settings.setValue('geometry', self.saveGeometry())
        if len(self.recent_files) >= self.recent_file_count:
            self.recent_files.pop(self.recent_file_count - 1)
        if {'filename': '', 'path': ''} in self.recent_files:
            i = self.recent_files.index({'filename': '', 'path': ''})
            self.recent_files.pop(i)
        self.current_file_path = self.current_file_path.replace('\\', '/')
        this_file_data = {
            'filename': os.path.basename(self.current_file_path),
            'path': self.current_file_path
        }
        if this_file_data not in self.recent_files and this_file_data != {'filename': '', 'path': ''}:
            self.recent_files.insert(0, this_file_data)
        self.settings.setValue('recent_files', self.recent_files)
        if len(self.recent_projects) >= 5:
            self.recent_projects.pop(4)
        current_project = cmds.workspace(q=True, act=True)
        current_project = current_project.replace('\\', '/')
        if current_project not in self.recent_projects:
            self.recent_projects.insert(0, current_project)
        self.settings.setValue('recent_projects', self.recent_projects)
        self.settings.setValue('autosave', self.ui.autosaver.isChecked())
        self.settings.setValue('asset_shot', self.ui.assetShot_type.currentText())
        self.settings.setValue('render_output', self.ui.image_format.currentText())
        self.settings.setValue('autoload', self.ui.autoload.isChecked())
        self.settings.setValue('artist_name', self.ui.artistName.text())


if __name__ == '__main__':
    saveas = sansPipe()
