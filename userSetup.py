import maya.cmds as cmds
import maya.mel as mel
import os
import sys
from PySide6.QtCore import QSettings

__version__ = '1.2.5'
__author__ = 'Adam Benson'

settings = QSettings(__author__, 'Sans Pipe Super Saver')
autoload = settings.value('autoload', None)
if autoload == 'true':
    autoload = True
else:
    autoload = False


def load_sansPipe():
    # Get the user app directory (which resolves to the base OneDrive path)
    user_app_dir = cmds.internalVar(userAppDir=True)

    # Get the Maya version year dynamically
    maya_version = mel.eval("getApplicationVersionAsFloat();")
    maya_version_year = str(int(maya_version))  # Convert to string and remove decimal

    # Define the path to the Maya plug-ins directory with the version year
    plugins_folder = os.path.join(user_app_dir, maya_version_year, 'plug-ins')

    # Define the path to your sansPipe folder within the plug-ins directory
    sans_pipe_folder = os.path.join(plugins_folder, 'sansPipe')

    # Verify if the sansPipe folder exists
    if not os.path.exists(sans_pipe_folder):
        print(f"Plugin folder {sans_pipe_folder} does not exist.")
        return

    # Add the sansPipe folder to the Python path
    if sans_pipe_folder not in sys.path:
        sys.path.append(sans_pipe_folder)

    # Automatically load the sansPipe plugin if it's not already loaded
    try:
        if not cmds.pluginInfo('sansPipe.py', query=True, loaded=True):
            cmds.loadPlugin(os.path.join(sans_pipe_folder, 'sansPipe.py'))
        print("sansPipe plugin loaded successfully.")
    except RuntimeError as e:
        print(f"Error loading sansPipe plugin: {e}")
    except Exception as e:
        print(f"Failed to initialize sansPipe: {e}")

    try:
        import sansPipe
        if autoload:
            sansPipe.sansPipe()

    except Exception as e:
        print(f'failed to run sansPipe: {e}')


def override_save_as(*args):
    try:
        import sansPipe
        sansPipe.sansPipe()
        # run.sansPipe()
    except Exception as e:
        print(f'failed to run sansPipe: {e}')


def create_sans_pipe_menu():
    # Check if the menu already exists (to avoid duplicates)
    if cmds.menu('sansPipeMenu', exists=True):
        cmds.deleteUI('sansPipeMenu', menu=True)

    # Add the custom "Sans Pipe" menu to Maya's main window
    cmds.menu('sansPipeMenu', label='Sans Pipe', parent='MayaWindow', tearOff=True)

    # Add items to the Sans Pipe menu
    cmds.menuItem(label='Sans Pipe Saver...', command=override_save_as)
    # You can add more menu items as needed
    # cmds.menuItem(label='Another Custom Command', command=lambda: print("Another command triggered"))


def setup_hotkey():
    if autoload:
        cmds.nameCommand('customSaveAsCommand', ann='SansPipe Save As...', command='python("override_save_as()")')
        cmds.hotkey(k='S', name='customSaveAsCommand', ctl=True, sht=True)
        print('Hotkey Ctrl + Shift + S overridden')
    else:
        cmds.hotkey(k='S', name='SaveSceneAsNameCommand', ctl=True, sht=True)
        # string $nameCommandCmd = "nameCommand -ann \"SaveSceneAsNameCommand\"
        # -command (\"SaveSceneAs\") SaveSceneAsNameCommand"; eval($nameCommandCmd);


# Delay the execution until Maya is fully loaded
cmds.evalDeferred(load_sansPipe, lp=True)
cmds.evalDeferred(create_sans_pipe_menu, lp=True)
cmds.evalDeferred(setup_hotkey, lp=True)
