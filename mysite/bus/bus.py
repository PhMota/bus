#import urllib2
import wget
import time
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys
import os
import glob

path = '/home/mota/Projects/bus/mysite/bus/data/'

def fetchData():
    print "fetching data at", sortTime( time.localtime() )
    url = 'http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/rest/index.cfm/onibus'
    os.system('wget %s -O %sgps%d.json >/dev/null'%(url,path,time.time()))
    print 'done fetching'
    return 

def cleanData( interval ):
    listoffiles = glob.glob(path+'*')
    for f in listoffiles:
        if time.time() - os.path.getmtime(f) > interval: os.remove(f)

def gpsData():
    latest = max( glob.glob(path+'*'), key=os.path.getmtime )
    print 'file', latest
    return json.load(open(latest))

def parsegpsData( data, bounds ):
    data2 = [ [entry[2], float(entry[3]), float(entry[4]), -1 if entry[6]=='' else float(entry[6]) ] for entry in data['DATA'] if entry[2] != '' ]
    data2 = [ entry for entry in data2 if bounds[0]>entry[1] and entry[1]>bounds[2] and bounds[1]>entry[2] and entry[2]>bounds[3] ]
    return data2

def test():
    print "test"
    
def sortTime( t ):
    return time.strftime('%Y-%m-%d_%H:%M:%S', t)

def parseTime( t ):
    return sortTime( time.strptime(t, '%m-%d-%Y %H:%M:%S') )

def plotGPS( data ):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    data2 = np.array( [ [entry[3],entry[4]] for entry in data['DATA'] ] )
    print data2
    mask = np.sqrt( (data2[:,0]+22.9)**2 + (data2[:,1]+43.4)**2) < .2
    ax.scatter( data2[mask][:,1], data2[mask][:,0], s=.1 )
    fig.savefig('map.pdf')
    plt.close(fig)


if __name__ == "__main__":
    if '-d' in sys.argv:
        print 'daemon mode'
        while 1:
            fetchData()
            cleanData(10*60)
            time.sleep(30)
        exit(0)
    print sortTime(time.localtime())
    data = gpsData()
    res = parsegpsData(data, [-22.94,-43.0,-22.92,-43.45] )
    print res
    exit(0)
    print len(data['DATA'])
    print len( set( [ entry[2] for entry in data['DATA'] ]) )
    for i in range(1,10):
        print data['DATA'][-i]
        print parseTime(data['DATA'][-i][0])

    plotGPS(data)        
