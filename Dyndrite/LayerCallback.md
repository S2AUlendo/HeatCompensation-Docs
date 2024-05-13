---
layout: default
title: Layer Callback 
description: "An overview of the Dyndrite LPBF Integration."
nav_order: 3
---

# Dyndrite LPBF Integratiion
This section provides an overview of how the Ulendo HC functionality can be integrated with the LPBF Pro front end.

# Placing User defined Callback: 
 1. Navigate to C:\Users\Public\Documents\Dyndrite\Python\python_ui_scripts\VectorSlice
 2. Create a new text document
 3. Open the newly created text document and place the path of the callback function and save the file
 4. Reset the Dyndrite Tool by clicking on Files->Reset Project
 5. Import the part to be printed
 6. Click on the slice toolbar
 7. Click on the turbo mode on the right window pane
 8. Select User Scripts and navigate to the new text file that was created (in our case UlendoHC)
 9. In the tab below, select the callback function that needs to be imported
 10. Click on Run and it should work with the User defined callback function
 11. The CLI+ file will be created in the current working directory 


# Importing UlendoHC Library files:
 1. Download the UlendoHC repository
 2. Open File Explorer
 3. Copy the UlendoHC repository from Downloads folder
 4. Navigate to C:\Users\Public\Documents\Dyndrite\Python
 5. Paste the UlendoHC repository the Dyndrite Tool can import the modules when using Turbo mode
 6. The Dyndrite Tool imports the library files from this location: C:\Users\Public\Documents\Dyndrite\Python, if the modules are missing or not imported properly, moving the modules to this folder location should work.

# Working with Obfuscated code: 
 1. Download the UlendoHC repository
 2. Open File Explorer
 3. Copy the UlendoHC repository to C:\Users\Public\Documents\Dyndrite\Python
 4. Ensure that the pyproject.toml file and Readme.md are also placed in the same location (C:\Users\Public\Documents\Dyndrite\Python)
 5. Right click on the folder and open command prompt or terminal
 6. To install the required packages: “pip install .” (this will install all the necessary packages to run UlendoHC)
 7. Navigate inside the ulendohc folder and copy the path of the current directory 
