# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PhaseScan.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

import sys
#import pythoncom
#from win32com import client
import random
import datetime
import time
import matplotlib
#matplotlib.use("Qt5Agg")
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from threading import Thread
from epics import pv
from matplotlib import pyplot as plt
#import socket

#LLRF_HOST='192.168.0.13'
#LLRF_PORT=2000

BUFFER_SIZE = 1024


def moving_average(a, n=35) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = (ret[n:] - ret[:-n])/n
    for i in range(0,n):
        ret[i]=ret[i]/(i+1)
    return ret

def moving_average1(a,N=35):
    vsum=0
    L=len(a)
    temp=np.zeros(L)
    for i in range (0,int(N/2+1)):
        
        vsum= vsum+a[i]
    for i in range(0,int(N/2+1)):
        temp[i]=vsum / int(i+ N/2+1)
        vsum =vsum + a[int(i+N/2+1)]
    for i in range(int(N/2 + 1), int(L-N/2-1) ):
        vsum = vsum- a[int(i-N/2-1)]
        temp[i]=vsum/N
        vsum = vsum + a[int(i+N/2+1)]
    for i in range(int(L-N/2-1),L):
        vsum=vsum-a[int(i-N/2-1)]
        temp[i]=vsum/int(L-i + N/2)
    return temp

def LowestLow(wf,NSPT=600):
    #NSPT: Num of data sample per period
    NS=len(wf)
    NP=int(NS/NSPT)
    Indx=[]
    VL=[]
    for i in range(NP):
        LL=1000
        LB=i*NSPT
        UB=LB+NSPT
        for j in range(LB,UB):
            if wf[j]< LL:
                LL=wf[j]
                ID=j
        Indx.append(ID)
        VL.append(LL)
    LL=1000
    for j in range(UB,NS):
        if wf[j]< LL:
            LL=wf[j]
            ID=j
    if ID-UB >3 and NS-ID > 3:
        Indx.append(ID) 
        VL.append(LL)
    return VL,Indx
    
def HighestHigh(wf,NSPT=600):
    #NSPT: Num of data sample per period
    NS=len(wf)
    NP=int(NS/NSPT)
    Indx=[]
    VH=[]
    for i in range(NP):
        HH=-1000
        LB=i*NSPT
        UB=LB+NSPT
        for j in range(LB,UB):
            if wf[j]> HH:
                HH=wf[j]
                ID=j
        Indx.append(ID)
        VH.append(HH)
    HH=-1000
    for j in range(UB,NS):
        if wf[j]> HH:
            HH=wf[j]
            ID=j
    if ID-UB >3 and NS-ID > 3:
        Indx.append(ID) 
        VH.append(HH)
    return VH,Indx
    
def Trim(v,index,NSPT=600):
    NP=len(v)
    pophead=False
    poptail=False
    if(index[1]-index[0])/NSPT < 0.9:
        pophead=True
    if(index[NP-1]-index[NP-2])/NSPT < 0.9:
        poptail=True
    if poptail == True:        
        v.pop(NP-1)
        index.pop(NP-1)
    if pophead == True:
        v.pop(0)
        index.pop(0)
    return v, index


#global VScope

class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=10, height=3.5, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        # We want the axes cleared every time plot() is called
#        self.axes.hold(False)

        self.compute_initial_figure()

        #
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass
    def SaveFigure(self,filename):
        self.print_jpg(filename);

class MyStaticMplCanvas(MyMplCanvas):
    """Simple canvas with a sine plot."""
    def compute_initial_figure(self):
        t = np.arange(0.0, 3.0, 0.01)
        t = np.arange(120, 140, 1)
        s = np.sin(2*3.1415926*t)*0  # GH modified
        self.axes.plot(t, s)
    def Update_Figure(self):
        l = [random.randint(0, 10) for i in range(4)]
        self.axes.clear()
        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()
    def plotData(self,x1,y1,x2,y2):
        self.axes.clear()
        self.axes.plot(x1,y1,'r.',x2,y2,'b-')
        self.axes.set_ylabel('Charge (nC)')
        self.draw()
    def plotData2(self,x1,y1,x2,y2):
        self.axes.clear()
        self.axes.plot(x1,y1,'r.',x2,y2,'b.')
        self.axes.set_ylabel('V')
        self.draw()
    def plotData1(self,x1,y1):
        self.axes.clear()
        self.axes.plot(x1,y1,'r.')
        self.axes.set_ylabel('AU')
        self.draw()
    def SetYLabel(self,strbuf):
        self.axes.set_ylabel(strbuf)
        self.draw()
    def SetXLabel(self,strbuf):
        self.axes.set_ylabel(strbuf)
        self.draw()
    def plotWaveform(self,x1,y1):
        self.axes.plot(x1,y1,'r.')
        self.draw()
    def Reset(self):
        self.axes.clear()
        

    def ShowImage(self,imdata):
        im=self.axes.imshow(imdata,cmap='plasma',resample=True)
        self.draw()
        

