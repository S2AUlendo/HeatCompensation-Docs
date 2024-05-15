# Standalone scripts which can be run and utilize the s
# Create a script that will use different hatcing optimizations
# for each of the parts that are loaded onto the bed, still a WIP
import math
import os, sys
cwd = os.getcwd()


## Find the file location for the Dyndrite Module
sys.path.insert(0, r'C:/Users/Public/Documents/Dyndrite/Python')
# open Dyndrite LPBF Pro
import dyndrite
try:
    # Tries to use an existing instance of Dyndrite LPBF Pro
    dyn = dyndrite.connect(connect_attempts=10)
except:
    # If it fails, opens new instance of Dyndrite LPBF Pro
    dyn = dyndrite.launch()

from ulendohc import LPBFWrapper as ss

dyn.printer.display_name="Dyndrite Vector Printer"
dyn.printer.plate=(200.0, 200.0)
dyn.printer.height=200.0
dyn.printer.plate_thickness=20.0

prt0=dyn.ops.import_part(path=r"C://Users/sthom/Documents/Development/Products/UlendoHC/input/Figure 1I_cyl_diff_shrink_2.stl",
    auto_center=True,
    transform=None,
    translate_only=None,
    brep_sampling_parameters=None,
    open_geometry=False)
prt0_rgn0=prt0.region[0]

[prt1] = dyn.ops.duplicate(dyn.part[0])
prt1_rgn0 = prt1.region[0]

[prt2] = dyn.ops.duplicate(dyn.part[0])
prt2_rgn0 = prt2.region[0]


#dyn.ops.translate(dyn.part[0], dyn.Vector3(0.000000,-30.000000,0.000000))
dyn.ops.place(dyn.part[0], dyn.Vector3(-107.763100,-54.500000,0.000000))

# dyn.ops.translate(dyn.part[1], dyn.Vector3(0.000000,30.000000,0.000000))
dyn.ops.place(dyn.part[1], dyn.Vector3(-107.763100,5.500000,0.000000))


#print part region 
print(prt0.limits)

vp = dyn.new_process(dyn.VectorProcess)
zoner = vp.zoner

# Set Global Slicing Parameters
SlicingThickness = 0.05
SlicingResolution = 0.5
stripeAngleVal = 67
stripeAngle = math.radians(stripeAngleVal)
vp.slicing_thickness = SlicingThickness
vp.slicing_resolution = dyn.Vector2(SlicingResolution, SlicingResolution)

vp.finalize()

sslpbf = ss.smartScanLBFPPro()

# only_contours - Everything in this section is custom
def cb(ctx: dyn.LayerContext, writer: dyn.VectorWriter, layer_idx):

    # DynDocs Within your Callback Function you can retrieve the initial group of unsorted and uncut fragments with
    collection = ctx.get_fragments()

    # Set default hatching parameters        
    hatching_params = vp.HatchingParameters(hatch_spacing=0.2, scan_angle=stripeAngleVal, hatch_length=1.0, alternate_direction=True)    

    # Cut all our fragments with a checkerboard pattern
    collection = ctx.cut_fragments(fragments=collection, tiles=ctx.checkerboard_tiles(5, 5, 0), cut_tag="collection")
    ctx.hatch_fragments(fragments=collection, hatching_params=hatching_params)

    # Unsorted fragments for the rest of the layers
    sorted_frags = collection
    print(f"Layer {layer_idx} total  collection for this layer: {len(collection)} ")



    # Do part 1 +++++
    selection_id = ctx.get_geometry_id(obj=prt1)                # Select the second part and get the geometry id
    selection_fragments = collection.select_by_geometry_id(geometry_id=selection_id)    # Filter the collection by the geometry ID
    # print(f"Part 1 Collection: {len(selection_fragments)} ")                             # Print the length of the collection to verify
    sorted_frags = selection_fragments.sort_by_area()           # Apply a different sorting algorithm 
    # Write perimeters
    writer.write_perimeters(perimeters=ctx.perimeters)
    # Write fragments
    writer.write_fragments(fragments=sorted_frags)


    # Do part 2  +++++
    selection_id = ctx.get_geometry_id(obj=prt2)            # Select the second part and get the geometry id
    selection_fragments = collection.select_by_geometry_id(geometry_id=selection_id)     # Filter the collection by the geometry ID
    # print(f"Part 2 Collection: {len(selection_fragments)} ")                         # Print the length of the collection to verify
    sorted_frags = selection_fragments.sort_by_perimeter()  # Apply a different sorting algorithm
    # Write perimeters
    writer.write_perimeters(perimeters=ctx.perimeters)
    # Write fragments
    writer.write_fragments(fragments=sorted_frags)




    # Do part 0 +++++
    selection_id = ctx.get_geometry_id(obj=prt0)
    selection_fragments = collection.select_by_geometry_id(geometry_id=selection_id)    
    # print(f"Part 0 Collection: {len(selection_fragments)} ")

    ss_Ordered_Segments = sslpbf.smartScanLPBF(selection_fragments, layer_idx, n_lyaers=2, use_Cache=True)  
    orderFragView, unorderfragsView = collection.sort_with_complement_by_ids(ss_Ordered_Segments)                 
    # Write fragments
    writer.write_fragments(fragments=orderFragView)

    # Write perimeters
    writer.write_perimeters(perimeters=ctx.perimeters)


# Use Custom CLI/DVF File Writer to Slice

# vp.slice_all(writers=dyn.DvfWriter(out_file=filepath), on_slice=cb)
vp.slice_all(writers=dyn.CliWriter(out_folder=cwd), on_slice=cb)



# Open Slice Viewer
outputfile = cwd + "/dyn_out.cli"
tab_id = dyn.gui.vector_slice_viewer.open_resource(path_or_stack=outputfile)
dyn.gui.vector_slice_viewer.set_envelope_from_plate(tab_id=tab_id, plate_dims=dyn.printer.plate)
dyn.gui.vector_slice_viewer.center_on_point(tab_id=tab_id, point=(0, 0), zoom_level=0)
