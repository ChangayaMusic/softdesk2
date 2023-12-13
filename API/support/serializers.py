# serializers.py
from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from django.contrib.auth.models import User
from accounts.models import CustomUser

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'user']

class IssueSerializer(serializers.ModelSerializer):
    issue_author = serializers.StringRelatedField(source='issue_author.username', read_only=True)

    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'status', 'priority', 'tag', 'created_time', 'issue_author']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_time']

class ProjectSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(many=True, read_only=True)
    issues = IssueSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'author', 'project_type', 'status', 'created_time', 'contributors', 'issues']

    def create(self, validated_data):
        # Set the author field to the user making the request
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    