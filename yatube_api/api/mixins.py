from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from posts.models import Post


User = get_user_model()


class GetPostMixin:

    def get_post(self):
        return get_object_or_404(Post, id=self.kwargs.get('post_id'))


class GetUserMixin:

    def get_user(self):
        return self.request.user
