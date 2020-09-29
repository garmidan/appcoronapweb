from django.db import models


class Tipodocumento(models.Model):
    tipodocumento = models.CharField(max_length=30)
    def __str__(self):
        return self.tipodocumento

class Usuario(models.Model):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    celular = models.CharField(max_length=15)
    correo = models.CharField(max_length=30)
    fechaprueba = models.DateTimeField('date published',null=True, blank=True)
    numerodocumento = models.CharField(max_length=15)
    codigoqr = models.CharField(max_length=5)
    tipodocumento = models.ForeignKey(Tipodocumento, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombres

class Preguntastes(models.Model):
    pregunta = models.CharField(max_length=80)
    def __str__(self):
        return self.pregunta
