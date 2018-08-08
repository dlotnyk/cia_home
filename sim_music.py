# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 21:00:26 2018

@author: dmytr
"""
from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import kaiserord, lfilter, firwin, freqz, correlate
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
#        print(int(l/2),int(l))
#        rec[int(l/2):-1]=rec[0:int(l/2)-1]
        rec1=np.fft.ifft(rec)
#        print(np.shape(self.time),np.shape(rec),np.shape(rec1))
        fig1 = plt.figure(num_fig, clear = True)
        ax1 = fig1.add_subplot(211)
        ax1.set_ylabel('Amplitude [a.u.]')
        ax1.set_xlabel('Frequency [Hz]')
        ax1.set_title('FFT')
        ax1.plot(f, p1, color='green',lw=1)
        ax1.set_xlim(0,7500)
#        ax1.plot(f,rec,color='red',lw=1)
        plt.grid()
        ax2 = fig1.add_subplot(212)
        ax2.set_ylabel('Amplitude [a.u.]')
        ax2.set_xlabel('Time [sec]')
        ax2.set_title(' ')
        ax2.plot(time,rec1, color='green',lw=1)
        plt.grid()
        plt.show()
        return p1,f
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
        ax1.set_ylabel('Amplitude [a.u.]')
        ax1.set_xlabel('Time [sec]')
        ax1.set_title('Original and FIR filtered Violin wav data')
        ax1.plot(self.time, self.data, color='green',lw=1)
        ax1.plot(self.time,filtered_x,color='red',lw=1)
        ax1.legend(['Original data','FIR filtered'])
        plt.grid()
        plt.show()
        self.filt=np.int16(filtered_x)
        
    def cut_wav(self,data,n1,n2):
        '''cut some note from wav file'''
        c_data=data[n1:n2]
        time=np.linspace(n1/self.fs,n2/self.fs,int(n2-n1))
#        print(np.shape(time)[0],np.shape(c_data)[0])
#        self.fft_f(time,c_data,5)
        self.save_f(c_data,'part.wav',0)
        return c_data,time
    def shift(self,data,nn):
        '''shift one wav over another'''
        num=int(nn)
        # first voice
        dnum=np.shape(data)[0]
        time=np.linspace(0,(num+dnum)/self.fs,int(num+dnum))
        ch1=np.zeros(dnum+num,dtype='int16')
        ch2=np.zeros(dnum+num,dtype='int16')
        for ii in range(dnum):
            ch1[ii]=data[ii]
            ch2[ii+num]=data[ii]
        ch_mix=np.zeros((dnum+num,2),dtype='int16')
        ch_add=np.zeros(dnum+num,dtype='int16')
        for ii in range(dnum+num):
            if ii%2==0:
                ch_add[ii]=ch1[ii]
            else:
                ch_add[ii]=ch2[ii]
            ch_mix[ii][0]=ch1[ii]
            ch_mix[ii][1]=ch2[ii]
        self.save_f(ch_add,'ch_add.wav',0)
        self.save_f(ch_mix,'ch_mix.wav',0)
        self.fft_f(time,ch_add,6)
        return ch_add,ch_mix,time
    def gen_sample(self,data):
        '''generate wav with'''
        delay=0
        delay2=3000
        for ii in range(10):
            if ii==0:
                ch_add,ch_mix,t=self.shift(data,delay)
                ch_add2,ch_mix2,t2=self.shift(data,delay2)
            else:
                ch_a,ch_m,t=self.shift(data,delay)
                ch_add=np.concatenate((ch_add,ch_a))
                ch_mix=np.concatenate((ch_mix,ch_m))
                ch_a2,ch_m2,t2=self.shift(data,delay2)
                ch_add2=np.concatenate((ch_add2,ch_a2))
                ch_mix2=np.concatenate((ch_mix2,ch_m2))
            delay+=200
            delay2-=300
        print(np.shape(ch_mix),delay)
        self.save_f(ch_add,'sample_1.wav',0)
        self.save_f(ch_mix,'sample_m.wav',0)
        self.save_f(ch_add2,'sample_2.wav',0)
        self.save_f(ch_mix2,'sample_m2.wav',0)
        
    def cr_corr(self,data):
        '''1D cross correleation'''          
        data1,ch_mix,time=self.shift(data,1800)
        lag = np.argmax(correlate(data1, data))
        d = np.roll(data, shift=int(np.ceil(lag)))
#        print(np.shape(c_sig))
#        d=np.correlate(data,data1)
        num=np.shape(d)[0]
        fig1 = plt.figure(30, clear = True)
        ax1 = fig1.add_subplot(111)
        ax1.set_ylabel('Amplitude [a.u.]')
        ax1.set_xlabel('Time [sec]')
        ax1.set_title('Original and FIR filtered Violin wav data')
        ax1.plot(range(num), d, color='green',lw=1)
#        ax1.plot(self.time,filtered_x,color='red',lw=1)
#        ax1.legend(['Original data','FIR filtered'])
        plt.grid()
        plt.show()
        
       
#file=wave.open(wavfiles[0],mode='r')
#data=wave_read.getparams()
A=wavf()
#print(np.shape(A.data),np.shape(A.time))
fig1 = plt.figure(1, clear = True)
ax1 = fig1.add_subplot(111)
ax1.set_ylabel('Amplitude [a.u.]')
ax1.set_xlabel('Time [sec]')
ax1.set_title('Original signal. Violin')
ax1.plot(A.time, A.data, color='green',lw=1)
d=A.data
plt.grid()
plt.show()

p1,f1=A.fft_f(A.time,A.data,2)
A.fir_f(5,5,50,1300)
p2,f2=A.fft_f(A.time,A.filt,4)

fig1 = plt.figure(10, clear = True)
ax1 = fig1.add_subplot(111)
ax1.set_ylabel('Amplitude [a.u.]')
ax1.set_xlabel('Frequency [Hz]')
ax1.set_title('FFT of original and FIR filtered Violin wav data')
ax1.plot(f1, p1, color='green',lw=1)
ax1.plot(f2,p2,color='red',lw=1)
ax1.legend(['Original data','FIR filtered'])
ax1.set_xlim(0,7500)
plt.grid()
plt.show()
       
A.save_f(A.filt,'test.wav',0)
c_data,c_time=A.cut_wav(A.filt,10000,75000)
p3,f3=A.fft_f(c_time,c_data,5)
ch_add,ch_mix,time2=A.shift(c_data,10000)
p4,f4=A.fft_f(time2,ch_add,8)

fig1 = plt.figure(11, clear = True)
ax1 = fig1.add_subplot(111)
ax1.set_ylabel('Amplitude [a.u.]')
ax1.set_xlabel('Frequency [Hz]')
ax1.set_title('FFT of sample and shifted')
ax1.plot(f3, p3, color='green',lw=1)
ax1.plot(f4, p4,color='red',lw=1)
ax1.legend(['Sample','Shifted'])
ax1.set_xlim(0,7500)
plt.grid()
plt.show()

A.gen_sample(c_data)
A.cr_corr(c_data)
del A