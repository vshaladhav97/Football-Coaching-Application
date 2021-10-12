from django.contrib.auth import authenticate
from customer.models import User
import os
from django.conf import settings
import random
from rest_framework.exceptions import AuthenticationFailed


def generate_username(name):

    username = "".join(name.split(' ')).lower()
    if not User.objects.filter(username=username).exists():
        return username
    else:
        random_username = username + str(random.randint(0, 1000))
        return generate_username(random_username)


def register_social_user(provider, user_id, email, name):
    filtered_user_by_email = User.objects.filter(email=email)

    if filtered_user_by_email.exists():
     

        if provider == filtered_user_by_email[0].auth_provider:

            registered_user = authenticate(
                email=email, password=settings.GOOGLE_CLIENT_SECRET)

          
            return {
                'username': registered_user.first_name,
                'email': registered_user.email,
                'tokens': registered_user.tokens()}

        else:
            raise AuthenticationFailed(
                detail='Please continue your login using ' + filtered_user_by_email[0].auth_provider)

    else:
  
        user = {
            'first_name': name, 'email': email,
            'password': settings.GOOGLE_CLIENT_SECRET}
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.auth_provider = provider
        user.save()

        new_user = authenticate(
            email=email, password=settings.GOOGLE_CLIENT_SECRET)
        return {
            'email': email,
            'username': new_user.first_name,
            'tokens': new_user.tokens()
        }