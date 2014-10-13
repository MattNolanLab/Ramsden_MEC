
'''
Classify mediolateral plane of images

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

from ABA_imageprocessing import getallfiledict
import re,os
import numpy as np


def sort_ml_images(homepath,filelist,filesearch):
	'''

	:param filepath:
	:param deletefilepath:
	:param filelist:
	:param dropboxpath:
	:return:
	'''
	specfolder = 'Resize_ish'
	[allfilesdict,iseriesdict] = getallfiledict(homepath + specfolder, filelist, filesearch)

	mldicts = userefatlasindex(iseriesdict)

	newlocfile = open(homepath + 'AllMLlocs.txt','w')
	outfolder = ['ML1/','ML2/','ML3/','ML4/','ML5/']
	for specfolder in ['Original_ish', 'Original_exp', 'Resize_ish', 'Resize_exp', 'SB', 'Thresh',
	                   'Segmented/SegmentedThresh/', 'Segmented/SegmentedOrig/', 'Segmented/SegmentedExp/',
	                   'Segmented/SegmentedMask/']:
		if specfolder == 'Segmented/SegmentedExp/': fileend = 'tif'
		else: fileend=filesearch
		[allfilesdict,iseriesdict] = getallfiledict(homepath + specfolder, filelist, fileend)
		deletefilepath = homepath + 'NoML/' + specfolder + '/'
		for filename in sorted(iseriesdict.keys()):
			check = 'n'
			for dcount,d in enumerate(mldicts):
				for iseries, loc in d.iteritems():
					if iseries == filename.split('_')[0] and int(filename.split('_')[2]) == loc:
						# print outfolder[dcount],iseries, loc, filename.split('_')[0], \
						# 	re.sub('expfull','',re.sub('ishfull','',filename.split('_')[2]))
						if dcount==2: # Only for ML3

							os.system("cp %s %s" % (homepath + specfolder + '/' + filename + '.' + fileend,
						                          homepath + outfolder[dcount] + specfolder + '/'))
						newlocfile.write('\t'.join([filename + '.' + fileend, outfolder[dcount]]) + '\n')
						check = 'y'
						break
			if check == 'n':
				# print filename, 'None found'
				os.system("cp %s %s" % (homepath + specfolder + '/' + filename  + '.' + fileend, deletefilepath))
				newlocfile.write('\t'.join([filename + '.' + fileend, 'NoML/']) + '\n')
	newlocfile.close()

def userefatlasindex(iseriesdict):
	'''

	:param homepath:
	:param filelist:
	:param filesearch:
	:return:
	'''
	refind_ideal = 66

	refdict = dict((i.split('_')[0],[[],[]]) for i in iseriesdict.keys())

	for i in iseriesdict:
		refind = int(re.sub('ishfull','',i.split('_')[3]))
		refdict[i.split('_')[0]][0].append(refind)
		refdict[i.split('_')[0]][1].append(int(i.split('_')[2]))


	ml1iloc = {}; ml2iloc = {}; ml3iloc = {}; ml4iloc = {}; ml5iloc = {}
	for iseries,locs in refdict.iteritems():
		# Could incorporate tending towards lower value rather than higher value
		refmin_ind = np.array([abs(x-refind_ideal) for x in locs[0]]).argmin()
		loc3 = locs[1][refmin_ind]
		ml3iloc[iseries] = loc3
		if int(loc3) - 16 in locs[1]:
			ml1iloc[iseries] = loc3 - 16
		if int(loc3) - 8 in locs[1]:
			ml2iloc[iseries] = loc3 - 8
		if int(loc3) + 8 in locs[1]:
			ml4iloc[iseries] = loc3 + 8
		if int(loc3) + 16 in locs[1]:
			ml5iloc[iseries] = loc3 + 16

	return ml1iloc,ml2iloc,ml3iloc,ml4iloc,ml5iloc

def useSVMclassification(iseriesdict):
	refdict = dict((i.split('_')[0],[]) for i in iseriesdict.keys())

	for i in iseriesdict:
		refdict[i.split('_')[0]].append(int(i.split('_')[2]))

	ml3iseriesdict = dict((int(line.strip().split('\t')[0]),int(line.strip().split('\t')[1]))
	                      for line in open('ML3loc.txt').readlines()[1:])

	ml1iloc ={}; ml2iloc = {}; ml3iloc = {};ml4iloc = {}; ml5iloc = {}
	for iseries,locs in refdict.iteritems():
		iseries = int(iseries)
		#print iseries,locs,ml3iseriesdict[iseries]
		if iseries in ml3iseriesdict and ml3iseriesdict[iseries] in locs:
			loc3 = ml3iseriesdict[iseries]
			ml3iloc[iseries] = loc3
			if loc3 - 16 in locs:
				ml1iloc[iseries] = loc3 - 16
			if loc3 - 8 in locs:
				ml2iloc[iseries] = loc3-8
			if loc3 +8 in locs:
				ml4iloc[iseries] = loc3+8
			if loc3 + 16 in locs:
				ml5iloc[iseries] = loc3+16
	return ml1iloc,ml2iloc,ml3iloc,ml4iloc,ml5iloc





