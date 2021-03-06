from django.db import models
from rest_framework import serializers
from .models import Document, Patient, Treatment, DocumentBody


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Patient


class DocumentBodySerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = DocumentBody

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Document

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Treatment