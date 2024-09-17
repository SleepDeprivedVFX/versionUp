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


class sp_toolkit(object):
    def __init__(self):
        """
        This may eventually need to process data from the config_file
        """
        pass

    def create_camera(self):
        """
        Creates a new camera using the film back and scene scale settings from the UI.  Asks for a focal length.
        :return:
        """
        # NOTE: filmback info can be acquired from the config
        filmback_w = float(self.ui.filmback_width.text())
        filmback_h = float(self.ui.filmback_height.text())
        mult_fb_w = (filmback_w / 10) / 2.54
        mult_fb_h = (filmback_h / 10) / 2.54
        # NOTE: Scene Scale can be acquired from the config
        scene_scale = float(self.ui.sceneScale.text())
        aspect_ratio = mult_fb_w / mult_fb_h
        # NOTE: base_name is tricky.
        base_name = self.ui.filename.text()
        # NOTE: show_code can be acquired from the config.
        show_code = self.ui.showCode.text()
        cam_name = f'{show_code}_{base_name}_shotCam'
        self.hide()
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

    def start_cam_bake(self):
        """
        This function starts the process of baking out the current scene camera and saves out an FBX into the Assets
        folder in a Shot_Cams sub-folder.
        :return:
        """
        # NOTE: This has no connection to the UI
        self.message(text='Baking Camera...', ok=True)
        bake_camera = self.cam_bake()
        if bake_camera:
            get_scene_name = cmds.file(q=True, sn=True)
            # NOTE: data doesn't have access to get_root_and_task() here.
            data = self.get_root_and_task(filename=get_scene_name)
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
            # NOTE: create_note and message aren't accessible here.
            self.create_note(notes=notes, output_file=output_file)
            self.message(text='Camera baked successfully: %s' % cam_name, ok=True)
        else:
            self.message(text='Camera could not be baked!', ok=False)

    def cam_bake(self):
        """
        This method does the actual baking of the shot camera.  It creates a duplicate camera, parents it in world space
        to the current scene camera and bakes out the keyframes for that camera.
        :return:
        """
        cam_transform = None
        all_cams = cmds.ls(ca=True)
        for cam in all_cams:
            # NOTE: no access to the UI here, but could get this from QSettings
            if self.ui.bakeCamSceneName.isChecked():
                # NOTE: no access to root_name here.
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
                    # NOTE: self.cameraNames are not currently accessible, but I want to isolate them anyways.
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
            # NOTE: cameraAttributes aren't accessible here, but I want to split them out anyways.
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

