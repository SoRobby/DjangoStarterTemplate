from django.db import models


class FeedbackQuerySet(models.QuerySet):
    def bug_feedback(self):
        return self.filter(category=self.model.CATEGORY.BUG)

    def feature_feedback(self):
        return self.filter(category=self.model.CATEGORY.FEATURE)

    def general_feedback(self):
        return self.filter(category=self.model.CATEGORY.GENERAL)

    def other_feedback(self):
        return self.filter(category=self.model.CATEGORY.OTHER)

    def processed(self):
        return self.filter(is_processed=True)

    def unprocessed(self):
        return self.filter(is_processed=False)
