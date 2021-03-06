import django
from django.db.models import query
from rest_framework import serializers, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import Patient, Document, Treatment, DocumentBody
from .serializers import PatientSerializer, DocumentSerializer, TreatmentSerializer, DocumentBodySerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    def get_queryset(self):
        queryset = self.queryset
        patient = self.request.query_params.get('patient', None)
        if patient is not None:
            queryset = queryset.filter(patient=patient)
        treatment = self.request.query_params.get('treatment', None)
        if treatment is not None:
            queryset = queryset.filter(treatment=treatment)
        return queryset


class TreatmentViewSet(viewsets.ModelViewSet):
    serializer_class = TreatmentSerializer
    queryset = Treatment.objects.all()

    def get_queryset(self):

        queryset = self.queryset

        patient = self.request.query_params.get('patient', None)
        if patient is not None:
            queryset = queryset.filter(patient=patient)
        return queryset

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        treatment = get_object_or_404(self.queryset, id=kwargs['pk'])
        documents = treatment.document.all()
        print(type(documents))
        response.data['documents'] = DocumentSerializer(
            documents, many=True).data
        return response
