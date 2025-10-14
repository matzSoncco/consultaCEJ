from django.db import models

class Expediente(models.Model):
    distrito_judicial = models.CharField(max_length=100)
    numero_expediente = models.CharField(max_length=50)
    parte = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.numero_expediente} - {self.parte}"
    
class Documento(models.Model):
    expediente = models.ForeignKey(Expediente, related_name = 'documentos', on_delete=models.CASCADE)
    fecha = models.DateField()
    acto_procesal = models.CharField(max_length=200)
    resolucion = models.CharField(max_length=200)
    sumilla = models.CharField(max_length=500)
    archivo_pdf = models.FileField(upload_to='expedientes/pdfs/')

    def __str__(self):
        return f"Documento {self.id} del Expediente {self.expediente.numero_expediente}"