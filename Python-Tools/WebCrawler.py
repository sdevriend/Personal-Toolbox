#!/usr/bin/python
"""
Created: 15-8-2016

This tool crawls a website for specific elements.
In this example the script was used for searching on isfinder.fr for
data on Insertion Sequences. 

THE INPUT FILE MUST CONTAIN THE FOLLOWING ITEMS:
ISFAM \n
OR:
ISFAM_aa1 \n

DON'T INCLUDE HEADERS!

CHANGE DIRECTORY PATHS TO CORRESPONDING VALUES FOR IN- AND OUTPUT
The tool was extended to find lengths of amino acids on open reading
frames.

Sebastiaan de Vriend	15-08-2016	Creation script
Sebastiaan de Vriend	16-08-2016	Added functionality
Sebastiaan de Vriend	23-08-2016	Added documentation

REQUIRED PACKAGE: BeautifulSoup
"""

import urllib

from bs4 import BeautifulSoup

FILELOC = "/media/sf_D_DRIVE/TOPLAB/blastRes15-8/inputfiles/FamAA.txt" # CHANGE ME
RESULTFILE = "/media/sf_D_DRIVE/TOPLAB/blastRes15-8/FamAAinfo.txt" # CHANGE ME
url = "https://www-is.biotoul.fr/scripts/ficheIS.php?name="
AA = False # Boolean to support amino acid lengths

def getLength(soup):
    """
	Input: soup: object containing website.
	
	Function looks for the div droite where the length is
	located. The funcion splits the text from the site and
	returns the one last element, where the length is stored.
	
	Output: String: Length of IS.
    """
    div = soup.find(id="droite")
    divlist = div.get_text().split()
    return divlist[len(divlist) - 2]

def getFname(soup):
    """
	Input: soup: Object containing website.

	The functions searches for a family name in
	a div and list element.
	
	Output: Str: familyname.
    """
    famdiv = soup.find(id="seq_ident")
    famname = famdiv.li.get_text().split()[1]
    return famname

def openWebpage(element):
    """
	Input: elementid
	
	The function returns a webpage object. If the tool searches for
	amino acids, then the tool splits the element string.

	Output: webpage object
    """
    if AA:
	return urllib.urlopen(url + element.split("_")[0])
    else:
	return urllib.urlopen(url + element)

def getSeq(soup, element):
    """
	Input:
	soup: html parser
	element: str of IS Fam and orf

	The function extracts the orf number and
	then it extracts the table which is corresponding with the orf number.
	
	Output:
	AALength: str with the length of the extracted AA sequence.
'   """
    ORFNum = element[len(element)-1]
    ORFTable =  soup.find_all('table')[1 + int(ORFNum)]
    AALength = ORFTable.find_all('td')[1].get_text().split()[0]
    return AALength

def getMotifFunction(soup, element):
    """
	Input:
	soup: html parser
	element: str of IS Fam and ORF

	The function sets the ORF number by stripping the last digit.
	Then the function sets a boolean and integer on zero values.

	After that the function loops through all the spam matches in the
	html parser. The loop checks if the i value is 1. If that is true,
	then the loop will return a stripped match.next.next. This is the
	location where the protein function is stored in the html.
	If i is not 0, than the function looks for the string 'ORF'
	in the next element. If that is true, then the ORF number will
	be checked by the next next match. If that is true, the i value 
	will be raised by one, to match the 1 for the first check.
    """
    ORFNum = element[len(element)-1]
    matchbool = False
    i = 0
    for match in soup.find_all("span"):
	if i == 1:
	    
            return match.next.next.strip()
	if "ORF " == match.next:
	    
	    if ORFNum == match.next.next:
		
		matchbool = True
	if matchbool:
	     i+=1

def main():
    """
	The function opens a inputfile and converts it into a list.
	
	After that the function checks if the first element of the
	elementlist contains ORF numbers. If that is true, then the
	script will look for protein lengths and function. Else the
	script will only look for IS sequence lengths.

	The script will then open a resultfile and loops though all
	the IS family's. 
	For each family in the list, the corresponding webpage will
	be opend with the openWebpage function. After that the
	site will be parsed by the beautifulsoup package.
	The length, family name and protein properties will be
	extracted by different functions. After the functions a
	line with the results will be written in the resultfile.

	After the loop the resultfile will be closed.
    """
    #elementList = ["ISKpn25_aa4"] # temp here
    with open(FILELOC) as f:
    	elementList = [line.rstrip() for line in f]
    if len(elementList[0].split("_")) > 1:
        global AA
	AA = True
    famfile = open(RESULTFILE, "w")
    for element in elementList:
	site = openWebpage(element)
    	soup = BeautifulSoup(site)
        length = getLength(soup)
	famname = getFname(soup)
	if AA:
	    AAseqLength = getSeq(soup, element)
	    AAFunc = getMotifFunction(soup, element)
	    
	    line = element + "\t" + famname + "\t" + length + "\t" + AAseqLength + "\t" + AAFunc + "\n"
	else:
	    line = element + "\t" + famname + "\t" + length + "\n"
        famfile.write(line)
	
    famfile.close()


main()
