# TODO:  Напишите свой вариант
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import (GenericViewSet, ModelViewSet,
                                     ReadOnlyModelViewSet)
from rest_framework.mixins import CreateModelMixin, ListModelMixin, DestroyModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters

from posts.models import Follow, Post, Group
from .serializers import (FollowSerializer, PostSerializer, GroupsSerializer,
                          CommentSerializer)
from .permissions import IsAthorOrReadOnly


User = get_user_model()


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAthorOrReadOnly]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FollowViewSet(DestroyModelMixin, CreateModelMixin, ListModelMixin,
                    GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)

    def get_user(self):
        return get_object_or_404(User, id=self.request.user.id)

    def get_queryset(self):
        return self.get_user().follows.all()

    # def get_or_none(self, **kwargs):
    #     try:
    #         return self.queryset.filter(**kwargs).first()
    #     except Follow.DoesNotExist:
    #         return None

    def perform_create(self, serializer):
        # if serializer.initial_data['following'] == self.request.user.username:
        #     raise PermissionDenied('Невозможно подписаться на самого себя')
        serializer.save(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     obj1 = self.get_or_none(following=serializer.initial_data['following'])
    #     obj2 = User.objects.filter(username=serializer.initial_data['following']).first()
    #     # obj2 = self.get_or_none(username=serializer.initial_data['following'])
    #     if obj2 is None:
    #         return Response({'detail': 'Пользователель не существует.'}, status=status.HTTP_400_BAD_REQUEST)
    #     if obj1:
    #         return Response({'detail': 'Вы уже подписаны на этого пользователя.'}, status=status.HTTP_400_BAD_REQUEST)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # def destroy(self, request, *args, **kwargs):
    #     print("aaaaaaaaaaaaaaaaaaaaaaa")
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)

    # def perform_destroy(self, instance):
    #     print("bbbbbbbbbbbbbbbbbbbbbbbb")
    #     instance.delete()


class GroupReadOnlyViewSet(ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupsSerializer
    permission_classes = [IsAthorOrReadOnly]


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAthorOrReadOnly]

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())
