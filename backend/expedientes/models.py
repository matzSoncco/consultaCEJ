from django.db import models
from supabase import create_client
from django.conf import settings

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
    archivo_pdf = models.URLField(max_length=500, blank=True, null=True)

    def guardar_pdf_supabase(self, archivo, nombre_archivo):
        supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        
        ruta = f"expediente_{self.expediente.id}/{nombre_archivo}"
        supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
            ruta,
            archivo.read(),
            {"content-type": "application/pdf"}
        )
        
        url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(ruta)
        self.archivo_pdf = url
        self.save()