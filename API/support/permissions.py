# permissions.py

from rest_framework import permissions

class IsProjectAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Seul l'auteur du projet peut effectuer certaines actions
        return obj.author == request.user

class IsIssueAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Seul l'auteur de l'issue peut effectuer certaines actions
        return obj.author == request.user

class IsCommentAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Seul l'auteur du commentaire peut effectuer certaines actions
        return obj.author == request.user

class IsContributor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Tous les contributeurs ont la permission de lecture
        return obj.contributors.filter(user=request.user).exists()

