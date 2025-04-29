---
layout: default
title: MultiOptic
description: "Ulendo HC and multi-optic builds"
parent: Dyndrite
nav_order: 3
---

# Ulendo HC and Multi-Optic
To optimize the distribution of heat within a layer, Ulendo HC re-orders the order of the fragments to create a more even distribution within a particular layer. 

When running multi-optic builds this re-ordering can potentially conflict with constraints that are added during the slicing process, if all the segments are re-ordered independent of these constraints.

The example below provides a guide on how Ulendo HC can be integrated with Multi-Optic systems within the Dyndrite Environment.

Import the Ulendo HC Plugin into the project

``` python
import ulendohc.LPBFWrapper as ss
sslpbf_0 = ss.smartScanLBFPPro(laser_power=400, port=8001)
```

One strategy to allow for optimization while reducing the risk of potential failures due to multi-optic systems is to only optimize segments which are only assigned to one laser region, and not to multiple overlapping regions. 

This should preserve the optimizations made to avoid potential collisions later in the build process.



## Ulendo HC and Multi-Optic Non-Overlapping Builds

To effectively optimize for multi-optic systems it recommended to create multiple Ulendo HC Instances as shown in the following code

Users can initiate multiple independent instances of the local Ulendo HC core, using a single webserver, as shown below, or create multiple instances of the Ulendo HC server by specifying a different port number as a parameter. 

```python
# Initialize Ulendo HC
import ulendohc.LPBFWrapper as ss
sslpbf_0 = ss.smartScanLBFPPro(laser_power=400, port=8001)
sslpbf_1 = ss.smartScanLBFPPro(laser_power=400, port=8001)

# Each instances runs on its own web server
# Each web call is stateless, but each smartScanLBFPPro manages the state
print(sslpbf_0.get_Port())
print(sslpbf_1.get_Port())
```

Each instance can then be directed to address each of the regions independently
With the first instance being assigned to laser 0

```python
# Hatch laser 0 fragments
ctx.hatch_fragments(fragments=laser_0_frags, hatching_params=hatching_params)

laser_0_ss_Ordered_Segments = sslpbf_0.smartScanLPBF(laser_0_frags, n_layers=2)  
laser_0_orderFragView, laser_0_unorderfragsView = laser_0_frags.sort_with_complement_by_ids(laser_0_ss_Ordered_Segments)

# Write laser 0 fragments
writer.write_fragments(fragments=laser_0_orderFragView)
writer.write_fragments(fragments=laser_0_unorderfragsView)    
```

and the second instance assigned to laser 2

```python
# Get the Optimized Sequence from the Ulendo HC plugin
laser_1_ss_Ordered_Segments = sslpbf_1.smartScanLPBF(laser_1_frags, n_layers=2)  
laser_1_orderFragView, laser_1_unorderfragsView = laser_1_frags.sort_with_complement_by_ids(laser_1_ss_Ordered_Segments)

# Write laser 1 fragments
writer.write_fragments(fragments=laser_1_orderFragView)
writer.write_fragments(fragments=laser_1_unorderfragsView)   
```

The image below shows a a multi-optic build using four lasers. Two of the regions on the right are optimized using Ulendo HC and the optic regions on the right use the default strategy. 
![Regions that are optimized by Ulendo HC.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/PartiallyOptimizedBuild.gif)



## Ulendo HC and Multi-Optic Overlapping Builds

When running builds that have regions that overlap it could potentially be good to limit the fragments that are optimized when using Ulendo HC, to fragments that can only be assigned to one laser. Using this option will exclude segments of the build that are close to different laser regions.

```python
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
```

The image provides an example of the build area, and which areas are assigned to each laser. 
![All layer regions.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/Single_Laser_assignment_full.png)

The image below shows a build where the overlapping regions of the layer have been excluded, and only the areas shown are optimized with Ulendo HC
![Regions that are optimized by Ulendo HC.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/Single_Laser_assignment.png)


Fragments in the overlapping areas will be scanned using the typical strategy for avoiding collisions as recommended by Dyndrite

```python
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
```

