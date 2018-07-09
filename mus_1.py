# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 16:13:21 2018

@author: dmytr
"""
import re
import numpy as np
chord=["CEG","DFA","EGB","FAC","GBD","ACE","BDF"]

tune="EGFEDC,DEF,EDFEGFE,FED,GGGC,DCDEFED,GGAF,ECDC"
commas=re.findall(r'(?<!\d),(?!\d)', tune) # find all parts
n1=0
mus=" "
for ii in range(len(commas)):
    ind=tune[n1:].find(',')
    s1=tune[n1:n1+ind] # the notes in the part 4/4
    n1+=ind+1
    if ii == len(commas)-1: # the last one
        s1=tune[n1:]
    print(s1)
    skip=np.random.randint(len(s1))
    for jj in range(len(s1)): # separate notes
        
        chor=[]
        note=s1[jj]
        if jj==skip:
            ran=""
        else:
            for ch in chord: # find three chords fittting with note
                if ch.find(note) != -1:
                    chor.append(ch)
                    ran=np.random.choice(chor)
        print(ran)
        mus=mus+note+"-"+ran+" "
    print(" ")
    mus=mus+"|"
print(mus)
        

#print(len(tune),len(commas),ind,a)