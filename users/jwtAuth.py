# from jwt.exceptions import ExpiredSignatureError
from rest_framework.views import APIView
from .models import Register
from rest_framework import authentication, status
# from django.middleware.csrf import CsrfViewMiddleware
import jwt
from rest_framework import exceptions
from django.conf import settings
from users.token_generator import get_access_token
from django.http import HttpResponse


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header=authentication.get_authorization_header(request)
        auth_data=auth_header.decode('utf-8')
        auth_token=auth_data.split(" ")

        if len(auth_token)!=2:
            raise exceptions.AuthenticationFailed("authentication falied.")
        token=auth_token[1]
        try:
            payload=jwt.decode(token,settings.SECRET_KEY,algorithms="HS256")
            email=payload['email']
            user=Register.objects.get(email=email) 

        except jwt.ExpiredSignatureError as ex:
            raise exceptions.AuthenticationFailed('signature expired')

        except jwt.DecodeError as er:
            raise exceptions.AuthenticationFailed('token is invalid.')
        except Register.DoesNotExist as ne:
            raise exceptions.AuthenticationFailed('invalid email id')
        return (user,None)


def refresh_acsess_token(request):
    refresh_token=request.COOKIES.get('refreshtoken')
    if refresh_token is None:
        raise exceptions.AuthenticationFailed("No token available")
    try:
        payload=jwt.decode(refresh_token,settings.SECRET_KEY,algorithms='HS256')
        email=payload['email']
        user=Register.objects.get(email=email)
        access_token=get_access_token(user)
    except jwt.ExpiredSignatureError as e:
        raise exceptions.AuthenticationFailed("Signature of refresh Token is Expired")
    except jwt.DecodeError as er:
        raise exceptions.AuthenticationFailed("Invalid Token")
    except Register.DoesNotExist as db_err:
        raise exceptions.AuthenticationFailed("Invalid data")
    finally:
        return HttpResponse (access_token,status.HTTP_200_OK)