# -*- coding: utf-8 -*-
"""
Markov chain
"""
import numpy as np
noun=np.array(["дом","школа","квартира","человек","окно","книга","огонь"]) #0
verb=np.array(["идти","бежать","делать","быть","лететь","искать","говорить"]) #1
advrb=np.array(["высокий","быстрый","сильный","красивый","яркий","умный","тёмный"]) #2
pronoun=np.array(["я","он","она","оно","мы","вы","ты","они","эти","те"]) #3
numeral=np.array(["один","два","три","четыре","пять","десять","сто"]) #4
pretext=np.array(["на","под","возле","перед","с","в","до","от"]) #5
first=np.array([0,0,0,1,2,2,3,3,4,4,4,5,5])
noun_f=np.array([1,1,1,2,4,5])
verb_f=np.array([0,0,2,3,3,4,4,4,5])
advrb_f=np.array([0,0,0,2,3,3])
pronoun_f=np.array([1,1,1,2,2,4,4,5])
numeral_f=np.array([0,0,0,2,2,5])
pretext_f=np.array([0,0,0,4,4])
count=0
word=0
while count<10:
    if count == 0:
        word=np.random.choice(first)
    else:
        if word == 0:
            word=np.random.choice(noun_f)
        elif word == 1:
            word=np.random.choice(verb_f)
        elif word == 2:
            word=np.random.choice(advrb_f)
        elif word == 3:
            word=np.random.choice(pronoun_f)
        elif word == 4:
            word=np.random.choice(numeral_f)
        elif word == 5:
            word=np.random.choice(pretext_f)
    if word == 0:
        print(np.random.choice(noun), end=" ")
    elif word == 1:
        print(np.random.choice(verb), end=" ")
    elif word == 2:
        print(np.random.choice(advrb), end=" ")
    elif word == 3:
        print(np.random.choice(pronoun), end=" ")
    elif word == 4:
        print(np.random.choice(numeral), end=" ")
    elif word == 5:
        print(np.random.choice(pretext), end=" ")
    
    count+=1
print(np.random.choice(noun))