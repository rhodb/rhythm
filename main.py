from envelopes import *
import glob, os
import numpy as np


#wrapper function to do envelope functionality. helps with organizing the 
#different processes as well
def envelope(filename):
    rate, audiodata = wav.read(filename)
    output = get_envelope(audiodata, rate, nsamples = 3, size = 40, filename)
    #get the local maxima and their values... FINISH LATER
    #maxima_values = get_maxima(output, rate)
    
    return output

    
#function which gets the local maxima and their values for a time series
def get_maxima(out, freq):
    maxima = signal.argrelextrema(output, np.greater)[0]*(1/freq)
    values = [output[m] for m in maxima]
    return zip(maxima,values)

    
#main routine
if __name__ == "__main__":
    
    #choose folder
    folder = input("Which folder? ")
    os.chdir("./"+folder)
    
    filename = input("Which file do you want? ")
    output = envelope(filename)
    
    np.savetxt(filename+"_smoothed", output, delimiter=',')

    
    #clean up files from the function `envelope'
    for f in glob.glob("sample*.wav"):
        try:
            os.remove(f)
        except:
            pass