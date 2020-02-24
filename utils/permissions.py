from rest_framework.permissions import BasePermission, SAFE_METHODS


class ReadOnly(BasePermission):
    """Allow ReadOnly permissions if the request is a safe method"""
    
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.role == 'BY'
        )


class CanEditUsers(BasePermission):
    """Client admins should be able to edit accounts they own"""

    def has_object_permission(self, request, view, obj):

        user = request.user
        if request.method in SAFE_METHODS:
            return True
        if user.is_authenticated and user.role == 'CA':
            return user == obj.client.client_admin
        if user.is_authenticated and user.role == 'FA':
            return True
        return False


# class IsClientAdmin(BasePermission):
#     """Grants client admins full access"""

#     def has_permission(self, request, view):
#         user = request.user if request.user.is_authenticated else None
#         if user.role == 'CA':
#             return user and user.role == 'CA'
#         if user.role == 'LA':
#             return user and user.role == 'LA'
        


class IsOwner(BasePermission):
    """ a user can be able to edit an account enquiry belonging to only him """

    def has_object_permission(self, request, view, obj):

        user = request.user

        if request.method in SAFE_METHODS:
            return True

        return obj.requester == user


class IsAdmin(BasePermission):
    """ check if its the Admin then allow to delete"""

    def has_object_permission(self, request, view, obj):

        user = request.user

        if request.method == 'DELETE' and user.role == 'FA':
            return True
