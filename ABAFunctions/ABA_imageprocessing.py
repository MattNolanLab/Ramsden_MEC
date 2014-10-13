'''
Code for processing images

Copyright (c) 2014, Helen Ramsden
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following
disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
disclaimer in the documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
__author__ = 'helenlramsden'
import os, re
import Image
import ImageChops, ImageOps
import numpy as np

def resizeimages(infolderpath, iseriesdict):
	'''
	Run image resize
	:param infolderpath:
	:param iseriesdict:
	:return:
	'''
	for iseries in iseriesdict.keys():
		filename = iseries + '.jpg'
		filename_exp = re.sub('ish','exp',filename)
		borderresize(filename, infolderpath, 'ish')
		borderresize(filename_exp, re.sub('ish','exp',infolderpath), 'exp')

def borderresize(filename, infolderpath, runtype):
	'''
	Resize ISH images
	:param filename:
	:param infolderpath:
	:return:
	'''
	newimagewidth = 6000/4
	newimageheight = 4500/4

	if 'ishfull' in filename: newimage = Image.new('L', (newimagewidth,newimageheight), (255) ) #white image
	else:newimage = Image.new('L', (newimagewidth,newimageheight), (0) ) #black image
	resizefactor = 1.25 # images 0.8 of original size
	try:
		ishimage = Image.open(infolderpath +filename).convert("L")
	except IOError:
		print filename, 'Image failed'
		return

	# Not used previously - remove outer border to get rid of any dark borders on original image
	ishimage = ImageOps.crop(ishimage, border=5)

	dwidth = newimagewidth - ishimage.size[0]
	dheight = newimageheight - ishimage.size[1]
	newimage.paste(ishimage, (dwidth/2,dheight/2,dwidth/2+ishimage.size[0],dheight/2+ishimage.size[1]))
	newimage = newimage.resize((int(float(newimagewidth)/resizefactor),int(float(newimageheight)/resizefactor)))
	newimage.save(re.sub('Original_%s' % runtype,'Resize_%s' % runtype, infolderpath) + filename)

def sb_images(infolderpath, outfolderpath,iseriesdict, outfile):
	'''
	Write ImageJ macro to subtract background
	:param infolderpath:
	:param outfolderpath:
	:param iseriesdict:
	:param outfile:
	:return:
	'''
	for iseries in iseriesdict.keys():
		filename = iseries + '.jpg'
		outfile.write('open("' + infolderpath + filename +'");\n')
		outfile.write('run("8-bit");\n')
		outfile.write('run("Subtract Background...", "rolling=1 light");\n') # changed from 3 for smaller images
		outfile.write('saveAs("Jpeg", "' +outfolderpath+ re.sub('.jpg','_sb.jpg',filename) + '");\n')
		outfile.write('run("Close All");\n')


def thresh_images(infolderpath, outfolderpath, iseriesdict, outfile):
	'''
	Images are thresholded for use in registration, but not for segmentation. Performance could possibly be improved by
	thresholding prior to edge detection
	:param infolderpath:
	:param outfolderpath:
	:param iseriesdict:
	:param outfile:
	:return:
	'''
	for iseries in iseriesdict.keys():
		filename = iseries + '.jpg'
		outfile.write('open("' + infolderpath + filename +'");\n')
		outfile.write('run("Auto Threshold", "method=MinError(I) white");\n')
		outfile.write('saveAs("Jpeg", "' + outfolderpath + re.sub('_sb.jpg','_sbthres.jpg',filename) + '");\n')
		outfile.write('run("Close All");\n')


def find_seg_edges(infilepath,outfilepath, iseriesdict, outfile):
	'''
	Detect the edges
	:param infilepath:
	:param outfilepath:
	:param iseriesdict:
	:param outfile:
	:return:
	'''
	for iseries in iseriesdict.keys():
		filename = iseries + '.jpg'
		outfile.write('open("' + infilepath + filename +'");\n')
		outfile.write('selectWindow("' + filename + '");\n')
		outfile.write('run("8-bit");\n')

		outfile.write('run("FeatureJ Edges", "compute smoothing=10 lower=[] higher=[]");\n') # check size for resized images
		outfile.write('selectWindow("' + filename + ' edges");\n')
		outfile.write('saveAs("Jpeg", "' + outfilepath+ re.sub('.jpg','_edges.jpg',filename) + '");\n')
		outfile.write('run("Close All");\n')

def create_seg_mask(infilepath, outfilepath, iseriesdict, outfile, thresh):
	'''
	Create segmentation mask
	:param infilepath:
	:param outfilepath:
	:param iseriesdict:
	:param outfile:
	:param thresh:
	:return:
	'''
	edgefilepath = re.sub('Segmented/','Edges/',outfilepath)
	origfilepath = re.sub('Segmented/','Resize_ish/',outfilepath)
	segorigfilepath = re.sub('Segmented/','Segmented/SegmentedOrig/',outfilepath)
	segmaskfilepath = re.sub('Segmented/','Segmented/SegmentedMask/',outfilepath)
	for iseries in iseriesdict.keys():
		filename = iseries + '.jpg'
		outfile.write('open("' + edgefilepath + filename + '");\n')
		outfile.write('run("Auto Threshold", "method=Li white");\n') # white ensures white on black background
		outfile.write('run("Fill Holes");\n')
		outfile.write('run("Watershed");\n')
		outfile.write('run("Analyze Particles...", "size=210000-Infinity circularity=0.00-1.00 show=Masks display clear summarize add");\n') # size needs altering for resized images

		outfile.write('selectWindow("Mask of ' + filename +'"); \n')
		outfile.write('saveAs("Jpeg", "' + segmaskfilepath + re.sub('_edges.jpg' , '_mask.jpg', filename) + '");\n')
		outfile.write('selectWindow("' + filename +'");\n')
		outfile.write('run("Close All");\n')


def apply_seg_mask(infilepath, outfilepath, iseriesdict):
	'''
	Apply mask to other images
	:param infilepath:
	:param outfilepath:
	:param iseriesdict:
	:return:
	'''
	sbinfilepath = re.sub('Segmented/SegmentedMask/','Thresh/',infilepath)
	origfilepath = re.sub('Segmented/','Resize_ish/',outfilepath)
	expfilepath = re.sub('Segmented/','Resize_exp/',outfilepath)
	segorigfilepath = re.sub('Segmented/','Segmented/SegmentedOrig/',outfilepath)
	segmaskfilepath = re.sub('Segmented/','Segmented/SegmentedMask/',outfilepath)
	segsbfilepath =re.sub('Segmented/','Segmented/SegmentedThresh/',outfilepath)
	segexpfilepath = re.sub('Segmented/','Segmented/SegmentedExp/',outfilepath)

	for iseries in iseriesdict.keys():
		seg_mask(iseries, sbinfilepath, segmaskfilepath, segsbfilepath,origfilepath,expfilepath,segexpfilepath,segorigfilepath)




def seg_mask(iseries, sbinfilepath, segmaskfilepath, segsbfilepath,origfilepath,expfilepath,segexpfilepath,segorigfilepath):
	#iseries is a filename, without jpg on the end and with sb on the end
	# First, apply mask to sb image - mask is black (or grey) on white background
	filename = re.sub('_mask','',iseries) + '.jpg' #this is the sb image
	# print 'Initial', filename

	maskim = Image.open(segmaskfilepath+ re.sub('.jpg','_mask.jpg',filename)).convert("L")
	# Mask not always black so first make sure it is
	threshold = 141
	maskim = maskim.point(lambda p: p > threshold and 255)

	threshfilename = re.sub('_sb','_sbthres', filename)
	sbim = Image.open(sbinfilepath + threshfilename)
	try:
		# print 'Get thresh'
		seg_sb = ImageChops.lighter(sbim,maskim)
		seg_sb.save(segsbfilepath+ re.sub('.jpg','_seg.jpg',threshfilename) )
	except IOError:
		print 'error in file'

	#Now open the original image - get rid of sb from filename
	filename = re.sub('_sb','', filename)
	origim = Image.open(origfilepath + filename).convert("L")
	seg_orig = ImageChops.lighter(origim,maskim)
	seg_orig.save(segorigfilepath+ re.sub('.jpg','_seg_orig.jpg',filename))

	#Now open the exp image and apply mask
	# First make mask white on black
	maskim = ImageChops.invert(maskim)

	# Now extract all the pixels that are white and make this region a transparent region on the mask
	maskim = maskim.convert('LA')
	datas = maskim.getdata()
	newData = list()
	for item in datas:
		if item[0] == 255:
			newData.append((255, 0))
		else:
			newData.append(item)

	maskim.putdata(newData)
	#img.save("img2.png", "PNG")
	l,a = maskim.split()

	# Check that exp file exists
	if os.path.exists(expfilepath +  re.sub('ish','exp',filename)):
		#seg_exp = ImageChops.logical_and(expim,maskim)
		expim = Image.open(expfilepath +  re.sub('ish','exp',filename)).convert("LA") # should be a grayscale image
		expim.paste(maskim, mask = a)
		expim = expim.convert("L")
		expim.save(segexpfilepath+ re.sub('.jpg','_seg_exp.tif',filename))
	else: print 'N'

def getallfiledict(filefolder, filelist, filetype, fileend='jpg'):
	'''
	Function finds all the files within a folder and returns a dictionary of their image series (val) and full filename
	 (key)
	:param filefolder:
	:param filelist:
	:param filetype:
	:param project:
	:return:
	'''
	ffilelist = re.sub('.txt',filefolder.split('/')[-2] + '.txt',filelist)
	os.system("ls %s | grep %s > %s" % (filefolder, filetype, ffilelist))
	allfilesdict = dict((line.strip(),line.strip().split('_')[0]) for line in open(ffilelist, 'r')) # key = whole filename, val = iseries
	iseriesdict = dict((line.strip().split('\t')[0].split('.' + fileend)[0], line.strip().split('\t'))
	                   for line in open(ffilelist,'r')) # key = filename without jpg, filename (replace tif with jpg)
	return allfilesdict, iseriesdict

def getnewdict(outfilefolder, filelist, preiseriesdict,fileendout, fileendin, fileend='jpg'):
	'''
	Get dictionary of images in a particular file. If file already present, don't overwrite
	'''
	print outfilefolder, fileendin,len(preiseriesdict.keys())
	[gotfilesdict,gotiseriesdict] = getallfiledict(outfilefolder, filelist, fileendout,fileend)

	gotfileskeys = [re.sub(fileendout,fileendin,g) for g in gotiseriesdict.keys()]
	print len(gotfileskeys)
	try:
		print list(preiseriesdict.keys())[0],len(gotfileskeys),gotfileskeys[0],list(preiseriesdict.keys())[0]
	except IndexError:
		print 'Empty list'
	allfiles = set(preiseriesdict.keys()).difference(gotfileskeys)
	print 'Files to be processed: ', len(allfiles)
	iseriesdict = dict((k,preiseriesdict[k]) for k in allfiles)
	return iseriesdict


def moveimages(originfolder, origfilename, maskinfolder, maskfilename,expinfolder, expfilename,outorigfolder,outexpfolder):
	'''
	Function for moving images into the centre - we didn't use this
	'''

	try:
		segorigimage = Image.open(originfolder +origfilename).convert("L")
		segexpimage = Image.open(expinfolder +expfilename).convert("L")
		maskim =  Image.open(maskinfolder + maskfilename).convert("L") # need to convert to 8 bit (not rgb)
	except IOError:
		print origfilename, 'Image failed'
		return

	threshold = 141
	maskim = maskim.point(lambda p: p > threshold and 255)
	maskim = ImageChops.invert(maskim)
	com = ndimage.measurements.center_of_mass(np.array(maskim))
	dwidth = int(com[1] - 525) # centre of mass - 600 (so leftwards will be negative)
	dheight = int(com[0] - 430) # centre of mass - 450 (so upwards will be negative)
	newsegimage = Image.new('L', (1200,900), (255) ) # white image for seg orig
	newexpimage = Image.new('L', (1200,900), (0) ) # black image for seg orig
	print dwidth, dheight
	le = up = 0; ri = segorigimage.size[0]; lo = segorigimage.size[1];left = upper = 0
	if dwidth > 0:le = int(dwidth)
	else: ri = segorigimage.size[0] +  int(dwidth); left = -dwidth
	if dheight > 0: up = int(dheight)
	else: lo = segorigimage.size[1]  + int(dheight); upper = -dheight
	box = (le, up, ri, lo)

	newsegorigimage = segorigimage.crop(box)
	newsegexpimage = segexpimage.crop(box)

	newsegimage.paste(newsegorigimage, (left,upper,left + newsegorigimage.size[0],upper + newsegorigimage.size[1])) # left, upper, right, lower
	newsegimage.save(outorigfolder +  origfilename)
	newexpimage.paste(newsegexpimage, (left,upper,left + newsegexpimage.size[0],upper + newsegexpimage.size[1])) # left, upper, right, lower
	newexpimage.save(outexpfolder +  expfilename)

