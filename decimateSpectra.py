import numpy
import glob, os
from scipy import interpolate

def decimateSpec(rawPSDLocation):
    rawPSDList = []
    os.chdir(rawPSDLocation)
    os.mkdir('decim_psd')
    for file in glob.glob("*.txt"):
        rawPSDList.append(file)
    
    adc_ch = 3 # PSD data is on 4th column of raw PSD file (Python starts count at 0)
    fpnts = 2001 # Decimate to make array the same as S-parameters
    a, b = 4075, 12223 # [a,b] corresponding to 50-150MHz
    
    # Taking rows 4075-12223 from column 4 and interpolating to 2001 points
    for rawPSD in rawPSDList:
        f = open(rawPSD, 'r')
        data = f.readlines()
        f.close()
        psd = []
        for line in data:
            psd.append(line.split(' ')[adc_ch])
        psd = psd[a-2:b]
        dd = interpolate.interp1d(numpy.arange(a-2,b), psd, kind='linear')
        fspace = numpy.linspace(a-1,b-1,fpnts)
        psd = dd(fspace)
    
        # Writing to file
        numpy.savetxt('decim_psd/decim_%s' %rawPSD, psd)
    return

# Input folder with raw psds
#decimateSpec('raw_psds')
