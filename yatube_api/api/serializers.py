from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Post, Follow, Group


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )
    following = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')

    def validate_following(self, following):
        request_user = self.context['request'].user

        if following == request_user:
            raise serializers.ValidationError(
                'Невозможно подписаться на себя.')

        following_user = User.objects.filter(
            username=following.username).first()

        if not following_user:
            raise serializers.ValidationError('Пользователь не существует.')

        if Follow.objects.filter(
                user=request_user, following=following_user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.')

        return following


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
