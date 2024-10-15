# Sans Pipe - Light Pipeline Utility for Maya version 1.3.11

## Description
Sans Pipe is a light pipeline utility designed specifically for Maya 2022 and above, aimed at enhancing project organization and efficiency. It provides a robust set of tools that streamline project workflows, including file versioning with notes, snapshot taking, file publishing, reference tracking, camera baking, asset and shot creation, playblasting animations, and asset exporting.

## Features
- **Version Control:** Automatically versions up Maya files with accompanying notes for better tracking.
- **Snapshot Taking:** Captures file snapshots for incremental backups or version comparison.
- **Publishing Tools:** Simplifies the process of publishing files for production.
- **Reference Tracking:** Ensures all references are up-to-date and correct.
- **Project Archiving:** Package only what you need and zip it into one light weight super archive!
- **Camera Baking:** Tools for baking out camera movements for export or further processing.
- **Asset and Shot Creation:** Facilitates the creation and organization of assets and shots within Maya.
- **Playblasting:** Integrated playblasting tools for previewing animations directly within Maya.

## Prerequisites
- **Autodesk Maya**: Designed for **Maya 2025**, but is compatible with **Maya 2022** and above.
- Requires Python 3 and PySide2 or PySide 6 (preferred)

## Installation
1. **Prepare the Installation Directory:** 
- Navigate to your Maya plugins directory, typically found at: 
  ``` 
  /Users/[YourUsername]/Documents/maya/20XX/plug-ins/
  ```  
2. Create a new folder named `sansPipe` within this directory and drag the contents of the SansPipe folder into that folder.  There should only be one sansPipe folder.  Alternately, you could drag the sansPipe folder into your `plug-ins` folder and then move the `userSetup.py` to the same location as in step 3.

3. **Copy Files:**
- Except for `userSetup.py`, copy all files from the provided package into the `sansPipe` folder you just created.

4. **Setup User Scripts:**
- Copy the `userSetup.py` file to your Maya scripts folder, usually located at:
  ```
  /Users/[YourUsername]/Documents/maya/20XX/scripts/
  ```

5. **Restart Maya:** 
- Close and reopen Maya to complete the setup.
- Make sure the plug-in is loaded in your Maya Plug-Ins Manager

## Usage
  **User Interface**

## Save - Publish - Snap Tab
  - The first tab of sansPipe is your main workflow utility.  While there are a lot of features on here, it is actually designed to be very minimalistic.  By default SansPipe should open when Maya opens, allowing you to start working right off the bat.  This feature can be turned off in the settings.
  - Here are the main sections of the first tab of SansPipe.
