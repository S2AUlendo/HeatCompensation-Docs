---
layout: default
title: Installation Overview 
description: "Installation Overview  of Ulendo HC Install for Dyndrite LPBF Pro."
parent: Dyndrite
nav_order: 1
---

# Installation
Locate the downloaded ulendohc_setup.exe file



![image](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/1342555/eb9c711c-8976-455a-b89b-eba7b50fdf97)

The installation package includes an encapsulated python package which also contains the the python runtime and the dependent packages. 
This package also includes a python plugin "ulendohc" which will be installed into the python environment. 
This installer will attempt to install the plugin into the Dyndrite environment using the following powershell command.

```powershell
C:\Program Files\Dyndrite\Dyndrite\Binaries\Win64\python.exe -m pip install . 
```
If you Dyndrite python environment is located in another directory, you can modify the path in the install.ps1 script and run the script with the updated package. Be sure to run this file from within the UlendoHC installation folder as it also creates a file and copies it to the Dyndrite environment.

### Requirements
The UlendoHC module currently references these external modules:
 - "numpy"   
 - "scipy>=1.10" 
 - "datetime"
 - "matplotlib"
 - "Flask"
 - "multiprocessing"
 - "requests"


