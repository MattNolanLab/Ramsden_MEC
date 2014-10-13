'''
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


# open Allregiseries.txt to give all names and iseries
# open ML3 loc to give all good locations
# open classifications to give all SVM locations
# for every gene in Allreg, check for location and classification location - make file

def makecompletelist(iseriesdict):
	alliseries = [line.strip().split('\t') for line in open('AllGeneiseries.txt')]
	allloc = dict((line.strip().split('\t')[0],line.strip().split('\t')[1]) for line in open(dropboxpath +'Reg2DResults/' + 'ML3locnew.txt'))
	#allloc = {}
	#for line in open(dropboxpath +'Results/' + 'ML3locfinal.txt'):
	#	print line.strip().split('\t')
	#	allloc[line.strip().split('\t')[0]] = line.strip().split('\t')[1]
	
	allsvm = dict((line.strip().split('\t')[0],line.strip().split('\t')) for line in open(dropboxpath +'Reg2DResults/' + 'classificationscores.txt'))
	newfile = open(dropboxpath +'Reg2DResults/' + 'CompleteML3loc.txt','w')
	newfile.write('\t'.join(['name','Iseries','Manual','Locs','Scores','Max score','Auto loc']))
	for a in alliseries:
		if a[1] in allloc.keys():
			a.append(allloc[a[1]])
		else:
			a.append('')
		if a[1] in allsvm.keys():
			a.append('\t'.join(allsvm[a[1]][1:]))
		else:
			a.append('-\t-\t-\t-')
		newfile.write('\t'.join(a) + '\n')
		
		