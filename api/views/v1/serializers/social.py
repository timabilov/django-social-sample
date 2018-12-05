from rest_framework import serializers

from api.models import UserProfile, PostLike, Post
import arrow

from api.utils import kformat


class ShortUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('id', 'username', 'img')


class PostSerializer(serializers.ModelSerializer):
    user = ShortUserSerializer(read_only=True)
    content = serializers.CharField(max_length=400)
    date = serializers.SerializerMethodField(read_only=True)
    likes = serializers.IntegerField(read_only=True)
    liked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'user', 'content', 'date', 'likes', 'liked')

    def get_date(self, obj):
        date = arrow.get(obj.created).humanize()
        return date.replace('minute', 'min')

    def get_likes(self, obj):

        return kformat(obj.likes)

    def get_liked(self, obj):

        user = self.context['request'].user
        if user and user.is_authenticated:
            return PostLike.objects.filter(
                reacted_id=user.id,
                post_id=obj.id
            ).exists()

        return False
