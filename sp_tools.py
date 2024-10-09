# Sans-Pipe Maya Light Pipeline Utility - Toolkit

"""
This tool kit stores the functions that help run the SANS-PIPE UTILITY.  The idea here is that these tools can be used
in or out of the pipeline system, with, or without the main UI.
"""

__version__ = '1.3.9'
__author__ = 'Adam Benson'

import shutil

from maya import cmds
import os
import sys
import re
import json
import time
from datetime import datetime
import configparser
import inspect
import math

try:
    from PySide6.QtCore import QSettings
    print('PySide6 detected.')
except ImportError:
    try:
        from PySide2.QtCore import QSettings
        print('PySide2 detected.')
    except ImportError:
        raise RuntimeError('Neither PySide 6 or PySide 2 detected!')

class sp_toolkit(object):
    def __init__(self):
        """
        Processing the global setups for the overall system
        """
        # Get the configuration and variables files for the project
        self.workspace = cmds.workspace(q=True, rd=True)
        self.config_path = os.path.join(self.workspace, 'show_config.cfg')
        if not os.path.exists(self.config_path):
            cmds.warning('No configuration file exists.  Please run SansPile for the first time.')

        # Get the configurations from the show_config.cfg file.
        config = configparser.ConfigParser()
        config.read(self.config_path)
        self.show_code = config['Project']['Show_Code']
        self.project_name = config['Project']['Show_Name']
        self.res_width = config['Camera']['resolution_width']
        self.res_height = config['Camera']['resolution_height']
        self.filmback_width = config['Camera']['filmback_width']
        self.filmback_height = config['Camera']['filmback_height']
        self.scene_scale = config['Scene']['scene_scale']
        self.recent_file_count = int(config['Project']['recent_file_count'])
        self.autosave_interval = int(config['Scene']['autosave_interval'])

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
                        'asset_tasks': None, 'shot_tasks': None}
        # Set the project constants.
        self.tasks = globVars['tasks']
        self.invalidCharacters = globVars['invalidCharacters']
        self.cameraNames = globVars['cameraNames']
        self.cameraAttributes = globVars['cameraAttributes']

        # Get the QSettings from the Super Saver
        self.settings = QSettings(__author__, 'Sans Pipe Super Saver')
        self.appendartist = self.settings.value('appendArtist', None, type=bool)
        self.bakeCamSceneName = self.settings.value('bake_cam_scene_name', None, type=bool)
        self.artist_name = self.settings.value('artist_name', None, type=str)

    def get_data(self):
        """
        This attempts to get as much data as the main UI to help fill in variables.
        :return:
        """
        filepath = cmds.file(q=True, sn=True)
        if not filepath:
            cmds.warning('You must save the file first!')
            return
        filename = os.path.basename(filepath)
        root_name = None
        task_name = None
        task_abbr = None
        data = None
        show_code = self.show_code
        artist_name = self.artist_name
        for task in self.tasks.keys():
            for abbr in self.tasks[task]:
                root_name = filename.split(abbr)[0]
                task_abbr = abbr
                task_name = task
                if root_name.endswith('_'):
                    root_name = root_name.rstrip('_')
                if root_name.startswith(show_code):
                    root_name = root_name.replace(show_code, '')
                    root_name = root_name.lstrip('_')
                if root_name.startswith('_'):
                    root_name = root_name.lstrip('_')
                artist = f'{artist_name}_'
                if artist in root_name:
                    root_name = root_name.replace(artist, '')
                break
        if root_name and task_name and task_abbr:
            data = {
                'root_name': root_name,
                'task_name': task_name,
                'task_abbr': task_abbr
            }
        return data

    def create_camera(self):
        """
        Creates a new camera using the film back and scene scale settings from the UI.  Asks for a focal length.
        :return:
        """
        filmback_w = float(self.filmback_width)
        filmback_h = float(self.filmback_height)
        mult_fb_w = (filmback_w / 10) / 2.54
        mult_fb_h = (filmback_h / 10) / 2.54
        scene_scale = float(self.scene_scale)
        aspect_ratio = mult_fb_w / mult_fb_h
        data = self.get_data()
        base_name = data['root_name']
        show_code = self.show_code
        cam_name = f'{show_code}_{base_name}_shotCam'
        result = cmds.promptDialog(
            title='Camera Focal Length',
            message='Focal Length (numeric value in mm):',
            button=['Accept', 'Cancel'],
            defaultButton='Accept',
            cancelButton='Cancel',
            dismissString='Cancel',
            text=str(35.0)
        )
        if result == 'Accept':
            input_value = cmds.promptDialog(q=True, text=True)
            try:
                focal_length = float(input_value)
            except ValueError as e:
                cmds.warning(f'Improper focal length value: {e}')
                self.show()
                return False
        else:
            return False

        new_cam = cmds.camera(vfa=mult_fb_h, hfa=mult_fb_w, ar=aspect_ratio, fl=focal_length, coi=5, lsr=1, hfo=0,
                              vfo=0, ff='Fill', ovr=1, mb=0, sa=144, ncp=1, fcp=10000000, o=False, ow=30, pze=False,
                              hpn=0, vpn=0, zom=1)
        new_cam_parent = cmds.listRelatives(new_cam, p=True)
        cmds.select(new_cam_parent, r=True)
        cmds.rename(cam_name)
        cmds.scale(scene_scale, scene_scale, scene_scale)
        return cam_name

    def start_cam_bake(self, data=None):
        """
        This function starts the process of baking out the current scene camera and saves out an FBX into the Assets
        folder in a Shot_Cams sub-folder.
        :return:
        """
        if not data:
            data = self.get_data()
        print(f'data["root_name"]: {data["root_name"]}')
        cmds.inViewMessage(amg="Baking Camera...", pos='midCenter', fade=True)
        bake_camera = self.cam_bake(root_name=data['root_name'])
        if bake_camera:
            get_scene_name = cmds.file(q=True, sn=True)
            scene_name = os.path.splitext(os.path.basename(get_scene_name))[0]
            get_root_path = cmds.workspace(q=True, rd=True)
            task = data['task_name']
            if task in scene_name:
                cam_name = scene_name.replace(task, 'cam')
                cam_name = cam_name + '.fbx'
            else:
                cam_name = 'shot_cam.fbx'

            cmds.select(bake_camera, r=True)
            output_path = os.path.join(get_root_path, 'assets/Shot_Cams')
            output_file = os.path.join(output_path, cam_name)
            try:
                cmds.file(
                    output_file,
                    f=True,
                    options=";exportUVs=1;exportSkels=none;exportSkin=none;exportBlendShapes=0;exportDisplayColor=0;exportColorSets=1;exportComponentTags=1;defaultMeshScheme=catmullClark;animation=0;eulerFilter=0;staticSingleSample=0;startTime=1;endTime=1;frameStride=1;frameSample=0.0;defaultUSDFormat=usdc;rootPrim=;rootPrimType=scope;defaultPrim=shotCam_baked;shadingMode=useRegistry;convertMaterialsTo=[UsdPreviewSurface];exportRelativeTextures=automatic;exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=0;worldspace=0;excludeExportTypes=[]",
                    type='FBX Export', pr=True, es=True, ex=False
                )
            except RuntimeError as e:
                cmds.error(f'Could not bake the camera!  Could be a permissions issue, or some other failure: {e}')
            cmds.select(bake_camera, r=True)
            cmds.delete()
            notes = (f'Automatic camera bake for {scene_name}.  Camera name: {bake_camera[0]}  '
                     f'Output filename: {os.path.basename(output_file)}')

            cmds.inViewMessage(amg=f"Camera Baked Successfully! {cam_name}", pos='midCenter', fade=True)
            return {'notes': notes, 'output': output_file, 'cam_name': cam_name}
        else:
            return None

    def cam_bake(self, root_name=None):
        """
        This method does the actual baking of the shot camera.  It creates a duplicate camera, parents it in world space
        to the current scene camera and bakes out the keyframes for that camera.
        :return:
        """
        cam_transform = None
        all_cams = cmds.ls(ca=True)
        root_name = root_name.replace('\\', '/')
        root_name = root_name.rstrip('/')
        get_root = root_name.split('/')
        root_name = get_root[-1]
        print(f'root_name: {root_name}')
        for cam in all_cams:
            if self.bakeCamSceneName:
                if root_name in cam:
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
            if cam_transform and root_name not in cam_transform:
                new_cam_name = '%s_%s' % (root_name, cam_transform)
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

    def create_burn_in(self, camera=None, filename=None, version=None, time_code=None, frame_number=None,
                       focal_length=None):
        burn_in_text = cmds.textCurves(ch=False, f='Arial', t=f'Filename: {filename}\nVersion: {version}\nTime Code: '
                                                              f'{time_code}\nFrame: {frame_number}\nFocal Length: '
                                                              f'{focal_length}')
        cmds.parent(burn_in_text[0], camera)
        cmds.move(0, 0, 1, burn_in_text, r=True)

        aspect_ratio = cmds.getAttr(camera + '.filmAspectRatio')
        sensor_width = cmds.getAttr(camera + '.horizontalFilmAperture') * 25.4  # Convert from inches to mm
        fov_degrees = cmds.getAttr(camera + '.focalLength') / sensor_width * 2 * math.degrees(math.atan(sensor_width / (2 * focal_length)))

        # Calculate width and scale text based on the FOV
        # Assuming FOV in degrees
        burn_in_width = 2 * math.tan(math.radians(fov_degrees / 2)) * 1  # 1 unit away
        scale_factor = burn_in_width / cmds.getAttr(burn_in_text[0] + '.boundingBox')[1][0]  # Scale to fit in width

        cmds.scale(scale_factor, scale_factor, scale_factor, burn_in_text)

        # Set visibility and other attributes as needed
        cmds.setAttr(burn_in_text[0] + '.overrideEnabled', 1)
        cmds.setAttr(burn_in_text[0] + '.overrideColor', 17)  # Change color as needed (17 is red)

        return burn_in_text

    def playblast(self):
        """
        Creates a playblast based on the UI Project settings and saves it with the current filename into the Movies
        folder.
        :return:
        """
        res_width = int(self.res_width)
        res_height = int(self.res_height)
        movies_folder = cmds.workspace(fre='movie')
        filename = cmds.file(q=True, sn=True, shn=True)
        basename = os.path.splitext(filename)[0]
        filename = basename + '.mov'
        # print(f'basename: {basename}')
        # pattern = r'(_v|_V)\d+'
        # version = re.findall(pattern, basename)
        # print(f'version: {version}')
        output = os.path.join(movies_folder, filename)
        # current_frame = cmds.currentTime(query=True)
        # current_camera = cmds.modelEditor('modelPanel4', q=True, camera=True)
        # focal_length = cmds.getAttr(current_camera + '.focalLength')
        #
        # burn_in_text = self.create_burn_in(camera=current_camera, filename=filename, version=version,
        #                                    time_code=current_frame, frame_number=current_frame,
        #                                    focal_length=focal_length)

        cmds.playblast(format='qt', filename=output, sequenceTime=0, clearCache=1, viewer=1, showOrnaments=1, fp=4,
                       percent=100, compression='PNG', quality=70, widthHeight=(res_width, res_height), exposure=0,
                       gamma=1, fo=True)

        # cmds.delete(burn_in_text)

    def db_seek_and_repair(self):
        """
        I'm running into a situation where sometimes one of the database files is getting corrupted, and I can't figure
        out where.  So, this tool is designed to try and find that corrupted DB file and potentially repair it.
        Fuckin' JSON.
        :return:
        """
        find_db_path = os.path.join(self.workspace, cmds.workspace(fre='scenes'))
        collect_dbs = []
        walk_path = os.walk(find_db_path)
        for root, dir, files in walk_path:
            if 'db' in root:
                for f in files:
                    if f.endswith('.json'):
                        path = os.path.join(root, f)
                        collect_dbs.append(path)
        for db in collect_dbs:
            with open(db, 'r') as odb:
                get_db = odb.read()
            try:
                db_data = json.loads(get_db)
            except Exception as e:
                cmds.warning(f'Could not load data for {db}')
                fixed_data = self.fix_json(odb)
                try:
                    db_data = json.loads(fixed_data)
                    print(f'Database has been repaired! {db}')
                    with open(db, 'w') as wdb:
                        json.dump(fixed_data, wdb, indent=4)
                except json.JSONDecodeError:
                    cmds.warning(f'Could not repair the database: {db}')
                    return None

    def fix_json(self, data):
        while data.strip().endswith('}'):
            data = data.strip()[:-1]
        if data.count('{') > data.count('}'):
            data += '}'
        return data

    def blow_away_snapshots(self, folder=None):
        success = False
        if folder:
            root_folder = folder
        else:
            proj_root = cmds.workspace(q=True, rd=True)
            scenes_folder = cmds.workspace(fre='scene')
            root_folder = os.path.join(proj_root, scenes_folder)

        result = cmds.promptDialog(
            title='Blow Away Snapshots?!!?',
            message='DANGER!\nBlow Away Snapshots will delete all snapshot files!\nIf called from a context menu it '
                    'will only delete snapshots within that folder, otherwise it does it for the entire project.\nThis '
                    'is not undoable!\nDo this only if you know you do not need them anymore and you just want to free '
                    'up some space!\nType "DELETE" in all caps if you really want to do this',
            button=['Accept', 'Cancel'],
            defaultButton='Cancel',
            cancelButton='Cancel',
            dismissString='Cancel',
            text=''
        )
        if result == 'Accept':
            input_value = cmds.promptDialog(q=True, text=True)
            if input_value == 'DELETE':
                success = True
                if os.path.exists(root_folder):
                    snaps_found = []
                    for root, dirs, files in os.walk(root_folder):
                        if 'snapshots' in root:
                            snaps_found.append(root)
                    if snaps_found:
                        for snap in snaps_found:
                            print(f'Deleting {snap}')
                            shutil.rmtree(snap)
                            print('Folder Deleted!')
        return success

