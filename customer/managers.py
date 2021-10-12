from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from datetime import datetime
from actstream.managers import ActionManager, stream


class UserManager(BaseUserManager):
    use_in_migrations = True

    def get_queryset(self):

        return super(UserManager, self).get_queryset().filter(
            deleted=False)

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class QueryManager(models.Manager):

    def get_queryset(self):

        return super(QueryManager, self).get_queryset().filter(
            deleted=False)


class FKFActionManager(ActionManager):
    @stream
    def mystream(self, obj, verb='posted', time=None):
        if time is None:
            time = datetime.now()
        return obj.actor_actions.filter(verb=verb, timestamp__lte=time)