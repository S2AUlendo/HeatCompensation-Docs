---
layout: default
title: Detailed Example
description: "An overview of the Dyndrite LPBF Integration."
parent: Dyndrite
nav_order: 5
---

# A complete build using the plugin. 
Integrating the UlendoHC optimizations into your workflow is simple. With only a few lines of code, it can be easily adapted into existing build files.
In the example below, all of the changes required to integrate UlendoHC are marked using:
```python
############################
```

The complete code for the example shown below is also available in the examples folder of the UlendoHC installation directory.

```python
import time, os, sys, math
from pathlib import Path

############################
### ULENDO HC OPTIMIZER ####
import ulendohc.LPBFWrapper as ss
sslpbf = ss.smartScanLBFPPro()
############################

# Connect to Dyndrite LPBF Pro
import dyndrite
try:
    # tries to use an existing instance of Dyndrite LPBF Pro
    dyn = dyndrite.connect(connect_attempts=2)
    dyn.reset()
except:
    # if it fails, opens new instance of Dyndrite LPBF Pro
    dyn = dyndrite.launch()


# Prepare both raster and vector process pipelines within the Turbo User Interface
vp = dyn.vector_process
rp = dyn.raster_process

zoner = dyn.zoner
toolpather = vp.toolpather

# Set up the printer
dyn.printer.plate = (250, 250)
dyn.printer.height = 350.0
dyn.printer.plate_thickness = 20.0
dyn.printer.display_name = "RenAM 500Q"

# If you install the UlendoHC plugin, and run the example from the installation folder, it will search for the available files in the "input" directory contained within the installation folder.

dir_path = os.path.dirname(os.path.realpath(__file__))
# Gets the absolute path of the current file
current_dir = Path(__file__).resolve() 
# Accesses the grandparent directory using index 2
grandparent_dir = current_dir.parents[3] 
print("Importing file from: " + str(grandparent_dir) + r"\input\Figure 1D_cantilever.stl")
# if the file has been successfully imported then, the Dyndrite window should show the model in the build preview.
prt0=dyn.ops.import_part(path=str(grandparent_dir) + r"\input\Figure 1D_cantilever.stl",
     auto_center=True,
     transform=None,
     translate_only=None,
     brep_sampling_parameters=None,
     open_geometry=False)
prt0_rgn0=prt0.region[0]


# Create the zones
# You can use the build zones that best suits your workflow. 
# No changes are required here to support UlendoHC integration
zoner.init_zone(zone_type=zoner.PartZoneType.SDF, width=0.4, color=(255, 0, 0))
zoner.init_zone(zone_type=zoner.PartZoneType.DOWNSKIN, width=0.4, color=(0, 255, 0))
zoner.init_zone(zone_type=zoner.PartZoneType.UPSKIN, width=0.4, color=(0, 0, 255))



# Modulated CW scans are composed of discrete exposure points along a hatch vector.
# As Renishaw machines use a modulated CW exposure instead of a continuous vector
# scan, we will create a different type of build style with different options
# to the usual.
# Modulated CW scans can be described using point jump delay, point distance,
# and point exposure time, instead of just scan speed.
# These parameters allow us to control the exposure profile of each exposure
# point.

core_params = dyn.RenishawToolParameters(laser_focus_mm=0,
                                         laser_index=1,
                                         laser_power_w=400,
                                         jump_delay_us=30,
                                         point_distance_um=20,
                                         point_exposure_time_us=70)

core_bst = toolpather.new_build_style(renishaw_params=core_params)

us_params = dyn.RenishawToolParameters(laser_focus_mm=0,
                                       laser_index=1,
                                       laser_power_w=400,
                                       jump_delay_us=30,
                                       point_distance_um=20,
                                       point_exposure_time_us=70)

us_bst = toolpather.new_build_style(renishaw_params=us_params)

ds_params = dyn.RenishawToolParameters(laser_focus_mm=0,
                                       laser_index=1,
                                       laser_power_w=400,
                                       jump_delay_us=30,
                                       point_distance_um=20,
                                       point_exposure_time_us=70)

ds_bst = toolpather.new_build_style(renishaw_params=ds_params)

sdf_params = dyn.RenishawToolParameters(laser_focus_mm=0,
                                        laser_index=1,
                                        laser_power_w=380,
                                        jump_delay_us=30,
                                        point_distance_um=20,
                                        point_exposure_time_us=70)

sdf_bst = toolpather.new_build_style(renishaw_params=sdf_params)

# Create the segments, and assign the modulated build styles to each
sdf_sgt0 = zoner.add_segment(zone_type=zoner.PartZoneType.SDF,color=(255, 0, 0))
us_sgt0 = zoner.add_segment(zone_type=zoner.PartZoneType.UPSKIN,color=(0, 255, 0))
ds_sgt0 = zoner.add_segment(zone_type=zoner.PartZoneType.DOWNSKIN,color=(0, 0, 255))
core_sgt0 = zoner.add_segment(zone_type=zoner.PartZoneType.CORE,color=(140, 140, 140))
support_sgt0 = zoner.add_segment(zone_type=zoner.PartZoneType.CORE, color=(140, 140, 140))

# Set Global Slicing Parameters
vp.slicing_thickness = .03
vp.slicing_resolution = dyn.Vector2(0.05, 0.05)


# Create segmentation strategy for the part
part_strat = zoner.new_segmentation_strategy(core_segment=core_sgt0, volumetric_segments=[(us_sgt0, 4), (ds_sgt0, 4), (sdf_sgt0, 4)])
support_strat = zoner.new_segmentation_strategy(core_segment=support_sgt0)

# Create a new contour strategy for the part
cst0 = toolpather.new_contour_strategy(offsets=[0.01, 0.02])


# Set up our build style mappings for our hatching
hatch_config = {
    core_sgt0: core_bst,
    sdf_sgt0: sdf_bst,
    us_sgt0: us_bst,
    ds_sgt0: ds_bst
}
support_hatch_config = {
    support_sgt0: core_bst,
}
# Set up our build style mappings for our contours
perimeter_config = {
    core_sgt0: [core_bst, core_bst, core_bst],
    sdf_sgt0: [sdf_bst, sdf_bst, sdf_bst],
    us_sgt0: [us_bst, us_bst, us_bst],
    ds_sgt0: [ds_bst, ds_bst, ds_bst]
}
support_perimeter_config = {
    support_sgt0: [core_bst, core_bst, core_bst]
}
# Create some default hatching parameters
# Create the hatching parameters
htp0 = vp.HatchingParameters(generation_origin=dyn.Vector2(0.0, 0.0),
                             fill_point=dyn.Vector2(0.0, 0.0),
                             fill_vector=dyn.Vector2(0.0, 0.0),
                             scan_angle=67, hatch_spacing=0.15,
                             hatch_length=400, alternate_direction=False,
                             fill_option=vp.FillOption.FILL_DEFAULT,
                             fill_to_perimeter=0)

# Create new toolpath schemas
part_schema = toolpather.new_toolpath_schema(segmentation_strategy=part_strat, contour_strategy=cst0)
support_schema = toolpather.new_toolpath_schema(segmentation_strategy=support_strat, contour_strategy=cst0)

# Set the build style configs
part_schema.set_hatch_config(config=hatch_config)
part_schema.set_all_perimeter_configs(config=perimeter_config)
support_schema.set_hatch_config(config=support_hatch_config)
support_schema.set_all_perimeter_configs(config=support_perimeter_config)

# Set the default hatching
part_schema.fill_default_hatch_generation(params=htp0)
support_schema.fill_default_hatch_generation(params=htp0)

# Prune and validate the schemas
toolpather.prune_all_schemas()
toolpather.validate_all_schemas()

# Apply the schema to our part
vp.apply_schema(geometry=dyn.part[0], schema=part_schema)
for support in dyn.part[0].support:
    vp.apply_schema(geometry=support, schema=support_schema)

vp.finalize()

scan_angle_delta = math.radians(67)


def cb(ctx: dyn.LayerContext, writer: dyn.VectorWriter, layer_idx):
    print("Slicing Layer: " + str(layer_idx))
    collection = ctx.fragments
    all_segments = ctx.zoner.get_all_segments()
    downskin_seg = []
    upskin_seg = []
    sdf_seg = []
    core_seg = []
    other_seg = []
    for seg in all_segments:
        if seg.zone == ctx.zoner.PartZoneType.CORE:
            core_seg.append(seg)
        elif seg.zone == ctx.zoner.PartZoneType.UPSKIN:
            upskin_seg.append(seg)
        elif seg.zone == ctx.zoner.PartZoneType.DOWNSKIN:
            downskin_seg.append(seg)
        elif seg.zone == ctx.zoner.PartZoneType.SDF:
            sdf_seg.append(seg)
        else:
            other_seg.append(seg)

    # Update the scan angle of all segments
    for hatching_param in toolpather.get_all_hatching_parameters():
        raw_params = hatching_param.parameters
        raw_params.scan_angle += scan_angle_delta

        toolpather.update_hatching_parameters(hatching_param, raw_params)

    ctx.hatch_fragments(collection)

    ############################
    ### ULENDO HC OPTIMIZER ####
    # Create the build mask for the layer.
    # This allows HC to assess all of the regions where heat will be input
    sslpbf.createBuildAreaMask(collection)
    ############################

    for seg in downskin_seg:
        ############################
        ### ULENDO HC OPTIMIZER ####
        # Each segment is optimized independently by UlendoHC
        # This prevents reallocation across zones
        new_seg = collection.select_by_segment(segment=seg)
        optimized_Order = sslpbf.smartScanLPBF(new_seg, n_layers=2, reduced_Order=50) 
        # The new order is provided to the Dyndrite software to update the order based 
        # on the provided criteria
        ############################
        optimized_ordered_Fragments, unordered_fragments = collection.sort_with_complement_by_ids(optimized_Order)   
        writer.write_fragments(fragments=optimized_ordered_Fragments)

    for seg in sdf_seg:
        new_seg = collection.select_by_segment(segment=seg)
        ############################
        ### ULENDO HC OPTIMIZER ####
        optimized_Order = sslpbf.smartScanLPBF(new_seg, n_layers=2, reduced_Order=50) 
        optimized_ordered_Fragments, unordered_fragments = collection.sort_with_complement_by_ids(optimized_Order)   
        ############################
        writer.write_fragments(fragments=optimized_ordered_Fragments)

    for seg in core_seg:
        new_seg = collection.select_by_segment(segment=seg)
        ############################
        ### ULENDO HC OPTIMIZER ####
        optimized_Order = sslpbf.smartScanLPBF(new_seg, n_layers=2, reduced_Order=50) 
        optimized_ordered_Fragments, unordered_fragments = collection.sort_with_complement_by_ids(optimized_Order)   
         ############################
        writer.write_fragments(fragments=optimized_ordered_Fragments)

    for seg in upskin_seg:
        new_seg = collection.select_by_segment(segment=seg)
        ############################
        ### ULENDO HC OPTIMIZER ####
        optimized_Order = sslpbf.smartScanLPBF(new_seg, n_layers=2, reduced_Order=50) 
        optimized_ordered_Fragments, unordered_fragments = collection.sort_with_complement_by_ids(optimized_Order)  
         ############################ 
        writer.write_fragments(fragments=optimized_ordered_Fragments)

    for seg in other_seg:
        new_seg = collection.select_by_segment(segment=seg)
        ############################
        ### ULENDO HC OPTIMIZER ####
        optimized_Order = sslpbf.smartScanLPBF(new_seg, n_layers=2, reduced_Order=50) 
        optimized_ordered_Fragments, unordered_fragments = collection.sort_with_complement_by_ids(optimized_Order)   
         ############################
        writer.write_fragments(fragments=optimized_ordered_Fragments)

    writer.write_perimeters(ctx.perimeters)


# Use Custom CLI/DVF File Writer to Slice
directory = "C:/Users/Public/Documents/Dyndrite/UlendoHC"
outputFile = directory + "/F1D_opt.dvf"
vp.slice_all(writers=dyn.DvfWriter(out_file=outputFile), on_slice=cb)


# Open Slice Viewer
tab_id = dyn.gui.vector_slice_viewer.open_resource(path_or_stack=outputFile)
dyn.gui.vector_slice_viewer.set_envelope_from_plate(tab_id=tab_id, plate_dims=dyn.printer.plate)
dyn.gui.vector_slice_viewer.center_on_point(tab_id=tab_id, point=(0, 0), zoom_level=0)



```

Integrating UlendoHc into your workflow is simple.


