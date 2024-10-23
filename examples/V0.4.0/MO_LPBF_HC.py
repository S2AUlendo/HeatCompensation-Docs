import time, os, sys


# Ulendo HC example with Multi-Optic and Multi-Instance Smart Scan
# This is a simple example showing how a Ulendo HC can be integrated with the 
# Multi-Optic functionality available in the Dyndrite Software
# In this example, 2 of the laser sequences are optimized with SmartScan
# While the other optics are not optimized and use the default strategy
# In this example the optic regions are each optimized independently 
# - with sslpbf_0 and sslpbf_1 each maintaining the state for each region


# Initialize Ulendo HC
import ulendohc.LPBFWrapper as ss
sslpbf_0 = ss.smartScanLBFPPro(laser_power=400, port=8001)


import time
tic = time.perf_counter()
# sslpbf_0 = ss.smartScanLBFPPro(laser_power=400, port=8001)

# Each instances runs on its own web server
# Each web call is stateless, but each smartScanLBFPPro manages the state
print(sslpbf_0.get_Port())


# open Dyndrite LPBF Pro
import dyndrite
try:
    # tries to use an existing instance of Dyndrite LPBF Pro
    dyn = dyndrite.connect(connect_attempts=2)
except:
    # if it fails, opens new instance of Dyndrite LPBF Pro
    dyn = dyndrite.launch()

# Set the printer size
dyn.printer.plate = (600, 600)

# Import part
# This function can also be called with a hard path as follows.
# prt0 = dyn.ops.import_part(path="C:/Users/Public/Documents/Dyndrite/Python/sample_data/step/multi_laser_assignment.step", ...)
prt0 = dyn.ops.import_part(path=dyn.paths.samples / "step" / "multi_laser_assignment.step",
                           auto_center=False,
                           transform=None,
                           translate_only=None,
                           brep_sampling_parameters=None)
prt0_rgn0 = prt0.region[0]
# Recenter the part on the build plate based on the parts world limits
center_x = prt0.world_limits.center.x
center_y = prt0.world_limits.center.y

# Move the center of the part to 0,0 of the build plate
prt0.position = dyn.Vector3(-center_x, -center_y, 0)

# Create a new VectorProcess object and store its Zoner and toolpather
# in a local variable
vp = dyn.vector_process
zoner = vp.zoner
toolpather = vp.toolpather

# Set the slicing parameters
vp.slicing_thickness = .5
vp.slicing_resolution = dyn.Vector2(.12, .12)

# Create a build style for each laser, assigning the laser_index
laser_0 = toolpather.new_build_style(laser_focus=0, laser_index=0, laser_power=400, laser_speed=20)

laser_1 = toolpather.new_build_style(laser_focus=0, laser_index=1, laser_power=400, laser_speed=20)

laser_2 = toolpather.new_build_style(laser_focus=0, laser_index=2, laser_power=400, laser_speed=20)

laser_3 = toolpather.new_build_style(laser_focus=0, laser_index=3, laser_power=400, laser_speed=20)


# Create a segment type for each of the lasers
core_laser_0 = zoner.add_segment(zone_type=zoner.PartZoneType.CORE, color=(255, 0, 0))

core_laser_1 = zoner.add_segment(zone_type=zoner.PartZoneType.CORE, color=(0, 255, 0))

core_laser_2 = zoner.add_segment(zone_type=zoner.PartZoneType.CORE, color=(0, 0, 255))

core_laser_3 = zoner.add_segment(zone_type=zoner.PartZoneType.CORE, color=(255, 255, 0))


segment_dict = {'laser_0': core_laser_0, 'laser_1': core_laser_1,
                'laser_2': core_laser_2, 'laser_3': core_laser_3, }

# Dictionary to hold where tiles should be sorted on for each laser
sort_point_dict = {'laser_0': dyn.Vector2(280, 280), 'laser_1': dyn.Vector2(280, -280),
                   'laser_2': dyn.Vector2(-280, -280), 'laser_3': dyn.Vector2(-280, 280)}


# Create segmentation strategy for the part
sst0 = zoner.new_segmentation_strategy(core_id=core_laser_0,
                                       alternate_segments=[core_laser_1,
                                                           core_laser_2,
                                                           core_laser_3])

# Set up our build style mappings for our hatching
hatch_config = {
    core_laser_0: laser_0,
    core_laser_1: laser_1,
    core_laser_2: laser_2,
    core_laser_3: laser_3
}

perimeter_config = {
    core_laser_0: [laser_0],
    core_laser_1: [laser_1],
    core_laser_2: [laser_2],
    core_laser_3: [laser_3]
}

# Create an empty contour strategy
cst0 = toolpather.new_contour_strategy()

# Create some default hatching parameters
htp0 = dyn.HatchingParameters(hatch_spacing=0.2, scan_angle=45)

# Create a new toolpath schema
schema0 = toolpather.new_toolpath_schema(segmentation_strategy=sst0,
                                         contour_strategy=cst0)

# Set the build style configs
schema0.set_hatch_config(config=hatch_config)
schema0.set_all_perimeter_configs(config=perimeter_config)

