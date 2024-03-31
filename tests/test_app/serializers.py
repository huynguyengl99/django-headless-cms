from headless_cms.serializers import LocalizedModelSerializer

from test_app.models import Comment, Post


class CommentSerializer(LocalizedModelSerializer):
    class Meta:
        model = Comment
        exclude = ["published_version"]


class PostSerializer(LocalizedModelSerializer):
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Post
        exclude = ["published_version"]
