from rest_framework.permissions import BasePermission


class IsTheUserWhoCreated(BasePermission):
    """
    Allows access only to the user who created the object.
    """
    def __init__(self, view_name):
        self.view_name = view_name
        super().__init__()

    def has_permission(self, request, view):
        current = view.get_queryset().filter(pk=view.kwargs.get("pk")).first()
        user_who_created = None
        match self.view_name:
            case "restaurant":
                if current:
                    user_who_created = current.user
            case "category":
                print(current)
                if current:
                    user_who_created = current.restaurant.user
            case "subcategory":
                if current:
                    user_who_created = current.parent.restaurant.user
            case "dish":
                if current:
                    user_who_created = current.category.parent.restaurant.user
            case "ingredient":
                if current:
                    user_who_created = current.dish.category.parent.restaurant.user
        if user_who_created:
            return bool(
                request.user == user_who_created and request.user.is_authenticated
            )
