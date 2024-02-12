# serializers.py
from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment
from django.contrib.auth.models import User
from accounts.models import CustomUser

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['id', 'users']




class IssueSerializer(serializers.ModelSerializer):
    issue_author = serializers.StringRelatedField(source='issue_author.username', read_only=True)

    class Meta:
        model = Issue
        fields = ['id','uuid', 'title', 'description', 'status', 'priority', 'tag', 'created_time', 'issue_author']

class CommentSerializer(serializers.ModelSerializer):
    comment_author = serializers.StringRelatedField(source='comment_author.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id','uuid', 'issue', 'comment_author', 'text', 'created_time']



class ProjectSerializer(serializers.ModelSerializer):
    contributors = ContributorSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'author', 'title', 'description', 'project_type', 'status', 'created_time', 'contributors', 'issues']
        read_only_fields = ['id']

    def create(self, validated_data):
        # Set the author field to the user making the request
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

    issues = serializers.PrimaryKeyRelatedField(many=True, queryset=Issue.objects.all(), required=False)

