---
layout: default
title: Advanced Examples
description: "Understanding the Capabilities of the programming interface."
parent: Dyndrite
nav_order: 4
---

# Ulendo HC Examples
In the main installation directory, users can browse the examples directory, which provides guides on how the UlendoHC plugin can be best integrated into their workflow. 

![Part Comparison showing Ulendo HC optimized part printing and still functional, while the unoptimized build has failed.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/UlendoHC_MainDirectory.png)

If you chose the default installation location, it will be available in the "C:\Program Files\UlendoHC\examples\" folder. 

This folder contains examples which are compatible for some of the major revisions of the Dyndrite software. Select the folder that contains the version nearest your current installation version. 

![Included Examples.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/UlendoHC_ExamplesDirectory.png)

For ease of use you can open these examples directly from your favorite python editor. The most recent folder indicates the most recent version of the Dyndrite software against which the updates have been tested. 

![VSCode with Ulendo HC examples folder.](https://s2aulendo.github.io/HeatCompensation-Docs/assets/images/UlendoHC_Examples_Editor.png)

# Thermal Uniformity
The objective of the Ulendo HC algorithm is to improve the thermal uniformity of each layer. 

When successfully launched, the plugin will provide an overall metric on the improvement of the relative thermal uniformity for each layer that it processes. 

The plugin also provides the number of segments used in the optimization. If only one segment type is used in a layer, the plugin will optimize all of the segments at once. However, for typical builds, each type of segment will be optimized independently. 


If you run into any issues launching the examples with your current version of the Dyndrite software, contact ulendo at support @ ulendo . io.
