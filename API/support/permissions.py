from django.core.exceptions import ObjectDoesNotExist
from rest_framework import permissions

from .models import Comment, Contributor, Issue, Project

class IsAuthorProjectView(permissions.BasePermission):
    """
    Check if the user is the author of the project.
    http_methods: destroy, update
    """
    def has_permission(self, request, view):
        if view.action in ("destroy", "update"):
            try:
                project = Project.objects.get(pk=view.kwargs["pk"])
            except ObjectDoesNotExist:
                return False
            return project.author == request.user
        return True

class IsAuthorContributorView(permissions.BasePermission):
    """
    Check if the user is a contributor of the project.
    http_methods: destroy, update
    """
    def has_permission(self, request, view):
        if view.action in ("destroy", "update"):
            try:
                project = Project.objects.get(pk=view.kwargs["project_pk"])
            except ObjectDoesNotExist:
                return False
            return Contributor.objects.filter(project=project, user=request.user).exists()
        return True

class IsAuthorContribIssue(permissions.BasePermission):
    """
    Check if the user is the author or a contributor for an issue.
    http_methods: list, retrieve, create
    """
    def has_permission(self, request, view):
        if view.action in ("list", "retrieve", "create"):
            try:
                project = Project.objects.get(id=view.kwargs["project_pk"])
            except ObjectDoesNotExist:
                return False
            is_contrib_issue = Contributor.objects.filter(
                project_id=view.kwargs["project_pk"],
                user=request.user.id
            ).exists()
            if project.author == request.user or is_contrib_issue:
                return True
            return False
        if view.action in ("destroy", "update"):
            try:
                issue = Issue.objects.get(id=view.kwargs["pk"])
            except ObjectDoesNotExist:
                return False
            return issue.author == request.user

class IsAuthorContribComment(permissions.BasePermission):
    """
    Check if the user is the author or a contributor for a comment.
    http_methods: list, retrieve, create
    """
    def has_permission(self, request, view):
        if view.action in ("list", "retrieve", "create"):
            try:
                project = Project.objects.get(id=view.kwargs["project_pk"])
            except ObjectDoesNotExist:
                return False
            is_contrib_comment = Contributor.objects.filter(
                project_id=view.kwargs["project_pk"],
                user=request.user.id
            ).exists()
            if project.author == request.user or is_contrib_comment:
                return True
        if view.action in ("destroy", "update"):
            try:
                comment = Comment.objects.get(id=view.kwargs["pk"])
            except ObjectDoesNotExist:
                return False
            return comment.user == request.user
        return False
