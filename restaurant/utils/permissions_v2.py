from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """
    Allows access only to the user who created the object.
    Works if every object has the user field.
    """
    def has_object_permission(self, request, view, obj):
        current_user = request.user.id
        if view.action != "retrieve":
            users_objects = view.get_queryset().filter(**{view.user_lookup: current_user})
            return obj in users_objects
        else:
            return True
