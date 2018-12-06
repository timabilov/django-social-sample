import logging

from django.db import IntegrityError
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from api.models import UserProfile, Post, PostLike
from django.utils.translation import ugettext_lazy as tr
from api.views.v1.serializers.social import PostSerializer

logger = logging.getLogger(__name__)


class PostViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.CreateModelMixin):

    queryset = Post.objects.order_by('-created')
    serializer_class = PostSerializer
    per_page = 12

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset(**kwargs))

        # built-in pagination does not suit for real-time list changes(mobile?)
        # infinite scrolling
        last_id = request.GET.get('cursor_id')
        if last_id:
            page = queryset.filter(id__lt=last_id)[:self.per_page]

            serializer = self.get_serializer(page, many=True)
            return JsonResponse({
                "perPage": self.per_page,
                "posts": serializer.data,

            })

        queryset = queryset[:self.per_page]
        serializer = self.get_serializer(queryset, many=True)
        return JsonResponse({
            "posts": serializer.data,
            "perPage": self.per_page,
        })

    def perform_create(self, serializer):

        serializer.save(
            user=self.request.user
        )

    @action(detail=True, methods=['POST', 'DELETE'])
    def like(self, *args,  **kwargs):

        post = get_object_or_404(Post, id=kwargs.get('pk'))

        if self.request.method == 'DELETE':
            like = PostLike.objects.filter(
                post_id=post.id, reacted_id=self.request.user.id
            )
            deleted, _ = like.delete()
            if not deleted:
                return JsonResponse({
                    "message": "Not found"
                }, status=404)
            Post.objects.filter(id=post.id).update(likes=F('likes') - 1)
        elif self.request.method == 'POST':
            try:
                like, created = PostLike.objects.get_or_create(
                    post_id=post.id, reacted_id=self.request.user.id
                )

                if created:
                    Post.objects.filter(id=post.id).update(likes=F('likes') + 1)
                else:
                    # we can omit this response - depends on arch and client
                    return JsonResponse({
                        "message": tr("You've already liked this post"),
                    }, status=400)
            except IntegrityError:
                # get or create  handles race condition problem
                # with getting already created object
                # but in that case we can be trapped to case where obj removed.
                # Todo a)simple solution, job with synchronous queue for high load likes for whole likes issue
                return JsonResponse({
                    "message": "Please try one more time",
                }, status=429)

        return JsonResponse({
            "message": "Successfully"
        })

