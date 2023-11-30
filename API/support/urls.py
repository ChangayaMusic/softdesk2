# urls.py
from django.urls import path
from .views import ContributorListCreateView, IssueListCreateView, ProjectListCreateView
from .views import ProjectCreateView

urlpatterns = [
    path('contributors/', ContributorListCreateView.as_view(), name='contributor-list-create'),
    path('issues/', IssueListCreateView.as_view(), name='issue-list-create'),
    path('projects/', ProjectListCreateView.as_view(), name='project-list-create'),
    path('projects/create/', ProjectCreateView.as_view(), name='create-project'),
    # Ajoutez d'autres URL au besoin
]
