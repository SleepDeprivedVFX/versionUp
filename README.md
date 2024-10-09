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
  /Users/[YourUsername]/Documents/maya/scripts/
  ```

5. **Restart Maya:** 
- Close and reopen Maya to complete the setup.

## Usage
  **User Interface**
  - The first tab of sansPipe is your main workflow utility.  While there are a lot of features on here, it is actually designed to be very minimalistic
![Tab 1 Breakdown](https://github.com/SleepDeprivedVFX/versionUp/blob/master/images/sansPipe_Tab1.png)

## Prerequisites
- **Autodesk Maya:** Designed for Maya 2025 but compatible with any Maya version that supports Python 3 and either PySide2 or PySide6.

## Contributions
Currently, Sans Pipe is a solo project and is not open to direct contributions. However, feedback and suggestions are always welcome.

## License
This project is available for purchase. Please contact the author for licensing details and purchasing information.

## Contact
For support or to purchase a license, please contact AdamBenson.vfx@gmail.com.



