#!/usr/bin/env python
###############################################################################
#
# Project:  azimuth.py
# Purpose:  Processa arquivos shapefile (ESRI) com lineamentos e retorna
#           arquivo texto com azimute e comprimento de cada lineamento.
#          
# Author:   Carlos H. Grohmann, carlos.grohmann@gmail.com
#
###############################################################################
# Copyright (c) 2009, Carlos H. Grohmann
# 
###############################################################################


# import modules
import osgeo.ogr as ogr
import os, sys, math

# =============================================================================
def Usage():
    print
    print 'azimuth.py reads ESRI shapefiles with simple lines (lineaments)'
    print 'and returns the azimuth and length of each line in a text file'
    print ''
    print
    print 'Usage: azimuth.py infile outfile'
    print
    sys.exit( 1 )

# =============================================================================

infile = None
outfile = None

# =============================================================================
# Parse command line arguments.
# =============================================================================
i = 1
while i < len(sys.argv):
    arg = sys.argv[i]

    if infile is None:
	infile = arg

    elif outfile is None:
	outfile = arg

    else:
	Usage()

    i = i + 1

if infile is None:
    Usage()
if outfile is None:
    Usage()


# get the driver
ogrdriver = ogr.GetDriverByName("ESRI Shapefile")

# open the data source
#shpFile = "/home/guano/Arbeit/python/shape/lin/lin2.shp"
dataSource = ogrdriver.Open(infile, 0)
if dataSource is None:
   print 'Arquivo nao encontrado: ' + infile
   sys.exit(1)

print 
print '< azimuth.py - (c) 2009, Carlos H. Grohmann >'
print 

# get the data layer
layer = dataSource.GetLayer()

# count features in layer
numFeatures = layer.GetFeatureCount()
#print 'Feature count: ' + str(numFeatures)
print 'Numero de lineamentos no arquivo:', numFeatures
print ''

# get the layer extent
#extent = layer.GetExtent()
#print 'Extent:', extent
#print 'UL:', extent[0], extent[3]
#print 'LR:', extent[1], extent[2]


#lists for vertices coordinates
coord_X0 = []
coord_X1 = []
coord_Y0 = []
coord_Y1 = []


# loop through the features 
f = layer.GetNextFeature()
while f is not None:
	geometry = f.GetGeometryRef()
# 	print 'X0: ', geometry.GetX(0), ' Y0: ', geometry.GetY(0)
# 	print 'X1: ', geometry.GetX(1), ' Y1: ', geometry.GetY(1)
	x0 = geometry.GetX(0)
	x1 = geometry.GetX(1)
	y0 = geometry.GetY(0)
	y1 = geometry.GetY(1)
	coord_X0.append(x0)
	coord_X1.append(x1)
	coord_Y0.append(y0)
	coord_Y1.append(y1)
	f = layer.GetNextFeature()

#need if looping again
layer.ResetReading() 

# close the data source
dataSource.Destroy()

#print vertices
#for i in range(numFeatures):
#     print "Linha: %d, X0: %f, Y0: %f, X1: %f, Y1: %f" % (i+1, coord_X0[i], coord_Y0[i], coord_X1[i], coord_Y1[i])
#print

#start calculations...

#empty list for results
azimuth = []
length = []


for i in range(numFeatures):

	#case of a N-S line
	if coord_X0[i] == coord_X1[i]:
		if coord_Y0[i] > coord_Y1[i]: #line goes from north to south
			az = 180
		else: #line goes from south to north
			az = 0
		hyp = math.fabs(coord_Y0[i] - coord_Y1[i])

	#case of an E-W line
	elif coord_Y0[i] == coord_Y1[i]:
		if coord_X0[i] < coord_X1[i]:  #line goes from west to east
			az = 90
		else: #line goes from east to west
			az = 270
		hyp = math.fabs(coord_Y0[i] - coord_Y1[i])

	#other cases, first point of line W of second point
	elif coord_X0[i] < coord_X1[i]:
		m = (coord_Y1[i]-coord_Y0[i]) / (coord_X1[i]-coord_X0[i])
#		print "X0 < X1: m = %f" % m
		dx = math.fabs(coord_X1[i]-coord_X0[i])
		dy = math.fabs(coord_Y1[i]-coord_Y0[i])
#		print "dx = %f, dy = %f" % (dx,dy)
		hyp = math.hypot(dx,dy)
		arc = math.atan(dx/dy)
		azim = math.degrees(arc) #(arc*180)/PI
		if m < 0:
			azim = 180 - azim
	#other cases, first point of line E of second point
	else:	#elif coord_X0[i] > coord_X1[i]
		m = (coord_Y1[i]-coord_Y0[i]) / (coord_X1[i]-coord_X0[i])
#		print "X0 > X1: m = %f" % m
		dx = math.fabs(coord_X1[i]-coord_X0[i])
		dy = math.fabs(coord_Y1[i]-coord_Y0[i])
#		print "dx = %f, dy = %f" % (dx,dy)
		hyp = math.hypot(dx,dy)
		arc = math.atan(dx/dy)
		azim = math.degrees(arc) #(arc*180)/PI
		if m < 0:
			azim = 360 - azim
		else:
			azim = 180 + azim
	azimuth.append(azim)
	length.append(hyp)


#print results
print
print "Resultados:\n"
for i in range(numFeatures):
     print "Linha %d:  azimute: %8.2f\t comprimento: %12.4f" % (i+1, azimuth[i], length[i])


#save results in a txt file
fileOut = open(outfile, 'w')

for i in range(numFeatures):
#	azim = str(azimuth[i])
#	leng = str(length[i])
#	fileOut.write(azim +"\t"+ leng +"\n")
	fileOut.write('%s\t%s\n' % (azimuth[i],length[i]))

fileOut.close()

print 
print 'Resultados salvos no arquivo: ' + outfile
print 





