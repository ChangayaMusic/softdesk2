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

from .permissions import (
    IsProjectAuthor, IsIssueAuthor, IsCommentAuthor, IsContributor
)

class ContributorListCreateView(generics.ListCreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer

class IssueListCreateView(generics.ListCreateAPIView):
    
    permission_classes = [IsAuthenticated, IsContributor]
    
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

class ProjectListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        data['author'] = request.user.id

        serializer = ProjectSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            # Save the project
            project = serializer.save()

            # Add the author as a contributor
            project.contributors.create(user=request.user)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteProjectView(APIView):
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def delete(self, request, project_id):
        try:
            # Récupérez le projet spécifique
            project = Project.objects.get(id=project_id)

            # Vérifie si l'utilisateur est l'auteur du projet
            print(f"Request user: {request.user.id}")
            print(f"Project author: {project.author.id}")

            self.check_object_permissions(request, project)

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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
# views.py

from .models import Project, Contributor, Issue
from .serializers import IssueSerializer
from .permissions import IsContributor

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# views.py

class AddIssueToProjectView(APIView):
    permission_classes = [IsAuthenticated, IsContributor]

    def post(self, request, project_id):
        try:
            # Récupérez le projet spécifique
            project = Project.objects.get(id=project_id)

            # Obtenez l'utilisateur actuel (contributeur)
            user = self.request.user

            # Ajoutez l'issue associée au projet avec l'issue_author défini
            request.data['project'] = project_id
            request.data['issue_author'] = user.id  # Set the issue_author based on the user

            serializer = IssueSerializer(data=request.data)
            if serializer.is_valid():
                # Set the project_id before saving the serializer
                serializer.validated_data['project_id'] = project_id

                # Créez l'issue associée au projet
                issue = serializer.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                print(f"Serializer errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Project.DoesNotExist:
            print(f"Project {project_id} not found")
            return Response({"error": "Project not found"}, status=status.HTTP_404_NOT_FOUND)


class DeleteIssueView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsIssueAuthor]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_url_kwarg = 'id'  # Specify the lookup field in the URL

    def get_object(self):
        # Use the specified lookup field to get the object
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        return generics.get_object_or_404(self.get_queryset(), **filter_kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"detail": "Issue successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
class UpdateIssueView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsIssueAuthor]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_url_kwarg = 'issue_id'  # Specify the lookup field in the URL

    def get_object(self):
        # Use the specified lookup field to get the object
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        return generics.get_object_or_404(self.get_queryset(), **filter_kwargs)

class UpdateIssueView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated, IsIssueAuthor]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    lookup_url_kwarg = 'issue_id'  # Specify the lookup field in the URL


class ProjectIssuesListView(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated, IsContributor]
    serializer_class = IssueSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        return Issue.objects.filter(project_id=project_id)

class AddCommentToIssueView(APIView):
    
    permission_classes = [IsAuthenticated, IsContributor]
    
    
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

    permission_classes = [IsAuthenticated, IsCommentAuthor]

    def delete(self, request, project_id, issue_id, comment_id):
        comment = Comment.objects.get(id=comment_id)
        comment.delete()
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

class UpdateCommentView(APIView):
    
    permission_classes = [IsAuthenticated, IsCommentAuthor]  # Seul l'auteur du commentaire peut modifier

    def patch(self, request, project_id, issue_id, comment_id):
        try:
            comment = Comment.objects.get(id=comment_id)

            # Ajoutez la vérification de la permission ici
            self.check_object_permissions(request, comment)

            serializer = CommentSerializer(comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Comment.DoesNotExist:
            return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
class CommentListAPIView(APIView):
    
    permission_classes = [IsAuthenticated, IsContributor]
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
