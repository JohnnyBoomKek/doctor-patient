from django.db import router
from django.urls import include, path
from rest_framework import urlpatterns
from rest_framework.routers import DefaultRouter

from .views import PatientViewSet, TreatmentViewSet, DocumentViewSet

router = DefaultRouter()

router.register('patient', PatientViewSet)
router.register('treatment', TreatmentViewSet)
router.register('document', DocumentViewSet)


urlpatterns = [
    path('', include(router.urls))
]
