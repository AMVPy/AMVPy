# -*- coding: utf-8 -*-
"""

               edi_extract1.py
                 ----------
 This Program deals with a signle edi file. It extract the impedance
 components from the file (.edi file) and calculates the Apparent resisivity
 and phases for XX, XY, YX and YY. It then plots the result and save it in
 your working directory.
            
            ----------------------------
            import edi_extract1
            Edifn = "A01"
            edi =  edi_extract1.EDI_extract() 
            edi.station = Edifn
            edi.edi_extract()
            edi.res_phase()
            ------------------------------

@author: Biruk A. Cherkose @UAEU
 birukabera39@yahoo.com
"""

import math 
import matplotlib.pyplot as plt

class EDI_extract:
    
    def edi_extract(self):      
        edif = open("{}.edi".format(self.station))
        EDIFile = edif.readlines()  
        
        nofreq1 = []; lat1=[]; long1 = []
        for index, line in enumerate(open("{}.edi".format(self.station))):
            if 'NFREQ=' in line: 
                nofreq1.append(line.split()[0])
            if 'REFLAT=' in line:
                lat1.append(line.split()[0])
            if 'REFLONG=' in line:
                long1.append(line.split()[0])
    
        # Extracts number of frequency (Nofreq)
        N = nofreq1[0]
        Nofreq = N[6:]
        
        Impedance_Components = ['ZXXR','ZXXI','ZXYR','ZXYI','ZYXR','ZYXI','ZYYR','ZYYI','FREQ']
        for ii in Impedance_Components:
            for i, line in enumerate(open("{}.edi".format(self.station))):    
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
            with open("{}_{}.dat".format(self.station, ii), 'w') as text_file:    
  
                for j in range(len(Zs)):
                    text_file.write('{:9.9s}\n'.format(str(Zcomponents[j])))
        filenames = ['{}_FREQ.dat'.format(self.station),'{}_ZXXR.dat'.format(self.station),
                '{}_ZXXI.dat'.format(self.station),'{}_ZXYR.dat'.format(self.station),
                '{}_ZXYI.dat'.format(self.station),'{}_ZYXR.dat'.format(self.station),
                '{}_ZYXI.dat'.format(self.station),'{}_ZYYR.dat'.format(self.station),
                '{}_ZYYI.dat'.format(self.station)]
        with open('{}_output.txt'.format(self.station), 'w') as writer:
            readers = [open(filename) for filename in filenames]
            for lines in zip(*readers):
                print(' '.join([line.strip() for line in lines]), file=writer) 
        edif.close()
        
# Calculates the Apparent resisitvity and phase        
    def res_phase(self):
        open_out = open("{}_output.txt".format(self.station), 'r')
        FREQ1 = []; ZXXR1 =[]; ZXXI1=[]; ZXYR1= []; ZXYI1=[]
        ZYXR1 = []; ZYXI1 =[]; ZYYR1 = []; ZYYI1= []
        for index, line in enumerate(open_out):
            if index >= 0:       
                FREQ1.append(line.split()[0])
                ZXXR1.append(line.split()[1])
                ZXXI1.append(line.split()[2])
                ZXYR1.append(line.split()[3])
                ZXYI1.append(line.split()[4])
                ZYXR1.append(line.split()[5])
                ZYXI1.append(line.split()[6])
                ZYYR1.append(line.split()[7])
                ZYYI1.append(line.split()[8])
        FREQ = [float(i) for i in FREQ1]
        ZXXR = [float(i) for i in ZXXR1]
        ZXXI = [float(i) for i in ZXXI1]
        ZXYR = [float(i) for i in ZXYR1]
        ZXYI = [float(i) for i in ZXYI1]
        ZYXR = [float(i) for i in ZYXR1]
        ZYXI = [float(i) for i in ZYXI1]
        ZYYR = [float(i) for i in ZYYR1]
        ZYYI = [float(i) for i in ZYYI1]

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
        plt.title('MT Station {}'.format(self.station),size=20,weight = 'bold')
         
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
        plt.savefig('{}_APPRES_PHASE.jpg'.format(self.station))
        plt.show()
        
       
