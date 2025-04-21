from django.db.models import QuerySet

from blog.models import Comment


class CommentService:

    @staticmethod
    def create_comment(
            author_id: int,
            post_id: int,
            text: str,
    ) -> Comment:
        comment = Comment(
            author_id=author_id,
            post_id=post_id,
            text=text
        )

        comment.save()

        return comment

    @staticmethod
    def get_comments_by_author(
            author_id: int
    ) -> QuerySet[Comment]:
        comments = (
            Comment.objects.select_related(
                "post",
                "post__author"
            )
            .filter(author_id=author_id)
        )

        return comments
