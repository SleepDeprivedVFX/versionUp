# Sans-Pipe Maya Light Pipeline Utility - Toolkit

"""
This tool kit stores the functions that help run the SANS-PIPE UTILITY.  The idea here is that these tools can be used
in or out of the pipeline system, with, or without the main UI.
"""

from maya import cmds
import os
import sys
import re
import json
import time
from datetime import datetime
import configparser

try:
    from PySide6.QtCore import QSettings
    print('PySide6 detected.')
except ImportError:
    try:
        from PySide2.QtCore import QSettings
        print('PySide2 detected.')
    except ImportError:
        raise RuntimeError('Neither PySide 6 or PySide 2 detected!')

# Temporary fix.  This gets removed when it gets ported over to the working drive
shit_path = 'c:/users/sleep/onedrive/documents/scripts/python/maya/utilities/sansPipe/'

__version__ = '1.3.0'
__author__ = 'Adam Benson'


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
        # NOTE: this is temporary
        sp_global_vars = os.path.join(shit_path, 'sp_global_vars.json')
        sp_global_vars = sp_global_vars.replace('\\', '/')
        with open(sp_global_vars, 'r') as global_vars:
            globVars = json.load(global_vars)
        # Set the project constants.
        self.tasks = globVars['tasks']
        self.invalidCharacters = globVars['invalidCharacters']
        self.cameraNames = globVars['cameraNames']
        self.cameraAttributes = globVars['cameraAttributes']

        # Get the QSettings from the Super Saver
        self.settings = QSettings(__author__, 'Sans Pipe Super Saver')
        self.appendartist = self.settings.value('appendArtist', None, type=bool)
        self.bakeCamSceneName = self.settings.value('bake_cam_scene_name', None, type=bool)

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
        # NOTE: base_name is tricky.
        base_name = self.ui.filename.text()
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
            focal_length = 35.0
            self.show()
            return False
        self.show()
        new_cam = cmds.camera(vfa=mult_fb_h, hfa=mult_fb_w, ar=aspect_ratio, fl=focal_length, coi=5, lsr=1, hfo=0,
                              vfo=0, ff='Fill', ovr=1, mb=0, sa=144, ncp=1, fcp=10000000, o=False, ow=30, pze=False,
                              hpn=0, vpn=0, zom=1)
        new_cam_parent = cmds.listRelatives(new_cam, p=True)
        cmds.select(new_cam_parent, r=True)
        cmds.rename(cam_name)
        cmds.scale(scene_scale, scene_scale, scene_scale)

    def start_cam_bake(self, data=None):
        """
        This function starts the process of baking out the current scene camera and saves out an FBX into the Assets
        folder in a Shot_Cams sub-folder.
        :return:
        """
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
                cmds.warning(f'Could not bake the camera!  Could be a permissions issue, or some other failure: {e}')
                self.message(text='Could NOT bake camera! Make sure Folder Permissions are set in your OS!', ok=False)
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

