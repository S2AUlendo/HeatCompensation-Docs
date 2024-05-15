---
layout: default
title: Installation Overview 
description: "Installation Overview  of Ulendo HC Install for Dyndrite LPBF Pro."
nav_order: 3
---
# Installation
Two installation options are provided.

## Working with obfuscated code: 
1. Download the UlendoHC repository
2. Extract the ulendohc folder from the downloaded package and place it into the Open File Explorer
3. Copy the ulendohc repository to C:\Users\Public\Documents\Dyndrite\Python
4. Ensure that the pyproject.toml file and Readme.md are also placed in the same folder 
```powershell
C:\Users\Public\Documents\Dyndrite\Python
```

![image](https://github.com/S2AUlendo/HeatCompensation-Docs/assets/1342555/eb9c711c-8976-455a-b89b-eba7b50fdf97)

5. To install the required dependencies open a new terminal and run the command. Be sure to the use the same python environment as the Dyndrite tool
```powershell
~python.exe -m pip install . 
```
7. Navigate inside the ulendohc folder and copy the path of the current directory


## Installation as a module (Not yet available)
To install the Ulendo HC plugin for Dyndrite LPBF

1.  Download the package.
2.  Copy the package to
```powershell
C:\Users\Public\Documents\Dyndrite\Python.
```
3.  Rename the folder "ulendohc"


Run the following commands:
```powershell
cd ulendohc
pip install -e .
```


 
