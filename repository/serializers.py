from rest_framework import serializers


class Repository(object):
    def __init__(self, **kwargs):
        for field in ('username', 'commits'):
            setattr(self, field, kwargs.get(field, None))


class Commit(object):
    def __init__(self, **kwargs):
        for field in ('count', 'date'):
            setattr(self, field, kwargs.get(field, None))


class CommitSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    date = serializers.DateField(input_formats=['iso-8601'])


class RepositoryDataSerializer(serializers.Serializer):
    username = serializers.CharField()
    commits = CommitSerializer(many=True)
