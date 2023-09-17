from django.db import models
from django.utils.timezone import is_aware, make_naive, utc


class DateCreatedAndModified(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created',
                                        help_text='Server date and time when the item was created modified')

    date_modified = models.DateTimeField(auto_now=True, verbose_name='Date modified',
                                         help_text='Server date and time when the item was last modified')

    class Meta:
        abstract = True

    def get_date_created_utc_standard(self):
        """
        Converts date_created to the standard UTC datetime format
        Returns:
            A string representing the date and time in UTC standard format "YYYY-MM-DDTHH:MM:SSZ"
        """
        date_created_utc = self.date_created
        if is_aware(date_created_utc):
            date_created_utc = make_naive(date_created_utc, timezone=utc)
        return date_created_utc.strftime('%Y-%m-%dT%H:%M:%SZ')

    def get_date_modified_utc_standard(self):
        """
        Converts date_modified to the standard UTC datetime format
        Returns:
            A string representing the date and time in UTC standard format "YYYY-MM-DDTHH:MM:SSZ"
        """
        date_modified_utc = self.date_modified
        if is_aware(date_modified_utc):
            date_modified_utc = make_naive(date_modified_utc, timezone=utc)
        return date_modified_utc.strftime('%Y-%m-%dT%H:%M:%SZ')


class DateDeleted(models.Model):
    date_deleted = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                        verbose_name='Date deleted',
                                        help_text='Server date and time when the item was deleted')

    class Meta:
        abstract = True

    def get_date_deleted_utc_standard(self):
        """
        Converts date_deleted to the standard UTC datetime format
        Returns:
            A string representing the date and time in UTC standard format "YYYY-MM-DDTHH:MM:SSZ"
        """
        date_deleted_utc = self.date_deleted
        if is_aware(date_deleted_utc):
            date_deleted_utc = make_naive(date_deleted_utc, timezone=utc)
        return date_deleted_utc.strftime('%Y-%m-%dT%H:%M:%SZ')
