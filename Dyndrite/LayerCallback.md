---
layout: default
title: Layer Callback 
description: "An overview of the Dyndrite LPBF Integration."
parent: Dyndrite
nav_order: 2
---

# Dyndrite LPBF Integration
This section provides an overview of how the Ulendo HC functionality can be integrated with the LPBF Pro front end.
Using the callback requires that the ulendohc plugin be installed in the Dyndrite environment. See the installation guide to ensure that the ulendohc python plugin is installed in the Dyndrite environment.

## Using a user defined callback: 
You can customize the UlendoHC callback to meet your needs if one of the predefined examples do not meet you needs. 

 1. Navigate to 
 ```
 C:\Users\Public\Documents\Dyndrite\Python\python_ui_scripts\VectorSlice
 ```
 2. Create a new text document

![Screenshot 2024-04-25 100642](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/29451862/62ae99a6-5894-4fcd-bca3-0e0914617a18)

 3. Open the newly created text document and place the path of the callback function and save the file 

![Screenshot 2024-04-25 100735](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/29451862/05c746a3-e3dc-43c4-b8a2-8ac8451480f1)

 4. Open the newly created text document and place the path of the callback function and save the file 
 
Note that custom callbacks located in the UlendoHC installation folder will be overwritten when new versions of the plugin are installed.

## Using the callback to optimize parts:
 1. Import the part, and configure your optimization and slicing parameters
 2. Click on the slice toolbar
 3. Click on the turbo mode on the right window pane

 ![Screenshot 2024-04-25 100920](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/29451862/5734279e-581a-4ddb-bda2-c245772070d6)
 
 4. Select User Scripts and navigate to the new text file that was created (in our case UlendoHC)
 5. In the tab below, select the callback function that needs to be imported

![Screenshot 2024-04-25 101037](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/29451862/86ec56a0-9fc7-41c0-b539-100bb9abd0a1)
 6. Click on Run and it should work with the User defined callback function
![Screenshot 2024-04-25 101151](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/29451862/bd5e197f-f572-4768-a7ea-2f8f608e4157)
 7. The output file will be created in the current working directory 
![Screenshot 2024-04-25 102005](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/29451862/a1124650-40fa-4057-a70e-d12ab812a28a)



 
 
