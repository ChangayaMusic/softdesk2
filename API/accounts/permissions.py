from rest_framework import permissions

class IsUserOwner(permissions.BasePermission):
    """
    Custom permission to only allow the user to modify or delete their own profile.
    """

    def has_object_permission(self, request, view, obj):
        print("checking is user owner")
        # Check if the user making the request is the owner of the profile
        return obj.uuid == request.user.uuid