# views.py

from .models import *
from .serializers import *
from .permissions import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.generics import DestroyAPIView
from rest_framework import generics


class ContributorListCreateView(generics.ListCreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

class IssueListCreateView(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class ProjectListCreateView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        data['author'] = request.user.id  # Récupère l'ID de l'utilisateur à partir du token JWT

        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteProjectView(APIView):
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def delete(self, request, project_id):
        try:
            # Récupérez le projet spécifique
            project = Project.objects.get(id=project_id)

            # Supprimez le projet
            project.delete()
            return Response({"message": "Project deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

class ProjectRetrieveUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsProjectAuthor]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectListView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class AddIssueToProjectView(APIView):
    def post(self, request, project_id):
        try:
            # Récupérez le projet spécifique
            project = Project.objects.get(id=project_id)

            # Obtenez l'utilisateur actuel (contributeur)
            user = self.request.user

            # Ajoutez le contributeur au projet s'il n'est pas déjà un contributeur
            contributor, created = Contributor.objects.get_or_create(user=user, project=project)

            # Ajoutez l'issue associée au projet
            request.data['project'] = project_id
            request.data['contributor'] = contributor.id

            serializer = IssueSerializer(data=request.data)
            if serializer.is_valid():
                # Créez l'issue associée au projet
                issue = serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Project.DoesNotExist:
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)

class DeleteIssueView(generics.DestroyAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_field = 'issue_id'

class UpdateIssueView(generics.UpdateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_url_kwarg = 'issue_id'

class ProjectIssuesListView(generics.ListAPIView):
    serializer_class = IssueSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Issue.objects.filter(project_id=project_id)

class AddCommentToIssueView(APIView):
    def post(self, request, project_id, issue_id):
        try:
            # Récupérez l'issue spécifique
            issue = Issue.objects.get(id=issue_id)

            # Ajoutez le commentaire à l'issue
            comment_text = request.data.get('comment', '')

            # Create a new Comment instance
            comment = Comment.objects.create(
                issue=issue,
                user=request.user,
                text=comment_text
            )

            # Récupérez le contributeur associé à l'utilisateur qui crée le commentaire
            contributor, created = Contributor.objects.get_or_create(user=request.user, project=issue.project)

            # Sauvegardez le contributeur (si nécessaire)
            contributor.save()

            serializer = CommentSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Issue.DoesNotExist:
            return Response({"error": "Issue not found"}, status=status.HTTP_404_NOT_FOUND)

class DeleteCommentView(APIView):


    def delete(self, request, project_id, issue_id, comment_id):
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class UpdateCommentView(APIView):
    def patch(self, request, project_id, issue_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)

            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
class CommentListAPIView(APIView):
    def get(self, request, project_id, issue_id):
        try:
            # Assuming you have a method to get the project based on project_id
            project = Project.objects.get(id=project_id)

            # Get the comments for the specified issue within the project
            comments = Comment.objects.filter(issue_id=issue_id, issue__project=project)

            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Comment.DoesNotExist:
            return Response({"error": "Comments not found"}, status=status.HTTP_404_NOT_FOUND)
