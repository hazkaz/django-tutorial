from rest_framework.authentication import TokenAuthentication

class custom_auth(TokenAuthentication):
    keyword = 'khuljasimsim'