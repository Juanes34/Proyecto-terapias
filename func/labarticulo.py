from btk import *
import numpy as np
from numpy.core.fromnumeric import size
from tabulate import tabulate

#tools:
# -*- coding: utf-8 -*-
"""
@autor: Eng. Alexander Sierra, Assistant Professor
"""
from typing import List
import numpy as np
import logging
import btk

global acq
# ----- acquisition -----
def smartReader(filename) -> btk.btkAcquisition:
    """Function to read a c3d file with BTK.

    :param `filename`: path and filename of the c3d
    :type `filename`: str
    :return: btk Acquisition instance
    :rtype: btk.btkAcquisition
    """
    
    reader = btk.btkAcquisitionFileReader()
    reader.SetFilename(filename)
    reader.Update()
    acq = reader.GetOutput()
    return acq


def smartWriter(acq, filename) -> None:
    """Function to write a c3d file with BTK.

    :param `acq`: a btk Acquisition instance
    :type `acq`: btkAcquisition
    :param `filename`: path and filename of the c3d
    :type `filename`: str
    """

    writer = btk.btkAcquisitionFileWriter()
    writer.SetInput(acq)
    writer.SetFilename(str(filename))
    writer.Update()


def getMarkerNames(acq) -> list:
    """Function to show point's label on acquisition.

    :param `acq`: a btk acquisition instance
    :type `acq`: btkAcquisition
    :return `marker_names`: marker names
    :rtype: list
    """

    marker_names = list()
    for it in btk.Iterate(acq.GetPoints()):
        if it.GetType() == btk.btkPoint.Marker and it.GetLabel()[0] != "*":
            marker_names.append(it.GetLabel())
    return marker_names


def isGap(acq, markerLabel) -> bool:
    """ Helper function to check if is there a gap.

    :param `acq`: a btk acquisition instance
    :type `acq`: btkAcquisition
    :param `markerLabel`: marker's label
    :type `markerLabel`: str
    :return `markerLabel`: True if there is a gap on specific marker
    :rtype: bool
    """

    residual_values = acq.GetPoint(markerLabel).GetResiduals()
    if np.any(residual_values == -1.0):
        logging.warning("Gap found for marker (%s)" % markerLabel)
        return True
    else:
        return False


def findMarkerGap(acq) -> list:
    """Function to find markers with Gap in a list of markers.

    :param `acq`: btk acquisition instance
    :type `acq`: btkAcquisition
    :return gaps: list of markers with gaps
    """
    gaps = list()
    markerNames = getMarkerNames(acq)
    for marker in markerNames:
        if isGap(acq, marker):
            gaps.append(marker)
    return gaps


def smartAppendPoint(acq, label, values,
                     pointType=btk.btkPoint.Marker, desc="",
                     residuals=None) -> None:
    """Function to append a point into an acquisition object.

    :param `acq`: (btkAcquisition) btk Acquisition instance
    :param `label`: (str) point's label
    :param `values`: (ndarray(n, 3)) point's values
    :param `pointType`: (enums of btkPoint) type of Point
    :param `residuals`:
    :return: None
    """
    values = np.nan_to_num(values)

    if residuals is None:
        residuals = np.zeros((values.shape[0], 1))
        for i in np.arange(values.shape[0]):
            if np.all(values[i, :] == 0.0):
                residuals[i] = -1.0

    new_btkPoint = btk.btkPoint(label, acq.GetPointFrameNumber())
    new_btkPoint.SetValues(values)
    new_btkPoint.SetDescription(desc)
    new_btkPoint.SetType(pointType)
    new_btkPoint.SetResiduals(residuals)
    acq.AppendPoint(new_btkPoint)


def constructEmptyMarker(acq, label, desc="") -> None:
    """
    Function to build an empty marker.
    :param acq: (btkAcquisition) btk Acquisition instance
    :param label: (str) marker's label
    :param desc: (str) "short description"
    :return: None
    """
    nFrames = acq.GetPointFrameNumber()
    values = np.zeros((nFrames, 3))
    residualValues = np.full((nFrames, 1), -1.0)
    smartAppendPoint(acq, label, values, desc=desc, residuals=residualValues)
    logging.debug("built " + label)


# ----- Angles -----

def getAngleNames(acq) -> list:
    """Function to show angle's label on acquisition.

    :param `acq`: a btk acquisition instance
    :type `acq`: btkAcquisition
    :return `marker_names`: marker names
    :rtype: list
    """

    angle_names = list()
    for it in btk.Iterate(acq.GetPoints()):
        if it.GetType() == btk.btkPoint.Angle:
            angle_names.append(it.GetLabel())
    return angle_names

# ----- Events -----

