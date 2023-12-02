# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('contributors/', ContributorListCreateView.as_view(), name='contributor-list-create'),
    path('issues/', IssueListCreateView.as_view(), name='issue-list-create'),
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/create/', ProjectCreateView.as_view(), name='create-project'),
    path('projects/list/', ProjectListView.as_view(), name='project-list'),
    path('projects/<int:project_id>/add-issue/', AddIssueToProjectView.as_view(), name='add-issue-to-project'),
    path('projects/<int:project_id>/issues/', ProjectIssuesListView.as_view(), name='project-issues-list'),
    path('projects/<int:project_id>/issues/<int:issue_id>/add-comment/', AddCommentToIssueView.as_view(), name='add-comment-to-issue'),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', CommentListAPIView.as_view(), name='comment-list'),
]
