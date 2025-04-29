---
layout: default
title: Installation Overview 
description: "Installation Overview  of Ulendo HC Install for Dyndrite LPBF Pro."
parent: Dyndrite
nav_order: 1
---

# Installation
The Ulendo plugin and it's associated components can be installed via a GUI installer. The process steps are outlined below. 

## Windows Installation Package
Locate the downloaded ulendohc_setup.exe file

This installer requires administrative privileges to be installed as a shared resource. After running the executable, you will be prompted to grant the installer administrative privileges.
![Administrative prompt to install the application.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/installer-prompt.png)


Unless you have made edits to the examples contained within the folder, it is recommended that users perform a clean installation of the application.

![Perform a clean installation of the application.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/clean-installation.png)

1. Follow the onscreen steps provided via the GUI based installer
2. Select a directory to install the Ulendo HC plugin into, and note the directory for future use.

After installation, the installation folder will contain ulendohc_server.exe - an executable application that contains the core of the Ulendo HC application. 


## Dyndrite Python Environment
This installation folder also includes a python plugin "ulendohc" which will be installed into the Dyndrite python environment. After the files are extracted the installer will attempt to install the python plugin into the Dyndrite environment using the following powershell command.

```powershell
C:\Program Files\Dyndrite\Dyndrite\Binaries\Win64\python.exe -m pip install . 
```

If the Dyndrite python environment is located in another directory, the installation path can be modified by editing the installation script install.ps1 script. To update the installation directory...

1. Edit the script to contain the new path:
```powershell
$DyndriteCompilerPath = "C:\Program Files\Dyndrite\Dyndrite\Binaries\Win64\python.exe"
$DyndriteVectorSlicePath = 'C:\Users\Public\Documents\Dyndrite\Python\python_ui_scripts\VectorSlice'
```
Set the path to the folder where the Dyndrite python executable is located. 

2. Run the script with the updated location.

### Dependencies 
The UlendoHC module currently references these external modules:
 - "numpy"   
 - "scipy>=1.10" 
 - "datetime"
 - "opencv"
 - "multiprocessing"
 - "requests"


