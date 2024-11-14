from rest_framework.permissions import BasePermission


class IsTheUserWhoCreated(BasePermission):
    """
    Allows access only to the user who created the object.
    Works if every object has the user field.
    """
    def has_permission(self, request, view):
        current = view.get_queryset().filter(pk=view.kwargs.get("pk")).first()
        user_who_created = current.user

        if user_who_created:
            return bool(
                request.user == user_who_created and request.user.is_authenticated
            )
