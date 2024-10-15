import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import platform
try:
    from PySide6.QtCore import QSettings
except ImportError:
    try:
        from PySide2.QtCore import QSettings
    except ImportError:
        raise RuntimeError('No PySide6 or PySide2 detected!')

__version__ = '1.3.11'
__author__ = 'Adam Benson'

user_app_dir = cmds.internalVar(userAppDir=True)

# Get the Maya version year dynamically
maya_version = mel.eval("getApplicationVersionAsFloat();")
maya_version_year = str(int(maya_version))

settings = QSettings(__author__, f'Sans Pipe Super Saver {maya_version_year}')
autoload = settings.value('autoload', None, type=bool)
hk_open_mod_1 = settings.value('hk_open_mod_1', None, type=str)
hk_open_mod_2 = settings.value('hk_open_mod_2', None, type=str)
hk_open_mod_3 = settings.value('hk_open_mod_3', None, type=str)
hk_open_key = settings.value('hk_open_key', None, type=str)

# Set OS differences.
if platform.system() == 'Windows':
    env_user = 'USERNAME'
    computername = 'COMPUTERNAME'
    ctrl = 'Ctrl'
    alt = 'Alt'
    command = 'Win'
else:
    env_user = 'USER'
    computername = 'HOSTNAME'
    ctrl = 'Ctrl'
    alt = 'option'
    command = 'cmd'


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
        cmds.error(f"Plugin folder {sans_pipe_folder} does not exist.")
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
        cmds.error(f"Error loading sansPipe plugin: {e}")
    except Exception as e:
        cmds.error(f"Failed to initialize sansPipe: {e}")

    try:
        import sansPipe
        if autoload:
            sansPipe.sansPipe()

    except Exception as e:
        print(f'failed to run sansPipe: {e}')


def override_save_as(*args):
    try:
        import sansPipe
        sansPipe.show_sans_pipe()
        # run.sansPipe()
    except Exception as e:
        cmds.error(f'failed to run sansPipe: {e}')


def run_cam_bake(*args):
    try:
        import sp_tools as sptk
        sptk.sp_toolkit().start_cam_bake()
    except Exception as e:
        cmds.error(f'failed to run Camera Bake: {e}')


def create_camera(*args):
    try:
        import sp_tools as sptk
        sptk.sp_toolkit().create_camera()
    except Exception as e:
        cmds.error(f'Unable to create camera! {e}')


def do_database_repair(*args):
    try:
        import sp_tools as sptk
        sptk.sp_toolkit().db_seek_and_repair()
    except Exception as e:
        cmds.error(f'Unable to run DB Seek and Repair! {e}')


def blow_away_snaps(*args):
    try:
        import sp_tools as sptk
        sptk.sp_toolkit().blow_away_snapshots()
    except Exception as e:
        cmds.error(f'Unable to run Blow Away Snapshots! {e}')


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
    cmds.menuItem(label='Bake Camera', command=run_cam_bake)
    cmds.menuItem(label='Create Camera', command=create_camera)
    cmds.menuItem(label='Do Database Repair', command=do_database_repair)
    cmds.menuItem(label='!Blow Away All Snapshots!', command=blow_away_snaps)


# Function to check if the hotkey set is locked by testing temporary command creation
def is_hotkey_set_locked():
    try:
        # Create a temporary runtime command
        if not cmds.runTimeCommand('tempCommand', exists=True):
            cmds.runTimeCommand('tempCommand', ann='Temp Command', c='print("Temp Command")', default=True)

        # Try to assign it to a temporary hotkey
        cmds.hotkey(k='F12', name='tempCommand')

        # Clean up by removing the temp hotkey and runtime command
        cmds.hotkey(k='F12', name='')
        cmds.runTimeCommand('tempCommand', edit=True, delete=True)

        return False  # If no errors, the set isn't locked
    except RuntimeError:
        return True  # If there are errors, the set is likely locked


# Function to create a new hotkey set and copy hotkeys
def create_new_hotkey_set():
    current_hotkey_set = cmds.hotkeySet(query=True, current=True)
    new_hotkey_set = "custom_hotkey_set"

    # Create a new hotkey set based on the current one
    if not cmds.hotkeySet(new_hotkey_set, exists=True):
        cmds.hotkeySet(new_hotkey_set, source=current_hotkey_set)  # This copies the current set
        print(f"New hotkey set '{new_hotkey_set}' created and unlocked.")

    # Switch to the new hotkey set
    cmds.hotkeySet(new_hotkey_set, edit=True, current=True)
    print(f"Switched to new hotkey set: {new_hotkey_set}")

    return new_hotkey_set


def setup_hotkey():
    if autoload:
        current_hotkey_set = cmds.hotkeySet(q=True, current=True)
        is_default = (current_hotkey_set == 'Maya_Default')
        is_locked = is_hotkey_set_locked()
        if is_locked or is_default:
            create_new_hotkey_set()
        if hk_open_mod_1 == ctrl or hk_open_mod_2 == ctrl or hk_open_mod_3 == ctrl:
            ctrl_ = True
        else:
            ctrl_ = False
        if hk_open_mod_1 == alt or hk_open_mod_2 == alt or hk_open_mod_3 == alt:
            alt_ = True
        else:
            alt_ = False
        if hk_open_mod_1 == 'Shift' or hk_open_mod_2 == 'Shift' or hk_open_mod_3 == 'Shift':
            shift_ = True
        else:
            shift_ = False
        cmds.nameCommand('customSaveAsCommand', ann='SansPipe Save As...', command='python("override_save_as()")')
        cmds.hotkey(k=hk_open_key, name='customSaveAsCommand', ctl=ctrl_, sht=shift_, alt=alt_)
        print(f'Hotkey {hk_open_mod_1} + {hk_open_mod_2} + {hk_open_key} overridden')
    else:
        cmds.hotkey(k='S', name='SaveSceneAsNameCommand', ctl=True, sht=True, alt=False)
        # string $nameCommandCmd = "nameCommand -ann \"SaveSceneAsNameCommand\"
        # -command (\"SaveSceneAs\") SaveSceneAsNameCommand"; eval($nameCommandCmd);


# Delay the execution until Maya is fully loaded
cmds.evalDeferred(load_sansPipe, lp=True)
cmds.evalDeferred(create_sans_pipe_menu, lp=True)
cmds.evalDeferred(setup_hotkey, lp=True)
