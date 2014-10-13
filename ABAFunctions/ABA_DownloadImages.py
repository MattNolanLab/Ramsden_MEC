'''
File contains functions to download images from ABA
To run:
downloadjpgbylistnew('Temp/','Temp/','Example')

File formats:
http://www.brain-map.org/aba/api/image?zoom=5&top=0&left=0&width=6000&
height=5000&mime=2&path=/external/aibssan/production7/Hras1_b04-0116_15861/
zoomify/primary/0100042475/Hras1_10_0100042475_B.aff

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

import re, os
import urllib
from time import localtime, strftime 

datestr = strftime("%y%m%d_%H.%M",localtime())

def downloadjpgbylistnew(folderaim, oldfolder, genelist):
	'''
	Download a set of images from the ABA API
	:param folderaim: the folder containing the list of genes that you want to download, in a file called 'iseries.txt'
	- this should contain a list of image series separated by \n
	:param oldfolder: path to save files to
	:param genelist:
	:return:
	'''
	# lat = 0; med = 100 # min/max value of range for referenceatlasindex
	lat = 0; med = 1400 #min/max value of range for position

	coords = ['0', '0', '6000', '5000'] # bounding box surrounding image

	iserieslist = [line.strip().split('\t')[1] for line in open(folderaim+ genelist + 'iseries.txt')]
	downloadjpg(iserieslist, '3',coords, '2', oldfolder,lat,med, oldfolder)
			
def downloadjpg(iserieslist, zoom, coords, mime, savefolder,lat,med, oldfolder):
	'''

	:param iserieslist: list of all genes (iseries) to have figures printed
	:param zoom: (str) resolution
	:param coords: list of str coords - left, upper, right, lower
	:param mime: (str)
	:param savefolder: folder path where images are saved to
	:param lat: (int) most lateral
	:param med: (int) most medial
	:param oldfolder: folde where you save log files to
	'''

	outfile = open(oldfolder +'names%s.txt' % datestr,'w') # this records all the downloaded images
	recordfile = open(oldfolder +'log%s.txt' % datestr,'w') # this records other info
	for icount, iseries in enumerate(iserieslist): # iterate through the list of image series (experiments)
		print icount, iseries
		recordfile.write(iseries + '\t')
		if len(iseries)>1: # check that it is a valid image series
			#print coords
			# Get information from image series file
			iseriesurl = 'http://www.brain-map.org/aba/api/imageseries/' + iseries + '.xml'
			print iseriesurl
			try:
				xmlfile = urllib.urlopen(iseriesurl)
			except IOError:
				recordfile.write( 'No image series information found\n')
				print 'No image series information found\n'
				continue
			c = 0 # use this to check if any images in category
			for sect in xmlfile.read().split('<image>')[1:]:
				# Use ref atlas index - probably better
				# section = re.search("<referenceatlasindex type='integer'>(.*)</referenceatlasindex>", sect).group(1)
				# Use position - we originally used
				section = re.search("<position type='integer'>(.*)</position>", sect).group(1)

				#print section
				if lat < int(section) < med: # lat and med are the constraints on your region perpendicular to your axis of interest
					recordfile.write('\t'.join(['_'.join(coords),zoom, section]) + '\t')
					imagename = getimages(sect, iseries, c, outfile, zoom, coords, oldfolder, mime, recordfile) # download images
					c+=1
					
			if c==0: # tells you that no images have been downloaded
				recordfile.write('No sections between %i and %i\t' % (lat, med))
				try: sect = xmlfile.read().split('<image>')[1] # investigate if there are other images
				except IndexError: recordfile.write( 'No position information found\n'); continue
				# choose first image to download (only relevant if you are selecting images near to the boundary)
				# section = re.search("<referenceatlasindex type='integer'>(.*)</referenceatlasindex>",sect).group(1)
				section = re.search("<position type='integer'>(.*)</position>",sect).group(1)

				recordfile.write('\t'.join(['_'.join(coords),zoom,section]) + '\t')
				imagename = getimages(sect, iseries, c, outfile, zoom, coords, oldfolder, mime, recordfile)


		if os.path.exists(savefolder + iseries + '_' + imagename + 'nissl.jpg'): # don't redownload file
			recordfile.write('Path exists, no need to recopy\t\n')
			continue				
		recordfile.write('\n')

			
def getimages(sect, iseries, c, outfile, zoom, coords, savefolder, mime, recordfile):
	'''
	Determines image paths so that images can be downloaded
	:param sect: section
	:param iseries:
	:param c: number of image in series
	:param outfile:
	:param zoom:
	:param coords:
	:param savefolder:
	:param mime:
	:param recordfile:
	:return:
	'''
	#print 'Get images'
	imagename = re.search('<imagedisplayname>(.*)</imagedisplayname>', sect).group(1)
	if c==0:outfile.write(imagename + '\t' + iseries +'\n') # sav information

	# get image paths for ish and exp
	path = re.search('<downloadImagePath>(.*)</downloadImagePath>', sect).group(1)
	pathexp= re.search('<downloadExpressionPath>(.*)</downloadExpressionPath>', sect).group(1)
	section = re.search("<referenceatlasindex type='integer'>(.*)</referenceatlasindex>", sect).group(1)

	# paths for grabbing info
	jpgurl = 'http://www.brain-map.org/aba/api/image?zoom=' + zoom + '&top=' + coords[0] +'&left=' + coords[1] +\
	         '&width=' + coords[2]  +'&height=' + coords[3]  +'&mime=' + mime +'&path=' + path
	expjpgurl = 'http://www.brain-map.org/aba/api/image?zoom=' + zoom + '&top=' +coords[0]  +'&left=' + coords[1]  +\
	            '&width=' + coords[2]  +'&height=' + coords[3]  +'&mime=' + mime +'&path=' + pathexp
	
	recordfile.write('\t'.join([jpgurl, expjpgurl]) + '\t')
	downloadimage(jpgurl, iseries, imagename, 'ish', savefolder, section,'Original_ish/')
	downloadimage(expjpgurl, iseries, imagename, 'exp', savefolder, section,'Original_exp/')
	
	return imagename

def downloadimage(jpgurl, iseries, imagename, runtype, savefolder, section, runfolder):
	'''
	Open file from image url and save to folder
	:param jpgurl:
	:param iseries: str
	:param imagename:
	:param runtype: whether the exp or ish image is required - str
	:param savefolder:
	:param section: str
	:return:
	'''
	try:
		jpgfile = urllib.urlopen(jpgurl)
	except IOError:
		print imagename, 'No image found'
		return
	readjpg = jpgfile.read()
	if os.path.exists(savefolder + runfolder) ==False:os.system("mkdir %s" % savefolder + runfolder)
	savejpg = open(savefolder + runfolder + iseries + '_' + imagename + '_' + section +runtype +'full.jpg','w')
	savejpg.write(readjpg)
	savejpg.close()

def checkpairs():
	'''
	Make sure that for every image you have both ish and expression mask
	#run allfilesdict with exp as search and allfilesdict with ish as search
	:return:
	'''
	downloadfolder = 'Example_Results/Images/'
	ifilelist = downloadfolder +'ishfilelist.txt'
	efilelist = downloadfolder +'expfilelist.txt'
	ishdict = getallfiledict(downloadfolder + 'OriginalISH/', ifilelist,'ishfull.jpg', 'iseries')
	expdict = getallfiledict(downloadfolder + 'Exp/', efilelist,'expfull.jpg', 'iseries')
	expnames = set([re.sub('expfull.jpg','','_'.join(e.split('_')[0:3])) for e in expdict.keys()])
	ishnames = set([re.sub('ishfull.jpg','','_'.join(e.split('_')[0:3])) for e in ishdict.keys()])
	#print expnames,ishnames
	print len(expnames), len(expnames.intersection(ishnames))
	ediff = expnames.difference(ishnames); idiff = ishnames.difference(expnames)

	print len(ediff),len(idiff),ediff

