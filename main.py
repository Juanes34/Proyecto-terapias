from types import MethodType
from xml.dom.minidom import Document
from flask import Flask, render_template,request,send_from_directory
from flask.wrappers import Request
import sys
from typing import List
import numpy as np
import logging
import btk
from pathlib import Path

sys.path.append('C:/Users/usuario/OneDrive/Escritorio/Python/biom/Reto/func')
ruta=Path("/Users/usuario/OneDrive/Escritorio/PYTHON/BIOM/Reto/bd/")
from func.labarticulo import *

UPLOAD_FOLDER = '/Users/usuario/OneDrive/Escritorio/PYTHON'
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
global usuario,genero,edad,caidas
@app.route('/')
def ingreso():
    return render_template('inicio.html')

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/login')
def inicio():
    return render_template('login.html')

@app.route('/menu',methods=['POST'])
def menu():
    if request.method=="POST":
        global usuario
        usuario=request.form['usuario']
        password=request.form['password']
        resultado=verificar(usuario,password)
        if resultado==True:
            return render_template("menu.html")
        else:
            return render_template("login2.html")

@app.route('/menu2')
def menu2():
    return render_template("menu.html")

@app.route('/menu3')
def menu3():
    global nt,num
    nt=int(nt)
    nt-=1
    vari=usuario+'t.csv'
    ruta_con_variable = ruta.joinpath(vari)
    fileterapia=open(ruta_con_variable,"a")
    t=str(num)+';'+str(nt)+'\n'
    fileterapia.write(t)
    fileterapia.close()
    if nt!=0:
        return render_template("menu.html")

@app.route('/regis',methods=['POST'])
def guardar_usuario():
    if request.method=="POST":
        global usuario
        usuario=request.form['usuario']
        password=request.form['password']
        resultado=verificar(usuario,password)
        if resultado==True:
            return render_template("registro2.html")
        else:
            savefile(usuario,password)
            return render_template('bienvenida.html')

@app.route('/resultado',methods=['POST'])
def resultado():
    if request.method=="POST":
        global genero,edad,pzanr,papoyor,pvuelor,plpasr,pzanl,papoyol,pvuelol,plpasl,vel,nombre,caidas
        vela=vel
        vel=round(vel*100,2)
        genero=int(request.form['uno'])
        if genero==1:
            genero2='Mujer'
        elif genero==0:
            genero2='Hombre'
        edad=int(request.form['dos'])
        if edad==1:
            edad2='Menor a 65'
        elif edad==2:
            edad2='65-69'
        elif edad==3:
            edad2='70-74'
        elif edad==4:
            edad2='75-79'
        elif edad==5:
            edad2='Mayor a 80'
        saveestado(pzanr,pzanl,vel,str(genero2),str(edad2),str(caidas))
        return render_template('resultado.html',uno=nombre,pzanr=pzanr,papoyor=papoyor,pvuelor=pvuelor,plpasr=plpasr
        ,pzanl=pzanl,papoyol=papoyol,pvuelol=pvuelol,plpasl=plpasl,vel=vela,genero=genero2,edad=edad2,caidas=caidas)

@app.route('/resultado1',methods=['POST'])
def resultado1():
    if request.method=="POST":
        global zanr,zanl,caidas2,vel2,genero21,edad21
        velb=round(vel2/100,2)
        genero21=int(request.form['uno'])
        if genero21==1:
            genero22='Mujer'
        elif genero21==0:
            genero22='Hombre'
        edad21=int(request.form['dos'])
        if edad21==1:
            edad22='Menor a 65'
        elif edad21==2:
            edad22='65-69'
        elif edad21==3:
            edad22='70-74'
        elif edad21==4:
            edad22='75-79'
        elif edad21==5:
            edad22='Mayor a 80'
        saveestado(zanr,zanl,vel2,str(genero22),str(edad22),str(caidas2))
        return render_template('resultado1.html',zanr=zanr,zanl=zanl,vel2=velb,genero22=genero22,edad22=edad22,caidas2=caidas2)

@app.route('/pruebaca',methods=['POST'])
def pruebaca():
    if request.method=="POST":
        global pzanr,papoyor,pvuelor,plpasr,pzanl,papoyol,pvuelol,plpasl,vel,nombre
        archivo=request.files['archivo']
        nombre=archivo.filename
        archivo.save(nombre)
        pzanr,papoyor,pvuelor,plpasr,pzanl,papoyol,pvuelol,plpasl,vel=mainfunc(nombre)
        return render_template('pruebaca.html')

