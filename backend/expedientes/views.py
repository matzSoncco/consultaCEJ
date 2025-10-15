from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Expediente, Documento
from .serializers import ExpedienteSerializer, DocumentoSerializer
from rest_framework.response import Response
from supabase import create_client
from django.conf import settings

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
    queryset = Documento.objects.all()
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
            supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            nombre_archivo = f"{documento.id}_{archivo.name}"
            ruta = f"expediente_{documento.expediente.id}/{nombre_archivo}"

            # Subir el archivo
            supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
                ruta,
                archivo.read(),
                {"content-type": "application/pdf"}
            )

            # Obtener URL pública
            url = supabase.storage.from_(settings.SUPABASE_BUCKET).get_public_url(ruta)
            documento.archivo_pdf = url
            documento.save()

        return Response(self.get_serializer(documento).data, status=status.HTTP_201_CREATED)