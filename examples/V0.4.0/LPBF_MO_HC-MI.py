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
sslpbf_1 = ss.smartScanLBFPPro(laser_power=400, port=8001)

# Each instances runs on its own web server
# Each web call is stateless, but each smartScanLBFPPro manages the state
print(sslpbf_0.get_Port())
print(sslpbf_1.get_Port())

# open Dyndrite LPBF Pro
import dyndrite
try:
    # tries to use an existing instance of Dyndrite LPBF Pro
    dyn = dyndrite.connect(connect_attempts=2)
except:
    # if it fails, opens new instance of Dyndrite LPBF Pro
    dyn = dyndrite.launch()

# Set the printer size
dyn.printer.plate = (280, 280)

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

# Create segmentation strategy for the part
sst0 = zoner.new_segmentation_strategy(core_id=core_laser_0, alternate_segments=[core_laser_1, core_laser_2, core_laser_3])

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

# Create laser_fov_dict, which is the x and y dimensions the laser can scan
laser_fov_dict = {'laser_0': {'x_start': 0, 'x_end': 40, 'y_start': 0, 'y_end': 40},
                  'laser_1': {'x_start': 0, 'x_end': 40, 'y_start': -40, 'y_end': 0},
                  'laser_2': {'x_start': -40, 'x_end': 0, 'y_start': -40, 'y_end': 0},
                  'laser_3': {'x_start': -40, 'x_end': 0, 'y_start': 0, 'y_end': 40}}

# Create a tile_points_dict to hold the cutting tiles for each laser
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


# Create the cutting tiles for each laser and add to tile_points_dict
for key, value in laser_fov_dict.items():
    polygon_path = create_rectangle_polygon(x_start=laser_fov_dict[key]['x_start'],
                                            x_end=laser_fov_dict[key]['x_end'],
                                            y_start=laser_fov_dict[key]['y_start'],
                                            y_end=laser_fov_dict[key]['y_end'])
    tile_points_dict[key] = [dyn.CuttingPolygon(outer_loop=polygon_path)]


def cb(ctx: dyn.LayerContext, writer: dyn.VectorWriter, layer_idx):
    '''This callback function will write the perimeter of our original model,
    but internally the fragments will be separated out into different laser
    assignments
    '''

    # Get the layer fragments
    collection = ctx.get_fragments()

    # Calculate the scan angle
    scan_angle = layer_idx * 0.5

    # Create hatching parameters, these will be the same for every laser
    hatching_params = vp.HatchingParameters(hatch_spacing=0.2,
                                            scan_angle=scan_angle)

    # Create a custom cutting tile for each of the laser areas
    laser_0_tile = ctx.custom_cutting_tiles(cutting_polygons=tile_points_dict['laser_0'])
    laser_1_tile = ctx.custom_cutting_tiles(cutting_polygons=tile_points_dict['laser_1'])
    laser_2_tile = ctx.custom_cutting_tiles(cutting_polygons=tile_points_dict['laser_2'])
    laser_3_tile = ctx.custom_cutting_tiles(cutting_polygons=tile_points_dict['laser_3'])

    # Get all fragments in laser 0 field of view
    laser_0_frags = ctx.cut_fragments(fragments=collection, tiles=laser_0_tile, cut_tag="laser_0")

    # Get all fragments in laser 1 field of view
    laser_1_frags = ctx.cut_fragments(fragments=collection, tiles=laser_1_tile, cut_tag="laser_1")

    # Get all fragments in laser 2 field of view
    laser_2_frags = ctx.cut_fragments(fragments=collection, tiles=laser_2_tile, cut_tag="laser_2")

    # Get all fragments in laser 3 field of view
    laser_3_frags = ctx.cut_fragments(fragments=collection, tiles=laser_3_tile, cut_tag="laser_3")



    # Reassign the segments ids to core_laser_0, so the laser_index is changed
    ctx.reassign_segment_ids(collection=laser_0_frags, segment_id=core_laser_0)

    # Stripe laser 0 fragments
    laser_0_frags = ctx.cut_fragments(fragments=laser_0_frags, tiles=ctx.stripe_tiles(2, 0, 0), cut_tag="laser_0_frags")

    # Hatch laser 0 fragments
    ctx.hatch_fragments(fragments=laser_0_frags, hatching_params=hatching_params)

    laser_0_ss_Ordered_Segments = sslpbf_0.smartScanLPBF(laser_0_frags, n_layers=2)  
    laser_0_orderFragView, laser_0_unorderfragsView = laser_0_frags.sort_with_complement_by_ids(laser_0_ss_Ordered_Segments)

    # Write laser 0 fragments
    writer.write_fragments(fragments=laser_0_orderFragView)
    writer.write_fragments(fragments=laser_0_unorderfragsView)    




    # Reassign the segments ids to core_laser_1, so the laser_index is changed
    ctx.reassign_segment_ids(collection=laser_1_frags, segment_id=core_laser_1)

    # Stripe laser 1 fragments
    laser_1_frags = ctx.cut_fragments(fragments=laser_1_frags, tiles=ctx.stripe_tiles(2, 0, 0), cut_tag="laser_1_frags")
    # Hatch laser 1 fragments
    ctx.hatch_fragments(fragments=laser_1_frags, hatching_params=hatching_params)

    # Get the Optimized Sequence from the Ulendo HC plugin
    laser_1_ss_Ordered_Segments = sslpbf_1.smartScanLPBF(laser_1_frags, n_layers=2)  
    laser_1_orderFragView, laser_1_unorderfragsView = laser_1_frags.sort_with_complement_by_ids(laser_1_ss_Ordered_Segments)

    # Write laser 1 fragments
    writer.write_fragments(fragments=laser_1_orderFragView)
    writer.write_fragments(fragments=laser_1_unorderfragsView)    
    # Write laser 1 fragments



    # Reassign the segments ids to core_laser_2, so the laser_index is changed
    ctx.reassign_segment_ids(collection=laser_2_frags, segment_id=core_laser_2)
    # Stripe laser 2 fragments
    laser_2_frags = ctx.cut_fragments(fragments=laser_2_frags, tiles=ctx.stripe_tiles(2, 0, 0), cut_tag="laser_2_frags")
    # Hatch laser 2 fragments
    ctx.hatch_fragments(fragments=laser_2_frags, hatching_params=hatching_params)
    # Write laser 2 fragments
    writer.write_fragments(fragments=laser_2_frags)


    # Reassign the segments ids to core_laser_3, so the laser_index is changed
    ctx.reassign_segment_ids(collection=laser_3_frags, segment_id=core_laser_3)
    # Stripe laser 3 fragments
    laser_3_frags = ctx.cut_fragments(fragments=laser_3_frags, tiles=ctx.stripe_tiles(2, 0, 0), cut_tag="laser_3_frags")
    # Hatch laser 3 fragments
    ctx.hatch_fragments(fragments=laser_3_frags, hatching_params=hatching_params)
    # Write laser 3 fragments
    writer.write_fragments(fragments=laser_3_frags)

    # Write the contours
    writer.write_perimeters(perimeters=ctx.get_perimeters())


# Create our output directory
out_dir = "C:/Users/Public/Documents/Dyndrite/tutorial_multi_laser"
os.makedirs(out_dir, exist_ok=True)

# Run the slicer, using our callback function (cb)
vp.slice_all(writers=dyn.DvfWriter(str(out_dir + "/tutorial_multi_laser.dvf")),
             on_slice=cb)

dyn.gui.vector_slice_viewer.open_resource(path_or_stack=out_dir + "/tutorial_multi_laser.dvf")