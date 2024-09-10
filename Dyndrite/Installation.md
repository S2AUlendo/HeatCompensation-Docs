---
layout: default
title: Installation Overview 
description: "Installation Overview  of Ulendo HC Install for Dyndrite LPBF Pro."
parent: Dyndrite
nav_order: 1
---

# Installation
Locate the downloaded ulendohc_setup.exe file

Select a directory to install the ulendohc plugin into.

After installation, the installation folder will contain app.exe - a launchable application that is a self contained python applications which the python runtime and the dependent packages that are required for the core of the smartScan application. 

This installation folder also includes a python plugin "ulendohc" which will be installed into the python environment. After the files are extracted the installer will attempt to install the python plugin into the Dyndrite environment using the following powershell command.

```powershell
C:\Program Files\Dyndrite\Dyndrite\Binaries\Win64\python.exe -m pip install . 
```

If you Dyndrite python environment is located in another directory, you can modify the path in the install.ps1 script and run the script with the updated package. Be sure to run this file from within the UlendoHC installation folder as it also creates a file and copies it to the Dyndrite environment.

### Dependencies 
The UlendoHC module currently references these external modules:
 - "numpy"   
 - "scipy>=1.10" 
 - "datetime"
 - "matplotlib"
 - "Flask"
 - "multiprocessing"
 - "requests"