class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""
    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(1000)

    def compute_initial_figure(self):
        self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')

    def update_figure(self):
        # Build a list of 4 random integers between 0 and 10 (both inclusive)
        l = [random.randint(0, 10) for i in range(4)]

        self.axes.plot([0, 1, 2, 3], l, 'r')
        self.draw()
    def plotData(self,x1,y1,x2,y2):
        self.axes.plot(x1,y1,'r.',x2,y2,'b-')
        self.draw()
    def SetYLabel(self,strbuf):
        self.axes.set_ylabel(strbuf)
        self.draw()
    def SetXLabel(self,strbuf):
        self.axes.set_ylabel(strbuf)
        self.draw()
    def plotWaveform(self,x1,y1):
        self.axes.plot(x1,y1,'r.')
        self.draw()
        

#pythoncom.CoInitialize()
UpdateTrigger = pyqtSignal()
StopRequested = 0

   
def Vpp(wf):
    low=1000
    high=-1000
    N=len(wf)
    for i in range(N):
        if high<wf[i]:
            high=wf[i]
        if low > wf[i]:
            low=wf[i]
    return high-low

def PostProc(wf,N,T,P0):
    v=np.zeros(N)
    for i in range(N-1):
        subarray=wf[i*T+P0:(i+1)*T+P0]
#        print(len(subarray))
        v[i]=Vpp(subarray)
    subarray=wf[(i+1)*T+P0:]
    v[i+1]=Vpp(subarray)
    return v



def CalculateCharge(voltsignal):
    ictRiseTime=25e-9
    ictFallTime=100e-9
    signal_time=voltsignal[:,0]
    voltage=-voltsignal[:,1]
    sv=moving_average(voltage,4)
    ipeak=sv.argmax()
    dt=signal_time[1]-signal_time[0]
    npoints=len(voltage)
    lit=int(ipeak-ictRiseTime/dt)
    if(lit<0):
        lit=0
    uit=int(ipeak+ictFallTime/dt)
    if(uit>=npoints):
        uit=npoints-1
    litb=int(ipeak-2*ictRiseTime/dt)
    uitb=int(ipeak-1.1*ictRiseTime/dt)
    if(litb<0):
        litb=0
    if(uitb>=npoints):
        uitb=npoints-1
    voff=voltage[range(litb,uitb)]
    voffmean=voff.mean()
    vict=voltage[range(lit,uit)]-voffmean
    Q=vict.sum()*dt*0.8
    if(np.isnan(Q)):
        Q=0.0
    return Q
    
#def GetScopeData():
#    global VScope    
#    VScope.SingleAcq()
#    VScope.WaitForData(5)
#    volts=np.asarray(VScope.GetData)
#    return volts


class WorkThread(Thread):
    def __init__(self,count):
        Thread.__init__(self)
        self.count=count
    def run(self):
        global StopRequested, ScanIsRunning
        global Initialized
        global ui
        global PhaseStart,PhaseStop,PhaseStep,NumOfSamples,LogLaser
        global PPCmd
   #        pythoncom.CoInitialize()
#        VScope = client.Dispatch(
#            pythoncom.CoGetInterfaceAndReleaseStream(VScope_id, pythoncom.IID_IDispatch))
#        ict=pv.PV("AWAVXI11ICT:Ch3")
        ict=pv.PV("AWAVXI11:Tek1:wf2")