# Set the default hatching
schema0.fill_default_hatch_generation(params=htp0)

# Prune and validate the schemas
toolpather.prune_all_schemas()
toolpather.validate_all_schemas()

# Apply the schema to our part
vp.apply_schema(geometry=dyn.part[0], schema=schema0)

# Finalize the configuration
vp.finalize()

# Create laser_fov_dict, which is the different tiles on the build area the
# the lasers can address, and which laser can address them
laser_fov_dict = {'tile_1': {'points': {'x_start': -40, 'x_end': -10,
                                        'y_start': 10, 'y_end': 40},
                             'lasers': (3,)},
                  'tile_2': {'points': {'x_start': -10, 'x_end': 10,
                                        'y_start': 10, 'y_end': 40},
                             'lasers': (0, 3)},
                  'tile_3': {'points': {'x_start': 10, 'x_end': 40,
                                        'y_start': 10, 'y_end': 40},
                             'lasers': (0,)},
                  'tile_4': {'points': {'x_start': -40, 'x_end': -10,
                                        'y_start': -10, 'y_end': 10},
                             'lasers': (2, 3)},
                  'tile_5': {'points': {'x_start': -10, 'x_end': 10,
                                        'y_start': -10, 'y_end': 10},
                             'lasers': (0, 1, 2, 3)},
                  'tile_6': {'points': {'x_start': 10, 'x_end': 40,
                                        'y_start': -10, 'y_end': 10},
                             'lasers': (0, 1)},
                  'tile_7': {'points': {'x_start': -10, 'x_end': -40,
                                        'y_start': -40, 'y_end': -10},
                             'lasers': (2,)},
                  'tile_8': {'points': {'x_start': -10, 'x_end': 10,
                                        'y_start': -40, 'y_end': -10},
                             'lasers': (1, 2)},
                  'tile_9': {'points': {'x_start': 10, 'x_end': 40,
                                        'y_start': -40, 'y_end': -10},
                             'lasers': (1,)},
                  }

# Create a tiles_dict to hold the cutting tiles for each unique FoV
tile_points_dict = {}


def create_rectangle_polygon(x_start, x_end, y_start, y_end):
    '''This function creates a polygon rectangle from the length and width
    and returns a Path of X and Y coordinates for the polygon'''

    # Define the coordinates for the rectangle
    x = [x_start, x_end, x_end, x_start, x_start]
    y = [y_start, y_start, y_end, y_end, y_start]
    x_y_list = list(zip(x, y))
    vector_point_list = [dyn.Vector2(i[0], i[1]) for i in x_y_list]

    polygon_path = dyn.Path(vector_point_list)
    return polygon_path


# Create the cutting tiles for each laser and add to tiles_dict along
# with the lasers that can address that cut tile
for key, value in laser_fov_dict.items():
    tile_points_dict[key] = {}
    polygon_path = create_rectangle_polygon(x_start=laser_fov_dict[key]['points']['x_start'],
                                            x_end=laser_fov_dict[key]['points']['x_end'],
                                            y_start=laser_fov_dict[key]['points']['y_start'],
                                            y_end=laser_fov_dict[key]['points']['y_end'])
    tile_points_dict[key]['cut_poly'] = [dyn.CuttingPolygon(outer_loop=polygon_path)]
    tile_points_dict[key]['lasers'] = laser_fov_dict[key]['lasers']


import math


