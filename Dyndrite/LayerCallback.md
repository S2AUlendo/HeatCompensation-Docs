---
layout: default
title: Layer Callback 
description: "An overview of the Dyndrite LPBF Integration."
parent: Dyndrite
nav_order: 2
---

# Dyndrite LPBF Integration
This section provides an overview of how the Ulendo HC functionality can be integrated with the LPBF Pro front end.

# Placing User defined Callback: 
 1. Navigate to C:\Users\Public\Documents\Dyndrite\Python\python_ui_scripts\VectorSlice
 2. Create a new text document
![Screenshot 2024-04-25 100642](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/29451862/62ae99a6-5894-4fcd-bca3-0e0914617a18)
 3. Open the newly created text document and place the path of the callback function and save the file 
![Screenshot 2024-04-25 100735](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/29451862/05c746a3-e3dc-43c4-b8a2-8ac8451480f1)
 4. Reset the Dyndrite Tool by clicking on Files->Reset Project
 5. Import the part to be printed
 6. Click on the slice toolbar
 7. Click on the turbo mode on the right window pane
 ![Screenshot 2024-04-25 100920](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/29451862/5734279e-581a-4ddb-bda2-c245772070d6)
 8. Select User Scripts and navigate to the new text file that was created (in our case UlendoHC)
 9. In the tab below, select the callback function that needs to be imported
![Screenshot 2024-04-25 101037](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/29451862/86ec56a0-9fc7-41c0-b539-100bb9abd0a1)
 10. Click on Run and it should work with the User defined callback function
![Screenshot 2024-04-25 101151](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/29451862/bd5e197f-f572-4768-a7ea-2f8f608e4157)
 11. The CLI+ file will be created in the current working directory 
![Screenshot 2024-04-25 102005](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/29451862/a1124650-40fa-4057-a70e-d12ab812a28a)

# Importing UlendoHC Library files:
 1. Download the UlendoHC repository
 2. Open File Explorer
 3. Copy the UlendoHC repository from Downloads folder
 4. Navigate to C:\Users\Public\Documents\Dyndrite\Python
 5. Paste the UlendoHC repository the Dyndrite Tool can import the modules when using Turbo mode
![Screenshot 2024-04-25 102049](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/29451862/aed9848f-66c1-4495-948a-5c93011cd3b9)
 6. The Dyndrite Tool imports the library files from this location: C:\Users\Public\Documents\Dyndrite\Python, if the modules are missing or not imported properly, moving the modules to this folder location should work.
 