#        RF=pv.PV("AWALLRF:K4:SetPhase")
#        RF=pv.PV("AWALLRF:K5:SetPhase")
        if Initialized == True:
            ScanIsRunning=True
            print(Initialized)
            ui.Reset()
            i=0
            IMax=int((PhaseStop-PhaseStart)/PhaseStep)
            Q=np.zeros(NumOfSamples*IMax) #charge value for each sample point
            Qaverage=np.zeros(IMax) #charge value for each phase
            phase=np.zeros(NumOfSamples*IMax) #phase value for each sample point
            phaverage=np.zeros(IMax) #phase value for each phase
            oldts=ict.timestamp
            while StopRequested == 0:
#            for i in range(0,IMax):
#                PhaseNow=PhaseStart+i*PhaseStep
#                print(PhaseNow)
#                RF.put(PhaseNow)
#                message='w 1 {:f}\n'.format(PhaseNow)
#                tcpip_client.send(message.encode())
#                QSum=0.0
#                vr1=range(0,i)
                oldts=ict.timestamp
                newts=oldts
 #                   VScope.SingleAcq()
 #                   VScope.WaitForData(600)
 #                   print(i,j)
 #                   Volts=np.asarray(VScope.GetData)
                    #Volts=GetScopeData()
                newts=ict.timestamp
                charge=ict.get() 
                while oldts==newts:
                    time.sleep(0.1)
                    newts=ict.timestamp
                    charge=ict.get() 
#                        charge=ict.value
                oldts=newts
                ui.PlotWaveform(charge)
                i=i+1
#                ui.UpdateCounts(f'{i}')
            a=time.localtime()
    #        name1='PhaseScan_rst_{year}_{mon}_{day}_{hour}_{mint}.txt'.format(year=a.tm_year,mon=a.tm_mon,day=a.tm_mday,hour=a.tm_hour,mint=a.tm_min)
    #        name2='PhaseScan_samples_{year}_{mon}_{day}_{hour}_{mint}.txt'.format(year=a.tm_year,mon=a.tm_mon,day=a.tm_mday,hour=a.tm_hour,mint=a.tm_min)
    #        np.savetxt(name1,np.column_stack((phaverage,Qaverage)))
    #        np.savetxt(name2,np.column_stack((phase,Q)))
    #        ui.PlotData(phase,Q,phaverage,Qaverage)
        ScanIsRunning=False
#        VScope.NormalAcq()
        ui.UpdateCounts(f"{i}")
        ui.StopScan()
        return

fnameprefix="FineScan"
NPeriods=3
StartP=0
LPeriod=650
Valley_Val=[]
Valley_Pos=[]
Peak_Val=[]
Peak_Pos=[]
ScannedPhase=[]


class ScanThread(Thread):
    def __init__(self,count):
        Thread.__init__(self)
        self.count=count
    def run(self):
        global StopRequested, ScanIsRunning
        global Initialized
        global ui
        global PhaseStart,PhaseStop,PhaseStep,NumOfSamples,LogLaser
        global PPCmd, NPeriods,StartP,LPeriod,fnameprefix
        global Valley_Pos, Valley_Val, Peak_Pos, Peak_Val, ScannedPhase
   #        pythoncom.CoInitialize()
#        VScope = client.Dispatch(
#            pythoncom.CoGetInterfaceAndReleaseStream(VScope_id, pythoncom.IID_IDispatch))
#        ict=pv.PV("AWAVXI11ICT:Ch3")
        ict=pv.PV("AWAVXI11:Tek1:wf2")
        ictwf=pv.PV("AWAVXI11ICT:wf1")
        xpv=pv.PV("AWAVXI11:Tek1:x")
        RF=pv.PV("AWALLRF:K5:SetPhase")
        data={}
        data["data"]=[]
        data["ts"]=[]
        data['ictwf']=[]
        data["x"]=[]
        data["x"].append(xpv.get())
