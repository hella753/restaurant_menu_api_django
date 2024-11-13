from rest_framework.permissions import BasePermission


class IsTheUserWhoCreated(BasePermission):
    """
    Allows access only to the user who created the object.
    """
    def __init__(self, view_name):
        self.view_name = view_name
        super().__init__()

    def has_permission(self, request, view):
        if self.view_name == "restaurant":
            user_who_created = view.get_object().user
        elif self.view_name == "category":
            user_who_created = view.get_object().restaurant.user
        elif self.view_name == "subcategory":
            user_who_created = view.get_object().parent.restaurant.user
        elif self.view_name == "dish":
            user_who_created = (view.get_object()
                                .category
                                .parent
                                .restaurant.user)
        elif self.view_name == "ingredient":
            user_who_created = (view.get_object()
                                .dish.category
                                .parent
                                .restaurant.user)
        return bool(
            request.user == user_who_created and request.user.is_authenticated
        )
