#
# 201007_234730     7.074 Rx FT8    -13  0.1 1080 N4LAZ DL5NAV -10
#

import numpy as np

#MyBins = [*range(0,5100,100)]

Hertz = []
Signal = []
deltaT = []
zeroCount = 0

f = open("ALL.TXT", "r")
for line in f:
    if len(line) > 49:
        #print (len(line),line)
        (DTS,MHz,TRx,FT8,RSS,dT,Hz,QSO) = line.split(None,7)
        if float(dT) == 0:
            zeroCount += 1
        #    print (line)
        Hertz.append(int(Hz))
        Signal.append(int(RSS))
        deltaT.append(float(dT))

print()
print('Audio Frequency:')
print (len(Hertz)," Entries")
print ('Min: ',min(Hertz),'Max: ',max(Hertz))
print()

MyBins = [*range(0,int((((max(Hertz)/100.0))+1)*100),100)]
#print (MyBins)

hist,bin_edges = np.histogram(Hertz,bins=MyBins)
for index in range(len(hist)):
    print ('{0:04d}\t{1:>6d}'.format(bin_edges[index],hist[index]))


print()
print('dB:')
print (len(Signal)," Entries")
print ('Min: ',min(Signal),'Max: ',max(Signal))
print()

MyBins = [*range(min(Signal),max(Signal)+2)]
#print (MyBins)

hist,bin_edges = np.histogram(Signal,bins=MyBins)
for index in range(len(hist)):
    print ('{0:>3d}\t{1:>6d}'.format(bin_edges[index],hist[index]))


print()
print('dT:')
print (len(deltaT)," Entries")
print ('Min: ',min(deltaT),'Max: ',max(deltaT))
print ('Zeros: ',zeroCount)
print()

MyBins = [*np.arange(float(min(deltaT)),(float(max(deltaT))+0.2),0.1)]
#print (MyBins)
MyBins = np.around(MyBins,decimals=1)
#print (MyBins)

hist,bin_edges = np.histogram(deltaT,bins=MyBins)
for index in range(len(hist)-1):
    print ('{0:>4.1f}\t{1:>6d}'.format(bin_edges[index],hist[index]))