#        RF=pv.PV("AWALLRF:K5:SetPhase")
        if Initialized == True:
            ScanIsRunning=True
            print(Initialized)
            ui.Reset()
            i=0
            NP=0
            NV=0
            NPOld=0 
            NVOld=0
            IMax=int((PhaseStop-PhaseStart)/PhaseStep)
            Q=np.zeros(NumOfSamples*IMax*NPeriods) #charge value for each sample point
            Qaverage=np.zeros(IMax) #charge value for each phase
            phase=np.zeros(NumOfSamples*IMax*NPeriods) #phase value for each sample point
            phaverage=np.zeros(IMax) #phase value for each phase
            oldts=ict.timestamp
            peak=[]
            peakpos=[]
            valley=[]
            valleypos=[]
            Valley_Val=[]
            Valley_Pos=[]
            Peak_Val=[]
            Peak_Pos=[]
            ScannedPhase=[]
            #walk the PV from current setting to the starting point
            cv=RF.get()
            tv=PhaseStart
            #stepsize need to be chage according to the nature of PV
            ss=1.0 
            N=int((tv-cv)/ss)
            if N<0:
                N=-N
                ss=-ss
            for i in range(N):
                RF.put(cv+i*ss)
                time.sleep(0.5)
                
#            while StopRequested == 0:
            for i in range(0,IMax):
                PhaseNow=PhaseStart+i*PhaseStep
                data["phase"]=PhaseNow
                print(PhaseNow)
                RF.put(PhaseNow)
                IBaseIndx=i*NumOfSamples*NPeriods
#                message='w 1 {:f}\n'.format(PhaseNow)
#                tcpip_client.send(message.encode())
#                QSum=0.0
#                vr1=range(0,i)
                oldts=ict.timestamp
                newts=oldts
 #                   VScope.SingleAcq()
 #                   VScope.WaitForData(600)
 #                   print(i,j)
 #                   Volts=np.asarray(VScope.GetData)
                    #Volts=GetScopeData()
                for j in range(NumOfSamples):
                    newts=ict.timestamp
                    charge=ict.get() 
                    while oldts==newts:
                        time.sleep(0.1)
                        newts=ict.timestamp
                        charge=ict.get() 
#                        charge=ict.value
                    oldts=newts
                    data["ts"].append(oldts)
                    data["data"].append(charge)
                    data['ictwf'].append(ictwf.get())
                    #v=PostProc(charge, NPeriods, LPeriod, StartP)
                    Length=len(charge)
                    wf=moving_average(charge[5:Length-6])
            #        plt.plot(wf)
                    v,indx=HighestHigh(wf)
                    v1,indx1=Trim(v,indx)
                    Peak_Val.append(v1)
                    Peak_Pos.append(indx1)
                    for j1 in range(len(indx1)):
                        peak.append(v1[j1])
                        peakpos.append(indx1[j1])
                    v,indx=LowestLow(wf)
                    v1,indx1=Trim(v,indx)
                    Valley_Val.append(v1)
                    Valley_Pos.append(indx1)
                    ScannedPhase.append(PhaseNow)
                    for j1 in range(len(indx1)):
                       valley.append(v1[j1])
                       valleypos.append(indx1[j1])
#                    NV += len(indx1)
                    
#                    for k in range(NPeriods):
#                        Q[IBaseIndx+j*NPeriods+k]=v[k]
#                        phase[IBaseIndx+j*NPeriods+k]=PhaseNow
#                    vr=range(IBaseIndx+j*NPeriods)
                    
#                    peak=np.reshape(Peak_Val,NP)
#                    peakpos=np.reshape(Peak_Pos, NP)
#                    valley=np.reshape(Valley_Val,NV)
 #                   valleypos=np.reshape(Valley_Pos, NV)
                    ui.PlotData2(valleypos,valley,peakpos,peak)
                    #ui.PlotData1(phase[vr],Q[vr])
                    #ui.PlotWaveform(charge)
                    if StopRequested != 0:
                        break
                if StopRequested != 0:
                    break
                ui.Reset()
                FName=f"{fnameprefix}_{i}.npy"
                np.save(FName,data)
                data["data"]=[]
                data["ts"]=[]
                    #ui.PlotWaveform(charge)
#                ui.UpdateCounts(f'{i}')
            a=time.localtime()
    #        name1='PhaseScan_rst_{year}_{mon}_{day}_{hour}_{mint}.txt'.format(year=a.tm_year,mon=a.tm_mon,day=a.tm_mday,hour=a.tm_hour,mint=a.tm_min)
    #        name2='PhaseScan_samples_{year}_{mon}_{day}_{hour}_{mint}.txt'.format(year=a.tm_year,mon=a.tm_mon,day=a.tm_mday,hour=a.tm_hour,mint=a.tm_min)
    #        np.savetxt(name1,np.column_stack((phaverage,Qaverage)))
    #        np.savetxt(name2,np.column_stack((phase,Q)))
    #        ui.PlotData(phase,Q,phaverage,Qaverage)
        ScanIsRunning=False
