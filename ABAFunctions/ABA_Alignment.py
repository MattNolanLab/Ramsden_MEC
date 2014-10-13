#!/usr/bin/env python
'''

Python functions to create ImageJ macro that opens files and aligns them based on specified ROI coordinate-based lines
# (1) Open imagej, record macro and draw ROI lines on each image - store the position of the roi line in a file called homepath + 'Positions/'+ layer + prefix + 'positions.txt'. Ma/ke sure you have one line for selecting window, 1 for making line
# (2) run decipher positions - this should extract all the roi coordinates from your Position file and put them tab separated into a file like this: homepath + layer + prefix + 'imagej.txt': filename, left, upper, right, lower
# (3) make align macro - (a) find all files in given filefolder, (b) extract coords (c) draw line (d) check line length (if all brains should be same size)
# (4) Run fiji

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

import os, re


def decipherpositions(layer, prefix, homepath):
	'''
	takes positions from positions.txt file and converts them into meaningful coordinates file
	:param layer:
	:param prefix:
	:param homepath:
	:return:
	'''
	positionlines = [line.strip() for line in open(homepath + 'Positions/'+ layer + prefix + 'positions.txt','r')]
	outfile = open(homepath + layer + prefix + 'imagejnew.txt','w')
	file = 0; numbers = 0
	for l in positionlines:	
		l = re.sub(r'"', "", l)
		l = re.sub(r'\(', "", l)
		l = re.sub(r'\)', "", l)
		if 'selectWindow' in l:
			#print re.search('selectWindow(.*);',l).group(1)
			filename = re.search('selectWindow(.*);',l).group(1)	
			file=1
			# print filename
		if 'make' in l:
			if 'Line' in l:
				positions = re.search('makeLine(.*);',l).group(1).split(',')
			if 'Rectangle' in l:
				positions = re.search('makeRectangle(.*);',l).group(1).split(',')
			# print positions[0], positions[2]
			if positions[0]== '0': 
				print 'Skipped'
			else:
				newpositions = '\t'.join(positions)
				numbers=1
		if numbers == 1 and file ==1:
			outfile.write(filename + '\t' + newpositions + '\n')
			file = 0
			numbers = 0
	outfile.close()


def makeline(outfile, filename, coords, infilepath):
	# Alignment function - will work on any image
	# simply makes a line

	outfile.write('open("'+ infilepath + filename +'");\n')
	outfile.write('run("8-bit");\n')
	outfile.write('selectWindow("' + filename + '");\n')
	outfile.write('makeLine(' + coords[0] + ',' + coords[1] + ',' + coords[2] + ',' + coords[3] + ');\n')


def alignmacro(outfile, chosentarget, iseriesdict, filetype, infilefolder, outfilefolder):

	outfile.write('//setTool("line");\n')
	coords = [iseriesdict[chosentarget][1],iseriesdict[chosentarget][2], iseriesdict[chosentarget][3], iseriesdict[chosentarget][4]]
	
	# First open image for all others to be aligned to
	makeline(outfile, chosentarget  + '.' +filetype, coords, infilefolder)
	outfile.write('saveAs("JPEG", "' + outfilefolder + chosentarget + '.' +filetype +'");\n')

	# Now open image by image
	for iseries in iseriesdict.keys():
		if iseries == chosentarget: continue
		filename =  iseries #allfilesdict[iseries]
		# print filename
		coords = [iseriesdict[iseries][1],iseriesdict[iseries][2],iseriesdict[iseries][3],iseriesdict[iseries][4]]

		makeline(outfile,filename + '.' +filetype, coords, infilefolder)
		outfile.write('run("Align Image", "source=' + filename + '.' + filetype +' target=' + chosentarget + '.' +filetype +'");\n')
		outfile.write('selectWindow("aligned ' + filename + '.' +filetype + '");\n') # filename or chosentarget?
		outfile.write('saveAs("JPEG", "'+ outfilefolder + filename + '.' +filetype +'");\nclose();\n')
		outfile.write('selectWindow("' + filename + '.' +filetype + '");\nclose();\n')

	outfile.write('run("Quit");\n')
	outfile.close()