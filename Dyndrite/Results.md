---
layout: default
title: Results
description: "Initial Results with output from LPBF Pro."
parent: Dyndrite
nav_order: 6
---

# Ulendo HC Results
The image below show a comparison of a part printed on the same machine using stainless steel 316L. 


## Thermal Uniformity
The objective of the Ulendo HC algorithm is to improve the thermal uniformity of each layer. 

Builds optimized with Ulendo HC will display an improvement score of the  thermal uniformity for each layer that it processes. 

The plugin also provides the number of segments used in the optimization. If only one segment type is used in a layer, the plugin will optimize all of the segments at once. However, for typical builds, each segment type (core, upskin, downskin) will be optimized independently. 
![Thermal Uniformity Score.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/Uniformity-Score.png)


## Figure 1B Results
The Bracket show below was printed at the University of Michigan, on a research focused LPBF machine. 
When optimized with Ulendo HC the bracket prints successfully. However, when printing using the default sequence the build fails. 

![Part Comparison showing Ulendo HC optimized part printing and still functional, while the unoptimized build has failed.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/figure1b_part_comparison.png)

In other independent tests, this part proved to be a useful benchmark when comparing the performance of different slicers. This benchmark shows the clear potential of Ulendo HC to be use to address some of the common failures in LPBF machines.

The image below shows a simulation of one of the layers of the part. You can see that at the same time, the segments of the part which have been already sintered differs between the HC optimized sequence and the default scan strategy. 
![Part Comparison showing Ulendo HC optimized part printing and still functional, while the un-optimized build has failed.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/altered_sequence.png)