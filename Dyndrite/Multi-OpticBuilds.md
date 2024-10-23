---
layout: default
title: MultiOptic
description: "Uses Ulendo HC when running multi-optic builds"
parent: Dyndrite
nav_order: 3
---

# Ulendo HC and Multi-Optic
To optimize the distribution of heat within a layer, Ulendo HC re-orders the order of the fragments to create a more even distribution within a particular layer. 

When running multi-optic builds this re-ordering can potentially conflict with constraints that are added during the slicing process, if all the segments are re-ordered independent of these constraints.

The example below provides a guide on how Ulendo HC can be integrated with Multi-Optic systems within the Dyndrite Environment

Import the Ulendo HC Plugin into the project

``` python
import ulendohc.LPBFWrapper as ss
sslpbf_0 = ss.smartScanLBFPPro(laser_power=400, port=8001)
```

One strategy to allow for optimization while reducing the risk of potential failures due to multi-optic systems is to only optimize segments which are only assigned to one laser region, and not to multiple overlapping regions. 

This should preserve the optimizations made to avoid potential collisions later in the build process.



## Ulendo HC and Multi-Optic Overlapping

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


## Ulendo HC and Multi-Optic Overlapping
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

![Regions that are optimized by Ulendo HC.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/Single_Laser_assignment.png)


![All layer regions.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/Single_Laser_assignment_full.png)


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


In other independent tests, this part proved to be a useful benchmark when comparing the performance of different slicers. This benchmark shows the clear potential of UlendoHC to be use to address some of the common failures in LPBF machines.

The image below shows a simulation of one of the layers of the part. You can see that at the same time, the segments of the part which have been already sintered differs between the HC optimized sequence and the default scan strategy. 
![Part Comparison showing Ulendo HC optimized part printing and still functional, while the un-optimized build has failed.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/altered_sequence.png)