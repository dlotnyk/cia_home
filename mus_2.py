# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 22:52:25 2018

@author: dmytr
"""

"""
Created on Sun Jul  8 16:13:21 2018

@author: dmytr
"""
import re
import numpy as np
from bs4 import BeautifulSoup as BS
from bs4 import Tag
from shutil import copyfile

def open_f():
    """open tune file"""
    source = "tune1.mscx"
    target="tune1_copy.mscx"
    infile = open(source,"r")
    contents = infile.read()
    data = BS(contents, 'xml')
    copyfile(source, target)
    return data

def save_f(data):
    """save modified data"""
    target="tune1_copy.mscx"
    st1=str(data)
    with open(target,'w') as file1:
        file1.write(st1)
 
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
    """ Convert number to letter"""
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

def find_note(notesb,pitch,tps):
    """find a note based on file's pitch and tps"""
    for ch in notesb:
        for ii in range(1,5,2):
            if ch[ii]==pitch and ch[ii+1]==tps:
                let=ch[0]
    return let
             
#def note_replace(chord,note):
def find_pitch(notesb,let,number):
    """find pitch and tps based on letter"""
    for ch in notesb:
        if ch[0]==let:
            if number==0:
                pitch=ch[1]
                tps=ch[2]
            else:
                pitch=ch[3]
                tps=ch[4]
    return pitch,tps
            
    
def exclude(chor,a):
    id1=chor.find(a)
    let=""
    for i in range(3):
        if i!=id1:
            let+=chor[i]
    return let

notesb=[["A","57","19","69","17"],["B","47","19","59","19"],["C","48","17","60","14"],["D","50","16","62","16"],["E","52","18","64","18"],["F","53","13","65","13"],["G","55","15","67","15"]]
harmony=["CEG","DFA","EGB","FAC","GBD","ACE","BDF"]
sp10=" "*10
lefbr="<Note>"+sp10+"<pitch>"
midbr="</pitch>"+sp10+"<tps>"
rigbr="</tps>"+sp10+"</Note>"+sp10
tune="EGFEDC,DEF,EDFEGFE,FED,GGGC,DCDEFED,GGAF,ECDC,"
updown=[-1,0,1]
sync="3 5,1 3,1 3 6,1 3,2 4,1 3 5,2 4,2 4,"
coms=re.findall(r'(?<!\d),(?!\d)', sync)
data=open_f()
measures=data.find_all('Measure') # number of bars
for jj in measures: #bars
    chords=jj.find_all('Chord')
    skip=np.random.randint(len(chords))
    sk_num=0
    for kk in chords: # chords
        
        note=kk.find_all('Note')
          
        for ll in note: # notes
            if sk_num!=skip:
                pitch=ll.find_all('pitch')
                tpc=ll.find_all('tpc')
    #                print(pitch[0].contents[0],tpc[0].contents[0])
                let=find_note(notesb,pitch[0].contents[0],tpc[0].contents[0])
                ch1=find_chord(harmony,let)
                ch2=np.random.choice(ch1)
                bbn=BS()
                
                for ii in ch2:
                    tag_note=bbn.new_tag("Note")
                    tag_pitch=bbn.new_tag("pitch")
                    tag_tps=bbn.new_tag("tps")
                    p1,t1=find_pitch(notesb,ii,1)
    #                    st=st+lefbr+p1+midbr+t1+rigbr
                    tag_note.append(tag_pitch)
                    tag_pitch.append(p1)
                    tag_note.append(tag_tps)
                    tag_tps.append(t1)
                    bbn.append(tag_note)
                ll.replaceWith(bbn)
        sk_num+=1

save_f(data)