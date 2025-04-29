---
layout: default
title: Installation Overview 
description: "Installation Overview  of Ulendo HC Install for Dyndrite LPBF Pro."
parent: Dyndrite
nav_order: 1
---

# Installation
The Ulendo plugin and it's associated components can be installed via a GUI installer. The process steps are outlined below. 

## Windows Installation Package: 
Locate the downloaded ulendohc_setup.exe file

This installer requires administrative privileges to be installed as a shared resource. After running the executable, you will be prompted to grant the installer administrative privileges.
![Administrative prompt to install the application.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/installer-prompt.png)


Unless you have made edits to the examples contained within the folder, it is recommended that users perform a clean installation of the application.

![Perform a clean installation of the application.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/clean-installation.png)

1. Follow the onscreen steps provided via the GUI based installer
2. Select a directory to install the Ulendo HC plugin into, and note the directory for future use.

After installation, the installation folder will contain app.exe - a executeable application that is a self contained python applications which the python runtime and the dependent packages that are required for the core of the Ulendo HC application. 

This installation folder also includes a python plugin "ulendohc" which will be installed into the python environment. After the files are extracted the installer will attempt to install the python plugin into the Dyndrite environment using the following powershell command.

```powershell
C:\Program Files\Dyndrite\Dyndrite\Binaries\Win64\python.exe -m pip install . 
```

If the Dyndrite python environment is located in another directory, you can modify the path in the install.ps1 script and run the script with the updated location, by editing the first two lines at the top of the script.

```powershell
$DyndriteCompilerPath = "C:\Program Files\Dyndrite\Dyndrite\Binaries\Win64\python.exe"
$DyndriteVectorSlicePath = 'C:\Users\Public\Documents\Dyndrite\Python\python_ui_scripts\VectorSlice'
```

Set the path to the folder where the Dyndrite python executable is located. Run this file from within the UlendoHC installation folder as it also creates a file and copies it to the Dyndrite environment.

### Dependencies 
The UlendoHC module currently references these external modules:
 - "numpy"   
 - "scipy>=1.10" 
 - "datetime"
 - "opencv"
 - "multiprocessing"
 - "requests"


