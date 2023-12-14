# permissions.py

from rest_framework import permissions
from .models import Project

class IsAuthenticated(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        result = super().has_permission(request, view)
        print(f"IsAuthenticated has_permission: {result}")
        return result

# permissions.py

# permissions.py

class IsContributor(permissions.BasePermission):
    def has_permission(self, request, view):
        print("IsContributor has_permission called")
        if request.user and request.user.is_authenticated:
            project_id = view.kwargs.get('project_id')
            if project_id:
                try:
                    project = Project.objects.get(id=project_id)
                    contributors = project.contributors.all()

                    # Extract contributor IDs from the list of contributors
                    contributor_ids = [user.id for contributor in contributors for user in contributor.users.all()]

                    print(f"Request user ID: {request.user.id}")
                    print(f"Contributor IDs: {contributor_ids}")

                    result = request.user.id in contributor_ids
                    print(f"IsContributor result: {result}")
                    return result
                except Project.DoesNotExist:
                    print("Project not found")
                    return False
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
