# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 21:28:32 2018

@author: dmytr
"""
import re
import numpy as np
from bs4 import BeautifulSoup as BS
from bs4 import Tag
from shutil import copyfile

def open_f():
    """open tune file"""
    source = "fugh.mscx"
    target="fugh_copy.mscx"
    infile = open(source,"r")
    contents = infile.read()
    data = BS(contents, 'xml')
    copyfile(source, target)
    return data

def save_f(data):
    """save modified data"""
    target="fugh_copy.mscx"
    st1=str(data)
    with open(target,'w') as file1:
        file1.write(st1)

def find_note(notesb,pitch,tps):
    """find a note based on file's pitch and tps"""
    for ch in notesb:
        for ii in range(1,5,2):
            if ch[ii]==pitch and ch[ii+1]==tps:
                let=ch[0]
    return let

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
def duration(num):
    """Convert number into string"""
    if num==1:
        let="whole"
    elif num==2:
        let="half"
    elif num==4:
        let="quarter"
    elif num==8:
        let="eighth"
    elif num==16:
        let="16th"
    return let
def make_chord(voice,dur,pitch,tpc):
    bbn=BS("","lxml")
    tag_chord=bbn.new_tag("Chord")
    tag_track=bbn.new_tag("track")
    tag_dur=bbn.new_tag("durationType")
    tag_note=bbn.new_tag("Note")
    tag_pitch=bbn.new_tag("pitch")
    tag_tps=bbn.new_tag("tpc")
    let=duration(dur)
    if voice==0:
        tag_chord.append(tag_dur)
        tag_dur.append(let)
        tag_chord.append(tag_note)
        tag_note.append(tag_pitch)
        tag_pitch.append(pitch)
        tag_note.append(tag_tps)
        tag_tps.append(tpc)
    else:
        tag_chord.append(tag_track)
        tag_track.append(str(voice))
        tag_chord.append(tag_dur)
        tag_dur.append(let)
        tag_chord.append(tag_note)
        tag_note.append(tag_pitch)
        tag_pitch.append(pitch)
        tag_note.append(tag_tps)
        tag_tps.append(tpc)
    bbn.append(tag_chord)   
    return bbn
a=make_chord(1,4,"65","15")
print(a)
#tune1="4 1,4 5,4 3,4-1"#,|8-2,8-1,4-2,8-3,8-4,8-3,8-2,"
tune=[[[4,1],[4,5],[4,3],[4,1]],[[8,2],[8,1],[4,2],[8,3],[8,4],[8,3],[8,2]]]
#print(tune[0][0][1])
harmony=["CEG","DFA","EGB","FAC","GBD","ACE","BDF"]
firstV=[["B","72","14"],["C","74","16"],["D","76","18"],["E","77","13"],["F","79","15"],["G","81","17"],["A","83","19"]]
secondV=[["B","60","14"],["C","62","16"],["D","64","18"],["E","65","13"],["F","67","15"],["G","69","17"],["A","71","19"]]
thirdV=[["B","48","14"],["C","50","16"],["D","52","18"],["E","53","13"],["F","55","15"],["G","57","17"],["A","59","19"]]
forthV=[["B","36","14"],["C","38","16"],["D","40","18"],["E","41","13"],["F","43","15"],["G","45","17"],["A","47","19"]]
data=open_f()
measures=data.find_all('Measure') # number of bars
counter=0
for mm in measures:
    if counter>1:
        if counter%2==0:
            rest=mm.find_all('Rest')
            bb=BS("","lxml")
            for ii in range(len(tune[0])):
                ch=make_chord(0,tune[0][ii][0],thirdV[tune[0][ii][1]][1],thirdV[tune[0][ii][1]][2])
                bb.append(ch)
            rest[0].replaceWith(bb)
        else:
            rest=mm.find_all('Rest')
            bb=BS("","lxml")
            for ii in range(len(tune[1])):
                ch=make_chord(0,tune[1][ii][0],thirdV[tune[1][ii][1]][1],thirdV[tune[1][ii][1]][2])
                bb.append(ch)
            rest[0].replaceWith(bb)
    counter+=1
    
save_f(data)                
print(tune[0][1][1])