![Save - Publish - Snap](https://github.com/SleepDeprivedVFX/versionUp/blob/master/images/sansPipe_Tab1.png?raw=true)
1. This is what sansPipe is *going* to save your next file as.  By default, this is a "version up" tool, and this is it's primary feature
2. This controls how the automatic naming convention works.  99% of the time, you'll never have to deal with this, and it is recommended that you leave it on "Auto".
   1. The simplest way to change tasks, i.e. Previs to Animation, is to simply change the **Task Type** drop-down menu from **previs** to **anim**.  SansPipe will automatically change the **Save As...** output to the correct task path and version number.
   2. To create a custom name and output, change the **Naming** radio buttons from **Auto** to **Custom**.  This unlocks the rest of the naming tools and allows you to create your own filename.  After that, sansPipe will automatically track its new version number and continue with your custom naming.![Custom Naming Panel](https://github.com/SleepDeprivedVFX/versionUp/blob/master/images/sansPipe_CustomName_settings.png?raw=true)
   3. If you want to add the artists name (First Initial and Last Name) to the output filename, simply check the **Append Artist** checkbox.  The **Artists Name** field is automatically generated from the computer's log in credentials, but can be set manually by changing it in the field.
   4. **Allow File Copy From --> To** checkbox is a special feature that allows you to save a current file as a completely other shot or asset.  This is mainly used if you have, for instance, a **layout** file that gets saved to every shot in a sequence.  Instead of importing your assets for every shot, you can simply check this, select the next shot in the shot tree, and sansPipe will automatically rename your shot from there.  More about that in the **Shot Tree** section below.
   5. The **Base Name** is the most rudimentary description of your file name.  For instance, if your **Show Code** is "BDD" and your **Task Type** is "previs", then the only thing you would put in here is the simplest name of the asset/shot - "Shot_0010" or "RowBoat".  sansPipe handles the rest of the naming convention from there.
   6. The **Show Code** is automatically generated from the Maya Project name, but can be manually changed in the **Show Settings** (More about that later).  This is a basic 3 letter code to tag on to your files for easy identification.
3. **Notes** is a multi-purpose section.  You must put in notes for just about everything you do.  This is forced for good record keeping and tracking across the project.
   1. When **Saving V Up** (Short for Saving Version Up)
   2. When **Publish**ing a file.
   3. When creating a **Snapshot**
   4. When changing the **Task Status**
4. The **Recent Files** list mirrors Maya's own *Recently Opened* files.  Simply double click one of the files in the stack to quickly open it.  If you want to clear it out, hit the **Clear Recent History** button and it will flush the list.  You can also set how many items appear in this list from the **Settings**
5. **Existing Files** list shows everything within your Maya Project's *Scenes* folder.  Whether created through SansPipe or not.  If you're using SansPipe to build your project from scratch, it will automatically create special folders for you for organizing **Characters (Char)**, **Cameras (Cams)**, **Environments (Env)**, **Props**, **Vehicles (Veh)** and **Shots**.  If the shots and assets are also created through SansPipe, then task folders are also generated and will appear in this stack.  A few things to note about the **Existing Files** tree:
   1. Items are color coded based on their **Task Status**
   2. A Camera icon appears if there is a Playblast associated with that shot.
   3. Right-Click options become available on files in the tree.  The options are:
      1. ![Existing File Right Click](https://github.com/SleepDeprivedVFX/versionUp/blob/master/images/sansPipe_EF_RightClick_1.png?raw=true)  
      2. **Open** does what you would expect, however, when you open a file from here, whether using the right-click option or by double clicking the file itself, it opens the file, but also sets the **Task Status** to "In Progress".
      3. **Open No Status Update** works the same way as open, except it does not change the current **Task Status**.  This is useful if you have a file marked "Needs Revision", "Done", or "For Review" and you want to leave that task status as is.
      4. **View Playblast** only works if there is an associated playblast, indicated by the Camera Icon ![Camera Icon](https://github.com/SleepDeprivedVFX/versionUp/blob/master/icons/cam_icon.png?raw=true)
      5. **Blow Away Snapshots** is a tool for deleting all the **Snapshots** associated with a particular file.  Snapshots are simply date-stamped copies of your working file, and thus take up space.  If you are sure you are through with your Snapshots, you can delete them for a given task by using this feature.  More about this later.
   4. The **Task Status** drop down sits at the top of the **Existing Files** tree.  It updates based on the current selection in the tree.  By manually changing it (You must add a note to do this) it will change the status of the selected file and record that into the version notes.
   5. If you are using the **Allow File Copy From --> To** feature in the *Section 2* Naming convention form, this is where that takes place.  By first clicking that checkbox, and then selecting an asset or shot name (top folder of that stack, for instance, select "BDD_Shot_0020") and it will rename your file to that, but only if that checkbox is selected first.
6. **Snapshots**.  Snapshots are wonderful things!  You should create Snapshots often instead of saving a version up.  **Snapshots** are basically versioning up a file, without versioning up a file.  They require a *Note* to be saved.  Here's some cool stuff about **Snapshots**:
   1. A Snapshot saves where you're at right now with a working file, let's call it BDD_Shot_0010_anim_v001.  You can start with your initial import of objects and do a quick Snapshot.  Add a note like, "Importing the assets" then hit the **Snapshot** button or use the hotkey **Alt + S**  (Option + S on Mac). A snapshot is created and will show up with a date stamp in the **Snapshots** stack.
   2. Now, you do some blocking animation, really basic stuff, no finesse.  Do another snapshot.  Put in a note like "Basic blocking" and then hit **Snapshot**.  A new Date stamped file shows up in the stack.
   3. One more **snapshot**, "First pass animation".  Now let's say that you hate it, and want to go back to that initial import...
   4. Drop down that first snapshot in your stack, and you'll see your first "Importing the assets" note.  Double click that note and suddenly your file will go back to its initial state.  If you have unsaved changes in your current file, it will pop up a message asking if you'd like to Snapshot your current place.  Do it - it can't hurt.
   5. Now your file is back to your initial import, and you can do another pass at blocking, animation, or whatever it is you want to redo.
   6. Now, if you decide that it was better the first time, simply go to your "First Pass Animation" snapshot and double click it.  It will return your file to that state.
   7. All of this and you never left version 1!  **Snapshots** are your friend!  USE THEM!
   8. That being said, they do take up space.  If you decide you're done with your snapshots, go to that right-click menu in the **Existing Files** tree and right click and chose "Blow Away Snapshots" and they will be deleted.
7. **Version Notes**  This is just a display for any notes created for publishes, version or task status updates.  It displays the file name, the user/artist, the computer they worked on, the date and time of the note and the current status.  Below that, any notes or status update notes will be displayed.  Any item you select in the **Existing Files** tree will display its associated notes in here.
8. **Buttons**
   1. **Publish** button.  Default hotkey (Ctrl + p).  Publishes the current file.  Publishing is an elaborate process that works like this:
      1. When Publish is pushed (A note is required!) then your current working file is versioned up to the next available version - thus ..anim_v001 becomes ..anim_v002
      2. A copy of the ..anim_v001 file is saved to the "Publishes" folder in your Maya project folder structure, and the tag **PUB** is added to the file name, for example ..anim_PUB_v001
      3. The Published file imports all references and removes the namespaces, unless more than one copy of an object exists in the original references.  For instance, NSChar1:Character_1.ma, NSChar2:Character_1.ma.  Those namespaces will be maintained.  The reason for stripping out as many namespaces as possible and importing the references is to avoid too many nested namespaces and too many nested references.
      4. Once published, the versioned up ...anim_v002 working file is reopened.
      5. The newly published file will now show up in the **Tools - References - Assets** Tab in the **Publishes** tree.
   2. **Snapshot** button.  Default Hotkey (Alt + s).  Takes a snapshot as discussed above
   3. **Save V Up** button.  Default Hotkey (Ctrl + Shift + v).  Saves the next version up for your file using the filename from section 1 of this tab.
   4. **Close** button.  Default Hotkey (Esc).  Does what you'd expect, but with the added benefit of saving out settings as it closes the tool.
9. **SansPipe Tabs** These are the tabs that cycle through different sections of the SansPipe workflow. 

## Tools - References - Asset
- The second tab of SansPipe.  This tab contains a list of tools, is where you create assets and shots, where you reference in published assets or load in exported assets.
- Below is the breakdown for this tab
![Tools - References - Assets](https://github.com/SleepDeprivedVFX/versionUp/blob/master/images/sansPipe_Tab2.png?raw=true)
1. **Tools**.  The Tools section holds a list of simple tools that correspond to other features within SansPipe.  These are designed to work with SansPipe and its organizational system.
   1. **Bake Camera**.  This button and its associated checkbox "**Use Shot/Asset as Cam Name**" will take your current shot camera and bake it out for use in other software, or in other scenes, as an FBX stand-alone camera in world space.  If the "Use Shot/Asset as Cam Name" checkbox is activated, then it puts that information into the camera name so that it can be easily identified if there are multiple cameras imported into a scene.  This tool is usefull if you'll be using the cameras in Nuke, Unreal or some other DCC.  Baked Cameras are saved in a "Shot_Cams" sub folder under the Maya project's **assets** folder.
   2. **Create Camera**.  This creates a standard Maya camera, but it does it with settings that are set in the SansPipe **Show Settings** sub-tab under the **Settings - Configuration** tab.  In that tab you can set things like standard camera film back, resolution, aspect ratio and scene scale.  This is useful to insure that all the cameras match a show's particular film style and live-action camera setup.
   3. **Publish Selection as FBX**, **Publish Selection as OBJ** and **Publish Selection as Alembic** will export any selected object into Maya's **assets** folder.  If nothing is selected, they export the entire scene as either FBX, OBJ or ABC (Alembic) files.
   4. **Playblaster**.  It is a good idea to use this option to playblast your files, instead of the Maya default playblaster for a few good reasons.
      1. It makes sure that the playblast name is correct and associates it with whatever scene file has created it.  This allows it to be access in the **Existing Files** tree by right-clicking and chosing "View Playblast".
      2. It uses the **Show Settings** from the **Show Settings** sub-tab in the **Settings - Configuration** tab to put everything in a consistent format.
      3. The advanced playblast features can add burn ins that accentuate each playblast with better details than you'll get out of a standard playblast.
   5. **Build Default Folders**.  This feature simply creates a default folder set for Maya.  It does not create the entire project folder structure, however. What it does is generate the basic Char, Cams, Props, Veh, Env and Shots folders.  All of these are created automatically if you're using the **Create Asset/Shot** sections of this tab, or if you're creating your initial project in the **Project Settings** tab.
   6. **Blow Away Snapshots**.  This is the same feature as the right-click **Blow Away Snapshots** from the **Existing Files** tree, except it deletes all snapshots from the entire project.  This is a feature that's best reserved for when you're totally done, and you're ready to archive your entire project.
2. **Create Asset / Shot**.  This section is for the clean creation of new assets or shots.  It is very simple, but has powerful functionality.  Individual assets or shots can be created, or an entire list of shots and assets can be created by browsing for a specifically formatted CSV file.  Here's how it all breaks down:
   1. To create a new Shot or Asset first pick the **Type** from the drop-down.  The options are:
      1. Char (Character)
      2. Env (Environment)
      3. Prop
      4. Ven (Vehicle)
      5. Cam (Camera)
      6. Shots
   2. Then give it a simple name: Harry, Wanda, Gun, Rowboat, Shot_0010, 0020, ShotCam
   3. Push **Make Asset/Shot**
   4. Using this feature will create all the task folders into the proper structure for their type: Shots in Shots, Chars in Chars, so forth and so on.  Furthermore, using this feature will do the following:
      1. For Non-Shot assets they will receive asset task folders, and for shots, they will receive shot tasks
      2. The Asset types will automatically create a **model** file and create a standard 1 meter cube based on the scene scale set in the SansPipe **Show Settings**.  Shots types will get the same 1 meter cube, but in a **layout** file.
      3. The new files statuses will be set to "Ready".
   5. If, on the other hand, you use the **Bulk Add from CSV** feature, then everything above in this section gets ignored and all of the shots/assets are created from the CSV file.  Here's how this works:
      1. Create a CSV file in Excel, or even in Notepad - remember CSV stands for "Comma Separated Values", so as long as there are commas and new lines in the document, this should work.  Excel is your best bet though as you can build your document there and then export it as a CSV.
      2. The CSV file can ONLY have two columns in each row!
      3. There should be NO HEADER!  It should look like this:
         1. Harry, Char 
         2. Rowboat, Veh
         3. Shot_0010, Shots
         4. Shot_0020, Shots
         5. Hammer, Prop
         6. Castle, Env
      4. It should use the same **Type** abbreviations as the main system.  It will still work if you use anything else, it will just create those as folders and track it as such.  You could create a "type" called *Hamburger, Food* and you would end up with a *food* folder with the asset hamburger under it, and SansPipe would track it the same way it does anything else, but ew...  Keep it clean.  That's what this tool is all about.
3. **Loaded References**.  This area tracks any references that you have in your scene file.  This works best if you use the Publishing system on the first tab, and load assets in using the **Publishes** section of this tab.  Here are some details about this:
   1. This section looks for asset/reference version numbers.  If a version number is out of date it does the following:
      1. SansPipe automatically opens to this tab to show you that you have out of date assets
      2. It highlights the out of date references RED and puts a check mark next to its name.
      3. You can uncheck assets that you don't want to update.
   2. Assets that are up-to-date are highlighted green and the SansPipe window will open to the first tab.
   3. If you have out of date assets, you can click the **Update Selected** button at the bottom of the section and it will update any referenced asset that still has the checkmark next to it.  Even if an up-to-date reference is checked, it will be ignored by this process.  Only out-of-date references will be updated.
4. **Publishes**.  This section lists only items that are properly published through the SansPipe system.  You can manually add items to the *publishes* folder created by SansPipe and they will show up here as well, but it is designed to work with the publishing process.  With this tool you can reference in assets or import them into the scene.  Referencing is recommended as that allows for things to be updated on the fly, and it keeps smaller file sizes over-all, especially for snapshots.  The publishing section has a right-click context menu that mirrors the two buttons in its section.  The only kinds of files that show up here are Maya files.
5. **Assets**.  This section works the same way as the **Publishes** section with the main difference being that it is looking at Maya's default *assets* folder and is primarily for giving you access to OBJ, FBX and ABC files, or anything else that has been exported, but not published.  It has the same right click functionality as the **Publishes** section, and any references with proper version numbers will be tracked in the **Loaded References** section.

## Project Settings
- **Project Settings** tab allows you to manage your Maya projects in the same way that you would using the default Maya project settings, except that it adds features that do not come with Maya by default, making it cleaner and more organized.
- Below is the breakdown for this tab
![Project Settings](https://github.com/SleepDeprivedVFX/versionUp/blob/master/images/sansPipe_Tab3.png?raw=true)
1. **Recent Projects**.  This works like the **Recent Files** from the first tab.  It keeps a record of any recently used projects.  Double click any one of these to quickly change your projects.
2. **Project**.  This section mirrors Maya's own "Set Project" feature.  You can browse to any existing project, whether it was created using SansPipe or not, and it will make that your current project and add it to the **Recent Projects** stack to the left.
3. **New Project**.  This feature mostly mirrors Maya's default "Project Window" feature, with the added detail that it creates extra folders for Publishes and organizational folders for Assets and Shots.  This is a better way to organize your workflow in Maya.  It is recommended that new projects are created here in SansPipe.
   1. The **Include Subfolders** checkbox is checked by default.  This is the feature that automatically creates Char, Prop, Veh, Env and Shots folders. 

## Settings - Configuration
**Sub Tabs**
- The system settings are broken down into a series of Sub-Tabs that separate out all the different function of SansPipe
## Show Settings
- The **Show Settings** sub-tab covers all the basic show specific settings like the name of the show, the three (3) letter code for the show, default render / camera resolution, the camera film-back, default render format and the scene scale.  Other features will be added in future versions of SansPipe.
- Below is the breakdown for this tab
![Show Settings](https://github.com/SleepDeprivedVFX/versionUp/blob/master/images/sansPipe_Tab4a.png?raw=true)
1. **Show Name**.  By default, this uses the Maya Project folder name, however it can be changed to anything you like after the initial opening of SansPipe.  SansPipe creates a **showConfig.cfg** file at the root of your Maya project to store all of these project configurations, and thus is able to remember them later on.
2. **Show Code**.  This is the primary three (3) letter code identifier for the project.  It gets appended as a prefix to anything that is done for the project in SansPipe.  This way, shots and assets are always tagged to a specific show, so, even if you use them in a different show, you know where they came from.  This three-letter code is automatically generated from the Maya Project folder name, however, it can be changed to anything you like later on.
3. **Default Resolution**.  This sets both the default render output resolution as well as the playblast setting resolution.  The default setting is 2048x1152, but you can set it to anything you like for your project.
4. **Default Filmback**.  This is important for your camera settings.  Many shows mirror live-action cameras, in which case, this setting is invaluable for maintaining proper cameras in your project.  Using the **Create Camera** tool here insures that the camera settings are correct.  This is also important, because focal lengths behave differently depending on the filmback settings of your camera.  For instance, a 50mm lens will look different on a camera that uses Academy Full Aperture vs. a camera that is using Super 8 Filmback.
5. **Default Render Format**.  This sets the default render output for your project.  Future versions will include more settings to make render defaults more unified.
6. **Scene Scale**.  This sets the default unit size for your project.  Under the hood, Maya's default units are 1/10th real world scale, thus 1 meter is actually 1 decimeter and 1 cm is actually 1 mm.  Here, the default setting of **10** scales things up so that 1 cm = 1 cm.  This affects the following settings in SansPipe:
   1. **Create Camera** - Scales the camera up by this **Scene Scale**
   2. **Create Asset / Shots** - the 1 meter cube created in the default *model* or *layout* files uses this setting to set its apparent scale in the Maya project.  In the future, this may also affect things like Nucleus physics and other settings that rely on scene scale.
7. **Save Configuration** button.  Whenever you change anything in any of the **Settings - Configuration** tabs, it is important to hit the **Save Configuration** button as that triggers the saving of the *showConfig.cfg* file, and ultimately, your settings.
8. **Sub Tabs** These are the sub-tabs that control the other settings.  Each section will be described below.

## Playblast Settings
 - These playblast settings override your default Maya settings and return your scene to their original state once the playblast is finished running.
- Below is the breakdown for this tab
![Playblast Settings](https://github.com/SleepDeprivedVFX/versionUp/blob/master/images/sansPipe_Tab4b.png?raw=true)
1. **Scene Elements**.  This attempts to minimize how much thought has to be put into your playblast.  In Maya, you have much more control over this, but often its tedious just to get some basic things done.  This compiles those into a list of common playblast settings.  It breaks them down into the following:
   1. **Geometry Only** - Only shows geometry
   2. **Geometry and Splines** - Only shows Geometry and Spline Curves
   3. **Geometry, Splines and Joints** - Keeps it minimal for rigging demos, showing geo, splines and joints.
   4. **Everything** - Basically turns "All" on in Maya's viewport settings.
2. This block of settings mirrors Maya's viewport settings and turns certain ones on by default to help pretty-up your playblasts.  You can change any of them at any time, just be sure to hit "Save Configuration".  There is one additional feature here that is not a part of Maya's default:
   1. **Burn In** - This creates a rudimentary scene burn in, and makes sure some HUD elements are active.  It displays the Filename, Focal Length, Show Code, Time Code and other pertinent information.

## Hotkeys
- This section needs little description.  A few default hotkeys are set for SansPipe, however, any of these can be set and changed to whatever you like here.  They function separately from Maya's default hotkeys accept for one.
- Below is the breakdown for this tab
![Hotkeys](https://github.com/SleepDeprivedVFX/versionUp/blob/master/images/sansPipe_Tab4c.png?raw=true)
1. The first hotkey, **Open Sans Pipe** is designed to ***replace*** Maya's default "Save As..." feature.  It is recommended that you leave this one at its default.  The reason for this is simple.  The "Save As..." feature in Maya is designed to let you manually version up, or copy a file to another scene file, which is exactly what SansPipe was built to do.  As such, it is meant to be a replacement for Maya's default "Save As...".  You can change this setting if you like, but it really is meant to take over and make your life easier in Maya.  The rest are up to you.

## Archiver
- The **Super Archiver** is exactly that!  This is a replacement for Maya's "Archive Scene" tool, and it really is one bad-ass archiver.
- Below is the breakdown for this tab
![Super Archiver](https://github.com/SleepDeprivedVFX/versionUp/blob/master/images/sansPipe_Tab4d.png?raw=true)
- The **Super Archiver** was designed to handle one conundrum.  Let's say you've got 100 scenes and you have to send them to a client, a vendor, or another artist.  In those scenes you've got 3 environments that are very heavy, and 2 characters that are being refrenced in to each one of those 100 scenes.  Each one of these characters and environments have two dozen sourceimages files that make up the textures and every scene has a sound file that's associated with it for lip sync.
- Traditionally, if you just tried to package up your entire show, you're getting a lot of cruft, you get every version of every file from every stage of development and you end up with 10 Terabytes of wasted storage space being compressed and shipped off.
- Or, if you went through every scene one at a time and used Maya's "Archive Scene" feature then every one of those files would include a copy of the heavy environments, the characters and all the sourceimages as well - and the sound files wouldn't even be included.  At the end, each one of those zip files becomes very heavy as you have copy after copy of all the assets included with your archives.
- Hello!  **Super Archiver**!
- The **Super Archiver** allows you to select the files you want to send from the folder tree of existing files in your project and compress them all into one carefully prepared zip file.  It does this by doing the following:
  1. Opens every file and takes a collection of what's inside, references, sounds, images.  It creates an inventory of what's being asked.
  2. Then it copies only the necessary files to an "Archives" folder with a date stamped folder with the show name: YourShow_10092024, and mirrors the file structure originally used in your scenes folders.
  3. After that it goes through each of the copied files and re-links them to the archived versions of your files with relative paths.
  4. Finally, it zips the minimized archive.  Leaving you with all of your 100 scene files along with 1 copy of the textures, 1 copy of the references and 1 copy of the necessary sound files.
- Doing this generates much smaller archives that can easily be moved around without additional cleanup needed!
- Let's discuss the basic features shown above.
1. **The file tree**. This is the file tree where you will select the files you want to archive.  Folders are ignored.  Only files are recorded.  You can select as many as you like.  If you are selecting shot files with things referenced in, there is no need to select the references.  The system will handle that for you.
2. **Import References** check box.  Once in a while, you may want to just skip the whole referencing thing and import them into the scene files.  This feature is here if you want it, but it will create heavier archives, since every copy of your reference will be imported into all your 100 scene files.  There if you need it, but it's not recommended.
3. **Archive Selected** button.  This does what you expect it to.  It starts your archive.  These kinds of archives can take a very long time, so it will ask you to confirm that you do, in fact, want to step away from your computer for a while, but in the end, you get a much nicer package out of it, so it is worth the wait.
- **FUTURE UPDATE**
- There is a plan in place to build an "Un-Archiver" that would take a previously Super Archived file and undo it, putting the files back into the production folder for you, basically reversing the process of the super archive.  It's not built yet, but it's on the books.

## System Settings
- The System Settings handle very little currently, but may be expanded in the future
- Below is the breakdown for this tab
![System Settings](https://github.com/SleepDeprivedVFX/versionUp/blob/master/images/sansPipe_Tab4e.png?raw=true)
1. **Recent File Count**.  This controls how many recent files are show in the **Recent Files** window on the **Save - Publish - Snap** main tab.
2. **Autoload on Startup**.  This feature makes SansPipe open when Maya does.  It also forces the replacement of the "Save As..." (Ctrl + Shift + s) hot key to make SansPipe open instead of the "Save As..." dialog box.  To turn this on or off, check or uncheck it.  Press "Save Configuration" and then re-start Maya.
3. **Autosave** & **Interval**.  This forces Maya's Autosave feature and sets the interval for you.  It is on by default and is a good way to protect yourself from accidental loss by Maya Crash.  **Snapshots** are another great way to keep yourself safe!.

## The Future
- There are a number of features coming to SansPipe now that are already in production:
1. Improved Playblast functions
2. Un-Archive Feature
3. Advanced render settings

## Contributions
Currently, Sans Pipe is a solo project and is not open to direct contributions. However, feedback and suggestions are always welcome.

## License
This project is available for purchase. Please contact the author for licensing details and purchasing information.

## Contact
For support or to purchase a license, please contact AdamBenson.vfx@gmail.com.



