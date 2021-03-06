import json
import django
from django.db.models import query
from django.http import response
from rest_framework import serializers, status, viewsets
import rest_framework
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from .models import Patient, Document, Treatment, DocumentBody
from .serializers import PatientSerializer, DocumentSerializer, TreatmentSerializer, DocumentBodySerializer


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    http_method_names = ['get']

    def retrieve(self, request, *args, **kwargs):
        return Response(status=status.HTTP_403_FORBIDDEN) 


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

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        document_id = kwargs['pk']
        document = Document.objects.get(id=document_id)
        try:
            document_body_data = DocumentBodySerializer(document.document_body).data 
            response.data['body'] = document_body_data
        except:
            response.data['body'] = None
        return response

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        document_body = request.POST.get('body')
        created_document = Document.objects.get(id=response.data['id'])
        if document_body is not None:
            DocumentBody.objects.create(
                document=created_document, body=json.loads(document_body))
        return response


class TreatmentViewSet(viewsets.ModelViewSet):
    serializer_class = TreatmentSerializer
    queryset = Treatment.objects.all()
    http_method_names = ['post','get']

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
        response.data['documents'] = DocumentSerializer(
            documents, many=True).data
        return response
