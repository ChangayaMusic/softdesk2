# urls.py
from django.urls import path
from .views import *
from accounts.views import ModifyUserView

urlpatterns = [
    path('contributors/', ContributorListCreateView.as_view(), name='contributor-list-create'),
    path('issues/', IssueListCreateView.as_view(), name='issue-list-create'),
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<int:project_id>/delete/', DeleteProjectView.as_view(), name='delete_project'),
    path('projects/<int:pk>/update/', ProjectRetrieveUpdateView.as_view(), name='project-update'),
    path('projects/create/', ProjectCreateView.as_view(), name='create-project'),
    path('projects/list/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:project_id>/add-contributor/', AddContributorToProjectView.as_view(), name='add-contributor-to-project'),
    path('projects/<int:project_id>/add-issue/', AddIssueToProjectView.as_view(), name='add-issue-to-project'),
    path('projects/<int:project_id>/issues/', ProjectIssuesListView.as_view(), name='project-issues-list'),
    path('projects/<int:project_id>/issues/<int:issue_id>/add-comment/', AddCommentToIssueView.as_view(), name='add-comment-to-issue'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('projects/<int:project_id>/issues/<int:issue_id>/update/', UpdateIssueView.as_view(), name='update-issue'),
    path('projects/<int:project_id>/issues/<int:id>/delete/', DeleteIssueView.as_view(), name='delete-issue'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/delete/', DeleteCommentView.as_view(), name='delete-comment'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/update/', UpdateCommentView.as_view(), name='update-comment'),
    path('users/', UsersListView.as_view(), name='user-list'),
    path('users/modify/<int:pk>/', ModifyUserView.as_view(), name='modify-user'),
]


