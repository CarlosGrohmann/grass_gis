# GRASS-GIS
GRASS-GIS scripts, add-ons, etc.

This is just my local repository.  
You can check all the add-ons can at the [GRASS Wiki](https://grasswiki.osgeo.org/wiki/AddOns).

[r_roughness_vector](r_roughness_vector) was used in my paper on surface roughness methods in geomorphology. Originally a bash script, it was ported to python with the help of Helmut Kudrnovsky.  
- Grohmann, C.H., Smith, M.J. & Riccomini, C., 2011. Multiscale Analysis of Topographic Surface Roughness in the Midland Valley, Scotland. Geoscience and Remote Sensing, IEEE Transactions on, 49:1200-1213. http://dx.doi.org/10.1109/TGRS.2010.2053546

[r_denoise_py](r_denoise_py) is a port of [r.denoise](http://trac.osgeo.org/grass/browser/grass-addons/grass6/raster/r.denoise/description.html) from bash to python. Originally written by John Stevenson, its purpose is to remove noise (smooth/despeckle) from topographic data, particular DEMs derived from radar data (including SRTM), using Xianfang Sun's [denoising algorithm](http://www.cs.cf.ac.uk/meshfiltering/index_files/Page342.htm). It is designed to preserve sharp edges and to denoise with minimal changes to the original data. Further information on Sun's denoising algorithm, including an example, is available [here](http://personalpages.manchester.ac.uk/staff/neil.mitchell/mdenoise/).
