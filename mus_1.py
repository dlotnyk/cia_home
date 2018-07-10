# -*- coding: utf-8 -*-
"""
Created on Sun Jul  8 16:13:21 2018

@author: dmytr
"""
import re
import numpy as np
chord=["CEG","DFA","EGB","FAC","GBD","ACE","BDF"]
def find_chord(chord,note):
    chor=[]
    chor1=[]
    i=0
    while i<len(note):
        if i==0:
            for ch in chord: # find three chords fittting with note
                if ch.find(note[i]) != -1:
                    chor.append(ch)
        if i!=0:
            for ch in chor: # find three chords fittting with note
                if ch.find(note[i]) != -1:
                    chor1.append(ch)
            chor=[]
            chor=chor1
        i+=1
    return chor

def in_letter(num):
    if num<65:
        num+=7
    elif num>71:
        num-=7
    else:
        num=num
    return chr(num)

def find_sec(chord,note,tun):
    updown=[-1,0,1]
    chor=[]
    for i in updown:
        n=ord(note)+i
        a=in_letter(n)
        b=a+tun
#        print(b)
        chor1=find_chord(chord,b)
        for ch in chor1:
            chor.append(ch)
        
    nnote=np.random.choice(chor)
    print(nnote)
    let=exclude(nnote,tun)
    return let

def exclude(chor,a):
    id1=chor.find(a)
    let=""
    for i in range(3):
        if i!=id1:
            let+=chor[i]
    return let

tune="EGFEDC,DEF,EDFEGFE,FED,GGGC,DCDEFED,GGAF,ECDC,"
commas=re.findall(r'(?<!\d),(?!\d)', tune) # find all parts
updown=[-1,0,1]



sync="3 5,1 3,1 3 6,1 3,2 4,1 3 5,2 4,2 4,"
commas=re.findall(r'(?<!\d),(?!\d)', tune) # find all parts
coms=re.findall(r'(?<!\d),(?!\d)', sync)
n1=0
n2=0
mus=" "
ss=[]
ss2=[]
first=1
better=" "
tune_list=[]
counter=0
for ii in range(len(commas)):
    # bar devision
#    print(ii)
    ind=tune[n1:].find(',') # tunes
    indc=sync[n2:].find(',') # order
    
    s1=tune[n1:n1+ind] # the notes in the part 4/4
    s2=sync[n2:n2+indc] # the notes to sync
    
    n1+=ind+1
    n2+=indc+1
    
    if ii == len(commas): # the last one
        s1=tune[n1:]
        s2=sync[n2:]
    # random harmonixation
    ss.append(s1)
    ss2.append(s2)
    skip=np.random.randint(len(s1))
    number=1
    
    for jj in range(len(s1)): # separate notes
        
        note=s1[jj]
        tune_list.append(note)
        if jj==skip:
            ran=""
        else:
            chor=find_chord(chord,note)
            ran=np.random.choice(chor)
#        print(ran)
        mus=mus+note+"-"+ran+" "
       
        mus=mus+"|"     
     # non random harmony
    sx=np.fromstring(s2, dtype=int, sep=' ')
    
    for jj in range(len(s1)): # separate notes
        if jj+1 in sx:
            el=True
        else:
            el=False
        
        note=s1[jj]
        bet_chor=find_chord(chord,note)
        if first==1: # find a first note 
            ran1=np.random.choice(bet_chor)
            innote=ran1.find(note)
            ran2=ran1.replace(note,"")
            fnote=ran2[np.random.choice(2)]
            prev=fnote
            first+=1
            better=better+note+fnote+"-"
            tune_list[jj]+=fnote
        else:
            if el is True:
#                voi=np.random.choice(updown) # random change in diff voice
                let=find_sec(chord,prev,note)
#                print(note,let)
#                newar1=[]
#                for voi in updown:
#                    let=in_letter(ord(prev)+voi) # shift note
#                    newc=find_chord(bet_chor,let) # find all chord satisfy harmony
#                    newar.append(newc)
#                for i in newar:
#                print(newar)   
#                if let == note:
#                    newc=[]
                 
#                si=np.shape(newc)
#                if newc:
                better=better+note+"/"+let+"-"
                tune_list[counter]+="/"+let
#                else:
#                    better=better+note+"-"
#                prev=let
            else:
                better=better+note+"-" 
        counter+=1
    better=better+"|"

print(better)
print(mus)
print(tune_list)
#print(ss2)
        

#print(len(tune),len(commas),ind,a)