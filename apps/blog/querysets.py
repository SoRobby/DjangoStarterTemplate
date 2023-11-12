from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Count, Prefetch
from django.db.models import Value as V
from django.db.models.functions import Concat

User = get_user_model()


class ArticleQuerySet(QuerySet):
    def with_comments_count(self):
        return self.annotate(comment_count=Count('comment'))


class CommentQuerySet(QuerySet):
    def with_likes_and_dislikes(self):
        return self.select_related('user').annotate(
            number_of_likes=Count('likes', distinct=True),
            number_of_dislikes=Count('dislikes', distinct=True)
        ).prefetch_related(
            Prefetch(
                'likes',
                queryset=User.objects.annotate(username_concat=Concat('username', V(' '))),
                to_attr='liked_usernames_list'
            )
        ).prefetch_related(
            Prefetch(
                'dislikes',
                queryset=User.objects.annotate(username_concat=Concat('username', V(' '))),
                to_attr='disliked_usernames_list'
            )
        ).order_by('-date_created')

    def active(self):
        # This method will filter the queryset to only include active (not deleted) comments
        return self.filter(is_deleted=False)

    def with_liked_usernames(self):
        """
        This will create a list of usernames for users who liked each comment.
        It's a Python-level operation, not a database-level operation.
        """
        comments = self.with_likes_and_dislikes()
        for comment in comments:
            comment.liked_usernames = [user.username for user in comment.liked_usernames_list]
        return comments

    def with_disliked_usernames(self):
        """
        This will create a list of usernames for users who liked each comment.
        It's a Python-level operation, not a database-level operation.
        """
        comments = self.with_likes_and_dislikes()
        for comment in comments:
            comment.liked_usernames = [user.username for user in comment.liked_usernames_list]
        return comments
