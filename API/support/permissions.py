# permissions.py

from rest_framework import permissions
from rest_framework.permissions import BasePermission
from .models import Project
from support.models import Contributor

class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        print("IsAuthenticated has_object_permission called")

        result = super().has_permission(request, view)
        print(f"IsAuthenticated has_permission: {result}")
        return result


class IsContributor(BasePermission):
    """
    Custom permission to check if the requesting user is in the list of contributors for the project.
    """

    def has_permission(self, request, view):
        project_id = view.kwargs.get('project_id') or view.kwargs.get('pk')

        try:
            # Check if the user is a contributor for the project
            contributor = Contributor.objects.get(project_id=project_id)

            return request.user in contributor.users.all()
        except (Contributor.DoesNotExist, Project.DoesNotExist):
            return False
class IsProjectAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("IsProjectAuthor has_object_permission called")
        return obj.author == request.user

class IsIssueAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("IsIssueAuthor has_object_permission called")
        print(f"Request user: {request.user}")
        print(f"Issue author: {obj.issue_author}")

        result = obj.issue_author == request.user
        print(f"IsIssueAuthor result: {result}")
        return result


class IsCommentAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print("IsCommentAuthor has_object_permission called")
        return obj.comment_author == request.user
