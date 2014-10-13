'''
Code for error analysis

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

import Image, ImageChops
import numpy as np
from scipy import ndimage
from GenericFunctions import checkOSpath, adjust_spines,st
import matplotlib.pyplot as plt
plt.rc('ytick', labelsize=12)
plt.rc('xtick', labelsize=12)
plt.rc('axes', labelsize=12)
plt.rc('axes', titlesize=20)


def checksegmented(segmaskfilepath,filedict,resultsfilepath):
	'''
	FUNCTION runs through all segmented masks and checks location of centre of mass and size of mask
	input SegmentedMask/
	output is a list containing name of file, size of mask,
	'''
	newfile = open(resultsfilepath + 'maskstatssize.txt','w')
	for f in filedict:
		# print f
		newfile.write(f )
		for filepath in [segmaskfilepath]:#, segmask2filepath]:
			maskim =  Image.open(filepath+ f).convert('L') # need to convert to 8 bit (not rgb)
			maskim = ImageChops.invert(maskim)
			maskarray = np.array(maskim)
			# print maskarray.shape
			com = ndimage.measurements.center_of_mass(maskarray)
			blackpixels = np.nonzero(maskarray==0)
			whitepixels = np.nonzero(maskarray>0)
			# print len(blackpixels[0]),len(whitepixels[0])
			masksize = len(blackpixels[0])
			newfile.write('\t' + '\t'.join([str(com[0]),str(com[1]),str(masksize)]))
		newfile.write('\n')

def plotmi():
	'''
	Plot the distribution of MI scores from the registration output
	'''
	milog = np.loadtxt('alllogdata.txt',delimiter = '\t',dtype = float,usecols=[2,3])
	diffs = milog[:,0] - milog[:,1]
	milognew = np.ma.masked_array(milog, np.isnan(milog))
	diffsnew = np.ma.masked_array(diffs, np.isnan(diffs))

	# Get rid of nans
	milogmaskpre = np.ma.masked_array(milog[:,0],np.isnan(milog[:,0]))
	milogmaskpost = np.ma.masked_array(milog[:,1],np.isnan(milog[:,1]))
	milogmaskpre = milogmaskpre[milogmaskpre>-1000]
	milogmaskpost = milogmaskpost[milogmaskpost>-1000]


	fig = plt.figure(figsize = (8,8))
	fig.subplots_adjust(bottom=0.2)
	fig.subplots_adjust(left=0.2)
	ax = fig.add_subplot(1,1,1)
	adjust_spines(ax, ['left','bottom'])
	cols = ['r','b','k','g','m','y']
#	histpre, binspre = np.histogram(milogmaskpre, bins=20)
#	histpost, binspre = np.histogram(milogmaskpre, bins=20)
	ax.hist(milogmaskpre, bins=20,histtype='step',color='b', range = [-600,0])
	ax.hist(milogmaskpost,bins=20,histtype='step',color='g', range = [-600,0]) # normed=True,
	[xmin, xmax, ymin, ymax] = ax.axis()
	ax.set_yticks([ymin,ymax])
	ax.set_yticklabels([int(ymin),int(ymax)], fontsize = 25)
	ax.xaxis.set_label_coords(0.5, -0.15)
	ax.set_xticks([xmin,xmax])
	ax.set_xticklabels([xmin,xmax], fontsize = 25)
	ax.set_xlabel('Joint Entropy', fontsize = 25)
	ax.set_ylabel('Frequency', fontsize = 25)
	ax.yaxis.set_label_coords( -0.15, 0.5)

	fig.savefig('MIlogdata.png', transparent = True)

