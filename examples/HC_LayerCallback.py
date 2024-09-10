# This is an example script which could be attached to the dyndrite software
# and added to the custom slicer scripts in Turbo mode, when selected
# This will call the SmartScan plugin directly from the slicer


from ulendohc import LPBFWrapper as ss
sslpbf = ss.smartScanLBFPPro()
stripeAngleVal = 67

vp.slicing_thickness = 0.1
vp.slicing_resolution = dyn.Vector2(0.03, 0.03)
vp.finalize()

def cb(ctx: dyn.VectorProcess, writer: dyn.VectorWriter, layer_idx):
    print("Slicing Layer: " + str(layer_idx))

    # DynDocs Within your Callback Function you can retrieve the initial group of unsorted and uncut fragments with
    # Unsorted fragments for the rest of the layers
    collection = ctx.get_fragments()

    # Set default hatching parameters
    hatching_params = vp.HatchingParameters(hatch_spacing=0.2, scan_angle=stripeAngleVal, hatch_length=1.0, alternate_direction=True)

    # Cut all our fragments with a checkerboard pattern
    collection = ctx.cut_fragments(fragments=collection, tiles=ctx.checkerboard_tiles(5, 5, 0), cut_tag="collection")

    ctx.hatch_fragments(fragments=collection, hatching_params=hatching_params)
          
    ss_Ordered_Segments = sslpbf.smartScanLPBF(collection, n_layers=2)  
    orderFragView, unorderfragsView = collection.sort_with_complement_by_ids(ss_Ordered_Segments)   

    # Write fragments
    writer.write_fragments(fragments=orderFragView)

    # Write perimeters
    writer.write_perimeters(perimeters=ctx.perimeters)



# Use Custom DVF File Writer to Slice
cwd = os.getcwd()

vp.slice_all(writers=dyn.CliWriter(out_folder=cwd), on_slice=cb)

# Open Slice Viewer
outputfile = cwd + "/dyn_out.cli"
tab_id = dyn.gui.vector_slice_viewer.open_resource(path_or_stack=outputfile)
dyn.gui.vector_slice_viewer.set_envelope_from_plate(tab_id=tab_id, plate_dims=dyn.printer.plate)
dyn.gui.vector_slice_viewer.center_on_point(tab_id=tab_id, point=(0, 0), zoom_level=0)
