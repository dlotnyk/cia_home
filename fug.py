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
    """make a chord a combine into file xml format"""
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
def make_tune(voice,VV,tune,part,num_measure):
    """save a tune into file"""
    bb=BS("","lxml")
    tag_tick=bb.new_tag("tick") # voice separator 1920
    
    if voice!=0:
        tag_tick.append(str(1920*num_measure))
        bb.append(tag_tick)
    for ii in range(len(tune[part])):
        ch=make_chord(voice,tune[part][ii][0],VV[tune[part][ii][1]][1],VV[tune[part][ii][1]][2])
        bb.append(ch)
    return bb
#tune1="4 1,4 5,4 3,4-1"#,|8-2,8-1,4-2,8-3,8-4,8-3,8-2,"
    #subject
tune=[[[4,1],[4,5],[4,3],[4,1]],[[8,2],[8,1],[4,2],[8,3],[8,4],[8,3],[8,2]]]
tune01=tune
tune01[0][1]=tune01[0][0]
# X
tunex=[[[4,2],[4,3],[4,1],[4,2]],[[4,1],[4,2],[4,3],[8,2],[8,1]]]
tunex1=tunex
tunex1[0][1]=tunex1[0][0]
# Y
tuney=[[[8,1],[8,2],[8,3],[8,4],[8,3],[8,2],[8,3],[8,4]],[[4,3],[4,2],[4,1],[4,0]]]
tuney1=tuney
tuney1[0][1]=tuney1[0][0]
#Z
tunez=[[[2,1],[2,2]],[[1,3]]]
tunez1=tunez
tunez1[0][1]=tunez1[0][0]
#A
tunea=[[[8,1],[8,2],[8,3],[8,4],[8,3],[8,2],[8,3],[8,4]],[[16,3],[16,2],[16,1],[16,0],[16,1],[16,2],[16,3],[16,4],[16,3],[16,4],[16,3],[16,4],[8,3],[8,2]]]
tunea1=tunea
tunea1[0][1]=tunea1[0][0]
#B
tuneb=[[[8,3],[8,2],[8,3],[8,4],[8,5],[8,4],[8,3],[8,2]],[[8,1],[8,2],[8,3],[8,4],[8,5],[8,4],[8,3],[8,2]]]
tuneb1=tuneb
tuneb1[0][1]=tuneb1[0][0]
#C
tunec=[[[4,4],[4,5],[4,1],[4,2]],[[4,1],[4,5],[4,3],[4,1]]]
tunec1=tunec
tunec1[0][1]=tunec1[0][0]
#print(tune01)
#print(tune[0][0][1])
harmony=["CEG","DFA","EGB","FAC","GBD","ACE","BDF"]
firstV=[["B","72","14"],["C","74","16"],["D","76","18"],["E","77","13"],["F","79","15"],["G","81","17"],["A","83","19"]]
secondV=[["B","60","14"],["C","62","16"],["D","64","18"],["E","65","13"],["F","67","15"],["G","69","17"],["A","71","19"]]
thirdV=[["B","48","14"],["C","50","16"],["D","52","18"],["E","53","13"],["F","55","15"],["G","57","17"],["A","59","19"]]
forthV=[["B","36","14"],["C","38","16"],["D","40","18"],["E","41","13"],["F","43","15"],["G","45","17"],["A","47","19"]]
data=open_f()
measures=data.find_all('Measure') # number of bars
counter=0
# measure 3 
# X -0- S'-0
rest=measures[2].find_all('Rest')
bb=make_tune(0,firstV,tunex,0,2) # first voice
bb3=make_tune(2,thirdV,tune01,0,2) # third voice
bb.append(bb3)
rest[0].replaceWith(bb)
# measure 4
rest=measures[3].find_all('Rest')
bb=make_tune(0,firstV,tunex,1,3)
bb1=make_tune(2,thirdV,tune01,1,3)
bb.append(bb1)
rest[0].replaceWith(bb)
#measure 5
#Y-S-X'
rest=measures[4].find_all('Rest')
bb=make_tune(0,firstV,tuney,0,4)
bb1=make_tune(1,secondV,tune,0,4)
bb2=make_tune(2,thirdV,tunex1,0,4)
bb.append(bb1)
bb.append(bb2)
rest[0].replaceWith(bb)
#measure 6
tune=[[[4,1],[4,5],[4,3],[4,1]],[[8,2],[8,1],[4,2],[8,3],[8,4],[8,3],[8,2]]]
rest=measures[5].find_all('Rest')
bb=make_tune(0,firstV,tuney,1,5)
bb1=make_tune(1,secondV,tune,1,5)
bb2=make_tune(2,thirdV,tunex1,1,5)
bb.append(bb1)
bb.append(bb2)
rest[0].replaceWith(bb)
# measure 7
#Z-X-Y'-S'
rest=measures[6].find_all('Rest')
bb=make_tune(0,firstV,tunez,0,6)
bb1=make_tune(1,secondV,tunex,0,6)
bb2=make_tune(2,thirdV,tuney1,0,6)
bb3=make_tune(3,forthV,tune01,0,6)
bb.append(bb1)
bb.append(bb2)
bb.append(bb3)
rest[0].replaceWith(bb)
# measure 8
rest=measures[7].find_all('Rest')
bb=make_tune(0,firstV,tunez,1,7)
bb1=make_tune(1,secondV,tunex,1,7)
bb2=make_tune(2,thirdV,tuney1,1,7)
bb3=make_tune(3,forthV,tune01,1,7)
bb.append(bb1)
bb.append(bb2)
bb.append(bb3)
rest[0].replaceWith(bb)
# measure 9
#A-Y-Z'-X'
rest=measures[8].find_all('Rest')
bb=make_tune(0,firstV,tunea,0,8)
bb1=make_tune(1,secondV,tuney,0,8)
bb2=make_tune(2,thirdV,tunez1,0,8)
bb3=make_tune(3,forthV,tunex1,0,8)
bb.append(bb1)
bb.append(bb2)
bb.append(bb3)
rest[0].replaceWith(bb)
# measure 10
#A-Y-Z'-X'
rest=measures[9].find_all('Rest')
bb=make_tune(0,firstV,tunea,1,9)
bb1=make_tune(1,secondV,tuney,1,9)
bb2=make_tune(2,thirdV,tunez1,1,9)
bb3=make_tune(3,forthV,tunex1,1,9)
bb.append(bb1)
bb.append(bb2)
bb.append(bb3)
rest[0].replaceWith(bb)
# measure 11
#B-Z-A'-Y'
rest=measures[10].find_all('Rest')
bb=make_tune(0,firstV,tuneb,0,10)
bb1=make_tune(1,secondV,tunez,0,10)
bb2=make_tune(2,thirdV,tunea1,0,10)
bb3=make_tune(3,forthV,tuney1,0,10)
bb.append(bb1)
bb.append(bb2)
bb.append(bb3)
rest[0].replaceWith(bb)
# measure 12
#B-Z-A'-Y'
rest=measures[11].find_all('Rest')
bb=make_tune(0,firstV,tuneb,1,11)
bb1=make_tune(1,secondV,tunez,1,11)
bb2=make_tune(2,thirdV,tunea1,1,11)
bb3=make_tune(3,forthV,tuney1,1,11)
bb.append(bb1)
bb.append(bb2)
bb.append(bb3)
rest[0].replaceWith(bb)
# measure 13
#C-A-B'-Z'
rest=measures[12].find_all('Rest')
bb=make_tune(0,firstV,tunec,0,12)
bb1=make_tune(1,secondV,tunea,0,12)
bb2=make_tune(2,thirdV,tuneb1,0,12)
bb3=make_tune(3,forthV,tunez1,0,12)
bb.append(bb1)
bb.append(bb2)
bb.append(bb3)
rest[0].replaceWith(bb)
# measure 14
#C-A-B'-Z'
rest=measures[13].find_all('Rest')
bb=make_tune(0,firstV,tunec,1,13)
bb1=make_tune(1,secondV,tunea,1,13)
bb2=make_tune(2,thirdV,tuneb1,1,13)
bb3=make_tune(3,forthV,tunez1,1,13)
bb.append(bb1)
bb.append(bb2)
bb.append(bb3)
rest[0].replaceWith(bb)
# measure 15
#0-0-0-A
tune=[[[4,1],[4,5],[4,3],[4,1]],[[8,2],[8,1],[4,2],[8,3],[8,4],[8,3],[8,2]]]
rest=measures[14].find_all('Rest')
bb=make_tune(0,forthV,tune,0,14)
rest[0].replaceWith(bb)
# measure 16
#A
rest=measures[15].find_all('Rest')
bb=make_tune(0,forthV,tune,1,15)
rest[0].replaceWith(bb)
## measure 17
tr1=tune[::-1]
tr2=tr1
tr2[0]=tr1[0][::-1]
tr2[1]=tr1[1][::-1]
rest=measures[16].find_all('Rest')
bb=make_tune(0,forthV,tr2,0,16)
rest[0].replaceWith(bb)
#measure 18
rest=measures[17].find_all('Rest')
bb=make_tune(0,forthV,tr2,1,17)
rest[0].replaceWith(bb)
#rest=measures[16].find_all('Rest')
#bb=make_tune(0,forthV,tune[1][::-1],0,16)
#rest[0].replaceWith(bb)
## measure 18
##rev
#rest=measures[17].find_all('Rest')
#bb=make_tune(0,forthV,r0,1,17)
#rest[0].replaceWith(bb)
# save
save_f(data)
#a1=1920*3
#s=str(a1)
#tag_tick.append("5760")
#for ii in range(len(tunex[1])):
#    ch=make_chord(0,tunex[1][ii][0],firstV[tunex[1][ii][1]][1],firstV[tunex[1][ii][1]][2])
#    bb.append(ch)
##third voice
#bb.append(tag_tick)
#for ii in range(len(tune01[1])):
#    ch=make_chord(2,tune01[1][ii][0],thirdV[tune01[1][ii][1]][1],thirdV[tune01[1][ii][1]][2])
#    bb.append(ch)

#for mm in measures:
#    if counter>1:
#        if counter%2==0:
#            rest=mm.find_all('Rest')
#            bb=BS("","lxml")
#            for ii in range(len(tune[0])):
#                ch=make_chord(0,tune[0][ii][0],thirdV[tune[0][ii][1]][1],thirdV[tune[0][ii][1]][2])
#                bb.append(ch)
#            rest[0].replaceWith(bb)
#        else:
#            rest=mm.find_all('Rest')
#            bb=BS("","lxml")
#            for ii in range(len(tune[1])):
#                ch=make_chord(0,tune[1][ii][0],thirdV[tune[1][ii][1]][1],thirdV[tune[1][ii][1]][2])
#                bb.append(ch)
#            rest[0].replaceWith(bb)
#    counter+=1
#    
                
