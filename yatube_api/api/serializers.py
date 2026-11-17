from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date', 'image', 'group')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'author', 'text', 'created', 'post')
        model = Comment
        read_only_fields = ('author', 'post')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(slug_field='username', read_only=True)
    following = SlugRelatedField(
        slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ('user', 'following')
        read_only_fields = ('user',)

    def validate(self, attrs):
        request = self.context['request']
        following = attrs['following']
        if request.user == following:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя.')
        if Follow.objects.filter(
                user=request.user, following=following).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.')
        return attrs