#        VScope.NormalAcq()
        print(len(Q))
        result={}
        result['peak']=Peak_Val
        result['peak_pos']=Peak_Pos
        result['valley']=Valley_Val
        result['valley_pos']=Valley_Pos
        result['phase']=ScannedPhase
        name1='{}_{year}_{mon}_{day}_{hour}_{mint}.npy'.format(fnameprefix,year=a.tm_year,mon=a.tm_mon,day=a.tm_mday,hour=a.tm_hour,mint=a.tm_min)
        np.save(name1,result)
        ui.UpdateCounts(f"{len(Q)}")
        ui.StopScan()
        return
 

            
class Ui_Dialog(QObject):
    trigger = pyqtSignal()
    def setupUi(self, Dialog):
        global UpdateTrigger
        Dialog.setObjectName("Dialog")
        Dialog.resize(1258, 498)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 440, 81, 17))
        self.label.setObjectName("label")
        self.LogLaserCheck = QtWidgets.QCheckBox(Dialog)
        self.LogLaserCheck.setGeometry(QtCore.QRect(400, 460, 141, 22))
        self.LogLaserCheck.setObjectName("LogLaserCheck")
        self.InitButton = QtWidgets.QPushButton(Dialog)
        self.InitButton.setGeometry(QtCore.QRect(30, 390, 71, 27))
        self.InitButton.setObjectName("InitButton")
        self.SaveButton = QtWidgets.QPushButton(Dialog)
        self.SaveButton.setGeometry(QtCore.QRect(240, 390, 61, 27))
        self.SaveButton.setObjectName("SaveButton")
#        self.widget = QtWidgets.QWidget(Dialog)
        self.widget = MyStaticMplCanvas(Dialog, width=12, height=3.5, dpi=100)
        self.widget.setGeometry(QtCore.QRect(40, 40, 1180, 341))
        self.widget.setObjectName("widget")
        self.ExitButton = QtWidgets.QPushButton(Dialog)
        self.ExitButton.setGeometry(QtCore.QRect(440, 390, 61, 27))
        self.ExitButton.setObjectName("ExitButton")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(170, 440, 51, 20))
        self.label_2.setObjectName("label_2")
        self.NSamplesEdit = QtWidgets.QLineEdit(Dialog)
        self.NSamplesEdit.setGeometry(QtCore.QRect(530, 430, 51, 27))
        self.NSamplesEdit.setObjectName("NSamplesEdit")
        self.StopPhaseEdit = QtWidgets.QLineEdit(Dialog)
        self.StopPhaseEdit.setGeometry(QtCore.QRect(220, 430, 71, 27))
        self.StopPhaseEdit.setObjectName("StopPhaseEdit")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(450, 440, 81, 17))
        self.label_4.setObjectName("label_4")
        self.StopButton = QtWidgets.QPushButton(Dialog)
        self.StopButton.setGeometry(QtCore.QRect(340, 390, 51, 27))
        self.StopButton.setObjectName("StopButton")
        self.PhaseStepEdit = QtWidgets.QLineEdit(Dialog)
        self.PhaseStepEdit.setGeometry(QtCore.QRect(370, 430, 61, 27))
        self.PhaseStepEdit.setObjectName("PhaseStepEdit")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(300, 440, 64, 17))
        self.label_3.setObjectName("label_3")
        self.PPCmdEdit = QtWidgets.QLineEdit(Dialog)
        self.PPCmdEdit.setGeometry(QtCore.QRect(100, 465, 500, 27))
        self.PPCmdEdit.setObjectName("PPCmdEdit")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(10, 465, 64, 17))
        self.label_4.setObjectName("label_4")
        self.StartButton = QtWidgets.QPushButton(Dialog)
        self.StartButton.setGeometry(QtCore.QRect(140, 390, 61, 27))
        self.StartButton.setObjectName("StartButton")
        self.StartPhaseEdit = QtWidgets.QLineEdit(Dialog)
        self.StartPhaseEdit.setGeometry(QtCore.QRect(90, 430, 71, 27))
        self.StartPhaseEdit.setObjectName("StartPhaseEdit")
        self.retranslateUi(Dialog)
        self.ExitButton.clicked.connect(self.Cleanup)
