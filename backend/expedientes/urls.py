from rest_framework.routers import DefaultRouter
from .views import ExpedienteViewSet, DocumentoViewSet

router = DefaultRouter()
router.register(r'expedientes', ExpedienteViewSet, basename='expediente')
router.register(r'documentos', DocumentoViewSet, basename='documento')

urlpatterns = router.urls