@app.route('/pruebaca2',methods=['POST'])
def pruebaca2():
    if request.method=="POST":
        global vel2
        t=int(request.form['tiempo'])
        d=int(request.form['distancia'])
        vel2=round(d/t,2)
        return render_template('pruebaca2.html')

@app.route('/recomen11')
def recomen11():
    global zanr,zanl,caidas2,vel2,genero21,edad21
    if genero21 == 0:
        if zanl  <112 or zanr < 112:
            pasos = 1
        else:
            pasos = 0
        if edad21 == 1:
            if vel2 < 128:
                velocidad = 1
            else:
                velocidad = 0
            if caidas2 < 14:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad21 == 2:
            if vel2 < 125:
                velocidad = 1
            else:
                velocidad = 0
            if caidas2 < 12:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad21 == 3:
            if vel2 < 120:
                velocidad = 1
            else:
                velocidad = 0
            if caidas2 < 12:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad21 == 4:
            if vel2 < 117:
                velocidad = 1
            else:
                velocidad = 0
            if caidas2 < 11:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad21 == 5:
            if vel2 < 100:
                velocidad = 1
            else:
                velocidad = 0
            if caidas2 < 10:
                equilibrio = 1
            else:
                equilibrio = 0
    else:
        if zanl  <99 or zanr < 99:
            pasos = 1
        else:
            pasos = 0
        if edad21 == 1:
            if vel2 < 120:
                velocidad = 1
            else:
                velocidad = 0
            if caidas2 < 12:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad21 == 2:
            if vel2 < 118:
                velocidad = 1
            else:
                velocidad = 0
            if caidas2 < 11:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad21 == 3:
            if vel2 < 116:
                velocidad = 1
            else:
                velocidad = 0
            if caidas2 < 10:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad21 == 4:
            if vel2 < 112:
                velocidad = 1
            else:
                velocidad = 0
            if caidas2 < 10:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad21 == 5:
            if vel2 < 99:
                velocidad = 1
            else:
                velocidad = 0
            if caidas2 < 9:
                equilibrio = 1
            else:
                equilibrio = 0
    if equilibrio==1 and velocidad==0 and pasos==0:
        return render_template('recomen1.html')
    elif equilibrio==0 and velocidad==0 and pasos==1:
        return render_template('recomen2.html')
    elif equilibrio==0 and velocidad==1 and pasos==0:
        return render_template('recomen3.html')
    elif equilibrio==1 and velocidad==0 and pasos==1:
        return render_template('recomen4.html')
    elif equilibrio==1 and velocidad==1 and pasos==0:
        return render_template('recomen5.html')
    elif equilibrio==0 and velocidad==1 and pasos==1:
        return render_template('recomen6.html')
    else:
        return render_template('recomen7.html')

@app.route('/recomen')
def recomen():
    global genero,edad,pzanr,pzanl,vel,caidas
    if genero == 0:
        if pzanl  <112 or pzanr < 112:
            pasos = 1
        else:
            pasos = 0
        if edad == 1:
            if vel < 128:
                velocidad = 1
            else:
                velocidad = 0
            if caidas < 14:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad == 2:
            if vel < 125:
                velocidad = 1
            else:
                velocidad = 0
            if caidas < 12:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad == 3:
            if vel < 120:
                velocidad = 1
            else:
                velocidad = 0
            if caidas < 12:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad == 4:
            if vel < 117:
                velocidad = 1
            else:
                velocidad = 0
            if caidas < 11:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad == 5:
            if vel < 100:
                velocidad = 1
            else:
                velocidad = 0
            if caidas < 10:
                equilibrio = 1
            else:
                equilibrio = 0
    else:
        if pzanl  <99 or pzanr < 99:
            pasos = 1
        else:
            pasos = 0
        if edad == 1:
            if vel < 120:
                velocidad = 1
            else:
                velocidad = 0
            if caidas < 12:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad == 2:
            if vel < 118:
                velocidad = 1
            else:
                velocidad = 0
            if caidas < 11:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad == 3:
            if vel < 116:
                velocidad = 1
            else:
                velocidad = 0
            if caidas < 10:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad == 4:
            if vel < 112:
                velocidad = 1
            else:
                velocidad = 0
            if caidas < 10:
                equilibrio = 1
            else:
                equilibrio = 0
        elif edad == 5:
            if vel < 99:
                velocidad = 1
            else:
                velocidad = 0
            if caidas < 9:
                equilibrio = 1
            else:
                equilibrio = 0
    if equilibrio==1 and velocidad==0 and pasos==0:
        return render_template('recomen1.html')
    elif equilibrio==0 and velocidad==0 and pasos==1:
        return render_template('recomen2.html')
    elif equilibrio==0 and velocidad==1 and pasos==0:
        return render_template('recomen3.html')
    elif equilibrio==1 and velocidad==0 and pasos==1:
        return render_template('recomen4.html')
    elif equilibrio==1 and velocidad==1 and pasos==0:
        return render_template('recomen5.html')
    elif equilibrio==0 and velocidad==1 and pasos==1:
        return render_template('recomen6.html')
    else:
        return render_template('recomen7.html')