def _GetEvents(acq):
    """
    Helper function to read and sort the event collection from an acq object
    :param acq: (btkAcquisition)
    :return: (list) List of btkEvent objects
    """
    event_list = [event for event in btk.Iterate(acq.GetEvents())]
    event_list.sort(key=lambda i:i.GetFrame())
    return  event_list

def get_events(acq, context):
    """
    Function to read the event's frame by context
    :param acq: (btkAcquisition) btk Acquisition instance
    :param context: (string) 'Right', 'Left' or 'General'
    :return: (tuple) Foot Strike list and Foot Off list
    """
    footStrike = []
    footOff =  []

    for e in _GetEvents(acq):
        if e.GetContext() == context:
            if e.GetLabel() == 'Foot Strike':
                footStrike.append(e.GetFrame())
            if e.GetLabel() == 'Foot Off':
                footOff.append(e.GetFrame())
    return (footStrike, footOff)
def ini(file):
    acq=smartReader(file)
    point_unit=acq.GetPointUnit()
    point_freq=acq.GetPointFrequency()
    point_num=acq.GetPointNumber()
    n=acq.GetPointFrameNumber()
    marker_names=getMarkerNames(acq)
    return n,marker_names,point_freq,acq
def loc(acq,n,point_freq,heelMarkerName,toeMarkerName,sacralMarkerName):
    xsacr1=acq.GetPoint(sacralMarkerName).GetValues()
    heel=acq.GetPoint(heelMarkerName).GetValues()
    toe=acq.GetPoint(toeMarkerName).GetValues()
    xsacr2=xsacr1[:,0]
    ysacr2=xsacr1[:,1]
    zsacr2=xsacr1[:,2]
    difx=xsacr2[-1]-xsacr2[0]
    dify=ysacr2[-1]-ysacr2[0]
    print(difx,dify)
    if difx > dify:
        xheel=heel[:,0]
    elif dify > difx:
        xheel=heel[:,1]
    xtoe=toe[:,0]
    Xdiff=abs(xsacr2[-1]-xsacr2[0])
    Zdiff=abs(zsacr2[-1]-zsacr2[0])
    Ydiff=abs(ysacr2[-1]-ysacr2[0])
    diff_mm=np.sqrt((Xdiff**2)+(Zdiff**2)+(Ydiff**2))
    time=(len(xsacr2))/point_freq

    vel=diff_mm/time
    Hvelocity=np.ones((int(n),1))
    Fvelocity=np.ones((int(n),1))
    for t in range(0,n-1):
            Hvelocity[t] = np.sqrt(((heel[t+1,0]-
            heel[t,0])**2)+((heel[t+1,2]-heel[t,2])**2)+((heel[t+1,1]-heel[t,1])**2))/(1/point_freq)
            Fvelocity[t] = np.sqrt(((toe[t+1,0]-
            toe[t,0])**2)+((toe[t+1,2]-toe[t,2])**2)+((toe[t+1,1]-toe[t,1])**2))/(1/point_freq)
    vThreshold_FS = 0.78*vel
    vThreshold_FO=0.66*vel
    Fs = []
    Fo = []
    twindow = 10
    for t in range (0,n-1):
        if Fs==[] and Fo==[]:
            temp = []
            if Hvelocity[t] <= vThreshold_FS:
                temp = t
            if temp!=[]:
                Fs.append(temp)
        elif Fs!=[] and Fo!=[] and len(Fs) == len(Fo):
            temp = []
            if Hvelocity[t] <= vThreshold_FS and t >= Fo[-1]+twindow:
                temp = t
            if temp!=[]:
                Fs.append(temp)
        elif Fs!=[] and Fo==[]:
            temp = []
            if Fvelocity[t] >= vThreshold_FO and t >= Fs[-1]+twindow:
                temp = t
            if temp!=[]:
                Fo.append(temp)
        elif Fs!=[] and Fo!=[] and len(Fo) < len(Fs):
            temp = []
            if Fvelocity[t] >= vThreshold_FO and t >= Fs[-1]+twindow:
                temp = t
            if temp!=[]:
                Fo.append(temp)
    return (xheel,Fs,Fo,vel)
