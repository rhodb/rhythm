#This module will be the home to the functions which actually create the 
#amplitude envelope.

#import necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile as wav
from scipy import signal
from playsound import playsound




#This function will do a hilbert transform on the signal, then take the absolute 
#value of that to get the envelope. To get a smoothed version of this, we will 
#use a fourth-order butterworth filter. The arguments for this function are the
#audio data (a vector of floats) and a sampling frequency. This function only 
#computes does the envelope for a few pieces of the data at first to make sure 
#the output is acceptable. If so, then it will proceed to compute it for the rest.

def get_envelope(filename, data, sfreq, nsamples = 5, size=5):
    #get the length of the audio data. then, get an upper limit on the interval 
    #of a sample chunk. then, only get a fraction of the upperlimit for sample
    n = len(data)
    upperlim = int(np.floor(n/nsamples))
    interval_size = int(np.ceil(upperlim/size))
    
    #get intervals randomly
    interval_list = []
    for i in range(nsamples):
        lower = np.random.randint(0, n-interval_size)
        interval_list += [(lower,lower+interval_size)]
    
    #run through each sample and make sure that the smoothing is good before 
    #proceeding for the whole file
    smooth = 5
    for i in range(nsamples):
        l = interval_list[i][0]
        u = interval_list[i][1]
        print("Interval you are listening to is " + str(l/sfreq) + " to " \
              + str(u/sfreq) + " secs")
        _, smooth = compute_envelope(data[l:u], sfreq, smooth, (l,u))
        
        #add chunk to data set if good
        if input("Use as piece of data? ") == "y":
            add_to_dataset(filename, data[l:u], smooth, (l/sfreq,u/sfreq))

    if input("Do complete signal? (y/n): ") == "y":
        output, _ = compute_envelope(data, sfreq, smooth, show=False)
        return output
    else:
        return None
    

    
#This function will do a hilbert transform on the signal, then take the absolute
#value of that to get the envelope. To get a smoothed version of this, we will 
#use a fourth-order butterworth filter. The arguments for this function are the
#audio data (a vector of floats), a sampling frequency and a smoothing parameter.
def compute_envelope(d, fr, smoothparameter=5, interval = None, show=True):
    newdata = np.abs(signal.hilbert(d))
    b, a = signal.butter(4, smoothparameter, fs=fr)
    output = signal.filtfilt(b, a, newdata)
    
    #bit of code to display envelope over signal, with audio to determine good 
    #smoothing parameter
        
    if show:
        #get window
        lower = str(interval[0]*(1/fr))
        upper = str(interval[1]*(1/fr))
        #plot
        plt.plot(d)
        plt.plot(output)
        plt.title("You are listening to " + lower + " to " + upper + " secs")
        plt.show(block=False)
        
        #play audio file
        i = np.random.randint(0, 10000)
        wav.write("sample" + str(i) + ".wav", fr, d)
        response = input("Hit enter to play sound: ")
        
        while (response == ""):
            playsound("sample" + str(i) + ".wav", block=False)
            response = input("Hit enter to play sound and 's' to stop: ")
        
        
        #cleanup
        plt.close()
        
        #check smoothing
        reply = input("Good smoothing? (y/n): ")
    
        #recurse until find good smoothing parameter
        if reply == "y":
            return output, smoothparameter
        else:
            new_smoothparameter = float(input("Specify new smoothing. Previous was " \
                                              + str(smoothparameter) + ": "))
            return compute_envelope(d,fr,new_smoothparameter,interval)
        
    return output, smoothparameter


#This function will open the data file in the current directory to add bits 
#of audio that have been labelled to an existing data set so that we can use 
#it for downstream automated labelling
def add_to_dataset(filename, data, label, time):
    audiofile = open("smoothing_data_audio.txt", "a")
    labelfile = open("smoothing_data_labels.txt", "a")
    
    #use this so that we can write the arrays as rows and not columns
    width = len(data)
    data = np.reshape(data, (1,width))
    
    np.savetxt(audiofile, data, delimiter = ",", fmt="%d")
    #audiofile.write(np.array2string(data, max_line_width = max_width)+"\n")
    labelfile.write(str(label)+","+filename+","+str(time[0])+","+\
                    str(time[1])+"\n")
    
    labelfile.close()
    audiofile.close()
    
    return
    