#        self.trigger.connect(Dialog.close)
        self.trigger.connect(Dialog.close)
        self.InitButton.clicked.connect(self.Initialize)
        self.StartButton.clicked.connect(self.StartScan)
        self.StopButton.clicked.connect(self.StopScan)
        self.SaveButton.clicked.connect(self.SaveFigure)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "AWA Phase Scan"))
        self.label.setText(_translate("Dialog", "Start from:"))
        self.LogLaserCheck.setText(_translate("Dialog", "Log Laser Energy(NotImpl.)"))
        self.InitButton.setText(_translate("Dialog", "Initialize"))
        self.SaveButton.setText(_translate("Dialog", "Save"))
        self.ExitButton.setText(_translate("Dialog", "Exit"))
        self.label_2.setText(_translate("Dialog", "Stop at:"))
        self.label_4.setText(_translate("Dialog", "N. Samples:"))
        self.StopButton.setText(_translate("Dialog", "Stop"))
        self.label_3.setText(_translate("Dialog", "Step size:"))
        self.label_4.setText(_translate("Dialog", "P. Proc. cmds:"))
        self.StartButton.setText(_translate("Dialog", "Start"))
        self.StartPhaseEdit.setText(_translate("Dialog", "0"))
        self.StopPhaseEdit.setText(_translate("Dialog", "360"))
        self.PhaseStepEdit.setText(_translate("Dialog", "10"))
        self.NSamplesEdit.setText(_translate("Dialog", "1"))
        self.StartButton.setDisabled(True)
    @pyqtSlot()    
    def Cleanup(self):
        self.StartPhaseEdit.setText("exit")
        self.trigger.emit()
    @pyqtSlot()    
    def Initialize(self):
        global tcpip_client, LLRF_HOST, LLRF_PORT,Initialized
#        tcpip_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        tcpip_client.connect((LLRF_HOST, LLRF_PORT))
        self.StartButton.setDisabled(False)
        Initialized=True
#        if tcpip_client._closed==True:
#            self.StartButton.setDisabled(True)
#            Initialized=False
    @pyqtSlot()
    def StopScan(self):
        global StopRequested,ScanIsRunning
        StopRequested =1
        while ScanIsRunning==True:
            time.sleep(0.1)
        self.StartButton.setEnabled(True)
        self.ExitButton.setEnabled(True)
    @pyqtSlot()    
    def SaveFigure(self):
        fname="phaseScan"+datetime.datetime.now().strftime("%d%b%Y_%H_%M_%S")+".jpg"
        self.widget.SaveFigure(fname)
    @pyqtSlot()    
    def UpdatePlot(self):
        self.widget.Update_Figure()
    @pyqtSlot()
    def StartScan(self):
        global StopRequested
        global PhaseStart,PhaseStop,PhaseStep,NumOfSamples,LogLaser,VScope_id, VScope
        global PPCmd,NPeriods,StartP,LPeriod,fnameprefix
#        VScope_id = pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, VScope)
        self.StartButton.setDisabled(True)
        self.ExitButton.setDisabled(True)
        StopRequested=0
        buffer=self.StartPhaseEdit.text()
        PhaseStart=float(buffer)
        buffer=self.StopPhaseEdit.text()
        PhaseStop=float(buffer)
        buffer=self.PhaseStepEdit.text()
        PhaseStep=float(buffer)
        buffer=self.NSamplesEdit.text()
        PhaseStop += PhaseStep
        NumOfSamples=int(buffer)
        PPCmd=self.PPCmdEdit.text()
        LogLaser=self.LogLaserCheck.isChecked()
        fnameprefix=self.PPCmdEdit.text()
#        self.th=WorkThread(0)
#        self.th.start()
        self.th=ScanThread(0)
        self.th.start()
    def PlotData(self,x1,y1,x2,y2):
        self.widget.plotData(x1,y1,x2,y2)
    def PlotData1(self,x1,y1):
        self.widget.plotData1(x1,y1)
    def PlotData2(self,x1,y1,x2,y2):
        self.widget.plotData2(x1,y1,x2,y2)
    def PlotWaveform(self,y1):
        x1=range(len(y1))
        self.widget.plotWaveform(x1,y1)
    def UpdateCounts(self,counts):
        #self.NSamplesEdit.setText(counts)
        print(counts)
    def Reset(self):
        self.widget.Reset()
        
