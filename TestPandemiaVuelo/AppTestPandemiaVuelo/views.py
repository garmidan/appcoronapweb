from django.shortcuts import render
from AppTestPandemiaVuelo.models import Preguntastes,Tipodocumento,Usuario
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime, timezone

def registrar(request):
    validahora = 0
    listtipodocument = Tipodocumento.objects.all()
    if request.method == 'POST':
        listapreguntas = Preguntastes.objects.all()
        nombres = request.POST["nombres"]
        apellidos = request.POST["apellidos"]
        tipodocumento = request.POST["tipodocumento"]
        numerodocumento = request.POST["numerodocumento"]
        correo = request.POST["correo"]
        celular = request.POST["celular"]
        if Usuario.objects.filter(numerodocumento=numerodocumento).exists():
            existusuario = Usuario.objects.get(numerodocumento=numerodocumento)
            hora_actual = datetime.now()
            fecharegistro = datetime.date(existusuario.fechaprueba)
            horaregistro = datetime.time(existusuario.fechaprueba)
            combinacionfechabase = datetime.combine(fecharegistro,horaregistro)
            total = (hora_actual-combinacionfechabase).total_seconds()
            minutos = total / 60
            horas = minutos / 60
            if horas >=24:
                documento = Tipodocumento(id=tipodocumento)
                guardarusuario = Usuario(tipodocumento=documento,nombres=nombres,apellidos=apellidos
                ,celular=celular,correo=correo,numerodocumento=numerodocumento)
                guardarusuario.save()
                return render(request,"preguntas.html",{"preguntas":listapreguntas,"validahora":validahora})
            else:
                validahora = 1
                return render(request,"registro.html",{"listtipodocumento":listtipodocument,"validahora":validahora})
        else:
            documento = Tipodocumento(id=tipodocumento)
            guardarusuario = Usuario(tipodocumento=documento,nombres=nombres,apellidos=apellidos
            ,celular=celular,correo=correo,numerodocumento=numerodocumento)
            guardarusuario.save()
            return render(request,"preguntas.html",{"preguntas":listapreguntas,"validahora":validahora})
    return render(request,"registro.html",{"listtipodocumento":listtipodocument,"validahora":validahora})

def resultado(request):
    listpreguntas = Preguntastes.objects.all()
    validar = "no puede ver los resultados sin primero registrarse no debe saltearse ningun paso"
    si = 0
    no = 0
    if request.method == 'POST':
        for preguntas in listpreguntas:
            try:
                sipreguntas = request.POST["si"+str(preguntas.id)]
                si = si + 1
            except MultiValueDictKeyError:
                no = no + 1
        obtenerultimoregistro = Usuario.objects.last()        
        if si >=2:
            obtenerultimoregistro.codigoqr = 1
        elif si == 1:
            obtenerultimoregistro.codigoqr = 2
        elif si <= 0:
            obtenerultimoregistro.codigoqr = 3
        obtenerultimoregistro.fechaprueba = datetime.now()   
        nombrescompletos = obtenerultimoregistro.nombres + " " +obtenerultimoregistro.apellidos 
        obtenerultimoregistro.save()
        return render(request,"mostrarresultados.html",{"nombres":nombrescompletos,"codigoqr":obtenerultimoregistro.codigoqr})
    return render(request,"preguntas.html",{"validar":validar})