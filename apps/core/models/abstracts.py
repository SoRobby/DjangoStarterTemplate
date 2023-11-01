import logging
from datetime import timedelta
from uuid import uuid4

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.timezone import is_aware, make_naive, utc


class BaseModel(models.Model):
    """
    Abstract base model providing core fields and functionality to derived models.

    Fields:
    - uuid: A unique identifier for each record, not editable.
    - date_created: A timestamp indicating when the record was created.
    - date_modified: A timestamp indicating the last time the record was modified.
    """

    # Unique identifier for each instance of the model. Uses UUIDv4 for random generation.
    uuid = models.UUIDField(default=uuid4, editable=False, unique=True, verbose_name='UUID',
                            help_text='Unique identifier for the item')

    # Date and time when the instance was first created. Field is automatically set when the instance is first saved.
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Date created',
                                        help_text='Server date and time when the item was created modified')

    # Date and time when the instance was last modified. Field is automatically set when the instance is saved.
    date_modified = models.DateTimeField(auto_now=True, verbose_name='Date modified',
                                         help_text='Server date and time when the item was last modified')

    class Meta:
        abstract = True


class UserCreatedAndModifiedModel(BaseModel):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name='%(app_label)s_%(class)s_created_by_set', verbose_name='Created by',
                                   help_text='User who created the item')

    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                    related_name='%(app_label)s_%(class)s_modified_by', verbose_name='Modified by',
                                    help_text='User who last modified the item')


class SoftDeletionModel(models.Model):
    date_deleted = models.DateTimeField(auto_now_add=False, auto_now=False, blank=True, null=True,
                                        verbose_name='Date deleted',
                                        help_text='Server date and time when the item was deleted')

    is_deleted = models.BooleanField(default=False, verbose_name='Is deleted',
                                     help_text='Whether the item has been deleted or not')

    class Meta:
        abstract = True


class SoftDeletionWithUserModel(SoftDeletionModel):
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True,
                                   related_name='%(app_label)s_%(class)s',
                                   verbose_name='Deleted by',
                                   help_text='User who deleted the item')

    class Meta:
        abstract = True


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

    @classmethod
    def percent_change(cls, delta_days: int):
        # Get the dates for the past week and the week before
        # end_date = datetime.now()
        end_date = timezone.now()

        start_date = end_date - timedelta(days=delta_days)
        period_before_start_date = start_date - timedelta(days=delta_days)
        period_before_end_date = start_date

        logging.debug(f'start_date: {start_date}')
        logging.debug(f'end_date: {end_date}')
        logging.debug(f'period_before_start_date: {period_before_start_date}')
        logging.debug(f'period_before_end_date: {period_before_end_date}')

        # Get the count of feedback entries for the past week
        last_period_count = cls.objects.filter(date_created__range=(start_date, end_date)).count()

        logging.debug(f'last_period_count: {last_period_count}')

        # Get the count of feedback entries for the week before the past week
        period_before_count = cls.objects.filter(
            date_created__range=(period_before_start_date, period_before_end_date)).count()

        logging.debug(f'period_before_count: {period_before_count}')

        # Calculate the percent increase
        try:
            percent_increase = ((last_period_count - period_before_count) / period_before_count) * 100
        except ZeroDivisionError:
            if last_period_count == 0:
                return 0  # If both counts are zero, the increase is zero
            return 100  # If week_before_count is zero but last_week_count isn't, the increase is 100%

        return percent_increase

    @classmethod
    def percent_change_last_day(cls):
        # Get the percent change for the last day (24 hrs)
        return cls.percent_change(delta_days=1)

    @classmethod
    def percent_change_last_week(cls):
        # Get the percent change for the last week
        return cls.percent_change(delta_days=15)

    @classmethod
    def percent_change_last_month(cls):
        # Get the percent change for the last month
        return cls.percent_change(delta_days=30)

    @classmethod
    def percent_change_last_year(cls):
        # Get the percent change for the last year
        return cls.percent_change(delta_days=365)
