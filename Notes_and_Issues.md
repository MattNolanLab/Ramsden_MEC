###Notes:
- We didn't process images with '*' in the gene name - although they were converted to ASTERISK - at some point we lost them
- It is very important to make sure that files are saved in grayscale, not RGB format. We have also saved expression files as uncompressed tifs to prevent an alteration.

###Possible improvements:
- Some images were larger than the 6000* 5000 that we allowed- this should be increased before downloading
- On some images there is a black outline that subsequently influences image processing. We did not remove this but have included code to do so in the demo
- It may be possible to improve registration by first using a median filter to strengthen edges. We used this to reregister images for Figure 4
- Brain sections could be moved into the centre of each image to improve registration performance (see moveimages in ABA_imageprocessing)

### Required Python libraries:
- Matplotlib
- Numpy
- PIL
- Pandas
- Scipy
- PIL
