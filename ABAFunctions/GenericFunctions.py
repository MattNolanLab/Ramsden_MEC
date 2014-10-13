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
import matplotlib.pyplot as plt
import numpy as np
from time import localtime, strftime 
import __main__ as main
import h5py
import matplotlib.cm as cm


plt.rc('axes', linewidth=1.5)
plt.rc('lines', linewidth=2)
plt.rc('lines', markersize=10)
plt.rc('ytick', labelsize=20)
plt.rc('xtick', labelsize=20)

plt.rc('axes', labelsize=20)
plt.rc(('xtick.major','xtick.minor','ytick.major','ytick.minor'), pad=5,size=5)
plt.rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
plt.rc('text', usetex=True)
params = {'legend.fontsize':15,'legend.linewidth':0}
plt.rcParams.update(params)

def getcolours(colmap,start, stop, interval):
	# Returns the colours of a colormap as a list
	# useful for making new colormaps or using colors from particular colormaps
	#colmap needs to be in the form cm.jet
	cmaplist = list(colmap(np.linspace(start,stop,interval)))
	return cmaplist

def makefilelog():
	datestr = strftime("%y%m%d_%H.%M",localtime())
	logfile = '/Users/helenlramsden/MyDocuments/PhDOther/ABAProject/RegistrationProject/PythonLogs/' + os.path.basename(main.__file__) + datestr + '.py'
	os.system("cp %s %s" % (os.path.basename(main.__file__),logfile))

def fixticks(ax,width):
	for line in ax.yaxis.get_ticklines():line.set_markeredgewidth(2)
	for line in ax.xaxis.get_ticklines():line.set_markeredgewidth(width)
	

def checkOSpath(macfilename, officefilename):
	if os.path.exists(macfilename) == True:
		print 'Mac'
		desiredfolder = macfilename
	else:
		print 'Office', macfilename
		desiredfolder = officefilename
	return desiredfolder

def adjust_spines(ax,spines):
	for loc, spine in ax.spines.iteritems():
		if loc in spines:
			spine.set_position(('outward',0)) # outward by 10 points
			#spine.set_smart_bounds(True)
		else:
			spine.set_color('none') # don't draw spine

	# turn off ticks where there is no spine
	if 'left' in spines:
		ax.yaxis.set_ticks_position('left')
	else:
		# no yaxis ticks
		ax.yaxis.set_ticks([])

	if 'bottom' in spines:
		ax.xaxis.set_ticks_position('bottom')
	else:
		# no xaxis ticks
		ax.xaxis.set_ticks([])
		
def maketicksthicker(ax):
	#ax = pylab.gca() #for each axis or whichever axis you want you should
	for line in ax.xaxis.get_ticklines():
		line.set_markeredgewidth(3)
	for line in ax.yaxis.get_ticklines():
		line.set_markeredgewidth(3)

def makefig(ymax, xlimmax,xrang,yrang):
	fig = plt.figure(figsize = (8,10)) # 4,4, for small ones
	fig.subplots_adjust(bottom=0.2)
	fig.subplots_adjust(left=0.2)
	ax = fig.add_subplot(1,1,1)
	adjust_spines(ax, ['left','bottom'])
	cols = ['r','b','k','g','m','y']
	ax.set_ylim(0,ymax)
	ax.set_xlim(0,xlimmax)
	if xrang != 'None':
		ax.set_xticks(np.linspace(0, xlimmax-xlimmax/20, xrang))
		ax.set_xticklabels([int(x) for x in  np.linspace(0, xlimmax, xrang)])
	if yrang != 'None':
		ax.set_yticks(np.linspace(0, ymax-ymax/50, yrang))
		ax.set_yticklabels([int(x) for x in  np.linspace(0, ymax, yrang)])
	maketicksthicker(ax) 
	return ax,fig,cols

def make_patch_spines_invisible(ax):
	ax.set_frame_on(True)
	ax.patch.set_visible(False)
	for sp in ax.spines.itervalues():
		sp.set_visible(False)
		
def formatgraph(ax,roinames, rois,icount, ylabs, ylaboffs):
	[xmin, xmax, ymin, ymax] = ax.axis()
	ax.set_xticklabels([r"$\mathbf{%s}$" % r for r in roinames])
	ax.set_xlim(0., xmax) # -
	#ytlabels = ax.get_yticklabels()
	#ax.set_yticklabels(ytlabels)
	ymin = max(ymin,0)
	ax.set_yticks(getyticks(ymin,ymax))
	ax.set_yticklabels([r"$\mathbf{%s}$" % x for x in getyticks(ymin,ymax)])
	newymin = ymin-(ymax-ymin)/50
	ax.set_ylim(newymin, ymax) # so that you can see zero
	#ax.yaxis.set_major_locator(MaxNLocator(5))
	ax.set_ylabel(ylabs[icount])
	ax.yaxis.set_label_coords(ylaboffs, 0.5) # depends on size of plot
	maketicksthicker(ax)

