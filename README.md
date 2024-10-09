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
      2. Open
      3. Open No Status Change
      4. View Playblast
      5. Blow Away Snapshots.
   4. Each of these
 

## Prerequisites
- **Autodesk Maya:** Designed for Maya 2025 but compatible with any Maya version that supports Python 3 and either PySide2 or PySide6.

## Contributions
Currently, Sans Pipe is a solo project and is not open to direct contributions. However, feedback and suggestions are always welcome.

## License
This project is available for purchase. Please contact the author for licensing details and purchasing information.

## Contact
For support or to purchase a license, please contact AdamBenson.vfx@gmail.com.



