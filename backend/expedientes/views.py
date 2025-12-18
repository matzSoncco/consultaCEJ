from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Expediente, Documento
from .serializers import ExpedienteSerializer, DocumentoSerializer
from rest_framework.response import Response
from supabase import create_client
from django.conf import settings
import traceback
import sys

class ExpedienteViewSet(viewsets.ModelViewSet):
    serializer_class = ExpedienteSerializer

    def get_queryset(self):
        queryset = Expediente.objects.all()
        
        distrito = self.request.query_params.get('distrito_judicial')
        numero = self.request.query_params.get('numero_expediente')
        parte = self.request.query_params.get('parte')

        # 🔍 DEBUG: Ver qué llega
        print("=" * 50)
        print(f"Distrito recibido: '{distrito}'")
        print(f"Número recibido: '{numero}'")
        print(f"Parte recibida: '{parte}'")
        
        # 🔍 DEBUG: Ver todos los expedientes en BD
        print("\n📋 Todos los expedientes en BD:")
        for exp in Expediente.objects.all()[:5]:  # Solo los primeros 5
            print(f"  ID: {exp.id}")
            print(f"  Distrito: '{exp.distrito_judicial}'")
            print(f"  Número: '{exp.numero_expediente}'")
            print(f"  Parte: '{exp.parte}'")
            print("-" * 30)

        if distrito:
            queryset = queryset.filter(distrito_judicial__icontains=distrito)
            print(f"Después de filtrar distrito: {queryset.count()} resultados")
        
        if numero:
            print(f"\n🔍 Buscando número exacto: '{numero}'")
            queryset = queryset.filter(numero_expediente__exact=numero)
            print(f"Después de filtrar número: {queryset.count()} resultados")
        
        if parte:
            # Dividir en palabras (esto ignora el tipo de espacio)
            palabras = parte.split()
            for palabra in palabras:
                queryset = queryset.filter(parte__icontains=palabra)
            print(f"Después de filtrar parte: {queryset.count()} resultados")
        
        return queryset

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all().order_by('id')
    serializer_class = DocumentoSerializer

    def create(self, request, *args, **kwargs):
        # Obtener el archivo desde request.FILES
        archivo = request.FILES.get('archivo_pdf')

        # Campos de texto
        data = {
            'expediente': request.data.get('expediente'),
            'fecha': request.data.get('fecha'),
            'acto_procesal': request.data.get('acto_procesal'),
            'resolucion': request.data.get('resolucion'),
            'sumilla': request.data.get('sumilla'),
        }

        # Crear el documento primero
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        documento = serializer.save()

        # Si hay archivo, subimos a Supabase
        if archivo:
            try:
                # LOGS DE DEPURACIÓN PARA RENDER
                print(f"--- Iniciando subida: {archivo.name} ---")
                print(f"Bucket: {settings.SUPABASE_BUCKET}")
                
                supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
                nombre_archivo = f"{documento.id}_{archivo.name}"
                # Asegúrate de que expediente_id no sea None
                exp_id = documento.expediente.id if documento.expediente else "sin_id"
                ruta = f"expediente_{exp_id}/{nombre_archivo}"

                # 1. Leer el contenido del archivo
                contenido = archivo.read()
                
                # 2. Subir a Supabase
                # Usamos response para ver qué dice la API de Supabase
                response = supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
                    path=ruta,
                    file=contenido,
                    file_options={"content-type": archivo.content_type or "application/pdf"}
                )
                
                print(f"Respuesta de Supabase: {response}")

                # 3. Obtener URL pública
                url_res = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(ruta)
                
                # Nota: Dependiendo de la versión de la librería, 
                # get_public_url puede devolver un string o un objeto.
                documento.archivo_pdf = url_res
                documento.save()
                print("--- Subida exitosa ---")

            except Exception as e:
                # ESTO MOSTRARÁ EL ERROR REAL EN LOS LOGS DE RENDER
                print("--- ERROR CRÍTICO EN SUBIDA ---", file=sys.stderr)
                print(f"Tipo de error: {type(e).__name__}", file=sys.stderr)
                print(f"Mensaje: {str(e)}", file=sys.stderr)
                traceback.print_exc() 
                
                # Opcional: Borrar el registro del documento si la subida falló
                # documento.delete() 
                
                return Response(
                    {"error": "Fallo al subir a Supabase", "details": str(e)}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(self.get_serializer(documento).data, status=status.HTTP_201_CREATED)