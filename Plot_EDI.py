# -*- coding: utf-8 -*-
"""
                Plot_EDI.py
                ------
  - This program plots Apparent resistivity and Phase curves

"""

#---USER INPUT Section-------------
station = 'A01'
name_of_folder = r'.' 
#------------------------------------
#=======================================================


import os
# import csv
import math
import matplotlib.pyplot as plt


#---INPUT-EDI file name and Folder---
station = 'A01'
name_of_folder = r'.' 
#------------------------------------

f = open("{}.edi".format(station))
EDIFile = f.readlines() 

#------ NFREQ, LAT and LONG ------------

nofreq1 = []; lat1=[]; long1 = [] 

for index, line in enumerate(open("{}.edi".format(station))):
    if 'NFREQ=' in line:       
        nofreq1.append(line.split()[0])
    if 'REFLAT=' in line:
        lat1.append(line.split()[0])
    if 'REFLONG=' in line:
        long1.append(line.split()[0])
       
# Extracts number of frequency (Nofreq)
N = nofreq1[0]
Nofreq = N[6:]
 
# Extract Latitude and Longitude 
nlat = lat1[0]         
nlong = long1[0]       
LONG = nlong[8:]
LAT = nlat[7:]

"""
  - Extracting Frequency and Real, Imaginary componets of Impedance Components
    ['FREQ',ZXXRe, ZXXImg, ZXYRe, ZXYImag,ZYXRe,ZYZImag, ZYYRe, ZYYImag] from 
    the EDI(z) file.
"""

Impedance_Components = ['ZXXR','ZXXI','ZXYR','ZXYI',
                        'ZYXR','ZYXI','ZYYR','ZYYI',
                        'FREQ']

for ii in Impedance_Components:
    for i, line in enumerate(EDIFile):    
        if '>{}'.format(ii) in line:
            impstart = i
        elif '>' in line:
            impstop = i
    Z_components1 = []
    Zs = []
         
    for j in range(impstart+1, impstop):
        raw_imp = [x for x in EDIFile[j].split('\n')]
        Z_components1.extend([l for l in raw_imp[0].split()])        
    Zs = Z_components1[:int(Nofreq)] 
    
    Zcomponents = []
    for item in Zs:
       Zcomponents.append(float(item))
       
#---------------- Write Re & Imag. Z and Freq ------------------- 
    
    with open("{}_{}.dat".format(station, ii), 'w') as text_file:    
#         text_file.write("{}\n".format(ii))   
         for j in range(len(Zs)):
             text_file.write('{:9.9s}\n'.format(str(Zcomponents[j])))
             


filenames = ['{}_FREQ.dat'.format(station),'{}_ZXXR.dat'.format(station),
           '{}_ZXXI.dat'.format(station),'{}_ZXYR.dat'.format(station),
           '{}_ZXYI.dat'.format(station),'{}_ZYXR.dat'.format(station),
           '{}_ZYXI.dat'.format(station),'{}_ZYYR.dat'.format(station),
           '{}_ZYYI.dat'.format(station)]
with open('output.txt', 'w') as writer:
    readers = [open(filename) for filename in filenames]
    for lines in zip(*readers):
        print(' '.join([line.strip() for line in lines]), file=writer)
#  ---- Defineing variables to extract frequency and impedance components       
FREQ1 = []; ZXXR1 =[]; ZXXI1=[]; ZXYR1= []; ZXYI1=[]
ZYXR1 = []; ZYXI1 =[]; ZYYR1 = []; ZYYI1= []


for index, line in enumerate(open(r"{}/output.txt".format(name_of_folder))):
    if index > 0:       
        FREQ1.append(line.split()[0])
        ZXXR1.append(line.split()[1])
        ZXXI1.append(line.split()[2])
        ZXYR1.append(line.split()[3])
        ZXYI1.append(line.split()[4])
        ZYXR1.append(line.split()[5])
        ZYXI1.append(line.split()[6])
        ZYYR1.append(line.split()[7])
        ZYYI1.append(line.split()[8])
        
#  ---- converts strings to folats       
ZXXR = list(map(float, ZXXR1))
ZXXI = list(map(float, ZXXI1))
ZXYR = list(map(float, ZXYR1))
ZXYI = list(map(float, ZXYI1))
ZYXR = list(map(float, ZYXR1))
ZYXI = list(map(float, ZYXI1))
ZYYR = list(map(float, ZYYR1))
ZYYI = list(map(float, ZYYI1))
FREQ = list(map(float, FREQ1))
 