@app.route('/primera')
def primera():
    return render_template("primera.html")

@app.route('/eleceval')
def eleceval():
    return render_template("eleceval.html")

@app.route('/eval')
def eval():
    return render_template("eval.html")

@app.route('/hist')
def hist():
    global cont2
    cont2=0
    estados=[]
    estados=loadestados()
    maximo=len(estados)
    return render_template("hist.html",maximo=maximo)

@app.route('/hist2',methods=['POST'])
def hist2():
    if request.method=="POST":
        global cont2
        elec=int(request.form['eleccion'])
        estados=[]
        estados=loadestados()
        maximo=len(estados)
        estado=estados[elec-1]
        estado=estado.split(";")
        zand=estado[0]
        zani=estado[1]
        v=estado[2]
        g=estado[3]
        a=estado[4]
        f=estado[5]
        return render_template('hist2.html',zani=zani,zand=zand,v=v,g=g,a=a,f=f,elec=str(elec))

@app.route('/estado')
def estado():
    try:
        ter,num=loadterapia()
        sesion=int(num)
        sesion=str(sesion)
    except:
        ter="No ha seleccionado una terapia"
        sesion="No ha seleccionado una terapia"
    
    zaniz,zander,speed,gender,age,fall=loadestado()
    return render_template("estado.html",terapia=ter,sesion=sesion,zaniz=zaniz,zander=zander,speed=speed,gender=gender,age=age,fall=fall,usuario=usuario)

@app.route('/terapia')
def terapia():
    return render_template("terapia.html")

@app.route('/terapia1')
def terapia1():
    saveterapia(1)
    global nt,num
    num,nt=loadterapia()
    sesion=11-int(nt)
    sesion=str(sesion)
    return render_template("terapia1_1.html",sesion=sesion)

@app.route('/terapia1_2')
def terapia1_2():
    return render_template("terapia1_2.html")

@app.route('/terapia1_3')
def terapia1_3():
    return render_template("terapia1_3.html")

@app.route('/terapia1_4')
def terapia1_4():
    return render_template("terapia1_4.html")

@app.route('/terapia2')
def terapia2():
    saveterapia(2)
    global nt,num
    num,nt=loadterapia()
    sesion=11-int(nt)
    sesion=str(sesion)
    return render_template("terapia2_1.html",sesion=sesion)

@app.route('/terapia2_2')
def terapia2_2():
    return render_template("terapia2_2.html")

@app.route('/terapia2_3')
def terapia2_3():
    return render_template("terapia2_3.html")

@app.route('/terapia2_4')
def terapia2_4():
    return render_template("terapia2_4.html")

@app.route('/terapia2_5')
def terapia2_5():
    return render_template("terapia2_5.html")

@app.route('/terapia2_6')
def terapia2_6():
    return render_template("terapia2_6.html")

@app.route('/terapia3')
def terapia3():
    saveterapia(3)
    global nt,num
    num,nt=loadterapia()
    sesion=11-int(nt)
    sesion=str(sesion)
    return render_template("terapia3_1.html",sesion=sesion)

@app.route('/terapia3_2')
def terapia3_2():
    return render_template("terapia3_2.html")

@app.route('/terapia3_3')
def terapia3_3():
    return render_template("terapia3_3.html")

