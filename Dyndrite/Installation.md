---
layout: default
title: Installation Overview 
description: "Installation Overview  of Ulendo HC Install for Dyndrite LPBF Pro."
parent: Dyndrite
nav_order: 1
---

# Installation
Ulendo provides a visual based installer for windows platforms to use the Dyndrite LPBF Pro plugin

## Windows Installation Package: 
Locate the downloaded ulendohc_setup.exe file

1. Follow the onscreen steps provided via the GUI based installer
2. Select a directory to install the ulendohc plugin into, and note the directory for future use.

After installation, the installation folder will contain app.exe - a executeable application that is a self contained python applications which the python runtime and the dependent packages that are required for the core of the smartScan application. 

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


