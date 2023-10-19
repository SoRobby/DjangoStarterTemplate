from .models import Comment


class CommentService:

    def __init__(self, comment):
        self.comment = comment

    def toggle_vote(self, user, vote_type: None):
        """
        Toggles user's vote on a comment.
        :param user: The user toggling the vote.
        :param vote_type: Should be 'upvote' or 'downvote'
        :return: None
        """
        if vote_type == 'upvote':
            if user in self.comment.downvotes.all():
                self.comment.downvotes.remove(user)
            self.comment.upvotes.add(user)
        elif vote_type == 'downvote':
            if user in self.comment.upvotes.all():
                self.comment.upvotes.remove(user)
            self.comment.downvotes.add(user)
        else:
            raise ValueError('vote_type must be either "upvote" or "downvote".')

    def remove_vote(self, user):
        """
        Removes user's vote on a comment.
        """
        if user in self.comment.upvotes.all():
            self.comment.upvotes.remove(user)
        elif user in self.comment.downvotes.all():
            self.comment.downvotes.remove(user)
        else:
            raise ValueError('User has not voted on this comment.')
