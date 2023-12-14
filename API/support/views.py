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

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Project, Contributor
from .serializers import ContributorSerializer
from accounts.serializers import CustomUserSerializer
from .permissions import IsProjectAuthor
from accounts.models import CustomUser

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
        # Add the 'author' field to the request data
        request.data['author'] = request.user.id

        serializer = ProjectSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            # Save the project
            project = serializer.save()

            # Create a Contributor instance with the author
            contributor = Contributor.objects.create(project=project)
            
            # Add the author to the users field
            contributor.users.add(request.user)

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


class AddIssueToProjectView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsContributor]
    serializer_class = IssueSerializer

    def get_project(self):
        project_id = self.kwargs.get('project_id')
        try:
            return Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return None

    def perform_create(self, serializer):
        project = self.get_project()

        if project:
            # Set the project and issue_author based on the current user
            serializer.save(project=project, issue_author=self.request.user)
        else:
            # Handle the case where the project does not exist
            raise serializers.ValidationError({"error": "Project not found."})
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

    def update(self, request, *args, **kwargs):
        # Ensure that permissions are checked when updating
        self.check_permissions(request)
        return super().update(request, *args, **kwargs)
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
            # Retrieve the issue using the issue_id from the URL
            issue = Issue.objects.get(id=issue_id)

            # Add the comment to the issue
            comment_text = request.data.get('text', '')

            # Create a new Comment instance
            comment = Comment.objects.create(
                issue=issue,
                comment_author=request.user,
                text=comment_text
            )


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
    
    permission_classes = [IsAuthenticated, IsCommentAuthor] 

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
        
class AddContributorToProjectView(APIView):
    permission_classes = [IsAuthenticated, IsProjectAuthor]

    def post(self, request, project_id, *args, **kwargs):
        print("AddContributorToProjectView post method called")
        try:
            project = Project.objects.get(id=project_id)
        except Project.DoesNotExist:
            return Response(
                {"detail": f"Project with id {project_id} not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        user_ids = request.data.get('user_ids', [])
        print(f"Project ID: {project_id}, User IDs: {user_ids}")

        if not user_ids:
            return Response(
                {"detail": "User IDs are required in the request data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        contributor, created = Contributor.objects.get_or_create(project=project)
        contributor.users.add(*user_ids)

        serializer = ContributorSerializer(contributor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
class UsersListView(generics.ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer