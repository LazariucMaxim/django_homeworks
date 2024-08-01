from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement, DateFilter
from advertisements.permissions import IsCreator
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_fields = ['creator', 'status']
    search_fields = ['description']
    ordering_fields = ['id', 'creator', 'created_at']
    filterset_class = DateFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update"]:
            return [IsAuthenticated(), IsCreator()]
        return []
