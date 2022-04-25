#!/usr/bin/env python3
#
#Find gaps in the audio spectrum that are not currently in use for ft8
#
# rev 1.0 11/04/2020 WPNS First release after much hacking
# rev 1.1 11/04/2020 WPNS cleanup header, display, etc
# rev 1.2 11/17/2020 WPNS flag crazy results
# rev 1.3 12/18/2020 WPNS hitcount versus linecount
# rev 1.4 07/24/2021 WPNS better sync hints
# rev 1.5 11/22/2021 WPNS QDX is (150 to) 3200 Hz bandwidth

import time
from datetime import datetime
from file_read_backwards import FileReadBackwards

print ("FindGaps 1.5 11/22/2021 at",time.asctime(),'\n', flush=True)

CurrentTime = datetime.now()
print('Currently: ',CurrentTime)
LineCount = 0
HitCount = 0
AFIU = []     # Audio Frequencies In Use

ChannelBW = 50 # FT8 Channel Bandwith is 50 Hz
AudioBW = 3200 # Max receiver passband (IC-7100 is 3600, QDX is 3200)
AudioStart = 200  # FT8 won't let you transmit at less than 200Hz
Debug = False
MinutesBack = 2   # how many minutes back to look

with FileReadBackwards("ALL.TXT", encoding="utf-8") as frb:
# getting lines by lines starting from the last line up
  for line in frb:
    if len(line) > 49:
      LineCount += 1
      #print (len(line),line)
      (DTS,MHz,TRx,FT8,RSS,dT,Hz,QSO) = line.split(None,7)
      TimeStamp = datetime.strptime(DTS, '%y%m%d_%H%M%S')
      #print (TimeStamp)
      TimeBack = (CurrentTime-TimeStamp).total_seconds()
      #print (TimeBack,"Seconds Ago",Hz)
      if TimeBack > int(MinutesBack*60):
        break
      if TimeBack < 0:
        print("Something wrong with system time?  Run ~/fixtimezone.scr and/or ~/timesync.scr?")
        break
      if not ('N1JBJ' in QSO):  # ignore where I'm operating, or my QSO partner is
        HitCount += 1
        AFIU.append(Hz)
      #input('Next?')

print ("{} Transmissions seen in the last {} minutes".format(HitCount,MinutesBack))
#print (AFIU)
GuessMax = MinutesBack*4*(4000/50)*2      # can't imagine it being bigger than this
if (LineCount>GuessMax):
  print("Something wrong with LineCount, check your code!")

# now an array of integral audio frequencies in the passband
Audio = [False]*(AudioBW+ChannelBW)  # Cover max range we should store
#print (Audio)
for Freq in AFIU:
  #print (Freq,end=" ")
  for index in range(int(Freq),int(Freq)+ChannelBW+1):
    Audio[index] = True

print (sum(Audio),'frequencies in use, {0} Percent nominal'
       .format(int(sum(Audio)/float((AudioBW-AudioStart)/100))
               )
       )

if Debug:
  print ('\n     ',end="")
  for index in range(20):
    print('    |',end="")
  print()
  for Hundreds in range(int(AudioBW/100)):
    print("{0:04d}".format(Hundreds*100),end=":")
    for Ones in range(100):
      if Audio[Hundreds*100+Ones]:
        print('.',end="")
      else:
        print(' ',end="")
    print()

# OK, so we've got this array of integral audio frequencies that are in use.

Start = AudioStart  # beginning of useful FT8 sub-band
GapSize = 0
InGap = True   # Assume we're in a gap
GapDict = {}   # start with a blank slate
AFIUcount = 0  # totalizer for how many are in use (should match sum(Audio))

for Freq in range(AudioStart,len(Audio)):
  if Audio[Freq]:                      # this AF is in use
    if InGap:                          # and if we were in a gap
      GapDict[Start] = GapSize         # save the details
      InGap = False                    # and that's the end of this gap
    else:                              # AF is in use, but we're not in a gap
      AFIUcount += 1                   # log it for 'how busy are we'?

  else:                                # this AF is _NOT_ in use
    if InGap:                          # and we're (still) in a gap
      GapSize += 1                     # it just got bigger
    else:                              # we were not in a gap, but we are now
      Start = Freq                     # save the start of this new gap
      GapSize = 1                      # at least one Hz free
      InGap = True                     # and set the flag

# at the end, close the last gap
GapDict[Start] = GapSize         # save the details

#now we have a dictionary of Start and GapSize, called GapDict
#print (GapDict)
if Debug:
  print("\nAll gaps:\n")
  for StartFreq,SizeOfGap in GapDict.items():
    if (SizeOfGap >=0):
      print ("{0:04d} {1:04d} Hz, [{2:04d}-{3:04d}]".format(StartFreq,SizeOfGap,StartFreq,StartFreq+SizeOfGap-ChannelBW))

print("\nUseful gaps:\nStart Size     Set Tx Range <Midpoint>")
for StartFreq,SizeOfGap in GapDict.items():
  if (SizeOfGap >=ChannelBW):
    print ("{0:04d}  {1:04d} Hz, [{2:04d}-{3:04d} <{4:04d}>]".
           format(StartFreq,SizeOfGap,StartFreq,
                  StartFreq+SizeOfGap-ChannelBW,
                  int(StartFreq+(SizeOfGap-ChannelBW)/2)
                  )
           )
    
