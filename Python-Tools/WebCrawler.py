#!/usr/bin/python
"""
Created: 15-8-2016

This tool crawls a website for specific elements.
In this example the script was used for searching on isfinder.fr for
data on Insertion Sequences.

The tool uses a base url to crawl a website.

Sebastiaan de Vriend	15-06-2016	Creation script
"""

import urllib

from bs4 import BeautifulSoup

FILELOC = "FILENAMEHERE"
RESULTFILE = "RESULTFILENAMEHERE"
url = "URL PART HERE"


def main():
    with open(FILELOC) as f:
    	elementList = [line.rstrip() for line in f]
    
    famfile = open(RESULTFILE, "w")
    for element in elementList:
    	site = urllib.urlopen(url + element)
    	soup = BeautifulSoup(site)
    	div = soup.find(id="droite")
	famdiv = soup.find(id="seq_ident")
 	famname = famdiv.li.get_text().split()[1]
    	divlist = div.get_text().split()
    	line = element + "\t" + famname + "\t" + divlist[len(divlist) - 2] + "\n"
        famfile.write(line)
    famfile.close()

main()
