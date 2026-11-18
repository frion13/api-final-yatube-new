from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

v1_router = DefaultRouter()
v1_router.register('posts', PostViewSet, basename='post')
v1_router.register('groups', GroupViewSet, basename='group')
v1_router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    re_path(
        r'^v1/posts/(?P<post_id>\d+)/comments/$',
        CommentViewSet.as_view({'get': 'list', 'post': 'create'}),
    ),
    re_path(
        r'^v1/posts/(?P<post_id>\d+)/comments/(?P<pk>\d+)/$',
        CommentViewSet.as_view({
            'get': 'retrieve', 'put': 'update', 'patch': 'partial_update',
            'delete': 'destroy',
        }),
    ),
    path('v1/jwt/create/', TokenObtainPairView.as_view()),
    path('v1/jwt/refresh/', TokenRefreshView.as_view()),
    path('v1/jwt/verify/', TokenVerifyView.as_view()),
]
