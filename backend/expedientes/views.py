from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Expediente, Documento
from .serializers import ExpedienteSerializer, DocumentoSerializer

class ExpedienteViewSet(viewsets.ModelViewSet):
    queryset = Expediente.objects.all()
    serializer_class = ExpedienteSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['numero_expediente', 'parte', 'distrito_judicial']

class DocumentoViewSet(viewsets.ModelViewSet):
    queryset = Documento.objects.all()
    serializer_class = DocumentoSerializer