def datos(xheelr,xheell,Fsr,For,Fsl,Fol,point_freq):
    zancada=[]
    tapoyo=[]
    tvuelo=[]
    lpasor=[]
    for i in range(0,len(Fsr)-1):
        zan=(xheelr[Fsr[i+1]]-xheelr[Fsr[i]])/10
        zancada.append(round(zan,2))
        tap=(For[i]-Fsr[i])*(1/point_freq)
        tvu=(Fsr[i+1]-For[i])*(1/point_freq)
        tapoyo.append(round(tap,2))
        tvuelo.append(round(tvu,2))
        try:
            if Fsr[0]<Fsl[0]:
                lpas=(xheell[Fsl[i]]-xheelr[Fsr[i]])/10
            else:
                lpas=(xheell[Fsl[i+1]]-xheelr[Fsr[i]])/10
            lpasor.append(round(lpas,2))
        except:
            pass
    pzanr=round(np.mean(zancada),2)
    papoyor=round(np.mean(tapoyo),2)
    pvuelor=round(np.mean(tvuelo),2)
    plpasr=round(np.mean(lpasor),2)
    #tabla=[["Dato 1",Fsr[0],zancada[0],tapoyo[0],tvuelo[0],lpasor[0]],["Dato 2",Fsr[1],zancada[1],tapoyo[1],tvuelo[1],lpasor[1]],["Dato 3",Fsr[2],zancada[2],tapoyo[2],tvuelo[2],lpasor[2]]
    #,["Dato 4",Fsr[3],"---","---","---","---"],["Promedio","---",pzanr,papoyor,pvuelor,plpasr]]
    #print(tabulate(tabla,headers=['Pie derecho',"Contactos iniciales","Zancada","Tiempo de apoyo","Tiempo de vuelo","Longitud de paso"]))
    #print('-'*85)
    zancada=[]
    tapoyo=[]
    tvuelo=[]
    lpasol=[]
    for i in range(0,len(Fsl)-1):
        zan=(xheell[Fsl[i+1]]-xheell[Fsl[i]])/10
        zancada.append(round(zan,2))
        tap=(Fol[i]-Fsl[i])*(1/point_freq)
        tvu=(Fsl[i+1]-Fol[i])*(1/point_freq)
        tapoyo.append(round(tap,2))
        tvuelo.append(round(tvu,2))
        try:
            if Fsl[0]<Fsr[0]:
                lpas=(xheelr[Fsr[i]]-xheell[Fsl[i]])/10
            else:
                lpas=(xheelr[Fsr[i+1]]-xheell[Fsl[i]])/10
            lpasol.append(round(lpas,2))
        except:
            pass
    pzanl=round(np.mean(zancada),2)
    papoyol=round(np.mean(tapoyo),2)
    pvuelol=round(np.mean(tvuelo),2)
    plpasl=round(np.mean(lpasol),2)
    #tabla=[["Dato 1",Fsl[0],zancada[0],tapoyo[0],tvuelo[0],lpasol[0]],["Dato 2",Fsl[1],zancada[1],tapoyo[1],tvuelo[1],lpasol[1]],["Dato 3",Fsl[2],zancada[2],tapoyo[2],tvuelo[2],lpasol[2]]
    #,["Dato 4",Fsl[3],"---","---","---","---"],["Promedio","---",pzanl,papoyol,pvuelol,plpasl]]
    #print(tabulate(tabla,headers=['Pie izquierdo',"Contactos iniciales","Zancada","Tiempo de apoyo","Tiempo de vuelo","Longitud de paso"]))
    #print('-'*85)
    print(Fsr)
    print(For)
    print(Fsl)
    print(Fol)
    return pzanr,papoyor,pvuelor,plpasr,pzanl,papoyol,pvuelol,plpasl

def mainfunc(file):
    n,marker_names,point_freq,acp=ini(file)
    try:
        xheell,Fsl,Fol,vel=loc(acp,n,point_freq,heelMarkerName='LHEE',toeMarkerName='LTOE',sacralMarkerName='SACR')
        xheelr,Fsr,For,vel=loc(acp,n,point_freq,heelMarkerName='RHEE',toeMarkerName='RTOE',sacralMarkerName='SACR')
    except:
        xheell,Fsl,Fol,vel=loc(acp,n,point_freq,heelMarkerName='LHEE',toeMarkerName='LTOE',sacralMarkerName='RPSI')
        xheelr,Fsr,For,vel=loc(acp,n,point_freq,heelMarkerName='RHEE',toeMarkerName='RTOE',sacralMarkerName='RPSI')
    if Fsr[0]==0:
        Fsr.pop(0)
    if For[0]<Fsr[0]:
        For.pop(0)
    if For[-1]>Fsr[-1]:
        For.pop(-1)
    if Fsl[0]==0:
        Fsl.pop(0)
    if Fol[0]<Fsl[0]:
        Fol.pop(0)
    if Fol[-1]>Fsl[-1]:
        Fol.pop(-1)
    pzanr,papoyor,pvuelor,plpasr,pzanl,papoyol,pvuelol,plpasl=datos(xheelr,xheell,Fsr,For,Fsl,Fol,point_freq)
    vel=np.round((vel/1000),2)
    return pzanr,papoyor,pvuelor,plpasr,pzanl,papoyol,pvuelol,plpasl,vel
