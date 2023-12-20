from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView, ListCreateAPIView, CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from .permissions import IsProjectAuthor, IsIssueAuthor, IsCommentAuthor, IsContributor
import uuid

def paginate_objects(request, objects, items_per_page=10):
    paginator = Paginator(objects, items_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_objects = paginator.page(page)
    except PageNotAnInteger:
        paginated_objects = paginator.page(1)
    except EmptyPage:
        paginated_objects = paginator.page(paginator.num_pages)

    return paginated_objects


class ContributorListCreateView(ListCreateAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]


class IssueListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsContributor]
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def list(self, request, *args, **kwargs):
        issues = Issue.objects.all()
        paginated_issues = paginate_objects(request, issues)
        serializer = self.get_serializer(paginated_issues, many=True)
        return Response(serializer.data)


class ProjectListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        projects = Project.objects.all()
        paginated_projects = paginate_objects(request, projects)
        serializer = ProjectSerializer(paginated_projects, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Generate a UUID for the project
        project_uuid = uuid.uuid4()

        # Add the 'author' field to the request data
        request.data['author'] = request.user.id
        # Replace the default 'id' field with the generated UUID
        request.data['id'] = project_uuid

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


class ProjectCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Generate a UUID for the project
        project_uuid = uuid.uuid4()

        # Add the 'author' field to the request data
        request.data['author'] = request.user.id
        # Replace the default 'id' field with the generated UUID
        request.data['id'] = project_uuid

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
        paginated_projects = paginate_objects(request, projects)
        serializer = ProjectSerializer(paginated_projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddIssueToProjectView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsContributor]
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


class DeleteIssueView(DestroyAPIView):
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


class UpdateIssueView(UpdateAPIView):
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


class ProjectIssuesListView(ListAPIView):
    permission_classes = [IsAuthenticated, IsContributor]
    serializer_class = IssueSerializer

    def get_queryset(self):
        project_id = self.kwargs['project_id']
        issues = Issue.objects.filter(project_id=project_id)
        return paginate_objects(self.request, issues)


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


class DeleteCommentView(DestroyAPIView):
    permission_classes = [IsAuthenticated, IsCommentAuthor]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


class UpdateCommentView(UpdateAPIView):
    permission_classes = [IsAuthenticated, IsCommentAuthor]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'

    def update(self, request, *args, **kwargs):
        # Ensure that permissions are checked when updating
        self.check_permissions(request)
        return super().update(request, *args, **kwargs)


class CommentListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated, IsContributor]

    def get(self, request, project_id, issue_id):
        try:
            # Assuming you have a method to get the project based on project_id
            project = Project.objects.get(id=project_id)

            # Get the comments for the specified issue within the project
            comments = Comment.objects.filter(issue_id=issue_id, issue__project=project)
            paginated_comments = paginate_objects(request, comments)

            serializer = CommentSerializer(paginated_comments, many=True)
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


class UsersListView(ListAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Retrieve the list of users from the database
        users = CustomUser.objects.all()
        paginated_users = paginate_objects(request, users)
        serializer = CustomUserSerializer(paginated_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
