import urllib
import time
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys

def gpsData():
    print "fetching data at", parseTime( time.localtime() )
    url = 'http://dadosabertos.rio.rj.gov.br/apiTransporte/apresentacao/rest/index.cfm/obterTodasPosicoes'
    response = urllib.urlopen( url )
    print response.info()
    html = response.read()
    response.close()  # best practice to close the file
    print 'done'
    return json.loads(html)

def parsegpsData( data ):
    

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

print sortTime(time.localtime())
data = gpsData()
print len(data['DATA'])
print len( set( [ entry[2] for entry in data['DATA'] ]) )
for i in range(1,10):
    print data['DATA'][-i]
    print parseTime(data['DATA'][-i][0])

plotGPS(data)

#if __name__ == "__main__":
    #if "-d" in sys.argv:
        
