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
import os
		
def parselogfiles():
	'''
	Function takes the files generated during 1-1 registration and extracts the mutual information score
	so that registration accuracy can be judged
	:return: file alllogdata.txt
	'''
	filepath = 'Segmented/Log/'
	os.system("ls %s > %s" % (filepath + '*.jpglog.txt', filepath + 'filelist.txt'))
	
	logs = [line.strip() for line in open(filepath + 'filelist.txt')]
	newparamfile = open(filepath + 'alllogdata.txt','w')
	for l in logs:
	# Open relevant log file for each image
		logfile = [line.strip() for line in open( l)] #filepath + '/' +
		# Make new logs list just containing relevant info
		newlogs = []
		for logs in logfile:
			if logs.startswith('MI ') and len(logs.split(' ')) == 15:
				newlogs.append([logs.split(' ')[1],logs.split(' ')[-1]])
			if logs.startswith('Time'):
				timetaken = logs
		if len(newlogs) ==0: startmi = endmi = diffmi = 'na'
		else:startmi = newlogs[0][0]; endmi = newlogs[-1][0]; diffmi = str(abs(float(newlogs[0][0])-float(newlogs[-1][0])))
		# Save filename, position, start MI value, finish MI value, MI change, time taken to file
		#print '\t'.join([imagefile, imageposition, '\t'.join([newlogs[0],newlogs[-1],abs(float(newlogs[0])-float(newlogs[-1]))]),timetaken])
		newparamfile.write('\t'.join([l.split('_')[0].split('/')[-1],l, 'na', '\t'.join([startmi,endmi,diffmi]),timetaken]) + '\n')
	newparamfile.close()

			

