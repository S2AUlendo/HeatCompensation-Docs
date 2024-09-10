# This is an automated installation script which adds Ulendo HC into the default python environment
# The script adds the path of callback file located in the callbacks subfolder and then
# copies that text file into the Dyndrite vector slice callback folder

$DyndriteCompilerPath = "C:\Program Files\Dyndrite\Dyndrite\Binaries\Win64\python.exe"
$DyndriteVectorSlicePath = 'C:\Users\Public\Documents\Dyndrite\Python\python_ui_scripts\VectorSlice'

$UlendoHCInstallmod = "-m"
$UlendoHCInstallmngr = "pip"
$UlendoHCInstallcmd = "install"
$UlendoHCInstallopt = "-e"   
$UlendoInstallDir = $PWD.path + "."

# Install the current ulendo hc plugin into the dyndrite environment
$pythonOutput = & $DyndriteCompilerPath $UlendoHCInstallmod $UlendoHCInstallmngr $UlendoHCInstallcmd $UlendoHCInstallopt $UlendoInstallDir

# Display the output (optional)
Write-Host "Python output: $pythonOutput"

# # Create the string to hold the current path and target file name
$sourcePath  = $PWD.path + '\ulendohc.txt' 

# # Wite the path of the current ulendo HC to the file 
$destinationPath = "$PWD\callbacks\ulendohc_callback.py"

[System.IO.File]::WriteAllLines($sourcePath, $destinationPath)

# # Copy the newly created file to the vector slice call back 
Copy-Item -Path $sourcePath -Destination $DyndriteVectorSlicePath -Force