if __name__ == "__main__":
    global ui
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    app.exec_()
    del(ui)
    sys.exit(0)


#%%


def moving_average(a, n=35) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = (ret[n:] - ret[:-n])/n
    for i in range(0,n):
        ret[i]=ret[i]/(i+1)
    return ret

def moving_average1(a,N=35):
    vsum=0
    L=len(a)
    temp=np.zeros(L)
    for i in range (0,int(N/2+1)):
        
        vsum= vsum+a[i]
    for i in range(0,int(N/2+1)):
        temp[i]=vsum / int(i+ N/2+1)
        vsum =vsum + a[int(i+N/2+1)]
    for i in range(int(N/2 + 1), int(L-N/2-1) ):
        vsum = vsum- a[int(i-N/2-1)]
        temp[i]=vsum/N
        vsum = vsum + a[int(i+N/2+1)]
    for i in range(int(L-N/2-1),L):
        vsum=vsum-a[int(i-N/2-1)]
        temp[i]=vsum/int(L-i + N/2)
    return temp

def LowestLow(wf,NSPT=600):
    #NSPT: Num of data sample per period
    NS=len(wf)
    NP=int(NS/NSPT)
    Indx=[]
    VL=[]
    for i in range(NP):
        LL=1000
        LB=i*NSPT
        UB=LB+NSPT
        for j in range(LB,UB):
            if wf[j]< LL:
                LL=wf[j]
                ID=j
        Indx.append(ID)
        VL.append(LL)
    LL=1000
    for j in range(UB,NS):
        if wf[j]< LL:
            LL=wf[j]
            ID=j
    if ID-UB >3 and NS-ID > 3:
        Indx.append(ID) 
        VL.append(LL)
    return VL,Indx
    
def HighestHigh(wf,NSPT=600):
    #NSPT: Num of data sample per period
    NS=len(wf)
    NP=int(NS/NSPT)
    Indx=[]
    VH=[]
    for i in range(NP):
        HH=-1000
        LB=i*NSPT
        UB=LB+NSPT
        for j in range(LB,UB):
            if wf[j]> HH:
                HH=wf[j]
                ID=j
        Indx.append(ID)
        VH.append(HH)
    HH=-1000
    for j in range(UB,NS):
        if wf[j]> HH:
            HH=wf[j]
            ID=j
    if ID-UB >3 and NS-ID > 3:
        Indx.append(ID) 
        VH.append(HH)
    return VH,Indx
    
def Trim(v,index,NSPT=600):
    NP=len(v)
    if(index[1]-index[0])/NSPT < 0.9:
        v.pop(0)
        index.pop(0)
    if(index[NP-1]-index[NP-2])/NSPT < 0.9:
        v.pop(NP-1)
        index.pop(NP-1)
    return v, index

def BPDPostP(fname):
    BPD=np.load(fname,allow_pickle=True).item()
    phase=BPD['phase']
    wfm=BPD['data']
    NTrace=len(wfm)
    Peak=[]
    pindx=[]
    Valley=[]
    vindx=[]
    NP=0 
    NV=0 
    for i in range(NTrace):
        wf=moving_average(wfm[i])
#        plt.plot(wf)
        v,indx=HighestHigh(wf)
        v1,indx1=Trim(v,indx)
        Peak.append(v1)
        pindx.append(indx1)
        NP += len(indx1)
        v,indx=LowestLow(wf)
        v1,indx1=Trim(v,indx)
        Valley.append(v1)
        vindx.append(indx1)
        NV += len(indx1)
#    plt.show()
    return Peak, pindx, Valley, vindx, phase 

def BPDPostP_GetValley(fprefix,index,VIndx):
    pos=[]
    val=[]
    ph=[]
    for i in index:
        fname=f'{fprefix}_{i}.npy'
        peak,pindx, valley, vindx, phase=BPDPostP(fname)
        NTrig=len(peak)
        for j in range(NTrig):
            val.append(valley[j][VIndx])
            pos.append(vindx[j][VIndx])
            ph.append(phase)
    return val, pos, ph
        