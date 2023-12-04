from rest_framework.permissions import BasePermission

class IsCommentAuthorOrProjectContributor(BasePermission):
    """
    Permission pour permettre l'accès à l'auteur du commentaire ou à tous les contributeurs du projet.
    """
    message = "Vous n'avez pas la permission d'effectuer cette action."

    def has_object_permission(self, request, view, obj):
        # Vérifier si l'utilisateur est l'auteur du commentaire ou un contributeur du projet
        return obj.author_user_id == request.user or obj.issue_id.project_id.contributors.filter(user=request.user).exists()

class IsIssueAuthorOrProjectContributor(BasePermission):
    """
    Permission pour permettre l'accès à l'auteur de l'issue ou à tous les contributeurs du projet.
    """
    message = "Vous n'avez pas la permission d'effectuer cette action."

    def has_object_permission(self, request, view, obj):
        # Vérifier si l'utilisateur est l'auteur de l'issue ou un contributeur du projet
        return obj.author_user_id == request.user or obj.project_id.contributors.filter(user=request.user).exists()

class IsProjectAuthor(BasePermission):
    """
    Permission pour permettre l'accès uniquement à l'auteur du projet.
    """
    message = "Vous n'avez pas la permission d'effectuer cette action."

    def has_object_permission(self, request, view, obj):
        # Vérifier si l'utilisateur est l'auteur du projet
        return obj.author_user_id == request.user