@app.route('/terapia3_4')
def terapia3_4():
    return render_template("terapia3_4.html")

@app.route('/terapia3_5')
def terapia3_5():
    return render_template("terapia3_5.html")

@app.route('/terapia3_6')
def terapia3_6():
    return render_template("terapia3_6.html")

@app.route('/terapia4')
def terapia4():
    saveterapia(4)
    global nt,num
    num,nt=loadterapia()
    sesion=11-int(nt)
    sesion=str(sesion)
    return render_template("terapia4_1.html",sesion=sesion)

@app.route('/terapia4_2')
def terapia4_2():
    return render_template("terapia4_2.html")

@app.route('/terapia4_3')
def terapia4_3():
    return render_template("terapia4_3.html")

@app.route('/terapia4_4')
def terapia4_4():
    return render_template("terapia4_4.html")

@app.route('/terapia4_5')
def terapia4_5():
    return render_template("terapia4_5.html")

@app.route('/terapia4_6')
def terapia4_6():
    return render_template("terapia4_6.html")

@app.route('/terapia5')
def terapia5():
    saveterapia(5)
    global nt,num
    num,nt=loadterapia()
    sesion=11-int(nt)
    sesion=str(sesion)
    return render_template("terapia5_1.html",sesion=sesion)

@app.route('/terapia5_2')
def terapia5_2():
    return render_template("terapia5_2.html")

@app.route('/terapia5_3')
def terapia5_3():
    return render_template("terapia5_3.html")

@app.route('/terapia5_4')
def terapia5_4():
    return render_template("terapia5_4.html")

@app.route('/terapia5_5')
def terapia5_5():
    return render_template("terapia5_5.html")

@app.route('/terapia6')
def terapia6():
    saveterapia(6)
    global nt,num
    num,nt=loadterapia()
    sesion=11-int(nt)
    sesion=str(sesion)
    return render_template("terapia6_1.html",sesion=sesion)

@app.route('/terapia6_2')
def terapia6_2():
    return render_template("terapia6_2.html")

@app.route('/terapia6_3')
def terapia6_3():
    return render_template("terapia6_3.html")

@app.route('/terapia6_4')
def terapia6_4():
    return render_template("terapia6_4.html")

@app.route('/terapia6_5')
def terapia6_5():
    return render_template("terapia6_5.html")

@app.route('/terapia6_6')
def terapia6_6():
    return render_template("terapia6_6.html")

@app.route('/terapia7')
def terapia7():
    saveterapia(7)
    global nt,num
    num,nt=loadterapia()
    sesion=11-int(nt)
    sesion=str(sesion)
    return render_template("terapia7_1.html",sesion=sesion)

@app.route('/terapia7_2')
def terapia7_2():
    return render_template("terapia7_2.html")

@app.route('/terapia7_3')
def terapia7_3():
    return render_template("terapia7_3.html")

@app.route('/terapia7_4')
def terapia7_4():
    return render_template("terapia7_4.html")

@app.route('/terapia7_5')
def terapia7_5():
    return render_template("terapia7_5.html")

@app.route('/terapia7_6')
def terapia7_6():
    return render_template("terapia7_6.html")

@app.route('/terapia7_7')
def terapia7_7():
    return render_template("terapia7_7.html")

@app.route('/terapiaactual')
def terapiaactual():
    global nt,num
    num,nt=loadterapia()
    num=str(num)
    sesion=11-int(nt)
    sesion=str(sesion)
    if num=='1':
        return render_template('terapia1_1.html',sesion=sesion)
    elif num=='2':
        return render_template('terapia2_1.html',sesion=sesion)
    elif num=='3':
        return render_template('terapia3_1.html',sesion=sesion)
    elif num=='4':
        return render_template('terapia4_1.html',sesion=sesion)
    elif num=='5':
        return render_template('terapia5_1.html',sesion=sesion)
    elif num=='6':
        return render_template('terapia6_1.html',sesion=sesion)
    elif num=='7':
        return render_template('terapia7_1.html',sesion=sesion)

@app.route('/electerapia')
def electerapia():
    return render_template("electerapia.html")

@app.route('/terapiainicial')
def terapiainicial():
    return render_template("terapiainicial.html")

@app.route('/encuesta',methods=['POST'])
def encuesta():
    if request.method=="POST":
        global caidas
        caidas=int(request.form['caidas'])
    return render_template("encuesta.html")