"""
   - Calculationg Complex Impedances [ZXXc,ZXYc,ZYXc,ZYYc] from the Real
     and Imaginary componets of Impedance tensor.
             ZXXc = ZXX_Re + ZXX_Imag.j
             ZXYc = ZXY_Re + ZXY_Imag.j
             ZyXc = ZYX_Re + ZYX_Imag.j
             ZXXc = ZYY_Re + ZYY_Imag.j
   - Calculates the Period (1/freq).
   - Calculates the Apparent Resisitvity and Phase using the following formulas.
     
            Phase = arctan{Z.Imag/Z.Re}, (for each component)
            Apparent Res. = 0.2 * Period*|Z,| (for each component)
            DET = 0.2*Period*|ZXXc-ZYYc - ZXYc*ZYX|, (Ranganayaki,1984; Vozoff, 
            1991)
            DET is the determinant mode (rotationally invariant)
""" 

# --- Defineing variables for complex imp. to be calculated
ZXXc = []; ZYYc = []; ZXYc = []; ZYXc = []
# ---- Defineing variables for period to be calculated
period = []
# ---- Defineing variables for resistivity to be calculated
RHOxy = []; RHOyx = []; RHOxx = []; RHOyy = []
phyYX=[]; phyXY = []; phyXX= []; phyYY= []
# ---- Defineing a variable for the derminant mode to be calculated

DET = []

for i in range(len(FREQ)):
    ZXXc.append(complex(ZXXR[i],ZXXI[i]))
    ZXYc.append(complex(ZXYR[i],ZXYI[i]))
    ZYXc.append(complex(ZYXR[i],ZYXI[i]))
    ZYYc.append(complex(ZYYR[i],ZYYI[i]))

    
    phyYX.append(math.degrees(math.atan(ZYXc[i].imag/ZYXc[i].real)))
    phyXY.append(math.degrees(math.atan(ZXYc[i].imag/ZXYc[i].real)))
    phyXX.append(math.degrees(math.atan(ZXXc[i].imag/ZXXc[i].real)))
    phyYY.append(math.degrees(math.atan(ZYYc[i].imag/ZYYc[i].real)))
    
    period.append(1/FREQ[i])
    
    RHOxy.append(0.2*period[i]*abs(ZXYc[i]**2))
    RHOyx.append(0.2*period[i]*abs(ZYXc[i]**2))
    RHOxx.append(0.2*period[i]*abs(ZXXc[i]**2))
    RHOyy.append(0.2*period[i]*abs(ZYYc[i]**2))
    
    DET.append((0.2*abs(ZXXc[i]*ZYYc[i]-ZXYc[i]*ZYXc[i]))/FREQ[i])

"""
 - Plotting Apparent Resisitvity and Phase and save the result in the working
   directory in .JPG format
"""   

plt.style.use('seaborn-white')

#------Plot Apparent resistivity xy,yx-----------------
plt.figure(figsize=(10,10))
plt.subplot(2,1,1)
plt.plot(period,RHOxy,color='blue',marker='o',linestyle =' ',label ='Res_XY')
plt.plot(period,RHOyx,color ='red',marker='o',linestyle =' ',label='Res_YX')
minval=min(min(RHOxy,RHOyx))
maxval=max(max(RHOxy,RHOyx))
plt.ylim([minval/10,maxval*10])
plt.xlim(0.5*min(period),2*max(period))
plt.xscale('log')
plt.yscale('log')
plt.xticks(size=18,weight = 'bold')
plt.yticks(size=18,weight = 'bold')
plt.legend(fontsize = 18,loc = 'best')          
# plt.ylabel(s='App. Res. [$\mathbf{\Omega \cdot m}$]',size=18,weight = 'bold')
plt.grid(which ='minor',axis = 'both',alpha=.5)
plt.title('MT Station {}'.format(station),size=20,weight = 'bold')
 
#---------Plot Phase xy,yx----------------

plt.subplot(2,1,2)
plt.plot(period,phyXY,color='b',marker='s',linestyle = ' ', label = 'Phase_XY')
plt.plot(period,phyYX,color='red',marker='s',linestyle =' ',label = 'Phase_YX')
plt.xscale('log')
plt.xticks(size=15,weight = 'bold')
plt.yticks(size=15,weight = 'bold')
# plt.xlabel(s='Period [s]',size=18,weight = 'bold')          
# plt.ylabel(s='Phase [deg.]',size=18,weight = 'bold')
plt.grid(which ='major',axis = 'both',alpha=.5)
plt.legend(fontsize = 18,loc = 'best')
plt.savefig('{}_APPRES_PHASE.jpg'.format(station))
plt.show()
