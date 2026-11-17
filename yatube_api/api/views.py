from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from posts.models import Comment, Follow, Group, Post
from .serializers import (
    CommentSerializer,
    FollowSerializer,
    GroupSerializer,
    PostSerializer,
)


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class ConditionalLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100


class ConditionalPaginationMixin:
    pagination_class = ConditionalLimitOffsetPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if not {'limit', 'offset'} & set(request.query_params):
            return Response(self.get_serializer(queryset, many=True).data)
        page = self.paginate_queryset(queryset)
        if page is not None:
            data = self.get_serializer(page, many=True).data
            return self.get_paginated_response(data)
        return Response(self.get_serializer(queryset, many=True).data)


class PostViewSet(ConditionalPaginationMixin, viewsets.ModelViewSet):
    queryset = Post.objects.select_related('author', 'group').all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.AllowAny,)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        get_object_or_404(Post, pk=self.kwargs['post_id'])
        return Comment.objects.filter(
            post_id=self.kwargs['post_id']).select_related('author', 'post')

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, post_id=self.kwargs['post_id'])


class FollowViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return Follow.objects.filter(
            user=self.request.user).select_related('user', 'following')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
