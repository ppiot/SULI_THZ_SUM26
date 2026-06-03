#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 09:11:05 2025

@author: awa
"""
import numpy as np 
import matplotlib.pylab as plt 
#%%
# July-31-2025 log: 

# studying the impact of wakefield 
fname='fine scan1nCNoBBO-NoSD-WithIrisDipoleOff_rotated45Shifted_2025_8_1_15_27.npy'
#fname='fine scan1nCNoBBO-NoSD-WithIrisDipoleOff_rotated90Shifted_2025_8_1_15_9.npy'
#fname='fine scan1nCNoBBO-NoSD-WithIrisDipoleOff_Shifted_2025_8_1_14_47.npy'
#fname='fine scan1nCNoBBO-NoSD-DipoleOff_Shifted_2025_8_1_14_27.npy'
#fname='fine scan1nCNoBBO-BBO-DipoleOn_Shifted_2025_8_1_14_6.npy'
#fname="FineScan1nCOneBBODipoleOn_Shifted_2025_8_1_11_50.npy"
#fname='quick scan1nCNoBBO-BBO-DipoleOn_Shifted_2025_8_1_13_52.npy'
#fname="quick scan1nCNoBBO-BBO-DipoleOn_Shifted_2025_8_1_13_48.npy"
#fname="FineScan1nCOneBBODipoleOn_Shifted_2025_8_1_11_35.npy"
#fname="FineScan1nCOneBBODipoleOff_Shifted_2025_8_1_11_12.npy"
#fname="FineScan1nCNoBBODipoleOff_Shifted_2025_8_1_10_54.npy"
#fname="FineScan1nCNoBBODipoleOff_2025_8_1_10_40.npy"
#fname="FineScan1nCDipoleOn_2025_8_1_10_14.npy"
#fname="FineScan1nC_2025_8_1_9_46.npy"
#fname="FineScan1nC_2025_8_1_9_34.npy"
# dipole OFF beam on CTR screen
#fname='cosrsescaneQ10nC_wh4_0_dipoleOFF_2025_7_31_17_24.npy'     

# dipole ON beam away from CTR screen
#fname='cosrsescaneQ10nC_wh4_0_dipoleON_2025_7_31_17_14.npy'     

#fine scans:
#10nC whele 5/4     
#fname='finescaneQ10nC_wh4_0_2025_7_31_16_49.npy' 
#7 nC whele 5/4     
#fname='finescaneQ7nC_wh4_2_2025_7_31_16_32.npy' 

#5 nC whele 5/4     
#fname='finescaneQ5nC_wh4_3_2025_7_31_16_18.npy' 
#4 nC whele 5/4
#fname='finescaneQ4nC_wh4_5_2025_7_31_15_57.npy' 
#1 nC whele 5/4     
#fname='finescaneQ1nC_wh5_6_2025_7_31_15_42.npy' 
#500 pC whele 5/4     
#fname='finescaneQ0p5nC_wh5_1_2025_7_31_15_27.npy' 
#250 pC whele 5/4     
#fname='finescaneQ0p25nC_wh5_4_2025_7_31_15_12.npy' 

#long scan.coarse 
#
#350 pC whele at 5|4 0.32%%
#fname='CoarseScan0p5nC_65_1_2025_7_31_14_48.npy' #lost data
#500 pC wheele at 5|1 0.63%
#fname='CoarseScan0p5nC_5_1_2025_7_31_14_55.npy' # redid scan due to file overwrite..
#fname='CoarseScan0p5nC_65_1_2025_7_31_14_40.npy ' #lost data
#1nC 5 | 6 for wheele settings not error in file name 5|6 correspinds to  1%
#fname="CoarseScan1nC_6_6_2025_7_31_14_30.npy"
# 7 nC wheele at 4|2
#fname="CoarseScan7nC_4_2_2025_7_31_14_24.npy"

#10nC at 4|0 
#fname="CoarseScan10nC_4_0_2025_7_31_14_16.npy"
#5nC wheele at 4|3 
#fname="CoarseScan4nC_4_3_2025_7_31_14_11.npy"
#4nC wheele at 4|5
#fname="CoarseScan4nC_4_5_Fiber2_2025_7_31_14_5.npy" # adjusted window
#fname="CoarseScan4nC_4_5_Fiber_2025_7_31_13_59.npy"  # resync and do same scan 

#mess up boudary redoing 
#fname="CoarseScan4nC_4_5_Fiber_2025_7_31_13_59.npy"  # resync and do same scan 
#fname="CoarseScan4nC_4_5_FiberResyncRoughscan_2025_7_31_13_53.npy"  # resync and do same scan 

#fname="CoarseScan4nC_4_5_2025_7_31_13_47.npy"  # data shifted by -7 deg 
#5nC

# fine scan efirst
#fname="FineScan1nC5_6_2025_7_31_13_39.npy"
#fname="FineScan1nC5_6_2025_7_31_13_6.npy"
#fname="FineScan4nC4_5_2025_7_31_13_6.npy"
#fname="FineScan5nC_2025_7_31_12_41.npy"
# scan for 10 nC
#fname="FineScan10nC_2025_7_31_12_11.npy"
#fname="CoarseScan10nCFiberResync_2025_7_31_11_52.npy"
#rstfine=np.load("CoarseScan10nC_2025_7_31_11_40.npy",allow_pickle=True).item()    
# do another jitter (edge)
#rstfine=np.load("jitter_finalEdgelarger_2025_7_31_11_26.npy",allow_pickle=True).item()
# check phase shift 
#rstfine=np.load("scan_576-578_0p05_edge_2025_7_31_11_17.npy",allow_pickle=True).item()
# jitter measurement
# final edge: 
#rstfine=np.load("jitter_finalEdge_2025_7_31_11_11.npy",allow_pickle=True).item()
# zero-crossing: 
#rstfine=np.load("jitter_0Xing_2025_7_31_11_5.npy",allow_pickle=True).item()
# doing a phase scan now (again corase should be "fine")
#rstfine=np.load("scan_coarse_573p8-578_0p025_CTR_2025_7_31_10_46.npy",allow_pickle=True).item()
# deoing a corase scan using the initial internal [565-577] deg w/0.1 deg steps    
#rstfine=np.load("scan_coarse_569-581_0p1_CTR_2025_7_31_10_32.npy",allow_pickle=True).item()
#rstfine=np.load("scan_coarse_565-577_0p1_CTR_2025_7_31_10_24.npy",allow_pickle=True).item()
# below was a FINE scan (note typo in file) but it was done after the laser was resynchonized and the phase shifted 
#rstfine=np.load("scan_coarse_569p5-572_0p025_CTR_2025_7_31_10_9.npy",allow_pickle=True).item()
# CTR out to get a baseline on the wide scan -- want to also recored the signal with CTR in and dipole on but not possible now
#rstfine=np.load("scan_coarse_560-572_0p05_CTRscrnOUT_2025_7_31_9_39.npy",allow_pickle=True).item()
# second scan shifted by 5 deg to capture the full field pattern
#rstfine=np.load("scan_coarse_560-572_0p05_2025_7_31_9_25.npy",allow_pickle=True).item()
# first coearse scan -- curve moved by -5 deg compared to last night 
#rstfine=np.load("scan_coarse_565-577_0p1_2025_7_31_9_6.npy",allow_pickle=True).item()

# 
# quick plot of processed data
####################################################### COPY THIS 
#%%
rstfine=np.load(fname,allow_pickle=True).item()
fpeak2=[]
fpeak1=[]
indx=5
fine_ph=rstfine['phase']
fine_peak=rstfine['peak']

for i in range(len(fine_ph)):
    fpeak2.append(fine_peak[i][indx])
    fpeak1.append(fine_peak[i][indx-1])
plt.plot(fine_ph,fpeak1,'r',fine_ph,fpeak2,'b')
plt.title (fname)
plt.grid()
plt.show()
####################################################### UP TO HERE
#%%
len(fine_ph)
for i in range(len(fine_ph)):
    fpeak2.append(fine_peak[i][indx])
    fpeak1.append(fine_peak[i][indx-1])
len(fpeak1)
fine_ph[0]
(710-350)/0.1
(710-350)/0.1*3

fpeak2=[]
fpeak1=[]
indx=5
fine_ph=rstfine['phase']
fine_peak=rstfine['peak']

for i in range(len(fine_ph)):
    fpeak2.append(fine_peak[i][indx])
    fpeak1.append(fine_peak[i][indx-1])
plt.plot(fine_ph,fpeak1,'r.',fine_ph,fpeak2,'b.')
plt.show()
plt.plot(fine_ph[5000:6000],fpeak1[5000:6000],'r.',fine_ph[5000:6000],fpeak2[5000:6000],'b.')
plt.show()
np.argmax(fpeak1)
plt.plot(fine_ph[6200:7000],fpeak1[6200:7000],'r.',fine_ph[6200:7000],fpeak2[6200:7000],'b.')
plt.show()
plt.plot(fine_ph[6400:7000],fpeak1[6400:7000],'r.',fine_ph[6400:7000],fpeak2[6400:7000],'b.')
plt.show()
rstfine=np.load("FineScan_2025_7_30_19_30.npy",allow_pickle=True).item()
runcell(19, '/home/awa/.config/spyder-py3/AWAPVRecorder.py')
plt.plot(fine_ph,fpeak1,'r.',fine_ph,fpeak2,'b.')
plt.show()
np.argmax(fpeak1)
plt.plot(fine_ph[4000:4500],fpeak1[4000:4500],'r.',fine_ph[4000:4500],fpeak2[4000:4500],'b.')
plt.show()