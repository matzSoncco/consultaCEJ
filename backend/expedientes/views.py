from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Expediente, Documento
from .serializers import ExpedienteSerializer, DocumentoSerializer

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