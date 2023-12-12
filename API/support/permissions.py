from rest_framework import permissions
from .models import Contributor

class IsProjectAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the author of the project
        return obj.author == request.user

class IsIssueAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the author of the issue
        return obj.issue_author == request.user

class IsCommentAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Check if the user is the author of the comment
        return obj.user == request.user
class IsContributor(permissions.BasePermission):
    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id')
        if project_id:
            try:
                # Check if the user is a contributor to the project
                Contributor.objects.get(user=request.user, project_id=project_id)
                return True
            except Contributor.DoesNotExist:
                return False
        return False