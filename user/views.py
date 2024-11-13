from django.contrib.auth import login
from rest_framework import mixins
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from user.models import User
from user.serializers import RegistrationSerializer


class UserViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  GenericViewSet):
    serializer_class = RegistrationSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action != "create":
            return [IsAuthenticated()]
        else:
            return []

    def perform_create(self, serializer):
        user = serializer.save()
        if user:
            login(self.request, user)
        else:
            return super().perform_create(serializer)
