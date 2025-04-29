---
layout: default
title: Results
description: "An overview of the Dyndrite LPBF Integration."
parent: Index
nav_order: 2
---

# Ulendo HC Results
This section provides an overview of some of the early results shown by when optimizing parts using UlendoHC. The image below show a comparison of a part printed on the same machine using stainless steel 316L. 

When printing with Ulendo HC the part prints successfully. However, when printing without the optimized sequence the build fails. 

![Part Comparison showing Ulendo HC optimized part printing and still functional, while the unoptimized build has failed.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/figure1b_part_comparison.png)

In other independent tests, this part proved to be a useful benchmark when comparing the performance of different slicers. This benchmark shows the clear potential of UlendoHC to be use to address some of the common failures in LPBF machines.

The image below shows a simulation of one of the layers of the part. You can see that at the same time, the segments of the part which have been already sintered differs between the HC optimized sequence and the default scan strategy. 
![Part Comparison showing Ulendo HC optimized part printing and still functional, while the un-optimized build has failed.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/altered_sequence.png)