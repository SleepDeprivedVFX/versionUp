# Sans Pipe - Light Pipeline Utility for Maya version 1.3.9

## Description
Sans Pipe is a light pipeline utility designed specifically for Maya, aimed at enhancing project organization and efficiency. It provides a robust set of tools that streamline project workflows, including file versioning with notes, snapshot taking, file publishing, reference tracking, camera baking, asset and shot creation, playblasting animations, and asset exporting.

## Features
- **Version Control:** Automatically versions up Maya files with accompanying notes for better tracking.
- **Snapshot Taking:** Captures file snapshots for incremental backups or version comparison.
- **Publishing Tools:** Simplifies the process of publishing files for production.
- **Reference Tracking:** Ensures all references are up-to-date and correct.
- **Camera Baking:** Tools for baking out camera movements for export or further processing.
- **Asset and Shot Creation:** Facilitates the creation and organization of assets and shots within Maya.
- **Playblasting:** Integrated playblasting tools for previewing animations directly within Maya.

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

## Usage
  **User Interface**
  - **Save - Publish - Snap** Tab.
  - The first tab of sansPipe is your main workflow utility.  While there are a lot of features on here, it is actually designed to be very minimalistic
![Tab 1 Breakdown](https://github.com/SleepDeprivedVFX/versionUp/blob/master/images/sansPipe_Tab1.png)
1. This is what sansPipe is *going* to save your next file as.  By default, this is a "version up" tool, and this is it's primary feature
2. This controls how the automatic naming convention works.  99% of the time, you'll never have to deal with this, and it is recommended that you leave it on "Auto".
   1. The simplest way to change tasks, i.e. Previs to Animation, is to simply change the **Task Type** drop-down menu from **previs** to **anim**.  SansPipe will automatically change the **Save As...** output to the correct task path and version number.
   2. To create a custom name and output, change the **Naming** radio buttons from **Auto** to **Custom**.  This unlocks the rest of the naming tools and allows you to create your own filename.  After that, sansPipe will automatically track its new version number and continue with your custom naming.
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
      1. ![Existing File Right Click](https://github.com/SleepDeprivedVFX/versionUp/blob/master/images/sansPipe_EF_RightClick_1.png)  
      2. **Open** does what you would expect, however, when you open a file from here, whether using the right-click option or by double clicking the file itself, it opens the file, but also sets the **Task Status** to "In Progress".
      3. **Open No Status Update** works the same way as open, except it does not change the current **Task Status**.  This is useful if you have a file marked "Needs Revision", "Done", or "For Review" and you want to leave that task status as is.
      4. **View Playblast** only works if there is an associated playblast, indicated by the Camera Icon ![Camera Icon](https://github.com/SleepDeprivedVFX/versionUp/blob/master/icons/cam_icon.png)
      5. **Blow Away Snapshots** is a tool for deleting all the **Snapshots** associated with a particular file.  Snapshots are simply date-stamped copies of your working file, and thus take up space.  If you are sure you are through with your Snapshots, you can delete them for a given task by using this feature.  More about this later.
   4. The **Task Status** drop down sits at the top of the **Existing Files** tree.  It updates based on the current selection in the tree.  By manually changing it (You must add a note to do this) it will change the status of the selected file and record that into the version notes.
   5. If you are using the **Allow File Copy From --> To** feature in the *Section 2* Naming convention form, this is where that takes place.  By first clicking that checkbox, and then selecting an asset or shot name (top folder of that stack, for instance, select "BDD_Shot_0020") and it will rename your file to that, but only if that checkbox is selected first.
6. **Snapshots**.  Snapshots are wonderful things!  You should create Snapshots often instead of saving a version up.  **Snapshots** are basically versioning up a file, without versioning up a file.  They require a *Note* to be saved.  Here's some cool stuff about **Snapshots**:
   1. A Snapshot saves where you're at right now with a working file, let's call it BDD_Shot_0010_anim_v001.  You can start with your initial import of objects and do a quick Snapshot.  Add a note like, "Importing the assets" then hit the **Snapshot** button or use the hotkey **Ctrl + Alt + S**  (Command + Option + S on Mac). A snapshot is created and will show up with a date stamp in the **Snapshots** stack.
   2. Now, you do some blocking animation, really basic stuff, no finesse.  Do another snapshot.  Put in a note like "Basic blocking" and the hit **Snapshot**.  A new Date stamped file shows up in the stack.
   3. One more **snapshot**, "First pass animation".  Now let's say that you hate it, and want to go back to that initial import...
   4. Drop down that first snapshot in your stack and you'll see your first "Importing the assets" note.  Double click that note and suddenly your file will go back to its initial state.  If you have unsaved changes in your current file, it will pop up a message asking if you'd like to Snapshot your current place.  Do it - it can't hurt.
   5. Now your file is back to your initial import and you can do another pass at blocking, animation, or whatever it is you want to redo.
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
 
## Prerequisites
- **Autodesk Maya:** Designed for Maya 2025 but compatible with any Maya version that supports Python 3 and either PySide2 or PySide6.

## Contributions
Currently, Sans Pipe is a solo project and is not open to direct contributions. However, feedback and suggestions are always welcome.

## License
This project is available for purchase. Please contact the author for licensing details and purchasing information.

## Contact
For support or to purchase a license, please contact AdamBenson.vfx@gmail.com.



