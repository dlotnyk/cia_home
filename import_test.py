# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 18:43:50 2018

@author: dmytr
"""

from bs4 import BeautifulSoup as BS
import numpy as np
#from shutil import copyfile

notesb=[["A","45 17","57 19"],["B","47 19","59 19"],["C","48 17","60 14"],["D","50 16","62 16"],["E","52 18","64 18"],["F","53 13","65 13"],["G","55 15","67 15"]]
b="EFB"
for ii in b:
    print(ii)
source = "tune1.mscx"
target = "tune1_copy.mscx"
a=" "*10
c='<a'
d=c.encode('ascii','xmlcharrefreplace')
print(d)
# adding exception handling
#copyfile(source, target)
infile=open(target,"r")
#print(wrfile)
#infile = open(source,"r")
contents = infile.read()
soup = BS(contents, 'xml')
meas=soup.find_all('Measure') # number of bars

#print(meas[0])
chor=meas[0].find_all('Chord')
note=chor[0].find_all('Note')
pitch=note[0].find_all('pitch')
tpc=note[0].find_all('tpc')

pitch[0].contents[0].replaceWith(c)
print(pitch[0].contents[0]=="60")
tpc[0].contents[0].replaceWith("14")
new_tag1 = soup.new_tag("pitch")
new_tag2 = soup.new_tag("tpc")
note[0].prettify(formatter=None)
print(note[0])


#with open(target,'w') as file1:
#            file1.write(st1)
#print(soup)