# urls.py
from django.urls import path
from .views import *
from accounts.views import ModifyUserView, DeleteUserView

urlpatterns = [
    path('contributors/', ContributorListCreateView.as_view(), name='contributor-list-create'),
    path('issues/', IssueListCreateView.as_view(), name='issue-list-create'),
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/<uuid:project_id>/delete/', DeleteProjectView.as_view(), name='delete_project'),
    path('projects/<uuid:pk>/update/', ProjectRetrieveUpdateView.as_view(), name='project-update'),
    path('projects/create/', ProjectCreateView.as_view(), name='create-project'),
    path('projects/list/', ProjectListView.as_view(), name='project-list'),
    path('projects/<uuid:project_id>/add-contributor/', AddContributorToProjectView.as_view(), name='add-contributor-to-project'),
    path('projects/<uuid:project_id>/add-issue/', AddIssueToProjectView.as_view(), name='add-issue-to-project'),
    path('projects/<uuid:project_id>/issues/', ProjectIssuesListView.as_view(), name='project-issues-list'),
    path('projects/<uuid:project_id>/issues/<uuid:issue_id>/add-comment/', AddCommentToIssueView.as_view(), name='add-comment-to-issue'),
    path('projects/<uuid:project_id>/issues/<uuid:issue_id>/comments/', CommentListAPIView.as_view(), name='comment-list'),
    path('projects/<uuid:project_id>/issues/<uuid:issue_id>/update/', UpdateIssueView.as_view(), name='update-issue'),
    path('projects/<uuid:project_id>/issues/<uuid:id>/delete/', DeleteIssueView.as_view(), name='delete-issue'),
    path('projects/<uuid:project_id>/issues/<uuid:issue_id>/comments/<uuid:comment_id>/delete/', DeleteCommentView.as_view(), name='delete-comment'),
    path('projects/<uuid:project_id>/issues/<uuid:issue_id>/comments/<uuid:comment_id>/update/', UpdateCommentView.as_view(), name='update-comment'),
    path('userslist/', UsersListView.as_view(), name='user-list'),
    path('users/modify/<int:pk>/', ModifyUserView.as_view(), name='modify-user'),
    path('users/delete/<int:pk>/', DeleteUserView.as_view(), name='delete-user'),
]