def getyticks(ymin,ymax):
	roughinterval = (ymax-ymin)/4
	interval = float('%.1g' % roughinterval); #print interval,ymin
	if interval > 0.05 and interval < 0.1: interval = 0.1
	if interval > 0.5 and interval < 1: interval = 1
	if interval > 5 and interval < 10: interval = 10
	yrange = np.arange(ymin, ymax+interval,interval)
	return yrange

def makelegend(ax, fig):
	print 'Making legend'
	handles, labels = ax.get_legend_handles_labels()
	leg = fig.legend(handles,labels, loc="upper right")
	for l in leg.get_lines():l.set_linewidth(2)
	frame  = leg.get_frame()
	frame.set_edgecolor('w')
	frame.set_alpha(0.2)


def st(x):
	newx = x.strip().split('\t')
	return newx

def figsfolderalias(genename, iseries, oldfolder, newfolder):
	#print 'Figsfolder'
	newfile = iseries + '_' + genename + '*'
	#newfile = iseries + '_' + genename[0] + '_' + genename[1] + '*' # genename contains  name and section number
	if os.path.exists(newfolder):
		os.system("ln -s %s %s" % (oldfolder + newfile, newfolder))
		#os.system("echo %s %s" % (oldfolder + newfile, newfolder))
	else:
		os.system("mkdir %s" % newfolder)
		os.system("ln -s %s %s" % (oldfolder + newfile, newfolder))
		
		
def figsfoldercopy(genename, iseries, oldfolder, newfolder):
	newfile = iseries + '_*'# + genename + '*'
#	 print newfile
	if os.path.exists(newfolder) == False:
		os.system("mkdir %s" % newfolder)
	os.system("cp %s %s" % (oldfolder + newfile, newfolder))
#		 #if os.path.exists(oldfolder + newfile):
#		 os.system("cp -n %s %s" % (oldfolder + newfile, newfolder))
#		 #else: writemissing(newfolder,newfile)

def getallfiles(filefolder,filetype):
	# Function finds all the files within a folder and returns a dictionary of their image series (val) and full filename (key) - can use ABA files or immuno files
	#print 'Getting filenames'
	filelist =filefolder + 'filelist.txt'
	os.system("ls %s | grep %s > %s" % (filefolder, filetype,filelist))
	allfilesdict = dict((line.strip(),line.strip().split('_')[0]) for line in open(filelist, 'r')) # key = whole filename, val = iseries
	iseriesdict = dict((line.strip().split('\t')[0].split('.jpg')[0], line.strip().split('\t')) for line in open(filelist,'r')) # key = filename without jpg, filename (replace tif with jpg)
	return allfilesdict, iseriesdict
		
def rebin(a, shape):
	#http://stackoverflow.com/questions/8090229/resize-with-averaging-or-rebin-a-numpy-2d-array
	sh = shape[0],a.shape[0]//shape[0],shape[1],a.shape[1]//shape[1]
	return a.reshape(sh).mean(-1).mean(1)
   
def writehdffile(narray, outpath,groupname,dataname):
	if os.path.exists(outpath+ '.hdf5'): rw = 'r+'
	else: rw = 'w-'	
	f = h5py.File(outpath + '.hdf5', rw)
	dataset = f.create_dataset(groupname + '/' +dataname, narray.shape, dtype=narray.dtype) 
	if len(narray.shape) ==1:dataset[:] = narray
	elif len(narray.shape) ==2:dataset[:,:] = narray
	f.close()
	
def readhdfdata(filename,group,dataset):
	# groups needs to include subgroups
	fopen = h5py.File(filename, 'r+')
	datasetopen  = fopen[group + dataset]
	openarray = datasetopen[:,:]
	fopen.close()
	return openarray

def makecbar(fig, im, ax):
	cbar =fig.colorbar(im, shrink=0.4)#,ticks = [np.log(x) for x in [1,10,100,500]])
	ticko = plt.getp(cbar.ax.axes,'yticklabels')
	plt.setp(ticko, color = 'k', fontsize=20)

