'''
Main file to run image processing functions from

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

from ABA_Alignment import alignmacro, decipherpositions
from ABA_imageprocessing import *

def preprocess_pipeline(layer, infolderpath, outfolderpath,chosentarget, filesearch, macropath, runtype, prefix,
                         filelist, headless):
	'''
	Pipeline for writing macros/running code then running ImageJ. Problems running ImageJ from ipython notebook so
	now running that separately
	:param layer:
	:param infolderpath:
	:param outfolderpath:
	:param chosentarget:
	:param filesearch:
	:param macropath:
	:param runtype:
	:param prefix:
	:param filelist:
	:param headless:
	:return:
	'''
	if '/Users/' in macropath:
		fiji = '/Applications/Fiji.app/Contents/MacOS/fiji-macosx' + headless
	else:
		fiji = 'sudo fiji' +headless

	if 'alignmacro' in runtype:
		decipherpositions(layer, prefix,infolderpath)
		iseriesdict = dict((line.strip().split('\t')[0].split('.jpg')[0], line.strip().split('\t'))
		                   for line in open(infolderpath + layer + prefix + 'imagejnew.txt','r'))
		outfile = open(macropath +  runtype +'.ijm','w')
		alignmacro(outfile, chosentarget, iseriesdict, filesearch, infolderpath, outfolderpath)
	else:
		run_preprocessing(infolderpath, outfolderpath, filelist, macropath, runtype, filesearch)

	if 'codeonly' in runtype: # need this for ipython notebook
		return
	elif 'alignmacro' in runtype:
		os.system("%s %s" % (fiji,macropath + runtype + '.ijm'))
	elif 'sbimages' in runtype:
		os.system("%s %s" % (fiji,macropath + runtype +'.ijm'))
	elif 'thresimages' in runtype:
		os.system("%s %s" % (fiji,macropath + runtype +'.ijm'))
	elif  'SegmentCereb' in runtype:
		os.system("%s %s" % (fiji,macropath + runtype +'.ijm'))



def run_preprocessing(infilefolder, outfilefolder,filelist, macropath, runtype, filesearch):
	'''
	Implements processing stages from
	:param infilefolder:
	:param outfilefolder:
	:param filelist:
	:param project:
	:param macropath:
	:param runtype:
	:param filesearch:
	:return:
	'''
	allfilesdict, preiseriesdict = getallfiledict(infilefolder, filelist,filesearch )
	#print preiseriesdict

	if 'resizeimages' in runtype:
		resizeimages(infilefolder, preiseriesdict)
		return

	elif 'sbimages' in runtype:
		iseriesdict = getnewdict(outfilefolder, filelist, preiseriesdict,'_sb','',filesearch)

		outfile = open(macropath + runtype +'.ijm','w')
		sb_images(infilefolder, outfilefolder,iseriesdict, outfile)

	elif 'threshimages' in runtype:
		iseriesdict = getnewdict(outfilefolder, filelist,preiseriesdict,'_sbthres','',filesearch)

		outfile = open(macropath +  runtype +'.ijm','w')
		thresh_images(infilefolder,outfilefolder, iseriesdict, outfile)


	elif 'SegmentCereb' in runtype:

		outfile = open(macropath +  runtype + '.ijm','w')
		thresh = runtype.split('_')[1]
		if 'p1' in runtype:
			iseriesdict = getnewdict(re.sub('Segmented/','Edges/',outfilefolder), filelist,
			                         preiseriesdict,'_edges','',filesearch)
			print len(iseriesdict.keys())
			find_seg_edges(infilefolder,re.sub('Segmented/','Edges/',outfilefolder), iseriesdict, outfile)
		if 'p2' in runtype:
			iseriesdict = getnewdict(re.sub('Segmented/','Segmented/SegmentedMask/',outfilefolder), filelist,
			                         preiseriesdict,'_mask','_edges',filesearch)
			print len(iseriesdict.keys())
			create_seg_mask(infilefolder, outfilefolder,iseriesdict, outfile, thresh)
			
		if 'p3' in runtype:
			iseriesdict = getnewdict(re.sub('Segmented/','Segmented/SegmentedExp/',outfilefolder), filelist,
			                         preiseriesdict,'seg_exp.tif','sb_mask',filesearch)
			print len(iseriesdict.keys())
			apply_seg_mask(infilefolder, outfilefolder, iseriesdict)


	
	outfile.write('run("Quit");\n')
	outfile.close()
