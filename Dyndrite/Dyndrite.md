---
layout: default
title: Dyndrite
description: "An overview of the Dyndrite LPBF Integration."
nav_order: 2
---

# Dyndrite LPBF Integratiion
This section provides an overview of how the Heat compensation plugin developed by Ulendo can be used with the Dyndrite LPBF system. 

For ease of integration the Ulendo HC plugin has been developed as a pythom module which can be directly installed in the Dyndrite python environment. 

## Usage 
The package can be used from either from the slicer callback or run directly from a standalone Python script. 

### Standalone Mode
There are three essential components to using the Ulendo HC plugin with the LPBF Pro framework

1. import the installed Ulendo HC Library
In the statement below, we import the module designed to interface with the LPBF Pro software, from ulendo heat compensation package, and name it "ss" short for SmartScan.
```python
import ulendohc.LPBFWrapper as ss
```

2. We initialize a new instance of the Heat Compensation LPBF Pro Interface
```python
sslpbf = ss.smartScanLBFPPro()
```
The instance can be initialized with the default parameters or additional parameters can be set or passed into the software. 
In order of the usage the available parameters to configure the module, include:
<div class="parameters" markdown="1">
1.  Conductivity [W/mK]
2.  Density [kg/m^3]
3.  Heat Capacity [J/kgK]
4.  Scanning speed [m/s]
5.  Convection coefficient [W/m^2K]        
6.  Laser power [W]
</div>
```python
sslpbf = ss.smartScanLBFPPro(kt=22.5, rho=7990, cp=500, vs=0.6, h=50, P=100)
```

3. Once the module has been initialize, it can be called in the layer callback as shown below:

```python
ss_Ordered_Segments = sslpbf.smartScanLPBF(collection, layer_idx, n_lyaers=2, use_Cache=False)  
```
The function takes as parameters, the:
1. The collection of fragments, as an object provided by LPBF Pro software
2. The id of the layer currently being processed
3. The number of previous layers to use to in the optimization of the sequence (Optimal values between 2 and 20)
4. Use cache - whether or not to use an pre-initialized data to perform the optimization. This can work well for parts that nearly uniform throughout the layers
5. For espeically large builds setting a higher reduction level can help to signifcantly reduce the time required to perform the optimization.



### Slicer Layer Callback Example
```python
def cb(ctx: dyn.VectorProcess, writer: dyn.VectorWriter, layer_idx):
    print("Slicing Layer: " + str(layer_idx))

    # DynDocs Within your Callback Function you can retrieve the initial group of unsorted and uncut fragments with
    # Unsorted fragments for the rest of the layers
    collection = ctx.get_fragments()

    # Set default hatching parameters
    stripeAngle = math.radians(stripeAngleVal * layer_idx)
    hatching_params = vp.HatchingParameters(hatch_spacing=0.2, scan_angle=stripeAngle, hatch_length=1.0)    

    # Cut all our fragments with a checkerboard pattern
    collection = ctx.cut_fragments(fragments=collection, tiles=ctx.checkerboard_tiles(5, 5, 0), cut_tag="collection")

    ctx.hatch_fragments(fragments=collection, hatching_params=hatching_params)
    
    # Call the smart scan plugin after the hatches are generated.
    ss_Ordered_Segments = sslpbf.smartScanLPBF(collection, layer_idx, n_lyaers=2, use_Cache=False)  
    orderFragView, unorderfragsView = collection.sort_with_complement_by_ids(ss_Ordered_Segments)   

    # Write fragments
    writer.write_fragments(fragments=orderFragView)

    # Write perimeters
    writer.write_perimeters(perimeters=ctx.perimeters)

directory="C:/Users/Public/Documents/Dyndrite"
filepath=os.path.join(directory, "dyn_out.dvf")

vp.slice_all(writers=dyn.DvfWriter(out_file=filepath), on_slice=cb)

# Open Slice Viewer
tab_id = dyn.gui.vector_slice_viewer.open_resource(path_or_stack=filepath)
dyn.gui.vector_slice_viewer.set_envelope_from_plate(tab_id=tab_id, plate_dims=dyn.printer.plate)
dyn.gui.vector_slice_viewer.center_on_point(tab_id=tab_id, point=(0, 0), zoom_level=0)
```
