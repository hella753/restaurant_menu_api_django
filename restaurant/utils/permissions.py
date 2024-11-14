from rest_framework.permissions import BasePermission


class IsTheUserWhoCreated(BasePermission):
    """
    Allows access only to the user who created the object.
    """
    def __init__(self, view_name):
        self.view_name = view_name
        super().__init__()

    def has_permission(self, request, view):
        current = view.get_object()
        match self.view_name:
            case "restaurant":
                user_who_created = current.user
            case "category":
                user_who_created = current.restaurant.user
            case "subcategory":
                user_who_created = current.parent.restaurant.user
            case "dish":
                user_who_created = current.category.parent.restaurant.user
            case "ingredient":
                user_who_created = current.dish.category.parent.restaurant.user
        return bool(
            request.user == user_who_created and request.user.is_authenticated
        )