def cb(ctx: dyn.LayerContext, writer: dyn.VectorWriter, layer_idx):
    '''This callback function will write the perimeter of our original model,
    as well as assigning the fragments inside each FoV tile to the lasers,
    keeping the number of fragments per laser balanced
    '''

    # Get all layer fragments
    collection = ctx.get_fragments()

    # Calculate the scan angle
    scan_angle = layer_idx * 0.5

    # Set default hatching parameters
    hatching_params = vp.HatchingParameters(hatch_spacing=0.2, scan_angle=scan_angle)

    # Cut all our fragments with a checkerboard pattern
    collection = ctx.cut_fragments(fragments=collection, tiles=ctx.checkerboard_tiles(5, 5, 0), cut_tag="collection")

    # Create a dictionary to hold the fragments for each FoV tile
    fragments_dict = {}

    # Create a dictionary to track how many fragments each laser is assigned
    laser_fragment_count = {'laser_0': 0, 'laser_1': 0, 'laser_2': 0, 'laser_3': 0}

    # Loop through tile_points_dict, creating cutting polygons for each tile
    for tile_id, values in tile_points_dict.items():
        # Create cutting tile
        cutting_tile = ctx.custom_cutting_tiles(cutting_polygons=values['cut_poly'])
        # Cut layer fragments with our cutting polygon and store the fragments
        # in fragments_dict
        tile_fragments = ctx.cut_fragments(fragments=collection,
                                           tiles=cutting_tile,
                                           cut_tag=tile_id)
        fragments_dict[tile_id] = tile_fragments

    # Go through and write all fragments that only have one laser assignation
    for key, value in tile_points_dict.items():
        # if there is just one laser assigned, redo all fragments in that style
        if len(value['lasers']) == 1:
            # Reassign the segment ids to the laser segment style,
            # so the laser_index is changed
            ctx.reassign_segment_ids(collection=fragments_dict[key], segment_id=segment_dict[f"laser_{value['lasers'][0]}"])
            # Increase the fragment count for this laser
            laser_fragment_count[f"laser_{value['lasers'][0]}"] += fragments_dict[key].size()
            # Hatch fragments
            ctx.hatch_fragments(fragments=fragments_dict[key], hatching_params=hatching_params)

             # Get the Optimized Sequence from the Ulendo HC plugin
            laser_1_ss_Ordered_Segments = sslpbf_0.smartScanLPBF(fragments_dict[key], n_layers=2)  
            laser_1_orderFragView, laser_1_unorderfragsView = fragments_dict[key].sort_with_complement_by_ids(laser_1_ss_Ordered_Segments)
            writer.write_fragments(fragments=laser_1_orderFragView)
            writer.write_fragments(fragments=laser_1_unorderfragsView)  


            # Write fragments
            # writer.write_fragments(fragments=fragments_dict[key])

    # Go through tiles with multi-laser assignation
    for key, value in tile_points_dict.items():
        if len(value['lasers']) > 1:

            # Collect the number of fragments, and the fragments themselves
            overlap_frag_count = fragments_dict[key].size()
            overlap_fragments = fragments_dict[key]

            # Create two dicts:
            # tile_laser_dict holds the total fragments for the lasers on
            # this tile
            # overlap_count holds the number of fragments each laser has in the
            # overlap region
            tile_laser_dict = {}  # Tracks the laser fragments on this tile
            overlap_count = {}  # Tracks the overlap split between lasers

            # Loop through the lasers assigned to this tile, and collect
            # how many fragments they have in total, and instantiate them
            # in the overlap_count dict
            for laser in value['lasers']:
                tile_laser_dict[f'laser_{laser}'] = laser_fragment_count[f'laser_{laser}']
                overlap_count[f'laser_{laser}'] = 0

            # Loops through the size of the overlap region, assigning a
            # fragment to the laser that current has fewer fragments
            for i in range(overlap_frag_count):
                min_key = min(tile_laser_dict, key=lambda k: tile_laser_dict[k])
                overlap_count[min_key] += 1
                laser_fragment_count[min_key] += 1
                tile_laser_dict[min_key] += 1

            # Divide each value by the total number of fragments in the overlap
            overlap_percent_dict = {key: value / overlap_frag_count for key, value in overlap_count.items()}

            # We need to add a segment % onto the first overlap %, so they
            # don't scan over the same spot
            # This should mean that one ends at fragment x, and the next
            # starts at x + 1
            overlap_increment = 1 / overlap_frag_count

            # Calculate the start and end %s of each laser in the overlap
            # Need to add an increment onto the start if it's not the first,
            # don't add if it's already 100% (1.0)
            overlap_percent_cumul_dict = {}
            start_percentage = 0.0
            for item, percentage in overlap_percent_dict.items():
                # print(layer_idx, percentage)
                if percentage == 0:
                    continue  # skip any 0%s
                end_percentage = start_percentage + percentage
                overlap_percent_cumul_dict[item] = ((start_percentage + overlap_increment) if start_percentage !=
                                                    0.0 and start_percentage != 1.0 else start_percentage, end_percentage)
                start_percentage = end_percentage

            # Sort and hatch the fragments by iterating through the dictionary
            # and using the values for the % filter - rounding them up
            # Use first_laser_pass to sort the fragments on the first pass,
            # so that we know they are in a good order to be scanned
            first_laser_pass = True
            for laser_id, percentage_values in overlap_percent_cumul_dict.items():
                if first_laser_pass:
                    sort_dir = sort_point_dict[laser_id]
                    first_laser_pass = False
                frags_to_write = overlap_fragments.sort_by_distance(ref_point=sort_dir).filter_by_percentage(
                    min_percentage=math.ceil(percentage_values[0] * 100),
                    max_percentage=math.ceil(percentage_values[1] * 100))
                # Reassign fragment type to the right laser
                ctx.reassign_segment_ids(collection=frags_to_write,
                                         segment_id=segment_dict[laser_id])
                # Hatch the fragments with the default type
                ctx.hatch_fragments(fragments=frags_to_write,
                                    hatching_params=hatching_params)
                # Write the fragments
                writer.write_fragments(fragments=frags_to_write)

    # Write the contours
    writer.write_perimeters(perimeters=ctx.get_perimeters())


# Create our output directory
out_dir = "C:/Users/Public/Documents/Dyndrite/tutorial_multi_laser"
os.makedirs(out_dir, exist_ok=True)

# Run the slicer, using our callback function (cb)
vp.slice_all(writers=dyn.DvfWriter(out_dir + "/tutorial_multi_laser_overlap_quad.dvf"), on_slice=cb)

toc = time.perf_counter()
print(f"Total runtime{toc - tic:0.4f} seconds", 0)   

dyn.gui.vector_slice_viewer.open_resource(path_or_stack=out_dir + "/tutorial_multi_laser_overlap_quad.dvf")