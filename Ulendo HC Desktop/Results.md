---
layout: default
title: Results
description: "A Result overview of the Dyndrite LPBF Integration."
parent: Autodesk Ulendo HC
nav_order: 4
---

# Ulendo HC Results

The results section provides a side-by-side comparison of the pre-optimized and post-optimized hatch sequences for each layer of the CLI file. This allows users to visualize how the sequence has been reordered to promote more even heat distribution, reducing the likelihood of deformities in printed parts.

### Key Features:
1. **Before and After Visualization**:  
   - By default, the app displays the optimized version of the hatch patterns.  
   - You can toggle the **"Show Original"** option to view the original sequence side by side with the optimized version.
2. **Interactive Slider**:  
   - Use the **layer slider** to navigate through individual layers of the model.  
   - Additionally, the **hatch slider** allows you to view the sequence of hatches being lasered within a layer.
3. **Playback Feature**:  
   - Click the **play button** to animate the sequence of hatches for a layer.  
   - This helps visualize the order in which hatches are lasered during the printing process.
4. **Heat Dissipation Visualization**:  
   - The app uses a fading color scheme to represent the relative timing of the lasered hatches in a layer.  
   - Newly lasered hatches are displayed in **red**, gradually fading through **purple**, and finally to **blue** to indicate that the heat has dissipated.  
   - **Note**: This is a conceptual representation of the heat dissipation and not an accurate heat map. Future updates will include a more realistic heat distribution model.

The optimized sequence shown in the results demonstrates how the hatch patterns have been reordered to minimize localized heating and ensure uniform cooling across the layer. This improvement significantly enhances the overall print quality and reduces deformation risks, providing a reliable foundation for high-precision manufacturing.
