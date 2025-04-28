# This is an example callback script which could be attached to the Vector Slicing Process
# To use this script select the Turbo mode, when the slicing widget is activated 
# Use the slicing callback that produces the desired callback.

# This callback specifically support the DVF format

import ulendohc.LPBFWrapper as ss
sslpbf = ss.smartScanLBFPPro()

import math
scan_angle_delta = math.radians(67)

def cb(ctx: dyn.VectorProcess, writer: dyn.VectorWriter, layer_idx):

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
    sslpbf.createBuildAreaMask(collection)

    for seg in downskin_seg:
        new_seg = collection.select_by_segment(segment=seg)
        optimized_Order = sslpbf.smartScanLPBF(new_seg, n_layers=2, reduced_Order=50)  
        optimized_ordered_Fragments, unordered_fragments = collection.sort_with_complement_by_ids(optimized_Order)   
        writer.write_fragments(fragments=optimized_ordered_Fragments)

    for seg in sdf_seg:
        new_seg = collection.select_by_segment(segment=seg)
        optimized_Order = sslpbf.smartScanLPBF(new_seg, n_layers=2, reduced_Order=50)  
        optimized_ordered_Fragments, unordered_fragments = collection.sort_with_complement_by_ids(optimized_Order)   
        writer.write_fragments(fragments=optimized_ordered_Fragments)

    for seg in core_seg:
        new_seg = collection.select_by_segment(segment=seg)
        optimized_Order = sslpbf.smartScanLPBF(new_seg, n_layers=2, reduced_Order=50)  
        optimized_ordered_Fragments, unordered_fragments = collection.sort_with_complement_by_ids(optimized_Order)   
        writer.write_fragments(fragments=optimized_ordered_Fragments)

    for seg in upskin_seg:
        new_seg = collection.select_by_segment(segment=seg)
        optimized_Order = sslpbf.smartScanLPBF(new_seg, n_layers=2, reduced_Order=50)  
        optimized_ordered_Fragments, unordered_fragments = collection.sort_with_complement_by_ids(optimized_Order)   
        writer.write_fragments(fragments=optimized_ordered_Fragments)

    for seg in other_seg:
        new_seg = collection.select_by_segment(segment=seg)
        optimized_Order = sslpbf.smartScanLPBF(new_seg, n_layers=2, reduced_Order=50)  
        optimized_ordered_Fragments, unordered_fragments = collection.sort_with_complement_by_ids(optimized_Order)   
        writer.write_fragments(fragments=optimized_ordered_Fragments)

    writer.write_perimeters(ctx.perimeters)



# Use Custom DVF File Writer to Slice
directory="C:/Users/Public/Documents/Dyndrite"

cli_writer_settings = dyn.CLIWriterSettings()
cli_writer_settings.export_type = dyn.ExportScheme.PART_AND_SUPPORTS_PER_FILE
cli_writer_settings.is_ascii = False


# Use Custom DVF File Writer to Slice
vp.slice_all(writers=dyn.CliWriter(out_folder=directory, cli_writer_settings=cli_writer_settings), on_slice=cb)