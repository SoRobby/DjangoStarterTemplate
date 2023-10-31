class ArticleService:
    def __init__(self, article):
        self.article = article


class CommentService:
    def __init__(self, comment):
        self.comment = comment

    def like_toggle(self, user):
        """
        Adds a like to a comment.
        """

        # Do a check to see if the user has already disliked the comment
        if user in self.comment.dislikes.all():
            self.comment.dislikes.remove(user)

        # Do a check to see if the user has already liked the comment
        if user in self.comment.likes.all():
            self.comment.likes.remove(user)
        else:
            self.comment.likes.add(user)

        self.comment.save()

    def dislike_toggle(self, user):
        """
        Adds a dislike to a comment.
        """

        # Do a check to see if the user has already liked the comment
        if user in self.comment.likes.all():
            self.comment.likes.remove(user)

        # Do a check to see if the user has already disliked the comment
        if user in self.comment.dislikes.all():
            self.comment.dislikes.remove(user)
        else:
            self.comment.dislikes.add(user)

        self.comment.save()

    def report_comment(self):
        """
        Report a comment.
        """
        if not self.comment.is_flagged:
            self.comment.is_flagged = True
            self.comment.save()
