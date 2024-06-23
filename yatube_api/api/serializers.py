from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


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

    def validate_following(self, value):
        request_user = self.context['request'].user
        following_user = User.objects.filter(username=value.username).first()
        # if value == self.context['request'].user.username:
        if value == self.context['request'].user:
            raise serializers.ValidationError(
                'Невозможно подписаться на себя')
        obj2 = User.objects.filter(username=value.username).first()
        if obj2 is None:
            raise serializers.ValidationError(
                'Пользователель не существует.')
        if Follow.objects.filter(
                user=request_user, following=following_user).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.')
        return value
    # def validate_following(self, value):
    #     request_user = self.context['request'].user

    #     if value == request_user.username:
    #         raise serializers.ValidationError('Невозможно подписаться на самого себя.')

    #     following_user = User.objects.filter(username=value).first()
    #     if following_user is None:
    #         raise serializers.ValidationError('Пользователь не существует.')

    #     if Follow.objects.filter(user=request_user, following=following_user).exists():
    #         raise serializers.ValidationError('Вы уже подписаны на этого пользователя.')

    #     return value

    # def create(self, validated_data):
    #     request_user = self.context['request'].user
    #     following_username = validated_data['following']

    #     following_user = User.objects.get(username=following_username)

    #     instance = Follow.objects.create(user=request_user, following=following_user)
    #     return instance

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     following = validated_data['following']

    #     instance = Follow.objects.create(user=user, following=following)
    #     return instance


class GroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
