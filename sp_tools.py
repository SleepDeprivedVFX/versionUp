# Sans-Pipe Maya Light Pipeline Utility - Toolkit

"""
This tool kit stores the functions that help run the SANS-PIPE UTILITY.  The idea here is that these tools can be used
in or out of the pipeline system, with, or without the main UI.
"""

__version__ = '1.3.11'
__author__ = 'Adam Benson'

import shutil

from maya import cmds
from maya import mel

import os
import sys
import re
import json
import time
from datetime import datetime
import configparser
import inspect
import math
import subprocess
import glob

try:
    from PySide6.QtCore import QSettings
    pyside_version = 6
    print('PySide6 detected.')
except ImportError:
    try:
        from PySide2.QtCore import QSettings
        pyside_version = 2
        print('PySide2 detected.')
    except ImportError:
        pyside_version = 0
        raise RuntimeError('Neither PySide 6 or PySide 2 detected!')

class sp_toolkit(object):
    def __init__(self):
        """
        Processing the global setups for the overall system
        """
        # Get the Maya version year dynamically
        maya_version = mel.eval("getApplicationVersionAsFloat();")
        maya_version_year = str(int(maya_version))

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
        # TODO: This will need to be changed for the mac version.
        self.ffmpeg_path = os.path.join(plugin_dir, 'bin', 'ffmpeg.exe')
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
        self.frame_rate_map = globVars['frame_rate_map']

        # Get the QSettings from the Super Saver
        self.settings = QSettings(__author__, f'Sans Pipe Super Saver {maya_version_year}')
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
                              vfo=0, ff='Fill', ovr=1, mb=0, sa=144, ncp=1, fcp=100000000, o=False, ow=30, pze=False,
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

    def viewer_setup(self, elements=None, wf=False, tx=True, ual=False, sh=True, ao=True, mb=True, aa=True):
        # Get the active viewer
        viewport = cmds.getPanel(wf=True)

        # Collect all the current settings.
        nurbsCurves = cmds.modelEditor(viewport, q=True, nurbsCurves=True)
        nurbsSurfaces = cmds.modelEditor(viewport, q=True, nurbsSurfaces=True)
        cv = cmds.modelEditor(viewport, q=True, cv=True)
        hulls = cmds.modelEditor(viewport, q=True, hulls=True)
        polymeshes = cmds.modelEditor(viewport, q=True, polymeshes=True)
        hos = cmds.modelEditor(viewport, q=True, hos=True)
        subdivSurfaces = cmds.modelEditor(viewport, q=True, subdivSurfaces=True)
        planes = cmds.modelEditor(viewport, q=True, planes=True)
        lights = cmds.modelEditor(viewport, q=True, lights=True)
        cameras = cmds.modelEditor(viewport, q=True, cameras=True)
        imagePlane = cmds.modelEditor(viewport, q=True, imagePlane=True)
        joints = cmds.modelEditor(viewport, q=True, joints=True)
        ikHandles = cmds.modelEditor(viewport, q=True, ikHandles=True)
        deformers = cmds.modelEditor(viewport, q=True, deformers=True)
        dynamics = cmds.modelEditor(viewport, q=True, dynamics=True)
        particleInstancers = cmds.modelEditor(viewport, q=True, particleInstancers=True)
        fluids = cmds.modelEditor(viewport, q=True, fluids=True)
        hairSystems = cmds.modelEditor(viewport, q=True, hairSystems=True)
        follicles = cmds.modelEditor(viewport, q=True, follicles=True)
        nCloths = cmds.modelEditor(viewport, q=True, nCloths=True)
        nParticles = cmds.modelEditor(viewport, q=True, nParticles=True)
        nRigids = cmds.modelEditor(viewport, q=True, nRigids=True)
        dynamicConstraints = cmds.modelEditor(viewport, q=True, dynamicConstraints=True)
        locators = cmds.modelEditor(viewport, q=True, locators=True)
        dimensions = cmds.modelEditor(viewport, q=True, dimensions=True)
        pivots = cmds.modelEditor(viewport, q=True, pivots=True)
        handles = cmds.modelEditor(viewport, q=True, handles=True)
        textures = cmds.modelEditor(viewport, q=True, textures=True)
        strokes = cmds.modelEditor(viewport, q=True, strokes=True)
        motionTrails = cmds.modelEditor(viewport, q=True, motionTrails=True)
        pluginShapes = cmds.modelEditor(viewport, q=True, pluginShapes=True)
        clipGhosts = cmds.modelEditor(viewport, q=True, clipGhosts=True)
        greasePencils = cmds.modelEditor(viewport, q=True, greasePencils=True)
        displayAppearance = cmds.modelEditor(viewport, q=True, displayAppearance=True)
        displayTextures = cmds.modelEditor(viewport, q=True, displayTextures=True)
        fogging = cmds.modelEditor(viewport, q=True, fogging=True)
        ssaoEnable = cmds.getAttr("hardwareRenderingGlobals.ssaoEnable")
        ssaoAmount = cmds.getAttr("hardwareRenderingGlobals.ssaoAmount")
        multiSampleEnable = cmds.getAttr("hardwareRenderingGlobals.multiSampleEnable")
        motionBlurEnable = cmds.getAttr("hardwareRenderingGlobals.motionBlurEnable")
        shadows = cmds.modelEditor(viewport, q=True, shadows=True)
        wireframeOnShaded = cmds.modelEditor(viewport, q=True, wireframeOnShaded=True)
        controllers = cmds.modelEditor(viewport, q=True, controllers=True)
        # lighting_mode returns either "default", "all", "active", "flat" or "none"
        displayLights = cmds.modelEditor(viewport, query=True, displayLights=True)

        # Create data
        data = {
            'UserViewportSettings': {
                'nurbsCurves': nurbsCurves,
                'nurbsSurfaces': nurbsSurfaces,
                'cv': cv,
                'hulls': hulls,
                'polymeshes': polymeshes,
                'hos': hos,
                'subdivSurfaces': subdivSurfaces,
                'planes': planes,
                'lights': lights,
                'cameras': cameras,
                'imagePlane': imagePlane,
                'joints': joints,
                'ikHandles': ikHandles,
                'deformers': deformers,
                'dynamics': dynamics,
                'particleInstancers': particleInstancers,
                'fluids': fluids,
                'hairSystems': hairSystems,
                'follicles': follicles,
                'nCloths': nCloths,
                'nParticles': nParticles,
                'nRigids': nRigids,
                'dynamicConstraints': dynamicConstraints,
                'locators': locators,
                'dimensions': dimensions,
                'pivots': pivots,
                'handles': handles,
                'textures': textures,
                'strokes': strokes,
                'motionTrails': motionTrails,
                'pluginShapes': pluginShapes,
                'clipGhosts': clipGhosts,
                'greasePencils': greasePencils,
                'displayAppearance': displayAppearance,
                'displayTextures': displayTextures,
                'fogging': fogging,
                'shadows': shadows,
                'wireframeOnShaded': wireframeOnShaded,
                'controllers': controllers
            },
            'UserHardwareSettings': {
                'ssaoEnable': ssaoEnable,
                'ssaoAmount': ssaoAmount,
                'multiSampleEnable': multiSampleEnable,
                'motionBlurEnable': motionBlurEnable
            },
            'UserLightsSettings': {
                'displayLights': displayLights
            },
            'Viewer': viewport
        }

        # Make display adjustments.
        attributes = data['UserViewportSettings']
        user_lights = data['UserLightsSettings']
        hardware = data['UserHardwareSettings']
        if elements == 'Geometry Only':
            for attr, val in attributes.items():
                if (attr is not 'polymeshes' or attr is not 'nurbsSurfaces' or attr is not 'subdivSurfaces' or
                        attr is not 'planes'):
                    cmds.modelEditor(viewport, edit=True, **{attr: False})
                else:
                    cmds.modelEditor(viewport, edit=True, **{attr: True})
        elif elements == 'Geometry and Splines':
            for attr, val in attributes.items():
                if (attr is not 'polymeshes' or attr is not 'nurbsSurfaces' or attr is not 'subdivSurfaces' or
                        attr is not 'planes' or attr is not 'nurbsCurves' or attr is not 'controllers'):
                    cmds.modelEditor(viewport, edit=True, **{attr: False})
                else:
                    cmds.modelEditor(viewport, edit=True, **{attr: True})
        elif elements == 'Geometry, Splines and Joints':
            for attr, val in attributes.items():
                if (attr is not 'polymeshes' or attr is not 'nurbsSurfaces' or attr is not 'subdivSurfaces' or
                        attr is not 'planes' or attr is not 'nurbsCurves' or attr is not 'controllers' or
                        attr is not 'joints' or attr is not 'ikHandles' or attr is not 'dimensions'):
                    cmds.modelEditor(viewport, edit=True, **{attr: False})
                else:
                    cmds.modelEditor(viewport, edit=True, **{attr: True})
        else:
            for attr, val in attributes.items():
                cmds.modelEditor(viewport, edit=True, **{attr: True})

        # Set user playblast render settings
        if wf:
            cmds.modelEditor(viewport, edit=True, wireframeOnShaded=True)
        if tx:
            cmds.modelEditor(viewport, edit=True, displayTextures=True)
        if ual:
            cmds.modelEditor(viewport, edit=True, displayLights='all')
        if sh:
            cmds.modelEditor(viewport, edit=True, shadows=True)
        if ao:
            cmds.setAttr('hardwareRenderingGlobals.ssaoEnable', True)
            cmds.setAttr('hardwareRenderingGlobals.ssaoAmount', float(hardware['ssaoAmount']))
        if mb:
            cmds.setAttr('hardwareRenderingGlobals.motionBlurEnable', True)
        if aa:
            cmds.setAttr('hardwareRenderingGlobals.multiSampleEnable', True)

        # Send the collected data back
        return data

    def basic_playblast(self, fmt=None, codec=None, so=False, slate=True, burn=True, data=None):
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
        start_frame = cmds.playbackOptions(q=True, min=True)
        end_frame = cmds.playbackOptions(q=True, max=True)

        # Get the camera focal length
        viewport = data['Viewer']
        active_camera = cmds.modelPanel(viewport, q=True, camera=True)
        focal_length = cmds.getAttr(f'{active_camera}.focalLength')

        if slate or burn:
            pass_fmt = fmt
            pass_codec = codec
            fmt = 'image'
            codec = 'png'
            ext = '.png'
        else:
            pass_fmt = fmt
            pass_codec = codec
            if fmt == 'qt':
                ext = '.mov'
            elif fmt == 'avi':
                ext = '.avi'
            else:
                ext = f'.{codec}'
        filename = basename + ext
        tracking_db = os.path.join(movies_folder, basename, 'db')
        if not os.path.exists(tracking_db):
            os.makedirs(tracking_db)
        tracking_db = os.path.join(tracking_db, f'{basename}_db.json')

        if slate or burn:
            output_folder = os.path.join(movies_folder, basename, 'temp')
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            output = os.path.join(output_folder, filename)
            final_output = os.path.join(movies_folder, basename, filename)
        else:
            output_folder = os.path.join(movies_folder, basename)
            if not os.path.exists(output_folder):
                os.makedirs(output_folder)
            output = os.path.join(output_folder, filename)
            final_output = output
        output = output.replace('\\', '/')
        final_output = final_output.replace('\\', '/')

        if pyside_version == 6:
            pb = cmds.playblast(
                format=fmt,
                filename=output,
                sequenceTime=0,
                clearCache=1,
                viewer=0,
                showOrnaments=so,
                fp=4,
                percent=100,
                compression=codec,
                quality=80,
                widthHeight=(res_width, res_height),
                exposure=0,
                gamma=1,
                fo=True
            )

        elif pyside_version == 2:
            pb = cmds.playblast(
                format=fmt,
                filename=output,
                sequenceTime=0,
                clearCache=1,
                viewer=0,
                showOrnaments=so,
                fp=4,
                percent=100,
                compression=codec,
                quality=80,
                widthHeight=(res_width, res_height),
                fo=True
            )
        else:
            cmds.error('Unable to playblast.  Sorry.')
            return False

        pb = os.path.join()
        with open(tracking_db, 'w') as tracking:
            tracking_data = {
                'output_folder': output_folder,
                'raw_playblast': pb,
                'format': pass_fmt,
                'codec': pass_codec,
                'final_playblast': final_output,
                'start_frame': start_frame,
                'end_frame': end_frame,
                'focal_length': focal_length
            }
            tracking_out = json.dumps(tracking_data, indent=4)
            tracking.write(tracking_out)
            tracking.close()

        return tracking_db

    def compile_playblast(self, viewer_data=None, playblast_data=None, notes=None, slate=True, slate_notes=None,
                          burn=True):
        """
        This creates the ffmpeg output files with the slate and burn ins on them.
        :param viewer_data: (dict) a pass-through of data that needs to be restored once the playblast is done.
        :param playblast_data: (dict) information about the playblast that was created. It includes:
                                output_folder: The folder where the playblast was written to.
                                raw_playblast: the basic_playblast that was created
                                format: the users chosen output format
                                codec: the users chosen output codec
                                final_playblast: this is where the output will be saved and what it will be called.
                                start_frame: the original start frame of the playblast
                                end_frame: the original end frame of the playblast
                                focal_length: The playblast camera's focal length
        :param notes: (dict) The notes file associated with the file being playblasted.  Mostly used for the following:
                                filename: Original filename of the file being playblasted
                                user: the user creating the playblast
                                computer: Computer used to make the playblast
                                details: This is a maybe, since we'll be getting notes from the slate_notes
        :param slate: (bool) Whether to create a slate
        :param slate_notes: (str) a custom note just for the slate frame.  It the slate is not active, this is None
        :param burn: (bool) Whether to create a burn in
        :return: The final_playblast
        """
        # Setup the primary data from the information passed.
        output_folder = playblast_data['output_folder']
        raw_playblast = playblast_data['raw_playblast']
        fmt = playblast_data['format']
        codec = playblast_data['codec']
        final_playblast = playblast_data['final_playblast']
        final_playblast = final_playblast.replace('\\', '/')
        base_folder = os.path.dirname(final_playblast)
        build_folder = os.path.join(base_folder, 'build')
        base_folder = base_folder.replace('\\', '/')
        build_folder = build_folder.replace('\\', '/')
        start_frame = float(playblast_data['start_frame'])
        end_frame = float(playblast_data['end_frame'])
        focal_length = f'{playblast_data["focal_length"]}mm'
        original_filename = notes['filename']
        artist = notes['user']
        computer = notes['computer']
        task_data = self.get_data()
        shot_asset_name = task_data['root_name']
        task = task_data['task_name']

        # Create TRT and Timecodes
        get_frame_units = cmds.currentUnit(q=True, time=True)
        frame_rate = float(self.frame_rate_map.get(get_frame_units, 'Unknown'))
        frame_trt = end_frame - start_frame + 1
        trt = self.create_timecode(frame=frame_trt, frame_rate=frame_rate)

        if slate:
            # Create the slate frame
            slate_frame_path = os.path.join(build_folder, 'slate_frame.png')

            # Construct the slate info
            slate_info = f'Shot: {shot_asset_name}\n'
            slate_info += f'Filename: {original_filename}\n'
            slate_info += f'Task: {task}\n'
            slate_info += f'Artist: {artist}\n'
            slate_info += f'Computer: {computer}\n'
            slate_info += f'Focal Length: {focal_length}\n'
            slate_info += f'Frame Range: {start_frame} - {end_frame}\n'
            slate_info += f'Total Frames: {frame_trt}\n'
            slate_info += f'TRT: {trt}\n'
            slate_info += f'NOTES: {slate_notes}'

            # Create the FFmpeg command with varying font sizes
            drawtext_commands = []
            drawtext_commands.append(
                f"drawtext=text='{slate_info[0]}':x=10:y=10:fontcolor=white:fontsize=60")  # Top line with 60px font

            # Subsequent lines with 48px font
            for i, line in enumerate(slate_info[1:], start=1):
                drawtext_commands.append(f"drawtext=text='{line}':x=10:y={10 + (i * 50)}:fontcolor=white:fontsize=48")

            # Join all drawtext commands
            drawtext_filter = ",".join(drawtext_commands)

            # Create the slate frame using FFmpeg
            command = [
                self.ffmpeg_path,
                "-f", "lavfi",
                "-i", "color=c=black:s=1280x720:d=1",  # Background color and size
                "-vf", drawtext_filter,
                slate_frame_path
            ]

            try:
                subprocess.run(command, check=True)
                cmds.warning("Slate frame created successfully.")
            except subprocess.CalledProcessError as e:
                cmds.warning(f"Failed to create slate frame: {e}")

        if burn:
            os.makedirs(build_folder, exist_ok=True)
            frame_files = self.collect_playblast_files(output_folder=output_folder)
            for frame_file in frame_files:
                frame_number = self.extract_frame_number(filename=frame_file)
                burn_in_frame_path = os.path.join(build_folder, f'burn_in_{frame_number:04d}.png')
                burn_in_frame_timecode = self.create_timecode(frame=frame_number, frame_rate=frame_rate)

                # Build burn in text
                burn_in_text = (
                    f'{original_filename}'
                    f'{frame_number}'
                    f'trt: {burn_in_frame_timecode}'
                    f'{focal_length}'
                )

                # FFMPEG command
                command = [
                    self.ffmpeg_path,
                    "-i", frame_file,
                    "-vf", f"drawbox=y=h-100:color=black:t=fill, drawtext=text='{burn_in_text}':x=10:y=h-90:fontcolor=white:fontsize=48",
                    burn_in_frame_path
                ]

                try:
                    subprocess.run(command, check=True)
                    cmds.warning(f'Burn-in frame created: {burn_in_frame_path}')
                except subprocess.CalledProcessError as e:
                    cmds.warning(f'Failed to burn-in frame: {e}')

    def extract_frame_number(self, filename=None):
        match = re.search(r'_(\d+)|\.(\d+)', filename)
        if match:
            return match.group(1) or match.group(2)
        return None

    def collect_playblast_files(self, output_folder=None):
        frame_files = glob.glob(os.path.join(output_folder, '*.png'))
        return frame_files

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

    def create_timecode(self, frame=0.0, frame_rate=24.0):
        """
        Create a time code from a frame number
        :param frame: The current frame, or the TRT
        :param frame_rate: Maya Frame Rate
        :return:
        """
        # Calculate total seconds
        total_seconds = frame / frame_rate

        # Convert total_seconds into hours, minutes, and seconds
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        # Calculate remaining frames (fractional part of the second)
        frames = int((total_seconds - int(total_seconds)) * frame_rate)

        # Format the timecode string as HH:MM:SS:FF
        timecode = f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"

        return timecode
