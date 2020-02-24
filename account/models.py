from django.db import models
from django.contrib.auth.models import ( AbstractUser, BaseUserManager)
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime, timedelta
import jwt
from rest_framework.authtoken.models import Token
from utils.models import BaseAbstractModel
from utils.managers import CustomQuerySet


class UserManager(BaseUserManager):
    '''
    We need to override the `create_user` method so that users can
    only be created when all non-nullable fields are populated.
    '''

    def create_user(
            self,
            first_name = None,
            last_name = None,
            email = None,
            password = None,
            role = 'CA'
    ):
        '''
        Create and return a `User` with an email, first name, last name and
        password.
        '''

        if not first_name:
            raise TypeError('Hello, Kindly provide us with your First Name.')

        if not last_name:
            raise TypeError('Hello, Kindly provide us with your Last Name.')

        if not email:
            raise TypeError('Hello, Kindly provide us with your Email Address.')

        if not password:
            raise TypeError('Hello, Kindly provide us with a Password to Secure your account')

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            username = self.normalize_email(email))

        user.set_password(password)
        user.role = role
        user.save()
        return user

    def create_superuser(
            self,
            first_name = None,
            last_name = None,
            email = None,
            password = None
            ):

        '''Create a `User` who is also a superuser'''
        if not first_name:
            raise TypeError('Hello, Kindly provide us with your First Name.')

        if not last_name:
            raise TypeError('Hello, Kindly provide us with your Last Name.')

        if not email:
            raise TypeError('Hello, Kindly provide us with your Email Address.')

        if not password:
            raise TypeError('Hello, Kindly provide us with a Password to Secure your account')

        user = self.model(
            first_name = first_name,
            last_name = last_name,
            email = self.normalize_email(email),
            role='FA')

        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.is_verified = True
        user.set_password(password)
        user.save()


class User(AbstractUser, BaseAbstractModel):
    """This class defines the User model"""

    USER_ROLES = (
        ('FA', 'FUSION ADMINISTRATOR'),
        ('CA', 'CLIENT ADMINISTRATOR')
    )

    username = models.CharField(
        null = True,
        blank = True,
        max_length = 100,
        unique = True)
    email = models.EmailField(unique = True)
    role = models.CharField(
        verbose_name = 'user role',
        max_length = 2,
        choices = USER_ROLES,
        default='CA'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()
    active_objects = CustomQuerySet.as_manager()

    def __str__(self):
        return f'{self.email}'

    @property
    def get_email(self):
        '''
        This method is required by Django for things like handling emails.
        Typically, this would be the user's first and last name. Since we do
        not store the user's real name, we return their emails instead.
        '''
        return self.email

    @property
    def token(self):
        '''
        We need to make the method for creating our token private. At the
        same time, it's more convenient for us to access our token with
        `user.token` and so we make the token a dynamic property by wrapping
        in in the `@property` decorator.
        '''
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        '''
        We generate JWT token and add the user id, username and expiration
        as an integer.
        '''
        token_expiry = datetime.now() + timedelta(hours=24)
        token = jwt.encode({
            'id': self.pk,
            'email': self.get_email,
            'exp': token_expiry.utcfromtimestamp(token_expiry.timestamp())
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

class PasswordResetToken(models.Model):
    '''This class creates a Password Reset Token model.'''

    token = models.CharField(max_length = 400)
    created = models.DateTimeField(auto_now = True)
    is_valid = models.BooleanField(default = True)

class BlackList(BaseAbstractModel):
    """
    This class defines black list model.
    Tokens of logged out users are stored here.
    """

    token = models.CharField(max_length=200, unique=True)

    @staticmethod
    def delete_tokens_older_than_a_day():
        """
        This method deletes tokens older than one day
        """
        past_24 = datetime.now() - timedelta(hours=24)

        BlackList(created_at__lt=past_24).delete()
