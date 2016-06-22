# -*- coding:utf-8 -*-

from django.contrib.auth.models import User, Group
from rest_framework import serializers

from models import Article


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, max_length=100)
    content = serializers.CharField()

    def create(self, validated_data):
        return  Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        return instance

    class Meta:
        model = Article
        fields = ('title', 'content', 'pk')
