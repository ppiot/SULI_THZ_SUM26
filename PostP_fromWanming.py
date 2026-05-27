# -*- coding: utf-8 -*-
"""
Created on Sun Aug 10 14:15:36 2025

@author: wmliu
"""
import numpy as np
from matplotlib import pyplot as plt


def savedata(phase,delay,BPD,Ref,fname):
    N=len(phase)
    file=open(fname,"wt")
    file.write(f"phase (degrees), delay (ns), EO Modulated (V), Un Modulatoed/Reference (V)\n")
    for i in range(N):
        file.write(f"{phase[i]}, {delay[i]}, {BPD[i]}, {Ref[i]}\n")
    file.close()

def PostP(npyfile):
    name=npyfile.split('.')[0]
    CoarseScan=np.load(npyfile, allow_pickle=True).item()
    CoarseScan.keys()
    peak=CoarseScan['peak']
    phase=CoarseScan['phase']
    
    N=len(peak)
    BPD=np.zeros(N)
    Ref=np.zeros(N)
    delay=np.zeros(N)
    tperdegree=1e9/81.25e6/360 
    for i in range(N):
        BPD[i]=peak[i][4]
        Ref[i]=peak[i][3]
        delay[i]=(phase[i]-phase[0])*tperdegree
    plt.plot(delay,BPD,'r-',label="EOModulated")
    plt.plot(delay,Ref,'b-',label="Reference")
    plt.xlabel(xlabel="Delay between lasers (ns)")
    plt.ylabel(ylabel="BPD (V)")    
    plt.legend(loc="upper left")
    plt.show()
    figfile=f"{name}.png"
    plt.savefig(figfile,format='png',dpi=300)
    plt.close()
    savedata(phase,delay,BPD,Ref,f"{name}.csv")
        
#%%
#History
cd /Users/ppiot/Library/CloudStorage/Box-Box/AWA_Data/Data2025/Beamnetus/Aug01/
PostP("FineScan1nCOneBBODipoleOff_Shifted_2025_8_1_11_12.npy")
PostP("FineScan1nCOneBBODipoleOn_Shifted_2025_8_1_11_50.npy")
cd ..
cd /Users/ppiot/Library/CloudStorage/Box-Box/AWA_Data/Data2025/Beamnetus/July30_
PostP("FineScan_2025_7_30_19_30.npy")
PostP("CoarseScan_2025_7_30_18_13.npy).npy")

#%%