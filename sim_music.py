# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 21:00:26 2018

@author: dmytr
"""
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import kaiserord, lfilter, firwin, freqz
#open wav files
class wavf:
    def __init__(self):
        self.wavfiles=['Violin-I-1.wav']
        self.fs,self.data=self.open_f(0)
        self.time=np.linspace(0,np.shape(self.data)[0]/self.fs,np.shape(self.data)[0])
#        self.fft_f()
    def open_f(self,num):
        '''opens the wavfile. num is usefull if files are many'''
        fs, data = wavfile.read(self.wavfiles[num]) # sampling frequency and the wav itself
        l=np.shape(data)[0]
        if l%2==0:
            data1=data
        else:
            data1=np.delete(data,0)
        return fs,data1
    def save_f(self,data,file,num):
        '''save data into wav file'''
#        file='test.wav'
        wavfile.write(file,self.fs,data)
    def fft_f(self,time,data,num_fig):
        '''fft of data file'''
        l=np.shape(data)[0]
        y=np.fft.fft(data)
        p2=np.abs(y/l)
        p1 = p2[0:int(l/2)+1]
        p1[0:-2] = 2*p1[0:-2];
        f = self.fs/l*np.linspace(0,l/2,int(l/2)+1);
        rec=np.zeros(len(y),dtype=np.complex_)
        count=0;
        for x in np.nditer(y):
            if np.abs(x/l)>=0.2:
                rec[count]=x
            else:
                rec[count]=0
            count+=1
        print(int(l/2),int(l))
#        rec[int(l/2):-1]=rec[0:int(l/2)-1]
        rec1=np.fft.ifft(rec)
#        print(np.shape(self.time),np.shape(rec),np.shape(rec1))
        fig1 = plt.figure(num_fig, clear = True)
        ax1 = fig1.add_subplot(211)
        ax1.set_ylabel('ampl')
        ax1.set_xlabel('frequency')
        ax1.set_title('ampl and f')
        ax1.plot(f, p1, color='green',lw=1)
#        ax1.plot(f,rec,color='red',lw=1)
        
        ax2 = fig1.add_subplot(212)
        ax2.set_ylabel('ampl')
        ax2.set_xlabel('time')
        ax2.set_title('ampl and time')
        ax2.plot(time,rec1, color='green',lw=1)
        plt.grid()
        plt.show()
    def fir_f(self,nr,wid,db,cut):
        '''the FIR filter'''
        # The Nyquist rate of the signal.
        nyq_rate = self.fs / nr
        # The desired width of the transition from pass to stop,
        # relative to the Nyquist rate.  We'll design the filter
        # with a 5 Hz transition width.
        width=wid/nyq_rate
        # The desired attenuation in the stop band, in dB.
        ripple_db = db
        # Compute the order and Kaiser parameter for the FIR filter.
        N, beta = kaiserord(ripple_db, width)
        # The cutoff frequency of the filter.
        cutoff_hz = cut
        # Use firwin with a Kaiser window to create a lowpass FIR filter.
        taps = firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
        # Use lfilter to filter x with the FIR filter.
        filtered_x = lfilter(taps, 1.0, self.data)
        fig1 = plt.figure(3, clear = True)
        ax1 = fig1.add_subplot(111)
        ax1.set_ylabel('ampl')
        ax1.set_xlabel('time')
        ax1.set_title('ampl and t')
        ax1.plot(self.time, self.data, color='green',lw=1)
        ax1.plot(self.time,filtered_x,color='red',lw=1)
        plt.grid()
        plt.show()
        self.filt=np.int16(filtered_x)
        
    def cut_wav(self,data,n1,n2):
        '''cut some note from wav file'''
        c_data=data[n1:n2]
        self.save_f(c_data,'part.wav',0)
        
    
#file=wave.open(wavfiles[0],mode='r')
#data=wave_read.getparams()
A=wavf()
#print(np.shape(A.data),np.shape(A.time))
fig1 = plt.figure(1, clear = True)
ax1 = fig1.add_subplot(111)
ax1.set_ylabel('ampl')
ax1.set_xlabel('time')
ax1.set_title('ampl and time')
ax1.plot(A.time, A.data, color='green',lw=1)
d=A.data
plt.grid()
plt.show()
A.fft_f(A.time,A.data,2)
A.fir_f(5,5,50,1000)
A.fft_f(A.time,A.filt,4)
A.save_f(A.filt,'test.wav',0)
A.cut_wav(A.filt,100,100000)
del A