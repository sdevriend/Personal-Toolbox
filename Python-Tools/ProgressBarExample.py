#!/usr/bin/python
from progressbar import ProgressBar, Counter, AnimatedMarker

from time import sleep
print "Ik ben het zandloperscriptje!"
print "Ik tel tot een x en stop daarna"
pbar = ProgressBar(maxval=20).start()

for i in range(1, 21):
    pbar.update(i)
    sleep(1)
    

pbar.finish()

print "Ik ben klaar!"
