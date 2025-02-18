---
title: Home
layout: home
nav_order: 1
---

# Ulendo HC (Heat Compensation)

The Ulendo HC Desktop Application derives from the *compensation-based* technologies for additive manufacturing developed by Ulendo Technologies, Inc.. The underlying algorithm in Ulendo HC optimizes the performance of Laser Power Bed Fusion (LPBF) printers. The technology is available in this desktop application and also as a plugin to Additive Manufacturing software platforms such as Dyndrite LPBF.

Parts produced by metal LPBF printers are prone to residual stress, deformation cracks and other quality defects due to uneven temperature distribution during the printing process. To address this issue, Ulendo has developed an algorithm that optimizes the laser scan sequence resulting in a 50% reduction in mean deformation and 88% reduction in residual stress. Instead of using a trial-and-error approach to selecting a heuristic scan sequence (e.g., stripe, chessboard, spiral), Ulendo HC automatically develops a custom scan sequence based on the geometry of the part and the metal being used. Using a physics model-based and optimization-driven approach, Ulendo HC achieves higher part quality than using heuristics.

For the Ulendo HC Desktop Application, a user selects a CLI file for the part to be printed as well as the metal to be used for the part and then selects PROCESS to create an optimized CLI file to be used in the LPBF printing process. The user can examine a layer-by-layer representation of the temperature gradients in the part.   The application can be enhanced to accommodate additional file types.

[Ulendo]: https://www.ulendo.io/
[Just the Docs]: https://just-the-docs.github.io/just-the-docs/
[GitHub Pages]: https://docs.github.com/en/pages
[README]: https://github.com/just-the-docs/just-the-docs-template/blob/main/README.md
[Jekyll]: https://jekyllrb.com
[GitHub Pages / Actions workflow]: https://github.blog/changelog/2022-07-27-github-pages-custom-github-actions-workflows-beta/
[use this template]: https://github.com/just-the-docs/just-the-docs-template/generate
