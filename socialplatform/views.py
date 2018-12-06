

# for demo index page

from django.shortcuts import render_to_response

from api.models import Post, PostLike


def index(request):

    count = Post.objects.count()
    likes = PostLike.objects.count()
    return render_to_response('index.html', context={
        "count": count,
        "likes": likes,
        "posts": Post.objects.order_by('-created')[:50]
    })