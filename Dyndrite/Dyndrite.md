---
layout: default
title: Dyndrite
description: "An overview of the Dyndrite LPBF Integration."
has_children: true
nav_order: 2
---

# Dyndrite LPBF Integration
The Ulendo HC plugin can be used with the Dyndrite LPBF Pro in two ways. 

1. Via the GUI interface
2. Via the programming interface

Both of these options present the same functionality, and can be used interchangeably based on the users' preference. 


### Advanced usage the API Interface
There are three essential components to using the Ulendo HC plugin with the LPBF Pro framework

1. Import the Ulendo HC package
In the statement below, we import the module designed to interface with the LPBF Pro software, from Ulendo heat compensation package, and name it "ss" short for SmartScan.
```python
import ulendohc.LPBFWrapper as ss
```

2. Initialize a new instance of the Heat Compensation LPBF Pro Interface
```python
sslpbf = ss.smartScanLBFPPro()
```
The instance can be initialized with the default parameters or additional parameters can be set or passed into the software. 
In order of the usage the available parameters to configure the module, include:

    1.  Conductivity [W/mK]
    2.  Density [kg/m^3]
    3.  Heat Capacity [J/kgK]
    4.  Scanning speed [m/s]
    5.  Convection coefficient [W/m^2K]        
    6.  Laser power [W]

```python
sslpbf = ss.smartScanLBFPPro(kt=22.5, rho=7990, cp=500, vs=0.6, h=50, P=100,  port = 8001, host = "127.0.0.1")
```

The UlendoHC plugin will attempt to launch a local server listening on the host and running on Port 8001, if the port is available. Users can manually specify a hostname and a port to be used by configuring those options.

1. Once the module has been initialize, it can be called in the layer callback as shown below:


    1. Create the mask of the entire build area
```python
sslpbf.createBuildAreaMask(collection)
```
This function allows HC to create a view over the entire build area, and assess all of the areas of the layer that will be scanned by the laser.

Next optimize the segments. If the part only contains one region. The following code can be used to return the entire updated sequence.

```python
ss_Ordered_Segments = sslpbf.smartScanLPBF(collection, n_layers=2, RO=40)  
```
The function takes the following parameters:
1. The collection of fragments, as an object provided by LPBF Pro software
3. The number of previous layers to use to in the optimization of the sequence (Optimal values between 2 and 20)
4. The Reduced Order of the StateMatrix - RO Higher values enable more precise optimization, but may result in longer calculation times, and increased memory usage. The recommended max size is the size in mm of the part in mm. Leave as default if you are not sure how this setting will affect your optimization.
5. For especially large builds setting a higher reduction level can help to significantly reduce the time required to perform the optimization.

2. Multi-Region Optimization
If the layer contains multiple regions, code like the example show below can be executed for each region. This allows HC to only optimize features which below to their specific region.

```python
for seg in downskin_seg:
        new_seg = collection.select_by_segment(segment=seg)
        optimized_Order = sslpbf.smartScanLPBF(new_seg, n_layers=2, reduced_Order=50)  
        optimized_ordered_Fragments, unordered_fragments = collection.sort_with_complement_by_ids(optimized_Order)   
        writer.write_fragments(fragments=optimized_ordered_Fragments)
```



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
    ss_Ordered_Segments = sslpbf.smartScanLPBF(collection, n_layers=2)  
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

> {: .note }
  Fragments must be cut and hatched before passing the collection to the UlendoHC plugin.