@app.route('/encuesta2',methods=['POST'])
def encuesta2():
    if request.method=="POST":
        global caidas2
        caidas2=int(request.form['caidas2'])
    return render_template("encuesta2.html")

@app.route('/pruebatalco')
def pruebatalco():
    return render_template("pruebatalco.html")

@app.route('/pruebavel',methods=['POST'])
def pruebavel():
    if request.method=="POST":
        global zanr,zanl
        zanr=int(request.form['zanr'])
        zanl=int(request.form['zanl'])
    return render_template("pruebavel.html")

@app.route('/confirmar')
def confirmar():
    return render_template("confirmar.html")

@app.route('/conf1')
def conf1():
    return render_template("conf1.html")

@app.route('/conf2')
def conf2():
    return render_template("conf2.html")

def verificar(usuario, password):
    cuentas=loadfromusers()
    cuent=False
    passw=False
    for a in cuentas:
        if usuario==a[0]:
            cuent=True
        if password==a[1]:
            passw=True
    if cuent==False:
        return False
    elif cuent==True and passw==False:
        return False
    elif cuent==True and passw==True:
        return True

def loadfromusers():
    users=[]
    total=[]
    fileusers=open("/Users/usuario/OneDrive/Escritorio/PYTHON/BIOM/Reto/bd/usuarios.csv","r")
    datos=fileusers.readlines()
    fileusers.close()
    for d in datos:
        users=[]
        d=d.replace("\n","")
        datos=d.split(";")
        usuario=datos[0]
        contraseña=datos[1]
        users.append(usuario)
        users.append(contraseña)
        total.append(users)
    return total

def savefile(usuario,password):
    fileusers=open("/Users/usuario/OneDrive/Escritorio/PYTHON/BIOM/Reto/bd/usuarios.csv","a")
    cuenta=usuario+';'+password+'\n'
    fileusers.write(cuenta)
    fileusers.close()

def loadterapia():
    vari=usuario+'t.csv'
    ruta_con_variable = ruta.joinpath(vari)
    file=open(ruta_con_variable,"r")
    datos=file.readlines()
    file.close()
    for d in datos:
        d=d.replace("\n","")
        datos=d.split(";")
        terapia=datos[0]
        nt=datos[1]
    return terapia,nt

def saveterapia(num):
    vari=usuario+'t.csv'
    ruta_con_variable = ruta.joinpath(vari)
    try:
        fileterapia=open(ruta_con_variable,"a")
        t=str(num)+';'+'10'+'\n'
        fileterapia.write(t)
        fileterapia.close()
    except:
        fileterapia=open(ruta_con_variable,"w")
        t=str(num)+'\n'
        fileterapia.write(t)
        fileterapia.close()
    
def loadestado():
    vari=usuario+'e.csv'
    ruta_con_variable = ruta.joinpath(vari)
    file=open(ruta_con_variable,"r")
    datos=file.readlines()
    file.close()
    estados=[]
    for d in datos:
        d=d.replace("\n","")
        datos=d.split(";")
        zander=datos[0]
        zaniz=datos[1]
        speed=datos[2]
        gender=datos[3]
        age=datos[4]
        fall=datos[5]
    return zaniz,zander,speed,gender,age,fall

def loadestados():
    vari=usuario+'e.csv'
    ruta_con_variable = ruta.joinpath(vari)
    file=open(ruta_con_variable,"r")
    datos=file.readlines()
    file.close()
    estados=[]
    for d in datos:
        d=d.replace("\n","")
        estados.append(d)
    return estados

def saveestado(pzanr,pzanl,vel,genero,edad,caidas):
    global usuario
    vari=usuario+'e.csv'
    ruta_con_variable = ruta.joinpath(vari)
    try:
        fileestado=open(ruta_con_variable,"a")
        t=str(pzanr)+';'+str(pzanl)+';'+str(vel)+';'+str(genero)+';'+str(edad)+';'+str(caidas)+';'+'\n'
        fileestado.write(t)
        fileestado.close()
    except:
        fileestado=open(ruta_con_variable,"w")
        t=str(pzanr)+';'+str(pzanl)+';'+str(vel)+';'+str(genero)+';'+str(edad)+';'+str(caidas)+';'+'\n'
        fileestado.write(t)
        fileestado.close()

if __name__=="__main__":
    app.run(debug=True)