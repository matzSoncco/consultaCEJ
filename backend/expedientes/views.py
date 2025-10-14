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

        if distrito:
            queryset = queryset.filter(distrito_judicial__icontains=distrito)
        if numero:
            queryset = queryset.filter(numero_expediente__exact=numero)
        if parte:
            queryset = queryset.filter(parte__icontains=parte)

        return queryset

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer