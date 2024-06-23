from django.contrib.auth import get_user_model
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from posts.models import Follow, Post, Group
from .permissions import IsAthorOrReadOnly
from .mixins import GetPostMixin, GetUserMixin
from .serializers import (FollowSerializer, PostSerializer,
                          GroupsSerializer, CommentSerializer)


User = get_user_model()


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(GetUserMixin, CreateModelMixin, ListModelMixin,
                    GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.get_user().follows.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GroupReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer
    permission_classes = [IsAthorOrReadOnly]


class CommentViewSet(GetPostMixin, ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAthorOrReadOnly]

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())
