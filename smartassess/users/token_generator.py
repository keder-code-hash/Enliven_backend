import jwt,datetime
from django.conf import settings

def get_access_token(user):
    payload={
            'email':user.email,
            'username':user.user_name,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=3)
        }
    access_token=jwt.encode(payload,settings.SECRET_KEY,algorithm='HS256')
    return access_token
def get_refresh_token(user):
    payload={
            'email':user.email,
            'username':user.user_name,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=2)
        }
    refresh_token=jwt.encode(payload,settings.SECRET_KEY,algorithm='HS256')
    return refresh_token